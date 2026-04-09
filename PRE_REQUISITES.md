# Pre-Requisites Checklist — Complete Before Running Kickstart

## VPS Requirements

**Minimum specs:**
- 4+ vCPU, 16+ GB RAM, 200+ GB SSD (~$25–35/mo on Hetzner, DigitalOcean, or equivalent)
- 16GB RAM is needed because Playwright + Chromium + Remotion rendering run sequentially but Claude Code + MCP servers run concurrently
- 200GB SSD because video files accumulate fast (50 videos × multiple clips × QA frames)
- Ubuntu 24.04 LTS recommended (25.10 works but is non-LTS — support ends ~July 2026)

**Verify your VPS meets this:**
```bash
nproc && free -h && df -h /
```

---

## Software to Install on VPS Before Kickstart

Claude Code cannot install these itself — they must be present before you run the prompt.

### 1. Node.js (v20+ LTS, v22 recommended for new installs)
Required by: Playwright, Remotion, most MCP servers, plugin system
```bash
# Node 22 LTS recommended for new installs. Node 20 works but reached EOL April 2026.
# If Node 20 is already installed and working, proceed with it — upgrade after first production run.
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -
sudo apt-get install -y nodejs
node --version  # must be v20+
npm --version
```

### 2. Python 3.11+
Required by: Hindsight, some MCP servers, FFmpeg scripting
```bash
sudo apt-get install -y python3 python3-pip python3-venv
python3 --version  # must be 3.11+
```

### 3. FFmpeg
Required by: all video post-production, frame extraction for QA
```bash
sudo apt-get install -y ffmpeg
ffmpeg -version
```

### 4. Git
Required by: Phase 0 repo init, auto memory scoping, Superpowers worktrees
```bash
sudo apt-get install -y git
git config --global user.name "Pipeline"
git config --global user.email "pipeline@yourdomain.com"
```

### 5. Chromium (headless)
Required by: Playwright for driving Higgsfield.ai
```bash
npx playwright install chromium
npx playwright install-deps
```

### 6. tmux
Required by: persistent Claude Code sessions that survive SSH disconnection
```bash
sudo apt-get install -y tmux
```

### 7. Build essentials
Required by: some npm packages that compile native modules
```bash
sudo apt-get install -y build-essential
```

### 8. uv (Python package manager)
Required by: ElevenLabs MCP server (uses `uvx` to run)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or restart shell to add uv to PATH
uv --version
uvx --version
```

**One-liner to install everything:**
```bash
sudo apt-get update && sudo apt-get install -y git python3 python3-pip python3-venv ffmpeg tmux build-essential && \
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash - && \
sudo apt-get install -y nodejs && \
curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc && \
npx playwright install chromium && npx playwright install-deps
```

---

## Accounts & API Keys You Need Ready

Collect these before running kickstart. The prompt will need them during plugin configuration.

### 1. Higgsfield Login Credentials
- Your email and password for higgsfield.ai
- Playwright will use these to log in via the browser
- Store securely in environment variables, NOT in code:
```bash
export HIGGSFIELD_EMAIL="your@email.com"
export HIGGSFIELD_PASSWORD="your_password"
```

### 2. ElevenLabs API Key
- Get it from: https://elevenlabs.io → Profile → API Key
- Store as:
```bash
export ELEVENLABS_API_KEY="your_key_here"
```

### 3. Telegram Bot Token
- You MUST create a bot BEFORE the kickstart prompt runs
- Open Telegram → search for @BotFather → send `/newbot`
- Follow the prompts: give it a name (e.g., "Pipeline Bot") and username (e.g., "mypipeline_bot")
- BotFather gives you a token like `7123456789:AAH...`
- Also note your own Telegram user ID (search @userinfobot and send `/start`)
- Store as:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_OWNER_ID="your_user_id"
```

### 5. Higgsfield API Key (for Cloud API access)
- Log into cloud.higgsfield.ai with your Higgsfield account
- Generate an API key from the dashboard
- The API uses the same credit pool as your subscription — no separate billing
- Store as:
```bash
export HIGGSFIELD_API_KEY="your_api_key"
export HIGGSFIELD_API_SECRET="your_api_secret"
```
- Note: The browser login credentials (HIGGSFIELD_EMAIL/PASSWORD) are still needed as a fallback for UI-only features

### 6. Freesound API Key
- Register at https://freesound.org/apiv2/apply/
- Get an API key for automated ambient SFX downloads
- Store as:
```bash
export FREESOUND_API_KEY="your_key_here"
```

### 7. CRITICAL: Hindsight LLM Provider + API Key Warning

Hindsight needs an LLM to extract facts from conversations. Tell it to use Claude Code itself (covered by your Max subscription):
```bash
export HINDSIGHT_LLM_PROVIDER="claude-code"
```

**DO NOT set ANTHROPIC_API_KEY on your VPS.** If this variable exists, Claude Code silently switches from your Max subscription to per-token API billing — you'd be paying twice for the same thing. Check and remove it now:
```bash
# Check if it's set
echo $ANTHROPIC_API_KEY

# If anything prints, remove it
unset ANTHROPIC_API_KEY

# Also check if it's in your shell config files
grep -rn "ANTHROPIC_API_KEY" ~/.bashrc ~/.profile ~/.zshrc 2>/dev/null
# If found, open the file and delete that line
```

Everything — Claude Code orchestration, vision QA, Hindsight memory extraction — runs through your single Max subscription. Zero additional API costs.

---

## Create the Project Directory

```bash
sudo mkdir -p /opt/pipeline
sudo chown $USER:$USER /opt/pipeline
```

---

## Upload the Three Documents

