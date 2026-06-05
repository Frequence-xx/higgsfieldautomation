---
name: Credit Efficiency
description: Rules for credit conservation across AIMLAPI (image + video generation). Model routing based on test run data and cost research.
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

**Hero Frame Generation:** AIMLAPI — Nano Banana Pro Edit (`google/nano-banana-pro-edit`) or Flux Kontext Max
**Video Animation — Character shots:** AIMLAPI — Kling v3 Pro I2V (`klingai/video-v3-pro-image-to-video`)
**Video Animation — Establishing/B-roll (no character):** AIMLAPI — Veo 3.1 Lite T2V (`google/veo-3-1-lite-generate-preview`)
**Voiceover:** ElevenLabs (Willem voice, eleven_multilingual_v2)
**Post-Production:** FFmpeg + Remotion (free, local)

No browser automation needed. Entire generation pipeline is clean API calls.

## Static-First Validation Funnel

**MUST NOT spend video credits without a passed static frame first.**

1. Generate hero frame via AIMLAPI NBP Edit or Flux Kontext Max (cheap per image)
2. Run the still through full QA rubric (8 dimensions + Shari'ah compliance + cinematic quality)
3. Only if the still passes → send to video generation
4. If the still fails → fix the prompt and regenerate the still (cheap, not video credits)

For T2V establishing shots (Veo 3.1 Lite, no character): generate a reference still first via NBP to confirm composition, then proceed to T2V generation with the same prompt intent.

## Model Routing — Updated 2026-05-17

| Shot Type | Image Model | Video Model | Cost/clip | Notes |
|-----------|------------|------------|-----------|-------|
| Character close-up | NBP Edit ($0.195) | Kling v3 Pro I2V ($1.46) | **~$1.66** | Subject Binding 80-90, I2V from hero frame |
| Character — draft/iteration | NBP Edit ($0.195) | Kling v3 Standard I2V ($1.09) | **~$1.29** | Use Standard until prompt is dialed in, Pro for final only |
| Wide establishing (no character, draft) | NBP (T2I, $0.13) | Veo 3.1 Lite T2V 720p ($0.26/4s) | **~$0.39** | Draft at 720p 4s — cheapest B-roll |
| Wide establishing (no character, final) | NBP (T2I, $0.13) | Hailuo 02 I2V 6s ($0.28) | **~$0.41** | CANARY REQUIRED — 1080p, no char, 9:16 confirmed |
| B-roll / texture (no character) | NBP ($0.13) | Hailuo 02 I2V 6s ($0.28) | **~$0.41** | No audio param needed — no surcharge risk |
| Truck/product (no char, draft) | NBP Edit ($0.195) | Veo 3.1 Fast I2V (~$0.65/5s est.) | **~$0.85** | CANARY REQUIRED — `google/veo-3.1-i2v-fast`, camelCase params |
| Truck/product (ghost-driving lock) | NBP Edit ($0.195) | Veo 3.1 First+Last Fast (~$0.65/5s est.) | **~$0.85** | CANARY REQUIRED — `google/veo-3.1-first-last-image-to-video-fast`, same first+last frame = stationary truck |
| Truck/product hero | NBP Edit ($0.195) | Kling v3 Pro I2V ($1.46) | **~$1.66** | cfg_scale 0.7, ghost-driving locks |
| Brand color still (#FC8434) | FLUX.2 Pro ($0.07) | — | $0.07 | HEX matching; T2I only |
| Typography/text still | Flux Kontext Max ($0.10) | — | $0.10 | Best text rendering |
| Money shot / CTA | Flux Pro v1.1 Ultra ($0.10) | Kling v3 Pro I2V ($1.46) | **~$1.56** | Highest quality |

**CRITICAL: Always use I2V (image-to-video) for character shots — I2V preserves hero frame composition.**
**CRITICAL: Veo 3.1 Lite is T2V only (no character). Its `image_url` parameter behavior on AIMLAPI is UNVERIFIED — do NOT use for character or hero-frame animation until tested.**
**CRITICAL: Always generate with audio OFF on ALL models. Audio adds 33–85% surcharge depending on model.**
**CRITICAL: New Veo 3.1 Fast models use camelCase params like Veo 3.1 Lite (`generateAudio`, `aspectRatio`, `durationSeconds`) — NOT snake_case.**

## Draft → Final Tiering (Kling only)

Use this funnel for every character or truck shot to minimize cost:

1. **Draft iterations:** Kling v3 Standard I2V (`klingai/video-v3-standard-image-to-video`) at $1.09/5sec — **use 3s clips for drafts (see below)**
2. **Final output:** Kling v3 Pro I2V (`klingai/video-v3-pro-image-to-video`) at $1.46/5sec — ONLY after prompt is approved by owner
3. **Savings (5s drafts):** Two Standard drafts + one Pro final = $3.64 vs three Pro passes = $4.38 — saves $0.74/clip (17%)
4. **Savings (3s drafts):** Two 3s Standard drafts + one Pro final = $2.76 vs three Pro passes = $4.38 — saves $1.62/clip (37%)

For Veo 3.1 Lite (B-roll/establishing): no tiering needed. Lite IS the final model — quality is sufficient at $0.52/5sec.

## Short-Duration Drafts (Kling Standard) — Updated 2026-04-26

**Use 3-second clips for ALL Standard draft iterations. Use 5s only for Pro finals.**

- Standard 3s clip cost: $0.218/sec × 3s = **$0.65** (vs $1.09 at 5s — saves $0.44/draft)
- 3 seconds is sufficient to evaluate: motion type, composition validity, identity drift, ghost-driving presence
- 3s clips reveal all failure modes that would cause a retry — no need to pay for 5 full seconds of drift
- After 2 Standard drafts confirm the prompt works → generate one 5s Pro final

**Duration rule by pass type:**

| Pass | Model | Duration | Cost | Purpose |
|------|-------|----------|------|--------|
| Draft 1 | Standard | **3s** | $0.65 | Evaluate motion direction and identity lock |
| Draft 2 (if needed) | Standard | **3s** | $0.65 | Confirm prompt fix worked |
| Final | Pro | **5s** | $1.46 | Owner delivery |

**Kling `duration` parameter accepts int 3-15 (seconds). Linear cost scaling confirmed.**

Exception: if the shot's key motion event occurs after 3s (e.g., character completes a multi-step action), use 5s Standard. This is rare — most motion assessment is visible in the first 3 seconds.

## Model Strings and Pricing (AIMLAPI, verified 2026-04-20)

### Video Models

| Model | AIMLAPI String | Resolution | Cost (5s, audio OFF) | Cost (3s) |
|-------|---------------|-----------|---------------------|----------|
| Kling v3 Standard I2V | `klingai/video-v3-standard-image-to-video` | 720p (9:16) | **$1.09** ($0.218/sec) | **$0.65** |
| Kling v3 Pro I2V | `klingai/video-v3-pro-image-to-video` | 1080p (9:16) | **$1.46** ($0.291/sec) | $0.87 |
| Veo 3.1 Lite T2V 720p | `google/veo-3-1-lite-generate-preview` | 720p (default) | **~$0.33** ($0.065/sec, 5s equiv) | ~$0.26 (4s) |
| Veo 3.1 Lite T2V 1080p | `google/veo-3-1-lite-generate-preview` | 1080p (requires dur=8) | **~$0.83** ($0.104/sec × 8s) | — |
| Veo 3.1 I2V | `google/veo-3.1-i2v` | 720p/1080p | **~$1.00** ($0.20/sec × 5s) | ~$0.60 (3s) |
| Veo 3.1 Fast I2V (canary) | `google/veo-3.1-i2v-fast` | 720p/1080p | **~$0.65** (~$0.13/sec est.) | ~$0.39 (3s) |
| Veo 3.1 First+Last Fast (canary) | `google/veo-3.1-first-last-image-to-video-fast` | 720p/1080p | **~$0.65** (~$0.13/sec est.) | — |
| Wan 2.6 I2V (fallback) | `alibaba/wan-2-6-i2v` | TBD | **~$0.65** ($0.13/sec, min 5s) | — |
| Wan 2.7 I2V | `alibaba/wan-2-7-i2v` ✓ CONFIRMED | 720p/1080p | **~$0.50** (~$0.10/sec × 5s) | **~$0.30** (3s), **~$0.20** (2s ultra-draft) — model string confirmed, no audio surcharge risk, CANARY REQUIRED |
| Wan 2.7 R2V | `alibaba/wan-2-7-r2v` | 720p/1080p | ~$0.50 est. | LIKELY LIVE (2026-06-05) — Wan 2.6 R2V exists on AIMLAPI as `alibaba/wan-2-6-r2v`; Wan 2.7 follows same naming. CANARY REQUIRED. Up to 5 mixed refs, character binding via `Image1`/`Video1` prompt slots. |
| Wan 2.7 T2V | `alibaba/wan-2-7-t2v` ✓ CONFIRMED | 720p/1080p | **~$0.50** (~$0.10/sec × 5s) | **~$0.30** (3s) — AIMLAPI docs page confirmed 2026-06-05. Use for wide shots without characters. CANARY REQUIRED before production. |
| Kling 2.6 Pro I2V (canary) | `klingai/video-v2-6-pro-image-to-video` | TBD | **~$0.46** ($0.091/sec) | ~$0.27 |
| Hailuo 02 I2V (6s) | `minimax/hailuo-02` | 1080p (9:16 ✓) | **$0.437** ($0.0728/sec × 6s) | No audio param — NOTE: $0.28 flat was fal.ai price, AIMLAPI is per-second |
| Hailuo 02 I2V (10s) | `minimax/hailuo-02` | 1080p (9:16 ✓) | **$0.728** ($0.0728/sec × 10s) | NOT the cheapest — LTXV 2 Fast wins at $0.40/10s; Hailuo 2.3 Fast at $0.416/10s |
| Hailuo 2.3 Fast | `minimax/hailuo-2.3-fast` | 1080p 24fps | **$0.0416/sec** ($0.416/10s flat — corrected 2026-05-19) | 5s = $0.208 (cheapest non-char 5s clip) |
| LTXV 2 Fast I2V | `ltxv/ltxv-2-fast` | 1080p | **$0.04/sec** ($0.24/6s min) | CANARY REQUIRED — cheapest 6s+ non-char I2V; audio OFF required |
| LTXV 2 Standard I2V | `ltxv/ltxv-2` | 1080p | **$0.06/sec** ($0.36/6s min) | Higher quality, slower than Fast |
| Luma Ray Flash 2 I2V | `luma/ray-flash-2` | 720p (9:16 ✓) | **~$0.048/sec** (~$0.24/5s, AIMLAPI $0.002/M pixels) | No audio generation, no surcharge risk — CANARY REQUIRED. I2V + first+last frame. Max 9s. |
| Seedance 2.0 (canary) | `bytedance/seedance-2-0` | TBD | **~$0.18/sec est.** (AIMLAPI docs example shows $0.06/gen — unverified) | CANARY REQUIRED — exact AIMLAPI price unknown; face content-policy risk |

**Non-character video routing by duration (updated 2026-06-05):**
- **5s clip:** Hailuo 2.3 Fast ($0.208) — cheapest; Luma Ray Flash 2 (~$0.24) is I2V alternative if Hailuo quality insufficient
- **6-9s clip:** LTXV 2 Fast ($0.04/sec, $0.24/6s) — beats Hailuo 2.3 Fast ($0.25/6s) and Luma Ray Flash 2 ($0.288/6s)
- **10s clip:** LTXV 2 Fast ($0.40/10s) — beats Hailuo 2.3 Fast ($0.416/10s) and Luma Ray Flash 2 ($0.48/10s)
- **CORRECTION 2026-05-23:** Hailuo 02 is $0.0728/sec on AIMLAPI (NOT $0.28 flat — that was fal.ai pricing). Hailuo 02 is no longer recommended for any clip length.

**LTXV 2 Fast note (confirmed 2026-05-22, updated 2026-06-03):** `ltxv/ltxv-2-fast` is LIVE on AIMLAPI. $0.04/sec at 1080p. Parameters use snake_case (not camelCase like Veo): `aspect_ratio`, `generate_audio`, `image_url`. `generate_audio: false` REQUIRED — audio defaults ON. Minimum duration 6s, max 20s. I2V supported. CANARY REQUIRED before production use. **LTX-2.3 caveat:** LTX released v2.3 in Q2 2026 at $0.05/sec (confirmed on other providers). If AIMLAPI has silently updated the `ltxv/ltxv-2-fast` endpoint to point to LTX-2.3, cost would be $0.05/sec not $0.04. Verify actual billing from AIMLAPI dashboard on first test call — record exact invoice amount before routing production shots.

**Veo 3.1 Lite pricing update (2026-05-06):** Resolution-tiered pricing confirmed. 720p: $0.05/sec (Vertex) → ~$0.065/sec on AIMLAPI (estimated, ~1.3× markup). 1080p: $0.08/sec (Vertex) → ~$0.104/sec on AIMLAPI (production-verified ✓). **Use 720p for B-roll drafts — saves ~37% vs 1080p.** Duration valid values: **4, 6, or 8 seconds ONLY** — 5 is invalid. 1080p requires duration=8.

**Veo 3.1 I2V (NEW — 2026-05-06):** `google/veo-3.1-i2v` at $0.20/sec = $1.00/5s — 32% cheaper than Kling v3 Pro ($1.46/5s). No Subject Binding, no character-locking. Suitable for truck/product shots and wide establishing shots where face identity lock is NOT required. DO NOT use for character face close-ups. Canary required before production use.

**Hailuo 02 I2V (pricing RE-CORRECTED 2026-05-23):** `minimax/hailuo-02` at **$0.0728/sec on AIMLAPI** (6s = $0.437, 10s = $0.728). The previously noted $0.28/clip flat price was fal.ai's pricing, NOT AIMLAPI's pricing. At AIMLAPI's per-second billing, Hailuo 02 is MORE expensive than Kling v3 Pro ($0.291/sec) and more expensive than all other non-character options. **NOT cost-efficient for this pipeline.** I2V (image_url parameter), 9:16 confirmed, **1080p** native resolution. No native audio generation — no audio parameter, no surcharge risk. Use LTXV 2 Fast ($0.04/sec) or Hailuo 2.3 Fast ($0.0416/sec) instead.

*The $0.0728/sec figure from the original AIMLAPI docs was correct all along — the 2026-05-15 "correction" to $0.28 flat incorrectly imported fal.ai pricing into the AIMLAPI pipeline. Always verify pricing from AIMLAPI docs, not fal.ai.*

**Wan 2.6 note (web research 2026-04-26, medium confidence):** $0.13/sec confirmed from AIMLAPI pricing page snippet. Minimum clip is 5 seconds — no 3s option. Slightly more expensive than Veo 3.1 Lite 720p but provides I2V capability (Veo Lite is T2V only). Use as fallback when Veo is unavailable.

**Wan 2.7 I2V (AIMLAPI status 2026-05-30):** `alibaba/wan-2-7-i2v` is LIVE on AIMLAPI (docs page confirmed). Pricing: ~$0.10/sec (updated from $0.08/sec estimate; multiple sources converge on $0.10/sec as base rate). Supports duration 2-15s (not just fixed values). NO `generate_audio` parameter — does not generate audio natively, no audio surcharge risk. `audio_url` accepts input audio for synchronization. Supports first+last frame pinning. **T2V: CONFIRMED LIVE as `alibaba/wan-2-7-t2v` (AIMLAPI docs page surfaced 2026-06-05). R2V: likely live per naming convention — Wan 2.6 R2V exists as `alibaba/wan-2-6-r2v`, Wan 2.7 R2V expected at `alibaba/wan-2-7-r2v`. Both need CANARY before production.**

**Kling 2.6 Pro I2V (CANARY REQUIRED):** At $0.091/sec it is 58% cheaper than Kling v3 Standard and 69% cheaper than Kling v3 Pro. Older model generation — quality vs. v3 unverified for character identity retention. Do NOT use on character shots without canary validation. May be appropriate for truck-only shots where identity drift is not a concern.

**AIMLAPI credit discount:** 10% discount auto-applied on every credit top-up purchase. Effective real-world costs are 10% lower than listed prices. Budget planning uses listed prices for conservatism; treat the 10% as a safety buffer.

### Image Models

| Model | AIMLAPI String | Cost/gen | Best For |
|-------|---------------|---------|--------|
| GPT Image 2 (DRAFT) | `openai/gpt-image-2` | **$0.053** (medium) | Character drafts, text-heavy frames — CANARY REQUIRED |
| NB2 Edit (DRAFT) | `google/nano-banana-2` | **$0.08** (1K) | Character draft iterations — CANARY REQUIRED |
| NBP Edit | `google/nano-banana-pro-edit` | **$0.195** (flat) | Character + brand refs (up to 14 refs) |
| NBP (T2I) | `google/nano-banana-pro` | **~$0.13** | Pure scenery, no refs |
| Flux Kontext Max | `flux/kontext-max/image-to-image` | **$0.10** | Typography, character lock |
| FLUX.2 Pro | `blackforestlabs/flux-2-pro` | **$0.07** | Brand color #FC8434 matching |
| Flux Pro v1.1 Ultra | `flux-pro/v1.1-ultra` | **$0.10** | Money shots / CTA |

*GPT Image 2 (NEW — 2026-04-21, updated 2026-06-03): AIMLAPI model string `openai/gpt-image-2` confirmed live. Medium quality sticker price $0.053/img = 3.7× cheaper than NBP Edit. **However, billing is token-based ($30/M output tokens + $8/M input tokens at high fidelity).** When processing character reference images (mandatory high-fidelity input), actual cost is 2–3× the sticker price — real character reference cost approaches $0.10–$0.42/image. The advantage over NBP Edit ($0.195) shrinks significantly for character work. GPT Image 2 has NO Subject Binding equivalent — does not lock face identity across generations the way NBP Edit does. Best use case remains text-heavy stills (layouts, CTA frames with text) not character hero frames. CANARY REQUIRED — verify 9:16 aspect ratio support and actual billing amount before routing character work here.*

*NB2: Google official rate **$0.08/image at 1K** ($0.045 at 512px, $0.12 at 2K, $0.151 at 4K). AIMLAPI pricing may differ — run canary test before production use. For 1K hero frames, expected cost ~$0.08-0.10 — 59% cheaper than NBP Edit at same resolution.*

## Veo 3.1 Lite API Template (T2V, no character)

```python
import httpx, os, time

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Submit Veo 3.1 Lite T2V
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "google/veo-3-1-lite-generate-preview",
    "prompt": "<scene description with motion — creative director language, 30-80 words>",
    "aspectRatio": "9:16",          # NOTE: camelCase for Veo (not snake_case like Kling)
    "durationSeconds": 6,           # VALID VALUES: 4, 6, or 8 ONLY — 5 is INVALID and may error/default
    "resolution": "720p",           # "720p" (cheaper, default) or "1080p" (requires durationSeconds: 8)
    "generateAudio": False,         # ALWAYS false — saves ~46% (35cr vs 65cr)
    "enhancePrompt": False,         # ALWAYS false — AI enhancement breaks brand control
    "negativePrompt": "blurry, distorted, low quality, jittery, flickering, watermark, text overlay, logos, people, faces",
}, headers=headers, timeout=30)

task_id = resp.json()["id"]

# Poll for completion (every 10s, max 5 min)
for i in range(30):
    time.sleep(10)
    sr = httpx.get("https://api.aimlapi.com/v2/video/generations",
                   params={"generation_id": task_id}, headers=headers, timeout=30)
    if sr.json()["status"] == "completed":
        video_url = sr.json()["video"]["url"]
        break
```

**Veo 3.1 Lite parameter differences from Kling (IMPORTANT):**
- `durationSeconds` (int) — **VALID VALUES: 4, 6, or 8 ONLY** (NOT 5, not continuous). NOT `duration` (string)
- `resolution` — "720p" (default, cheaper) or "1080p". **1080p REQUIRES durationSeconds: 8**
- `aspectRatio` (camelCase) NOT `aspect_ratio` (snake_case)
- `generateAudio` (camelCase) NOT `generate_audio` (snake_case)
- `enhancePrompt` (camelCase) — must set false for brand control
- `negativePrompt` (camelCase) — supported
- `seed` (int, 0-4294967295) — supported for reproducibility
- No `cfg_scale`, no `camera_control`, no `elements` (Subject Binding) — these are Kling-only
- No `tail_image_url`, no `static_mask_url` — Kling-only

**Do NOT mix Kling and Veo parameter names in the same call — they will silently fail or use defaults.**

## Kling API Template (Character/Truck shots, I2V)

```python
resp = httpx.post("https://api.aimlapi.com/v2/generate/video/kling/generation", json={
    "model": "klingai/video-v3-pro-image-to-video",   # or standard for drafts
    "image_url": "<hero_frame_cdn_url>",
    "prompt": "<motion description ONLY, 15-40 words>",
    "duration": "5",
    "aspect_ratio": "9:16",
    "generate_audio": False,        # CRITICAL: AIMLAPI defaults TRUE for Kling v3 Pro
    "cfg_scale": 0.5,               # 0.7 for truck/branded shots
    "negative_prompt": "blurry, distorted, low quality, jittery, flickering, morphing faces, warping, deformed hands, extra fingers, sliding feet, identity drift, watermark, camera shake, inconsistent lighting, plastic skin, cartoonish, color shift",
}, headers=headers, timeout=30)
```

## Hailuo 02 API Template (Non-character I2V — B-roll, establishing, truck)

```python
import httpx, os, time

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Submit Hailuo 02 I2V
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "minimax/hailuo-02",
    "prompt": "<scene description, motion, camera — 30-80 words. No characters in frame.>",
    "image_url": "<hero_frame_cdn_url>",   # Optional for T2V; required for I2V
    "duration": "6",                        # CANARY: verify "6" string vs int format
    "aspect_ratio": "9:16",
    # NOTE: No generate_audio parameter — Hailuo 02 has NO native audio, no surcharge risk
}, headers=headers, timeout=30)

task_id = resp.json()["id"]

for i in range(30):
    time.sleep(10)
    sr = httpx.get("https://api.aimlapi.com/v2/video/generations",
                   params={"generation_id": task_id}, headers=headers, timeout=30)
    if sr.json()["status"] == "completed":
        video_url = sr.json()["video"]["url"]
        break
```

**Hailuo 02 vs Kling for non-character shots:**
- Hailuo 02 6s I2V: $0.28 (1080p, flat price, no audio surcharge)
- Kling v3 Standard 3s draft: $0.65 (720p)
- Hailuo 02 gives 6s/1080p output at $0.28 vs Kling Standard 3s/720p at $0.65 — longer clip, higher res, **57% cheaper**
- Hailuo 02 10s at same $0.28 = $0.028/sec — cheapest non-character option by far

**CANARY checklist (run before first production use):**
1. Verify duration parameter accepts string `"6"` or requires int `6`
2. Verify `aspect_ratio: "9:16"` produces vertical output
3. Run brand binary checklist on output (cargo box sealed, no ghost driving)
4. Compare 768p output quality with Veo 3.1 Lite 720p for same scene
5. Log actual cost from AIMLAPI dashboard (verify $0.0728/sec billing)

## Budget Math — Updated 2026-05-10

### Per-clip costs (production ready, audio OFF):

| Clip type | Image | Video | Total |
|-----------|-------|-------|-------|
| Character shot (final) | $0.195 | $1.46 (Pro 5s) | **$1.66** |
| Character shot (draft 3s) | $0.195 | $0.65 (Std 3s) | **$0.85** |
| Character shot (draft 5s) | $0.195 | $1.09 (Std 5s) | **$1.29** |
| Establishing/B-roll (Veo 720p 6s) | $0.13 | ~$0.39 (Lite 720p 6s) | **~$0.52** |
| Establishing/B-roll (Veo 1080p 8s) | $0.13 | ~$0.83 (Lite 1080p 8s) | **~$0.96** |
| Truck shot (final) | $0.195 | $1.46 (Pro 5s) | **$1.66** |

### Typical video (4 clips: 1 character + 2 establishing + 1 truck):

**Current routing (Kling + Veo):**

| Phase | Clips | Cost |
|-------|-------|------|
| Hero frames (4×$0.195 avg) | 4 | $0.78 |
| Character: 2 Standard 3s drafts + 1 Pro 5s final | 3 | $2.76 |
| 2 Establishing shots (Veo Lite 720p 6s, 1 pass each) | 2 | ~$0.78 |
| Truck: 2 Standard 3s drafts + 1 Pro 5s final | 3 | $2.76 |
| **Total** | | **~$7.08** |

**Optimized routing (LTXV 2 Fast for non-character, after canary pass):**

| Phase | Clips | Cost |
|-------|-------|------|
| Hero frames (4×$0.195 avg) | 4 | $0.78 |
| Character: 2 Standard 3s drafts + 1 Pro 5s final | 3 | $2.76 |
| 2 Establishing shots (LTXV 2 Fast 6s, 1 pass each) | 2 | **$0.48** |
| Truck: 2 Kling Std 3s drafts + 1 Kling Pro 5s final | 3 | $2.76 |
| **Total** | | **~$6.78** |

**Super-optimized (Wan 2.7 I2V for character drafts + LTXV 2 Fast for non-char — after both canaries pass):**

| Phase | Clips | Cost |
|-------|-------|------|
| Hero frames (4×$0.195 avg) | 4 | $0.78 |
| Character: 2 Wan 2.7 I2V 3s drafts + 1 Kling Pro 5s final | 3 | **$2.06** |
| 2 Establishing shots (LTXV 2 Fast 6s, 1 pass each) | 2 | **$0.48** |
| Truck: 2 Wan 2.7 I2V 3s + 1 Kling Pro 5s final | 3 | **$2.06** |
| **Total** | | **~$5.38** |

**Ultra-optimized (2s Wan 2.7 drafts, 2× per shot):**

| Phase | Clips | Cost |
|-------|-------|------|
| Hero frames (4×$0.195 avg) | 4 | $0.78 |
| Character: 2 Wan 2.7 I2V **2s** drafts + 1 Kling Pro 5s final | 3 | **$1.86** |
| 2 Establishing shots (LTXV 2 Fast 6s, 1 pass each) | 2 | **$0.48** |
| Truck: 2 Wan 2.7 I2V **2s** + 1 Kling Pro 5s final | 3 | **$1.86** |
| **Total** | | **~$4.98** |

*Note: 2s drafts sufficient for identity and motion direction check; may miss artifacts appearing after 2s. Start with 3s drafts; drop to 2s only after workflow is validated.*

*Savings vs current ($7.08): $0.30 with LTXV only; $1.70 with LTXV + Wan 2.7 3s drafts (after canary); $2.10 with LTXV + Wan 2.7 2s drafts.*
*Hailuo 02 is NOT in these scenarios — $0.0728/sec AIMLAPI price makes it the most expensive non-character option.*

**Target: ~$5.38/video (Wan 2.7 3s drafts) or ~$4.98 (2s drafts) after canary passes. $15 ceiling covers ~2-3 retry passes per clip.**

### Monthly (50 videos):

| Scenario | Old estimate (5s drafts) | New (3s drafts) |
|----------|-------------|-------------|
| 50 videos at 1× (no waste) | ~$346 | ~$292 |
| 50 videos at 1.3× (iterations) | ~$450 | ~$380 |

Note: savings increase proportionally with iteration count — more drafts per clip = larger 3s-vs-5s gains.

## Veo Seed Logging — Added 2026-04-26

**Log the `seed` value from every successful Veo 3.1 Lite shot. Reuse on retry to reduce variance.**

Veo 3.1 Lite supports a `seed` parameter (int, 0-4294967295). When a shot is 90% correct but needs a minor prompt tweak, reusing the same seed narrows the output space and typically delivers the variation in 1 pass rather than 2-3 random explorations.

```python
# After a successful Veo generation, extract and log the seed:
result = sr.json()
seed_used = result.get("seed")   # capture from response if returned
# Log to SQLite: shot_id, model, seed, prompt, cost, qa_score

# On retry with minor prompt change, reuse the seed:
"seed": seed_used,   # add to the submission payload
```

**Seed strategy:**
- Seed confirmed in approved shot → log it as the "golden seed" for that scene type
- Minor prompt revision (fix a word, add "eases to stop") → reuse golden seed
- Significant prompt change (different motion or camera) → omit seed, let model explore freely
- If Veo API doesn't return seed in response, record the submission seed from your payload

## Unverified Fallback Models — Canary Required

### Veo 3.1 I2V (`google/veo-3.1-i2v`) — NEW 2026-05-06

$0.20/sec = $1.00/5s. 32% cheaper than Kling v3 Pro. I2V (image-to-video). No Subject Binding, no face-consistency parameter.

**Use case:** Truck-only and product shots where character face identity lock is NOT needed. Wide establishing shots with minor character presence at distance.

**Canary test:**
1. Submit one 5s I2V call with a truck hero frame, standard truck prompt
2. Run brand binary checklist: box sealed, logo orange, no ghost driving
3. If passes → route truck-only draft passes to Veo 3.1 I2V (saves $0.46/draft vs Kling Pro)

**DO NOT use for character face close-ups** — no Subject Binding = identity drift risk.

### Veo 3.1 Fast I2V (`google/veo-3.1-i2v-fast`) — NEW 2026-05-17

**PRICING RESOLVED (2026-05-26):** Billing is per-second, NOT flat-rate. Vertex AI charges **$0.10/sec without audio, $0.15/sec with audio**. The "$0.15/clip flat" figure from third-party sources referred to a short audio-OFF test clip (~1s duration), not a flat rate. AIMLAPI typically adds ~1.3× markup → estimated **~$0.13/sec on AIMLAPI = ~$0.65/5s** (audio OFF). Canary step 2 still critical: record actual billing to confirm AIMLAPI's exact markup on this model.

**~$0.13/sec estimated on AIMLAPI** = ~$0.65/5s. 55% cheaper than Kling v3 Pro ($1.46). Same camelCase parameter names as Veo 3.1 Lite: `aspectRatio`, `durationSeconds`, `generateAudio: false`, `enhancePrompt: false`. Has `image_url` for I2V. No Subject Binding, no face-consistency.

**Use case:** Truck/product shots and B-roll with an anchor image — cheaper than Veo 3.1 Standard I2V at same estimated $0.65/5s but with 2× speed. Replacing Kling v3 Standard 3s drafts (also $0.65) with a 5s clip at potentially equal cost.

**Canary test:**
1. Submit one 5s I2V call to `google/veo-3.1-i2v-fast` with truck hero frame, `generateAudio: false`, `aspectRatio: "9:16"`
2. Record actual cost from AIMLAPI dashboard — determine if billing is per-second (~$0.13/sec) or per-clip (~$0.15 flat)
3. Run brand binary checklist: box sealed, logo orange, no ghost driving
4. If passes → use as truck-only draft alternative to Kling Standard (same cost, full 5s, higher res)

**DO NOT use for character face close-ups.** Verify pricing before routing production shots.

### Veo 3.1 First+Last Frame Fast (`google/veo-3.1-first-last-image-to-video-fast`) — NEW 2026-05-17

**~$0.13/sec estimated** (Vertex AI $0.10/sec + ~1.3× markup) = ~$0.65/5s. Parameters: `image_url` (first frame), `last_image_url` (last frame), `prompt`. Both standard and Fast variants exist; Fast is the cost-efficient choice.

**Key use case — ghost-driving elimination for truck shots:** Set `image_url` = parked truck hero frame AND `last_image_url` = same image. Model must interpolate between two identical frames → truck stays stationary. Add ambient motion in prompt only ("autumn leaves drift past, sunlight shifts across the hood"). This achieves zero truck movement at ~$0.13/sec without needing Kling's `camera_fixed` + anti-ghost-driving prompt locks.

**Expected savings:** If truck final shot moves from Kling Pro ($1.46/5s) to Veo 3.1 First+Last Fast (~$0.65/5s) = saves $0.81/final truck shot. Over a 3-clip truck sequence: saves ~$2.43.

**Canary test:**
1. Submit 5s call: `image_url` = truck hero, `last_image_url` = same truck hero, prompt = minimal ambient motion only, `generateAudio: false`, `aspectRatio: "9:16"`
2. Verify truck is stationary, box sealed, no ghost driving
3. If passes → route truck final shots here instead of Kling Pro

**CAUTION:** No Subject Binding — do NOT use when character face must appear.

### Veo 3.1 Extend Video — CONFIRMED ON AIMLAPI (2026-06-01)

Two variants confirmed live on AIMLAPI:

| Variant | Model String | Notes |
|---------|-------------|-------|
| Standard | `google/veo-3.1-extend-video` | Full quality |
| Fast | `google/veo-3.1-fast-extend-video` | Lower cost, faster |

**Parameters:**
- `video_url` — URL of an existing Veo 3.1 generated clip to extend
- `prompt` — text describing what happens next (redirects narrative)
- `generateAudio: false` — camelCase, same as other Veo models
- `aspectRatio` — camelCase, "9:16" for vertical
- Processing time: ~3 minutes

**Use case:** Extend an approved Veo 3.1 establishing shot beyond the single-generation 4/6/8s limit. Chain two extensions for a 12-16s master establishing shot from a single reference frame. Preserves visual consistency, motion dynamics, and scene logic from the original clip.

**Cost:** Priced per extension length at the same per-second rate as the base model (~$0.065/sec Lite tier). Cheaper than regenerating a second independent clip.

**Workflow for longer establishing shots:**
1. Generate base Veo 3.1 Lite clip (6s, ~$0.39)
2. QA base clip — if passed, extend via `google/veo-3.1-fast-extend-video` with new `video_url`
3. Merge with FFmpeg: `ffmpeg -i base.mp4 -i extension.mp4 -filter_complex concat final.mp4`

**CANARY REQUIRED before production use.** Verify: (1) `video_url` accepts direct CDN link from prior generation, (2) actual cost per extension, (3) visual continuity at join point.

### Veo 3.1 Reference-to-Video (`google/veo-3.1-reference-to-video`) — AIMLAPI DOCS CONFIRMED (2026-06-01)

Doc page confirmed: `docs.aimlapi.com/api-references/video-models/google/veo-3-1-reference-to-video`. Standard (not Fast) model. Estimated **~$0.40/sec = $3.20/8s run** (WaveSpeedAI confirmed, medium confidence). Parameter: `image_urls` (array, up to 3 reference images). Accepts character reference images to guide identity — Google calls this "Ingredients to Video." No explicit Subject Binding strength parameter.

**Use case assessment:** Too expensive at ~$3.20/8s for draft iterations. May be viable as a final-pass character shot model IF identity lock matches Kling Subject Binding quality — saves zero vs Kling Pro if pricing is correct. SKIP until pricing drops or Kling identity retention degrades. Note: Veo 3.1 FAST does NOT have the multi-reference capability — only standard model.

### Wan 2.7 (`alibaba/wan-2-7-*`) — I2V LIVE on AIMLAPI (2026-05-30)

Wan 2.7 I2V is confirmed live on AIMLAPI. Model string confirmed: `alibaba/wan-2-7-i2v`. Pricing: ~$0.10/sec (updated 2026-05-30; AIMLAPI blog says "from $0.10/sec"). T2V and R2V: in AIMLAPI model database as "Coming Soon" — not yet callable. See full section below.

### Wan 2.6 I2V (`alibaba/wan-2-6-i2v`)

Listed in routing matrix as B-roll fallback. **Price researched 2026-04-26: ~$0.13/sec ($0.65/5s), medium confidence.** Minimum clip is 5 seconds — no 3s option. Useful as a fallback when Veo 3.1 Lite is unavailable: provides I2V capability that Veo lacks, at cost between Veo ($0.52) and Kling Standard ($1.09).

**Canary test before first production use:**
1. Submit one 5s I2V call with a simple scenery prompt, no characters, `"aspect_ratio": "9:16"`
2. Record actual cost and resolution from AIMLAPI response
3. If cost ≤ $0.75/5s and 9:16 confirmed → document as verified

### Wan 2.7 — T2V / I2V / R2V (STATUS UPDATED 2026-06-05)

**STATUS:** I2V and T2V are confirmed live on AIMLAPI. R2V is likely live per naming convention.

**Confirmed live model strings:**
- I2V: `alibaba/wan-2-7-i2v` ✓ (AIMLAPI docs page confirmed, May 13, 2026)
- T2V: `alibaba/wan-2-7-t2v` ✓ (AIMLAPI docs page surfaced in search, **confirmed 2026-06-05**)

**STATUS UPDATE (2026-06-05):** AIMLAPI docs page for Wan 2.7 T2V (`docs.aimlapi.com/api-references/video-models/alibaba-cloud/wan-2.7-image-to-video`) confirmed live. T2V use case: wide establishing shots WITHOUT characters at ~$0.50/5s — more expensive than Veo 3.1 Lite (~$0.33/5s) but provides T2V capability similar to Veo Lite. R2V status:
- R2V: `alibaba/wan-2-7-r2v` — likely live; Wan 2.6 R2V exists at `alibaba/wan-2-6-r2v`; verify `docs.aimlapi.com` before first call

**Pricing (updated 2026-05-30):** ~$0.10/sec flat (AIMLAPI blog: "from $0.10/sec"). Previous $0.08/sec (720p) estimate was below the confirmed rate. Use $0.10/sec for all planning. At 2s: ~$0.20. At 3s: ~$0.30. At 5s: ~$0.50.

**Parameters (confirmed via AIMLAPI docs + research):**
- `model`: `"alibaba/wan-2-7-i2v"`
- `prompt`: scene description
- `image_url`: first frame image URL
- `last_image`: last frame URL — enables **first+last frame pinning** (same as truck hero = ghost-driving elimination)
- `duration`: integer 2-15 seconds (string or int; default 5). **2-second ultra-drafts supported at ~$0.20!**
- `aspect_ratio`: "9:16", "16:9", "1:1", "4:3", "3:4" — 9:16 confirmed
- `audio_url`: optional input audio for synchronized music (NOT audio generation — no surcharge risk)
- NO `generate_audio` parameter — Wan 2.7 I2V does **not** generate audio natively. No audio surcharge.

**Why this is the biggest cost optimization since 3s drafts:**
- Wan 2.7 I2V at ~$0.10/sec vs Kling Standard at $0.218/sec = **54% cheaper per draft**
- At 3s: ~$0.30 vs $0.65 Kling Standard = **saves $0.35/draft**
- At 2s ultra-draft: ~$0.20 vs $0.65 Kling Standard = **saves $0.45/draft** (identity check only — 2s may not catch all motion artifacts)
- 4 Standard drafts per shot: saves $1.40 (3s) or $1.80 (2s) before Pro final
- Character shot 3-pass workflow: $2.06 (2× $0.30 + $1.46) vs $2.76 current — saves $0.70/shot

**First+Last Frame pinning for ghost-driving (NEW — 2026-05-30):**
Set `image_url` = truck hero frame AND `last_image` = same truck hero frame. Model interpolates between two identical frames → truck stays stationary, ambient motion only. Same technique as Veo 3.1 First+Last Fast but at ~$0.10/sec vs ~$0.13/sec. Verify exact `last_image` parameter name in canary.

**R2V character consistency (likely live — CANARY REQUIRED):**
- Accepts up to 5 mixed refs (images, video clips, audio)
- Characters referenced in prompt by slot name: `Image1`, `Image2`, `Video1`
- Measured 80% identity hit rate with multi-image (9-grid) input vs 55% single ref
- Voice cloning from 1-10s audio ref — supports Arabic/Dutch accents
- No explicit Subject Binding strength parameter (unlike Kling's 0-100 slider)
- R2V character binding could reduce NBP Edit + Kling Subject Binding to a single call — high priority canary

**Canary test sequence (updated 2026-06-05):**
1. I2V truck: One 5s call to `alibaba/wan-2-7-i2v` with truck hero frame, `aspect_ratio: "9:16"`. Run brand binary checklist: box sealed, no ghost driving, logo orange. Record actual cost (expect ~$0.50 — verify $0.10/sec).
2. I2V first+last: Same call but also pass `last_image` = same truck hero. Verify truck is stationary.
3. I2V character: One 3s call with character hero frame + prompt. QA identity retention and Shari'ah compliance.
4. If all pass → route Kling Standard 3s draft passes to Wan 2.7 I2V. **Log actual cost.**
5. **T2V (confirmed live):** Run one 5s T2V call to `alibaba/wan-2-7-t2v`, wide establishing prompt, no characters. Verify 9:16 output and actual billing (~$0.50). If passes → use for T2V establishing shots where Veo 3.1 Lite is unavailable.
6. **R2V (likely live):** Check `docs.aimlapi.com` for `alibaba/wan-2-7-r2v` doc page. If confirmed, run R2V canary: one 5s call with character hero frame as `Image1`, prompt referencing `Image1`. QA identity retention vs NBP Edit baseline.

**Do NOT use for character finals until R2V canary clears.** Kling Pro with Subject Binding 80-90 remains the final-pass standard.

**Wan 2.6 pricing resolved (2026-05-15):** $0.07/sec is the **720p rate**; $0.13/sec is the **1080p rate**. Both figures were correct — they reflect resolution tiers, not conflicting data. AIMLAPI's listed $0.13 is for 1080p. Use 720p ($0.07/sec, $0.35/5s) for all B-roll and fallback use cases.

### Kling 2.6 Pro I2V (CANARY REQUIRED)

Older model at **~$0.091/sec ($0.46/5s)** — 58% cheaper than Kling v3 Standard. Not yet in routing matrix.

**Potential use:** Truck shots and product-only shots where character identity retention is not needed. NOT recommended for character face shots without validation.

**Canary test:**
1. Generate one 5s truck I2V using the standard truck hero frame
2. Run brand binary checklist: cargo box sealed? logo color correct? no ghost driving?
3. If all pass → route truck-only shots to Kling 2.6 Pro during draft phase
4. Savings: $0.63/truck draft (vs $1.09 Kling v3 Standard)

### LTXV 2 Fast (`ltxv/ltxv-2-fast`) — CONFIRMED LIVE on AIMLAPI 2026-05-22

Lightricks open-source model, confirmed available on AIMLAPI. **Cheapest non-character I2V option for 6s+ clips.**

**Pricing: $0.04/sec at 1080p** → 6s = **$0.24**, 8s = $0.32, 10s = $0.40. 1440p = $0.08/sec. 2160p = $0.16/sec.

**Model strings (AIMLAPI confirmed):**
- I2V: `ltxv/ltxv-2-fast`
- Standard (slower, higher quality): `ltxv/ltxv-2`

**Parameters:**
- `image_url` — anchor frame for I2V (snake_case like Kling, NOT camelCase like Veo)
- `prompt` — scene description
- `aspect_ratio: "9:16"` — vertical output (snake_case confirmed)
- `duration` — 6-20 seconds with frame-level precision (MINIMUM 6s — no 5s option)
- `resolution: "1080p"` — default; also supports 1440p, 2160p at higher cost
- `generate_audio: false` — CRITICAL: disable audio (snake_case, same as Kling; audio defaults ON)
- `seed` — supported for reproducibility

**Use case:** Non-character B-roll, establishing shots, truck exterior without character. I2V capability gives it a composition advantage over Veo 3.1 Lite T2V (which is T2V only). DO NOT use for character face shots — no Subject Binding equivalent.

**Duration-based routing vs competitors (6s clip):**
- LTXV 2 Fast 6s at 1080p: **$0.24** ← cheapest 6s option
- Hailuo 2.3 Fast 6s at 1080p: $0.25
- Hailuo 02 6s at 1080p: $0.28 (flat)
- Veo 3.1 Lite 720p 6s: ~$0.39

**Canary checklist (run before production use):**
1. Submit one 6s I2V call: `ltxv/ltxv-2-fast`, truck hero frame, `aspect_ratio: "9:16"`, `generate_audio: false`
2. Verify actual cost ~$0.24 from AIMLAPI dashboard
3. Run brand binary checklist: box sealed, no ghost driving, logo color correct
4. Compare motion quality vs Hailuo 2.3 Fast on same scene
5. If passes → route 6-9s non-character shots to LTXV 2 Fast (saves $0.01-0.15/clip vs alternatives)

---

### Luma Ray Flash 2 (`luma/ray-flash-2`) — NEW on AIMLAPI, CANARY REQUIRED (2026-06-05)

**AIMLAPI docs page confirmed:** `docs.aimlapi.com/api-references/video-models/luma-ai/luma-ray-flash-2`

**Pricing: ~$0.048/sec** (AIMLAPI: $0.002/M pixels — 4× cheaper than Ray 2's $0.008/M pixels). At 5s: ~$0.24. At 4s: ~$0.19.

**Parameters:**
- `model`: `"luma/ray-flash-2"` — AIMLAPI endpoint `https://api.aimlapi.com/v2/video/generations`
- `prompt`: scene description
- `image_url`: first frame for I2V
- `last_frame_url` or `last_image_url`: last frame (supports first+last keyframe lock — verify param name in canary)
- `aspect_ratio: "9:16"` — vertical output confirmed supported
- **No `generate_audio` parameter** — Ray Flash 2 generates silent video only, no audio surcharge risk
- Duration: up to 9 seconds, 720p

**Strengths vs alternatives:**
- Supports I2V (unlike Veo 3.1 Lite T2V) — can animate a truck hero frame as B-roll
- First+last frame lock available — ghost-driving elimination technique applies
- No audio surcharge risk — no parameter needed, always silent
- Max 9s clips — longer than Hailuo 2.3 Fast without per-second penalty

**Cost position vs non-character alternatives (5s clip):**
- Hailuo 2.3 Fast: $0.208 ← cheapest 5s
- Luma Ray Flash 2: ~$0.24 — 15% more but provides I2V + first+last frame capability
- LTXV 2 Fast: $0.24 at 6s min (not available at 5s)

**Use case:** Non-character I2V shots (truck exterior, establishing, B-roll from hero frame) where Hailuo 2.3 Fast quality is insufficient. First+last frame truck-lock is a direct alternative to Wan 2.7 I2V truck technique at similar cost.

**NOT for character face shots** — no Subject Binding equivalent.

**Canary checklist:**
1. Submit one 5s I2V call: `luma/ray-flash-2`, truck hero frame, `aspect_ratio: "9:16"`, no audio param
2. Verify actual cost ~$0.24 from AIMLAPI dashboard (confirm $0.002/M pixels billing)
3. Run brand binary checklist: box sealed, no ghost driving, logo orange
4. Test first+last frame lock: same truck image as start and end — verify truck stays stationary
5. If passes → use as I2V alternative to Hailuo 2.3 Fast for 5s non-character shots

---

### Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`) — PRICING CORRECTED 2026-05-19

**Confirmed pricing: $0.416/10s flat = $0.0416/sec.** Prior estimate of ~$0.08/sec was wrong. Resolution: **1080p 24fps** (not 768p as previously noted — full Hailuo 2.3 family is 1080p).

**Key cost position (UPDATED 2026-06-05):**
- At 5s: **$0.208** — cheapest non-character 5s clip in pipeline
- At 6s: $0.250 — vs LTXV 2 Fast $0.24 (LTXV wins by $0.01 after canary)
- At 10s: $0.416 — vs LTXV 2 Fast $0.40 (LTXV wins by $0.016); Hailuo 02 costs $0.728 (worst option)
- **Limitation:** T2V only — no I2V capability. For I2V 5s non-character shots, use Luma Ray Flash 2 (~$0.24, canary) instead.

**Quality:** 80-90% of Hailuo 2.3 standard. "Major improvements in physical actions, stylization, and subtle character expressions." Suitable for B-roll and establishing shots. No character face shots.

**Routing rule (updated 2026-06-05):** Use Hailuo 2.3 Fast for 5s non-character T2V clips. Use Luma Ray Flash 2 for 5s non-character I2V clips (canary). Use LTXV 2 Fast for 6s+ clips after canary. Hailuo 02 is NOT recommended (per-second billing on AIMLAPI makes it uncompetitive at all durations).

---

### Kling 3.0 = Kling v3 (CONFIRMED — same model, 2026-06-01)

**`klingai/video-v3-pro-image-to-video` IS Kling 3.0 Pro.** Kuaishou calls it "Kling 3.0"; AIMLAPI surfaces it as "v3." They are the same model — confirmed via cross-referencing AIMLAPI model page (`aimlapi.com/models/kling-video-v3-pro`) and Kuaishou's Feb 5, 2026 release. No string change needed; we are already on Kling 3.0. Features: first+last frame control, physics-aware motion, native 1080p up to 15s, up to 15s duration.

**Kling O3 (= Kling 3.0 Omni) is a separate, premium model** — released Feb 2026, optimized for multi-shot storytelling (up to 6 shots, 15s total in one pass). Available on fal.ai; **NOT confirmed on AIMLAPI** as of 2026-06-01. Not cost-efficient for our single-clip workflow (pricing higher than v3 Pro).

Note: "Kling v4" does not exist. Our production strings remain `klingai/video-v3-pro-image-to-video` (final) and `klingai/video-v3-standard-image-to-video` (draft).

---

### Seedance 2.0 (`bytedance/seedance-2-0`) — AIMLAPI DOCS CONFIRMED, CANARY REQUIRED

**Status (2026-05-26, updated 2026-06-03):** Two variants confirmed on AIMLAPI.

| Variant | Model String | AIMLAPI Price | Cost/5s |
|---------|-------------|---------------|---------|
| Seedance 2.0 Standard | `bytedance/seedance-2-0` | **$0.316/sec** | **$1.58** |
| Seedance 2.0 Fast | `bytedance/seedance-2-0-fast` | **$0.182/sec** | **$0.91** |

**The $0.06 example in AIMLAPI docs is misleading** — it reflects a ~0.2s test generation, not a 5s clip rate. The confirmed standard price is $0.316/sec (same as old Seedance 1.5 Pro). Seedance 2.0 Fast at $0.182/sec is cheaper than Kling Standard ($0.218/sec) but still has face content-policy block risk from Seedance 1.5.

**Resolution update (2026-06-03):** The 720p cap noted in the Farouq directive (2026-04-16) was a Seedance 1.x/Lite limitation. Seedance 2.0 supports 480p/720p/1080p natively. **This does not lift the Farouq ban** — the ban is on face content-policy block risk (3 prior failures), not on resolution. Seedance 2.0 remains prohibited for character shots. The resolution upgrade is only relevant if Farouq explicitly lifts the ban in the future.

**Multimodal:** up to 9 image + 3 video + 3 audio refs per request. Max 15s clip. Released February 9, 2026.

**Use case for Seedance 2.0 Fast only:** Character draft shots if face content-policy blocks prove absent. At $0.91/5s vs Kling Standard $1.09/5s → 17% cheaper per 5s draft. At 3s: ~$0.546 vs $0.65. Not as cheap as Wan 2.7 I2V (~$0.24/3s) if Wan 2.7 canary passes.

**Canary test for Seedance 2.0 Fast (if Wan 2.7 I2V fails canary):**
1. Submit one 5s I2V call with `bytedance/seedance-2-0-fast`, one character ref image, `aspect_ratio: "9:16"`, no audio flag
2. Check actual `usd_spent` from response — confirm ~$0.91
3. Run brand binary checklist + Shari'ah compliance check. Monitor for face content-policy blocks.

**Standard variant ($0.316/sec) is more expensive than Kling Pro ($1.46) — do NOT use. Fast variant needs canary before production.**

---

### NB2 Edit (`google/nano-banana-2`)

Draft-tier image model. Google official rate: **$0.08/image at 1K** ($0.045 at 512px, $0.12 at 2K, $0.151 at 4K). Ranked best for character-locked generation — face, clothing, accessories stable across scenes (confirmed Atlas Cloud benchmark). AIMLAPI may charge flat or tiered — canary test to verify actual price.

**Canary test (3 steps, one API call):**
1. Call `google/nano-banana-2` with 1 ref image, 9:16, simple prompt
2. Verify: response has `data[0].url`, aspect ratio is 9:16, cost logged from AIMLAPI dashboard
3. If cost ≤ $0.10 → unlock as draft tier for prompt iteration before NBP Edit finals

**Expected savings if canary passes:** $0.115/iteration image ($0.195 NBP → ~$0.08 NB2 at 1K). Over 5 hero frame iterations = $0.575 saved per shot's iteration phase.

## Rules

1. **MUST generate ONE at a time. MUST NOT batch multiple without confirmation.**
2. Log every generation with model, cost, and QA score in SQLite
3. If a shot fails QA 3 times → STOP, escalate to owner with failure details
4. Verify correct image is selected before ANY Kling I2V generation
5. Always use Kling I2V (not T2V) for character and truck shots — preserves hero frame
6. Use Veo 3.1 Lite T2V for wide shots with NO characters — 2.8x cheaper than Kling Pro
7. Draft with Kling Standard **at 3s**, final with Kling Pro at 5s — never use Pro for iteration passes
8. Track per-model success rates in learned_preferences — route future shots to most efficient model
9. AIMLAPI defaults `generate_audio: true` for Kling v3 Pro — **ALWAYS explicitly pass `generate_audio: false`**
10. Veo 3.1 Lite: **ALWAYS** set `enhancePrompt: false` — AI enhancement overrides brand prompt details
11. **Polling status checks are FREE on AIMLAPI** — tokens consumed only on generation submission. Poll every 10s without cost concern.
12. **No batch discount exists on AIMLAPI.** All cost savings come from model selection and clip duration management only.
13. **Negative prompts for Kling I2V: 5-8 terms maximum.** Kling weights earlier terms more heavily — longer lists dilute effectiveness. Drop terms below 5-8 and move the strongest failure-prevention terms first. Confirmed via 2026 prompt engineering benchmarks.
14. **Reduce element count before retrying a failed shot.** Complexity overload is a primary Kling I2V failure mode. If a shot fails, remove one moving element from the prompt before changing model or cfg_scale.
15. **Hailuo 02 has NO audio generation** — no `generate_audio` parameter required. Safe to call without audio flags. For Kling, AIMLAPI still defaults audio ON — `generate_audio: false` remains mandatory on all Kling calls. NOTE: Hailuo 02 is $0.0728/sec on AIMLAPI — do NOT use for production shots.
16. **Kling v3 = Kling 3.0 (CONFIRMED 2026-06-01).** `klingai/video-v3-pro-image-to-video` is Kling 3.0 Pro. No string change needed — we are already using the correct model. Kling O3 (Kling 3.0 Omni) is a separate premium model (multi-shot, up to 6 shots/pass); NOT confirmed on AIMLAPI. Do NOT use for single-clip production shots.
17. **Hailuo 02 pricing CORRECTED (2026-05-23): $0.0728/sec on AIMLAPI** — NOT $0.28/clip flat (the flat price was fal.ai). At $0.437/6s and $0.728/10s, Hailuo 02 is the most expensive non-character video option on AIMLAPI. Do NOT use. Route to LTXV 2 Fast ($0.04/sec) or Hailuo 2.3 Fast ($0.0416/sec) instead.
18. **Non-character routing by duration (updated 2026-05-23):** 5s → Hailuo 2.3 Fast ($0.208). 6-10s → LTXV 2 Fast ($0.04/sec, $0.24/6s, $0.40/10s) after canary. Hailuo 02 removed from routing — $0.0728/sec makes it uncompetitive. AIMLAPI string: `minimax/hailuo-2.3-fast`, `ltxv/ltxv-2-fast`.
19. **Wan 2.7 I2V and T2V are now LIVE on AIMLAPI. R2V is likely live.** I2V: `alibaba/wan-2-7-i2v` (confirmed). T2V: `alibaba/wan-2-7-t2v` (AIMLAPI docs confirmed 2026-06-05). R2V: `alibaba/wan-2-7-r2v` (likely live — Wan 2.6 R2V precedent; verify docs page). All at ~$0.10/sec. NO `generate_audio` param on any Wan 2.7 variant. T2V use case: wide establishing shots without characters (~$0.50/5s, more expensive than Veo Lite ~$0.33 but usable when Veo unavailable). CANARY REQUIRED for T2V and R2V before production.
20. **LTXV 2 Fast is live on AIMLAPI (`ltxv/ltxv-2-fast`).** $0.04/sec at 1080p. Minimum 6s clip. Parameters are snake_case (`aspect_ratio`, `generate_audio: false`). CANARY REQUIRED before production use. For 6s+ non-character shots, this is the lowest-cost option pending canary pass.
21. **Seedance 2.0 pricing confirmed (2026-05-26): Standard = $0.316/sec ($1.58/5s), Fast = $0.182/sec ($0.91/5s).** The $0.06/generation in AIMLAPI docs example was a misleading short-clip artifact. Standard is MORE expensive than Kling Pro ($1.46/5s) — never use. Fast (`bytedance/seedance-2-0-fast`) at $0.91/5s is cheaper than Kling Standard ($1.09/5s) but still more expensive than Wan 2.7 I2V (~$0.40/5s). Face content-policy block risk from Seedance lineage applies. CANARY REQUIRED before use. Only consider Fast variant if Wan 2.7 I2V canary fails.
22. **Wan 2.7 I2V (`alibaba/wan-2-7-i2v`) is the cheapest confirmed character-draft candidate on AIMLAPI** at ~$0.10/sec (updated 2026-05-30). 3s draft = ~$0.30 vs Kling Standard 3s = $0.65 — 54% savings. 2s ultra-draft = ~$0.20 — 69% savings (use for identity spot-checks only). No audio surcharge. First+last frame truck-lock available. CANARY REQUIRED. Do not use for finals — Kling Pro with Subject Binding 80-90 remains required. R2V supports up to 5 mixed refs (image/video/audio) with character binding — relevant for character consistency once verified.
23. **Hailuo 2.3 Standard ≠ Fast (confirmed 2026-06-01):** Standard = `minimax/hailuo-2.3` at $0.0728/sec ($0.728/10s) — same price as Hailuo 02, do NOT use. Fast = `minimax/hailuo-2.3-fast` at $0.0416/sec ($0.416/10s) — this is the routing target for 5s non-character T2V clips. Always use `-fast` suffix; standard variant is uncompetitive.
24. **Veo 3.1 Extend Video confirmed on AIMLAPI (2026-06-01):** `google/veo-3.1-extend-video` (Standard) and `google/veo-3.1-fast-extend-video` (Fast). Takes `video_url` of existing Veo 3.1 clip + new `prompt`. Use to extend approved establishing shots beyond single 4/6/8s generation limit. CANARY REQUIRED — verify `video_url` param accepts CDN link, confirm actual per-second cost, check visual continuity at join.
25. **Kling v3 = Kling 3.0 confirmed (2026-06-01).** Our `klingai/video-v3-pro-image-to-video` and `klingai/video-v3-standard-image-to-video` strings are correct and up-to-date — no action needed. Kling O3 (Omni) is a separate premium multi-shot model, NOT on AIMLAPI yet.
26. **Luma Ray Flash 2 confirmed on AIMLAPI (`luma/ray-flash-2`) — NEW 2026-06-05.** ~$0.048/sec (~$0.24/5s). Supports 9:16, I2V, first+last frame keyframes. **No audio generation** — no `generate_audio` param needed, no surcharge risk. Max 9s at 720p. CANARY REQUIRED. Use case: non-character I2V 5s clips where composition anchoring from a hero frame matters (e.g., truck exterior). Hailuo 2.3 Fast ($0.208/5s T2V) remains cheapest for 5s; Ray Flash 2 is the I2V alternative at ~$0.24.
27. **Wan 2.7 T2V confirmed live on AIMLAPI (`alibaba/wan-2-7-t2v`) — 2026-06-05.** AIMLAPI docs page confirmed. Cost: ~$0.50/5s ($0.10/sec). Use for T2V establishing shots without characters when Veo 3.1 Lite is unavailable. Veo 3.1 Lite 720p (~$0.33/5s) is cheaper — prefer Veo. Wan 2.7 T2V is a Veo fallback at higher cost. CANARY REQUIRED before production.
