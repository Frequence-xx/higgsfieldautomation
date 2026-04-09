---
name: Brand Identity
description: Complete brand assets, colors, typography, uniform specs, vehicle livery, and visual identity for Snel Verhuizen. All values verified and approved.
autoInvoke: true
triggers:
  - brand
  - logo
  - colors
  - uniform
  - truck
  - identity
  - Snel Verhuizen
---

# Brand Identity — Snel Verhuizen

## Company

- **Name:** Snelverhuizen.nl (styled as "SNELVERHUIZEN" in branding)
- **Tagline:** "Betaalbaar, Betrouwbaar & Binnen 30 min reactie"
- **Voiceover tagline (approved):** "Uw verhuizing, vakkundig uitgevoerd. Snel Verhuizen brengt zorg en precisie bij elke verhuizing."
- **Box slogan:** "VERHUIZEN ZONDER ZORGEN"
- **Website:** snelverhuizen.nl
- **Service area:** Whole of the Netherlands and Europe (EU relocations)
- **Address:** Oosteinderweg 541, 1432 BL Aalsmeer
- **Phone:** +31 85 3331 133 / +31 62 6618 666
- **Email:** info@snelverhuizen.nl

## Colors

- **Primary orange:** `#FC8434` — used in logo, box branding, accent elements
- **Primary blue:** `#214562` — used in backgrounds, truck accents, text on light
- **Accent green:** `#25D366` — WhatsApp green, CTA buttons (matches the brand's orange warmth and blue depth)
- **Text on dark backgrounds:** `#FFFFFF` (white)
- **Text on light backgrounds:** `#101518` (near-black)
- **Logo icon background:** Orange `#FC8434` box icon with white box illustration

## Logo

- **File:** `/opt/pipeline/assets/logo-snelverhuizen.png`
- **Logo format:** Orange box icon + "SNELVERHUIZEN" text in dark
- **Placement rule:** Bottom-right corner, 20px margin from edges, 8-10% of frame width
- **Minimum clear space:** Half the logo height on all sides
- **On dark backgrounds:** Use the logo as-is (orange icon + white text variant if available)
- **On branded boxes:** Orange `#FC8434` with white text + QR code

## Truck

- **Vehicle:** Mercedes Sprinter box truck
- **Base color:** White cab + white cargo box
- **Branding:** Orange `#FC8434` band across lower half of cargo box with "SNELVERHUIZEN" in white
- **Logo placement:** Orange box icon + "SNELVERHUIZEN" text on both sides, front top panel, and rear
- **Contact info on truck:** www.snelverhuizen.nl, phone numbers
- **Rear features:** Hydraulic liftgate, reflective safety stripes
- **Reference photos:** `/opt/pipeline/assets/truck/`
  - `truck_front.png` — front view with Mercedes badge
  - `truck_back.png` — rear view with liftgate
  - `truck_left_side_view.png` — driver side
  - `truck_right_side_view.png` — passenger side
  - `truck_rightdiagnol_side_view.png` — 3/4 hero angle
  - `truck_reference_sheet.png` — all 4 views with annotations

## Crew — Characters

### Karel
- **Role:** Crew member
- **Build:** Large, stocky
- **Hair:** Bald, light beard
- **Skin tone:** Light/fair
- **Uniform:** Black crewneck sweatshirt with orange SNELVERHUIZEN logo on left chest, blue jeans, white sneakers
- **Character prompt snippet:** "a stocky bald man with a light beard, fair skin, wearing a black crewneck sweatshirt with an orange SNELVERHUIZEN logo on the left chest, blue jeans, and white sneakers"
- **Reference photos:** `/opt/pipeline/assets/crew/`
  - `karel_character_sheet.png` — multi-angle reference sheet
  - `karel_full_body.png` — full body 3/4 angle
  - `karel_full_body_hallway.png` — in action, hallway
  - `karel_full_body_outside_with_box.png` — carrying box outdoors
  - `karel_full_body_outside_with_box_2.png` — carrying box, different angle
  - `karel_close_up_chest_logo.png` — logo detail
  - `karel_jacket_reference_sheet.png` — workwear jacket reference
  - `karel_jacket_reference_sheet_2.png` — workwear jacket alternative
  - `karel_mid_back.png` — back view, mid shot

### Mourad
- **Role:** Crew lead / company face
- **Build:** Medium
- **Hair:** Bald, clean shaven
- **Skin tone:** Medium olive
- **Uniform:** Black crewneck sweatshirt with orange SNELVERHUIZEN logo on left chest, blue jeans, white sneakers
- **Character prompt snippet:** "a medium-built bald man with clean shaven face, medium olive skin, wearing a black crewneck sweatshirt with an orange SNELVERHUIZEN logo on the left chest, blue jeans, and white sneakers"
- **Reference photos:** `/opt/pipeline/assets/crew/`
  - `mourad_reference_sheet.png` — multi-angle reference sheet
  - `mourad_full_body.png` — full body 3/4 angle
  - `mourad_full_body_hallway.png` — in action, hallway
  - `mourad_hand_shake.png` — customer interaction
  - `mourad_closeup_chest_logo.png` — logo detail
  - `mourad_jacket_reference_sheet.png` — workwear jacket reference
  - `mourad_and_karel_together.png` — both crew members together
  - `mourad_and_karel_working.png` — working together, moving scene
  - `mourad_and_karel_working_2.png` — working together, different angle

## Workwear Options

Two uniform variants (see `/opt/pipeline/assets/brand/snelverhuizen_workwear_reference_sheet.png`):

1. **Work Jacket:** Black waterproof nylon, orange "SNELVERHUIZEN" logo on chest and back, reflective trim, hooded option
2. **Turtleneck Shirt:** Black thermal fabric, orange "SNELVERHUIZEN" logo on chest and back collar

Both always worn with blue jeans and white sneakers in current reference material.

## Branded Moving Boxes

Two box types (see `/opt/pipeline/assets/brand/snelverhuizen_boxes_reference_sheet.png`):

- **Type A:** QR code front, orange and white variants, "SNELVERHUIZEN.NL" + phone + "VERHUIZEN ZONDER ZORGEN"
- **Type B:** Small logo front, same branding
- **Material:** Cardboard with handle cutouts
- **Replacement value printed:** €3.25 per box

## Locations

- **Typical neighborhoods:** Dutch suburban residential — brick rowhouses, tree-lined streets, cobblestone/paver roads
- **Interior settings:** Dutch apartments/homes — hardwood floors, steep staircases (typical for Netherlands), modern kitchens
- **Reference palette:** See color grading images at `/opt/pipeline/assets/color_ref_*.png`

## Typography

- **Primary font:** Montserrat Black (900 weight) — ALL CAPS for captions and headlines
- **Primary font path:** `/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf`
- **Secondary font:** Raleway Light (300 weight) — for subtitles, taglines, lighter text elements in title combinations
- **Secondary font path:** `/opt/pipeline/assets/fonts/Raleway-Light.ttf`
- **Title card combination:** Montserrat Black headline + Raleway Light subtitle (heavy/light contrast)
- **Caption style:** Montserrat Black, ALL CAPS, centered at 60% height
- **Caption shadow:** -45°, 55% opacity, 5% blur, distance 5
- **Caption color:** `#FFFFFF` (white text on footage)

## Tone of Voice

- **Style:** Friendly, warm, trustworthy, sometimes funny
- **Personality:** Natural and human — like talking to a reliable friend who happens to be amazing at moving
- **Humor:** Light, relatable jokes about moving day stress — never at anyone's expense, always tasteful
- **Language:** Dutch (primary), all voiceover and captions in Dutch
- **Voiceover voice:** Willem (`yBtEjlHaWNu9xrYohjbA`), ElevenLabs eleven_multilingual_v2, native Dutch professional
- **Voiceover settings:** stability 0.55, similarity_boost 0.75, style 0.35
- **Avoid:** Corporate jargon, aggressive sales, sensationalism, anything that feels scripted or robotic
- **Shari'ah compliance:** All content adheres to Islamic guidelines (see `shariah-compliance.md`)

## Color Grading

Based on three approved reference images (`/opt/pipeline/assets/color_ref_1.png`, `color_ref_2.png`, `color_ref_3.png`):

- **Overall feel:** Warm cinematic commercial — like a modern film shot on Alexa or RED
- **Color temperature:** Warm (shifted towards amber/golden, especially highlights)
- **Highlights:** Golden amber, slightly warm orange (~4500K pushed warm)
- **Shadows:** Cool blue-tinted, NOT crushed — lifted slightly for a modern film look
- **Midtones:** Slightly desaturated, natural skin tones preserved
- **Contrast:** Medium-high — strong separation between subject and background but not harsh
- **Saturation:** Slightly pulled back overall, but orange brand colors remain vibrant
- **Blacks:** Lifted slightly (not true black, more like #0A0A0A to #151515) — gives a cinematic softness
- **Film grain:** Subtle, fine grain — present but not distracting
- **Skin tones:** Natural and warm, never green or magenta shifted

**FFmpeg color grading approximation:**
```
eq=contrast=1.15:brightness=0.02:saturation=0.9,
curves=r='0/0.03 0.25/0.22 0.5/0.52 0.75/0.78 1/0.95':g='0/0.02 0.25/0.20 0.5/0.48 0.75/0.76 1/0.93':b='0/0.05 0.25/0.24 0.5/0.50 0.75/0.74 1/0.88',
unsharp=5:5:0.5
```

**Prompt keywords to achieve this look:** "warm golden hour lighting, cinematic color grading, slightly desaturated, lifted blacks, amber highlights, cool blue shadows, film grain, professional commercial look, shot on RED camera"
