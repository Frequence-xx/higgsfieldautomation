"""Tests for pre_flight_gate.check_payload.

Run:  cd /opt/pipeline && /opt/pipeline/venv/bin/python -m pytest scripts/test_pre_flight_gate.py -v
"""
import sys
import os

# Allow importing pre_flight_gate from the same directory
sys.path.insert(0, os.path.dirname(__file__))

from pre_flight_gate import check_payload


# ---------------------------------------------------------------------------
# Shari'ah compliance — female character hair coverage
# ---------------------------------------------------------------------------

def test_blocks_female_character_with_visible_hair_prompt():
    """Prompt has no hair-coverage keywords → BLOCK with female_character_full_hair_coverage."""
    payload = {
        "model": "google/nano-banana-pro-edit",
        "prompt": "a young woman in her late 20s seated on a sofa looking at camera",
    }
    result = check_payload(payload, character_type="female")
    assert result["status"] == "BLOCK", f"Expected BLOCK, got {result}"
    assert "female_character_full_hair_coverage" in result["violated_rules"]


def test_passes_female_character_with_full_hair_coverage_prompt():
    """Prompt explicitly covers beanie + hair coverage → PASS."""
    payload = {
        "model": "google/nano-banana-pro-edit",
        "prompt": (
            "a young woman wearing a chunky cream cable-knit beanie pulled deep down to "
            "her eyebrows, every strand of hair completely hidden under the beanie, "
            "thick cowl wrapped around her neck, no makeup, calm expression"
        ),
    }
    result = check_payload(payload, character_type="female")
    assert result["status"] == "PASS", f"Expected PASS, got {result}"
    assert "female_character_full_hair_coverage" not in result["violated_rules"]


# ---------------------------------------------------------------------------
# Composition rule — Avatar Pro: single-face-only lipsync
# ---------------------------------------------------------------------------

def test_blocks_avatar_pro_with_two_unhidden_faces():
    """Avatar Pro + multiple_faces=True + secondary_face_hidden=False → BLOCK."""
    payload = {
        "model": "klingai/avatar-pro",
        "image_url": "data:image/jpeg;base64,/9j/...",
        "image_metadata": {
            "multiple_faces": True,
            "secondary_face_hidden": False,
        },
    }
    result = check_payload(payload)
    assert result["status"] == "BLOCK", f"Expected BLOCK, got {result}"
    assert "single_face_only_avatar_pro" in result["violated_rules"]


def test_passes_avatar_pro_with_secondary_face_hidden():
    """Avatar Pro + multiple_faces=True but secondary_face_hidden=True → PASS for that rule."""
    payload = {
        "model": "klingai/avatar-pro",
        "image_url": "data:image/jpeg;base64,/9j/...",
        "image_metadata": {
            "multiple_faces": True,
            "secondary_face_hidden": True,
        },
    }
    result = check_payload(payload)
    assert result["status"] == "PASS", f"Expected PASS, got {result}"
    assert "single_face_only_avatar_pro" not in result["violated_rules"]


# ---------------------------------------------------------------------------
# Prompt constraint — truck shot anti-ghost-driving
# ---------------------------------------------------------------------------

def test_blocks_kling_v3_pro_truck_shot_without_anti_ghost_driving_language():
    """Kling v3 Pro truck shot with no stationary/parked keyword → BLOCK."""
    payload = {
        "model": "klingai/video-v3-pro-image-to-video",
        "prompt": "crew member loading boxes onto the truck, golden hour light, 9:16",
        "shot_type": "truck",
    }
    result = check_payload(payload)
    assert result["status"] == "BLOCK", f"Expected BLOCK, got {result}"
    assert "stationary_truck_no_vehicle_movement" in result["violated_rules"]


def test_passes_kling_v3_pro_truck_shot_with_anti_ghost_driving_language():
    """Kling v3 Pro truck shot with 'stationary truck, parked' keywords → PASS.

    generate_audio=False is also required for Kling video payloads — include it
    so this test isolates only the anti-ghost-driving rule.
    """
    payload = {
        "model": "klingai/video-v3-pro-image-to-video",
        "prompt": (
            "crew member loading boxes onto the stationary truck, parked at the curb, "
            "no vehicle movement, golden hour light, 9:16"
        ),
        "shot_type": "truck",
        "generate_audio": False,  # required for all Kling video calls
    }
    result = check_payload(payload)
    assert result["status"] == "PASS", f"Expected PASS, got {result}"
    assert "stationary_truck_no_vehicle_movement" not in result["violated_rules"]


