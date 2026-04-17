---
name: Model Prompting Guide
description: Definitive reference for prompting every model in the pipeline. Covers Nano Banana Pro, Flux Kontext Max, Higgsfield Soul Cinema, Kling v3 Pro I2V, Seedance 2.0, Cinema Studio 3.0, routing matrix, character consistency, text workarounds, and update mechanism.
autoInvoke: true
triggers:
  - prompt
  - generate
  - hero frame
  - animate
  - video generation
  - image generation
  - model selection
  - Kling
  - Seedance
  - Nano Banana
  - Flux
  - Kontext
  - Soul Cinema
  - Cinema Studio
negatives:
  - Do NOT invoke for post-production tasks (FFmpeg, Remotion, audio mixing)
  - Do NOT invoke for QA scoring (use video-qa-rubric.md)
  - Do NOT invoke for brief intake or shot planning (use brief-intake.md)
  - Do NOT invoke for study/research tasks
---

# Model Prompting Guide — Snelverhuizen Pipeline

Single reference document covering every model in the routing matrix. Replaces all prior prompting research. Last updated 2026-04-16 (4-agent verification sweep of Kling v3 Pro, NBP Edit, Flux Kontext + FLUX.2, Wan/Veo/Higgsfield/ElevenLabs).

---

## Part 1 — Hero Frame & Image Models

### Nano Banana Pro (Gemini 3 Pro Image)

Naming: "Nano Banana Pro" = Gemini 3 Pro Image. On AIMLAPI: `google/nano-banana-pro` (text-only) and `google/nano-banana-pro-edit` (reference-based). NBP is a "Thinking" model — natural language outperforms tag soup categorically.

**Prompt structure** — 3 to 6 sentences in natural creative-director language.

Formula: [Subject + specific adjectives] doing [Action] in [Location]. [Composition/Camera angle]. [Lighting/Atmosphere]. [Style/Media]. [Constraints or text to render].

- Prompts over ~200 words trigger internal summarization where earlier instructions fade
- Maximum input 65k tokens but practical sweet spot is far lower
- Use positive framing ("empty street" not "no cars")
- Edit-don't-reroll: when image is 80% correct, describe the specific change rather than starting from scratch

**Reference images (NBP Edit)** — Up to 14 per call, 6 with high fidelity.

- Control via natural language: "Use Image 1 as a strict identity reference. Use Image 2 as a composition reference only."
- Always label: "Image 1: Mourad character sheet. Image 2: Truck reference."
- For Mourad/Karel: 4-angle reference sheet (front, left profile, right profile, three-quarter) on clean neutral background as Image 1 in EVERY call
- Identity-locking phrases (UPDATED 2026-04-16): generic "preserve face" underperforms — enumerate features explicitly: *"Maintain identical eye shape, nose bridge contour, jawline angle, lip proportions, and skin texture as Image 1"*. Generic "preserve fabric texture" and "preserve logo" still work for non-face elements.
- Explicitly remove objects from previous scenes ("No longer holding the clipboard") — model persists them otherwise
- **Edit-chain ceiling:** ≤2 sequential edits per reference. Beyond that, April 2026 "smart-downgrading" pattern compounds — outputs go plastic/aged. Restart with original ref instead.
- **Smart-downgrading (April 2026):** under peak load Pro silently degrades — if face looks plastic or aged, re-run or compress input refs to ≤2K before upload.

**Aspect ratio** — Native 9:16 via `aspect_ratio: "9:16"` (top-level string, not nested imageConfig). Verified: 1K = 768×1344, 2K = 1536×2688, 4K = 3072×5376. 10 ratios supported: `1:1, 21:9, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 5:4, 4:5`.

Known issue: imageConfig sometimes silently falls back to 1:1/1K through proxy APIs. AIMLAPI honors top-level `aspect_ratio` string — keep using that. Always provide a reference image at correct aspect ratio as fallback anchor.

**Cost (AIMLAPI, verified 2026-04-16):** $0.195/generation flat across resolutions. Google direct rate is $0.134 at 2K / $0.24 at 4K — AIMLAPI charges single price. Log $0.195/image in cost ledger.

