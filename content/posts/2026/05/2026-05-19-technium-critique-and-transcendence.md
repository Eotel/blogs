---
title: "テクニウム概念への批判と超克 ── ケヴィン・ケリーから「操舵可能な技術生態系」へ"
slug: "technium-critique-and-transcendence"
date: 2026-05-19
lastmod: 2026-05-19
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "ケヴィン・ケリーの『テクニウム』概念を AI エージェント時代に再評価する。技術決定論・進歩史観・資本主義の自然化という三つの観点から批判し、思想史（テイヤール／マクルーハン／カリフォルニアン・イデオロギー）を踏まえて『操舵可能な技術生態系』へ再定義する。"
categories: ["AI/LLM"]
tags: ["技術哲学", "ケヴィン・ケリー", "テクニウム", "AI エージェント", "カリフォルニアン・イデオロギー", "技術決定論"]
---

## エグゼクティブサマリ

ケヴィン・ケリーの「テクニウム」(technium) は、個々の機械や発明ではなく、技術・制度・文化・ソフトウェア・法・知的生産物を含む地球規模の技術総体を指す概念である。ケリー自身は、これを「技術を自律的なシステムであるかのように見る」視角として提示しつつ、別の箇所ではテクニウムが「自らの衝動」に従う有機体のようなものへと成熟した、とまで述べる。このため、テクニウムは単なる比喩ではなく、しばしば準実在論的な語りへ滑っていく。ここに、この概念の魅力と危うさの両方が集中している。

結論を先に述べれば、テクニウムは **技術を生態系・複雑系・累積的ネットワークとして捉えるためのヒューリスティックとしては有効** だが、**技術の方向を決める政治経済的フィードバックを十分に理論化していないため、政治理論や規範理論としては不十分** である。Langdon Winner が古典的論文「Do Artifacts Have Politics?」で論じたように、人工物や技術システムは権力と権威を体現しうるし、技術史研究は技術を必要な運命ではなく分岐と選択の系列として理解してきた。Richard Barbrook と Andy Cameron が "The Californian Ideology" (1995) で批判したのも、まさにこの点 ── 自由市場・テクノロジー・カウンターカルチャーを混ぜた歴史観が、政治的選択を「自然化」してしまうことだった。

本稿の中心的な主張は次のとおりである。テクニウム概念の本質的弱点は、**技術を生命の延長として見ること自体** よりも、**どの制度・市場・国家・軍事・プラットフォーム・教育・身体実践が、どの技術を増殖させるのか** という選択環境を薄くしか描けないことにある。Shoshana Zuboff が「監視資本主義」を人間経験を原料化する経済秩序として定義したこと、DARPA が ARPANET の基礎を作り GPS が米軍開発から出発したことは、技術進化が「技術自身の欲望」だけでなく、国家・資本・安全保障・インフラ投資に深く方向づけられていることを示している。

AI エージェント時代は、テクニウムを古びさせるのではなく、別の仕方で切迫させる。OpenAI と Anthropic は現在、エージェントを「ループ」「ツール使用」「ハンドオフ」「ワークフロー／エージェント」のアーキテクチャとして定義し、Google DeepMind はコード生成エージェント、マルチエージェント研究支援系、ロボティクスへ展開している。AI はテクニウムの **自己記述・自己評価・自己改変に見える能力** を強めている。しかしその「自律性」は、実際には目的関数、評価器、ツール接続、標準プロトコル、計算資源、ガードレールによって条件づけられた **統治された自律性** である。AI が現実化しているのは「技術の欲望」そのものというより、**制度化された最適化の連鎖** である。

本稿の提案は、テクニウムを捨てることではなく、**「操舵可能な技術生態系」** へと再定義することだ。問うべきは「技術が何を欲するか」ではなく、「どのような選択環境のもとで、どの技術が増殖し、どの技術が衰退するのか」である。

## ケリーのテクニウム ── 何を含み、何を主張する概念か

