#!/usr/bin/env python3
"""V3 shot 3 hero v10 — start from approved v7 (woman perfect) and edit ONLY the man
to be 100% back-to-camera reading a book."""
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

V7_HERO = Path("/opt/pipeline/output/video3-testimonial-prijs/hero_frames/s3_couple_hero_v11.jpg")
WOMAN_REF = Path("/home/farouq/.claude/channels/telegram/inbox/1777157859075-AQAD-QtrG-MtcFN-.jpg")

OUT_FILE = Path("/opt/pipeline/output/video3-testimonial-prijs/hero_frames/s3_couple_hero_v12.png")


def to_data_uri(p: Path) -> str:
    b64 = base64.b64encode(p.read_bytes()).decode()
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{b64}"


def main():
    prompt = (
        "Edit this image (Image 1): reframe to a TIGHT HEAD-AND-SHOULDERS CLOSE-UP. "
        "KEEP THE WOMAN IDENTICAL: same face, same cream cable-knit beanie pulled to "
        "eyebrows fully covering her hairline + ears + temples + every strand of hair, "
        "same cream knit cowl wrapped high to her chin, same calm direct-to-camera gaze, "
        "same no-makeup natural face. NEW FRAMING: zoom in tight — bottom edge of frame "
        "ends at the COWL/UPPER CHEST level, just below where the cowl meets the olive "
        "top. NO arms, NO hands, NO midsection, NO body below the cowl visible at all — "
        "just face, beanie, cowl, and the very top of the olive top. Her face fills the "
        "central portion of the frame larger than before. Behind her in the upper area "
        "of the frame, still visible: the man with his FULL BACK turned 180 degrees "
        "toward the camera — back of his head + back of shoulders in navy crewneck "
        "sweatshirt. NO face/ear/beard/profile of him visible — pure back-only. Same "
        "beige sofa, warm sunlit living room background. Critical: head-and-shoulders "
        "tight crop, ZERO hands or arms in frame, woman face larger."
    )

    payload = {
        "model": "google/nano-banana-pro-edit",
        "image_urls": [
            to_data_uri(V7_HERO),
            to_data_uri(WOMAN_REF),
        ],
        "prompt": prompt,
        "aspect_ratio": "9:16",
        "resolution": "2K",
    }

    # Pre-flight gate
    gate = check_payload(payload, character_type="female")
    if gate["status"] == "BLOCK":
        print(f"[pre-flight BLOCKED] violated rules: {gate['violated_rules']}", file=sys.stderr)
        sys.exit(2)
    print(f"[pre-flight PASS] all rules clear")

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    print(f"[submit] base=v7 woman_ref=Image 2 cost~=$0.195")
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
