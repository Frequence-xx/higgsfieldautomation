#!/usr/bin/env python3
"""V3 shot 3 — Kling Avatar Pro lipsync of woman to Jolanda VO.

Hero: s3_couple_hero_v2.jpg (Tarik + woman, no touching)
Audio: s3_audio.mp3 (3.24s Jolanda VO)
"""
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

HERO = Path("/opt/pipeline/output/video3-testimonial-prijs/hero_frames/s3_couple_hero_v11_crop.jpg")
AUDIO = Path("/opt/pipeline/captions/public/video3/s3_audio.mp3")

OUT_DIR = Path("/opt/pipeline/output/video3-testimonial-prijs/clips")
OUT_FILE = OUT_DIR / "s3_couple_lipsync_v11_nohand.mp4"
TASK_LOG = OUT_DIR / "s3_couple_lipsync_v11_nohand_task.json"


def to_data_uri(p: Path) -> str:
    suffix = p.suffix.lower()
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".m4a": "audio/mp4",
    }.get(suffix, "application/octet-stream")
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def main():
    payload = {
        "model": "klingai/avatar-pro",
        "image_url": to_data_uri(HERO),
        "audio_url": to_data_uri(AUDIO),
    }

    # Pre-flight gate
    gate = check_payload(payload, character_type="female")
    if gate["status"] == "BLOCK":
        print(f"[pre-flight BLOCKED] violated rules: {gate['violated_rules']}", file=sys.stderr)
        sys.exit(2)
    print(f"[pre-flight PASS] all rules clear")

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    print(f"[submit] hero={HERO.name} audio={AUDIO.name} ({AUDIO.stat().st_size} bytes)")
    resp = httpx.post(
        "https://api.aimlapi.com/v2/video/generations",
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
    TASK_LOG.write_text(json.dumps({"task_id": task_id, "submitted_at": time.time()}, indent=2))

    # Poll for completion (different endpoint for this generation type)
    poll_url = "https://api.aimlapi.com/v2/generate/video/kling/generation"
    for i in range(72):  # up to 12 min
        time.sleep(10)
        poll = httpx.get(poll_url, params={"generation_id": task_id}, headers=headers, timeout=30)
        if poll.status_code >= 300:
            print(f"[poll #{i}] status={poll.status_code} body={poll.text[:300]}")
            continue
        j = poll.json()
        status = j.get("status") or j.get("state")
        print(f"[poll #{i}] status={status}")
        if status == "completed":
            url = (j.get("video") or {}).get("url") or j.get("url")
            if not url:
                print(json.dumps(j, indent=2))
                sys.exit(1)
            print(f"[download] {url}")
            with httpx.Client(timeout=180) as c:
                with c.stream("GET", url) as r:
                    r.raise_for_status()
                    with OUT_FILE.open("wb") as f:
                        for chunk in r.iter_bytes():
                            f.write(chunk)
            print(f"[done] {OUT_FILE} ({OUT_FILE.stat().st_size} bytes)")
            return
        if status in ("failed", "error"):
            print(json.dumps(j, indent=2))
            sys.exit(1)
    sys.exit("timeout")


if __name__ == "__main__":
    main()
