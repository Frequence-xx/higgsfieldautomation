#!/usr/bin/env python3
"""Generate new 9:16 end keyframe via Nano Banana Pro Edit:
brother 2 mounting TV in wider living-room framing with white sofa + glass coffee table in foreground.

Uses reference sheet bottom panel + existing brother2_tv.jpg as edit inputs.
"""
import base64
import json
import os
import sys
from pathlib import Path

import httpx

# Pre-flight gate imports
from pre_flight_gate import check_payload

API_KEY = os.environ.get("AIMLAPI_API_KEY")
if not API_KEY:
    sys.exit("AIMLAPI_API_KEY not set")

REFS = Path("/opt/pipeline/output/video3-testimonial-prijs/refs/brother")
WIDE_REFS = Path("/opt/pipeline/output/video3-testimonial-prijs/refs/brother_wide")

BROTHER2_TIGHT = REFS / "brother2_tv.jpg"  # existing tight end keyframe
ROOM_WIDE = WIDE_REFS / "brother2_wide_bottom.png"  # bottom panel of reference sheet (has sofa)
REF_SHEET_SMALL = WIDE_REFS / "ref_sheet_small.jpg"  # compressed full ref sheet

OUT_FILE = WIDE_REFS / "brother2_sofa_wide_9x16.png"


def to_data_uri(p: Path) -> str:
    b64 = base64.b64encode(p.read_bytes()).decode()
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{b64}"


def main():
    prompt = (
        "Recompose this scene as a vertical 9:16 portrait frame of the same living room. "
        "Include the white fabric sofa with black armrests on the left-foreground, glass "
        "coffee table with dark blue pedestal vase and small mug in the middle-foreground, "
        "and the same bald man in an orange polo shirt and light chino pants on the right, "
        "carefully mounting the black wall-mounted TV on the dark wood dresser. Keep the "
        "tall window with grey curtains visible in the background, the sun-warmed lighting, "
        "wooden floor with area rug, and black leather armchair slightly visible in the "
        "lower-right foreground. Natural cinematic lighting, golden hour warm tones, 35mm "
        "depth of field, photorealistic."
    )

    payload = {
        "model": "google/nano-banana-pro-edit",
        "image_urls": [
            to_data_uri(ROOM_WIDE),
            to_data_uri(BROTHER2_TIGHT),
        ],
        "prompt": prompt,
        "aspect_ratio": "9:16",
        "resolution": "2K",
    }

    # Pre-flight gate (room scene only, no specific character type)
    gate = check_payload(payload, character_type=None)
    if gate["status"] == "BLOCK":
        print(f"[pre-flight BLOCKED] violated rules: {gate['violated_rules']}", file=sys.stderr)
        sys.exit(2)
    print(f"[pre-flight PASS] all rules clear")

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    print(f"[submit] refs={len(payload['image_urls'])} aspect=9:16 resolution=2K cost~=$0.195")
    resp = httpx.post(
        "https://api.aimlapi.com/v1/images/generations",
        json=payload,
        headers=headers,
        timeout=120,
    )
    print(f"[submit] status={resp.status_code}")
    if resp.status_code >= 300:
        print(resp.text)
        sys.exit(1)
    j = resp.json()
    # NBP Edit response can be: {"data": [{"url": "..."}]} or {"images": [{"url": "..."}]}
    url = None
    for k in ("data", "images"):
        if k in j and j[k]:
            url = j[k][0].get("url")
            if url:
                break
    if not url:
        print(json.dumps(j, indent=2))
        sys.exit("no url in response")
    print(f"[download] {url}")
    with httpx.Client(timeout=120) as c:
        r = c.get(url)
        r.raise_for_status()
        OUT_FILE.write_bytes(r.content)
    print(f"[done] {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
