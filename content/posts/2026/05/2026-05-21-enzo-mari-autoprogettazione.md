---
title: 「1%しか理解されなかった」エンツォ・マーリ ── Autoprogettazione を AI 時代の判断教育として読み直す
slug: enzo-mari-autoprogettazione
date: 2026-05-21
lastmod: 2026-05-21
draft: false
author: eotel
model: claude-opus-4-7
description: 「1% しか理解されなかった」と嘆いたエンツォ・マーリの 1974 年 Autoprogettazione を一次資料で読み直し、Fab
  Lab・OSHWA・IKEA・generative design との距離を測りながら、AI 時代の「判断教育」として再翻訳する。
categories:
- その他
tags:
- エンツォ・マーリ
- デザイン哲学
- autoprogettazione
- 技術哲学
- 生成AI
audio_url: https://github.com/Eotel/blogs/releases/download/audio/2026-05-21-enzo-mari-autoprogettazione.m4a
audio_lang: ja
audio_generated_at: '2026-05-21T05:01:42Z'
audio_source: notebooklm
audio_format: debate
---

エンツォ・マーリ (Enzo Mari, 1932–2020) は、1974 年に粗木板と釘だけで家具を組む図面集『Proposta per un'autoprogettazione』を公開した。一般向けに無償で配布され、新聞報道され、数千件の請求が届いた。にもかかわらず、晩年のマーリ自身は、企画の意図を理解した人は **「1% しかいなかった」** と述べている [^designmuseum]。

この嘆きは、半世紀以上たった 2026 年に、別の文脈で重みを増している。LLM とジェネレーティブデザインが「案を出す」コストを限りなく下げ、デザイナーは増殖する選択肢のどれを採用するかを判断する側に追いやられている。マーリは生前、Autodesk の generative design が登場するより前に、**「条件を増やす人」と「条件を学ばせる人」** の違いを言語化していた。本稿では、まず Autoprogettazione が当時何を狙っていたのかを一次資料で確認し、それが現在の Fab Lab / OSHWA / IKEA / 生成設計とどう違うのか、そしてなぜ AI 時代に再読する価値があるのかを整理する。

![1970 年代の設計工房で粗木板と釘で組まれた素朴な椅子。周囲には端材、釘、金槌、図面が散乱している、エンツォ・マーリの Autoprogettazione を象徴する版画調イラスト](/blogs/images/enzo-mari-autoprogettazione-hero.png)

## 『Autoprogettazione?』とは結局なんだったのか

まず一次資料に戻る。2002 年に Corraini から再版された英訳版で、マーリ本人はこの企画を冒頭にこう要約している [^pirate]。

> "A project for making easy-to-assemble furniture using rough boards and nails. An elementary technique to teach anyone to look at present production with a critical eye. (Anyone, apart from factories and traders, can use these designs to make them by themselves. The author hopes the idea will last into the future and asks those who build the furniture, and in particular, variations of it, to send photos to his studio at 10 piazzale Baracca, 10 - 20123 Milan)."

ここから読み取れる事実は 3 つある。

1. **道具と材料は意図的に貧しい**。ハンマーと釘、粗木板。Design Museum の解説によれば、マーリは「誰もが少なくとも一度は釘を打ったことがある」と考えてこの組み合わせを選んだ [^designmuseum]
2. **対象から「工場と仲買 (factories and traders)」が最初から除外されている**。OSHWA の open hardware 定義が「学習・改変・配布・製造・販売」を可とするのと正反対の制限である [^oshwa]
3. **目的は完成品ではなく、「現在の生産を批判的な眼で見るための初歩的な技法 (elementary technique to ... look at present production with a critical eye)」を教えること**

2002 年再版に付けられた翻訳者注では、マーリの意図がもう一段ほどけて説明されている [^pirate]。

> "It is not easy to translate into English the Italian word autoprogettazione. Literally it means auto = self and progettazione = design. But the term 'self-design' is misleading since the word 'design' to the general public now signifies a series of superficially decorative objects. By the word autoprogettazione Mari means an exercise to be carried out individually to improve one's personal understanding of the sincerity behind the project. To make this possible you are guided through an archetypal and very simple technique. Therefore the end product, although usable, is only important because of its educational value."

