#!/usr/bin/env python3
"""One-shot generation: V4 shot 2 brother_pan at 10s via Kling v3 Pro I2V with keyframe pan."""
import base64
import json
import os
import sys
import time
from pathlib import Path

import httpx

# Pre-flight gate imports
from pre_flight_gate import check_payload

API_KEY = os.environ.get("AIMLAPI_API_KEY")
if not API_KEY:
    sys.exit("AIMLAPI_API_KEY not set")

REFS = Path("/opt/pipeline/output/video3-testimonial-prijs/refs/brother")
WIDE_REFS = Path("/opt/pipeline/output/video3-testimonial-prijs/refs/brother_wide")
START_IMG = REFS / "brother_eyecontact.jpg"
END_IMG = WIDE_REFS / "brother2_sofa_wide_9x16.png"
OUT_DIR = Path("/opt/pipeline/output/video3-testimonial-prijs/clips")
OUT_FILE = OUT_DIR / "brother_pan_v4_10s_sofa.mp4"
TASK_LOG = OUT_DIR / "brother_pan_v4_10s_sofa_task.json"


def to_data_uri(p: Path) -> str:
    b64 = base64.b64encode(p.read_bytes()).decode()
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{b64}"


def main():
    prompt = (
        "Slow cinematic camera pan left to right through the living room, smoothly "
        "transitioning across the space and revealing the white sofa, coffee table, "
        "and full room decor between the subjects. Subjects and furniture remain "
        "stationary in their places. Boxes, sofa, and TV stay completely still. "
        "Ambient window light stays consistent. Motion eases to a gentle stop."
    )
    negative = (
        "blurry, distorted, low quality, jittery, flickering, morphing faces, warping, "
        "deformed hands, extra fingers, sliding feet, identity drift, watermark, camera "
        "shake, inconsistent lighting, plastic skin, cartoonish, color shift, face "
        "distortion, unnatural skin texture, floating limbs, breathing movement, body "
        "sway, weight shifting, expression change, mood shift, camera drift, sudden "
        "zooms, background shifting, unstable details, background morphing, vehicle "
        "movement, text morphing, label warping, geometry distortion"
    )

    payload = {
        "model": "klingai/video-v3-pro-image-to-video",
        "image_url": to_data_uri(START_IMG),
        "tail_image_url": to_data_uri(END_IMG),
        "prompt": prompt,
        "duration": "10",
        "aspect_ratio": "9:16",
        "generate_audio": False,
        "cfg_scale": 0.5,
        "negative_prompt": negative,
    }

    # Pre-flight gate (pan shot, no specific character type)
    gate = check_payload(payload, character_type=None)
    if gate["status"] == "BLOCK":
        print(f"[pre-flight BLOCKED] violated rules: {gate['violated_rules']}", file=sys.stderr)
        sys.exit(2)
    print(f"[pre-flight PASS] all rules clear")

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    print(f"[submit] start={START_IMG.name} end={END_IMG.name} duration=10s cost~=$2.92")
    resp = httpx.post(
        "https://api.aimlapi.com/v2/generate/video/kling/generation",
        json=payload,
        headers=headers,
        timeout=60,
    )
    print(f"[submit] status={resp.status_code}")
    if resp.status_code >= 300:
        print(resp.text)
        sys.exit(1)
    data = resp.json()
    task_id = data.get("id") or data.get("generation_id")
    if not task_id:
        print(json.dumps(data, indent=2))
        sys.exit(1)
    print(f"[submit] task_id={task_id}")
    TASK_LOG.write_text(json.dumps({"task_id": task_id, "submitted_at": time.time(), "payload_meta": {"model": payload["model"], "duration": payload["duration"], "aspect_ratio": payload["aspect_ratio"]}}, indent=2))

    for i in range(60):  # up to 10 min
        time.sleep(10)
        poll = httpx.get(
            "https://api.aimlapi.com/v2/generate/video/kling/generation",
            params={"generation_id": task_id},
            headers=headers,
            timeout=30,
        )
        if poll.status_code >= 300:
            print(f"[poll #{i}] status={poll.status_code} body={poll.text[:200]}")
            continue
        j = poll.json()
        status = j.get("status") or j.get("state")
        print(f"[poll #{i}] status={status}")
        if status == "completed":
            url = j.get("video", {}).get("url") or j.get("url")
            if not url:
                print(json.dumps(j, indent=2))
                sys.exit(1)
            print(f"[download] {url}")
            with httpx.Client(timeout=120) as c:
                with c.stream("GET", url) as r:
                    r.raise_for_status()
                    with OUT_FILE.open("wb") as f:
                        for chunk in r.iter_bytes():
                            f.write(chunk)
            print(f"[done] saved -> {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")
            return
        if status in ("failed", "error"):
            print(json.dumps(j, indent=2))
            sys.exit(1)
    sys.exit("timeout waiting for generation")


if __name__ == "__main__":
    main()
