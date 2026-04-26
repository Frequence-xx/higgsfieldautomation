"""Component library lookup helper.

Reads assets/library/components.json and provides named access to approved
production assets: characters, scenes, and audio beds.

All paths in components.json are relative to /opt/pipeline/.
"""

import json
from pathlib import Path

LIB_DIR = Path("/opt/pipeline/assets/library")
INDEX = LIB_DIR / "components.json"


def _load() -> dict:
    """Load and return the full components index."""
    return json.loads(INDEX.read_text())


def get_character(name: str) -> dict:
    """Return the full record for an approved character.

    Args:
        name: Character key as stored in components.json
              (e.g. "tarik", "tarik_wife", "karel", "brother_willemjan")

    Returns:
        dict with approved_at, ref_files, constraints, voice, outfit_description, etc.

    Raises:
        KeyError: if name is not found in the library
    """
    data = _load()
    if name not in data["characters"]:
        raise KeyError(
            f"Character '{name}' not found in library. "
            f"Available: {list(data['characters'].keys())}"
        )
    return data["characters"][name]


def get_scene(name: str) -> dict:
    """Return the full record for an approved scene.

    Args:
        name: Scene key as stored in components.json
              (e.g. "warm_living_room", "brother_living_room")

    Returns:
        dict with approved_at, key_features, ref_files, constraints

    Raises:
        KeyError: if name is not found in the library
    """
    data = _load()
    if name not in data["scenes"]:
        raise KeyError(
            f"Scene '{name}' not found in library. "
            f"Available: {list(data['scenes'].keys())}"
        )
    return data["scenes"][name]


def get_audio_bed(name: str) -> dict:
    """Return the full record for an approved audio bed.

    Args:
        name: Audio bed key as stored in components.json
              (e.g. "halal_nasheed", "ambient_room_tone")

    Returns:
        dict with file path, volume, loudnorm_target, fade_settings, constraints

    Raises:
        KeyError: if name is not found in the library
    """
    data = _load()
    if name not in data["audio_beds"]:
        raise KeyError(
            f"Audio bed '{name}' not found in library. "
            f"Available: {list(data['audio_beds'].keys())}"
        )
    return data["audio_beds"][name]


def list_approved_outfits(character: str) -> list[str]:
    """Return the list of approved outfit slugs for a character.

    Args:
        character: Character key (e.g. "tarik")

    Returns:
        List of outfit slug strings (e.g. ["navy_crewneck_dark_jeans"])

    Raises:
        KeyError: if character is not found in the library
    """
    return get_character(character)["approved_outfits"]


def list_all_characters() -> list[str]:
    """Return the names of all characters registered in the library.

    Returns:
        Sorted list of character key strings.
    """
    data = _load()
    return sorted(data["characters"].keys())


def list_all_scenes() -> list[str]:
    """Return the names of all scenes registered in the library."""
    data = _load()
    return sorted(data["scenes"].keys())


def list_all_audio_beds() -> list[str]:
    """Return the names of all audio beds registered in the library."""
    data = _load()
    return sorted(data["audio_beds"].keys())
