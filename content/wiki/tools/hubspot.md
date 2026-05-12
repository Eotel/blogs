---
title: "HubSpot"
description: "CRM を中核とした Marketing / Sales / Service / Content / Data / Commerce の 6 Hub 構成の SaaS プラットフォーム"
date: 2026-05-09
lastmod: 2026-05-12
aliases: ["HubSpot", "ハブスポット"]
related_posts:
  - "/posts/2026/04/2026-04-23-hubspot-hscachebuster/"
  - "/posts/2026/04/2026-04-28-hubspot-pro-merits/"
  - "/posts/2025/03/2025-03-25-35d3a45a26e53c6245aac6e52d9917f8/"
  - "/posts/2026/03/2026-03-18-geo-marketing/"
  - "/posts/2026/03/2026-03-18-hubspot-line-items-api/"
  - "/posts/2026/03/2026-03-18-restaurant-marketing-hubspot/"
  - "/posts/2026/03/2026-03-18-zapier-hubspot-asana/"
tags: ["HubSpot", "CRM", "マーケティングオートメーション", "SaaS", "BtoB"]
---

## 概要

HubSpot は CRM を中核に置き、Marketing・Sales・Service・Content・Data・Commerce の 6 つの Hub で構成される統合 SaaS プラットフォーム。各 Hub は Starter / Professional / Enterprise の 3 グレードで提供され、Hub 単位で課金・組み合わせができる。

## 6 Hub の役割

| Hub | 主な機能 | Pro 化の主なメリット |
|-----|---------|-------------------|
| **Marketing Hub** | メール配信・フォーム・広告連携・ランディングページ | AEO 対応・ナーチャリングワークフロー・類似オーディエンス広告 |
| **Sales Hub** | ディール管理・シーケンス・会議予約 | Forecasting（予実管理）・シーケンス自動化 |
| **Service Hub** | チケット・チャット・ナレッジベース | 営業時間外チャットボット運用 |
| **Content Hub** | CMS・ブログ・AI コンテンツ生成 | AEO 対応コンテンツ生成・検索ワードレコメンド |
| **Data Hub** | データ統合・ワークフロー | 双方向シンク・外部 API 連携 |
| **Commerce Hub** | 決済・請求・サブスク | 日本ではまだ採用例が少ない |

## Starter → Professional のポイント

### Marketing Hub Pro

- **AEO（Answer Engine Optimization）**: ChatGPT・Google AI Overviews などの「回答エンジン」に自社コンテンツが拾われるかを最適化
- **ナーチャリングワークフロー**: 失注後リードへの再アプローチを自動化（効果が出始めるのは約 1,500 リード以上）
- **類似オーディエンス**: Google / Meta / LinkedIn に HubSpot コンタクトリストを元に Lookalike Audiences を配信

### Sales Hub Pro

- **Forecasting**: ディールステージの加重確率でパイプラインを予実管理
- **Sequences**: 返信があると自動停止する個別営業向けのフォローアップ自動化

### Commerce Hub の日本での制約

HubSpot 独自の決済機能（HubSpot payments）は日本未対応。Stripe 連携は可能だが 0.75% のプラットフォーム手数料が加算される。日本のインボイス制度（適格請求書）への標準対応もないため、日本企業では Marketing / Sales / Service の 3 本柱を先行させ、Commerce Hub は様子見という温度感が多い。

## hsCacheBuster

HubSpot CDN のキャッシュを回避するためのクエリパラメータ。開発・確認時に URL に `?hsCacheBuster=12345` を追加することで、CDN にキャッシュされた古いバージョンではなく最新ファイルを取得できる。`12345` の数値は任意（乱数で問題ない）。

## 関連ページ

- [MCP](/blogs/wiki/concepts/mcp/) — HubSpot の MCP 統合が提供されている
- [AI BPR](/blogs/wiki/concepts/ai-bpr/) — HubSpot の機能を AI で最大活用する業務再設計

## ソース記事

- [HubSpot の hsCacheBuster で CDN キャッシュを回避する](/blogs/posts/2026/04/2026-04-23-hubspot-hscachebuster/) — 2026-04-23
- [HubSpot Professional にアップグレードするメリットを 6 Hub 別に整理](/blogs/posts/2026/04/2026-04-28-hubspot-pro-merits/) — 2026-04-28
- [Hubspot](/blogs/posts/2025/03/2025-03-25-35d3a45a26e53c6245aac6e52d9917f8/) — 2025-03-25
- [ジオマーケティングとは？位置情報を活用した集客手法と FreakOut ASE の特徴](/blogs/posts/2026/03/2026-03-18-geo-marketing/) — 2026-03-18
- [HubSpot Line Items API：取引・見積もりに紐づく商品項目を管理する](/blogs/posts/2026/03/2026-03-18-hubspot-line-items-api/) — 2026-03-18
- [HubSpotを活用したレストランのディナータイム集客戦略](/blogs/posts/2026/03/2026-03-18-restaurant-marketing-hubspot/) — 2026-03-18
- [Zapier を使った HubSpot と Asana の連携：集計ロジックも追加する方法](/blogs/posts/2026/03/2026-03-18-zapier-hubspot-asana/) — 2026-03-18
