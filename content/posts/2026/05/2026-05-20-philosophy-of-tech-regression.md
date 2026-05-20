---
title: "技術縮退の哲学 — local-first・graceful degradation・AI oversight をひとつの設計判断にまとめる"
slug: "2026-05-20-philosophy-of-tech-regression"
date: 2026-05-20
lastmod: 2026-05-20
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "Heidegger・Illich から local-first・graceful degradation・EU AI Act Article 14 まで、複雑性を「責任」として扱う設計判断を 1 本の軸でまとめる。"
categories: ["AI/LLM"]
tags: ["技術哲学", "local-first", "human-oversight", "resilience-engineering", "repairability"]
---

![Heidegger・Illich・local-first・AI oversight を「技術縮退」という一本の軸でつなぐ概念図のヒーロービジュアル](/blogs/images/philosophy-of-tech-regression-hero.png)

「技術縮退の哲学」という単独の標準用語は、原典・学術文献・実装ドキュメントを横断してもほとんど登場しない。一方で、Heidegger から Illich、Winner、Borgmann、Feenberg、Stiegler を経て、local-first、graceful degradation、resilience engineering、repairability、EU AI Act の human oversight に至るまで、**「複雑化そのものを善としない」という思考の系譜** は確かに存在する。

本稿はこれらを縦に貫いて、「どの能力を高度化し、どの能力を意図的に単純化し、どの能力を外部化し、どの能力を残すか」を決めるための実務哲学として、「技術縮退」を再構築する。

## Executive Summary

**事実**: 本稿で確認した主要な原典・学術文献・実装文書には、「技術縮退の哲学」という単独の標準用語はほぼ見当たらない。実際には、技術哲学、適正技術、low-tech、レジリエンス工学、repairability、local-first、graceful degradation、technical debt、AI の人間監督という複数の系譜が交差する形で論じられている。哲学史の側では、Heidegger が技術を単なる道具ではなく「世界の現れ方」を規定するものとして捉え、Ellul が「機械」ではなく「技法の全体」を問題化し、Illich が道具を制度まで含めて拡張し、Winner が人工物の政治性を論じ、Borgmann が「device paradigm」を批判し、Feenberg と Stiegler が政治・知識・労働の観点から再編した。これらは「複雑化そのもの」を善としない思考の系譜を形成している[^1]。

**解釈**: 以上を踏まえると、「技術縮退」は、単なる後退や性能低下ではなく、**必須機能を残しながら、依存半径・媒介の層・ブラックボックス性・技能の外部化・エネルギー、保守負荷を意図的に減らす設計と統治の選択** として定義するのが最も有効である。この意味での縮退は、local-first が重視する所有権・オフライン性・長期保存・ユーザー制御、graceful degradation が重視する本質機能の維持、repairability が重視する分解・部品供給・保守情報、resilience engineering が重視する吸収・適応・回復と整合する[^2]。

**事実**: 実装レベルでは、local-first は「オフライン」「マルチデバイス」「シームレスな協働」「長期保存」「プライバシー」「ユーザー制御」を同時に満たそうとする構想であり、offline-first は主に不安定なネットワーク下での UX とローカルキャッシュ戦略を扱う。PWA の service worker、cache-first / network-first 戦略、SQLite の単一ファイル・後方互換・可搬・長期保存性、Google SRE における degraded response や load shedding は、いずれも「全部を常時・完全に動かす」のではなく、「**落ちるときも要点を残す**」設計原理を共有している[^3]。

**事実**: 他方で、技術縮退はいつも選択的・自発的とは限らない。GAO は、米連邦政府の最重要 legacy IT の多くが旧式言語、サポート切れハード・ソフト、既知のサイバー脆弱性を抱えていると報告している。JFTC は cloud での vendor lock-in を「他社の同種サービスへの切替が難しい状態」として定義した。OECD と CMA も、クラウド市場での集中、相互運用性の限界、移行の複雑さ、スイッチング障壁に注意を向けている。サプライチェーン側でも OECD は半導体の価値連鎖を重大な脆弱性源と評価している。つまり、**縮退はしばしば「思想」ではなく「維持不能化」から始まる**[^4]。

**事実**: AI 時代には、この問題はさらに先鋭化する。Bainbridge の古典的論文は、自動化が人間の問題を消すどころか拡大しうると述べた。Endsley と Kaber の研究は、高度自動化が out-of-the-loop 問題、状況認識の低下、手動技能の減衰を生みうることを示している。NIST AI RMF、OECD AI Principles、EU AI Act の Article 14 は、AI の信頼性において human oversight を中核に置いている。実務ガイドでも Anthropic は「まず最も単純な解を探し、必要なときだけ複雑化せよ」と述べ、Microsoft は agent を可観測・統治可能・停止可能にすべきだと勧告している[^5]。

**結論**: 技術縮退の哲学は反技術主義ではない。むしろ、**どこに高度化を集中し、どこで意図的に単純化し、どの能力を外部化し、どの能力を残すかを決めるための実務哲学** である。実務的には、「不可逆な失敗が起きるところ」「監査責任が重いところ」「人間の熟達が安全に直結するところ」では、高度化よりも可視化・冗長化・人間介入可能性を優先すべきである。逆に、計算量が多く、反復的で、可逆で、監査ログが取りやすい領域では、AI や自動化の導入余地が大きいと判断できる[^6]。

