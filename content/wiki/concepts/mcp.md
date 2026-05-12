---
title: "MCP (Model Context Protocol)"
description: "LLM が外部ツール・データベースと通信するためのオープンプロトコル"
date: 2026-04-06
lastmod: 2026-05-12
aliases: ["MCP", "Model Context Protocol"]
related_posts:
  - "/posts/2026/03/openclaw-claude-code-setup/"
  - "/posts/2026/03/sd-202604/"
  - "/posts/2026/05/2026-05-11-truss-c-openframeworks-alternative/"
  - "/posts/2026/05/2026-05-11-aws-agent-toolkit-strands-skills/"
  - "/posts/2026/03/2026-03-01-0ee19b59603fd68d6a0295e4e94ac6f9/"
  - "/posts/2026/03/2026-03-03-8feec16470c6e442ce0b999e472ec095/"
  - "/posts/2026/03/2026-03-03-eccd6b7eeb61d1f6278961cf6717e3ec/"
  - "/posts/2026/03/2026-03-04-4aef4c49d26cce4394f04e3ffebfb7fe/"
  - "/posts/2026/03/2026-03-04-a0e7a789ef7534c7cb6136d7fb00572e/"
  - "/posts/2026/03/2026-03-04-ae50e162a7b49d5efc0a3b1f21a449db/"
  - "/posts/2026/03/2026-03-05-1f81385148befa3ee0e980408c174676/"
  - "/posts/2026/03/2026-03-10-freee-mcp-claude-code/"
  - "/posts/2026/03/2026-03-22-mcp-oauth21-security/"
  - "/posts/2026/03/2026-03-25-claude-code-expert-agents/"
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
- [MCP のトークン消費問題 — スキーマ注入で 55,000 トークン、CLI は 35 倍効率的](/blogs/posts/2026/03/2026-03-01-0ee19b59603fd68d6a0295e4e94ac6f9/) — 2026-03-01
- [MCP サーバーを増やしてもコンテキストを食わせない — Claude Code の Tool Search でトークン消費を95%削減](/blogs/posts/2026/03/2026-03-03-8feec16470c6e442ce0b999e472ec095/) — 2026-03-03
- [Claude Code / MCP を安全に使うための実践ガイド — settings.json の多層防御と deny の落とし穴](/blogs/posts/2026/03/2026-03-03-eccd6b7eeb61d1f6278961cf6717e3ec/) — 2026-03-03
- [「MCPは死んだ、CLIに栄光あれ」— Playwright CLI が出した結論と、それでもMCPが生き残る理由](/blogs/posts/2026/03/2026-03-04-4aef4c49d26cce4394f04e3ffebfb7fe/) — 2026-03-04
- [Claude Code Skills × 自己完結スクリプト — MCP/CLIの先にある「トークン効率」設計](/blogs/posts/2026/03/2026-03-04-a0e7a789ef7534c7cb6136d7fb00572e/) — 2026-03-04
- [labor-law-mcp — Claude の労務ハルシネーションを防ぐ MCP サーバーと「一次情報/二次情報」の設計思想](/blogs/posts/2026/03/2026-03-04-ae50e162a7b49d5efc0a3b1f21a449db/) — 2026-03-04
- [Claude-Native Designer — デザイナーが「作る人」になるFigma MCP × Claude Codeワークフロー](/blogs/posts/2026/03/2026-03-05-1f81385148befa3ee0e980408c174676/) — 2026-03-05
- [freee MCP × Claude Code で確定申告の仕訳1,428件を20分で終わらせた話](/blogs/posts/2026/03/2026-03-10-freee-mcp-claude-code/) — 2026-03-10
- [MCP のセキュリティが OAuth 2.1 で大幅進化：AI エージェントと社内データを安全に接続する仕組み](/blogs/posts/2026/03/2026-03-22-mcp-oauth21-security/) — 2026-03-22
- [Claude Codeで「専門家チーム」を構築する：カスタムエージェントとCoworkの活用法](/blogs/posts/2026/03/2026-03-25-claude-code-expert-agents/) — 2026-03-25
