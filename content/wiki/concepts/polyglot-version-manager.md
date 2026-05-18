---
title: "polyglot version manager"
description: "複数言語のランタイムを統一インタフェースで管理するツール群。asdf を祖とし、mise / proto / pkgx が後継として並走している。"
date: 2026-05-16
lastmod: 2026-05-16
aliases: ["multi-language version manager", "runtime version manager"]
related_posts:
  - "/posts/2026/05/2026-05-13-package-manager-history-2026/"
tags: ["パッケージ管理", "開発環境", "asdf", "mise", "proto"]
---

## 概要

「プロジェクトごとに違う言語バージョンを使う」問題を、**複数言語にまたがって統一的に解決する**ツールカテゴリ。2000 年代の単一言語 version manager（rvm / nvm / pyenv）の乱立を統合する形で生まれた。

## 歴史

### 単一言語 version manager 時代（2009–2014）

`rvm`（Ruby）→ `nvm`（Node）→ `rbenv`（Ruby）→ `pyenv`（Python）と、**各言語コミュニティが同じ shim パターンを再実装**し続けた。`~/.rbenv/shims/ruby` のような「本物を解決して exec する偽バイナリ」を PATH に挟む方式で、言語数だけ似た shim ツールが乱立した（shim 戦争）。

### asdf による統合（2014）

2014 年 11 月、Elixir コミュニティの Akash Manohar（HashNuke）が `asdf` をリリース。「1 つの shim で全部やる」発想で `~/.tool-versions` に宣言した言語・バージョンをプラグイン経由で解決し、polyglot プロジェクトのデファクトになった。

### Rust / Go 実装への移行（2023–2026）

asdf は Bash 製のため起動が遅いという弱点があった。2023 年に同時多発的に高速な後継が登場：

| ツール | 初出 | 実装 | 特徴 |
|---|---|---|---|
| **mise** | 2023-01（rtx として） | Rust | `.tool-versions` 互換・tasks・env var 管理を統合 |
| **proto** | 2023-02 | Rust | moonrepo の toolchain 基盤として開発、後にスタンドアロン化 |
| **pkgx** | 2021（tea として） | — | `pkgx node@20 script.ts` のような 1 行実行思想 |
| **asdf v0.16** | 2025-01 | Go | 本家が Go 実装に書き換え |

`asdf` の `.tool-versions` フォーマットは mise も proto も互換読み込みを提供しており、**形式は残り、エンジンが入れ替わった**。

## shim 方式 vs shell hook 方式

| 方式 | 仕組み | 代表 |
|---|---|---|
| **shim** | 偽バイナリを PATH に挟む。shell 非依存 | rbenv、asdf |
| **shell hook** | `cd` 時に `.envrc` 等を評価して PATH を書き換える | direnv、mise の env 機能 |

shim 方式は shell を選ばず安定しているが、起動オーバーヘッドがある。shell hook は高速だが shell 依存で副作用に注意。

## 主要ツールの比較

| ツール | 実装 | `.tool-versions` 互換 | tasks | env var |
|---|---|---|---|---|
| asdf | Go（v0.16〜） | ネイティブ | なし | なし |
| mise | Rust | ◯ | ◯（just 風） | ◯ |
| proto | Rust | △（互換読み込みあり） | △ | △ |
| pkgx | — | — | — | — |

## 関連ページ

- [APM（Agent Package Manager）](/blogs/wiki/tools/apm/) — AI エージェント設定を npm のように管理する新しいレイヤ
- [moon (moonrepo)](/blogs/wiki/tools/moon/) — proto を toolchain 基盤として使う monorepo ツール
- [mise](/blogs/wiki/tools/mise/) — 現時点で最も広く採用されている polyglot version manager
