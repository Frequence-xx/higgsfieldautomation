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
| Wide establishing (no character, T2V — cheapest canary) | NBP (T2I, $0.13) | Krea WAN 14B T2V ($0.033/sec, ~$0.165/5s) | **~$0.295** | CANARY REQUIRED — cheapest T2V on AIMLAPI if quality passes |
| Wide establishing (no character, draft) | NBP (T2I, $0.13) | Veo 3.1 Lite T2V 720p ($0.26/4s) | **~$0.39** | Draft at 720p 4s — cheapest confirmed B-roll |
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
| Kling v3 Std Turbo I2V (canary) | `klingai/video-v3-standard-turbo-image-to-video` | 720p (9:16) | **$0.73** ($0.146/sec est.) | **$0.44** — Last frame OPTIONAL (confirmed June 2026). ✓ SILENT VIDEO by default in single-clip mode (audio only enabled in multi-shot mode). No audio strip needed. CANARY before routing drafts here. |
| Kling v3 Std Turbo T2V (canary) | `klingai/video-v3-standard-turbo-text-to-video` | 720p (9:16) | **$0.73** ($0.146/sec est.) | **$0.44** — T2V variant. Same silent-video behavior as I2V Turbo in single-clip mode. CANARY REQUIRED. |
| Kling v3 Turbo Pro I2V (canary) | `klingai/video-v3-turbo-pro-image-to-video` | **1080p (9:16)** | **$0.91** ($0.182/sec — AIMLAPI pricing page confirmed June 2026) | **$0.546** (3s) — 37% cheaper than v3 Pro ($1.46). ✓ SILENT VIDEO by default in single-clip mode. No audio strip needed. Last frame OPTIONAL. CANARY REQUIRED before routing finals here. |
| Kling v3 Turbo Pro T2V (canary) | `klingai/video-v3-turbo-pro-text-to-video` | **1080p (9:16)** | **$0.91** ($0.182/sec) | T2V variant at 1080p. Same silent-video behavior as Turbo Pro I2V. CANARY REQUIRED. |
| **Kling O1 Image-to-Video (CANARY)** | `klingai/video-o1-image-to-video` | 1080p (9:16) | **$0.73** ($0.146/sec — CORRECTED SC199, was $0.118/SC194) | **$0.44** (3s) — Standard I2V, tag-based subject consistency, up to 7 refs. 33% cheaper than Kling v3 Standard ($1.09/5s). CANARY REQUIRED — verify identity vs NBP Edit baseline before routing character drafts here. |
| **Kling O1 Reference-to-Video (CANARY)** | `klingai/video-o1-reference-to-video` | 1080p (9:16) | **$0.73** ($0.146/sec — CORRECTED SC194, was $0.112) | **$0.44** (3s) — Multi-image identity lock via `image_list` (1-7 refs). 50% cheaper than v3 Pro. Use for character **draft** iterations requiring multi-image identity check. NOT confirmed to match v3 Pro identity quality — canary InsightFace comparison required. |
| **Kling O1 V2V Reference (CANARY)** | `klingai/video-o1-video-to-video-reference` | 1080p (9:16) | **$0.82** ($0.164/sec — SC199) | **$0.49** (3s) — Video-to-video reference mode; uses existing clip + refs for identity lock. Slightly pricier than I2V O1. CANARY REQUIRED. |
| **Kling O1 V2V Edit (CANARY)** | `klingai/video-o1-video-to-video-edit` | 1080p (9:16) | **$0.82** ($0.164/sec — SC199) | **$0.49** (3s) — Video-to-video editing mode. Same price as V2V Reference. CANARY REQUIRED. |
| Kling v3 Standard I2V | `klingai/video-v3-standard-image-to-video` | 720p (9:16) | **$1.09** ($0.218/sec) | **$0.65** |
| Kling v3 Standard T2V | `klingai/video-v3-standard-text-to-video` | 720p (9:16) | **$1.09** ($0.218/sec) | **$0.65** |
| Kling v3 Pro I2V | `klingai/video-v3-pro-image-to-video` | 1080p (9:16) | **$1.46** ($0.291/sec) | $0.87 |
| Kling v3 Pro T2V | `klingai/video-v3-pro-text-to-video` | 1080p (9:16) | **$1.46** ($0.291/sec) | $0.87 |
| Veo 3.1 Lite T2V 720p (audio OFF — always use) | `google/veo-3-1-lite-generate-preview` | 720p (default) | **~$0.234** (~$0.039/sec AIMLAPI est.; $0.03/sec native CONFIRMED SC290 — OpenRouter + costgoat + MaxVideoAI + buildfastwithai converge) | ~$0.156 (4s), ~$0.312 (8s) |
| Veo 3.1 Lite T2V 720p (audio ON — reference only) | same | 720p | ~$0.39 ($0.065/sec AIMLAPI est.) | — NEVER USE (audio defaults ON = Shari'ah risk) |
| Veo 3.1 Lite T2V 1080p (audio OFF est.) | `google/veo-3-1-lite-generate-preview` | 1080p (requires dur=8) | **~$0.52** (~$0.065/sec AIMLAPI est. × 8s; audio-off 1080p native ~$0.05/sec unconfirmed) | — |
| Veo 3.1 I2V | `google/veo-3.1-i2v` | 720p/1080p | **~$1.00** ($0.20/sec × 5s) | ~$0.60 (3s) |
| Veo 3.1 Fast I2V (canary) | `google/veo-3.1-i2v-fast` | 720p/1080p | **~$0.65** (~$0.13/sec est.) | ~$0.39 (3s) |
| Veo 3.1 First+Last Fast (canary) | `google/veo-3.1-first-last-image-to-video-fast` | 720p/1080p | **~$0.65** (~$0.13/sec est.) | — |
| Wan 2.6 I2V Flash (canary) | `alibaba/wan2.6-i2v-flash` | 720p/1080p | **~$0.033/sec est.** (~$0.165/5s silent 720p) | **CANARY REQUIRED.** Alibaba native: $0.025/sec silent 720p, $0.0375/sec silent 1080p. With AIMLAPI ~1.3× markup → ~$0.033/sec 720p (~$0.165/5s). If AIMLAPI-confirmed: **beats Hailuo 2.3 Fast ($0.208/5s) by 21%**. I2V only. Faster variant of Wan 2.6 I2V. Audio param unclear — canary: try `audio_mode: "mute"` (Wan convention). Log actual AIMLAPI billing. SC255 2026-07-27. |
| Wan 2.6 I2V (fallback) | `alibaba/wan-2-6-i2v` | TBD | **~$0.65** ($0.13/sec, min 5s) | — |
| Wan 2.7 I2V | `alibaba/wan-2-7-i2v` ✓ CONFIRMED | 720p/1080p | **~$0.50** (~$0.10/sec × 5s) | **~$0.30** (3s), **~$0.20** (2s ultra-draft) — model string confirmed, no audio surcharge risk, CANARY REQUIRED |
| Wan 2.7 R2V | `alibaba/wan-2-7-r2v` | 720p/1080p | ~$0.50 est. | **CANARY-TEST RECOMMENDED (SC241/SC240, 2026-07-23).** AIMLAPI blog explicitly states all 4 Wan 2.7 modes (T2V/I2V/R2V/Edit) accessible via AIMLAPI. All third-party providers (Segmind, Replicate, Together AI, Kie.ai, inference.sh, WaveSpeedAI) confirm R2V live. No dedicated docs.aimlapi.com page yet — do NOT assume callable without a canary. Canary: call with `image_urls: [hero_frame_url]`, `aspect_ratio: "9:16"`, `duration: 5`, `audio_mode: "mute"`. If valid job ID returned → R2V live, proceed to InsightFace score (PASS ≥ 0.62). Fallback: `alibaba/wan-2-6-r2v`. Params: `image_urls` (max 3 image-only; ≤ 5 total mixed), `aspect_ratio: "9:16"`, duration 2-10s, `audio_mode: "mute"` (NOT `generate_audio: false`). |
| Wan 2.7 T2V | `alibaba/wan-2-7-t2v` ✓ CONFIRMED | 720p/1080p | **~$0.50** (~$0.10/sec × 5s) | **~$0.30** (3s) — AIMLAPI docs page confirmed 2026-06-05. Use for wide shots without characters. CANARY REQUIRED before production. |
| **Wan 3.0 T2V/I2V/R2V (canary)** | `alibaba/wan3.0-video` | 480p/720p/1080p | **~$0.065/sec 480p; ~$0.13/sec 720p (~$0.65/5s); ~$0.26/sec 1080p — AIMLAPI est.** (Alibaba USD: $0.05/$0.10/$0.20/sec; AIMLAPI 1.3× markup) | ✓ NOW ON AIMLAPI (SC297, confirmed GitHub commit 2026-08-24). **MAX 30s native single-pass clips.** T2V, I2V, first+last frame, R2V (up to 10 images + 5 videos + 5 audio refs). Alt string: `alibaba/wan-3-0-video`. Audio param: `generate_audio` (UNCONFIRMED — canary verify). CANARY REQUIRED. HIGH PRIORITY — R2V 10-ref lock could replace Kling Standard drafts at 40% lower cost. |
| Kling 2.6 Pro I2V (canary) | `klingai/video-v2-6-pro-image-to-video` | TBD | **~$0.46** ($0.091/sec) | ~$0.27 |
| Hailuo 02 I2V (6s) | `minimax/hailuo-02` | 1080p (9:16 ✓) | **$0.437** ($0.0728/sec × 6s) | No audio param — NOTE: $0.28 flat was fal.ai price, AIMLAPI is per-second |
| Hailuo 02 I2V (10s) | `minimax/hailuo-02` | 1080p (9:16 ✓) | **$0.728** ($0.0728/sec × 10s) | NOT the cheapest — Hailuo 2.3 Fast wins at $0.416/10s; DO NOT USE |
| Hailuo 2.3 Fast | `minimax/hailuo-2.3-fast` | 1080p 24fps | **$0.0416/sec** ($0.416/10s flat — corrected 2026-05-19) | 5s = $0.208 — **cheapest non-char clip at ALL durations** (beats LTXV 2 Fast) |
| LTXV 2 Fast I2V | `ltxv/ltxv-2-fast` | 1080p | **$0.052/sec (was CONFIRMED)** | ❌ **BROKEN as of 2026-08-15.** Lightricks removed LTX-2 strings on Aug 15 — `ltxv/ltxv-2-fast` ERRORS on AIMLAPI. AIMLAPI never added replacement string as of SC262 (2026-08-16). Expected new string: `ltxv/ltxv-2-3-fast` (CANARY REQUIRED when/if AIMLAPI adds it). Use Hailuo 2.3 Fast ($0.0416/sec) for all non-char I2V. Watch: **LTX-2.5** released 2026-08-11 (open weights, 22B, I2V + T2V + audio; ltx-2-5-fast/pro on LTX native API) — NOT on AIMLAPI yet. |
| LTXV 2 Standard I2V | `ltxv/ltxv-2` | 1080p | **$0.06/sec (was CONFIRMED)** | ❌ **BROKEN as of 2026-08-15.** Same Lightricks Aug 15 deprecation. String ERRORS on AIMLAPI. Do NOT use. |
| Luma Ray Flash 2 I2V | `luma/ray-flash-2` | 720p (9:16 ✓) | **~$0.048/sec** (~$0.24/5s, AIMLAPI $0.002/M pixels) | No audio generation, no surcharge risk — CANARY REQUIRED. I2V + first+last frame. Max 9s. |
| Grok Imagine Video 1.5 I2V/R2V | `xai/grok-imagine-video` | 720p (9:16 ✓) | **~$0.104/sec 480p** (~$0.52/5s); **~$0.182/sec 720p** (~$0.91/5s) — CORRECTED 2026-06-18. Audio always generated — strip required. WIDE RELEASE June 17. CANARY REQUIRED. |
| Seedance 2.0 Fast | `bytedance/seedance-2-0-fast` | TBD | **$0.316/sec ($1.58/5s — CONFIRMED 2026-06-30)** | **DO NOT USE** — more expensive than Kling Pro ($1.46/5s) at corrected price. Standard = $0.394/sec ($1.97/5s), also DO NOT USE. Face content-policy block risk. |
| MiniMax H3 (Hailuo 3.0) | `minimax/h3` | 2K (2560×1440) | **$0.169/sec** + $0.052/ref image (2K); 768p TBD | ✓ NOW ON AIMLAPI (SC283 2026-08-21). T2V/I2V/R2V/edit; 9-ref lock; 15s max. **DO NOT USE** for non-char shots — Hailuo 2.3 Fast wins at $0.0416/sec. Only viable for 2K or 15s requirements. CANARY REQUIRED (audio disable param unconfirmed). |
| PixVerse V5.5 I2V | `pixverse/v5-5-image-to-video` | 360p-1080p | **$0.156/sec** ($0.78/5s confirmed) | 9:16 ✓; audio optional via `generate_audio_switch: false`; CANARY REQUIRED |
| PixVerse V5.5 T2V | `pixverse/v5-5-text-to-video` | 360p-1080p | **$0.156/sec** ($0.78/5s confirmed) | 9:16 ✓; same price as I2V; CANARY REQUIRED |
| Sora 2 Standard I2V | `openai/sora-2-i2v` | 720p | **~$0.13/sec est.** (~$0.65/5s) | ⚠️ SUNSET Sept 24 2026 (32 days from SC290 Aug 23 — confirmed by OpenAI). Audio ALWAYS generated — no disable param. DO NOT USE. |
| Sora 2 Standard T2V | `openai/sora-2-t2v` | 720p | **~$0.13/sec est.** (~$0.65/5s) | ⚠️ SUNSET Sept 24 2026. Audio ALWAYS generated. DO NOT USE. |

**Non-character video routing (CORRECTED SC126, 2026-06-14 — Hailuo 2.3 Fast is I2V only, NOT T2V):**
- **T2V (no reference image, 4-8s):** Veo 3.1 Lite T2V (`google/veo-3-1-lite-generate-preview`) — 720p ~$0.33/5s (~$0.39/6s). Hailuo 2.3 Fast CANNOT do T2V (Fast variant requires `image_url`).
- **T2V fallback (Veo unavailable):** Wan 2.7 T2V (`alibaba/wan-2-7-t2v`) ~$0.50/5s — CANARY REQUIRED.
- **I2V 5s (anchor frame available):** Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`) $0.208/5s — confirmed cheapest. CANARY REQUIRED. **Watch: Wan 2.6 I2V Flash (`alibaba/wan2.6-i2v-flash`) ~$0.165/5s est. — if canary passes, becomes new cheapest by 21%.**
- **I2V 5s fallback:** Luma Ray Flash 2 (`luma/ray-flash-2`) ~$0.24/5s — CANARY REQUIRED.
- **I2V 6s+:** ❌ LTXV 2 Fast (`ltxv/ltxv-2-fast`) **BROKEN since 2026-08-15 — string ERRORS on AIMLAPI.** Use Hailuo 2.3 Fast ($0.0416/sec = $0.250/6s) or Luma Ray Flash 2 (~$0.24/5s). Expected replacement: `ltxv/ltxv-2-3-fast` — CANARY REQUIRED when AIMLAPI adds it.
- **LTXV 2 Fast was $0.052/sec on AIMLAPI (CONFIRMED 2026-06-14, now defunct).** At 6s: $0.312. Hailuo 2.3 Fast ($0.0416/sec) was already cheaper — now Hailuo 2.3 Fast is the ONLY confirmed I2V 6s+ option.
- **Hailuo 02 and Hailuo 2.3 Standard: DO NOT USE** — $0.0728/sec on AIMLAPI, uncompetitive.

**LTXV 2 Fast — ❌ BROKEN as of 2026-08-15 (SC262):** `ltxv/ltxv-2-fast` NOW ERRORS on AIMLAPI. Lightricks removed LTX-2 strings on Aug 15, 2026 as announced. AIMLAPI did not add `ltxv/ltxv-2-3-fast` before the deadline. Do NOT call this string — it will fail. Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`, $0.0416/sec) is the confirmed fallback for all non-character I2V 5s+ clips. When AIMLAPI adds the replacement string (expected: `ltxv/ltxv-2-3-fast`), run a canary to confirm. **Note:** LTX-2.5 released 2026-08-11 (22B, 4K, 50fps, native audio, I2V in 6.8s on GB200 superchips). NOT on AIMLAPI yet. Third-party unconfirmed prices: $0.09/s 720p, $0.15/s 1080p. Watch for AIMLAPI model string (likely `ltxv/ltxv-2-5-fast`).

