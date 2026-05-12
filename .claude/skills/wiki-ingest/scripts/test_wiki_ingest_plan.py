#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "wiki_ingest_plan.py"
SPEC = importlib.util.spec_from_file_location("wiki_ingest_plan", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
wiki_ingest_plan = importlib.util.module_from_spec(SPEC)
sys.modules["wiki_ingest_plan"] = wiki_ingest_plan
SPEC.loader.exec_module(wiki_ingest_plan)

APPLY_SCRIPT = Path(__file__).resolve().parent / "wiki_ingest_apply.py"
APPLY_SPEC = importlib.util.spec_from_file_location("wiki_ingest_apply", APPLY_SCRIPT)
assert APPLY_SPEC is not None and APPLY_SPEC.loader is not None
wiki_ingest_apply = importlib.util.module_from_spec(APPLY_SPEC)
sys.modules["wiki_ingest_apply"] = wiki_ingest_apply
APPLY_SPEC.loader.exec_module(wiki_ingest_apply)


class WikiIngestPlanTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "content" / "wiki" / "concepts").mkdir(parents=True)
        (self.root / "content" / "wiki" / "tools").mkdir(parents=True)
        (self.root / "content" / "wiki" / "guides").mkdir(parents=True)
        (self.root / "content" / "posts" / "2026" / "04").mkdir(parents=True)
        (self.root / ".claude" / "temp").mkdir(parents=True)
        self.write(
            "content/wiki/tools/claude-code.md",
            """---
title: "Claude Code"
description: "CLI AI coding agent"
date: 2026-04-01
lastmod: 2026-04-20
aliases: ["claude-code", "ClaudeCode"]
related_posts:
  - "/posts/2026/04/2026-04-20-covered/"
tags: ["Claude Code", "AIエージェント"]
---

## 概要

Claude Code は AI エージェントの実行環境。
""",
        )
        self.write(
            "content/wiki/concepts/llm-wiki-pattern.md",
            """---
title: "LLM Wiki パターン"
description: "知識を積み上げる Wiki 運用"
date: 2026-04-01
lastmod: 2026-04-01
aliases: ["Karpathy Wiki"]
related_posts: []
tags: ["LLM", "Wiki", "Obsidian"]
---

Karpathy の LLM Wiki は Obsidian と Markdown で知識を育てる。
""",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def plan(self, target: str, since=None):
        return wiki_ingest_plan.build_plan(self.root, target, since, limit=5)

    def test_related_posts_is_covered(self) -> None:
        self.write(
            "content/posts/2026/04/2026-04-20-covered.md",
            """---
title: "Covered post"
date: 2026-04-20
lastmod: 2026-04-20
categories: ["AI/LLM"]
tags: ["Claude Code"]
---

Already covered.
""",
        )
        item = self.plan("all")["articles"][0]
        self.assertEqual(item["status"], "covered")
        self.assertEqual(item["candidates"][0]["wiki"], "tools/claude-code.md")

    def test_alias_match_is_update_candidate(self) -> None:
        self.write(
            "content/posts/2026/04/2026-04-21-claude-code-workflow.md",
            """---
title: "ClaudeCode の運用ワークフロー"
date: 2026-04-21
categories: ["AI/LLM"]
tags: ["Claude Code", "AIエージェント"]
---

ClaudeCode を使って日々の開発タスクを自動化する。
""",
        )
        item = self.plan("all")["articles"][0]
        self.assertEqual(item["status"], "update_candidate")
        self.assertEqual(item["candidates"][0]["wiki"], "tools/claude-code.md")

    def test_japanese_fts_returns_review_candidate(self) -> None:
        self.write(
            "content/posts/2026/04/2026-04-22-karpathy-wiki.md",
            """---
title: "Karpathy の知識管理"
date: 2026-04-22
categories: ["AI/LLM"]
tags: ["ナレッジ管理"]
---

Obsidian と Markdown を使って LLM が Wiki を継続的に更新する。
""",
        )
        item = self.plan("all")["articles"][0]
        self.assertIn(item["status"], {"review_candidate", "update_candidate"})
        self.assertEqual(item["candidates"][0]["wiki"], "concepts/llm-wiki-pattern.md")

    def test_since_filters_posts(self) -> None:
        self.write(
            "content/posts/2026/04/2026-04-10-old.md",
            """---
title: "Old"
date: 2026-04-10
categories: ["AI/LLM"]
tags: ["old"]
---

old
""",
        )
        self.write(
            "content/posts/2026/04/2026-04-22-new.md",
            """---
title: "New"
date: 2026-04-22
categories: ["AI/LLM"]
tags: ["new"]
---

new
""",
        )
        plan = self.plan("all", wiki_ingest_plan.parse_date("2026-04-15"))
        self.assertEqual(plan["posts"], 1)
        self.assertTrue(plan["articles"][0]["post"].endswith("2026-04-22-new.md"))

    def test_json_cli_shape(self) -> None:
        self.write(
            "content/posts/2026/04/2026-04-22-new.md",
            """---
title: "New"
date: 2026-04-22
categories: ["AI/LLM"]
tags: ["new"]
---

new
""",
        )
        output = subprocess.check_output(
            [
                sys.executable,
                str(SCRIPT),
                "all",
                "--root",
                str(self.root),
                "--format",
                "json",
            ],
            text=True,
        )
        data = json.loads(output)
        self.assertEqual(data["target"], "all")
        self.assertEqual(data["posts"], 1)
        self.assertIn("articles", data)

    def test_apply_adds_related_post_and_source_line(self) -> None:
        fm = """title: "Test"
date: 2026-04-01
lastmod: 2026-04-01
aliases: []
related_posts: []
tags: ["test"]"""
        fm, changed = wiki_ingest_apply.add_related_post(
            fm, "/posts/2026/04/example/", "2026-05-12"
        )
        self.assertTrue(changed)
        self.assertIn('  - "/posts/2026/04/example/"', fm)
        self.assertIn("lastmod: 2026-05-12", fm)
        body, body_changed = wiki_ingest_apply.add_source_line(
            "## 概要\n\n本文",
            "/posts/2026/04/example/",
            "Example",
            "2026-04-22",
        )
        self.assertTrue(body_changed)
        self.assertIn("## ソース記事", body)
        self.assertIn("[Example](/blogs/posts/2026/04/example/)", body)

    def test_apply_renders_backlog(self) -> None:
        backlog = [
            {
                "post_url": "/posts/hello/",
                "title": "はじめての記事",
                "date": "2026-03-08",
                "status": "new_candidate",
            }
        ]
        text = wiki_ingest_apply.render_backlog(backlog, "2026-05-12")
        self.assertIn('title: "Wiki ingest backlog"', text)
        self.assertIn('  - "/posts/hello/"', text)
        self.assertIn("[はじめての記事](/blogs/posts/hello/)", text)

    def test_apply_preserves_existing_backlog_coverage(self) -> None:
        plan = {
            "articles": [
                {
                    "post_url": "/posts/2026/04/old/",
                    "title": "Old unresolved",
                    "date": "2026-04-01",
                    "status": "covered",
                    "candidates": [
                        {"wiki": "guides/wiki-ingest-backlog-2026-new_candidate.md"}
                    ],
                },
                {
                    "post_url": "/posts/2026/04/new/",
                    "title": "New unresolved",
                    "date": "2026-04-02",
                    "status": "new_candidate",
                    "candidates": [],
                },
            ]
        }
        wiki_ingest_apply.apply_plan(
            root=self.root,
            plan=plan,
            policy="all",
            max_candidates=5,
            backlog_rel="guides/wiki-ingest-backlog.md",
            today="2026-05-12",
            dry_run=False,
        )
        shard = (
            self.root / "content/wiki/guides/wiki-ingest-backlog-2026-new_candidate.md"
        )
        text = shard.read_text(encoding="utf-8")
        self.assertIn('  - "/posts/2026/04/old/"', text)
        self.assertIn('  - "/posts/2026/04/new/"', text)


if __name__ == "__main__":
    unittest.main()
