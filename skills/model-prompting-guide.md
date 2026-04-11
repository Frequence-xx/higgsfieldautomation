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

Single reference document covering every model in the routing matrix. Replaces all prior prompting research. Last updated 2026-04-11.

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
- Identity-locking phrases: "Keep facial features exactly the same as Image 1", "preserve the face", "preserve fabric texture", "preserve logo"
- Explicitly remove objects from previous scenes ("No longer holding the clipboard") — model persists them otherwise

**Aspect ratio** — Native 9:16 via `aspect_ratio: "9:16"`. Verified: 1K = 768×1344, 2K = 1536×2688, 4K = 3072×5376.

Known issue: imageConfig sometimes ignored through proxy APIs — always provide a reference image at correct aspect ratio as fallback anchor.

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

### Flux Kontext Max (Black Forest Labs)

Context: BFL now labels Kontext as "previous-generation" and recommends FLUX.2 Pro for new projects (92% accuracy on complex layouts, native HEX color matching, multi-reference). If FLUX.2 Pro is available, prefer it for SNELVERHUIZEN text and brand color #FC8434.

When to use Max over Pro: when getting text right on first attempt matters. Max uses more compute for prompt adherence and typography.

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

**Brand color #FC8434** — Use descriptive + material: "glossy bright orange painted metal" not just "orange." Hex codes inconsistent in Max. FLUX.2 Pro has native HEX matching: format `hex #FC8434 bright orange`.

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
| cfg_scale | 0.5 | 0.7 | 0.4 |
| Duration | 5 sec max | 5 sec | 5-10 sec |
| generate_audio | false ALWAYS | false ALWAYS | false ALWAYS |
| aspect_ratio | "9:16" | "9:16" | "9:16" |
| Face adherence (Subject Binding) | 80-90 | N/A | N/A |

Default face adherence of 42 is FAR too low for Mourad/Karel — MUST bump to 80-90 via Element Library with 3-4 reference photos.

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
| Character close-up/dialogue | Seedance 2.0 | @ reference, 70-80% strength, locked seed | Kling 3.0 Subject Binding 80-90 |
| Truck/vehicle shots | Kling 3.0 Pro | Physics, I2V from static, camera_fixed | Seedance 2.0 Environment Lock |
| Wide establishing | Kling 3.0 Standard or Veo 3.1 | Cheap, good for non-hero | Wan 2.2 |
| B-roll/transitions | Wan 2.2 or Veo 3.1 Light | Lowest cost | Kling Standard |
| Hero frames (still) | NBP Edit or Soul Cinema | Cinematic-grade keyframes | Flux Kontext Max |
| Truck/brand stills | Flux Kontext Max (or Flux 2 Pro for HEX) | Best text rendering | NBP for non-text |
| Text + brand elements | Image layer + post overlay | Video models cannot do text | After Effects + Mocha |
| Hero shot manual cinematic | Cinema Studio 3.0 (web UI) | Camera rig, reasoning engine | Seedance 2.0 raw API |

**Cost tier — 30-second ad (6-8 clips):**
- 3-4 b-roll via Kling Standard / Wan 2.2: $0.50-0.70 each
- 3-4 hero via Seedance 2.0 / Kling Pro: $1.30-2.80 each
- Multiply by 1.5 for failure rate + 3-5 variations per hero
- Realistic budget: **$15-50 per finished approved ad** including iterations

**Provider note:** fal.ai 50% market share for image APIs, 44% video. 30-50% cheaper than Replicate. Doesn't charge for failed generations. Atlas Cloud cheapest for Seedance ($0.022/sec). Benchmark AIMLAPI against these.

### Three-Try Fallback Chain

**Try 1:** Route to primary per matrix. Automated QA: DINO similarity >0.85 (subject), CLIP similarity >0.90 (background).

**Try 2:** On failure, escalate. Character failures → Kling 3.0 Subject Binding. Product failures → Seedance 2.0 Environment Lock. Action failures → Cinema Studio 3.0 manual.

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

## Summary — Three Highest-Impact Changes

1. **Route character shots to Seedance 2.0** with @ reference system, 2-3 tightly controlled references from same lighting session, strength 70-80%, locked seed. Directly addresses expression drift.

2. **Route truck shots to Kling 3.0 Pro** with I2V from high-quality static hero (Flux/NBP source), camera_fixed/stationary language, identical start/end frame. Directly addresses ghost driving.

3. **Eliminate text from ALL video generations** — render text/logos in image layer, composite in post. No current video model renders text reliably. Eliminates text morphing completely.
