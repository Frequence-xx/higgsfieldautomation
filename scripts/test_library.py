"""Tests for scripts/library.py — component library lookup helper."""

import pytest
import sys
from pathlib import Path

# Ensure scripts/ is on path when run from any cwd
sys.path.insert(0, str(Path(__file__).parent))

from library import (
    get_character,
    get_scene,
    get_audio_bed,
    list_approved_outfits,
    list_all_characters,
    list_all_scenes,
    list_all_audio_beds,
)


# ---------------------------------------------------------------------------
# Character lookup
# ---------------------------------------------------------------------------

def test_get_tarik_returns_record():
    record = get_character("tarik")
    assert record["approved_at"] == "2026-04-16"
    assert "ref_files" in record
    assert len(record["ref_files"]) == 3
    assert "constraints" in record
    assert isinstance(record["constraints"], list)
    # Voice should be null — Tarik is silent on-screen
    assert record["voice"] is None


def test_get_tarik_wife_returns_record():
    record = get_character("tarik_wife")
    assert record["approved_at"] == "2026-04-26"
    # Must have avatar_pro_ref for crop input
    assert "avatar_pro_ref" in record
    assert "s3_couple_hero_v11_crop" in record["avatar_pro_ref"]
    # Shari'ah constraints must be present
    shariah_constraints = [c for c in record["constraints"] if "hair" in c.lower() or "shariah" in c.lower() or "cowl" in c.lower()]
    assert len(shariah_constraints) > 0, "Tarik wife must have shari'ah coverage constraints"


def test_get_karel_returns_record():
    record = get_character("karel")
    assert record["approved_at"] == "2026-04-12"
    assert record["avatar_pro_compatible"] is False
    assert "flits_karel_clipboard_v4" in record["primary_ref"]


def test_get_brother_willemjan_returns_record():
    record = get_character("brother_willemjan")
    assert record["approved_at"] == "2026-04-17"
    # Must have voice clone ID
    assert record["voice"] == "44qL1A8Rf7MFQ8SerN2Q"
    assert record["voice_provider"] == "elevenlabs"
    assert len(record["ref_files"]) == 5


def test_get_unknown_character_raises_keyerror():
    with pytest.raises(KeyError) as exc_info:
        get_character("does_not_exist")
    assert "does_not_exist" in str(exc_info.value)
    # Error message should name available characters
    assert "tarik" in str(exc_info.value)


def test_list_all_characters_includes_known_names():
    names = list_all_characters()
    assert "tarik" in names
    assert "tarik_wife" in names
    assert "karel" in names
    assert "brother_willemjan" in names
    assert len(names) == 4


def test_list_approved_outfits_tarik():
    outfits = list_approved_outfits("tarik")
    assert isinstance(outfits, list)
    assert "navy_crewneck_dark_jeans" in outfits


def test_list_approved_outfits_unknown_raises_keyerror():
    with pytest.raises(KeyError):
        list_approved_outfits("ghost_character")


# ---------------------------------------------------------------------------
# Scene lookup
# ---------------------------------------------------------------------------

def test_get_warm_living_room_scene():
    scene = get_scene("warm_living_room")
    assert "approved_at" in scene
    assert "key_features" in scene
    features_text = " ".join(scene["key_features"]).lower()
    assert "sofa" in features_text
    assert "sunlight" in features_text or "warm" in features_text
    assert "constraints" in scene


def test_get_brother_living_room_scene():
    scene = get_scene("brother_living_room")
    features_text = " ".join(scene["key_features"]).lower()
    assert "snelverhuizen" in features_text or "boxes" in features_text
    assert "constraints" in scene


def test_get_unknown_scene_raises_keyerror():
    with pytest.raises(KeyError) as exc_info:
        get_scene("no_such_scene")
    assert "no_such_scene" in str(exc_info.value)


def test_list_all_scenes():
    scenes = list_all_scenes()
    assert "warm_living_room" in scenes
    assert "brother_living_room" in scenes


# ---------------------------------------------------------------------------
# Audio bed lookup
# ---------------------------------------------------------------------------

def test_get_halal_nasheed_audio_bed():
    audio = get_audio_bed("halal_nasheed")
    assert audio["instruments"] is False
    assert audio["volume"] == 0.22
    assert "-16 LUFS" in audio["loudnorm_target"]
    assert "fade_settings" in audio
    assert audio["fade_settings"]["fade_out_duration_seconds"] == 3
    # File path should point into library
    assert "nasheed2_trimmed" in audio["file"]


def test_get_ambient_room_tone_audio_bed():
    audio = get_audio_bed("ambient_room_tone")
    assert audio["volume"] == 0.025
    assert audio["play_range"] == "frame 0 to end of composition"
    assert audio["instruments"] is False


def test_get_unknown_audio_bed_raises_keyerror():
    with pytest.raises(KeyError) as exc_info:
        get_audio_bed("no_such_bed")
    assert "no_such_bed" in str(exc_info.value)


def test_list_all_audio_beds():
    beds = list_all_audio_beds()
    assert "halal_nasheed" in beds
    assert "ambient_room_tone" in beds


# ---------------------------------------------------------------------------
# File existence sanity check
# ---------------------------------------------------------------------------

def test_all_character_ref_files_exist():
    """Every ref_file listed in components.json must actually exist on disk."""
    base = Path("/opt/pipeline")
    for name in list_all_characters():
        record = get_character(name)
        for ref in record["ref_files"]:
            p = base / ref
            assert p.exists(), f"Missing ref file for character '{name}': {ref}"


def test_all_audio_bed_files_exist():
    """Audio bed files in library dir must exist."""
    base = Path("/opt/pipeline")
    for name in list_all_audio_beds():
        record = get_audio_bed(name)
        p = base / record["file"]
        assert p.exists(), f"Missing audio file for bed '{name}': {record['file']}"