**Veo 3.1 Lite pricing update (2026-05-06, updated SC213 2026-07-15, SC290 2026-08-23):** Resolution-tiered pricing confirmed. 720p WITH audio: $0.05/sec (Vertex) → ~$0.065/sec on AIMLAPI. 1080p: $0.08/sec (Vertex) → ~$0.104/sec on AIMLAPI (production-verified ✓). **PRICING UPGRADE — 720p WITHOUT audio (SC290 HIGH CONFIDENCE):** $0.03/sec confirmed by OpenRouter ($0.03/sec direct proxy of Vertex pricing) + costgoat ($0.03/sec), MaxVideoAI ($0.04/sec, likely markup), buildfastwithai, and the official Veo 3.1 Lite model page — all Aug 2026 sources converge on **$0.03/sec at 720p audio-off** (vs $0.05/sec audio-on). Audio-off pricing tier is a Vertex billing split: `generateAudio: false` routes to the cheaper tier. With AIMLAPI ~1.3× markup → **~$0.039/sec on AIMLAPI est. = ~$0.234/6s** (vs previously documented $0.39/6s audio-on rate). **This cuts all B-roll T2V cost by ~40%.** Since we always send `generateAudio: false`, ALL Veo 3.1 Lite clips should hit this cheaper tier. **AIMLAPI billing canary urgently needed** to confirm AIMLAPI splits the audio-off/audio-on tiers identically to Vertex — if confirmed, update budget math. Duration valid values: **4, 6, or 8 seconds ONLY** — 5 is invalid. 1080p requires duration=8. Use 720p for B-roll drafts.

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
| Seedream 5.0 Lite (DRAFT) | `bytedance/seedream-5-0-lite-preview` | **~$0.035** | Cheapest image draft with 14 refs; char identity CANARY REQUIRED — see gen-image.md |
| NB2 Lite (DRAFT) | `google/gemini-3.1-flash-lite-image` | **~$0.044 AIMLAPI** | Non-char T2I/I2I layout drafts — 1K ONLY, 5-ref max, CANARY for param names |
| GPT Image 2 (DRAFT) | `openai/gpt-image-2` | **$0.053** (medium) | Character drafts, text-heavy frames — CANARY REQUIRED |
| NB2 Edit (DRAFT) | `google/nano-banana-2` | **~$0.087 AIMLAPI** ($0.067 native 1K) | Character draft iterations — CANARY to confirm AIMLAPI price |
| NBP Edit | `google/nano-banana-pro-edit` | **$0.195** (flat) | Character + brand refs (up to 14 refs) |
| NBP (T2I) | `google/nano-banana-pro` | **~$0.13** | Pure scenery, no refs |
| Flux Kontext Max | `flux/kontext-max/image-to-image` | **$0.10** | Typography, character lock |
| FLUX.2 Pro | `blackforestlabs/flux-2-pro` | **$0.07** | Brand color #FC8434 matching |
| Flux Pro v1.1 Ultra | `flux-pro/v1.1-ultra` | **$0.10** | Money shots / CTA |
| Wan 2.7 Image Pro (DRAFT) | `alibaba/wan-2-7-image-pro` | **~$0.06** | Draft hero frames, multi-ref identity test — CANARY REQUIRED |
| Wan 2.7 Image (DRAFT) | `alibaba/wan-2-7-image` | **~$0.03** est. | Ultra-cheap T2I draft stills — CANARY REQUIRED |

*Wan 2.7 Image Pro (NEW — 2026-06-09): AIMLAPI model string `alibaba/wan-2-7-image-pro`. ~$0.06/image on AIMLAPI (example in AIMLAPI docs: 120k credits = $0.06); Segmind lists $0.037/image. Reference image parameter: `image_urls` (array, up to 9 refs). Character Locking feature locks facial geometry and clothing across batch generations — up to 9 input refs, up to 12 consistent outputs in one run. 4K native output. **Limitation:** No Subject Binding slider equivalent. Identity lock is architectural (multi-ref embedding), not parametric (no 0-100 strength dial). NOT a replacement for NBP Edit on finals — use for cheap draft iterations only. 69% cheaper than NBP Edit ($0.195 → ~$0.06). Canary: call with one character ref + 9:16 aspect_ratio. Verify actual AIMLAPI cost and compare face consistency vs NBP Edit baseline.*

*Wan 2.7 Image standard (`alibaba/wan-2-7-image`): estimated ~$0.04/image. Cheaper but weaker multi-ref character locking than Pro variant. Best for pure T2I scenery where character identity is not needed.*

*GPT Image 2 (NEW — 2026-04-21, updated 2026-06-03): AIMLAPI model string `openai/gpt-image-2` confirmed live. Medium quality sticker price $0.053/img = 3.7× cheaper than NBP Edit. **However, billing is token-based ($30/M output tokens + $8/M input tokens at high fidelity).** When processing character reference images (mandatory high-fidelity input), actual cost is 2–3× the sticker price — real character reference cost approaches $0.10–$0.42/image. The advantage over NBP Edit ($0.195) shrinks significantly for character work. GPT Image 2 has NO Subject Binding equivalent — does not lock face identity across generations the way NBP Edit does. Best use case remains text-heavy stills (layouts, CTA frames with text) not character hero frames. CANARY REQUIRED — verify 9:16 aspect ratio support and actual billing amount before routing character work here.*

*NB2: Google official rate **$0.067/image at 1K** ($0.045 at 512px, $0.101 at 2K — CORRECTED 2026-06-12, Rule 31). With AIMLAPI ~1.3× markup → ~$0.087/image at 1K estimated. AIMLAPI canary required to confirm actual price. 77% cheaper than NBP Edit ($0.195) at 1K. Full specs in `generation-image.md`.*

*NB2 Lite (`google/gemini-3.1-flash-lite-image`, NEW 2026-06-30 — CONFIRMED on AIMLAPI 2026-07-03): Google's cheapest and fastest image model. ~$0.044/image at 1K on AIMLAPI (native Google $0.034/1K + markup). T2I + I2I + multi-image composition in one API. **5-ref ceiling, 1K ONLY** — NOT for character hero frames. Use for composition/layout drafts (non-character) and B-roll anchor previews before Veo 3.1 Lite T2V. Replaces Gemini 2.5 Flash Image (retiring Oct 2, 2026) as the cheapest non-ref draft tier. Full specs in `generation-image.md`. CANARY REQUIRED for param names beyond `prompt`, `image_urls`, `aspect_ratio`.*

*Seedream 5.0 Lite Preview (`bytedance/seedream-5-0-lite-preview`, CONFIRMED on AIMLAPI — CANARY REQUIRED): ~$0.031–$0.035/image. Up to 14 refs (same slot count as NBP Edit). 9:16 via `size: "9:16"`. 2K default, 3K max. Chain-of-thought reasoning. Cheapest confirmed 14-ref image model — if character identity canary passes, saves $0.052–$0.056/draft iteration vs NB2 Edit. Full specs in `generation-image.md`.*

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

**⚠️ STALE DATA — DO NOT USE HAILUO 02 FOR PRODUCTION:**
- Hailuo 02 6s I2V: **$0.437** ($0.0728/sec × 6s) — NOT $0.28. The $0.28 was fal.ai pricing. AIMLAPI bills per-second.
- At $0.0728/sec, Hailuo 02 is MORE expensive than Kling Pro ($0.291/sec). Worst non-character option on AIMLAPI.
- Use LTXV 2 Fast ($0.04/sec, 6s min) or Hailuo 2.3 Fast ($0.0416/sec) instead. Template above kept for reference only.

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
| Establishing/B-roll (Veo 720p 6s, audio OFF est.) | $0.13 | **~$0.234** est. (Lite 720p 6s, $0.039/sec AIMLAPI est. — pending canary) | **~$0.36** est. |
| Establishing/B-roll (Veo 720p 6s, audio ON documented) | $0.13 | ~$0.39 (Lite 720p 6s, $0.065/sec) | **~$0.52** (reference) |
| Establishing/B-roll (Veo 1080p 8s) | $0.13 | ~$0.83 (Lite 1080p 8s) | **~$0.96** |
| Truck shot (final) | $0.195 | $1.46 (Pro 5s) | **$1.66** |

### Typical video (4 clips: 1 character + 2 establishing + 1 truck):

**Current routing (Kling + Veo):**

| Phase | Clips | Cost |
|-------|-------|------|
| Hero frames (4×$0.195 avg) | 4 | $0.78 |
| Character: 2 Standard 3s drafts + 1 Pro 5s final | 3 | $2.76 |
| 2 Establishing shots (Veo Lite 720p 6s, 1 pass each) | 2 | ~$0.78 (audio-on rate) |
| Truck: 2 Standard 3s drafts + 1 Pro 5s final | 3 | $2.76 |
| **Total** | | **~$7.08** |

**Optimized routing (CORRECTED SC126 — Hailuo 2.3 Fast is I2V only; T2V establishing shots use Veo 3.1 Lite):**

| Phase | Clips | Cost |
|-------|-------|------|
| Hero frames (4×$0.195 avg) | 4 | $0.78 |
| Character: 2 Standard 3s drafts + 1 Pro 5s final | 3 | $2.76 |
| 2 Establishing shots (Veo 3.1 Lite 720p 6s T2V, audio-off est.) | 2 | **~$0.47 est.** (~$0.234×2 est., pending AIMLAPI canary; was $0.78 audio-on) |
| Truck: 2 Kling Std 3s drafts + 1 Kling Pro 5s final | 3 | $2.76 |
| **Total (audio-off canary pending)** | | **~$6.77 est.** (was ~$7.08) |

*Note: If establishing shots have an anchor reference image, use Hailuo 2.3 Fast I2V ($0.25/6s × 2 = $0.50) instead of Veo 3.1 Lite — saves $0.28. Hailuo 2.3 Fast CANNOT do pure T2V (no image). For truck shots with a hero frame, Hailuo 2.3 Fast I2V is also viable at $0.208/5s vs Kling Std $0.65/3s.*

**Super-optimized (Wan 2.7 I2V for character drafts + Hailuo 2.3 Fast I2V for non-char with anchor frame — after canaries pass):**

| Phase | Clips | Cost |
|-------|-------|------|
| Hero frames (4×$0.195 avg) | 4 | $0.78 |
| Character: 2 Wan 2.7 I2V 3s drafts + 1 Kling Pro 5s final | 3 | **$2.06** |
| 2 Establishing shots (Hailuo 2.3 Fast I2V 6s, anchor frame req.) | 2 | **$0.50** |
| Truck: 2 Wan 2.7 I2V 3s + 1 Kling Pro 5s final | 3 | **$2.06** |
| **Total** | | **~$5.40** |

*Establishing shots here assume an anchor image (hero frame) is available for I2V. If no anchor → use Veo 3.1 Lite T2V (~$0.39/6s × 2 = $0.78), which raises total to ~$5.68.*

**Ultra-optimized (2s Wan 2.7 drafts, 2× per shot):**

| Phase | Clips | Cost |
|-------|-------|------|
| Hero frames (4×$0.195 avg) | 4 | $0.78 |
| Character: 2 Wan 2.7 I2V **2s** drafts + 1 Kling Pro 5s final | 3 | **$1.86** |
| 2 Establishing shots (Hailuo 2.3 Fast I2V 6s, anchor frame req.) | 2 | **$0.50** |
| Truck: 2 Wan 2.7 I2V **2s** + 1 Kling Pro 5s final | 3 | **$1.86** |
| **Total** | | **~$5.00** |

*Note: 2s drafts sufficient for identity and motion direction check; may miss artifacts appearing after 2s. Start with 3s drafts; drop to 2s only after workflow is validated.*

*Savings vs baseline ($7.08): SC126 correction — Hailuo 2.3 Fast I2V saves $0.28 vs Veo for shots with anchor frames. $1.68 with Wan 2.7 3s drafts (after canary); $2.08 with Wan 2.7 2s drafts. Hailuo 2.3 Fast T2V was incorrect — it is I2V only.*
*LTXV 2 Fast role: I2V 6s+ anchor shots only ($0.312/6s). Hailuo 2.3 Fast wins at ALL I2V durations where anchor frame exists. For pure T2V: Veo 3.1 Lite.*

**Target: ~$5.40/video (Wan 2.7 3s drafts + I2V anchor) or ~$5.00 (2s drafts) after canaries pass. $15 ceiling covers ~2-3 retry passes per clip.**

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

**STATUS UPDATE (2026-06-14):** Wan 2.7 T2V doc page confirmed live. R2V remains unavailable.

**STATUS UPDATE (SC276 2026-08-19 — CONFIRMED):** R2V is CONFIRMED LIVE on AIMLAPI.
- R2V: `alibaba/wan-2-7-r2v` ✓ CONFIRMED — AIMLAPI models page (`aimlapi.com/models/wan-2-7`) confirms all 4 Wan 2.7 modes live. Blog post "Wan 2.7 Video — Next-Generation AI Video Generation Model" explicitly states "all four modes (T2V, I2V, R2V, and video editing)" accessible via AIMLAPI. Pricing $0.10/sec confirmed across all four modes per multiple sources. `image_urls` max 3 image-only refs (total refs ≤ 5 when mixing images + videos). Duration cap: 2-10s for R2V (NOT 2-15). **Identity quality canary still required** — test InsightFace score ≥ 0.62 vs NBP Edit baseline before routing production character shots here. Wan 2.6 R2V (`alibaba/wan-2-6-r2v`) remains fallback.

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

