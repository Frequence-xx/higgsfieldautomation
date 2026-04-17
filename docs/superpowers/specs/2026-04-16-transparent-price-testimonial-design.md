# "Geen Verrassingen" — Transparente Prijs Testimonial Design Spec

**Date:** 2026-04-16
**Brief:** Vertical 9:16 testimonial van een tevreden klantkoppel over duidelijke offerte-prijs zonder achteraf-verrassingen
**Status:** Concept approved by owner (2026-04-16, Telegram msg 1037)
**Prior production:** Builds on Video 2 "Proces" approved patterns (2026-04-12)

## Overview

A ~22 second customer testimonial. The man speaks on camera in his new living room about the relief of getting a transparent moving quote. His wife is voice-only (off-camera) — preserves dialogue dynamic without showing female face/awrah. Tone is calm, trustworthy, professional. Ends on clean orange-branded CTA.

## Specifications

| Property | Value |
|----------|-------|
| Format | 9:16 vertical (1080×1920), native — no crop/pad |
| Duration | ~22 seconds |
| Shots | 7 (4 character animated + 3 text/mockup) |
| Tone | Trustworthy, calm, professional |
| Voiceovers | 2 — Man (on-camera) + Vrouw (VO only, no on-screen) |
| Music | None (Shari'ah) |
| Ambient SFX | Quiet living room: subtle ceramic clink, distant outdoor ambience, soft fabric rustle |
| Captions | Word-by-word animated, orange highlight on active word |
| CTA | "Ontvang Direct Prijsindicatie" + snelverhuizen.nl |
| Platforms | Instagram Reels, TikTok, YouTube Shorts |

## Voiceover Script

| # | Speaker | Line (Dutch) |
|---|---------|--------------|
| 1 | Man | "We waren eerlijk gezegd bang dat de kosten achteraf hoger zouden uitvallen." |
| 2 | Vrouw (VO) | "Ja, dat hadden we eerder meegemaakt bij een ander verhuisbedrijf." |
| 3 | Man | "Maar hier vulden we onze gegevens in en kregen we meteen een offerte met een duidelijke prijs." |
| 4 | Vrouw (VO) | "En die prijs klopte uiteindelijk gewoon." |
| 5 | Man | "Geen verrassingen achteraf." |

## Character Specification — "Customer Man" (NEW character, NOT Karel/Mourad)

```
Tarik — 35-year-old Dutch man, neat short beard (lightly trimmed),
warm brown eyes, friendly approachable face, medium build. Wearing
a soft navy crewneck sweater (NOT Snel Verhuizen branded — he is
a customer not employee), dark jeans, sitting at home casually.
Background: tasteful modern Dutch living room, partially unpacked
moving boxes visible in soft focus.
```

Naming reference internally as **"Tarik"** to distinguish from Karel/Mourad (Snel Verhuizen crew). Generate fresh ref sheet — 4 angles (front, three-quarter L, three-quarter R, profile) on neutral background, no logos on clothing.

## Shot List

### Shot 1 — Hook: Text Reveal (0-3s)

- **Description:** Black frame with orange #FC8434 text fade-in: "Wat als je vooraf de exacte prijs wist?" — clean sans-serif (Montserrat Bold), centered, gentle fade through to next shot
- **Camera:** Static text composition, soft fade-out at 2.7s
- **On-screen text:** "Wat als je vooraf de exacte prijs wist?" — orange #FC8434, Montserrat Bold 80px
- **Voiceover:** None (silent hook — text holds attention)
- **Ambient:** Soft room tone fades in last 0.5s
- **Generation:** **Remotion only** (no AI gen needed)
- **Cost:** $0
- **Difficulty:** Trivial

### Shot 2 — Man speaks line 1 (3-7s)

- **Description:** Tarik on living room sofa, three-quarter angle, calm speaking expression, partial moving boxes visible behind in soft focus
- **Camera:** Medium shot, 50mm look, shallow depth of field, eye-level
- **On-screen text:** Caption (word-by-word, orange highlight)
- **Voiceover:** Man — "We waren eerlijk gezegd bang dat de kosten achteraf hoger zouden uitvallen."
- **Characters:** Tarik (NEW)
- **Image model:** NBP Edit (`google/nano-banana-pro-edit`) using Tarik character sheet + room reference
- **Video model:** Kling v3 Pro I2V (`klingai/video-v3-pro-image-to-video`)
- **Reference assets:** `/opt/pipeline/assets/customer/tarik_character_sheet.png`, `/opt/pipeline/assets/customer/living_room_reference.png` (TBD)
- **Difficulty:** Moderate (face must match ref + natural speaking pose)
- **Motion prompt:** "Locked-off camera, subject's lips and jaw move naturally with speech rhythm, slight head tilt right at end, eyes maintain gaze toward off-camera interviewer position. Preserve face structure, no body sway, no breathing motion, eases to stop. Natural micro-gestures only."
- **Cost:** ~$1.67 (NBP $0.03 + Kling Pro $1.64)

### Shot 3 — Cutaway during vrouw VO (7-10s)

- **Description:** Detail shot — Tarik's hands wrapped around a ceramic coffee mug on the salon table, Snel Verhuizen branded moving box visible blurred in background
- **Camera:** Close-up macro, 85mm look, very shallow DOF on hands+mug
- **On-screen text:** Caption (word-by-word)
- **Voiceover:** Vrouw — "Ja, dat hadden we eerder meegemaakt bij een ander verhuisbedrijf."
- **Characters:** None visible (just hands)
- **Image model:** NBP Edit + box reference asset
- **Video model:** Kling v3 Pro I2V
- **Reference assets:** `/opt/pipeline/assets/brand/snelverhuizen_boxes_reference_sheet.png` (existing)
- **Difficulty:** Easy (hands + object, low identity risk)
- **Motion prompt:** "Locked-off camera. Wisps of steam rise gently from coffee mug. Fingers maintain firm grip on ceramic. Soft warm light shifts subtly across surface. No camera movement, no hand repositioning, eases to stop."
- **Cost:** ~$1.67

### Shot 4 — Man speaks line 3 (10-14s)

- **Description:** Tarik different angle (closer, slightly warmer light), gestures briefly toward smartphone resting on coffee table
- **Camera:** Medium close-up, 85mm, shallow DOF, eye-level
- **On-screen text:** Caption (word-by-word)
- **Voiceover:** Man — "Maar hier vulden we onze gegevens in en kregen we meteen een offerte met een duidelijke prijs."
- **Characters:** Tarik
- **Image model:** NBP Edit (same Tarik ref + smartphone-on-table prop)
- **Video model:** Kling v3 Pro I2V
- **Difficulty:** Moderate (face match + hand gesture)
- **Motion prompt:** "Locked-off camera. Subject speaks with calm warmth, brief open-handed gesture toward off-camera right toward end (palm-up, settles back to lap). Preserve face structure, no body sway, no breathing motion. Single defined gesture, eases to stop."
- **Cost:** ~$1.67

### Shot 5 — Phone screen mockup during vrouw VO (14-17s)

- **Description:** Close-up of smartphone screen showing the Snel Verhuizen offerte page (mocked in Remotion based on real PDF template). Format matches exactly: orange "Offerte" header, ordernummer, addresses, pricing table with bold orange "Totaal" row.
- **Camera:** Static phone screen, slight Ken Burns slow zoom toward "Totaal" cell
- **On-screen text:** Mockup contains the offerte data — fictional Dutch couple, plausible €600-800 amount
- **Voiceover:** Vrouw — "En die prijs klopte uiteindelijk gewoon."
- **Generation:** **Remotion mockup** (no AI gen) — replicates layout from real PDF reference
- **Mockup data (proposed):**
  - Ordernummer: 125698432
  - Naam: T. Bakker
  - Datum: 15 maart 2026
  - STARTLOCATIE: Ambachtsweg 33M, Utrecht
  - ADRES 1: [Dutch suburban address]
  - Volume: 18 m³
  - Subtotaal €656.20 → BTW (21%) €137.80 → **Totaal €794.00**
- **Cost:** $0

### Shot 6 — Man closes (17-20s)

- **Description:** Tarik tighter close-up, peaceful warm smile, looking gently into camera lens
- **Camera:** Close-up, 100mm look, very shallow DOF
- **On-screen text:** Caption (word-by-word)
- **Voiceover:** Man — "Geen verrassingen achteraf."
- **Characters:** Tarik
- **Image model:** NBP Edit (same Tarik ref, closer framing)
- **Video model:** Kling v3 Pro I2V
- **Difficulty:** Moderate (face + warm subtle smile)
- **Motion prompt:** "Locked-off camera. Subject's mouth opens to speak short phrase, slight smile forms in final moment, eyes warm. Preserve face structure, no body sway, no breathing motion, eases to stop."
- **Cost:** ~$1.67

### Shot 7 — CTA End Card (20-23s)

- **Description:** Brand-orange end card — Snel Verhuizen logo top, headline "Ontvang Direct Prijsindicatie", URL "snelverhuizen.nl", phone "085 333 1133"
- **Camera:** Static composition, gentle scale-in animation on logo + text
- **On-screen text:** Logo + CTA copy
- **Voiceover:** None (CTA holds with ambient + maybe subtle whoosh SFX)
- **Generation:** **Remotion only**
- **Cost:** $0

## Audio Design

| Layer | Source | Details |
|-------|--------|---------|
| Voiceover (Man) | ElevenLabs `eleven_multilingual_v2` | Jaimie `hLnc7y4d152WGG2BQlAY` (warm Amsterdam 30, confident yet approachable). Alt: Rick `AyQGttFzg1EY7EIKkpHs` (articulate slow-paced) |
| Voiceover (Vrouw) | ElevenLabs `eleven_multilingual_v2` | Jolanda `DiUBVrSFwkMaPz4XqWvR` (pleasant soothing middle-aged narrative). Alt: Ruth `YUdpWWny7k5yb4QCeweX` (warm dynamic young corporate) |
| Ambient SFX | Freesound (CC) or generated | Quiet living room — distant outdoor ambience, occasional ceramic clink, soft fabric rustle |
| Music | NONE | Shari'ah compliance — no music ever |

VO recorded FIRST. Word-level timestamps via ElevenLabs **Forced Alignment API** (`POST /v1/forced-alignment` — NOT the TTS-with-timestamps endpoint which is char-level only) → drive shot timing in Remotion.

## Caption Design

- **Font:** Montserrat Black, 900 weight
- **Style:** Lowercase first letter only (more conversational than ALL CAPS shouting), word-by-word reveal synced to VO timestamps
- **Color:** White (#FFFFFF) base, **active word highlight in orange #FC8434**
- **Shadow:** -45° angle, 55% opacity, 5px distance, 5px blur
- **Position:** Centered at 70% height (safe zone for 9:16 + leaves face area clear)
- **No name cards** (per V2 lessons — name cards conflicted with VO captions)

## Shari'ah Compliance Checklist

- [x] No music or instruments
- [x] Modest dress on man: navy sweater + dark jeans (covers awrah)
- [x] Vrouw is voice-only — no awrah display, no kledingvereiste needed
- [x] No free-mixing visuals (man alone in shots, vrouw never on-camera)
- [x] No haram background elements
- [x] No deceptive advertising — testimonial scenario plausible
- [x] Professional, dignified tone (amanah)
- [x] Anti-fear-tactics: hook is positive ("wat als je wist") not negative ("verborgen kosten")

## Brand Binary Checklist

- [x] Logo color: orange #FC8434 (in S1 hook, S5 mockup, S7 CTA)
- [x] Box branding: white cardboard with orange #FC8434 SNELVERHUIZEN.NL text (in S3 background)
- [x] No truck in this video (testimonial setting is home, not move day) — N/A
- [x] CTA card uses brand orange #FC8434 prominently
- [x] Offerte mockup matches real PDF template structurally

## Color Grading

Apply standard Snelverhuizen warm cinematic grading to all character shots:
- Warm amber highlights (~4500K pushed warm) — golden hour through windows feel
- Cool blue-tinted shadows (lifted, not crushed)
- Slightly desaturated midtones, natural skin tones preserved
- Subtle fine film grain
- Reference: `/opt/pipeline/assets/color_ref_1.png` etc

S5 phone mockup: cleaner/whiter (matches real phone screen brightness), but slight warm tint to match grading flow.

## Cost Estimate

| Item | Cost |
|------|------|
| 4× Kling v3 Pro I2V (S2, S3, S4, S6) at $1.46/clip | $5.84 |
| 4× NBP Edit hero frames at $0.195/img | $0.78 |
| 1× NBP character ref sheet (Tarik, 4 angles) at $0.195 | $0.20 |
| 2× ElevenLabs VO (man + vrouw, multilingual_v2) | ~$0.50 |
| Remotion S1 + S5 + S7 + assembly | $0 |
| Freesound ambient | Free |
| **Estimated total** | **~$7.32** |

Under $15 ceiling. Above $5 target — explained to owner, accepted because character quality matters for testimonial credibility. Pricing verified 2026-04-16 by 4-agent research sweep.

**Cost optimization (if requested):**
- Drop S3 cutaway to Kling Standard (~$0.55 vs $1.46) — saves $0.91 → total ~$6.41. Recommended only if S3 hand cutaway tests fine in Standard.
- Drop S3 + S5 entirely (cut to ~17s video) — saves $1.46 + $0 = $5.86. NOT recommended — both cutaways crucial for visual rhythm during vrouw VO lines.

## Generation Order

1. **Research updates** — verify model guide currency (4 parallel agents — IN PROGRESS)
2. **Update model-prompting-guide.md** — apply verified findings
3. **Record VO** — ElevenLabs man + vrouw, get word-level timestamps
4. **Generate Tarik character ref sheet** — NBP, 3 variations for owner to choose
5. **Owner approves Tarik look**
6. **Hero frame S2** → owner approval
7. **Animate S2** → owner approval
8. **Hero frame S3** → owner approval
9. **Animate S3** → owner approval
10. **Hero frame S4** → owner approval
11. **Animate S4** → owner approval
12. **Hero frame S6** → owner approval
13. **Animate S6** → owner approval
14. **Build S1 (Remotion text hook)** + **S5 (offerte mockup)** + **S7 (CTA card)**
15. **Assemble in Remotion** — all clips + VO + ambient SFX + captions
16. **Loudnorm** audio pass
17. **Final review** — frame-by-frame, brand binary check
18. **Deliver via Telegram**

## Risk Register

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Kling v3 Pro motion still choppy on character speech | Medium | Use minimal motion prompts. If motion fails, fall back to subtle Ken Burns on hero still. |
| Tarik face drifts across shots 2/4/6 | Medium | Same character sheet ref every NBP call. Subject Binding 80-90 on Kling. Same starting hero frame style across all 3 character shots. |
| Vrouw VO sounds robotic/non-Dutch | Low-Medium | Test 2-3 ElevenLabs Dutch female voices, pick warmest. Adjust stability/style. |
| Offerte mockup looks fake on phone screen | Low | Use real PDF as exact template. Match Inter/system fonts, exact orange shade, realistic Dutch addresses. |
| Cost overrun if S2/S4/S6 need re-generation | Medium | $15 ceiling = ~9 extra Kling Pro retries possible. Stop + escalate at 80%. |

## Approval Trail

- 2026-04-16 16:14: Brief received via Telegram (msg 1027)
- 2026-04-16 16:25: Vrouw treatment confirmed — option A (VO only) (msg 1029)
- 2026-04-16 16:27: Man character — fresh Dutch generation, option A (msg 1031)
- 2026-04-16 16:30: Hook style — option A clean text (msg 1033)
- 2026-04-16 16:31: Audio — option A SFX-only (msg 1035)
- 2026-04-16 16:38: Full concept approved + offerte PDF received (msg 1037)
