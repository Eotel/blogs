---
title: "LLM Wiki パターン"
description: "AI エージェントに個人ナレッジベースを継続的に構築・保守させるパターン"
date: 2026-04-05
lastmod: 2026-05-09
aliases: ["LLM Wiki", "Karpathy Wiki"]
related_posts:
  - "/posts/2026/04/karpathy-llm-wiki/"
  - "/posts/2026/04/2026-04-22-obsidian-claude-code-personal-os/"
  - "/posts/2026/04/2026-04-23-claude-code-obsidian-second-brain/"
tags: ["LLM", "ナレッジマネジメント", "AIエージェント", "RAG", "Obsidian"]
---

## 概要

Andrej Karpathy が提案した、LLM エージェントに個人ナレッジベース（Wiki）を継続的に構築・保守させるパターン。RAG が「毎回ゼロから読み直す」のに対し、LLM Wiki は知識を積み上げて複利的に成長させる。

## 三層構造

| 層 | 役割 | 誰が扱うか |
|---|---|---|
| **Raw Sources** | 論文・記事・メモなどの原本資料 | 人間がキュレーション、AI は読むだけ |
| **Wiki** | AI が生成・保守するマークダウン群 | AI が書き、人間が読む |
| **Schema** | AI への管理指示（構造・命名規則・ワークフロー） | 人間が定義 |

## 三つの基本操作

- **Ingest（取り込み）**: 新しい資料を投入し、AI に Wiki を更新させる
- **Query（質問）**: Wiki に対して質問し、統合的な回答を得る
- **Lint（保守）**: 矛盾・古い記述・孤立ページなどを定期チェック

## なぜ機能するか

人間が Wiki を放棄する主因は保守コスト。LLM は相互参照の更新、要約の最新化、一貫性維持を飽きずに続けられる。保守コストがほぼゼロになることで Wiki が持続する。

## Obsidian × Claude Code の実装

Karpathy の概念を実践する具体的な環境として、Obsidian と Claude Code の組み合わせが広まっている:

- **Obsidian** — ローカルファーストの Markdown PKM。AI が読み書きしやすいプレーンテキスト。バックリンク・グラフビューで関係性を可視化
- **Claude Code** — Obsidian の vault をそのまま読み込み、Wiki ページの生成・更新・相互参照を行う

Greg Isenberg が提案する 10 ステップのセットアップ:
1. Obsidian で vault を作る
2. Claude Code にプロジェクトルールを書く（CLAUDE.md）
3. `wiki-ingest` スキルで記事から Wiki を自動生成
4. `wiki-query` で質問を投げ、引用付き回答を得る
5. `wiki-lint` で孤立ページ・矛盾を定期クリーンアップ

ワークフロー上の分業: 「左画面に Claude Code → 右画面に Obsidian」でリアルタイムに Wiki が育つ。

## `.raw/` パターン（Karpathy 実装）

Karpathy のオリジナル実装では:
- `.raw/` フォルダに元記事・論文・メモを投入
- Claude Code が `.raw/` を読んで `wiki/` を生成・更新
- 人間は `wiki/` だけを読む

## 関連ページ

- [コンテキスト圧縮](/blogs/wiki/concepts/context-compression/) — LLM の文脈管理における関連技術
- [Claude Code](/blogs/wiki/tools/claude-code/) — LLM Wiki の実行環境として利用可能
- [Obsidian](/blogs/wiki/tools/obsidian/) — LLM Wiki の保存・閲覧基盤
- [RAG](/blogs/wiki/concepts/rag/) — LLM Wiki が解決する RAG の限界

## ソース記事

- [Karpathy の LLM Wiki — AIエージェントが育てる個人ナレッジベースという新パターン](/blogs/posts/2026/04/karpathy-llm-wiki/) — 2026-04-05
- [Claude Code × Obsidian で「第二の脳」を構築する — Greg Isenberg の 10 ステップ](/blogs/posts/2026/04/2026-04-22-obsidian-claude-code-personal-os/) — 2026-04-22
- [LLM Wiki パターンを Obsidian と Claude Code で実装する](/blogs/posts/2026/04/2026-04-23-claude-code-obsidian-second-brain/) — 2026-04-23