**R2V character consistency (✓ CONFIRMED ON AIMLAPI — SC276 2026-08-19; identity quality canary still required):**
- `image_urls` (array) — confirmed parameter name from official Alibaba Cloud API docs. NOT `image_list`.
- Max 5 mixed refs total (images + video clips + audio files combined)
- `aspect_ratio: "9:16"` confirmed supported
- `first_frame` (image URL) — optional first-frame anchor; if passed, overrides aspect_ratio
- `audio_url` — voice timbre cloning (1-10s audio clip, NOT audio generation, no surcharge)
- Characters referenced in prompt by slot name: `Image1`, `Image2`, `Video1`
- No `generate_audio` parameter — R2V does NOT generate audio natively
- Measured 80% identity hit rate with multi-image (9-grid) input vs 55% single ref
- No explicit Subject Binding strength parameter (unlike Kling's 0-100 slider)
- R2V character binding could reduce NBP Edit + Kling Subject Binding to a single call — high priority canary once AIMLAPI page appears

**Canary test sequence (updated 2026-07-02):**
1. I2V truck: One 5s call to `alibaba/wan-2-7-i2v` with truck hero frame, `aspect_ratio: "9:16"`. Run brand binary checklist: box sealed, no ghost driving, logo orange. Record actual cost (expect ~$0.50 — verify $0.10/sec).
2. I2V first+last: Same call but also pass `last_image` = same truck hero. Verify truck is stationary.
3. I2V character: One 3s call with character hero frame + prompt. QA identity retention and Shari'ah compliance.
4. If all pass → route Kling Standard 3s draft passes to Wan 2.7 I2V. **Log actual cost.**
5. **T2V (confirmed live):** Run one 5s T2V call to `alibaba/wan-2-7-t2v`, wide establishing prompt, no characters. Verify 9:16 output and actual billing (~$0.50). If passes → use for T2V establishing shots where Veo 3.1 Lite is unavailable.
6. **R2V (✓ CONFIRMED ON AIMLAPI — SC276 2026-08-19):** Model string `alibaba/wan-2-7-r2v` is live. Quality canary: `image_urls: [hero_frame_url_1, hero_frame_url_2]`, `aspect_ratio: "9:16"`, `duration: 5` (max is 10s for R2V — NOT 15), prompt referencing `Image1`. Note `image_urls` max 3 image-only refs (total refs ≤ 5 including video/audio). Verify InsightFace score ≥ 0.62 vs NBP Edit baseline and log actual AIMLAPI cost (~$0.50 expected at $0.10/sec). **R2V duration cap: 2-10 seconds (NOT 2-15 — that limit applies to I2V/T2V only).**

**Do NOT use for character finals until R2V canary clears.** Kling Pro with Subject Binding 80-90 remains the final-pass standard.

**Wan 2.6 pricing resolved (2026-05-15):** $0.07/sec is the **720p rate**; $0.13/sec is the **1080p rate**. Both figures were correct — they reflect resolution tiers, not conflicting data. AIMLAPI's listed $0.13 is for 1080p. Use 720p ($0.07/sec, $0.35/5s) for all B-roll and fallback use cases.

### MiniMax H3 (Hailuo 3.0) — NOW ON AIMLAPI (SC283 2026-08-21)

**Released July 31, 2026. Open weights released Aug 3, 2026 (33B, HuggingFace/ModelScope).** Omni-modal 2K video model — T2V, I2V, R2V, video editing in one model. Accepts up to 9 reference images + 3 reference video clips + 3 audio clips. 15s max clip, 2560×1440 (2K), native stereo audio. Also known as Hailuo 3.0 / Hailuo 03.

**Status on AIMLAPI: NOW CONFIRMED (SC283 2026-08-21).** Model string: `minimax/h3`. Was NOT on AIMLAPI as of 2026-08-19 (SC276); added sometime Aug 19-21. OpenRouter slug: `minimax/hailuo-3`.

**Pricing (AIMLAPI confirmed — SC283 2026-08-21):**
- 2K: **$0.169/sec on AIMLAPI** (5s = $0.845, 10s = $1.69); OpenRouter $0.13/sec; native MiniMax $0.13/sec; AIHubMix $0.124/sec — AIMLAPI adds ~30% markup
- 768p: $0.08/sec native (confirm 768p availability on AIMLAPI; CANARY REQUIRED for 768p model string)
- Reference images: **+$0.052 each on AIMLAPI** (first 5 free on some providers; verify AIMLAPI policy)
- Reference audio: free

**Cost position vs current alternatives (5s clip, AIMLAPI pricing):**
- Hailuo 2.3 Fast 5s: **$0.208** ($0.0416/sec) ← cheapest non-char I2V ✓
- Wan 2.7 R2V 5s: **$0.50** ($0.10/sec, up to 5 mixed refs) — better character lock
- MiniMax H3 2K 5s: **$0.845** + reference image cost — NOT competitive for non-char shots
- **Verdict: DO NOT USE MiniMax H3 for non-character B-roll or establishing shots** — Hailuo 2.3 Fast wins by 4×. H3 is ONLY viable if 2K resolution or 15s max clip duration is specifically required.

**Why to monitor:** 9-ref R2V (character consistency) is unique — H3 accepts more refs than Wan 2.7 R2V (3 image-only max). 15-second max clip length is longest in the pipeline. CANARY REQUIRED before any production use: verify (1) `minimax/h3` model string format, (2) actual per-second billing vs flat-rate, (3) audio disable param (native audio = Shari'ah concern — FFmpeg strip required if no disable param).

---

### FLUX 3 Video — WATCH ITEM, NOT ON AIMLAPI (SC276 2026-08-19; SC290 pass 2 recheck 2026-08-23)

**Released July 23, 2026 (early access); GA August 5, 2026.** Black Forest Labs multimodal model — T2V, I2V, V2V, up to 20-second clips, native audio synchronized in single pass. 1080p GA (2K/4K/open weights coming). Up to 10 reference images accepted. Claims to beat Seedance 2.0.

**Pricing (BFL native API and OpenRouter — audio always included):**
- Draft mode HD T2V/I2V: **$0.06/sec** (5s = $0.30, 20s = $1.20)
- Draft mode HD V2V: $0.12/sec
- Full Quality HD T2V/I2V: $0.17/sec (OpenRouter confirmed $0.17/sec at 720p)
- Full Quality Full HD T2V/I2V: $0.29/sec

**Status on AIMLAPI (SC290 Aug 23, 2026):** NOT on AIMLAPI — pass 2 recheck confirms still not available. Available via BFL native API + fal.ai (`blackforestlabs/flux-3` on fal). Monitor AIMLAPI blog for `blackforestlabs/flux-3-i2v` or `blackforestlabs/flux-3-t2v`.

**⚠️ Audio always generated — cannot disable at generation time.** Audio is an integral part of the model's unified backbone; no `generate_audio: false` equivalent. Production workflow: FFmpeg strip audio immediately after generation (`-an` flag). Extra step but manageable. Price includes audio whether wanted or not — no surcharge per se, just audio generation cost baked in. Monitor whether BFL adds an audio-off pricing tier.

**Cost position (Draft $0.06/s, if/when on AIMLAPI — estimate ~$0.078/s with markup):**
- At 5s: ~$0.39 — worse than Hailuo 2.3 Fast ($0.208) but comparable to Wan 2.7 I2V ($0.50)
- Advantage: up to 20s clips and 10-ref identity lock in one call

**Why to watch:** Draft mode at $0.06/s native (est. ~$0.078/s AIMLAPI) could be cheapest I2V option if confirmed. 10-ref identity lock in draft mode could replace NBP Edit + Kling Standard for character draft iterations. Do NOT assume audio strip removes cost — generation cost is the same with or without audio disable.

---

### Kling 2.6 Pro I2V (CANARY REQUIRED)

Older model at **~$0.091/sec ($0.46/5s)** — 58% cheaper than Kling v3 Standard. Not yet in routing matrix.

**Potential use:** Truck shots and product-only shots where character identity retention is not needed. NOT recommended for character face shots without validation.

**Canary test:**
1. Generate one 5s truck I2V using the standard truck hero frame
2. Run brand binary checklist: cargo box sealed? logo color correct? no ghost driving?
3. If all pass → route truck-only shots to Kling 2.6 Pro during draft phase
4. Savings: $0.63/truck draft (vs $1.09 Kling v3 Standard)

### LTXV 2 Fast (`ltxv/ltxv-2-fast`) — ❌ BROKEN since 2026-08-15, PRICING WAS $0.052/sec

⚠️ **BROKEN — DO NOT CALL.** LTX-2 strings (`ltxv/ltxv-2-fast`, `ltxv/ltxv-2`) were removed by Lightricks on August 15, 2026 and NOW ERROR on AIMLAPI. **AIMLAPI has NOT added a replacement string as of 2026-08-19 (SC276 recheck — no AIMLAPI docs page found for LTX-2.3 or LTX-2.5).** Use Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`, $0.0416/sec) for all non-char I2V. Watch for `ltxv/ltxv-2-3-fast` or `ltxv/ltxv-2-5-fast` to appear on AIMLAPI.

**LTX-2.5 (NEW — 2026-08-11; SC290 pass 40 recheck 2026-08-23):** Open weights + LTX native API. Native pricing: **$0.09/sec (720p), $0.15/sec (1080p), $0.19/sec (2K), $0.37/sec (4K).** Model IDs on LTX native API: `ltx-2-5-fast`, `ltx-2-5-pro`. **NOT on AIMLAPI as of 2026-08-23 (SC290 pass 40 recheck — no AIMLAPI docs page or model database entry found).** When/if added, expected AIMLAPI string: `ltxv/ltxv-2-5-fast` (CANARY REQUIRED). At native 720p ($0.09/s): 5s = $0.45 — more expensive than Hailuo 2.3 Fast ($0.208/5s). No cost advantage at 720p vs Hailuo 2.3 Fast. Features: multi-shot scene consistency, synchronized audio generation (I2V in 6.8s on GB200), supports T2V + I2V + audio-to-video. Generate audio is off by default at LTX native API. Watch for AIMLAPI string.

**LTX-2.3 (intermediate — 2026-07-15 to 2026-08-11):** LTX-2 strings auto-routed to LTX-2.3 during the grace period. LTX-2.3 itself is superseded by LTX-2.5. Expected AIMLAPI strings: `ltxv/ltxv-2-3-fast`, `ltxv/ltxv-2-3` — neither confirmed on AIMLAPI as of 2026-08-18.

Lightricks open-source model, confirmed available on AIMLAPI. **Cheapest non-character I2V option for 6s+ clips where composition anchoring is needed.**

**Pricing: $0.052/sec on AIMLAPI (CONFIRMED 2026-06-14, unchanged July 2026).** fal.ai charges $0.04/sec; AIMLAPI's markup brings it to $0.052/sec. Lightricks native API raised to $0.06/sec after April 1 but fal.ai (and AIMLAPI) kept old rate. 6s = $0.312, 10s = $0.52. 1440p = higher cost.

**Model strings (AIMLAPI confirmed — use until Aug 15):**
- I2V: `ltxv/ltxv-2-fast` (auto-routes to LTX-2.3 quality since 2026-07-15)
- Standard (slower, higher quality): `ltxv/ltxv-2` (same August 15 removal risk)

**Parameters:**
- `image_url` — anchor frame for I2V (snake_case like Kling, NOT camelCase like Veo)
- `prompt` — scene description
- `aspect_ratio: "9:16"` — vertical output (snake_case confirmed)
- `duration` — 6-20 seconds with frame-level precision (MINIMUM 6s — no 5s option)
- `resolution: "1080p"` — default; also supports 1440p, 2160p at higher cost
- `generate_audio: false` — CRITICAL: disable audio (snake_case, same as Kling; audio defaults ON). ✓ Confirmed working with LTX-2.3 routing (2026-07-19)
- `seed` — supported for reproducibility

**LTX-2.3 improvements (via auto-routing since July 15):** 22B parameters (vs LTX-2), better physics and motion quality, native synchronized audio capability (audio-off still supported via `generate_audio: false`). No prompt or parameter changes needed — drop-in.

**Use case:** Non-character I2V shots (6s+ clips) where the anchor frame is needed for composition control. I2V capability gives it a role when Hailuo 2.3 Fast (T2V only) cannot be used. DO NOT use for character face shots or when T2V is sufficient.

**Routing position vs competitors (6s clip, CONFIRMED pricing):**
- LTXV 2 Fast 6s at 1080p: **$0.312** ($0.052/sec CONFIRMED)
- Hailuo 2.3 Fast 6s at 1080p: **$0.250** ($0.0416/sec) — WINS for T2V
- Luma Ray Flash 2 5s at 720p: **~$0.24** — WINS for I2V ≤5s
- LTXV wins only when: I2V required AND clip ≥6s AND Luma Ray Flash 2 unavailable/insufficient

**No further canary required for pricing** — cost is confirmed at $0.052/sec. Canary for quality and parameter verification still recommended before first production use.

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

**Key cost position (CORRECTED SC126, 2026-06-14 — I2V only, requires image_url):**
- At 5s: **$0.208** — cheapest non-character I2V 5s clip in pipeline
- At 6s: $0.250 — vs LTXV 2 Fast $0.312 (Hailuo 2.3 Fast wins for I2V at 6s)
- At 10s: $0.416 — vs LTXV 2 Fast $0.52 (Hailuo 2.3 Fast wins for I2V at 10s); Hailuo 02 costs $0.728 (worst option)
- **CORRECTION (SC126):** I2V only (requires `image_url`) — the Fast variant does NOT support text-to-video. The Standard Hailuo 2.3 model supports both T2V and I2V, but the Fast variant is image-to-video only. Confirmed: official MiniMax/hailuoai.video blog, fal.ai, replicate, veed, modelslab all list Fast as "Image to Video" only. For T2V non-character establishing shots (no reference image), use Veo 3.1 Lite instead.

**Quality:** 80-90% of Hailuo 2.3 standard. "Major improvements in physical actions, stylization, and subtle character expressions." Suitable for B-roll and establishing shots with an anchor frame. No character face shots.

**Routing rule (CORRECTED SC126, 2026-06-14):** Use Hailuo 2.3 Fast for I2V non-character shots where a reference/anchor image exists ($0.208/5s, CANARY REQUIRED). For T2V shots (no reference image), use Veo 3.1 Lite as primary. Luma Ray Flash 2 is I2V fallback if Hailuo 2.3 Fast canary fails. Use LTXV 2 Fast for I2V 6s+ clips. Hailuo 02 is NOT recommended (per-second billing makes it uncompetitive at all durations).

---

### Kling 3.0 = Kling v3 (CONFIRMED — same model, 2026-06-01)

**`klingai/video-v3-pro-image-to-video` IS Kling 3.0 Pro.** Kuaishou calls it "Kling 3.0"; AIMLAPI surfaces it as "v3." They are the same model — confirmed via cross-referencing AIMLAPI model page (`aimlapi.com/models/kling-video-v3-pro`) and Kuaishou's Feb 5, 2026 release. No string change needed; we are already on Kling 3.0. Features: first+last frame control, physics-aware motion, native 1080p up to 15s, up to 15s duration.

**Kling O3 (= Kling 3.0 Omni) is a separate, premium model** — released Feb 2026, optimized for multi-shot storytelling (up to 6 shots, 15s total in one pass). Available on fal.ai; **NOT confirmed on AIMLAPI** as of 2026-06-01. Not cost-efficient for our single-clip workflow (pricing higher than v3 Pro).

Note: "Kling v4" does not exist. Our production strings remain `klingai/video-v3-pro-image-to-video` (final) and `klingai/video-v3-standard-image-to-video` (draft).

**Kling v3 Turbo Series — CONFIRMED ON AIMLAPI (June 17, 2026 launch):** Two tiers on AIMLAPI:
- **Standard Turbo I2V/T2V** (`klingai/video-v3-standard-turbo-image-to-video`, `klingai/video-v3-standard-turbo-text-to-video`): $0.146/sec = **$0.73/5s**. Resolution: 720p. 33% cheaper than Standard ($1.09).
- **Turbo Pro I2V/T2V** (`klingai/video-v3-turbo-pro-image-to-video`, `klingai/video-v3-turbo-pro-text-to-video`): $0.182/sec = **$0.91/5s** — CONFIRMED on AIMLAPI pricing page (June 2026). Resolution: **1080p**. 37.7% cheaper than Kling v3 Pro ($1.46). **NEW — not previously documented.**

**Last frame is OPTIONAL** (confirmed across multiple API providers June 2026 — WaveSpeedAI, Kie.ai): single-frame I2V works on both Turbo tiers. Last frame can also be used for A→B transitions or truck ghost-driving lock (first=last frame technique).

**✓ AUDIO BEHAVIOR CORRECTED (2026-06-21):** Kling 3.0 Turbo generates **SILENT VIDEO by default in single-clip mode.** Prior warning ("audio always generated") was based on multi-shot mode docs and is INCORRECT for single-clip I2V/T2V calls. Audio is only always-enabled in multi-shot mode (not applicable to our AIMLAPI single-clip workflow). No `generate_audio: false` parameter needed. No audio strip required for Shari'ah compliance on Turbo single-clip calls. Canary to confirm: verify downloaded clip has no audio track (`ffprobe -show_streams output.mp4 | grep codec_type=audio` → should return nothing). Standard Kling 3.0 (non-Turbo) and Kling O3 retain native audio generation capability.

**Turbo Pro final-pass savings (if canary passes):** 1 character + 1 truck final: saves ~$1.10/video ($1.46 → $0.91 × 2 clips). Requires InsightFace cosine similarity ≥ 95% vs v3 Pro baseline before routing finals here. Subject Binding (elements parameter) is supported in Turbo Pro (confirmed — "enhanced subject consistency" for faces and brand assets).

**Kling O3/Omni and v3 Motion Control are still NOT on AIMLAPI as of July 2026 (reconfirmed SC227 2026-07-19).** Kling Omni received a June 17 upgrade (4K editing, 3-15s clips, better consistency) but remains unavailable on AIMLAPI. See `generation-video.md` for full Turbo canary checklist and per-tier parameter details.

---

### Seedance 2.0 (`bytedance/seedance-2-0`) — AIMLAPI DOCS CONFIRMED, CANARY REQUIRED

**Status (2026-05-26, updated 2026-06-03):** Two variants confirmed on AIMLAPI.

| Variant | Model String | AIMLAPI Price | Cost/5s |
|---------|-------------|---------------|---------|
| Seedance 2.0 Standard | `bytedance/seedance-2-0` | **$0.394/sec** | **$1.97** |
| Seedance 2.0 Fast | `bytedance/seedance-2-0-fast` | **$0.316/sec** | **$1.58** |

**PRICING CORRECTED 2026-06-30 (AIMLAPI pricing page):**
- Standard (`bytedance/seedance-2-0`): **$0.394/sec ($1.97/5s)** — was incorrectly listed as $0.316/sec
- Fast (`bytedance/seedance-2-0-fast`): **$0.316/sec ($1.58/5s)** — was incorrectly listed as $0.182/sec

**Both variants are NOW MORE EXPENSIVE than Kling Pro ($1.46/5s). DO NOT USE either.** The $0.182/sec figure in prior entries referred to AIMLAPI's Kling v3 Turbo Pro and Happy Horse 1.1 (1080p) — not Seedance.

**Resolution update (2026-06-03):** The 720p cap noted in the Farouq directive (2026-04-16) was a Seedance 1.x/Lite limitation. Seedance 2.0 supports 480p/720p/1080p natively. **This does not lift the Farouq ban** — the ban is on face content-policy block risk (3 prior failures), not on resolution.

**Multimodal:** up to 9 image + 3 video + 3 audio refs per request. Max 15s clip. Released February 9, 2026.

**Standard ($0.394/sec, $1.97/5s) and Fast ($0.316/sec, $1.58/5s) are both more expensive than Kling Pro ($1.46/5s) — DO NOT USE either variant. Use Wan 2.7 I2V ($0.30/3s canary) for cheap character drafts instead.**

---

### Grok Imagine Video 1.5 (`xai/grok-imagine-video`) — WIDE RELEASE June 17, 2026. CANARY REQUIRED (2026-06-18 update)

**Context:** Preview launched June 3, 2026. **WIDE RELEASE: June 17, 2026.** #1 on Image-to-Video Arena (+52 Elo over v1.0). AIMLAPI docs page confirmed: `docs.aimlapi.com/api-references/video-models/xai/grok-imagine-video`. GA model alias: `grok-imagine-video-1.5` (xAI); AIMLAPI string likely still `xai/grok-imagine-video` — verify in canary.

**Pricing (CORRECTED 2026-06-18 — prior entry had v1.0 rates, now showing v1.5 GA rates):**
- xAI API: **$0.08/sec (480p), $0.14/sec (720p)** + $0.01/image input — NOT $0.05/$0.07 (those were v1.0 rates)
- AIMLAPI estimated (~1.3× markup): **~$0.104/sec (480p) = ~$0.52/5s**, **~$0.182/sec (720p) = ~$0.91/5s**
- Audio always included at no extra charge (baked into per-second rate — no parameter to disable)

**ROUTING VERDICT (updated at GA pricing):**
- 480p (~$0.52/5s): More expensive than Hailuo 2.3 Fast ($0.208), Luma Ray Flash 2 (~$0.24), LTXV 2 Fast ($0.26/6s). Not competitive for non-char I2V.
- 720p (~$0.91/5s): Cheaper than Kling Standard ($1.09/5s) but requires mandatory audio strip. Not recommended over Wan 2.7 I2V ($0.30/3s) for character drafts.
- **Best use case if canary passes:** Reference-to-video (up to 7 image refs) for character draft iterations when Wan 2.7 R2V is unavailable on AIMLAPI. At 480p, $0.52/5s is below Kling Standard.

**Why it matters for this pipeline:**
- I2V supported — can animate truck hero frames and B-roll
- First+last frame keyframe control available (ghost-driving lock technique applies)
- Reference-to-video (R2V): up to 7 reference images for character consistency
- Max 15s clip, 24fps, 480p or 720p, 9:16 supported

**Critical blocker — audio always generated:**
- Every Grok Imagine Video generation produces audio (dialogue, SFX, ambient) in a single pass
- **No `generate_audio: false` parameter exists.** Audio cannot be disabled.
- Workaround: `ffmpeg -i input.mp4 -an -c:v copy output.mp4` strips audio post-generation
- Shari'ah compliance: AI-generated audio may include music. **Strip immediately on download — do NOT play audio during QA.** Always deliver with audio stripped.

**NOT text-to-video:** T2V is not available through the Grok Imagine Video API — I2V and R2V only. (Confirmed for both preview and GA release.)

**Canary test before routing production shots:**
1. Submit one 5s 480p I2V call: truck hero frame, `aspect_ratio: "9:16"`, confirm model string from AIMLAPI docs
2. Record actual cost from AIMLAPI dashboard — verify ~$0.52 (480p, 5s; CORRECTED from old ~$0.325 estimate)
3. On download: strip audio immediately (`ffmpeg -i input.mp4 -an -c:v copy output_silent.mp4`)
4. Run brand binary checklist: box sealed, logo orange, no ghost driving
5. If passes → use ONLY when Wan 2.7 I2V and other cheaper non-char options fail canary

---

### NB2 Edit (`google/nano-banana-2`)

Draft-tier image model. Google official rate: **$0.067/image at 1K** ($0.045 at 512px, $0.12 at 2K, $0.151 at 4K — pricing verified March 2026, corrected from prior $0.08 estimate). With AIMLAPI ~1.3× markup → ~$0.087/image at 1K on AIMLAPI. Ranked best for character-locked generation — face, clothing, accessories stable across scenes (confirmed Atlas Cloud benchmark). AIMLAPI may charge flat or tiered — canary test to verify actual price.

**Canary test (3 steps, one API call):**
1. Call `google/nano-banana-2` with 1 ref image, 9:16, simple prompt
2. Verify: response has `data[0].url`, aspect ratio is 9:16, cost logged from AIMLAPI dashboard
3. If cost ≤ $0.10 → unlock as draft tier for prompt iteration before NBP Edit finals

**Expected savings if canary passes:** ~$0.108/iteration image ($0.195 NBP → ~$0.087 NB2 at 1K, AIMLAPI est.). Over 5 hero frame iterations = $0.54 saved per shot's iteration phase.

---

### PixVerse V5.5 (`pixverse/v5-5-image-to-video`, `pixverse/v5-5-text-to-video`) — AIMLAPI CONFIRMED, CANARY REQUIRED (2026-06-12)

**AIMLAPI docs pages confirmed:** `docs.aimlapi.com/api-references/video-models/pixverse/v5-5-image-to-video` and `/v5-5-text-to-video`.

**Pricing: $0.78/5s = $0.156/sec on AIMLAPI** (I2V and T2V same price).

**Parameters:**
- `aspect_ratio`: 9:16 confirmed — vertical output supported
- `resolution`: "360p", "540p", "720p", "1080p" — 1080p limited to 5s or 8s clips; 720p up to 10s
- `generate_audio_switch`: boolean — **set `false` to disable audio** (optional, not forced)
- `duration`: 5, 8, or 10 seconds depending on resolution tier
- Also supports `generate_multi_clip_switch` and `thinking_type` optional params
- Style presets: "anime", "3d_animation", "clay", "comic", "cyberpunk"

**Cost position vs alternatives (5s clip):**
- Hailuo 2.3 Fast (T2V): $0.208 ← cheapest non-char T2V
- Luma Ray Flash 2 (I2V): ~$0.24
- LTXV 2 Fast (I2V, 6s min): $0.24
- **PixVerse V5.5 (I2V or T2V): $0.78** ← NOT competitive for non-character shots

**Character draft position:**
- Wan 2.7 I2V 3s draft: $0.30 ← cheapest character draft (canary)
- **PixVerse V5.5 3s draft: $0.468** ← mid-tier
- Kling v3 Standard 3s draft: $0.65 ← current production draft

At $0.156/sec, PixVerse V5.5 is 28% cheaper than Kling Standard but 56% more expensive than Wan 2.7 I2V. **Not a primary routing target** while Wan 2.7 and LTXV are available. Potential fallback if both Wan 2.7 and LTXV canaries fail.

**Character consistency claims:** "strict character consistency across frames, no identity shift" — stronger than Hailuo or LTXV claims. May be valuable as mid-tier character draft if Wan 2.7 I2V fails.

**Canary checklist (before production use):**
1. Submit one 5s I2V call: `pixverse/v5-5-image-to-video`, character hero frame, `aspect_ratio: "9:16"`, `generate_audio_switch: false`, `resolution: "720p"`
2. Record actual cost from AIMLAPI dashboard — verify $0.78
3. Run brand binary checklist + Shari'ah compliance
4. Compare face identity retention vs NBP Edit baseline
5. If character retention ≥ 80% of Kling Standard → route as fallback draft (after Wan 2.7 I2V fails)

**Note:** PixVerse V5.6 exists (released Jan 2026, supports start+end frame control, 5-15s) but is NOT confirmed on AIMLAPI as of 2026-06-12. Only V5.5 has a confirmed AIMLAPI docs page.

---

### Sora 2 (`openai/sora-2-i2v`, `openai/sora-2-t2v`, `openai/sora-2-pro-i2v`, `openai/sora-2-pro-t2v`) — AIMLAPI CONFIRMED, NOT RECOMMENDED (2026-06-12)

**AIMLAPI docs page confirmed:** `docs.aimlapi.com/api-references/video-models/openai/sora-2-i2v`.

**⚠️ SUNSET: Sora 2 API ends September 24, 2026. Do not build pipeline dependency on this model.**

**OpenAI pricing (Standard tier, per-second):** $0.10/sec (720p). AIMLAPI estimated (~1.3× markup): **~$0.13/sec = ~$0.65/5s**.

**Model strings:**
- `openai/sora-2-i2v` — Standard I2V (720p)
- `openai/sora-2-t2v` — Standard T2V (720p)
- `openai/sora-2-pro-i2v` — Pro I2V ($0.30-$0.70/sec, very expensive)
- `openai/sora-2-pro-t2v` — Pro T2V ($0.30-$0.70/sec, very expensive)

**Critical blockers:**
1. **Audio is always generated** — no `generate_audio` disable parameter. Audio includes dialogue, SFX, soundscapes, lip-sync. Same issue as Grok Imagine Video 1.5. **AUDIO STRIP REQUIRED** immediately on download: `ffmpeg -i input.mp4 -an -c:v copy output.mp4`
2. **Shari'ah compliance risk** — AI-generated audio may include music. Strip before ANY playback.
3. **Sunset September 24, 2026** — pipeline dependency is a 3-month risk.

**Cost verdict:** Sora 2 Standard at ~$0.65/5s = same cost as Kling v3 Standard 3s ($0.65). Not cheaper. Wan 2.7 I2V at $0.30/3s is 54% cheaper for drafts. Pro tier ($0.30-$0.70/sec) is more expensive than Kling Pro.

**Routing decision: NOT recommended for this pipeline.** Forced audio strips, sunset deadline, and no cost advantage over existing models make it a poor fit. Do not canary unless Kling and Wan 2.7 both fail simultaneously.

---

### Veo 3 Fast I2V / T2V (`google/veo-3-fast-image-to-video`, `google/veo-3-fast-text-to-video`) — AIMLAPI DOCS CONFIRMED, CANARY REQUIRED (2026-06-16)

Both Veo 3 Fast variants confirmed on AIMLAPI docs:
- I2V: `docs.aimlapi.com/api-references/video-models/google/veo-3-fast-image-to-video`
- T2V: `docs.aimlapi.com/api-references/video-models/google/veo-3-fast-text-to-video`

**Pricing:** fal.ai charges $0.10/sec (audio off) or $0.15/sec (audio on). AIMLAPI estimated (~1.3× markup): **~$0.13/sec = ~$0.65/5s** (audio off). Audio CAN be disabled — parameter exists (likely `generateAudio: false` — verify in canary).

**Veo 3 Fast vs Veo 3.1 Fast:** Both are confirmed on AIMLAPI and estimated at ~$0.13/sec. **Veo 3.1 Fast is the newer/better model** — prefer Veo 3.1 Fast I2V (`google/veo-3.1-i2v-fast`) over Veo 3 Fast for quality. Veo 3 Fast exists as a fallback if 3.1 Fast is unavailable.

**Do NOT confuse with Veo 3 Standard I2V ($0.788/sec) — 6× more expensive and NOT worth using.**

**Canary test (low priority — Veo 3.1 Fast preferred):**
1. Submit 5s call: `google/veo-3-fast-image-to-video`, truck hero frame, `generateAudio: false`, `aspectRatio: "9:16"`
2. Confirm model string and actual AIMLAPI cost (~$0.65 expected)
3. Run brand binary checklist

---

### Veo 3 Standard I2V (`google/veo-3-image-to-video`) — CONFIRMED ON AIMLAPI, DO NOT USE (2026-06-16)

Confirmed on AIMLAPI docs page: `docs.aimlapi.com/api-references/video-models/google/veo-3-image-to-video`

**Pricing: ~$0.788/sec on AIMLAPI** — confirmed from multiple research sources (120,000 credits for 8s clip example). At 5s = ~$3.94. At 8s = ~$6.30. **6-7× more expensive than Kling v3 Pro ($1.46/5s).** Veo 3 is the full native-audio 4K model — premium pricing for a premium product unsuitable for our per-clip budget.

**DO NOT ROUTE ANY SHOTS HERE.** Cost ceiling of $15/video would be consumed by 2-4 Veo 3 Standard clips alone.

---

### VEED Fabric-1.0 Fast (`veed/fabric-1.0-fast`) — CONFIRMED ON AIMLAPI (2026-06-16)

**AIMLAPI docs page confirmed:** `docs.aimlapi.com/api-references/video-models/veed/fabric-1.0-fast`  
**AIMLAPI model page:** `aimlapi.com/models/veed-fabric-1-0-fast`

**What it does:** Audio-to-Video (A2V) talking-head model. Takes a face image + audio file → generates a lip-synced, talking video. NOT a motion/cinematic model — specialized for character dialogue delivery. Fabric-1.0 Fast is optimized for fast generation; quality is maintained at 720p.

**Pricing:**
- 480p: **$0.08/sec** (~$0.40/5s)
- 720p: **$0.15/sec** (~$0.75/5s)
- 9:16 aspect ratio supported ✓
- Max 30s per clip; clips can be stitched for longer outputs
- Input: image URL (face) + audio URL (MP3/WAV/M4A)
- No `generate_audio` param needed — no audio generation, audio is INPUT not output

**Pipeline use case:** If a shot requires a character to visibly speak to camera (e.g., customer testimonial CTA), pass the NBP Edit hero frame + ElevenLabs voiceover MP3 to Fabric Fast. The result is a lip-synced talking head clip. This is DIFFERENT from our standard cinematic hero shots — use only when direct-to-camera speech delivery is the shot intent.

**Shari'ah compliance:** Character must be modestly dressed in source image. Content of the audio is the voiceover script, so compliant by definition if script is halal. Maximum 3 retries on QA failures.

**Cost vs Kling for equivalent 5s clip:**
- VEED Fabric Fast 720p: **$0.75/5s** (includes lip-sync delivery)
- Kling Standard 3s draft: $0.65 (cinematic motion, no speech delivery)
- These are different shot types — not a direct substitution

**Canary test (before any production use):**
1. Submit one 5s call: `veed/fabric-1.0-fast`, NBP Edit hero frame URL + 5s ElevenLabs audio clip, `aspect_ratio: "9:16"`, `resolution: "720p"`
2. Record actual AIMLAPI cost (~$0.75 expected)
3. Verify lip-sync alignment with audio
4. Run brand binary checklist + Shari'ah compliance (modest dress preserved from source image?)
5. If passes → available for "character delivers CTA" shot type

**Standard variant:** `veed/fabric-1.0` also confirmed on AIMLAPI at same per-second pricing, slower generation. Use Fast variant by default.

---

### Wan 2.2 14B Animate Move + Replace — CONFIRMED ON AIMLAPI, CANARY REQUIRED (2026-06-28, pricing updated 2026-07-04)

Docs pages confirmed:
- `docs.aimlapi.com/api-references/video-models/alibaba-cloud/wan-2.2-14b-animate-move-image-to-video`
- `docs.aimlapi.com/api-references/video-models/alibaba-cloud/wan-2.2-14b-animate-replace-image-to-video`

**Model strings:**
- Animate Move: `alibaba/wan2.2-14b-animate-move` — API endpoint `/v2/video/generations`
- Animate Replace: `alibaba/wan2.2-14b-animate-replace` — API endpoint `/v2/video/generations`

**Animate Move — Character Animation from Reference Video:**
Input: a static character image (`image_url`) + a reference drive video (`video_url`). The model extracts poses, body skeleton, and facial expressions from the drive video, then applies them to the character image. The character in the output mimics the motions of the drive video exactly.

**Pipeline use case:** Given an approved NBP Edit hero frame, find or generate a drive video of a person performing the desired motion (e.g., picking up a box, walking, waving). Pass both to Animate Move → get the Snelverhuizen character performing that same motion, with face preserved from hero frame. Eliminates complex Kling motion prompting for well-defined actions. No Subject Binding needed — identity preservation is structural (motion transfer, not generation).

**Animate Replace — Character Swap in Existing Video:**
Input: existing video (`video_url`) + character reference photo (`image_url`). Replaces the person in the video with the character from the photo while preserving background, camera angles, timing, and scene. Enables use of stock B-roll footage of movers working, with our approved character swapped in.

**Pipeline use case for Animate Replace:** Source stock or self-shot footage of moving activity → replace person with our character → get realistic movers footage WITHOUT needing Kling character generation. Potential to bypass $1.46 Kling Pro shots entirely for non-close-up character shots.

**Pricing (ESTIMATED 2026-07-04 — MEDIUM CONFIDENCE, CANARY REQUIRED):** AIMLAPI docs example shows `"credits_used": 120000` per generation for both Move and Replace. Using the confirmed 120k credits = $0.06 precedent (from Wan 2.7 Image Pro docs example), estimated cost is **~$0.06/generation flat** for both models. WaveSpeedAI charges $0.20/run — AIMLAPI is ~$0.06 on same model. If confirmed at canary, this is the cheapest character video option on the entire platform — 24× cheaper than Kling Pro ($1.46). **Verify actual AIMLAPI billing amount in canary step 2 — this is not confirmed from pricing page.**

**Canary checklist — Animate Replace (HIGHEST PRIORITY — 24× cheaper than Kling Pro if $0.06 confirmed):**
1. Submit one call: `alibaba/wan2.2-14b-animate-replace`, video_url = 5s stock footage of person moving boxes, image_url = NBP Edit hero frame
2. **Record actual cost from AIMLAPI dashboard — confirm it is ~$0.06** (120k credits). This is the critical verification step. If cost is $0.30+ instead, the model is NOT the routing win we expect.
3. QA: background/scene intact? Face matches character? Shari'ah compliance (modest dress preserved in swap)?
4. If cost ≤ $0.10 AND face swap passes → route non-close-up character B-roll shots here instead of Kling Pro (saves ~$1.40/shot)

**Canary checklist — Animate Move:**
1. Submit one call: `alibaba/wan2.2-14b-animate-move`, image_url = NBP Edit hero frame, video_url = 5s reference drive video of a person walking, `aspect_ratio: "9:16"`
2. Record actual cost from AIMLAPI dashboard (expect ~$0.06 if same credit pricing)
3. QA: does character face match hero frame? Shari'ah compliance (modest dress preserved)? Brand binary (uniform correct?)
4. If face retention ≥ 80% Kling Standard baseline → unlock for non-close-up character action shots

**CRITICAL:** Neither model does character generation — they animate/swap existing characters. Do NOT use for establishing shots without people or for truck-only shots. Only relevant when a character must appear in motion or performing an action.

---

### Krea WAN 14B T2V — PRICING CONFIRMED, CANARY PRIORITY HIGH (2026-07-02 update)

**Pricing CONFIRMED:** T2V = $0.033/sec (~$0.165/5s) on AIMLAPI. V2V = $0.033/sec (~$0.165/5s) — CORRECTED SC248: was $0.026/sec (SC234 error); AIMLAPI pricing page confirms both T2V and V2V at same $0.033/sec rate.

This makes Krea WAN 14B the **cheapest T2V model on AIMLAPI** — 50% cheaper than Veo 3.1 Lite 720p ($0.065/sec). It replaces Veo 3.1 Lite as the cheapest B-roll/establishing T2V option IF quality is sufficient.

**Architecture note:** Distilled from Wan 2.1 14B (older than Wan 2.7) using Self-Forcing (autoregressive technique). Real-time generation speed (11fps on B200). Optimized primarily for V2V style transfer, but T2V quality signals are positive.

**Quality signals (2026-07-02 research — CANARY NOT YET RUN, based on third-party reviews):**
- Cinematic establishing shots: architecture and urban environments render convincingly with atmospheric effects (fog, lighting shifts, dramatic wide framing). Suitable for professional contexts.
- Motion stability: strong temporal consistency, detailed textures, coherent style across frames.
- Weakness: distilled from Wan 2.1 14B (older base than Veo 3.1 Lite). May struggle with complex dynamic motion or fine-detail close-ups. Best for scenic B-roll, not tight product shots.
- CANARY PRIORITY: **HIGH** — 50% cheaper than Veo 3.1 Lite with encouraging quality signals. Run canary before next video session.

**Canary test:**
1. Submit 5s T2V call: `krea/krea-wan-14b/text-to-video`, wide establishing shot prompt (NO characters), `aspect_ratio: "9:16"`
2. Record actual cost from AIMLAPI dashboard (expect ~$0.165)
3. Compare output quality vs Veo 3.1 Lite 720p output from the same prompt
4. Run brand binary checklist (no characters in frame — so: no distortion, no text artifacts)
5. If quality ≥ 80% of Veo 3.1 Lite → route B-roll T2V shots to Krea WAN 14B (saves ~$0.165/5s clip)
6. Test V2V (`krea/krea-wan-14b/video-to-video`): restyle an approved Veo 3.1 Lite clip with a prompt change — verify output coherence and actual $0.033/sec billing (CORRECTED SC248: was $0.026/sec)

**Savings if canary passes (per 2 T2V establishing shots at 6s):** $0.033 × 12 = $0.396 vs Veo Lite $0.065 × 12 = $0.78 → saves $0.384/video on establishing shots alone.

---

### Happy Horse 1.1 — NOW ON AIMLAPI (2026-06-30) — CANARY REQUIRED

**STATUS UPDATE (SC167):** Happy Horse 1.0 was fal.ai-exclusive (Rule 37 said "NOT on AIMLAPI"). Happy Horse 1.1 was unveiled June 23, 2026; AIMLAPI published a guide on June 25. **The model is now on AIMLAPI.**

**Resources:** AIMLAPI blog guide: `aimlapi.com/blog/happy-horse-1-1-specs-pricing-and-api-guide`. Model string: **`alibaba/happyhorse-1.1`**.

**Pricing (AIMLAPI, confirmed 2026-06-30): $0.182/sec** (~$0.91/5s flat rate).

**Capabilities:**
- 9:16 aspect ratio confirmed ✓ (also supports 8 other ratios including 16:9, 1:1, 4:3)
- Duration: 4-10 seconds
- Resolution: 720p or 1080p
- I2V: reference image → video ✓
- R2V: up to 7 image references for character consistency ✓
- Audio: co-generated in single pass. **`generate_audio: false` disables audio** (defaults ON). Audio strip fallback: `ffmpeg -i input.mp4 -an -c:v copy output.mp4`
- Face drift (1.0's main failure mode) largely resolved in 1.1

**Cost position vs alternatives (5s clip):**
- Hailuo 2.3 Fast I2V: $0.208 ← cheapest non-char I2V
- Wan 2.7 I2V (~$0.50/5s canary): cheapest character draft
- **Happy Horse 1.1: ~$0.91/5s** = same price tier as Kling v3 Turbo Pro ($0.91/5s)
- Kling v3 Pro: $1.46/5s

**Routing decision:** NOT a budget model. Same cost as Kling Turbo Pro. Primary value is 7-ref R2V for character consistency — canary its R2V against Kling Subject Binding before routing character shots here. Until Wan 2.7 R2V canary passes, Happy Horse 1.1 R2V is the strongest multi-ref character option on AIMLAPI.

**CANARY CHECKLIST (before production):**
1. Submit one 5s I2V call: `alibaba/happyhorse-1.1`, NBP Edit hero frame, `aspect_ratio: "9:16"`, `generate_audio: false`
2. Record actual AIMLAPI cost (~$0.91 expected)
3. Verify `ffprobe` confirms no audio track if `generate_audio: false` accepted
4. Run brand binary checklist + Shari'ah compliance
5. Test R2V with 3 character refs — compare face lock vs Kling Subject Binding 80 baseline
6. If passes → available as peer-cost alternative to Kling Turbo Pro with multi-ref capability

**Happy Horse 1.0 (fal.ai only):** 1.0 remains fal.ai-exclusive. Only 1.1 is on AIMLAPI.

---

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
18. **Non-character routing (UPDATED SC262, 2026-08-16):** T2V (no image) → Veo 3.1 Lite ($0.33/5s 720p, `google/veo-3-1-lite-generate-preview`). I2V 5s (anchor frame) → Hailuo 2.3 Fast ($0.208, `minimax/hailuo-2.3-fast` — I2V only). I2V 5s fallback → Luma Ray Flash 2 (~$0.24/5s). I2V 6s+ → Hailuo 2.3 Fast ($0.250/6s) — **LTXV 2 Fast (`ltxv/ltxv-2-fast`) is BROKEN since 2026-08-15, do NOT use.** **Hailuo 2.3 Fast does NOT support T2V** — Fast variant requires `image_url`. Hailuo 02 and Hailuo 2.3 Standard DO NOT USE — $0.0728/sec uncompetitive.
19. **Wan 2.7 I2V and T2V are now LIVE on AIMLAPI. R2V is likely live.** I2V: `alibaba/wan-2-7-i2v` (confirmed). T2V: `alibaba/wan-2-7-t2v` (AIMLAPI docs confirmed 2026-06-05). R2V: `alibaba/wan-2-7-r2v` (likely live — Wan 2.6 R2V precedent; verify docs page). All at ~$0.10/sec. NO `generate_audio` param on any Wan 2.7 variant. T2V use case: wide establishing shots without characters (~$0.50/5s, more expensive than Veo Lite ~$0.33 but usable when Veo unavailable). CANARY REQUIRED for T2V and R2V before production.
20. **LTXV 2 Fast pricing CONFIRMED: $0.052/sec on AIMLAPI (2026-06-14, AIMLAPI pricing page).** The "indirect evidence" is now resolved. At $0.052/sec: 6s = $0.312 (Hailuo 2.3 Fast $0.25 wins), 10s = $0.52 (Hailuo 2.3 Fast $0.416 wins). **Hailuo 2.3 Fast is cheaper at ALL durations for T2V.** LTXV 2 Fast role: I2V-only, 6s+ clips where composition anchor frame is required and Luma Ray Flash 2 is unavailable. Minimum 6s clip. Parameters are snake_case (`aspect_ratio`, `generate_audio: false`). No further pricing canary required.
21. **Seedance 2.0 pricing CORRECTED (2026-06-30, AIMLAPI pricing page): Standard = $0.394/sec ($1.97/5s), Fast = $0.316/sec ($1.58/5s).** Prior entries had both wrong ($0.316 Standard, $0.182 Fast — those were Wan-adjacent prices). **Both variants are now MORE expensive than Kling Pro ($1.46/5s). DO NOT USE either.** The $0.182/sec figure is Kling v3 Turbo Pro and Happy Horse 1.1 (1080p), not Seedance. Face content-policy block risk from Seedance lineage still applies. Do not canary — cost is uncompetitive regardless of quality.
22. **Wan 2.7 I2V (`alibaba/wan-2-7-i2v`) is the cheapest confirmed character-draft candidate on AIMLAPI** at ~$0.10/sec (updated 2026-05-30). 3s draft = ~$0.30 vs Kling Standard 3s = $0.65 — 54% savings. 2s ultra-draft = ~$0.20 — 69% savings (use for identity spot-checks only). No audio surcharge. First+last frame truck-lock available. CANARY REQUIRED. Do not use for finals — Kling Pro with Subject Binding 80-90 remains required. R2V supports up to 5 mixed refs (image/video/audio) with character binding — relevant for character consistency once verified.
23. **Hailuo 2.3 Standard ≠ Fast (SC126 correction, 2026-06-14):** Standard = `minimax/hailuo-2.3` at $0.0728/sec ($0.728/10s) — same price as Hailuo 02, do NOT use for non-char shots. Standard supports BOTH T2V and I2V. Fast = `minimax/hailuo-2.3-fast` at $0.0416/sec ($0.416/10s) — I2V ONLY (requires `image_url`; does NOT support T2V). The Fast variant is the routing target for non-character I2V shots with an anchor frame. For T2V shots (no image), use Veo 3.1 Lite.
24. **Veo 3.1 Extend Video confirmed on AIMLAPI (2026-06-01):** `google/veo-3.1-extend-video` (Standard) and `google/veo-3.1-fast-extend-video` (Fast). Takes `video_url` of existing Veo 3.1 clip + new `prompt`. Use to extend approved establishing shots beyond single 4/6/8s generation limit. CANARY REQUIRED — verify `video_url` param accepts CDN link, confirm actual per-second cost, check visual continuity at join.
25. **Kling v3 = Kling 3.0 confirmed (2026-06-01).** Our `klingai/video-v3-pro-image-to-video` and `klingai/video-v3-standard-image-to-video` strings are correct and up-to-date — no action needed. Kling O3 (Omni) is a separate premium multi-shot model, NOT on AIMLAPI yet.
26. **Luma Ray Flash 2 confirmed on AIMLAPI (`luma/ray-flash-2`) — NEW 2026-06-05.** ~$0.048/sec (~$0.24/5s). Supports 9:16, I2V, first+last frame keyframes. **No audio generation** — no `generate_audio` param needed, no surcharge risk. Max 9s at 720p. CANARY REQUIRED. Use case: non-character I2V 5s clips where composition anchoring from a hero frame matters (e.g., truck exterior). Hailuo 2.3 Fast ($0.208/5s T2V) remains cheapest for 5s; Ray Flash 2 is the I2V alternative at ~$0.24.
27. **Wan 2.7 T2V confirmed live on AIMLAPI (`alibaba/wan-2-7-t2v`) — 2026-06-05.** AIMLAPI docs page confirmed. Cost: ~$0.50/5s ($0.10/sec). Use for T2V establishing shots without characters when Veo 3.1 Lite is unavailable. Veo 3.1 Lite 720p (~$0.33/5s) is cheaper — prefer Veo. Wan 2.7 T2V is a Veo fallback at higher cost. CANARY REQUIRED before production.
28. **Wan 2.7 R2V (`alibaba/wan-2-7-r2v`) STATUS: NAVIGATION INDEX ONLY (2026-07-02).** Appeared in AIMLAPI docs navigation index on 2026-06-30, but dedicated callable API page NOT FOUND in search as of July 2. Only Wan 2.6 R2V has a confirmed AIMLAPI docs page — Wan 2.7 R2V does not appear in search of `docs.aimlapi.com`. Status downgraded to "navigation listed, page not confirmed callable." Do NOT attempt to call until dedicated docs page appears. Wan 2.6 R2V (`alibaba/wan-2-6-r2v`) remains live fallback. **Confirmed R2V parameters from official Alibaba Cloud API docs (pre-documented for when AIMLAPI page appears):** `image_urls` (array of URLs, JPEG/PNG/BMP/WEBP, max 20MB each) — NOT `image_list`; up to 5 total mixed refs (images + video clips + audio combined); `aspect_ratio: "9:16"` confirmed supported; `first_frame` (image URL, overrides aspect_ratio if passed); `audio_url` (1-10s audio clip for voice timbre cloning — NOT audio generation, no surcharge); characters referenced in prompt as `Image1`, `Image2`, `Video1` slot names. No `generate_audio` parameter — Wan 2.7 R2V does NOT generate audio natively. Expected AIMLAPI price: ~$0.10/sec (same as Wan 2.7 I2V/T2V). Segmind flat rates ($0.625/720p, $0.9375/1080p) are Segmind-only, NOT applicable here.
29. **Grok Imagine Video 1.5 NOW IN WIDE RELEASE (June 17, 2026). PRICING CORRECTED (2026-06-18).** AIMLAPI page: `docs.aimlapi.com/api-references/video-models/xai/grok-imagine-video`. **Correct xAI GA pricing: $0.08/sec (480p), $0.14/sec (720p)** — prior entry had $0.05/$0.07 which were v1.0 rates. AIMLAPI estimated: ~$0.104/sec (480p) = ~$0.52/5s; ~$0.182/sec (720p) = ~$0.91/5s. Audio is always generated — no disable parameter. **AUDIO STRIP REQUIRED** (`ffmpeg -i input.mp4 -an -c:v copy output.mp4`) immediately on every download — before QA playback. At corrected GA pricing, Grok 1.5 is NOT competitive for non-char I2V (Hailuo 2.3 Fast at $0.208 wins). Use only for R2V character drafts when Wan 2.7 R2V is unavailable. Not T2V — I2V and R2V only. CANARY REQUIRED.
30. **Wan 2.7 Image Pro and Standard now on AIMLAPI (2026-06-09).** `alibaba/wan-2-7-image-pro` at ~$0.06/image (69% cheaper than NBP Edit $0.195). Multi-ref via `image_urls` array (up to 9 refs). Character Locking feature for cross-generation identity consistency. Use for draft hero frame iterations only — NOT for finals (no Subject Binding strength dial; identity lock is less precise than NBP Edit). `alibaba/wan-2-7-image` (standard) at ~$0.04/image — even cheaper but weaker character locking. CANARY REQUIRED for both variants.
31. **NB2 pricing corrected (2026-06-12): $0.067/image at 1K** (Google direct API, verified March 2026). Prior entry had $0.08 — corrected. With AIMLAPI ~1.3× markup → ~$0.087/image at 1K estimated. Batch API (Google direct) offers $0.034/image at 1K — but AIMLAPI does not expose Google Batch discount. Savings vs NBP Edit on AIMLAPI: $0.195 − $0.087 = $0.108/draft image (55% savings). CANARY REQUIRED on AIMLAPI to confirm exact price.
32. **PixVerse V5.5 confirmed on AIMLAPI (2026-06-12): `pixverse/v5-5-image-to-video` and `pixverse/v5-5-text-to-video`.** Price: $0.78/5s = $0.156/sec. Audio optional via `generate_audio_switch: false` (NOT forced). 9:16 confirmed. 1080p max 5s or 8s; 720p up to 10s. NOT competitive for non-character shots (Hailuo 2.3 Fast and LTXV 2 Fast are 3-4× cheaper). Potential fallback for character drafts if Wan 2.7 I2V canary fails — 28% cheaper than Kling Standard, with strong character retention claims. CANARY REQUIRED before any production use.
33. **Sora 2 confirmed on AIMLAPI (2026-06-12) — DO NOT USE.** Model strings: `openai/sora-2-i2v`, `openai/sora-2-t2v`, `openai/sora-2-pro-i2v`, `openai/sora-2-pro-t2v`. Estimated ~$0.13/sec (Standard 720p). DOUBLE DISQUALIFIER: (1) Audio is ALWAYS generated — no disable parameter, strip required on every download; (2) **API sunsets September 24, 2026** — do not build pipeline dependency. No cost advantage vs existing models. Do not canary.
34. **Veo 3 Fast I2V/T2V confirmed on AIMLAPI docs (2026-06-16) — CANARY REQUIRED.** Model strings: `google/veo-3-fast-image-to-video` (I2V), `google/veo-3-fast-text-to-video` (T2V). Estimated ~$0.13/sec = ~$0.65/5s (fal.ai $0.10/sec + AIMLAPI markup). Audio CAN be disabled (verify param name in canary). **Prefer Veo 3.1 Fast I2V over Veo 3 Fast** — 3.1 is newer and higher quality at same estimated cost. Use Veo 3 Fast only if 3.1 Fast is unavailable.
35. **Veo 3 Standard I2V on AIMLAPI (`google/veo-3-image-to-video`) — DO NOT USE.** $0.788/sec confirmed (~$3.94/5s). 6-7× more expensive than Kling v3 Pro. $15/video ceiling would be exhausted by 3-4 clips. Not cost-efficient at any quality level for this pipeline.
36. **VEED Fabric-1.0 Fast on AIMLAPI (`veed/fabric-1.0-fast`) — CANARY REQUIRED.** A2V talking-head model. Takes face image + audio URL → lip-synced video. Pricing: $0.08/sec (480p), $0.15/sec (720p). 9:16 supported. Max 30s/clip. Use case: character delivers speech directly to camera, synced with ElevenLabs voiceover. NOT a replacement for cinematic motion shots — separate shot type only. `veed/fabric-1.0` (Standard) also confirmed.
37. **Happy Horse 1.1 NOW ON AIMLAPI (2026-06-30).** Model string: `alibaba/happyhorse-1.1`. Price: $0.182/sec (~$0.91/5s). 9:16 confirmed, duration 4-10s. `generate_audio: false` to disable audio (defaults ON). R2V: up to 7 image refs. Happy Horse 1.0 remains fal.ai-exclusive — only 1.1 is on AIMLAPI. CANARY REQUIRED. Cost peers with Kling v3 Turbo Pro ($0.91/5s); NOT a budget option. Primary value: 7-ref R2V character consistency before Wan 2.7 R2V canary passes.
38. **Kling v3 Turbo AUDIO CORRECTED (2026-06-21): SILENT VIDEO in single-clip mode.** Prior entry stated "audio always generated" — this was WRONG (based on multi-shot mode docs). Confirmed via multiple independent sources (Evolink, WaveSpeedAI): Kling 3.0 Turbo generates **silent video by default in single-clip mode**. Audio is only forced-on in multi-shot mode. For our AIMLAPI single-clip I2V/T2V workflow: no `generate_audio` parameter needed, no audio strip required, no Shari'ah compliance risk from Turbo audio. Turbo Pro ($0.182/sec = $0.91/5s, 1080p) and Standard Turbo ($0.146/sec = $0.73/5s, 720p) are both silent by default. Updated canary checklist: verify (1) actual AIMLAPI cost, (2) 1080p output, (3) InsightFace cosine ≥ 95% vs v3 Pro, (4) `ffprobe` confirms no audio track. Remove mandatory audio strip from Turbo workflow. Turbo Pro T2V also confirmed at $0.182/sec. Kling O3/Omni still NOT on AIMLAPI.
39. **Krea WAN 14B pricing CONFIRMED on AIMLAPI (2026-06-28). CANARY PRIORITY HIGH (2026-07-02).** Two model strings confirmed: `krea/krea-wan-14b/text-to-video` (T2V) and `krea/krea-wan-14b/video-to-video` (V2V). **Pricing: T2V = $0.033/sec (~$0.165/5s), V2V = $0.026/sec (~$0.13/5s)** — confirmed from AIMLAPI pricing page. At $0.033/sec, Krea WAN 14B T2V is the **cheapest T2V option on AIMLAPI** — 50% cheaper than Veo 3.1 Lite 720p ($0.065/sec). Third-party quality reviews (2026-07-02): cinematic establishing shots render well — architecture, atmospheric effects, wide framing tested suitable for professional contexts. Motion stability is strong. Weakness: Wan 2.1 14B base (older than Wan 2.7); may not match Veo 3.1 Lite on complex dynamic scenes. V2V ($0.033/sec — CORRECTED SC248, was $0.026/sec) = cheapest video restyling option. No Subject Binding, no character identity lock. **Do NOT route character face shots here.** Positive quality signals → run canary before next production session to unlock $0.384/video savings on establishing shots.
40. **LTX 2.3 (22B) — NOT on AIMLAPI (confirmed 2026-07-02 status check).** Lightricks released LTX-2.3 (22B DiT), supporting 4K at 50fps, synchronized audio+video in single pass, clips up to 20s. Open-source model available locally and on LTX native API ($0.04/sec Fast 1080p, $0.06/sec Pro 1080p). NOT ON AIMLAPI as of 2026-07-02 — no docs page found on `docs.aimlapi.com`. Monitor for AIMLAPI availability. If added, expected model strings: `ltxv/ltxv-2-3-fast` and `ltxv/ltxv-2-3`. LTX 2.3 generates native audio (stereo 24kHz) — audio strip required for Shari'ah compliance. Cost position would be same as LTX 2 Fast (~$0.052/sec est. on AIMLAPI).
41. **Wan 2.2 Animate Move and Animate Replace now CONFIRMED on AIMLAPI (2026-06-28). Pricing estimated ~$0.06/generation (2026-07-04 update).** Two specialized character animation models with dedicated docs pages: (1) **Wan 2.2 14B Animate Move** (`alibaba/wan2.2-14b-animate-move`): I2V model that animates a static character image to mimic movements from a reference drive video. Input: character still image + drive video. Output: character performing those motions. Use case for this pipeline: given an approved NBP Edit hero frame, pass a drive video of a person moving naturally → character animates identically. Consistent motion technique without complex motion prompting. (2) **Wan 2.2 14B Animate Replace** (`alibaba/wan2.2-14b-animate-replace`): Video-to-video character swap — takes existing video + reference photo, replaces character with new one while preserving scene/background/timing. Use case: stock or B-roll footage of a mover working → swap the face/body with our approved Snelverhuizen character. **Pricing (MEDIUM CONFIDENCE):** AIMLAPI docs example shows 120,000 credits per generation for both Move and Replace. 120k credits = $0.06 (same as Wan 2.7 Image Pro precedent). **Estimated ~$0.06/generation flat** — if confirmed at canary, 24× cheaper than Kling Pro ($1.46). Canary step: verify actual AIMLAPI billing amount matches ~$0.06. Wan 2.2 Plus T2V (`alibaba/wan-2-2-plus-t2v`) and I2V also confirmed as separate entries. CANARY REQUIRED for all Wan 2.2 variants. Animate Replace is highest-priority canary: could eliminate the "blank slate" B-roll problem and reduce character shot dependency on Kling Pro for non-face-close-up shots.
42. **Wan 2.2 VACE Fun family — additional variants confirmed on AIMLAPI (2026-06-30).** Multiple specialized controlled-generation models confirmed via `docs.aimlapi.com`: **Pose** (`alibaba/wan2.2-vace-fun-a14b-pose`, $0.065/generation) — pose skeleton-driven animation from a drive video; Inpainting (`alibaba/wan2.2-vace-fun-a14b-inpainting`) — targeted region editing within an existing clip; Outpainting (`alibaba/wan2.2-vace-fun-a14b-outpainting`) — expand video frame boundaries; Reframe (`alibaba/wan2.2-vace-fun-a14b-reframe`) — reposition video content. The Depth variant was already documented (SC141 era). At $0.065/generation the Pose model is extremely cheap — potential use for controlled character motion without complex motion prompting. Resolution: 512/768/1024px — 9:16 support and actual output quality need canary verification at 768px. CANARY REQUIRED for each variant before production use. Pricing for non-Pose variants not yet confirmed.
43. **Seedance 2.5 — NOT on AIMLAPI (2026-07-02 status).** Announced June 23, 2026 at Volcano Engine FORCE conference. Public access rolling out in stages — enterprise beta first, then broader rollout expected mid-July 2026. Seedance 2.0 updated in parallel to support 4K. Key specs for 2.5: 30-second native clips (no stitching), up to 50 multimodal references, region-level controllable editing, co-generated synchronized audio. API pricing NOT YET DISCLOSED. No AIMLAPI blog post or docs page found as of 2026-07-02. Third-party platforms (Rita, ImagineArt, kie.ai) listing "Coming Soon" for 2.5. Volcano Engine API must open before AIMLAPI integration. Both Seedance 2.0 Standard ($0.394/sec) and Fast ($0.316/sec) remain DO NOT USE — more expensive than Kling Pro. Monitor for AIMLAPI page mid-July 2026.
44. **Wan 2.7 R2V parameter names CONFIRMED from official Alibaba Cloud API docs (2026-07-02).** When AIMLAPI page appears, use: `image_urls` (array, NOT `image_list`), max 5 refs (images + video + audio total), `aspect_ratio: "9:16"` (confirmed), `first_frame` (optional first-frame anchor), `audio_url` (1-10s voice cloning input, NOT audio generation). Characters in prompt: `Image1`, `Image2`, `Video1` slot names. No `generate_audio` parameter — R2V does not generate audio natively. Expected AIMLAPI string: `alibaba/wan-2-7-r2v` at ~$0.10/sec.
45. **STATUS REFRESH 2026-07-04 (SC181 — cost optimization study):** (a) **Wan 2.7 R2V**: Still "Coming Soon" on AIMLAPI per search-indexed docs as of ~2 weeks ago. Still not callable — Wan 2.6 R2V remains live fallback. (b) **LTX 2.3** (22B, released March 2026): Confirmed NOT on AIMLAPI as of 2026-07-04. Available on fal.ai ($0.04/sec Fast) and LTX native API. Monitor for AIMLAPI docs page. (c) **Seedance 2.5** (announced June 23, 2026): Still in enterprise closed beta, no public API access, no AIMLAPI page. No pricing disclosed. Expected mid-to-late July broader rollout — monitor AIMLAPI blog weekly. (d) **Wan 2.2 Animate Move/Replace pricing**: Estimated **~$0.06/generation flat** (MEDIUM CONFIDENCE — from 120k credits/gen AIMLAPI docs example). If confirmed at canary, Animate Replace at $0.06 vs Kling Pro $1.46 = 24× cheaper for character shots in existing footage. HIGHEST PRIORITY CANARY for next production session. (e) **Krea WAN 14B quality**: Third-party reviews (July 2026) confirm cinematic establishing shots render well — architecture, atmospheric effects, wide framing tested positive. Strong temporal consistency. Weakness: Wan 2.1 14B base (older). Canary priority remains HIGH — potential $0.384/video savings on B-roll T2V vs Veo 3.1 Lite.
47. **SC194 STATUS REFRESH (2026-07-09 — cost optimization study, pass 26):** (a) **Kling O1 I2V (NEW): `klingai/video-o1-image-to-video` at $0.118/sec ($0.59/5s, $0.35/3s).** Confirmed on AIMLAPI. Standard I2V with tag-based subject consistency supporting up to 7 reference inputs. 46% cheaper than Kling v3 Standard ($1.09/5s) and 19% cheaper than Kling Turbo Pro I2V ($0.91/5s). At 3s draft: $0.35 vs Kling Standard $0.65 — saves $0.30/draft. CANARY REQUIRED — must verify face identity retention vs NBP Edit baseline before routing any character shots here. Added to video models table above. (b) **Kling O1 R2V pricing CORRECTED: $0.146/sec ($0.73/5s, $0.44/3s).** Prior entry had $0.112/sec ($0.56/5s) — incorrect. AIMLAPI pricing search confirms $0.146/sec. Still 50% cheaper than Kling Pro. Table row corrected above. (c) **Wan 2.7 R2V duration CORRECTED: 2-10s max in R2V mode.** Prior notes said "2-15s" — this applies to T2V/I2V only. R2V mode cap is 10s. First+last-frame mode cap is 5s. 1080p I2V also caps at 10s. 720p I2V first-frame-only: up to 15s. Use `duration: 5` as default for R2V canary. (d) **Wan 2.7 R2V status (2026-07-09): AIMLAPI docs navigation now shows R2V entry.** Last confirmed status was "Coming Soon" on 2026-07-06 (Rule 46). As of 2026-07-09, navigation entry appeared — may now be callable. Verify by checking `docs.aimlapi.com/api-references/video-models/alibaba-cloud/wan-2.7-reference-to-video` before calling. If page exists: run canary (see step 6 above). Wan 2.6 R2V remains confirmed fallback. (e) **Gemini Omni Flash (WATCH — low canary priority).** Google launched June 30, 2026. AIMLAPI model string unconfirmed. Estimated ~$0.13/sec on AIMLAPI (~$0.65/5s). Audio ALWAYS co-generated — no `generate_audio` disable parameter. Strip mandatory: `ffmpeg -i input.mp4 -an -c:v copy output.mp4`. Unique feature: conversational video editing (prompt chain refines same video turn-by-turn). At ~$0.65/5s, NOT competitive vs Krea WAN 14B ($0.165/5s T2V) or Veo 3.1 Lite ($0.33/5s T2V) for B-roll. Canary only when AIMLAPI model string confirmed. (f) **Kling O1 V2V-Reference (NEW — DO NOT ROUTE): `klingai/video-o1-video-to-video-reference` at $0.218/sec ($1.09/5s).** Confirmed on AIMLAPI. Copies cinematic style and motion dynamics from a source video clip — NOT a character face lock model. Takes source video + up to 4 element images. Same cost as Kling v3 Standard. No character identity advantage. Use only if cinematic style transfer from a reference clip is specifically required.
46. **STATUS REFRESH 2026-07-06 (SC188 — cost optimization study):** (a) **Wan 2.7 R2V**: Confirmed still "Coming Soon" on AIMLAPI model database as of 2026-07-06 (web search returned AIMLAPI docs listing it as "Coming Soon"). Status unchanged from July 4. Wan 2.6 R2V (`alibaba/wan-2-6-r2v`) remains the live R2V fallback. Do NOT attempt to call `alibaba/wan-2-7-r2v` until dedicated AIMLAPI docs page appears. (b) **NB2 Lite** (`google/gemini-3.1-flash-lite-image`): Released 2026-06-30, confirmed on AIMLAPI product page 2026-07-03. ~$0.044/image (AIMLAPI est.; native Google $0.034 at 1K). 1K ONLY, 5-ref ceiling. Use as cheapest non-character T2I/I2I draft — replaces Gemini 2.5 Flash Image (retiring Oct 2, 2026). Added to Image Models table above. Full specs + model string confirmed in `generation-image.md`. CANARY REQUIRED for param names. (c) **Seedream 5.0 Lite Preview** (`bytedance/seedream-5-0-lite-preview`): Confirmed on AIMLAPI, ~$0.031–$0.035/img, 14 refs, 2K/3K. Added to Image Models table. If character identity passes canary: cheapest draft-tier with full slot count, saves ~$0.05/draft vs NB2 Edit. Seedream 5.0 Full (10-ref blending, 4K native) not yet on AIMLAPI — monitor. (d) **Kling Turbo Pro pricing**: $0.182/sec on AIMLAPI confirmed via third-party cross-reference (July 2026 search). Standard Turbo $0.146/sec also confirmed. Both match existing entries — no change required. (e) **Kling O3/Omni and Kling 4K**: Still NOT on AIMLAPI as of July 2026. Kling 4K (`klingai/video-o3-4k`) available on Runware and other platforms — absent from AIMLAPI model database. AIMLAPI-only mandate means no access. (f) **Image draft funnel update**: Cheapest path is now Seedream 5.0 Lite ($0.035, CANARY) → NB2 Lite ($0.044, non-char only) → NB2 Edit ($0.087, char drafts) → NBP Edit ($0.195, finals). Saves ~$0.05-0.10/draft image vs old NB2 → NBP path.
48. **SC199 CORRECTIONS (2026-07-11 — cost optimization study, pass 27):** (a) **Kling O1 I2V price CORRECTED: $0.146/sec ($0.73/5s, $0.44/3s).** SC194 recorded $0.118/sec ($0.59/5s, $0.35/3s) — this was wrong. July 2026 AIMLAPI pricing page search confirms $0.146/sec for `klingai/video-o1-image-to-video`. Savings vs Kling v3 Standard revised from "46% cheaper" to **33% cheaper** at 5s. Table and canary notes corrected. (b) **Kling O1 V2V-Reference price CORRECTED: $0.164/sec ($0.82/5s, $0.49/3s).** SC194 rule 47(f) recorded $0.218/sec ($1.09/5s) — incorrect. July 2026 AIMLAPI pricing confirms $0.164/sec. Two new V2V variant rows added to table: `klingai/video-o1-video-to-video-reference` and `klingai/video-o1-video-to-video-edit`, both $0.164/sec, CANARY REQUIRED. (c) **Wan 2.7 R2V status upgraded to LIKELY LIVE (2026-07-11).** AIMLAPI blog on Wan 2.7 explicitly states "rates apply across all four modes (T2V, I2V, R2V, and video editing) via the AI/ML API platform." Model string `alibaba/wan-2-7-r2v` in AIMLAPI model database. `image_urls` max clarified: 3 image-only refs (total including video/audio ≤ 5). R2V duration cap: 2-10s. Table row and canary step 6 updated. CANARY still required before production use. (d) **Veo 3.1 Lite 720p price floor watch.** Multiple July 2026 sources cite $0.03/sec at Vertex for 720p without audio (vs. $0.05/sec audio-on / 1080p). If AIMLAPI passes this reduction, effective rate would drop from ~$0.065/sec to ~$0.039/sec — halves B-roll cost. Log actual AIMLAPI billing on next canary use. (e) **"Kling 3.0" = Kling v3 (confirmed).** External branding "Kling 3.0" = `klingai/video-v3-*` on AIMLAPI. No new model — naming convention only. No action.
49. **SC206 STATUS REFRESH (2026-07-13 — cost optimization study, pass 28):** (a) **⚠️ URGENT: LTXV 2 Fast / Standard DEPRECATION RISK.** LTX's own API deprecated `ltx-2-fast` and `ltx-2-pro` on July 15, 2026 (2 days from this entry) and removes them on August 15. Migration target: `ltx-2-3-fast` and `ltx-2-3-pro`. AIMLAPI has NOT added `ltxv-2-3-fast` to their docs or model database as of July 13. If AIMLAPI routes through the LTX native API, `ltxv/ltxv-2-fast` and `ltxv/ltxv-2` WILL BREAK by August 15. **Action: Remove `ltxv/ltxv-2-fast` from active production routing immediately.** Use Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`, $0.0416/sec, I2V) as replacement for non-character I2V 5s+ clips. Monitor AIMLAPI for `ltxv/ltxv-2-3-fast` addition. (b) **Wan 2.7 R2V status DOWNGRADED to NOT CALLABLE.** SC199 (2026-07-11) elevated to "LIKELY LIVE" based on model database entry and blog language — this was incorrect. July 13, 2026 search: AIMLAPI docs still link to Wan 2.6 R2V docs page; no dedicated Wan 2.7 R2V page found. Model database entry ≠ callable endpoint. Status reverted to "Coming Soon — NOT CALLABLE." Table row corrected. Rule 48(c) "LIKELY LIVE" is WRONG — disregard. Wan 2.6 R2V (`alibaba/wan-2-6-r2v`) remains the only confirmed live R2V fallback. (c) **Gemini Omni Flash model string CONFIRMED: `google/gemini-omni-flash-preview`.** Pricing: $0.10/sec at 720p ($0.50/5s, $0.85/8s) — confirmed via AIMLAPI model database and multiple third-party cross-references (July 2026). Audio ALWAYS generated — no `generate_audio` disable parameter. **Mandatory audio strip** on every download: `ffmpeg -i input.mp4 -an -c:v copy output.mp4`. Unique feature: conversational multi-turn editing (prompt chain refines same video). NOT cost-competitive vs Krea WAN 14B T2V ($0.165/5s) or Veo 3.1 Lite ($0.33/5s) for B-roll. Low canary priority — audio-always-on + $0.50/5s are both disqualifying for this pipeline. (d) **Seedance 2.5 — still NOT on AIMLAPI.** Enterprise beta, no public pricing. Third-party platforms (kie.ai, PiAPI) show "Coming Soon." Expected broader rollout post-July — monitor AIMLAPI blog weekly. (e) **Krea WAN 14B quality re-confirmed.** July 2026 reviews: cinematic establishing shots (architecture, atmosphere, wide framing) render well with strong temporal consistency. Based on Wan 2.1 14B base — weakness on complex dynamic scenes. T2V at $0.033/sec remains the cheapest T2V on AIMLAPI. V2V at $0.033/sec cheapest restyling (CORRECTED SC248: was $0.026/sec). Canary priority HIGH — run before next production session to unlock $0.165/5s B-roll vs Veo Lite $0.33/5s.
51. **SC220 STATUS REFRESH (2026-07-17 — cost optimization study, pass 30):** (a) **LTXV August 15 deadline — 29 days out, no AIMLAPI string update found.** AIMLAPI's GitHub api-docs repo updated July 16, 2026 (yesterday) — commits added `moonshotai/kimi-k3` and `meta/muse-spark-1.1` (both text/vision models). No `ltxv/ltxv-2-3-fast` added. `ltxv/ltxv-2-fast` still auto-routes to LTX-2.3 quality (SC213 confirmed) and is still callable today — but will ERROR on August 15 if AIMLAPI does not act. Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`, $0.0416/sec) remains the production I2V fallback if LTXV breaks. Monitor AIMLAPI docs weekly — next check required by August 1. (b) **Wan 2.7 R2V: STILL "Coming Soon" on AIMLAPI (July 17, 2026).** Multiple independent search results explicitly confirm AIMLAPI marks `alibaba/wan-2-7-r2v` as "Coming Soon" as of today. This is the third consecutive cost-optimization cycle (SC206, SC213, SC220) with no status change — the SC199 "LIKELY LIVE" and SC213 "UNVERIFIED" upgrades were both premature. Treat as NOT CALLABLE until a search explicitly returns an AIMLAPI docs page at `docs.aimlapi.com/api-references/video-models/alibaba-cloud/wan-2.7-reference-to-video`. Wan 2.6 R2V (`alibaba/wan-2-6-r2v`) remains the only confirmed live R2V fallback. (c) **Seedance 2.5: BytePlus API launched July 16 — NOT on AIMLAPI.** ByteDance's own developer API (BytePlus) went live July 16, 2026. Third-party platforms (kie.ai, PiAPI) still show "Coming Soon." No AIMLAPI model string, blog post, or docs page found as of July 17. SC213 predicted "end of July" — revised estimate: late July to early August on AIMLAPI. Monitor AIMLAPI blog. Both Seedance 2.0 variants remain DO NOT USE (more expensive than Kling Pro). (d) **Kling 4.0: Expected but NOT released.** No official Kuaishou release date. Not on AIMLAPI. Current `klingai/video-v3-pro-image-to-video` and `klingai/video-v3-standard-image-to-video` strings remain correct for all production shots. (e) **Wan 2.2 Animate Replace $0.06 DOUBLE-CONFIRMED (2026-07-17).** Three independent sources (AIMLAPI model page, AIMLAPI docs example, WaveSpeedAI comparison) all confirm 120,000 credits per generation for both `alibaba/wan2.2-14b-animate-replace` and `alibaba/wan2.2-14b-animate-move`. At 2M credits = $1, this is **$0.06/generation flat** — confirmed, not estimated. At $0.06 vs Kling Pro $1.46, Animate Replace is the highest-ROI canary on the platform. HIGHEST PRIORITY for next production session. (f) **Krea WAN 14B July 2026 quality signals: STRONG.** July 2026 reviews surface a specific test: ancient temple at sunset with fog rolling through columns — atmospheric effects, wide framing, dramatic light — rated suitable for professional contexts. Strong temporal consistency and detailed textures confirmed. Weakness: Wan 2.1 14B base (older than Wan 2.7); may not match Veo 3.1 Lite on complex dynamic scenes. T2V at $0.033/sec ($0.165/5s) vs Veo Lite $0.065/sec ($0.33/5s) = **50% cheaper B-roll T2V if canary passes**. Canary priority: HIGH — run before next production session. (g) **No new AIMLAPI video models in last 2 days.** AIMLAPI api-docs GitHub confirms no video model additions on July 16. All existing routing decisions remain current.

52. **SC234 STATUS REFRESH (2026-07-21 — cost optimization study, pass 32):** (a) **⚠️ LTXV August 15 deadline — 25 days, still NO AIMLAPI update.** AIMLAPI GitHub api-docs commits through July 16 added text/reasoning models only (no video additions). LTX's official migration strings are `ltx-2-3-fast` and `ltx-2-3-pro` (LTX native API names, NOT AIMLAPI names). If AIMLAPI adds them, expected AIMLAPI strings: `ltxv/ltxv-2-3-fast` and `ltxv/ltxv-2-3`. Current `ltxv/ltxv-2-fast` still callable today (auto-routes to LTX-2.3 quality since July 15) but will ERROR after August 15. Do NOT route new production shots to LTXV — use Hailuo 2.3 Fast ($0.0416/sec I2V) exclusively for non-char I2V. Monitor AIMLAPI docs by August 1 for new string. (b) **Wan 2.7 R2V — FOURTH CONSECUTIVE CYCLE: NOT CALLABLE on AIMLAPI.** SC220, SC227, SC233, SC234 — four cost-optimization cycles with no status change. Search still returns Wan 2.6 R2V as the AIMLAPI R2V docs page. Wan 2.7 R2V is live on Replicate, inference.sh, Segmind — but NOT confirmed on AIMLAPI. Do NOT attempt to call `alibaba/wan-2-7-r2v` until AIMLAPI docs page appears. Wan 2.6 R2V (`alibaba/wan-2-6-r2v`) remains the only confirmed live R2V fallback. (c) **Seedance 2.5 — BytePlus API live July 16, NOT on AIMLAPI as of July 21.** ByteDance/BytePlus public developer API opened July 16. AIMLAPI and fal.ai both absent. Expected late July to early August. Monitor AIMLAPI blog — no model string, no docs page, no pricing found as of today. (d) **Wan 2.2 Animate Replace parameters confirmed (secondary sources).** Model string: `alibaba/wan2.2-14b-animate-replace` (Replace mode), `alibaba/wan2.2-14b-animate-move` (Move mode). Parameters: `video_url` (driving motion video), `image_url` (reference character photo), `resolution: "720p"`. Move mode: character photo animates to match drive video motion. Replace mode: replaces character in drive video with reference photo character. Both confirmed in AIMLAPI docs. Cost: $0.06/generation flat (CONFIRMED). HIGHEST PRIORITY CANARY — canary sequence: (1) Move: pass NBP Edit hero frame as `image_url` + simple drive video, verify identity lock and actual $0.06 billing; (2) Replace: pass existing B-roll as `video_url` + hero frame as `image_url`, verify character swap quality. (e) **Krea WAN 14B V2V practical use case clarified.** T2V ($0.033/sec, $0.165/5s) = cheapest B-roll T2V. V2V ($0.033/sec, ~$0.165/5s — CORRECTED SC248 from $0.026/sec) = cheapest video restyling on AIMLAPI. Workflow: Generate Veo 3.1 Lite establishing shot (approved) → pass to Krea V2V with cinematic style prompt ("cinematic 24fps film look, subtle grain, warm shadows") → V2V enhances the shot without changing composition/timing. At $0.033/sec, a single 6s restyle pass = $0.198 — substantially cheaper than regenerating with a higher-quality model. Canary priority HIGH — run with existing approved clip before first production deployment. (f) **Kling 4.0 — NOT released, NOT on AIMLAPI as of July 21.** No official Kuaishou release date announced. `klingai/video-v3-pro-image-to-video` and `klingai/video-v3-standard-image-to-video` remain correct production strings. (g) **No new AIMLAPI video models July 18-21.** GitHub commits in this window: text/reasoning additions only (Inkling, other LLMs). Zero video model additions. All existing routing decisions current.

53. **SC241 STATUS REFRESH (2026-07-23 — cost optimization study, pass 33):** (a) **⚠️ LTXV August 15 deadline — 23 days, STILL NO AIMLAPI video model additions.** GitHub commits July 21-22: `alibaba/qwen-image-3` (VLM — vision-language, NOT T2I), `alibaba/qwen-image-3-edit` (VLM), `poolside/laguna-m-1` and `poolside/laguna-s-2.1` (code-gen models), `google/gemini-3.x-flash-lite` variants (text/vision). Zero video model additions in this window. `ltxv/ltxv-2-fast` remains the only callable string — WILL ERROR after August 15. AIMLAPI has not acted. Continue routing all non-char I2V to Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`, $0.0416/sec). If AIMLAPI adds `ltxv/ltxv-2-3-fast` before August 15, parameters are drop-in identical — no prompt changes needed, only model string swap. (b) **Wan 2.7 R2V: STATUS SYNCED WITH SC240 — CANARY-TEST RECOMMENDED (2026-07-23).** SC234 marked this "FOURTH CONSECUTIVE CYCLE: NOT CALLABLE." SC240 (character-consistency study, 2026-07-23, same day) upgraded to "canary-test recommended" based on: (1) AIMLAPI blog post explicitly naming all four Wan 2.7 modes (T2V/I2V/R2V/Edit) as accessible via AIMLAPI; (2) All third-party providers (Segmind, Replicate, Together AI, Kie.ai, inference.sh, WaveSpeedAI) confirm R2V live. No dedicated docs.aimlapi.com page confirmed yet. Canary protocol: call `alibaba/wan-2-7-r2v` with `image_urls: [hero_frame_url]`, `aspect_ratio: "9:16"`, `duration: 5`, `audio_mode: "mute"`. If valid job ID returned → canary score with InsightFace (PASS ≥ 0.62). If 404/model-not-found → fallback to `alibaba/wan-2-6-r2v`. Do NOT promote to production without owner-reviewed output. NOTE: Wan 2.7 R2V audio control param is `audio_mode: "mute"` (NOT `generate_audio: false` — Wan does not use boolean audio flags; use string mode values). (c) **Qwen Image 3 and Qwen Image 3 Edit: VLMs — NOT T2I generators.** `alibaba/qwen-image-3` and `alibaba/qwen-image-3-edit` added to AIMLAPI July 22. These are vision-language models (image understanding and editing based on instruction) — NOT photorealistic character generators. They CANNOT generate 9:16 character hero frames. Do not add to routing matrix. (d) **Kling 4.0: NOT released, NOT on AIMLAPI as of July 23.** SC240 (character-consistency) confirmed: docs.aimlapi.com search returns only v3-standard, v3-standard-turbo, v2.6-motion-control, v2-master — no Kling 4.0 or O3 endpoint. Correct production strings remain `klingai/video-v3-pro-image-to-video` (finals) and `klingai/video-v3-standard-image-to-video` (drafts). (e) **Kling O3: NOT on AIMLAPI as of July 23.** SC240 confirmed. O3 live on Runware, fal.ai, Atlas Cloud — not on AIMLAPI. When O3 lands on AIMLAPI, character shot cost drops ~3× (O3 R2V = $0.5625/5s on native Kling API vs v3 Pro $1.46/5s). Continue monitoring. (f) **Seedance 2.5: BytePlus live July 16, NOT on AIMLAPI as of July 23.** Late-July window is closing — revised estimate: early August on AIMLAPI. Both Seedance 2.0 variants remain DO NOT USE (more expensive than Kling Pro per prior analysis). Monitor AIMLAPI blog. (g) **No new AIMLAPI video models July 21-23.** GitHub commits in this window confirm only image/text/code model additions. All existing routing decisions remain current. (h) **Key cost saves still pending canary:** Wan 2.2 Animate Replace ($0.06/gen — 24× cheaper than Kling Pro, HIGHEST PRIORITY); Krea WAN 14B T2V ($0.165/5s — 50% cheaper than Veo 3.1 Lite, HIGH PRIORITY); Wan 2.7 R2V canary (see above). None of these have been run yet — unblocking even one would materially reduce per-video cost.

54. **SC248 STATUS REFRESH (2026-07-25 — cost optimization study, pass 34):** (a) **No new AIMLAPI video models July 22-25.** GitHub api-docs commits in this window: `anthropic/claude-opus-5` (text, July 24), `alibaba/qwen-image-3` / `qwen-image-3-edit` (VLMs, July 22), `poolside/laguna-m-1` / `laguna-s-2.1` (code-gen, July 22). Zero video model additions. All existing routing decisions remain current. (b) **⚠️ LTXV August 15 deadline — 21 days out, AIMLAPI STILL HAS NOT ACTED.** The Aug 1 monitoring checkpoint (flagged in SC220) is now 7 days away. No `ltxv/ltxv-2-3-fast` appears in any GitHub commit through July 24. `ltxv/ltxv-2-fast` will ERROR on August 15 if AIMLAPI does not update their model string. **Action: check AIMLAPI docs by August 1 — if still absent, notify owner.** Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`, $0.0416/sec, I2V only) remains the confirmed fallback for non-char I2V. Do NOT route new production non-char I2V to LTXV. (c) **Krea WAN 14B V2V price CORRECTED: $0.033/sec (NOT $0.026/sec).** AIMLAPI pricing page confirms both `krea/krea-wan-14b/text-to-video` and `krea/krea-wan-14b/video-to-video` at **$0.033/sec** as of July 2026. SC234 Rule 39 stated V2V at $0.026/sec — this was wrong. At $0.033/sec, a 6s V2V restyle pass = $0.198 (revised from $0.156). V2V remains the cheapest restyling option on AIMLAPI at $0.033/sec, but the gap vs T2V is zero (same price). All references in Rules 39, 49, 52 corrected. (d) **Wan 2.7 R2V — no new docs page found (July 25, SC248).** SC241 raised to "canary-test recommended." This cycle's site:docs.aimlapi.com search returned only Wan 2.7 I2V and Wan 2.7 Image Pro pages — no dedicated R2V page. Status unchanged from SC241. The AIMLAPI blog continues to claim all four Wan 2.7 modes are accessible; a canary call remains the only way to confirm. Use `image_urls: [hero_frame_url]`, `aspect_ratio: "9:16"`, `duration: 5`, `audio_mode: "mute"` for canary. Fallback: `alibaba/wan-2-6-r2v`. (e) **Seedance 2.5 — BytePlus only, NOT on AIMLAPI (July 25).** BytePlus API live since July 16. No AIMLAPI model string, blog post, or docs page found. Kie.ai and PiAPI still "Coming Soon." Late-July estimate from SC241 did not materialize — revised to early August on AIMLAPI. Both Seedance 2.0 variants remain DO NOT USE. (f) **Kling 4.0 NOT released (confirmed July 25).** Third-party sites using "Kling 4.0" branding are running Kling 3.0 underneath (kling4.co confirmed this explicitly). No official Kuaishou release. Not on AIMLAPI. Current `klingai/video-v3-pro-image-to-video` and `klingai/video-v3-standard-image-to-video` strings remain correct. (g) **Kling O3 NOT on AIMLAPI (confirmed July 25).** Available on fal.ai, Morphic, PixVerse — AIMLAPI-only mandate means no access regardless. O3 released February 2026, up to 15s, 1080p, native audio. When O3 lands on AIMLAPI, character shot cost drops significantly; continue monitoring. (h) **LingBot-Video (Ant Group / Robbyant, July 9, 2026) — NOT relevant to pipeline.** Open-source 30B MoE (3B active). Designed for embodied intelligence / robotics, not cinematic video. Available on Reactor API only. Not on AIMLAPI. Do not add to routing matrix.

