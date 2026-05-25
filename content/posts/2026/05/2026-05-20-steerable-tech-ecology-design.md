---
title: 操舵可能な技術生態系（STE）── ケヴィン・ケリーの Technium を AI ガバナンスの語彙に置き換える
slug: steerable-tech-ecology-design
date: 2026-05-20
lastmod: 2026-05-20
draft: false
author: eotel
model: claude-opus-4-7
description: ケヴィン・ケリーの Technium に代わる中範囲概念として「操舵可能な技術生態系 (Steerable Technological Ecosystem,
  STE)」を提案する。AI ガバナンス、修理する権利、cosmotechnics、EU AI Act、national compute を貫く設計語彙として、steerable
  / technical / ecology / selection environment / reversibility の五部品を Mumford・Ellul・Hughes・Latour・Jasanoff・Hui・Jackson
  の系譜から構築する。
categories:
- AI/LLM
tags:
- 技術哲学
- ケヴィン・ケリー
- テクニウム
- AIガバナンス
- 修理する権利
- cosmotechnics
- STS
audio_url: https://github.com/Eotel/blogs/releases/download/audio/2026-05-20-steerable-tech-ecology-design.m4a
audio_lang: ja
audio_generated_at: '2026-05-21T05:48:36Z'
audio_source: notebooklm
audio_format: deep_dive
---

![Steerable Technological Ecosystem の五部品（Steerable / Technical / Ecology / Selection Environment / Reversibility）が歯車のように連動する概念図](/blogs/images/steerable-tech-ecology-five-components.png)

## エグゼクティブサマリ

前稿 [テクニウム概念への批判と超克](/blogs/posts/2026/05/technium-critique-and-transcendence/) では、Kevin Kelly の technium を「ヒューリスティックとしては有効だが、政治理論としては未熟」と評価し、代替概念として **操舵可能な技術生態系 (Steerable Technological Ecosystem、以下 STE)** を提案した。本稿はその続編として、**STE の構成要素・操舵メカニズム・設計原則** を本格的に設計する。

結論を先に書く。STE は、technium を分析概念として置き換える有力な候補ではある。ただし、それは「技術に固有の生命や意志がある」という強い存在論を採るからではない。むしろ逆で、技術を、**制度・市場・所有・教育・インフラ・評価・保守・撤退設計によって方向づけられる、可塑的で複数的な複雑系** として捉えるからだ。

この見方は、Kelly の「技術の総体は連鎖し相互依存し自己強化的に見える」という観察を残す。同時に、Ellul の technique、Lewis Mumford の技術文明史、Thomas Hughes の大規模技術システム、Bruno Latour・Madeleine Akrich・Sheila Jasanoff の STS (Science and Technology Studies、科学技術社会論)、香港の哲学者 Yuk Hui の cosmotechnics、Steven Jackson や The Maintainers の maintenance/repair 研究を継承する。本稿はこれらを一本の設計語彙へ束ね直すことを目指す。

## 定義 ── 五部品で構成する

STE は五つの部品から構成すると最も整合的になる。前稿で骨子だけ示したが、ここでは各部品の根拠と実務的含意を明確にする。

### 1. Steerable ── 「方向づけられる」ことを設計する

ここでの「操舵」は「完全に支配可能」を意味しない。Collingridge が示した通り、技術は初期には影響が予測しにくく、後期には埋め込みが進んで変えにくい。だから操舵とは、**早い段階の可逆性確保と、後期の退出・修理・代替経路の設計** を指す。Stafford Beer の管理サイバネティクス（組織の複雑性 = variety を扱う理論）で言えば、variety を吸収する自律性設計である。Jackson や repair 政策の文脈で言えば、壊れたときに回復できる社会技術条件の整備を指す。

### 2. Technical ── 装置だけでは不十分

IIASA (International Institute for Applied Systems Analysis) は技術を「hardware、software、orgware」の三層で捉える定義を採っており、技術には物・知識・制度が含まれる。Susan Leigh Star のインフラ論、Madeleine Akrich の script 論も、技術が plug、standard、form、manual、UI といった平凡な要素に宿ることを示している。したがって「技術生態系」は、AI のモデル本体だけでなく、API、評価器、クラウド契約、保守契約、学習データ、教育カリキュラム、権限管理まで含むべきだ。

