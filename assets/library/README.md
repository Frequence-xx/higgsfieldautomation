# Component Library

Catalog of approved reusable production assets for Snel Verhuizen video ads.

## Purpose

Every asset here has been owner-approved in at least one shipped video. Reference them by name in new productions instead of regenerating — this eliminates drift, saves cost, and guarantees brand compliance from shot one.

## Structure

```
assets/library/
├── characters/           # Approved hero frames + ref sheets per character
│   ├── tarik/            # V3-Tarik (approved 2026-04-16)
│   ├── tarik_wife/       # V3-Tarik-v2-couple (approved 2026-04-26)
│   ├── karel/            # V2-Proces (approved 2026-04-12)
│   └── brother_willemjan/ # V4-Brother (approved 2026-04-17)
├── scenes/               # Scene reference frames (currently inferred from character refs)
│   ├── warm_living_room/
│   └── brother_living_room/
├── audio_beds/           # Approved audio loops and ambient tracks
│   ├── halal_nasheed/    # nasheed2_trimmed.mp3 — vocal only, no instruments
│   └── ambient_room_tone/ # ambient_clean.mp3 — continuous room tone
└── components.json       # Machine-readable index of all entries above
```

Files in each character dir are COPIES of approved originals. Source originals remain in `output/`. Never delete from `output/`.

## Consuming this library

Use `scripts/library.py` to look up assets by name:

```python
from library import get_character, get_scene, get_audio_bed, list_all_characters

# Get full record for a character
tarik = get_character("tarik")
# Returns: approved_at, ref_files, constraints, voice, outfit_description, etc.

# Get the right ref for API calls
api_ref = tarik["api_ref"]           # compressed .jpg for API upload
primary_ref = tarik["primary_ref"]   # full-quality .png for QA

# Get scene
room = get_scene("warm_living_room")
# Returns: key_features, constraints, ref_files

# Get audio bed
nasheed = get_audio_bed("halal_nasheed")
# Returns: file path, volume, loudnorm_target, fade_settings, constraints

# List all registered characters
names = list_all_characters()
# Returns: ["tarik", "tarik_wife", "karel", "brother_willemjan"]
```

## Adding a new approved asset

Do this ONLY after Farouq has approved the asset in a shipped video.

1. Create the subdir:
   ```
   assets/library/characters/<name>/
   ```
2. Copy (do not move) all ref files from `output/`:
   ```bash
   cp output/<video>/refs/<name>/* assets/library/characters/<name>/
   ```
3. Add an entry to `components.json` following the existing schema:
   - `approved_at` — date of owner approval
   - `approved_in` — list of video IDs where used
   - `ref_files` — paths relative to `/opt/pipeline/`
   - `primary_ref` — best-quality ref for QA
   - `api_ref` — compressed ref for API calls (max ~300KB)
   - `voice` — ElevenLabs voice_id or null
   - `outfit_description` — plain-English description for prompt writing
   - `constraints` — mandatory rules (brand, shari'ah, technical)
4. Run tests to verify lookup works:
   ```bash
   /opt/pipeline/venv/bin/python -m pytest /opt/pipeline/scripts/test_library.py -v
   ```
5. Do NOT commit without explicit owner approval.

## Rules

- `components.json` is source of truth. The files in subdirs must match what is listed in `ref_files`.
- Never add an asset that has not shipped in an approved video.
- Never remove an existing entry — deprecate with `"deprecated": true` if no longer used.
- `constraints` arrays are mandatory QA input — they feed the pre-flight gate (`scripts/pre_flight_gate.py`).
- For characters: `shariah_compliance` entries must include coverage details (beanie depth, cowl coverage).
- For voice: always store the ElevenLabs voice_id, never just the display name. Display names can change.
