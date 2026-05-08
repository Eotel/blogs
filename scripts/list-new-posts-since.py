#!/usr/bin/env python3
"""List post paths whose frontmatter `date:` is strictly after the given YYYY-MM-DD.

Used by .github/workflows/auto-wiki-ingest.yml to determine which posts
should be processed by /wiki-ingest in each weekly run.

The watermark file `.claude/wiki-last-ingest.txt` stores the date of the
last successful ingest; this script lists posts whose frontmatter date is
strictly greater (`>`) than that watermark, so posts already covered by the
previous run are not reprocessed.

Limitation: posts whose frontmatter `date:` is older than the watermark
but were committed after it (backdated posts, migrations) will not be
picked up. Run with `workflow_dispatch` and a manually adjusted watermark
when this happens.

Usage:
    python scripts/list-new-posts-since.py 2026-04-15
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DATE_RE = re.compile(r'^date:\s*"?(\d{4}-\d{2}-\d{2})', re.M)
# Resolve relative to this file so the script works from any cwd
# (matches the pattern used by scripts/categorize.py, scripts/backfill_authors.py).
REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_ROOT = REPO_ROOT / "content" / "posts"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: list-new-posts-since.py YYYY-MM-DD", file=sys.stderr)
        return 1
    since = sys.argv[1]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", since):
        print(f"Invalid date format: {since!r} (expected YYYY-MM-DD)", file=sys.stderr)
        return 1
    if not POSTS_ROOT.exists():
        return 0
    for path in sorted(POSTS_ROOT.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
            continue
        match = DATE_RE.search(text)
        if match and match.group(1) > since:
            print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