## 概念と定義

### 表記ルール

本稿では、**事実** を文献・公的資料・実装文書で確認できる内容、**解釈** を複数資料から導いた分析的統合、**推測** を条件付きの将来見通しとして示す。

### 作業定義

**解釈**: 本稿における「技術縮退」とは、目的達成に不可欠な機能を保持しつつ、技術システムの依存半径・媒介の階層・保守負荷・資源使用・技能外部化・ブラックボックス性を縮小し、可逆性・修理可能性・説明可能性・局所自律性を高める方向への設計と統治を指す。したがって、縮退は「全部を捨てること」ではなく、「**どの複雑性を保持し、どの複雑性を外に出さないか**」を決めることである。local-first の七つの理想、MDN の graceful degradation / progressive enhancement、Illich の convivial tools、Tainter の複雑性費用という別系統の議論は、この定義を支える骨格になる[^7]。

**事実**: local-first は、ユーザーがオフラインで作業でき、複数デバイス間で同期でき、長期保存・プライバシー・最終的な所有権を保持することを理想として掲げる。graceful degradation は、新しいブラウザや環境では最良の体験を提供しつつ、古い環境や制限下でも「本質的な内容と機能」は残す設計思想である。progressive enhancement は、その逆向きに、まずベースラインの利用可能性を確保してから上位機能を追加する。これらはいずれも「**全員に一律の完全機能を前提にしない**」という点で、技術縮退の実装語彙である[^8]。

### 近接概念比較表

| 概念 | 中心問題 | 複雑性への態度 | スケール | 技術縮退との関係 |
| --- | --- | --- | --- | --- |
| 技術縮退 | 必須機能を残しつつ、依存・不可逆性・保守負荷を減らす | 選択的に減らす | 製品・組織・制度・市場 | 本稿の作業定義[^9] |
| low-tech | 持続可能で頑健、人をエンパワーする技術を探る | 資源・材料・制御の過剰を批判 | 製品・地域社会 | 近いが、環境・生活世界への比重が強い[^10] |
| appropriate technology | 文脈適合、人間中心、小規模、地域自律 | 「高」か「低」かより適合性を重視 | 開発・地域社会 | 技術縮退の祖型[^11] |
| degrowth | 資源・エネルギー throughput を公正に減らす | 経済全体の縮小を議論 | マクロ経済・政策 | 技術縮退より広い政治経済概念[^12] |
| collapse | 複雑性投資の収穫逓減後に起こる急速な簡素化 | 不本意な縮小 | 文明・社会 | 技術縮退の失敗形態[^13] |
| resilience engineering | 攪乱下でも重要機能を保ち、回復する | 必ずしも単純化しないが、重要機能を守る | インフラ・システム | 技術縮退の運用原理を与える[^14] |
| graceful degradation | 能力低下や障害時でも必須機能を残す | 過負荷時に品質を落として継続 | アプリ・サービス | 縮退の直接的なソフトウェア設計原理[^15] |
| local-first | 協働と所有権を両立し、ネットワーク依存を下げる | 複雑性をエッジに再配置する | アプリ・データ | 縮退の有力なデータ設計パターン[^16] |
| technical debt | 内部品質の欠陥が将来変更コストを上げる | 偶発的複雑化を抑える | コードベース・チーム | 縮退が必要かを診断する概念[^17] |

**解釈**: この比較から見えるのは、「技術縮退」が low-tech や degrowth の単なる言い換えではないことである。low-tech は価値論、degrowth は政治経済、collapse は病理、resilience は能力概念、graceful degradation と local-first は実装概念、technical debt は診断概念である。**技術縮退は、そのあいだを接続するメタ概念として使うと最も生産的** である[^18]。

## 思想史と系譜

### 系譜の要点

**事実**: 哲学としての技術論は、少なくとも近代以降、技術を単なる中立的手段ではなく、人間と世界の関係を再編する力として論じてきた。Internet Encyclopedia of Philosophy は技術哲学の成立を 19 世紀後半以降に位置づけつつ、Heidegger を転回点として扱う。Heidegger は技術を「道具」に還元せず、「**隠れているものを現れさせる仕方**」と捉え、現代技術ではその現れ方が「挑発的」に変わると論じた[^19]。

**事実**: Ellul は『The Technological Society』で、問題の核を個々の機械ではなく、**標準化された手段の総体としての technique** に置いた。Anders は『The Obsolescence of the Human』で、人間が自ら作った技術の前に劣等感を抱く「Promethean shame」を論じ、技術優位のもとで主体性が失われる危険を描いた。Mumford は「authoritarian and democratic technics」という区別そのもので、集中・巨大・統制の技術と、より分散的・共同的な技術の対立軸を提示した[^20]。

