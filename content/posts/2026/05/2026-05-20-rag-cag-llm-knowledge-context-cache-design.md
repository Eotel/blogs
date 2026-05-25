---
title: "RAG vs CAG という雑な対立をやめる — 知識・コンテキスト・キャッシュの 3 軸で LLM を設計する"
slug: "rag-cag-llm-knowledge-context-cache-design"
date: 2026-05-20
lastmod: 2026-05-20
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "RAG と Cache-Augmented Generation (CAG) は対立しない。Chan et al. 2024、Lost in the Middle、Anthropic context rot を踏まえ、知識・コンテキスト・キャッシュの 3 軸でエンタープライズ LLM を設計する指針を整理する。"
categories: ["AI/LLM"]
tags: ["RAG", "CAG", "プロンプトキャッシュ", "ロングコンテキスト", "LLM"]
---

![Retrieval / Context / Cache の 3 軸を表現した抽象的なヒーロー画像。ディープブルー・グリーン・アンバーで色分けされた 3 本のピラーが等しく並び、上空のニューラルノードへ向かって 3 つのデータパスが収束していくミニマルなフラットデザイン](/blogs/images/rag-cag-3axis-hero.png)

## はじめに — 「RAG は死んだ、これからは CAG だ」が雑すぎる理由

ロングコンテキストモデルの登場以降、「RAG はもう不要、これからは Cache-Augmented Generation (CAG) だ」という言説が増えた。だがこの対立軸は、少なくとも 3 つの異なる問題を 1 つに潰している。

- **知識**: モデルが学習していない情報をどう取り込むか
- **コンテキスト**: ユーザー識別・セッション・業務状態をどう運ぶか
- **計算**: 同じプロンプト前半をどこまでキャッシュ再利用できるか

この記事は、上の 3 軸に沿って [RAG](/blogs/wiki/concepts/rag/)・CAG・キャッシュを整理し、エンタープライズで実際に使える設計判断を導く。ベースにしているのは原典 RAG 論文 [Lewis et al. 2020][1]、「Don't Do RAG」を掲げた Cache-Augmented Generation 論文 [Chan et al. 2024][2]、ロングコンテキスト評価系の一連の研究、そして OpenAI / Anthropic / Google のキャッシング公式ドキュメントである。

> 結論を先に言うと、「**RAG か CAG か**」ではなく「**何を取り出し (retrieval)、何をランタイムに持ち回り (context)、何を再利用 (cache) するか**」が正しい問い立てになる。

![RAG パス・Cache-CAG パス・Context Manager・Provider Prompt/KV Cache の 4 つを Hybrid アーキテクチャとして並置した図。ユーザークエリは Context Manager を経由してから RAG と Cache-CAG の 2 経路に分岐し、プロンプト組み立てで合流して LLM 生成へ流れる](/blogs/images/rag-cag-hybrid-architecture.png)

## 「CAG」という略称が指す 3 つの別物

実務記事を読むときに最初にぶつかる罠は、CAG という同じ略称が文脈ごとに違うものを指していることだ。少なくとも次の 3 つは区別しておきたい。

### Cache-Augmented Generation (Chan et al. 2024)

[Chan et al. の論文][2] が言う CAG は狭義のテクニカル定義で、**限られたサイズの権威あるコーパスを長いコンテキストに事前ロードし、推論時の中間状態をキャッシュしておいて、繰り返し同じバンドルに対する質問に答える**手法を指す。論文は適用範囲を「limited and manageable size の知識ソース」と明示的に限定している。

### Context-Augmented Generation (実務系記事の用法)

InfoQ などの [実務系アーキテクチャ記事][3] が使う CAG は、ロングコンテキストへの事前ロードとは別物で、**ユーザー識別・セッション履歴・ワークフロー状態・部門・ポリシー制約・パーソナライゼーション・業務ルールをアプリ側で組み立てて、検索や生成の周辺に注入するレイヤ**を指す。研究用語というよりはエンジニアリング上のパターン名である。

### Response Cache（応答キャッシュ）/ Semantic Cache

