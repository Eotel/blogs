---
title: "Hexagonal Architecture（ヘキサゴナルアーキテクチャ / Ports and Adapters）"
description: "Alistair Cockburn が考案し 2005 年の原典で整理した設計様式。Ports and Adapters は同じパターンの説明的な別名。UI なし・DB なしでもアプリを動かせるよう inside / outside を非対称に分離する原理"
date: 2026-05-20
lastmod: 2026-05-20
aliases: ["hexagonal architecture", "ヘキサゴナルアーキテクチャ", "ports and adapters", "ports-and-adapters", "ポーツアンドアダプタ"]
related_posts:
  - "/blogs/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/"
tags: ["アーキテクチャ", "hexagonal-architecture", "ports-and-adapters", "design-pattern"]
---

## 概要

Hexagonal Architecture は、Alistair Cockburn が考案し 2005 年の原典 ([Hexagonal architecture](https://alistair.cockburn.us/hexagonal-architecture)) で整理した設計様式。同じパターンの説明的な別名として **Ports and Adapters** が用いられる。「UI なし・DB なしでもアプリケーションを動かせるようにする」ことが原典の意図であり、自動回帰テスト、ヘッドレス実行、外部プログラム連携を容易にすることが動機。重要なのは「左と右」ではなく「内側と外側」の非対称であり、六角形は "6 が重要だから" ではなく、複数のポートを描きやすくするための視覚的比喩。

Cockburn 原典:

> Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases.
>
> — Alistair Cockburn, [Hexagonal architecture (2005)](https://alistair.cockburn.us/hexagonal-architecture)

## 原典の定義

- **Port** — "purposeful conversation" を識別する API。外部装置が差し替わっても会話の目的は変わらない。Cockburn 原典: *"A port identifies a purposeful conversation."*
- **Adapter** — 外部デバイスや技術の信号を port の API に変換するもの。GUI、HTTP、SQL、フラットファイル、mock DB など
- **Primary actor / primary port** — アプリケーションを駆動する側 (= 現代の inbound / driving)
- **Secondary actor / secondary port** — アプリケーションが駆動する側 (= 現代の outbound / driven)
- Port の数は固定ではなく、Cockburn は 2〜4 個程度を好むと述べる

## 近縁概念との関係

| 観点 | Hexagonal | Onion | Clean Architecture | Layered |
|---|---|---|---|---|
| 提唱者 | Cockburn (2005) | Palermo (2008) | Martin (2012) | Fowler / Evans 系 |
| 中心 | application core | domain model | entities / use cases | domain layer |
| 依存方向 | 具体技術から core へ | すべて中心へ | source dependencies inward | 通常は下位層依存 |
| 表現の重点 | inside / outside 非対称 | 同心円 | 統合説明枠 | 階層 |

**Hexagonal / Onion / Clean は「同じ家族、表現の重点が違う」**と見るのが実務的整理。DDD はその家族の "中心に何を置くか" を与え、CQRS は read/write 分離の追加戦術。

## 現代実装の対応

| 原典用語 | 現代実装 | 代表例 |
|---|---|---|
| primary port | inbound / driving port | REST、GraphQL、CLI、batch、MQ consumer |
| secondary port | outbound / driven port | DB、cache、search、mailer、payment API、MQ publisher |
| use case | application service | 注文確定、返金実行などの操作境界 |

## よくある誤解

- 「六角形のフォルダ構成」を意味する → 誤り。形ではなく依存方向と境界が本質
- Controller / Service / Repository の三層と同じ → 誤り。原典の中心は port = "目的ある会話" の識別
- すべてのアプリに必須 → 誤り。Palermo 自身が Onion は小さな Web サイト向きではないと述べている。短命 CRUD では過剰設計になりやすい
- DB は必ず repository 経由 → 誤り。Microsoft Learn は "Repositories shouldn't be mandatory" と明記
- resolver や controller が use case と同義 → 誤り。それらは inbound adapter であり、use case の起動口に過ぎない

## 適用が効くシステム

3 つ以上当てはまるなら強く検討する価値がある:

- 同じ業務機能を REST / GraphQL / CLI / batch / MQ など複数入口から呼ぶ
- DB、外部 API、課金、認証、通知など副作用源が多い
- ドメインルールが複雑で、UI / ORM 変更と独立に保ちたい
- 長寿命システムで、フレームワーク置換や再配線の可能性が高い
- チームが増え、文脈単位のモジュール境界が必要

逆に、単純 CRUD 中心 / ドメインルールが薄い / システム寿命が短い / フレームワーク慣習から外れるコストが利益を上回る場合は軽量版で十分。

## 適用先として最有力

現代の最有力な適用先は [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) の内部。bounded context ごとに hexagonal にしておけば、複数チャネル対応・外部依存・将来のサービス分割に耐えやすい。

境界の維持には静的解析ツールが有効: [Packwerk](/blogs/wiki/tools/packwerk/) / [import-linter](/blogs/wiki/tools/import-linter/) / [dependency-cruiser](/blogs/wiki/tools/dependency-cruiser/) / [ArchUnitNET](/blogs/wiki/tools/archunitnet/)。

## 関連 Wiki

- [Onion Architecture](/blogs/wiki/concepts/onion-architecture/)
- [Clean Architecture](/blogs/wiki/concepts/clean-architecture/)
- [Repository Pattern](/blogs/wiki/concepts/repository-pattern/)
- [CQRS](/blogs/wiki/concepts/cqrs/)
- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/)

## ソース記事

- [ヘキサゴナルアーキテクチャの実務ガイド](/blogs/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/) — 2026-05-20
