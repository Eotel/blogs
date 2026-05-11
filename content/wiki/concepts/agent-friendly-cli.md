---
title: "エージェントフレンドリー CLI"
description: "LLM エージェントが確実に操作できる CLI の設計原則。安定した JSON 出力・What/Why/Hint エラー・段階的ヘルプ・ヘッドレス認証など"
date: 2026-05-09
lastmod: 2026-05-09
aliases: ["agent-friendly CLI", "LLM CLI設計"]
related_posts:
  - "/posts/2026/05/2026-05-08-agent-friendly-cli-for-llm/"
tags: ["CLI", "AIエージェント", "開発ツール", "設計パターン", "LLM"]
---

## 概要

LLM エージェントを操作主体として設計された CLI の原則。人間が直感的に読める出力と、AI が確実にパースできる出力は異なる。エージェントが自律的に CLI を操作するユースケースが増えるにつれ、「エージェントフレンドリー」な設計が重要になっている。

## 設計原則

### 1. 安定した JSON 出力（stdout/stderr 分離）

```bash
# BAD: 人間向けの混在出力
echo "Processing... done! Result: 42"

# GOOD: JSON を stdout、ログを stderr に分離
echo '{"status":"ok","result":42}' >&1
echo "[INFO] Processing complete" >&2
```

LLM はテキストのパターンマッチングに頼らざるを得ない。JSON で構造化された stdout を返すことで、エージェントが確実に値を抽出できる。

### 2. What/Why/Hint エラーメッセージ

```json
{
  "error": "INVALID_CONFIG",
  "what": "設定ファイルに必須キーが存在しません",
  "why": "api_key は認証に必要です",
  "hint": "MYAPP_API_KEY 環境変数を設定するか、config.yaml に api_key を追記してください"
}
```

エラーの「何が」「なぜ」「どう直すか」を構造化することで、エージェントがエラーから自律的に回復できる。

### 3. 段階的ヘルプ（Staged Help）

```bash
# レベル1: 概要のみ
myapp --help

# レベル2: サブコマンド詳細
myapp deploy --help

# レベル3: 完全リファレンス
myapp --help-full
```

一度に全ドキュメントを出力するとコンテキストウィンドウを消費する。段階的に開示することでエージェントのトークン消費を抑える。

### 4. エスケープハッチ（Escape Hatches）

- `--dry-run` — 実行せずに何が起きるかを確認
- `--output json` — 出力形式を強制指定
- `--yes` / `--non-interactive` — インタラクティブプロンプトをスキップ
- `--timeout <seconds>` — タイムアウトを明示的に指定

エージェントはインタラクティブな入力を求められると止まる。`--non-interactive` フラグで回避できる設計が必要。

### 5. ヘッドレス認証

```bash
# BAD: ブラウザを開く OAuth フロー
myapp login  # → ブラウザが開く → エージェントは操作不能

# GOOD: トークンを環境変数で渡す
MYAPP_TOKEN=xxx myapp --token-from-env deploy
```

## 既存ツールとの適合性

| ツール | エージェントフレンドリー度 | 備考 |
|--------|--------------------------|------|
| `gh` (GitHub CLI) | 高 | `--json` フラグ対応、エラーも構造化 |
| `kubectl` | 中〜高 | `-o json` 対応、ただしエラーメッセージは改善余地あり |
| `npm` / `pip` | 低〜中 | ログと結果が混在しがち |
| `curl` | 中 | `-s -f` フラグで制御可能 |

## Claude Code での活用

Claude Code は Bash ツールで CLI を呼び出す。エージェントフレンドリーな CLI を使うと:
- ツール実行結果を JSON でパースできる
- エラーから自律回復できる（Hint を次のアクションに使う）
- `--dry-run` で安全に計画段階の確認ができる

## 関連ページ

- [Claude Code](/blogs/wiki/tools/claude-code/) — エージェントフレンドリー CLI の利用環境
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) — CLI をハーネス設計に組み込む方法
- [MCP](/blogs/wiki/concepts/mcp/) — CLI の代わりに構造化インターフェースを提供するプロトコル

## ソース記事

- [LLM エージェントのための CLI 設計原則 — What/Why/Hint エラーと段階的ヘルプ](/blogs/posts/2026/05/2026-05-08-agent-friendly-cli-for-llm/) — 2026-05-08
