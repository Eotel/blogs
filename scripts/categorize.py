#!/usr/bin/env python3
"""Auto-categorize Hugo blog posts based on title and content keywords."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

POSTS_DIR = Path(__file__).resolve().parent.parent / "content" / "posts"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)\Z", re.DOTALL)

# Category rules: (category, [keywords])
# Order matters - first match wins for primary category
CATEGORY_RULES: list[tuple[str, list[str]]] = [
    # AI/LLM
    ("AI/LLM", [
        "claude", "gpt", "chatgpt", "llm", "ai ", "ai-", "aiエージェント",
        "anthropic", "openai", "gemini", "copilot", "qwen", "ollama",
        "プロンプト", "prompt", "rag", "langchain", "agent", "エージェント",
        "機械学習", "深層学習", "大規模言語", "生成ai", "notebooklm",
        "mcp", "agentic", "openhands", "openclaw", "openfang",
        "vibe coding", "cursor", "ハルシネーション", "sycophancy",
        "シコファンシー", "fingpt", "animaworks", "goose",
        "tts", "音声合成", "voice cloning", "text-to-speech",
        "f5-tts", "cosyvoice", "vall-e", "llasa", "vadusa",
        "投機的デコード", "投機的tts", "speculative decoding",
        "speculative tts", "flow matching", "推測デコード",
    ]),
    # セキュリティ
    ("セキュリティ", [
        "セキュリティ", "security", "脆弱性", "vulnerability", "攻撃",
        "inject", "インジェクション", "xss", "csrf", ".env", "dotenv",
        "認証", "暗号", "encrypt", "credential", "trivy", "shannon",
        "ペネトレーション", "dmarc", "spf", "hijack", "マルウェア",
        "1password", "keychain", "vault", "lkr",
    ]),
    # クラウド/インフラ
    ("クラウド/インフラ", [
        "aws", "gcp", "azure", "docker", "kubernetes", "k8s",
        "terraform", "cloudfront", "bigquery", "bedrock",
        "nginx", "apache", "linux", "centos", "ubuntu",
        "sre", "devops", "ci/cd", "github actions",
    ]),
    # Web開発
    ("Web開発", [
        "django", "flask", "fastapi", "rails", "laravel",
        "react", "vue", "next", "nuxt", "angular",
        "javascript", "typescript", "node", "deno", "bun",
        "html", "css", "bootstrap", "jquery", "webpack",
        "rest", "api", "graphql", "websocket",
        "wagtail", "wordpress", "cakephp", "php",
    ]),
    # プログラミング言語
    ("プログラミング言語", [
        "python", "rust", "go ", "golang", "swift",
        "java ", "kotlin", "ruby", "perl", "c++",
        "haskell", "elixir", "scala",
    ]),
    # モバイル
    ("モバイル", [
        "ios", "android", "swift", "kotlin",
        "react native", "flutter", "mobile",
    ]),
    # データベース
    ("データベース", [
        "mysql", "postgresql", "postgres", "sqlite",
        "redis", "mongodb", "database", "sql",
        "doctrine", "orm",
    ]),
    # ツール/開発環境
    ("ツール/開発環境", [
        "git ", "github", "vscode", "vim", "emacs",
        "homebrew", "brew", "packer", "vagrant",
        "editor", "terminal", "tmux", "shell",
        "obsidian", "figma", "theatre.js",
    ]),
    # ビジネス/キャリア
    ("ビジネス/キャリア", [
        "ビジネス", "経営", "採用", "キャリア", "仕事",
        "マネジメント", "組織", "市場", "売上", "vc",
        "スタートアップ", "起業", "ceo", "cto",
        "言語化", "勉強法", "学習", "ロードマップ",
        "デザイナー", "エンジニア",
    ]),
    # 地域/グルメ
    ("地域/グルメ", [
        "town:", "横浜", "中華街", "恵比寿", "渋谷",
        "新宿", "目黒", "世田谷", "品川", "港区",
        "レストラン", "カフェ", "ラーメン", "グルメ",
        "running", "散歩",
    ]),
]

# Tag extraction rules
TAG_RULES: list[tuple[str, list[str]]] = [
    ("claude-code", ["claude code", "claude-code"]),
    ("claude", ["claude"]),
    ("chatgpt", ["chatgpt", "gpt-4", "gpt-3"]),
    ("llm", ["llm", "大規模言語"]),
    ("openai", ["openai"]),
    ("anthropic", ["anthropic"]),
    ("gemini", ["gemini"]),
    ("qwen", ["qwen"]),
    ("ollama", ["ollama"]),
    ("mcp", [" mcp ", "mcp ", " mcp"]),
    ("agent", ["agent", "エージェント"]),
    ("rag", [" rag ", "rag "]),
    ("prompt", ["プロンプト", "prompt"]),
    ("python", ["python"]),
    ("django", ["django"]),
    ("rust", [" rust ", "rust "]),
    ("go", [" go ", "golang"]),
    ("swift", ["swift"]),
    ("javascript", ["javascript", " js "]),
    ("typescript", ["typescript"]),
    ("react", ["react"]),
    ("docker", ["docker"]),
    ("kubernetes", ["kubernetes", " k8s"]),
    ("aws", [" aws ", "aws-", "aws "]),
    ("github", ["github"]),
    ("github-actions", ["github actions"]),
    ("security", ["セキュリティ", "security", "脆弱性"]),
    ("hugo", ["hugo"]),
    ("github-pages", ["github pages"]),
    ("figma", ["figma"]),
    ("obsidian", ["obsidian"]),
    ("vscode", ["vscode", "vs code"]),
    ("tdd", ["tdd", "テスト駆動"]),
    ("bigquery", ["bigquery"]),
    ("nginx", ["nginx"]),
    ("mysql", ["mysql"]),
    ("redis", ["redis"]),
    ("wordpress", ["wordpress"]),
    ("laravel", ["laravel"]),
    ("homebrew", ["homebrew"]),
    ("tts", ["tts", "text-to-speech"]),
    ("音声合成", ["音声合成", "voice synthesis"]),
    ("投機的デコード", ["投機的デコード", "speculative decoding", "投機的tts", "speculative tts", "推測デコード"]),
    ("推論高速化", ["推論高速化", "inference acceleration", "rtf", "real-time factor"]),
    ("flow-matching", ["flow matching", "rectified flow", "matcha-tts", "f5-tts"]),
]


def split_frontmatter(text: str) -> tuple[str, str] | None:
    """Split a Hugo post into (frontmatter_text, body). Return None if no frontmatter."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    return match.group(1), match.group(2)


