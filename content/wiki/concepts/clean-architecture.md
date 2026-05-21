---
title: "Clean Architecture（クリーンアーキテクチャ）"
description: "Robert C. Martin が 2012 年に Hexagonal・Onion・Screaming などを統合説明した設計枠。Dependency Rule（source code dependencies can only point inwards）を中核に据える"
date: 2026-05-20
lastmod: 2026-05-20
aliases: ["clean architecture", "クリーンアーキテクチャ", "uncle bob clean architecture"]
related_posts:
  - "/blogs/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/"
  - "/blogs/posts/2026/03/2026-03-03-0617418777ad8f46ddf3f1d9bfbfb06f/"
tags: ["アーキテクチャ", "clean-architecture", "design-pattern", "solid"]
---

## 概要

Clean Architecture は、Robert C. Martin (Uncle Bob) が 2012 年のブログ記事 [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) で提示した、Hexagonal・Onion・Screaming・DCI・BCE を「目的が同じ似たアーキテクチャ群」としてまとめた**統合説明枠**。中核原理は **Dependency Rule**。

Martin 原文:

> The overriding rule that makes this architecture work is The Dependency Rule. This rule says that source code dependencies can only point inwards.
>
> — Robert C. Martin, [The Clean Architecture (2012)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## 4 層モデル

中心から外側へ:

1. **Entities** — 業務ルールの中心。page navigation や security の変化に影響されにくい high-level rule
2. **Use Cases** — application-specific business rules
3. **Interface Adapters** — controllers、presenters、gateways。data を use case と外部の間で変換
4. **Frameworks and Drivers** — UI、DB、Web、外部 I/O など実装 detail

## 共通の誤解

- 「層の名前 (Entities / UseCases / Adapters / Frameworks) をディレクトリ名にすればよい」→ 誤り。Martin は名前ではなく Dependency Rule の遵守が本質と述べる
- すべてのアプリに必須 → 誤り。過剰な層分割でドメインを貧血化させる anti-pattern も知られる
- [Hexagonal Architecture](/blogs/wiki/concepts/hexagonal-architecture/) を否定した新概念 → 誤り。Hexagonal・Onion・Screaming を**統合した説明枠**であり、それらを置き換える別物ではない

## 過剰適用への批判

「クリーンアーキテクチャ風」フォルダ構造を機械的に作ると、業務コードよりも DTO・mapper・interface のほうが多い anemic な設計になりやすい。Fowler は [Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html) を anti-pattern と呼び、「service 層に行動を抜きすぎると Domain Model の費用だけ払って利益を失う」と批判している。

実際、現場での過剰適用への批判は強く、[クリーンアーキテクチャという「型」の暴力](/blogs/posts/2026/03/2026-03-03-0617418777ad8f46ddf3f1d9bfbfb06f/) のような議論も活発。Martin の意図と現場での「型」化のギャップに注意。

## 関連 Wiki

- [Hexagonal Architecture](/blogs/wiki/concepts/hexagonal-architecture/)
- [Onion Architecture](/blogs/wiki/concepts/onion-architecture/)
- [Repository Pattern](/blogs/wiki/concepts/repository-pattern/)

## ソース記事

- [ヘキサゴナルアーキテクチャの実務ガイド](/blogs/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/) — 2026-05-20
- [クリーンアーキテクチャという「型」の暴力](/blogs/posts/2026/03/2026-03-03-0617418777ad8f46ddf3f1d9bfbfb06f/) — 2026-03-03
