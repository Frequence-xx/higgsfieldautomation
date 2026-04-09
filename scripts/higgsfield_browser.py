"""
Higgsfield Cinema Studio — Patchright browser automation.

Uses Patchright (CDP-leak-patched Playwright fork), persistent Chrome profile,
Xvfb headed mode, and human-like interaction to drive Cinema Studio 2.0
for hero frame generation. Video animation is handled by AIMLAPI (see
higgsfield-generation.md skill for the full architecture).

Architecture:
  - Patchright patches Runtime.Enable CDP detection that DataDome flags
  - System Chrome (not Chromium) for correct TLS fingerprint
  - Persistent user_data_dir keeps login alive across all runs
  - Xvfb headed mode (headless=False) avoids headless detection
  - Human-like delays and mouse movement patterns

Cinema Studio 2.0 workflow (from tutorials):
  1. Image tab → create Elements (4 reference angles per character)
  2. Grid Mode 4x4 → generate hero frame variations
  3. Select best frame → Animate → moves to Video tab
  4. Director Panel: characters, genre, camera body + lens + focal length
  5. Shot mode: Single / Multi-shot Auto / Multi-shot Manual
  6. Per-shot: prompt, camera movement, speed ramp, duration
  7. Generate → download

Model switching: Left sidebar dropdown in active project →
  Cinema 3.0 / Cinema 2.5 / Soul Cinema / Cinema 2.0
"""

import asyncio
import json
import os
import random
from pathlib import Path

from patchright.async_api import async_playwright

# ── Paths ──────────────────────────────────────────────────────────────
PROFILE_DIR = Path.home() / ".config" / "higgsfield-profile"
SCREENSHOT_DIR = Path("/opt/pipeline/qa")
DOWNLOAD_DIR = Path("/opt/pipeline/generations")
CODE_FILE = Path("/opt/pipeline/config/verify-code.txt")

