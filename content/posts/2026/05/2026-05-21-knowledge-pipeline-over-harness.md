---
title: ハーネスより先にナレッジ作成と『本気の意味検索』を整える — RAG の前にやることリスト
slug: 2026-05-21-knowledge-pipeline-over-harness
date: 2026-05-21
lastmod: 2026-05-21
draft: false
author: eotel
model: claude-opus-4-7
description: ハーネスより先に整えるべきは『知識化 → hybrid retrieval → rerank → 評価』の検索パイプラインだ。Elastic・Azure
  AI Search・Weaviate・GraphRAG 等の一次情報から、RAG の前にやるべき順番を整理する。
categories:
- AI/LLM
tags:
- RAG
- ハイブリッド検索
- 意味検索
- GraphRAG
- rerank
- Harness Engineering
audio_url: https://github.com/Eotel/blogs/releases/download/audio/2026-05-21-knowledge-pipeline-over-harness.m4a
audio_lang: ja
audio_generated_at: '2026-05-21T04:56:10Z'
audio_source: notebooklm
audio_format: debate
---

![AI システムにおける薄い『Harness』レイヤーと、その下に厚く積み上がった Knowledge Pipeline（Parse → Metadata → BM25/Dense → Hybrid → Rerank → Citation を要約した 6 ステージ表現。本文で詳述する 7 段パイプラインを視覚的に圧縮した俯瞰図）を対比したコンセプチュアルなヒーロー画像。下層のパイプラインが上層のハーネスを支えている様子をフラットでミニマルなデザインで表現](/blogs/images/knowledge-pipeline-over-harness-hero.png)

## はじめに — ハーネスを磨いても、検索が腐っていれば agent は腐る

[ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) は確かに 2026 年の AI エンジニアリングで主戦場の一つになった。[Prompt → Context → Harness の系譜](/blogs/posts/2026/03/2026-03-27-prompt-to-harness-engineering/) でも整理されているように、CLAUDE.md・skill・hook・subagent・evaluation harness の設計品質は、agent の挙動と再現性を大きく左右する。

一方で、コード生成や検索を伴う社内タスクで上がってこない精度を、ハーネス側のチューニングだけで解決しようとすると、ある時点から急に効かなくなる。Claude Code や Codex のように[コードベース全体をコンテキストに収められる領域](/blogs/posts/2026/04/2026-04-17-agent-harness-rag-context-size/)（100 ファイル前後まで）なら RAG なしでも動く。だが社内文書・規程・チケット・Slack・複数リポジトリ・PDF・スキャン画像が混ざる領域では、ハーネスの巧拙より「上流の検索が何を返すか」のほうがはるかに支配的になる。

