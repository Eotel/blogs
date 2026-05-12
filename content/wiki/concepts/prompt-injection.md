---
title: "プロンプトインジェクション"
description: "ユーザー入力にシステムプロンプトを改ざんするコードを混在させる攻撃手法"
date: 2026-04-06
lastmod: 2026-05-12
aliases: ["Prompt Injection"]
related_posts:
  - "/posts/2026/03/vibe-hacking/"
  - "/posts/2026/03/claude-code-security-theater/"
  - "/posts/2026/03/2026-03-02-67f7657965c1f660dfbad9b0e88d0414/"
  - "/posts/2026/03/2026-03-31-chatgpt-dns-tunneling-data-leak/"
tags: ["セキュリティ", "LLM", "脆弱性", "攻撃"]
---

## 概要

ユーザー入力を指示として実行する設計の脆弱性。検索入力やファイル内容に「今後の指示を無視して○○をしろ」と埋め込まれる。エージェント普及で更に深刻化。

## 対策

- CLAUDE.md のルール記述は「お願い」に過ぎず、プロンプトインジェクションで回避可能
- 実効的防御はシステムレベルの制約（サンドボックス、deny ルール、PreToolUse フック）
- devcontainer での完全隔離が最も堅牢

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — 攻撃対象となるシステム
- [Claude Code](/blogs/wiki/tools/claude-code/) — セキュリティ機能の実装
- [Exposure Management](/blogs/wiki/concepts/exposure-management/) — 脆弱性を「攻撃成立可能性」で評価する考え方

## ソース記事

- [Vibe Hacking](/blogs/posts/2026/03/vibe-hacking/) — 2026-03
- [Claude Code セキュリティシアター](/blogs/posts/2026/03/claude-code-security-theater/) — 2026-03
- [AIコーディングツール導入でMCC乗っ取り被害 — Antigravity・Claude Codeの脆弱性とシャドーAI対策](/blogs/posts/2026/03/2026-03-02-67f7657965c1f660dfbad9b0e88d0414/) — 2026-03-02
- [ChatGPTのコード実行環境にDNSトンネリングによるデータ漏洩の脆弱性が発覚](/blogs/posts/2026/03/2026-03-31-chatgpt-dns-tunneling-data-leak/) — 2026-03-31
