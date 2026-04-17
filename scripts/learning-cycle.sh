#!/bin/bash
# Daily learning cycle — tracks upstream changes across pipeline dependencies.
# Scheduled via user crontab (every 6h). Self-hardening: flock concurrency guard,
# log rotation, dedup of HN findings, absolute binary paths for cron PATH.
#
# Outputs:
#   /opt/pipeline/output/research/daily/YYYY-MM-DD.md   (human-readable)
#   learned_preferences SQLite rows                      (machine-readable)
#   /opt/pipeline/data/learning-cycle.log                (operational log)
#
# Finding model:
#   STRONG  = GitHub release tag bump OR doc-page content change
#   WEAK    = HN mentions (informational, logged to markdown, NOT counted)
#   HEARTBEAT row written every run regardless of findings (liveness signal)

set -uo pipefail

# --- Absolute paths — cron's PATH is minimal ---
CURL=/usr/bin/curl
PY=/usr/bin/python3
SQLITE=/usr/bin/sqlite3
FLOCK=/usr/bin/flock

# --- Config ---
PIPELINE=/opt/pipeline
CACHE="$PIPELINE/data/learning-cycle-cache"
OUT="$PIPELINE/output/research/daily"
LOG="$PIPELINE/data/learning-cycle.log"
DB="$PIPELINE/data/pipeline.db"
LOCK=/tmp/snelverhuizen-learning-cycle.lock
HN_SEEN="$CACHE/hn-seen.txt"
MAX_LOG_BYTES=$((10 * 1024 * 1024))  # 10MB

DATE=$(date -u +%Y-%m-%d)
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)

mkdir -p "$CACHE" "$OUT"
touch "$HN_SEEN"

# --- Log rotation: truncate if over 10MB ---
if [ -f "$LOG" ]; then
    log_size=$(stat -c %s "$LOG" 2>/dev/null || echo 0)
    if [ "$log_size" -gt "$MAX_LOG_BYTES" ]; then
        mv "$LOG" "${LOG}.old"
        echo "[$TS] rotated previous log to ${LOG}.old" > "$LOG"
    fi
fi

# --- Concurrency guard: acquire lock or exit quietly ---
exec 200>"$LOCK"
if ! $FLOCK -n 200; then
    echo "[$TS] another instance is running, skipping" >> "$LOG"
    exit 0
fi

exec >> "$LOG" 2>&1
echo ""
echo "=== $TS learning cycle start (pid $$) ==="

REPORT="$OUT/$DATE.md"
BUF=$(mktemp) || { echo "mktemp failed"; exit 1; }
trap 'rm -f "$BUF"' EXIT

findings_strong=0
findings_weak=0

# --- 1. GitHub releases (pipeline-critical repos) ---
echo "## GitHub releases" >> "$BUF"
repo_changes=0
for repo in \
    remotion-dev/remotion \
    elevenlabs/elevenlabs-python \
    jdepoix/youtube-transcript-api \
    yt-dlp/yt-dlp
