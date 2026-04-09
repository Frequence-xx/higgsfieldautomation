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

## Thresholds

- **Pass:** All dimensions ≥ 7 AND shariah_compliance = 10
- **Marginal (flag for review):** Any dimension 5-6, rest ≥ 7
- **Reject:** Any dimension ≤ 4 OR shariah_compliance < 10

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

## Post-QA Cleanup

After a clip passes final review, **delete the QA frame extractions** from `/opt/pipeline/qa/`. Keep only the scored summary in SQLite `generation_history.qa_scores_json`.
