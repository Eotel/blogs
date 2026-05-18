---
title: "moon (moonrepo)"
description: "Rust 製 monorepo orchestration ツール。task runner・project graph・incremental cache・toolchain 統合を 1 つにまとめる。"
date: 2026-05-16
lastmod: 2026-05-16
aliases: ["moonrepo", "moon monorepo"]
related_posts:
  - "/posts/2026/05/2026-05-13-moon-monorepo-orchestration/"
tags: ["monorepo", "task-runner", "build-system", "rust", "toolchain"]
---

## 概要

[moon](https://moonrepo.dev/) は `moonrepo` が開発する Rust 製の monorepo 管理ツール（MIT ライセンス）。task runner・project / dependency graph・incremental cache・language toolchain 自動化を 1 つにまとめる。2026-02 に v2 が stable 化し、v2.2.4 まで進んでいる（2026-05 時点）。

## 主な機能

| 機能 | 説明 |
|---|---|
| **task runner** | `<project>:<task>` 形式で各パッケージの build / test などを統一実行 |
| **project / dependency graph** | `dependsOn` から DAG を構築し、トポロジカル並列実行 |
| **incremental cache** | input/output の SHA256 hash でローカル + remote cache を制御 |
| **toolchain 統合** | Node / Bun / Deno / Rust / Go / Python（unstable）のランタイムを proto 経由で自動管理 |
| **task inheritance** | `.moon/tasks/**/*.yml` でグローバル task を宣言し、project 単位で上書き |

## 設定ファイル

| ファイル | 役割 |
|---|---|
| `.moon/workspace.yml` | workspace 全体（project glob、VCS 設定）|
| `.moon/toolchains.yml` | 言語ランタイムとバージョン（v2 で rename）|
| `<project>/moon.yml` | project 単位の type・language・dependsOn・tasks |

## remote cache — moonbase は discontinued

moonrepo はかつて **moonbase** という SaaS remote cache を提供していたが、**discontinued** になっている。現在の公式推奨は [Bazel Remote Execution API v2](https://github.com/bazelbuild/remote-apis) 互換サーバー：

- セルフホスト: [bazel-remote](https://github.com/buchgr/bazel-remote)（S3 / GCS / disk backend）
- マネージド: [Depot Cache](https://depot.dev/products/cache)

`.moon/workspace.yml` での設定例：

```yaml
remote:
  host: 'grpcs://cache.internal:9092'
  auth:
    token: 'MOON_REMOTE_TOKEN'
```

古い `moonbase:` セクションは v2 以降では動かない。

## proto との関係

[proto](https://github.com/moonrepo/proto) は moonrepo が並行開発する multi-language version manager。`.moon/toolchains.yml` でバージョンを指定すると moon が proto 経由でランタイムを自動インストールする。`.prototools` で moon 自身のバージョンも pin 可能。

## 他ツールとの比較

| ツール | 対象 | polyglot | remote cache |
|---|---|---|---|
| moon | Web + 一部 polyglot | 中程度 | Bazel REAPI |
| Turborepo | JS/TS 中心 | 間接的 | Vercel Remote Cache |
| Nx | enterprise / plugin | プラグイン経由 | Nx Cloud |
| Bazel | 真の polyglot | 強い | REAPI ネイティブ |

moon が向く場面: Node/TypeScript 中心だが一部 Rust/Go/Python が混ざる中規模 monorepo、ツールチェイン統合の恩恵が欲しいチーム。

## 代表コマンド

```bash
moon run web:build        # 単一 target 実行
moon ci                   # 影響範囲の自動検出・差分実行（CI 向け）
moon check --all          # 全 project を一括チェック
moon project-graph        # project DAG の可視化
moon action-graph web:build  # action DAG の可視化
```

## 関連ページ

- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) — monorepo の「コードの分け方」を整理
