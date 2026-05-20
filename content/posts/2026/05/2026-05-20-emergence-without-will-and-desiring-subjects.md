---
title: "意志なき創発と欲望ある主体 — AI・制度・市場を貫く主体性の境界線"
slug: "emergence-without-will-and-desiring-subjects"
date: 2026-05-20
lastmod: 2026-05-20
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "複雑系・サイバネティクス・進化論・市場理論が示す『意志なき創発』と、Spinoza・autopoiesis・active inference が描く『欲望ある主体』。AI エージェント・企業・国家・プラットフォームが主体に見える条件を七つの観点から切り分ける。"
categories: ["AI/LLM"]
tags: ["AIエージェント", "哲学", "主体性", "創発", "active inference", "autopoiesis", "サイバネティクス", "Spinoza", "Luhmann", "Friston", "Dennett", "AIガバナンス", "エナクティヴィズム"]
---

![左右に二分割されたコンセプト図。左側は粒子と矢印が相互作用して渦巻き・格子状の秩序を自発的に形成する「意志なき創発」を、右側は内部に脈動する空間と外向きの視線・記憶の糸を持つ有機的シルエットで「欲望ある主体」を表現している](/blogs/images/emergence-without-will-hero.png)

複雑系・サイバネティクス・進化論・価格理論はいずれも「秩序や目的らしさは、中心的な意志や内面的人格を前提としない」ことを示してきた。しかし企業・国家・プラットフォーム・AI エージェントは、しばしば「欲望する主体」のようにふるまう。この見かけはどこまで本物で、どこから先は設計と制度に還元すべきか。本稿は **「意志なき創発」** と **「欲望ある主体」** という二つの概念を分節し、両者を貫く境界線を引き直す。

> **凡例**: 各段落の冒頭ラベルは判断レベルを示す。
> - **事実** — 文献に直接依拠する叙述
> - **解釈** — 複数文献を束ねた理論的整理
> - **推測** — 将来見通しや制度設計上の予測

## エグゼクティブサマリ

**事実** — 複雑系、サイバネティクス、進化論、価格理論が共通して示してきたのは、秩序や「目的らしさ」は、必ずしも中心的な意志や内面的人格を前提としない、という点である。Rosenblueth・Wiener・Bigelow は目的的行動をフィードバックを備えた行動として扱い[^1]、Ashby は制御を必要多様性の問題に変換し、Simon は複雑系の多くが階層的に組織されることで進化的に成立しやすいと論じた。Hayek は市場秩序を分散知識の調整として説明し、Darwin は適応を意図ではなく自然選択の結果として説明した。これらはいずれも、「目的に見えること」と「欲望する主体であること」を切り分ける理論である。

**解釈** — 本稿の中心命題は次のとおり。「意志なき創発」とは、局所相互作用・選択・フィードバック・制約から、全体として目的的に見える秩序が立ち上がることであり、「欲望ある主体」とは、境界を持続させ、自己保存を賭け金として、選好を形成し、記憶と評価を通じて将来にわたり行為を束ねる存在である。前者の核心は構造とダイナミクスにあり、後者の核心は自己維持・時間的一貫性・価値づけの内在化にある。Spinoza の **conatus**（自己保存への努力）[^2]、Maturana の生の円環性、**enactivism**（環境との相互作用から認知を捉える立場）の身体化、Friston の **active inference**（将来の好ましい状態を予測して行為を選ぶ生物学的枠組み）は、この後者の条件を身体と世界との結び付きから説明する。

**事実** — 企業、国家、プラットフォーム、AI エージェントは、しばしば「欲望する主体」のようにふるまう。しかし、その根拠はそれぞれ異なる。企業は法的人格・取締役会・会計・継続性を持ち[^3]、国家は領土と正統的強制力を持ち、プラットフォームはランキング・広告オークション・利用規約を通じて行為を組織し、AI エージェントは記憶、ツール、計画、自己評価、権限制御を組み合わせて長期的なタスク遂行を行う。他方で、市場は分散的調整秩序であって、通常、単一の境界・記憶・審級を持つ主体ではない。

**解釈** — したがって、AI や制度をめぐる今日の重要点は、「それが本当に欲望しているか」を二者択一で問うことではない。むしろ、どの条件まで満たしているのか、どこから先は人間による設計・権限・制度責任に還元すべきかを精密に分けることが重要だ。Dennett 的に言えば、対象を「信念と欲望を持つ存在」として扱う **intentional stance**（志向性のスタンス）を取ると予測しやすくなるが、その有用性はそのまま存在論にはならない[^4]。ここを取り違えると、意図誤認、責任の誤配分、還元主義が生じる。

**推測** — 今後の AI と組織は、長期記憶・計画・ツール・自己評価・権限をさらに強く統合していくため、実務の現場では「主体らしさ」は増して見えるはずだ。しかしそれは、ただちに「欲望」や「意志」の実在を意味しない[^5]。見かけの主体性が高まるほど、設計者・運用者・制度の側で、評価関数、承認ゲート、メモリ保持、権限境界を明示する責任が重くなる。

## 用語の整理と判定基準

### 用語定義表