### 3. Ecology ── 単なる比喩としての「生態系」ではない

Susan Leigh Star は ["The Ethnography of Infrastructure"](https://www.ics.uci.edu/~wscacchi/GameLab/Recommended%20Readings/ethnography-infrastructure-Star-1999.pdf) (American Behavioral Scientist, 1999) で、インフラを **relational** かつ **ecological** な対象としてフレーミングし、さらに 9 つの性質を列挙した（Embeddedness、Transparency、Reach/Scope、Learned as part of membership、Links with conventions of practice、Embodiment of standards、Built on installed base、**Becomes visible upon breakdown**、Fixed in modular increments）。本稿が STE の ecology 部品にとくに重要だと考えるのは、このうち以下の三点だ（Star の 2 項フレーミングと breakdown 性質を踏まえた本稿の再整理である）。

- **関係的 (relational)** ── 何かに対して「インフラ」になる。ある活動者にとっての道具が、別の活動者にとってはインフラに見える
- **生態学的 (ecological)** ── 多くの構成要素が相互依存して動いている
- **故障時に可視化される (becomes visible upon breakdown)** ── ふだんは透明で見えないが、壊れた瞬間に不透明に現れる

STE における ecology は、この性質を継承する。Kelly の technium も、技術全体を相互依存する自己組織系として見る点で同じ直観を持っていた。だが STE はそれを **単一の巨大主体ではなく、多層の関係生態** として受け直す。

### 4. Selection Environment ── 本概念の要

Kelly の問いは「What does technology want?」だった。STE の問いはそれを反転させる ── **「どの環境が、どの技術的振る舞いを選び、生き残らせ、拡張し、あるいは衰退させるのか」**。

Jasanoff の sociotechnical imaginaries、Latour/Akrich の network/script、Hughes の reverse salient はいずれも、技術の方向が単独の発明者や単独の市場ではなく、**制度化された選別** から生じることを示す。AI ではとくに、evals、UI の既定値、課金モデル、クラウド credits、モデル公開形態、修理制限、調達条件が、この selection environment の具体項目になる。

### 5. Reversibility ── 法・設計・契約・保守の実装要件

可逆性は「全部を元に戻せる」という幻想ではない。やめられること、切り離せること、代替できること、監査できること、保守できること、ローカルに寄せられることの総称である。

EU の修理に関する指令 (Directive (EU) 2024/1799、いわゆる "right to repair" directive) は、修理義務、修理阻害ソフトウェアの禁止、スペアパーツ供給、保証延長、修理プラットフォームまで制度化した。米国 FTC の "Nixing the Fix" 報告は、メーカーによる修理制限が消費者をメーカーの修理ネットワークに誘導し、実質的に製品寿命を短くしているとまとめている。可逆性は思考実験ではなく、**法・設計・契約・保守の実装要件** である。

### 五部品のまとめ表

| 構成要素 | 分析上の意味 | 実務上の含意 | 根拠 |
|---|---|---|---|
| Steerable | 方向づけ・介入・停止・代替が可能 | kill switch、ロールバック、退出権、複線化 | Collingridge、Beer、repair 政策 |
| Technical | 物＋コード＋規格＋組織＋契約 | API、権限、保守、契約設計まで対象化 | IIASA、Star、Akrich |
| Ecology | 相互依存・脆弱性・多層性 | 局所最適ではなく全体系評価 | Star、Hughes |
| Selection Environment | 何が採用・拡張・淘汰されるかを決める条件 | 規制、評価、調達、課金、UI を設計変数にする | Jasanoff、Hughes、CMA |
| Reversibility | やめられる・直せる・移れる・戻せる | repairability、exportability、sunset plan | EU 修理指令、FTC 報告 |

## Technium 批判 ── 四つの水準を区別する

[前稿](/blogs/posts/2026/05/technium-critique-and-transcendence/) と重複しすぎないよう、ここでは批判を **存在論・ヒューリスティック・政治理論・AI 適用** の四つの水準に分けて整理する。Kelly に対するすべての批判をひとつのラベル（「技術決定論」など）に束ねてしまうと、概念のどこを残しどこを捨てるかが見えなくなるからだ。

| 争点 | Technium の長所 | Technium の限界 | STE の置換案 |
|---|---|---|---|
| 存在論 | 技術を総体系として見せる | emergent pattern を超主体化しやすい | 主体ではなく「操舵されうる複雑系」とみる |
| ヒューリスティック | 相互依存・収斂・慣性を可視化 | 欲望語りが説明を曖昧にする | selection environment と feedback で言い換える |
| 政治理論 | 技術圏の大きさを示す | 所有・競争・国家・軍事・調達を薄く扱う | 所有構造・規制・調達・修理政策を中核に置く |
| AI 時代 | 自己運用的風景を捉えやすい | AI を神話化しやすい | RLHF/RLAIF/evals/RSP/compute を制度化された最適化として分析する |

Kelly の最大の強みは、emergent な相互依存を概念化したことだ。彼自身、講演や著作で technium を **自己組織化する複雑系** として描写し、「the greater, global, massively interconnected system of technology vibrating around us」と要約している（[Edge.org でのインタビュー](https://www.edge.org/conversation/kevin_kelly-the-technium)）。これは Hughes の technological systems や Latour の durability、Star の infrastructure、Jasanoff の imaginaries と並べると、「技術の総体が個別発明の寄せ集め以上である」という直観をうまく掴んでいる。STE はそこを **捨てない**。

捨てるのは、emergent pattern を「欲望ある主体」として語り直す側の動作だけだ。STE はそれを「自己強化する selection environment と相互依存ネットワーク」と言い換える。

## 操舵メカニズム ── AI 時代に何が方向を決めるか

STE が実務語彙として機能するかは、「具体的に何が操舵装置か」を列挙できるかにかかっている。AI を例に八つ示す。

### (1) 法・標準

NIST AI Risk Management Framework は 2023 年 1 月に初版 (AI RMF 1.0) が公開され、2024 年 7 月には生成 AI 固有のリスクを扱う [Generative AI Profile (NIST AI 600-1)](https://www.nist.gov/itl/ai-risk-management-framework) が追加された。OECD AI Principles は 2024 年 5 月に更新され、生成 AI と汎用 AI のリスクを取り込んだ。EU AI Act は 2024 年 8 月 1 日に発効し、義務の大部分は 2026 年 8 月 2 日に適用開始という段階的タイムラインを採用している。AI の方向づけがすでに「自主規範」だけでなく、公的ルール形成の段階に入っていることを意味する。

### (2) 所有・市場・競争

英国 CMA は 2025 年 7 月の Cloud services market investigation 最終決定で、UK・EEA を合算した IaaS 市場で Microsoft と AWS がそれぞれ 30–40%、Google が 5–10% のシェアを占めると認定した。さらに Microsoft・AWS・Google を accelerated compute と AI 関連クラウドサービスの **vertically integrated providers** として位置づけている。論点は単なるシェア数値ではない ── 誰が計算資源・モデル流通・周辺サービスを支配するかが、どの AI 形態が伸び、どれが市場から退出するかを実質的に決める。

### (3) 評価・ベンチマーク

OpenAI の公式ドキュメントは、evals を信頼可能な LLM アプリ構築の本質的要素として説明し、real-world distributions を反映した task-specific eval を継続的に回すべきだとする。Anthropic は Claude の constitution を公開しており、2023 年の [Collective Constitutional AI](https://www.anthropic.com/news/collective-constitutional-ai-aligning-a-language-model-with-public-input) では Polis を介した約 1,000 人の米国参加者から得た public input をもとに別の constitution を作り、それで訓練したモデルが標準モデルとどう違うかを比較した。**ベンチマークは測定器であると同時に、開発目標そのものになる**。

### (4) UI・script

Akrich は、技術的対象の設計者が、対象の性質を決めると同時に、人と対象の関係も「script」していると論じた。AI アシスタントの **既定値、拒否挙動、提案文の選好、ボタンの並び、ログ取得の有無** は、利用者の振る舞いを前もって整形する。コードを書かなくても、設定とコピーだけで操舵が起こる。

### (5) 教育・専門職

何を作れる人が増えるかが、どの技術圏が伸びるかを決める。Right to repair の文脈では、修理スキル振興そのものを操舵装置に位置づける議論があり、AI 文脈では eval culture（評価を書く文化）と安全運用スキルが同じ役割を果たす。

### (6) 電力・計算資源

IEA の [Energy and AI](https://www.iea.org/reports/energy-and-ai) (2025) は、データセンターの世界電力消費を 2024 年に約 415TWh、2030 年のベースケースで約 945TWh と予測した。成長はとくに accelerated servers (AI 向け GPU/TPU) が牽引する。OECD は [A blueprint for building national compute capacity for AI](https://www.oecd.org/en/publications/a-blueprint-for-building-national-compute-capacity-for-artificial-intelligence_876367e3-en.html) (2023) で、national AI compute plan の不在を policy blind-spot と呼び、capacity・effectiveness・resilience の三側面を示した。AI をどこに置くかは、便利かどうかだけでなく、**どの送配電網・どの地域・どの冷却方式・どの電力源に乗るか** というインフラ政治である。

### (7) 配置アーキテクチャ ── ローカル AI と集中型 AI

Apple は [Private Cloud Compute](https://security.apple.com/blog/private-cloud-compute/) (PCC、2024) の発表で、配置アーキテクチャを二段階で語っている。第一に、on-device 計算が可能な場合は端末がユーザーの統制下にあり、研究者がハードもソフトも検査できることを privacy/security 上の利点として挙げる。第二に、より高度な要求のためにはクラウドが必要だが、その場合は PCC サーバ側で **Apple の運用スタッフですら privileged interfaces 経由でユーザーデータにアクセスできないこと**、**production software image を独立検査可能な形で公開すること** を約束している ── すなわち、cloud に降りた場合でも操舵可能性を保つ設計だ。一方、Google AI Edge / [Google AI Edge Gallery](https://ai.google.dev/edge) は、generative AI を含む処理を Android / iOS / web / embedded に展開し、ローカル LLM の実行体験を提供する。

ここから導けるのは、ローカル AI が常に善で、クラウド AI が常に悪だという単純図式ではない。

| AI 適用論点 | 集中型クラウド | オンプレ / エッジ / ローカル | 操舵の観点 |
|---|---|---|---|
| 性能と更新 | 大規模モデル更新が速い | 端末性能と保守に制約 | 一律ではなく用途別分離が必要 |
| プライバシー | 事業者設計に依存 | 端末主体の制御が強い | 機密・個人情報ほど local-first が有利 |
| 競争と依存 | Cloud lock-in が起きやすい | 依存を分散できる | 可搬性・輸出可能性を要件化すべき |
| エネルギーと配置 | 地域集中が起こる | 分散配置で一部緩和 | ただし総効率は用途次第 |
| 主権とアクセス | 少数事業者・少数地域に集中しやすい | 国家・組織の主権を高めやすい | OECD の national compute 視点が有効 |

操舵の問いは「どちらが優れているか」ではなく、**「どの用途をどの場所に置くと、可逆性と責任分界が最も明確になるか」** である。

### (8) 修理・保守・撤退

EU の repair directive は、修理義務、修理阻害ソフトや契約条項の制限、スペアパーツアクセス、修理後の保証延長、共通の修理プラットフォーム、修理スキル振興までを制度化した。FTC は repair restrictions が早すぎる買い替えを促していると結論づけている。AI でも同じで、停止、縮退運転、モデル切替、データエクスポート、評価器更新停止、API 廃止計画が制度として必要だ。

## 設計原則 ── 四つのレイヤーで「介入点」を増やす

STE を実務に落とす原則は、「より賢い自動化」ではなく、**より明確な介入点を増やす** ことだ。プロダクト、AI システム、組織、政策の四レイヤーで最小原則を示す。

### プロダクト

- 既定値を可逆にし、上書き可能にする
- データと設定の export / import を標準化する
- バージョン固定、ロールバック、縮退運転を実装する

### AI システム

- constitution / system rule / eval 体系を公開可能な範囲で明示する
- 公的 benchmark だけでなく、現場 task-specific eval を持つ
- compute・latency・energy の予算を設計要件に入れる

### 組織

- モデル所有、インフラ所有、監査責任を分けて明示する
- 定期的な sunset review を設ける
- 「誰が操舵者か」を曖昧にしない

### 政策

- 調達条件に repairability、interoperability、logging、exit を入れる
- competition policy と right to repair を AI インフラまで拡張する
- national compute と grid/cooling/water の制約を AI 戦略の前提に置く

## STE の固有貢献 ── 五点に束ねる

STE が既存理論の単なる寄せ集めではなく、固有の設計語彙を提供しうるのは、次の五点を一本に束ねるからだ。

1. **欲望ではなく選択環境を分析単位にする** ── 「technology wants X」ではなく「environment selects X」
2. **成長ではなく maintenance と reversibility を中心指標に置く** ── 何を作るかではなく、何を保ち、何をやめられるか
3. **単数の Technology ではなく複数の技術圏を認める** ── Hui の cosmotechnics を継承
4. **人間を「外部」でも「宿主」でもなく、継続的な操舵者として置く** ── 介入・停止・代替を設計原理に
5. **AI を、意志や自律神話ではなく、protocol・eval・resource constraint・ownership structure の結節として理解する**

## 未解決の論点 ── 操舵という語をどう守るか

STE は完成品ではない。次の論点はまだ閉じていない。

- 可逆性をどう測るか（停止時間、ロールバック容易性、exportability、repairability、保守費比率の合成指標が要る）
- ローカル AI が本当に主権を増やすのか、それとも別の上流依存（モデル重み配布、ファインチューン基盤、半導体）を隠すだけなのか
- 複数の技術圏を認めながら、相互運用性と安全基準をどう保つか
- 保守コストを誰が負担するか
- 「操舵」が民主的参加を意味するのか、それとも新しい管理技術の正当化になるのか

最後の論点はとくに重要だ。「操舵可能」と言った瞬間、誰がハンドルを握っているかという問いから逃げにくくなる。Jasanoff が imaginaries の制度的安定化を、Beer が autonomy 設計を、EU と FTC が repair 制度を示している以上、これらは抽象的な思弁ではなく、すでに運用と規制の場にある問いである。

## 研究アジェンダ

短期に着手できる課題を五つ挙げる。

1. **Reversibility 指標の設計** ── 停止時間、ロールバック容易性、exportability、repairability、保守費比率を組み合わせた合成指標
2. **Selection environment の監査手法** ── law・pricing・credits・UI・benchmark・compute のどれが、実際に挙動を最も強く選んでいるかを比較可能にする
3. **比較 cosmotechnics** ── 国・地域・産業・組織文化ごとに技術圏がどう異なるかを記述する経験研究
4. **AI インフラ主権と competition** ── national compute と垂直統合型クラウドの実証研究
5. **Sunset design の実装** ── どの条件で、どの AI 機能を停止・縮退・分離するのが適切かの設計パターンの蓄積

## 結論

存在論としての Technium は過剰だ。ヒューリスティックとしての Technium はなお有効である。しかし、AI 時代の分析概念として必要なのは、Technium よりも、**操舵・可逆性・保守・所有・評価・複数技術圏を前面に出す「操舵可能な技術生態系」** である。

この概念は、技術を過小評価せず、同時に神話化もしない、その中間の位置を与える。Kelly の与えた「文明叙事詩」としての魅力は失われる。しかし研究概念としては前進である。「操舵」が新しい管理技術の正当化に堕する危険は残る ── だからこそ条件節が要る。Yes, but conditionally ── STE は Technium を置き換えうる。**条件は、何が操舵装置で、誰が操舵者で、どこから降りられるかを、毎回明示することだ**。

## 参考リンク

### 理論的系譜

- [Kevin Kelly, *What Technology Wants* (Carnegie Council 掲載 PDF)](https://cdn.carnegiecouncil.org/media/cceia/import/studio/What_Technology_Wants.pdf)
- [IIASA, "What is technology?"](https://iiasa.ac.at/what-is-technology)
- [Bruno Latour, "Technology is society made durable" (1991)](http://www.bruno-latour.fr/sites/default/files/46-TECHNOLOGY-DURABLE-GBpdf.pdf)
- [Madeleine Akrich, "The de-scription of technical objects"](https://pedropeixotoferreira.files.wordpress.com/2014/03/akrich-the-de-scription-of-technical-objects.pdf)
- [Susan Leigh Star, "The ethnography of infrastructure" (1999)](https://www.ics.uci.edu/~wscacchi/GameLab/Recommended%20Readings/ethnography-infrastructure-Star-1999.pdf)
- [Sheila Jasanoff & Sang-Hyun Kim, *Dreamscapes of Modernity* (2015) — Introduction PDF](https://law.unimelb.edu.au/__data/assets/pdf_file/0009/3305673/1.-Jasanoff-and-Kim-2015-Dreamscapes-of-Modernity-Sociotechnical-Imaginari.pdf)
- [Thomas P. Hughes, "The seamless web: Technology, science, etcetera, etcetera" (WZB Discussion Paper)](https://bibliothek.wzb.eu/pdf/1986/p86-9.pdf)
- [Yuk Hui, "Cosmotechnics as Cosmopolitics" (Philosophy and Technology Network 紹介)](https://philosophyandtechnology.network/605/article-cosmotechnics-as-cosmopolitics-by-yuk-hui/)
- [Lewis Mumford, *Technics and Civilization* — University of Chicago Press](https://press.uchicago.edu/ucp/books/book/chicago/T/bo10388066.html)
- [Jacques Ellul on technique — ellul.org](https://ellul.org/themes/ellul-and-technique/)
- [Steven Jackson, "Rethinking Repair" — Mines Paris 紹介](https://www.csi.minesparis.psl.eu/agenda/steven-jackson/)
- [David Collingridge dilemma — Liebert (2010)](https://www.axelarnbak.nl/wp-content/uploads/2014/01/Liebert-2010-Collingridge%E2%80%99s-dilemma-and-technoscience.pdf)

### AI ガバナンスと操舵装置

- [NIST AI Risk Management Framework (incl. GenAI Profile)](https://www.nist.gov/itl/ai-risk-management-framework)
- [Anthropic, Responsible Scaling Policy v3](https://www.anthropic.com/news/responsible-scaling-policy-v3)
- [Anthropic, Collective Constitutional AI (2023)](https://www.anthropic.com/news/collective-constitutional-ai-aligning-a-language-model-with-public-input)
- [OpenAI, Evals guide](https://developers.openai.com/api/docs/guides/evals)
- [InstructGPT 論文 (Ouyang et al., 2022)](https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)
- [UK CMA, Cloud services market investigation — summary of final decision (2025)](https://assets.publishing.service.gov.uk/media/688b20e6ff8c05468cb7b120/summary_of_final_decision.pdf)
- [IEA, Energy and AI (2025)](https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai)
- [OECD, A blueprint for building national compute capacity for AI (2023)](https://www.oecd.org/en/publications/a-blueprint-for-building-national-compute-capacity-for-artificial-intelligence_876367e3-en.html)
- [Apple, Private Cloud Compute (2024)](https://security.apple.com/blog/private-cloud-compute/)

### 修理・保守・撤退

- [EU Directive on the right to repair (Directive (EU) 2024/1799)](https://commission.europa.eu/law/law-topic/consumer-protection-law/directive-repair-goods_en)

## 関連 Wiki / 関連記事

- [テクニウム (technium) — Wiki](/blogs/wiki/concepts/technium/) — 本概念のソース批判対象。aliases に「操舵可能な技術生態系」を含む
- [テクニウム概念への批判と超克 ── ケヴィン・ケリーから「操舵可能な技術生態系」へ](/blogs/posts/2026/05/technium-critique-and-transcendence/) — 前稿、批判の理論的整理
- [ヌースフィアとオメガ点 (テイヤール・ド・シャルダン)](/blogs/wiki/concepts/noosphere-omega-point/) — 「複雑性上昇」系譜の宗教的原型
- [雑種文化論 (加藤周一)](/blogs/wiki/concepts/kato-shuichi-hybridity/) — カリフォルニアン・イデオロギーの雑種性を方法論的に対比できる
- [AI エージェント (Wiki)](/blogs/wiki/concepts/ai-agent/) — STE における「制度化された自律性」の現代的具体例
- [自己改善型エージェント (Wiki)](/blogs/wiki/concepts/self-improving-agents/) — selection environment 内部に置き直すべき対象
- [MCP (Model Context Protocol)](/blogs/wiki/concepts/mcp/) — 統治された自律性の標準化されたインターフェース
