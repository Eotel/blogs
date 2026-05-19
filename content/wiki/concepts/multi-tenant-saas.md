---
title: "マルチテナント SaaS（Multi-Tenant SaaS）"
description: "1 つのアプリケーションスタックで複数テナントを扱う設計パターン。silo / bridge / pool、instance / database / table / row など、ベンダー横断で語られる分離度の連続体として位置づけられる"
date: 2026-05-19
lastmod: 2026-05-19
aliases: ["multi-tenant", "multitenant", "マルチテナント", "マルチテナンシー", "SaaS マルチテナンシー"]
related_posts:
  - "/posts/2026/05/2026-05-19-multi-tenant-saas-architecture-guide/"
tags: ["マルチテナント", "SaaS", "アーキテクチャ", "AWS", "PostgreSQL"]
---

## 概要

マルチテナント SaaS は、**1 つのプロダクトコードベースとインフラを複数の顧客（テナント）で共有させる**設計パターン。実装は単一の選択ではなく、コンピュート・データ・認証・観測性・運用にまたがる **分離度合いのポートフォリオ** として現れる。AWS は silo / bridge / pool、Google Cloud Spanner は instance / database / table / row、Azure は「共有から分離までの連続体」という語彙でこの分離度を表現しており、いずれも本質は「**強い分離は運用負荷とコストを上げる、深い共有は効率を上げるがアプリ側の責任を増やす**」というトレードオフを別の言葉で言い換えている。

## 分離モデルの分類

ベンダー横断でほぼ同型の分類が現れる。

| 一般語彙 | AWS | Google Cloud Spanner | 典型的な実装 |
|---|---|---|---|
| Single-tenant | silo | instance | テナント専用のスタック / DB / アカウント |
| Separate schema | bridge（resource-level の混合） | table / database | 共有インフラ上に論理スキーマで分離 |
| Shared schema | pool | row | `tenant_id` をパーティショニングキーに据えた完全共有 |
| Hybrid | pool + silo の併用 | パターン併用 | フリーティアは pool、エンタープライズは silo |

成熟した SaaS では **hybrid** がデフォルト解になりやすい。商業ティアと規制要件が分かれた瞬間、単一モデルでは収まらなくなる。

## 設計判断の主軸

- **分離度はティアと契約から逆算する** ── 一律で選ばず、テナント segment ごとに business reason を明文化する
- **共有を選んでも分離義務は減らない** ── pool 化はコストを下げる仕組みであり、コンプライアンス義務を免れる仕組みではない（AWS SaaS Tenant Isolation Strategies が明示）
- **identity を先に tenant-aware にする** ── データパス改修より前に JWT に tenant claim を埋め、tenant catalog を 1 つに集約する
- **観測性・コスト・DR は tenancy モデルに従属する** ── stamp-id / shard-id / tenant-id の構造的タグ付けで、運用と請求を一貫させる
- **expand-contract と feature flag を標準にする** ── テナント単位の段階適用が、shared でも dedicated でも安全な唯一の道

## コントロールプレーンとデータプレーンの分離

最も役に立つメンタルモデルは、**コントロールプレーン**（オンボーディング、placement、プロビジョニング、課金、ポリシー管理）と **データプレーン**（リクエストルーティング、DB アクセス、テレメトリ）の分離。Azure はテナントを「デプロイパイプラインの設定として扱う」か「コントロールプレーンが管理するデータとして扱う」かを設計の起点と位置づけている。

## PostgreSQL での実装

shared schema では `tenant_id` を **主アクセス経路**（複合主キーの先頭）に置き、PostgreSQL Row Security Policies で偶発漏洩を機械的に防ぐのが定石。`current_setting('app.tenant_id')` のような custom GUC とポリシーを組み合わせることで、アプリ層のクエリミスを RLS が下層で受け止める二段ガードになる。Supabase はこの構造を BaaS のデフォルトとして採用しており、参照実装として有用（[Supabase](/blogs/wiki/tools/supabase/) を参照）。

## バックアップ・DR の制約

tenancy モデルは「per-tenant point restore」「legal hold」など **commercial commitment と直接結びつく** ため、ここで設計の自由度が一気に下がる。Google Spanner の公式ドキュメントは「table / row パターンでは個別テナントのバックアップを DB はサポートできない、アプリケーションが実装しなければならない」と明言しており、shared schema を選んだ瞬間に backup/restore tooling は app-level の責任に移る。

## 関連ページ

- [Modular Monolith（モジュラーモノリス）](/blogs/wiki/concepts/modular-monolith/) — 「システム境界とデプロイ境界を一致させない」設計は、shared schema 内のモジュール境界にも応用できる
- [Framework-defined Infrastructure](/blogs/wiki/concepts/framework-defined-infrastructure/) — コントロールプレーンをフレームワーク側に押し出す近接概念
- [Supabase](/blogs/wiki/tools/supabase/) — PostgreSQL RLS をマルチテナント分離の主機構として採用する BaaS
- [Terraform IaC](/blogs/wiki/guides/terraform-iac/) — stamp / shard / tenant の placement / tagging を IaC で表現する実装パターン
- [インシデント対応](/blogs/wiki/guides/incident-response/) — tenancy モデル別の DR と blast radius を運用面から補強

## ソース記事

- [マルチテナント SaaS アーキテクチャ設計ガイド ── silo / bridge / pool から hybrid 運用まで](/blogs/posts/2026/05/2026-05-19-multi-tenant-saas-architecture-guide/) — 2026-05-19