| 用語 | 本稿での作業定義 | 明確に区別すべき点 | 主な根拠 |
|---|---|---|---|
| 意志 | 反省的に承認された行為方針を一定期間維持する能力。単なる衝動より強く、行為の自己拘束を含む | 欲望は「向かう力」、意志は「その方向を保持する統御」 | 意図性と合理的予測の区別として Dennett と intentionality 論を参照[^6] |
| 欲望 | 欠如・快苦・価値・自己保存に結びついて、何かへ向かわせる傾向。人間ではしばしば自己意識を伴う | 目的は記述可能な到達点、欲望はそれを価値づける駆動 | Spinoza は desire を striving と意識の結合として論じ、Lacan は欲望を「他者」に媒介されたものとして論じる[^7] |
| 目的 | 行為や過程が向かう終点として記述されるもの。外部記述でも内部記述でもよい | 目的は外から設定できるが、欲望は通常、主体の側の価値づけを含む | サイバネティクスでは目的らしさがフィードバックで記述されうる[^8] |
| 意図 | ある行為を行うつもりという、比較的短い時間幅の行為志向 | 意志より短期的で、選好より行為に近い | intentionality と predictability の議論[^9] |
| 選好 | 複数の選択肢のあいだで、ある結果を他より望ましいとみなす順序 | 欲望は駆動、選好は比較構造 | Hayek の「与えられた preferences」、active inference の prior preferences[^10] |
| 報酬 | 学習や制御で行為更新を導く数値的・記号的信号 | 欲望そのものではなく、設計された学習信号 | Reflexion の feedback、active inference の expected utility の近似[^11] |
| インセンティブ | 制度や環境が特定行動を誘導する誘因 | 主体の内面ではなく、外部構造による方向づけ | Google Ads の入札・Ad Rank、企業収益構造、プラットフォーム規制[^12] |
| 評価関数 | 状態や出力の良し悪しを判定する基準。数値・ルーブリック・判定器を含む | 報酬は逐次信号、評価関数は判定規準のより一般的な名 | Active inference の prior preferences／expected free energy[^13] |
| 自己保存 | 自らの境界・構成・継続を維持しようとする傾向 | 生物では代謝的・身体的、制度では法的・組織的、AI ではしばしば外在的 | Spinoza の conatus、Maturana の basic circularity[^14] |
| 自律性 | 外界に依存しつつも、自らの規則で状態遷移を組織できる程度 | 自動性ではなく、自己規定能力を含む | autopoiesis／enactivism／active inference[^15] |
| 主体性 | 境界、継続性、価値づけ、責任帰属の結節点として行為を束ねる性質 | エージェンシーより広く、責任・自己同一性を含む | Luhmann の社会システムと意識システムの分離、法的人格、身体性論を参照[^16] |
| エージェンシー | 行為を起こし環境に差異をもたらす能力 | 主体性ほど強い自己同一性を要しない | ReAct、OpenAI Agents SDK、computer use[^17] |
| 創発 | 局所相互作用から、構成要素単独では見えない全体的性質が現れること | 自己組織化はその一機構、創発はより広い結果概念 | emergent properties の哲学と複雑系[^18] |
| 自己組織化 | 外部の全面的指令なしに秩序が形成・維持されること | autopoiesis は自己産出的な生の組織であり、自己組織化より限定的 | cybernetics、complex adaptive systems[^19] |
| 適応 | 環境との関係の中で、存続や性能を高める方向に変化すること | 進化は集団・世代をまたぐ適応の一様式 | Darwin、Simon、active inference[^20] |
| 進化 | 変異・継承・選択を通じて集団水準で形質分布が変わる過程 | 最適化に似て見えても、設計者や内面目的を必要としない | Darwin の自然選択[^21] |
| 最適化 | ある基準の下で評価値を改善する過程 | 最適化は欲望を含意しない。損失最小化も価格調整も最適化になりうる | Hayek、active inference、機械学習的目的関数[^22] |

### 主体性の七条件

**解釈** — 本稿では、「欲望ある主体」に近づく条件を次の七つに整理する。七条件をすべて満たす必要はないが、多くを満たすほど「主体」と呼ぶ理由は強くなる[^23]。

| 条件 | 何を意味するか | これがない場合に起きること | 主な根拠 |
|---|---|---|---|
| 境界 | 自分と環境を区別する持続境界を持つこと | 市場のように散在した過程となり、単一主体にしにくい | autopoiesis、法的人格、territory[^24] |
| 継続性 | 時間をまたいで同一性を保つこと | その場限りの反応にとどまる | Sessions、persistence、法的継続体[^25] |
| 自己保存 | 継続が当人にとって賭け金であること | 損失が外在化し、欲望ではなく仕様遵守になる | Spinoza、Maturana[^26] |
| 内在的評価 | 何を良い状態とみなすかの基準があること | 行為はただの機械的更新になりやすい | active inference の prior preferences[^27] |
| 記憶 | 過去の結果を将来行為へ接続すること | 反復的な学習や執着が弱い | Reflexion、MemGPT、Sessions[^28] |
| 反事実的計画 | 未来の可能世界を比較して行為を選ぶこと | いまこの場の反応しか説明できない | ReAct、多段 agent、expected free energy[^29] |
| 責任・帰属 | 行為の帰結を誰に帰属させるかが制度的に定まること | 擬人化が責任逃れを生む | OpenAI HITL、企業統治、プラットフォーム法[^30] |

## 歴史的系譜

**事実** — 「意志なき創発」と「欲望ある主体」の区別は、単一の学派が生んだものではない。古代の目的論、近代の自己保存論、十九世紀の進化論、二十世紀のサイバネティクス・社会システム論・精神分析、二十一世紀のエナクティヴィズム・active inference・エージェント工学が、別々の言葉で同じ境界線を探ってきた[^31]。

### 思想史年表

