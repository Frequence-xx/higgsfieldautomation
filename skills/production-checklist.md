---
name: Production Checklist
description: MANDATORY pre-flight and QA checklists that MUST be completed at every step of production. Never skip. Never shortcut. Read EVERY memory entry before starting.
autoInvoke: true
triggers:
  - generate
  - animate
  - production
  - video
  - hero frame
  - assembly
negatives:
  - Do NOT invoke when doing research, study, or documentation tasks
  - Do NOT invoke when parsing briefs or planning shot lists (use brief-intake.md)
  - Do NOT invoke when the task is purely administrative (git, file cleanup, database maintenance)
---

# Production Checklist — MANDATORY

**This checklist is NON-NEGOTIABLE. Every item must be verified. Skipping any step is a pipeline failure.**

## Character Type Classification — MANDATORY Pre-Generation Step

Before generating ANY shot containing people, determine the character type. This step is NON-NEGOTIABLE. See `character-consistency.md` for full details on each type.

### Decision Tree

```
Does this shot contain people? → NO → Skip to Pre-Production Gate
                                → YES ↓

Is this Karel or Mourad? → YES → Type A: Use existing reference sheets
                          → NO ↓

Does this person appear in multiple shots? → YES → Type B: Create reference sheet FIRST
                                             → NO ↓

Is this a wide shot, silhouette, or back-of-head? → YES → Type C: Text-only prompt, no refs needed
                                                     → NO → Type B (create refs for consistency)
```

### Type A: Existing Characters (Karel & Mourad)

- [ ] Reference sheets located at `/opt/pipeline/assets/crew/`
- [ ] Use Nano Banana Pro Edit with character sheet as Image 1 in EVERY call
- [ ] Include identity-locking phrase: "Keep facial features exactly the same as Image 1"
- [ ] Include full clothing description in prompt (black crewneck, orange logo, blue jeans, white sneakers)
- [ ] For video: Kling v3 Pro with Subject Binding 80-90, Element Library with 3-4 reference photos

### Type B: New Recurring Character

- [ ] Owner has provided character description
- [ ] Generate 4-angle reference sheet (front, 3/4, profile, full body) via Nano Banana Pro at 1:1
- [ ] Send reference sheet to owner for approval via Telegram
- [ ] Owner approved? → Save to `/opt/pipeline/assets/characters/{name}/` with character.json
- [ ] Owner rejected? → Adjust and regenerate (max 2 retries on ref sheet)
- [ ] Character locked — proceed as Type A from this point

### Type C: Generic One-Off Person

- [ ] Confirm person appears only once OR in wide/silhouette/back framing
- [ ] Use Nano Banana Pro text-only with detailed appearance + Shari'ah dress description
- [ ] Do NOT reuse across shots — each generation may look different
- [ ] Best for: wide shots, back-of-head, silhouettes, crowd scenes

**MUST complete character classification before proceeding to the Pre-Production Gate below.**

---

## Pre-Production Gate

Before generating ANY image or video:

- [ ] Read ALL memory entries in MEMORY.md — every single one
- [ ] Read feedback entries for known issues (truck side door, logo color, breathing, ghost truck, etc.)
- [ ] Confirm target aspect ratio and resolution
- [ ] Confirm budget remaining and cost of this generation
- [ ] Review reference images that will be used
- [ ] Check prompt against known failure patterns:
  - [ ] No "breathing movement" or "weight shift" in motion prompts
  - [ ] "stationary truck, no vehicle movement" included if truck is in frame
  - [ ] "maintains exact expression, no expression changes" for character shots
  - [ ] "no side door on cargo box" if truck side is visible
  - [ ] Negative prompt includes all 16 baseline terms
  - [ ] Motion prompt is ONLY about motion, does NOT redescribe the image
  - [ ] Motion prompt is 15-40 words, ends with "eases to stop"

## Hero Frame QA Gate

After generating EACH hero frame, before animating:

- [ ] READ the generated image (not just check the URL worked)
- [ ] Check: Does the face match the reference? (if character shot)
- [ ] Check: Is the truck branding correct? (SNELVERHUIZEN, orange)
- [ ] Check: No side door on cargo box?
- [ ] Check: Logo color correct? (orange on front panel)
- [ ] Check: Clothing correct? (black crewneck, orange logo, blue jeans, white sneakers)
- [ ] Check: No haram elements? (shariah_compliance = 10)
- [ ] Check: Native 9:16 composition? (no black bars, no cropping needed)
- [ ] Check: Would I accept this if I were the client?
- [ ] Send to owner for approval — DO NOT animate until approved

## Video Animation QA Gate

After animating EACH clip, before proceeding to next:

- [ ] Extract 5 frames spread across the clip (every 30th frame)
- [ ] READ each extracted frame
- [ ] Check: Is the truck stationary? (no ghost driving)
- [ ] Check: Does the character maintain their expression? (no breathing artifacts, no mood changes)
- [ ] Check: Are faces consistent across all frames? (no morphing/drift)
- [ ] Check: Do objects stay in place? (no sliding, no disappearing)
- [ ] Check: Are colors consistent? (no sudden color shifts)
- [ ] Check: Is motion smooth? (no jitter, no choppy slowmo)
- [ ] Check: Is text/branding still legible? (no garbling)
- [ ] Delete extracted QA frames after review
- [ ] Send clip to owner for approval — DO NOT proceed until approved
- [ ] If ANY issue found: flag to owner, DO NOT auto-proceed

## Assembly QA Gate

Before sending final assembled video:

- [ ] Watch the entire assembled video by extracting frames every 15 frames
- [ ] Check: Are transitions between shots clean?
- [ ] Check: Is voiceover in sync with visuals?
- [ ] Check: Are captions synced to voiceover? (real timestamps, not estimated)
- [ ] Check: Are captions readable on every shot? (not overlapping subjects)
- [ ] Check: Is audio mix balanced? (VO clear, SFX subtle, no music)
- [ ] Check: No black bars anywhere?
- [ ] Check: Final duration matches spec?
- [ ] Check: Resolution is 1080x1920?

## Caption Sync Gate

- [ ] Word-level timestamps obtained from ACTUAL transcription (not estimated)
- [ ] Timestamps verified against audio playback
- [ ] Each word appears when narrator speaks it (±100ms tolerance)
- [ ] Active word highlighted in orange
- [ ] Max 2 rows visible at any time
- [ ] Text fully within frame (no cutoff)
- [ ] No overlap with subject's face

## FAILURE MODES TO PREVENT

These are mistakes that have been made before. NEVER repeat them:

1. **Estimating timestamps** instead of getting real word-level data
2. **Not watching animated clips** before assembly
3. **Sending marginal quality** to owner instead of fixing first
4. **Using "breathing" in motion prompts** — causes unnatural movement
5. **Not specifying "stationary truck"** — causes ghost driving
6. **Assembling from clips not individually approved** by owner
7. **Skipping reference images** for brand consistency
8. **Using FFmpeg drawtext** instead of Remotion for captions
9. **Cropping/zooming/padding** instead of native 9:16 generation
10. **Rushing to deliver** instead of checking every detail
