#!/usr/bin/env python3
"""Plan wiki ingest work by finding covered posts and duplicate wiki candidates.

This script does not write wiki pages. It builds a local SQLite FTS index over
content/wiki and emits a deterministic ingest plan for posts.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any


FM_RE = re.compile(r"^---\n(.*?)\n---\n(.*)\Z", re.DOTALL)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)$")
URL_PREFIX = "/posts/"
DEFAULT_LIMIT = 5
STOP_TERMS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "into",
    "that",
    "this",
    "という",
    "まとめ",
    "完全",
    "ガイド",
    "解説",
}


@dataclass
class WikiDoc:
    path: Path
    rel_path: str
    section: str
    slug: str
    title: str
    description: str
    aliases: list[str]
    tags: list[str]
    related_posts: list[str]
    lastmod: date | None
    body: str

    @property
    def url(self) -> str:
        return f"/blogs/wiki/{self.section}/{self.slug}/"


@dataclass
class PostDoc:
    path: Path
    rel_path: str
    title: str
    description: str
    categories: list[str]
    tags: list[str]
    date: date | None
    lastmod: date | None
    body: str
    url: str
    alt_urls: set[str] = field(default_factory=set)


@dataclass
class Candidate:
    wiki: WikiDoc
    score: int
    reasons: list[str]


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "content" / "wiki").is_dir() and (
            candidate / "content" / "posts"
        ).is_dir():
            return candidate
    raise SystemExit(
        "Could not find repo root (no content/wiki and content/posts found upward)."
    )


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FM_RE.match(text)
    if not match:
        return {}, text
    data: dict[str, Any] = {}
    current_list: list[str] | None = None
    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("  - ") or line.startswith("- "):
            if current_list is not None:
                current_list.append(
                    line.split("- ", 1)[1].strip().strip('"').strip("'")
                )
            continue
        if ":" not in line:
            current_list = None
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "":
            current_list = []
            data[key] = current_list
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if not inner:
                data[key] = []
            else:
                data[key] = [x.strip().strip('"').strip("'") for x in inner.split(",")]
            current_list = None
        else:
            data[key] = value.strip('"').strip("'")
            current_list = None
    return data, match.group(2)


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def parse_date(value: Any) -> date | None:
    if value is None:
        return None
    text = str(value).strip().strip('"').strip("'")
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def post_urls(path: Path, posts_dir: Path, fm: dict[str, Any]) -> tuple[str, set[str]]:
    rel = path.relative_to(posts_dir)
    parts = rel.parts
    urls: set[str] = set()
    if len(parts) >= 3:
        year, month = parts[0], parts[1]
        stem = path.stem
        canonical = f"{URL_PREFIX}{year}/{month}/{stem}/"
        urls.add(canonical)
        short = DATE_RE.match(stem)
        if short:
            urls.add(f"{URL_PREFIX}{year}/{month}/{short.group(1)}/")
        slug = fm.get("slug")
        if isinstance(slug, str) and slug.strip():
            canonical = f"{URL_PREFIX}{year}/{month}/{slug.strip()}/"
            urls.add(canonical)
    else:
        canonical = f"{URL_PREFIX}{path.stem}/"
        urls.add(canonical)
    return canonical, urls


def load_wiki_docs(root: Path) -> list[WikiDoc]:
    wiki_dir = root / "content" / "wiki"
    docs: list[WikiDoc] = []
    for path in sorted(wiki_dir.rglob("*.md")):
        if path.name == "_index.md":
            continue
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        rel = path.relative_to(wiki_dir)
        if len(rel.parts) < 2:
            continue
        docs.append(
            WikiDoc(
                path=path,
                rel_path=str(rel),
                section=rel.parts[0],
                slug=path.stem,
                title=str(fm.get("title") or "").strip(),
                description=str(fm.get("description") or "").strip(),
                aliases=as_list(fm.get("aliases")),
                tags=as_list(fm.get("tags")),
                related_posts=as_list(fm.get("related_posts")),
                lastmod=parse_date(fm.get("lastmod") or fm.get("date")),
                body=body.strip(),
            )
        )
    return docs


def load_post(path: Path, posts_dir: Path) -> PostDoc | None:
    if path.name == "_index.md" or path.suffix != ".md":
        return None
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    url, alt_urls = post_urls(path, posts_dir, fm)
    return PostDoc(
        path=path,
        rel_path=str(path.relative_to(posts_dir.parent.parent)),
        title=str(fm.get("title") or path.stem).strip(),
        description=str(fm.get("description") or "").strip(),
        categories=as_list(fm.get("categories")),
        tags=as_list(fm.get("tags")),
        date=parse_date(fm.get("date")),
        lastmod=parse_date(fm.get("lastmod") or fm.get("date")),
        body=body.strip(),
        url=url,
        alt_urls=alt_urls,
    )


def load_posts(root: Path) -> list[PostDoc]:
    posts_dir = root / "content" / "posts"
    posts: list[PostDoc] = []
    for path in sorted(posts_dir.rglob("*.md")):
        post = load_post(path, posts_dir)
        if post is not None:
            posts.append(post)
    return posts


def resolve_posts(root: Path, target: str, since: date | None) -> list[PostDoc]:
    posts_dir = root / "content" / "posts"
    candidate = Path(target)
    if not candidate.is_absolute():
        candidate = root / candidate
    if candidate.exists() and candidate.is_file():
        post = load_post(candidate.resolve(), posts_dir)
        return [post] if post is not None else []

    posts = load_posts(root)
    if target != "all":
        posts = [p for p in posts if target in p.categories]
    if since is not None:
        posts = [p for p in posts if p.date is not None and p.date > since]
    return posts


def ensure_fts(root: Path, wiki_docs: list[WikiDoc]) -> Path:
    db_path = root / ".claude" / "temp" / "wiki_ingest_index.sqlite"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    with sqlite3.connect(db_path) as con:
        con.execute(
            """
            CREATE VIRTUAL TABLE wiki_docs USING fts5(
                rel_path UNINDEXED,
                title,
                aliases,
                tags,
                description,
                body,
                tokenize='trigram'
            )
            """
        )
        con.executemany(
            """
            INSERT INTO wiki_docs(rel_path, title, aliases, tags, description, body)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    doc.rel_path,
                    doc.title,
                    " ".join(doc.aliases),
                    " ".join(doc.tags),
                    doc.description,
                    doc.body,
                )
                for doc in wiki_docs
            ],
        )
    return db_path