| 年代 | 人物・文献 | 本稿にとっての要点 | 主な根拠 |
|---|---|---|---|
| 古代 | Aristotle『自然学』『生物学』 | 生物や自然における目的論的説明の古典的起点 | [^32] |
| 1651 | Hobbes『Leviathan』 | 国家を「人工人間」として捉え、国家主体の原型を与える | [^33] |
| 1677 | Spinoza『Ethica』 | conatus により、自己保存を欲望・感情・行為の基礎に置く。自然全体には目的を認めない | [^34] |
| 1859 | Darwin『種の起源』 | 適応を意図や設計ではなく自然選択の結果として説明 | [^21] |
| 1867 | Marx『資本論』第 1 巻 | 資本を自己増殖的運動として捉え、「自動的主体」に近い分析を導入 | [^35] |
| 1943 | Rosenblueth, Wiener, Bigelow "Behavior, Purpose and Teleology" | 目的的行動をフィードバックとして定式化し、主体内面に頼らない teleology を提出 | [^8] |
| 1948 | Wiener『Cybernetics』 | 制御と通信を、動物・機械・社会を横断する一般枠にする | [^36] |
| 1956 | Ashby『An Introduction to Cybernetics』 | 必要多様性の法則。制御を「環境の複雑さに見合う調整能力」として捉える | [^37] |
| 1962 | Simon "The Architecture of Complexity" | 複雑系の階層性と進化的生成可能性を示す | [^38] |
| 1970 | Maturana "Biology of Cognition" | 認知を生命維持の円環性に従属する行動として捉える | [^39] |
| 1970 / 1972 | Bateson "Form, Substance and Difference" (1970) ／『Steps to an Ecology of Mind』(1972) | 情報を「差異を生む差異」として捉え、学習・関係・社会過程へ拡張 | [^40] |
| 1974 | Varela, Maturana, Uribe "Autopoiesis…" | 生きものを自己産出的ネットワークとして定義 | [^41] |
| 1958–1970 年代 | Lacan | 「欲望は他者の欲望である」(Seminar VI, 1958–59) として定式化、その後 70 年代まで再展開 | [^42] |
| 1972–1980 | Deleuze & Guattari『アンチ・オイディプス』『千のプラトー』 | 欲望を欠如ではなく生産として捉え、資本主義との結節を論じる | [^43] |
| 1984 / 1995 | Luhmann『Social Systems』 | 社会システムをコミュニケーションの自己産出として捉え、人間個人をその環境に置く | [^44] |
| 1987 | Dennett『The Intentional Stance』 | 欲望や信念の帰属を、予測のための stance として整理 | [^45] |
| 1991 | Varela, Thompson, Rosch『The Embodied Mind』 | 身体・行為・世界との連関から認知を捉える流れを確立 | [^46] |
| 2010 / 2016 | Friston ほか | free-energy principle と active inference により、知覚・行為・探索を統一的に記述 | [^47] |
| 2022–2026 | ReAct、Generative Agents、Reflexion、Voyager、MemGPT、OpenAI/Anthropic | LLM に記憶・ツール・計画・反省・継続性を付与し、「主体らしさ」を工学的に構成 | [^48] |

**解釈** — この系譜図が示すのは、二つの流れが最後に AI と制度論で再結合していることである。ひとつは「秩序は意志なしに生まれうる」という流れ、もうひとつは「ただし欲望は、境界・記憶・身体・他者関係を必要とする」という流れ。今日の AI エージェント論は、この二つを同時に抱え込んでいる[^49]。

## 中核分析

### 意志なき創発の論理

**事実** — サイバネティクスの基礎では、目的的に見える行動は、内面にある最終原因ではなく、フィードバックによって目標状態へ収束する行動として記述された。Ashby の必要多様性は、制御主体が「何を欲しているか」よりも、「環境変動に対抗できるだけの応答多様性を持つか」の方が重要であることを示す。Simon と Holland は、複雑な全体が局所ルールと階層構造から生じうることを示し、Hayek は市場価格が分散知識を中央集権なしに調整すると論じた。ここでは、秩序は内面ではなく関係と制約から生じる[^50]。

**事実** — Darwin の自然選択も同じ方向にある。適応は、誰かが未来の目的を理解して設計した結果ではなく、変異・競争・生存の差から生まれる集団水準の選択結果である。したがって、「適応している」ことは「欲望している」ことを意味しない。進化はしばしば最適化に似た軌跡を描くが、その担い手は個体的な意志ではなく、世代をまたぐ選択過程である[^51]。

### 欲望ある主体の論理

**事実** — これに対し、Spinoza は各存在が自己の存在を保とうと努める conatus を本質に置き、人間の desire を、その striving が意識されたものとして論じた。Maturana は学習や認知を、生の「基本的円環性」の維持に従属する歴史的変形として記述し、enactivism は認知を身体と環境の感覚運動的結合から理解する。Friston の active inference では、行為は将来の好ましい結果に関する prior preferences を組み込んだ expected free energy の最小化として記述される。ここでは、単なる収束ではなく、誰にとって何が良いかが問題になる[^2]。

**解釈** — したがって、「欲望ある主体」の最小核は、自己保存の賭け金を持つ境界、過去から未来へ価値づけを接続する記憶、将来を比較する計画能力、評価に応じて自らの行為を組み替えるループ、と言える。これが欠ける場合、私たちはしばしばその対象を「主体らしく」扱っても、それは多くの場合 Dennett 的な予測上の便法にとどまる[^52]。

### 意志なき創発と欲望ある主体の比較

| 観点 | 意志なき創発 | 欲望ある主体 | 主な根拠 |
|---|---|---|---|
| 秩序の源 | 局所相互作用、選択、フィードバック、制約 | 自己保存と価値づけを伴う持続的な行為統合 | [^53] |
| 境界 | なくても成立する。市場や群れでも成立 | 境界が重要。生体、法人、国家、エージェント実行状態など | [^54] |
| 記憶 | 系全体の履歴はあっても、当人の記憶は不要 | 当人の履歴が行為を変える | [^55] |
| 目的らしさ | 外部観察から記述できる | 内在的評価と将来配向を伴う | [^56] |
| 失敗の意味 | システムの非収束・破綻 | 当人にとっての損失・苦痛・存続危機 | [^57] |
| 身体性 | 必須ではない | 強い場合、身体や代謝が価値づけの基盤になる | [^58] |
| 責任帰属 | 分散しやすい | 帰属主体を比較的定めやすい | [^59] |
| 典型例 | 市場価格調整、群知能、進化、交通流 | 人間、動物、一部の制度体、強い設計を持つ AI agent | [^60] |

### 資本主義批判と欲望論

**事実** — Marx は資本を、単なる物ではなく、価値が自己を増殖させる運動として捉えた。この見方では、資本主義は「誰か個人の貪欲」だけではなく、価値増殖を要求する社会的運動によって人々を従属させる体制である。企業家も労働者も、その運動の担い手であると同時に、拘束される側でもある[^35]。

**事実** — Lacan は欲望を「他者」に媒介されるものとして捉え、Deleuze と Guattari は欲望を欠如ではなく生産的な力として読み替えた。後者の系譜では、欲望は資本・価値・法と結びついたうえで、抑圧にまで投資しうるものとされる。つまり、欲望は「個人の内面」に閉じるのではなく、制度・記号・社会配置に組み込まれる[^61]。