Copy these files to your VPS (via scp, rsync, or paste):
```
/opt/pipeline/PIPELINE_PLAN.md
/opt/pipeline/PROJECT_PLUGINS.md
/opt/pipeline/PROJECT_KICKSTART.md
```

Example via scp from your local machine:
```bash
scp PIPELINE_PLAN.md PROJECT_PLUGINS.md PROJECT_KICKSTART.md user@your-vps-ip:/opt/pipeline/
```

---

## Environment Variables File

Create a single env file that loads on every session. This keeps secrets out of your shell history:

```bash
cat > /opt/pipeline/.env << 'EOF'
# Higgsfield (browser login)
HIGGSFIELD_EMAIL="your@email.com"
HIGGSFIELD_PASSWORD="your_password"

# Higgsfield (Cloud API — primary generation method)
HIGGSFIELD_API_KEY="your_api_key"
HIGGSFIELD_API_SECRET="your_api_secret"

# ElevenLabs
ELEVENLABS_API_KEY="your_key"

# Telegram
TELEGRAM_BOT_TOKEN="your_bot_token"
TELEGRAM_OWNER_ID="your_user_id"

# Freesound (ambient SFX)
FREESOUND_API_KEY="your_key"

# Hindsight — uses Claude Code (Max subscription), NOT a separate API key
HINDSIGHT_LLM_PROVIDER="claude-code"

# DO NOT add ANTHROPIC_API_KEY here — it will override your Max subscription
EOF

chmod 600 /opt/pipeline/.env
echo 'source /opt/pipeline/.env' >> ~/.bashrc
source /opt/pipeline/.env
```

**Make sure `.env` is in `.gitignore`** — this file must NEVER be committed:
```bash
echo ".env" > /opt/pipeline/.gitignore
```

---

## Pre-Flight Verification

Run this checklist before executing the kickstart prompt:

```bash
echo "=== PRE-FLIGHT CHECK ==="
echo -n "Node.js: " && node --version
echo -n "npm: " && npm --version
echo -n "Python: " && python3 --version
echo -n "FFmpeg: " && ffmpeg -version 2>&1 | head -1
echo -n "Git: " && git --version
echo -n "tmux: " && tmux -V
echo -n "Chromium: " && npx playwright --version
echo -n "uv: " && uv --version
echo -n "Claude Code: " && claude --version
echo ""
echo "=== API KEYS ==="
[ -n "$HIGGSFIELD_EMAIL" ] && echo "✓ Higgsfield login credentials set" || echo "✗ MISSING: Higgsfield login credentials"
[ -n "$HIGGSFIELD_API_KEY" ] && echo "✓ Higgsfield API key set" || echo "✗ MISSING: Higgsfield API key (get from cloud.higgsfield.ai)"
[ -n "$ELEVENLABS_API_KEY" ] && echo "✓ ElevenLabs API key set" || echo "✗ MISSING: ElevenLabs API key"
[ -n "$TELEGRAM_BOT_TOKEN" ] && echo "✓ Telegram bot token set" || echo "✗ MISSING: Telegram bot token"
[ -n "$TELEGRAM_OWNER_ID" ] && echo "✓ Telegram owner ID set" || echo "✗ MISSING: Telegram owner ID"
[ -n "$FREESOUND_API_KEY" ] && echo "✓ Freesound API key set" || echo "✗ MISSING: Freesound API key (register at freesound.org)"
[ "$HINDSIGHT_LLM_PROVIDER" = "claude-code" ] && echo "✓ Hindsight using Max subscription" || echo "✗ MISSING: HINDSIGHT_LLM_PROVIDER=claude-code"
[ -z "$ANTHROPIC_API_KEY" ] && echo "✓ No ANTHROPIC_API_KEY (Max subscription will be used)" || echo "✗ WARNING: ANTHROPIC_API_KEY is set — Claude Code will use API billing instead of Max! Run: unset ANTHROPIC_API_KEY"
echo ""
echo "=== FILES ==="
[ -f "/opt/pipeline/PIPELINE_PLAN.md" ] && echo "✓ PIPELINE_PLAN.md" || echo "✗ MISSING: PIPELINE_PLAN.md"
[ -f "/opt/pipeline/PROJECT_PLUGINS.md" ] && echo "✓ PROJECT_PLUGINS.md" || echo "✗ MISSING: PROJECT_PLUGINS.md"
[ -f "/opt/pipeline/PROJECT_KICKSTART.md" ] && echo "✓ PROJECT_KICKSTART.md" || echo "✗ MISSING: PROJECT_KICKSTART.md"
[ -f "/opt/pipeline/.gitignore" ] && echo "✓ .gitignore" || echo "✗ MISSING: .gitignore"
echo ""
echo "=== DISK ==="
df -h / | tail -1
echo ""
echo "All checks passed? Run the kickstart prompt in Claude Code."
```

Every line should show ✓ before you proceed. If anything shows ✗, fix it first.

---

## How to Execute the Kickstart

Once all checks pass:

```bash
cd /opt/pipeline
tmux new-session -s pipeline
# Inside tmux:
claude
```

Then paste the kickstart prompt from `PROJECT_KICKSTART.md` (the section inside the code block starting with "You are the autonomous orchestrator...").

If you get disconnected from SSH, reconnect with:
```bash
tmux attach -t pipeline
```

---

## Brand Assets (NOT needed for kickstart, but needed before first production run)

Start collecting these while the pipeline initializes:
- Truck photos: front, back, both sides, 3/4 angle — in good lighting
- Crew photos: individual and group, in uniform, natural poses
- Logo: PNG with transparent background, vector (SVG/AI) if available
- Location reference shots: typical residential neighborhoods you service
- Brand colors: exact hex codes
- Any existing marketing materials for style reference

Upload to `/opt/pipeline/assets/` when ready, then fill in `brand-identity.md` and send your first brief via Telegram.