つまり autoprogettazione は self-design と訳すと誤解を呼ぶ。なぜならその時点で「design」は世間にとって装飾的な物の系列を意味してしまっているからだ。マーリがこの語で示すのは **「設計の sincerity (誠実さ) に対する個人的理解を深めるために、各自が単独で行う訓練」** であり、その成果物は使えても **「教育的価値ゆえにのみ重要」** だとされている。家具のカタログだと思って読むと、マーリのテキストに何度も裏切られる構造になっている。

加えて、配布物には作者からの一方的な要求もあった。1974 年の公開文 (上記の Corraini 再版引用の括弧内) には、**「家具を組んだ人、特にその派生形を作った人は、写真を Milano の作者スタジオまで送るように」** という要請が明示されている。つまりこれは、図面を一方向に投げ渡すブロードキャストではなく、最初から **変形・応答・再送を含む開いた過程** として設計されていた [^designmuseum]。

## なぜマーリは「1%しか理解されなかった」と嘆いたのか

1974 年の公開は、当時としては予想を超える反響を引き起こした。Design Museum の資料 (執筆: Francesca Giacomelli) によれば、イタリア国内紙だけでなく *The New York Times* でも取り上げられ、数千件の請求や手紙が集まったという。にもかかわらず、マーリは生前、その反応にほぼ満足していなかった。Design Museum の同資料は、マーリがその反応を次のように振り返ったと記述している [^designmuseum]。

> He received thousands of requests and letters of feedback from the general public. He encouraged people to send photographs of built variations, but was disappointed that "only 1% understood what the project was about". The majority praised him for the rustic aesthetic of the models or took it as an endorsement of DIY.

再版の付録に収録された 1975 年テキストでも、マーリは、この試みから起きたことは自分の意図と "the exact opposite to the initiative itself" だったと回顧している [^pirate]。

何が誤読されたのか。Design Museum と Catharine Rossi (Kingston University 在籍時、現 University for the Creative Arts) が *Made in Italy* (Bloomsbury 2014) 第 7 章で論じた内容を突き合わせると、誤読のパターンが見えてくる [^designmuseum] [^rossi]。

- **rustic な見た目だけが称賛された**。粗木板の質感が「自然派インテリア」として消費された
- **単なる DIY 推奨と受け止められた**。家具を安く作るためのカタログとして読まれ、批判教育の側面が落とされた
- **1974 年のうちに Simon International が "Metamobile" として商業化** した。ICS テーブル、EFFE テーブル、EMME ベッドの三型を、図面・寸法切りされた板材・完成家具まで注文可能な形で売り出している [^designmuseum]

最後の点が興味深い。マーリ本人が「産業と商人は使うな」と書いた図面が、公開と同じ年に大手家具メーカーによって商品化されている。2010 年に Artek が `Chair 1` (旧 Sedia 1) を限定的に製品化したときも、構造は似ている。Autoprogettazione は最初から **「反市場として始まり、市場に再吸収される」** という再帰構造を抱えていた。

そして 2026 年現在、Danese の公式オンラインストアでは Timor / Formosa が各 150 ユーロ、`16 Animali` / `16 Pesci` が 410 ユーロから、Putrella が 740 ユーロで売られている [^danesestore]。さらに 16 Animali は年 200 点、Putrella は年 100 点の **限定生産扱い**。マーリの反商品フェティシズムは、現代の制度のなかで、逆に **収集対象 (collectible)** という別種のフェティシズムへ変換されている。これは [技術縮退の哲学](/blogs/wiki/concepts/tech-regression/) の議論にあった「luxury branding に回収される危険」と同型の罠である。

## マーリの仕事全体に貫かれている倫理

ここで重要なのは、Autoprogettazione がマーリのキャリアのなかで例外的な実験ではない、ということだ。Danese の教育玩具、Driade の椅子、Zanotta の高精度椅子、これらは一見別系統に見えるが、同じ倫理で貫かれている。

### Tonietta — 技術を見せ物にしない

1985 年に Zanotta から発表された椅子 Tonietta は、家庭用椅子としては当時珍しかったアルミダイキャスト技術を採用している。完成までに 1981 年から 4 年を要した。Zanotta の公式ページに引かれているマーリ本人の説明はこうだ [^zanottatonietta]。

