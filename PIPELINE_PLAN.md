# Autonomous Cinematic Video Ad Pipeline for a Moving Company

**Stack: Claude Code (orchestrator + vision QA) · Higgsfield Ultra 6,000 credits/mo · VPS · FFmpeg · ElevenLabs**
**New monthly cost: ~$47 | Existing subscriptions leveraged: Higgsfield Ultra (yearly) + Claude Max**
**Content standard: All output adheres to Islamic Shari'ah guidelines of Ahlus Sunnah wal Jama'ah**

---

## Why Claude Code — Not OpenClaw

OpenClaw has accumulated 138+ CVEs in under 90 days, including a CVSS 9.9 remote code execution flaw that exposed 135,000 instances globally. Cisco found that 12% of its skill marketplace performed data exfiltration. Running it on a VPS holding your brand assets, API keys, and client footage would be irresponsible.

Claude Code runs headlessly on a VPS via its SDK (`claude -p "prompt" --output-format json`). It executes shell commands, manages files, calls external APIs, drives headless browsers via Playwright for web automation, and — critically — processes images natively through Claude's vision capabilities. Your Max subscription covers all orchestration and vision QA usage with no additional API costs. It has built-in permission scoping (`--allowedTools`) and spend caps (`--max-budget-usd`) that OpenClaw lacks entirely. Claude Code is your orchestrator, your browser operator, your QA director, and your creative intelligence in one tool.

---

## 24/7 Communication & Endless Memory

OpenClaw's two killer features were always-on messaging and persistent memory across sessions. Claude Code now matches both — using the same memory system OpenClaw used, without any of the security exposure.

### Always-On Messaging via Channels

Claude Code Channels connects your VPS-based agent to messaging platforms — Telegram, Discord, Slack, or WhatsApp. The agent runs as a persistent daemon on your VPS. You message it from your phone at any hour: "generate 5 new ads for the Riyadh relocation campaign" or "the last batch felt too cold, warm up the lighting for future runs." It receives the message, executes the full pipeline, and replies when work is complete — or asks for clarification if the brief is ambiguous.

This is not a chatbot. It's your production agent with full access to the VPS filesystem, Higgsfield via browser automation, FFmpeg, the asset vault, and the QA pipeline. Everything it can do in a headless script, it can do when triggered by a Telegram message. You review final videos as attachments in the chat, approve or reject with a reply, and that feedback flows directly into the learning loop.

For the video pipeline specifically, the interaction pattern looks like this: you send a concept → the agent confirms it passes Shari'ah compliance → expands it into a shot list and sends it back for your approval → you approve → it runs generation, QA, post-production overnight → sends you the finished videos in the morning. All from your phone.

### Three-Layer Persistent Memory

Every Claude Code session starts with a fresh context window. Three mechanisms ensure nothing is ever lost:

**Layer 1 — CLAUDE.md (your rules, always loaded).** This is a markdown file on your VPS that Claude Code reads at the start of every session. It contains your non-negotiable instructions: the Shari'ah compliance guidelines, your brand bible (colors, logo specs, tone of voice), credit allocation strategy, QA scoring rubric, and operational rules ("never use Sora 2 for close-up hand shots"). You edit this file manually when your rules change. It fully survives session restarts and context compaction — Claude re-reads it from disk every time.

