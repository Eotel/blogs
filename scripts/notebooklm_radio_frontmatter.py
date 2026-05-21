#!/usr/bin/env -S uv run --quiet --no-project --with PyYAML>=6 python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML>=6"]
# ///
"""Patch a Hugo post's YAML frontmatter with audio_* keys.

Called from `scripts/notebooklm-radio.sh` after the NotebookLM audio overview
is downloaded. Existing values are preserved — we only fill in keys that are
absent. This avoids clobbering manually-tuned audio metadata when a user
re-runs the script with --force.

Run via `uv run scripts/notebooklm_radio_frontmatter.py ...` so PyYAML is
resolved without depending on a project venv.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def split_frontmatter(text: str) -> tuple[dict, str, str]:
    """Return (frontmatter_dict, body, raw_frontmatter_block).

    Raises ValueError if the file does not start with a YAML frontmatter block.
    """
    if not text.startswith("---\n"):
        raise ValueError("file does not start with YAML frontmatter (---)")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("YAML frontmatter not terminated by ---")
    raw_fm = text[4:end]
    body = text[end + 5 :]
    fm = yaml.safe_load(raw_fm) or {}
    if not isinstance(fm, dict):
        raise ValueError("frontmatter is not a YAML mapping")
    return fm, body, raw_fm


def write_back(path: Path, fm: dict, body: str) -> None:
    dumped = yaml.safe_dump(
        fm,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
    new_text = f"---\n{dumped}---\n{body}"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(new_text, encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--md", required=True, type=Path, help="path to the post .md file"
    )
    parser.add_argument("--audio-url", required=True)
    parser.add_argument("--audio-lang", required=True)
    parser.add_argument("--audio-generated-at", required=True)
    parser.add_argument("--audio-source", required=True)
    parser.add_argument("--audio-format", required=True)
    args = parser.parse_args()

    md_path: Path = args.md
    if not md_path.is_file():
        print(f"ERROR: not a file: {md_path}", file=sys.stderr)
        return 2

    text = md_path.read_text(encoding="utf-8")
    fm, body, _ = split_frontmatter(text)

    additions = {
        "audio_url": args.audio_url,
        "audio_lang": args.audio_lang,
        "audio_generated_at": args.audio_generated_at,
        "audio_source": args.audio_source,
        "audio_format": args.audio_format,
    }

    changed = False
    for key, value in additions.items():
        if key not in fm:
            fm[key] = value
            changed = True

    if not changed:
        print(f"[frontmatter] no changes (audio_* already present): {md_path}")
        return 0

    write_back(md_path, fm, body)
    print(f"[frontmatter] patched: {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
