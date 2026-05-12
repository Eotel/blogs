#!/usr/bin/env python3
"""Wiki content decay detector.

Ranks `content/wiki/{concepts,tools,guides}/*.md` pages by how stale they are,
based purely on frontmatter `lastmod`. Section-tiered thresholds reflect how
fast each kind of knowledge decays:

- ``tools/``   soft  45d / hard  90d  — version churn (CLI flags, pricing)
- ``guides/``  soft  75d / hard 150d  — procedure drift
- ``concepts/`` soft 150d / hard 300d — abstract knowledge ages slowest

A page is *warming* when ``age > soft`` and *stale* when ``age > hard``.
``score = clamp((age - soft) / (hard - soft), 0, 1)`` is used to rank.

Designed for two consumers:

- Weekly cron (``.github/workflows/wiki-decay-report.yml``) — emits a markdown
  report that ``gh issue create`` posts to the repo for the operator to triage.
- ``wiki_lint.py`` — imports :func:`score_pages` to append a non-blocking
  advisory section to its existing health report.

Usage::

  wiki_decay.py                            # markdown report (top 10 / section)
  wiki_decay.py --json                     # machine-readable
  wiki_decay.py --top 5 --as-of 2026-09-01 # simulate future date
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

# Reuse wiki_lint helpers to avoid duplicating the YAML-ish parser and the
# repo-root walk. wiki-decay is a sibling skill, so we mutate sys.path to
# import it without packaging either as a real Python package.
_HERE = Path(__file__).resolve()
_WIKI_LINT_SCRIPTS = _HERE.parents[2] / "wiki-lint" / "scripts"
sys.path.insert(0, str(_WIKI_LINT_SCRIPTS))
from wiki_lint import find_repo_root, parse_date, parse_frontmatter  # noqa: E402

# Section-tiered thresholds (days). See module docstring for rationale.
DEFAULT_THRESHOLDS: dict[str, tuple[int, int]] = {
    "tools": (45, 90),
    "guides": (75, 150),
    "concepts": (150, 300),
}

DEFAULT_TOP = 10


@dataclass(frozen=True)
class DecayEntry:
    section: str
    path: str  # relative to repo root
    title: str
    lastmod: str  # ISO date, may be "" if missing
    age_days: int
    soft: int
    hard: int
    score: float  # 0.0 (fresh) .. 1.0 (well past hard threshold)
    status: str  # "fresh" | "warming" | "stale"
    refresh_command: str


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _score(age: int, soft: int, hard: int) -> float:
    if hard <= soft:
        return 1.0 if age >= hard else 0.0
    return _clamp((age - soft) / (hard - soft), 0.0, 1.0)


def _status(age: int, soft: int, hard: int) -> str:
    if age >= hard:
        return "stale"
    if age >= soft:
        return "warming"
    return "fresh"


def score_pages(
    root: Path,
    *,
    as_of: date,
    thresholds: dict[str, tuple[int, int]] | None = None,
) -> list[DecayEntry]:
    """Return decay entries for every wiki page, sorted by score desc."""
    thr = thresholds or DEFAULT_THRESHOLDS
    wiki_dir = root / "content" / "wiki"
    entries: list[DecayEntry] = []
    for section, (soft, hard) in thr.items():
        section_dir = wiki_dir / section
        if not section_dir.is_dir():
            continue
        for path in sorted(section_dir.rglob("*.md")):
            if path.name == "_index.md":
                continue
            try:
                fm = parse_frontmatter(path.read_text(encoding="utf-8"))
            except OSError:
                continue
            lastmod_raw = fm.get("lastmod") or fm.get("date") or ""
            lastmod_date = parse_date(
                lastmod_raw if isinstance(lastmod_raw, str) else None
            )
            if lastmod_date is None:
                # Missing or unparseable date — treat as maximally stale so
                # the operator notices and either backfills or removes.
                age = (as_of - date.min).days
                lastmod_iso = ""
            else:
                age = (as_of - lastmod_date).days
                lastmod_iso = lastmod_date.isoformat()
            rel = path.relative_to(root)
            slug = path.stem
            entries.append(
                DecayEntry(
                    section=section,
                    path=str(rel),
                    title=str(fm.get("title") or slug).strip(),
                    lastmod=lastmod_iso,
                    age_days=age,
                    soft=soft,
                    hard=hard,
                    score=_score(age, soft, hard),
                    status=_status(age, soft, hard),
                    refresh_command=f"/wiki-decay refresh {section}/{slug}",
                )
            )
    entries.sort(key=lambda e: (-e.score, -e.age_days, e.path))
    return entries


def to_markdown(entries: list[DecayEntry], top: int, as_of: date) -> str:
    """Render entries as a sectioned markdown report.

    Only ``warming`` + ``stale`` entries surface; ``fresh`` are summarized as
    a count at the bottom of each section.
    """
    lines: list[str] = [
        f"## Wiki Decay Report ({as_of.isoformat()})",
        "",
        "wiki ページの `lastmod` を section 別の閾値で評価し、touch されずに古びた候補を浮かせる。",
        "閾値は `tools/` 45/90d, `guides/` 75/150d, `concepts/` 150/300d (soft/hard)。",
        "",
    ]
    by_section: dict[str, list[DecayEntry]] = {}
    for e in entries:
        by_section.setdefault(e.section, []).append(e)
    total_warming = 0
    total_stale = 0
    for section in ("tools", "guides", "concepts"):
        section_entries = by_section.get(section, [])
        warming = [e for e in section_entries if e.status == "warming"]
        stale = [e for e in section_entries if e.status == "stale"]
        total_warming += len(warming)
        total_stale += len(stale)
        fresh = len(section_entries) - len(warming) - len(stale)
        lines.append(
            f"### {section}/ — stale {len(stale)} / warming {len(warming)} / fresh {fresh}"
        )
        surfaced = (stale + warming)[:top]
        if not surfaced:
            lines.append("- なし (全 page 健全)")
        else:
            for e in surfaced:
                badge = "🔴 stale" if e.status == "stale" else "🟡 warming"
                lines.append(
                    f"- {badge} `{e.path}` — age {e.age_days}d (lastmod {e.lastmod or 'unknown'}) "
                    f"score {e.score:.2f} — `{e.refresh_command}`"
                )
        lines.append("")
    lines.append("### Totals")
    lines.append(f"- stale: {total_stale}")
    lines.append(f"- warming: {total_warming}")
    lines.append(f"- pages scanned: {len(entries)}")
    return "\n".join(lines) + "\n"


def to_json(entries: list[DecayEntry], as_of: date) -> str:
    return json.dumps(
        {
            "as_of": as_of.isoformat(),
            "thresholds": {
                k: {"soft": s, "hard": h} for k, (s, h) in DEFAULT_THRESHOLDS.items()
            },
            "entries": [asdict(e) for e in entries],
        },
        ensure_ascii=False,
        indent=2,
    )


def _parse_as_of(value: str | None) -> date:
    if not value:
        return date.today()
    parsed = parse_date(value)
    if parsed is None:
        raise SystemExit(f"--as-of: invalid date {value!r}")
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Emit JSON (default: markdown)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=DEFAULT_TOP,
        help="entries per section (markdown only)",
    )
    parser.add_argument("--as-of", help="evaluate decay as if today were YYYY-MM-DD")
    parser.add_argument("--root", help="repo root (default: auto-detect)")
    parser.add_argument(
        "--threshold-tools",
        type=int,
        nargs=2,
        metavar=("SOFT", "HARD"),
        help="override tools/ thresholds",
    )
    parser.add_argument(
        "--threshold-guides",
        type=int,
        nargs=2,
        metavar=("SOFT", "HARD"),
        help="override guides/ thresholds",
    )
    parser.add_argument(
        "--threshold-concepts",
        type=int,
        nargs=2,
        metavar=("SOFT", "HARD"),
        help="override concepts/ thresholds",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else find_repo_root(_HERE)
    as_of = _parse_as_of(args.as_of)
    thresholds = dict(DEFAULT_THRESHOLDS)
    if args.threshold_tools:
        thresholds["tools"] = tuple(args.threshold_tools)  # type: ignore[assignment]
    if args.threshold_guides:
        thresholds["guides"] = tuple(args.threshold_guides)  # type: ignore[assignment]
    if args.threshold_concepts:
        thresholds["concepts"] = tuple(args.threshold_concepts)  # type: ignore[assignment]

    entries = score_pages(root, as_of=as_of, thresholds=thresholds)

    if args.as_json:
        print(to_json(entries, as_of))
    else:
        print(to_markdown(entries, args.top, as_of), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
