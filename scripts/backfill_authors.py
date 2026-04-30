#!/usr/bin/env python3
"""Backfill `author: <id>` into existing post frontmatter.

All historical posts in this repo were imported from hdknr's gists, so the
default author is `hdknr`. Posts that already declare an author are left
untouched.

Usage:
    python scripts/backfill_authors.py                    # dry-run
    python scripts/backfill_authors.py --apply            # write changes
    python scripts/backfill_authors.py --apply --default eotel
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "content" / "posts"
AUTHORS_FILE = ROOT / "scripts" / "authors.json"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)\Z", re.DOTALL)


def load_author_ids() -> set[str]:
    data = json.loads(AUTHORS_FILE.read_text(encoding="utf-8"))
    return {a["id"] for a in data["authors"]}


def split_frontmatter(text: str) -> tuple[str, str] | None:
    m = FRONTMATTER_RE.match(text)
    return (m.group(1), m.group(2)) if m else None


def has_author(fm_text: str) -> bool:
    """True iff frontmatter has a non-empty top-level `author` field."""
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        return bool(re.search(r"(?m)^author:\s*\S", fm_text))
    if not isinstance(data, dict):
        return False
    val = data.get("author")
    return val is not None and str(val).strip() != ""


def insert_author(fm_text: str, author_id: str) -> str:
    """Insert `author: "<id>"` after `draft:`, falling back to `lastmod:` /
    `date:`, or appending to the end of the frontmatter."""
    line = f'author: "{author_id}"'
    for anchor in (r"(?m)^draft:.*$", r"(?m)^lastmod:.*$", r"(?m)^date:.*$"):
        m = re.search(anchor, fm_text)
        if m:
            return fm_text[: m.end()] + "\n" + line + fm_text[m.end():]
    return fm_text.rstrip() + "\n" + line


def process(filepath: Path, default_id: str, apply: bool) -> str:
    text = filepath.read_text(encoding="utf-8")
    split = split_frontmatter(text)
    if split is None:
        return "no-frontmatter"
    fm_text, body = split

    if has_author(fm_text):
        return "already-set"

    new_fm = insert_author(fm_text, default_id)
    if not apply:
        return "would-update"

    filepath.write_text(f"---\n{new_fm}\n---\n{body}", encoding="utf-8")
    return "updated"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--default", default="hdknr",
                        help="default author id when missing (must exist in authors.json)")
    parser.add_argument("--apply", action="store_true",
                        help="write changes; without this flag the script is a dry-run")
    args = parser.parse_args()

    if not POSTS_DIR.is_dir():
        print(f"posts directory not found: {POSTS_DIR}", file=sys.stderr)
        return 1
    if not AUTHORS_FILE.is_file():
        print(f"authors config not found: {AUTHORS_FILE}", file=sys.stderr)
        return 1

    valid_ids = load_author_ids()
    if args.default not in valid_ids:
        print(f"--default '{args.default}' is not in {AUTHORS_FILE} "
              f"(valid: {sorted(valid_ids)})", file=sys.stderr)
        return 1

    counts: dict[str, int] = {}
    for path in sorted(POSTS_DIR.rglob("*.md")):
        if path.name == "_index.md":
            continue
        result = process(path, args.default, args.apply)
        counts[result] = counts.get(result, 0) + 1

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"[{mode}] default author = {args.default!r}")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
