---
title: "Packwerk"
description: "Shopify が公開した Ruby/Rails 向けの modular monolith 境界強制ツール。constant 参照を静的解析して許可されていないモジュール間依存をビルド時に検出する"
date: 2026-05-11
lastmod: 2026-05-11
aliases: ["packwerk", "Shopify Packwerk"]
related_posts:
  - "/posts/2026/05/2026-05-11-modular-monolith-large-services/"
tags: ["ruby", "rails", "modular-monolith", "アーキテクチャ", "shopify", "静的解析"]
---

## 概要

[Packwerk](https://github.com/Shopify/packwerk) は Shopify が 2020 年に OSS 化した、Rails アプリケーション内のモジュール境界を強制するための静的解析ツール。Ruby の **constant 参照を解析**し、package（モジュール）ごとに定義された可視性（`public/` / `private/`）を破る依存があれば CI を赤くする。280 万行規模の Shopify モノリスを **壊さずに** modular monolith として運用するための実務ツールとして生まれた。

## 何を解決するか

Rails の慣習的なディレクトリ構成（`app/controllers/` `app/models/` ...）は **技術レイヤ** での分割であり、ビジネスドメイン（Billing / Orders / Shipping）を跨ぐ依存は静的には可視化されない。Packwerk は:

1. アプリを **package** 単位（≒ ビジネスドメイン）に分割する規約を導入
2. 各 package の `public/` 配下にあるクラスだけが「外向きの公開 API」
3. 他 package の `private/` を参照する constant があれば違反として検出
4. CI に組み込めば、境界違反は PR の段階で必ずブロックされる

これにより [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) の最大の弱点である「境界の腐敗」を継続的に防ぐ。

## 基本構造

```
my_app/
├── packs/
│   ├── billing/
│   │   ├── package.yml         # 公開設定
│   │   ├── app/
│   │   │   ├── public/         # 他 pack から参照 OK
│   │   │   └── private/        # 自 pack 内のみ
│   ├── orders/
│   └── shipping/
└── ...
```

`package.yml` には enforce_privacy / enforce_dependencies などのオプションがあり、段階的に厳格化していけるようになっている（既存モノリスへの後付け導入を想定）。

## Shopify での実績

- 公開時点で **約 48 packages、そのうち 30 件で境界強制を有効化** 済みと公表
- 250 万行超の Rails コードを継続的に運用しつつ、ドメイン境界を CI で維持
- 公開後、Gusto / Square などの大規模 Rails 企業でも採用報告がある

## 類似アプローチ（他言語）

| 言語/環境 | 同等のツール |
|-----------|--------------|
| Java | [ArchUnit](https://www.archunit.org/)、`module-info`（JPMS） |
| Go | `internal/` パッケージ（言語仕様で強制） |
| TypeScript | [eslint-plugin-boundaries](https://github.com/javierbrea/eslint-plugin-boundaries)、Nx の project boundaries |
| .NET | NsDepCop、NetArchTest |

いずれも **境界強制を CI に組み込む** という思想は同じ。

## 関連ページ

- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) — Packwerk が支える上位アーキテクチャパターン

## ソース記事

- [Modular Monolith に回帰する大手サービス — Shopify・Amazon Prime Video・Segment の事例](/blogs/posts/2026/05/2026-05-11-modular-monolith-large-services/) — 2026-05-11
