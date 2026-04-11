---
name: Video QA Rubric
description: Frame-by-frame visual QA scoring system with 8 dimensions, failure codes, threshold scores, regeneration limits, and Telegram escalation protocol.
autoInvoke: true
triggers:
  - QA
  - quality assurance
  - frame analysis
  - score clip
  - review frames
negatives:
  - Do NOT invoke when generating images or video (use generation-image.md or generation-video.md)
  - Do NOT invoke when assembling final video in post-production (use production-checklist.md)
  - Do NOT invoke when writing prompts (use model-prompting-guide.md)
---

# Video QA Rubric

## Frame Extraction

Extract every 4th frame from each clip:
```bash
ffmpeg -i clip.mp4 -vf "select=not(mod(n\,4))" -vsync vfn /opt/pipeline/qa/<brief_id>/<shot_number>/frame_%03d.jpg
```

Send frames in batches to Claude vision API with the scoring rubric below.

## Scoring Schema

Return JSON for each frame batch:
```json
{
  "hand_anatomy": <1-10>,
  "face_consistency_vs_reference": <1-10>,
  "physics_plausibility": <1-10>,
  "brand_accuracy": <1-10>,
  "lighting_coherence": <1-10>,
  "ai_artifact_severity": <1-10>,
  "shariah_compliance": <1-10>,
  "overall_realism": <1-10>,
  "failure_codes": [],
  "improvement_suggestions": ""
}
```

## Dimension Definitions

| Dimension | 10 (perfect) | 7 (acceptable) | 4 (poor) | 1 (reject) |
|-----------|-------------|-----------------|----------|------------|
| hand_anatomy | Correct finger count, natural grip, realistic interaction | Minor imperfection, not distracting | Wrong finger count or impossible grip | Melted/fused/extra hands |
| face_consistency | Matches reference photo exactly | Recognizable but minor drift | Noticeably different from reference | Wrong person entirely |
| physics_plausibility | Objects behave realistically, weight feels correct | Minor physics oddity | Floating objects, wrong gravity | Impossible physics |
| brand_accuracy | Truck/uniform/logo match reference perfectly | Close match, minor differences | Noticeable differences | Wrong brand elements |
| lighting_coherence | Consistent shadows, correct color temperature | Minor shadow inconsistency | Multiple light sources conflict | Shadows in wrong direction |
| ai_artifact_severity | Indistinguishable from real footage | Slight AI smoothness on close inspection | Visible AI texture, plastic-looking | Obviously AI-generated |
| shariah_compliance | Fully compliant — no violations | N/A — this is a hard gate | N/A | Any violation = reject |
| overall_realism | Would pass as real footage | Good enough for social media | Looks like a tech demo | Uncanny valley |

## Cinematic Quality Scoring (Added to Video QA)

Score each video clip on these cinematic dimensions (1-10):

```json
{
  "composition": <1-10>,       // Rule of thirds, leading lines, framing
  "camera_movement": <1-10>,   // Smooth, deliberate, cinematic motion
  "lighting_mood": <1-10>,     // Does lighting match the brief's emotional intent?
  "color_palette": <1-10>,     // Consistent, graded, not flat or oversaturated
  "production_value": <1-10>,  // Would this pass as professional footage?
  "temporal_coherence": <1-10> // Frame-to-frame stability, no morphing/jitter
}
```

| Score | Meaning |
|-------|---------|
| 9-10 | Theatrical / broadcast quality |
| 7-8 | Premium social media ad — publishable |
| 5-6 | Acceptable draft, needs post-production lift |
| 3-4 | Obvious AI, unprofessional |
| 1-2 | Unwatchable, immediate reject |

**Cinematic pass threshold: ALL dimensions ≥ 7.** Any dimension below 7 triggers prompt refinement and regeneration. Refer to `cinematic-standards.md` shot type quality map for per-shot-type expectations.

## Thresholds

- **Pass:** All QA dimensions ≥ 7 AND all cinematic dimensions ≥ 7 AND shariah_compliance = 10
- **Marginal (flag for review):** Any dimension 5-6, rest ≥ 7
- **Reject:** Any dimension ≤ 4 OR shariah_compliance < 10 OR any cinematic dimension < 5