do
    latest=$(
        { $CURL -fsSL -m 10 "https://api.github.com/repos/$repo/releases/latest" 2>/dev/null \
            | $PY -c "import sys,json
try:
    r=json.load(sys.stdin); print(r.get('tag_name') or r.get('name') or '?')
except Exception: print('?')" 2>/dev/null; } || true
    )
    [ -z "$latest" ] && latest="?"
    [ "$latest" = "?" ] && continue
    safe=$(echo "$repo" | tr / _)
    cache_file="$CACHE/${safe}.tag"
    prev=$(cat "$cache_file" 2>/dev/null || echo "__first__")
    if [ "$latest" != "$prev" ]; then
        if [ "$prev" = "__first__" ]; then
            echo "- **$repo**: baseline \`$latest\`" >> "$BUF"
        else
            echo "- **$repo**: \`$prev\` → \`$latest\` STRONG" >> "$BUF"
            repo_changes=$((repo_changes + 1))
            findings_strong=$((findings_strong + 1))
        fi
        echo "$latest" > "$cache_file"
    fi
done
[ "$repo_changes" -eq 0 ] && echo "- _no changes since last run_" >> "$BUF"

# --- 2. Doc pages: content-hash change detection ---
# Strip common dynamic patterns (timestamps, CSRF tokens, build hashes) before hash
echo "" >> "$BUF"
echo "## Doc pages" >> "$BUF"
doc_changes=0
doc_list="aimlapi|https://docs.aimlapi.com
remotion|https://www.remotion.dev/docs
elevenlabs|https://elevenlabs.io/docs"
# klingai.com dropped: CDN rotation produces false-positive hash flips.
# Kling updates are tracked via AIMLAPI docs since we access through that provider.

while IFS='|' read -r name url; do
    [ -z "$name" ] && continue
    body=$($CURL -fsSL -m 15 -A "pipeline-learning-bot/1.0" "$url" 2>/dev/null || true)
    [ -z "$body" ] && { echo "- **$name**: fetch failed (network/404)" >> "$BUF"; continue; }
    # Sanity: real doc pages are >500 bytes; anything smaller is likely an error page/redirect
    body_size=${#body}
    if [ "$body_size" -lt 500 ]; then
        echo "- **$name**: fetch returned only ${body_size}B (error page?), skipping" >> "$BUF"
        continue
    fi
    # Strip dynamic patterns before hash:
    #   <script>/<style>/<!--...--> removed entirely (where most dynamic config lives),
    #   then timestamps/UUIDs/hashes/CDN paths normalized.
    stripped=$(echo "$body" | $PY -c "
import sys, re
t = sys.stdin.read()
t = re.sub(r'<script\b[^>]*>.*?</script>', '', t, flags=re.DOTALL|re.IGNORECASE)
t = re.sub(r'<style\b[^>]*>.*?</style>',   '', t, flags=re.DOTALL|re.IGNORECASE)
t = re.sub(r'<!--.*?-->', '', t, flags=re.DOTALL)
t = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z?', 'TIMESTAMP', t)
t = re.sub(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', 'UUID', t)
t = re.sub(r'(?i)(nonce|csrf|token|build[_-]?id|hash)[=:\"\'\s]+[a-f0-9]{8,}', 'DYNAMIC', t)
t = re.sub(r'\"ts\":\s*\d+', '\"ts\":0', t)
t = re.sub(r'_next/static/[^\"\']+', '_next/static/DYNAMIC', t)
t = re.sub(r'\s+', ' ', t).strip()
print(t, end='')" 2>/dev/null || echo "$body")
    new_hash=$(echo "$stripped" | sha256sum | awk '{print $1}')
    hash_file="$CACHE/doc_${name}.sha"
    prev_hash=$(cat "$hash_file" 2>/dev/null || echo "__first__")
    if [ "$new_hash" != "$prev_hash" ]; then
        if [ "$prev_hash" = "__first__" ]; then
            echo "- **$name**: baseline captured" >> "$BUF"
        else
            echo "- **$name**: content changed (${url}) STRONG" >> "$BUF"
            doc_changes=$((doc_changes + 1))
            findings_strong=$((findings_strong + 1))
        fi
        echo "$new_hash" > "$hash_file"
    fi
done <<< "$doc_list"
[ "$doc_changes" -eq 0 ] && echo "- _no changes since last run_" >> "$BUF"

# --- 3. HN mentions — dedup by objectID, informational only ---
echo "" >> "$BUF"
echo "## HN mentions (last 24h — weak signal, informational)" >> "$BUF"
since=$(( $(date +%s) - 86400 ))
new_hn=0
# Use narrow, project-specific queries (no generic "AI video" catch-all)
for query in "remotion.dev" "klingai" "aimlapi" "elevenlabs"; do
    result=$($CURL -fsSL -m 10 "https://hn.algolia.com/api/v1/search?query=${query}&tags=story&numericFilters=created_at_i%3E${since}&hitsPerPage=5" 2>/dev/null || true)
    [ -z "$result" ] && continue
    parsed=$(echo "$result" | $PY -c "
import sys,json
try:
    r = json.load(sys.stdin)
    for h in r.get('hits', [])[:5]:
        oid = h.get('objectID','')
        title = h.get('title','').replace('\n',' ').replace('|',' ')
        url = h.get('url') or f'https://news.ycombinator.com/item?id={oid}'
        points = h.get('points', 0)
        print(f'{oid}|{title}|{url}|{points}')
except Exception: pass
" 2>/dev/null || true)
    [ -z "$parsed" ] && continue
    query_has_new=0
    while IFS='|' read -r oid title url points; do
        [ -z "$oid" ] && continue
        if ! grep -Fxq "$oid" "$HN_SEEN" 2>/dev/null; then
            if [ "$query_has_new" -eq 0 ]; then
                echo "**query: \`$query\`**" >> "$BUF"
                query_has_new=1
            fi
            echo "- [$title]($url) (${points}pt) [new]" >> "$BUF"
            echo "$oid" >> "$HN_SEEN"
            new_hn=$((new_hn + 1))
        fi
    done <<< "$parsed"
done
if [ "$new_hn" -eq 0 ]; then
    echo "- _no new HN posts_" >> "$BUF"
else
    findings_weak=$new_hn
fi

# --- 4. Persist report ---
total_findings=$((findings_strong + findings_weak))
{
    echo "# Learning cycle — $DATE"
    echo ""
    echo "_Last run: $TS. STRONG: $findings_strong, WEAK: $findings_weak._"
    echo ""
    cat "$BUF"
    echo ""
} > "$REPORT"

# --- 5. Heartbeat row in learned_preferences (always) ---
# Escape for SQL
note=$(echo "STRONG=$findings_strong WEAK=$findings_weak — $REPORT" | sed "s/'/''/g")
$SQLITE "$DB" -cmd ".timeout 5000" <<SQL
INSERT INTO learned_preferences (category, parameter, optimal_value, confidence_score, sample_count, updated_at)
VALUES ('learning-cycle-heartbeat', '$TS', '$note', 1.0, $total_findings, '$TS');
SQL

# --- 6. Strong findings: one row per ---
if [ "$findings_strong" -gt 0 ]; then
    # Log what changed, structured — parse "STRONG" lines from buffer
    grep -E "STRONG" "$BUF" | while IFS= read -r line; do
        safe_line=$(echo "$line" | sed "s/'/''/g")
        $SQLITE "$DB" -cmd ".timeout 5000" <<SQL
INSERT INTO learned_preferences (category, parameter, optimal_value, confidence_score, sample_count, updated_at)
VALUES ('learning-cycle-strong', '$TS-$RANDOM', '$safe_line', 0.95, 1, '$TS');
SQL
    done
fi

echo "[$TS] heartbeat written, STRONG=$findings_strong WEAK=$findings_weak"
echo "=== $TS learning cycle end ==="
