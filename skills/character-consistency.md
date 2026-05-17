---
name: Character Consistency
description: Maintains visual consistency for recurring characters (crew, family archetypes) across multiple shots and videos using reference anchoring and prompt structure.
autoInvoke: true
triggers:
  - character
  - crew member
  - person
  - family
  - consistent
  - reference image
  - anchor
negatives:
  - Do NOT invoke when generating shots with no people (truck-only, B-roll, establishing shots)
  - Do NOT invoke when doing post-production or caption work
  - Do NOT invoke when the shot uses a Type C generic one-off person in a wide/silhouette framing
---

# Character Consistency System

## The Problem
AI models drift: a crew member's face, build, skin tone, and clothing change between shots. Without explicit anchoring, every generation treats characters as new.

## AIMLAPI Character Reference Models

| Stage | Model | Param | Max Refs | Use For |
|-------|-------|-------|----------|---------|
| Hero frame with character lock | `flux/kontext-max/image-to-image` | `image_url` (array) | 4 | Lock character identity across scenes |
| Compositing character into scene | `google/nano-banana-pro-edit` | `image_urls` (array) | **14** | Place character into any background |
| Character-consistent video | `klingai/video-o1-reference-to-video` | `elements` + `image_list` | 4 elements, 7 total | Video with locked character identity |
| High-quality character video | `google/veo-3.1-reference-to-video` | `image_urls` (array) | ~3+ | Premium character video |

## Step-by-Step Workflow

### Step 1: Create Character Reference Sheet
For each recurring character, MUST generate 4 reference images using Nano Banana Pro.
Use 1:1 for reference sheets (consistency matching), 9:16 for final hero frames.

```python
# Generate 4 angles of the character via AIMLAPI
for angle in ["front view", "3/4 angle from left", "profile from right side", "full body standing"]:
    resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
        "model": "google/nano-banana-pro",
        "prompt": f"A 37-year-old Dutch man with short dark brown hair, medium olive skin, clean shaven, wearing a navy blue polo shirt with company logo on left chest and dark grey cargo trousers with black work boots, {angle}, professional photography, neutral background",
        "aspect_ratio": "1:1",
        "resolution": "1K",
    }, headers=headers, timeout=60)
```

Save to `/opt/pipeline/assets/characters/{name}/`.

### Step 2: Lock Character via Flux Kontext Max

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "flux/kontext-max/image-to-image",
    "prompt": "Place this person on a Dutch suburban street next to a white moving truck, golden hour lighting, cinematic vertical composition, 35mm lens",
    "image_url": [
        "https://cdn.example.com/characters/crew_lead/front.png",
        "https://cdn.example.com/characters/crew_lead/three_quarter.png"
    ],
    "aspect_ratio": "9:16",
    "num_images": 1,
}, headers=headers, timeout=90)
hero_frame_url = resp.json()["data"][0]["url"]
```

### Step 3: Animate with Character Reference (Kling O1)

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/video-o1-reference-to-video",
    "prompt": "The person from @Element1 walks confidently towards the moving truck, picks up a box, golden hour light",
    "elements": [
        {
            "frontal_image_url": "https://cdn.example.com/characters/crew_lead/front.png",
            "reference_image_urls": [
                "https://cdn.example.com/characters/crew_lead/three_quarter.png",
                "https://cdn.example.com/characters/crew_lead/profile.png"
            ]
        }
    ],
    "duration": 5,
    "aspect_ratio": "16:9"
}, headers=headers)
```

**Important:** Elements extract face + posture + clothing together. **No face_weight API parameter exists on AIMLAPI.** "Subject Binding 80-90" in CLAUDE.md is a quality target, not a parameter.