55. **SC255 STATUS REFRESH (2026-07-27 — cost optimization study, pass 35):** (a) **NEW: Wan 2.6 I2V Flash (`alibaba/wan2.6-i2v-flash`) confirmed on AIMLAPI.** Alibaba native pricing: $0.025/sec silent 720p, $0.0375/sec silent 1080p. Estimated AIMLAPI with ~1.3× markup: ~$0.033/sec 720p (~$0.165/5s), ~$0.049/sec 1080p (~$0.245/5s). If AIMLAPI pricing confirmed at canary, this beats Hailuo 2.3 Fast ($0.208/5s) by 21% at 720p — becomes new cheapest non-character I2V option. I2V only (requires image). Faster than standard Wan 2.6 I2V. Audio param: likely `audio_mode: "mute"` (Wan convention — verify at canary). CANARY REQUIRED: call with non-char anchor frame, log actual AIMLAPI billing. Table row and I2V routing note updated. (b) **⚠️ LTXV August 15 deadline — now 19 days out (July 27).** No `ltxv/ltxv-2-3-fast` found in any AIMLAPI source as of today. No AIMLAPI video model additions found July 26-27. Aug 1 checkpoint is now 5 days away — if still absent Aug 1, owner notification required. Table countdown updated from 27→19 days. (c) **Wan 2.7 R2V: STILL "Coming Soon" on AIMLAPI model database (July 27).** Search confirms AIMLAPI model DB still marks `alibaba/wan-2-7-r2v` as "Coming Soon" with no dedicated docs page. Status unchanged from SC241/SC248 "canary-test recommended." Do NOT call without canary. Fallback: `alibaba/wan-2-6-r2v`. (d) **Kling O3: NOT on AIMLAPI (July 27 — SC254 recheck same day).** Available on fal.ai, Atlas Cloud, Runware. AIMLAPI-only mandate = no access. Continue monitoring. (e) **Wan 2.6 I2V Flash highest-priority canary this cycle.** Potential $0.04/5s savings over Hailuo 2.3 Fast if pricing holds. Run before next production session alongside Wan 2.2 Animate Replace ($0.06/gen, HIGHEST PRIORITY).

