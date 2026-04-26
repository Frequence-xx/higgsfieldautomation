#!/usr/bin/env python3
"""Pattern Extractor — mines feedback_log + generation_history for repeated rejection patterns.

Runs weekly (Sundays via learning-cycle.sh). Outputs a draft review markdown to
/opt/pipeline/output/research/patterns/<YYYY-MM-DD>.md for human review.
Human decides which candidates to harden into feedback-catalog.json + skills/.
"""

import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

# --- Absolute paths — works under cron's minimal PATH ---
DB = Path("/opt/pipeline/data/pipeline.db")
OUT_DIR = Path("/opt/pipeline/output/research/patterns")

# Phrases that indicate rejection/problems in free-text feedback.
# Ordered coarse-to-fine: longer phrases first so they shadow substring matches.
KNOWN_FAILURE_PHRASES = [
    "black bars",
    "aspect ratio",
    "choppy motion",
    "laggy motion",
    "face inconsistent",
    "karel inconsistent",
    "ghost driving",
    "breathing",
    "captions not synced",
    "name cards overlapping",
    "side door",
    "no side door",
    "hand visible",
    "hair visible",
    "logo white",
    "logo orange",
    "text garbled",
    "no audio",
    "generate_audio",
    "subject binding",
    "avatar pro",
    "face warp",
    "liftgate",
    "compressed",
    "black bottom",
    "ambient gap",
    "loudnorm",
    "auto-ducking",
    "auto ducking",
    "bleed",
    "caption bleed",
    "micro-jitter",
    "micro jitter",
]

# Stop-words to drop before bigram/trigram extraction
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "this", "that", "these", "those", "it",
    "its", "i", "we", "you", "he", "she", "they", "not", "no", "from",
    "by", "as", "up", "out", "via", "so", "if", "after", "before",
    "then", "also", "very", "just", "each", "per", "all", "1", "2", "3",
    "4", "5", "6", "7", "8", "s1", "s2", "s3", "s4", "s5", "s6",
}


# ---------------------------------------------------------------------------
# Core helpers (importable for unit tests)
# ---------------------------------------------------------------------------

def connect(db_path: Path = DB) -> sqlite3.Connection:
    """Open DB connection. Returns connection or raises."""
    return sqlite3.connect(str(db_path))


def get_generation_stats(cur: sqlite3.Cursor, week_ago: str) -> dict:
    """Return counts of pass/fail/pending in generation_history for the last 7 days."""
    cur.execute(
        "SELECT pass_fail, COUNT(*) FROM generation_history WHERE created_at >= ? GROUP BY pass_fail",
        (week_ago,),
    )
    rows = cur.fetchall()
    stats = {"total": 0, "pass": 0, "fail": 0, "pending": 0, "other": 0}
    for pass_fail, count in rows:
        stats["total"] += count
        pf = (pass_fail or "").lower()
        if pf == "pass":
            stats["pass"] += count
        elif pf in ("fail", "rejected", "reject"):
            stats["fail"] += count
        elif "pending" in pf:
            stats["pending"] += count
        else:
            stats["other"] += count
    return stats


def count_repeated_failures(cur: sqlite3.Cursor, week_ago: str) -> Counter:
    """Count failure_codes from generation_history rejected/failed rows (last 7 days).

    failure_codes is a comma-separated string or NULL.
    Returns Counter mapping code -> count.
    """
    cur.execute(
        """
        SELECT failure_codes
        FROM generation_history
        WHERE pass_fail IN ('fail', 'rejected', 'reject')
          AND failure_codes IS NOT NULL
          AND failure_codes != ''
          AND created_at >= ?
        """,
        (week_ago,),
    )
    code_counter: Counter = Counter()
    for (codes,) in cur.fetchall():
        for code in codes.split(","):
            code = code.strip()
            if code:
                code_counter[code] += 1
    return code_counter


def extract_keywords_from_feedback(cur: sqlite3.Cursor, week_ago: str) -> tuple[Counter, Counter]:
    """Mine owner_feedback + adjustments_applied text from feedback_log (last 7 days).

    Returns:
        phrase_counter  — counts of KNOWN_FAILURE_PHRASES found
        bigram_counter  — counts of meaningful bigrams from rejected feedback
    """
    cur.execute(
        """
        SELECT owner_feedback, adjustments_applied, sentiment
        FROM feedback_log
        WHERE created_at >= ?
        """,
        (week_ago,),
    )
    rows = cur.fetchall()

    phrase_counter: Counter = Counter()
    bigram_counter: Counter = Counter()

    for owner_feedback, adjustments_applied, sentiment in rows:
        # Combine both text fields for mining
        combined = " ".join(
            filter(None, [owner_feedback or "", adjustments_applied or ""])
        ).lower()

        if not combined.strip():
            continue

        # 1. Known phrase detection (case-insensitive substring match)
        for phrase in KNOWN_FAILURE_PHRASES:
            if phrase.lower() in combined:
                phrase_counter[phrase] += 1

        # 2. Bigram frequency on rejected feedback only (free-form discovery)
        if (sentiment or "").lower() in ("rejected", "fail", "bad"):
            words = re.findall(r"[a-z0-9\-]+", combined)
            clean = [w for w in words if w not in STOPWORDS and len(w) > 2]
            for i in range(len(clean) - 1):
                bigram = f"{clean[i]} {clean[i+1]}"
                bigram_counter[bigram] += 1

    return phrase_counter, bigram_counter


