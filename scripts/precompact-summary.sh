#!/bin/bash
# PreCompact hook: writes a session-pickup summary to disk before context compaction.
# Goal: the next session (which starts with cleared context) can resume work intelligently.
# Triggered by Claude Code's PreCompact event. Receives JSON on stdin with session_id + trigger.

set -u
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)
TRIGGER=$(echo "$INPUT" | jq -r '.trigger // "unknown"' 2>/dev/null)

OUT=/opt/pipeline/data/last-session-summary.md
DB=/opt/pipeline/data/pipeline.db
JSONL=/home/farouq/.claude/projects/-opt-pipeline/${SESSION_ID}.jsonl
TS=$(date '+%Y-%m-%d %H:%M:%S %Z')

# Always emit something readable, even on partial failure.
{
  echo "# Last session summary"
  echo
  echo "_Saved at ${TS} by PreCompact hook (trigger: ${TRIGGER}, session: ${SESSION_ID:-unknown})._"
  echo
  echo "## Recent user messages"
  if [ -n "$SESSION_ID" ] && [ -f "$JSONL" ]; then
    jq -rR 'fromjson? | select(.type=="user")
            | .message.content
            | if type=="array" then
                .[] | select(.type=="text" or (has("type")|not)) | (.text // .)
              else . end
            | select(type=="string" and length>0 and (startswith("<")|not))' "$JSONL" 2>/dev/null \
      | tail -n 8 | sed 's/^/- /' || echo "- (parse failed)"
  else
    echo "- (transcript not found at $JSONL)"
  fi
  echo
  echo "## Recent assistant tool calls (last 15)"
  if [ -n "$SESSION_ID" ] && [ -f "$JSONL" ]; then
    jq -rR 'fromjson? | select(.type=="assistant")
            | .message.content[]?
            | select(.type=="tool_use") | .name' "$JSONL" 2>/dev/null \
      | tail -n 15 | sed 's/^/- /' || echo "- (parse failed)"
  fi
  echo
  echo "## Active briefs (SQLite)"
  if [ -f "$DB" ]; then
    sqlite3 "$DB" "SELECT '- brief #' || id || ' [' || status || '] step=' || COALESCE(current_step,'-') || ' updated=' || datetime(updated_at,'localtime') FROM briefs WHERE status NOT IN ('rejected','delivered','approved') ORDER BY updated_at DESC LIMIT 5;" 2>/dev/null \
      || echo "- (sqlite query failed)"
    echo
    echo "## Last 5 generations"
    sqlite3 "$DB" "SELECT '- gen #' || id || ' brief=' || COALESCE(brief_id,'-') || ' shot=' || COALESCE(shot_number,'-') || ' model=' || COALESCE(model,'-') || ' result=' || COALESCE(pass_fail,'?') || ' at=' || datetime(created_at,'localtime') FROM generation_history ORDER BY created_at DESC LIMIT 5;" 2>/dev/null
    echo
    echo "## Last feedback entry"
    sqlite3 "$DB" "SELECT '- video=' || COALESCE(video_id,'-') || ' sentiment=' || COALESCE(sentiment,'-') || ' at=' || datetime(created_at,'localtime') || char(10) || '  feedback: ' || substr(COALESCE(owner_feedback,''),1,200) FROM feedback_log ORDER BY created_at DESC LIMIT 1;" 2>/dev/null
  fi
  echo
  echo "## Recent git activity"
  echo "- Branch: $(git -C /opt/pipeline rev-parse --abbrev-ref HEAD 2>/dev/null)"
  echo "- Last 5 commits:"
  git -C /opt/pipeline log --oneline -5 2>/dev/null | sed 's/^/  - /'
  echo "- Working-tree changes (status):"
  git -C /opt/pipeline status --porcelain 2>/dev/null | head -20 | sed 's/^/  /'
  echo
  echo "## Files modified in last 2 hours"
  find /opt/pipeline -type f -mmin -120 \
    -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/venv/*' \
    -not -path '*/data/*' -not -path '*.log' 2>/dev/null \
    | head -20 | sed 's/^/- /'
  echo
  echo "## Cost log (last 5 lines, if present)"
  if [ -f /opt/pipeline/data/cost_log.txt ]; then
    tail -5 /opt/pipeline/data/cost_log.txt | sed 's/^/    /'
  else
    echo "- (no cost log file)"
  fi
} > "$OUT" 2>/dev/null

# Tell the user the snapshot was saved (visible in UI).
SIZE=$(wc -c < "$OUT" 2>/dev/null || echo 0)
echo "{\"systemMessage\":\"PreCompact: session summary saved to ${OUT} (${SIZE} bytes). Next session will load it via SessionStart hook.\"}"
exit 0
