---
name: Credit Efficiency
description: Rules for credit conservation across Higgsfield (hero frames) and AIMLAPI (video generation). Model routing based on test run data.
autoInvoke: true
triggers:
  - generation
  - credits
  - budget
  - model selection
  - aimlapi
---

# Credit Efficiency Rules

## Single-Platform Architecture (AIMLAPI for everything)

**Hero Frame Generation:** AIMLAPI — Nano Banana Pro (`google/nano-banana-pro`) or Flux Pro (`flux-pro`)
**Video Animation:** AIMLAPI — Kling v3 Standard I2V (`kling-video/v3/standard/image-to-video`)
**Voiceover:** ElevenLabs (Willem voice, eleven_multilingual_v2)
**Post-Production:** FFmpeg + Remotion (free, local)

No browser automation needed. Entire generation pipeline is clean API calls.

## Static-First Validation Funnel

**NEVER spend video credits without a passed static frame first.**

1. Generate hero frame via AIMLAPI Nano Banana Pro or Flux Pro (cheap per image)
2. Run the still through full QA rubric (8 dimensions + Shari'ah compliance + cinematic quality)
3. Only if the still passes → send to AIMLAPI Kling v3 I2V for video animation
4. If the still fails → fix the prompt and regenerate the still (cheap, not video credits)

## Model Routing (Updated from Test Data)

| Shot Type | Image Model (AIMLAPI) | Video Model (AIMLAPI) | Est. Cost/5s | Notes |
|-----------|----------------------|----------------------|-------------|-------|
| Wide establishing (80%) | Nano Banana Pro Edit (multi-ref) | Kling v3 Standard I2V (audio OFF) | **~$1.85** | $0.20 image + $1.64 video. ALWAYS use reference images. |
| Hero shots (15%) | Flux Kontext Max (character ref) | Kling v3 Standard I2V (audio OFF) | **~$1.75** | $0.10 image + $1.64 video |
| Money shot / CTA (5%) | Flux Pro v1.1 Ultra | Veo 3.1 Lite I2V | **~$2.00+** | Highest quality available |
| B-roll / texture | Nano Banana Pro Edit (multi-ref) | Kling v3 Standard I2V (audio OFF) | **~$1.85** | Same pipeline, reference-based |

**CRITICAL: Always use I2V (image-to-video), NOT T2V (text-to-video). I2V is 2.6x cheaper and preserves hero frame composition.**
**CRITICAL: Always generate with audio OFF. Add voiceover/SFX in post-production. Audio adds 50% surcharge.**

Exact AIMLAPI model strings:
- Standard I2V: `kling-video/v3/standard/image-to-video` (**$1.64/5s** — confirmed 2026-04-10)
- Pro I2V: `kling-video/v3/pro/image-to-video` (est. ~$2.00/5s)
- Note: Previous docs said $0.42 — this was WRONG. Actual price confirmed at $1.638 across 4 generations.

## Budget Math (AIMLAPI) — UPDATED 2026-04-10

- Kling v3 Standard I2V (5s): **$1.64** per generation (not $0.42)
- Hero frame (Nano Banana Pro Edit): **$0.20** per generation
- Hero frame (Kontext Max): **$0.10** per generation
- Per clip total (image + video): **~$1.85**
- 50 videos × 5 clips = 250 clips
- At 1.3× iteration: 325 generations × $1.85 = **~$600/month**
- At 2× iteration (month 1): 500 × $1.85 = **~$925/month**
- **Month 1 realistic budget: ~$800-1000 AIMLAPI**
- **Steady state: ~$500-700 AIMLAPI/month**
- IMPORTANT: Consider reducing clips per video (3-4 instead of 5) to manage costs

## Rules

1. **ONE generation at a time. NEVER batch multiple without confirmation.**
2. Log every generation with model, cost, and QA score in SQLite
3. If a shot fails QA 3 times → STOP, escalate to owner with failure details
4. Verify correct image is selected before ANY generation
5. Always use image-to-video (I2V) — never text-to-video for final shots (I2V preserves the hero frame's composition)
6. Track per-model success rates in learned_preferences — route future shots to most efficient model
