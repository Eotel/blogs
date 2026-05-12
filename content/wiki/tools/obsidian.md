---
title: "Obsidian"
description: "ローカルファーストの Markdown ベース PKM（個人知識管理）ツール。データはすべて自分のマシンに保存されベンダーロックインなし"
date: 2026-04-23
lastmod: 2026-05-12
aliases: ["オブシディアン", "PKM", "Personal Knowledge Management", "第二の脳"]
related_posts:
  - "/posts/2026/04/2026-04-17-obsidian-pkm-second-brain/"
  - "/posts/2026/04/2026-04-22-obsidian-claude-code-personal-os/"
  - "/posts/2026/04/2026-04-23-claude-code-obsidian-second-brain/"
  - "/posts/2026/03/2026-03-05-00a5a21b56da09807d7c114573cbcf14/"
  - "/posts/2026/04/2026-04-09-exbrain-claude-code-obsidian-ai-brain/"
tags: ["PKM", "ナレッジ管理", "Markdown", "ツール", "Claude Code", "LLM Wiki"]
---

## 概要

Obsidian はローカルファイルベースの Markdown エディタであり、個人の知識管理（PKM）に特化したツール。個人利用は完全無料、データはすべて自分のマシン上の `.md` ファイルとして保存されるため、ベンダーロックインがない。2,700 種以上のコミュニティプラグインが存在する。

## 設計哲学

「Your thoughts are yours（あなたの思考はあなたのもの）」。ローカルファースト・プレーンテキスト・オフライン動作・ベンダーロックインなしを基本原則とする。

## 主な機能

- **バックリンクとグラフビュー**: ノート間の双方向リンクと視覚的な知識マップ
- **Dataview プラグイン**: Markdown ファイルをデータベースとしてクエリ
- **Templater**: 動的テンプレートで繰り返し作業を自動化
- **Canvas**: ホワイトボード的なビジュアル思考ツール
- **AI 連携**: Smart Composer / Copilot プラグインで LLM をノート作成に統合

## 料金

| プラン | 価格 | 用途 |
|---|---|---|
| 個人 | 無料 | 個人利用 |
| Commercial | $50/年 | 商用利用 |
| Sync | $4/月（年払い）／ $5/月（月払い） | デバイス間同期 |
| Publish | $8/月（年払い）／ $10/月（月払い） | Web 公開 |

## Claude Code との統合（LLM Wiki パターン）

Obsidian の vault は Markdown ファイルの集合であり、Claude Code が直接読み書きできる。これにより [LLM Wiki パターン](/blogs/wiki/concepts/llm-wiki-pattern/)の実装基盤となる:

- Obsidian vault = Wiki の保存場所（人間が読む）
- Claude Code = Wiki の生成・更新エンジン（AI が書く）
- CLAUDE.md = Wiki の構造・命名規則を定義するスキーマ

Greg Isenberg の「Claude Code × Obsidian = Personal OS」では、この組み合わせを「思考を外部化して AI に拡張させるOS」と位置づけている。ワークフロー: 「左画面に Claude Code、右画面に Obsidian」で、AI がリアルタイムに vault を更新する。

## 関連ページ

- [LLM Wiki パターン](/blogs/wiki/concepts/llm-wiki-pattern/) — Obsidian を基盤とした AI 知識管理パターン
- [Claude Code](/blogs/wiki/tools/claude-code/) — Obsidian vault を操作する AI エンジン
- [Open-notebook](/blogs/wiki/tools/open-notebook/) — NotebookLM のオープンソース代替、セルフホスト型 AI ナレッジベース

## ソース記事

- [Obsidian 完全ガイド — ローカルファーストで「第二の脳」を構築する](/blogs/posts/2026/04/2026-04-17-obsidian-pkm-second-brain/) — 2026-04-17
- [Claude Code × Obsidian で「第二の脳」を構築する — Greg Isenberg の 10 ステップ](/blogs/posts/2026/04/2026-04-22-obsidian-claude-code-personal-os/) — 2026-04-22
- [LLM Wiki パターンを Obsidian と Claude Code で実装する](/blogs/posts/2026/04/2026-04-23-claude-code-obsidian-second-brain/) — 2026-04-23
- [Obsidian × Claude Code で「AIセカンドブレイン」を構築する — コンテキストがプロンプトに勝つ時代](/blogs/posts/2026/03/2026-03-05-00a5a21b56da09807d7c114573cbcf14/) — 2026-03-05
- [Exbrain — Claude Code × Obsidian で「外付けAI脳」を構築する](/blogs/posts/2026/04/2026-04-09-exbrain-claude-code-obsidian-ai-brain/) — 2026-04-09
