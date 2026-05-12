#!/usr/bin/env python3
"""Post-process Hugo-built HTML to inject Hatena-style keyword auto-links.

Reads:
  - .claude/temp/keywords.json  (produced by build_keyword_index.py)
  - .claude/keyword-stoplist.txt (optional, one keyword per line, `#` comments)

Rewrites in place:
  - public/posts/**/index.html
  - public/wiki/**/index.html  (single pages only; list pages are skipped)

Policy:
  - Inside each page, every keyword (target_id) is linked at most once (first occurrence).
  - Skip text inside <a>, <code>, <pre>, <h1>-<h6>, <script>, <style>, <nav>,
    <aside>, <figcaption>, and within ToC / highlight containers.
  - ASCII-only keywords require non-word characters on both sides (word boundary).
  - Japanese / mixed keywords use literal substring match.
  - Longest keyword wins at the same position (alternation sorted by length desc).
  - Wiki single pages do not self-link (their own target_id is pre-seeded as used).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parent.parent
KEYWORDS_PATH = ROOT / ".claude" / "temp" / "keywords.json"
STOPLIST_PATH = ROOT / ".claude" / "keyword-stoplist.txt"

EXCLUDED_ANCESTORS = {
    "a",
    "code",
    "pre",
    "script",
    "style",
    "nav",
    "aside",
    "figcaption",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
}
EXCLUDED_CLASSES = {"toc", "highlight", "post-meta", "breadcrumbs", "post-tags"}

ASCII_RE = re.compile(r"^[\x00-\x7f]+$")


def load_stoplist() -> set[str]:
    if not STOPLIST_PATH.exists():
        return set()
    out: set[str] = set()
    for line in STOPLIST_PATH.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.add(s.casefold())
    return out


def load_keywords() -> list[dict]:
    if not KEYWORDS_PATH.exists():
        return []
    data = json.loads(KEYWORDS_PATH.read_text(encoding="utf-8"))
    stop = load_stoplist()
    return [e for e in data if e["keyword"].casefold() not in stop]


def is_ascii(s: str) -> bool:
    return bool(ASCII_RE.match(s))


def is_word_char(c: str) -> bool:
    return c.isascii() and (c.isalnum() or c == "_")


def site_path_prefix() -> str:
    with (ROOT / "hugo.toml").open("rb") as fp:
        cfg = tomllib.load(fp)
    base = cfg.get("baseURL", "/")
    m = re.match(r"^[a-z]+://[^/]+(/.*)?$", base)
    prefix = (m.group(1) if m and m.group(1) else "/") if m else base
    if not prefix.endswith("/"):
        prefix += "/"
    return prefix


def build_matcher(entries: list[dict]):
    entries = sorted(entries, key=lambda e: (-len(e["keyword"]), e["keyword"]))
    by_cf: dict[str, dict] = {}
    for e in entries:
        by_cf.setdefault(e["keyword"].casefold(), e)
    parts = [re.escape(e["keyword"]) for e in entries]
    pattern = re.compile("(" + "|".join(parts) + ")", re.IGNORECASE)
    return pattern, by_cf


def has_excluded_ancestor(node) -> bool:
    p = node.parent
    while p is not None and getattr(p, "name", None):
        if p.name in EXCLUDED_ANCESTORS:
            return True
        cls = p.get("class") or []
        if any(c in EXCLUDED_CLASSES for c in cls):
            return True
        # id-based exclusions for ToC etc.
        node_id = p.get("id") or ""
        if node_id in {"toc", "TableOfContents"}:
            return True
        p = p.parent
    return False


def find_content_root(soup: BeautifulSoup):
    node = soup.select_one("div.post-content")
    if node:
        return node
    return None


def page_target_id(html_path: Path, public_root: Path) -> str | None:
    rel = html_path.relative_to(public_root)
    parts = list(rel.parts[:-1])
    if len(parts) >= 2 and parts[0] == "wiki":
        return f"wiki:{'/'.join(parts[1:])}"
    return None


def page_self_url(html_path: Path, public_root: Path, prefix: str) -> str:
    rel = html_path.relative_to(public_root).parent
    if str(rel) in (".", ""):
        return prefix
    return prefix + str(rel).replace("\\", "/") + "/"


def inject(html_text: str, pattern, by_cf, self_url: str, self_target: str | None):
    soup = BeautifulSoup(html_text, "html.parser")
    root = find_content_root(soup)
    if root is None:
        return html_text, 0  # list page or no content
    used_targets: set[str] = set()
    if self_target:
        used_targets.add(self_target)
    text_nodes = [t for t in root.descendants if isinstance(t, NavigableString)]
    n_linked = 0
    for node in text_nodes:
        if has_excluded_ancestor(node):
            continue
        text = str(node)
        if not text.strip():
            continue
        fragments: list = []
        last = 0
        changed = False
        for m in pattern.finditer(text):
            matched = m.group(1)
            entry = by_cf.get(matched.casefold())
            if entry is None:
                continue
            if entry["target_id"] in used_targets:
                continue
            if entry["url"] == self_url:
                continue
            if is_ascii(matched):
                before = text[m.start() - 1] if m.start() > 0 else ""
                after = text[m.end()] if m.end() < len(text) else ""
                if before and is_word_char(before):
                    continue
                if after and is_word_char(after):
                    continue
            fragments.append(text[last : m.start()])
            a = soup.new_tag("a", href=entry["url"])
            a["class"] = ["kw-link", f"kw-link--{entry['type']}"]
            desc = entry.get("description") or ""
            if desc:
                a["title"] = desc
            a["data-kw"] = matched
            a.string = matched
            fragments.append(a)
            last = m.end()
            used_targets.add(entry["target_id"])
            n_linked += 1
            changed = True
        if not changed:
            continue
        fragments.append(text[last:])
        for frag in fragments:
            if isinstance(frag, str):
                if frag:
                    node.insert_before(NavigableString(frag))
            else:
                node.insert_before(frag)
        node.extract()
    return str(soup), n_linked


def iter_target_files(public_root: Path):
    posts_dir = public_root / "posts"
    if posts_dir.is_dir():
        for p in posts_dir.rglob("index.html"):
            yield p

    wiki_dir = public_root / "wiki"
    if not wiki_dir.is_dir():
        return
    for p in wiki_dir.rglob("index.html"):
        rel = p.relative_to(public_root)
        # Only wiki single pages have public/wiki/<section>/<slug>/index.html.
        if len(rel.parts) == 4:
            yield p


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("public", help="path to Hugo public/ directory")
    ap.add_argument(
        "--prefix", default=None, help="site path prefix (auto-detected from hugo.toml)"
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="don't write files; just report"
    )
    ap.add_argument("--limit", type=int, default=0, help="process only N files (debug)")
    args = ap.parse_args()

    public_root = Path(args.public).resolve()
    if not public_root.is_dir():
        print(f"error: not a directory: {public_root}", file=sys.stderr)
        sys.exit(1)

    prefix = args.prefix or site_path_prefix()
    entries = load_keywords()
    if not entries:
        print("no keyword entries — run build_keyword_index.py first", file=sys.stderr)
        sys.exit(1)
    pattern, by_cf = build_matcher(entries)

    targets = list(iter_target_files(public_root))
    if args.limit:
        targets = targets[: args.limit]

    files_changed = 0
    total_links = 0
    skipped = 0
    for path in targets:
        html = path.read_text(encoding="utf-8")
        self_target = page_target_id(path, public_root)
        self_url = page_self_url(path, public_root, prefix)
        new_html, n = inject(html, pattern, by_cf, self_url, self_target)
        if n == 0:
            skipped += 1
            continue
        files_changed += 1
        total_links += n
        if not args.dry_run:
            path.write_text(new_html, encoding="utf-8")
    print(
        f"injected {total_links} link(s) across {files_changed} file(s); "
        f"{skipped} unchanged (of {len(targets)} scanned)",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
