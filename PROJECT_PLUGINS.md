# Every Claude Code plugin for an autonomous video pipeline

**Claude Code's plugin ecosystem has exploded to 415+ plugins and 2,800+ skills as of April 2026**, and a carefully selected stack of roughly 25 tools can transform it into a fully autonomous video production orchestrator running headless on a VPS. The pipeline you describe—Playwright driving Higgsfield.ai, automated visual QA, FFmpeg post-production, persistent memory—maps almost perfectly onto existing plugins. Below is every plugin worth installing, grouped by function, with installation commands and specific relevance to cinematic video ad generation.

The plugin system reached stability in early 2026. Plugins install via `/plugin install name@marketplace`, MCP servers via `claude mcp add`, and skills via `npx skills add`. The official Anthropic marketplace (`claude-plugins-official`) loads automatically. Community marketplaces are added with `/plugin marketplace add user/repo`. All configuration lives in `~/.claude.json` (user scope) or `.claude/settings.json` (project scope).

---

## How the plugin system actually works

Claude Code plugins are **bundles that can contain any combination of five components**: skills (Markdown instruction files), MCP servers (external tool connections), hooks (deterministic shell scripts on lifecycle events), agents (subagent definitions), and slash commands. Every plugin requires a `plugin.json` manifest in a `.claude-plugin/` directory.

**Skills** are the most common component—simple `SKILL.md` files with YAML frontmatter that teach Claude when and how to perform tasks. They auto-invoke when relevant or respond to `/slash-commands`. Skills follow an open standard at agentskills.io and work across Claude Code, Cursor, Gemini CLI, Codex CLI, and others.

**Installation methods** (pick whichever fits your workflow):

- `/plugin install name@claude-plugins-official` — from Anthropic's official marketplace
- `/plugin marketplace add user/repo` then `/plugin install name@marketplace-id` — community marketplaces
- `claude mcp add name -- command args` — standalone MCP servers
- `npx skills add repo/skills` — agent skills standard
- Manual clone into `~/.claude/skills/` — for skills like gstack

The ecosystem is tracked by several community directories: claudemarketplaces.com indexes **2,500+ marketplaces**, tonsofskills.com catalogs browsable skills, and multiple "awesome" GitHub lists curate the best options.

---

## Core orchestration: Superpowers and gstack

### Superpowers — the structured development engine

**~137,600 GitHub stars** | **355,600+ marketplace installs** | By Jesse Vincent (obra) | MIT license

Superpowers transforms Claude Code from reactive autocomplete into a structured senior developer through a **7-phase workflow**: Socratic brainstorming → micro-task planning → test-driven development → subagent-driven execution → code review → git worktree isolation → verification-before-completion. It ships with **38 agents, 156 skills, and 72 legacy command shims**.

```bash
# Install from official Anthropic marketplace
/plugin install superpowers@claude-plugins-official

# Or from Superpowers' own marketplace
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

Key commands: `/superpowers:brainstorm`, `/superpowers:write-plan`, `/superpowers:execute-plan`. Skills activate automatically when relevant—the TDD skill kicks in during feature implementation, the code-review agent validates against plans.

**Pipeline relevance**: Every pipeline component (Playwright automation scripts, FFmpeg processing chains, QA routines) benefits from Superpowers' plan-then-execute discipline. The subagent-driven development and git worktree isolation prevent half-finished code from breaking a running production system.

### gstack — Gary Tan's virtual engineering team

**~54,000–66,400 GitHub stars** (hit 50K in 16 days after March 12, 2026 launch) | **~9,200 forks** | By Garry Tan (YC CEO) | MIT license

gstack provides **28 slash commands**, each activating a specialized cognitive mode: CEO (`/office-hours`, `/plan-ceo-review`), Engineering Manager (`/plan-eng-review`), Designer (`/design-consultation`, `/design-review`), Code Reviewer (`/review`), QA Lead (`/qa` — opens a real Playwright browser), Release Manager (`/ship`, `/canary`), and Security Officer (`/cso` — OWASP Top 10 + STRIDE).

```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && \
cd ~/.claude/skills/gstack && ./setup
```

Then add a `## gstack` section to your CLAUDE.md. Note: gstack is a skills framework, not a traditional plugin—it installs Markdown files plus a ~58MB browser daemon.