ケリーの定義で決定的なのは、テクニウムが単なるハードウェア集合ではないことだ。彼は [*What Technology Wants*](https://www.upf.edu/documents/4185509/228936771/Kelly%2C%2BWhat%2BTechnology%2BWants.pdf/de4650a1-473f-e1cd-07c2-2c213d0740fd) (Viking, 2010) で、UNIX のコードを技術とみなすならハムレットも技術とみなしうると述べ、テクニウムを地球規模に相互接続された技術システムとして規定する。そこには文化、芸術、社会制度、知的創造物、ソフトウェア、法、哲学概念、さらには特許制度まで含まれる。つまりテクニウムは **人工物の総体** ではなく、**人工物を再生産し続ける条件の総体** である。ここにケリーの射程の広さがある。

テクニウム概念の核は、射程の広さだけではない。ケリーは [*Out of Control*](https://kk.org/books/out-of-control) (Addison-Wesley, 1994) の段階から、自己組織化・分散性・「ネオ生物学的世界」への関心を強く示しており、『The Inevitable』(Viking, 2016) では、今後三十年を形づくる力を「すでに動き出している技術的トレンド」として整理している。『What Technology Wants』では、テクノロジーを生命進化の延長、「第七の生命界」として描き、複雑性・多様性・美・自由・進化可能性の増大を技術の目的に列挙する。これは技術哲学であると同時に、かなり強い進歩史観でもある。

重要なのは、「技術が欲望を持つ」という言い方がケリーの内部でも揺れていることだ。ある箇所では、技術を自律的なシステムとして眺める方法論的視角 ── つまりメタファーとしての「あたかも」 ── として扱う一方、本文の別の箇所では、テクニウムは自らの衝動を持つ複雑な有機体のようになった、とも述べる。**メタファーとしての視角** と **実際に自律性を獲得したという主張** が同居している、ということだ。テクニウムは単なる詩的比喩ではなく、**比喩から存在論に越境しかける概念** として読む必要がある（Cool Tools サイトでの著者自身の概念解説は [こちら](https://kk.org/cooltools/what-technology/)）。

この点を整理すると、テクニウムは [人工生命](https://en.wikipedia.org/wiki/Artificial_life) 論とも、[ヴェルナツキーの noosphere](https://en.wikipedia.org/wiki/Noosphere)（人類の理性的・科学的活動が地球を覆って一つの知的層を形成するという 1920 年代の概念）とも、単純には一致しない。生命に似た自己組織化を強調する点では人工生命的であり、地球規模の知的層としては noosphere に近い。しかしケリーは、noosphere のように人間理性を中心に置くのではなく、技術的複合体それ自体を進化主体のように扱う。彼の関心は「人間の知性が地球を覆う」ことより、「技術が人間を含む生成条件を組み替えながら増殖する」ことにある。だからこそ、彼の概念は広くて強いが、そのぶん責任主体が見えにくくなる。

> noosphere 概念とテイヤール・ド・シャルダンの思想史的位置づけ、AI シンギュラリティ論との連続と断絶については、別記事 [ヌースフィアとオメガ点は AI シンギュラリティ論の前史か：テイヤール・ド・シャルダン再読](/blogs/posts/2026/05/teilhard-noosphere-omega-singularity/) と Wiki ページ [ヌースフィアとオメガ点](/blogs/wiki/concepts/noosphere-omega-point/) を参照。

## 思想史的位置づけ

### Vernadsky / Teilhard ── 複雑性上昇の系譜の世俗化

テクニウムは無から出てきたものではない。第一に、ヴェルナツキーとテイヤール・ド・シャルダンの系譜に接続する。[ヴェルナツキー](https://en.wikipedia.org/wiki/Vladimir_Vernadsky) は、生物圏から noosphere への移行を、人間の理性的・技術的活動が地球過程に組み込まれる一段階として考えた（[EOLSS: Vernadsky の biosphere/noosphere 論の要約](https://www.eolss.net/sample-chapters/c12/e1-01-08-08.pdf)）。テイヤールはこれを、より神学的に、複雑性と意識が高まり最終的統合へ向かう運動として見た。ケリーが技術を宇宙進化と生命進化の延長に置くとき、その語りはこの「複雑性の上昇」系譜を世俗化し、シリコンバレー化したものとみなせる。

ただし違いも大きい。テイヤールの終点はキリスト論的・人格論的な収束点であり、ヴェルナツキーの noosphere は地球化学的・地質学的な新状態だった。ケリーはそこから神学を抜き、人格化の主題も抜き、複雑性そのものを技術圏の自己駆動因に置き換えた。これは継承というより、**同じ語彙的家族の中での選択的記憶喪失** である。

### マクルーハンとサイバネティクス ── 「人間の延長」から「技術の自律」へ

第二に、テクニウムはメディア論の [Marshall McLuhan](https://en.wikipedia.org/wiki/Marshall_McLuhan) とサイバネティクスを強く継承する。マクルーハンは [*Understanding Media: The Extensions of Man*](https://web.mit.edu/allanmc/www/mcluhan.mediummessage.pdf) (1964) で、メディアを「人間の延長」(extensions of man) と捉え、問題はコンテンツではなく、それが人間関係のスケールとパターンをどう変えるかだと論じた。数学者ノーバート・ウィーナーの [サイバネティクス](https://en.wikipedia.org/wiki/Cybernetics) もまた、動物と機械を貫く制御と通信の一般理論を立てた。

ケリーが技術を外在的道具から離し、生命・情報・制御・ネットワークの延長として見るとき、その基盤にはこの発想がある。ただし、マクルーハンやウィーナーは、技術形態が人間の知覚や制御構造を変えると論じても、そこから直ちに「技術自身の欲望」へ跳躍することはなかった。この差は小さくない。マクルーハンは媒介の効果を論じたのであって、媒介する側の主体性を語ったのではない。

### Whole Earth から Wired へ ── カリフォルニアン・イデオロギー

第三に、テクニウムは Whole Earth から Wired への文化的移行の産物である。Stewart Brand の [Whole Earth Catalog](https://wholeearth.info/) は "Access to Tools" を掲げ、自給・DIY・全体論・コミュニティを結ぶ媒体だった。Fred Turner は『From Counterculture to Cyberculture』(University of Chicago Press, 2006) で、このネットワークが Brand を媒介に、カウンターカルチャーとシリコンバレーを長期的に接続したと論じる。

Richard Barbrook と Andy Cameron はさらに踏み込み、Wired や Kelly、Brand らの言説を、サイバネティクス・自由市場経済・対抗文化的リバタリアニズムの混成として ["The Californian Ideology"](https://handmade-web.net/assets/barbrook_californian-ideology.pdf) (Mute Magazine, 1995) と呼んで批判した。彼らの中心的論点は、この混成イデオロギーが代替未来を封じる、というものだ。Barbrook と Cameron は、コンピュータとネットの発展自体が大規模な公的資金と国家介入に依存した事実 ── DARPA による [ARPANET](https://en.wikipedia.org/wiki/ARPANET) の構築、米軍開発から出発した [GPS](https://en.wikipedia.org/wiki/Global_Positioning_System) ── を、シリコンバレー神話が組織的に忘却していると指摘した。

テクニウムは、思想史的にはこの文脈で読むと最も輪郭がはっきりする。

### 比較思想 ── Arthur, Latour, Simondon, Stiegler, Heidegger, Ellul, Hui

第四に、比較思想として見ると、テクニウムは複数の技術哲学のあいだに位置するが、どれとも一致しない。

- **複雑系経済学者の W. Brian Arthur** は [*The Nature of Technology: What It Is and How It Evolves*](https://sites.santafe.edu/~wbarthur/thenatureoftechnology.htm) (Free Press, 2009) で、技術を既存技術の組み合わせと問題解決の進化として捉えるが、統一的な「意志」を仮定しない。
- **科学社会学者の Bruno Latour** が展開した [Actor-Network Theory](https://en.wikipedia.org/wiki/Actor%E2%80%93network_theory) は、人間と非人間（道具・機械・文書・微生物までも）を対等な actant として同じネットワーク上で記述するが、超越的な巨大主体を置かない。
- **Gilbert Simondon** と **Bernard Stiegler** は、人間と技術を相互生成的に捉える。Stiegler の『Technics and Time』シリーズは、技術を時間と記憶の外在化として理論化した（参照: [Tracy Colony, "Stiegler's politics of operativity", *Parrhesia* 27 (2017)](https://parrhesiajournal.org/wp-content/uploads/2023/10/parrhesia27_colony.pdf)）。
- **Martin Heidegger** は「技術への問い」(1954) で、技術を存在開示の様式 (Gestell、しばしば「立て-組み」「集-立」と訳される) として捉えた。
- **Jacques Ellul** は『La Technique ou l'enjeu du siècle』(1954) で、効率としての technique（技法・テクニーク）の全面化を批判した。
- **香港の哲学者 Yuk Hui** はさらに、技術を普遍単数形ではなく、宇宙論と倫理に応じた複数の [cosmotechnics](https://sidoli.w.waseda.jp/Hui_2016_The_Question_Concerning_Technology_in_China_An_Essay_in_Cosmotechnics_Introduction.pdf) として捉え直す（*The Question Concerning Technology in China: An Essay in Cosmotechnics*, Urbanomic, 2016, Introduction）。

テクニウムはこれらの論点を横断しながらも、**単一の巨大技術主体を語る点で固有** である。Arthur が組み合わせ進化を語っても単一の超主体は置かないこと、ANT が分散ネットワークを描いても巨大主体を置かないことと比べると、ケリーの語りは特殊である。

### 加速主義との距離

最後に、加速主義との関係を整理しておく必要がある。Nick Land 系の [加速主義 (accelerationism)](https://www.britannica.com/topic/accelerationism) は、資本と技術の自己増殖をほとんど非人間的プロセスとして肯定する。テクニウムは Land ほど露骨には反人間主義ではないが、技術の不可避な前進を語るとき、しばしば似た傾きに接近する。ここでも差は程度問題であって、方向の違いではない。

## テクニウム概念の強み

批判の前に、テクニウムの強さを明確にしておく必要がある。

第一の長所は、技術を個別装置の集まりではなく、**相互依存的・累積的・不可逆的な生態系** として捉える点にある。ある技術は単独では存在せず、標準、法、教育、供給網、記録形式、保守体制、知識共同体の上に乗る。Brian Arthur が技術を既存技術の組み合わせと捉えたのも同じ方向であり、Kelly が特許制度や文化までテクニウムに含めたのも、技術の再生産条件そのものを考えようとしたからである。プラットフォーム、クラウド、API、学習データ、半導体、電力網が絡み合う今日の AI 時代では、この視角の有効性はむしろ高まっている。

第二の長所は、**人間中心主義を相対化すること** である。マクルーハンがメディアを人間の延長と見たように、ケリーは「人間が技術を使う」という一方向図式を崩し、人間もまた技術環境によって構成されると示唆する。Simondon や Stiegler の、人間と技術の生成を切り離せないという立場にも通じる。少なくともこのレベルでは、テクニウムは「人間が主で技術は従」という単純な道具観を超えるための強力な概念装置である。

第三の長所は、**AI、ソフトウェア、制度、知識、インフラを連続的に考えられる** ことだ。Anthropic が [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (2024) で agents を「長時間自律的にツールを使うシステム」と「規定的なワークフロー」の両方を含むものとして定義し、OpenAI が [A practical guide to building AI agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) (2025) でマネージャ型や分散型のマルチエージェント構成を実務的に整理しているように、今日の AI システムはすでに「モデル」単体ではなく、ツール・メモリ・プロトコル・ハンドオフ・評価の複合体として設計されている。テクニウムは、この複合体全体を「技術圏」として眺める語彙を与える。

したがって、テクニウムは **説明力の強い中層概念** だと言える。個体としての技術論では狭すぎ、宇宙論としての技術神秘主義では広すぎるところで、技術の累積性・接続性・歴史的慣性をまとめて捉えられる。この強みを失わず、しかも政治性を回復することが、超克の条件になる。

## テクニウムへの批判

### 1. 技術決定論批判 ── 「不可避」の語法

最大の問題は、ケリーが「進行中の複雑な相互作用」を描くと同時に、その流れをしばしば不可避とみなすことである。技術哲学者 Langdon Winner は古典的論文 ["Do Artifacts Have Politics?"](https://faculty.cc.gatech.edu/~beki/cs4001/Winner.pdf) (1980; *The Whale and the Reactor*, 1986 に収録) で、人工物や技術システムが効率だけでなく権力と権威の形を体現しうることを示し、技術を必要な運命ではなく分岐・選択・代替可能性のある系列として読む技術史的視座を提示した。後年の ["Social Constructivism: Opening the Black Box and Finding It Empty"](https://sidoli.w.waseda.jp/Winner_1993.pdf) (Science as Culture, 1993) では、技術の社会構成主義 (SCOT) が政治経済的文脈や規範的判断を扱わない「空の箱」になっていると批判している。両者を合わせれば、技術の方向は政治的選択の積み重ねであり、外側から「inevitable」と語ることはむしろ思考停止に近い、ということになる。

Kelly の語法では、技術の進行はしばしば「inevitable」と形容される ── 実際、彼の 2016 年の著書タイトルそのものが『The Inevitable』である。技術の進化圧を強く見ること自体は有益でも、それを「避けられないもの」と言い換えた瞬間に、政策、制度、規制、労働運動、失敗、拒否、撤退の余地が痩せる。Winner の警告は、まさにこの「inevitable」を解除することにあった。

### 2. 進歩史観批判 ── 破壊・負債・監視を中心化しない

ケリーは技術を生命の延長として、複雑性・多様性・美を増やす肯定的な力として描く。だが Ellul が technique を効率の全面化として捉えたように、近代技術は人間的豊かさと同時に、標準化・従属・搾取・予測可能性の強制も拡大してきた。英国の作家・技術批評家 James Bridle が『New Dark Age』(Verso, 2018) で論じたように、計算量やデータの増大は自動的に可視性や知性を増やすのではなく、ときに不透明性と無力感を増幅する。

Kelly の進歩叙述は、破壊・老朽化・負債・環境負荷・戦争技術・監視の累積を十分に中心化していない。これは強調点の偏り以上の問題で、**何を中心化するかが、技術哲学の政治性そのもの** だからである。

### 3. 資本主義の自然化批判 ── 中心的論点

ここが本稿の中心である。英国のメディア理論家 Richard Barbrook と Andy Cameron は、Kelly や Brand 周辺の言説を、自由市場経済と対抗文化的リバタリアニズムを技術決定論で接着した「カリフォルニアン・イデオロギー」とみなし、これが代替未来を封じると論じた。彼らの議論で繰り返し強調されるのは、20 世紀のコンピュータ・ネットワーク技術が自由市場の自然な作動の結果ではなく、大規模な公的資金と国家介入に依存して生み出された、という事実である（[Barbrook & Cameron, "The Californian Ideology" (Mute, 1995)](https://handmade-web.net/assets/barbrook_californian-ideology.pdf)）。

Barbrook と Cameron が中心的に挙げた具体例は、インターネットの基礎を作った [ARPANET](https://en.wikipedia.org/wiki/ARPANET) ── 米国防総省 DARPA (米国防高等研究計画局) のプロジェクト ── である。同じ系譜には、現在の位置情報インフラを支える [GPS](https://en.wikipedia.org/wiki/Global_Positioning_System) も加えうる（こちらは Barbrook & Cameron の論文ではなく、本稿が補足する例）。シリコンバレーの主要技術の系譜を辿れば、軍事・国家・公的資金の刻印が随所に残っている。

ゆえに、「市場で勝ち残った技術」を「技術自身の自然な欲望」とみなすことは、国家、軍事、補助金、安全保障、資本集約性を不可視化する。テクニウムの弱点は、生命比喩そのものよりも、**選択環境の政治経済学が薄いこと** にある。

### 4. 人間主体の希薄化批判 ── Zuboff の問い

ハーバード・ビジネス・スクール名誉教授の Shoshana Zuboff は、[*The Age of Surveillance Capitalism*](https://we.riseup.net/assets/533560/Zuboff%2C%2BShoshana.The%2BAge%2Bof%2BSurveillance%2BCapitalism.2019.pdf) (PublicAffairs, 2019) の定義部で、監視資本主義を「人間経験を予測と販売のための行動データへ変換することを基礎とした、新たな経済秩序」として規定した。彼女が早い段階の *In the Age of the Smart Machine* (Basic Books, 1988) から繰り返し立ててきたのは、人間と機械の関係において主体性・自治・家・聖域・未来への権利がどう配置されるかという問いである。

Kelly のテクニウムは人間を宿主や媒介に近いものとして描きがちだが、Zuboff の問いは、これらの人間的条件が依然として政治的に賭けられていることを思い出させる。

テクニウムは、人間を脱中心化する点では有益だが、身体・ケア・死・弱さ・躊躇・拒否権といった人間的条件を痩せさせる危険がある。

### 5. 擬人化・擬似生命論批判

複雑系科学における自己組織化は、一般に局所相互作用と正のフィードバックから秩序が生じることを意味する概念であり、そこからただちに意志・目的・欲望は導かれない。Kelly は「欲望 (want)」を「傾向」「衝動」「軌道」に近いものとして使う場合もあるが、その言い方はしばしば「生命が望むものを技術も望む」というテレオロジーへ傾く。

Richard Dawkins の [ミーム](https://en.wikipedia.org/wiki/Meme) 論ですら、文化的複製子の競争を語っても、統一された巨大主体の意志は仮定しない。Arthur の技術進化論も、組み合わせ進化を語るが、単一の超主体は置かない。テクニウムが複雑系として有効なのは「意志なき創発」までであり、「欲望ある主体」へ進むと理論的リスクが急増する。

### 6. 政治性の隠蔽批判 ── 大きな物語が責任を曖昧にする

Winner の古典的主張は、人工物やシステムは効率だけでなく、権力や権威の形を体現しうる、というものだった。Evgeny Morozov もまた『To Save Everything, Click Here』(PublicAffairs, 2013) で、深く政治的・倫理的・解決不能な問題が、追跡・定量化・ゲーミフィケーションによって技術的効率の問題へ還元される「ソリューショニズム」を批判した。

Kelly 的な大きな語りは、設計者・所有者・規制者・被害者・周辺化される地域や労働者の差異を平滑化しやすい。テクニウム批判の核心は、「技術は自律しない」という一点よりも、**技術の大きな物語が具体的な不平等と責任を曖昧にする** ことにある。

## AI 時代における再評価

### 「自己強化する技術圏」の現象的説得力

AI 時代は、テクニウム概念を二重の意味で再活性化している。実務レベルでは、OpenAI は agents を while ループとツール呼び出し、複数エージェントのハンドオフとして説明し、Anthropic は workflow と agent を区別しつつ、いずれも "agentic systems" に含めている。現在の AI は、単発の推論装置ではなく、**自己反復的に環境へ作用する構成体** として設計されている。ケリーが見た「自己強化する技術圏」は、少なくとも現象面では、以前より説得力を帯びている。

研究開発の最前線でも同様である。Google DeepMind の [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) (2025) は進化的コーディング・エージェントとして、データセンター効率・チップ設計・AI 訓練プロセスの最適化に寄与したとされる。[AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/) は Gemini 2.0 を中核にしたマルチエージェント研究支援システムとして提示されている。[Gemini Robotics](https://deepmind.google/discover/blog/gemini-robotics-brings-ai-into-the-physical-world/) は、複数ステップの計画を立て自律的に実行する身体化エージェントとして売り出されている。

ここでは AI が、**技術の設計者であり、運用者であり、改善者でもある** という循環が実際に進んでいる。「テクニウムが自己記述・自己改変・自己運用する情報生態系に近づいている」という仮説は、かなりの部分で支持できる。

### 「機械の欲望」ではなく「制度化された最適化」

しかし、ここで誤解してはならないのは、AI が「本当に欲望を持った」ということではない。現在のエージェント設計は、目的・ツール権限・停止条件・評価指標・コンテキスト接続・ガードレールを人間が与えて初めて成立する営みである。

- [Model Context Protocol (MCP)](https://www.anthropic.com/news/model-context-protocol) は、AI が外部システムへ安全に接続するための標準として Anthropic から 2024 年に公開された。
- [NIST AI 600-1 (Generative AI Profile)](https://www.nist.gov/itl/ai-risk-management-framework) は、生成 AI 固有のリスクを特定し、信頼性ある運用のための行動を提示している。

ここで増えているのは「野生の自律性」ではなく、**標準化され、計測され、制御された自律性** である。AI がケリーの比喩を強化するのは事実だが、それは「機械の欲望」が現れたからではなく、**最適化ループが制度化されたから** だと考えるほうが理論的に強い。

### 実在論から制度論へ

この意味で、AI 時代は Kelly を単純に正当化もしないし、単純に破綻させもしない。むしろ、AI はテクニウム概念を **実在論から制度論へ押し戻す**。AI の「欲望」に見えるものは、ベンチマーク、報酬関数、企業収益、データセンター投資、国家安全保障、ツール利用可能性、ユーザーインターフェース設計、法規制の組み合わせから現れる。

AI インフラは近年、国家安全保障・経済競争力・電力網・コミュニティ影響を含む政策対象として明示的に扱われてきた。2025 年 1 月の米国大統領令 [Advancing United States Leadership in Artificial Intelligence Infrastructure](https://www.federalregister.gov/documents/2025/01/17/2025-01395/advancing-united-states-leadership-in-artificial-intelligence-infrastructure) は、AI 計算リソースを電力網・コミュニティ・安全保障とまとめて統治対象に置いた典型例である（その後の政権交代で同 EO は撤回されたが、AI を国家インフラとして扱う発想そのものは政策トラックに残っている）。問題にすべきはテクニウムそのものより、**加速それ自体を善とみなす価値観** のほうである。

### 応答の芽 ── オープン標準とローカル実行

同時に、応答の芽もある。オープン標準とローカル実行環境は、巨大プラットフォームへの全面依存を少しずつ緩めうる。MCP はツール接続の互換性を開き、[LocalAI](https://localai.io/) のようなローカル実行基盤は、消費者向けハードウェア上で LLM やエージェントを走らせることを掲げている。

もちろん、オープン性やローカル性はそれ自体で民主性を保証しない。それでも、**主体が技術圏の内部にしかいられないとしても、内部での位置と交渉力は設計し直せる** という点は重要である。

## 超克のための理論枠組み ── 「操舵可能な技術生態系」

テクニウムを超克するには、まず問いの立て方を変える必要がある。

### 問いの変換: 「技術が何を欲するか」から「どの選択環境が何を増殖させるか」

ケリーの問いは「What does technology want?」だった。これに対して本稿が提案する問いは、**「どのような選択環境が、どのような技術を増殖させるのか」** である。

Winner が整理したように、技術史は分岐・選択・社会的形成を含む。Arthur も技術進化を、既存要素の組み合わせとニーズに対する解の探索として捉える。ここに政治経済を加えれば、技術の方向は「技術の本性」ではなく、評価基準・所有形態・資本コスト・法制度・軍事需要・教育・身体習慣・メンテナンス能力によって決まると考えられる。これはテクニウムの解体ではなく、その **選択環境の可視化** である。

### 成長対象から保守・修理・撤退の対象へ

第二に、技術を成長対象だけでなく、**保守・修理・更新・撤退の対象** として捉え直す必要がある。インフラ維持に関するサーベイ ── 例えば [Eno Center / TRIP の "What Is the Value of Infrastructure Maintenance?"](https://etd723z5379.exactdn.com/app/uploads/2024/04/what-is-the-value-of-infrastructure-maintenance_0.pdf) ── が示すように、公共インフラは経済活動の基盤であり、状態の管理と適時のメンテナンスが不可欠で、維持を怠れば劣化が進む。これは道路や水道だけの話ではない。AI システムにもモデル劣化、データ腐敗、権限逸脱、依存関係の老朽化、セキュリティ脆弱性がある。

未来の技術哲学は「何を新しく作るか」だけでなく、**「何を安全に保ち、何を縮退させ、何をやめられるか」** を中心に据えるべきである。

### 単数の technology から複数の cosmotechnics へ

第三に、技術を単数ではなく **複数形** で考える必要がある。Yuk Hui の cosmotechnics は、技術を普遍単一の運命ではなく、宇宙論と倫理が結びついた複数の技術的秩序として考える道を開く。

これに従えば、シリコンバレー的高速化だけが技術発展ではない。土着技術、民具、修理文化、ローカル AI、コミュニティ・ネットワーク、公共クラウド、非商業プロトコルもまた、別様の技術生態系を形成しうる。テクニウムを複数化することは、西洋近代の進歩史観を相対化し、技術の価値基準を一つに固定しないために必要である。

### 人間の位置を「外部観察者」でも「宿主」でもなく、「継続的な操舵者」に

第四に、人間と技術の関係を再定義する必要がある。Stiegler が示したように、技術は単なる外部道具ではなく、時間と記憶の外在化に関わる。だから、人間はテクニウムの外部観察者でも、完全な主人でもない。

だがそれは、人間がただ宿主になることを意味しない。人間は **操作者・訓練者・監督者・共作者・拒否者** として複数の位置を持つ。AI エージェント時代の設計思想は、この複数位置を制度的に守る必要がある。

説明可能性 (explainability) は重要だが、それは「動いているシステムを理解する」段階の要請である。その前提として、「動いているシステムを止め、別の挙動に切り替えられる」運用面の操舵可能性がなければならない。具体的には、以下の要素が前提条件となる。

- **介入可能性 (interruptibility)**: 動いているプロセスを止められること
- **停止可能性 (stoppability)**: 完全に終了させ、状態を巻き戻せること
- **権限の段階化 (graduated permissions)**: ツール権限を最小から段階的に拡大すること
- **ログによる責任追跡 (auditable logs)**: 誰が、何を、いつ、なぜ実行したか
- **局所実行 (local execution)**: 巨大プラットフォームへの全面依存を避ける
- **データ可搬性 (portability)**: ロックインを解除する
- **代替可能性 (substitutability)**: モデル・ツール・プロバイダを差し替えられる

これらは、AI agent 時代の「人間の操舵可能性」を支える具体的設計原理である。

### 新概念: 「操舵可能な技術生態系」

以上を踏まえて、テクニウムに代わる新概念として、ここでは **操舵可能な技術生態系 (steerable technical ecology)** を提案する。これは、技術を一個の巨大主体とも、単なる受動的道具ともみなさず、**複数の技術生態系が、制度・市場・身体・教育・インフラによって方向づけられる可塑的な複雑系** だと定義する概念である。

要点は五つ。

1. **欲望ではなく選択環境を分析単位にする** ── 「技術が何を欲するか」ではなく「どの環境が何を選ぶか」
2. **成長ではなくメンテナンスと可逆性を中核指標にする** ── 「何を作るか」ではなく「何を保ち、何をやめられるか」
3. **単一の最適解ではなく複数の技術圏を認める** ── 単数の Technology ではなく、複数の cosmotechnics
4. **人間を外部でも宿主でもなく、継続的な操舵者として位置づける** ── 介入・停止・代替を設計原理に
5. **AI を神話化せず、プロトコル・評価器・資源制約・所有構造のなかで理解する** ── 「機械の欲望」ではなく「制度化された最適化」

## 結論

テクニウムは **いまでも有効な技術哲学か** という問いには、次のように答えるのが最も妥当である。**存在論としては過剰、ヒューリスティックとしては有効、政治理論としては未熟、AI 時代の診断概念としては更新必須** である。

鋭いのは、技術をネットワーク化された進化系として見た点、人間もまた技術圏に作られると見た点、AI・制度・知識・インフラを連続的に見た点である。危ういのは、そこで生じる慣性や依存を、「技術の意志」として再神秘化してしまう点にある。

「テクニウムは技術決定論か、それとも複雑系的共進化論か」という二択で言えば、ケリーの最良の直観は後者に属するが、彼のレトリックはしばしば前者へ滑る。批判の中心は、純粋な理論的誤りだけではない。むしろ、**政治的無邪気さと、資本・国家・軍事・プラットフォームが技術の方向を決める仕組みの理論化不足** にある。

AI 時代にこの概念が再び強度を持つのは、エージェント・評価器・ロボティクス・プロトコル・データセンターが確かに「自己運用的」な風景を作っているからだ。しかしそれでも、設計すべきなのは「人間を不要にするテクニウム」ではなく、**人間の自在性・介入可能性・拒否権・可逆性・ケア能力を増幅する技術生態系** である。

## 参考リンク

### 一次文献 ── Kevin Kelly

- [Kevin Kelly, *What Technology Wants* (Viking, 2010) — PDF (Universitat Pompeu Fabra)](https://www.upf.edu/documents/4185509/228936771/Kelly%2C%2BWhat%2BTechnology%2BWants.pdf/de4650a1-473f-e1cd-07c2-2c213d0740fd)
- [Kevin Kelly, *Out of Control* (Addison-Wesley, 1994) — 著者公式サイト](https://kk.org/books/out-of-control)
- [Kevin Kelly, "What Technology Wants" — Cool Tools 自己解説](https://kk.org/cooltools/what-technology/)

### 思想史・比較文献

- [Marshall McLuhan, "The Medium is the Message"（『Understanding Media』第 1 章）— PDF (MIT)](https://web.mit.edu/allanmc/www/mcluhan.mediummessage.pdf)
- [Vladimir Vernadsky, biosphere / noosphere 論 — EOLSS sample chapter](https://www.eolss.net/sample-chapters/c12/e1-01-08-08.pdf)
- [W. Brian Arthur, *The Nature of Technology: What It Is and How It Evolves* — Santa Fe Institute 紹介ページ](https://sites.santafe.edu/~wbarthur/thenatureoftechnology.htm)
- [Yuk Hui, *The Question Concerning Technology in China: An Essay in Cosmotechnics* (Urbanomic, 2016) — Introduction PDF](https://sidoli.w.waseda.jp/Hui_2016_The_Question_Concerning_Technology_in_China_An_Essay_in_Cosmotechnics_Introduction.pdf)
- [Whole Earth Catalog / wholeearth.info アーカイブ](https://wholeearth.info/)
- [Britannica: Accelerationism](https://www.britannica.com/topic/accelerationism)
- [Tom Colony, "Stiegler's politics of operativity", *Parrhesia* 27 (2017)](https://parrhesiajournal.org/wp-content/uploads/2023/10/parrhesia27_colony.pdf)

### 批判文献

- [Langdon Winner, "Do Artifacts Have Politics?" (1980) — PDF (Georgia Tech)](https://faculty.cc.gatech.edu/~beki/cs4001/Winner.pdf)
- [Langdon Winner, "Social Constructivism: Opening the Black Box and Finding It Empty" (1993) — PDF (Waseda)](https://sidoli.w.waseda.jp/Winner_1993.pdf)
- [Richard Barbrook & Andy Cameron, "The Californian Ideology" (Mute Magazine, 1995) — PDF](https://handmade-web.net/assets/barbrook_californian-ideology.pdf)
- [Shoshana Zuboff, *The Age of Surveillance Capitalism* (PublicAffairs, 2019) — PDF](https://we.riseup.net/assets/533560/Zuboff%2C%2BShoshana.The%2BAge%2Bof%2BSurveillance%2BCapitalism.2019.pdf)
- [自己組織化と擬似テレオロジー批判の現代的整理 — arXiv:1708.03394](https://arxiv.org/abs/1708.03394)

### AI 時代の現代的接続

- [Anthropic, "Building effective agents" (2024)](https://www.anthropic.com/research/building-effective-agents)
- [OpenAI, "A practical guide to building AI agents" (2025)](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- [Model Context Protocol (MCP) — Anthropic (2024)](https://www.anthropic.com/news/model-context-protocol)
- [Google DeepMind, AlphaEvolve (2025)](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)
- [Google Research, AI co-scientist](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- [Google DeepMind, Gemini Robotics](https://deepmind.google/discover/blog/gemini-robotics-brings-ai-into-the-physical-world/)
- [NIST AI Risk Management Framework (incl. GenAI Profile)](https://www.nist.gov/itl/ai-risk-management-framework)
- [LocalAI](https://localai.io/)
- [Executive Order "Advancing United States Leadership in Artificial Intelligence Infrastructure" (Federal Register, 2025-01-17)](https://www.federalregister.gov/documents/2025/01/17/2025-01395/advancing-united-states-leadership-in-artificial-intelligence-infrastructure)

### インフラ維持・修理の経済学

- [Eno Center / TRIP, "What Is the Value of Infrastructure Maintenance?" (2024)](https://etd723z5379.exactdn.com/app/uploads/2024/04/what-is-the-value-of-infrastructure-maintenance_0.pdf)

## 限界 ── この記事が扱えていないこと

本稿は Kelly の概念の射程と盲点を整理したが、Donna Haraway、Lewis Mumford、Nick Land、Benjamin Bratton、James Bridle、Bernard Stiegler、Gilbert Simondon については、Kelly 批判に対して強い圧力を与える論点に絞って扱っており、各思想家の全体系を均等に再構成したものではない。

また、現代 AI の事例も、現場実装の速度が速いため、エージェント製品や評価値よりも、比較的安定した一次資料と設計原理に重心を置いた。次の段階では、AI エージェントの企業内運用、ローカル AI の実装形態、公共インフラとしての AI の制度設計を、より実証的に追う余地がある。

## 関連 Wiki / 関連記事

- [ヌースフィアとオメガ点（テイヤール・ド・シャルダン）](/blogs/wiki/concepts/noosphere-omega-point/) — 「複雑性上昇」系譜の宗教的・地球化学的原型
- [ヌースフィアとオメガ点は AI シンギュラリティ論の前史か：テイヤール・ド・シャルダン再読](/blogs/posts/2026/05/teilhard-noosphere-omega-singularity/) — シンギュラリティ論の宗教的前史を扱う隣接記事
- [加藤周一『日本文化の雑種性』と「雑種性」概念の展開](/blogs/posts/2026/05/kato-shuichi-hybridity/) — 外来概念の受容・変形・再編という方法論的隣接。カリフォルニアン・イデオロギーがサイバネティクス＋自由市場経済＋カウンターカルチャーの雑種であるという読みは、加藤の雑種文化論と方法論的に対比できる
- [雑種文化論（加藤周一）](/blogs/wiki/concepts/kato-shuichi-hybridity/) — Wiki 側エントリ
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — テクニウム概念の現代的具体例。エージェント設計原理は「操舵可能性」の制度的実装に直結する
- [自己改善型エージェント](/blogs/wiki/concepts/self-improving-agents/) — 「機械の欲望」ではなく「制度化された最適化ループ」として読み直すべき対象
- [マルチエージェント協調パターン](/blogs/wiki/concepts/multi-agent-coordination-patterns/) — Kelly 的な「集合知性」を技術的に解体した実装語彙