def normalize(value: str) -> str:
    return value.casefold().strip()


def extract_terms(post: PostDoc) -> list[str]:
    raw: list[str] = []
    raw.extend(post.tags)
    raw.extend(post.categories)
    raw.append(post.title)
    raw.append(post.description)
    split_parts = re.split(
        r"[\s　、。・/|:：—\-×()（）\[\]「」『』!?！？]+", post.title
    )
    raw.extend(split_parts)
    body_parts = re.split(
        r"[\s　、。・/|:：—\-×()（）\[\]「」『』!?！？]+", post.body[:1200]
    )
    raw.extend(body_parts)
    terms: list[str] = []
    seen: set[str] = set()
    for item in raw:
        item = item.strip()
        if len(item) < 2:
            continue
        if item.casefold() in STOP_TERMS:
            continue
        if item.casefold() in seen:
            continue
        seen.add(item.casefold())
        terms.append(item)
    return terms[:14]


def fts_query(terms: list[str]) -> str:
    quoted = []
    for term in terms:
        safe = term.replace('"', '""')
        if safe:
            quoted.append(f'"{safe}"')
    return " OR ".join(quoted)


def search_fts(db_path: Path, post: PostDoc, limit: int) -> dict[str, int]:
    matches: dict[str, int] = {}
    terms = extract_terms(post)
    if not terms:
        return matches
    with sqlite3.connect(db_path) as con:
        for term in terms:
            query = fts_query([term])
            if not query:
                continue
            try:
                rows = con.execute(
                    """
                    SELECT rel_path, bm25(wiki_docs) AS rank
                    FROM wiki_docs
                    WHERE wiki_docs MATCH ?
                    ORDER BY rank
                    LIMIT ?
                    """,
                    (query, max(limit, DEFAULT_LIMIT)),
                ).fetchall()
            except sqlite3.OperationalError:
                continue
            for idx, (rel_path, _rank) in enumerate(rows):
                bonus = max(5, 25 - idx * 5)
                key = str(rel_path)
                matches[key] = min(45, matches.get(key, 0) + bonus)
    return matches


