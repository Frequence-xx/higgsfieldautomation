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

## Model Routing — Updated 2026-05-10

| Shot Type | Image Model | Video Model | Cost/5s clip | Notes |
|-----------|------------|------------|-------------|-------|
| Character close-up | NBP Edit ($0.195) | Kling v3 Pro I2V ($1.46) | **~$1.66** | Subject Binding 80-90, I2V from hero frame |
| Character — draft/iteration | NBP Edit ($0.195) | Kling v3 Standard I2V ($1.09) | **~$1.29** | Use Standard until prompt is dialed in, Pro for final only |
| Wide establishing (no character, draft) | NBP (T2I, $0.13) | Veo 3.1 Lite T2V 720p ($0.26/4s) | **~$0.39** | Draft at 720p 4s — cheapest B-roll |
| Wide establishing (no character, final) | NBP (T2I, $0.13) | Hailuo 02 I2V 6s ($0.44) | **~$0.57** | CANARY REQUIRED — 768p, no char, 9:16 confirmed |
| B-roll / texture (no character) | NBP ($0.13) | Hailuo 02 I2V 6s ($0.44) | **~$0.57** | No audio param needed — no surcharge risk |
| Truck/product (no char, draft) | NBP Edit ($0.195) | Hailuo 02 I2V 6s ($0.44) | **~$0.63** | CANARY REQUIRED — 75% cheaper than Kling Pro |
| Truck/product hero | NBP Edit ($0.195) | Kling v3 Pro I2V ($1.46) | **~$1.66** | cfg_scale 0.7, ghost-driving locks |
| Brand color still (#FC8434) | FLUX.2 Pro ($0.07) | — | $0.07 | HEX matching; T2I only |
| Typography/text still | Flux Kontext Max ($0.10) | — | $0.10 | Best text rendering |
| Money shot / CTA | Flux Pro v1.1 Ultra ($0.10) | Kling v3 Pro I2V ($1.46) | **~$1.56** | Highest quality |

**CRITICAL: Always use I2V (image-to-video) for character shots — I2V preserves hero frame composition.**
**CRITICAL: Veo 3.1 Lite is T2V only (no character). Its `image_url` parameter behavior on AIMLAPI is UNVERIFIED — do NOT use for character or hero-frame animation until tested.**
**CRITICAL: Always generate with audio OFF on ALL models. Audio adds 33–85% surcharge depending on model.**

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
| Wan 2.6 I2V (fallback) | `alibaba/wan-2-6-i2v` | TBD | **~$0.65** ($0.13/sec, min 5s) | — |
| Wan 2.7 I2V/T2V | `alibaba/wan-2-7` | TBD | **~$0.65** ($0.13/sec) | — |
| Kling 2.6 Pro I2V (canary) | `klingai/video-v2-6-pro-image-to-video` | TBD | **~$0.46** ($0.091/sec) | ~$0.27 |
| Hailuo 02 I2V (5s) | `minimax/hailuo-02` | 768p (9:16 ✓) | **$0.36** ($0.0728/sec × 5s) | No audio param — no surcharge |
| Hailuo 02 I2V (6s) | `minimax/hailuo-02` | 768p (9:16 ✓) | **~$0.44** ($0.0728/sec × 6s) | — |
| Hailuo 02 I2V (10s) | `minimax/hailuo-02` | 768p (9:16 ✓) | **$0.73** ($0.0728/sec × 10s) | Longest clip, best value/sec |
| Hailuo 2.3 Fast (canary) | `minimax/hailuo-2.3-fast` | 768p | **~$0.19** (fal.ai; AIMLAPI unverified) | Draft tier candidate |
| Wan 2.7 I2V (canary) | `alibaba/wan-2-7-i2v` | 1080p | **~$0.50** (~$0.10/sec, estimated) | R2V variant for identity lock |

**Veo 3.1 Lite pricing update (2026-05-06):** Resolution-tiered pricing confirmed. 720p: $0.05/sec (Vertex) → ~$0.065/sec on AIMLAPI (estimated, ~1.3× markup). 1080p: $0.08/sec (Vertex) → ~$0.104/sec on AIMLAPI (production-verified ✓). **Use 720p for B-roll drafts — saves ~37% vs 1080p.** Duration valid values: **4, 6, or 8 seconds ONLY** — 5 is invalid. 1080p requires duration=8.

**Veo 3.1 I2V (NEW — 2026-05-06):** `google/veo-3.1-i2v` at $0.20/sec = $1.00/5s — 32% cheaper than Kling v3 Pro ($1.46/5s). No Subject Binding, no character-locking. Suitable for truck/product shots and wide establishing shots where face identity lock is NOT required. DO NOT use for character face close-ups. Canary required before production use.

**Hailuo 02 I2V (NEW — 2026-05-10):** `minimax/hailuo-02` at $0.0728/sec = ~$0.44/6s or $0.73/10s. **75% cheaper than Kling v3 Pro, 67% cheaper than Kling v3 Standard.** I2V (image_url parameter), 9:16 confirmed, 768p resolution, duration 6–10s. **No native audio generation** — no audio parameter, no surcharge risk. No Subject Binding equivalent. Use for B-roll, establishing, and truck-only shots. Canary required before production use — verify quality, 9:16 behavior, and duration parameter format.

**Wan 2.6 note (web research 2026-04-26, medium confidence):** $0.13/sec confirmed from AIMLAPI pricing page snippet. Minimum clip is 5 seconds — no 3s option. Slightly more expensive than Veo 3.1 Lite 720p but provides I2V capability (Veo Lite is T2V only). Use as fallback when Veo is unavailable.

**Wan 2.7 (NEW — 2026-05-06):** Available on AIMLAPI (has dedicated model page). Priced at $0.13/sec — same cost as Wan 2.6 but with improved instruction following and motion quality. Model string unverified on AIMLAPI — canary required. Blog post: https://aimlapi.com/blog/wan-2-7-video-next-generation-ai-video-generation-model

**Kling 2.6 Pro I2V (CANARY REQUIRED):** At $0.091/sec it is 58% cheaper than Kling v3 Standard and 69% cheaper than Kling v3 Pro. Older model generation — quality vs. v3 unverified for character identity retention. Do NOT use on character shots without canary validation. May be appropriate for truck-only shots where identity drift is not a concern.

**AIMLAPI credit discount:** 10% discount auto-applied on every credit top-up purchase. Effective real-world costs are 10% lower than listed prices. Budget planning uses listed prices for conservatism; treat the 10% as a safety buffer.

### Image Models

| Model | AIMLAPI String | Cost/gen | Best For |
|-------|---------------|---------|--------|
| NB2 Edit (DRAFT) | `google/nano-banana-2` | **~$0.07*** | Character draft iterations — CANARY REQUIRED |
| NBP Edit | `google/nano-banana-pro-edit` | **$0.195** (flat) | Character + brand refs (up to 14 refs) |
| NBP (T2I) | `google/nano-banana-pro` | **~$0.13** | Pure scenery, no refs |
| Flux Kontext Max | `flux/kontext-max/image-to-image` | **$0.10** | Typography, character lock |
| FLUX.2 Pro | `blackforestlabs/flux-2-pro` | **$0.07** | Brand color #FC8434 matching |
| Flux Pro v1.1 Ultra | `flux-pro/v1.1-ultra` | **$0.10** | Money shots / CTA |

*NB2: Google's official starting rate is **$0.067/image at 1K**, scaling to $0.151 at 4K. AIMLAPI pricing may differ — run canary test before production use (see "Unverified Models" section below). For 1K hero frames, expected AIMLAPI cost ~$0.067-0.10.

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
- Hailuo 02 6s I2V: ~$0.44 (768p, no audio surcharge)
- Kling v3 Standard 3s draft: $0.65 (720p)
- Hailuo 02 gives 6s output at $0.44 vs Kling Standard 3s at $0.65 — longer clip, 32% cheaper

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
| 2 Establishing shots (Hailuo 02 6s, 1 pass each) | 2 | ~$0.88 |
| Truck: 2 Hailuo 02 6s drafts + 1 Kling Pro 5s final | 3 | ~$2.34 |
| **Total** | | **~$6.76** |

*Savings vs current: $0.32/video on this clip mix. Savings increase significantly if truck hero can also use Hailuo 02 final (pending canary quality check).*
*If truck hero passes on Hailuo 02: 2×$0.44 + 1×$0.44 = $1.32 vs $2.76 Kling — saves $1.44/video.*

**Target: $5.50-7/video with Hailuo 02 for non-character shots + Kling 3s draft tiering for character. $15 ceiling covers ~2 retry passes per clip.**

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

### Wan 2.7 (`alibaba/wan-2-7`) — NEW 2026-05-06

Same pricing as Wan 2.6 ($0.13/sec) but improved instruction following and motion quality. Available on AIMLAPI. Model string unverified — check AIMLAPI model page for exact string. Potential drop-in replacement for Wan 2.6 fallback with better output quality at same cost.

**Canary test:** One B-roll generation with scenery prompt, verify model string, cost, and resolution.

### Wan 2.6 I2V (`alibaba/wan-2-6-i2v`)

Listed in routing matrix as B-roll fallback. **Price researched 2026-04-26: ~$0.13/sec ($0.65/5s), medium confidence.** Minimum clip is 5 seconds — no 3s option. Useful as a fallback when Veo 3.1 Lite is unavailable: provides I2V capability that Veo lacks, at cost between Veo ($0.52) and Kling Standard ($1.09).

**Canary test before first production use:**
1. Submit one 5s I2V call with a simple scenery prompt, no characters, `"aspect_ratio": "9:16"`
2. Record actual cost and resolution from AIMLAPI response
3. If cost ≤ $0.75/5s and 9:16 confirmed → document as verified

### Wan 2.7 — T2V / I2V / R2V (CANARY REQUIRED)

Three video variants confirmed on AIMLAPI blog (model strings medium confidence — derived from naming convention, docs blocked):
- T2V: `alibaba/wan-2-7-t2v`
- I2V: `alibaba/wan-2-7-i2v`
- R2V: `alibaba/wan-2-7-r2v`

**R2V (Reference-to-Video) capability:** Accepts up to 5 mixed references (images, video clips, audio files) and extracts identity embeddings simultaneously. Can lock character face geometry + camera motion style + voice sync in one call. If identity retention matches Subject Binding, this could replace Kling for character draft passes.

**I2V first+last frame control:** Wan 2.7 I2V lets you specify both the first AND last frame — model infers the motion between them, keeping subject identity stable. Could reduce ghost-driving by anchoring the end state.

Price: ~$0.10/sec estimated on AIMLAPI (Wan 2.6 is $0.07/sec confirmed; Wan 2.7 may carry a modest premium). If $0.10/sec: 5s = $0.50 vs Kling Pro $1.46 — 66% cheaper for character drafts if quality matches.

**Canary test:**
1. Submit one 5s I2V call to `alibaba/wan-2-7-i2v` with character hero frame — verify 9:16, actual cost, identity retention
2. If I2V passes: test R2V with 3 reference images of the same character — compare identity lock vs Subject Binding
3. If R2V passes → evaluate as Kling Standard replacement for character draft passes (saves ~$0.44/draft pass)

**Wan 2.6 pricing note (2026-05-10):** Research agent found Wan 2.6 priced at $0.07/sec on AIMLAPI — lower than our prior $0.13/sec (medium confidence, April 2026). Discrepancy may reflect AIMLAPI price change or source variation. Verify with a test call before relying on updated price.

### Kling 2.6 Pro I2V (CANARY REQUIRED)

Older model at **~$0.091/sec ($0.46/5s)** — 58% cheaper than Kling v3 Standard. Not yet in routing matrix.

**Potential use:** Truck shots and product-only shots where character identity retention is not needed. NOT recommended for character face shots without validation.

**Canary test:**
1. Generate one 5s truck I2V using the standard truck hero frame
2. Run brand binary checklist: cargo box sealed? logo color correct? no ghost driving?
3. If all pass → route truck-only shots to Kling 2.6 Pro during draft phase
4. Savings: $0.63/truck draft (vs $1.09 Kling v3 Standard)

### NB2 Edit (`google/nano-banana-2`)

Draft-tier image model. Google official rate: **$0.067/image at 1K** (confirmed via web research 2026-04-26). AIMLAPI may charge flat or tiered — canary test to verify.

**Canary test (3 steps, one API call):**
1. Call `google/nano-banana-2` with 1 ref image, 9:16, simple prompt
2. Verify: response has `data[0].url`, aspect ratio is 9:16, cost logged from AIMLAPI dashboard
3. If cost ≤ $0.10 → unlock as draft tier for prompt iteration before NBP Edit finals

**Expected savings if canary passes:** $0.125/iteration image ($0.195 NBP → ~$0.07 NB2). Over 5 hero frame iterations = $0.63 saved per shot's iteration phase.

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
16. **Kling O3 is NOT on AIMLAPI (May 2026).** O3 is available on fal.ai and Runware but not confirmed on AIMLAPI. Do NOT update Kling model strings. Current v3 Pro string `klingai/video-v3-pro-image-to-video` remains correct.
