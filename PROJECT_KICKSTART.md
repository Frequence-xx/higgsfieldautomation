# PROJECT KICKSTART: Autonomous Cinematic Video Ad Pipeline

## Background & Conversation Summary

This project emerged from a deep exploration of how to fully automate the production of cinematic video ads for a Muslim-owned moving company using AI. The conversation spanned 15+ exchanges and evolved through several key realizations:

**The core idea:** Build an autonomous system that takes a simple concept ("emotional ad: family arrives at dream home, golden hour, 30 seconds") and produces a finished, branded, Shari'ah-compliant cinematic video ad — with zero manual editing.

**The stack crystallized through iteration:** We started by exploring Higgsfield AI's Cinema Studio as the generation engine, with its real optical physics simulation, multi-model access (Kling 3.0, Veo 3.1, Cinema Studio), and reference-anchored workflows. We then evaluated orchestration options — OpenClaw was disqualified due to 138+ CVEs and catastrophic security exposure, and Claude Code emerged as the clear winner for its headless VPS operation, vision capabilities, permission scoping, and the owner's existing Max subscription.

**Key design decisions made during the conversation:**

1. **Browser automation over API** — Higgsfield's Cloud API has sparse documentation and unclear billing relationship with subscription credits. Playwright driving the actual Higgsfield website guarantees the owner's existing Ultra plan credits (6,000/month) are used directly.

2. **Claude as intelligent QA, not just pixel-checker** — Claude's vision API combined with its real-world knowledge creates a QA system that reasons about physics, anatomy, brand accuracy, and "AI slop" the way a human creative director would. It knows what moving trucks look like, what proper lifting posture is, what real cardboard boxes look like vs. AI-smooth fakes.

3. **Shari'ah compliance as a foundational design principle** — Not a post-production filter. Embedded at every pipeline stage: no music (voiceover + ambient SFX only), modest dress standards, no free-mixing, no haram background elements, no deceptive advertising, tone of amānah and iḥsān. Hard gate in QA — any compliance violation is an instant reject.

4. **Three-layer persistent memory** — CLAUDE.md for permanent rules, auto memory for learned operational intelligence, and Hindsight/claude-mem for full semantic conversational history. The system on day 180 is profoundly more capable than day 1.

5. **24/7 communication via Telegram** — Claude Code Channels connects the VPS agent to Telegram. The owner sends concepts from their phone, approves/rejects deliverables in chat, and provides feedback that flows into the learning loop.

6. **Credit efficiency architecture** — Static-first validation (generate free stills before committing video credits), learned prompt patterns, model-appropriate routing (Kling 3.0 for 80% of shots, premium models only for hero shots). Target: ~3,120 credits/month for 50 videos, half the 6,000 allocation.

**Monthly cost: ~$47 in new spending** (VPS $25 + ElevenLabs $22), with Higgsfield Ultra and Claude Max already subscribed.

---

## Critical Plugin Assessment

The plugin research surfaced 25+ tools. Installing all of them would create dependency conflicts, bloated context windows, slower startup times, and maintenance overhead that defeats the purpose of an autonomous system. Here is the honest assessment:

### ESSENTIAL (Install these — the pipeline doesn't work without them)

| Plugin | Why it's essential |
|---|---|
| **Playwright MCP** | Core interface to Higgsfield. Without it, no video generation. |
| **Hindsight Memory** | Persistent conversational memory across sessions. The learning loop depends on this. |
| **Telegram Channel** | 24/7 communication. Owner sends concepts and approves deliverables from phone. |
| **SQLite MCP** | Structured database for generation history, QA scores, learned preferences. |
| **ElevenLabs MCP** | Voiceover generation. Called directly by the agent during post-production. |
| **Superpowers** | Plan-before-execute discipline. Prevents the agent from burning credits on poorly structured prompts. |
| **Security Guidance** | Non-negotiable when running `--dangerously-skip-permissions` with API keys on a VPS. |
| **Remotion Superpowers** | Cinematic captions, professional transitions, title cards, and motion graphics. FFmpeg alone cannot produce blockbuster-tier animated text and transitions. Includes AI review loop and TikTok-style word-by-word captions. |