**Pipeline relevance**: The `/qa` command opens a real Chromium browser for testing, directly useful for verifying rendered video outputs in a browser context. `/cso` security review catches vulnerabilities in your API key handling and automation scripts. `/ship` and `/canary` manage deployment of pipeline updates.

---

## Persistent memory across sessions

Memory is critical for an autonomous pipeline that must remember past renders, client preferences, quality thresholds, and debugging history across sessions.

### claude-mem — the community standard

**~46,100 GitHub stars** | **v12.0.0** | By Alex Newman | AGPL-3.0

claude-mem automatically captures everything Claude does, compresses observations with AI, and injects relevant context into future sessions. It uses **5 lifecycle hooks** (SessionStart → UserPromptSubmit → PostToolUse → Summary → SessionEnd) and stores data in SQLite at `~/.claude-mem/`. A web viewer at `http://localhost:37777` shows the real-time memory stream.

```bash
# Recommended installation
npx claude-mem install

# Or via plugin system
/plugin marketplace add thedotmack/claude-mem && /plugin install claude-mem
```

Three-layer retrieval: summaries → timeline → full observations, with token cost visibility at each layer. Privacy tags (`<private>`) prevent storage of sensitive data.

**Pipeline relevance**: Remembers which video renders succeeded or failed, client feedback patterns, optimal FFmpeg encoding settings discovered through iteration, and Higgsfield prompt refinements. The progressive disclosure system keeps context costs manageable during long production runs.

### Hindsight — biomimetic long-term memory

By Vectorize.io | Available at github.com/vectorize-io/hindsight

Hindsight uses biomimetic data structures (World facts, Experiences, Entities, Relationships, Time series) and claims state-of-the-art LongMemEval performance. It auto-recalls relevant memories on every user prompt and auto-retains conversation content for fact extraction.

```bash
claude plugin marketplace add vectorize-io/hindsight
claude plugin install hindsight-memory

# Configure LLM provider
export HINDSIGHT_LLM_PROVIDER=claude-code  # uses Claude's own model
```

Memory is isolated per-project via git repository identity. Banks provide separate "brains" for different contexts.

**Pipeline relevance**: The entity and relationship tracking is powerful for video pipelines managing multiple clients, brand guidelines, and asset libraries. Per-project isolation means each client's pipeline maintains its own memory bank.

### MemPalace — hierarchical spatial memory

**7,000+ GitHub stars** (in 48 hours of launch) | By Milla Jovovich & Ben Sigman

Inspired by the ancient Greek method of loci, MemPalace organizes memories into Wings → Halls → Rooms → Closets → Drawers. Stores raw verbatim text in ChromaDB with **96.6% LongMemEval R@5** in raw mode. Ships 19 MCP tools.

```bash
pip install mempalace
mempalace init ~/projects/video-pipeline
# Add to MCP config:
# {"mcpServers": {"mempalace": {"command": "mempalace", "args": ["mcp"]}}}
```

**Pipeline relevance**: The hierarchical organization maps naturally to video production—one Wing per client, Halls for scripts/assets/renders/feedback, Rooms for individual projects.

### memsearch — lightweight Markdown-first memory

By Zilliz (creators of Milvus) | MIT license | Released March 12, 2026

A simpler alternative using daily Markdown files as source of truth with Milvus as a rebuildable shadow index. Hybrid search combines dense vector + BM25 sparse + RRF reranking.

```bash
/plugin marketplace add zilliztech/memsearch
/plugin install memsearch
pip install "memsearch[onnx]"  # for zero-config local embeddings
```

**Pipeline relevance**: The Markdown-first approach means memory files are human-readable and git-trackable—useful for auditing pipeline decisions.

---

## Browser automation for driving Higgsfield.ai

### Playwright MCP — the primary choice

By Microsoft | Official at github.com/microsoft/playwright-mcp

The official Playwright MCP server provides navigation, clicking, form filling, screenshots, PDF generation, tab management, network inspection, and custom script execution. Supports Chrome, Firefox, WebKit, and Edge with persistent browser profiles.