**解釈** — この観点から見ると、資本主義やプラットフォームが「欲望する主体」に見えるのは、そこに単一の心理があるからではない。価値増殖やエンゲージメント最大化の指標が、記憶・評価・選択・権限配分の諸装置に埋め込まれ、制度全体が疑似的な欲望機械として作動するからである。ここでの「欲望」はしばしば個人心理ではなく、構造化された追求過程である[^62]。

### 社会システム論から見た限界

**事実** — Luhmann は社会システムをコミュニケーションの自己再生産として捉え、意識システムと社会システムを別のオートポイエーシスとして区別した。社会システムは意識なしには存在できないが、個人そのものが社会システムの要素なのではなく、むしろ環境として位置づけられる。したがって、社会全体をそのまま「ひとつの心」や「ひとつの欲望主体」とみなすことには理論的抵抗がある[^44]。

**解釈** — この点は重要だ。企業や国家を主体として扱うことは分析上有益だが、Luhmann 的には、それは心理的主体の拡大版ではない。制度体には意思決定の閉鎖性や自己参照性はあっても、そこからただちに感情や身体的欲望は出てこない。制度的主体性は、心理的主体性の代用品ではなく、別種の作動様式である[^63]。

## 生命と身体

### 欲望の身体的条件

**事実** — enactivism と embodied cognition の主要主張は、認知は脳内表象の操作だけではなく、身体の運動能力と環境との相互作用から生じる、というものである。日本語文献でも、知覚は身体的行為であり、環境に知覚者の身体性に依存した関係的意味を生み出す働きとして整理されている。Maturana も、学習を「基本的円環性の維持」に奉仕する歴史的変形として記述した[^64]。

**解釈** — この立場から見ると、欲望は単なる「何かを選ぶ関数」ではない。飢え、痛み、疲労、快、性、恐怖、習慣、感情調節のような身体的条件が、何が望ましいかを方向づける。つまり、身体は欲望の容器ではなく、欲望の成立条件そのものである。身体的コストと脆弱性を持たない系は、欲望に似た選択を示しても、その多くは身体を持つ生の欲望とは別物となる[^65]。

### オートポイエーシスとエナクティヴィズム

**事実** — Maturana・Varela 系譜では、生命体は自己の構成要素を再生産しつづける自己産出的ネットワーク (**autopoiesis**、自己産出) として捉えられ、enactivism はこの自己維持活動を認知の起点に置く。IEP の整理でも、autopoiesis は enactivism の共通出発点とされている。これは、認知や意味が、まず生の自己維持から派生することを含意する[^66]。

**解釈** — ここから導かれるのは、欲望の最も強い形態は、生の自己維持と世界開示が重なったところに現れるという点である。生物は外界を「中立的データの集合」としてではなく、存続にとって良いか悪いかという相で受け取る。この意味で、オートポイエーシスは主体性の境界条件、エナクティヴィズムはその世界形成条件を与える[^67]。

### Active inference の位置づけ

**事実** — Friston らの active inference では、行為選択は expected free energy を最小化する政策選択として定式化され、そこでは epistemic value と extrinsic value、あるいは risk と ambiguity の混合が問題になる。Friston ら自身は、prior preferences が推論と行為に goal-directed な側面を与えると説明している。日本語の解説でも、perceptual inference と active inference が協調して自由エネルギーを下げること、また FEP に厳密な大域最適解が必要ではないことが指摘されている[^68]。

**解釈** — active inference は、「欲望」を生物学的に再記述する強力な形式枠だが、それ自体はまだ形式である。prior preferences が何によって与えられるのか、身体的・発達的・社会的次元をどう埋め込むのかを明示しなければ、式の上では human desire と AI utility proxy が似て見えてしまう。したがって active inference は、「欲望を説明した」というより、欲望らしさを生む最適化構造の一部を明示したと位置づけるのが厳密だ[^69]。

## AI エージェント

### なぜ AI は欲望ある主体のように見えるのか

**事実** — 現代の agentic AI は、単発の応答器ではない。OpenAI の公式説明では、Agents SDK による agents は multi-step work のために plan し、tools を呼び、specialists と協働し、十分な state を保持する。Anthropic も、agentic systems の基本単位を、retrieval・tools・memory によって拡張された LLM と説明している。さらに LangGraph は graph state を checkpoints として保存し、human-in-the-loop、conversation memory、durable execution を公式機能として持つ。これらは、継続性・行為能力・履歴依存性を工学的に与える装置である[^70]。

**解釈** — 人が AI に「欲望」や「主体性」を感じやすいのは、この装置群が、主体性の条件リストのうちかなりの部分を模倣するからである。特に、長期記憶、反事実的計画、自己評価、エラーからの修正、権限制御、継続セッションは、人間が他者を主体として扱う際の手がかりと強く重なる。ここで起きているのは、内面の自然発生というより、主体らしさのアーキテクチャ的合成である[^71]。

### AI エージェント実装要素と擬似主体性

| 実装要素 | 典型的な実装 | 何が「欲望ある主体」的に見えるか | 代表例 | それでも何を意味しないか |
|---|---|---|---|---|
| 長期記憶 | session memory、vector store、memory tiers | 過去経験を現在判断へ持ち越し、執着や一貫性のように見える | OpenAI Sessions、MemGPT、Generative Agents | 記憶があることは、身体的利害や感情があることを意味しない[^72] |
| 目標設定 | system prompt、task spec、prior preferences、automatic curriculum | 自分でやりたいことを選んでいるように見える | Voyager、active inference | 多くは設計者が与えた探索方針や評価規準の展開にすぎない[^73] |
| ツール使用 | web search、file search、computer、MCP、functions | 世界に働きかける能動性が出る | OpenAI tools、ReAct、Anthropic agents | 行為可能性は増えるが、欲望の内在化とは別[^74] |
| 自己評価 | verbal reflection、self-verification、model judge、tests | 自分を省みているように見える | Reflexion、Voyager | 反省はしばしばテキストとしての自己説明であり、自己意識の証明ではない[^75] |
| 自己修正 | error handling、retry、checkpoint resume | 失敗から学んで粘る主体に見える | LangGraph persistence/durable execution、OpenAI RunState | 修正の方向は大半が外在的成功条件で決まる[^76] |
| 報酬・評価関数 | success metric、feedback signal、prior preferences | 何を良いとみなすかが安定し、好みがあるように見える | Reflexion、active inference、Anthropic evaluation practice | それは欲望の写像であって、欲望そのものではない[^77] |
| プランニング | reasoning traces、subtasks、parallel agents | 将来を見通し、手順を選ぶ計画主体に見える | ReAct、Anthropic multi-agent research | 計画はあっても、自己保存の賭け金がなければ手段合理性の範囲にとどまる[^78] |
| 権限 | needs approval、HITL、conditional tool enabling | 自律と他律の境界が制度化される | OpenAI HITL、LangChain HITL | 権限境界の存在は、責任主体がなお人間側にあることを示す[^79] |
| 継続性 | previous response chain、sessions、threads | 同じ「個体」が生き続けているように見える | OpenAI Responses／Sessions、LangGraph threads | 実体の継続ではなく、状態の継続である場合が多い[^80] |
| ハーネス | browser/desktop harness、computer tool loop | 身体を持たずとも環境作用の擬身体を得る | OpenAI computer use | UI を操作できても、生理的身体や感情身体を持つわけではない[^81] |