# ---------------------------------------------------------------------------
# Brand compliance — #FC8434 color in brand-color still prompts
# ---------------------------------------------------------------------------

def test_passes_brand_compliant_prompt_with_FC8434_color():
    """FLUX.2 Pro brand still prompt with #FC8434 explicitly → PASS for brand color check."""
    payload = {
        "model": "blackforestlabs/flux-2-pro",
        "prompt": (
            "Snelverhuizen moving box, white cardboard, orange text #FC8434 label, "
            "SNELVERHUIZEN.NL printed on the side, studio lighting"
        ),
        "shot_type": "brand_color_still",
    }
    result = check_payload(payload)
    assert result["status"] == "PASS", f"Expected PASS, got {result}"
    assert "logo_color_orange_fc8434_missing" not in result["violated_rules"]


def test_blocks_brand_color_still_without_fc8434():
    """FLUX.2 Pro brand still with no color hex → BLOCK (orange color unspecified)."""
    payload = {
        "model": "blackforestlabs/flux-2-pro",
        "prompt": "Snelverhuizen moving box with orange text on white cardboard",
        "shot_type": "brand_color_still",
    }
    result = check_payload(payload)
    assert result["status"] == "BLOCK", f"Expected BLOCK, got {result}"
    assert "logo_color_orange_fc8434_missing" in result["violated_rules"]


# ---------------------------------------------------------------------------
# Model routing — banned model: seedance on AIMLAPI
# ---------------------------------------------------------------------------

def test_blocks_seedance_model():
    """Any use of seedance-2.0 → BLOCK per AIMLAPI-only routing rules."""
    payload = {
        "model": "seedance-2.0",
        "prompt": "man walking down the street",
    }
    result = check_payload(payload)
    assert result["status"] == "BLOCK", f"Expected BLOCK, got {result}"
    assert "aimlapi_only_no_seedance" in result["violated_rules"]


# ---------------------------------------------------------------------------
# Operational constraint — generate_audio must be False for video
# ---------------------------------------------------------------------------

def test_blocks_video_generation_without_generate_audio_false():
    """Kling video generation missing generate_audio=False → BLOCK."""
    payload = {
        "model": "klingai/video-v3-pro-image-to-video",
        "prompt": "man smiling eases to stop",
        "duration": "5",
        # generate_audio key is missing entirely → BLOCK
    }
    result = check_payload(payload)
    assert result["status"] == "BLOCK", f"Expected BLOCK, got {result}"
    assert "generate_audio_false_mandatory" in result["violated_rules"]


def test_passes_video_generation_with_generate_audio_false():
    """Kling video generation with generate_audio=False → PASS for that rule."""
    payload = {
        "model": "klingai/video-v3-pro-image-to-video",
        "prompt": "man smiling eases to stop, stationary truck, parked, no vehicle movement",
        "duration": "5",
        "generate_audio": False,
    }
    result = check_payload(payload)
    assert result["status"] == "PASS", f"Expected PASS, got {result}"
    assert "generate_audio_false_mandatory" not in result["violated_rules"]


# ---------------------------------------------------------------------------
# Graceful handling — missing fields don't crash
# ---------------------------------------------------------------------------

def test_empty_payload_does_not_crash():
    """Completely empty payload → no crash, returns PASS (nothing to check)."""
    result = check_payload({})
    assert isinstance(result, dict)
    assert result["status"] in ("PASS", "BLOCK")


def test_no_character_type_skips_hair_check():
    """No character_type → female hair check skipped, no false positive."""
    payload = {
        "model": "google/nano-banana-pro-edit",
        "prompt": "a sofa in a warm living room, afternoon light",
    }
    result = check_payload(payload)  # no character_type
    assert result["status"] == "PASS", f"Expected PASS, got {result}"
    assert "female_character_full_hair_coverage" not in result["violated_rules"]
