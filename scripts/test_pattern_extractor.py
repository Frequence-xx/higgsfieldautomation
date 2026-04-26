"""Unit tests for scripts/pattern-extractor.py

Uses in-memory SQLite — no live DB required.
Run: /opt/pipeline/venv/bin/python -m pytest scripts/test_pattern_extractor.py -v
"""

import sqlite3
import sys
import tempfile
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import pytest

# Allow importing from the scripts/ dir regardless of working directory
sys.path.insert(0, str(Path(__file__).parent))
from pattern_extractor import (
    build_candidate_rules,
    build_report,
    count_repeated_failures,
    extract_keywords_from_feedback,
    get_generation_stats,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_db() -> sqlite3.Connection:
    """Create a fresh in-memory SQLite DB with the pipeline schema."""
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE generation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brief_id INTEGER,
            shot_number INTEGER,
            prompt TEXT,
            model TEXT,
            settings_json TEXT,
            reference_image TEXT,
            qa_scores_json TEXT,
            pass_fail TEXT,
            failure_codes TEXT,
            improvement_suggestions TEXT,
            retry_count INTEGER DEFAULT 0,
            generation_method TEXT DEFAULT 'api',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE feedback_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER,
            owner_feedback TEXT,
            sentiment TEXT,
            adjustments_applied TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn


def _now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def _days_ago(n: int) -> str:
    return (datetime.utcnow() - timedelta(days=n)).strftime("%Y-%m-%d %H:%M:%S")


def _week_ago() -> str:
    return (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Tests: count_repeated_failures
# ---------------------------------------------------------------------------

class TestCountRepeatedFailures:
    def test_empty_table_returns_empty_counter(self):
        conn = _make_db()
        result = count_repeated_failures(conn.cursor(), _week_ago())
        assert result == Counter()

    def test_counts_single_failure_code(self):
        conn = _make_db()
        for _ in range(3):
            conn.execute(
                "INSERT INTO generation_history (pass_fail, failure_codes, created_at) VALUES (?, ?, ?)",
                ("rejected", "ghost_driving", _now()),
            )
        conn.commit()
        result = count_repeated_failures(conn.cursor(), _week_ago())
        assert result["ghost_driving"] == 3

    def test_counts_multiple_codes_per_row(self):
        conn = _make_db()
        conn.execute(
            "INSERT INTO generation_history (pass_fail, failure_codes, created_at) VALUES (?, ?, ?)",
            ("fail", "aspect_ratio,black_bars", _now()),
        )
        conn.execute(
            "INSERT INTO generation_history (pass_fail, failure_codes, created_at) VALUES (?, ?, ?)",
            ("fail", "aspect_ratio", _now()),
        )
        conn.commit()
        result = count_repeated_failures(conn.cursor(), _week_ago())
        assert result["aspect_ratio"] == 2
        assert result["black_bars"] == 1

    def test_ignores_pass_rows(self):
        conn = _make_db()
        conn.execute(
            "INSERT INTO generation_history (pass_fail, failure_codes, created_at) VALUES (?, ?, ?)",
            ("pass", "aspect_ratio", _now()),
        )
        conn.commit()
        result = count_repeated_failures(conn.cursor(), _week_ago())
        assert "aspect_ratio" not in result

    def test_ignores_rows_older_than_7_days(self):
        conn = _make_db()
        conn.execute(
            "INSERT INTO generation_history (pass_fail, failure_codes, created_at) VALUES (?, ?, ?)",
            ("rejected", "ghost_driving", _days_ago(10)),
        )
        conn.commit()
        result = count_repeated_failures(conn.cursor(), _week_ago())
        assert "ghost_driving" not in result

    def test_ignores_null_failure_codes(self):
        conn = _make_db()
        conn.execute(
            "INSERT INTO generation_history (pass_fail, failure_codes, created_at) VALUES (?, ?, ?)",
            ("rejected", None, _now()),
        )
        conn.commit()
        result = count_repeated_failures(conn.cursor(), _week_ago())
        assert result == Counter()

    def test_trims_whitespace_in_codes(self):
        conn = _make_db()
        conn.execute(
            "INSERT INTO generation_history (pass_fail, failure_codes, created_at) VALUES (?, ?, ?)",
            ("fail", " aspect_ratio , black_bars ", _now()),
        )
        conn.commit()
        result = count_repeated_failures(conn.cursor(), _week_ago())
        assert "aspect_ratio" in result
        assert "black_bars" in result


# ---------------------------------------------------------------------------
# Tests: extract_keywords_from_feedback
# ---------------------------------------------------------------------------

class TestExtractKeywordsFromFeedback:
    def test_empty_table_returns_empty_counters(self):
        conn = _make_db()
        phrase_counter, bigram_counter = extract_keywords_from_feedback(
            conn.cursor(), _week_ago()
        )
        assert phrase_counter == Counter()
        assert bigram_counter == Counter()

    def test_detects_known_phrase_in_owner_feedback(self):
        conn = _make_db()
        conn.execute(
            "INSERT INTO feedback_log (owner_feedback, sentiment, created_at) VALUES (?, ?, ?)",
            (
                "Issues: (1) black bars from aspect ratio padding, (2) choppy motion in shot 3",
                "rejected",
                _now(),
            ),
        )
        conn.commit()
        phrase_counter, _ = extract_keywords_from_feedback(conn.cursor(), _week_ago())
        assert phrase_counter["black bars"] >= 1
        assert phrase_counter["choppy motion"] >= 1
        assert phrase_counter["aspect ratio"] >= 1

    def test_detects_known_phrase_in_adjustments_applied(self):
        conn = _make_db()
        conn.execute(
            "INSERT INTO feedback_log (owner_feedback, adjustments_applied, sentiment, created_at) VALUES (?, ?, ?, ?)",
            (
                "Fine",
                "ghost driving still visible in truck shot. Side door visible.",
                "rejected",
                _now(),
            ),
        )
        conn.commit()
        phrase_counter, _ = extract_keywords_from_feedback(conn.cursor(), _week_ago())
        assert phrase_counter["ghost driving"] >= 1
        assert phrase_counter["side door"] >= 1

    def test_bigram_extraction_from_rejected_only(self):
        conn = _make_db()
        # Rejected row — should contribute to bigrams
        conn.execute(
            "INSERT INTO feedback_log (owner_feedback, sentiment, created_at) VALUES (?, ?, ?)",
            ("face warp visible on close-up shot", "rejected", _now()),
        )
        # Approved row — should NOT contribute to bigrams
        conn.execute(
            "INSERT INTO feedback_log (owner_feedback, sentiment, created_at) VALUES (?, ?, ?)",
            ("face warp visible on close-up shot", "approved", _now()),
        )
        conn.commit()
        _, bigram_counter = extract_keywords_from_feedback(conn.cursor(), _week_ago())
        # Bigram "face warp" should appear exactly once (only from rejected row)
        assert bigram_counter["face warp"] == 1

    def test_ignores_rows_older_than_7_days(self):
        conn = _make_db()
        conn.execute(
            "INSERT INTO feedback_log (owner_feedback, sentiment, created_at) VALUES (?, ?, ?)",
            ("black bars visible", "rejected", _days_ago(10)),
        )
        conn.commit()
        phrase_counter, _ = extract_keywords_from_feedback(conn.cursor(), _week_ago())
        assert phrase_counter["black bars"] == 0

    def test_handles_none_text_fields_gracefully(self):
        conn = _make_db()
        conn.execute(
            "INSERT INTO feedback_log (owner_feedback, adjustments_applied, sentiment, created_at) VALUES (?, ?, ?, ?)",
            (None, None, "rejected", _now()),
        )
        conn.commit()
        phrase_counter, bigram_counter = extract_keywords_from_feedback(
            conn.cursor(), _week_ago()
        )
        assert phrase_counter == Counter()
        assert bigram_counter == Counter()


# ---------------------------------------------------------------------------
# Tests: get_generation_stats
# ---------------------------------------------------------------------------

class TestGetGenerationStats:
    def test_empty_table(self):
        conn = _make_db()
        stats = get_generation_stats(conn.cursor(), _week_ago())
        assert stats["total"] == 0
        assert stats["pass"] == 0
        assert stats["fail"] == 0
        assert stats["pending"] == 0

    def test_counts_pass_and_fail(self):
        conn = _make_db()
        for _ in range(4):
            conn.execute(
                "INSERT INTO generation_history (pass_fail, created_at) VALUES (?, ?)",
                ("pass", _now()),
            )
        for _ in range(2):
            conn.execute(
                "INSERT INTO generation_history (pass_fail, created_at) VALUES (?, ?)",
                ("rejected", _now()),
            )
        conn.execute(
            "INSERT INTO generation_history (pass_fail, created_at) VALUES (?, ?)",
            ("pending_owner_review", _now()),
        )
        conn.commit()
        stats = get_generation_stats(conn.cursor(), _week_ago())
        assert stats["total"] == 7
        assert stats["pass"] == 4
        assert stats["fail"] == 2
        assert stats["pending"] == 1


# ---------------------------------------------------------------------------
# Tests: build_candidate_rules
# ---------------------------------------------------------------------------

class TestBuildCandidateRules:
    def test_no_candidates_when_below_threshold(self):
        result = build_candidate_rules(
            Counter({"aspect_ratio": 2}),
            Counter({"black bars": 1}),
            threshold=3,
        )
        assert result == []

    def test_returns_candidate_for_code_at_threshold(self):
        result = build_candidate_rules(
            Counter({"ghost_driving": 3}),
            Counter(),
            threshold=3,
        )
        assert len(result) == 1
        assert "ghost_driving" in result[0]
        assert "3×" in result[0]

    def test_returns_candidate_for_phrase_at_threshold(self):
        result = build_candidate_rules(
            Counter(),
            Counter({"black bars": 4}),
            threshold=3,
        )
        assert len(result) == 1
        assert "black bars" in result[0]

    def test_returns_candidates_sorted_by_frequency(self):
        result = build_candidate_rules(
            Counter({"a": 5, "b": 3}),
            Counter(),
            threshold=3,
        )
        assert "a" in result[0]  # highest count first
        assert "b" in result[1]


# ---------------------------------------------------------------------------
# Integration: build_report renders valid markdown
# ---------------------------------------------------------------------------

class TestBuildReport:
    def test_report_contains_required_sections(self):
        report = build_report(
            today="2026-04-17",
            gen_stats={"total": 10, "pass": 7, "fail": 2, "pending": 1, "other": 0},
            code_counter=Counter({"ghost_driving": 3}),
            phrase_counter=Counter({"black bars": 4}),
            bigram_counter=Counter({"face warp": 2}),
            threshold=3,
        )
        assert "# Pattern Extractor Report" in report
        assert "## Generation history" in report
        assert "## Repeated failure codes" in report
        assert "## Known failure phrases" in report
        assert "## Top bigrams" in report
        assert "## Action" in report

    def test_report_shows_candidate_marker_above_threshold(self):
        report = build_report(
            today="2026-04-17",
            gen_stats={"total": 5, "pass": 2, "fail": 3, "pending": 0, "other": 0},
            code_counter=Counter(),
            phrase_counter=Counter({"black bars": 3}),
            bigram_counter=Counter(),
            threshold=3,
        )
        assert "candidate constraint" in report

    def test_report_shows_no_findings_message_when_empty(self):
        report = build_report(
            today="2026-04-17",
            gen_stats={"total": 0, "pass": 0, "fail": 0, "pending": 0, "other": 0},
            code_counter=Counter(),
            phrase_counter=Counter(),
            bigram_counter=Counter(),
            threshold=3,
        )
        assert "No patterns met" in report


# ---------------------------------------------------------------------------
# Integration: main() writes file and returns path
# ---------------------------------------------------------------------------

class TestMainWritesFile:
    def test_main_writes_report_file(self, tmp_path):
        """main() should write a .md file even when DB has no data."""
        from pattern_extractor import main

        db_path = tmp_path / "test.db"
        conn = _make_db()
        # Save in-memory DB to file so main() can connect
        import shutil
        conn.execute("VACUUM INTO ?", (str(db_path),))
        conn.close()

        out_dir = tmp_path / "patterns"
        report_path = main(db_path=db_path, out_dir=out_dir)

        assert report_path.exists()
        assert report_path.suffix == ".md"
        content = report_path.read_text()
        assert "# Pattern Extractor Report" in content
