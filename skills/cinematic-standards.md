---
name: Cinematic Standards
description: Non-negotiable quality bar — blockbuster production quality (Transformers, Avengers, Superman 2025 tier). Defines shot-type quality map, cinematography grammar, transition vocabulary, and AI artifact mitigation.
autoInvoke: true
triggers:
  - prompt engineering
  - shot list
  - camera settings
  - video generation
  - cinematic
  - quality
negatives:
  - Do NOT invoke when task is caption/text overlay work only (use captions-and-titles.md)
  - Do NOT invoke when performing QA scoring (use video-qa-rubric.md for scoring dimensions)
  - Do NOT invoke when handling Shari'ah compliance checks with no visual quality question
---

# Cinematic Standards

The quality bar is blockbuster production. Every frame must look like it belongs in a theatrical trailer, not an AI demo. If it looks like AI, it's a reject.

## Shot Type Quality Map

AI video generation excels at some shot types and struggles with others. Route shots to maximize quality:

### STRONG — Near-blockbuster quality achievable
- **Wide establishing shots with camera movement** (drone, dolly, crane) — AI excels here. Use as hero shots. Best with slow, deliberate movement.
- **Exterior B-roll** (trucks on streets, buildings, neighborhoods, sky, nature) — highly cinematic at 4K. Add atmosphere: golden hour light, gentle wind in trees, wet pavement reflections.
- **Slow-motion captures** — AI handles temporal consistency well when slowed. Use for emotional moments: family stepping through doorway, hand on railing, truck driving away.
- **Static compositions with shallow depth of field** — locked tripod, 85mm, wide aperture. Beautiful bokeh backgrounds.

### MODERATE — Achievable with careful prompting
- **Medium shots of people in simple poses** (standing, walking, carrying) — works with Kling 3.0 + specific clothing descriptions. Keep movements simple and deliberate.
- **Over-shoulder shots** — reduce face detail requirements. Good for watching-the-movers scenes.
- **Silhouette shots** — backlit figures are naturally detail-free. Powerful for emotional moments.

### DIFFICULT — High failure rate, use workarounds
- **Close-up hands performing actions** (gripping furniture, turning keys, taping boxes) — 30-40% failure rate. **Workaround:** Use medium shots showing the full person. When hands must appear, use wider framing. Add "natural hand positions, relaxed grip" to prompts.
- **Facial expressions during dialogue** — character consistency degrades. **Workaround:** Profile angles, over-shoulder shots, silhouettes. Reserve direct face shots for single best model (Veo 3.1) and keep clips under 5 seconds.
- **Complex multi-person interactions** (two movers carrying couch) — simultaneous physics + anatomy is hard. **Workaround:** Break into sequential shots (mover 1 grips → cut → mover 2 lifts → cut → both walk). Edit creates the illusion of continuous action.

## Cinematography Grammar

### Lens Choices
| Shot type | Lens | Rationale |
|-----------|------|-----------|
| Wide establishing | 24mm anamorphic | Cinematic width, subtle distortion |
| Truck beauty shot | 35mm | Natural perspective, slight compression |
| Portrait / emotional | 85mm f/1.4 | Shallow DOF, subject isolation |
| Action / movement | 50mm | Versatile, natural eye perspective |
| Detail / texture | 100mm macro | Object beauty shots |

### Camera Movement
| Emotion | Movement | Notes |
|---------|----------|-------|
| Emotional reveal | Slow dolly push-in | 2-3 seconds, steady, deliberate |
| Action / energy | Steadicam tracking | Follow movement, slight handheld feel |
| Establishing / scale | Drone ascending or orbiting | Reveal the scene, show context |
| Intimacy | Locked tripod, shallow DOF | Let the subject breathe in the frame |
| Tension / anticipation | Slow zoom (not digital, simulate lens zoom) | Subtle, barely perceptible |

### Color Grading
| Scene type | Palette | LUT approach |
|------------|---------|-------------|
| Family / warmth / arrival | Warm golden: lifted shadows, amber highlights | Orange-teal complementary |
| Professional service | Clean neutral: balanced whites, slight cool shadows | Minimal grade, trust the natural |
| Dramatic / moving day stress | Desaturated cool: blue shadows, muted colors | Teal dominant, crushed blacks |
| Hero / reveal moment | High contrast warm: deep blacks, golden highlights | Cinema-grade, rich saturation |

## Transition Vocabulary

**USE:**
- Match cuts (door closing → door opening at new home)
- Whip pans (fast pan between scenes, implies time passing)
- Light leaks (golden anamorphic flares between scenes)
- J-cuts / L-cuts (audio leads or follows the visual transition)
- Hard cuts on action (cut mid-movement for energy)

**MUST NOT USE:**
- Star wipes, circle wipes, or novelty transitions
- Default dissolves longer than 0.5 seconds
- Digital zoom transitions
- Any transition that screams "template" or "stock"

## AI Artifact Mitigation

MUST include these in EVERY generation prompt:
- "natural wear, texture, and imperfections on all surfaces"
- "realistic fabric wrinkles and folds on clothing"
- "subtle asymmetry in composition"
- "practical on-set lighting, not studio-perfect"
- "film grain, slight lens imperfections"

Clip length limits for maximum temporal coherence:
- Standard clips: 5-8 seconds
- Simple/static compositions: up to 12 seconds
- Complex/moving compositions: 3-5 seconds maximum

Known AI tells to watch for in QA:
1. **Temporal jitter** — micro-movements in static elements
2. **Texture smoothing** — surfaces too uniform, no dust/scratches/wear
3. **Perfect symmetry** — real scenes are never perfectly symmetrical
4. **Plastic skin** — faces too smooth, lacking pores/texture
5. **Fabric physics** — cloth that doesn't fold correctly
6. **Shadow consistency** — shadows shifting direction within a clip
7. **Motion blur** — incorrect or missing on fast-moving elements
