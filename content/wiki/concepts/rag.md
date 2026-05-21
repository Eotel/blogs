---
title: "RAG (Retrieval-Augmented Generation)"
description: "外部データベースから情報検索し、それを基に LLM が応答を生成する技術"
date: 2026-04-06
lastmod: 2026-05-21
aliases: ["RAG", "検索拡張生成", "意味検索", "semantic search"]
related_posts:
  - "/posts/2026/05/2026-05-21-knowledge-pipeline-over-harness/"
  - "/posts/2026/05/rag-cag-llm-knowledge-context-cache-design/"
  - "/posts/2026/04/karpathy-llm-wiki/"
  - "/posts/2026/03/rag-adaptive-search-strategy/"
  - "/posts/2024/02/2024-02-12-d1d192cc863cb9fbb1417f49a3067e53/"
  - "/posts/2024/04/2024-04-12-7495152700831224546a8c1630d54138/"
  - "/posts/2024/08/2024-08-01-9e4638d4420bcf5b99ba203726921888/"
  - "/posts/2024/03/2024-03-14-05df197941702710ea55013287157a16/"
  - "/posts/2026/02/2026-02-27-066b5a501b99b2a36e1e5e4496d1ead0/"
  - "/posts/2026/03/2026-03-04-911137ea2e4da5af4ed98a6f29e995fb/"
  - "/posts/2026/03/2026-03-05-783efe7ccb15ece292b5d6210664c397/"
  - "/posts/2026/03/2026-03-05-cb9c696dbeb648e3286f2976b9a3eac6/"
  - "/posts/2026/03/2026-03-05-d6238d29f67740e50870a83860a480fc/"
  - "/posts/2026/03/2026-03-10-qwen-finetuning-vs-rag/"
  - "/posts/2026/03/2026-03-11-bytedance-deerflow/"
  - "/posts/2026/03/2026-03-11-gemini-embedding-2/"
  - "/posts/2026/03/2026-03-18-opendataloader-pdf-to-markdown/"
  - "/posts/2026/03/2026-03-05-7eb04a726f76f2ff880bc2b18efa42b2/"
tags: ["RAG", "LLM", "ベクトル検索", "ナレッジマネジメント", "アダプティブ検索", "ハイブリッド検索", "rerank", "GraphRAG"]
---

## 概要

最新のドキュメントやナレッジベースをベクトル DB に保存し、クエリ時に関連文書を検索して LLM に供与する手法。LLM の知識カットオフを補い、ハルシネーション低減に効果的。

## 仕組み

1. ドキュメントをチャンクに分割
2. Embeddings でベクトル化してベクトル DB に格納
3. クエリ時に類似ベクトルを検索
4. 検索結果をコンテキストとして LLM に渡す

## RAG の限界と LLM Wiki

Karpathy は RAG を「毎日同じ本を初めて読む人に質問を投げるようなもの」と評し、知識を積み上げる LLM Wiki パターンを提案した。RAG は都度検索、LLM Wiki は事前コンパイル。

## アダプティブ検索 RAG（新手法）

従来の RAG は検索戦略が固定されているため、クエリに合わない場合は精度が著しく低下する。**モデル自身が検索方法を選択・組み合わせる**アダプティブ RAG は、この問題に対応する新手法。

### 3つの検索戦略

| 検索戦略 | 向いているケース |
|----------|-----------------|
| **キーワード検索** | 固有名詞・型番・コマンドなど特定語句の検索 |
| **意味検索（セマンティック）** | 概念的な質問、言い換えが多い文書 |
| **チャンク全文読み** | 文脈・前後関係が重要な長文 |

モデルの推論能力が高いほど検索戦略の判断精度が向上するため、モデル進化と共に RAG 全体の性能が自然にスケールする構造となっている。読み込むテキスト量は従来と同等以下でも回答精度は向上する。

## 本気の意味検索 — RAG を支える 7 段パイプライン

