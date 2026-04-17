#!/bin/bash
# Test harness for learning-cycle.sh + learning-cycle-monitor.sh
# Exercises: first-run baselines, idempotent re-run, flock concurrency,
# log rotation trigger, monitor healthy/stale/dedup paths.
# Asserts DB state after each phase. Exits non-zero on any failure.
#
# Run manually: bash /opt/pipeline/scripts/test-learning-cycle.sh
# Cleans up its test data after itself.

set -uo pipefail

PIPELINE=/opt/pipeline
DB="$PIPELINE/data/pipeline.db"
SCRIPT="$PIPELINE/scripts/learning-cycle.sh"
MONITOR="$PIPELINE/scripts/learning-cycle-monitor.sh"
HEALTH="$PIPELINE/scripts/health-check.sh"
SYNC="$PIPELINE/scripts/sync-memory-to-sqlite.sh"
CACHE="$PIPELINE/data/learning-cycle-cache"
OUT="$PIPELINE/output/research/daily"
LOG="$PIPELINE/data/learning-cycle.log"
STATE_FILE="$PIPELINE/data/learning-cycle-monitor.state"
HEALTH_STATE="$PIPELINE/data/health-check-state.json"

pass_count=0
fail_count=0

assert_eq() {
    local label="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        echo "  PASS: $label (= $actual)"
        pass_count=$((pass_count + 1))
    else
        echo "  FAIL: $label — expected '$expected', got '$actual'"
        fail_count=$((fail_count + 1))
    fi
}

assert_ge() {
    local label="$1" minimum="$2" actual="$3"
    if [ "$actual" -ge "$minimum" ] 2>/dev/null; then
        echo "  PASS: $label ($actual >= $minimum)"
        pass_count=$((pass_count + 1))
    else
        echo "  FAIL: $label — expected >= $minimum, got $actual"
        fail_count=$((fail_count + 1))
    fi
}

reset_state() {
    rm -rf "$CACHE"
    rm -f "$OUT/$(date -u +%Y-%m-%d).md"
    rm -f "$STATE_FILE"
    /usr/bin/sqlite3 "$DB" "DELETE FROM learned_preferences WHERE category LIKE 'learning-cycle%';"
}

db_count() {
    /usr/bin/sqlite3 "$DB" "SELECT COUNT(*) FROM learned_preferences WHERE category='$1';"
}

echo "========================================"
echo "Learning cycle test harness"
echo "========================================"

# ---- Phase 1: first run = baselines, no strong findings ----
echo ""
echo "[Phase 1] First run — expect baselines, zero strong findings"
reset_state
bash "$SCRIPT" > /dev/null
assert_eq "heartbeat count after run 1" "1" "$(db_count learning-cycle-heartbeat)"
assert_eq "strong-findings count after run 1" "0" "$(db_count learning-cycle-strong)"

# ---- Phase 2: back-to-back runs must remain idempotent ----
echo ""
echo "[Phase 2] Idempotency — 3 more runs, strong count must stay 0"
for i in 1 2 3; do
    bash "$SCRIPT" > /dev/null
done
assert_eq "heartbeat count after 4 total runs" "4" "$(db_count learning-cycle-heartbeat)"
assert_eq "strong-findings still 0" "0" "$(db_count learning-cycle-strong)"

# ---- Phase 3: flock prevents parallel stomp ----
echo ""
echo "[Phase 3] Concurrency — fire 2 in parallel, only 1 heartbeat added"
hb_before=$(db_count learning-cycle-heartbeat)
bash "$SCRIPT" > /dev/null &
p1=$!
bash "$SCRIPT" > /dev/null &
p2=$!
wait $p1 $p2
hb_after=$(db_count learning-cycle-heartbeat)
added=$(( hb_after - hb_before ))
assert_eq "only 1 heartbeat added after parallel run" "1" "$added"

# ---- Phase 4: cron-env simulation (stripped PATH) ----
echo ""
echo "[Phase 4] Cron env — stripped PATH + HOME must succeed"
hb_before=$(db_count learning-cycle-heartbeat)
env -i PATH=/usr/bin:/bin HOME=/home/farouq bash "$SCRIPT"
cron_exit=$?
hb_after=$(db_count learning-cycle-heartbeat)
assert_eq "cron-env exit code" "0" "$cron_exit"
assert_eq "heartbeat added in cron env" "1" "$(( hb_after - hb_before ))"

# ---- Phase 5: log rotation trigger ----
echo ""
echo "[Phase 5] Log rotation — force log >10MB, next run should rotate"
# Synthesize >10MB log
/usr/bin/dd if=/dev/zero bs=1M count=11 2>/dev/null | /usr/bin/tr '\0' 'x' >> "$LOG"
size_before=$(stat -c %s "$LOG")
bash "$SCRIPT" > /dev/null
size_after=$(stat -c %s "$LOG")
rotated=$([ -f "${LOG}.old" ] && echo 1 || echo 0)
assert_eq "log rotated" "1" "$rotated"
# After rotation, new log should be small (just this run's output)
if [ "$size_after" -lt "$size_before" ]; then
    echo "  PASS: log shrunk after rotation ($size_before → $size_after bytes)"
    pass_count=$((pass_count + 1))