> "I was particularly hostile towards fashion that wanted objects, including chairs, overloaded with technological or typological arrogance of design: I wanted to design the simplest chair possible, almost obvious, not an object that appears different at any cost. After careful analysis I saw that among modern chairs, Thonet are the ones that best embody the idea of an archetypal image, and so to define the character of my chair I decided to dialogue with this single example of an upper class piece, full of semantic and symbolic values."

つまりマーリが拒否したのは技術それ自体ではなく、**「技術的・類型論的な傲慢さ (technological or typological arrogance)」で重武装された椅子という流行** である。最新技術を使うこと自体は良い。「他と違って見せるために」技術を誇示し、archetype から椅子を遠ざけることが問題だ ── Tonietta はその論理で Thonet の archetype と対話しようとした椅子と読める。

これは Autoprogettazione の「ハンマーと釘で組む」選択と矛盾しない。両者は同じ判断軸の両端にある:

- 高度な技術を **見せ物として** 使うのは、設計理由を見えなくする
- 低度な技術を **教育として** 使うのは、設計理由を見せるためである

判断軸は「技術の高低」ではなく「設計理由が読み手に見えるかどうか」だった。

### Java — 「誰がどんな身振りを繰り返すか」まで設計する

Triennale Milano が 2020 年に公開したマーリ追悼インタビュー連載 *Costellazione Enzo Mari* の第 4 回で、デザインデュオ Formafantasma の Simone Farresin がもう一つの示唆的な事例を挙げている (原文はイタリア語のみ) [^formafantasma]。

> "Quando Mari lo ha progettato non voleva avere cerniere perché non voleva che qualcuno durante la produzione dovesse mettere molle o cerniere tutto il giorno." ── Simone Farresin (Formafantasma)

つまり、マーリが 1960 年代に設計した容器 Java では、**「製造工程で誰かが一日中バネやヒンジを付け続けることを避けたいから」という理由で、最初からヒンジを使わない設計** が選ばれていた、と Farresin は語る。さらに 1973 年の `Proposte lavorazione della ceramica` (Serie Samos) では、マーリはモジュールと指示を陶芸職人に与えながら、職人側の自由度を逆に広げ、労働内部の疎外を減らそうとした [^formafantasma]。

ここから読めるのは、マーリにとって「構造設計」とは、耐力や見た目だけでなく、**誰がどの身振りをどれだけ繰り返すか** を含む労働設計だった、ということである。家具を組む側 (Autoprogettazione) も、工場で組み立てる側 (Java) も、両方が設計対象だった。

### Putrella — 工業半製品をそのまま転用する

1958 年の Putrella は、構造用 I 形鋼 (puttrella, double-T beam) の短い一片の両端をわずかに反らせて、透明塗装をかけただけのセンターピースだ [^daneseputrella]。素材の出自と労働痕跡を一切隠さない。「これは工業用半製品です、加工しないとここまで来ません」というメッセージが、形そのものに含まれている。

Tonietta、Java、Putrella、Autoprogettazione。手法は違うが、どれも同じ問いに向かっている: **「この物がどこから来て、誰の労働を経て、今ここにあるのか」を読み手が判定できる状態を確保すること**。形は問題の解ではなく、読み解きの入口として設計されている。

## 現代システムとの距離 ── 4 つの誤った類似

Autoprogettazione は今日、しばしば「DIY の元祖」「open design の先駆」と紹介される。だが一次資料を読むと、その類似はかなり粗い。マーリは現代のどの実践とも違うものを目指していた。一次資料を突き合わせて整理する。

### Fab Lab との違い

MIT の Fab Charter (現行版) は Fab Lab を次のように定義している。

> "Fab labs share a core capability to make almost anything, allowing people and projects to be shared. [...] Education: training in a fab lab is based on doing projects and learning from peers; you're expected to contribute to documentation and instruction."[^fabcharter]

近い。「作ることで学ぶ」「ピアからの学習」「ドキュメンテーション義務」── どれもマーリと響き合う。だが決定的に違う点が一つある。Fab Lab は **デジタル工作機械 (3D プリンタ、レーザーカッター、CNC) へのアクセス** を中核に置いている。一方マーリは、ハンマーと釘という、文化的にほぼ普遍的な低技術を選んだ。