## Hard Gate

**shariah_compliance must score 10/10.** Any score below 10 triggers immediate rejection. No averaging, no compensation from other dimensions. See `shariah-compliance.md` for failure codes.

## Failure Codes

- `HAND_ERROR` — anatomical hand failure
- `FACE_DRIFT` — character consistency loss
- `PHYSICS_VIOLATION` — unrealistic object behavior
- `BRAND_MISMATCH` — wrong truck/uniform/logo
- `LIGHTING_INCONSISTENCY` — shadow/color temperature errors
- `AI_SLOP` — obvious AI texture/artifacts
- `DRESS_CODE_VIOLATION` — clothing doesn't meet Shari'ah standards
- `HARAM_BACKGROUND_ELEMENT` — impermissible object in scene
- `FREE_MIXING_VIOLATION` — inappropriate gender interaction
- `TEMPORAL_JITTER` — frame-to-frame inconsistency in video
- `TEXT_GARBLE` — AI-generated text in scene (should be composited, not generated)
- `FLAT_COMPOSITION` — boring framing, no depth, no leading lines
- `WEAK_CAMERA_MOTION` — jerky, unmotivated, or static when motion was requested
- `BAD_COLOR_GRADE` — oversaturated, flat, or inconsistent color palette
- `LOW_PRODUCTION_VALUE` — looks like a tech demo, not a professional ad

## Regeneration Limits

**Maximum 3 retry attempts per clip per failure category.**

Each retry MUST add progressively stronger corrective language:

| Retry | Action |
|-------|--------|
| 1 | Add specific corrective prompt targeting the failure code |
| 2 | Add corrective prompt AND negative prompts AND reference-anchor to known-compliant frame |
| 3 | Simplify composition (wider shot, fewer people, less detail) AND all above |

After 3 failures on the same failure category:
1. **STOP** regeneration for this clip
2. **Send to owner via Telegram:**
   - The specific frames that failed (as images)
   - The failure codes
   - The 3 corrective prompts that were tried
   - A recommendation: different shot concept, different model, or manual override request
3. **Wait for owner response** before proceeding
4. **Log the escalation** in `generation_history` with retry_count = 3

## Brand Binary Checklist (Pass/Fail)

In addition to the 1-10 scoring dimensions above, every frame containing brand elements MUST pass ALL of these binary checks. A single FAIL on any item rejects the clip.

| Check | Criteria | Pass | Fail |
|-------|----------|------|------|
| Logo color | Orange matches #FC8434 (not red, not yellow, not brown) | Correct orange | Wrong hue |
| No side door | Cargo box has NO door on its side panel (Mercedes Sprinter box truck has rear doors only) | No side door visible | Side door present |
| Correct uniform | Black crewneck sweatshirt with orange SNELVERHUIZEN logo on left chest, blue jeans, white sneakers | All items match | Any item wrong |
| Correct box | Branded cardboard box with SNELVERHUIZEN.NL text, orange and white, handle cutouts | Matches reference | Wrong box design |
| Truck livery | White cab + white cargo box + orange #FC8434 band across lower half with "SNELVERHUIZEN" in white | Matches reference | Wrong livery |
| Text accuracy | Any visible text reads correctly (no garbled/morphed text like "SEDEERHUIREN") | Text legible and correct | Any text corruption |

**Scoring:** Brand binary checks are separate from the 1-10 dimensions. A clip can score 10/10 on brand_accuracy but still FAIL if the binary checklist catches a specific defect (e.g., side door present).

**Action on FAIL:** Identify which binary check failed, apply corrective prompt targeting that specific defect, regenerate. If the defect is text corruption, remove text from generation and composite in post (see `text-overlay-compositing.md`).

## InsightFace Character Consistency Check (Evaluator MUST run for character shots)

For EVERY animated clip containing Mourad or Karel (or any recurring character):

