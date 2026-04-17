#!/bin/bash
# Sync Claude memory files (~/.claude/projects/-opt-pipeline/memory/*.md)
# into SQLite learned_preferences table as category prefix 'memory-<type>'.
#
# Behaviour:
#   - Parses YAML frontmatter (name, description, type)
#   - UPSERTs via DELETE+INSERT within a transaction (idempotent)
#   - Only touches rows where category LIKE 'memory-%'
#   - Other learned_preferences rows (heartbeats, old entries) untouched
#
# Run manually or from cron (daily at :23 — off-peak, after learning cycle)

set -uo pipefail

PY=/usr/bin/python3
SQLITE=/usr/bin/sqlite3

PIPELINE=/opt/pipeline
DB="$PIPELINE/data/pipeline.db"
MEM_DIR="$HOME/.claude/projects/-opt-pipeline/memory"
LOG="$PIPELINE/data/learning-cycle.log"

TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
log() { echo "[$TS] [sync-memory] $*" >> "$LOG"; }

if [ ! -d "$MEM_DIR" ]; then
    log "memory dir missing: $MEM_DIR"
    exit 1
fi

# Parse files + emit SQL statements via python (handles YAML frontmatter cleanly)
sql=$($PY <<PYEOF
import os, sys, glob

MEM_DIR = "$MEM_DIR"
ts = "$TS"

def escape(s):
    return s.replace("'", "''")

def parse(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('---'):
        return None
    # split into frontmatter + body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    fm_raw, body = parts[1], parts[2].strip()
    fm = {}
    for line in fm_raw.strip().splitlines():
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        fm[k.strip()] = v.strip()
    return {
        'name': fm.get('name', os.path.basename(path).replace('.md','')),
        'description': fm.get('description', ''),
        'type': fm.get('type', 'feedback'),
        'body': body,
        'filename': os.path.basename(path),
    }

rows = []
for path in sorted(glob.glob(os.path.join(MEM_DIR, '*.md'))):
    if path.endswith('MEMORY.md'):
        continue  # the index file, not a memory itself
    m = parse(path)
    if not m:
        continue
    rows.append(m)

print(f"-- sync of {len(rows)} memory files at {ts}", file=sys.stderr)

print("BEGIN;")
print("DELETE FROM learned_preferences WHERE category LIKE 'memory-%';")
for m in rows:
    category = f"memory-{m['type']}"
    # use filename (without .md) as parameter — stable, unique per memory
    parameter = m['filename'][:-3]
    # optimal_value = description + \n\n + body (full content queryable)
    value = f"{m['description']}\n\n{m['body']}" if m['description'] else m['body']
    print(
        f"INSERT INTO learned_preferences "
        f"(category, parameter, optimal_value, confidence_score, sample_count, updated_at) "
        f"VALUES ('{escape(category)}', '{escape(parameter)}', '{escape(value)}', 1.0, 1, '{ts}');"
    )
print("COMMIT;")
PYEOF
)

if [ -z "$sql" ]; then
    log "SQL generation failed — no output"
    exit 1
fi

# Execute in one transaction
echo "$sql" | $SQLITE "$DB" -cmd ".timeout 5000" 2>/tmp/sync-memory.err
rc=$?

if [ $rc -ne 0 ]; then
    log "SQL execution FAILED rc=$rc — stderr: $(cat /tmp/sync-memory.err 2>/dev/null | head -c 300)"
    exit $rc
fi
rm -f /tmp/sync-memory.err

# Report counts
count=$($SQLITE "$DB" "SELECT COUNT(*) FROM learned_preferences WHERE category LIKE 'memory-%';")
by_type=$($SQLITE "$DB" "SELECT category||':'||COUNT(*) FROM learned_preferences WHERE category LIKE 'memory-%' GROUP BY category;" | tr '\n' ' ')
log "synced $count memory rows — $by_type"
echo "Synced $count rows — $by_type"
