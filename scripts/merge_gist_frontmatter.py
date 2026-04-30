#!/usr/bin/env python3
"""Merge a gist's optional inline frontmatter with auto-generated metadata.

Reads the raw gist file contents from stdin and prints the final Hugo post
(frontmatter + body) to stdout. Used by ``scripts/import-gists.sh``.

Merge rules
-----------
- ``date``, ``lastmod``, ``author``, ``gist_id``, ``gist_url``, ``gist_file``
  come from CLI flags (auto-generated, system of record).
- All other keys come from the gist's inline frontmatter when present.
- ``title`` precedence: gist frontmatter > gist description > first H1 > basename.
- ``draft`` defaults to ``false`` if the gist did not set it.
- ``categories`` and ``tags`` default to empty lists; ``categorize.py`` fills
  them later when empty.
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import Any

import yaml

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
HEADING_RE = re.compile(r"^#+\s*(.+?)\s*$", re.MULTILINE)

SYSTEM_FIELDS = ("date", "lastmod", "author", "gist_id", "gist_url", "gist_file")


def split_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Return ``(frontmatter_dict, body)``.

    If the gist file has no inline frontmatter, returns ``({}, content)``.
    """
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}, content
    raw, body = match.group(1), match.group(2)
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return {}, content
    if not isinstance(loaded, dict):
        return {}, content
    return loaded, body


def first_heading(body: str) -> str | None:
    match = HEADING_RE.search(body)
    return match.group(1) if match else None


def strip_first_heading(body: str) -> str:
    """Remove the first H1/H2/... line so the rendered post does not duplicate
    the title that lives in the frontmatter."""
    return HEADING_RE.sub("", body, count=1).lstrip("\n")


def resolve_title(
    gist_fm: dict[str, Any],
    description: str,
    heading: str | None,
    basename: str,
) -> str:
    if gist_fm.get("title"):
        return str(gist_fm["title"])
    if description and description != basename:
        return description
    if heading:
        return heading
    return basename


def build_merged(
    gist_fm: dict[str, Any],
    args: argparse.Namespace,
    heading: str | None,
) -> dict[str, Any]:
    merged: dict[str, Any] = dict(gist_fm)
    merged["title"] = resolve_title(gist_fm, args.description, heading, args.basename)
    merged.setdefault("draft", False)
    merged.setdefault("categories", [])
    merged.setdefault("tags", [])
    for field in SYSTEM_FIELDS:
        merged[field] = getattr(args, field.replace("-", "_"))
    return merged


def order_keys(merged: dict[str, Any]) -> dict[str, Any]:
    """Stable, human-friendly ordering for the rendered frontmatter."""
    preferred = [
        "title", "date", "lastmod", "draft", "author",
        "gist_id", "gist_url", "gist_file",
        "description", "aliases", "source_url",
        "categories", "tags",
    ]
    ordered: dict[str, Any] = {}
    for key in preferred:
        if key in merged:
            ordered[key] = merged[key]
    for key, value in merged.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def render(merged: dict[str, Any], body: str) -> str:
    yaml_text = yaml.safe_dump(
        merged,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    ).rstrip()
    body_clean = body.lstrip("\n")
    return f"---\n{yaml_text}\n---\n\n{body_clean}\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gist-id", required=True)
    parser.add_argument("--gist-url", required=True)
    parser.add_argument("--gist-file", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--lastmod", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--basename", default="")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    raw = sys.stdin.read()

    gist_fm, body = split_frontmatter(raw)

    heading = first_heading(body)
    if not gist_fm and heading:
        body = strip_first_heading(body)

    merged = order_keys(build_merged(gist_fm, args, heading))
    sys.stdout.write(render(merged, body))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