**Do NOT use Nano Banana 2 (`google/nano-banana-2`) as drop-in:** caps at 5 references and 5 aspect ratios. Breaks our 6-ref character workflow. Always pass explicit `model: "google/nano-banana-pro-edit"`.

**Parameters NOT exposed:** seed, guidance scale, CFG, negative prompt. All control via natural language. Do NOT import Stable Diffusion habits.

**Failure modes:**
- Phantom brand text on clothing → "plain uniform with no visible text, no logos, no writing on clothing"
- Expression drift in multi-turn editing → start new session, paste winning prompt verbatim, re-upload best output as fresh reference
- Safety filter silent failures → rephrase with neutral framing or add "illustration style" prefix

**API call (AIMLAPI):**
```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-pro-edit",
    "prompt": "Image 1: Mourad character reference sheet. Image 2: Truck reference. Generate Mourad standing next to the truck cab, three-quarter view. Keep facial features exactly the same as Image 1. Golden hour warm backlight, 85mm portrait lens, shallow depth of field, cinematic color grading, vertical composition.",
    "image_urls": [mourad_sheet_url, truck_ref_url],
    "aspect_ratio": "9:16",
    "resolution": "1K",
    "num_images": 1,
}, headers=headers, timeout=90)
```

---

### Flux Kontext Max + FLUX.2 Pro (Black Forest Labs)

Context (verified 2026-04-16): BFL has NOT officially deprecated Kontext — both lines coexist on bfl.ai/models and pricing pages. Earlier "previous-generation" framing is unverified. Treat as parallel tools, route by use case:
- **Brand color #FC8434 hero stills** → FLUX.2 Pro (HEX matching is real, ~33% cheaper at 9:16)
- **SNELVERHUIZEN.NL text rendering** → Kontext Max (independent Melies head-to-head: cleaner typography integration)
- **Multi-ref >3 refs** → Kontext Max (8 refs) or NBP Edit (14) — FLUX.2 Pro Edit on AIMLAPI caps at 3

