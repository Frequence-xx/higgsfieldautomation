#!/bin/bash
# Staleness monitor — runs hourly via cron.
# Alerts Farouq on Telegram if no learning-cycle heartbeat for >12h
# (learning cycle runs every 6h, so threshold = 2+ missed cycles).
# Deduplicates: suppresses repeat alerts for 6h after first send.

set -uo pipefail

CURL=/usr/bin/curl
SQLITE=/usr/bin/sqlite3

PIPELINE=/opt/pipeline
DB="$PIPELINE/data/pipeline.db"
TG_ENV="$HOME/.claude/channels/telegram/.env"
CHAT_ID="1677012496"
STALE_THRESHOLD_SEC=43200    # 12h
ALERT_DEDUPE_SEC=21600        # 6h (don't re-alert within this window)
STATE_FILE="$PIPELINE/data/learning-cycle-monitor.state"
LOG="$PIPELINE/data/learning-cycle.log"

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [monitor] $*" >> "$LOG"; }

# --- Find most recent heartbeat timestamp (ISO 8601) ---
last_hb=$($SQLITE "$DB" -cmd ".timeout 5000" "SELECT updated_at FROM learned_preferences WHERE category='learning-cycle-heartbeat' ORDER BY id DESC LIMIT 1;" 2>/dev/null || echo "")

if [ -z "$last_hb" ]; then
    log "no heartbeats found — cycle has never run (or db wiped)"
    exit 0
fi

# Convert ISO timestamp to epoch seconds
last_hb_epoch=$(date -u -d "$last_hb" +%s 2>/dev/null || echo 0)
now=$(date -u +%s)
age=$(( now - last_hb_epoch ))

if [ "$age" -lt "$STALE_THRESHOLD_SEC" ]; then
    log "heartbeat ${age}s old — healthy"
    exit 0
fi

# --- Stale. Check if we already alerted recently ---
last_alert_epoch=$(cat "$STATE_FILE" 2>/dev/null || echo 0)
# guard: if state file has garbage (non-numeric), treat as 0
case "$last_alert_epoch" in ''|*[!0-9]*) last_alert_epoch=0;; esac
since_alert=$(( now - last_alert_epoch ))

if [ "$since_alert" -lt "$ALERT_DEDUPE_SEC" ]; then
    log "STALE (${age}s) but suppressed — alerted ${since_alert}s ago"
    exit 0
fi

# --- Send alert ---
if [ ! -f "$TG_ENV" ]; then
    log "STALE but cannot alert — $TG_ENV missing"
    exit 1
fi

TELEGRAM_BOT_TOKEN=$(grep -E '^TELEGRAM_BOT_TOKEN=' "$TG_ENV" | cut -d= -f2-)
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    log "STALE but cannot alert — token empty in $TG_ENV"
    exit 1
fi

age_hours=$(( age / 3600 ))
msg="⚠️ Learning cycle STALE — last heartbeat ${age_hours}h ago ($last_hb). Cron may be stopped. Check: systemctl status cron && tail /opt/pipeline/data/learning-cycle.log"

response=$($CURL -fsSL -m 10 \
    -d "chat_id=${CHAT_ID}" \
    -d "text=${msg}" \
    "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" 2>&1 || echo "CURL_FAIL")

if echo "$response" | grep -q '"ok":true'; then
    echo "$now" > "$STATE_FILE"
    log "ALERT sent — learning cycle stale for ${age_hours}h"
else
    log "ALERT send FAILED — response: ${response:0:200}"
    exit 1
fi
