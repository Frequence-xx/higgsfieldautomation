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
# Use 1:1 for reference sheets — these are for identity matching, not final output
for angle in ["front view", "3/4 angle from left", "profile from right side", "full body standing"]:
    resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
        "model": "google/nano-banana-pro",
        "prompt": f"A 37-year-old Dutch man with short dark brown hair, medium olive skin, clean shaven, wearing a navy blue polo shirt with company logo on left chest and dark grey cargo trousers with black work boots, {angle}, professional photography, neutral background",
        "aspect_ratio": "1:1",    # 1:1 for ref sheets
        "resolution": "1K",
    }, headers=headers, timeout=60)
```

Save to `/opt/pipeline/assets/characters/{name}/`:
```
/assets/characters/
├── crew_lead/
│   ├── front.png          # Generated via Nano Banana Pro
│   ├── three_quarter.png  # Generated via Nano Banana Pro
│   ├── profile.png        # Generated via Nano Banana Pro
│   ├── full_body.png      # Generated via Nano Banana Pro
│   └── character.json     # Metadata (see below)
```

### Step 2: Lock Character via Flux Kontext Max
Use Kontext Max to place the character into each scene while preserving identity.
**Always use `aspect_ratio: "9:16"` for vertical hero frames.**

```python
# Generate hero frame with character locked into the scene — NATIVE 9:16
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "flux/kontext-max/image-to-image",
    "prompt": "Place this person on a Dutch suburban street next to a white moving truck, golden hour lighting, cinematic vertical composition, 35mm lens",
    "image_url": [
        "https://cdn.example.com/characters/crew_lead/front.png",
        "https://cdn.example.com/characters/crew_lead/three_quarter.png"
    ],
    "aspect_ratio": "9:16",   # VERIFIED: produces native ~752x1392 vertical output
    "num_images": 1,
}, headers=headers, timeout=90)
# Response is SYNCHRONOUS — no polling needed
hero_frame_url = resp.json()["data"][0]["url"]
```

### Step 3: Animate with Character Reference (Kling O1)
For video clips where character must stay consistent:

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
# ASYNC — poll for completion
```

### Step 4: Alternative — Nano Banana Pro Edit for Compositing
For placing a character into a specific background scene (max 14 reference images).
**Always use `aspect_ratio: "9:16"` for vertical hero frames.**

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-pro-edit",
    "image_urls": [
        "https://cdn.example.com/characters/crew_lead/front.png",
        "https://cdn.example.com/characters/crew_lead/full_body.png",
        "https://cdn.example.com/scenes/dutch_street_golden_hour.png"
    ],
    "prompt": "Place the person from the first two images into the street scene from the third image, maintaining their exact appearance and clothing, cinematic vertical composition",
    "aspect_ratio": "9:16",   # Native 9:16 output — no cropping needed
    "resolution": "1K",       # Options: 1K (768x1344), 2K (1536x2688), 4K (3072x5376)
}, headers=headers, timeout=60)
```

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

**Automated (InsightFace — free, runs on CPU):**

```bash
pip install insightface onnxruntime  # CPU; use onnxruntime-gpu for GPU
```

```python
import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=-1, det_size=(640, 640))  # ctx_id=-1 = CPU

def get_embedding(image_path):
    img = cv2.imread(image_path)
    faces = app.get(img)
    return faces[0].embedding if faces else None  # 512-dim vector

def face_similarity(path1, path2):
    e1, e2 = get_embedding(path1), get_embedding(path2)
    if e1 is None or e2 is None:
        return 0.0
    return float(np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2)))

