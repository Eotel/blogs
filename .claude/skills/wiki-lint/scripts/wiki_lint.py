#!/usr/bin/env python3
"""Wiki health check: orphans, broken links, dead related_posts, stale pages, frontmatter gaps.

Also checks blog posts for broken /blogs/wiki/... links.

Designed to be invoked from either:
  - .claude/skills/wiki-lint/scripts/wiki_lint.py
  - .agents/skills/wiki-lint/scripts/wiki_lint.py

Detects repo root by walking upward until `content/wiki/` is found.

Usage:
  wiki_lint.py                          # full check (pre-push)
  wiki_lint.py --post-files f1.md ...   # check only specified post files for wiki links (pre-commit)
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

REQUIRED_FRONTMATTER = [
    "title",
    "description",
    "date",
    "lastmod",
    "related_posts",
    "tags",
]
RECOMMENDED_FRONTMATTER = ["aliases"]

# Scalar required keys must have a non-empty value. The parser stores a bare
# YAML key (e.g. `author:` with no value) as `[]`, so for scalar keys we treat
# `[]` as missing too — otherwise structurally invalid required scalars would
# slip through. List-type required keys (`related_posts`, `tags`) may
# legitimately be empty (`tags: []`), so `[]` is treated as present for them.
_SCALAR_KEYS = {"title", "description", "date", "lastmod", "author"}


def is_missing(fm: dict, key: str) -> bool:
    if key not in fm:
        return True
    v = fm[key]
    if v is None or v == "":
        return True
    if v == [] and key in _SCALAR_KEYS:
        return True
    return False


FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
WIKI_LINK_RE = re.compile(r"\]\((/blogs/wiki/[^)]+)\)")
POST_LINK_RE = re.compile(r"^/(?:blogs/)?posts/([^#?]*)")


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "content" / "wiki").is_dir() and (
            candidate / "content" / "posts"
        ).is_dir():
            return candidate
    raise SystemExit(
        "Could not find repo root (no content/wiki and content/posts found upward)."
    )


def parse_frontmatter(text: str) -> dict:
    m = FM_RE.match(text)
    if not m:
        return {}
    fm_text = m.group(1)
    data: dict = {}
    current_list: list[str] | None = None
    for raw in fm_text.split("\n"):
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("  - ") or line.startswith("- "):
            if current_list is not None:
                val = line.split("- ", 1)[1].strip().strip('"').strip("'")
                current_list.append(val)
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "":
                current_list = []
                data[key] = current_list
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                if not inner:
                    data[key] = []
                else:
                    items = [s.strip().strip('"').strip("'") for s in inner.split(",")]
                    data[key] = items
                current_list = None
            else:
                data[key] = val.strip('"').strip("'")
                current_list = None
    return data


def wiki_link_to_path(link: str, wiki_dir: Path) -> tuple[Path, bool]:
    """Return (resolved_path, exists)."""
    m = re.match(r"^/blogs/wiki/([^#?]*)", link)
    if not m:
        return wiki_dir / "_invalid", False
    rel = m.group(1).rstrip("/")
    if not rel:
        p = wiki_dir / "_index.md"
        return p, p.exists()
    for c in (wiki_dir / f"{rel}.md", wiki_dir / rel / "_index.md"):
        if c.exists():
            return c, True
    return wiki_dir / f"{rel}.md", False


def build_post_slug_index(posts_dir: Path) -> dict[tuple[str, str, str], Path]:
    idx: dict[tuple[str, str, str], Path] = {}
    for f in posts_dir.rglob("*.md"):
        if f.name == "_index.md":
            continue
        parts = f.relative_to(posts_dir).parts
        if len(parts) < 3:
            try:
                fm = parse_frontmatter(f.read_text(encoding="utf-8"))
            except Exception:
                fm = {}
            stem = f.stem
            idx[("", "", stem)] = f
            slug = fm.get("slug")
            if isinstance(slug, str) and slug:
                idx[("", "", slug.strip())] = f
            continue
        year, month = parts[0], parts[1]
        try:
            fm = parse_frontmatter(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = fm.get("slug")
        stem = f.stem
        if isinstance(slug, str) and slug:
            slug_clean = slug.strip()
            idx[(year, month, slug_clean)] = f
            # Also index the date-stripped short form so wiki related_posts
            # written before slug backfill (e.g. /posts/2026/04/foo/ for
            # 2026-04-06-foo.md) keep resolving.
            m = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", slug_clean)
            if m:
                idx.setdefault((year, month, m.group(1)), f)
        else:
            idx[(year, month, stem)] = f
            m = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", stem)
            if m:
                idx.setdefault((year, month, m.group(1)), f)
        # The filename stem itself is always a valid alternate key.
        idx.setdefault((year, month, stem), f)
    return idx


def post_link_to_path(
    link: str, slug_index: dict[tuple[str, str, str], Path]
) -> Path | None:
    m = POST_LINK_RE.match(link)
    if not m:
        return None
    parts = m.group(1).rstrip("/").split("/")
    if len(parts) == 1 and parts[0]:
        return slug_index.get(("", "", parts[0]))
    if len(parts) < 3:
        return None
    return slug_index.get((parts[0], parts[1], parts[2]))


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    s = s.strip().strip('"').strip("'")
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Wiki health check. With --post-files, runs a fast post→wiki link check only."
    )
    parser.add_argument(
        "--post-files",
        nargs="+",
        metavar="FILE",
        help="Check only these post files for broken wiki links (pre-commit mode). "
        "Wiki-only checks are skipped.",
    )
    args = parser.parse_args()

    root = find_repo_root(Path(__file__).resolve().parent)
    wiki_dir = root / "content" / "wiki"
    posts_dir = root / "content" / "posts"

    # --post-files mode: fast check for pre-commit (only post→wiki links)
    if args.post_files:
        post_wiki_broken: list[tuple[Path, str]] = []
        for raw in args.post_files:
            f = Path(raw).resolve()
            if not f.exists() or f.suffix != ".md" or f.name == "_index.md":
                continue
            text = f.read_text(encoding="utf-8")
            for link in WIKI_LINK_RE.findall(text):
                _, exists = wiki_link_to_path(link, wiki_dir)
                if not exists:
                    post_wiki_broken.append((f, link))
        if post_wiki_broken:
            print("## Wiki Lint (staged post files)\n")
            print(f"### 記事内の欠落 Wiki リンク ({len(post_wiki_broken)}件) — FATAL")
            for f, link in post_wiki_broken:
                print(f"- `{f.name}` → `{link}` — リンク先 Wiki ページが存在しない")
            return 1
        return 0

    wiki_files = sorted(p for p in wiki_dir.rglob("*.md"))
    pages: dict[Path, dict] = {}
    page_text: dict[Path, str] = {}
    for f in wiki_files:
        text = f.read_text(encoding="utf-8")
        page_text[f] = text
        pages[f] = parse_frontmatter(text)

    incoming: dict[Path, set[Path]] = {f: set() for f in wiki_files}
    broken_links: list[tuple[Path, str]] = []
    for f, text in page_text.items():
        for link in WIKI_LINK_RE.findall(text):
            target, exists = wiki_link_to_path(link, wiki_dir)
            if exists:
                if target != f:
                    incoming[target].add(f)
            else:
                broken_links.append((f, link))

    orphans = [f for f, refs in incoming.items() if f.name != "_index.md" and not refs]

    slug_index = build_post_slug_index(posts_dir)
    related_post_issues: list[tuple[Path, str]] = []
    stale_pages: list[tuple[Path, date, date]] = []
    for f, fm in pages.items():
        if f.name == "_index.md":
            continue
        rp = fm.get("related_posts")
        if not rp or not isinstance(rp, list):
            continue
        wiki_lastmod = parse_date(fm.get("lastmod") or fm.get("date"))
        for ref in rp:
            ref_path = post_link_to_path(ref, slug_index)
            if ref_path is None or not ref_path.exists():
                related_post_issues.append((f, ref))
                continue
            post_fm = parse_frontmatter(ref_path.read_text(encoding="utf-8"))
            post_lastmod = parse_date(post_fm.get("lastmod") or post_fm.get("date"))
            if wiki_lastmod and post_lastmod and post_lastmod > wiki_lastmod:
                stale_pages.append((f, wiki_lastmod, post_lastmod))

    fm_issues: list[tuple[Path, list[str], list[str]]] = []
    fm_required_count = 0  # pages with at least one missing REQUIRED key (fatal)
    for f, fm in pages.items():
        if f.name == "_index.md":
            continue
        missing = [k for k in REQUIRED_FRONTMATTER if is_missing(fm, k)]
        recommended_missing = [k for k in RECOMMENDED_FRONTMATTER if is_missing(fm, k)]
        if missing or recommended_missing:
            fm_issues.append((f, missing, recommended_missing))
            if missing:
                fm_required_count += 1

    counts: dict[str, int] = {}
    for f in wiki_files:
        if f.name == "_index.md":
            continue
        section = f.relative_to(wiki_dir).parts[0]
        counts[section] = counts.get(section, 0) + 1
    total_pages = sum(counts.values())

    print("## Wiki Lint レポート\n")

    print(f"### 孤立ページ ({len(orphans)}件)")
    if orphans:
        for f in orphans:
            print(f"- `{f.relative_to(wiki_dir)}` — どこからもリンクされていない")
    else:
        print("- なし")
    print()

    print(f"### 欠落リンク ({len(broken_links)}件)")
    if broken_links:
        for f, link in broken_links:
            print(f"- `{f.relative_to(wiki_dir)}` → `{link}` — リンク先が存在しない")
    else:
        print("- なし")
    print()

    print(f"### related_posts 不整合 ({len(related_post_issues)}件)")
    if related_post_issues:
        for f, ref in related_post_issues:
            print(f"- `{f.relative_to(wiki_dir)}` → `{ref}` — 記事が存在しない")
    else:
        print("- なし")
    print()

    print(f"### 古い可能性のあるページ ({len(stale_pages)}件)")
    if stale_pages:
        for f, wlm, plm in stale_pages:
            print(
                f"- `{f.relative_to(wiki_dir)}` (lastmod: {wlm}) — ソース記事が {plm} に更新"
            )
    else:
        print("- なし")
    print()

    print(f"### フロントマター不備 ({len(fm_issues)}件)")
    if fm_issues:
        for f, missing, rec in fm_issues:
            parts = []
            if missing:
                parts.append(f"必須欠落: {', '.join(missing)}")
            if rec:
                parts.append(f"推奨欠落: {', '.join(rec)}")
            print(f"- `{f.relative_to(wiki_dir)}` — {' / '.join(parts)}")
    else:
        print("- なし")
    print()

    print("### 統計")
    print(f"- 総ページ数: {total_pages}")
    for sec in sorted(counts):
        print(f"- {sec}: {counts[sec]}")
    print()

    # Scan all blog posts for broken /blogs/wiki/... links
    post_wiki_broken: list[tuple[Path, str]] = []
    for post_file in posts_dir.rglob("*.md"):
        if post_file.name == "_index.md":
            continue
        try:
            text = post_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for link in WIKI_LINK_RE.findall(text):
            _, exists = wiki_link_to_path(link, wiki_dir)
            if not exists:
                post_wiki_broken.append((post_file, link))

    print(f"### 記事内の欠落 Wiki リンク ({len(post_wiki_broken)}件)")
    if post_wiki_broken:
        for f, link in post_wiki_broken:
            rel = f.relative_to(posts_dir)
            print(f"- `posts/{rel}` → `{link}` — リンク先 Wiki ページが存在しない")
    else:
        print("- なし")
    print()

    # Posts must define `slug:` explicitly. Hugo's `:slug` permalink token
    # falls back to the title (slugified) when `slug:` is absent, which makes
    # URLs unstable and breaks filename-pattern related_posts links.
    posts_missing_slug: list[Path] = []
    for post_file in posts_dir.rglob("*.md"):
        if post_file.name == "_index.md":
            continue
        try:
            fm = parse_frontmatter(post_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        slug = fm.get("slug")
        if not (isinstance(slug, str) and slug.strip()):
            posts_missing_slug.append(post_file)

    print(f"### 記事の slug 欠落 ({len(posts_missing_slug)}件)")
    if posts_missing_slug:
        for f in posts_missing_slug:
            rel = f.relative_to(posts_dir)
            print(
                f"- `posts/{rel}` — `slug:` 未定義 (Hugo は title 由来 slug にフォールバックし URL が不安定になる)"
            )
    else:
        print("- なし")
    print()

    # Decay (advisory): wiki pages whose `lastmod` is past the section
    # threshold. Imported lazily so wiki_lint.py keeps working even if the
    # wiki-decay skill is uninstalled.
    decay_count = 0
    try:
        sys.path.insert(0, str(root / ".claude" / "skills" / "wiki-decay" / "scripts"))
        from wiki_decay import score_pages as _score_pages  # type: ignore

        decay_entries = _score_pages(root, as_of=date.today())
        warming = [e for e in decay_entries if e.status == "warming"]
        stale = [e for e in decay_entries if e.status == "stale"]
        decay_count = len(warming) + len(stale)
        print(f"### Decay (advisory) — stale {len(stale)} / warming {len(warming)}")
        if decay_count == 0:
            print("- なし (全 page 新鮮)")
        else:
            for e in (stale + warming)[:9]:  # top 3 per section worth of room
                badge = "🔴 stale" if e.status == "stale" else "🟡 warming"
                print(
                    f"- {badge} `{e.path}` — age {e.age_days}d "
                    f"(`{e.refresh_command}`)"
                )
            if decay_count > 9:
                print(f"- … その他 {decay_count - 9} 件 (詳細は `/wiki-decay`)")
    except Exception as exc:  # pragma: no cover - defensive against optional skill
        print(f"### Decay (advisory) — skipped ({exc.__class__.__name__})")

    # Fatal: structural / referential issues that should block pre-push and CI.
    #   - broken_links / related_post_issues / post_wiki_broken: dead references
    #   - fm_required_count: pages missing at least one REQUIRED frontmatter key
    #   - posts_missing_slug: posts without `slug:` (URLs become title-derived)
    # Advisory (non-blocking):
    #   - orphans / stale pages: surfaced by /wiki-lint review, but /wiki-ingest
    #     output is temporarily orphan by design until cross-links are added
    #   - fm pages missing only RECOMMENDED keys (e.g. `aliases`)
    fatal_issues = (
        len(broken_links)
        + len(related_post_issues)
        + fm_required_count
        + len(post_wiki_broken)
        + len(posts_missing_slug)
    )
    fm_recommended_only = len(fm_issues) - fm_required_count
    advisory_issues = len(orphans) + len(stale_pages) + fm_recommended_only
    if advisory_issues:
        print(
            f"\n(advisory: {advisory_issues} non-blocking finding(s) — 孤立 / 古い可能性 / 推奨欠落)"
        )
    return 0 if fatal_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
