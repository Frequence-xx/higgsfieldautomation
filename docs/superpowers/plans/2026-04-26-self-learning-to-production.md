# Self-Learning → Production Improvement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redirect existing self-learning cron from upstream-monitoring-only to closed-loop production improvement, so we ramp from "1 video with effort" toward 2-3 flawless videos per session.

**Architecture:** Three new layers on top of existing learning-cycle.sh — (1) a Pre-Flight Gate that validates every API call against learned constraints from feedback_log, (2) a Component Library of reusable approved assets (characters, scenes, outfits, captions, audio beds), (3) a Pattern Extractor that mines feedback_log + generation_history weekly and distills new constraints into skills. Family Lock-In is a workflow rule (next 3 videos in same testimonial format) — no code, just discipline.

**Tech Stack:** Bash + Python (cron jobs), SQLite (existing pipeline.db), shell-script gate hooks, Markdown skill files. Same stack as current pipeline.

---

## File Structure

**New files:**
- `scripts/pre-flight-gate.py` — pre-generation validator, queries feedback_log + memory, returns BLOCK/PASS
- `scripts/pattern-extractor.py` — weekly job, mines feedback patterns, writes draft skill updates
- `assets/library/components.json` — registry of approved characters, scenes, outfits, audio beds
- `assets/library/<character>/` — per-character approved hero frames, outfits, voice IDs
- `skills/pre-flight-checks.md` — generated constraints (auto-updated by pattern extractor)
- `data/family-lock.json` — current production family + active rules
- `docs/superpowers/plans/2026-04-26-self-learning-to-production.md` — this plan

**Modified files:**
- `scripts/gen_*.py` (all generation scripts) — call pre-flight-gate at top, abort if BLOCK
- `scripts/learning-cycle.sh` — add pattern-extractor invocation
- `CLAUDE.md` — link family-lock + pre-flight-gate as mandatory before generation

---

## Phase 1: Pre-Flight Gate (Day 1, ~3h)

### Task 1: Read & catalog feedback_log entries

**Files:**
- Read: `data/pipeline.db` table `feedback_log`
- Create: `data/feedback-catalog.json` (machine-readable summary)

- [ ] **Step 1: Query existing feedback_log structure**

Run: `sqlite3 /opt/pipeline/data/pipeline.db ".schema feedback_log"` and `SELECT COUNT(*), MIN(created_at), MAX(created_at) FROM feedback_log;`

Document the rows: video_id, sentiment, feedback text, created_at.

- [ ] **Step 2: Categorize feedback into constraint types**

Manually scan all rejected/accepted entries. Bucket each into:
- `prompt_constraint` (e.g., "no breathing word in motion prompt")
- `composition_rule` (e.g., "hands out of frame for Avatar Pro")
- `brand_compliance` (e.g., "no side door on truck cargo box")
- `shariah_compliance` (e.g., "no hair/ears visible for women")
- `model_routing` (e.g., "Avatar Pro lipsyncs both faces — solve via face hiding")

- [ ] **Step 3: Write categorized constraints to JSON**

```json
{
  "shariah_compliance": [
    {
      "rule": "no_hair_visible",
      "applies_to": ["female_character"],
      "implementation": "beanie_pulled_to_eyebrows + cowl_to_chin",
      "source_feedback_id": 123,
      "first_observed": "2026-04-25"
    }
  ],
  "composition_rule": [
    {
      "rule": "hands_out_of_frame",
      "applies_to": ["avatar_pro_lipsync"],
      "implementation": "crop_input_below_chest_or_pre_crop",
      "source_feedback_id": 124
    }
  ]
}
```

- [ ] **Step 4: Commit catalog**

```bash
git add data/feedback-catalog.json
git commit -m "feat: catalog feedback_log into machine-readable constraints"
```

### Task 2: Build pre-flight gate script

**Files:**
- Create: `scripts/pre-flight-gate.py`
- Test: `scripts/test_pre_flight_gate.py`

