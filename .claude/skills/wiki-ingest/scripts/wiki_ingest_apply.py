#!/usr/bin/env python3
"""Apply a wiki ingest plan.

The safe path updates existing wiki pages only for high-confidence candidates.
The all path additionally creates/updates a backlog wiki page for unresolved
review/new candidates, so full-repository runs are possible without forcing
weak matches into semantic pages.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import wiki_ingest_plan


FM_RE = re.compile(r"^---\n(.*?)\n---\n(.*)\Z", re.DOTALL)
DEFAULT_BACKLOG = "guides/wiki-ingest-backlog.md"


def qualifies_safe(candidate: dict[str, Any]) -> bool:
    if candidate["score"] >= 90:
        return True
    if candidate["score"] < 70:
        return False
    reasons = " / ".join(candidate.get("reasons") or [])
    return (
        "title/alias match in post title" in reasons
        or "tool-like exact title token" in reasons
    )


def has_related_post(fm: str, post_url: str) -> bool:
    return (
        f'  - "{post_url}"' in fm
        or f"  - '{post_url}'" in fm
        or f"  - {post_url}" in fm
    )


def add_related_post(fm: str, post_url: str, today: str) -> tuple[str, bool]:
    if has_related_post(fm, post_url):
        return fm, False
    lines = fm.splitlines()
    out: list[str] = []
    changed = False
    inserted_related = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("lastmod:"):
            out.append(f"lastmod: {today}")
            i += 1
            continue
        if line.strip() == "related_posts: []":
            out.append("related_posts:")
            out.append(f'  - "{post_url}"')
            changed = True
            inserted_related = True
            i += 1
            continue
        if line.strip() == "related_posts:":
            out.append(line)
            i += 1
            while i < len(lines) and (
                lines[i].startswith("  - ") or not lines[i].strip()
            ):
                out.append(lines[i])
                i += 1
            out.append(f'  - "{post_url}"')
            changed = True
            inserted_related = True
            continue
        out.append(line)
        i += 1
    if not inserted_related:
        out.append("related_posts:")
        out.append(f'  - "{post_url}"')
        changed = True
    return "\n".join(out), changed


def add_source_line(
    body: str, post_url: str, title: str, post_date: str | None
) -> tuple[str, bool]:
    blog_url = "/blogs" + post_url
    if blog_url in body or post_url in body:
        return body, False
    date_suffix = f" — {post_date}" if post_date else ""
    line = f"- [{title}]({blog_url}){date_suffix}"
    if "\n## ソース記事\n" in body:
        marker = "\n## ソース記事\n"
        before, after = body.split(marker, 1)
        source_block, sep, rest = after.partition("\n## ")
        source_block = source_block.rstrip() + "\n" + line + "\n"
        if sep:
            return before + marker + source_block + "\n## " + rest, True
        return before + marker + source_block, True
    body = body.rstrip() + "\n\n## ソース記事\n\n" + line + "\n"
    return body, True


def apply_to_wiki(
    root: Path,
    wiki_rel: str,
    post_url: str,
    title: str,
    post_date: str | None,
    today: str,
    dry_run: bool,
) -> bool:
    path = root / "content" / "wiki" / wiki_rel
    text = path.read_text(encoding="utf-8")
    match = FM_RE.match(text)
    if not match:
        raise RuntimeError(f"missing frontmatter: {path}")
    fm, body = match.group(1), match.group(2)
    fm, fm_changed = add_related_post(fm, post_url, today)
    body, body_changed = add_source_line(body, post_url, title, post_date)
    if not fm_changed and not body_changed:
        return False
    if not dry_run:
        path.write_text("---\n" + fm + "\n---\n" + body, encoding="utf-8")
    return True


def select_semantic_candidates(
    article: dict[str, Any],
    policy: str,
    max_candidates: int,
) -> list[dict[str, Any]]:
    if article["status"] != "update_candidate":
        return []
    selected: list[dict[str, Any]] = []
    for candidate in article.get("candidates", [])[:max_candidates]:
        if policy == "all":
            if candidate["score"] >= 70:
                selected.append(candidate)
        elif qualifies_safe(candidate):
            selected.append(candidate)
    return selected


def is_backlog_wiki(wiki_rel: str, backlog_rel: str) -> bool:
    wiki = Path(wiki_rel)
    base = Path(backlog_rel).with_suffix("")
    return wiki.parent == base.parent and wiki.stem.startswith(base.name)


def status_from_backlog_wiki(wiki_rel: str, backlog_rel: str) -> str | None:
    wiki = Path(wiki_rel)
    base = Path(backlog_rel).with_suffix("")
    if not is_backlog_wiki(wiki_rel, backlog_rel):
        return None
    suffix = wiki.stem.removeprefix(base.name).lstrip("-")
    if not suffix:
        return None
    parts = suffix.split("-", 1)
    if len(parts) != 2:
        return None
    return parts[1]


def backlog_articles(
    plan: dict[str, Any],
    semantic_applied_posts: set[str],
    policy: str,
    backlog_rel: str,
) -> list[dict[str, Any]]:
    if policy != "all":
        return []
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for article in plan["articles"]:
        if article["post_url"] in semantic_applied_posts:
            continue
        if article["status"] == "covered":
            candidates = article.get("candidates", [])
            covered_by_real_wiki = any(
                not is_backlog_wiki(c["wiki"], backlog_rel)
                and "related_posts already contains this post" in c.get("reasons", [])
                for c in candidates
            )
            if covered_by_real_wiki:
                continue
            for candidate in candidates:
                status = status_from_backlog_wiki(candidate["wiki"], backlog_rel)
                if status:
                    item = dict(article)
                    item["status"] = status
                    out.append(item)
                    seen.add(article["post_url"])
                    break
            continue
        if article["status"] == "stale_candidate":
            continue
        if article["post_url"] in seen:
            continue
        out.append(article)
        seen.add(article["post_url"])
    return out


def article_year(item: dict[str, Any]) -> str:
    post_url = item["post_url"]
    parts = post_url.strip("/").split("/")
    if len(parts) >= 2 and parts[1].isdigit():
        return parts[1]
    return "root"


def render_backlog(
    backlog: list[dict[str, Any]], today: str, title_suffix: str = ""
) -> str:
    related = "\n".join(f'  - "{item["post_url"]}"' for item in backlog)
    title = "Wiki ingest backlog" + (f" ({title_suffix})" if title_suffix else "")
    lines = [
        "---",
        f'title: "{title}"',
        'description: "全記事 wiki-ingest で、既存 Wiki への高信頼統合には至らなかった記事のレビュー用バックログ"',
        f"date: {today}",
        f"lastmod: {today}",
        'aliases: ["wiki ingest backlog", "未蒸留記事"]',
        "related_posts:",
        related if related else "  []",
        'tags: ["wiki-ingest", "LLM Wiki", "backlog"]',
        "---",
        "",
        "## 概要",
        "",
        "このページは `/wiki-ingest all` の全記事処理で、既存の概念・ツール・ガイドページへ高信頼で統合できなかった記事を集約するレビュー用バックログ。Karpathy の LLM Wiki パターンにおける Raw Sources と Wiki の間に置く未蒸留層であり、ここから個別の概念ページへ再分類していく。",
        "",
        "## レビュー対象",
        "",
    ]
    for item in backlog:
        blog_url = "/blogs" + item["post_url"]
        lines.append(
            f"- [{item['title']}]({blog_url}) — {item.get('date') or '-'} / {item['status']}"
        )
    return "\n".join(lines) + "\n"


def render_backlog_index(
    groups: dict[tuple[str, str], list[dict[str, Any]]], rel_path: str, today: str
) -> str:
    base = Path(rel_path).with_suffix("")
    lines = [
        "---",
        'title: "Wiki ingest backlog"',
        'description: "全記事 wiki-ingest で、既存 Wiki への高信頼統合には至らなかった記事の年別・状態別レビュー用インデックス"',
        f"date: {today}",
        f"lastmod: {today}",
        'aliases: ["wiki ingest backlog", "未蒸留記事"]',
        "related_posts: []",
        'tags: ["wiki-ingest", "LLM Wiki", "backlog"]',
        "---",
        "",
        "## 概要",
        "",
        "全記事 `/wiki-ingest` のうち、高信頼で既存 Wiki に統合できなかった記事を年別・状態別に分割したレビュー用インデックス。",
        "",
        "## バックログ",
        "",
    ]
    for (year, status), items in sorted(groups.items(), reverse=True):
        slug = f"{base.name}-{year}-{status}"
        url = f"/blogs/wiki/{base.parent.name}/{slug}/"
        lines.append(f"- [{year} / {status}]({url}) — {len(items)}件")
    return "\n".join(lines) + "\n"


def write_text_if_changed(path: Path, content: str, dry_run: bool) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return True


def write_backlog(
    root: Path, backlog: list[dict[str, Any]], rel_path: str, today: str, dry_run: bool
) -> bool:
    if not backlog:
        return False
    base_path = root / "content" / "wiki" / rel_path
    base = Path(rel_path).with_suffix("")
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in backlog:
        groups.setdefault((article_year(item), item["status"]), []).append(item)
    changed = write_text_if_changed(
        base_path, render_backlog_index(groups, rel_path, today), dry_run
    )
    for (year, status), items in groups.items():
        shard_rel = base.parent / f"{base.name}-{year}-{status}.md"
        shard_path = root / "content" / "wiki" / shard_rel
        title_suffix = f"{year} / {status}"
        changed = (
            write_text_if_changed(
                shard_path, render_backlog(items, today, title_suffix), dry_run
            )
            or changed
        )
    return changed


def ensure_index_link(root: Path, backlog_rel: str, dry_run: bool) -> bool:
    section = backlog_rel.split("/", 1)[0]
    slug = Path(backlog_rel).stem
    index = root / "content" / "wiki" / section / "_index.md"
    if not index.exists():
        return False
    text = index.read_text(encoding="utf-8")
    link = f"/blogs/wiki/{section}/{slug}/"
    if link in text:
        return False
    addition = f"\n- [Wiki ingest backlog]({link})\n"
    if "## ページ" not in text:
        addition = "\n## ページ\n" + addition
    if not dry_run:
        index.write_text(text.rstrip() + "\n" + addition, encoding="utf-8")
    return True


def apply_plan(
    root: Path,
    plan: dict[str, Any],
    policy: str,
    max_candidates: int,
    backlog_rel: str,
    today: str,
    dry_run: bool,
) -> dict[str, Any]:
    touched: set[str] = set()
    semantic_links = 0
    semantic_applied_posts: set[str] = set()
    for article in plan["articles"]:
        selected = select_semantic_candidates(article, policy, max_candidates)
        if selected:
            semantic_applied_posts.add(article["post_url"])
        for candidate in selected:
            if apply_to_wiki(
                root,
                candidate["wiki"],
                article["post_url"],
                article["title"],
                article.get("date"),
                today,
                dry_run,
            ):
                semantic_links += 1
                touched.add(candidate["wiki"])
    unresolved = backlog_articles(plan, semantic_applied_posts, policy, backlog_rel)
    backlog_changed = write_backlog(root, unresolved, backlog_rel, today, dry_run)
    index_changed = (
        ensure_index_link(root, backlog_rel, dry_run) if backlog_changed else False
    )
    return {
        "policy": policy,
        "dry_run": dry_run,
        "semantic_links_added": semantic_links,
        "semantic_pages_touched": sorted(touched),
        "semantic_pages_touched_count": len(touched),
        "backlog_articles": len(unresolved),
        "backlog_page": backlog_rel if unresolved else None,
        "backlog_changed": backlog_changed,
        "index_changed": index_changed,
    }


def load_or_build_plan(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    if args.plan:
        return json.loads(Path(args.plan).read_text(encoding="utf-8"))
    since = wiki_ingest_plan.read_since(root, args)
    return wiki_ingest_plan.build_plan(root, args.target, since, max(1, args.limit))


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply wiki ingest plan updates.")
    parser.add_argument(
        "target", nargs="?", default="all", help="post path, category, or all"
    )
    parser.add_argument("--plan", help="Existing JSON plan file")
    parser.add_argument(
        "--since", help="Only include posts after YYYY-MM-DD when building a plan"
    )
    parser.add_argument(
        "--since-file", help="Read since date from a file when building a plan"
    )
    parser.add_argument("--policy", choices=["safe", "all"], default="safe")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--max-candidates", type=int, default=5)
    parser.add_argument("--backlog-page", default=DEFAULT_BACKLOG)
    parser.add_argument("--today", default=date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--root", help=argparse.SUPPRESS)
    args = parser.parse_args()

    root = (
        Path(args.root).resolve()
        if args.root
        else wiki_ingest_plan.find_repo_root(Path(__file__).resolve())
    )
    plan = load_or_build_plan(root, args)
    result = apply_plan(
        root=root,
        plan=plan,
        policy=args.policy,
        max_candidates=max(1, args.max_candidates),
        backlog_rel=args.backlog_page,
        today=args.today,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
