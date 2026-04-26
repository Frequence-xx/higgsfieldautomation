#!/usr/bin/env python3
"""Pre-flight gate: validates API generation payloads against learned constraints.

Usage (CLI):
    echo '{"model":"...", "prompt":"...", "_character_type": "female"}' | \\
        /opt/pipeline/venv/bin/python /opt/pipeline/scripts/pre_flight_gate.py

Exit codes:
    0  → PASS   (all checks cleared)
    1  → BLOCK  (one or more rules violated — see violated_rules in JSON output)
    2  → malformed input (invalid JSON / missing required fields for mode)

Importable API:
    from pre_flight_gate import check_payload
    result = check_payload(payload, character_type="female")
    # result: {"status": "PASS"|"BLOCK", "violated_rules": [list of rule_ids]}
"""

import json
import re
import sys
from pathlib import Path

CATALOG_PATH = Path("/opt/pipeline/data/feedback-catalog.json")

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_catalog() -> dict:
    """Load feedback-catalog.json. Returns {} if missing (graceful)."""
    if not CATALOG_PATH.exists():
        return {}
    try:
        return json.loads(CATALOG_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _prompt_lower(payload: dict) -> str:
    return payload.get("prompt", "").lower()


def _model(payload: dict) -> str:
    return payload.get("model", "").lower()


def _is_kling_video(model: str) -> bool:
    return "kling" in model and "avatar" not in model


def _is_kling_avatar_pro(model: str) -> bool:
    return "avatar-pro" in model or "avatar_pro" in model


def _is_truck_shot(payload: dict) -> bool:
    """Shot is a truck shot when explicitly flagged OR model is kling video + truck in prompt."""
    if payload.get("shot_type") == "truck":
        return True
    model = _model(payload)
    prompt = _prompt_lower(payload)
    if _is_kling_video(model) and ("truck" in prompt or "verhuiswagen" in prompt):
        return True
    return False


def _is_brand_color_still(payload: dict) -> bool:
    """Shot is a brand-color still when explicitly flagged or uses flux-2-pro model."""
    if payload.get("shot_type") == "brand_color_still":
        return True
    model = _model(payload)
    return "flux-2-pro" in model or "flux_2_pro" in model


def _is_video_generation(model: str) -> bool:
    """True for any video generation model (not image generation)."""
    video_indicators = [
        "image-to-video", "image_to_video", "video-v3", "video_v3",
        "avatar-pro", "avatar_pro", "wan-2-5", "wan_2_5",
        "veo-3", "veo_3", "seedance",
    ]
    return any(v in model for v in video_indicators)


# ---------------------------------------------------------------------------
# Rule checker functions
# Each returns a list of violated rule_ids (empty list = no violation)
# ---------------------------------------------------------------------------

def _check_female_hair_coverage(payload: dict, character_type: str | None) -> list[str]:
    """shariah_compliance: female_character_full_hair_coverage.

    For female characters, the prompt MUST contain:
    - "beanie" (or "hijab" or "niqab" or "khimar")  — head covering present
    - at least one hair-concealment term: "hair" + "hidden" | "covered" | "covering" | "tucked"
      OR the phrase "strand" appearing with the beanie context
    """
    if character_type != "female":
        return []
    prompt = _prompt_lower(payload)
    # Must have a head covering mentioned
    head_covers = ["beanie", "hijab", "niqab", "khimar", "headscarf"]
    has_cover = any(h in prompt for h in head_covers)
    if not has_cover:
        return ["female_character_full_hair_coverage"]
    # Must also have hair concealment language
    hair_hidden = (
        ("hair" in prompt and any(w in prompt for w in ["hidden", "covered", "covering", "tucked", "strand", "zero"]))
    )
    if not hair_hidden:
        return ["female_character_full_hair_coverage"]
    return []


def _check_avatar_pro_single_face(payload: dict) -> list[str]:
    """composition_rule: single_face_only_avatar_pro.

    When model is avatar-pro AND image_metadata.multiple_faces=True AND
    secondary_face_hidden is NOT True → block.
    """
    if not _is_kling_avatar_pro(_model(payload)):
        return []
    meta = payload.get("image_metadata") or {}
    if meta.get("multiple_faces") and not meta.get("secondary_face_hidden"):
        return ["single_face_only_avatar_pro"]
    return []


def _check_avatar_pro_hands(payload: dict) -> list[str]:
    """composition_rule: hands_out_of_frame_avatar_pro.

    If caller explicitly sets image_metadata.hands_visible=True on an avatar-pro
    payload → block.
    """
    if not _is_kling_avatar_pro(_model(payload)):
        return []
    meta = payload.get("image_metadata") or {}
    if meta.get("hands_visible"):
        return ["hands_out_of_frame_avatar_pro"]
    return []


def _check_truck_anti_ghost_driving(payload: dict) -> list[str]:
    """prompt_constraint: stationary_truck_no_vehicle_movement.

    For truck shots (Kling video), prompt must contain anti-ghost-driving language.
    Required: at least "stationary" OR ("parked" AND "no vehicle movement") in prompt.
    """
    if not _is_truck_shot(payload):
        return []
    prompt = _prompt_lower(payload)
    negative = payload.get("negative_prompt", "").lower()
    combined = prompt + " " + negative
    has_stationary = "stationary" in combined
    has_parked = "parked" in combined
    has_no_vehicle = "no vehicle movement" in combined
    if has_stationary or (has_parked and has_no_vehicle):
        return []
    return ["stationary_truck_no_vehicle_movement"]


def _check_brand_color_hex(payload: dict) -> list[str]:
    """brand_compliance: logo_color_orange_fc8434_missing.

    For brand-color still shots (FLUX.2 Pro), the prompt MUST reference #FC8434
    (or fc8434 without the hash). Prevents generating wrong orange shade.
    """
    if not _is_brand_color_still(payload):
        return []
    prompt = _prompt_lower(payload)
    if "fc8434" in prompt:
        return []
    return ["logo_color_orange_fc8434_missing"]


def _check_banned_seedance(payload: dict) -> list[str]:
    """model_routing: aimlapi_only_no_seedance.

    Seedance 2.0 on AIMLAPI has no quality/cost advantage vs Kling v3 Pro and
    has prior face content-policy blocks. Block its use entirely.
    """
    if "seedance" in _model(payload):
        return ["aimlapi_only_no_seedance"]
    return []


def _check_generate_audio_false(payload: dict) -> list[str]:
    """prompt_constraint: generate_audio_false_mandatory.

    All Kling video generation calls MUST have generate_audio=False explicitly.
    AIMLAPI default flipped to TRUE — missing key silently enables audio.
    """
    model = _model(payload)
    # Only applies to Kling I2V (not avatar-pro, not still image generation)
    if not ("video-v3" in model or "video_v3" in model or
            ("kling" in model and "image-to-video" in model)):
        return []
    if payload.get("generate_audio") is not False:
        return ["generate_audio_false_mandatory"]
    return []


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------

def check_payload(payload: dict, character_type: str | None = None) -> dict:
    """Validate a generation payload against learned constraints.

    Args:
        payload: The API call payload dict (prompt, model, image_metadata, etc.)
        character_type: Optional hint — pass "female" when shot contains a
            female character to trigger Shari'ah compliance checks.

    Returns:
        {"status": "PASS" | "BLOCK", "violated_rules": [list of rule_ids]}

    The gate never crashes on missing payload fields — it simply skips checks
    that require caller-provided metadata when that metadata is absent.
    """
    if not isinstance(payload, dict):
        return {"status": "BLOCK", "violated_rules": ["malformed_payload_not_dict"]}

    # Merge character_type from payload if caller embedded it
    if character_type is None:
        character_type = payload.get("character_type") or payload.get("_character_type")

    violations: list[str] = []

    # Run all checks — order doesn't matter, all are independent
    violations.extend(_check_female_hair_coverage(payload, character_type))
    violations.extend(_check_avatar_pro_single_face(payload))
    violations.extend(_check_avatar_pro_hands(payload))
    violations.extend(_check_truck_anti_ghost_driving(payload))
    violations.extend(_check_brand_color_hex(payload))
    violations.extend(_check_banned_seedance(payload))
    violations.extend(_check_generate_audio_false(payload))

    if violations:
        return {"status": "BLOCK", "violated_rules": violations}
    return {"status": "PASS", "violated_rules": []}


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main() -> None:
    """Read JSON payload from stdin, print result, exit 0/1/2."""
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        sys.stderr.write(f"[pre-flight] malformed JSON input: {exc}\n")
        sys.exit(2)

    if not isinstance(payload, dict):
        sys.stderr.write("[pre-flight] input must be a JSON object\n")
        sys.exit(2)

    # Allow caller to embed _character_type in the payload dict
    character_type = payload.pop("_character_type", None)

    result = check_payload(payload, character_type=character_type)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
