---
name: Brief Intake
description: Parse video ad concepts from simple one-liners to detailed shot lists. Validate, expand, override Shari'ah violations, and produce a standardized shot list for production.
autoInvoke: true
triggers:
  - brief
  - concept
  - video ad
  - campaign
  - shot list
---

# Brief Intake Skill

## Handling Different Brief Types

### Type 1: Simple one-liner
> "emotional ad: family arrives at new home, golden hour, 30 seconds"

Expand into full shot list with:
- 5-6 shots at 5s each to fill 30s
- Camera angles per cinematic-standards.md shot type quality map
- Character references needed (family = multiple characters)
- Voiceover script written in Dutch
- Send expanded shot list to owner for approval

### Type 2: Detailed concept with shot list
> Full brief with timing, voiceover, visual elements, CTA, style notes

Extract and normalize:
- Parse exact timing from shot list
- Map each shot to a pipeline-compatible generation approach
- Flag any Shari'ah violations (music requests, immodest scenes)
- Flag DIFFICULT shots that need workarounds
- Preserve the owner's creative vision while adapting to AI capabilities

## Standardized Brief Format

Every brief, regardless of input format, must be normalized to this structure before production:

```json
{
  "id": "brief_003",
  "title": "Process Trust Ad",
  "format": "9:16",
  "total_duration_s": 18,
  "language": "nl",
  "voiceover_script": "Een goede verhuizing begint met...",
  "voiceover_voice": "willem",
  "cta_text": "Start je aanvraag...",
  "shariah_overrides": ["music_requested → replaced_with_ambient_sfx"],
  "shots": [
    {
      "number": 1,
      "start_s": 0,
      "end_s": 3,
      "description": "Phone screen with moving quote form",
      "shot_type": "ui_mockup",
      "difficulty": "difficult",
      "workaround": "Generate clean phone mockup, add UI via Remotion overlay",
      "on_screen_text": "BINNEN MINUTEN DUIDELIJKHEID",
      "characters": [],
      "image_model": "google/nano-banana-pro",
      "video_model": "kling-video/v3/standard/image-to-video",
      "camera": "static, slight zoom in",
      "lighting": "clean, modern, bright"
    }
  ]
}
```

## Shari'ah Auto-Override Rules

When parsing a brief, automatically catch and override:

| Brief says | Pipeline does | Reason |
|------------|---------------|--------|
| "background music" | Replace with ambient SFX (office sounds, nature, city) | No music — ever |
| "soft music" | Replace with quiet ambient atmosphere | No music |
| "energetic beat" | Replace with faster-paced ambient + quicker cuts | No music |
| "man and woman together casually" | Reframe as family (mahram) or separate scenes | No free-mixing |
| "shorts" / casual beach wear | Reframe with modest work clothing | Dress code |
| "bar" / "club" / "party" | Reframe to appropriate venue (office, home, park) | No haram venues |

Always flag overrides to the owner: "Brief requested background music — replaced with ambient office sounds per Shari'ah guidelines. Please confirm."

## Shot Type Mapping

Map each shot description to the best generation approach:

| Shot Description | Pipeline Approach |
|-----------------|-------------------|
| Truck on street, exterior, no people | Nano Banana Pro → Kling v3 Standard I2V (cheapest, proven) |
| Crew carrying furniture | Kontext Max (character refs) → Kling O1 Reference (character lock) |
| Customer reaction / portrait | Kontext Max → Kling v3 Standard I2V (profile/silhouette angle) |
| Phone/laptop screen UI | Nano Banana Pro (mockup) + Remotion overlay (UI elements) |
| Interior room / packing scene | Nano Banana Pro → Kling v3 Standard I2V |
| Aerial / drone / wide city | Nano Banana Pro → Kling v3 Standard I2V (AI excels at these) |
| Text card / title card | Remotion only (no AI generation needed) |
| CTA end card | Remotion (logo + text + background from last shot) |

## On-Screen Text vs Captions

Briefs may specify two types of text:

1. **Voiceover captions** — synced to speech timing, Montserrat Black ALL CAPS at 60% height. Handled by FFmpeg/Remotion in post-production.

2. **On-screen text cards** — designed text elements with specific timing (e.g., "BINNEN MINUTEN DUIDELIJKHEID" at 0-3s). These are separate from captions and rendered via Remotion as animated overlays. They have their own timing independent of voiceover.

Both types can appear simultaneously if the brief calls for it.

## Pacing and Style

| Brief style | Post-production approach |
|-------------|------------------------|
| "fast-paced intro" | First 3 seconds: quick cuts (0.5-1s per shot), dynamic camera movement |
| "clean transitions" | Match cuts, light leaks, 0.3s crossfades — never wipes or novelty |
| "calm, professional" | Longer shots (4-5s), slower camera movement, gentle crossfades |
| "energetic" | Faster cuts, more camera movement, shorter clips |
| "cinematic" | Slow deliberate movement, shallow DOF, anamorphic lens simulation |

## Viral Research Integration

Before expanding any brief into a shot list, the Viral Research Agent (`viral-research.md`) must:
1. Analyze the brief's content category (trust, emotional, humor, process, testimonial)
2. Research current viral patterns relevant to that category
3. Optimize the hook (first 3 seconds) based on proven scroll-stopping techniques
4. Apply pacing patterns that maximize retention
5. Filter all findings through Shari'ah compliance
6. Inject learnings into the shot list before sending to owner for approval

This ensures every video is not just well-produced but strategically designed for engagement.

## Output

After parsing, produce:
1. Standardized JSON brief (saved to `/opt/pipeline/briefs/brief_{id}.json`)
2. SQLite entry in `briefs` table with status "queued"
3. Summary sent to owner via Telegram for approval
4. Do NOT generate anything until owner approves the shot list
