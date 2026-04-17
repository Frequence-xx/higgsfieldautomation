#!/bin/bash
# Pipeline health-check — runs every 15 min via cron.
# Runs a suite of checks; aggregates failures; sends ONE Telegram alert per
# run containing all new/re-alertable failures. Per-check dedup windows.
#
# Checks:
#   [A] cron service running (systemctl is-active cron)
#   [B] disk space on / > 2GB free
#   [C] SQLite DB integrity (PRAGMA integrity_check returns 'ok')
#   [D] learning-cycle heartbeat fresher than 12h
#   [E] learning-cycle.log modified within 24h (cycle writing at all)
#   [F] memory-file-count matches memory-* SQLite row-count (drift check)
#
# State:
#   /opt/pipeline/data/health-check-state.json — per-check last-alert epoch
#
# Exits 0 on success OR on partial failures that were deduped. Exit 2 on
# config error (no Telegram env). Exits 1 only if the run itself aborted.

set -uo pipefail

CURL=/usr/bin/curl
SQLITE=/usr/bin/sqlite3
PY=/usr/bin/python3

PIPELINE=/opt/pipeline
DB="$PIPELINE/data/pipeline.db"
LOG="$PIPELINE/data/learning-cycle.log"
# MEM_DIR and TG_ENV default to HOME-relative but can be overridden for testing
MEM_DIR="${MEM_DIR:-$HOME/.claude/projects/-opt-pipeline/memory}"
TG_ENV="${TG_ENV:-$HOME/.claude/channels/telegram/.env}"
CHAT_ID="1677012496"
STATE="$PIPELINE/data/health-check-state.json"

# Per-check dedup windows (seconds)
DEDUP_CRON=3600        # 1h — critical, want frequent retry
DEDUP_DISK=21600       # 6h — disk fills slowly
DEDUP_DB=3600          # 1h — critical
DEDUP_HEARTBEAT=21600  # 6h
DEDUP_LOG_STALE=21600  # 6h
DEDUP_DRIFT=21600      # 6h

# Thresholds
HEARTBEAT_STALE_SEC=43200     # 12h
LOG_STALE_SEC=86400           # 24h
DISK_MIN_FREE_KB=$((2 * 1024 * 1024))  # 2GB
DRIFT_TOLERANCE=2             # allow ±2 row difference

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
now=$(date +%s)

log_line() { echo "[$TS] [health-check] $*" >> "$LOG"; }

# State file: {"cron": epoch, "disk": epoch, ...}
state_get() {
    local key="$1"
    $PY -c "
import json, sys
try:
    with open('$STATE') as f: s = json.load(f)
    print(s.get('$key', 0))
except Exception: print(0)
" 2>/dev/null || echo 0
}

state_set() {
    local key="$1" val="$2"
    $PY -c "
import json, os
s = {}
if os.path.exists('$STATE'):
    try:
        with open('$STATE') as f: s = json.load(f)
    except Exception: pass
s['$key'] = $val
with open('$STATE', 'w') as f: json.dump(s, f)
" 2>/dev/null
}

# failures[] collects human-readable lines; failure_keys[] has the dedup keys
declare -a failures=()
declare -a failure_keys=()

record_fail() {
    local key="$1" dedup="$2" msg="$3"
    local last_alert
    last_alert=$(state_get "$key")
    case "$last_alert" in ''|*[!0-9]*) last_alert=0;; esac
    local since=$(( now - last_alert ))
    if [ "$since" -ge "$dedup" ]; then
        failures+=("$msg")
        failure_keys+=("$key")
    else
        log_line "SUPPRESSED [$key]: $msg (last alert ${since}s ago)"
    fi
}

# === CHECK A: cron service running ===
if ! systemctl is-active --quiet cron 2>/dev/null; then
    record_fail "cron" "$DEDUP_CRON" "A. cron service DOWN — all scheduled work stopped"
fi

# === CHECK B: disk free ===
free_kb=$(df --output=avail / 2>/dev/null | tail -1 | tr -d ' ' || echo 0)
case "$free_kb" in ''|*[!0-9]*) free_kb=0;; esac
if [ "$free_kb" -lt "$DISK_MIN_FREE_KB" ]; then
    free_gb=$(( free_kb / 1024 / 1024 ))
    record_fail "disk" "$DEDUP_DISK" "B. Disk on / only ${free_gb}GB free (threshold 2GB)"
fi

# === CHECK C: SQLite integrity ===
integrity=$($SQLITE "$DB" -cmd ".timeout 5000" "PRAGMA integrity_check;" 2>/dev/null | head -1 || echo "FAIL")
if [ "$integrity" != "ok" ]; then
    record_fail "db" "$DEDUP_DB" "C. SQLite integrity_check returned: $integrity"
fi

# === CHECK D: heartbeat freshness ===
last_hb=$($SQLITE "$DB" -cmd ".timeout 5000" \
    "SELECT updated_at FROM learned_preferences WHERE category='learning-cycle-heartbeat' ORDER BY id DESC LIMIT 1;" \
    2>/dev/null || echo "")
if [ -z "$last_hb" ]; then
    # Only alert if the DB is otherwise healthy — avoid double-alert with check C
    if [ "$integrity" = "ok" ]; then
        record_fail "heartbeat" "$DEDUP_HEARTBEAT" "D. No learning-cycle heartbeats in DB — cycle never ran"
    fi