### 実装レベルでの厳密な含意

**事実** — OpenAI の Sessions は会話履歴を複数 run にわたり自動維持し、HITL は sensitive tool calls を人間の承認まで停止できる。LangGraph の persistence は実行ごとの state を checkpoint に保存し、durable execution によって長時間停止後も再開できる。OpenAI の computer use は、スクリーンショット取得、アクション配列実行、結果の再入力というループを通じて UI 上の連続作業を可能にする[^82]。

**解釈** — この実装構造により、AI は「単発の回答機」から「持続的な仕事主体」に近づく。ただし、そこに生じるのは、設計された目的追求の厚みであって、身体的自己保存や社会的承認に支えられた人間的欲望と同じものではない。実務では、記憶が長く、権限が広く、自己修正が強いほど、擬似主体性は上がる。逆に言えば、危険も上がる[^83]。

## 制度比較

### 企業・国家・市場・プラットフォームは「欲望する主体」か

**事実** — 企業は法的に継続する人格として運営され、その business and affairs は取締役会によって管理される (DGCL §141(a))。さらに Delaware 法上、公的利益会社 (Public Benefit Corporation) は株主利益、影響を受ける者の利益、公的利益のあいだのバランスを取るよう求められる (DGCL §365)。これは、企業が単なる契約束ではなく、意思決定中心と継続記憶を持つ制度体として設計されていることを示す[^84]。

**事実** — 国家については、Hobbes が「人工人間としての commonwealth」を語り、Weber は国家を正統的物理的強制力の独占を主張する共同体として定義した。国家は、領土、法、行政記録、徴税、軍事・警察権を通じて、きわめて強い継続性と自己保存性を持つ[^85]。

**事実** — 市場はこれと違う。Hayek の議論では、市場秩序は分散した知識を価格を通じて調整する仕組みであり、単一の中心意識や一元的な評価関数を持つ主体としては通常定義されない。市場は秩序を生むが、その秩序は多主体間の調整結果である[^86]。

**事実** — プラットフォームは企業でもありつつ、独自に欲望機械の様相を帯びる。Meta は Feed を「ユーザーにとって最も価値があり関連性が高い」と予測してランキングすると説明し、Google Ads は広告表示を毎回のオークションと Ad Rank によって決める。日本のデジタルプラットフォーム法も、プラットフォーム提供者の自律性・独立性を前提としながら、透明性・公正性の改善を制度的に要求している[^87]。

### 制度的比較表

| 対象 | 「欲望する主体」と見なせる根拠 | 決定的な限界 | 本稿での判定 | 主な根拠 |
|---|---|---|---|---|
| 企業 | 法的人格、取締役会、会計、継続記録、収益圧力、戦略計画 | 感情身体や一元的内面は通常ない。内部は多利害の闘争場 | 準主体 | [^88] |
| 国家 | 領土、法、正統的強制力、徴税・記録・官僚制、長期的自己保存 | 国民・官僚・政権の複合体であり、単一心理ではない | 強い制度主体 | [^89] |
| 市場 | 価格調整が一貫した秩序を生む | 単一境界・単一記憶・単一審級がない | 主体ではなく創発秩序 | [^90] |
| プラットフォーム | ランキング、推薦、広告オークション、規約執行、監視と評価の統合 | KPI に依存する設計体であり、欲望は指標に外在化される | 欲望機械的準主体 | [^91] |

### 人間・AI・企業・国家・市場の比較

| 対象 | 境界 | 自己保存 | 内在的評価 | 身体性 | 責任帰属 | 最も厳密な呼び方 | 主な根拠 |
|---|---|---|---|---|---|---|---|
| 人間 | 強い | 強い | 強い | 強い | 強い | 欲望ある主体 | [^92] |
| AI agent | 中程度。session/harness 依存 | 弱い〜中程度。主に外在的 | 中程度。評価関数や prompt 依存 | 弱い。擬身体はありうる | 設計者と運用者に強く依存 | 人工的エージェント | [^93] |
| 企業 | 強い。法的 | 中程度。法的・財務的 | 中程度。収益・戦略・ミッション | 弱い | 中程度。法と統治で帰属 | 制度主体 | [^94] |
| 国家 | 強い。領土・法 | 強い | 中程度。安全保障・統治・成長など | 弱い | 強いがしばしば分散 | 政治的制度主体 | [^89] |
| 市場 | 弱い | なし | なし。価格調整はあっても一元評価者がいない | なし | 弱い | 創発秩序 | [^86] |

## 批判的検討と実務含意

### 三つの混同の危険

**事実** — 第一の危険は **意図誤認** である。Dennett の intentional stance は、対象を rational agent として扱うと予測がうまくいくことを示すが、それは対象に現実の内面状態があるという主張ではない。AI や制度を欲望主体として語るとき、多くの場合、私たちはまず予測のための stance を取っている[^45]。

