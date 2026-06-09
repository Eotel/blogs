---
title: "「ソフトウェアエンジニアリングの終わり」を読む — コードが「使い捨ての道具」になる世界の見取り図"
slug: "end-of-software-engineering"
date: 2026-06-09
lastmod: 2026-06-09
draft: false
author: "eotel"
model: "claude-opus-4-8"
description: "AI エージェントが決定ロジックの担い手をコードから奪う——arXiv 論文『The End of Software Engineering』の複雑性スケーリング論、AaaS 三世代、Agentic Engineering、SWE-bench / EvoClaw のベンチマークを批判的に読む。結論は「現時点では拡張パラダイム、完全自律はまだ先」。"
source_url: "https://arxiv.org/abs/2606.05608"
categories: ["AI/LLM"]
tags: ["AIエージェント", "ソフトウェアエンジニアリング", "LLM", "SWE-bench", "Agentic Engineering"]
---

「ソフトウェアエンジニアリングは終わる」と題された論文が 2026 年 6 月に arXiv に上がった。挑発的なタイトルだが、中身は感情論ではなく **複雑性のスケーリング則** からの第一原理的な議論で組み立てられている。本稿はこの論文 — Zhenfeng Cao, *The End of Software Engineering: How AI Agents Are Fundamentally Restructuring the Software Paradigm*（[arXiv:2606.05608](https://arxiv.org/abs/2606.05608), cs.SE / cs.AI, 2026-06-04, CC-BY 4.0）— の主張を整理し、どこが鋭くてどこを割り引いて読むべきかを検討する。

> なお本記事は単著のポジションペーパー（14 ページ、図 2・表 3）を題材にしている。論文が引用する個別の数値やシステム名は「著者がそう主張している」という距離感で読むのが安全だ。最後に批判的に読むセクションを設けた。

## 中心にある一つの問い: コードとは何の担い手か

論文の核は、ソフトウェアを 2 種類に形式的に分けるところにある。

**従来のソフトウェア（Definition 2.1）** は `S = (C, D, E)` のタプルで、`C` は計算資源、`D` はソースコードに書かれた決定論的な決定ルール、`E` は実行環境だ。決定的な性質はこう書かれている。

> The critical property is that D is static with respect to execution: all decision logic must be explicitly written by human engineers before the system encounters any input.
>
> （決定的な性質は、D が実行に対して静的であることだ。すべての決定ロジックは、システムが入力に出会う前に人間のエンジニアによって明示的に書かれていなければならない。）

つまり従来型では、機能追加・バグ修正・環境変化への適応のすべてが「人間が `D` の正しい位置を見つけて、リグレッションを起こさずに書き換える」という作業に帰着する。

**エージェントシステム（Definition 2.2）** は `A = (M, 𝒯, ℳ, Π)` のタプルで、`M` は推論エンジンとしての LLM、`𝒯` は実行可能なツール群、`ℳ` はメモリ、`Π` はプランニング機構だ。決定的に違うのは、決定ロジックが事前に書かれていない点にある。

> The key distinction is that in an agentic system, the decision logic is generated at runtime. (...) The code it generates is not the system; it is a transient artifact, produced and discarded as needed.
>
> （決定的な違いは、エージェントシステムでは決定ロジックが実行時に生成されることだ。エージェントが生成するコードはシステムそのものではない。必要に応じて生成され、捨てられる一時的な成果物だ。）

ここがタイトルの「終わり」の正体だ。コードが **決定ロジックの担い手（the carrier of decision logic）** から **推論ループのための使い捨ての道具（ephemeral tooling）** へと役割を変える。著者はこれを Karpathy の「Software 2.0」のさらに一歩先だと位置づける。Software 2.0 ではニューラルネットが手書きのプログラムロジックを *置き換えた* が、エージェントシステムではニューラルネットが *オンデマンドでプログラムを書く* —— コードはより広い推論目標に奉仕する道具になる、という整理だ。

## なぜ「終わる」のか: 複雑性は指数で、人間の認知は定数

論文がタイトルを正当化する論拠は、Brooks の『人月の神話』が指摘した **本質的複雑性（essential complexity）** のスケーリングにある。論文は次の命題を立てる。

> **Proposition 2.1 (Complexity Scaling).** For a system with n components, each potentially interacting with any other, the number of possible interaction paths P(n) is bounded by: P(n) ∈ Θ(2ⁿ)

`Θ(2ⁿ)` はビッグシータ記法で、相互作用パスがコンポーネント数 `n` に対して漸近的に 2ⁿ のオーダー（指数）で増えることを表す。

`n` 個のコンポーネントが互いに相互作用しうるとき、依存グラフの取りうる構成は指数的に増える。一方で次の一文が効いている。

> the upper bound on complexity grows exponentially, while human cognitive capacity to reason about these interactions is essentially constant.
>
> （複雑性の上限は指数的に増えるが、その相互作用を推論する人間の認知容量は本質的に一定だ。）

階層分解・モジュール化・カプセル化といった伝統的な対処は「定数項を下げるだけで漸近的な振る舞いは変えない」と切り捨てられる。ここから著者は、解くべき空間のサイズ `N` に対して、人間の認知容量 `C_H` は固定だが、LLM の実効容量 `C_M` は **モデルサイズと訓練計算量に伴って増える** と論じる。だからエージェントのパラダイムは「解の容量を人間の認知限界から切り離す（decouples solution capacity from human cognitive limits）」—— 10% の改善ではなく質的な転換だ、というのが第一原理の主張だ。

この議論の鋭さは、AI コーディングを「人間が速くコードを書くための補助輪」と見なす立場（論文が "AI→Software→Result" と呼ぶ）を構造的に否定している点にある。補助輪では最終成果物が依然として `S = (C, D, E)` のままで、複雑性の天井は `D` のサイズに縛られたまま動かない。

## 配信モデルの三世代: Local → SaaS → AaaS

歴史側の整理が分かりやすい。論文はソフトウェア配信の歴史を「複雑性をエンドユーザーから誰が引き取るか」の累進的な移転として描く。

![ソフトウェア配信の三世代とエージェンティックエンジニアリングの4段階ロードマップを示した図。上段はローカル実行（複雑性の所有者はエンドユーザー）からSaaS（ベンダー）を経てAaaSすなわちAgent-as-a-Service（エージェント）への移行を、下段はTool-Augmented・Single-Task Autonomous・Multi-Agent Teams・Self-Evolving Ecosystemsの4段階を年代と人間の役割の変化とともに示す](/blogs/images/end-of-software-engineering-roadmap.png)

| 世代 | 中核メカニズム | 複雑性の所有者 | 収益モデル | 例 |
|---|---|---|---|---|
| Software 1.0（ローカル） | コードとデータをオンプレミスで実行 | エンドユーザー（インストール・保守） | ライセンス販売 | Microsoft, Oracle |
| Software 2.0（SaaS） | コードとデータをクラウドで実行 | ベンダー（インフラ・更新） | サブスクリプション | Salesforce, AWS |
| Software 3.0（AaaS） | エージェントがクラウドで自律的に動作 | エージェント（理解・構築・実行） | 成果ベース | OpenAI, Anthropic |

この移転を貫く法則を、著者はこう要約する。

> Each transition follows the same pattern: the party best positioned to absorb complexity absorbs it, and the party least positioned to manage it is liberated from it.
>
> （どの移行も同じパターンに従う。複雑性を最も引き取れる主体が引き取り、最もそれを扱えない主体が解放される。）

SaaS が企業をサーバールームから解放したように、**AaaS（Agent-as-a-Service）** は「どう作るか（how）」の指定からユーザーを解放し、「何が欲しいか（what）」だけを言えばよくする —— これが「第三のパラダイムシフト」だという主張だ。ソフトウェアが納品されるのではなく、**成果（outcomes）が納品される**。エージェントは数千行のコードを生成し、DB クエリを実行し、API を叩くかもしれないが、それらはすべて一時的で、残るのはエージェントの *能力* であって中間成果物ではない。

## Agentic Engineering という新しい規律

論文は、この実務を従来のソフトウェアエンジニアリングと別物の規律 **Agentic Engineering** として立てる。論文は「LangChain が 2026 年 4 月に提唱した」概念だとするが、正確には引用 [7] は **Cisco の Renuka Kumar と Prashanth Ramagopal** が LangChain のブログに寄稿した記事（"Agentic Engineering: How Swarms of AI Agents Are Redefining Software Engineering", 2026-04）で、LangChain は提唱者ではなく掲載媒体だ。そこでの定義はこうなっている。

> a multi-agent coordination model where AI agents function as digital team members—each with defined roles, shared memory, and a unified observability layer—to drive software through the entire delivery pipeline, not merely to generate code faster.
>
> （AI エージェントがデジタルなチームメンバーとして機能する——それぞれが定義された役割、共有メモリ、統一された可観測性レイヤーを持ち——デリバリーパイプライン全体を駆動するマルチエージェント協調モデル。単にコードを速く生成するためのものではない。）

同じ出典は、AI コーディングエージェントと Agentic Engineering の抽象度の違いをこう対比している。

> AI coding agents excel at translating intent into code within a single user-driven session. Agentic engineering operates at a higher level of abstraction—it's a control plane that orchestrates cross-team workflows, maintains long-term memory across agents, and manages state and traceability across the full software delivery lifecycle.
>
> （AI コーディングエージェントは、単一のユーザー駆動セッション内で意図をコードに翻訳することに長けている。Agentic Engineering はより高い抽象度で動く——チーム横断のワークフローをオーケストレートし、エージェント間で長期記憶を保ち、ソフトウェアデリバリーのライフサイクル全体で状態とトレーサビリティを管理するコントロールプレーンだ。）

論文の Table 2 が二つのパラダイムの差を並べている。

| 次元 | 従来の SE | Agentic Engineering |
|---|---|---|
| 中核成果物 | ソースコード（静的） | エージェントシステム（動的） |
| 制御の中心 | 人間のエンジニア | LLM の推論エンジン |
| 決定機構 | 事前設計されたロジック | 実行時生成の推論 |
| 開発サイクル | 線形（設計→コード→テスト） | 自律的な反復ループ |
| 人間の役割 | コードの著者 | 意図のアーキテクト・調整役・監査役 |
| 複雑性の天井 | 人間の認知（O(1)） | モデル容量（計算量とともに成長） |
| エラー処理 | プログラマ定義 | モデル適応的 |
| 進化 | 手動リファクタリング | 自己修正 |

人間の役割についての主張が最も重い。従来は「正しく効率的なコードを書く能力」で価値が測られたが、エージェント時代にはコード生成スキルがコモディティ化し、差別化要因は **意図の明確化（intent articulation）**・**アーキテクチャの監督（architectural oversight）**・**品質のキャリブレーション（quality calibration）**・**倫理的ガバナンス（ethical governance）** に移る、とする。「10x エンジニア」を超える生産性の倍率は、速くタイプすることではなく、エージェントの群れを複雑な成果へと協調させる能力から生まれる、という。

## 経験的証拠 — そして冷や水としての EvoClaw

論文は楽観論一辺倒ではない。代表的なデータ点を 4 つ挙げ、最後の一つで自分の主張に冷や水を浴びせる。

**SWE-bench Verified.** 論文が引用する Ma et al. [5] によれば、オープンな開発プロセス中心モデル Lingma SWE-GPT 72B は SWE-bench Verified の GitHub Issue を **30.20%** 解決し、GPT-4o の **31.80%** に迫った。さらに 7B 版でも **18.20%** を解決した。これは約 6 倍大きい Llama 3.1 405B に対して相対 **22.76%** の改善にあたるという。静的コードではなくプロセスデータで訓練すれば小さいモデルでも意味のある自動ソフトウェアエンジニアリングができる、という論拠だ。

**マルチエージェント協調.** LangChain のパイロット研究（[7]）では、20 以上の企業デバッグワークフローに協調エージェント群を投入し、根本原因特定の時間を **93% 削減**、1 か月で 200 エンジニアリング時間以上を節約したと報告される。論文はここで「この成果は個々のエージェントの性能向上からではなく、*オーケストレーション* から来た」と強調する。

**自己進化.** 論文は Hermes Agent（Nous Research のオープンソースフレームワーク、論文は「17 万 9000 GitHub stars 超」と記載）を、自己進化原理の最も完成した実装として挙げる。複雑なタスクを終えるとエージェントが再利用可能な「Skills」（成功戦略を捉えたパラメータ化された手続きモジュール）を自律生成し、呼び出して不十分だと分かると自動でパッチを当てる「作る→使う→弱点を検知→自己修正」のループを人間の介入なしに回す、という。

**そして EvoClaw の崖.** 最も冷静なデータは EvoClaw ベンチマーク（Deng et al. [6]）から来る。これはコミット履歴をまたぐ **継続的なソフトウェア進化** をエージェントに要求するベンチマークで、各変更がシステムの整合性を保たねばならず、エラーが累積する設定だ。論文はその結論をこう引用する。

> Overall performance scores drop significantly from >80% on isolated tasks to at most 38% in continuous settings, exposing agents' profound struggle with long-term maintenance and error propagation.
>
> （総合スコアは、孤立したタスクでの 80% 超から、継続的な設定では最大でも 38% へと大きく落ちる。これはエージェントの、長期保守とエラー伝播に対する根深い苦戦を露わにする。）

論文はこの崖の背後に 4 つの課題を見る —— **コンテキストドリフト**（コードベースが実効コンテキスト窓を超えると系全体の不変条件を見失う）、**エラー伝播**（初期コミットの小さな誤りが連鎖的に膨らむ）、**技術的負債への無自覚**（即時のタスク完了を最適化し保守性を考えない）、**検証の忠実度**（テストを通しても新規入力で初めて顕在化する意味的バグを混入させる）。

著者はこのギャップを「本質的なものではない」と位置づけつつ、結論はかなり禁欲的だ。

> agentic engineering is real and transformative today as an *augmentation* paradigm, but will require several more years of concentrated research before fully autonomous software development becomes reliable in production settings.
>
> （Agentic Engineering は今日、*拡張（augmentation）* のパラダイムとしては現実的で変革的だ。だが完全自律のソフトウェア開発が本番環境で信頼できるものになるには、あと数年の集中的な研究が必要だ。）

つまり「ソフトウェアエンジニアリングは終わる」という表題とは裏腹に、**現時点での現実は拡張パラダイム** であり、完全自律はまだ先だと著者自身が認めている。タイトルは到達点の宣言ではなく、向かっている方向の宣言として読むべきだ。

## 4 段階ロードマップ

論文は到達までの道筋を 4 段階で描く（Table 3、上の図の下段に対応）。

1. **Stage I: Tool-Augmented（2023–2025）** — コード補完・単発の Issue 修正。技術は in-context learning と RAG。人間は著者かつレビュアー。代表例: GitHub Copilot, Claude Code。
2. **Stage II: Single-Task Autonomous（2025–2027）** — 仕様からデプロイまでタスクを丸ごと所有。技術はプランニング＋ツール使用と自己修正。人間は意図のアーキテクト＋監査役。代表例: Devin, OpenHands。
3. **Stage III: Multi-Agent Teams（2026–2029）** — 専門エージェントが人間の開発組織を模して協調する（PM エージェント・アーキテクトエージェント・開発者エージェント・QA エージェント）。共有メモリと可観測性が重要インフラに。代表例: LangChain のオーケストレーション, MetaGPT。
4. **Stage IV: Self-Evolving Ecosystems（2028+）** — エージェントが自らのアーキテクチャを改善し、新しい問題領域に向けてサブエージェントを生成し、人間の介入なしに環境変化へ適応する。ここで「ソフトウェア」と「エージェント」の区別は完全に溶け、人間はメタレベルのガバナンス（倫理的境界の設定・価値関数の定義・アライメントの保証）に退く。

現在地はあくまで Stage I の終盤〜II の入り口、というのが論文の自己評価だ。

## 批判的に読む — どこを割り引くか

論文の **骨格**（コード = 使い捨ての道具という再定義、複雑性スケーリングの非対称性、配信モデルの三世代）は説得力がある。一方で、いくつかの点は割り引いて読むのが妥当だ。

- **単著のポジションペーパーである。** 査読を経た実証研究ではなく、第一原理の議論と二次引用で構成された見通しの文書だ。`P(n) ∈ Θ(2ⁿ)` は「最悪ケースの上界」であって、現実のシステムがその構成をすべて実現するわけではない（論文自身も "real systems do not realize all configurations" と断っている）。複雑性の議論はレトリックとして強いが、定量的予測としては弱い。
- **引用される個別の数値は一次情報で確かめる価値がある。** Lingma SWE-GPT の 30.20%、LangChain パイロットの 93% 削減、Hermes Agent の「17 万 9000 GitHub stars 超」といった数字は、いずれも論文が引いた二次情報だ。本記事もこれらを「論文によれば」という距離で紹介している。実務判断に使うなら元の Ma et al. / Kumar and Ramagopal / Deng et al. を直接当たるべきだ。
- **EvoClaw の崖こそが本論の良心だ。** タイトルの煽りに反して、継続的進化での 38% という数字が「いま何ができて何ができないか」を最も誠実に語っている。長期保守・エラー伝播・技術的負債への無自覚という 4 課題は、現場で AI エージェントを使った人なら肌感覚と一致するはずだ。「完全自律」を売り文句にするプロダクトは、まずこの継続設定での性能を聞くべきだ、という実務的な物差しになる。

総じて、この論文は「予言」としてより「**現在地の地図**」として価値がある。コードが成果物そのものから推論の道具へ滑っていく方向は確かに見えていて、その方向で自分の役割（意図の設計・オーケストレーション・評価ハーネスの構築・ガバナンス）を再定義しておくのは、Stage I の終盤にいる今こそ妥当な投資だ。

## 関連 Wiki

- [AI エージェント](/blogs/wiki/concepts/ai-agent/)
- [自己改善エージェント](/blogs/wiki/concepts/self-improving-agents/)
- [マルチエージェント調整パターン](/blogs/wiki/concepts/multi-agent-coordination-patterns/)
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/)
- [スケーラブル・オーバーサイト](/blogs/wiki/concepts/scalable-oversight/)
