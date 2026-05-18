---
title: "mise"
description: "Rust 製 polyglot version manager。.tool-versions 互換で asdf の高速置き換えになり、タスクランナーと env var 管理も統合する。"
date: 2026-05-16
lastmod: 2026-05-16
aliases: ["rtx", "mise-en-place", "rtx-vm"]
related_posts:
  - "/posts/2026/05/2026-05-13-package-manager-history-2026/"
tags: ["パッケージ管理", "開発環境", "polyglot", "rust"]
---

## 概要

[mise](https://mise.jdx.dev/)（mise-en-place）は Jeff Dickey（jdx）が開発する Rust 製 polyglot version manager。asdf の `.tool-versions` フォーマットと互換性を保ちながら、起動速度の改善とタスクランナー・env var 管理の統合を実現する。

- **前身**: 2023-01-09 に `rtx` という名前で公開
- **リネーム**: 2024-01-10 のコミット `rename rtx-vm -> mise-en-dev` で `mise` に改称

## 主な機能

| 機能 | 説明 |
|---|---|
| **runtime 管理** | Node / Python / Ruby / Go / Rust など多言語のバージョンを `.tool-versions` または `mise.toml` で宣言 |
| **asdf 互換** | `.tool-versions` をそのまま読めるため asdf からの移行が無痛 |
| **タスクランナー** | `just` 風のタスク定義（`mise run build` など）|
| **env var 管理** | `.env` ライクな env var を `mise.toml` で宣言し、ディレクトリ切り替え時に自動設定 |
| **direnv 統合** | `direnv` と連携可能 |

## インストールと基本操作

```bash
# インストール
curl https://mise.run | sh

# バージョン追加・指定
mise use node@22
mise use python@3.12

# グローバルデフォルト
mise use -g node@lts

# 現在の環境確認
mise list
mise doctor
```

## 設定ファイル

`mise.toml`（または `.tool-versions` 互換形式）をプロジェクト直下に置く：

```toml
[tools]
node = "22"
python = "3.12"

[env]
DATABASE_URL = "postgres://localhost/dev"

[tasks.build]
run = "npm run build"
```

## asdf との比較

| 観点 | asdf | mise |
|---|---|---|
| 実装 | Go（v0.16〜、旧 Bash） | Rust |
| 起動速度 | やや遅い（旧 Bash 実装比） | 高速 |
| `.tool-versions` | ネイティブ | 互換読み込み |
| タスクランナー | なし | あり |
| env var 管理 | なし | あり |

既存の asdf ユーザーは `.tool-versions` を置き換えずに mise へ移行できる。

## 関連ページ

- [polyglot version manager](/blogs/wiki/concepts/polyglot-version-manager/) — カテゴリ全体の歴史と比較
- [moon (moonrepo)](/blogs/wiki/tools/moon/) — toolchain 管理に proto（同系列の Rust 製ツール）を使う monorepo ツール