**FLUX.2 Pro on AIMLAPI (NEW, 2026-04-16 verified):**
- Models: `blackforestlabs/flux-2-pro` (T2I), `blackforestlabs/flux-2-pro-edit` (I2I/multi-ref, max 3 refs)
- Pricing: ~$0.07/gen at 9:16 (1024×1792, 1.83MP × $0.039/MP) — vs Kontext Max $0.104/gen
- HEX syntax: natural-language form `"the color of X is color #FC8434"` or gradient form
- Dimensions: presets (`portrait_16_9`, etc.) OR custom 512–2048 in multiples of **32** (NOT 16 like direct BFL)
- `flux-2-pro` is "zero-config" — no `guidance_scale` parameter exposed
- `flux-2-pro-edit` exposes `guidance_scale` with example value 19 (different semantics from Kontext's 2.5–3.5) — **untested for our brand work, run canary first**
- March 3 2026: BFL doubled FLUX.2 generation speed at zero quality loss

**Prompt structure** — 30-80 word sweet spot. Maximum 512 tokens.

- FLUX does NOT support CLIP-style weighting — `(keyword:1.5)` and `++` are silently ignored
- Use natural emphasis: "with a strong focus on," "the most prominent element is"
- Token hierarchy (earlier tokens weigh more): subject → action/pose → environment → lighting → style
- For editing: clear action verbs (Change, add, remove, replace) + tell model what to keep

**Text rendering for SNELVERHUIZEN.NL** — 17 characters, upper edge of reliable rendering.
- Always use quotation marks: `"SNELVERHUIZEN.NL"`
- ALL CAPS in prompt → ALL CAPS out
- Specify font style: "bold, clean sans-serif font"
- Specify placement: "prominently displayed on the flat side panel"
- Annotation boxes: draw colored rectangles on input image for exact text placement
- Workaround: split "SNELVERHUIZEN" top line, ".NL" second line
- Generate batches of 3-5, select best text rendering
- If text morphs: generate truck text-free, composite in post

**Brand color #FC8434** — Use descriptive + material in Kontext Max: "glossy bright orange painted metal" not just "orange." Hex codes inconsistent in Kontext Max. FLUX.2 Pro has native HEX matching — verified syntax `"the color of [object] is color #FC8434"` (natural-language form).

**API parameters** — `guidance_scale: 2.5-3.5` (default 3.5, above 4.0 over-saturates). 9:16 = 768×1344. Up to 8 images in multi-image mode. Quality degrades after 6+ sequential edits — limit chains, use PNG between edits.

**API call (AIMLAPI):**
```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "flux/kontext-max/image-to-image",
    "prompt": "Place this exact truck on a quiet Dutch residential street. Keep all branding and text exactly the same. Golden hour warm sunlight, cinematic wide shot, vertical composition.",
    "image_url": [truck_ref_url],
    "aspect_ratio": "9:16",
    "num_images": 1,
}, headers=headers, timeout=90)
```

---

### Higgsfield Soul Cinema (Image Model)

Released March 4, 2026. Generates still images — designed as high-quality keyframe generator for I2V workflows.

**Strengths:** Deep textures, natural film grain, compositions that look like real film stills. 40+ curated cinematic presets (70s, 90s, 2000s cam). Toggleable prompt enhancer — turn OFF for character work where exact control is needed.

**Soul ID + Soul Cast** — Soul ID locks character identity from single reference. Soul Cast builds customizable AI actors (genre, era, archetype, physique, outfit, details). For Mourad/Karel: create Soul Cast actor each, use Soul ID for identity locking on every keyframe.

Specifically excels at skin textures and emotional range — addresses "plastic AI look."

**Cost** — ~0.25 credits/image. ~600 images from 150-credit Basic plan. Extremely cheap for frame factory before animating.

**Recommended pipeline workflow:** Soul Cinema frame → Soul ID lock → feed as first_frame_url to Seedance 2.0 or Kling 3.0 I2V → animate.

---

## Part 2 — Video Models (I2V Focused)

### Kling v3 Pro I2V

**THE FUNDAMENTAL I2V RULE: Never re-describe what's in the image. The image IS the scene description. Prompt contains ONLY motion instructions.**

**Prompt length:** 15-40 words. Write like a director's brief.

Formula: [Shot type], [focal length], [camera motion]. Subject [does specific motion]. [Environmental motion]. Constraints: preserve face, no morphing, no text, no new objects.

**Words that DESTROY shots (confirmed in V1-V3 feedback):**
- "breathing" / "breath" → unnatural chest pulsing
- "subtle natural movement" / "subtle motion" / "very subtle" → vague, causes morphing
- "moves" / "goes" → too generic, no anchor
- "emotional" → too vague for expression
- Contradictory instructions ("slow motion fast-paced")

**Words that WORK:**
- Stillness → "locked-off camera with tiny handheld micro-jitter" + environmental micro-motions only
- Single action → "Subject blinks once" — one clear action
- Walking → "heel-first, weight transfer" — physics-anchored
- Hands → "Her fingers firmly grip the edge of the cardboard box" — ALWAYS anchor to object
- Expression → "slight smile forming" or "eyes glistening" — staged not vague
- Stability → "preserve face structure," "stable geometry," "no face warp"
- Constraints → "no new objects, no text, no logos, no extra fingers"
- Motion endpoints → "then settles," "coming to rest," "eases to stop" — EVERY motion needs a defined endpoint

**Critical parameters:**

| Parameter | Character shots | Branded/truck shots | B-roll |
|-----------|----------------|---------------------|--------|
| cfg_scale | 0.5 (Atlas Cloud uses 0.8 for face-lock — A/B test on next character shot) | 0.7 | 0.4 |
| Duration | 5 sec max | 5 sec | 5-10 sec |
| generate_audio | false ALWAYS | false ALWAYS | false ALWAYS |
| aspect_ratio | "9:16" | "9:16" | "9:16" |
| Face adherence (Subject Binding) | 80-90 | N/A | N/A |

**⚠️ CRITICAL (verified 2026-04-16):** AIMLAPI now defaults `generate_audio: true` for Kling v3 Pro I2V. **Every API call MUST explicitly pass `"generate_audio": false`** — silent breakage risk if a code path omits this. Audio in our character clips destroys Shari'ah compliance.

Default face adherence of 42 is FAR too low for Mourad/Karel — MUST bump to 80-90 via Element Library with 3-4 reference photos.

**Element Library structure (verified 2026-04-16):** Max 4 elements per call, max 7 character elements per video, 2-4 reference images per element (1 main + 1-3 supplementary). Reference in prompt as `@Element1`, `@Element2`. Max 3 elements bound in start frame.

**Cost (AIMLAPI, verified 2026-04-16):** $0.291/sec → ~$1.46/5sec clip. Plan budget at $1.46/clip not $1.64.

**Generation latency:** 60-180 seconds per call. Expect 3-5 attempts per production-quality clip — bake into ceiling math.

**Endpoints (both still work, verified 2026-04-16):**
- Universal: `https://api.aimlapi.com/v2/video/generations`
- Legacy: `https://api.aimlapi.com/v2/generate/video/kling/generation`

**Anti-ghost-driving for trucks:**
- Prompt MUST contain: "stationary truck, parked, no vehicle movement, no forward creep"
- Add rigidity: "the vehicle remains rigid and solid, metal does not deform"
- Use start + end frame showing same vehicle position to force stationarity
- Use Motion Brush to paint which areas move — leave vehicle body unpainted
- Negative: "vehicle movement, driving, rolling, ghost driving, no distortion in vehicle proportions"

**Negative prompt template:**
```
morphing, de-aging, shifting jawline, changing clothes, suit color shift,
skin changes, extra fingers, bad hands, distorted hands, extra limbs,
text morphing, garbled text, blurry, flickering, jittery movement,
vehicle movement, driving, rolling, ghost driving, breathing motion,
chest expansion, body sway, expression change
```

**v3 vs v2 for character work** — v3 Unified Spatial Anchor: identity drift dropped from 50%+ (v2.6) to <10% (v3). Also: 15s clips, multi-shot up to 6 scenes, native 4K, advanced physics. Subject Binding improvement is the single biggest reason to use v3.

**API call (AIMLAPI):**
```python
resp = httpx.post("https://api.aimlapi.com/v2/generate/video/kling/generation", json={
    "model": "klingai/video-v3-pro-image-to-video",
    "image_url": hero_frame_url,
    "prompt": "Locked-off camera, subject maintains warm expression, gentle golden hour light plays across face, eases to stop",
    "duration": "5",
    "aspect_ratio": "9:16",
    "generate_audio": False,
    "cfg_scale": 0.5,
    "negative_prompt": "morphing, shifting jawline, extra fingers, text morphing, garbled text, blurry, flickering, jittery, vehicle movement, ghost driving, breathing motion, expression change",
}, headers=headers, timeout=60)
```

---

### Seedance 2.0 (ByteDance)

**Why Seedance for characters** — The @ reference tagging system. Bind uploaded images to specific elements: @image1 = main character, @image2 = truck. Creates persistent conditioning anchors across generations. Independent testing: 90-second narrative, same protagonist, 8 actions, ~5% variance — commercially viable.

**Prompt structure** — 30-80 words. Shorter causes hallucination; longer gets selectively ignored.

Formula: [Camera/shot type], [Subject with @ references], [Action/motion], [Environment], [Lighting], [Visual style].

- Lead with camera direction
- Specific cinematic language: "Dolly zoom", "rack focus", "handheld"
- Temporal markers for multi-shot: "Shot 1 | 0s-3s"
- Replace vague adjectives — "warm golden hour backlight on weathered steel" not "beautiful"
- CRITICAL: ONE camera movement per generation. Combining dolly zoom + pan produces artifacts.

**Negative prompts** — Do NOT work on 1.0, limited on 2.0. Use positive specification instead: "parked truck, engine off, completely stationary" with `camera_fixed: true`.

**Parameters:**

| Parameter | Value |
|-----------|-------|
| Resolution | Up to native 2K (2048×1080) |
| Duration | 4-15s |
| Aspect ratio | 7 options including 21:9 |
| camera_fixed | true for static shots |
| first_frame_url | Hero frame URL for I2V |
| Reference strength | 70-80% sweet spot (>85% rigid, <60% drift) |

**Reference image rules:**
- FEWER references (2-3 tightly controlled, same lighting) > more (6+ causes identity averaging)
- 3-Angle Rule: front, three-quarter, profile from same lighting session
- Re-anchor periodically using ORIGINAL reference, not generated frames (accumulate drift)
- Lock seed after first successful identity verification

**I2V reduces facial drift ~80% vs T2V.**

**Seedance 2.0 vs 1.0 Pro** — Generation leap: 1080p → native 2K, 2-12s → 4-15s, native audio-video synthesis, multilingual lip-sync 8+ languages, Omni-reference (9 images + 3 video + 3 audio as inputs), Environment Lock maintains background stability for 15s.

**Pricing across providers:**
- Atlas Cloud: $0.022/sec Fast — cheapest
- AIMLAPI: $0.316/sec Fast
- fal.ai: ~$0.62-0.74/5s 1080p
- Segmind: 8-10s 720p under $1

**CRITICAL LIMITATION ON AIMLAPI: Seedance 2.0 is BLOCKED for human faces (content_policy_violation, tested 3x April 2026). Additionally, AIMLAPI only supports 480p/720p for Seedance, NOT 1080p. Two separate issues: (1) content policy blocks all realistic human faces in I2V, (2) resolution limited to 720p max. For Seedance with characters: consider Atlas Cloud ($0.022/sec) as alternative provider.**

**Failure modes & fixes:**

| Failure | Fix |
|---------|-----|
| Expression drift | Same expression all refs; lock age range; ref strength 70-80% |
| Ghost driving | camera_fixed: true; "parked, engine off, stationary"; I2V from static |
| Text morphing | Generate without text; composite in post |
| Face warp / extra limbs | Max 2 characters per scene; physical distance |
| Jittery footage | One camera move per generation |
| Prompt ignoring | 30-80 words; one primary action |
| Edge artifacts | Break into hero + cutaway; under 8 seconds |

---

### Higgsfield Cinema Studio 3.0 (Workflow, NOT a model)

Built on Seedance 2.0 as underlying model. Launched March 30, 2026.

**What it adds:** Deterministic optical physics, virtual camera rig (ARRI, Panavision), lens types including anamorphic, focal length/aperture/DOF, stack up to 3 simultaneous camera movements, 8 speed ramp presets, color grading without re-rendering. Upload 9 references, write narrative prompt, reasoning engine breaks into shots with character consistency.

**Cost** — Significant. ~76 credits per clip. ~35% hit rate. Restricted to Business Plan.

**CRITICAL for pipeline:** Web-UI ONLY. Not accessible via API. Multi-reference workflow, genre system, camera rig, reasoning engine cannot be automated. Only paths: (1) Playwright browser automation (fragile), (2) manual hero-shot tool for 1-2 key shots per ad.

### Higgsfield Cloud API

Real but immature. Endpoint: cloud.higgsfield.ai. SDK: `pip install higgsfield-client`. Auth via API key + secret. Supports async/await, file uploads, webhook notifications via `webhook_url`. Rate limits undocumented (429s require exponential backoff). API exposes underlying models ONLY — NOT Cinema Studio workflows, Soul Cast, color grading, or LipSync Studio.

**Recommendation:** Test API for Kling v3 Pro where webhooks eliminate polling. Keep Playwright as fallback for Cinema Studio 3.0.

---

## Part 3 — Workflow Chaining (Image → Video)

The 2026 standard: "ingredients-to-video" — generate locked hero frames first, storyboard in Figma for QA, animate only approved frames. I2V model's job = "moving pixels that already exist."

**Hero frame characteristics that survive animation:**
- Leave room for motion — don't fill entire frame. Add atmospheric elements (fog, haze, bokeh)
- Neutral stable pose — front or three-quarter, mouth closed, even expression
- Simple uncluttered backgrounds — solid colors or gradients most stable
- Avoid complex intersections — hands meeting objects, arms crossing body, hair over face
- Soft diffused lighting from clear direction
- **NO text or logos in the frame** — they WILL warp during animation
- Generate at higher resolution than I2V native (4K source for 1080p video)
- Bokeh/DOF — blurred backgrounds survive far better than sharp detailed ones

**Same-ecosystem advantage:** Gemini latent space "speaks same language" as Veo 3.1. Cross-ecosystem (NBP → Kling, Flux → Kling) works but introduces more boundary artifacts.

**Plan for 4:1 generation-to-usable ratio** — for 5 seconds usable, generate 20 seconds and cull.

---

## Part 4 — Character Consistency for Mourad and Karel

### Three-Layer Identity Anchoring

**Layer 1 — Character reference sheet (8-10 images per character):**
Generate large batch (50-100), select "golden" image, generate variations for poses while maintaining identity. Arrange front/side/three-quarter/full-body into composite. Include close-ups of uniform details with exact color codes and logo placement.

**Layer 2 — Text-based identity header (paste at TOP of EVERY prompt — IDENTICAL across all calls):**

```
Mourad — 32-year-old Dutch-Moroccan man, short black beard, warm brown eyes,
broad shoulders, oval face with high cheekbones. Wearing black crewneck
sweatshirt with small orange Snelverhuizen logo on left chest, large orange
logo on back, blue jeans, white AF1-style sneakers. Athletic build, 5'10".

Karel — Large stocky build, completely bald with dark full beard, fair light
skin. Wearing identical black crewneck sweatshirt with small orange
Snelverhuizen logo on left chest, blue denim jeans, white sneakers.
```

Even slightly different descriptions produce different faces. MUST be identical across calls.

**Layer 3 — API-level identity preservation:**
- Kling v3: Subject Binding ON, 3-4 refs in Element Library, face adherence 80-90
- Seedance 2.0: @ reference tagging, 2-3 photos same lighting, ref strength 70-80%, locked seed
- NBP Edit: Character sheet as Image 1 every call, "preserve face" language

### Cloud LoRA Training (no local GPU)

For maximum fidelity: train LoRA per character on Imagera (~$5/run, 15-45 min) or Replicate (~90 min). Upload 15-30 curated refs. Assign trigger words (mourad_mover, karel_mover). Deploy via API.

### Zero-shot Alternatives
- InstantID (Replicate): zero-shot from one face. instantid_weight: 0.6, ipadapter_weight: 0.7
- IP-Adapter-FaceID: face recognition embeddings. FaceID-Portrait variant accepts multiple faces without LoRA

---

## Part 5 — Text in AI Video is Broken — Workarounds

**Universal finding April 2026:** Text rendering in AI video is fundamentally unreliable. Models process text as visual texture, not semantic content. Temporal diffusion reinterprets patterns frame-by-frame causing progressive degradation. "SNELVERHUIZEN.NL" → "www.sedeerhuiren.nl" is expected behavior, not a bug.

**The only reliable solution: post-production overlay.**

1. Generate hero frame with blank truck panel (solid #FC8434, no text)
2. Run I2V — focus on motion only, negative: "text, garbled, logos"
3. Import into After Effects
4. Mocha AE planar tracking on truck side panel
5. Create text layer with exact brand typography
6. Apply corner pin tracking data
7. Match perspective, add grain, apply motion blur

**For static camera + truck drives through:** Skip tracking. Place "SNELVERHUIZEN.NL" as static screen overlay (lower-third or title card).

**If text MUST be baked in (rare, ≤3s, minimal motion):** Large font, max contrast, sans-serif, placed in non-moving areas. Use Kling Motion Brush to mask text area as static. Add "maintain label text" and "preserve product shape." Even with all precautions, reliability below production standards.

---

## Part 6 — Routing Matrix

No single model excels at everything. Each failure mode maps to a specific model strength.

| Shot type | Primary model | Why | Fallback |
|-----------|---------------|-----|----------|
| Character close-up/dialogue | Kling v3 Pro I2V (Subject Binding 80-90) | Identity drift <10%, native 4K, reliable on AIMLAPI | — |
| Truck/vehicle shots | Kling v3 Pro I2V | Physics, I2V from static, camera_fixed, anti-ghost-driving | Kling Standard |
| Wide establishing | **Veo 3.1 Lite** (`google/veo-3-1-lite-generate-preview`) | Native 9:16, first+last frame control, cheap | Kling v3 Standard |
| B-roll/transitions | **Veo 3.1 Lite** or Wan 2.5 Preview (`wan-2-5-image-to-video`) | Wan 2.5 Preview cheaper + better than Wan 2.2 ($0.065/480p, $0.13/720p, $0.195/1080p, 10s @ 24fps) | Kling Standard |
| Hero frames (still) | NBP Edit ($0.195/img) or Soul Cinema | Cinematic-grade keyframes | Flux Kontext Max |
| Brand color #FC8434 stills | **FLUX.2 Pro** (`blackforestlabs/flux-2-pro`) | Native HEX matching, ~33% cheaper at 9:16 vs Kontext | Kontext Max |
| SNELVERHUIZEN.NL text stills | Flux Kontext Max | Cleaner typography integration than FLUX.2 (Melies head-to-head) | NBP Edit + post |
| Multi-ref hero (>3 refs) | NBP Edit (14 refs) or Kontext Max (8 refs) | FLUX.2 Pro Edit on AIMLAPI caps at 3 refs | — |
| Text + brand elements | Image layer + post overlay | Video models cannot do text | After Effects + Mocha |
| Hero shot manual cinematic | Cinema Studio 3.0 (web UI only — no API) | Camera rig, reasoning engine | Kling v3 Pro raw API |

**Seedance 2.0 — PERMANENTLY BLOCKED for human faces (verified 2026-04-16):** ByteDance officially suspended the Face-to-Voice feature on 2026-02-10 over privacy. Jimeng/Dreamina operators globally block real-human-like reference photos. U.S. Senate halted Seedance on copyright grounds 2026-03-18. Global API launch quietly delayed indefinitely (TheSource report 2026-04-15). **Atlas Cloud also does not list Seedance 2.0** — no longer a viable alternative. The block is policy, not technical — will not be resolved. DO NOT consider Seedance for character shots. Workaround: stylized/anime references bypass filter (irrelevant to our brand). Stop spending API calls testing this.

**Cost tier — 30-second ad (6-8 clips, verified 2026-04-16):**
- 3-4 b-roll via Veo 3.1 Lite or Wan 2.5 Preview: ~$0.13-0.20 each
- 3-4 hero via Kling v3 Pro: ~$1.46 each (5sec at $0.291/sec)
- 4-6 NBP Edit hero frames: $0.195 each
- Multiply by 1.5 for failure rate + 3-5 variations per hero
- ElevenLabs VO: ~$0.50/video
- Realistic budget: **$8-15 per finished approved ad** including iterations (down from $15-50 — primary drivers: NBP cheaper than per-image-quoted, Kling Pro slightly cheaper than estimated, Veo 3.1 Lite displaces Wan 2.2)

**Provider note:** fal.ai 50% market share for image APIs, 44% video. 30-50% cheaper than Replicate. Doesn't charge for failed generations. Atlas Cloud cheapest for Seedance ($0.022/sec) — only relevant if Atlas Cloud is added and Seedance block is resolved. Benchmark AIMLAPI against these.

### Three-Try Fallback Chain

**Try 1:** Route to primary per matrix. Automated QA: DINO similarity >0.85 (subject), CLIP similarity >0.90 (background).

**Try 2:** On failure, escalate. Character failures → Kling 3.0 Subject Binding. Product failures → Kling v3 Pro I2V with increased cfg_scale (BLOCKED on AIMLAPI: Seedance 2.0 — skip unless Atlas Cloud active). Action failures → Cinema Studio 3.0 manual.

**Try 3:** Conservative fallback. Reduce motion to 0.3, shorten to 3-4s, static or slow pan camera.

**Detection methods:**
- Expression drift: InsightFace/ArcFace face embeddings per frame, cosine similarity <0.80 = drift
- Ghost driving: Vehicle bounding boxes per frame, flag implausible motion vectors

---

## Part 7 — Update Mechanism

Static prompt libraries become stale within a month. Four layers: monitoring, alerts, versioned templates, regression testing.

### Monitoring Sources
- **Artificial Analysis Video Arena** (artificialanalysis.ai/video) — weekly check, ELO rankings, speed, pricing
- Kling AI Official Discord (~48k members) — real-time regressions
- r/aivideo (~160k) — primary subreddit
- X/Twitter: @Kling_ai, @runwayml, @ArtificialAnlys
- Magic Hour AI Video Model Release Tracker — curated, confirmed only

### Automated Monitoring
n8n workflow: RSS feeds → AI summarization → Telegram alerts. Feeds: Runway changelog, HuggingFace blog, Artificial Analysis.

### Prompt Library Structure
Git repo with YAML templates: model/version/shot_type. Each template: prompt text, parameters, model-specific notes, last quality score, changelog. Template inheritance: base per shot type with model-specific overrides.

### Re-auditing Cadence
- Within 48h of model release: canary tests of top 5 prompts
- Weekly: quick tests on high-traffic prompts
- Bi-weekly: full regression across active models
- Monthly: leaderboard review and competitive eval
- Quarterly: full library audit, deprecate stale, update metadata

### Evaluate-Before-Adopt
When new model drops, do NOT immediately switch:
1. Monitor community 24-48h
2. Canary test golden suite within 48h
3. Evaluate 1 week — quality vs baseline, cost, prompt compatibility
4. Decide: adopt / adapt (model-specific overrides) / skip
5. Stage rollout: shadow → internal → 10% → 50% → 100% with rollback

---

## Summary — Highest-Impact Changes

1. **Route character shots to Kling v3 Pro I2V** with Subject Binding 80-90, 3-4 reference photos in Element Library, cfg_scale 0.5 (A/B test 0.8 next character clip — Atlas Cloud uses 0.8 for face-locked work). Seedance 2.0 is PERMANENTLY BLOCKED for human faces — policy block, not technical, will not be resolved.

2. **Route truck shots to Kling v3 Pro I2V** with I2V from high-quality static hero (Flux Kontext / NBP source), camera_fixed/stationary language, identical start/end frame. Directly addresses ghost driving.

3. **Eliminate text from ALL video generations** — render text/logos in image layer, composite in post. No current video model renders text reliably. Eliminates text morphing completely.

4. **⚠️ ALWAYS pass `generate_audio: false` explicitly to Kling v3 Pro on AIMLAPI** — default flipped to TRUE in 2026-04-16 verification. Audio in clips destroys Shari'ah compliance.

5. **Replace generic "preserve face" with enumerated features in NBP Edit prompts** — *"Maintain identical eye shape, nose bridge contour, jawline angle, lip proportions, and skin texture as Image 1"*. Outperforms generic phrasing.

6. **Use ElevenLabs Forced Alignment API (`POST /v1/forced-alignment`) for word-level timestamps**, NOT TTS-with-timestamps endpoint (char-level only). Likely root cause of V2 caption sync issues.

7. **Update fallback B-roll routing to Veo 3.1 Lite** (`google/veo-3-1-lite-generate-preview`) — native 9:16, first+last frame control, cheaper than Wan 2.2. Use Wan 2.5 Preview as Wan tier upgrade.

8. **Route brand-color #FC8434 stills to FLUX.2 Pro** (`blackforestlabs/flux-2-pro`) — verified HEX matching, ~33% cheaper at 9:16 vs Kontext Max. Keep Kontext Max for SNELVERHUIZEN.NL text rendering only.
