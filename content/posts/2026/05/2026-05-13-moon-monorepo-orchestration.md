---
title: "monorepo の orchestration tool — moon (moonrepo) 入門"
slug: "2026-05-13-moon-monorepo-orchestration"
description: "Rust 製 monorepo orchestration ツール moon (moonrepo) v2 の入門。task runner / project graph / incremental cache の仕組み、proto との toolchain 統合、moonbase 廃止後の Bazel REAPI 互換 remote cache 構成までを Turborepo・Nx・Bazel と比較しながら整理する。"
date: 2026-05-13
lastmod: 2026-05-13
draft: false
author: "eotel"
model: "claude-opus-4-7"
categories: ["ツール/開発環境"]
tags: ["monorepo", "moon", "turborepo", "nx", "task-runner"]
---

## TL;DR

- [moon (moonrepo)](https://moonrepo.dev/) は Rust 製の monorepo 管理ツール。task runner、project / dependency graph、incremental cache、language toolchain 自動化を 1 つにまとめている
- 2026-02 に v2 が stable 化し、2026-05-04 時点で `v2.2.4` まで進んでいる ([releases](https://github.com/moonrepo/moon/releases))
- Turborepo のシンプルさと Bazel の厳密さの中間。Node.js を中心に Bun / Deno / Rust / Go / Python (unstable) まで toolchain を同梱できるのが、他のツールには少ない強み
- 旧 SaaS の **moonbase は discontinued**。remote cache は現在 [Bazel Remote Execution API v2](https://github.com/bazelbuild/remote-apis) 互換のセルフホスト（bazel-remote, Depot Cache 等）に向ける構成が公式推奨

## monorepo orchestration ツールに求められるもの

monorepo を運用すると、ビルド・テスト・lint・型チェックを「変更があったパッケージだけ」「依存順に」「並列で」「キャッシュを効かせて」走らせたくなる。これを担うのが orchestration ツールで、主に 3 つの機能を持つ。

1. **task runner** — 各パッケージの `build` / `test` などを統一されたインターフェースで実行する
2. **dependency graph** — パッケージ間の依存とタスク間の依存を解析し、トポロジカルに並列実行する
3. **caching** — input hash が同じなら output を再利用する（local + remote）

pnpm workspaces や Yarn workspaces は package linking とワークスペース解決を担当するだけで、上記の orchestration は守備範囲外である。`pnpm -r run build` のような最小機能はあるが、task graph や remote cache は持たない（[pnpm workspaces docs](https://pnpm.io/workspaces)）。

## moon の位置づけ

moon は GitHub org `moonrepo` が開発する Rust 製ツールで、ライセンスは MIT（[`moonrepo/moon` の LICENSE](https://github.com/moonrepo/moon/blob/master/LICENSE)）。公式 README では次のように説明されている。

> A build system and monorepo management tool for the web ecosystem, written in Rust.

([moonrepo/moon README](https://github.com/moonrepo/moon))

公式の [Comparison ページ](https://moonrepo.dev/docs/comparison) には、Turborepo / Nx / Lerna といった既存ツールとの差分が並んでいる（Bazel との比較は別途）。要点を絞ると次のとおり。

| 観点 | moon の立ち位置 |
|---|---|
| 実装言語 | Rust |
| 主な対象 | Web ecosystem 中心、ただし polyglot 寄り (Node / Bun / Deno / Rust / Go / Python は unstable) |
| 強み | toolchain (proto) との統合 / task inheritance / 厳密な project graph |
| 弱み | Bazel のような hermetic build までは行かない / GUI 系の dashboard は別解（cloud 製品は discontinued） |

「Rust 製で速い」は Turborepo も Nx も Rust hot path を採用済みなので、もはや差別化ポイントではない。moon の差別化はむしろ **toolchain 自動化と task inheritance** にある。

## アーキテクチャ：Action Pipeline

`moon run <target>` を叩いたあと、moon は内部で次の流れを取る。

![moon の Action Pipeline が project graph と dependency graph をもとに並列実行し、入出力ハッシュで local cache / remote cache を引く流れを示す図](/blogs/images/2026-05-13-moon-action-pipeline.png)

1. **project graph** を解決する：`.moon/workspace.yml` の `projects` 設定からプロジェクト集合を発見し、`moon.yml` の `dependsOn` から依存関係を構築する
2. **dependency graph (action graph)** を構築する：要求されたタスクと、その前提となる依存タスクをトポロジカル順に並べる
3. **thread pool** で並列実行する：依存のないアクションは並列に走る
4. 各タスクの **input/output を hashing** し、cache key を生成する
5. local cache (`.moon/cache/`) を引き、ヒットしなければ **remote cache**（後述）に問い合わせる
6. 両方ミスしたらタスクを実行し、output を local / remote cache に保存する

`moon action-graph` や `moon project-graph` で実際の DAG を可視化できる（[CLI reference](https://moonrepo.dev/docs/commands/overview)）。

## インストールと最小構成

### インストール

公式が用意している方法は 2 つある。

```bash
# 1) シェルスクリプト経由（公式推奨形式）
bash <(curl -fsSL https://moonrepo.dev/install/moon.sh)

# 2) proto 経由（推奨）— moonrepo 製の multi-language version manager
proto install moon
```

`proto` は moonrepo が並行して開発している tool manager で、`.prototools` で moon 自身のバージョンも pin できる（[`moonrepo/proto`](https://github.com/moonrepo/proto)）。CI でローカルと同じバージョンを再現したいなら proto 経由が無難。

### 最小構成ファイル

moon の設定は 3 つのファイルに分かれる。

```yaml
# .moon/workspace.yml — workspace 全体
$schema: 'https://moonrepo.dev/schemas/workspace.json'

projects:
  - 'apps/*'
  - 'packages/*'

vcs:
  manager: 'git'
  defaultBranch: 'main'
```

```yaml
# .moon/toolchains.yml — 言語ランタイム / ツールチェイン（v2 で singular toolchain.yml から rename）
$schema: 'https://moonrepo.dev/schemas/toolchain.json'

node:
  version: '22.14.0'
  packageManager: 'pnpm'
  pnpm:
    version: '10.0.0'
```

```yaml
# apps/web/moon.yml — project 単位
$schema: 'https://moonrepo.dev/schemas/project.json'

type: 'application'
language: 'typescript'

dependsOn:
  - 'ui'

tasks:
  build:
    command: 'next build'
    inputs:
      - 'src/**/*'
      - 'next.config.*'
    outputs:
      - '.next'
```

`moon init` で雛形を生成できる。スキーマファイルが `$schema` で公開されているので、エディタ補完が効く。

## 代表的なコマンド

```bash
# 単一の target を実行（<project>:<task> 形式）
moon run web:build

# 影響を受けたタスクだけ走らせる（CI 向け）
moon ci

# 対象プロジェクトの build / test を一括実行する
moon check --all

# project graph と action graph を表示（デフォルトはブラウザ visualizer、--dot / --json も指定可）
moon project-graph
moon action-graph web:build

# project をクエリで絞り込む
moon query projects --language typescript
```

`moon ci` は影響範囲を自動で検出し、必要なタスクだけを走らせるショートカットになっている。GitHub Actions などで `moon ci` を 1 行入れておけば良い。

## task inheritance：moon の "隠れた" 強み

moon の特徴で見過ごされがちなのが **task inheritance**。v2 では `.moon/tasks/**/*.yml` 配下のファイルにグローバル task を定義し、各 `moon.yml` で部分的に上書きできる。v1 の単一 `.moon/tasks.yml` は廃止され、現在はファイル内の `inheritedBy` でマッチ条件を宣言する。

```yaml
# .moon/tasks/node.yml — Node 系プロジェクトへ継承される共通 tasks
$schema: 'https://moonrepo.dev/schemas/tasks.json'

inheritedBy:
  toolchains: ['node']

tasks:
  lint:
    command: 'eslint .'
  test:
    command: 'vitest run'
    inputs:
      - 'src/**/*'
      - 'tests/**/*'
```

```yaml
# packages/utils/moon.yml — 個別 project で test だけ上書き
tasks:
  test:
    args:
      - '--coverage'
```

Turborepo の `turbo.json` も `pipeline` で task を共通化できるが、moon は **project tag / language / type** ごとに継承元を分けられるのが強い。たとえば「TypeScript プロジェクトだけ `tsc --noEmit` を継承する」ような書き方ができる（[Task inheritance docs](https://moonrepo.dev/docs/concepts/task-inheritance)）。

## caching と remote cache（最重要・歴史に注意）

### local cache

moon は各タスクの `inputs` / `outputs` / 環境変数 / `command` 等から SHA256 ベースの hash を生成し、`.moon/cache/` 配下に出力を保存する。次回同じ hash になれば実行せず、保存済み output を復元する。

### remote cache — moonbase は discontinued

ここが古い記事のままだと事実誤認になるポイント。moonrepo はかつて **moonbase** という SaaS（remote cache + insights）を提供していたが、これは **discontinued** になっている。公式ブログでサンセットが告知されている（[moonbase has been sunset](https://moonrepo.dev/blog/moonbase-sunset)）。

現在の公式推奨は **[Bazel Remote Execution API v2](https://github.com/bazelbuild/remote-apis) 互換のサーバー** に向けることだ。具体的には以下のような選択肢がある（[公式 remote cache guide](https://moonrepo.dev/docs/guides/remote-cache)）。

- セルフホスト：[bazel-remote](https://github.com/buchgr/bazel-remote)（S3 / GCS / disk 等の backend に対応）
- マネージド：[Depot Cache](https://depot.dev/products/cache)（Depot が提供する REAPI 互換 cache）

`.moon/workspace.yml` から見ると次のような設定になる（v1.30.0 で `remote` フィールドが stable 化している。詳細は[公式 remote cache guide](https://moonrepo.dev/docs/guides/remote-cache) と [workspace スキーマ](https://moonrepo.dev/schemas/workspace.json) を参照）。

```yaml
# 公式 guide のサンプルに準拠。auth.token は環境変数の "名前" のみ書く（$ プレフィックスは不要）
remote:
  host: 'grpcs://cache.internal:9092'
  auth:
    token: 'MOON_REMOTE_TOKEN'
```

古い `moonbase:` セクションを使った設定例を載せている記事が多いが、これは v1 初期の遺物で **moon v2 以降では動かない**。

## proto との関係

moon の `.moon/toolchain.yml` で Node や Bun のバージョンを指定すると、初回実行時に moon が自動でランタイムをインストールしてくれる。この裏側で動いているのが [proto](https://github.com/moonrepo/proto) で、moonrepo がもう 1 つメンテしている multi-language version manager だ。

- ローカル開発者は `proto` 1 つ入れれば moon 本体も Node も Bun も Deno も同じ仕組みで pin できる
- CI でも `proto install` を 1 行入れれば同じバージョン群が揃う
- moon のキャッシュ key に toolchain version が含まれるので、誰の手元でも同じ output になりやすい

「Nx + Volta + .nvmrc + .tool-versions」のような寄せ集めを 1 個に統合した、と捉えると分かりやすい。

## 軽い比較（Nx / Turborepo / Bazel / Lerna / pnpm workspaces）

| ツール | 立ち位置 | polyglot | remote cache |
|---|---|---|---|
| moon | Web ecosystem + 一部 polyglot、toolchain 同梱 | 中程度（Node / Bun / Deno / Rust / Go / Python は unstable） | Bazel REAPI 互換セルフホスト |
| Turborepo (Vercel) | JS/TS の `package.json` convention 中心のシンプル task runner | 間接的（[公式 multi-language guide](https://turborepo.com/docs/guides/multi-language) で Rust/Go/Python を `package.json` wrapper 経由で扱える） | Remote Cache (公式 / Vercel と統合) |
| Nx | enterprise 向け / plugin 文化 / generator | プラグイン経由で polyglot 拡張可 | Nx Cloud（SaaS） |
| Bazel | 真の polyglot、hermetic build、巨大組織向け | 強い (Java / C++ / Go / Python / iOS / Android …) | REAPI ネイティブ |
| Lerna | 現在は Nx team がメンテ。task runner として再定義 | JS/TS 中心 | Nx Cloud と統合 |
| pnpm workspaces | package linking のみ。orchestration は範囲外 | — | — |

Lerna が「死んだ」と書かれた古い記事もあるが、2022 年に Nx team へ移管されたあとも active で、2026 年現在も `9.x` 系がリリースされている（[`lerna/lerna`](https://github.com/lerna/lerna)）。

## どこに向くか / 向かないか

向いている:

- Node / TypeScript 中心で、一部に Rust / Go / Python が混ざる monorepo
- 開発者ごとに `node -v` が違って嫌になっているチーム（toolchain 統合の恩恵が大きい）
- Turborepo の単純さに不満が出はじめた中規模 monorepo

向いていない:

- 完全に JS/TS だけで完結する小規模 monorepo（Turborepo で十分）
- 1000 人以上の polyglot 巨大 monorepo で hermetic build が必須なケース（Bazel）
- task runner より package linking と version 解決のほうが課題のケース（pnpm workspaces + Changesets）

monorepo は「どのツールを選ぶか」より「どこまでの厳密さを買うか」のグラデーションが本質で、moon はそのうち **中規模 polyglot レイヤーの空白地帯** に綺麗に収まる選択肢になっている。

## 関連 Wiki

- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) — 単一デプロイ単位の中でモジュール境界を保つアプローチ。monorepo + orchestration とは別軸の「コードの分け方」を整理している
