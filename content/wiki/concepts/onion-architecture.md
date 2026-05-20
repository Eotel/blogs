---
title: "Onion Architecture（オニオンアーキテクチャ）"
description: "Jeffrey Palermo が 2008 年に提唱した、長寿命業務アプリ向けの同心円型アーキテクチャ。すべての依存を中心に向かわせ、infrastructure を最外殻に置く"
date: 2026-05-20
lastmod: 2026-05-20
aliases: ["onion architecture", "オニオンアーキテクチャ"]
related_posts:
  - "/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/"
tags: ["アーキテクチャ", "onion-architecture", "design-pattern"]
---

## 概要

Onion Architecture は、Jeffrey Palermo が 2008 年に提唱した同心円型のアーキテクチャ。長寿命で複雑な業務アプリケーション向けの named pattern として提案され、すべての依存を中心 (domain model) に向かわせ、infrastructure を最外殻に置くことを原則とする。

Palermo 原文:

> Hexagonal architecture and Onion Architecture share the following premise: Externalize infrastructure and write adapter code so that the infrastructure does not become tightly coupled.
>
> — [The Onion Architecture : part 1 (2008)](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/)

## 原則

- **依存方向は内向き** — すべての依存は中心 (domain) へ向かい、その逆はない
- **DB は中心ではなく外部** — 永続化は infrastructure 層の detail
- **infrastructure を外在化** — adapter コードを書き、infrastructure が core と密結合しないようにする
- **長寿命業務アプリ向け** — Palermo 自身が小さな Web サイト向きではないと明言

## [Hexagonal Architecture](/blogs/wiki/concepts/hexagonal-architecture/) との関係

- **共有する前提**: infrastructure を外在化し adapter を書く（Palermo 本人が明言）
- **違い**: Hexagonal は inside / outside の非対称を強調、Onion は同心円で「すべて中心へ」を強調
- 表現の重点が違うだけで、実装上は近似する

## [Clean Architecture](/blogs/wiki/concepts/clean-architecture/) との関係

Martin の Clean Architecture (2012) は Hexagonal、Onion、Screaming、DCI、BCE を「目的が同じ似たアーキテクチャ群」とまとめた。Onion はその家系図の中間世代であり、Palermo の「依存は中心へ」は Martin の Dependency Rule にほぼ吸収されている。

## 適用と非適用

| 規模 | 推奨度 | 理由 |
|---|---|---|
| 小規模・短命な内部ツール | 低 | Palermo 本人が「小さな Web サイト向きではない」と明言 |
| 中規模 SaaS / 業務アプリ | 中〜高 | 長寿命と複数外部依存があれば効く |
| 大規模・長寿命業務システム | 非常に高 | bounded context ごとに onion にする modular monolith 内部運用が最適 |

## 関連 Wiki

- [Hexagonal Architecture](/blogs/wiki/concepts/hexagonal-architecture/)
- [Clean Architecture](/blogs/wiki/concepts/clean-architecture/)
- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/)

## ソース記事

- [ヘキサゴナルアーキテクチャの実務ガイド](/blogs/posts/2026/05/2026-05-20-hexagonal-architecture-practical-guide/) — 2026-05-20
