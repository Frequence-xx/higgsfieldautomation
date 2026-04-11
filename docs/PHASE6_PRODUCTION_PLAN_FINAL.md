# Production Plan — Video 2 "Proces" (FINAL)

## PLANNER Output

### Brief
Concept: Professional moving process — trust + authority
VO: "Een goede verhuizing begint met duidelijkheid. Binnen enkele minuten weten wij precies wat er nodig is. Daarna regelen we alles van planning tot uitvoering. Zonder verrassingen."
Duration: ~18 seconds, 5 shots
Format: 9:16, 1080p

### Memory/Hindsight Queried
- Ghost driving: Five-Layer Freeze Protocol required for truck shot
- Text ceiling: ALL text as post-overlay, never in AI generation
- A3-S4 success pattern: close-up, static, minimal motion = highest quality
- Character refs: NBP Edit + character sheet mandatory for Mourad
- Banned words: no breathing, subtle motion, emotional in prompts

---

## DEFINITIVE SHOTLIST

### SHOT 1 (0-3s) — HOOK: "De Zorgvuldige Handen" (Optie C)
**Visual:** Extreme close-up of gloved hands carefully wrapping a delicate ceramic vase in bubble wrap. Shallow depth of field, warm golden light from side.
**On-screen text (post-overlay):** "ELKE VERHUIZING BEGINT HIER"
**VO:** (none — silent hook, VO starts shot 2)
**Character type:** Type C — generic hands, no face, no refs needed
**Hero frame model:** google/nano-banana-pro (text-only, no character refs)
**Video model:** klingai/video-v3-pro-image-to-video
**Motion prompt:** "Hands gently fold bubble wrap around the vase, fingers press firmly on tape, warm light shifts across surface, eases to stop"
**cfg_scale:** 0.5
**Ceiling risks:** Hand anatomy — close-up gloved hands reduce risk vs bare hands. Bubble wrap texture may shimmer. Keep motion minimal.
**Acceptance criteria:** Hands look natural (5 fingers per hand), wrap motion smooth, no artifacts on bubble wrap, warm cinematic light.
**Cost:** ~$0.13 (hero) + ~$1.46 (video) = $1.59

### SHOT 1B (backup) — HOOK: "De Verdwijnende Kamer" (Optie B)
**Visual:** Furnished living room → rapid cut → same room empty.
**Implementation:** Two separate hero frames (furnished + empty), rapid cross-dissolve via FFmpeg. Not a single AI animation — two stills with a cut.
**Cost:** ~$0.26 (2 hero frames) + $0 (FFmpeg cut)

### SHOT 2 (3-7s) — Mourad close-up portrait
**Visual:** Mourad in SNELVERHUIZEN uniform, calm confident expression, golden hour.
**On-screen text (post-overlay):** word-by-word VO captions with orange highlight
**VO:** "Een goede verhuizing begint met duidelijkheid."
**Character type:** Type A — existing reference sheets
**Hero frame model:** google/nano-banana-pro-edit (character sheet + truck ref)
**Video model:** klingai/video-v3-pro-image-to-video
**Identity header:** "Mourad — 32yo Dutch-Moroccan man, short black beard, warm brown eyes, broad shoulders, oval face. Black crewneck with small orange Snelverhuizen logo left chest, blue jeans, white AF1-style sneakers."
**Prompt additions:** "Keep facial features exactly the same as Image 1. Plain uniform with no visible text except small orange chest logo."
**Motion prompt:** "Locked-off camera, subject maintains calm confident expression, gentle golden hour light plays across face, eases to stop"
**cfg_scale:** 0.5, face adherence: 80-90
**Negative prompt:** full template (morphing, shifting jawline, breathing motion, expression change, etc.)
**Ceiling risks:** Expression drift — InsightFace check mandatory. Face adherence 80-90.
**Acceptance criteria:** Face matches reference (InsightFace cosine sim ≥0.80 across frames), brand binary pass, no expression changes, no breathing artifacts.
**Cost:** ~$0.20 (hero) + ~$1.46 (video) = $1.66

