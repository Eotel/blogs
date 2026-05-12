---
title: "Exa MCP"
description: "ニューラル検索エンジン Exa の MCP サーバー。Claude に高精度な Web 検索能力を追加する"
date: 2026-05-09
lastmod: 2026-05-12
aliases: ["Exa", "exa-mcp", "Exa neural search"]
related_posts:
  - "/posts/2026/04/2026-04-25-exa-for-claude-mcp-plugin/"
  - "/posts/2026/03/2026-03-05-b4b02c682a675d88c7200e82dba16420/"
tags: ["MCP", "Claude Code", "検索", "AIエージェント", "Web検索"]
---

## 概要

Exa は AI エージェント向けに設計されたニューラル検索エンジン。MCP（Model Context Protocol）サーバーとして提供されており、Claude に接続することで高精度な Web 検索能力を追加できる。従来のキーワード検索ではなくセマンティック検索を行い、意図に合った結果を返す。

## 特徴

- **ニューラル検索**: 意味的な類似度でウェブをインデックスし、クエリの意図に合った結果を返す
- **エージェント向け設計**: JSON 形式での構造化出力、信頼性の高い URL 取得
- **カテゴリフィルタ**: ニュース・学術論文・GitHub・会社情報などを絞り込み検索
- **コンテンツ取得**: URL からページ全文を取得するツール（Web スクレイピング代替）

## セットアップ（Claude Code）

```json
// ~/.claude/claude_desktop_config.json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "your-api-key"
      }
    }
  }
}
```

API キーは [exa.ai](https://exa.ai) で取得。無料枠あり。

## 主なツール

| ツール | 機能 |
|--------|------|
| `web_search_exa` | キーワード・セマンティック検索 |
| `web_fetch_exa` | URL からページ全文取得 |
| `web_search_advanced_exa` | カテゴリ・期間などの絞り込み付き検索 |

> ホスト版 (`https://mcp.exa.ai/mcp`) も利用可能。ローカル起動を避けたい場合はそちらを参照する。

## 関連ページ

- [MCP](/blogs/wiki/concepts/mcp/) — Exa が実装するプロトコル
- [Claude Code](/blogs/wiki/tools/claude-code/) — Exa MCP の利用環境
- [Google Workspace MCP](/blogs/wiki/tools/google-workspace-mcp/) — 別の MCP サーバー実装

## ソース記事

- [Exa for Claude — ニューラル検索を MCP で Claude に追加する](/blogs/posts/2026/04/2026-04-25-exa-for-claude-mcp-plugin/) — 2026-04-25
- [Google Workspace CLI（gws）— Drive・Gmail・Calendarを1コマンドで操作するAIエージェント対応ツール](/blogs/posts/2026/03/2026-03-05-b4b02c682a675d88c7200e82dba16420/) — 2026-03-05