両者の差は技術スタックの違いではなく、**「機械へのアクセス」を解放したいのか、「判断へのアクセス」を解放したいのか** の違いである。Fab Lab で 3D プリントされたパーツの内部構造を読める人は限られるが、ハンマーで打った釘の合理は誰にでも見える。マーリは後者を選んだ。

### OSHWA / open hardware との違い

OSHWA (Open Source Hardware Association) の Open Source Hardware Definition 1.0 はこう定義している。

> "Open source hardware is hardware whose design is made publicly available so that anyone can study, modify, distribute, make, and sell the design or hardware based on that design."[^oshwa]

学習 (study)、改変 (modify)、配布 (distribute)、製造 (make)、**販売 (sell)** ── すべてが認められる。これに対しマーリの 1974 年公開文言は、利用対象から **「manufacturers and dealers」を最初から除外** している [^pirate]。

両者は表層的には似ている (図面を公開し、改変を許す) が、思想は逆向きだ。

- OSHWA は **ライセンスとしての openness**。法的・商業的な自由を保障する
- マーリは **教育としての openness**。商業化を許す openness ではない

これは OSI 系のオープンソース運動と Stallman の自由ソフトウェア運動が「商業利用」をめぐって衝突した歴史と似た構造を持つ ── ただしマーリは商業利用を拒否する側の、さらに先鋭化した立場にいた。

### IKEA との違い

IKEA Museum のサイトで紹介されている flatpack の歴史によれば、IKEA のセルフ組立て家具は 1956 年頃、テーブル LÖVET を運ぶために脚を外したのが起点だ。**輸送・破損・コストの合理化** という物流側の動機から発達した [^ikea]。

ユーザーが組み立てるという表層は似ているが、IKEA は「組立てる労働を消費者に肩代わりさせることで、家具を安く運び、安く売る」発明である。マーリの場合、組立てそのものが学習目的であり、安く済ませることは副次的でしかない。

両者の差を一文で書けば、**「組立て行為の意味が、物流最適化か、判断形成か」** で逆転する。だが市場ではこの違いがしばしば見失われる。Autoprogettazione の写真は「安く作れる」「ハンドメイドの雰囲気が良い」というメッセージに回収されやすく、マーリが「1% しか理解されなかった」と感じた最大の理由はおそらくここにある。

### Generative Design との違い

Autodesk は generative design を次のように説明している。

> "Generative design is an iterative design process that involves a program which will generate a certain number of outputs that meet certain constraints, and a designer that will fine tune the feasible region by selecting specific output or changing input values, ranges and distribution."[^autodesk]

複数の制約 (荷重、材料、コスト、製造法) を入力すると、AI と最適化アルゴリズムが何百もの候補形状を返してくる。デザイナーは選び、絞る側に回る。これは現在の LLM ベースのコード生成・UI 生成のメタファとも重なる。

ここでマーリの態度は決定的に異なる。マーリは **「制約を増やす人」ではなく、「制約を自分で読めるようにする人」** だった。Autoprogettazione の練習生は、釘を打ちながら、寸法誤差、反り、剛性、荷重経路、加工コストを身体で覚える。それは AI が条件として「与える」ものではなく、人が条件として「読み取る」ものだ。

| 比較対象 | 共通点 | 根本的な差異 |
|---|---|---|
| Fab Lab | 作ることを通じて学ぶ | Fab Lab は機械へのアクセス、マーリは判断へのアクセス |
| OSHWA | 図面公開、改変可能性 | OSHWA は販売まで認める、マーリは「産業と商人」を除外 |
| IKEA | ユーザーが組み立てる | IKEA は物流最適化、マーリは批判教育 |
| Generative design | プロセス重視 | AI は選択肢を増やす、マーリは選択基準を鍛える |

## 反フェティシズムが収集価値に転化する皮肉

ここまで読んで、マーリが幸せだったとは思えないかもしれない。実際そうである。死後の状況は、マーリの思想と二重三重にねじれている。

メディア報道では、彼のスタジオ・アーカイブはミラノ市に寄贈されたが、**40 年間開示しない条件** がついていたことが話題になった [^ft]。一方で、パルマ大学 CSAC に寄託されたマーリのアーカイブ (8,352 文書、3 作品、68 オブジェクト／プロトタイプ) は、4,711 archival units がデジタル公開されている [^designmuseum]。Triennale Milano と Design Museum は彼を canon 化する大回顧展を開きながら、同時に全体像へのアクセスを部分的に閉じている。