公開情報を広く見直すと、2026 年時点で実運用の検索基盤はほぼ例外なく「単一の検索手法」ではなく **多段の知識化と検索パイプライン** でできている。Elastic はハイブリッド検索と [RRF](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)、クロスエンコーダによる [semantic reranking](https://www.elastic.co/docs/solutions/search/ranking/semantic-reranking) を前提にしている。Azure AI Search は hybrid search と semantic ranker、[document-level access control](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview) を前面に出す。OpenSearch・Weaviate・Qdrant・Milvus・Vespa も dense・sparse・hybrid・rerank・multi-stage を組み合わせる設計を公式に示している。Google も Agent Search on Gemini Enterprise Agent Platform として、権限制御とメタデータフィルタを備えた企業向け検索基盤を整理した。

実務でいう「意味検索」は、ベクトル検索の別名ではなく、**知識化・検索・再順位付け・権限・鮮度・引用までを含むシステム** だ。本稿では、その全体像を一次情報ベースで再構成し、ハーネスより先に整えるべき優先順位を明確にする。

## 結論を先に — 整える順番

> ハーネスより先に整えるべきものは、検索対象を「AI が扱える知識オブジェクト」に変換するパイプラインと、それを使い分ける多段検索パイプラインである。

最小構成は次の 7 段（粒度は「最小実装手順」レベル。後段の「7 段の役割と省略時の症状」表は同じ流れを「パイプライン段階」の粒度で再分類したものなので、対応はゆるく取って読んでほしい）。

1. 構造を保った取り込み（layout-aware parse + OCR）
2. メタデータ付与（owner / ACL / 鮮度 / version / citation span）
3. BM25 か全文検索（lexical baseline）
4. ベクトル検索（dense / sparse / late interaction）
5. メタデータフィルタ
6. 上位候補への rerank（cross-encoder）
7. 引用付き応答 + 評価セットの継続運用

[GraphRAG](https://arxiv.org/abs/2404.16130) はこの最小構成には含まれない。全体俯瞰や多段関係探索が要るときの **拡張** であり、最初から全文書を graph 化するのは過剰設計になりやすい。

## 「grep で十分」論の射程

[ripgrep](https://github.com/BurntSushi/ripgrep/blob/master/README.md) が本当に強いのは、質問者が **正しい語・識別子・正規表現・ファイル境界をすでに知っている** 場面である。ripgrep は再帰的な regex 検索を高速に行い `.gitignore` も尊重する。GitHub Code Search も regex と symbol search を備えるため、コード・設定・ログ・エラーコード・関数名・クラス名・設定キー・パス名の探索では、意味検索より lexical search のほうが速く、説明しやすく、誤りも少ない。

ただし、多くの社内検索は「語を知らない」状況で起きる。

- 略称しか知らない
- 原文と質問文の言い回しが違う
- 日本語と英語が混ざる
- 章立てのどこにあるか分からない

この時点で grep の前提が崩れる。本番利用では「一致した行を出す」だけでは足りず、「最も関連度が高い文書や節を上に出す」必要がある。ここで最低でも [BM25](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) や PostgreSQL の [ts_rank](https://www.postgresql.org/docs/current/textsearch-controls.html) のような **ランキング付き lexical retrieval** が必要になる。PostgreSQL の `ts_rank` は語の頻度と weight A/B/C/D（構造）を考慮し、`ts_rank_cd` はさらに語の近接（coverage density）も加味する。BM25 系も長さ正規化とフィールド重み付けを前提に進化してきた。

## 「単純なベクトル検索」の限界

dense retrieval は言い換え・同義語・自然文の質問に強い一方で、**単語の厳密一致が効く rare token や識別子・数値条件・版数・パス・法令番号** のような「取りこぼしが致命傷になるクエリ」では弱くなりやすい。だから主要製品は dense 単独ではなく、keyword と vector の両方を使う [hybrid](https://www.elastic.co/docs/solutions/search/hybrid-search) を標準化している。

| 製品 | hybrid の実装 |
|---|---|
| Weaviate | [BM25F と vector の融合](https://docs.weaviate.io/weaviate/search/hybrid) |
| Milvus | sparse と dense の組み合わせ |
| Qdrant | dense・sparse・multivector の multi-stage |
| Azure AI Search | full-text と vector の並列実行 + RRF |
| OpenSearch | hybrid query + neural sparse + semantic field |

単純ベクトル検索のもう一つの限界は **単一ベクトルへの圧縮** だ。[ColBERT](https://arxiv.org/abs/2004.12832) は query と document を別々に token-level で表現し、後段で細粒度の相互作用を行う late interaction を導入することで、single-vector dense retrieval より精密な照合を可能にした。[BEIR](https://arxiv.org/abs/2104.08663) ベンチマークでも late interaction と reranking は平均性能で強く、ColBERTv2 はその品質と効率の改良版である。

> embedding 類似検索は「意味検索システムの一部」ではあっても「意味検索システムそのもの」ではない。

ACL は別のメタデータと認可機構で扱う必要があり、鮮度は ingestion と更新戦略で担保し、回答の根拠は citation 用の provenance で別途残す必要がある。

## 検索方式の整理表

| 方式 | 強み | 主な弱み | 向いている問い |
|---|---|---|---|
| grep / ripgrep | exact match、regex、速度、説明可能性 | ランキングも言い換え吸収も弱い | コード、ログ、識別子、設定 |
| BM25 / FTS / sparse lexical | exact match に強くランキングできる。BM25F は構造も使える | 語が違うと弱い | 文書検索の最低ライン |
| dense retrieval | 言い換え・同義語・自然文質問に強い | rare token・識別子・厳密条件に弱い | FAQ、自然文 QA、曖昧クエリ |
| hybrid retrieval | lexical と dense の補完が効く | 指標融合・運用複雑性が増える | 本番の第一候補 |
| rerank | top-k の並べ替え精度が高い | 遅く高価。候補生成はできない | 最終精度を詰める段階 |
| graph retrieval / GraphRAG | 全体俯瞰、多段関係、説明性 | indexing と推論のコストが高い | 多ホップ、概観、関係探索 |

## 全体アーキテクチャ — 知識化と問い合わせ処理の二本立て

![AI 検索システムの 7 段パイプライン: 上から Parse、Normalize、Enrichment、Index、Query Understanding、Hybrid Retrieval + Fusion、Rerank + Citation の流れを矢印で繋いだ縦型フローチャート。左に「Knowledge Construction」、右に「Query Time」のラベルが添えられている](/blogs/images/knowledge-pipeline-stack.png)

実運用の意味検索は、多くの場合「知識化」と「問い合わせ処理」の二本立てになる。

- **知識化**: 原本を解析し、構造とメタデータを保った形へ正規化し、lexical / sparse / dense / graph の複数 index を作る
- **問い合わせ処理**: query understanding で意図・対象集合・時間条件・権限制約を整理し、候補生成を hybrid で広く取り、最後に rerank と citation 付き生成で精度を詰める

Elastic・Azure AI Search・OpenSearch・Weaviate・Qdrant・Milvus・Vespa は、細部は違ってもこの形へ収束している。

### 7 段の役割と省略時の症状

| 段階 | 目的 | 代表技術 | 省略すると起きること |
|---|---|---|---|
| 解析 | 文書を読める形にする | Document AI, Azure DI, Unstructured, LlamaParse | 表・図・段落境界が壊れる |
| 正規化 | 構造を保って統一する | Markdown、要素 JSON、header path | 章・表題・引用元が消える |
| 候補生成 | recall を取る | BM25、SPLADE、dense、late interaction | 取りこぼしが増える |
| 融合 | 異種スコアをまとめる | RRF、weighted fusion | lexical と semantic が競合する |
| 再順位付け | precision を詰める | cross-encoder、reranker API | 上位がノイジーになる |
| 応答生成 | 根拠付きで答える | citation engine、RAG | 正答しても検証できない |
| 評価と改善 | 退行を防ぐ | golden set、Ragas、LangSmith | 品質低下に気づけない |

### Hybrid / rerank / query understanding の役割分担

**Hybrid** の役割は「意味」と「文字列」の補完だ。Elastic も Azure AI Search も OpenSearch も、keyword と vector を並列に走らせたうえで RRF などで融合する形を正式に案内している。RRF の利点は、異なるスコア空間を無理に正規化せず、**順位情報だけで頑健に統合できる** ことだ。

**Rerank** の役割は「上位候補の精密判定」である。Elastic の semantic reranking docs は cross-encoder を bi-encoder より強力な query-aware ranking と位置づけており、Sentence Transformers も cross-encoder は top-k rerank に使うのが一般的だと説明している。Cohere の Rerank API も、query と候補文書列を入力として relevance score を返す設計だ。**rerank は recall を取る道具ではなく、候補集合が取れた後に precision を押し上げる道具** だと押さえておく。

**Query understanding** の役割は、問い合わせを「検索可能な形」へ変えることだ。[HyDE](https://arxiv.org/abs/2212.10496) は仮想文書を生成して埋め込み検索を安定させる手法で、LlamaIndex は HyDE・query rewriting・sub-question decomposition をモジュール化している。Weaviate Query Agent や Azure の agentic retrieval は、平易な自然文を最適化された query・filter・routing に変換する方向へ進んでいる。これは「検索の前に意味理解を行う」層であり、単なる vector similarity とは別物だ。同じ問題意識を「モデル自身に検索方法を選ばせる」方向で整理した [adaptive search 戦略](/blogs/posts/2026/03/2026-03-17-rag-adaptive-search-strategy/) も参考になる。

### GraphRAG が必要になる条件 — そして、必要ない条件

GraphRAG が有効なのは、

- 「この文書群の主要テーマは何か」
- 「この組織の方針変更が複数部門へどう波及したか」
- 「人物・組織・出来事の関係を横断して説明してほしい」

といった **文書群全体の概観や多段関係を問う質問** だ。Microsoft Research の [GraphRAG](https://arxiv.org/abs/2404.16130) は、entity knowledge graph を作り、community hierarchy と community summaries を生成し、global search ではそれらを map-reduce して全体質問へ答える設計になっている。local search は graph と raw text を併用し、DRIFT search は local に community 情報を足して探索の breadth を強める。

逆に、FAQ・社内規程の条文検索・チケット本文の該当箇所検索・仕様書の章検索のような問いでは、GraphRAG は **過剰設計** になりやすい。GraphRAG 自身も [global search が階層レベルを下げるほど時間と LLM リソースを多く消費すると説明している](https://microsoft.github.io/graphrag/query/global_search/) し、LightRAG のような軽量化研究が出ていること自体、graph 系 indexing のコストが課題であることを示している。現実には、graph は corpus 全体の俯瞰や高価値領域に限定し、通常の検索は hybrid + rerank で回すのが現実的だ。

## ナレッジ作成パイプライン — 良い retrieval は良い parser からしか始まらない

ナレッジ作成は、文書をただ chunk へ切る作業ではない。最低でも、

- 原本収集
- レイアウト解析
- OCR
- 要素抽出
- 構造保持の正規化
- chunking
- メタデータ付与
- 引用元保持
- 権限付与
- 更新と廃止の管理

まで含む。Google の Document AI Layout Parser は text・tables・lists を context-aware chunk として抽出し、Azure Document Intelligence は text・tables・selection marks・document structure を返し、Markdown 出力では元の組織や関係性を保つと明記している。Unstructured は Title・NarrativeText・ListItem などの Element 単位へ分解し、LlamaParse は複雑レイアウトや表・図・手書きを Markdown へ変換することを前面に出している。

LlamaIndex は、`MarkdownNodeParser` で header path を metadata に持たせ、`HierarchicalNodeParser` で親子階層を保ち、`CodeHierarchyNodeParser` で AST ベースにコードブロックの scope と関係を保存できる。これは重要で、**文書検索とコード検索は同じ「chunk」でも望ましい単位が違う** からだ。自然文書は章節や見出しに沿った階層が効き、コードは関数・クラス・スコープ・参照関係が効く。「何でも 1,000 文字で切る」方式では、本当に使える知識にはならない。

### 知識オブジェクトに最低限持たせるべき metadata

本気で運用するなら、各知識片に少なくとも次のフィールドを持たせるべきだ。

- `source_id`
- `section_path`
- `title`
- `owner`
- `language`
- `created_at` / `updated_at`
- `valid_from` / `valid_to`
- `acl`（item-level access control）
- `content_type`
- `parser_confidence`
- `version_id` / `supersedes`
- `citation_span`

理由は単純で、**検索品質の多くは本文からではなく metadata と policy から決まる** からだ。Haystack・Vertex/Agent Search・LlamaIndex はメタデータフィルタを前提にしており、Microsoft Copilot connectors は item ごとの ACL を持ち、citation engine は source node を返す。

> AI が使える知識とは「文章」ではなく「本文 + 構造 + 権限 + 出典 + 時間」を持つオブジェクトである。

### 工程と品質確認の観点

| 工程 | 出力 | 代表技術・資料 | 品質確認の観点 |
|---|---|---|---|
| 原本収集 | source inventory | connectors, indexers, data stores | 所有者・更新頻度・権限 |
| 解析 | layout / OCR 結果 | Document AI, Azure DI, Unstructured, LlamaParse | 表・図・段組みの崩れ |
| 正規化 | Markdown / element JSON | Markdown 出力、element partition | 見出し階層・順序・欠落 |
| chunking | segment 群 | sentence / markdown / hierarchical / code parser | 境界・重複・粒度 |
| enrichment | metadata, tags, entities | metadata filters, entity extraction | owner・時刻・ACL・language |
| provenance | citation, source span | citation engine | どの出典か追えるか |
| indexing | lexical / dense / graph | BM25, vector, graph index | recall と更新遅延 |
| lifecycle | active / stale / archived | incremental indexing, sync policies | 廃止文書の混入防止 |

## 実装パターンの選び方

実装パターンは大きく四つに分かれる。

1. **Database-centric**: PostgreSQL + pgvector + RLS。既存アプリの近くで全文検索・行レベル権限・ベクトル検索をまとめられる
2. **Search-engine-centric**: Elastic / OpenSearch / Azure AI Search。全文検索・hybrid・rerank・DLS/FLS・indexer・connector を一枚岩で持ちやすい
3. **Vector-centric**: Qdrant / Weaviate / Milvus。dense・sparse・multivector の柔軟性が高い
4. **Graph overlay**: Neo4j / GraphRAG。通常検索の上に多ホップと概観を加える

これに加えて、Glean・Notion・Dropbox Dash・Atlassian Rovo・Microsoft Copilot connectors・Google Agent Search のような **SaaS enterprise search** は connector と permission sync を売り物にしている。

### パターン別の長所と弱点

| パターン | 代表例 | 長所 | 弱点 | 向く組織 |
|---|---|---|---|---|
| OSS 中心 | pgvector, Qdrant, Weaviate, Milvus, Vespa, OpenSearch | 自由度が高い、内製しやすい | 運用負荷が高い | 検索を核心技術にしたい組織 |
| Managed search | Azure AI Search, Google Agent Search | ACL・indexer・ranking がまとまる | ベンダー依存 | 企業向けの短期立ち上げ |
| SaaS enterprise search | Glean, Notion, Dropbox Dash, Rovo | 導入が速い、connector が豊富 | 内部 ranking の自由度が低い | 社内横断検索をすぐ始めたい組織 |
| 自前ハイブリッド | parser + search engine + vector DB + reranker | 最大自由度、差別化しやすい | 開発と継続投資が重い | 検索をプロダクト機能として持つ組織 |

### 規模別の現実的な構成案

| 規模 | 推奨構成 | 理由 | 避けたい誤り |
|---|---|---|---|
| 小規模 | PostgreSQL FTS + pgvector + metadata filter + 軽量 rerank | 既存 DB に近く、RLS も使える | いきなり分散 vector DB を足す |
| 中規模 | Elastic / OpenSearch / Azure AI Search の hybrid + RRF + cross-encoder | lexical と semantic、ACL、更新運用がまとまる | vector only に寄せる |
| 大規模 | Vespa か managed enterprise search を中核に、必要箇所のみ graph overlay | 高 QPS・巨大 corpus・multi-stage ranking に向く | 全文書を GraphRAG 化する |

小規模では [pgvector](https://github.com/pgvector/pgvector) が exact NN を default にし、ANN は「recall を犠牲に速度を取る選択肢」として後から追加する方針を取っている点が効く。中規模で hybrid + RRF + cross-encoder rerank をすぐ始めるなら、Azure AI Search の hybrid + semantic ranker、Elastic/OpenSearch の hybrid + RRF + rerank が最も現実的な選択肢になる。なお「[RAG vs CAG という雑な対立をやめる](/blogs/posts/2026/05/rag-cag-llm-knowledge-context-cache-design/)」で整理した『知識・コンテキスト・キャッシュの 3 軸』のうち、ここで扱っているのは『知識』軸の話だ。プロンプトキャッシュやロングコンテキストの話と混ぜないこと。

## 評価と運用設計

retrieval の評価は、最低でも Recall@k、Precision@k、MRR、nDCG@k を **分けて見る** べきだ。TREC Deep Learning Track は nDCG@10 を主要指標とし、recall-oriented な指標も併用している。Haystack も precision や recall を ground truth と比較する統計評価を標準にしている。

生成側は retrieval 指標だけでは見えない。Ragas は faithfulness・answer relevancy・context precision などを提供し、LangSmith は manually curated test cases・production traces・synthetic data を dataset 化した offline / online evaluation を案内している。

### 層別の評価指標

| 層 | 指標 | 見る対象 | 使いどころ |
|---|---|---|---|
| 候補生成 | Recall@k | relevant を取りこぼしていないか | BM25 / dense / hybrid 比較 |
| 上位品質 | Precision@k / Context Precision | 上位がノイズまみれでないか | fusion / rerank 調整 |
| 最初の一撃 | MRR | 最初の relevant がどこに来るか | FAQ、known-item search |
| 全体順位 | nDCG@k / MAP | graded relevance を踏まえた並び | 本番検索品質の比較 |
| 生成整合 | Faithfulness | 回答が context に支えられているか | hallucination 抑制 |
| 生成適合 | Answer Relevancy | 質問意図へ答えているか | 冗長回答・論点ずれ検出 |
| 運用 | freshness lag / ACL leakage / citation accuracy | 更新遅延・権限漏洩・根拠誤り | 本番監視 |

`citation accuracy` と `ACL leakage` は実務では必須でも、一般ベンチマークではまだ弱い領域である。自前で監視するしかない。

### 対抗クエリで「見つかってはいけないもの」を測る

ゴールデンセットには、

- 特定語が分かっている query
- 言い換え query
- 略語 query
- 日付・版数・数値 constraint query
- abstract query
- multi-hop query

を混ぜる。さらに **対抗クエリ** として、同義語・否定・略語展開・異表記・近いが違う製品名・期限切れ文書への誘導・権限外文書の存在を匂わせる問い合わせを入れる。

鮮度テストでは、文書の更新・削除・権限剥奪が **何分で検索へ反映されるか** を計測する。Glean は Slack RTS で query time に鮮度と許可を担保し、Dropbox Dash は権限同期の間隔を明示し、Azure AI Search は incremental indexing を公式に案内している。Permission leakage test は「見えてはいけないユーザー」で negative case を常に回すべきだ。

## 代表的な失敗パターン

| 失敗パターン | 症状 | 原因 | 対策 |
|---|---|---|---|
| PDF 取り込みが浅い | 表や図の情報が出ない | OCR / layout が弱い | layout-aware parser を入れる |
| 固定長 chunk だけで切る | 見出しや文脈が壊れる | 構造無視 | header / hierarchical chunking |
| vector only | 識別子や版数を落とす | lexical 欠如 | hybrid 化 |
| rerank なし | 上位がノイジー | candidate はあるが順番が悪い | top-k rerank |
| ANN 後に雑に filter | 必要件数が返らない | vector と filter の相性を無視 | prefilter / exact fallback / index 設計 |
| ACL を後付け | 権限漏洩 | 認可を retrieval 前提にしていない | item ACL を index へ同伴 |
| 更新設計なし | 古い手順が出る | incremental sync 不足 | source 別の freshness SLA |
| GraphRAG を全面適用 | コスト過大・遅い | 問いの選別がない | 高価値領域だけ graph 化 |
| connector 依存を過小評価 | 突然データが減る | 上流 API 制約変更 | query-time / direct connector / 契約確認 |

最後の行は具体的な事例がある。2025-06-11 に The Information が報じ、[Reuters も同日伝えた](https://www.reuters.com/business/salesforce-blocks-ai-rivals-using-slack-data-information-reports-2025-06-11/) ように、Salesforce が外部ソフトウェアによる Slack データの長期 indexing や保存を制限し、Glean などのアプリが Slack API 経由で取得したデータを長期保存できなくなった。connector リスクは「将来起きるかもしれない懸念」ではなく、現実にデータ供給を止める運用課題だ。

## 未解決論点

- **汎用埋め込みの『決定版』はまだない** — [MTEB](https://arxiv.org/abs/2210.07316) は単一の埋め込み法が全タスクを支配していないと述べ、BEIR も dense・sparse・late interaction・rerank の優位がタスクとコストで変わることを示した。E5 のようにベースラインを更新するモデルは出ているが、「dense さえ入れれば勝てる」時代ではない
- **enterprise search の難しさは benchmark に十分入っていない** — 多くの公開 benchmark は relevance を測れるが、ACL leakage・permission propagation delay・削除反映・connector failure・引用の正確さまでは測らない。**実務の難しさは relevance 半分、governance 半分**
- **GraphRAG の適用境界はまだ固まっていない** — Microsoft GraphRAG は global・local・DRIFT を分け、LightRAG は簡素化と incremental update を打ち出したが、どのドメインで graph 投資がペイするかは強い経験則がまだ要る
- **長文処理の競争軸も動いている** — late interaction は依然強力だが、長コンテキスト embeddings・late chunking・listwise reranking の研究と実装も進む。Jina は reranker v3 で長い context window と listwise 寄りの設計を打ち出している
- **外部プラットフォーム依存は技術選定の隠れコストである** — Slack の API 制約変更が示すように、enterprise search は ranking だけでなく connector 契約・API 利用条件・許可モデル・query-time アクセスの可否に左右される

## 実装ロードマップ — PoC の進め方

社内検索プロダクトを作るなら、流行順ではなく **一次情報が示す成功確率の高い順** で進める。

1. layout-aware parsing と metadata 付き chunking
2. BM25 + dense の hybrid
3. cross-encoder rerank
4. ACL と freshness test
5. global question が多い領域だけ graph overlay

この順番にしておくと、各段の追加投資が前段を無駄にしない。逆に「いきなり GraphRAG」「いきなり巨大 vector DB」「いきなり LLM チューニング」から入ると、ほぼ確実に下流で metadata 不足・権限漏洩・鮮度ラグに足を取られる。

## まとめ — ハーネスは検索の上に乗る

AI エージェントの性能を本当に上げる順番は、

> 知識化改善 → 検索改善 → 評価改善 → 最後にエージェント最適化

である。検索基盤が悪いと、上にどれだけ賢いエージェントを載せても、**古い・権限外・断片的・出典不明** の文脈しか渡せない。逆に、良い parser・良い metadata・hybrid candidate generation・rerank・citation・ACL・鮮度監視が揃っていれば、上の LLM や agent は比較的素直に性能を出す。

ハーネスは大事だ。だがハーネスを磨く前に、検索基盤を「現代的な意味検索パイプライン」として整え直すほうが、ほとんどの場合 ROI が高い。主要製品群が connector・permission・ranking を前面に出しているのは、この順番が実務で正しいからである。

## 関連 Wiki

- [RAG (Retrieval-Augmented Generation)](/blogs/wiki/concepts/rag/)
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/)
- [Cache-Augmented Generation (CAG)](/blogs/wiki/concepts/cache-augmented-generation/)
- [Context Rot](/blogs/wiki/concepts/context-rot/)
- [LLM Wiki パターン](/blogs/wiki/concepts/llm-wiki-pattern/)
- [Agent Memory Architecture](/blogs/wiki/concepts/agent-memory-architecture/)
