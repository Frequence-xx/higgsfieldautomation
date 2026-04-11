#!/bin/bash
# Pre-generation BLOCKING gate hook
# Validates API call parameters before allowing execution
# Only triggers on actual python3 httpx API calls, not echo/test commands

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""' 2>/dev/null)

# Only check actual python3 calls that hit AIMLAPI
if ! echo "$COMMAND" | grep -q "^python3\|^export.*python3"; then
    exit 0
fi

# Check 1: Image generation must include 9:16
if echo "$COMMAND" | grep -q "images/generations"; then
    if ! echo "$COMMAND" | grep -qi '9:16\|"9:16"'; then
        echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED: Image generation without 9:16 aspect ratio. MUST use aspect_ratio: 9:16."}}'
        exit 0
    fi
fi

# Check 2: Video generation must not have audio true
if echo "$COMMAND" | grep -q "generate/video\|video/generation"; then
    if echo "$COMMAND" | grep -qi '"generate_audio":\s*true\|generate_audio.*True'; then
        echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED: Video generation with audio ON. MUST set generate_audio: false."}}'
        exit 0
    fi
fi

# Advisory checklist for all AIMLAPI python calls
echo '{"systemMessage":"PRE-GENERATION GATE: (1) Model per routing matrix (2) Character identity header (3) 9:16 (4) No text in video (5) Motion 15-40 words+endpoint (6) Negative prompt (7) audio:false (8) Truck: stationary (9) Face adherence 80-90 (10) Cost logged"}'
exit 0