```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

Key flags: `--vision` enables screenshot-based interaction, `--save-video=1920x1080` records browser sessions, `--browser-channel=chrome` selects the browser.

**Pipeline relevance**: **This is your core tool for driving Higgsfield.ai's web interface.** Navigate to Higgsfield, fill in prompts, trigger generation, monitor progress, download results—all through Playwright automation. The `browser_run_code` tool enables custom Playwright scripts for complex multi-step workflows.

### Higgsfield MCP servers — direct API integration

Two community MCP servers provide direct Higgsfield API access without browser automation:

**geopopos/higgsfield_ai_mcp** (Python/FastMCP): Text-to-image (Soul model), image-to-video with motion presets, character consistency, style presets.

```bash
pip install higgsfield-mcp
# Config: {"mcpServers": {"higgsfield": {"command": "higgsfield-mcp", 
#   "env": {"HIGGSFIELD_API_KEY": "key", "HIGGSFIELD_SECRET": "secret"}}}}
```

**jfikrat/higgsfield-mcp** (TypeScript/Bun): Same capabilities with DataDome bot protection handling via Helm daemon + curl-impersonate.

**Pipeline relevance**: **The Higgsfield Cloud API (cloud.higgsfield.ai) draws from your subscription credits and should be the primary generation method.** API access eliminates the fragility of browser automation and bypasses DataDome bot protection entirely. Use the Python MCP server for simplicity or TypeScript for better bot-protection handling if the API lacks specific features. Playwright browser automation should be reserved as a fallback for UI-only features (Cinema Studio camera controls, certain Hero Frame workflows).

### Playwright Skill — higher-level abstraction

```bash
/plugin marketplace add lackeyjb/playwright-skill
/plugin install playwright-skill@playwright-skill
```

Claude autonomously writes and executes custom Playwright code rather than using predefined MCP tools. More flexible for complex Higgsfield interactions.

### Additional browser tools

- **Browser MCP** (browsermcp.io) — Chrome extension + MCP server connecting to your actual browser, useful for authenticated Higgsfield sessions
- **Puppeteer MCP** (`@modelcontextprotocol/server-puppeteer`) — alternative to Playwright
- **Chrome DevTools MCP** — deep browser inspection via CDP, useful for debugging Higgsfield interactions

---

## Video and media production plugins

### Remotion Skills — programmatic video from React

**Went viral January 2026** (6M+ views, 25k+ installs first week) | Official by Remotion

Write React/TypeScript components → render to MP4. Teaches Claude correct Remotion patterns: `useCurrentFrame()`, `interpolate()`, `spring()`, `<Sequence>`, `<Composition>`.

```bash
npx skills add remotion-dev/skills
```

**Pipeline relevance**: For generating motion graphics, title cards, transitions, and template-based video segments that don't require Higgsfield's AI generation. Remotion handles the deterministic video elements while Higgsfield creates the cinematic AI footage.

**Licensing note**: Remotion uses a custom license — companies with 3+ employees or revenue above a threshold need a Company License. Single-owner operations and small businesses below the threshold can use it free. Check remotion.dev/license for current terms.

### Remotion Superpowers — full production studio

By DojoCodingLabs | MIT license

Turns Remotion into a complete video production pipeline with **5 MCP servers and 13 commands**. Includes AI voiceovers, music generation, stock footage sourcing, AI image/video generation, TikTok-style captions, professional transitions, 3D content, and an AI review loop.

```bash
/plugin marketplace add DojoCodingLabs/remotion-superpowers
/plugin install remotion-superpowers@remotion-superpowers
```

Pipeline: Prompt → Concept → Script → Voiceover → Music → Footage → Visuals → Render → Review.

**Pipeline relevance**: This single plugin covers nearly every step of video ad production—script generation, voiceover, music, footage assembly, and quality review. Combined with Higgsfield for cinematic shots, this could be the backbone of the entire pipeline.

### FFmpeg MCP — video post-production

By bitscorp-mcp | github.com/bitscorp-mcp/mcp-ffmpeg

Natural language control over FFmpeg: transcoding, cutting/merging, audio extraction, thumbnails, GIFs, resolution scaling, subtitles, watermarks, color correction.

```bash
# Via Smithery
npx -y @smithery/cli install @bitscorp-mcp/mcp-ffmpeg --client claude