### Step 3b: Multi-Character Scene

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/video-o1-reference-to-video",
    "prompt": "@Element1 and @Element2 carry boxes together towards the truck, natural collaboration, golden hour",
    "elements": [
        {"frontal_image_url": "mourad/front.png", "reference_image_urls": ["mourad/three_quarter.png", "mourad/profile.png"]},
        {"frontal_image_url": "karel/front.png", "reference_image_urls": ["karel/three_quarter.png", "karel/profile.png"]}
    ],
    "generate_audio": False,
    "duration": 5,
    "aspect_ratio": "9:16"
}, headers=headers)
```

**Multi-character known failure mode:** Feature swapping when characters touch or overlap. Mitigation: keep characters spatially separated in prompt, run InsightFace QA on BOTH.

### Step 3c: Video-Based Element

```python
"elements": [{"video_url": "https://cdn.example.com/characters/mourad/reference_clip.mp4"}]
```

Best for carrying consistency forward from clip N to clip N+1.

### Step 4: Alternative — Nano Banana Pro Edit

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-pro-edit",
    "image_urls": ["crew_lead/front.png", "crew_lead/full_body.png", "dutch_street_golden_hour.png"],
    "prompt": "Place the person from the first two images into the street scene from the third image",
    "aspect_ratio": "9:16",
    "resolution": "1K",
}, headers=headers, timeout=60)
```

### Step 4b: Flux Kontext Max — Noun-Phrase Prompts (no pronouns)

When using `flux/kontext-max/image-to-image` for character hero frames, **always describe the character in the prompt with noun phrases, never pronouns**. The model treats each reference independently and has no pronoun resolution.

**DO:** `"The man with short dark brown hair and medium olive skin, wearing a navy blue polo, stands next to the truck"`
**DON'T:** `"He stands next to the truck"` — "he" is ignored, identity reverts to model default

Up to 10 reference images are technically supported; 3–5 covering distinct angles (front, 3/4, profile, full body) is the practical optimum. Beyond 5, references compete and consistency degrades.

### Step 5: Character Metadata (character.json)

```json
{
  "name": "Crew Lead",
  "gender": "male",
  "approximate_age": "35-40",
  "build": "medium athletic",
  "skin_tone": "medium olive",
  "hair": "short dark brown",
  "uniform": "navy blue polo with Snel Verhuizen logo on left chest, dark grey cargo trousers, black work boots",
  "distinguishing": "clean shaven, friendly expression",
  "prompt_snippet": "a 37-year-old man with short dark brown hair, medium olive skin, clean shaven, wearing a navy blue polo shirt with company logo and dark grey cargo trousers with black work boots",
  "reference_urls": {
    "front": "/assets/characters/crew_lead/front.png",
    "three_quarter": "/assets/characters/crew_lead/three_quarter.png",
    "profile": "/assets/characters/crew_lead/profile.png",
    "full_body": "/assets/characters/crew_lead/full_body.png"
  }
}
```

### Step 6: QA Check for Character Drift

```python
from insightface.app import FaceAnalysis
import cv2, numpy as np

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=-1, det_size=(640, 640))  # init once per session

def clip_qa(ref_path: str, frame_paths: list[str]) -> dict:
    ref_img = cv2.imread(ref_path)
    ref_faces = app.get(ref_img)
    if not ref_faces:
        return {"error": "no face in reference"}
    ref_emb = ref_faces[0].normed_embedding  # already L2-normalized

    results = {}
    labels = ["t0", "t2_5", "t5"]
    for label, path in zip(labels, frame_paths):
        img = cv2.imread(path)
        faces = app.get(img)
        if not faces:
            results[label] = 0.0
        else:
            emb = faces[0].normed_embedding
            results[label] = float(np.dot(ref_emb, emb))  # cosine sim (no division needed)
    return results

# PASS if all scores >= 0.68; note if 0.60-0.67; retry if < 0.60; reject if < 0.50
```

**Threshold guide (buffalo_l model):**

| Score | Meaning | Action |
|-------|---------|--------|
| ≥ 0.68 | Strong identity match | PASS |
| 0.60 – 0.67 | Acceptable drift | PASS with note |
| 0.50 – 0.59 | Marginal | RETRY |
| < 0.50 | Identity failure | REJECT — try FaceFusion fallback |

