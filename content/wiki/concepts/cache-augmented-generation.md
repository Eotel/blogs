---
title: "Cache-Augmented Generation (CAG)"
description: "権威ある有限コーパスをロングコンテキストに事前ロードし KV キャッシュを再利用する手法。RAG と対比される設計だが、3 つの別物が同じ略称で呼ばれている"
date: 2026-05-20
lastmod: 2026-05-21
aliases: ["CAG", "Cache-Augmented Generation", "Context-Augmented Generation", "Cache-CAG", "Context-CAG"]
related_posts:
  - "/posts/2026/05/rag-cag-llm-knowledge-context-cache-design/"
tags: ["CAG", "RAG", "LLM", "プロンプトキャッシュ", "ロングコンテキスト"]
---

## 概要

Cache-Augmented Generation (CAG) は、Chan et al. (2024) の「[Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks](https://arxiv.org/abs/2412.15605)」で提案された LLM の知識供給手法。**権威あるコーパスをモデルのロングコンテキストに事前ロードして KV キャッシュを再利用し、繰り返し質問にクエリ時の検索なしで答える**手法を指す。論文は適用範囲を「limited and manageable size の知識ソース」に明示的に限定している。

ロングコンテキストモデルの登場以降「RAG はもう不要、これからは CAG だ」という言説が増えたが、これは複数の問題を 1 軸に潰した雑な対立軸である。CAG という略称が指すものは少なくとも 3 つに分かれる。

## CAG という略称が指す 3 つの別物

| 名称 | 何を再利用するか | 出典 / 標準化レベル |
|---|---|---|
| **Cache-Augmented Generation (Cache-CAG)** | 事前ロード済みの長プロンプトの KV キャッシュ | Chan et al. 2024 (arXiv:2412.15605) |
| **Context-Augmented Generation (Context-CAG)** | アプリ側で組み立てたランタイム業務状態 (ユーザー識別 / セッション / ポリシー) | 実務系アーキテクチャ用語として浮上中 |
| **Semantic Cache** | 過去の応答そのもの (埋め込み類似度で再生) | LangChain / Redis などの実装パターン |

設計レビューでの混乱を避けるための命名規約: 検索パターンは **RAG**、有限コーパスの事前ロード + KV キャッシュ再利用は **Cache-CAG**、ランタイム業務状態の管理は **Context-CAG**、応答そのものの再利用は **Semantic Cache** または **Response Cache**。

## Cache-CAG (Chan et al. 2024) の手順

Chan et al. の論文 (Section 2 Methodology) では 3 段階で構成される:

1. **External Knowledge Preloading**: 権威あるコーパスをロングコンテキストに丸ごとロード
2. **Inference**: KV キャッシュを再利用しながら多数の質問に回答
3. **Cache Reset**: セッション切り替え時にキャッシュを安価にリセット

検索コンポーネントが消えるため、リトリーバーの複雑性や検索ミスが原理的に発生しない。代わりに、ロングコンテキスト利用率とコーパス版数管理に新しい依存が生じる。

## RAG / Cache-CAG / Hybrid の使い分け

| 状況 | 推奨アーキテクチャ |
|---|---|
| 小規模・安定したコーパス、頻繁に再利用 | **Cache-CAG** + プロンプト / KV キャッシュ + コーパス版数管理 |
| 大規模・動的コーパス | **[RAG](/blogs/wiki/concepts/rag/)** + リランキング + 引用 / abstention 制御 |
| ACL 制約・テナント境界がある社内ナレッジ | **Hybrid** (namespace 付き RAG + Context-CAG) |
| 中規模で安定性混合 | **Hybrid** (安定バンドルを preload、動的テールを retrieve) |

実戦投入の現実解は、**RAG をバックボーンとし、業務状態を Context Manager に置き、構造が繰り返される箇所にプレフィックス / KV キャッシュを積極適用する** こと。

## ロングコンテキストで RAG は不要か

Cache-CAG が有効な前提条件:

- 権威あるコーパスがモデルの**実効** コンテキスト内に収まる
- 繰り返し同じバンドルに対する質問が来る
- コーパスの更新頻度が低い
- プロンプトキャッシュや KV キャッシュで前半部のコストを償却できる

これらが揃わない場合、ロングコンテキスト利用率の劣化 ([Context Rot](/blogs/wiki/concepts/context-rot/)) が顕在化する。Lost in the Middle、RULER、LongBench、NoLiMa、Databricks の long-context RAG 研究などが繰り返し示すのは、**公称ウィンドウ容量と頑健なコンテキスト利用率は別物**であるという事実だ。

## キャッシュは「インフラ最適化」とは限らない

しばしば混同されるが、キャッシュには性質の異なる 2 種類がある:

- **計算の再利用**: OpenAI prompt caching、Anthropic prompt caching、vLLM Automatic Prefix Caching、TensorRT-LLM KV reuse などは、共通プレフィックスの prefill 計算を内部で省略するだけで、出力されるトークンは変わらない (OpenAI は「the output generated will be identical」と明言)。実装の詳細はベンダーごとに異なり、OpenAI / vLLM / TensorRT-LLM が内部 KV 状態の再利用を明示するのに対し、Anthropic は API レベルのプレフィックスキャッシュとして記述している。
- **回答の再利用**: Semantic Cache (Redis VL の `SemanticCache` 等) や Exact-Match Response Cache (LangChain の `InMemoryCache` / `SQLiteCache` / `RedisCache` 等) は過去の応答そのものを再生する。これは応答の選択に参加しており、freshness window やテナント分離が**性能ではなく正しさの問題**になる。

## 関連ページ

- [RAG (Retrieval-Augmented Generation)](/blogs/wiki/concepts/rag/) — 対比される検索ベースのアプローチ
- [Context Rot](/blogs/wiki/concepts/context-rot/) — Cache-CAG が依存する「実効コンテキスト長」の劣化現象
- [コンテキスト圧縮](/blogs/wiki/concepts/context-compression/) — 圧縮で対応するアプローチ

## ソース記事

- [RAG vs CAG という雑な対立をやめる — 知識・コンテキスト・キャッシュの 3 軸で LLM を設計する](/blogs/posts/2026/05/rag-cag-llm-knowledge-context-cache-design/) — 2026-05-20