### RECOMMENDED (Install after core is stable — meaningful quality improvements)

| Plugin | Why it helps |
|---|---|
| **FFmpeg MCP** | Natural language FFmpeg control. Not strictly required (Claude can write FFmpeg commands via bash), but reduces errors in complex filter chains. |
| **Prompt Architect** | Optimizes Higgsfield prompts using research-backed frameworks. Worth testing after 2-3 weeks of baseline data. |
| **ccusage** | Cost tracking. Add to cron after launch to monitor credit burn rate. |

### SKIP (Don't install — adds complexity without proportional value for THIS project)

| Plugin | Why to skip |
|---|---|
| **gstack** | Designed for software engineering teams. The CEO/Engineering Manager/Release Manager roles don't map to video production. Its QA browser testing is redundant with Playwright MCP. |
| **claude-mem** | Redundant if using Hindsight. Pick ONE memory system. Running two causes context bloat and potential conflicts. |
| **MemPalace / memsearch** | Same reason. One memory system is enough. |
| **Frontend Design** | No web dashboard needed at launch. Add later if building a review portal. |
| **Code Review (5 agents)** | For software development PR reviews, not video production QA. |
| **QA Skills** | For software testing (smoke tests, UX audits). Our QA is vision-based, handled by Claude natively. |
| **Vision MCP (Z.AI)** | Claude's built-in vision capabilities handle all our QA needs. Adding another vision service is redundant and adds API cost. |
| **Kie.ai MCP** | We're using Higgsfield as our single generation platform. Adding 15 more models creates decision paralysis and inconsistent output. |
| **claude-workflow** | Over-engineering. Claude Code + Superpowers + a well-written CLAUDE.md handles our workflow. |
| **Agent Teams** | Experimental feature. Adds coordination overhead. A single agent with Superpowers' subagent delegation is simpler and more reliable. |
| **Higgsfield MCP servers** | The Higgsfield Cloud API is now the primary generation method (see PIPELINE_PLAN.md Phase 3). The community MCP servers (geopopos/higgsfield_ai_mcp) are a viable option if direct SDK integration proves insufficient. Evaluate after initial API testing in Phase 0. |
| **Filesystem MCP** | Redundant. Claude Code has built-in Read, Write, Edit, Bash, Glob, Grep tools. |
| **Fetch MCP** | Redundant. Claude Code can use curl via bash. Only needed if you're building MCP-only workflows. |

### SKILLS TO INCLUDE (lightweight, no overhead)

Skills are just markdown instruction files — they add zero performance overhead and load only when relevant. Include these in your `.claude/skills/` directory:

- **FFmpeg CLI skill** — Best practices for video processing commands
- **Remotion skill** — Correct Remotion patterns for cinematic compositions, captions, and transitions
- **Custom: Shari'ah Compliance skill** — Your specific guidelines as a skill file so Claude auto-invokes during QA
- **Custom: Higgsfield Navigation skill** — Step-by-step instructions for navigating Higgsfield's UI via Playwright
- **Custom: Brand Identity skill** — Your truck colors, logo specs, uniform details, approved shot compositions
- **Custom: Video QA Rubric skill** — The scoring dimensions, thresholds, and failure codes
- **Custom: Cinematic Standards skill** — Reference cinematography language: lens choices, camera movements, color grading LUTs, transition styles, and caption typography that match blockbuster production quality (Transformers/Avengers/Superman tier)

These custom skills are the most valuable part of the system — they encode YOUR specific knowledge into reusable instructions that Claude follows consistently.

---

## The Kickstart Prompt

Copy the prompt below and run it in your Claude Code session on the VPS. It assumes `PIPELINE_PLAN.md` and `PROJECT_PLUGINS.md` are in your project directory.