else
    echo "  FAIL: log did not shrink ($size_before → $size_after)"
    fail_count=$((fail_count + 1))
fi
rm -f "${LOG}.old"

# ---- Phase 6: monitor — healthy path ----
echo ""
echo "[Phase 6] Monitor — healthy heartbeat, no alert"
bash "$MONITOR"
mon_exit=$?
assert_eq "monitor exit 0 on healthy" "0" "$mon_exit"
assert_eq "no state file written on healthy" "0" "$([ -f "$STATE_FILE" ] && echo 1 || echo 0)"

# ---- Phase 7: monitor — stale path (without pinging Farouq) ----
echo ""
echo "[Phase 7] Monitor — stale heartbeat, token missing, must exit 1 gracefully"
# Force heartbeats old
/usr/bin/sqlite3 "$DB" "UPDATE learned_preferences SET updated_at='2026-04-15T00:00:00Z' WHERE category='learning-cycle-heartbeat';"
# Run with HOME pointing elsewhere so env file is missing
HOME=/tmp/nonexistent bash "$MONITOR"
mon_exit=$?
assert_eq "monitor exit 1 on stale+no-env" "1" "$mon_exit"

# ---- Phase 8: monitor — alert dedup ----
echo ""
echo "[Phase 8] Monitor — alert dedup via state file"
# Simulate an alert was sent 1h ago
echo "$(( $(date +%s) - 3600 ))" > "$STATE_FILE"
# Heartbeats still stale from phase 7
HOME=/tmp/nonexistent bash "$MONITOR"
mon_exit=$?
assert_eq "monitor exit 0 when alert was recent" "0" "$mon_exit"

# ---- Phase 9: health-check under healthy system ----
echo ""
echo "[Phase 9] Health-check — all 6 checks must pass"
rm -f "$HEALTH_STATE"
bash "$SCRIPT" > /dev/null   # fresh heartbeat for health check
health_exit=$(bash "$HEALTH" > /tmp/health-out.txt 2>&1; echo $?)
assert_eq "health-check exit 0 on healthy" "0" "$health_exit"
# Verify state file NOT written (no alerts fired)
assert_eq "no state file written on healthy" "0" "$([ -f "$HEALTH_STATE" ] && echo 1 || echo 0)"

# ---- Phase 10: health-check detects missing heartbeats ----
echo ""
echo "[Phase 10] Health-check — no heartbeats path (tries to alert, no-env graceful fail)"
/usr/bin/sqlite3 "$DB" "DELETE FROM learned_preferences WHERE category='learning-cycle-heartbeat';"
rm -f "$HEALTH_STATE"
# HOME=nonexistent → no Telegram env → graceful exit 2
HOME=/tmp/nonexistent bash "$HEALTH" > /tmp/health-out.txt 2>&1
h_exit=$?
assert_eq "health-check exit 2 on no-token" "2" "$h_exit"
# Log should contain the failure details
if grep -q "No learning-cycle heartbeats" "$LOG"; then
    echo "  PASS: heartbeat-missing failure logged"
    pass_count=$((pass_count + 1))
else
    echo "  FAIL: heartbeat-missing failure not in log"
    fail_count=$((fail_count + 1))
fi

# ---- Phase 11: health-check drift detection ----
echo ""
echo "[Phase 11] Health-check — memory-DB drift detection"
# Delete all memory rows to force drift. Keep real MEM_DIR so check runs,
# but point TG_ENV at non-existent file so no real alert fires.
/usr/bin/sqlite3 "$DB" "DELETE FROM learned_preferences WHERE category LIKE 'memory-%';"
rm -f "$HEALTH_STATE"
TG_ENV=/tmp/nonexistent-tg.env bash "$HEALTH" > /tmp/health-out.txt 2>&1
if grep -q "Memory-SQLite drift" "$LOG"; then
    echo "  PASS: drift detected"
    pass_count=$((pass_count + 1))
else
    echo "  FAIL: drift not detected"
    fail_count=$((fail_count + 1))
fi

# ---- Cleanup: reset state, then seed a fresh heartbeat + re-sync memory
#              so health-check won't alert "no heartbeats" / "drift" after tests ----
reset_state
rm -f "$STATE_FILE" "$HEALTH_STATE" /tmp/health-out.txt
bash "$SCRIPT" > /dev/null   # fresh heartbeat
bash "$SYNC" > /dev/null     # re-sync memory rows

echo ""
echo "========================================"
echo "Results: $pass_count passed, $fail_count failed"
echo "========================================"
[ "$fail_count" -eq 0 ]
