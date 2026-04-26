#!/bin/bash
# SessionStart hook: surfaces previous-session summary + active production state
# (family-lock + component library + recent feedback) so the new context auto-knows
# what to reuse and what constraints apply. Pairs with precompact-summary.sh.

SUMMARY=/opt/pipeline/data/last-session-summary.md
FAMILY_LOCK=/opt/pipeline/data/family-lock.json
LIBRARY=/opt/pipeline/assets/library/components.json
CATALOG=/opt/pipeline/data/feedback-catalog.json

EMIT=""

# --- Previous session summary (skip if missing or >7d old) ---
if [ -f "$SUMMARY" ] && [ $(find "$SUMMARY" -mtime +7 2>/dev/null | wc -l) -eq 0 ]; then
  EMIT+="# Last session summary\n\n$(cat "$SUMMARY")\n\n---\n\n"
fi

# --- Active production state (always emit if files exist) ---
if [ -f "$FAMILY_LOCK" ] && [ -f "$LIBRARY" ]; then
  FAMILY=$(jq -r '.current_family' "$FAMILY_LOCK" 2>/dev/null)
  COUNT=$(jq -r '.videos_in_family | length' "$FAMILY_LOCK" 2>/dev/null)
  LOCK=$(jq -r '.lock_until' "$FAMILY_LOCK" 2>/dev/null)
  CHARACTERS=$(jq -r '.characters | keys | join(", ")' "$LIBRARY" 2>/dev/null)
  SCENES=$(jq -r '.scenes | keys | join(", ")' "$LIBRARY" 2>/dev/null)
  AUDIO=$(jq -r '.audio_beds | keys | join(", ")' "$LIBRARY" 2>/dev/null)

  EMIT+="# Active production state (auto-loaded)\n\n"
  EMIT+="**Family lock:** \`$FAMILY\` ($COUNT/$LOCK videos completed). Switching families requires owner approval.\n\n"
  EMIT+="**Approved components — REUSE these instead of regenerating:**\n"
  EMIT+="- Characters: $CHARACTERS\n"
  EMIT+="- Scenes: $SCENES\n"
  EMIT+="- Audio beds: $AUDIO\n\n"
  EMIT+="**Mandatory workflow before producing any video:**\n"
  EMIT+="1. Read \`data/family-lock.json\` — confirm new video stays in current family\n"
  EMIT+="2. Use \`scripts/library.py\` (\`from library import get_character, get_scene, get_audio_bed\`) to look up reusable assets BEFORE generating new ones\n"
  EMIT+="3. Every API call routes through \`scripts/pre_flight_gate.py\` (already wired in gen_*.py) — gate blocks payloads violating \`data/feedback-catalog.json\`\n"
  EMIT+="4. New patterns surface weekly via \`scripts/pattern_extractor.py\` reports in \`output/research/patterns/\`\n\n"
  EMIT+="**The user does NOT need to remember this — YOU auto-apply it.** Don't ask permission to consult library/family-lock; just do it as Step 0 of any video task.\n\n---\n\n"
fi

# Nothing to emit → exit
if [ -z "$EMIT" ]; then
  exit 0
fi

# Emit as additionalContext via hook protocol
jq -n --arg c "$EMIT" '{
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: ("SessionStart auto-context:\n\n" + $c)
  }
}'
exit 0
