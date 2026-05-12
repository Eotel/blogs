---
title: "Modular Monolith（モジュラーモノリス）"
description: "1 つのデプロイ単位を保ちつつ内部に明示的なモジュール境界を持つアーキテクチャ。Shopify、Amazon Prime Video、Segment などが採用・回帰した中間解"
date: 2026-05-11
lastmod: 2026-05-12
aliases: ["modular monolith", "モジュラーモノリス", "modulith", "majestic monolith"]
related_posts:
  - "/posts/2026/05/2026-05-11-modular-monolith-large-services/"
  - "/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/"
tags: ["アーキテクチャ", "modular-monolith", "microservices", "monolith"]
---

## 概要

Modular monolith は、**システム境界とデプロイ境界を一致させない**アーキテクチャ。外形的には monolith と同じ「1 プロセス・1 デプロイ単位」だが、内部にはビジネスドメインごとの明示的なモジュール境界を持ち、各モジュールは公開された内部 API のみで通信する。マイクロサービスの分散コストを払わずに、論理的な責務分離だけを得ることを狙う。2020 年代に Shopify、Amazon Prime Video、Segment などが採用または回帰した結果、**「マイクロサービスかモノリスか」の二項対立を埋める中間解**として再評価が進んでいる。

## 3 つのアーキテクチャの違い

| 観点 | Monolith | Modular Monolith | Microservice |
|------|----------|------------------|--------------|
| デプロイ単位 | 1 | 1 | N |
| プロセス数 | 1 | 1 | N |
| DB | 共有 1 つ | 共有 1 つ（スキーマ分離が一般的） | サービスごと |
| モジュール間通信 | 直接呼び出し | 内部 API | ネットワーク |
| 障害ドメイン | 1 つ | 1 つ | サービス境界で分離 |
| 言語選択 | 単一 | 単一 | サービスごと |
| トランザクション | ローカル ACID | ローカル ACID | 分散・Saga |
| 観測性 | ローカルログ | ローカルログ + モジュールタグ | 分散トレーシング必須 |
| 組織への要求 | 小〜中 | 小〜中 | 多数チームに耐える運用力 |

## 利点

- **デプロイの単純さ**: 1 つの artifact、1 つの DB マイグレーション順序。サービス間のロールバック順序を考えなくてよい。
- **トランザクションの一貫性**: モジュール間操作もローカル DB トランザクションで完結。Saga や outbox 不要。
- **レイテンシ**: モジュール間呼び出しがメモリ内のメソッド呼び出し。ネットワーク往復・直列化コストがゼロ。
- **観測性**: 1 プロセスのスタックトレース 1 本で原因に到達できる。
- **オンボーディング**: 1 リポジトリ clone で全体像が見える。

## 欠点

- **垂直スケールの限界**: 1 プロセスが扱える QPS / メモリ / CPU に物理的天井がある。
- **言語・ランタイム固定**: モジュールごとに別言語、という選択肢が事実上消える。
- **障害ドメインの集中**: 1 モジュールのバグやリーク（メモリ・コネクションプール枯渇）が全体に波及する。
- **モジュール境界の腐敗**: 「気をつける」だけでは時間とともに崩れる。**境界強制ツール** を CI に組み込まないと巨大な泥団子に戻る。

## 主な採用・回帰事例

### Shopify（意図的に採用）

世界最大級の Rails アプリの 1 つ（2.8M LoC）を、**Billing / Orders / Shipping** などビジネスドメイン単位の component に分割し続けている。境界強制は OSS の [Packwerk](/blogs/wiki/tools/packwerk/) によって CI で行う。「壊して分散させる」のではなく **モノリスの内側に境界線を入れる** 路線。

### GitHub（意図的に採用）

`github/github` Rails モノリスを 10 年以上運用。Rails Engine やパッケージで内部分割しつつ、Pages / Actions など周辺機能だけ別サービス化する **Citadel 型**（DHH の命名）に近い。

### Basecamp / 37signals（"Majestic Monolith"）

DHH が 2016 年に "The Majestic Monolith" を提唱して以降、Basecamp 3 → 4、HEY と majestic monolith を守り続けている。約 12 名で 6 プラットフォームを支える現実解として擁護。

### Amazon Prime Video（マイクロサービスから回帰、2023）

Video Quality Analysis チームが Step Functions + Lambda + S3 で組んでいた分散構成を **単一の ECS タスク** に統合し、フレーム受け渡しをインメモリ化することで **コスト 90% 削減**。ただし Prime Video 本体（カタログ・CDN・再生）は依然として分散構成であり、回帰したのは「監視ワークロード 1 つ」だけ。

### Segment（マイクロサービスから回帰、2018）

destination ごとに 100 以上のマイクロサービスを抱えた構成が、依存パッケージ管理・オンコール・リリースの **運用総量** で破綻。全 destination コードを単一リポジトリ・単一バージョン・単一サービスに統合し、運用負荷を激減させた。

## 判断軸

1. **組織規模（Conway's Law）**: チームが 1〜2 つなら modular monolith でほぼ間違いない。10 を超えてから microservice を本気で検討する。
2. **スケールの形**: 全体均一スケールか、特定機能だけ突出か。後者なら **その機能だけ切り出す** Citadel モデルが第一候補。
3. **障害ドメイン要件**: 「決済が落ちても閲覧は続けたい」レベルの SLO 差があるか。なければ無理に分けない。
4. **境界強制機構を CI に入れる**: [Packwerk](/blogs/wiki/tools/packwerk/)（Ruby）/ [Tach](/blogs/wiki/tools/tach/) や [Import Linter](/blogs/wiki/tools/import-linter/)（Python）/ [dependency-cruiser](/blogs/wiki/tools/dependency-cruiser/)（TypeScript）/ [NsDepCop](/blogs/wiki/tools/nsdepcop/) や [ArchUnitNET](/blogs/wiki/tools/archunitnet/)（.NET）/ ArchUnit（Java）/ Go の internal package / Java の `module-info` など、**言語に合った境界強制**を最初から組み込む。
5. **逆方向も許容する**: 切り出したサービスをモノリスに戻す勇気。Segment と Prime Video が示した「戻す」も等しく正しい判断。

## 関連ページ

- [Packwerk](/blogs/wiki/tools/packwerk/) — Shopify が公開した Ruby/Rails 向け境界強制ツール
- [Tach](/blogs/wiki/tools/tach/) / [Import Linter](/blogs/wiki/tools/import-linter/) — Python 側の Packwerk 相当
- [dependency-cruiser](/blogs/wiki/tools/dependency-cruiser/) — TypeScript 側の Packwerk 相当
- [NsDepCop](/blogs/wiki/tools/nsdepcop/) / [ArchUnitNET](/blogs/wiki/tools/archunitnet/) — .NET 側の Packwerk 相当
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) — システム境界を強制する設計思想として通底する考え方

## ソース記事

- [Modular Monolith に回帰する大手サービス — Shopify・Amazon Prime Video・Segment の事例](/blogs/posts/2026/05/2026-05-11-modular-monolith-large-services/) — 2026-05-11
- [他言語に Packwerk はあるか — Python・TypeScript・.NET のモジュラーモノリス境界強制ツール 2026 年版](/blogs/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/) — 2026-05-12