RAG = 「embedding 類似検索」と単純化すると実運用で必ずハマる。Elastic / Azure AI Search / OpenSearch / Weaviate / Qdrant / Milvus / Vespa など主要製品はいずれも、**多段の知識化と検索パイプライン** に収束している。最小構成は次の 7 段。

1. **解析** — layout-aware parse + OCR（Google Document AI / Azure Document Intelligence / Unstructured / LlamaParse）
2. **正規化** — Markdown / element JSON / header path を保つ
3. **enrichment** — metadata（owner / ACL / 鮮度 / version / citation span）を付与
4. **候補生成** — BM25（lexical） + dense + sparse（SPLADE） + late interaction（[ColBERT](https://arxiv.org/abs/2004.12832)）
5. **融合** — RRF（Reciprocal Rank Fusion）で異種スコアを順位だけで統合
6. **rerank** — cross-encoder で precision を押し上げる
7. **応答生成 + 評価** — citation engine と golden set / Ragas / LangSmith

「単純なベクトル検索」が落とすもの:

- 識別子・版数・パス・法令番号など rare token の厳密一致
- 単一ベクトルへの圧縮損失（late interaction が補う）
- ACL・鮮度・引用・version — これらはメタデータ層で別途運ぶ

embedding 類似検索は **意味検索システムの一部** ではあっても **意味検索システムそのもの** ではない。

詳細は [ハーネスより先にナレッジ作成と『本気の意味検索』を整える](/blogs/posts/2026/05/2026-05-21-knowledge-pipeline-over-harness/) を参照。

## GraphRAG が必要になる条件 — 必要ない条件

Microsoft Research の [GraphRAG](https://arxiv.org/abs/2404.16130) は entity knowledge graph + community summaries で **文書群全体の概観・多段関係** を問う質問に強い（global search / local search / DRIFT search）。逆に、FAQ・条文検索・該当箇所検索のような focused query では GraphRAG は過剰設計になりやすい。LightRAG のような軽量化研究が出ていること自体、graph 系 indexing のコストが課題であることを示している。

実務では graph は corpus 全体の俯瞰や高価値領域に限定し、通常の検索は hybrid + rerank で回すのが現実的。

## RAG と CAG の関係

ロングコンテキストモデルの登場以降、「RAG はもう不要で CAG (Cache-Augmented Generation) で十分」という言説が増えたが、これは複数の問題を 1 軸に潰している。実際には RAG / CAG は対立せず、3 つの直交する設計軸として整理するのが正確:

- **知識**: 学習外の情報をどう取り込むか → RAG が解く
- **コンテキスト**: ユーザー識別・セッション・業務状態をどう運ぶか → Context Manager が解く
- **計算**: 同じプレフィックスをどこまで再利用するか → プロンプト / KV キャッシュが解く

Chan et al. (2024) の CAG (Cache-Augmented Generation) は「権威ある有限コーパスを長コンテキストに事前ロードし、KV キャッシュを再利用する」狭義の手法で、コーパスが大規模・動的・ACL 制約付きのときは RAG が依然として最適解。詳細は [Cache-Augmented Generation](/blogs/wiki/concepts/cache-augmented-generation/) を参照。

## 関連ページ

- [Cache-Augmented Generation (CAG)](/blogs/wiki/concepts/cache-augmented-generation/) — RAG と対比される事前ロード型アプローチ
- [Context Rot (コンテキスト劣化)](/blogs/wiki/concepts/context-rot/) — ロングコンテキスト RAG が抱える失敗モード
- [LLM Wiki パターン](/blogs/wiki/concepts/llm-wiki-pattern/) — RAG の限界を超える知識積み上げ型アプローチ
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — RAG を内部で利用するシステム
- [MemPalace](/blogs/wiki/tools/mempalace/) — ベクトル検索による永続メモリシステム
- [Onyx](/blogs/wiki/tools/onyx/) — 企業内検索とエージェントを統合する OSS RAG プラットフォーム
- [Supabase](/blogs/wiki/tools/supabase/) — pgvector による RAG 用ベクトルストア基盤
- [Open-notebook](/blogs/wiki/tools/open-notebook/) — NotebookLM 代替、ローカル LLM でドキュメントを Q&A できる OSS

## ソース記事

- [ハーネスより先にナレッジ作成と『本気の意味検索』を整える — RAG の前にやることリスト](/blogs/posts/2026/05/2026-05-21-knowledge-pipeline-over-harness/) — 2026-05-21
- [RAG vs CAG という雑な対立をやめる — 知識・コンテキスト・キャッシュの 3 軸で LLM を設計する](/blogs/posts/2026/05/rag-cag-llm-knowledge-context-cache-design/) — 2026-05-20
- [Karpathy の LLM Wiki](/blogs/posts/2026/04/karpathy-llm-wiki/) — 2026-04
- [AIが自分で調べ方を選ぶRAG — モデル推論能力でスケールする新手法](/blogs/posts/2026/03/rag-adaptive-search-strategy/) — 2026-03-17
- [生成AI: RAG](/blogs/posts/2024/02/2024-02-12-d1d192cc863cb9fbb1417f49a3067e53/) — 2024-02-12
- [GetAI: RAG](/blogs/posts/2024/04/2024-04-12-7495152700831224546a8c1630d54138/) — 2024-04-12
- [ColPali](/blogs/posts/2024/08/2024-08-01-9e4638d4420bcf5b99ba203726921888/) — 2024-08-01
- [AWS: Bedrock: KnowlegeBase](/blogs/posts/2024/03/2024-03-14-05df197941702710ea55013287157a16/) — 2024-03-14
- [# コンテキストエンジニアリング — AI を「使う人」と「使いこなす人」の違い](/blogs/posts/2026/02/2026-02-27-066b5a501b99b2a36e1e5e4496d1ead0/) — 2026-02-27
- [AIエージェント「デモ→本番」95%脱落 × 4つの壁とエージェンティックRAG実践](/blogs/posts/2026/03/2026-03-04-911137ea2e4da5af4ed98a6f29e995fb/) — 2026-03-04
- [Agentic AIの周期表 — 66要素で読み解くAIエージェント構築の全体像](/blogs/posts/2026/03/2026-03-05-783efe7ccb15ece292b5d6210664c397/) — 2026-03-05
- [Agentic AI 学習ロードマップ — 「フルスタックインテリジェンス」を9ヶ月で習得する体系的な道筋](/blogs/posts/2026/03/2026-03-05-cb9c696dbeb648e3286f2976b9a3eac6/) — 2026-03-05
- [gen-ai-experiments × 130超の生成AIアプリを「動かして学ぶ」LangChain・RAG・エージェント実践集](/blogs/posts/2026/03/2026-03-05-d6238d29f67740e50870a83860a480fc/) — 2026-03-05
- [ローカルQwenに個人知識を覚えさせたい — ファインチューニング vs RAG](/blogs/posts/2026/03/2026-03-10-qwen-finetuning-vs-rag/) — 2026-03-10
- [ByteDance DeerFlow — オープンソースの SuperAgent 基盤でAIエージェントを自律運用する](/blogs/posts/2026/03/2026-03-11-bytedance-deerflow/) — 2026-03-11
- [Google Gemini Embedding 2：テキスト・画像・動画・音声を統一ベクトル空間に埋め込むマルチモーダル埋め込みモデル](/blogs/posts/2026/03/2026-03-11-gemini-embedding-2/) — 2026-03-11
- [OpenDataLoader PDF — CPUだけで毎秒100ページ、PDFをMarkdownに超高速変換するOSSツール](/blogs/posts/2026/03/2026-03-18-opendataloader-pdf-to-markdown/) — 2026-03-18
- [Agentic AI の仕組み — 4層アーキテクチャで理解する「考えて動く AI」の全体像](/blogs/posts/2026/03/2026-03-05-7eb04a726f76f2ff880bc2b18efa42b2/) — 2026-03-05
