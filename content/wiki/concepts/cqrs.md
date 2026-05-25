---
title: "CQRS（Command Query Responsibility Segregation）"
description: "読み (query) と書き (command) を別モデル・別経路で扱う設計戦術。Greg Young が提唱、Fowler が紹介。多くの情報システムには過剰になりうると Fowler 自身が警告"
date: 2026-05-20
lastmod: 2026-05-20
aliases: ["cqrs", "command query responsibility segregation", "command-query responsibility segregation"]
related_posts:
  - "/blogs/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/"
  - "/blogs/posts/2026/05/2026-05-11-transaction-strategies-saga-outbox-catalog/"
tags: ["アーキテクチャ", "cqrs", "ddd", "design-pattern"]
---

## 概要

CQRS は、**読み (query) と書き (command) を別モデル・別経路で扱う**設計戦術。Bertrand Meyer の Command-Query Separation (CQS) を、システム規模に拡張したのが Greg Young の CQRS。Martin Fowler が [CQRS (bliki)](https://martinfowler.com/bliki/CQRS.html) で紹介し、Eric Evans の DDD Reference (2015) でも CQRS / Event Sourcing は DDD システムの mainstream options と位置づけられている。

## Fowler の警告（重要）

> Despite these benefits, you should be very cautious about using CQRS. Many information systems fit well with the notion of an information base that is updated in the same way that it's read [...] adding CQRS to such a system can add significant complexity.
>
> — Martin Fowler, [CQRS (2011)](https://martinfowler.com/bliki/CQRS.html)

つまり「すべての DDD / Hexagonal に CQRS が必要」というのは誤解。多くの情報システムは read と write を同じモデルで扱うのが自然で、安易に分離すると有意な複雑性増を招く。

## 適用が効く場面

- 読みと書きで負荷特性が極端に違う（読み 1000:1 書き比率など）
- 読みの集計・検索が複雑で、write モデルとは別最適化したい
- write 側で aggregate 単位の不変条件、read 側で多テーブル join、という責務差が明確
- Event Sourcing と組み合わせて、過去の状態を任意時点で再構成したい

## 適用が過剰になりやすい場面

- 単純 CRUD アプリ
- read と write がほぼ同じ shape のデータを扱う
- read の集計が ORM の query 機能で十分まかなえる
- チームが CQRS の運用コスト（複数モデル維持、最終整合性の取り扱い）を払える状態にない

## [Repository Pattern](/blogs/wiki/concepts/repository-pattern/) との接続

CQRS の典型的な実装は次のとおり:

- **Write-side**: Repository 経由で aggregate root を操作（[Hexagonal Architecture](/blogs/wiki/concepts/hexagonal-architecture/) の outbound port）
- **Read-side**: Repository を経由せず、SQL / 専用 query service / read model から直接読む

Repository を「すべての DB アクセスに使う」のではなく、write-side に限定する判断軸として CQRS は有効。

## Event Sourcing との関係

CQRS と Event Sourcing は別概念だが組み合わせて使われることが多い:

- **CQRS**: read / write の経路分離
- **Event Sourcing**: 状態を event の連続として永続化、現在状態は event の畳み込みで再構成

両者を組み合わせると、event ストリームを write-side、それを投影した read model を read-side、という構成になる。

## 関連 Wiki

- [Hexagonal Architecture](/blogs/wiki/concepts/hexagonal-architecture/)
- [Repository Pattern](/blogs/wiki/concepts/repository-pattern/)
- [Clean Architecture](/blogs/wiki/concepts/clean-architecture/)

## ソース記事

- [ヘキサゴナルアーキテクチャの実務ガイド](/blogs/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/) — 2026-05-20
- [ACID から Saga まで — トランザクション戦略 10 種の地図と判断軸](/blogs/posts/2026/05/2026-05-11-transaction-strategies-saga-outbox-catalog/) — 2026-05-11
