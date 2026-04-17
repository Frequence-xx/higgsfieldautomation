#!/bin/bash
# SessionStart hook: surfaces the previous session's summary to the new context.
# Pairs with precompact-summary.sh — together they preserve continuity across compactions / new sessions.

SUMMARY=/opt/pipeline/data/last-session-summary.md

if [ ! -f "$SUMMARY" ]; then
  exit 0
fi

# Stale guard: if older than 7 days, skip — likely irrelevant.
if [ $(find "$SUMMARY" -mtime +7 2>/dev/null | wc -l) -gt 0 ]; then
  exit 0
fi

CONTENT=$(cat "$SUMMARY")
# Emit as additionalContext so it lands in the model's context at session start.
jq -n --arg c "$CONTENT" '{
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: ("Previous-session summary (auto-loaded by SessionStart hook). Use this to pick up where the last session left off.\n\n" + $c)
  }
}'
exit 0