# Usage: compare reference photo to each extracted frame
ref_score = face_similarity("assets/characters/mourad/front.png", "frame_t0.png")
```

**Threshold guide (buffalo_l model, cross-pose video QA):**

| Score | Meaning | Action |
|-------|---------|--------|
| ≥ 0.68 | Strong identity match | PASS |
| 0.60 – 0.67 | Acceptable drift (pose/lighting variation) | PASS with note |
| 0.50 – 0.59 | Marginal — borderline drift | RETRY with more refs or higher face adherence |
| < 0.50 | Identity failure | REJECT, regenerate |

> **Note:** The prior threshold of `<0.80 = drift` in model-prompting-guide.md was too strict for cross-pose/lighting comparison. 0.80+ is correct for strict same-photo identity verification; 0.65 is the practical production threshold for I2V character consistency across different angles.

**Manual QA checklist (visual):**
- Face geometry: same jaw shape, nose, eye spacing
- Skin tone: no shifts between shots
- Clothing: same items, same colors, same fit
- Build/proportions: no height or weight changes

Score character consistency 1-10. Below 7 = reject and regenerate with stronger reference anchoring.

## Model Selection for Character Shots

| Scenario | Character Type | Image Model | Video Model | Cost Est. |
|----------|---------------|-------------|-------------|-----------|
| Karel/Mourad alone | A (existing) | Nano Banana Pro Edit (existing refs) | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |
| Karel/Mourad in scene | A (existing) | Nano Banana Pro Edit (refs + truck + box) | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |
| New recurring character | B (create refs first) | Kontext Max or NBP Edit (new refs) | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |
| Multiple characters | A or B | Nano Banana Pro Edit (14 refs) | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |
| Generic one-off person | C (text-only) | Nano Banana Pro (no refs) | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |
| Ref sheet creation (Type B) | — | Nano Banana Pro × 4 angles | — | ~$0.52 (one-time) |

## Character Types — Decision Tree

Every production starts here. Determine which character type applies:

### Type A: Existing Characters (Karel & Mourad)
- Reference sheets already exist at `/opt/pipeline/assets/crew/`
- Use Nano Banana Pro Edit with existing character sheets + brand assets
- Cheapest option — no new reference generation needed

### Type B: New Recurring Character (invented)
- Owner provides a description (age, build, skin tone, hair, clothing)
- Generate a 4-angle reference sheet (front, 3/4, profile, full body) via Nano Banana Pro
- Cost: ~$0.50 (4 × $0.13)
- Send to owner for approval BEFORE using in production
- After approval: save to `/opt/pipeline/assets/characters/{name}/` with character.json
- Character is now "locked" and reusable across all future videos
- Workflow: same as Karel/Mourad from this point on

### Type C: Generic One-Off Person (no consistency needed)
- For concepts where the specific person doesn't matter
- Use Nano Banana Pro text-only with detailed appearance + Shari'ah dress description
- Cheapest option — no reference generation needed
- NOT reusable — each generation may look different
- Best for: wide shots, back-of-head, silhouettes, crowd scenes

### Decision Flow
```
Is this Karel or Mourad? → Type A (use existing refs)
Is this a new character that appears in multiple shots? → Type B (create ref sheet first)
Is this a person who only appears once or in a wide shot? → Type C (text-only, no ref needed)
```

### Creating a New Character (Type B — Full Workflow)

1. **Owner provides brief:** "Man, 45 jaar, baard, stevig, vriendelijk, traditionele kleding"
2. **Generate 4 reference images:**
   ```python
   angles = ["front view facing camera", "3/4 angle from left", "profile from right side", "full body standing"]
   for angle in angles:
       resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
           "model": "google/nano-banana-pro",
           "prompt": f"<owner description with full Shari'ah compliant clothing details>, {angle}, professional photography, neutral white background, studio lighting",
           "aspect_ratio": "1:1",
           "resolution": "1K",
       }, headers=headers, timeout=60)
   ```
3. **Send all 4 to owner via Telegram for approval**
4. **If approved:** Save to `/opt/pipeline/assets/characters/{name}/` + create character.json
5. **If rejected:** Adjust description and regenerate (max 2 retries)
6. **Character is now locked** — use in all shots with Nano Banana Pro Edit or Kontext Max

## Reference Image Quality Requirements (Research 2026-04-20)

These requirements apply to ALL reference images — both existing Karel/Mourad sheets and new Type B character sheets.

**Resolution:** 1024×1024 minimum. Clarity matters more than megapixels — a sharp 1024px image outperforms a blurry 4K photo for the 3D face mapping algorithm.

**Background:** Completely solid (flat color, not gradient) — makes character/background separation much easier for the model. White or light grey preferred.

**Lighting:** Soft, even, diffused from a single clear direction. AVOID:
- Strong directional shadows (model may read them as permanent facial features)
- Color casts (warm/cool casts alter skin tone across shots)
- Dramatic high-contrast lighting

**Lighting consistency across all 4 refs:** All 4 angles MUST be from the same lighting setup. Refs with different lighting conditions produce conflicting 3D face reconstruction signals, which reduces consistency.

**Expression:** Neutral across ALL reference images. Slight smile is acceptable but must be identical in all 4 shots. Do NOT mix expressions (one smiling, one neutral, one surprised) — locks in expression conflicts.

**Ref count — sweet spot:**
- 2-4 refs: optimal for identity lock
- 6-8 refs: diminishing returns, slightly worse than 4
- 12-15+ refs: conflicting signals can actively reduce consistency
- For NBP Edit: use 4 high-quality refs even though 14 are supported — quality > quantity

**Do NOT feed generated frames back as references.** Re-anchor ALWAYS from original approved reference photos. Generated frames accumulate drift.

**10% expected failure zone:** Kling v3 achieves ~90% identity consistency with good refs. The remaining 10% fail predictably at: extreme angles (profile beyond 90°), very dark or heavily shadowed lighting in the scene, and when the character is small in frame (<15% frame height).

## Shari'ah-Specific Character Rules
- Male crew: long trousers, covered 'awrah, modest work clothing
- Female family members (if depicted): full hijab, loose-fitting garments
- MUST specify exact clothing in prompts — MUST NOT leave it to the model's default
- MUST include clothing description in EVERY prompt, even if the character appeared in a previous shot
- Reference images themselves MUST be Shari'ah compliant — MUST run QA on character sheets before using