```
You are the autonomous orchestrator for a cinematic AI video ad production pipeline for a Muslim-owned moving company. Your two reference documents are:

- PIPELINE_PLAN.md — the full seven-phase production architecture
- PROJECT_PLUGINS.md — the complete plugin ecosystem research

Read both documents now before proceeding.

Your mission is to set up this VPS as a fully autonomous video ad production system. Here is what is already in place:
- Claude Code running on this VPS with a Max subscription
- Higgsfield Ultra yearly plan (6,000 credits/month)
- ElevenLabs Creator account ($22/mo)

PHASE 0 — INITIALIZE AND VERIFY FOUNDATIONS

Step 1: Initialize git repository. This is structurally required — Claude Code's auto memory, Hindsight's memory banks, and Superpowers' worktree isolation all scope by git repo.

cd /opt/pipeline
git init
git add -A
git commit -m "Initial pipeline structure"

All pipeline code, skills, config, and CLAUDE.md will be version controlled from this point forward. Every significant change gets committed. If something breaks during an overnight batch, we can git revert.

Step 2: Verify Higgsfield API access. The pipeline uses the Higgsfield Cloud API as the primary generation method, with Playwright browser automation as a fallback for UI-only features. Before proceeding, test that the API works with the subscription credits:

pip install higgsfield-client
python3 -c "
from higgsfield import HiggsClient
client = HiggsClient(api_key='$HIGGSFIELD_API_KEY', api_secret='$HIGGSFIELD_API_SECRET')
# Attempt a minimal API call (e.g., list available models or generate a test image)
print(client.models.list())
"

If the API test succeeds: the primary generation path is confirmed. Continue.
If the API test fails: check credentials at cloud.higgsfield.ai. If the API is not available for your plan tier, the pipeline will rely on Playwright browser automation with stealth measures — still viable but less reliable.

Step 3: Verify prerequisites. Run these checks and fix any failures before proceeding:
- uvx --version (required for ElevenLabs MCP — if missing: curl -LsSf https://astral.sh/uv/install.sh | sh)
- npx playwright --version (required for browser fallback)
- ffmpeg -version (required for post-production)
- node --version (must be v20+)

PHASE 1 — INSTALL ESSENTIAL PLUGINS

Install the following plugins. For each one: attempt installation, verify it works, and log the result. If a plugin fails to install, note the error, attempt the alternative installation method listed, and continue with the remaining plugins. Do not let one failed plugin block the entire setup.

1. Playwright MCP — browser automation for Higgsfield fallback
   Primary:   claude mcp add playwright -- npx @playwright/mcp@latest
   Verify:    Use the Playwright MCP to navigate to https://higgsfield.ai and take a screenshot

2. Hindsight Memory — persistent conversational memory across sessions
   Primary:   claude plugin marketplace add vectorize-io/hindsight && claude plugin install hindsight-memory
   Fallback:  If Hindsight is unavailable, rely on Claude Code's built-in auto memory (Layer 2). The learning loop still works via SQLite + auto memory, just without semantic conversational recall.

3. Telegram Channel — 24/7 owner communication
   Configure: /telegram:configure (paste the bot token when prompted)
   Verify:    Send a test message to the owner's Telegram

4. SQLite MCP — pipeline database
   Primary:   claude mcp add sqlite -- npx -y @modelcontextprotocol/server-sqlite /opt/pipeline/data/pipeline.db
   Verify:    Create a test table and query it

5. ElevenLabs MCP — voiceover generation (requires uvx — see Phase 0 Step 3)
   Primary:   Add to MCP config: {"mcpServers": {"ElevenLabs": {"command": "uvx", "args": ["elevenlabs-mcp"], "env": {"ELEVENLABS_API_KEY": "$ELEVENLABS_API_KEY"}}}}
   Verify:    Generate a 5-second test voiceover

6. Superpowers — structured plan-before-execute workflow
   Primary:   /plugin install superpowers@claude-plugins-official
   Fallback:  /plugin marketplace add obra/superpowers-marketplace && /plugin install superpowers@superpowers-marketplace
   If both fail: proceed without it — Claude Code's built-in planning capabilities are sufficient

7. Security Guidance — security scanning for API key protection
   Primary:   /plugin install security-guidance@claude-plugins-official

8. Remotion Superpowers — cinematic captions, transitions, title cards, motion graphics
   Primary:   /plugin marketplace add DojoCodingLabs/remotion-superpowers && /plugin install remotion-superpowers@remotion-superpowers
   Fallback:  If unavailable, install base Remotion skills only (npx skills add remotion-dev/skills) — Claude Code can still generate Remotion compositions manually

Also install the Remotion base skills regardless:
npx skills add remotion-dev/skills

After all installations, report: which plugins installed successfully, which failed, and what fallback was used. Continue setup even if some optional plugins failed — the pipeline can operate with Playwright MCP + SQLite MCP + ElevenLabs MCP + Telegram as the minimum viable set.

Do NOT install gstack, claude-mem, MemPalace, memsearch, Frontend Design, Code Review, QA Skills, Vision MCP, Kie.ai, claude-workflow, Agent Teams, Filesystem MCP, or Fetch MCP. See PROJECT_PLUGINS.md for the full assessment.

PHASE 2 — CREATE PROJECT STRUCTURE AND INITIALIZE REMOTION

Step 1: Set up the following directory structure:
/opt/pipeline/
├── briefs/          # Input: concept briefs (JSON/text)
├── assets/          # Brand assets: truck photos, crew photos, logos, LUTs
├── config/          # shariah-guidelines.json, brand-identity.json, qa-rubric.json
├── generations/     # Raw Higgsfield output clips
├── qa/              # QA frame extractions and score logs
├── assembly/        # Post-production working directory
├── captions/        # Remotion caption project (React/TypeScript)
├── output/          # Final rendered videos ready for approval
├── data/            # SQLite database (pipeline.db)
├── logs/            # Execution logs, cost tracking
└── skills/          # Custom skill files

Step 2: Initialize Remotion project in /opt/pipeline/captions/. This is required for cinematic captions, title cards, and motion graphics:
cd /opt/pipeline/captions
npx create-video@latest --template blank
npm install

Create a base Remotion composition for word-by-word captions that accepts props:
- words: array of {text: string, startFrame: number, endFrame: number}
- style: object with fontFamily, fontSize, color, position, animation settings
- platformFormat: "9:16" | "1:1" | "16:9" (adjusts safe zones)

The composition renders to transparent video (ProRes 4444 or WebM with alpha) so it can be composited over the main video via FFmpeg. Test the setup by rendering a 3-second sample with placeholder text.

PHASE 3 — CREATE CUSTOM SKILLS

Write the following skill files in /opt/pipeline/skills/:

1. shariah-compliance.md — Encode the full Shari'ah guidelines from PIPELINE_PLAN.md as an auto-invokable skill. Include: no music rule, modest dress standards, no free-mixing, no haram imagery, no deceptive advertising, tone of amānah. This skill must trigger during brief validation AND visual QA.

2. higgsfield-generation.md — Two-path generation skill. PRIMARY: Higgsfield Cloud API via Python SDK (higgsfield-client) — submit prompt, model, parameters, poll for completion, download result. FALLBACK: Playwright browser automation for UI-only features (Cinema Studio camera controls, Hero Frame workflows). Include: model selection rules (Kling 3.0 default, Veo 3.1 for hero shots only), API error handling (rate limits, credit exhaustion, model unavailability), Playwright stealth configuration (--browser-channel=chrome, --vision mode, human-like interaction timing), DataDome detection recovery (switch to API if browser is blocked), and credit warning responses.

3. brand-identity.md — Placeholder skill that will be populated with actual brand assets (truck colors, logo placement rules, uniform specs, approved neighborhoods/locations). For now, create the structure with clear sections the owner will fill in.

4. video-qa-rubric.md — The full QA scoring system: hand_anatomy, face_consistency, physics_plausibility, brand_accuracy, lighting_coherence, ai_artifact_severity, shariah_compliance, overall_realism. Include the JSON output schema, threshold scores, failure codes, and the hard gate rule (shariah_compliance must score 10/10 or instant reject). CRITICAL: Include regeneration limits — maximum 3 retry attempts per clip per failure category. Each retry must add progressively stronger corrective language to the prompt. After 3 failures on the same category, escalate to owner via Telegram with: the specific frames that failed, the failure codes, the corrective prompts tried, and a recommendation (different shot concept, different model, or manual override request).

5. credit-efficiency.md — Rules for the static-first validation funnel: generate free stills before video, use Kling 3.0 for 80% of shots, reserve premium models for hero shots only, never generate without a passed static frame.

6. cinematic-standards.md — The non-negotiable quality bar: blockbuster production quality (Transformers, Avengers, Superman 2025 tier). This skill must define:

SHOT TYPE QUALITY MAP — which shots can achieve near-blockbuster quality and which require careful handling:
- STRONG: Wide establishing shots with camera movement (drone, dolly, crane) — AI excels here. Use these as your hero shots.
- STRONG: Exterior B-roll (trucks, streets, buildings, neighborhoods, sky) — highly achievable at cinematic quality.
- STRONG: Slow-motion captures and static compositions — AI handles these well.
- MODERATE: Medium shots of people in simple poses (standing, walking, carrying) — achievable with Kling 3.0 + careful prompting.
- DIFFICULT: Close-up hands performing precise actions (gripping furniture, turning keys, taping boxes) — high failure rate. Workaround: use medium shots that show the full person, not isolated hand close-ups. When hands must appear, use wider framing that de-emphasizes them.
- DIFFICULT: Facial expressions during dialogue or emotional beats — character consistency degrades. Workaround: use silhouettes, over-shoulder shots, or profile angles that reduce face detail requirements. Save direct face shots for the single best model (Veo 3.1).
- DIFFICULT: Complex multi-person interactions — two movers carrying a couch simultaneously. Workaround: break into sequential shots (mover 1 grips, cut, mover 2 lifts) rather than continuous multi-person physics.

CINEMATOGRAPHY GRAMMAR: approved lens choices per shot type (anamorphic for wides, 85mm for portraits), camera movement vocabulary (dolly push-ins for emotional moments, steadicam for action, locked tripod for establishing shots), color grading profiles (warm golden for family scenes, cool blue for dramatic).

TRANSITION VOCABULARY: match cuts, whip pans, light leaks — never cheap dissolves or star wipes. Reference Remotion for implementation.

CAPTION TYPOGRAPHY: cinematic serif fonts (Playfair Display, Cormorant Garamond, or equivalent from Google Fonts — free for commercial use), proper kerning, animated word-by-word reveal with motion blur, positioned lower-third with platform-specific safe margins.

AI ARTIFACT MITIGATION: known tells to avoid — temporal jitter (keep clips under 10 seconds for maximum coherence), texture smoothing (add "natural wear, texture, and imperfections" to all prompts), too-perfect symmetry (specify slight asymmetry in compositions), fabric rendering (specify specific fabric types: "cotton work uniform" not "clothing").

7. captions-and-titles.md — Specific instructions for Remotion Superpowers caption workflow: word-by-word animated captions synced to voiceover timing, cinematic title cards for opening/closing, branded lower-third overlays, consistent typography across all 50 videos, platform-specific safe zones (9:16 caption positioning differs from 16:9). No generic AI caption styling — every text element must look like it belongs in a theatrical trailer.

PHASE 4 — CREATE CLAUDE.MD

Write a CLAUDE.md file for this project that includes:
- Project identity and mission
- The seven-phase pipeline overview (reference PIPELINE_PLAN.md for details)
- Shari'ah compliance as non-negotiable (reference the skill)
- Cinematic quality standard: every frame must look like it belongs in a blockbuster film, not an AI demo. If it looks like AI, it's a reject.
- Caption requirements: every video gets cinematic animated captions via Remotion, synced to voiceover
- Credit conservation rules
- QA hard gates with regeneration limits (max 3 retries per clip per failure category, then escalate to owner)
- Telegram communication protocol (how to report progress, request approval, handle feedback). Always acknowledge received briefs immediately ("Brief received, processing"). Send progress updates at major milestones (brief validated, generation started, QA complete, video ready for review).
- Auto memory instructions (what to remember: prompt success rates, model performance, owner preferences, failure patterns)
- Git discipline: commit after every significant pipeline change, skill update, or config modification

Resource management rules (add a dedicated section):
- NEVER run Remotion rendering and FFmpeg encoding simultaneously — process sequentially
- NEVER run more than one Playwright browser session at a time
- Delete QA frame extractions after a clip passes final review (keep only the scored summary in SQLite)
- Auto-cleanup: delete QA frames older than 7 days, delete raw generation clips older than 30 days (after final video is approved and archived)
- Monitor disk space before starting a batch: if less than 20GB free, run cleanup first

Crash recovery protocol (add a dedicated section):
- The SQLite database is the source of truth for pipeline state
- Every brief has a status field: queued → generating → qa → post_production → rendering → complete → approved/rejected
- On restart after a crash, query the database for briefs with status != complete/approved/rejected
- Resume from the last completed step for each in-progress brief
- Never re-generate clips that already passed QA — check generation_history first

Memory maintenance (add a dedicated section):
- Monthly: review auto memory files, archive entries older than 90 days that have not been referenced
- Monthly: review generation_history, move records older than 90 days to generation_history_archive table
- If context window feels slow or noisy, run /memory to review and prune stale entries

PHASE 5 — INITIALIZE DATABASE

Create the SQLite schema for pipeline.db with tables:
- briefs (id, concept_text, shot_list_json, shariah_validated, status TEXT DEFAULT 'queued', current_step TEXT, created_at, updated_at)
  -- status values: queued, generating, qa, post_production, rendering, complete, approved, rejected
  -- current_step tracks the specific shot/clip being processed for crash recovery
- generation_history (id, brief_id, shot_number, prompt, model, settings_json, reference_image, qa_scores_json, pass_fail, failure_codes, improvement_suggestions, retry_count INTEGER DEFAULT 0, generation_method TEXT DEFAULT 'api', created_at)
  -- retry_count tracks regeneration attempts per clip (max 3 per failure category)
  -- generation_method tracks whether API or Playwright was used
- learned_preferences (id, category, parameter, optimal_value, confidence_score, sample_count, updated_at)
- feedback_log (id, video_id, owner_feedback, sentiment, adjustments_applied, created_at)
- generation_history_archive — same schema as generation_history, for records older than 90 days

PHASE 6 — VERIFY AND REPORT

After completing all phases:
1. Run /security-review on the entire /opt/pipeline/ directory
2. Test Higgsfield API: attempt a test image generation via the Python SDK and confirm credits are deducted from the subscription pool
3. Test Playwright can open https://higgsfield.ai and take a screenshot (fallback verification)
4. Test Telegram connection by sending me a message: "Pipeline initialized. Ready for first brief."
5. Test SQLite by inserting and querying a test record in pipeline.db
6. Test ElevenLabs: generate a 5-second test voiceover and verify word-level timestamps are returned
7. Test Remotion: render a 3-second test composition with animated caption text from the /opt/pipeline/captions/ project
8. Check disk space: df -h / (must have >50GB free to start production)
9. Report the full status: which plugins installed successfully, which used fallbacks, which failed, disk space, and all verified integrations
10. Git commit the full initialized state: git add -A && git commit -m "Pipeline setup complete — all plugins, skills, database, and config initialized"

Do not proceed to video generation yet. This session is infrastructure setup only. The first production run will be triggered via Telegram once I confirm the brand assets are uploaded.
```

---

## What Happens After Kickstart

1. **You upload brand assets** — truck photos (every angle), crew photos, logo files (PNG with alpha), location reference shots — into `/opt/pipeline/assets/`
2. **You fill in brand-identity.md** — actual colors, logo placement rules, uniform details, approved caption fonts and styles
3. **You send your first brief via Telegram** — "test ad: truck arrives at suburban home, crew unloads carefully, family watches happily, 30 seconds"
4. **The system runs** — brief validation → Shari'ah check → shot list → Higgsfield generation → QA → cinematic captions via Remotion → voiceover mix → post-production → delivered to Telegram for your approval
5. **You approve or reject with feedback** — every decision feeds the learning loop
6. **Repeat 50 times** — by video 20, the system knows your brand's visual DNA better than any external agency
7. **Every change is git-tracked** — you can always roll back, audit decisions, and see how the system evolved

Bismillah. Let's build.