**Layer 2 — Auto Memory (Claude's own notes).** Claude Code's built-in auto memory lets it accumulate knowledge across sessions without you writing anything. It decides what's worth remembering: which prompt patterns produce the highest QA pass rates, which camera settings work best for your truck shots, your feedback tendencies, debugging insights from failed generations. These are saved as plain markdown files in `~/.claude/projects/<project>/memory/` — fully human-readable and editable. You can browse them anytime with the `/memory` command.

**Layer 3 — Hindsight (semantic conversational memory).** This is the same memory system that powered OpenClaw agents, now available as a Claude Code plugin. It works automatically: before every prompt, it queries the memory bank for relevant past conversations and injects them as invisible context. After every response, it extracts facts and retains them for long-term storage. Six months from now, when you message the agent "remember that golden hour look we nailed for the Dubai campaign?", it retrieves the exact generation parameters, prompt text, and model settings from that session — even though hundreds of conversations have happened since.

Installation:
```
claude plugin marketplace add vectorize-io/hindsight
claude plugin install hindsight-memory
```

Hindsight runs locally on your VPS using a lightweight embedding daemon. Memory banks are isolated per project, so your video pipeline memories stay separate from any other Claude Code work. Zero cloud dependency — all data stays on your machine.

**How the three layers work together for the video pipeline:**

CLAUDE.md holds the rules that never change (or change rarely): Shari'ah guidelines, brand specs, QA thresholds. Auto Memory holds the operational intelligence that evolves: model performance data, prompt success patterns, your aesthetic preferences. Hindsight holds the full conversational history: every brief you submitted, every piece of feedback you gave, every creative direction conversation. Together, they mean the agent on day 180 is profoundly more capable than the agent on day 1 — and nothing is ever forgotten or lost between sessions.

---

## Shari'ah Compliance as a Design Principle

This is not a post-production filter. Shari'ah adherence is embedded in the system prompt that governs every phase of the pipeline. Claude Code carries a persistent compliance document (`/config/shariah-guidelines.json`) loaded into every generation and QA call. The guidelines enforce:

**No music or musical instruments.** Audio is restricted to voiceover narration, natural ambient sound effects (truck engines, doors, footsteps, birdsong, street ambience), and vocal nasheeds without instruments where appropriate. Epidemic Sound and all music libraries are excluded from the stack entirely.

**Modest appearance in all depicted people.** Men in appropriate clothing (no shorts above the knee, covered 'awrah). Women, if depicted, in full hijab with loose-fitting garments. The system prompt explicitly instructs generation models to render modest dress and instructs QA to reject any frame where clothing does not meet these standards.

**No free-mixing scenarios.** Scenes are designed to avoid inappropriate gender interactions. Family scenes depict mahram relationships naturally. Crew scenes show male workers in professional contexts.

**No deceptive or exaggerated advertising.** The Prophet ﷺ prohibited deception in trade. Generated ads must show realistic service depictions — no impossible promises, no misleading before/after scenarios, no exaggeration of capabilities.

**No haram imagery.** No depictions of impermissible items, symbols, or environments. The QA layer actively scans for unintended background elements that AI models sometimes hallucinate (bottles, statues, inappropriate signage, etc.) and rejects those frames.

**Overall tone of dignity and trustworthiness.** The brand voice reflects amānah (trustworthiness) and iḥsān (excellence). Content should inspire confidence through professionalism and sincerity, not through sensationalism or manipulation.

These rules are non-negotiable at every pipeline stage. Claude's world knowledge includes understanding of these principles, making it uniquely capable of enforcing them during QA — it can identify a background element that shouldn't be there, flag clothing that doesn't meet the standard, or catch an AI-hallucinated object that would be inappropriate.

---

## The Seven-Phase Pipeline

### Phase 1 — Brief Intake
You drop a concept into a `/briefs/` folder as a simple text or JSON file. Examples: "emotional ad: family arrives at new home, golden hour, 30 seconds" or "viral comedy: couch won't fit through door, slapstick energy, 15 seconds." Claude Code parses the brief, validates it against the Shari'ah compliance guidelines, and expands it into a structured shot list with scene descriptions, camera specs, emotional tone, and target duration per clip. Any concept element that conflicts with the guidelines is flagged before a single credit is spent. This expansion draws from your learned preferences database (see Phase 7).

### Phase 2 — Asset Matching & Prompt Engineering
Claude Code checks your `/assets/` vault for matching reference photos: truck angles, crew in uniform, specific locations, logo files. For shots based on real subjects (your actual truck, your actual crew), it builds image-to-video prompts anchored to those references. For conceptual shots (the comedy scenario, the emotional wide), it writes text-to-video prompts using patterns from your success history.

Before any generation, Claude Code validates every prompt against the learned knowledge base: "This prompt structure has a 91% first-pass rate on Kling 3.0 with slow dolly push-in" vs. "Avoid Sora 2 for close-up hand interactions — 62% failure rate on finger coherence." This is where credit savings compound over time.

### Phase 3 — Generation via Higgsfield Ultra (API-First with Browser Fallback)
Your 6,000 monthly credits are the generation budget. Claude Code uses a **dual approach** to drive Higgsfield, choosing the most reliable method for each generation task.

**Primary method — Higgsfield Cloud API (cloud.higgsfield.ai).** Higgsfield provides a Cloud API with an official Python SDK (`higgsfield-ai/higgsfield-client`). API credits draw from your existing subscription pool — there is no separate billing. The API supports text-to-image, image-to-video, async generation with webhook/polling completion, and model selection. Community MCP servers (`geopopos/higgsfield_ai_mcp`, `jfikrat/higgsfield-mcp`) wrap this API for direct integration with Claude Code. The API path is faster, more reliable, and immune to UI changes or bot protection.

**Fallback method — Playwright browser automation.** For features only available through the web UI (Cinema Studio's full camera body/lens/focal length controls, certain Hero Frame workflows, new features not yet in the API), Claude Code falls back to Playwright driving the Higgsfield website. Higgsfield uses **DataDome bot protection**, which detects stock headless browsers. The Playwright fallback uses `--browser-channel=chrome` (system Chrome, not Chromium), `--vision` mode (screenshot-based interaction rather than DOM traversal), and human-like interaction patterns (typing delays, mouse movements, realistic timing). If DataDome blocks a session, Claude Code switches back to the API path or flags for manual intervention.

**How it works:** For API generations, Claude Code calls the Higgsfield SDK directly — submit prompt, model, parameters, poll for completion, download result. For browser-based generations, it launches a headless browser session, logs into your Higgsfield account (credentials in environment variables), navigates to the tool, configures settings, submits, and downloads. In both cases, if something unexpected occurs (credit warning, model unavailable, rate limit), Claude Code adapts — retries, switches models, or flags for your attention via Telegram.

**This gives you full access to every Ultra feature** through the combination of API and browser paths. For 50 videos/month (~400 total generations including QA stills), the automation runs ~15–20 hours unattended overnight on the VPS.

**Credit allocation strategy:**

- **80% of shots → Kling 3.0 (~6 credits/clip):** Establishing shots, truck footage, interiors, B-roll. Reliable, cost-efficient, strong motion coherence.
- **15% of shots → Cinema Studio with reference anchoring:** Hero shots requiring precise camera control. Lock a static Hero Frame from your real photo first (image generation is free/cheap on Ultra's unlimited image models), then animate from that locked reference.
- **5% of shots → Veo 3.1 or premium models (40–70 credits/clip):** Only for the money shot — the emotional climax, the reveal, the CTA moment. Never used without a passed static frame first.

**Static-first validation:** Before spending 40–70 credits on a premium video clip, generate a still frame using one of Ultra's unlimited image models (Flux.2 Pro, Seedream, Nano Banana). Run it through QA. If the still fails, you've spent zero video credits. Only passed stills proceed to video generation.

**Credit math for 50 videos:** Each 30–60 second video needs 4–6 clips. With the static-first funnel and learned prompts reducing iteration to ~1.3× average: ~300 clips × 1.3 × ~8 avg credits = **~3,120 credits/month.** That's roughly half your 6,000 allocation — leaving a generous buffer for experimentation, premium model hero shots, and re-generations.

**Month 1 caveat:** The 1.3× iteration factor assumes learned prompt patterns and a tuned QA pipeline. In month 1, before the learning loop has data, expect ~2× iteration instead: ~300 × 2 × ~8 = ~4,800 credits. Still within the 6,000 budget, but plan for 30–35 videos in the first month rather than 50 while the system calibrates. By month 2–3, iteration rates should reach the 1.3× steady state.

### Phase 4 — Intelligent Visual QA (The Core Innovation)

This is where the system fundamentally differs from any pixel-checking tool. Claude's vision doesn't just detect artifacts — it *reasons about reality*. When it looks at a generated frame of your crew carrying a dresser through a doorway, it simultaneously evaluates:

**Real-world physics & anatomy:** Is the dresser proportioned correctly relative to the doorway? Are the movers' arms at angles that could actually support that weight? Does the strain in their posture match the apparent heaviness of the object? Are there the correct number of fingers, gripping in a way that makes biomechanical sense?

**Brand & object accuracy:** Does the truck match your reference photo — same color, same logo placement, same proportions? Is the crew wearing the correct uniform? Does the neighborhood look residential and not industrial? Is the dolly the right type for the object being moved?

**Cinematic coherence:** Does the lighting direction stay consistent between the subject and the environment? Are shadows falling the correct way? Does the depth of field match the specified lens? Is the color temperature consistent with the time of day in the brief?

**AI slop detection:** This is what no OpenCV pipeline can do. Claude recognizes the *texture* of AI-generated content — the too-smooth skin, the plastic-looking hair, the subtly wrong reflections, the uncanny symmetry in faces, the way AI renders fabric folds differently from real cloth. It knows what real moving blankets look like vs. AI's interpretation. It knows that real cardboard boxes have tape, labels, and wear marks. It catches the things a human creative director would catch.

**Implementation:** Claude Code extracts every 4th frame from each clip using FFmpeg (`ffmpeg -i clip.mp4 -vf "select=not(mod(n\,4))" -vsync vfn frame_%03d.jpg`). It sends batches of frames to Claude's vision API with a structured rubric:

```
Score each dimension 1-10. Return JSON.
{
  "hand_anatomy": score,
  "face_consistency_vs_reference": score,
  "physics_plausibility": score,
  "brand_accuracy": score,
  "lighting_coherence": score,
  "ai_artifact_severity": score,  // 10 = undetectable, 1 = obvious AI
  "shariah_compliance": score,    // checks dress code, background elements, overall appropriateness
  "overall_realism": score,
  "failure_codes": ["HAND_ERROR", "FACE_DRIFT", "DRESS_CODE_VIOLATION", "HARAM_BACKGROUND_ELEMENT", etc.],
  "improvement_suggestions": "specific prompt adjustments"
}
```

Clips scoring below threshold on any dimension are auto-rejected. **Shari'ah compliance is a hard gate — any score below 10 triggers immediate rejection with no override.** Failure codes like `DRESS_CODE_VIOLATION` or `HARAM_BACKGROUND_ELEMENT` prompt the agent to add explicit corrective language to the regeneration prompt (e.g., "all men wearing long trousers and modest work uniforms," "no bottles, statues, or inappropriate signage visible in background"). The `improvement_suggestions` field feeds directly back into prompt revision — Claude doesn't just flag the problem, it tells the system *how to fix it* for the next generation attempt.

**Regeneration limits:** Each clip gets a maximum of **3 regeneration attempts** for any single failure category. Each retry adds progressively stronger corrective language to the prompt. If a clip fails the same category 3 times, it is **escalated to the owner via Telegram** with: (a) the specific frames that failed, (b) the failure codes, (c) the corrective prompts that were tried, and (d) a recommendation — either a different shot concept, a different model, or manual approval if the violation is borderline. This prevents credit-burning loops on shots that the current models cannot render compliantly.

**Your Max subscription covers all of this.** No per-call API charges for vision processing. The only compute cost is FFmpeg frame extraction on your VPS — negligible.

### Phase 5 — Post-Production Assembly

Two tools handle post-production: **FFmpeg** for video/audio processing, and **Remotion** for cinematic motion graphics (captions, title cards, transitions). Claude Code orchestrates both, running them sequentially (never simultaneously — see resource management below).

**FFmpeg processing** (called by Claude Code):

- **Clip stitching** with crossfade transitions (`xfade` filter, 0.5s dissolves between scenes)
- **Logo overlay** at a fixed position using your PNG logo with alpha channel (`overlay=W-w-20:H-h-20`). The logo is composited in post, never generated by AI — this eliminates the #1 source of text distortion in AI video.
- **Color grading** via a brand `.cube` LUT file applied uniformly (`lut3d=file=brand.cube`). One consistent look across all 50 videos.
- **Voiceover** from ElevenLabs ($22/mo Creator plan, ~100 minutes included). Claude Code generates the script from the brief, calls the ElevenLabs API, receives the audio file, and mixes it in. Voice cloning available if you want a consistent brand narrator. ElevenLabs returns **word-level timestamps** with the audio — these are preserved for caption synchronization.
- **Ambient sound design** using Freesound API (CC-licensed, free). Natural SFX layered for realism: truck engine idling, doors opening, footsteps on pavement, birdsong, neighborhood ambience, tape pulling, furniture settling. No music or musical instruments — ever. Where emotional emphasis is needed, the voiceover cadence and ambient sound design carry the tone.

**Remotion cinematic captions and motion graphics:**

- **Word-by-word animated captions** synced to voiceover timing. The data flow: ElevenLabs word-level timestamps → parsed into frame-number arrays → passed as props to Remotion `<Composition>` components → rendered to transparent overlay video → composited onto the main video via FFmpeg. Captions use cinematic typography (see `captions-and-titles.md` skill), positioned in platform-specific safe zones.
- **Title cards** for opening and closing — branded, animated, consistent across all 50 videos.
- **Lower-third overlays** for CTA text, phone numbers, service descriptions.
- **Transition overlays** where FFmpeg crossfades are insufficient — light leaks, cinematic wipes, match-cut animations.

Remotion compositions live in `/opt/pipeline/captions/` as a React/TypeScript project. Claude Code generates composition code per video, renders via `npx remotion render`, and composites the result with the FFmpeg assembly.

- **Platform formatting:** One master render, then FFmpeg crops/scales to 9:16 (Reels/TikTok), 1:1 (Feed), and 16:9 (YouTube) automatically.

**Resource management:** Remotion rendering is CPU-intensive. Never run Remotion and FFmpeg encoding simultaneously. The pipeline processes sequentially: FFmpeg clip stitching → Remotion caption render → FFmpeg final composite with captions, logo, audio, and color grading → platform format exports.

### Phase 6 — Final Brand Compliance Pass

The assembled video gets one last Claude vision review. Not frame-by-frame this time — sampled frames from the final render checked against the original brief:

- Logo visible and correctly placed in every required frame
- Color palette matches brand guidelines
- No QA issues introduced during compositing
- Tone and pacing match the brief's intent
- CTA text (composited, not AI-generated) is legible and correctly spelled
- Full Shari'ah compliance confirmed: modest dress maintained throughout, no impermissible background elements, no music in audio track, overall tone reflects amānah and professionalism

Pass → moved to `/output/final/` for your approval. Fail → specific failure report generated, auto-fix attempted or flagged for your review.

### Phase 7 — Learning Loop (How the System Gets Smarter)

A SQLite database (`pipeline.db`) on your VPS stores the full lineage of every generation:

**`generation_history`** — prompt text, model used, camera settings, reference images used, QA scores per dimension, pass/fail, specific failure codes, improvement suggestions applied, final approval status.

**`learned_preferences`** — aggregated patterns: "Kling 3.0 + 35mm + slow push-in has 94% pass rate for exterior truck shots." "Veo 3.1 fails on hand coherence 38% of the time in close-ups." "Adding 'natural wear and texture' to furniture prompts increases realism score by 1.8 points average."

**Your qualitative feedback** — when you approve or reject a final video, Claude Code logs your notes. "Too corporate" adjusts future prompt tone toward warmer, more candid compositions. "Loved the lighting" reinforces those specific generation parameters.

Claude Code runs periodic SQLite queries on this data, surfacing the patterns it consults before every new generation. After 20–30 completed projects, the system has a custom playbook that no generic tool could match.

---

## Monthly Cost Breakdown

| Component | Tool | Cost |
|---|---|---|
| Video generation (6,000 credits) | Higgsfield Ultra (existing yearly sub) | **$0** |
| Orchestration + Vision QA | Claude Max (existing sub) | **$0** |
| VPS (4+ vCPU, 16+ GB RAM, 200+ GB SSD) | Hetzner or equivalent | **~$25–35** |
| Browser automation + API | Playwright + Higgsfield SDK (open source) | **$0** |
| 24/7 messaging | Claude Code Channels → Telegram (open source) | **$0** |
| Persistent memory | Hindsight plugin + auto memory (open source, local) | **$0** |
| Voiceover (~25 min/mo) | ElevenLabs Creator | **$22** |
| Ambient SFX library | Freesound API (CC-licensed) | **$0** |
| Post-production | FFmpeg + Python (open source) | **$0** |
| Database & analytics | SQLite (open source) | **$0** |
| **Total new monthly spend** | | **$47** |

The $453 remaining under your $500 ceiling is pure buffer — available for Higgsfield credit top-ups during heavy months, ElevenLabs overages, or a VPS upgrade if you want to run InsightFace locally for faster face-matching QA.

---

## Publishing (When Ready)

When you move to distribution, Claude Code can call the Meta Graph API (Instagram + Facebook) and TikTok Content Posting API to upload directly from the VPS. It generates captions from the brief, applies hashtags from a stored strategy document, and schedules posts using optimal timing data. No additional tools needed — just API credentials. Budget impact: $0 (these APIs are free to use). The entire publish flow is triggerable from Telegram: "publish the Jeddah campaign batch to Instagram and TikTok" — and the agent handles formatting, captions, and upload.