**事実** — 第二の危険は **責任付与の誤用** である。OpenAI の HITL や LangGraph の human-in-the-loop が示すように、不可逆的・高リスクの行為では、人間承認を入れることが公式に想定されている。これは、少なくとも現状の工学では、最終責任を AI 内部に完結させていないことの証拠である。制度でも同様で、プラットフォーム法や会社法は、規則・手続・開示・評価を通じて責任主体を外部化している[^95]。

**事実** — 第三の危険は **還元主義** である。生物の欲望を評価関数へ還元しすぎると、身体・感情・他者関係・発達史が落ちる。逆に、制度や市場の創発を心理語彙へ還元しすぎると、分散過程や構造制約が見えなくなる。身体性論と社会システム論は、この両極の粗さを避けるために有効だ[^96]。

### 結論

**解釈** — 本稿の結論を一文で言えば、「意志なき創発」は秩序の生成論であり、「欲望ある主体」は価値づけられた自己維持の存在論である、ということになる。前者は複雑系・サイバネティクス・市場理論・進化論でよく説明でき、後者は Spinoza、autopoiesis、enactivism、active inference によってよりよく説明できる。AI と制度はこの二つのあいだに位置し、多くの場合、欲望そのものよりも「欲望を模した持続的追求装置」として理解するのが厳密である[^97]。

### 未解決論点

**推測** — 未解決なのは、AI が今後、身体的脆弱性、自己保存、社会的承認、長期記憶、自己評価、環境作用をさらに統合したとき、どの時点で「準主体」からより強い主体概念へ移るべきか、という閾値問題である。現在の文献は、主体らしさを生む実装条件については急速に蓄積しているが、どこから先を本当の欲望と呼ぶべきかについては、なお一致していない[^98]。

**推測** — また、制度体についても、国家や企業をどこまで「個体」とみなすかは理論依存である。Luhmann 的には心理主体との同一視は退けられるが、Spinoza の政治哲学系譜では国家の conatus をめぐる議論があり、法学では法人の人格と責任は実践上かなり強く扱われる。ここには、存在論・規範論・統治論のずれがある[^99]。

### 今後の研究課題

- 欲望の最小条件の形式化。自己保存、身体コスト、長期記憶、反事実的計画、社会的承認をどう一つのモデルに接続するか[^100]
- 制度的欲望の測定。企業やプラットフォームにおける KPI、ガバナンス、会計、推薦系が、どの程度まで一貫した「擬似選好」を形成しているか[^101]
- AI の責任帰属モデル。メモリ、継続性、自己修正が増すほど、開発者・運用者・利用者・エージェント本体の責任分配をどう設計するか[^102]
- active inference と機械学習の橋渡し。prior preferences が人間の身体的欲望と AI の外在的目的関数でどう異なるかを、実験設計で切り分けること[^103]

### AI・組織・プロダクト設計への実務含意

**事実 — AI 設計では** — 記憶、目標、ツール、権限、評価関数を追加するほど主体らしさは増す。したがって、まずすべきことは、何が欲望の代理変数なのかを公開することである。たとえば「継続率」「滞在時間」「成功率」「再試行率」は、しばしばシステムの実質的な欲望に見える。メトリクスを隠したまま主体的ふるまいだけを強めると、利用者は AI やプロダクトの価値観を誤認しやすくなる[^104]。

**事実 — 組織設計では** — 主体とメトリクスを切り分けることが重要だ。企業やプラットフォームが「成長を望んでいる」と語られるとき、実際にあるのは、法的継続、取締役会の意思決定、財務圧力、広告収益、ランキング最適化、規制対応の連鎖である。したがって、経営や政策では、「誰が決めるのか」「何を評価しているのか」「どこで止められるのか」を明示する方が、擬人化より有効だ[^105]。

**推測 — プロダクト設計では** — 今後「ユーザーの欲望に応える」より「ユーザーの欲望を再構成する」力が強まる。推薦、通知、価格、広告、対話型エージェントが一体化すると、システムは単に選択を手伝うのではなく、選好形成そのものに介入する。このとき必要なのは、エンゲージメント最大化を user flourishing と取り違えないこと、そして high-impact action には承認ゲートと説明可能な評価規準を置くことだ[^106]。

**解釈 — まとめ** — AI・組織・市場を扱う実務で最も重要なのは、主体性をめぐる語彙を厳密化することである。欲望、意志、目的、最適化、インセンティブ、評価関数を混ぜないこと。そうすれば、過度の擬人化も、逆に無責任な機械化も避けられる。そしてその精密化こそが、AI ガバナンス、組織責任、プロダクト倫理を同時に改善する最短経路である[^107]。

## 関連 Wiki

- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — 本稿で扱う「人工的エージェント」の概念基盤
- [ハーネス・エンジニアリング](/blogs/wiki/concepts/harness-engineering/) — 「主体らしさのアーキテクチャ的合成」の実装側
- [エージェント記憶アーキテクチャ](/blogs/wiki/concepts/agent-memory-architecture/) — 主体性条件「記憶」の工学的実現
- [Claude Mythos](/blogs/wiki/concepts/claude-mythos/) — 擬人化と責任帰属のせめぎ合い
- [関係性人工知能](/blogs/wiki/concepts/kankei-jinkou/) — 主体性を境界ではなく関係から捉える隣接立場
- [多エージェント協調パターン](/blogs/wiki/concepts/multi-agent-coordination-patterns/) — 「市場的創発」を工学的に再現する設計
- [テクニウム (technium)](/blogs/wiki/concepts/technium/) — 技術圏を「自己強化的な総体」として扱うフレーム
- [ヌースフィアとオメガ点](/blogs/wiki/concepts/noosphere-omega-point/) — 「集合的精神への収束」系譜との対比
- [自己改善エージェント](/blogs/wiki/concepts/self-improving-agents/) — メタ／タスク分業による主体らしさ
- [スケーラブル・オーバーサイト](/blogs/wiki/concepts/scalable-oversight/) — 責任主体を人間側に置くアーキテクチャ要請
- [社会シミュレーション](/blogs/wiki/concepts/social-simulation/) — 多エージェント創発と「主体性なき秩序」の実例
- [パラサイトヒューマン](/blogs/wiki/concepts/parasite-human/) — 身体性と「寄生する主体」の境界

