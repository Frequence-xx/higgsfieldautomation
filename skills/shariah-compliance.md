---
name: Shari'ah Compliance
description: Enforces Islamic Shari'ah guidelines of Ahlus Sunnah wal Jama'ah at every pipeline stage — brief validation, prompt engineering, visual QA, audio compliance, and final review.
autoInvoke: true
triggers:
  - brief validation
  - visual QA
  - frame analysis
  - video review
  - audio mixing
  - content generation
negatives:
  - Do NOT invoke when task is purely technical (FFmpeg encoding, file management, git operations)
  - Do NOT invoke when reviewing non-content artifacts (code, config files, database schemas)
  - Do NOT invoke when generating reference sheets on neutral backgrounds with no scene context
---

# Shari'ah Compliance Guidelines

This skill is a HARD GATE. Every piece of content — briefs, prompts, generated frames, assembled videos, audio tracks — must pass these checks. No exceptions. No overrides without explicit owner approval via Telegram.

## Audio Rules

**MUST NOT include music or musical instruments — ever.** Audio is restricted to:
- Voiceover narration (ElevenLabs)
- Natural ambient sound effects (Freesound API): truck engines, doors, footsteps, birdsong, street ambience, tape pulling, furniture settling
- Vocal nasheeds without instruments (where appropriate)

**MUST NOT use** Remotion Superpowers' music generation feature, Epidemic Sound, or any music library. If a Freesound SFX file contains musical elements, MUST reject it and find an alternative.

**Default audio when brief does not specify:** Use Willem voiceover (ElevenLabs) + quiet street ambiance with birds from Freesound (search: "quiet residential street birds ambient", duration 10-30s, CC license). Volume: voiceover 100%, ambient SFX 25-30%. This is the standard fallback for any brief that does not explicitly request different audio.

## Visual Rules — Modest Appearance

**Men:** Appropriate clothing at all times. No shorts above the knee. 'Awrah must be covered. Work uniforms should be long trousers, full-sleeve or rolled-sleeve shirts.

**Women (if depicted):** Full hijab with loose-fitting garments. No form-fitting clothing. No visible hair. If in doubt about whether AI-generated clothing meets the standard, reject and regenerate with stronger corrective language.

**Prompt enforcement:** Every generation prompt involving people must include explicit dress code language: "wearing modest work uniforms with long trousers" (for crew), "wearing hijab with loose-fitting modest clothing" (for women).

## Scene Composition Rules

**No free-mixing.** Avoid inappropriate gender interactions. Family scenes depict mahram relationships naturally. Crew scenes show male workers in professional contexts.

**No haram imagery.** Actively scan for and reject:
- Bottles (alcoholic or ambiguous)
- Statues or idols
- Inappropriate signage or symbols
- Impermissible environments
- Any AI-hallucinated objects that would be inappropriate

**No deceptive advertising.** Show realistic service depictions. No impossible promises. No misleading before/after scenarios. No exaggeration of capabilities. The Prophet ﷺ prohibited deception in trade.

## Tone

All content reflects **amānah** (trustworthiness) and **iḥsān** (excellence). Professional, sincere, dignified. Never sensationalist or manipulative.

## QA Scoring

`shariah_compliance` score MUST be **10/10** or the clip is instantly rejected. Failure codes:
- `DRESS_CODE_VIOLATION` — clothing doesn't meet modest dress standards
- `HARAM_BACKGROUND_ELEMENT` — impermissible object in scene
- `FREE_MIXING_VIOLATION` — inappropriate gender interaction
- `MUSIC_DETECTED` — musical elements in audio track
- `DECEPTIVE_CONTENT` — unrealistic or exaggerated claims
- `INAPPROPRIATE_TONE` — sensationalist or manipulative framing

## Regeneration Protocol

Maximum **3 regeneration attempts** per clip for compliance failures. Each retry adds progressively stronger corrective language:
- Retry 1: Add specific corrective prompt (e.g., "all men wearing long trousers and modest work uniforms")
- Retry 2: Add negative prompts AND reference-anchor to a known-compliant frame
- Retry 3: Simplify the composition (fewer people, wider shot, less detail that can go wrong)

After 3 failures: **escalate to owner via Telegram** with the specific frames, failure codes, and a recommendation.