def build_candidate_rules(
    code_counter: Counter,
    phrase_counter: Counter,
    threshold: int = 3,
) -> list[str]:
    """Return candidate constraint strings that appear >= threshold times."""
    candidates: list[str] = []
    for code, count in code_counter.most_common():
        if count >= threshold:
            candidates.append(f"failure_code:{code} ({count}×) → add to feedback-catalog.json")
    for phrase, count in phrase_counter.most_common():
        if count >= threshold:
            candidates.append(
                f"keyword:'{phrase}' ({count}× in feedback) → review/harden in skills/"
            )
    return candidates


# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def build_report(
    today: str,
    gen_stats: dict,
    code_counter: Counter,
    phrase_counter: Counter,
    bigram_counter: Counter,
    threshold: int = 3,
) -> str:
    lines: list[str] = []
    lines.append(f"# Pattern Extractor Report — {today}")
    lines.append("")
    lines.append(
        "_Auto-generated by scripts/pattern-extractor.py. Human review required "
        "before promoting candidates to feedback-catalog.json or skills/._"
    )
    lines.append("")

    # --- Generation history stats ---
    lines.append("## Generation history (last 7 days)")
    lines.append("")
    lines.append(f"- Total: {gen_stats['total']}")
    lines.append(f"- Pass: {gen_stats['pass']}")
    lines.append(f"- Fail / rejected: {gen_stats['fail']}")
    lines.append(f"- Pending owner review: {gen_stats['pending']}")
    if gen_stats["other"] > 0:
        lines.append(f"- Other status: {gen_stats['other']}")
    lines.append("")

    # --- Structured failure codes ---
    lines.append("## Repeated failure codes (≥3×)")
    lines.append("")
    candidates_codes = [(c, n) for c, n in code_counter.most_common() if n >= threshold]
    if candidates_codes:
        for code, count in candidates_codes:
            lines.append(f"- `{code}`: {count}×")
    else:
        lines.append("- _None found — failure_codes column may be sparsely populated_")
    lines.append("")

    # --- Known-phrase hits in feedback text ---
    lines.append("## Known failure phrases in feedback_log (≥1 occurrence)")
    lines.append("")
    phrase_hits = [(p, n) for p, n in phrase_counter.most_common() if n >= 1]
    if phrase_hits:
        for phrase, count in phrase_hits:
            marker = " ← **candidate constraint**" if count >= threshold else ""
            lines.append(f"- \"{phrase}\": {count}×{marker}")
    else:
        lines.append("- _No known phrases found in feedback from this period_")
    lines.append("")

    # --- Free-form bigrams from rejected feedback ---
    lines.append("## Top bigrams from rejected feedback (free-form discovery)")
    lines.append("")
    top_bigrams = bigram_counter.most_common(20)
    if top_bigrams:
        for bigram, count in top_bigrams:
            lines.append(f"- \"{bigram}\": {count}×")
    else:
        lines.append("- _No rejected feedback rows in this period_")
    lines.append("")

    # --- Action summary ---
    lines.append("## Action: Review and promote to feedback-catalog.json + skills/")
    lines.append("")
    candidates = build_candidate_rules(code_counter, phrase_counter, threshold)
    if candidates:
        for rule in candidates:
            lines.append(f"- {rule}")
    else:
        lines.append(
            "- _No patterns met the ≥3× threshold this week. "
            "Check phrase hits above for manual promotion candidates._"
        )
    lines.append("")
    lines.append("---")
    lines.append(f"_Report generated: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}_")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(db_path: Path = DB, out_dir: Path = OUT_DIR, threshold: int = 3) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

    conn = connect(db_path)
    cur = conn.cursor()

    gen_stats = get_generation_stats(cur, week_ago)
    code_counter = count_repeated_failures(cur, week_ago)
    phrase_counter, bigram_counter = extract_keywords_from_feedback(cur, week_ago)

    conn.close()

    report_text = build_report(
        today, gen_stats, code_counter, phrase_counter, bigram_counter, threshold
    )

    report_path = out_dir / f"{today}.md"
    report_path.write_text(report_text, encoding="utf-8")

    # --- Stdout summary ---
    total_candidates = sum(
        1 for _, n in code_counter.items() if n >= threshold
    ) + sum(
        1 for _, n in phrase_counter.items() if n >= threshold
    )
    print(f"[pattern-extractor] {today}")
    print(f"  generations last 7d: total={gen_stats['total']} pass={gen_stats['pass']} "
          f"fail={gen_stats['fail']} pending={gen_stats['pending']}")
    print(f"  feedback phrases detected: {sum(phrase_counter.values())} hits "
          f"({len(phrase_counter)} unique phrases)")
    print(f"  candidate constraints (≥{threshold}×): {total_candidates}")
    print(f"  report → {report_path}")

    return report_path


if __name__ == "__main__":
    sys.exit(0) if main() else sys.exit(1)