def score_candidate(post: PostDoc, wiki: WikiDoc, fts_bonus: int) -> Candidate:
    score = 0
    reasons: list[str] = []
    post_title = normalize(post.title)
    post_body = normalize("\n".join([post.description, post.body]))
    names = [wiki.title, *wiki.aliases]
    for name in names:
        n = normalize(name)
        if not n or len(n) < 2:
            continue
        if n in post_title:
            score += 50
            reasons.append(f"title/alias match in post title: {name}")
            break
    for name in names:
        n = normalize(name)
        if not n or len(n) < 2:
            continue
        if n in post_body:
            score += 20
            reasons.append(f"title/alias match in post body: {name}")
            break
    tag_overlap = sorted(
        {normalize(t) for t in post.tags} & {normalize(t) for t in wiki.tags}
    )
    if tag_overlap:
        points = min(20, len(tag_overlap) * 5)
        score += points
        reasons.append(f"tag overlap: {', '.join(tag_overlap)}")
    if fts_bonus:
        score += fts_bonus
        reasons.append(f"FTS trigram hit: +{fts_bonus}")
    if wiki.section == "tools":
        for name in names:
            n = normalize(name)
            if n and re.search(
                rf"(^|[\s/・:：]){re.escape(n)}($|[\s/・:：])", post_title
            ):
                score += 10
                reasons.append("tool-like exact title token")
                break
    return Candidate(wiki=wiki, score=min(score, 100), reasons=reasons)


def classify(score: int) -> str:
    if score >= 70:
        return "update_candidate"
    if score >= 35:
        return "review_candidate"
    return "new_candidate"


def suggested_section(post: PostDoc) -> str:
    text = normalize(" ".join([post.title, *post.tags, *post.categories]))
    if any(
        word in text
        for word in ("手順", "設定", "導入", "構築", "移行", "ガイド", "how-to")
    ):
        return "guides"
    if any(
        cat in post.categories
        for cat in ("ツール/開発環境", "クラウド/インフラ", "データベース")
    ):
        return "tools"
    if any(
        word in text
        for word in ("api", "cli", "sdk", "mcp", "github", "aws", "claude code")
    ):
        return "tools"
    return "concepts"


def suggested_slug(post: PostDoc) -> str:
    slug = post.url.rstrip("/").split("/")[-1]
    slug = DATE_RE.sub(r"\1", slug)
    return re.sub(r"[^a-z0-9-]+", "-", slug.casefold()).strip("-") or "new-wiki-page"


def plan_post(
    post: PostDoc,
    wiki_docs: list[WikiDoc],
    related_index: dict[str, list[WikiDoc]],
    db_path: Path,
    limit: int,
) -> dict[str, Any]:
    covered: list[WikiDoc] = []
    seen_covered: set[str] = set()
    for url in sorted(post.alt_urls):
        for wiki in related_index.get(url, []):
            if wiki.rel_path in seen_covered:
                continue
            seen_covered.add(wiki.rel_path)
            covered.append(wiki)
    if covered:
        wiki = covered[0]
        status = "covered"
        if post.lastmod and any(
            candidate.lastmod and post.lastmod > candidate.lastmod
            for candidate in covered
        ):
            status = "stale_candidate"
        return {
            "post": post.rel_path,
            "post_url": post.url,
            "title": post.title,
            "date": post.date.isoformat() if post.date else None,
            "status": status,
            "suggested_new_page": None,
            "candidates": [
                {
                    "wiki": candidate.rel_path,
                    "wiki_url": candidate.url,
                    "title": candidate.title,
                    "score": 100,
                    "reasons": ["related_posts already contains this post"],
                }
                for candidate in covered
            ],
        }

    fts_hits = search_fts(db_path, post, limit=limit * 3)
    candidates: list[Candidate] = []
    for wiki in wiki_docs:
        fts_bonus = fts_hits.get(wiki.rel_path, 0)
        candidate = score_candidate(post, wiki, fts_bonus)
        if candidate.score > 0:
            candidates.append(candidate)
    candidates.sort(key=lambda c: (-c.score, c.wiki.section, c.wiki.rel_path))
    candidates = candidates[:limit]
    top_score = candidates[0].score if candidates else 0
    status = classify(top_score)
    return {
        "post": post.rel_path,
        "post_url": post.url,
        "title": post.title,
        "date": post.date.isoformat() if post.date else None,
        "status": status,
        "suggested_new_page": (
            {
                "section": suggested_section(post),
                "slug": suggested_slug(post),
                "reason": "No strong existing wiki candidate; create a concept/tool/guide page, not a 1:1 post copy.",
            }
            if status == "new_candidate"
            else None
        ),
        "candidates": [
            {
                "wiki": c.wiki.rel_path,
                "wiki_url": c.wiki.url,
                "title": c.wiki.title,
                "score": c.score,
                "reasons": c.reasons,
            }
            for c in candidates
        ],
    }


