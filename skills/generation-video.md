---
name: Generation — Video Animation (I2V)
description: Tier 1B video animation via AIMLAPI Kling v3 I2V. Covers motion prompting, camera control, negative prompts, cfg_scale, duration strategy, ghost-driving prevention, breathing artifact prevention, known failures, and API call templates.
autoInvoke: true
triggers:
  - video generation
  - animate
  - I2V
  - image to video
  - Kling
  - motion prompt
  - video clip
  - generate video
negatives:
  - Do NOT invoke when generating hero frames (use generation-image.md)
  - Do NOT invoke when performing QA or scoring (use video-qa-rubric.md)
  - Do NOT invoke when doing post-production, captions, or audio assembly
---

# Generation — Video Animation (I2V Models)

Tier 1B of the pipeline. Animate QA-passed hero frames into 5-second video clips via AIMLAPI Kling v3 I2V.

## Critical Rules

1. **MUST NOT animate a hero frame that has not passed QA AND received owner approval.** Static-first validation + owner sign-off are both mandatory before spending video credits.
2. **MUST set `generate_audio: false`** on every call. Audio ON adds 50% surcharge. Add audio in post.
3. **MUST set `aspect_ratio: "9:16"`** to match the hero frame and target platform.
4. **MUST use Pro model for final output** — Standard is only 720p. Pro gives native 1080p.
5. **MUST generate ONE clip at a time.** Verify before proceeding.
6. **SHOULD default to 5-second duration** for maximum quality per credit.

## Model Strings and Pricing