- [ ] **Step 1: Write failing test**

```python
# scripts/test_pre_flight_gate.py
from pre_flight_gate import check_payload

def test_blocks_avatar_pro_with_hands_in_frame():
    payload = {
        "model": "klingai/avatar-pro",
        "image_url": "data:image/jpeg;base64,...",  # frame contains hands
        "image_metadata": {"hands_visible": True}
    }
    result = check_payload(payload, character_type="female")
    assert result["status"] == "BLOCK"
    assert "hands_out_of_frame" in result["violated_rules"]

def test_blocks_female_character_with_visible_hair():
    payload = {
        "model": "google/nano-banana-pro-edit",
        "prompt": "woman in cream beanie",
        "character_type": "female"
    }
    # missing explicit hair-coverage instruction
    result = check_payload(payload, character_type="female")
    assert result["status"] == "BLOCK"
    assert "no_hair_visible" in result["violated_rules"]

def test_passes_when_all_constraints_met():
    payload = {
        "model": "google/nano-banana-pro-edit",
        "prompt": "woman in cream beanie pulled to eyebrows fully covering hairline + ears + every strand of hair, cream knit cowl wrapped to chin, oversized poncho top no body shape",
        "character_type": "female"
    }
    result = check_payload(payload, character_type="female")
    assert result["status"] == "PASS"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /opt/pipeline && /opt/pipeline/venv/bin/python -m pytest scripts/test_pre_flight_gate.py -v`
Expected: FAIL with `ModuleNotFoundError: pre_flight_gate`

- [ ] **Step 3: Implement pre_flight_gate.py**

```python
# scripts/pre-flight-gate.py
import json
import re
import sys
from pathlib import Path

CATALOG = Path("/opt/pipeline/data/feedback-catalog.json")


def check_payload(payload: dict, character_type: str = None) -> dict:
    violations = []
    catalog = json.loads(CATALOG.read_text())
    prompt = payload.get("prompt", "").lower()
    model = payload.get("model", "")

    # Shari'ah compliance for female characters
    if character_type == "female":
        for rule in catalog.get("shariah_compliance", []):
            if rule["rule"] == "no_hair_visible":
                if not all(t in prompt for t in ["beanie", "cover", "hair"]):
                    violations.append("no_hair_visible")
            if rule["rule"] == "no_ears_visible":
                if "ear" not in prompt and "cowl" not in prompt:
                    violations.append("no_ears_visible")

    # Composition rules for Avatar Pro
    if "avatar-pro" in model:
        meta = payload.get("image_metadata", {})
        if meta.get("hands_visible"):
            violations.append("hands_out_of_frame")
        if meta.get("multiple_faces", False) and not meta.get("secondary_face_hidden", False):
            violations.append("single_face_only_avatar_pro")

    if violations:
        return {"status": "BLOCK", "violated_rules": violations}
    return {"status": "PASS", "violated_rules": []}


def main():
    payload = json.loads(sys.stdin.read())
    character_type = payload.pop("_character_type", None)
    result = check_payload(payload, character_type)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `/opt/pipeline/venv/bin/python -m pytest scripts/test_pre_flight_gate.py -v`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add scripts/pre-flight-gate.py scripts/test_pre_flight_gate.py
git commit -m "feat: pre-flight gate validates payloads against learned constraints"
```

### Task 3: Wire pre-flight into existing generation scripts

**Files:**
- Modify: `scripts/gen_v3_shot3_couple.py:35-50` (and all gen_*.py scripts)

- [ ] **Step 1: Add gate call to gen_v3_shot3_couple.py**

```python
# After payload definition, BEFORE httpx.post:
from subprocess import run as run_cmd
gate = run_cmd(
    ["/opt/pipeline/venv/bin/python", "/opt/pipeline/scripts/pre-flight-gate.py"],
    input=json.dumps({**payload, "_character_type": "female"}),
    capture_output=True, text=True
)
if gate.returncode != 0:
    print(f"[pre-flight BLOCKED]\n{gate.stdout}")
    sys.exit(2)
```