**Skin-tone bias correction (pass 4 finding):** buffalo_l was trained predominantly on lighter-skinned subjects. For olive/brown skin characters (Karel, Mourad), the model produces systematically lower cosine scores at the same identity. **Lower the RETRY threshold to 0.42–0.45 for these characters** to avoid false QA rejects. The REJECT floor stays at 0.40 (below which identity failure is genuine). Calibrate per character by scoring 4 approved reference images against each other — the lowest pair score is the effective floor.

```python
# Character-specific threshold example:
THRESHOLDS = {
    "karel":  {"pass": 0.62, "note": 0.55, "retry": 0.42, "reject": 0.40},
    "mourad": {"pass": 0.62, "note": 0.55, "retry": 0.42, "reject": 0.40},
    "generic_light_skin": {"pass": 0.68, "note": 0.60, "retry": 0.50, "reject": 0.50},
}
```

**buffalo_l vs antelopev2 (pass 5 finding):** antelopev2 uses an R100 backbone (vs buffalo_l's R50) and outperforms buffalo_l on IJB-C per InsightFace's own model table. Upgrade path:
```python
# Upgrade: R100 backbone, better identity accuracy on harder cases
app = FaceAnalysis(name='antelopev2')
app.prepare(ctx_id=-1, det_size=(640, 640))
# NOTE: antelopev2 produces lower raw cosine values than buffalo_l for the same identity.
# Confirmed threshold range for 1:1 verification: 0.30–0.45 cosine at FMR=1e-4 to 1e-5
# (pass 6 finding, 2026-05-17). Start retry threshold at 0.30, not 0.42–0.50.
# Requires manual model download: pip install insightface then run prepare() once to auto-fetch.
```
**Current production model stays buffalo_l** (auto-downloads, validated thresholds). Upgrade to antelopev2 only after re-calibrating thresholds on approved character sheets.

**AuraFace** (open-source, commercially licensed): ResNet100 + ArcFace, drop-in ONNX replacement for buffalo_l's recognition head. Key advantage: BSD license (buffalo_l ONNX models carry non-commercial restriction). **LFW benchmark confirmed at 99.65%** (pass 6 finding, 2026-05-17). Multiple production teams have validated it. Recommended upgrade path from buffalo_l when BSD licensing matters. No per-demographic benchmark published yet; calibrate thresholds per character as with antelopev2.

### FaceFusion Fallback (identity score < 0.50)

FaceFusion v3.6.0+ uses a **job-based architecture** — `run` is replaced by `headless-run`. The old `python facefusion.py run --headless` syntax is broken in v3.

```bash
conda create -n facefusion python=3.12 -y && conda activate facefusion
git clone https://github.com/facefusion/facefusion && cd facefusion && python install.py

# v3.6.0+ syntax (headless-run, NOT run)
python facefusion.py headless-run \
  --source-paths /path/to/approved_character_front.png \
  --target-path /path/to/failed_clip.mp4 \
  --output-path /path/to/fixed_clip.mp4 \
  --processors face_swapper face_enhancer \
  --face-swapper-model inswapper_128_fp16 \
  --face-selector-mode reference \
  --reference-face-position 0 \
  --face-enhancer-model gfpgan_1.4 \
  --face-enhancer-blend 80
```

**v3 model change:** `hyperswap_1a_256` is the new default face swapper. Use `inswapper_128_fp16` explicitly for highest quality (especially for non-white skin fidelity).

**New parameters in v3.4.0–v3.5.0 (pass 6 findings, 2026-05-17):**

```bash
# --face-swapper-weight (v3.4.0+): source-target balance. Default 1.0 (full source identity).
# Use 0.8 for olive/brown skin to reduce over-swap artifacts and preserve skin tone nuance.
python facefusion.py headless-run \
  --source-paths /path/to/approved_character_front.png \
  --target-path /path/to/failed_clip.mp4 \
  --output-path /path/to/fixed_clip.mp4 \
  --processors face_swapper face_enhancer \
  --face-swapper-model inswapper_128_fp16 \
  --face-swapper-weight 0.8 \
  --face-selector-mode reference \
  --reference-face-position 0 \
  --face-enhancer-model gfpgan_1.4 \
  --face-enhancer-blend 80 \
  --output-video-encoder libx264rgb   # prevents RGB→YUV color shift on brown/olive skin

# face_dat_x4 frame processor (v3.5.0+): 4× face detail upscaler.
# Use instead of (or after) face_enhancer when GFPGAN over-smooths.
# Replace --processors face_swapper face_enhancer with:
#   --processors face_swapper face_dat_x4

# --face-detector-margin (v3.5.0+): extend detection box beyond frame edge.
# Add when character face is partially cropped at clip edge.
```

Re-run InsightFace QA after FaceFusion. Score should be ≥ 0.65.

**CodeFormer alternative (better for olive/brown skin):** GFPGAN can whiten/flatten brown skin features at high fidelity. Use CodeFormer with `w=0.5–0.6` instead — lower w preserves skin tone accuracy.

```bash
# CodeFormer face restoration (better for non-white skin than GFPGAN)
python inference_codeformer.py \
  -w 0.6 \
  --input_path /path/to/failed_clip.mp4 \
  --output_path /path/to/fixed_clip.mp4 \
  --face_upsample \
  --bg_upsampler realesrgan
# w=0.5-0.6: preserve skin tone; w>0.7: over-smooth, whitens features
```

**ComfyUI InstantID + IP-Adapter + FaceDetailer stack (best quality, most effort):**
For clips where FaceFusion produces unnatural results (stiff face, wrong skin tone):
1. InstantID node: inject reference face identity
2. IP-Adapter node: match pose + lighting from reference
3. FaceDetailer node: CodeFormer polish (w=0.6)
Best for non-celebrity, non-white subjects. Setup time: ~2h first run.

## Model Selection for Character Shots

| Scenario | Image Model | Video Model | Cost Est. |
|----------|-------------|-------------|----------|
| Karel/Mourad alone | Nano Banana Pro Edit | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |
| Multiple characters | Nano Banana Pro Edit (14 refs) | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |
| Generic one-off person | Nano Banana Pro (no refs) | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |

## Character Types — Decision Tree

### Type A: Existing Characters (Karel & Mourad)
Ref sheets at `/opt/pipeline/assets/crew/`. Use Nano Banana Pro Edit with existing sheets.

### Type B: New Recurring Character
Generate 4-angle ref sheet via Nano Banana Pro. Owner approval required before use.

### Type C: Generic One-Off Person
Nano Banana Pro text-only. Not reusable. Best for wide shots, back-of-head, silhouettes.

## Reference Image Quality Requirements

- **Resolution:** 1024×1024 minimum
- **Background:** Pure flat white or green screen — MANDATORY for Kling Element binding
- **Lighting:** Soft, even, diffused. All 4 angles MUST be from the same lighting setup
- **Expression:** Neutral across ALL reference images
- **Ref count sweet spot:** 3–4 refs optimal; cap at 4 (Kling hard limit). More than 4 increases copy-paste artifact risk ("view-dependent copy-paste," per arXiv 2508.09476 Mixture of Facial Experts research).
- **Angular diversity > expression diversity:** front + 3/4 + profile is the minimal effective multi-view set (confirmed by Mv²ID and MoFE research). Do NOT replace an angle ref with an expression variant — cover angles first.
- **Array order does not matter for Kling elements binding.** No published evidence of order sensitivity. Focus on angle coverage.
- **Do NOT feed generated frames back as references.** Always re-anchor from original approved photos
- **Each clip in a video sequence MUST independently derive character identity** from original approved reference photos

## Multi-Shot Frame-Chaining

```python
# Extract last clean frame — prefer t=4.5s if t=5.0s has motion blur
# -sseof -0.5 = 0.5s before end; use -sseof -0.1 only for well-resolved final frames
os.system(f"ffmpeg -i {prev_clip} -vframes 1 -sseof -0.5 {last_frame_path}")
# If that frame has motion blur, fall back to t=4.5s absolute:
# os.system(f"ffmpeg -i {prev_clip} -ss 4.5 -vframes 1 {last_frame_path}")

resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/kling-video-v3-pro-image-to-video",
    "image_url": last_frame_path_or_url,   # Continuity anchor
    "elements": [{"frontal_image_url": "crew_lead/front.png", "reference_image_urls": ["crew_lead/three_quarter.png"]}],
    "prompt": "...",
    "generate_audio": False,
    "duration": 5,
    "aspect_ratio": "9:16"
}, headers=headers)
```

## InsightFace buffalo_l Benchmarks

| Model | LFW | CFP-FP | AgeDB-30 | IJB-C(E4) | Size |
|-------|-----|--------|----------|-----------|------|
| buffalo_l | 99.83% | 99.33% | 98.23% | 97.25% | 326MB |
| buffalo_s (CPU fallback) | 99.70% | 98.00% | — | — | 159MB |

## Kling Element Library Auto-View Generation

Upload ONE good front-facing reference; enable "AI-generate additional views" in Kling web UI. Saves ~$0.39 vs 4 separate NBP calls. **Caveat:** web UI feature only — not exposed via AIMLAPI as of 2026-04.

## face_consistency Parameter (Kling v3 / O1 — Research 2026-05-04)

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/video-o1-reference-to-video",
    "prompt": "...",
    "elements": [...],
    "face_consistency": True,   # Occlusion recovery — add when face may be partially hidden
    "generate_audio": False,
    "duration": 5,
    "aspect_ratio": "9:16"
}, headers=headers)
```

**When to set `face_consistency: True`:** Face partially covered — hands near face, carrying box, hat brim, strong shadows. **AIMLAPI passthrough unverified as of 2026-05-04.** Test on draft before Pro.

**Do NOT set for full clear face visibility** — adds latency with no benefit.

## Veo 3.1 Reference-to-Video — BLOCKED for Character Shots

- **Cost: ~$0.788/sec → $6.30 per 5s clip** (vs Kling v3 Pro $0.291/sec → $1.46 per 5s clip)
- **4× more expensive** than Kling v3 Pro, no evidence of superior identity lock
- **DO NOT use for character shots.** Kling O1 reference-to-video remains correct model.

## Kling O3 — Future Watch for Character Consistency (NOT on AIMLAPI as of 2026-05-17)

Kling O3 (Omni, released Feb 2026; migrated on AIMLAPI Apr 10, 2026 — **still not confirmed**) introduces major character consistency upgrades. Monitor for AIMLAPI availability.

**O3 advantages for character shots:**
- Multi-shot: up to 6 shots in single API call with consistent character across all shots
- `face_consistency: True` confirmed functional — forces face reconstruction from element even when occluded (hands, hat, shadows). Currently unverified on AIMLAPI but works on fal.ai/Atlas Cloud.
- Stronger element binding (3D Spacetime Joint Attention)

**O3 breaking changes that WILL affect this skill when it lands on AIMLAPI:**
- `start_image_url` → renamed to `image_url` (frame-chaining code in Multi-Shot section must update)
- `negative_prompt` **REMOVED** — O3 handles internally; remove from all API calls
- `cfg_scale` **REMOVED** — O3 handles internally; remove from all API calls
- AIMLAPI endpoint will shift from `/v3/` to `/o3/` pattern
- Text prompts capped at 2,500 characters (was unlimited)

**Action on O3 landing:** Update `generation-video.md` templates first, then this file's frame-chaining snippet.

## Shari'ah-Specific Character Rules
- Male crew: long trousers, covered 'awrah, modest work clothing
- Female family members (if depicted): full hijab, loose-fitting garments
- MUST specify exact clothing in prompts — MUST NOT leave it to the model's default
- MUST include clothing description in EVERY prompt, even if character appeared in a previous shot
- Reference images themselves MUST be Shari'ah compliant — MUST run QA on character sheets before using