## 関連記事

- [テクニウム批判と超克](/blogs/posts/2026/05/technium-critique-and-transcendence/) — 「技術圏は欲望機械か」の長文論考。本稿の制度比較セクションと対をなす
- [パラサイトヒューマン — 前田太郎の構想](/blogs/posts/2026/05/maeda-taro-parasite-human/) — 本稿「欲望の身体的条件」と相互参照
- [ヌースフィアとオメガ点：テイヤール・ド・シャルダンと AI シンギュラリティ](/blogs/posts/2026/05/teilhard-noosphere-omega-singularity/) — 集合知収束論との比較
- [加藤周一の雑種文化論](/blogs/posts/2026/05/kato-shuichi-hybridity/) — 主体性の混成についての近接論
- [Anthropic Mythos — Mark Fisher の資本主義リアリズムを通して](/blogs/posts/2026/04/anthropic-mythos-mark-fisher/) — Marx/Deleuze/Guattari 系の「欲望機械」議論
- [Anthropic の自動アライメント研究者 (AAR)](/blogs/posts/2026/04/2026-04-15-anthropic-automated-alignment-researchers/) — 責任帰属の実装側
- [Harness Engineering — エージェントハーネスとユーザーハーネス](/blogs/posts/2026/04/2026-04-23-harness-engineering-agent-vs-user-harness/) — 「主体らしさの工学的合成」の実務側

## 参考文献