- [ ] **Step 2: Test against last session's bad payload**

Take the v6 payload (where hair was visible), run it through the gate. Expected: BLOCK with "no_hair_visible".

- [ ] **Step 3: Commit**

```bash
git add scripts/gen_v3_shot3_couple.py
git commit -m "feat: gate gen_v3_shot3 against learned constraints"
```

---

## Phase 2: Component Library (Days 2-3, ~6h)

### Task 4: Define library schema

**Files:**
- Create: `assets/library/components.json`
- Create: `assets/library/README.md`

- [ ] **Step 1: Define schema**

```json
{
  "characters": {
    "tarik": {
      "approved_at": "2026-04-16",
      "ref_sheet": "output/video3-testimonial-prijs/refs/tarik/tarik_v2_full_sheet.png",
      "voice_clone": null,
      "avatar_pro_compatible": true,
      "constraints": ["never lip-sync simultaneously with second character"],
      "approved_outfits": ["navy_crewneck_dark_jeans"]
    },
    "tarik_wife": {
      "approved_at": "2026-04-26",
      "ref_image": "output/video3-testimonial-prijs/hero_frames/s3_couple_hero_v11.jpg",
      "constraints": ["awrah covered without Islamic dress", "no makeup", "beanie + cowl combo"],
      "approved_outfits": ["cream_beanie_cowl_olive_tunic"]
    }
  },
  "scenes": {
    "warm_living_room": {
      "approved_at": "2026-04-26",
      "key_features": ["beige sofa", "hanging plants", "warm afternoon sunlight", "wood floor", "white walls"]
    }
  },
  "audio_beds": {
    "halal_nasheed": {
      "file": "captions/public/video3/nasheed2_trimmed.mp3",
      "approved_at": "2026-04-16",
      "loudnorm_target": "-16 LUFS linear"
    }
  }
}
```

- [ ] **Step 2: Commit schema**

```bash
git add assets/library/components.json assets/library/README.md
git commit -m "feat: component library schema"
```

### Task 5: Migrate approved assets into library

**Files:**
- Create: `assets/library/characters/tarik/`
- Create: `assets/library/characters/tarik_wife/`
- Create: `assets/library/scenes/warm_living_room/`

- [ ] **Step 1: Copy approved assets**

Run:
```bash
mkdir -p assets/library/characters/tarik
cp output/video3-testimonial-prijs/refs/tarik/* assets/library/characters/tarik/
mkdir -p assets/library/characters/tarik_wife
cp output/video3-testimonial-prijs/hero_frames/s3_couple_hero_v11.* assets/library/characters/tarik_wife/
```

- [ ] **Step 2: Commit assets**

```bash
git add assets/library/
git commit -m "feat: seed component library with approved Tarik + wife assets"
```

### Task 6: Build library lookup helper

**Files:**
- Create: `scripts/library.py`

- [ ] **Step 1: Implement helper**

```python
# scripts/library.py
import json
from pathlib import Path

LIB = Path("/opt/pipeline/assets/library")
INDEX = LIB / "components.json"


def get_character(name: str) -> dict:
    data = json.loads(INDEX.read_text())
    return data["characters"][name]


def get_scene(name: str) -> dict:
    data = json.loads(INDEX.read_text())
    return data["scenes"][name]


def list_approved_outfits(character: str) -> list:
    return get_character(character)["approved_outfits"]
```

- [ ] **Step 2: Commit**

```bash
git add scripts/library.py
git commit -m "feat: library lookup helper"
```

---

## Phase 3: Pattern Extractor (Day 4, ~4h)

### Task 7: Build pattern extractor script

**Files:**
- Create: `scripts/pattern-extractor.py`
- Modify: `scripts/learning-cycle.sh` (add weekly invocation)

- [ ] **Step 1: Implement extractor**