**事実**: Illich は道具をハードウェアに限らず、**教育・医療・知識・意思決定を生む制度まで含めて定義** し、学校や自動車や流れ作業が「有効な道具」でなくなる閾値を論じた。Schumacher は 1960 年代初頭から intermediate technology を構想し、後に *Small Is Beautiful* で「人間的尺度」に合う技術選択を大衆化した。Winner は人工物が政治的性質をもつと論じ、Borgmann は device paradigm を通じて、負担や技能から切り離された「便利さ」が人間的実践を痩せさせる仕方を分析した[^21]。

**事実**: 後期には、Feenberg が哲学と構成主義的技術研究の統合を唱え、技術設計を社会的・政治的争点として再開放した。Stiegler はデジタル産業社会における **proletarianization** を、知識と技能の喪失として捉える。ここで「技術を使う／使わない」の二分法は崩れ、問題は「**誰が理解可能性と技能と裁量を持つか**」に移る[^22]。

### 年表

| 時期 | 節目 | 技術縮退との関係 |
| --- | --- | --- |
| 1949〜1954 | Heidegger が "Die Frage nach der Technik"（1949 Bremen 講演 → 1953 Bavarian Academy of Fine Arts 講演 → 1954 出版）で現代技術を「道具以上の現れ方」として論じる | 技術を性能ではなく世界把握の様式として考える出発点[^23] |
| 1954／1964 | Ellul『La Technique』『The Technological Society』 | 問題を個別機械から「技法の体制」に拡張[^24] |
| 1956 | Anders『The Obsolescence of the Human』第 1 巻 | 技術優位のもとでの人間の劣位と主体性喪失を主題化[^25] |
| 1962 | Schumacher が intermediate technology を提起 | 人間的尺度・地域適合・小規模技術の系譜を形成[^26] |
| 1964 | Mumford "Authoritarian and Democratic Technics" | 中央集権的巨大技術と民主的技術の対立軸を明示[^27] |
| 1973 | Illich『Tools for Conviviality』、Schumacher『Small Is Beautiful』 | 自律・閾値・制度としての道具が前景化[^28] |
| 1980 年代 | Winner、Borgmann、Bainbridge | 政治性、便利さの代償、自動化の皮肉が接続される[^29] |
| 1990 年代 | Lehman の法則、technical debt の普及 | ソフトウェア複雑化の持続的コストが可視化される[^30] |
| 2019 | local-first 論文 | クラウド依存を再設計し、所有権と協働を両立させる提案[^31] |
| 2024〜2026 | NIST AI RMF、EU AI Act、human oversight・agent governance、EU repairability score | AI と修理可能性が制度的に「縮退の設計」を要求し始める[^32] |

### 思想家・理論・実装例 対応表

| 思想家・理論 | 主張の核 | 技術縮退への示唆 | 実装への翻訳 |
| --- | --- | --- | --- |
| Heidegger | 技術は単なる手段ではなく、現れの様式 | 「何が見えなくなるか」を問う | 依存関係・データ経路・計算資源を見える化する設計[^23] |
| Ellul | 問題は機械単体でなく technique の総体 | 効率の自己目的化を疑う | KPI だけで機能を増やさず、目的と手段を再接続する[^33] |
| Mumford | authoritarian / democratic technics | 集中化と分散化を政治問題として扱う | federation、相互運用、自治可能な運用単位[^27] |
| Illich | 道具は制度も含み、閾値を超えると反生産的になる | 「便利」が人の能力を奪う閾値を測る | 手動経路、修理可能性、教育・医療での人間裁量保持[^34] |
| Schumacher | 文脈適合・人間的尺度 | 高度化より適合性を優先 | 小規模・現地保守・低資本依存の設計[^11] |
| Winner | 人工物は政治性をもつ | アーキテクチャは権力配分である | open standards、portability、脱ロックイン設計[^35] |
| Borgmann | device paradigm は実践の厚みを奪う | 摩擦ゼロの便利さを無条件に善としない | focal practice を支える UI、手動操作、学習可能性[^36] |
| Feenberg | 技術設計は社会的に争われうる | 技術を民主的に再設計できる | participatory design、公共的 governance[^37] |
| Stiegler | 技術は知識を奪い得る | 外部化は脱熟達を招く | AI を autopilot ではなく co-pilot として制約する[^38] |
| Bainbridge / Endsley | 自動化は皮肉にも人間を弱くしうる | 監視係に落とされた人は異常時に弱い | human-in-the-loop、訓練、手動復帰、可視化[^39] |

## 実装原理と制度条件

### ソフトウェア設計としての技術縮退

**事実**: local-first はクラウドの利点を捨てずに、ユーザーの所有権・オフライン作業・長期保存・プライバシー・制御を取り戻すことを目指す。Ink & Switch は「No spinners」「ネットワークは optional」「Long Now」「最終的な所有権と制御」など七つの理想を明示した。これは、中心サーバへの依存をゼロにする思想ではなく、**同期を補助にし、ローカルを一次にする思想** である[^31]。

**事実**: offline-first は、PWA において service worker、cache、background sync で不安定な接続に耐える設計である。MDN は、offline operation により接続がなくても良い UX を実現できるとしつつ、cache-first は高速だが stale response を返しやすいと注意している。つまり、offline-first は主として接続障害への運用戦略であり、local-first のように所有権や長期保存までを必ずしも含意しない[^40]。