LangChain の [LLM caching][4] や Redis の [semantic cache][5] が提供するのは、**過去の応答そのものを再生して LLM 呼び出し自体をスキップする**仕組みだ。これは「計算の再利用」ではなく「回答の再利用」で、freshness とテナント分離の扱いを誤ると正しさの問題になる。

整理用のミニ語彙表を置いておく。

| 用語 | 何を再利用するか | 回答の意味は変わるか | 標準化レベル |
|---|---|---|---|
| RAG | クエリ時に取得した文書 / チャンク | はい (取得結果がクエリごとに変わる) | 高 (canonical な研究用語) |
| Cache-CAG | 事前ロード済みプロンプト前半 / KV 状態 | 同一プレフィックスならほぼ変わらない | 中 (Chan et al. の枠組み) |
| Provider prompt / context cache | 共通プレフィックスの内部 KV 状態 | 同一プロンプトに対しては変わらない (OpenAI は最終応答は変わらないと明言) | 高 (インフラ機能として) |
| Runtime KV-cache reuse | 共有プレフィックスの KV ページ / ブロック | 変わらない (推論最適化) | 高 (サービングスタック内) |
| Exact response cache | 完全一致リクエストへの保存済み応答 | 古くなり得る | 一般的な実装パターン |
| Semantic cache | 意味的に類似したリクエストへの保存済み応答 | はい (キャッシュされた応答が新しいクエリと厳密一致しないため) | 一般的な実装パターン |
| Context-CAG | アプリが組み立てたランタイムコンテキスト | はい (業務状態に応答が依存する) | 実務系アーキテクチャ用語として浮上中 |

> 設計レビューで混乱を避けるための命名規約: 検索パターンは **RAG**、有限コーパスの事前ロード + ランタイム状態再利用は **cache-CAG**、ランタイムコンテキストの管理は **context-CAG**、応答そのものの再利用は **response / semantic cache**。

## 「ロングコンテキストで RAG は要らなくなる」は条件付きで真

「コンテキストウィンドウが 100 万トークン入るなら RAG は不要だ」というのは、**条件付きで真、ただし通常は誇張**である。

成り立つのは、権威あるコーパスがモデルの **実効** コンテキスト内に収まり、繰り返し同じバンドルに対する質問が来て、更新頻度が低く、プロンプトキャッシュや KV キャッシュで前半部のコストを償却できるとき。これは Chan et al. が CAG の作戦領域として記述した条件そのものだ。[Li et al. (EMNLP Industry 2024)][6] も、リソースを十分に注ぎ込んだロングコンテキスト系は平均では RAG を上回りうると報告している。

成り立たないのは、コーパスが大規模・動的・テールヘビーまたは ACL 制約付きで、文書粒度や条項粒度の出典が必要なとき。理由はトークンコストだけではない。**ロングコンテキストの実効利用率は窓のサイズ通りには伸びない**ことが、複数の評価で繰り返し示されている。

- **Lost in the Middle** ([Liu et al. TACL 2024][7]) — 関連情報が入力の中央にあるとき性能が大きく落ちる
- **RULER** — 公称ウィンドウが大きくても 32K で満足のいく性能を維持するモデルは評価対象の半数程度しかない
- **LongBench / LongICLBench / NoLiMa** — 長文での推論や、語彙オーバーラップを減らした条件で性能が劣化する
- **[Databricks の long-context RAG 研究][19]** — 64K を超えて精度が安定するモデルは依然として数えるほどしかない

Anthropic は公式ドキュメントで次のように注意喚起している。

> "more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as *context rot*." — [Anthropic context windows docs][8]

つまり Anthropic はこの劣化現象を文字通り "context rot" と命名している ([Wiki: Context Rot](/blogs/wiki/concepts/context-rot/) も参照)。要するに、**公称容量と頑健なコンテキスト利用率は別物**である。

正しい解釈は「ロングコンテキストはワークロードの**ヘッド**は置き換えうるが、ロングテール全体までは置き換えない」というもので、[Li et al.][6] が blanket replacement ではなくルーティングを提案しているのもこの理由だ。

## RAG / Cache-CAG / Hybrid のパイプライン比較

### 典型的な RAG パイプライン

