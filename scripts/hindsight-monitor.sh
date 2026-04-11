#!/bin/bash
# Hindsight resource monitor
# Checks CPU/RAM every 60 seconds, kills if exceeds caps

HINDSIGHT_PID=$(pgrep -f "hindsight_api" | head -1)

if [ -z "$HINDSIGHT_PID" ]; then
    echo '{"systemMessage": "Hindsight daemon is NOT running. Memory retrieval unavailable."}'
    exit 0
fi

CPU=$(ps -p $HINDSIGHT_PID -o pcpu= 2>/dev/null | tr -d ' ')
MEM=$(ps -p $HINDSIGHT_PID -o pmem= 2>/dev/null | tr -d ' ')
RSS_KB=$(ps -p $HINDSIGHT_PID -o rss= 2>/dev/null | tr -d ' ')
RSS_MB=$((RSS_KB / 1024))

# Hard caps: 50% CPU sustained, 30% RAM
CPU_INT=${CPU%.*}
MEM_INT=${MEM%.*}

if [ "${CPU_INT:-0}" -gt 50 ]; then
    kill $HINDSIGHT_PID 2>/dev/null
    echo "{\"systemMessage\": \"HINDSIGHT KILLED: CPU ${CPU}% exceeded 50% cap. PID $HINDSIGHT_PID terminated. Restart manually after investigation.\"}"
    exit 0
fi

if [ "${MEM_INT:-0}" -gt 30 ]; then
    kill $HINDSIGHT_PID 2>/dev/null
    echo "{\"systemMessage\": \"HINDSIGHT KILLED: RAM ${MEM}% exceeded 30% cap. PID $HINDSIGHT_PID terminated. Restart manually after investigation.\"}"
    exit 0
fi

# Normal status — suppress output to avoid noise
exit 0