**解釈**: したがって、local-first と offline-first は重なるが同一ではない。前者は **権利とアーキテクチャの議論**、後者は **可用性と UX の議論** である。技術縮退の観点では、local-first は依存半径を縮め、offline-first は障害時の継続性を確保し、graceful degradation は過負荷時に品質を制御して必須機能を残す。三者は代替関係ではなく、階層の異なる補完関係にある[^41]。

**事実**: Google SRE は、過負荷時に degraded responses を返すこと、より安価なローカルコピーに依拠すること、低優先度の仕事を shed することを勧めている。さらに、**graceful degradation のコードパスは普段使われないため壊れやすく**、複雑にしすぎるとそれ自体が障害要因になると警告する。ここでの教訓は明快で、縮退機構そのものは単純で理解可能であるべきだということである[^42]。

**事実**: SQLite は単一ファイル、移植性、後方互換、アトミック更新、将来の回復可能性を利点として挙げ、米国議会図書館が長期保存形式として推奨していると述べている。これは「**data lives longer than code**」という思想を実装したものである。Low-Tech Magazine の solar-powered site も、DB 駆動 CMS をやめて static site にし、既定フォント、dithered image、offline reading を活用して、古い計算機や不安定回線でもアクセスできるようにしている。前者は高信頼の一般化可能な実装知、後者は思想実験的な living lab である[^43]。

### 制度的条件

**事実**: 技術縮退が思想として必要になるのは、複雑性がしばしば組織的・制度的に維持不能になるからである。GAO は、米連邦の最重要 legacy IT 11 件のうち多くが旧式言語、サポート切れハード・ソフト、既知の脆弱性を抱え、2025 年時点でも近代化が完了していない案件が多いと報告した。Lehman も E-type software は環境変化に応じて継続適応されねば満足度が下がり、変更を重ねるほど複雑性が増すと述べている[^44]。

**事実**: クラウドでは、JFTC が vendor lock-in を「他社の同種サービスへの切替が難しい状態」と定義し、CMA は英国の public cloud infrastructure 市場で競争上の懸念を公表した。OECD も、市場集中、移行の複雑さ、相互運用性の限界、データ移転コストや制限的ライセンスが、顧客ロックインを強める可能性に言及している。技術の複雑化は、**市場構造の硬直化でもある**[^45]。

**事実**: 供給の側では、OECD は supply-side risk に capacity constraints や technological issues を含め、半導体の価値連鎖そのものを重要な脆弱性源と評価している。よって、技術縮退を「ローカル化すれば必ず安全」という単純な標語としてではなく、**保守可能性・部品供給・技能供給・移行可能性の束** として扱う必要がある[^46]。

### 実務判断フロー

**解釈**: 下図は、上記文献群をもとに再構成した「高度化するか、縮退させるか」の判断フローである。根拠は、SRE の graceful degradation、local-first、legacy / lock-in 問題、automation の人間要因、AI governance にある[^47]。

![失敗の不可逆性・ネットワーク依存・lock-in 度合いを順に問うて、高度化レーンと縮退レーンに振り分ける判断フロー図](/blogs/images/philosophy-of-tech-regression-decision-flow.png)

図の読み方: 上から順に「失敗は不可逆か」「ネットワーク同期は本質要件か」「lock-in が強く移行経路に乏しいか」「自動化で skill decay が起きるか」の 4 問を Yes/No で辿り、左下の **縮退レーン**（human-in-the-loop、local-first、portability、repairability）と右下の **高度化レーン**（full automation、cloud-native、高速統合）に振り分ける。質問順序は recoverability → coupling → portability → human skill で、責任の大きい軸ほど早く問う設計になっている。

## 組織・市場・AI 時代の含意

### 組織と運用

**解釈**: 組織にとっての技術縮退は、「高機能をやめる」よりも、「**運用が理解できる単位に戻す**」に近い判断である。Google SRE が言うように、普段使わない複雑な縮退コードは危険であり、legacy IT の現実は「理解できない複雑性」が保守と安全保障の両面でコストになることを示している。よって、組織設計では、機能分割、明確な ownership、レジストリ、ログ、停止権限、脱ロックイン計画が先に来るべきである[^48]。

**事実**: Microsoft の AI agent governance 文書は、すべての agent を observable, governed, secure に保つこと、所有者を特定すること、アクセスを制限すること、止めるべきものを止められることを要件にしている。これは AI に特有の話ではなく、**複雑化したソフトウェア一般に対する統治理性の回復** と読める[^49]。

### 市場とブランド化

**事実**: repairability は、すでに市場の周辺ではなく制度化の対象である。EU JRC は 2025 年からスマートフォン・タブレット向けに repairability score をエネルギーラベルに表示し、分解手順、必要工具、部品と修理情報の入手可能性などを評価すると説明している。欧州委員会の repair directive も、保証内外を通じて repair と reuse を増やすことを目的にしている[^50]。