知識ベースがコンテキストに乗せきれないほど大きい・動的なときに最もクリーンな解。ドキュメントを取り込み、チャンク化と索引化を行い、クエリ時に検索とリランキングをして、最も関連するエビデンスだけを LLM に渡す。新鮮さ・[ACL フィルタ][9]・リランキング品質・多様性・引用処理が独立した制御点として持てるのが強みである ([LlamaIndex の RAG 文書][10] の整理に従う)。

### Cache-CAG パイプライン

[Chan et al.][2] の手順は「knowledge preloading → inference from the stored cache → fast cache reset」の 3 段で、リトリーバーの複雑性と検索ミスのリスクを丸ごと消す代わりに、**ロングコンテキスト利用率とコーパス版数管理に新しい依存を生む**。

### Hybrid (推奨デフォルト)

最も堅牢な企業向けパターン。静的または変化の遅いポリシー文書・マニュアル・リポジトリマップはキャッシュまたは事前ロード、動的でテールな情報は依然として retrieval、ユーザー識別・ワークフロー状態・ポリシー制約は別の Context Manager で組み立てる。これがアーキテクチャ用語としての context-CAG の意味する所であり、Provider 側のプロンプトキャッシュや、検索を維持しつつチャンク単位 KV キャッシュを先計算する [TurboRAG (Lu et al. 2024)][11] と相性が良い。TurboRAG はベンチマーク平均で **TTFT を 8.6 倍短縮、最大 9.4 倍**、標準的な RAG と同等の精度を維持したと報告している。

## キャッシュは「インフラ最適化」とは限らない

「キャッシュはインフラ最適化に過ぎず、回答の意味には影響しない」という主張は**プレフィックス / KV キャッシュには真、応答キャッシュには偽**である。

- [OpenAI prompt caching][12] は「Regardless of whether caching is used, the output generated will be identical」と明言している。プレフィックスの KV 状態を内部で再利用しているだけで、出力されるトークンは変わらない。
- [vLLM Automatic Prefix Caching][13] と TensorRT-LLM の KV ブロック再利用も、共有プレフィックスの prefill 計算を省略する純粋な推論最適化である。
- 一方で [Redis の semantic cache][5] は埋め込み類似度で過去の応答を再生する。これは応答の選択に参加しており、freshness window・テナントキー・無効化ポリシーが**性能の問題ではなく正しさの問題**になる。

キャッシュを語るとき、この 2 種類を混ぜないことが議論を建設的にする第一歩だ。

## 設計判断のマトリクス

3 つの資産 — **権威ある知識・ランタイム業務状態・再利用可能な計算** — を分離して考えるのが、根本的な設計姿勢になる。

| コーパス / ユースケース | デフォルト選択 | 根拠 |
|---|---|---|
| 小規模・安定したコーパス | Cache-CAG + プロンプト / KV キャッシュ + コーパス版数管理 | Chan et al. の作戦領域そのもの。Provider キャッシュで繰り返しプレフィックスのコストとレイテンシが下がる |
| 中規模で安定性混合 | Hybrid (安定バンドルを preload、動的テールを retrieve) | ルーティングと計装が増えるが大半の CAG 利得を取れる |
| 大規模・動的コーパス | RAG + リランキング + sufficiency チェック + 引用 / abstention 制御 | スケーラブルに作業コンテキストを小さく保てる唯一の手段。リトリーバーの質が品質を支配する |
| コードベース | Hybrid (リポマップや構造サマリは cache、ファイル / シンボル / ブランチは retrieve) | Google は [context caching の例][14] にリポジトリ解析を明示しているが、大規模・ブランチ活動のあるリポジトリ全体は静的プロンプト化しづらい |
| 契約書・マニュアル | デフォルトはセクション認識 RAG。単一文書レビューに限り cache-CAG | 条項粒度の出典が要るワークロードと自然に噛み合う |
| 社内ナレッジ | namespace / metadata filter 付き Hybrid + Context Manager | ACL 感受性が高く、組織状態と混在する。retrieval フィルタと明示的コンテキスト組み立ての両方が必要 |
| ローカル LLM デプロイ | vLLM / TensorRT-LLM のプレフィックスキャッシュ + 小さな RAG | プレフィックス再利用の恩恵が大きい一方、KV メモリが先に頭打ちする |
| サポートボット | Hybrid: アカウント / セッション Context Manager + KB RAG + FAQ への semantic cache | サポート回答はユーザーコンテキスト依存。semantic cache は freshness と tenant scope を要する |
| 業務エージェント | permission-aware RAG を context-CAG で包む + 安定したポリシー / システムプレフィックスをキャッシュ | 「誰が、どの業務状態で、どの制約下で問い合わせているか」は retrieval だけでは表現できない |

