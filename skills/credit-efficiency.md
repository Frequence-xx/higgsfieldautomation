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
| Wan 2.7 I2V | `alibaba/wan-2-7-i2v` (canary) | 720p/1080p | **~$0.50** ($0.10/sec × 5s) | **~$0.30** (3s) — CANARY REQUIRED |
| Wan 2.7 R2V | `alibaba/wan-2-7-r2v` (canary) | 720p/1080p | **~$0.50** ($0.10/sec × 5s) | Up to 5 mixed refs, 80% identity hit rate |
| Wan 2.7 T2V | `alibaba/wan-2-7-t2v` (canary) | 720p/1080p | **~$0.50** ($0.10/sec × 5s) | CANARY REQUIRED |
| Kling 2.6 Pro I2V (canary) | `klingai/video-v2-6-pro-image-to-video` | TBD | **~$0.46** ($0.091/sec) | ~$0.27 |
| Hailuo 02 I2V (6s) | `minimax/hailuo-02` | 1080p (9:16 ✓) | **$0.28** (flat price/clip) | No audio param — best value 6s |
| Hailuo 02 I2V (10s) | `minimax/hailuo-02` | 1080p (9:16 ✓) | **$0.28** (flat price/clip) | Same price as 6s — **$0.028/sec, cheapest non-char option** |
| Hailuo 2.3 Fast | `minimax/hailuo-2.3-fast` | 1080p 24fps | **$0.0416/sec** ($0.416/10s flat — corrected 2026-05-19) | 5s = $0.208 (cheapest non-char 5s clip) |

**Veo 3.1 Lite pricing update (2026-05-06):** Resolution-tiered pricing confirmed. 720p: $0.05/sec (Vertex) → ~$0.065/sec on AIMLAPI (estimated, ~1.3× markup). 1080p: $0.08/sec (Vertex) → ~$0.104/sec on AIMLAPI (production-verified ✓). **Use 720p for B-roll drafts — saves ~37% vs 1080p.** Duration valid values: **4, 6, or 8 seconds ONLY** — 5 is invalid. 1080p requires duration=8.

**Veo 3.1 I2V (NEW — 2026-05-06):** `google/veo-3.1-i2v` at $0.20/sec = $1.00/5s — 32% cheaper than Kling v3 Pro ($1.46/5s). No Subject Binding, no character-locking. Suitable for truck/product shots and wide establishing shots where face identity lock is NOT required. DO NOT use for character face close-ups. Canary required before production use.

**Hailuo 02 I2V (pricing corrected 2026-05-15):** `minimax/hailuo-02` at **$0.28/clip flat** (6s OR 10s — same price, not per-second billing). **81% cheaper than Kling v3 Pro, 74% cheaper than Kling v3 Standard.** I2V (image_url parameter), 9:16 confirmed, **1080p** native resolution, duration 6s or 10s only. **No native audio generation** — no audio parameter, no surcharge risk. No Subject Binding equivalent. Use for B-roll, establishing, and truck-only shots. Canary required before production use — verify quality, 9:16 behavior, and duration parameter format.

*Prior estimate of $0.0728/sec ($0.44/6s, $0.73/10s) was WRONG — Hailuo 02 uses flat-price billing. At $0.28/10s = $0.028/sec, this is the cheapest non-character video option in the pipeline. 10s clips at 6s price is exceptional value for long B-roll segments.*

**Wan 2.6 note (web research 2026-04-26, medium confidence):** $0.13/sec confirmed from AIMLAPI pricing page snippet. Minimum clip is 5 seconds — no 3s option. Slightly more expensive than Veo 3.1 Lite 720p but provides I2V capability (Veo Lite is T2V only). Use as fallback when Veo is unavailable.

**Wan 2.7 (COMING SOON on AIMLAPI — 2026-05-17 update):** Wan 2.7 T2V, I2V, and R2V are confirmed "Coming Soon" in AIMLAPI docs — not yet live. Do NOT attempt API calls. When released, expected pricing ~$0.13/sec I2V. R2V (Reference-to-Video) accepts up to 5 mixed refs (images, clips, audio). First+last frame I2V also planned. Blog: https://aimlapi.com/blog/wan-2-7-video-next-generation-ai-video-generation-model

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

*GPT Image 2 (NEW — 2026-04-21): AIMLAPI model string `openai/gpt-image-2` confirmed. Medium quality tier at $0.053/img = 3.7× cheaper than NBP Edit. Multi-reference editing supported. Best text rendering of any image model. CANARY REQUIRED before production use — verify ref image quality and 9:16 aspect ratio support.*

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

**Optimized routing (Kling for character, Hailuo 02 for B-roll/truck — after canary pass):**

| Phase | Clips | Cost |
|-------|-------|------|
| Hero frames (4×$0.195 avg) | 4 | $0.78 |
| Character: 2 Standard 3s drafts + 1 Pro 5s final | 3 | $2.76 |
| 2 Establishing shots (Hailuo 02 6s, 1 pass each) | 2 | **$0.56** |
| Truck: 2 Hailuo 02 6s drafts + 1 Kling Pro 5s final | 3 | **$2.02** |
| **Total** | | **~$6.12** |