**事実**: 企業のブランド戦略にも複数の型がある。Fairphone は「repairability を念頭に置いた世界初の modular phone」を自称し、長寿命化と自己修理のしやすさを前面に出している。Patagonia の Worn Wear は、買い替えより repair と trade-in を推奨する。Leica は purist design と timeless icon を掲げ、1954 年導入の M マウントの多くのレンズが現行デジタル M でも使える継承性をブランド化している[^51]。

**解釈**: ここから分かるのは、市場における「縮退」は一枚岩ではないことである。Fairphone は機能的 repairability、Patagonia は循環型サービス、Leica は継承可能性と操作の純化を売っている。したがって、**ブランド化された「シンプルさ」は、実質的自律性にもなりうるし、単に高価格な審美的ミニマリズムにもなりえる**。実務では、見た目の簡素さではなく、部品供給、エクスポート、相互運用、修理情報、技能移転の有無で判定すべきである[^52]。

### AI 時代の含意

**事実**: Bainbridge は 1983 年に、自動化が人間の役割を異常時対応だけに狭めることで、かえってオペレータの困難を拡大すると論じた。Endsley らは、高度自動化が out-of-the-loop performance problem を引き起こし、状況認識と手動制御能力を損なうことを示した。2024 年の理論的論文も、AI 支援が専門家の skill decay を加速し、初心者の技能獲得を妨げるおそれを指摘している。さらに、embodied cognition の近年レビューは、身体を伴う学習が学習と指導を強化しうる証拠を整理している[^53]。

**解釈**: したがって、AI 時代の技術縮退は、単に GPU コストや API コストを下げる話ではなく、**人間の判断筋力をどこで温存するか** の問題である。外部化してよいのは、反復的で、可逆で、ログ可能で、説明責任を後から再構成しやすい作業である。残すべきなのは、問題設定、例外処理、責任帰属、現場文脈の読み替え、身体技能と tacit knowledge を必要とする判断である。これは Illich の conviviality と Stiegler の脱熟達批判を、AI 実務に翻訳したものである[^54]。

**事実**: 制度面でも、EU AI Act の Article 14 は、高リスク AI に human oversight を要求し、人間が monitor, interpret, override できること、さらに over-reliance への注意を要件化している。NIST AI RMF は generative AI 向け profile を公開し、OECD AI Principles は trustworthy かつ human-rights-respecting な AI を基準に据えている。実装ガイドでも Anthropic は、最初に最も単純な解を探し、必要なら workflow、さらに必要なら agent と段階的に複雑化すべきだと述べている[^55]。

**事実**: 実装上は、Anthropic が simple, composable patterns を推奨し、Microsoft は human approval を要する tool 呼び出し、structured logging、registry、ownership、control plane を推奨している。ここで推されているのは「全面自律化」ではなく、「**止められる自動化**」である[^56]。

## 限界・未解決論点・判断基準

### 批判と限界

**事実**: 技術縮退には、少なくとも四つの限界がある。第一に、すべての領域で単純化が善ではない。local-first の補助文献は、非同期協働には有効でも、金融取引や巨大データ処理のような領域を全面代替できないと述べている。第二に、repairability や low-tech は、しばしばユーザーや現場に余分な手間を戻す。第三に、縮退は luxury branding に回収される危険がある。第四に、複雑な graceful degradation 自体が新たな複雑性を生むと Google SRE は明記している[^57]。

**解釈**: さらに批判的に言えば、「縮退」はときに **責任転嫁の言葉** にもなる。企業が保守投資を怠った結果生じた劣化を、「ミニマル」「軽量」「フリクションレス」と言い換えることは可能だからである。したがって、縮退を是とするには、**誰の負担が減り、誰の負担が増えるかを必ず追跡** しなければならない。Illich 的に言えば、道具が convivial であるかどうかは、性能ではなく、使用者の行為能力を増やすかどうかで判定されるべきである[^58]。

### 判断基準表

| 観点 | 高度化すべき条件 | 縮退すべき条件 | 外部化してよい能力 | 残すべき能力 |
| --- | --- | --- | --- | --- |
| 失敗の不可逆性 | 人命・法的責任・高額損失に直結 | 失敗が可逆で巻き戻せる | 計算、検索、補助推論 | 承認、停止、例外判断[^59] |
| ネットワーク依存 | リアルタイム共有が本質要件 | 単独作業や遅延同期で足りる | 同期、配布 | 一次保存、オフライン作業[^60] |
| 変更頻度と負債 | 高頻度変更でも内部品質が高い | 新機能より負債返済が得 | 定型生成、テスト補助 | 設計境界の判断[^17] |
| 過負荷・障害時の継続性 | フル機能維持が不可欠 | 必須機能だけ残せばよい | 品質低下を伴う自動応答 | どの機能を残すかの設計[^61] |
| ベンダー依存 | 標準化され、移行経路がある | lock-in、egress、独自仕様が強い | 一時的な managed service 利用 | データ portability、移行計画[^62] |
| 保守・供給可能性 | 部品・技能・サポートが継続する | 旧式・脆弱・供給脆弱 | 一部運用自動化 | 交換・修理・復旧の技能[^63] |
| 学習・熟達への影響 | 自動化しても技能維持策がある | out-of-the-loop や skill decay が起きる | 下調べ、ドラフト、単純監視 | 状況認識、身体技能、問題設定[^64] |
| 市場価値 | 顧客価値が速度・統合性にある | 顧客価値が寿命・修理・継承にある | レコメンド、支援機能 | 所有感、修理可能性、操作の理解[^65] |

