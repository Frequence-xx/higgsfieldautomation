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
negatives:
  - Do NOT invoke when performing post-production tasks (FFmpeg, Remotion, audio mixing — these are free/local)
  - Do NOT invoke when doing brief intake or shot list planning (no credits spent yet)
  - Do NOT invoke when running QA on already-generated content (scoring does not cost credits)
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
- Standard I2V: `kling-video/v3/standard/image-to-video`
  - Audio OFF: **$1.09/5s** ($0.218/sec) ← USE THIS
  - Audio ON: **$1.64/5s** ($0.328/sec) ← NEVER USE, add audio in post
- Pro I2V: `kling-video/v3/pro/image-to-video` (est. ~$1.50-2.00/5s)
- CRITICAL: Always set `"generate_audio": false` — saves 33%!

Required parameters for optimal Kling v3 I2V generation:
```json
{
    "model": "kling-video/v3/standard/image-to-video",
    "image_url": "<url>",
    "prompt": "<motion description>",
    "duration": "5",
    "aspect_ratio": "9:16",
    "generate_audio": false,
    "cfg_scale": 0.5,
    "negative_prompt": "blurry, low quality, distorted, jittery, flickering"
}
```

## Budget Math (AIMLAPI) — UPDATED 2026-04-10

- Kling v3 Standard I2V (5s, audio OFF): **$1.09** per generation
- Hero frame (Nano Banana Pro Edit): **$0.20** per generation
- Hero frame (Kontext Max): **$0.10** per generation
- Per clip total (image + video, audio OFF): **~$1.30**
- 50 videos × 4 clips = 200 clips
- At 1.0× (no waste): 200 × $1.30 = **~$260/month**
- At 1.3× iteration: 260 × $1.30 = **~$338/month**
- **Steady state target: ~$300-400 AIMLAPI/month**
- CRITICAL: Zero waste means getting hero frames right first time with multi-reference

## Rules

1. **ONE generation at a time. NEVER batch multiple without confirmation.**
2. Log every generation with model, cost, and QA score in SQLite
3. If a shot fails QA 3 times → STOP, escalate to owner with failure details
4. Verify correct image is selected before ANY generation
5. Always use image-to-video (I2V) — never text-to-video for final shots (I2V preserves the hero frame's composition)
6. Track per-model success rates in learned_preferences — route future shots to most efficient model
