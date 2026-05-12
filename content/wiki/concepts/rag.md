---
title: "RAG (Retrieval-Augmented Generation)"
description: "外部データベースから情報検索し、それを基に LLM が応答を生成する技術"
date: 2026-04-06
lastmod: 2026-05-12
aliases: ["RAG", "検索拡張生成"]
related_posts:
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
tags: ["RAG", "LLM", "ベクトル検索", "ナレッジマネジメント", "アダプティブ検索"]
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

## 関連ページ

- [LLM Wiki パターン](/blogs/wiki/concepts/llm-wiki-pattern/) — RAG の限界を超える知識積み上げ型アプローチ
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — RAG を内部で利用するシステム
- [MemPalace](/blogs/wiki/tools/mempalace/) — ベクトル検索による永続メモリシステム
- [Onyx](/blogs/wiki/tools/onyx/) — 企業内検索とエージェントを統合する OSS RAG プラットフォーム
- [Supabase](/blogs/wiki/tools/supabase/) — pgvector による RAG 用ベクトルストア基盤
- [Open-notebook](/blogs/wiki/tools/open-notebook/) — NotebookLM 代替、ローカル LLM でドキュメントを Q&A できる OSS

## ソース記事

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