選択ルールを 1 段落で要約するとこうなる。**権威あるバンドルがすべてモデルの実効コンテキストに無理なく収まり、変化が遅く、再利用頻度が高いなら cache-CAG から始める**。大規模・動的・ACL 制約のいずれかがあれば **RAG から始める**。「誰が・どのワークフロー状態で」が回答に効くなら、いずれの場合でも **Context Manager を足す**。安定プレフィックスが大きく繰り返されるなら、知識戦略と無関係に **Provider のプロンプト / KV キャッシュを足す**。

## ベンチマーク設計と運用メトリクス

この設計判断のための良いベンチマークは、回答正解率だけでは不十分で、少なくとも次を分けて測る必要がある。

| 観点 | 推奨メトリクス | なぜ必要か |
|---|---|---|
| 回答正解率 | Exact Match / F1 / タスクスコア / 人手評価 | コアな課題達成度 |
| Faithfulness | [AIS-style support rate (Rashkin et al. 2023)][15] | 正解だが出典が無いケースと、出典に支持された回答を区別する |
| 引用品質 | [ALCE (Gao et al. EMNLP 2023)][16] | 引用された出典が実際に主張を支持しているかを評価 |
| 検索効用 | recall@k / nDCG@k / [eRAG][17] / sufficiency rate | relevance は downstream utility を必ずしも捉えない。Google の sufficient-context 研究 ([blog post][18]) は relevance より sufficiency の方が有用と論じる |
| コンテキスト利用率 | position-based / 語彙オーバーラップ抑制 / multi-hop テスト | ロングコンテキストの失敗モードを captures する |
| レイテンシ | TTFT と E2E (retrieve / rerank / prefill / decode 分割)、p50 / p95 / p99 | キャッシュ効果は phase によって偏在する |
| コスト | input / output / cached tokens、embedding / index コスト | 「速いが高い」「精度高いが運用が辛い」を表面化させる |
| キャッシュ挙動 | hit rate / miss rate / eviction rate / warm/cold ratio | cache-CAG が実際に効いているかの判定 |
| ガバナンス | cross-tenant 漏洩率 / role-policy 違反率 | 社内ナレッジ・業務エージェントでは必須 |

これに加えて、**同じクエリ・同じコーパスのスナップショット**に対して 4 種の system variant — classical RAG / cache-CAG cold start / cache-CAG warm start / Hybrid — を必ず並列に走らせる。さらにロングコンテキスト重視のタスクでは、関連事実をコンテキストの先頭 / 中央 / 末尾に置く位置依存テスト、語彙オーバーラップの高低を振るテスト、複数文書合成を要するテストをセットで持つ。これらは Lost in the Middle、RULER、NoLiMa、LongBench、LongICLBench からそのまま導かれる要請である。

キャッシュメタデータは Provider が露出している。OpenAI は応答に `cached_tokens` を返し、リクエスト側で `prompt_cache_key` を指定できる。Anthropic は応答にキャッシュ読み込み / 作成のトークン数 (`cache_read_input_tokens` / `cache_creation_input_tokens`) を、Google は `cachedContentTokenCount` を含めて返す。これらは本番ログに必ず出力すべきだ。

## まとめ — retrieval / context / cache で分けて設計する

設計問題は本質的に「RAG vs CAG」ではない。