def build_plan(
    root: Path, target: str, since: date | None, limit: int
) -> dict[str, Any]:
    wiki_docs = load_wiki_docs(root)
    posts = resolve_posts(root, target, since)
    db_path = ensure_fts(root, wiki_docs)
    related_index: dict[str, list[WikiDoc]] = {}
    for wiki in wiki_docs:
        for ref in wiki.related_posts:
            related_index.setdefault(ref, []).append(wiki)
    articles = [plan_post(p, wiki_docs, related_index, db_path, limit) for p in posts]
    counts: dict[str, int] = {}
    for item in articles:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    return {
        "target": target,
        "since": since.isoformat() if since else None,
        "wiki_pages": len(wiki_docs),
        "posts": len(posts),
        "counts": dict(sorted(counts.items())),
        "articles": articles,
        "index": str(db_path.relative_to(root)),
    }


def markdown(plan: dict[str, Any]) -> str:
    lines = [
        "## Wiki Ingest Plan",
        "",
        f"- target: `{plan['target']}`",
        f"- since: `{plan['since'] or '-'}`",
        f"- posts: {plan['posts']}",
        f"- wiki_pages: {plan['wiki_pages']}",
        f"- index: `{plan['index']}`",
        "",
        "### Summary",
    ]
    if plan["counts"]:
        for key, count in plan["counts"].items():
            lines.append(f"- {key}: {count}")
    else:
        lines.append("- no target posts")
    lines.extend(["", "### Articles"])
    for item in plan["articles"]:
        lines.append(f"- `{item['post']}` — **{item['status']}**")
        lines.append(f"  - title: {item['title']}")
        lines.append(f"  - post_url: `{item['post_url']}`")
        if item.get("suggested_new_page"):
            suggested = item["suggested_new_page"]
            lines.append(
                "  - suggested_new_page: "
                f"`content/wiki/{suggested['section']}/{suggested['slug']}.md`"
            )
        if item["candidates"]:
            lines.append("  - candidates:")
            for candidate in item["candidates"]:
                reason = "; ".join(candidate["reasons"]) or "matched"
                lines.append(
                    "    - " f"`{candidate['wiki']}` ({candidate['score']}) — {reason}"
                )
        else:
            lines.append("  - candidates: none")
    return "\n".join(lines) + "\n"


def read_since(root: Path, args: argparse.Namespace) -> date | None:
    raw = args.since
    if args.since_file:
        since_path = Path(args.since_file)
        if not since_path.is_absolute():
            since_path = root / since_path
        if since_path.exists():
            raw = since_path.read_text(encoding="utf-8").strip()
    return parse_date(raw)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plan /wiki-ingest work and detect existing wiki merge candidates."
    )
    parser.add_argument("target", help="post path, category name, or 'all'")
    parser.add_argument(
        "--since", help="Only include posts with frontmatter date after YYYY-MM-DD"
    )
    parser.add_argument("--since-file", help="Read since date from a file")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="Accepted for explicitness; the local index is rebuilt on every run.",
    )
    parser.add_argument("--root", help=argparse.SUPPRESS)
    args = parser.parse_args()

    root = (
        Path(args.root).resolve()
        if args.root
        else find_repo_root(Path(__file__).resolve())
    )
    since = read_since(root, args)
    plan = build_plan(root, args.target, since, max(1, args.limit))
    if args.format == "json":
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(markdown(plan), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