### 実務的結論

**解釈**: 「どの技術を高度化すべきか／縮退すべきか」への端的な答えは、**複雑性を、価値ではなく責任に近いものとして扱うこと** である。高度化すべきなのは、暗号、監査、冗長化、障害時のフェイルセーフ、可観測性、相互運用、データ移行、修理部品供給のように、**自由度と安全性を同時に上げる層** である。縮退すべきなのは、常時接続前提、ブラックボックスな便益、過剰なパーソナライズ、切替不能なクラウド依存、技能喪失を招く全面自動化である[^66]。

**解釈**: 「どの能力を外部化すべきか／残すべきか」については、**速度のための外部化と責任のための保持を分ける** べきである。外部化してよいのは、反復計算、機械的照合、候補生成、低リスク要約、下書き、ログ整理である。残すべきなのは、問題設定、承認、異常時対応、倫理的・法的責任、技能継承、現場文脈の解釈である。AI を導入するほど、人間の役割は「監督する人」ではなく、「**いつ自動化を止めるかを判断できる人**」に再定義される[^67]。

### 未解決の論点

**推測**: 今後の重要論点は三つある。第一に、local-first・repairability・AI oversight を同時に満たす標準アーキテクチャが確立するか。第二に、ブランド化された「シンプルさ」と、実質的な自律性・修理可能性とを、制度がどこまで見分けられるか。第三に、AI が熟達を代替するのではなく、**熟達を育てる設計** に転じられるか。現時点で制度は human oversight と repairability の方向へ動いているが、実装と市場はまだ過渡期にある[^68]。

### 情報源の信頼度評価

**事実**: 本稿では、原典・公的資料・査読論文を最優先した。高信頼に置いたのは、NIST、OECD、欧州委員会・AI Act Service Desk、GAO、JFTC、Google SRE、SQLite 公式、Ink & Switch 論文、*Human Factors* などである。中信頼として扱ったのは、Anthropic・Microsoft の実装ガイドや企業公式のブランド説明である。これらは一次実装知として有用だが、規範的正当化そのものではない。Low-Tech Magazine や permacomputing の文書は、運動体・実践コミュニティの資料として補助的に参照し、一般理論の根拠ではなく「実験的実装例」として位置づけた[^69]。

## 関連 Wiki

- [スケーラブル・オーバーサイト](/blogs/wiki/concepts/scalable-oversight/) — EU AI Act Article 14 と human oversight を結ぶ概念ハブ
- [ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) — 「止められる自動化」の設計層
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — Anthropic *Building Effective Agents* の段階的複雑化原則
- [エージェントメモリのロックイン](/blogs/wiki/concepts/agent-memory-lock-in/) — クラウド lock-in と agent lock-in の対称性
- [テクニウム](/blogs/wiki/concepts/technium/) — 「複雑化そのもの」を善とする言説への対置
- [ヘキサゴナルアーキテクチャ](/blogs/wiki/concepts/hexagonal-architecture/) — 依存半径を縮める実装パターン
- [モジュラーモノリス](/blogs/wiki/concepts/modular-monolith/) — 機能分割と ownership の単位設計

## 関連記事

- [テクニウム批判と超克 — ケヴィン・ケリーの『止められない技術』言説に対する別ルート](/blogs/posts/2026/05/technium-critique-and-transcendence/) — 本稿のメタ前提（複雑化を所与としない）と地続き
- [前田太郎のパラサイトヒューマン](/blogs/posts/2026/05/maeda-taro-parasite-human/) — 身体技能・embodied cognition と「残すべき能力」の議論
- [AI 疲れへのアンサー: Claude Code のハーネス機能は本当に必要か](/blogs/posts/2026/03/2026-03-26-ai-fatigue-claude-code-simplicity/) — Anthropic「最初に最も単純な解を」原則の実務適用

## 出典