- **外部知識アクセスは retrieval で解く** — 大規模・動的・パーミッション付きコーパスでは依然として RAG が最も一般化されて統治しやすい解。
- **ランタイム業務状態は context assembly で解く** — ユーザー・セッション・ポリシーへの依存は、retrieval でも cache-CAG でもなく、明示的な Context Manager で扱うのが clean。
- **繰り返しの prefill コストは caching で解く** — Provider のプロンプト / KV キャッシュは知識戦略と独立に効く。

実戦投入の現実解は、**RAG をバックボーンとし、業務状態を Context Manager に置き、構造が繰り返される箇所に prefix / KV キャッシュを積極適用する** こと。1〜2 の権威コーパスがトラフィックの大半を占めるなら、その経路にだけ cache-CAG ファストパスを追加する。引用の信頼性が要るなら、Provider キャッシュの内部にプロベナンスを期待せず、プロンプト組み立て側で source id を明示的に運ぶ。最後に、warm / cold パスは分けて計測し、キャッシュヒット率はレイテンシと同じ重さで計装し、sufficient-context チェックと abstention を後付けの安全弁ではなく第一級の設計要素として持つこと。

## 関連 Wiki

- [RAG (Retrieval-Augmented Generation)](/blogs/wiki/concepts/rag/) — RAG の基本と Karpathy の LLM Wiki 批判、アダプティブ検索
- [Context Rot (コンテキスト劣化)](/blogs/wiki/concepts/context-rot/) — ロングコンテキスト劣化と Anthropic の 5 択セッション管理
- [コンテキスト圧縮](/blogs/wiki/concepts/context-compression/) — Claude Code の 5 段カスケード圧縮戦略

## 参考文献

[1]: https://arxiv.org/abs/2005.11401 "Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, NeurIPS 2020"
[2]: https://arxiv.org/abs/2412.15605 "Chan et al., Don't Do RAG: When Cache-Augmented Generation is All You Need for Knowledge Tasks, 2024"
[3]: https://www.infoq.com/articles/beyond-rag-context-aware/ "InfoQ, Beyond RAG: Building Context-Aware AI Applications"
[4]: https://docs.langchain.com/oss/javascript/integrations/llm_caching "LangChain, LLM Caching"
[5]: https://redis.io/docs/latest/develop/ai/redisvl/0.6.0/user_guide/llmcache/ "Redis, Semantic Caching for LLMs"
[6]: https://aclanthology.org/2024.emnlp-industry.66/ "Li et al., Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach, EMNLP Industry 2024"
[7]: https://aclanthology.org/2024.tacl-1.9/ "Liu et al., Lost in the Middle: How Language Models Use Long Contexts, TACL 2024"
[8]: https://docs.anthropic.com/en/docs/build-with-claude/context-windows "Anthropic, Context Windows"
[9]: https://docs.pinecone.io/guides/index-data/implement-multitenancy "Pinecone, Implement Multitenancy"
[10]: https://developers.llamaindex.ai/python/framework/understanding/rag/ "LlamaIndex, Understanding RAG"
[11]: https://arxiv.org/abs/2410.07590 "Lu et al., TurboRAG: Accelerating Retrieval-Augmented Generation with Precomputed KV Caches for Chunked Text, 2024"
[12]: https://developers.openai.com/api/docs/guides/prompt-caching "OpenAI, Prompt Caching"
[13]: https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html "vLLM, Automatic Prefix Caching"
[14]: https://ai.google.dev/gemini-api/docs/caching "Google, Gemini API Context Caching"
[15]: https://aclanthology.org/2023.cl-4.2/ "Rashkin et al., Measuring Attribution in Natural Language Generation Models, Computational Linguistics 2023"
[16]: https://aclanthology.org/2023.emnlp-main.398/ "Gao et al., Enabling Large Language Models to Generate Text with Citations (ALCE), EMNLP 2023"
[17]: https://arxiv.org/abs/2404.13781 "Salemi & Zamani, Evaluating Retrieval Quality in Retrieval-Augmented Generation (eRAG), SIGIR 2024"
[18]: https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/ "Google Research, Deeper Insights into Retrieval-Augmented Generation: The Role of Sufficient Context"
[19]: https://www.databricks.com/blog/long-context-rag-performance-llms "Databricks, Long Context RAG Performance of LLMs"