| Model | AIMLAPI String | Resolution | Cost (5s, audio OFF) |
|-------|---------------|------------|---------------------|
| Kling O1 Reference-to-Video | `klingai/video-o1-reference-to-video` | 1080p (9:16) | **$0.56** |
| Kling v3 Standard Turbo I2V | `klingai/video-v3-standard-turbo-image-to-video` | 720p (9:16) | **$0.73** ($0.146/sec) — Last frame OPTIONAL. ✓ CORRECTED 2026-06-21: Silent video by default in single-clip mode (AIMLAPI docs list `generate_audio` with default=true — ALWAYS pass `false` as safety; strip audio immediately as precaution). CANARY REQUIRED. |
| Kling v3 Standard Turbo T2V | `klingai/video-v3-standard-turbo-text-to-video` | 720p (9:16) | **$0.73** ($0.146/sec) — T2V variant. Same corrected audio behavior. ALWAYS pass `generate_audio: false`. CANARY REQUIRED. |
| **Kling v3 Turbo Pro I2V** | `klingai/video-v3-turbo-pro-image-to-video` | **1080p (9:16)** | **$0.91** ($0.182/sec — AIMLAPI pricing confirmed June 2026) — 37.7% cheaper than v3 Pro. ✓ CORRECTED 2026-06-21: Silent video by default in single-clip mode. ALWAYS pass `generate_audio: false`. Strip audio as safety precaution. CANARY REQUIRED. |
| **Kling v3 Turbo Pro T2V** | `klingai/video-v3-turbo-pro-text-to-video` | **1080p (9:16)** | **$0.91** ($0.182/sec) — ALWAYS pass `generate_audio: false`. CANARY REQUIRED. |
| Kling v3 Standard I2V | `klingai/video-v3-standard-image-to-video` | 720x1280 (9:16) | **$0.546** ($0.1092/sec — SC350 2026-09-11 CONFIRMED; old $1.09 was 2.6× markup, now 1.3×) |
| Kling v3 Standard T2V | `klingai/video-v3-standard-text-to-video` | 720x1280 (9:16) | **$0.546** ($0.1092/sec — SC350 confirmed) |
| Kling v3 Pro I2V | `klingai/video-v3-pro-image-to-video` | **1080x1920 (9:16)** | **$0.728** ($0.1456/sec — SC360 Sept 14, 2026; old $1.46 was 2.6× markup era, now 1.3×). **⚠️ THIRD STRING CANARY (SC451 2026-11-21):** AIMLAPI has a SEPARATE page `aimlapi.com/models/kling-video-v3-pro` listing $0.291/sec audio-off, $0.437/sec audio-on — 2× more expensive. Matches `kling-video/v3/pro/...` alias pattern confirmed for Turbo Pro. Unknown if same quality or different tier. CANARY: test `kling-video/v3/pro/image-to-video` before use. Use `klingai/video-v3-pro-image-to-video` ($0.1456/sec confirmed) until tested. |
| Kling v3 Pro T2V | `klingai/video-v3-pro-text-to-video` | **1080x1920 (9:16)** | **$0.728** ($0.1456/sec — SC360 Sept 14, 2026). Same third-string CANARY applies (SC451). |
| **Kling v4 I2V** | `kling-video/v4/image-to-video` | 720p or 1080p (`resolution` param; default 1080p) | **720p: $0.785/5s ($0.157/sec) · 1080p: $1.175/5s ($0.235/sec)** — AIMLAPI pricing confirmed SC395 Oct 31 2026 from AIMLAPI model page (release Oct 15, 2026). **More expensive than v3 Pro ($0.728) — use v3 Pro for production.** NO `generate_audio`, no `cfg_scale`, no `camera_control`, no `negative_prompt`. Audio always on; strip immediately. **⚠️ DUAL MODEL STRING (SC409 2026-11-03):** AIMLAPI has TWO confirmed pages for v4 I2V: `kling-video/v4/image-to-video` and `klingai/video-v4-image-to-video`. The `klingai/` variant explicitly documents `tail_image_url` for end-frame conditioning — **`tail_image_url` confirmed for v4 I2V on AIMLAPI**. Try `kling-video/v4/image-to-video` first; fallback to `klingai/video-v4-image-to-video` if rejected. CANARY REQUIRED to confirm which string is active. |
| **Kling v4 T2V** | `kling-video/v4/text-to-video` | 720p or 1080p (`resolution` param; default 1080p) | **720p: $0.785/5s ($0.157/sec) · 1080p: $1.175/5s ($0.235/sec)** — same rates as I2V (AIMLAPI model page SC395). No `generate_audio`, no `cfg_scale`, no `camera_control`, no `negative_prompt`. **⚠️ DUAL MODEL STRING (SC416 2026-11-05):** SC409 "corrected" this to `klingai/video-v4-text-to-video` based on one AIMLAPI model page — but search now confirms AIMLAPI has TWO pages: `aimlapi.com/models/kling-video-v4-text-to-video` (ID: `kling-video/v4/text-to-video`) AND `aimlapi.com/models/klingai-video-v4-text-to-video` (ID: `klingai/video-v4-text-to-video`). Same dual-string pattern as v4 I2V. Try `kling-video/v4/text-to-video` first; fallback to `klingai/video-v4-text-to-video`. CANARY REQUIRED to confirm which is active. |
| **Kling v4 Reference-to-Video** | `kling-video/v4/reference-to-video` | 720p or 1080p (`resolution` param; default 1080p) | **720p: $0.785/5s · 1080p: $1.175/5s** (SC395). Supports **up to 10 reference images (`image_urls`, @Image1 syntax) + 7 character elements (`elements`, @Element1 syntax)** (AIMLAPI docs confirmed SC423 2026-11-07 — significant upgrade from v3 Pro's 3 elements). Each element requires `frontal_image_url` + `reference_image_urls` (1–3, REQUIRED not optional). No `generate_audio`. **⚠️ CONFIRMED DUAL STRING (SC423 2026-11-07, supersedes SC416):** Both `kling-video/v4/reference-to-video` AND `klingai/video-v4-reference-to-video` are dedicated AIMLAPI model pages — confirmed by direct model page URL at `aimlapi.com/models/klingai-video-v4-reference-to-video`. CANARY REQUIRED to confirm which string is ACTIVE in live API; try `kling-video/v4/reference-to-video` first. |
| **Kling v4 Video Edit** | `klingai/video-v4-video-to-video-edit` | 720p or 1080p | **720p: $0.188/sec · 1080p: $0.282/sec** — CONFIRMED on AIMLAPI (SC395 Oct 31 2026, AIMLAPI model page). Takes source clip + text instruction, returns edited video of same length. **⚠️ MODEL STRING CORRECTED (SC409 2026-11-03):** Previous entry `kling-video/v4/video-to-video/edit` was unconfirmed — AIMLAPI model page confirms correct string is `klingai/video-v4-video-to-video-edit`. CANARY REQUIRED. |

**AIMLAPI unified endpoint (SC451 2026-11-21):** New unified endpoint confirmed at `https://api.aimlapi.com/v2/video/generations`. Legacy endpoint `https://api.aimlapi.com/v2/generate/video/kling/generation` still works. No action required for existing scripts.