56. **SC262 STATUS REFRESH (2026-08-16 — cost optimization study, pass 36):** (a) **❌ LTXV 2 Fast (`ltxv/ltxv-2-fast`) and LTXV 2 Standard (`ltxv/ltxv-2`) ARE NOW BROKEN.** Lightricks removed LTX-2 strings on August 15, 2026 as announced. AIMLAPI never added `ltxv/ltxv-2-3-fast` before the deadline. Both strings WILL ERROR on AIMLAPI as of today (Aug 16). **Action complete: removed from all routing. Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`, $0.0416/sec) is now the confirmed I2V non-character route at all durations.** Watch for AIMLAPI to add `ltxv/ltxv-2-3-fast` — if it appears, run canary (parameters expected identical: snake_case, `generate_audio: false`, `image_url`, 6s min). (b) **LTX-2.5 released 2026-08-11 (NEW WATCH ITEM).** Open-weights 22B model from Lightricks. Native API variants: `ltx-2-5-fast` and `ltx-2-5-pro` (LTX native API). I2V in 6.8s on GB200 superchips. Up to 4K, 50fps, native multi-shot generation, diffusion video decoder for face/text reconstruction. Third-party unconfirmed prices: $0.09/s 720p, $0.15/s 1080p. NOT on AIMLAPI as of Aug 16. Expected AIMLAPI string when added: `ltxv/ltxv-2-5-fast`. Audio generated natively — strip required. (c) **MiniMax H3 (Hailuo 3.0) launched 2026-07-31 (NEW WATCH ITEM).** $0.13/sec for 2K video (official MiniMax pricing). 768p tier at $0.09/s (closed beta). T2V and I2V. Up to 5 reference images (first 5 free, then $0.04 each). Native stereo audio (mandatory strip for Shari'ah compliance). At $0.13/sec = $0.65/5s — if on AIMLAPI, would be viable as a character draft model (33% cheaper than Kling Turbo Pro at $0.91/5s). NOT confirmed on AIMLAPI as of Aug 16 — available on Segmind, fal.ai, OpenRouter. Expected AIMLAPI string: `minimax/hailuo-3`. WATCH — do not canary until AIMLAPI docs page confirmed. (d) **Wan 2.7 R2V: STILL "Coming Soon" on AIMLAPI (Aug 16 search confirms).** Search result from AIMLAPI docs page confirms "Coming Soon" status. Unchanged since SC241. Wan 2.6 R2V (`alibaba/wan-2-6-r2v`) remains the only confirmed live R2V. (e) **No other new AIMLAPI video models confirmed Aug 1-16.** All other existing routing decisions remain current.

57. **SC297 STATUS REFRESH (2026-08-25 — cost optimization study, pass 38):** (a) **NEW: Wan 3.0 now on AIMLAPI — confirmed from GitHub commit 2026-08-24.** Model string: `alibaba/wan3.0-video` (alt: `alibaba/wan-3-0-video`). Alibaba Cloud USD official pricing: $0.05/sec (480p), $0.10/sec (720p), $0.20/sec (1080p). AIMLAPI estimated with 1.3× markup: ~$0.065/sec (480p, ~$0.33/5s), ~$0.13/sec (720p, ~$0.65/5s), ~$0.26/sec (1080p, ~$1.30/5s). Key capabilities: **30-second native single-pass clips** (no stitching/extension chains), T2V, I2V, first+last-frame, R2V. R2V accepts up to 10 images + 5 videos + 5 audio files as combined references — largest multi-ref pool of any AIMLAPI model. Audio control: `generate_audio` parameter suspected (UNCONFIRMED for AIMLAPI — must canary). Cost position: 720p 5s at ~$0.65/5s est. = 40% cheaper than Kling v3 Standard I2V ($1.09/5s) for character drafts, but 30% more than Wan 2.7 I2V ($0.50/5s). For 30s establishing shots: ~$3.90 single-pass est. vs Veo 3.1 Lite extend-chain ($0.39/8s × 3 = $1.17 for 24s — cheaper, but with join artifacts). **CANARY PRIORITY: HIGH** — test R2V with character refs (InsightFace score vs Kling Standard baseline); test audio-off param; verify AIMLAPI billing matches estimate. Table row added above. (b) **No other new AIMLAPI video models Aug 21-24.** GitHub commits in this window: Tencent HY-MT2 models, Zhipu GLM variants (all text/LLM). LTX-2.5 still NOT on AIMLAPI (confirmed; expected AIMLAPI string `ltxv/ltxv-2-5-fast` when added — LTX native API pricing $0.09/sec 720p, $0.15/sec 1080p). Seedance 2.5 still NOT on AIMLAPI. Wan 2.7 R2V still "Coming Soon" on AIMLAPI (unchanged since SC241). Kling 4.0 still NOT on AIMLAPI. MiniMax H3 already documented at SC283 (Aug 21). All other routing decisions remain current.

50. **SC213 STATUS REFRESH (2026-07-15 — cost optimization study, pass 29):** (a) **LTXV 2.3 AUTO-ROUTING LIVE TODAY.** As of July 15, 2026, LTX's own API auto-routes calls to `ltx-2-fast` → `ltx-2-3-fast` and bills at LTX-2 rates. This means AIMLAPI's `ltxv/ltxv-2-fast` (which routes through LTX's API) NOW silently uses LTX-2.3 quality at the same $0.052/sec. LTX-2.3 is a drop-in replacement — all existing parameters work. **No change needed TODAY.** However: on **August 15, 2026, LTX removes the old strings entirely** — after that, `ltxv/ltxv-2-fast` will error on AIMLAPI unless they update to `ltxv/ltxv-2-3-fast`. AIMLAPI has NOT added the new string as of July 15. **Monitor AIMLAPI docs weekly through August 15.** Hailuo 2.3 Fast remains the production fallback. (b) **Veo 3.1 Lite 720p audio-off pricing — NEAR-CONFIRMED AT $0.03/sec at Vertex.** Multiple July 2026 sources (costgoat, MaxVideoAI, buildfastwithai, veo3ai) now converge on $0.03/sec for 720p WITHOUT audio at Google Vertex AI (vs. $0.05/sec with audio, $0.05/sec previously documented). One source (MaxVideoAI) says $0.04/sec without audio; others say $0.03/sec. Best estimate: **$0.03–$0.04/sec at Vertex** for 720p audio-off. With AIMLAPI ~1.3× markup → **~$0.039–$0.052/sec on AIMLAPI** = ~$0.195–$0.26/5s (vs. currently-documented ~$0.33/5s). **Log actual AIMLAPI billing on next canary use — this change, if confirmed at AIMLAPI, saves $0.07–$0.135 per 5s B-roll clip.** The old ~$0.065/sec ($0.33/5s) was based on the audio-ON rate. DO NOT change the routing table until AIMLAPI billing is verified. (c) **Wan 2.2 Animate Move/Replace pricing CONFIRMED: $0.06/generation.** 120,000 credits per generation confirmed in AIMLAPI docs example. 2,000,000 credits = $1 → 120,000 credits = **$0.06 flat per generation** (both `alibaba/wan2.2-14b-animate-move` and `alibaba/wan2.2-14b-animate-replace`). Upgrades from "MEDIUM CONFIDENCE" to **CONFIRMED**. At $0.06 flat vs Kling Pro $1.46/5s = 24× cheaper for character animation shots. Canary sequence: (1) Animate Move — pass NBP Edit hero frame + drive video, verify output quality and actual $0.06 billing; (2) Animate Replace — pass existing B-roll + character reference photo, verify seamless swap. High-priority canary before next production session. (d) **Seedance 2.5 timeline update.** BytePlus (ByteDance developer API) opened July 16, 2026. Third-party platforms including AIMLAPI expected late July 2026. No pricing disclosed. No AIMLAPI model string or docs page found as of July 15. Monitor AIMLAPI blog — first page expected by end of July. (e) **Wan 2.7 R2V status: UNVERIFIED (blog claims live, no dedicated docs page).** AIMLAPI blog explicitly states "all four modes (T2V, I2V, R2V, and video editing) via the AI/ML API platform" but July 15 search of docs.aimlapi.com still does not return a dedicated Wan 2.7 R2V page — only Wan 2.7 I2V and Wan 2.6 R2V pages exist. Status upgraded from SC206's "NOT CALLABLE" to **"UNVERIFIED — blog claims live, no docs page confirmed."** The difference: SC206 had active evidence that AIMLAPI docs pointed to Wan 2.6 R2V for R2V queries; SC213 finds the AIMLAPI blog directly claims R2V is accessible via AIMLAPI. Cautious canary recommended before next production session: call `alibaba/wan-2-7-r2v` with `image_urls: [hero_frame_url]`, `aspect_ratio: "9:16"`, `duration: 5`. If it returns a valid job ID, R2V is live. If it 404s or errors, revert to Wan 2.6 R2V. Do NOT route production shots here without canary confirmation.
