# Meet the Team — Video Ad Design Spec

**Date:** 2026-04-10
**Brief:** "Maak kennis met het team achter Snelverhuizen" — korte, warme kennismaking met Mourad en Karel bij de bus
**Status:** Approved by owner

## Overview

A 15-second warm, professional team introduction video for Instagram Reels, TikTok, and YouTube Shorts. Willem (ElevenLabs Dutch voice) narrates while we see the Snelverhuizen truck and meet Mourad and Karel.

## Specifications

| Property | Value |
|----------|-------|
| Format | 9:16 vertical (1080x1920) |
| Duration | 15 seconds |
| Shots | 5 |
| Tone | Warm & professional |
| Voiceover | Willem (yBtEjlHaWNu9xrYohjbA), eleven_multilingual_v2, Dutch |
| Music | None (Shari'ah) |
| Ambient SFX | Soft street ambiance, birds, light wind |
| CTA | None — logo closing only |
| Platforms | Instagram Reels, TikTok, YouTube Shorts |

## Voiceover Script

> "Dit is het team achter Snelverhuizen. Mourad en Karel. Uw verhuizing is bij ons in goede handen."

## Shot List

### Shot 1 — Hook: Truck Establishing (0-3s)

- **Description:** Snelverhuizen truck parked on a quiet Dutch suburban street, golden hour light, warm cinematic color grading
- **Camera:** Wide shot, slight dolly push-in, 24mm anamorphic
- **On-screen text:** None (voiceover carries)
- **Voiceover:** "Dit is het team..."
- **Characters:** None
- **Image model:** Nano Banana Pro (`google/nano-banana-pro`)
- **Video model:** Kling v3 Standard I2V (`kling-video/v3/standard/image-to-video`)
- **Reference assets:** `/opt/pipeline/assets/truck/truck_rightdiagnol_side_view.png`
- **Difficulty:** Easy
- **Prompt keywords:** warm golden hour lighting, cinematic color grading, slightly desaturated, lifted blacks, amber highlights, cool blue shadows, film grain, professional commercial look, shot on RED camera, quiet Dutch residential street, brick houses, trees

### Shot 2 — Mourad Introduction (3-6s)

- **Description:** Mourad standing next to the truck, half-body shot, looking at camera with a slight warm smile, black crewneck with orange SNELVERHUIZEN logo
- **Camera:** 85mm portrait, shallow depth of field, golden hour backlight
- **On-screen text:** "MOURAD" (Montserrat Black, white, ALL CAPS, centered)
- **Voiceover:** "...achter Snelverhuizen."
- **Characters:** Mourad (medium build, bald, clean shaven, medium olive skin)
- **Image model:** Flux Kontext Max (character reference anchoring)
- **Video model:** Kling v3 Standard I2V
- **Reference assets:** `/opt/pipeline/assets/crew/mourad_reference_sheet.png`, `/opt/pipeline/assets/crew/mourad_full_body.png`
- **Difficulty:** Moderate (face must match reference)
- **Prompt keywords:** professional portrait, warm smile, confident, trustworthy, black crewneck sweatshirt with small orange logo on left chest, blue jeans, golden hour lighting, cinematic bokeh, film grain

### Shot 3 — Karel Introduction (6-9s)

- **Description:** Karel standing at the truck liftgate, half-body shot, holding a moving box, warm smile, black crewneck with orange SNELVERHUIZEN logo
- **Camera:** 85mm portrait, shallow depth of field, golden hour light
- **On-screen text:** "KAREL" (Montserrat Black, white, ALL CAPS, centered)
- **Voiceover:** "Mourad en Karel."
- **Characters:** Karel (large/stocky build, bald, light beard, fair skin)
- **Image model:** Flux Kontext Max (character reference anchoring)
- **Video model:** Kling v3 Standard I2V
- **Reference assets:** `/opt/pipeline/assets/crew/karel_character_sheet.png`, `/opt/pipeline/assets/crew/karel_full_body_outside_with_box.png`
- **Difficulty:** Moderate (face + box interaction)
- **Prompt keywords:** professional portrait, warm smile, strong, reliable, holding cardboard moving box, black crewneck sweatshirt with small orange logo on left chest, blue jeans, white sneakers, golden hour lighting, cinematic bokeh, film grain

### Shot 4 — Team Together (9-12s)

- **Description:** Mourad and Karel standing side by side next to the truck, confident posture, arms at their sides, warm professional look
- **Camera:** Medium wide, 35mm, both in frame, golden hour
- **On-screen text:** None
- **Voiceover:** "Uw verhuizing is bij ons..."
- **Characters:** Mourad + Karel
- **Image model:** Nano Banana Pro (with 2 character references)
- **Video model:** Kling v3 Standard I2V
- **Reference assets:** `/opt/pipeline/assets/crew/mourad_and_karel_together.png`, `/opt/pipeline/assets/truck/truck_right_side_view.png`
- **Difficulty:** Moderate (2 persons must be recognizable)
- **Prompt keywords:** two professional movers, standing confidently, team portrait, next to white Mercedes Sprinter truck with orange branding, golden hour, cinematic, warm, professional commercial look, film grain

### Shot 5 — Logo Closing (12-15s)

- **Description:** Snelverhuizen logo centered on dark background, fade-in animation
- **Camera:** Static
- **On-screen text:** Logo + "snelverhuizen.nl" below
- **Voiceover:** "...in goede handen."
- **Characters:** None
- **Generation:** Remotion composition only (no AI generation needed)
- **Reference assets:** `/opt/pipeline/assets/logo-snelverhuizen.png`
- **Difficulty:** Easy

## Audio Design

| Layer | Source | Details |
|-------|--------|---------|
| Voiceover | ElevenLabs Willem | stability 0.55, similarity_boost 0.75, style 0.35 |
| Ambient SFX | Freesound API | Quiet street ambiance, birds, light wind — fade in from shot 1, fade out at shot 5 |
| Music | NONE | Shari'ah compliance — no music ever |

## Caption Design

- **Font:** Montserrat Black, 900 weight
- **Style:** ALL CAPS, word-by-word animated reveal synced to voiceover timestamps
- **Color:** White (#FFFFFF), active word highlight optional
- **Shadow:** -45 deg, 55% opacity, 5% blur, 5px distance
- **Position:** Centered at 60% height (safe zone for 9:16)
- **Name cards:** "MOURAD" and "KAREL" as static text cards, center of frame, 72px, scale-up spring entrance

## Shari'ah Compliance Checklist

- [x] No music or instruments
- [x] Modest dress: black crewneck + blue jeans (covers 'awrah)
- [x] No free-mixing of genders
- [x] No haram background elements
- [x] No deceptive advertising
- [x] Professional, dignified tone (amanah)

## Color Grading

Apply the standard Snelverhuizen color grading profile to all shots:
- Warm golden amber highlights (~4500K pushed warm)
- Cool blue-tinted shadows (lifted, not crushed)
- Slightly desaturated midtones, natural skin tones preserved
- Medium-high contrast
- Lifted blacks (#0A0A0A to #151515)
- Subtle fine film grain
- Reference: `/opt/pipeline/assets/color_ref_1.png`, `color_ref_2.png`, `color_ref_3.png`

## Cost Estimate

| Item | Cost |
|------|------|
| 3x Nano Banana Pro / Flux Kontext Max hero frames | ~$0.30-0.50 |
| 4x Kling v3 Standard I2V animations (5s each) | ~$1.68 |
| 1x ElevenLabs voiceover (short script) | ~$0.05 |
| Freesound ambient SFX | Free (CC license) |
| **Total** | **~$2-3** |

## Generation Order

1. Shot 1 hero frame (truck) → QA → animate
2. Shot 2 hero frame (Mourad) → QA → animate
3. Shot 3 hero frame (Karel) → QA → animate
4. Shot 4 hero frame (together) → QA → animate
5. Generate voiceover with word-level timestamps
6. Download ambient SFX from Freesound
7. Create Shot 5 (logo) in Remotion
8. Assemble all clips + audio in FFmpeg
9. Add animated captions via Remotion
10. Final brand compliance check
11. Deliver via Telegram
