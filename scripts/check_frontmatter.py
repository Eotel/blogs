#!/usr/bin/env python3
"""Fast frontmatter validator for staged Markdown files.

Designed for lefthook pre-commit. Receives one or more file paths as args,
checks each one for required frontmatter keys, and exits non-zero on any failure.

Reuses parse_frontmatter / REQUIRED_FRONTMATTER from the wiki-lint skill
so the rules stay in one place.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_LINT_PATH = (
    REPO_ROOT / ".claude" / "skills" / "wiki-lint" / "scripts" / "wiki_lint.py"
)


def _load_wiki_lint():
    spec = importlib.util.spec_from_file_location("wiki_lint", WIKI_LINT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {WIKI_LINT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_wl = _load_wiki_lint()
REQUIRED_FRONTMATTER: list[str] = _wl.REQUIRED_FRONTMATTER
parse_frontmatter = _wl.parse_frontmatter
is_missing = _wl.is_missing

POST_REQUIRED = ["title", "date", "author"]


def _validate(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"read error: {exc}"]
    fm = parse_frontmatter(text)
    if not fm:
        return ["no frontmatter block (---) found"]
    if path.name == "_index.md":
        return []
    rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == "content" and parts[1] == "wiki":
        required = REQUIRED_FRONTMATTER
    elif len(parts) >= 2 and parts[0] == "content" and parts[1] == "posts":
        required = POST_REQUIRED
    else:
        return []
    missing = [k for k in required if is_missing(fm, k)]
    return [f"missing required key: {k}" for k in missing]


def main(argv: list[str]) -> int:
    if not argv:
        return 0
    failures: list[tuple[Path, list[str]]] = []
    for arg in argv:
        p = Path(arg)
        if not p.exists() or p.is_dir():
            continue
        if p.suffix != ".md":
            continue
        issues = _validate(p)
        if issues:
            failures.append((p, issues))
    if failures:
        print("Frontmatter validation failed:", file=sys.stderr)
        for path, issues in failures:
            for issue in issues:
                print(f"  {path}: {issue}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
