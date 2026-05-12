#!/usr/bin/env python3
"""Re-scan posts listed in wiki-ingest-backlog-*.md against the current wiki.

Reuses wiki_ingest_plan.plan_post() so the scoring is identical to the regular
ingest pipeline. Emits only posts whose top candidate score has reached the
promotion threshold (default >=70), i.e. update_candidate.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from wiki_ingest_plan import (  # noqa: E402
    DEFAULT_LIMIT,
    PostDoc,
    WikiDoc,
    ensure_fts,
    find_repo_root,
    load_posts,
    load_wiki_docs,
    parse_frontmatter,
    plan_post,
)

BACKLOG_FILE_RE = re.compile(
    r"^wiki-ingest-backlog-(?P<year>\d{4}|root)-(?P<status>review_candidate|new_candidate)\.md$"
)


def is_backlog_wiki(wiki: WikiDoc) -> bool:
    """The backlog index and its shards live under guides/ and start with
    `wiki-ingest-backlog`. Exclude them from scoring/coverage so backlog
    entries are evaluated against *real* destination wiki pages only."""
    return wiki.section == "guides" and wiki.slug.startswith("wiki-ingest-backlog")


def collect_backlog_entries(
    root: Path,
    year_filter: str | None,
    status_filter: str | None,
) -> list[tuple[str, str, str]]:
    """Return list of (post_url, year_bucket, status) parsed from backlog shards."""
    backlog_dir = root / "content" / "wiki" / "guides"
    entries: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for path in sorted(backlog_dir.glob("wiki-ingest-backlog-*.md")):
        match = BACKLOG_FILE_RE.match(path.name)
        if not match:
            continue
        year_bucket = match.group("year")
        status = match.group("status")
        if year_filter is not None and year_bucket != year_filter:
            continue
        if status_filter is not None and status != status_filter:
            continue
        text = path.read_text(encoding="utf-8")
        fm, _body = parse_frontmatter(text)
        related = fm.get("related_posts")
        if not isinstance(related, list):
            continue
        for url in related:
            url = str(url).strip().strip('"').strip("'")
            if not url:
                continue
            if url in seen:
                continue
            seen.add(url)
            entries.append((url, year_bucket, status))
    return entries


def build_url_index(posts: list[PostDoc]) -> dict[str, PostDoc]:
    index: dict[str, PostDoc] = {}
    for post in posts:
        index[post.url] = post
        for alt in post.alt_urls:
            index.setdefault(alt, post)
    return index


def rescan(
    root: Path,
    min_score: int,
    year_filter: str | None,
    status_filter: str | None,
    limit: int,
    cap: int | None,
) -> dict[str, Any]:
    all_wiki_docs: list[WikiDoc] = load_wiki_docs(root)
    wiki_docs: list[WikiDoc] = [w for w in all_wiki_docs if not is_backlog_wiki(w)]
    posts: list[PostDoc] = load_posts(root)
    url_to_post = build_url_index(posts)
    db_path = ensure_fts(root, wiki_docs)
    related_index: dict[str, list[WikiDoc]] = {}
    for wiki in wiki_docs:
        for ref in wiki.related_posts:
            related_index.setdefault(ref, []).append(wiki)

    backlog_entries = collect_backlog_entries(root, year_filter, status_filter)
    candidates_out: list[dict[str, Any]] = []
    not_resolved: list[dict[str, str]] = []
    promoted = 0
    still_low = 0
    now_covered = 0

    for url, year_bucket, status in backlog_entries:
        post = url_to_post.get(url)
        if post is None:
            not_resolved.append(
                {"post_url": url, "from_backlog": f"{year_bucket}/{status}"}
            )
            continue
        plan = plan_post(post, wiki_docs, related_index, db_path, limit)
        new_status = plan["status"]
        top = plan["candidates"][0] if plan["candidates"] else None
        top_score = top["score"] if top else 0
        if new_status in ("covered", "stale_candidate"):
            now_covered += 1
            continue
        if top_score < min_score:
            still_low += 1
            continue
        promoted += 1
        candidates_out.append(
            {
                "post": post.rel_path,
                "post_url": post.url,
                "title": post.title,
                "date": post.date.isoformat() if post.date else None,
                "current_status": status,
                "backlog_year": year_bucket,
                "promoted_to": new_status,
                "score": top_score,
                "best_target": top["wiki"] if top else None,
                "best_target_url": top["wiki_url"] if top else None,
                "reasons": top["reasons"] if top else [],
                "alt_candidates": plan["candidates"][1:5],
            }
        )

    candidates_out.sort(key=lambda c: (-c["score"], c["post"]))
    if cap is not None:
        candidates_out = candidates_out[:cap]

    return {
        "scanned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "wiki_pages": len(wiki_docs),
        "posts_in_repo": len(posts),
        "backlog_entries": len(backlog_entries),
        "filters": {
            "year": year_filter,
            "status": status_filter,
            "min_score": min_score,
        },
        "stats": {
            "checked": len(backlog_entries),
            "promoted": promoted,
            "still_low": still_low,
            "now_covered": now_covered,
            "not_resolved": len(not_resolved),
        },
        "candidates": candidates_out,
        "not_resolved": not_resolved,
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "## Wiki Backlog Rescan",
        "",
        f"- scanned_at: `{report['scanned_at']}`",
        f"- wiki_pages: {report['wiki_pages']}",
        f"- backlog_entries: {report['backlog_entries']}",
        f"- filters: `{report['filters']}`",
        "",
        "### Stats",
    ]
    for key, value in report["stats"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "### Promoted Candidates"])
    if not report["candidates"]:
        lines.append("- (none)")
    for cand in report["candidates"]:
        lines.append(
            f"- `{cand['post']}` — **{cand['promoted_to']}** "
            f"(score {cand['score']}, was {cand['current_status']})"
        )
        lines.append(f"  - title: {cand['title']}")
        lines.append(f"  - target: `{cand['best_target']}`")
        if cand["reasons"]:
            lines.append(f"  - reasons: {'; '.join(cand['reasons'])}")
    if report["not_resolved"]:
        lines.extend(["", "### Unresolved URLs"])
        for entry in report["not_resolved"][:20]:
            lines.append(f"- `{entry['post_url']}` (from {entry['from_backlog']})")
        if len(report["not_resolved"]) > 20:
            lines.append(f"- ... and {len(report['not_resolved']) - 20} more")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Re-scan posts listed in wiki-ingest-backlog-*.md against the current wiki "
            "and report those that have promoted to update_candidate (score>=70 by default)."
        )
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=70,
        help="Only output posts whose top candidate score >= this threshold (default 70).",
    )
    parser.add_argument(
        "--year",
        help="Filter by backlog year bucket (e.g. 2014, 2026, root).",
    )
    parser.add_argument(
        "--status",
        choices=["review_candidate", "new_candidate"],
        help="Filter by original backlog status.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help="Per-post candidate limit passed through to plan_post (default 5).",
    )
    parser.add_argument(
        "--cap",
        type=int,
        help="Cap the total number of promoted candidates in the output.",
    )
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--root", help=argparse.SUPPRESS)
    args = parser.parse_args()

    root = (
        Path(args.root).resolve()
        if args.root
        else find_repo_root(Path(__file__).resolve())
    )
    report = rescan(
        root=root,
        min_score=args.min_score,
        year_filter=args.year,
        status_filter=args.status,
        limit=max(1, args.limit),
        cap=args.cap,
    )
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(markdown(report), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