```python
# scripts/pattern-extractor.py
"""Mines feedback_log + generation_history for repeated rejection patterns.
Outputs draft skill update markdown to /opt/pipeline/output/research/patterns/<date>.md
for human review."""

import json
import sqlite3
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

DB = Path("/opt/pipeline/data/pipeline.db")
OUT_DIR = Path("/opt/pipeline/output/research/patterns")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Pull rejected generations from last week
    cur.execute(
        """
        SELECT prompt, failure_codes, improvement_suggestions
        FROM generation_history
        WHERE pass_fail IN ('rejected', 'fail') AND created_at >= ?
        """,
        (week_ago,),
    )
    rejected = cur.fetchall()

    # Count failure code frequency
    code_counter = Counter()
    for _, codes, _ in rejected:
        if codes:
            for c in codes.split(","):
                code_counter[c.strip()] += 1

    # Threshold: any code appearing 3+ times = candidate new constraint
    candidates = [c for c, n in code_counter.items() if n >= 3]

    # Write markdown report
    today = datetime.utcnow().strftime("%Y-%m-%d")
    report = OUT_DIR / f"{today}.md"
    with report.open("w") as f:
        f.write(f"# Pattern Extractor Report — {today}\n\n")
        f.write(f"Rejected generations last 7 days: {len(rejected)}\n\n")
        f.write("## Repeated Failure Codes (≥3 occurrences)\n\n")
        for code in candidates:
            f.write(f"- `{code}` ({code_counter[code]}× in 7d)\n")
        f.write("\n## Action: review and add to feedback-catalog.json + skills\n")

    print(f"[pattern-extractor] wrote {report}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Add to learning-cycle.sh**

Modify learning-cycle.sh to call pattern-extractor.py once per week (Sundays).

- [ ] **Step 3: Commit**

```bash
git add scripts/pattern-extractor.py scripts/learning-cycle.sh
git commit -m "feat: pattern extractor + weekly hook in learning cycle"
```

---

## Phase 4: Family Lock-In (Workflow rule, no code)

### Task 8: Document family-lock state

**Files:**
- Create: `data/family-lock.json`
- Modify: `CLAUDE.md` (add family-lock section)

- [ ] **Step 1: Initial state**

```json
{
  "current_family": "testimonial",
  "videos_in_family": ["V3-Tarik", "V4-Brother", "V3-Tarik-v2-couple"],
  "approved_components": ["tarik", "tarik_wife", "willemjan_voice", "warm_living_room"],
  "next_videos": ["V5-testimonial-pro1", "V6-testimonial-pro2"],
  "lock_until": 3
}
```

- [ ] **Step 2: Add to CLAUDE.md**

Add section: "Before producing a new video, check `data/family-lock.json`. If `videos_in_family` count < `lock_until`, the new video MUST stay in the same family format and reuse approved components."

- [ ] **Step 3: Commit**

```bash
git add data/family-lock.json CLAUDE.md
git commit -m "feat: family-lock workflow rule"
```

---

## Self-Review

**Spec coverage:**
- ✅ Pre-flight gate → Phase 1 (Tasks 1-3)
- ✅ Component library → Phase 2 (Tasks 4-6)
- ✅ Pattern extractor → Phase 3 (Task 7)
- ✅ Family lock-in → Phase 4 (Task 8)

**Order:** Phase 1 first (highest leverage — prevents repeating known mistakes). Phase 2 second (compounds Phase 1 by giving gate concrete approved assets to reference). Phase 3 third (automates discovery). Phase 4 fourth (workflow discipline).

**Total estimated time:** ~14h spread across 4 days.

**Expected outcome ramp:**
- After Phase 1: ~50% one-shot success rate (up from ~40%) — known mistakes blocked at gate
- After Phase 2: ~65% — reusable components reduce drift
- After Phase 3: ~75% — patterns get auto-distilled into skills weekly
- After Phase 4 + 3 testimonials in same family: ~85-90% — taste convergence + locked components