*Savings vs current ($7.08): $0.96/video on this clip mix (corrected from prior $0.32 — Hailuo 02 flat-price billing changes the math significantly).*
*If truck hero also passes on Hailuo 02 final: 3×$0.28 = $0.84 vs $2.76 Kling — saves $1.92/video. Total ≈ $4.20.*

**Target: $4.50-6.50/video with Hailuo 02 for non-character shots + Kling 3s draft tiering for character. $15 ceiling covers ~2-3 retry passes per clip.**

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

**~$0.13/sec estimated** (Vertex AI price $0.10/sec + ~1.3× AIMLAPI markup) = ~$0.65/5s. 55% cheaper than Kling v3 Pro ($1.46). Same camelCase parameter names as Veo 3.1 Lite: `aspectRatio`, `durationSeconds`, `generateAudio: false`, `enhancePrompt: false`. Has `image_url` for I2V. No Subject Binding, no face-consistency.

**Use case:** Truck/product shots and B-roll with an anchor image — cheaper than Veo 3.1 Standard I2V at same estimated $0.65/5s but with 2× speed. Replacing Kling v3 Standard 3s drafts (also $0.65) with a 5s clip at potentially equal cost.

**Canary test:**
1. Submit one 5s I2V call to `google/veo-3.1-i2v-fast` with truck hero frame, `generateAudio: false`, `aspectRatio: "9:16"`
2. Record actual cost from AIMLAPI dashboard (verify ~$0.13/sec estimate)
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

### Veo 3.1 Reference-to-Video (`google/veo-3.1-reference-to-video`) — NEW 2026-05-17

Standard (not Fast) model. Estimated **~$0.40/sec = $3.20/8s run** (WaveSpeedAI confirmed, medium confidence). Parameter: `image_urls` (array, up to 3 reference images). Accepts character reference images to guide identity — Google calls this "Ingredients to Video." No explicit Subject Binding strength parameter.

**Use case assessment:** Too expensive at ~$3.20/8s for draft iterations. May be viable as a final-pass character shot model IF identity lock matches Kling Subject Binding quality — saves zero vs Kling Pro if pricing is correct. SKIP until pricing drops or Kling identity retention degrades. Note: Veo 3.1 FAST does NOT have the multi-reference capability — only standard model.

### Wan 2.7 (`alibaba/wan-2-7-*`) — CANARY REQUIRED (now live on AIMLAPI — updated 2026-05-19)

Wan 2.7 is now live on AIMLAPI. AIMLAPI model strings unconfirmed — canary required before production. See full section below.

### Wan 2.6 I2V (`alibaba/wan-2-6-i2v`)

Listed in routing matrix as B-roll fallback. **Price researched 2026-04-26: ~$0.13/sec ($0.65/5s), medium confidence.** Minimum clip is 5 seconds — no 3s option. Useful as a fallback when Veo 3.1 Lite is unavailable: provides I2V capability that Veo lacks, at cost between Veo ($0.52) and Kling Standard ($1.09).

**Canary test before first production use:**
1. Submit one 5s I2V call with a simple scenery prompt, no characters, `"aspect_ratio": "9:16"`
2. Record actual cost and resolution from AIMLAPI response
3. If cost ≤ $0.75/5s and 9:16 confirmed → document as verified

### Wan 2.7 — T2V / I2V / R2V (CANARY REQUIRED — now live on AIMLAPI 2026-05-19)

Wan 2.7 full suite launched April 1-6, 2026 and is now confirmed live on AIMLAPI (model page + blog exist). AIMLAPI model strings follow the `alibaba/wan-2-7-{variant}` convention but are not yet canary-validated — test before routing production shots.

**Expected model strings:**
- T2V: `alibaba/wan-2-7-t2v`
- I2V: `alibaba/wan-2-7-i2v`
- R2V: `alibaba/wan-2-7-r2v`

**Pricing confirmed ($0.10/sec across all modes):** At 3s = $0.30, at 5s = $0.50. Previously estimated $0.08/sec at 720p — confirmed higher at $0.10/sec across resolutions.

**Why this is the biggest cost optimization since 3s drafts:**
- Wan 2.7 I2V at $0.10/sec vs Kling Standard at $0.218/sec = **54% cheaper per draft**
- At 3s: $0.30 vs $0.65 Kling Standard = **saves $0.35/draft pass**
- Over a typical 4 Standard drafts per character shot: saves $1.40 before even reaching the Pro final
- Full savings if R2V validates: character shot 3-pass workflow drops from $2.76 to ~$1.36

