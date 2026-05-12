---
title: "Google Workspace MCP"
description: "Google 公式の MCP サーバー。Gmail・カレンダー・ドライブ・スプレッドシートを Claude から直接操作できる"
date: 2026-05-09
lastmod: 2026-05-12
aliases: ["Google MCP", "Workspace MCP"]
related_posts:
  - "/posts/2026/04/2026-04-23-google-workspace-mcp-server/"
tags: ["MCP", "Google", "Gmail", "Google Calendar", "Claude Code", "自動化"]
---

## 概要

Google が公式に提供する MCP（Model Context Protocol）サーバー。Claude に接続することで Gmail・Google カレンダー・Google ドライブ・スプレッドシートなどの Workspace サービスを AI から直接操作できる。

## 対応サービス

| サービス | 主な操作 |
|---------|---------|
| **Gmail** | メール送受信・検索・ラベル管理 |
| **Google Calendar** | 予定の作成・変更・検索 |
| **Google Drive** | ファイル検索・作成・共有 |
| **Google Sheets** | セル読み書き・シート操作 |
| **Google Docs** | ドキュメント作成・編集 |

## セットアップ

Google 公式版は **リモートマネージド MCP サーバー**（`*.googleapis.com` の OAuth エンドポイント）として提供される。ローカルで `uvx` や `npm` パッケージを起動する形ではない点に注意。

### 公式リモートサーバー利用フロー

1. Google Cloud Console で対象 API（Gmail / Calendar / Drive 等）を有効化
2. OAuth クライアント認証情報を作成（Desktop or Web）
3. Claude Code の `mcpServers` に該当の HTTPS エンドポイント（例: `gmailmcp.googleapis.com`）を OAuth 接続として登録

詳細は [Configure the Google Workspace MCP servers](https://developers.google.com/workspace/guides/configure-mcp-servers) を参照。

### コミュニティ版（ローカル MCP）

公式に加え、個人が `uvx`/`npx` 経由で動かすコミュニティ実装も複数あるが、認証スコープや更新頻度に差があるため自己責任で選定する。

## 活用例

- **メール自動作成**: 「この件名でこの内容のメールを送って」
- **スケジュール調整**: 「来週空いている会議時間を 3 つ提案して」
- **スプレッドシート分析**: 「この CSV を読み込んで売上推移を計算して」
- **ドキュメント生成**: 「この会議メモを元に議事録を作成して」

## 注意点

- Google アカウントへの OAuth 権限が必要（ユーザーが承認）
- センシティブなデータ（メール本文など）が Claude に渡る点を理解した上で使用
- API クォータ制限が適用される（高頻度自動化には注意）

## 関連ページ

- [MCP](/blogs/wiki/concepts/mcp/) — Google Workspace MCP が実装するプロトコル
- [Claude Code](/blogs/wiki/tools/claude-code/) — MCP サーバーの接続環境
- [Exa MCP](/blogs/wiki/tools/exa-mcp/) — 別の MCP サーバー実装（Web 検索）

## ソース記事

- [Google Workspace 公式 MCP サーバー — Gmail・カレンダーを Claude から操作する](/blogs/posts/2026/04/2026-04-23-google-workspace-mcp-server/) — 2026-04-23