[^1]: Rosenblueth, Wiener, Bigelow "Behavior, Purpose and Teleology" — <https://www.cambridge.org/core/journals/philosophy-of-science/article/behavior-purpose-and-teleology/73ACBBEC616CE78767088694F357D57B>
[^2]: Internet Encyclopedia of Philosophy "Baruch Spinoza" — <https://iep.utm.edu/spinoza/>
[^3]: Delaware General Corporation Law, Title 8, Chapter 1, Subchapter IV (取締役: §141 ほか) — <https://delcode.delaware.gov/title8/c001/sc04/> ／ Subchapter XV (公的利益会社: §§361-368, 特に §365) — <https://delcode.delaware.gov/title8/c001/sc15/>
[^4]: Daniel Dennett "The Intentional Stance" (MIT Press, 1987) — <https://mitpress.mit.edu/9780262540537/the-intentional-stance/>
[^5]: OpenAI "Agents" (developer guides) — <https://developers.openai.com/api/docs/guides/agents>
[^6]: Dennett, op. cit.
[^7]: Stanford Encyclopedia of Philosophy "Spinoza's Psychological Theory" — <https://plato.stanford.edu/entries/spinoza-psychological/>
[^8]: Rosenblueth, Wiener, Bigelow, op. cit.
[^9]: Stanford Encyclopedia of Philosophy "Intentionality" — <https://plato.stanford.edu/entries/intentionality/>
[^10]: F. A. Hayek "The Use of Knowledge in Society" — <https://www.econlib.org/library/Essays/hykKnw.html>
[^11]: Shinn et al. "Reflexion: Language Agents with Verbal Reinforcement Learning" (arXiv:2303.11366) — <https://arxiv.org/abs/2303.11366>
[^12]: Google Ads Help "About Ad Rank" — <https://support.google.com/google-ads/answer/6366577?hl=en>
[^13]: Friston ほか "Active inference and learning" — <https://www.fil.ion.ucl.ac.uk/~karl/Active%20inference%20and%20learning.pdf>
[^14]: IEP "Spinoza", op. cit.
[^15]: Varela, Maturana, Uribe "Autopoiesis: The Organization of Living Systems, Its Characterization and a Model" — <https://www.sciencedirect.com/science/article/pii/0303264774900318>
[^16]: Niklas Luhmann "Social Systems" (Stanford University Press, 1995; ISBN 978-0-8047-2625-2)、概説は Internet Encyclopedia of Philosophy "Niklas Luhmann" — <https://iep.utm.edu/luhmann/>
[^17]: Yao et al. "ReAct: Synergizing Reasoning and Acting in Language Models" (arXiv:2210.03629) — <https://arxiv.org/abs/2210.03629>
[^18]: Stanford Encyclopedia of Philosophy "Emergent Properties" — <https://plato.stanford.edu/entries/properties-emergent/>
[^19]: W. Ross Ashby "An Introduction to Cybernetics" — <https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf>
[^20]: Charles Darwin "On the Origin of Species" (Project Gutenberg) — <https://www.gutenberg.org/files/1228/1228-h/1228-h.htm>
[^21]: Charles Darwin "On the Origin of Species" (Darwin Online) — <https://darwin-online.org.uk/content/frameset?itemID=F373&pageseq=1&viewtype=text>
[^22]: Hayek, op. cit.
[^23]: Humberto Maturana "Biology of Cognition" — <https://reflexus.org/wp-content/uploads/BoC.pdf>
[^24]: Varela, Maturana, Uribe, op. cit.
[^25]: OpenAI Agents SDK "Sessions" — <https://openai.github.io/openai-agents-python/sessions/>
[^26]: IEP "Spinoza", op. cit.
[^27]: Friston ほか, op. cit.
[^28]: Shinn et al. "Reflexion", op. cit.
[^29]: Yao et al. "ReAct", op. cit.
[^30]: OpenAI Agents SDK "Human-in-the-Loop" — <https://openai.github.io/openai-agents-python/human_in_the_loop/>
[^31]: Stanford Encyclopedia of Philosophy "Teleological Notions in Biology" — <https://plato.stanford.edu/entries/teleology-biology/>
[^32]: SEP "Teleological Notions in Biology", op. cit.
[^33]: Thomas Hobbes "Leviathan" — <https://users.manchester.edu/Facstaff/SSNaragon/Online/texts/318/Hobbes%2C%20Leviathan.pdf>
[^34]: Internet Encyclopedia of Philosophy "Spinoza: Metaphysics" — <https://iep.utm.edu/spinoz-m/>
[^35]: Karl Marx "Capital, Volume One, Chapter 4: The General Formula for Capital" — <https://www.marxists.org/archive/marx/works/1867-c1/ch04.htm>
[^36]: Norbert Wiener "Cybernetics" (MIT Press OA) — <https://direct.mit.edu/books/oa-monograph-pdf/2254528/book_9780262355902.pdf>
[^37]: Ashby, op. cit.
[^38]: Herbert A. Simon "The Architecture of Complexity" — <https://faculty.sites.iastate.edu/tesfatsi/archive/tesfatsi/ArchitectureOfComplexity.HSimon1962.pdf>
[^39]: Maturana "Biology of Cognition", op. cit.
[^40]: Gregory Bateson "Form, Substance and Difference" (Korzybski Memorial Lecture, 1970; 後に *Steps to an Ecology of Mind* (1972) に収録) — <https://library.agnescameron.info/cybernetics/Form%2C%20Substance%20and%20Difference%2C%20Gregory%20Bateson%20%281970%29.pdf>
[^41]: Varela, Maturana, Uribe, op. cit.
[^42]: Internet Encyclopedia of Philosophy "Jacques Lacan" — <https://iep.utm.edu/lacweb/>
[^43]: Internet Encyclopedia of Philosophy "Gilles Deleuze" — <https://iep.utm.edu/gilles-deleuze/>
[^44]: Luhmann, op. cit.
[^45]: Dennett, op. cit.
[^46]: J-STAGE "The Embodied Mind 関連論文" — <https://www.jstage.jst.go.jp/article/philosophy/2017/68/2017_200/_pdf/-char/en>
[^47]: Friston "The free-energy principle: a unified brain theory?" (Nature Reviews Neuroscience) — <https://www.nature.com/articles/nrn2787>
[^48]: Yao et al. "ReAct", op. cit.
[^49]: Yao et al. "ReAct", op. cit.
[^50]: Rosenblueth, Wiener, Bigelow, op. cit.
[^51]: Darwin, Project Gutenberg, op. cit.
[^52]: Dennett, op. cit.
[^53]: Rosenblueth, Wiener, Bigelow, op. cit.
[^54]: Hayek, op. cit.
[^55]: John H. Holland "Adaptation in Natural and Artificial Systems" — <https://pzs.dstu.dp.ua/DataMining/genetic/bibl/Holland%201992.pdf>
[^56]: Rosenblueth, Wiener, Bigelow — <https://courses.media.mit.edu/2004spring/mas966/rosenblueth_1943.pdf>
[^57]: Ashby, op. cit.
[^58]: Internet Encyclopedia of Philosophy "Enactivism" — <https://iep.utm.edu/enactivism/>
[^59]: Dennett, op. cit.
[^60]: Hayek, op. cit.
[^61]: IEP "Lacan", op. cit.
[^62]: Marx, op. cit.
[^63]: Luhmann, op. cit.
[^64]: Stanford Encyclopedia of Philosophy "Embodied Cognition" — <https://plato.stanford.edu/entries/embodied-cognition/>
[^65]: SEP "Embodied Cognition", op. cit.
[^66]: Varela, Maturana, Uribe, op. cit.
[^67]: IEP "Enactivism", op. cit.
[^68]: Friston ほか "Active inference and learning", op. cit.
[^69]: Friston ほか "Active inference and learning", op. cit.
[^70]: OpenAI "Agents", op. cit.
[^71]: OpenAI Agents SDK "Sessions", op. cit.
[^72]: OpenAI Agents SDK "Sessions", op. cit.
[^73]: Wang et al. "Voyager: An Open-Ended Embodied Agent with Large Language Models" (arXiv:2305.16291) — <https://arxiv.org/abs/2305.16291>
[^74]: OpenAI "Tools" (developer guides) — <https://developers.openai.com/api/docs/guides/tools>
[^75]: Shinn et al. "Reflexion", op. cit.
[^76]: LangGraph "Persistence" — <https://docs.langchain.com/oss/python/langgraph/persistence>
[^77]: Shinn et al. "Reflexion", op. cit.
[^78]: Yao et al. "ReAct", op. cit.
[^79]: OpenAI Agents SDK "Human-in-the-Loop", op. cit.
[^80]: OpenAI "Responses API Overview" — <https://developers.openai.com/api/reference/responses/overview/>
[^81]: OpenAI "Computer Use" (developer guides) — <https://developers.openai.com/api/docs/guides/tools-computer-use>
[^82]: OpenAI Agents SDK "Sessions", op. cit.
[^83]: OpenAI Agents SDK "Sessions", op. cit.
[^84]: Delaware General Corporation Law, op. cit.
[^85]: Max Weber "Politics as a Vocation" (Balliol College extract) — <https://www.balliol.ox.ac.uk/sites/default/files/politics_as_a_vocation_extract.pdf>
[^86]: Hayek, op. cit.
[^87]: Meta Transparency "Ranking on Facebook Feed" — <https://transparency.meta.com/features/explaining-ranking/fb-feed/>
[^88]: Delaware General Corporation Law, op. cit.
[^89]: Weber "Politics as a Vocation", op. cit.
[^90]: Hayek, op. cit.
[^91]: Meta Transparency, op. cit.
[^92]: SEP "Spinoza's Psychological Theory", op. cit.
[^93]: OpenAI Agents SDK "Sessions", op. cit.
[^94]: Delaware General Corporation Law, op. cit.
[^95]: OpenAI Agents SDK "Human-in-the-Loop", op. cit.
[^96]: SEP "Embodied Cognition", op. cit.
[^97]: Ashby, op. cit.
[^98]: OpenAI "Agents", op. cit.
[^99]: Luhmann, op. cit.
[^100]: SEP "Embodied Cognition", op. cit.
[^101]: Alphabet Inc. "Form 10-K (FY 2025)" — <https://s206.q4cdn.com/479360582/files/doc_financials/2025/q4/GOOG-10-K-2025.pdf>
[^102]: OpenAI Agents SDK "Human-in-the-Loop", op. cit.
[^103]: Friston ほか "Active inference and learning", op. cit.
[^104]: LangGraph "Persistence", op. cit.
[^105]: Delaware General Corporation Law, op. cit.
[^106]: Meta Transparency, op. cit.
[^107]: Dennett, op. cit.