**R2V character consistency:**
- Accepts up to 5 mixed refs (images, video clips, audio)
- Characters referenced in prompt by slot name: `Image1`, `Image2`, `Video1`
- Measured 80% identity hit rate with multi-image (9-grid) input vs 55% single ref
- Voice cloning from 1-10s audio ref — supports Arabic/Dutch accents
- No explicit Subject Binding strength parameter (unlike Kling's 0-100 slider)

**Canary test sequence (run in order, stop if any fails):**
1. T2V: One 5s call, `aspect_ratio: "9:16"`, scenery prompt, no character. Verify: 9:16 output, actual cost ~$0.50, no garbled text.
2. I2V: One 5s call with truck hero frame. Run brand binary checklist: box sealed, no ghost driving, logo orange.
3. R2V: One 5s call with 2 character ref images. QA identity hit rate and Shari'ah compliance.
4. If all 3 pass → route Kling Standard 3s draft passes to Wan 2.7 I2V. Log verified model strings.

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

### LTXV 2 Fast (`ltxv-2-fast`) — STATUS UNCERTAIN 2026-05-17

AIMLAPI search results indicate LTXV variants may be "Coming Soon" (unverified — docs blocked). The `ltxv-2-fast-image-to-video` model page exists on AIMLAPI but availability is unclear. Lightricks open-source model, 30fps, faster than real-time generation.

Pricing (fal.ai confirmed): **$0.04/sec at 1080p** = $0.20/5s — potentially cheapest non-character B-roll if available on AIMLAPI. AIMLAPI pricing may differ.

**Use case:** Abstract B-roll, environmental motion, scenery, transitions — nothing with character faces. I2V capability (if available) gives it an edge over Veo 3.1 Lite T2V for scene-locked composition.

**Canary test (verify availability first):**
1. Check AIMLAPI model page for `ltxv-2-fast-image-to-video` status before submitting
2. Submit one 5s I2V scenery call, verify model string, actual cost, and 9:16 output
3. Compare quality vs Veo 3.1 Lite 720p ($0.05/sec) for a standard establishing shot
4. If passes at ≤$0.05/sec → cheapest non-character B-roll option in pipeline

---

### Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`) — PRICING CORRECTED 2026-05-19

**Confirmed pricing: $0.416/10s flat = $0.0416/sec.** Prior estimate of ~$0.08/sec was wrong. Resolution: **1080p 24fps** (not 768p as previously noted — full Hailuo 2.3 family is 1080p).

**Key cost position:**
- At 5s: **$0.208** — cheapest non-character 5s clip in pipeline (beats Hailuo 02 flat $0.28)
- At 10s: $0.416 — more expensive than Hailuo 02 ($0.28 flat) → use Hailuo 02 for 10s clips
- Break-even: at 6.7s ($0.28), Hailuo 02 flat price wins; below 6.7s, Hailuo 2.3 Fast wins

**Quality:** 80-90% of Hailuo 2.3 standard. "Major improvements in physical actions, stylization, and subtle character expressions." Suitable for B-roll and establishing shots. No character face shots.

**Routing rule:** Use Hailuo 2.3 Fast for ≤6s non-character clips; use Hailuo 02 for 10s clips.

---

### Kling 3.0 — NEW Feb 2026 (AIMLAPI model string UNCONFIRMED)

Kling 3.0 released February 5, 2026. Features: first+last frame control, physics-aware motion, native 1080p up to 15s. Pricing on fal.ai/EvoLink: ~$0.075–$0.112/sec. **No confirmed AIMLAPI model string** — Kling 3.0 may not yet be on AIMLAPI (Kling 2.6 Pro is the newest confirmed Kling on AIMLAPI). Do NOT update Kling model strings until verified.

Note: "Kling v4" does not exist — Kling 3.0 is the current generation. Our v3 Pro string `klingai/video-v3-pro-image-to-video` remains the correct production model string.

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
15. **Hailuo 02 has NO audio generation** — no `generate_audio` parameter required. Safe to call without audio flags. For Kling, AIMLAPI still defaults audio ON — `generate_audio: false` remains mandatory on all Kling calls.
16. **Kling O3 / Kling 3.0 are NOT confirmed on AIMLAPI (May 2026).** Kling 3.0 exists on fal.ai (Feb 2026). AIMLAPI's newest confirmed Kling is v2.6 Pro. Do NOT update Kling model strings until verified. Current v3 Pro string `klingai/video-v3-pro-image-to-video` remains correct.
17. **Hailuo 02 uses flat-price billing ($0.28/clip) NOT per-second billing.** Both 6s and 10s clips cost $0.28 — always request 10s for maximum value when scene allows. Pricing model is fundamentally different from Kling/Veo.
18. **Hailuo 2.3 Fast routing rule:** Use for ≤6s non-character clips ($0.0416/sec = $0.208/5s, cheaper than Hailuo 02 flat $0.28). Use Hailuo 02 for 10s clips (Hailuo 02 $0.28 flat beats Hailuo 2.3 Fast $0.416/10s). AIMLAPI string confirmed: `minimax/hailuo-2.3-fast`, 1080p 24fps.
19. **Wan 2.7 is now live on AIMLAPI (May 2026).** Run canary before routing production shots. On canary pass: replace Kling Standard 3s drafts with Wan 2.7 I2V 3s ($0.30 vs $0.65 — saves $0.35/draft, 54% cheaper). R2V variant supports 5 mixed refs for character drafts — 80% identity hit rate with multi-image input.