[^1]: Internet Encyclopedia of Philosophy, "Philosophy of Technology" — <https://iep.utm.edu/technolo/>
[^2]: Kleppmann et al., "Local-first software" (Ink & Switch, 2019) — <https://www.inkandswitch.com/essay/local-first/>
[^3]: 同上、Ink & Switch local-first essay — <https://www.inkandswitch.com/essay/local-first/>
[^4]: U.S. GAO, "Information Technology: Agencies Need to Plan for Modernizing Critical Decades-Old Legacy Systems" (GAO-25-107795) — <https://www.gao.gov/products/gao-25-107795>
[^5]: Bainbridge, "Ironies of Automation" (1983) — <https://davidjusth.com/s/Ironies-of-Automation_Bainbridge_1983.pdf>
[^6]: Google SRE Book, "Addressing Cascading Failures" — <https://sre.google/sre-book/addressing-cascading-failures/>
[^7]: Ink & Switch local-first essay — <https://www.inkandswitch.com/essay/local-first/>
[^8]: 同上 — <https://www.inkandswitch.com/essay/local-first/>
[^9]: 本稿の作業定義（local-first essay の問題設定を一般化）— <https://www.inkandswitch.com/essay/local-first/>
[^10]: Bihouix et al., "What is low tech?" (HAL working paper) — <https://hal.univ-lorraine.fr/hal-03598528v3/document>
[^11]: Pansera & Sarkar, "Crafting Sustainable Development Solutions: Frugal Innovations of Grassroots Entrepreneurs" (UQAM working paper, 2018) — <https://economie.esg.uqam.ca/wp-content/uploads/sites/54/2020/01/2018-22_docdt_eco.compressed.pdf>
[^12]: Hickel et al., "Degrowth scenarios for emissions and energy use" (Ecological Economics, 2024) — <https://www.sciencedirect.com/science/article/pii/S0921800923003646>
[^13]: Tainter, "Social complexity and sustainability" (USDA Forest Service reprint) — <https://www.fs.usda.gov/rm/pubs_journals/2006/rmrs_2006_tainter_j001.pdf>
[^14]: Bergström et al., "On the rationale of resilience in the domain of safety" (European Journal of Risk Regulation, 2016) — <https://link.springer.com/article/10.1007/s41125-016-0002-4>
[^15]: MDN Web Docs, "Graceful degradation" — <https://developer.mozilla.org/en-US/docs/Glossary/Graceful_degradation>
[^16]: Ink & Switch local-first essay — <https://www.inkandswitch.com/essay/local-first/>
[^17]: Martin Fowler, "TechnicalDebt" — <https://martinfowler.com/bliki/TechnicalDebt.html>
[^18]: Bihouix et al., "What is low tech?" (HAL working paper) — <https://hal.univ-lorraine.fr/hal-03598528v3/document>
[^19]: Internet Encyclopedia of Philosophy, "Philosophy of Technology" — <https://iep.utm.edu/technolo/>
[^20]: EBSCO Research Starters, "Jacques Ellul's *The Technological Society*" — <https://www.ebsco.com/research-starters/literature-and-writing/jacques-elluls-technological-society>
[^21]: Kerschner & Ehlers, "A framework of attitudes towards technology in theory and practice" (Ecological Economics, 2016, S0921800916302129) — <https://www.sciencedirect.com/science/article/abs/pii/S0921800916302129>
[^22]: Feenberg, "Critical Theory of Technology" (chapter from *Between Reason and Experience*) — <https://www.sfu.ca/~andrewf/books/critbio.pdf>
[^23]: Internet Encyclopedia of Philosophy, "Philosophy of Technology" — <https://iep.utm.edu/technolo/>
[^24]: EBSCO Research Starters, "Jacques Ellul's *The Technological Society*" — <https://www.ebsco.com/research-starters/literature-and-writing/jacques-elluls-technological-society>
[^25]: University of Minnesota Press, *The Obsolescence of the Human, Volume 1* — <https://www.upress.umn.edu/9781517912659/the-obsolescence-of-the-human/>
[^26]: STEPS Centre, "Concept of 'Intermediate Technology' introduced" — <https://steps-centre.org/timeline/concept-of-intermediate-technology-introduced/> (1962 年導入を裏付け)。Small Is Beautiful (1973) の大衆化については Schumacher Center for a New Economics — <https://centerforneweconomics.org/envision/legacy/small-is-beautiful/> を参照
[^27]: Mumford, "Authoritarian and Democratic Technics" (1964 reprint, UFMG) — <https://www.mom.arq.ufmg.br/mom/02_babel/textos/mumford_authoritarian.pdf>
[^28]: Kerschner & Ehlers (2016), ScienceDirect S0921800916302129 — <https://www.sciencedirect.com/science/article/abs/pii/S0921800916302129>
[^29]: Winner, "Do Artifacts Have Politics?" (Daedalus, 1980, Georgia Tech reprint) — <https://faculty.cc.gatech.edu/~beki/cs4001/Winner.pdf>
[^30]: Lehman, "Laws of Software Evolution Revisited" (1996, Kent State reprint) — <https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Lehman96.pdf>
[^31]: Ink & Switch local-first essay — <https://www.inkandswitch.com/essay/local-first/>
[^32]: NIST AI Risk Management Framework — <https://www.nist.gov/itl/ai-risk-management-framework>
[^33]: EBSCO Research Starters, "Jacques Ellul's *The Technological Society*" — <https://www.ebsco.com/research-starters/literature-and-writing/jacques-elluls-technological-society>
[^34]: Kerschner & Ehlers (2016), ScienceDirect S0921800916302129 — <https://www.sciencedirect.com/science/article/abs/pii/S0921800916302129>
[^35]: Winner, "Do Artifacts Have Politics?" — <https://faculty.cc.gatech.edu/~beki/cs4001/Winner.pdf>
[^36]: Chughtai, "Human Values and Digital Work: An Ethnographic Study of Device Paradigm" (*Journal of Contemporary Ethnography*, 49(1), 2020) — <https://journals.sagepub.com/doi/abs/10.1177/0891241619855130>。なお Borgmann 自身の device paradigm は *Technology and the Character of Contemporary Life* (University of Chicago Press, 1984) を一次原典として参照すると確実。
[^37]: Feenberg, "Critical Theory of Technology" — <https://www.sfu.ca/~andrewf/books/critbio.pdf>
[^38]: Stiegler-related working paper on proletarianization (University of Bath; British English title "Proletarianisation" in source URL) — <https://researchportal.bath.ac.uk/files/156015994/Proletarianisation_b2_article_Final_.pdf>
[^39]: Bainbridge, "Ironies of Automation" — <https://davidjusth.com/s/Ironies-of-Automation_Bainbridge_1983.pdf>
[^40]: MDN, "Offline and background operation" — <https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Offline_and_background_operation>
[^41]: Ink & Switch local-first essay — <https://www.inkandswitch.com/essay/local-first/>
[^42]: Google SRE Book, "Handling Overload" — <https://sre.google/sre-book/handling-overload/>
[^43]: SQLite, "Application File Format" — <https://www.sqlite.org/aff_short.html>
[^44]: U.S. GAO, "Information Technology: Agencies Need to Plan for Modernizing Critical Decades-Old Legacy Systems" (GAO-25-107795) — <https://www.gao.gov/products/gao-25-107795>
[^45]: JFTC, "Final Report on Trade Practices in the Cloud Services Sector" (2022, English release) — <https://www.jftc.go.jp/en/pressreleases/yearly-2022/June/221102EN.pdf>
[^46]: OECD, *Supply Chain Resilience Review* (2025) — <https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/06/oecd-supply-chain-resilience-review_9930d256/94e3a8ea-en.pdf>
[^47]: Google SRE Book, "Addressing Cascading Failures" — <https://sre.google/sre-book/addressing-cascading-failures/>
[^48]: 同上 — <https://sre.google/sre-book/addressing-cascading-failures/>
[^49]: Microsoft Learn, "AI agent governance and security" — <https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai-agents/governance-security-across-organization>
[^50]: European Commission JRC, "New EU labels help consumers choose more repairable electronics" (2025) — <https://joint-research-centre.ec.europa.eu/jrc-news-and-updates/new-eu-labels-help-consumers-choose-more-repairable-electronics-2025-06-20_en>
[^51]: Fairphone, "Design for repairability" — <https://www.fairphone.com/hub/en/impact/design-2/>
[^52]: European Commission JRC, "New EU labels help consumers choose more repairable electronics" — <https://joint-research-centre.ec.europa.eu/jrc-news-and-updates/new-eu-labels-help-consumers-choose-more-repairable-electronics-2025-06-20_en>
[^53]: Bainbridge, "Ironies of Automation" — <https://davidjusth.com/s/Ironies-of-Automation_Bainbridge_1983.pdf>
[^54]: Kerschner & Ehlers (2016), ScienceDirect S0921800916302129 — <https://www.sciencedirect.com/science/article/abs/pii/S0921800916302129>
[^55]: EU AI Act Service Desk, "Article 14: Human Oversight" — <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14>
[^56]: Anthropic, "Building Effective Agents" — <https://www.anthropic.com/engineering/building-effective-agents>
[^57]: Korhonen et al., "Critical perspectives on the circular and local-first economy" (Aalto University) — <https://aaltodoc.aalto.fi/items/473870e8-2fc4-44f6-8562-7dff022f2206>
[^58]: Kerschner & Ehlers (2016), ScienceDirect S0921800916302129 — <https://www.sciencedirect.com/science/article/abs/pii/S0921800916302129>
[^59]: EU AI Act Service Desk, "Article 14: Human Oversight" — <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14>
[^60]: Ink & Switch local-first essay — <https://www.inkandswitch.com/essay/local-first/>
[^61]: MDN Web Docs, "Graceful degradation" — <https://developer.mozilla.org/en-US/docs/Glossary/Graceful_degradation>
[^62]: JFTC, "Final Report on Trade Practices in the Cloud Services Sector" (2022) — <https://www.jftc.go.jp/en/pressreleases/yearly-2022/June/221102EN.pdf>
[^63]: U.S. GAO, GAO-25-107795 — <https://www.gao.gov/products/gao-25-107795>
[^64]: Bainbridge, "Ironies of Automation" — <https://davidjusth.com/s/Ironies-of-Automation_Bainbridge_1983.pdf>
[^65]: Fairphone, "Design for repairability" — <https://www.fairphone.com/hub/en/impact/design-2/>
[^66]: Google SRE Book, "Addressing Cascading Failures" — <https://sre.google/sre-book/addressing-cascading-failures/>
[^67]: Endsley & Kiris, "The Out-of-the-Loop Performance Problem and Level of Control in Automation" (*Human Factors*, 37(2), 381–394, 1995) — <https://journals.sagepub.com/doi/10.1518/001872095779064555>
[^68]: EU AI Act Service Desk, "Article 14: Human Oversight" — <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-14>
[^69]: NIST AI Risk Management Framework — <https://www.nist.gov/itl/ai-risk-management-framework>
