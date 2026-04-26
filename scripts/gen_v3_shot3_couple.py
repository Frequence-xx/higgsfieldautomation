#!/usr/bin/env python3
"""Generate V3 shot 3 hero: Tarik + modest woman sitting together on couch.

Refs:
- Tarik character sheet (compressed)
- Woman style reference (cream beanie + knit cowl + olive tunic, no makeup)

Output: /opt/pipeline/output/video3-testimonial-prijs/hero_frames/s3_couple_hero.png
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

TARIK_SHEET = Path("/opt/pipeline/output/video3-testimonial-prijs/refs/tarik/tarik_sheet_small.jpg")
WOMAN_REF = Path("/home/farouq/.claude/channels/telegram/inbox/1777157859075-AQAD-QtrG-MtcFN-.jpg")

OUT_DIR = Path("/opt/pipeline/output/video3-testimonial-prijs/hero_frames")
OUT_FILE = OUT_DIR / "s3_couple_hero_v9.png"


def to_data_uri(p: Path) -> str:
    b64 = base64.b64encode(p.read_bytes()).decode()
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{b64}"


def main():
    prompt = (
        "Cinematic 9:16 vertical close-up portrait. PRIMARY FOCUS: a young woman in her "
        "late 20s seated on a beige fabric sofa, framed CHEST-UP and CENTERED in the frame, "
        "looking DIRECTLY AT THE CAMERA with calm warm presence and a soft thoughtful "
        "expression. She wears exactly the outfit from the second reference image (Image 2): "
        "a chunky cream cable-knit beanie pulled DEEP down — the beanie's bottom front "
        "edge touches her EYEBROWS (the beanie comes ALL the way down to her brow line), "
        "and the beanie wraps fully around the sides EXTENDING DOWN PAST THE EARLOBES "
        "AND PAST THE JAWLINE at the sides — the entire ear (both ears) is COMPLETELY "
        "AND TOTALLY HIDDEN under the beanie's side flaps, with ZERO PART of any ear "
        "visible (no earlobe peek, no ear cartilage, no ear shadow, no earring, NOTHING "
        "of either ear shows). The beanie's side flaps blend seamlessly into the cowl. "
        "Her bare "
        "skin is the ONLY thing visible from her eyebrows down to her chin — no forehead "
        "skin shows above the eyebrows. Her HEAD UNDER THE BEANIE IS SHAVED OR THE HAIR "
        "IS COMPLETELY TUCKED INSIDE THE BEANIE — there is ZERO hair texture, ZERO hair "
        "strand, ZERO wisp, ZERO curl, ZERO bump of hair visible at temples, cheeks, "
        "neck, ears, or anywhere — the beanie's surface is smooth and uninterrupted. "
        "Imagine she is bald under the beanie — the beanie sits flush against her scalp "
        "and skin with no hair pushing it out anywhere. A thick cream knit cowl scarf "
        "wrapped around her neck reaching UP TO HER LOWER LIP at the front, "
        "and a HEAVY EXTREMELY OVERSIZED olive-sage green linen poncho-style top that "
        "drapes straight down from her shoulders like a rectangular sack — completely "
        "BAGGY and STRUCTURED, hanging loose with NO defined waist, NO visible chest "
        "curves, NO breast shape, NO body silhouette whatsoever. The fabric falls "
        "vertically in straight folds from shoulder to hip without revealing any of her "
        "body underneath. Long loose sleeves that hang past wrists. She has a "
        "completely natural fresh face with NO makeup whatsoever — no foundation, no "
        "lipstick, no mascara, no blush, no eyeshadow. Plain, calm, friendly expression, "
        "lips slightly closed, eyes calm. SECONDARY/BACKGROUND: visible to her left/behind "
        "her, slightly OUT OF FOCUS, the bearded man from the first reference image "
        "(Image 1) — early 30s Middle Eastern, full neat beard, navy blue crewneck "
        "sweatshirt — is seated with his FULL BACK turned 180 DEGREES TOWARD THE CAMERA. "
        "We ONLY see the BACK OF HIS HEAD (short dark hair on the back of his skull, "
        "no scalp showing) and the BACK OF HIS SHOULDERS/upper back in the navy "
        "sweatshirt. His face, beard, profile, cheek, ear, mouth, nose are ALL HIDDEN "
        "from the camera — completely 100% back-facing. He is hunched slightly forward "
        "holding a hardcover book in his lap, reading peacefully — the back of his head "
        "tilted slightly down toward the book. The pose is unmistakably 'man with his "
        "back to camera, reading a book in his lap'. They are clearly a married couple "
        "sitting on the same sofa but NOT touching. Background: warm afternoon sunlight, "
        "hanging plants, soft white walls. Photorealistic, 85mm portrait lens compression, "
        "shallow depth of field — the woman is tack-sharp, the man's back is slightly "
        "blurred but his back-to-camera reading pose is unmistakable."
    )

    payload = {
        "model": "google/nano-banana-pro-edit",
        "image_urls": [
            to_data_uri(TARIK_SHEET),
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
