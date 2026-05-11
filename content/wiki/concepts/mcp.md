---
title: "MCP (Model Context Protocol)"
description: "LLM が外部ツール・データベースと通信するためのオープンプロトコル"
date: 2026-04-06
lastmod: 2026-05-11
aliases: ["MCP", "Model Context Protocol"]
related_posts:
  - "/posts/2026/03/openclaw-claude-code-setup/"
  - "/posts/2026/03/sd-202604/"
  - "/posts/2026/05/2026-05-11-truss-c-openframeworks-alternative/"
  - "/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/"
tags: ["MCP", "protocol", "agent", "integration"]
---

## 概要

Anthropic が主導する、AI モデルと外部システムの連携のためのオープンプロトコル。Claude Code、Cursor など主要 AI ツールで採用が進み、AWS、GitHub、Google Workspace など主要プラットフォームが MCP Server を公開。

## 特徴

- ベンダーロックインを避けた相互運用性
- ツール定義の標準化（JSON Schema ベース）
- サブミリ秒レイテンシでの動作

## 関連ページ

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — MCP を利用してツール連携するシステム
- [Claude Code](/blogs/wiki/tools/claude-code/) — MCP の主要クライアント実装
- [GenAI-DrawIO-Creator](/blogs/wiki/tools/draw-io-ai/) — MCP 経由で図を生成する Claude Code 連携ツール
- [TrussC](/blogs/wiki/tools/trussc/) — MCP サーバをコアに組み込み、アプリ自身が AI から JSON-RPC で操作できるクリエイティブコーディングフレームワーク

## ソース記事

- [SD 2026年4月号](/blogs/posts/2026/03/sd-202604/) — 2026-03
- [TrussC: openFrameworks に着想を得た sokol ベースの C++ クリエイティブコーディングフレームワーク](/blogs/posts/2026/05/2026-05-11-truss-c-openframeworks-alternative/) — 2026-05-11
- [AWS が Skills フォーマットに合流 — Agent Toolkit for AWS の Skills を Strands Agents から呼ぶ](/blogs/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/) — 2026-05-11（MCP を介さない Skills ローカル読み込みの対比事例）
