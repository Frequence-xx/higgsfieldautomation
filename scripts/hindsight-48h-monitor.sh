#!/bin/bash
# Hindsight 48-hour stability monitor
# Logs health checks to a file. Does NOT restart — only alerts.
# Run via: nohup /opt/pipeline/scripts/hindsight-48h-monitor.sh &

LOG="/opt/pipeline/data/hindsight-monitor.log"
ALERT_SENT=0

echo "$(date) — Hindsight 48h monitor started" >> "$LOG"

for i in $(seq 1 2880); do  # 2880 × 60s = 48 hours
    sleep 60

    HPID=$(pgrep -f "hindsight_api" | head -1)

    if [ -z "$HPID" ]; then
        echo "$(date) — ALERT: Hindsight daemon NOT running" >> "$LOG"
        # Don't auto-restart — log and alert only
        continue
    fi

    CPU=$(ps -p $HPID -o pcpu= 2>/dev/null | tr -d ' ')
    MEM=$(ps -p $HPID -o pmem= 2>/dev/null | tr -d ' ')
    RSS_KB=$(ps -p $HPID -o rss= 2>/dev/null | tr -d ' ')
    RSS_MB=$((RSS_KB / 1024))

    CPU_INT=${CPU%.*}
    MEM_INT=${MEM%.*}

    # Log every 10 minutes
    if [ $((i % 10)) -eq 0 ]; then
        echo "$(date) — OK: PID=$HPID CPU=${CPU}% MEM=${MEM}% RSS=${RSS_MB}MB" >> "$LOG"
    fi

    # Alert on high CPU (sustained >50%)
    if [ "${CPU_INT:-0}" -gt 50 ]; then
        echo "$(date) — WARNING: CPU ${CPU}% exceeds 50% cap. PID=$HPID" >> "$LOG"
    fi

    # Alert on high RAM (>30%)
    if [ "${MEM_INT:-0}" -gt 30 ]; then
        echo "$(date) — WARNING: RAM ${MEM}% exceeds 30% cap. PID=$HPID" >> "$LOG"
    fi

    # Kill on extreme (>80% CPU or >50% RAM sustained)
    if [ "${CPU_INT:-0}" -gt 80 ] || [ "${MEM_INT:-0}" -gt 50 ]; then
        echo "$(date) — CRITICAL: Killing Hindsight. CPU=${CPU}% MEM=${MEM}%" >> "$LOG"
        kill $HPID 2>/dev/null
    fi
done

echo "$(date) — 48h monitor completed" >> "$LOG"