for d in [SCREENSHOT_DIR, DOWNLOAD_DIR, PROFILE_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ── Human behavior simulation ──────────────────────────────────────────
class Human:
    """Natural interaction patterns — variable timing, imprecise clicks."""

    @staticmethod
    async def pause(lo=0.4, hi=1.2):
        await asyncio.sleep(random.uniform(lo, hi))

    @staticmethod
    async def type_into(page, selector, text):
        el = page.locator(selector).first
        await el.click()
        await asyncio.sleep(random.uniform(0.2, 0.5))
        for ch in text:
            await page.keyboard.type(ch, delay=random.randint(30, 85))
        await asyncio.sleep(random.uniform(0.2, 0.4))

    @staticmethod
    async def click_at(page, x, y):
        """Move mouse naturally then click with slight offset."""
        ox = x + random.uniform(-3, 3)
        oy = y + random.uniform(-3, 3)
        await page.mouse.move(ox, oy, steps=random.randint(6, 18))
        await asyncio.sleep(random.uniform(0.08, 0.25))
        await page.mouse.click(ox, oy)
        await asyncio.sleep(random.uniform(0.3, 0.8))

    @staticmethod
    async def click_el(page, selector, timeout=10000):
        el = page.locator(selector).first
        await el.wait_for(state="visible", timeout=timeout)
        box = await el.bounding_box()
        if box:
            await Human.click_at(
                page,
                box["x"] + box["width"] * random.uniform(0.3, 0.7),
                box["y"] + box["height"] * random.uniform(0.3, 0.7),
            )
        else:
            await el.click()
            await asyncio.sleep(random.uniform(0.3, 0.6))


# ── Main browser class ─────────────────────────────────────────────────
class HiggsfieldBrowser:

    def __init__(self):
        self.pw = None
        self.ctx = None
        self.page = None
        self.h = Human()

    async def __aenter__(self):
        await self.launch()
        return self

    async def __aexit__(self, *a):
        await self.close()

    # ── lifecycle ──────────────────────────────────────────────────────
    async def launch(self):
        self.pw = await async_playwright().start()

        # Persistent context = login survives across all runs
        self.ctx = await self.pw.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",           # System Chrome — correct TLS fingerprint
            headless=False,             # Headed via Xvfb — avoids headless detection
            no_viewport=False,
            viewport={"width": 1920, "height": 1080},
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ],
        )
        self.page = self.ctx.pages[0] if self.ctx.pages else await self.ctx.new_page()
        print("[browser] Launched — Patchright + Chrome + persistent profile")

    async def close(self):
        if self.ctx:
            await self.ctx.close()
        if self.pw:
            await self.pw.stop()
        print("[browser] Closed")

    async def ss(self, name="debug"):
        p = SCREENSHOT_DIR / f"{name}.png"
        await self.page.screenshot(path=str(p))
        return str(p)

    # ── auth ───────────────────────────────────────────────────────────
    async def ensure_logged_in(self):
        """Navigate to Higgsfield. If not logged in, perform login."""
        await self.page.goto("https://higgsfield.ai", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(5)

        # Check: do we see Login/Sign up buttons?
        text = await self.page.evaluate("() => document.body.innerText.substring(0, 2000)")
        # If "Credits" or profile avatar visible and no login modal → logged in
        if "Buy Credits" in text or "Assets" in text:
            print("[auth] Session valid — already logged in")
            return True

        # Check if the login modal is covering the page
        has_welcome = "Welcome to Higgsfield" in text or "Continue with Google" in text
        if not has_welcome:
            # No login modal and no obvious logged-in indicator — might be logged in
            # Check nav for user indicators
            nav = await self.page.evaluate("""() => {
                const el = document.querySelector('header, nav');
                return el ? el.innerText : '';
            }""")
            if "Login" not in nav:
                print("[auth] Session valid — no Login button in nav")
                return True

        print("[auth] Need to log in...")
        return await self._login()

    async def _login(self):
        # Verify we're on the real Higgsfield domain before entering credentials
        current_url = self.page.url
        if not current_url.startswith("https://higgsfield.ai"):
            print(f"[auth] SECURITY: Refusing to enter credentials — wrong domain: {current_url}")
            return False

        email = os.environ.get("HIGGSFIELD_EMAIL", "")
        password = os.environ.get("HIGGSFIELD_PASSWORD", "")

        # Accept cookies if present
        try:
            await self.h.click_el(self.page, "text=Accept all", timeout=3000)
        except Exception:
            pass
        await self.h.pause(0.5, 1)

        # Click Login in nav
        await self.h.click_el(self.page, "a:has-text('Login')", timeout=5000)
        await self.h.pause(1.5, 3)

        # Click Continue with Email if welcome modal shows
        try:
            await self.h.click_el(self.page, "text=Continue with Email", timeout=3000)
            await self.h.pause(1, 2)
        except Exception:
            pass

        # Fill credentials
        await self.h.type_into(self.page, "input[name=email]", email)
        await self.h.pause(0.2, 0.5)
        await self.h.type_into(self.page, "input[name=password]", password)
        await self.h.pause(0.3, 0.6)

        # Submit
        await self.h.click_el(self.page, "button:has-text('Log in'), input[type=submit]", timeout=5000)
        await self.h.pause(3, 5)

        # Check for email verification
        text = await self.page.evaluate("() => document.body.innerText.substring(0, 1000)")
        if "Verify" in text or "verification" in text:
            print("[auth] Verification code needed — write it to /opt/pipeline/config/verify-code.txt")
            return await self._handle_verify()

        print("[auth] Login complete")
        return True

    async def _handle_verify(self):
        for _ in range(300):
            # Verify still on Higgsfield domain
            if not self.page.url.startswith("https://higgsfield.ai"):
                print(f"[auth] SECURITY: Aborting verify — redirected to: {self.page.url}")
                return False
            if CODE_FILE.exists():
                code = CODE_FILE.read_text().strip()
                print(f"[auth] Entering code: {code}")
                await self.page.locator("input").first.fill(code)
                await self.page.keyboard.press("Enter")
                await self.h.pause(5, 8)
                CODE_FILE.unlink(missing_ok=True)

                text = await self.page.evaluate("() => document.body.innerText.substring(0, 500)")
                if "INCORRECT" in text or "incorrect" in text:
                    print("[auth] Code incorrect — waiting for new code...")
                    continue
                print("[auth] Verified")
                return True
            await asyncio.sleep(1)
        print("[auth] Timeout")
        return False

    # ── Cinema Studio navigation ───────────────────────────────────────
    async def open_cinema_studio(self):
        """Navigate to Cinema Studio and dismiss any overlays."""
        await self.page.goto(
            "https://higgsfield.ai/cinema-studio",
            wait_until="domcontentloaded",
            timeout=30000,
        )
        await asyncio.sleep(6)
        await self._dismiss_overlays()
        await self.ss("cinema_studio_loaded")
        print("[nav] Cinema Studio loaded")

    async def _dismiss_overlays(self):
        """Remove any login/marketing modals covering the UI."""
        await self.page.evaluate("""() => {
            document.querySelectorAll('*').forEach(e => {
                const s = getComputedStyle(e);
                if (s.position === 'fixed' && parseInt(s.zIndex || 0) > 50
                    && e.getBoundingClientRect().height > 200) {
                    e.remove();
                }
            });
        }""")
        await asyncio.sleep(0.5)

    async def switch_to_cinema_2(self):
        """
        Switch to Cinema Studio 2.0 via the Scenes panel dropdown.
        Proven workflow: Open Scenes panel → find Cinema 2.0 button → JS click.
        Requires an active project with at least one scene.
        """
        # Step 1: Open Scenes panel to reveal the model selector
        await self.open_scenes_panel()
        await self.h.pause(2, 3)

        # Step 2: Click Cinema 2.0 via JavaScript (proven reliable)
        switched = await self.page.evaluate("""() => {
            for (const b of document.querySelectorAll('button')) {
                for (const s of b.querySelectorAll('span')) {
                    if (s.textContent?.trim() === 'Cinema 2.0') {
                        b.click();
                        return true;
                    }
                }
            }
            return false;
        }""")

        if switched:
            await self.h.pause(3, 4)
            # Verify by checking toolbar for Cinema 2.0 label
            model = await self.page.evaluate("""() => {
                for (const b of document.querySelectorAll('button')) {
                    const img = b.querySelector('img[alt*="Cinema"]');
                    if (img && b.getBoundingClientRect().y > 950) return img.alt;
                }
                return null;
            }""")
            if model and '2.0' in model:
                print(f"[nav] Confirmed: {model} active")
                return True
            print(f"[nav] Cinema 2.0 clicked but toolbar shows: {model}")
            return True  # Click succeeded even if verification is ambiguous
        else:
            print("[nav] Cinema 2.0 button not found in Scenes panel")
            await self.ss("cinema2_not_found")
            return False

    # ── Cinema Studio 2.0 generation flow ──────────────────────────────
    async def open_scenes_panel(self):
        """Open the Scenes panel at the bottom of Cinema Studio."""
        scenes_btn = await self.page.evaluate("""() => {
            const btns = document.querySelectorAll('button, span');
            for (const b of btns) {
                if (b.textContent?.trim() === 'Scenes') {
                    const r = b.getBoundingClientRect();
                    if (r.y > 900) return {x: r.x + r.width/2, y: r.y + r.height/2};
                }
            }
            return null;
        }""")
        if scenes_btn:
            await self.h.click_at(self.page, scenes_btn["x"], scenes_btn["y"])
            await self.h.pause(1, 2)
            print("[ui] Scenes panel opened")

    async def set_video_mode(self):
        """Switch from Image to Video mode in the bottom bar."""
        vid_btn = await self.page.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                if (b.textContent?.trim() === 'Video') {
                    const r = b.getBoundingClientRect();
                    if (r.y > 900) return {x: r.x + r.width/2, y: r.y + r.height/2};
                }
            }
            return null;
        }""")
        if vid_btn:
            await self.h.click_at(self.page, vid_btn["x"], vid_btn["y"])
            await self.h.pause(1, 2)
            print("[ui] Video mode selected")

    async def type_prompt(self, prompt):
        """Type a scene prompt into the prompt input area."""
        # The prompt area is a contentEditable div or textarea near the bottom
        prompt_el = await self.page.evaluate("""() => {
            // Try contentEditable div first
            const ce = document.querySelectorAll('[contenteditable=true]');
            for (const el of ce) {
                const r = el.getBoundingClientRect();
                if (r.width > 300 && r.y > 800) return {x: r.x + 20, y: r.y + r.height/2};
            }
            // Try button with "Describe your scene" text
            const btns = document.querySelectorAll('button, div');
            for (const b of btns) {
                if (b.textContent?.includes('Describe your scene')) {
                    const r = b.getBoundingClientRect();
                    if (r.width > 200) return {x: r.x + r.width/2, y: r.y + r.height/2};
                }
            }
            return null;
        }""")

        if prompt_el:
            await self.h.click_at(self.page, prompt_el["x"], prompt_el["y"])
            await self.h.pause(0.3, 0.6)
            for ch in prompt:
                await self.page.keyboard.type(ch, delay=random.randint(20, 60))
            await self.h.pause(0.5, 1)
            print(f"[gen] Prompt typed ({len(prompt)} chars)")
        else:
            print("[gen] Prompt area not found")

    async def click_generate(self):
        """Click the GENERATE button and return the credit cost shown."""
        gen = await self.page.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                if (b.textContent?.includes('GENERATE')) {
                    const r = b.getBoundingClientRect();
                    return {
                        x: r.x + r.width/2, y: r.y + r.height/2,
                        text: b.textContent.trim()
                    };
                }
            }
            return null;
        }""")

        if gen:
            # Extract credit cost from button text (e.g. "GENERATE8" → 8)
            cost = ''.join(c for c in gen["text"] if c.isdigit()) or "?"
            print(f"[gen] Clicking GENERATE ({cost} credits)...")
            await self.h.click_at(self.page, gen["x"], gen["y"])
            await self.h.pause(2, 4)
            return int(cost) if cost.isdigit() else 0
        else:
            print("[gen] GENERATE button not found")
            return 0

    async def wait_for_result(self, timeout_s=300):
        """Poll until a video/image result appears. NOTE: For video generation,
        prefer AIMLAPI API over this browser-based polling — it's more reliable.
        This method is primarily for hero frame image generation results."""
        print(f"[gen] Waiting for result (max {timeout_s}s)...")
        for i in range(timeout_s // 5):
            await asyncio.sleep(5)
            elapsed = (i + 1) * 5

            result = await self.page.evaluate("""() => {
                // Look for result video/image elements with CDN URLs
                const vids = document.querySelectorAll('video source, video');
                for (const v of vids) {
                    const src = v.src || v.getAttribute('src') || '';
                    if (src.includes('cloud-cdn.higgsfield') || src.includes('cloudfront')) {
                        return {type: 'video', url: src};
                    }
                }
                const imgs = document.querySelectorAll('img');
                for (const img of imgs) {
                    const src = img.src || '';
                    if ((src.includes('cloud-cdn.higgsfield') || src.includes('cloudfront'))
                        && img.getBoundingClientRect().width > 200) {
                        return {type: 'image', url: src};
                    }
                }
                return null;
            }""")

            if result and result["url"]:
                print(f"[gen] Result found after {elapsed}s: {result['type']}")
                await self.ss("generation_complete")
                return result

            if elapsed % 30 == 0:
                await self.ss(f"gen_poll_{elapsed}")
                print(f"[gen] Still generating... ({elapsed}s)")

        print("[gen] Timeout — no result found")
        await self.ss("gen_timeout")
        return None


# ── Test run ───────────────────────────────────────────────────────────
async def main():
    os.environ["DISPLAY"] = ":99"

    async with HiggsfieldBrowser() as hf:
        # Step 1: Login
        logged_in = await hf.ensure_logged_in()
        if not logged_in:
            print("FAILED: Could not log in")
            return

        # Step 2: Open Cinema Studio
        await hf.open_cinema_studio()

        # Step 3: Open Scenes panel
        await hf.open_scenes_panel()
        await hf.ss("test_scenes_open")

        # Step 4: Check if Cinema 2.0 switching is available
        switched = await hf.switch_to_cinema_2()
        await hf.ss("test_after_switch")

        # Step 5: Set Video mode and type prompt
        await hf.set_video_mode()
        await hf.type_prompt(
            "A white moving truck parked on a quiet Dutch suburban street, "
            "golden hour sunlight, cinematic wide shot, brick rowhouses, "
            "tree-lined street, natural wear on surfaces"
        )
        await hf.ss("test_prompt_ready")

        # Report
        gen_text = await hf.page.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                if (b.textContent?.includes('GENERATE')) return b.textContent.trim();
            }
            return 'NOT FOUND';
        }""")
        print(f"\n=== Test complete ===")
        print(f"Generate button: {gen_text}")
        print("Screenshots in /opt/pipeline/qa/")


if __name__ == "__main__":
    asyncio.run(main())