else
    hb_epoch=$(date -u -d "$last_hb" +%s 2>/dev/null || echo 0)
    hb_age=$(( now - hb_epoch ))
    if [ "$hb_age" -gt "$HEARTBEAT_STALE_SEC" ]; then
        hb_hours=$(( hb_age / 3600 ))
        record_fail "heartbeat" "$DEDUP_HEARTBEAT" "D. Last heartbeat ${hb_hours}h ago ($last_hb) — cycle stopped"
    fi
fi

# === CHECK E: learning-cycle.log freshness ===
if [ -f "$LOG" ]; then
    log_epoch=$(stat -c %Y "$LOG" 2>/dev/null || echo 0)
    log_age=$(( now - log_epoch ))
    if [ "$log_age" -gt "$LOG_STALE_SEC" ]; then
        log_hours=$(( log_age / 3600 ))
        record_fail "log_stale" "$DEDUP_LOG_STALE" "E. Log not written for ${log_hours}h — pipeline silent"
    fi
else
    record_fail "log_stale" "$DEDUP_LOG_STALE" "E. Log file missing: $LOG"
fi

# === CHECK F: memory → SQLite drift ===
if [ -d "$MEM_DIR" ]; then
    mem_count=$(ls "$MEM_DIR"/*.md 2>/dev/null | grep -v MEMORY.md | wc -l)
    db_count=$($SQLITE "$DB" -cmd ".timeout 5000" \
        "SELECT COUNT(*) FROM learned_preferences WHERE category LIKE 'memory-%';" \
        2>/dev/null || echo 0)
    drift=$(( mem_count - db_count ))
    abs_drift=${drift#-}
    if [ "$abs_drift" -gt "$DRIFT_TOLERANCE" ]; then
        record_fail "drift" "$DEDUP_DRIFT" "F. Memory-SQLite drift: $mem_count files vs $db_count DB rows (Δ$drift). Run sync-memory-to-sqlite.sh"
    fi
fi

# === Report results ===
check_count=6
ok_count=$(( check_count - ${#failures[@]} ))

if [ "${#failures[@]}" -eq 0 ]; then
    log_line "all $check_count checks OK"
    # Dead-man's-switch ping — signals healthchecks.io we're alive.
    # If this cron dies, healthchecks.io alerts Farouq externally.
    # Ping URL is read from /opt/pipeline/.env (HEALTHCHECKS_URL=...).
    if [ -f "$PIPELINE/.env" ]; then
        hc_url=$(grep -E '^HEALTHCHECKS_URL=' "$PIPELINE/.env" 2>/dev/null | cut -d= -f2- | tr -d '"' | tr -d "'")
        if [ -n "$hc_url" ]; then
            $CURL -fsS -m 10 -o /dev/null "$hc_url" 2>/dev/null \
                && log_line "dead-man ping sent" \
                || log_line "dead-man ping FAILED (hc down or url wrong)"
        fi
    fi
    exit 0
fi

# --- If there ARE failures, send a /fail variant to healthchecks so they
# --- alert externally too (backup channel if Telegram is broken) ---
if [ -f "$PIPELINE/.env" ]; then
    hc_url=$(grep -E '^HEALTHCHECKS_URL=' "$PIPELINE/.env" 2>/dev/null | cut -d= -f2- | tr -d '"' | tr -d "'")
    if [ -n "$hc_url" ]; then
        $CURL -fsS -m 10 -o /dev/null "${hc_url}/fail" 2>/dev/null \
            && log_line "dead-man /fail ping sent" \
            || log_line "dead-man /fail ping FAILED"
    fi
fi

# Build alert message
{
    echo "⚠️ Pipeline health-check FAIL ($ok_count/$check_count OK)"
    echo ""
    for msg in "${failures[@]}"; do
        echo "$msg"
    done
    echo ""
    echo "Time: $TS"
    echo "Log:  $LOG"
} > /tmp/health-alert.txt
alert_body=$(cat /tmp/health-alert.txt)

# Try to send via Telegram
if [ -f "$TG_ENV" ]; then
    TELEGRAM_BOT_TOKEN=$(grep -E '^TELEGRAM_BOT_TOKEN=' "$TG_ENV" | cut -d= -f2-)
else
    TELEGRAM_BOT_TOKEN=""
fi

if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    response=$($CURL -fsSL -m 10 \
        --data-urlencode "chat_id=${CHAT_ID}" \
        --data-urlencode "text=${alert_body}" \
        "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" 2>&1 || echo "CURL_FAIL")
    if echo "$response" | grep -q '"ok":true'; then
        # Mark all failure keys as alerted
        for k in "${failure_keys[@]}"; do
            state_set "$k" "$now"
        done
        log_line "ALERT sent — ${#failures[@]} failures"
        exit 0
    else
        log_line "ALERT send FAILED — response: ${response:0:200}"
        # Still record what failed so we don't lose visibility
        for f in "${failures[@]}"; do log_line "FAIL: $f"; done
        exit 1
    fi
else
    log_line "cannot alert (no Telegram token) — failures were:"
    for f in "${failures[@]}"; do log_line "FAIL: $f"; done
    exit 2
fi