### SHOT 3 (7-11s) — Branded box close-up (A3-S4 pattern)
**Visual:** Close-up SNELVERHUIZEN.NL branded box, text facing camera, warm light on cardboard.
**On-screen text (post-overlay):** word-by-word VO captions
**VO:** "Binnen enkele minuten weten wij precies wat er nodig is."
**Character type:** N/A — no people
**Hero frame model:** google/nano-banana-pro-edit (box reference sheet as input)
**Video model:** klingai/video-v3-pro-image-to-video
**Motion prompt:** "Gentle camera push-in, warm light shifts across cardboard surface, dust particles in light beam, eases to stop"
**cfg_scale:** 0.7 (branded shot)
**Ceiling risks:** LOW — A3-S4 proved this exact pattern works. Text at large scale in close-up survives Kling animation.
**Acceptance criteria:** SNELVERHUIZEN.NL legible throughout animation, box color white/orange (not brown/kraft), brand binary pass.
**Cost:** ~$0.20 (hero) + ~$1.46 (video) = $1.66

### SHOT 4 (11-15s) — Truck on street, golden hour
**Visual:** SNELVERHUIZEN truck parked on quiet Dutch residential street, golden hour.
**On-screen text (post-overlay):** word-by-word VO captions
**VO:** "Daarna regelen we alles van planning tot uitvoering."
**Character type:** N/A — no people
**Hero frame model:** flux/kontext-max/image-to-image (truck reference)
**Video model:** klingai/video-v3-pro-image-to-video
**Five-Layer Freeze Protocol:**
1. Prompt: "stationary truck, parked, engine off, no vehicle movement, no forward creep"
2. Negative: "vehicle movement, driving, rolling, ghost driving, truck rocking"
3. Motion Brush: vehicle body UNPAINTED (if supported)
4. Endpoint: identical to start frame
5. cfg_scale: 0.7
**Motion prompt:** "Locked-off camera, gentle golden hour light plays across truck surface, leaves rustle softly in breeze, truck remains completely stationary and rigid, eases to stop"
**Ceiling risks:** Ghost driving — Five-Layer Protocol applied. Text degradation — text is post-overlay, not in frame.
**Acceptance criteria:** Truck does NOT move between t=0, t=2.5, t=5 (bounding box check). Brand binary pass. No text garbling (text is overlay).
**Cost:** ~$0.10 (hero) + ~$1.46 (video) = $1.56

### SHOT 5 (15-18s) — CTA Remotion end card
**Visual:** Phone UI mockup with SNELVERHUIZEN.NL + logo + form + CTA button
**On-screen text:** "Start je aanvraag" + "SNELVERHUIZEN.NL" + "085 3331133"
**VO:** "Zonder verrassingen."
**Implementation:** Remotion PhoneUI.tsx (existing, needs logo + margin fix)
**Cost:** $0

---

## BUDGET SUMMARY

| Shot | Hero Frame | Video Animation | Total |
|------|-----------|-----------------|-------|
| 1 (Hook hands) | $0.13 | $1.46 | $1.59 |
| 1B (Backup) | $0.26 | $0 | $0.26 |
| 2 (Mourad) | $0.20 | $1.46 | $1.66 |
| 3 (Box) | $0.20 | $1.46 | $1.66 |
| 4 (Truck) | $0.10 | $1.46 | $1.56 |
| 5 (CTA) | $0 | $0 | $0 |
| Voiceover | — | — | $0.10 |
| **Total** | | | **$6.83** |

Within $15 ceiling. Room for 1-2 retries.

---

## EXECUTION ORDER

1. Generate voiceover FIRST (need duration for timing)
2. Get word-level timestamps via ElevenLabs SDK
3. Hero frames: Shot 3 (box, lowest risk) → Shot 4 (truck) → Shot 1 (hands) → Shot 2 (Mourad, highest risk)
4. Owner approval on ALL hero frames before any animation
5. Animate: one at a time, Evaluator reviews each
6. Fix Remotion PhoneUI (logo + margins) for Shot 5
7. Assembly: FFmpeg concat + voiceover + SFX + Remotion caption overlay
8. Final Evaluator review
9. Deliver to owner with scores