そして Putrella は 740 ユーロ、年 100 点限定。マーリが「設計の honest reason を見せる」ために選んだ工業半製品の詩学が、収集家が囲い込む luxury object になっている。

これは [テクニウム](/blogs/wiki/concepts/technium/) や [技術縮退](/blogs/wiki/concepts/tech-regression/) の議論で繰り返し指摘される、**思想の市場回収パターン** の典型だ。Fairphone の機能的 repairability、Patagonia の循環型サービス、Leica の継承可能性 ── これらは実質的自律性を実現するための工夫だったはずだが、市場のなかではブランド化されたミニマリズムに変換され、結局のところ「高くて長く使える物」というカテゴリに収まる。マーリが Putrella で起こしたかったのは、設計の出自を読む眼を養うことだった。だが市場が起こしたのは、設計の出自そのものを記号化することだった。

## AI 時代に Autoprogettazione を本当に生かすには

ここからは推測の領域に入る。AI による生成設計が、コード、UI、家具、建築、すべての領域で「案を出すコスト」を 1/100 にしつつある 2026 年現在、マーリを本当に生かす方法は何か。

復刻家具を所有することでもなければ、デザイン史の教科書に名前を加えることでもない。マーリの方法の本質は、**「判断の遅さ」を制度として埋め込むこと** にある。

これは Anthropic の "Building Effective Agents" の次の一節と同じ方向を向いている [^anthropic]。

> "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all."

Bainbridge (1983) "Ironies of Automation" 以来の human-in-the-loop 研究も、自動化が人間を異常時対応に追い込むほど skill decay と out-of-the-loop performance problem が悪化することを 40 年にわたって示し続けている。AI 時代のデザイナーや開発者にとって、生産速度の問題はもう解けている。難しいのは **判断の質を保つ時間をどう確保するか** だ。

授業設計に落とすなら、以下のような 5 フェーズになる ── ソース文書での提案を、AI 時代の文脈に少し書き換えた。

| フェーズ | 実施内容 | 学習目標 | マーリ的な要点 |
|---|---|---|---|
| 観察 | 既製椅子・既製コードを分解的に読む | 接合・荷重・依存関係を把握する | 「見た目」より「なぜそうなっているか」を問う |
| 制作 | 規格木材と釘だけで / 最小ライブラリだけで一型を作る | 寸法、誤差、エッジケースを体で知る | 図面理解ではなく、材料経験を中心に置く |
| 変形 | 原型に対して必ず一か所改変する (椅子なら座面の角度を 5 度変える / コードなら関数を一つだけ別実装に差し替える) | 設計判断を言語化する | マーリが求めた「変形を返送する」回路を再生する |
| 比較 | IKEA / Fab Lab / OSHWA / AI 生成と比較する | 自己制作の意味を制度的に位置づける | 「手作業=善」「自動化=悪」の短絡を避ける |
| 公開 | 写真・図面・反省文を公開する | 制作を公共的知識へ変える | ライセンス設計と帰属表示を明確にする |

AI を排除する必要はない。生成設計を使ってもいい。ただし、**AI 案を採用する前に必ず手直しと理由説明を課す**。マーリの方法は、「AI で 100 案出してから 1 つ選ぶ」フローのなかに、**「自分の手で 1 案を作って、なぜそれを直したいかを書く」工程を 1 つ挟む** ことに翻訳できる。これは速度を下げるが、出力の責任を、AI ではなく設計者の身体に戻す。

これは、コードレビューのなかに「機械が生成した diff を、人がもう一度キーボードで写経する」工程を意図的に挟むことに似ている。生産性は下がる。だが、生成された案を「なんとなく許可する」状態から、「なぜこの行を残すかを言える」状態に戻すことができる。

## 限界と注意

最後に、マーリの方法をそのまま現代に適用することの限界も書いておきたい。これは彼自身の責任ではなく、現代側の条件の話だ。

第一に、**「ハンマーと釘」は誰にでも開かれた道具ではない**。木材を置けるスペース、騒音を出しても問題ない環境、最低限の安全教育、身体的な打撃作業に耐える力、これらすべてが前提として要る。マーリはこれを「誰もが知る道具」と仮定したが、都市部のアパートに住むソフトウェアエンジニアが釘を打つには、共有工房まで出向く必要がある。**「比較的単純な道具で始められるが、条件は依然として偏っている」** と捉えるほうが正確である。

