---
title: "Repository Pattern（リポジトリパターン）"
description: "aggregate root への global access を抽象化する DDD パターン。Evans/Microsoft Learn 共に『必須ではない』と明言、過剰適用で薄いラッパに化けやすい"
date: 2026-05-20
lastmod: 2026-05-20
aliases: ["repository pattern", "リポジトリパターン", "repository design pattern"]
related_posts:
  - "/blogs/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/"
tags: ["アーキテクチャ", "repository-pattern", "ddd", "design-pattern"]
---

## 概要

Repository Pattern は、永続化技術 (ORM、SQL、外部 API) への依存を domain / application から切り離し、データ集約への global access を抽象化する設計パターン。最初に Martin Fowler が 2002 年の *Patterns of Enterprise Application Architecture* で [Repository](https://martinfowler.com/eaaCatalog/repository.html) として提示し、その翌年に Eric Evans が *Domain-Driven Design* (2003) で aggregate root への global access という DDD 固有の文脈に統合した。

## Evans の原典

> For each type of aggregate that needs global access, create a service that can provide the illusion of an in-memory collection of all objects of that aggregate's root type [...] Provide repositories only for aggregate roots that actually need direct access.
>
> — Eric Evans, [DDD Reference (2015)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)

重要な制約: **direct access が本当に必要な aggregate root にだけ用意せよ**。すべてのテーブルに repository を生やす設計とは原典的にはずれている。

## 「必須ではない」が公式見解

Microsoft Learn の DDD/CQRS 実装ガイドには「**Repositories shouldn't be mandatory**」という節があり、本文で次のように記されている:

> Custom repositories are useful for the reasons cited earlier, and that is the approach for the ordering microservice in eShopOnContainers. However, it isn't an essential pattern to implement in a DDD design or even in general .NET development.
>
> — [Designing the infrastructure persistence layer](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design)

つまり Repository は**原理上は有用だが、教義として必須ではない**。

## 推奨パターン

- aggregate root ごとに小さな repository interface を定義
- read 側の複雑検索は query service / read model に逃がす（CQRS の発想）
- repository は domain language で命名（`OrderRepository`、`InvoiceRepository`）

## 反例（典型的アンチパターン）

- 全テーブル共通の `IRepository<T>` に CRUD を全部生やす
- repository が ORM のメソッド名を隠すだけの薄いラッパになる
- query まで全部 repository に押し込み、巨大化する
- aggregate boundary を無視して内部 entity 単位の repository を作る

## 使うべき場面 / 使わなくてよい場面

| 状況 | Repository | 理由 |
|---|---|---|
| 永続化技術の差し替えが想定される | 使う | abstraction の本来の利益 |
| 複数データソース | 使う | source の差異を core から隠せる |
| aggregate 単位の不変条件保護が重要 | 使う | trans-aggregate な query を遮断 |
| テスト容易性が重要 | 使う | fake で差し替えやすい |
| ORM context 自体が十分な abstraction を提供 | 使わない | 追加 abstraction の利益が薄い |
| domain が軽く CRUD 中心 | 使わない | 抽象追加が本質的利益を生まない |

## [Hexagonal Architecture](/blogs/wiki/concepts/hexagonal-architecture/) における位置づけ

- Repository **interface** は core (application port) に置く
- Repository **実装** は外側 (outbound adapter) に置く
- domain / application は interface のみに依存する

## 関連 Wiki

- [Hexagonal Architecture](/blogs/wiki/concepts/hexagonal-architecture/)
- [Clean Architecture](/blogs/wiki/concepts/clean-architecture/)
- [CQRS](/blogs/wiki/concepts/cqrs/)

## ソース記事

- [ヘキサゴナルアーキテクチャの実務ガイド](/blogs/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/) — 2026-05-20