# Or direct config
# {"mcpServers": {"ffmpeg": {"command": "npx", "args": ["--yes", "mcp-ffmpeg"]}}}
```

**Pipeline relevance**: **Essential post-production tool.** Concatenate Higgsfield clips, add audio tracks, apply color grading, encode to delivery formats, generate thumbnails for QA review.

There's also an **FFmpeg CLI Skill** available:
```bash
mkdir -p .claude/skills/ffmpeg-cli && \
curl -L -o skill.zip "https://mcp.directory/api/skills/download/1613" && \
unzip -o skill.zip -d .claude/skills/ffmpeg-cli && rm skill.zip
```

### ElevenLabs MCP — voiceover generation

Official by ElevenLabs | github.com/elevenlabs/elevenlabs-mcp

Text-to-speech, voice cloning, audio transcription, audio processing.

```bash
# Config: {"mcpServers": {"ElevenLabs": {"command": "uvx", 
#   "args": ["elevenlabs-mcp"], "env": {"ELEVENLABS_API_KEY": "key"}}}}
```

**Prerequisite:** Requires `uv` (Python package manager) — install via `curl -LsSf https://astral.sh/uv/install.sh | sh`. The `uvx` command is included with `uv`.

**Pipeline relevance**: Generate voiceovers and narration for video ads. Voice cloning maintains brand consistency across campaigns.

### Kie.ai MCP — multi-model media generation

By felores | github.com/felores/kie-ai-mcp-server

Unified access to **Veo3, Runway Aleph, Suno V5, ElevenLabs, Seedance, Midjourney, Flux Kontext**, and more via a single API key. Image (8 tools), video (7 tools), audio (3 tools).

```bash
# Config: {"mcpServers": {"kie": {"command": "npx", 
#   "args": ["-y", "@felores/kie-ai-mcp-server"], "env": {"KIE_AI_API_KEY": "key"}}}}
```

**Pipeline relevance**: One-stop fallback when Higgsfield is unavailable or for specific creative needs—Runway for certain styles, Suno for background music, Midjourney for storyboard concepts.

### Vision MCP — visual quality assurance

By Z.AI | Tools: `ui_diff_check`, `image_analysis`, `video_analysis`, `extract_text_from_screenshot`

```bash
claude mcp add -s user zai-mcp-server \
  --env Z_AI_API_KEY=your_key Z_AI_MODE=ZAI \
  -- npx -y "@z_ai/mcp-server"
```

**Pipeline relevance**: Automated visual QA—compare rendered frames against storyboards, detect artifacts, verify text overlay legibility, check brand color compliance.

---

## VPS infrastructure plugins

### Filesystem and database

Claude Code has built-in `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep` tools, but for structured access add:

```bash
# Filesystem MCP with access controls
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /opt/pipeline

# SQLite for pipeline state tracking
claude mcp add sqlite -- npx -y @modelcontextprotocol/server-sqlite /opt/pipeline/data/pipeline.db
```

The **SQLite MCP** (part of the official MCP servers repo at **~81,800 stars**) enables full database management—track render queue, asset metadata, client preferences, and production history.

### Scheduling and background tasks

Claude Code **v2.1.72+** includes built-in scheduling: `/loop 5m check render status` creates session-scoped recurring tasks using `CronCreate`, `CronList`, `CronDelete` tools (up to 50 tasks per session).

For **persistent scheduling** that survives session restarts on a VPS:

```bash
# claude-code-scheduler — uses OS-level cron
/plugin marketplace add jshchnz/claude-code-scheduler
/plugin install scheduler@claude-code-scheduler

# ClaudeCron — MCP-based with file-watcher triggers
# Config: {"mcpServers": {"claudecron": {"command": "node", 
#   "args": ["/path/to/claudecron/mcp-server/dist/server.js"]}}}
```

**VPS best practice**: Run Claude Code in a tmux session with system cron for the outer scheduling loop:
```bash
tmux new-session -d -s pipeline "claude --dangerously-skip-permissions --channels plugin:telegram@claude-plugins-official"
# System cron for scheduled renders:
# 0 9 * * * cd /opt/pipeline && claude -p "Run morning video batch"
```

### Telegram and Discord integration

**Claude Code Channels** is the official system for bidirectional messaging with a running Claude Code session:

```bash
# Install Telegram channel plugin
/plugin install telegram@claude-plugins-official
/telegram:configure set-token <BOT_TOKEN>

# Launch with channels enabled
claude --channels plugin:telegram@claude-plugins-official
```

Supports photo forwarding, sender allowlists, `/reply`, `/react`, `/edit_message` tools. Lock down with an allowlist policy to restrict who can send commands.

**Discord** works identically: `/plugin install discord@claude-plugins-official` (requires bot creation with Message Content Intent).

**Pipeline relevance**: Send "render video for Client X campaign" from your phone via Telegram, Claude executes on VPS and reports back with preview screenshots. **Caveat**: Some reliability issues reported with zombie processes and dropped messages—monitor and restart periodically.

### API calling and HTTP requests

```bash
# Official Fetch MCP
claude mcp add fetch -- npx -y @anthropic-ai/mcp-server-fetch
```

Enables HTTP requests to external APIs—Higgsfield API, cloud storage, webhook notifications, stock footage services.

### Cost tracking — essential for autonomous operation

**ccusage** (github.com/ryoppippi/ccusage) analyzes Claude Code token usage from local JSONL files:

```bash
npx ccusage daily --project video-pipeline  # daily cost report
npx ccusage daily --json  # machine-readable for dashboards
```

**Anthropic OpenTelemetry** provides production-grade metrics:

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
# Feed into Prometheus/Grafana on VPS
```

**Pipeline relevance**: An autonomous pipeline can burn through credits fast. Schedule `ccusage` reports via cron and set budget alerts. The OpenTelemetry integration feeds directly into Grafana dashboards.

---

## Quality assurance and security review

### Code Review — 5 parallel agents

Official Anthropic plugin | Built into Claude Code repository

Launches **5 parallel Sonnet agents** examining changes from different angles: two CLAUDE.md compliance auditors, one Haiku agent for historical context via git history, one Opus agent hunting bugs and security issues, and one code comment verification agent. Only findings scoring **≥80 confidence** (configurable) surface.

```bash
/code-review              # Local review
/code-review --comment    # Post as GitHub PR comment
```

### Security Review — multi-layered protection

Three options at different levels:

- **`/security-review`** slash command — SQL injection, XSS, auth flaws, dependency vulnerabilities, secret exposure. Uses Opus model. Also available as a GitHub Action
- **Security Guidance plugin** — **107,600 installs**, pre-tool hook intercepting Write/Edit operations, detects 8 vulnerability categories including command injection and unsafe `eval()`
- **Trail of Bits skills** — security analysis marketplace with specialized vulnerability scanners: `/plugin marketplace add trailofbits/skills`

```bash
/plugin install security-guidance@claude-plugins-official
```

**Pipeline relevance**: Your pipeline handles API keys (Higgsfield, ElevenLabs), runs with `--dangerously-skip-permissions`, and executes shell commands. Security review is non-optional.

### QA Skills — systematic testing

By neonwatty | Three specialized agents: smoke tester, UX auditor, adversarial breaker.

```bash
/plugin marketplace add neonwatty/qa-skills
/plugin install qa-skills@neonwatty-qa
# Then: /run-qa smoke|ux|adversarial|all
```

### Frontend Design — polishing visual output

**455,600+ marketplace installs** | Official Anthropic plugin | By Prithvi Rajasekaran & Alexander Bricken

Generates distinctive, production-grade frontend interfaces by establishing a design framework before coding—purpose, audience, aesthetic direction (brutalist, maximalist, luxury, playful). Intentionally avoids generic AI aesthetics.

```bash
/plugin install frontend-design@claude-plugins-official
```

Auto-invokes when Claude detects frontend work. No commands needed.

**Pipeline relevance**: If your pipeline includes a web dashboard for monitoring renders, reviewing outputs, or client previews, this ensures it doesn't look like generic AI slop.

---

## Workflow orchestration for multi-step production

### Agent Teams — official multi-agent coordination

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

One lead session assigns tasks to teammates that work independently with their own context windows. Requires Claude Code v2.1.32+.

**Pipeline relevance**: Run a lead agent managing the overall video pipeline with specialist teammates for scriptwriting, asset generation, rendering, and QA—each with isolated contexts.

### claude-workflow — 56 agents with video support

Available at claudeworkflow.com | 56 agents, 42 skills, 21 MCP tool servers

Specifically includes Replicate, ElevenLabs, and video generation MCP servers. YAML workflow definitions with parallel execution and built-in backlog with acceptance criteria.

**Pipeline relevance**: Purpose-built for the kind of multi-step, multi-tool workflow your video pipeline needs.

### Prompt optimization

**Prompt Architect** (ckelsoe) transforms vague prompts into structured expert-level prompts using 7 research-backed frameworks:

```bash
/plugin marketplace add ckelsoe/prompt-architect
/plugin install prompt-architect@prompt-architect-marketplace
```

**Pipeline relevance**: Optimize Higgsfield generation prompts and video ad scripts for maximum creative quality.

---

## Complete installation script for the video pipeline VPS

Here is a consolidated setup for a fresh VPS deployment, organized by priority:

```bash
# === CORE ORCHESTRATION ===
/plugin install superpowers@claude-plugins-official
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git \
  ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup

# === PERSISTENT MEMORY (pick one primary + one backup) ===
npx claude-mem install                    # Primary: claude-mem
claude plugin marketplace add vectorize-io/hindsight
claude plugin install hindsight-memory    # Backup: Hindsight

# === BROWSER AUTOMATION ===
claude mcp add playwright -- npx @playwright/mcp@latest
pip install higgsfield-mcp               # Direct Higgsfield API

# === VIDEO & MEDIA PRODUCTION ===
npx skills add remotion-dev/skills       # Remotion video generation
/plugin marketplace add DojoCodingLabs/remotion-superpowers
/plugin install remotion-superpowers@remotion-superpowers
npx -y @smithery/cli install @bitscorp-mcp/mcp-ffmpeg --client claude

# === VOICEOVER & AUDIO ===
# Add ElevenLabs to ~/.claude.json mcpServers

# === INFRASTRUCTURE ===
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /opt/pipeline
claude mcp add sqlite -- npx -y @modelcontextprotocol/server-sqlite /opt/pipeline/data/pipeline.db
claude mcp add fetch -- npx -y @anthropic-ai/mcp-server-fetch
/plugin marketplace add jshchnz/claude-code-scheduler
/plugin install scheduler@claude-code-scheduler

# === MESSAGING ===
/plugin install telegram@claude-plugins-official

# === QUALITY & SECURITY ===
/plugin install frontend-design@claude-plugins-official
/plugin install security-guidance@claude-plugins-official
/plugin marketplace add neonwatty/qa-skills
/plugin install qa-skills@neonwatty-qa

# === COST TRACKING ===
# Add to system cron: 0 */6 * * * npx ccusage daily --json >> /opt/pipeline/logs/costs.json

# === PROMPT OPTIMIZATION ===
/plugin marketplace add ckelsoe/prompt-architect
/plugin install prompt-architect@prompt-architect-marketplace

# === LAUNCH ===
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
tmux new-session -d -s pipeline \
  "claude --dangerously-skip-permissions --channels plugin:telegram@claude-plugins-official"
```

---

## Conclusion

The Claude Code plugin ecosystem has reached the point where an autonomous video production pipeline is not just possible but **well-supported by purpose-built tooling**. The most surprising finding is how deep the media production stack runs—Remotion Superpowers alone covers the full pipeline from script to render with AI review loops, and dedicated Higgsfield MCP servers exist for direct API integration, potentially eliminating the browser automation fragility that comes with Playwright-driving a web UI.

Three architectural decisions matter most for your setup. First, **choose between browser automation and API-direct for Higgsfield**—the MCP servers (geopopos/higgsfield_ai_mcp) are more reliable than Playwright-driving the web UI, but may lack newer features. Second, **pick one primary memory system**—claude-mem has the strongest community support at 46K stars and the most mature hook integration, while Hindsight's entity-relationship tracking is better for multi-client pipelines. Third, **invest in cost monitoring early**—ccusage plus OpenTelemetry into Grafana provides the visibility needed before an autonomous pipeline burns through your API budget overnight.

The ecosystem is still early-stage. Expect breaking changes across Claude Code versions, community plugins vary in maintenance quality, and always audit plugin code before installing on a production VPS with `--dangerously-skip-permissions` enabled. The official Anthropic marketplace provides the safest baseline; community marketplaces add power but carry risk.