def parse_frontmatter(fm_text: str) -> dict[str, Any]:
    """Parse frontmatter YAML safely. Return empty dict on failure."""
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def categorize(title: str, body_preview: str) -> str:
    """Assign category based on title and first 500 chars of body."""
    text = (title + " " + body_preview[:500]).lower()
    for category, keywords in CATEGORY_RULES:
        for kw in keywords:
            if kw.lower() in text:
                return category
    return "その他"


def extract_tags(title: str, body_preview: str) -> list[str]:
    """Extract up to 5 tags based on title and content."""
    text = (title + " " + body_preview[:1000]).lower()
    tags: list[str] = []
    for tag, keywords in TAG_RULES:
        for kw in keywords:
            if kw.lower() in text:
                tags.append(tag)
                break
    return tags[:5]


def is_empty_list(value: Any) -> bool:
    """True if value is missing, None, or an empty list."""
    return value is None or (isinstance(value, list) and len(value) == 0)


def update_post(filepath: Path) -> tuple[bool, str | None]:
    """Update a post's frontmatter with category and tags.

    Returns (updated, category). category is None if the post was skipped.
    """
    text = filepath.read_text(encoding="utf-8")
    split = split_frontmatter(text)
    if split is None:
        return False, None
    fm_text, body = split

    fm = parse_frontmatter(fm_text)

    # Skip if already categorized (non-empty list)
    if not is_empty_list(fm.get("categories")):
        return False, None

    title = str(fm.get("title", ""))
    category = categorize(title, body)
    tags = extract_tags(title, body)

    cat_str = f'["{category}"]'
    tag_str = "[" + ", ".join(f'"{t}"' for t in tags) + "]" if tags else "[]"

    # Replace empty arrays only on top-level lines (start-of-line anchored).
    new_fm = re.sub(
        r"(?m)^categories:\s*\[\s*\]\s*$", f"categories: {cat_str}", fm_text
    )
    new_fm = re.sub(
        r"(?m)^tags:\s*\[\s*\]\s*$", f"tags: {tag_str}", new_fm
    )

    if new_fm == fm_text:
        # Nothing to substitute (e.g., categories field uses different syntax).
        return False, None

    filepath.write_text(f"---\n{new_fm}\n---\n{body}", encoding="utf-8")
    return True, category


def iter_posts(posts_dir: Path) -> list[Path]:
    """Return all post files except section index files."""
    return sorted(
        p for p in posts_dir.rglob("*.md") if p.name != "_index.md"
    )


def main() -> int:
    if not POSTS_DIR.is_dir():
        print(f"Posts directory not found: {POSTS_DIR}", file=sys.stderr)
        return 1

    updated = 0
    category_counts: dict[str, int] = {}

    for filepath in iter_posts(POSTS_DIR):
        changed, category = update_post(filepath)
        if changed and category is not None:
            updated += 1
            category_counts[category] = category_counts.get(category, 0) + 1

    print(f"Updated {updated} posts")
    print("\nCategory distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