```python
import insightface
import numpy as np
from insightface.app import FaceAnalysis

# Initialize once per session
app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

# Extract face embedding from a frame
def get_face_embedding(image_path):
    import cv2
    img = cv2.imread(image_path)
    faces = app.get(img)
    if not faces:
        return None
    return faces[0].embedding

# Compare frames: extract at t=0, t=2.5, t=5
emb_0 = get_face_embedding("frame_t0.png")
emb_25 = get_face_embedding("frame_t2.5.png")
emb_50 = get_face_embedding("frame_t5.png")

# Cosine similarity
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

sim_0_25 = cosine_sim(emb_0, emb_25)
sim_0_50 = cosine_sim(emb_0, emb_50)

# Threshold: <0.80 = expression drift = REJECT
if sim_0_25 < 0.80 or sim_0_50 < 0.80:
    print(f"REJECT: Face drift detected. Similarity: {sim_0_25:.3f} / {sim_0_50:.3f}")
else:
    print(f"PASS: Face consistent. Similarity: {sim_0_25:.3f} / {sim_0_50:.3f}")
```

**Thresholds:**
- ≥0.90: Excellent consistency
- 0.80-0.89: Acceptable
- <0.80: REJECT — expression drift detected

**Also compare against reference sheet:** Extract embedding from the character reference sheet and compare against frame 0 of the generated clip. Similarity <0.75 = character mismatch = REJECT.

---

## Failure Category Classification

Every QA failure MUST be classified into one of four categories. The category determines the corrective action.

### Cat A — Prompt-Fixable

The model CAN produce correct output. The failure was caused by an insufficient, incorrect, or missing prompt instruction.

**Examples:**
- Missing "stationary truck" caused ghost driving
- Missing clothing description caused wrong uniform
- Missing negative prompt term allowed an artifact
- Incorrect aspect ratio parameter

**Action:** Fix the prompt/parameters. Retry with the same model. Log the corrective prompt for future reuse.

### Cat B — Model Limit (Ceiling)

The model CANNOT produce correct output for this shot type regardless of prompt quality. This is a fundamental capability gap.

**Examples:**
- Kling v3 cannot render "SNELVERHUIZEN.NL" text without morphing
- Close-up hand interactions produce melted fingers despite all mitigations
- Multi-person scenes with complex interactions degrade despite reference anchoring
- Character face identity drifts beyond acceptable threshold despite Subject Binding at 90

**Action:** Mark as ceiling in `learned_preferences` (see `model-ceiling-detection.md`). Route to next-tier model or simplify composition. Do NOT retry same model — it wastes credits.

### Cat C — Reference Quality

The failure traces back to the quality of the input — the hero frame, reference images, or character sheet.

**Examples:**
- Hero frame had harsh shadows that confused the I2V motion model
- Character reference sheet had inconsistent lighting across angles
- Truck reference photo was low resolution or wrong angle
- Hero frame had busy background that morphed during animation

**Action:** Fix the source material. Regenerate the hero frame or reference images with corrective instructions, then re-attempt I2V. Do NOT blame the video model for source quality issues.

### Cat D — Concept Issue

The shot concept itself is fundamentally problematic — it requires capabilities that no available model can deliver at production quality.

**Examples:**
- Two people carrying a couch simultaneously (multi-person + complex physics)
- Close-up dialogue with facial expressions (character consistency + expression control)
- Truck driving through a busy intersection with text visible (motion + text + complex scene)
- Interior staircase scene with narrow angles and multiple subjects

**Action:** Redesign the shot. Simplify to a composition pattern known to succeed (A3-S4 pattern: close-ups, simple compositions, one subject per shot). Notify owner via Telegram with the concept limitation and proposed alternative.

### Classification Decision Tree

```
Did a prompt change fix it on retry? → Cat A (prompt-fixable)
Did 2 retries with progressively stronger prompts both fail at same dimension? → Cat B (model limit)
Was the hero frame / reference image itself flawed? → Cat C (reference quality)
Is this shot type fundamentally beyond current model capabilities? → Cat D (concept issue)
```

### Logging

Log every failure with its category in `generation_history`:

```sql
UPDATE generation_history SET
    failure_category = '<A|B|C|D>',
    failure_dimension = '<dimension_name>',
    failure_code = '<failure_code>',
    corrective_action = '<what was done>'
WHERE id = <generation_id>;
```

## Post-QA Cleanup

After a clip passes final review, **delete the QA frame extractions** from `/opt/pipeline/qa/`. Keep only the scored summary in SQLite `generation_history.qa_scores_json`.