第二に、**ユーザーへの労働移転リスク**。IKEA 的セルフ組立てが消費者の労働を物流コストに変換したように、Autoprogettazione 的な「自分で作る」枠組みも、悪用すれば消費者への無償労働の押し付けになりうる。AI 時代の文脈に置き換えれば、「あなたの仕事は AI が出した案をチェックすることです」と言って判定責任だけ人間に押し付ける構造と隣接している。マーリが教育的価値を強調したのは、この危険を意識していたからだろう。

第三に、**マーリの本人テキストは難解で長い**。再版本を読んでも、autoprogettazione の意味を取り違える人は今でも多い。実践に落とすときは、彼のテキストを読ませるだけでは足りず、ファシリテーターの介入が要る。

それでも、AI が「案を増やす」ことしかしない時代に、**「案を選ぶ訓練」** を本格的に設計した稀少な実践として、Autoprogettazione は再読に値する。マーリが残したのは「正しい形」ではなく、**正しさを見抜くための面倒な方法** だった。

2026 年、残り 99% の側に回らないためにできることは、たぶん次のひとつだけだ。**AI が出した案を採用する前に、自分の手でもう一案を作り、それを直したい理由を書く。** マーリが Milano のスタジオで写真を返送させようとしたのは、結局のところそういう小さな迂回路だった。それをデザインの世界の外にも持ち込めるかどうかが、AI と一緒に判断を続ける全ての職業の問題でもある。

## 関連 Wiki

- [技術縮退 (technical regression)](/blogs/wiki/concepts/tech-regression/) ── 「判断の遅さ」を制度として埋め込む議論のメタ概念
- [テクニウム (technium)](/blogs/wiki/concepts/technium/) ── 「複雑化そのものを善とする」言説への対置
- [パラサイトヒューマン](/blogs/wiki/concepts/parasite-human/) ── 身体技能・embodied cognition と「残すべき能力」

[^designmuseum]: Design Museum, *Enzo Mari* exhibition resource (2021). <https://designmuseum.org/asset/download?id=2bb1b5af-bc2d-43ef-897d-64f78ae8dc2a>
[^pirate]: Enzo Mari, *Autoprogettazione?* (Corraini, 2002 reprint, English text). <https://syllabus.pirate.care/library/Enzo%20Mari/Autoprogettazione_%20%28221%29/Autoprogettazione_%20-%20Enzo%20Mari.pdf>
[^oshwa]: Open Source Hardware Association, *Open Source Hardware Definition* 1.0. <https://oshwa.org/resources/open-source-hardware-definition/>
[^rossi]: Cat Rossi, "Crafting a Design Counterculture" (in *Made in Italy*). <https://research.uca.ac.uk/6052/7/Made%20in%20Italy%20-%207.%20Crafting%20a%20Design%20Counterculture%20-%20Cat%20Rossi.pdf>
[^danesestore]: Danese Milano Online Store. <https://onlinestore.danesemilano.com/>
[^zanottatonietta]: Zanotta, "Tonietta" product page. <https://www.zanotta.com/en-us/products/chairs-small-armchairs-stools/tonietta>
[^formafantasma]: Triennale Milano Magazine, "Em / Formafantasma" (on Mari retrospective). <https://triennale.org/en/magazine/em-formafantasma>
[^daneseputrella]: Danese Milano, "Putrella" product page. <https://www.danesemilano.com/en/productDetails?idProduct=136>
[^fabcharter]: MIT Center for Bits and Atoms, *The Fab Charter*. <https://fab.cba.mit.edu/about/charter/>
[^ikea]: IKEA Museum, "Flatpacks: The story of IKEA". <https://ikeamuseum.com/en/explore/the-story-of-ikea/flatpacks/>
[^autodesk]: Autodesk, "Generative Design" solutions page. <https://www.autodesk.com/solutions/generative-design>
[^ft]: Financial Times, on Mari's archive bequest. <https://www.ft.com/content/c9e57d79-b3d0-441b-b540-19505c4959bd>
[^anthropic]: Anthropic, "Building Effective Agents" (2024). <https://www.anthropic.com/engineering/building-effective-agents>
