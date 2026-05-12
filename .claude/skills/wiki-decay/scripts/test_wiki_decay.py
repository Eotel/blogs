"""Tests for wiki_decay.py.

Uses a fixture wiki tree with frozen ``--as-of`` so age math is deterministic.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from wiki_decay import (
    DEFAULT_THRESHOLDS,
    DecayEntry,
    main,
    score_pages,
    to_markdown,
)


def _write_page(root: Path, section: str, slug: str, lastmod: str | None) -> Path:
    page = root / "content" / "wiki" / section / f"{slug}.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    fm_lines = [f'title: "{slug}"']
    if lastmod is not None:
        fm_lines.append(f"date: {lastmod}")
        fm_lines.append(f"lastmod: {lastmod}")
    fm = "\n".join(fm_lines)
    page.write_text(f"---\n{fm}\n---\n\nbody\n", encoding="utf-8")
    return page


@pytest.fixture()
def wiki_root(tmp_path: Path) -> Path:
    # Required by find_repo_root.
    (tmp_path / "content" / "wiki").mkdir(parents=True)
    (tmp_path / "content" / "posts").mkdir(parents=True)
    return tmp_path


def test_scores_three_tiers_by_age(wiki_root: Path) -> None:
    _write_page(wiki_root, "tools", "fresh-tool", "2026-08-01")  # age 14d
    _write_page(
        wiki_root, "tools", "warming-tool", "2026-07-01"
    )  # age 45d -> exactly soft
    _write_page(wiki_root, "tools", "stale-tool", "2026-04-01")  # age 136d > hard 90

    entries = score_pages(wiki_root, as_of=date(2026, 8, 15))
    assert [e.path.split("/")[-1] for e in entries[:3]] == [
        "stale-tool.md",
        "warming-tool.md",
        "fresh-tool.md",
    ]
    assert entries[0].status == "stale"
    assert entries[0].score == pytest.approx(1.0)
    assert entries[1].status == "warming"
    assert entries[2].status == "fresh"
    assert entries[2].score == pytest.approx(0.0)


def test_section_thresholds_differ(wiki_root: Path) -> None:
    # All three pages at 100 days old vs as-of 2026-08-15: stale for tools
    # (>90), warming for guides (>75 but <150), fresh for concepts (<150).
    lastmod = "2026-05-07"
    _write_page(wiki_root, "tools", "t", lastmod)
    _write_page(wiki_root, "guides", "g", lastmod)
    _write_page(wiki_root, "concepts", "c", lastmod)

    entries = {e.section: e for e in score_pages(wiki_root, as_of=date(2026, 8, 15))}
    assert entries["tools"].status == "stale"
    assert entries["guides"].status == "warming"
    assert entries["concepts"].status == "fresh"


def test_missing_lastmod_treated_as_max_stale(wiki_root: Path) -> None:
    _write_page(wiki_root, "tools", "no-date", lastmod=None)

    entries = score_pages(wiki_root, as_of=date(2026, 8, 15))
    assert len(entries) == 1
    assert entries[0].status == "stale"
    assert entries[0].score == pytest.approx(1.0)
    assert entries[0].lastmod == ""


def test_index_md_is_ignored(wiki_root: Path) -> None:
    section_dir = wiki_root / "content" / "wiki" / "tools"
    section_dir.mkdir(parents=True)
    (section_dir / "_index.md").write_text(
        "---\ntitle: Tools\n---\n",
        encoding="utf-8",
    )
    entries = score_pages(wiki_root, as_of=date(2026, 8, 15))
    assert entries == []


def test_custom_thresholds_override(wiki_root: Path) -> None:
    _write_page(wiki_root, "tools", "p", "2026-08-01")  # age 14d
    entries = score_pages(
        wiki_root,
        as_of=date(2026, 8, 15),
        thresholds={"tools": (7, 10), "guides": (0, 1), "concepts": (0, 1)},
    )
    assert entries[0].status == "stale"


def test_markdown_renders_section_headers(wiki_root: Path) -> None:
    _write_page(wiki_root, "tools", "stale-tool", "2026-04-01")
    _write_page(wiki_root, "concepts", "fresh-concept", "2026-08-10")

    entries = score_pages(wiki_root, as_of=date(2026, 8, 15))
    md = to_markdown(entries, top=10, as_of=date(2026, 8, 15))
    assert "### tools/" in md
    assert "### guides/" in md
    assert "### concepts/" in md
    assert "🔴 stale" in md
    assert "なし (全 page 健全)" in md  # concepts section is healthy
    assert "stale: 1" in md
    assert "pages scanned: 2" in md


def test_main_json_output(wiki_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_page(wiki_root, "tools", "stale-tool", "2026-04-01")
    rc = main(["--json", "--as-of", "2026-08-15", "--root", str(wiki_root)])
    assert rc == 0
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["as_of"] == "2026-08-15"
    assert payload["thresholds"]["tools"] == {"soft": 45, "hard": 90}
    assert len(payload["entries"]) == 1
    assert payload["entries"][0]["status"] == "stale"


def test_default_thresholds_constants() -> None:
    # Guard against accidental edits to the documented contract.
    assert DEFAULT_THRESHOLDS["tools"] == (45, 90)
    assert DEFAULT_THRESHOLDS["guides"] == (75, 150)
    assert DEFAULT_THRESHOLDS["concepts"] == (150, 300)


def test_decay_entry_is_frozen() -> None:
    e = DecayEntry(
        section="tools",
        path="content/wiki/tools/x.md",
        title="x",
        lastmod="2026-04-01",
        age_days=136,
        soft=45,
        hard=90,
        score=1.0,
        status="stale",
        refresh_command="/wiki-decay refresh tools/x",
    )
    with pytest.raises(Exception):
        # frozen=True dataclass — runtime FrozenInstanceError.
        setattr(e, "score", 0.5)
