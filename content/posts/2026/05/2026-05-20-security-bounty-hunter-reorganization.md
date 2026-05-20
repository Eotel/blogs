---
title: "バグバウンティは本当に終わったのか — HackerOne・Google・Apple の一次資料で読む 2026 年の再編"
slug: "security-bounty-hunter-reorganization"
date: 2026-05-20
lastmod: 2026-05-20
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "「バグバウンティはもう終わった」は本当か。HackerOne 8,100 万ドル、Google VRP 1,710 万ドル、Apple 累計 3,500 万ドルなど一次資料を統計化し、AI 時代の市場再編と二極化、企業の多層購買モデルを読み解く。"
ShowToc: true
TocOpen: false
categories: ["セキュリティ"]
tags: ["bug-bounty", "VRP", "脆弱性開示", "HackerOne", "Google-VRP", "Apple-Security-Bounty", "AI-security", "AppSec", "PTaaS", "バグハンター"]
---

「もうバグバウンティで生活できる時代は終わった」「AI が研究者を駆逐する」という言葉を SNS や勉強会で耳にする機会が増えた。本当にそうだろうか。

結論から書くと、**「バグバウンティ市場そのものの滅び」は事実ではない**。HackerOne では 2025 年に bug bounty だけで 8,100 万ドルが支払われた。Google VRP も 2025 年に 1,710 万ドル、Microsoft Bounty も 1,700 万ドルを公開している。Apple は 2020 年以降の累計支払いを 3,500 万ドル超・受賞研究者 800 人超と公表した。市場は縮んでいない。

ただし、**「Web の定番脆弱性を拾って生活する従来型ハンター像」は急速に崩れている**のも事実だ。AI が母数を増やし、重複と未検証報告で入口が詰まり、企業の購買は VDP・Bug Bounty・PTaaS・Red Team・ASM・AI Red Teaming を組み合わせた多層モデルへ移っている。

この記事では、HackerOne・Google・Microsoft・Meta・Apple・Bugcrowd・Intigriti・YesWeHack・DARPA・NIST・CISA・DOJ・GitHub などの一次資料をもとに、**「滅び」ではなく「再編」**として市場を読み解く。

## 調査の前提と定義

本稿では情報の確からしさを 3 段階に分けて記す。**事実**は公式統計・公式ブログ・規制当局文書に基づく記述、**解釈**はそれらの組み合わせから導く分析、**推測**は今後の展開に関する条件付き見通しを指す。対象期間は主要ベンダーとプラットフォームの公開資料が比較しやすい 2021〜2026 年前半を中心に据えた。

議論の前提として、関連するセキュリティサービスのモデルを次に整理する。**Zero-day Market** は比較のための作業定義で、「協調的開示や正式な報奨制度の外側で、排他的な脆弱性知見や exploitability を売買する経済圏」を指す。法的・倫理的に評価が分かれるため、ここでは市場メカニズムの比較対象として扱う。

| モデル | 主目的 | 支払い形態 | 期間 | 典型的な成果物 | AI の影響 | 現時点の評価 |
|---|---|---|---|---|---|---|
| **Bug Bounty** | 未知の実害ある脆弱性の継続発見 | 成果報酬 | 継続 | 再現可能な valid report と修正可能な文脈 | 発見母数を増やすが、検証品質が勝敗を分ける | 続く。ただし選別が厳しくなる |
| **VDP** | 安全な報告窓口と受理プロセス | 通常は無償、謝辞中心 | 継続 | 受理・トリアージ・連絡 | AI 時代ほど入口として重要 | さらに拡大 |
| **VRP** | ベンダー製品の高影響脆弱性の奨励 | 報奨金 | 継続 | 製品・サービス別の高品質報告 | 高難度側に報酬集中 | 強い |
| **Pentest** | 期間限定の体系的評価 | 工数課金が中心 | 時限 | 報告書、網羅的確認 | 前処理は速くなる | 需要継続 |
| **Red Team** | 攻撃者模倣による目的達成演習 | 工数・成果混合 | 時限 | 攻撃シナリオ、到達証明 | 一部自動化されるが人の設計が要 | 需要増加 |
| **ASM** | 攻撃面の発見と把握 | サブスク中心 | 継続 | 資産一覧、露出把握 | AI と自動化の恩恵が大きい | バウンティの前段として拡大 |
| **Zero-day Market** | 排他的価値の現金化 | 売買・仲介 | 単発〜継続 | exploitability と独占性 | 高難度側で依然競争 | 正規市場と競合する参照軸として残る（解釈） |

**解釈**として重要なのは、AI が入ってもこれらのモデルが一つに収束するのではなく、むしろ役割分担が鮮明になっていることだ。下層は自動化が、中層は VDP と Bug Bounty が、上層は招待制・exploit chain・Red Team が担う。

## 年表 — 「滅び」ではなく「再編」が起きてきた

次の年表は、過去 10 年で起きた主要イベントを時系列に並べたものだ。2016 年の DARPA Cyber Grand Challenge が自動化研究の起点となり、2020 年に CISA が BOD 20-01 で米連邦機関に VDP 公表を求めた。2021 年以降、主要ベンダーの報奨総額は拡大軌道に入る。2023〜2025 年には Microsoft の AI Bounty、Google の AI/Cloud VRP、Apple の PCC 研究対象追加、DARPA AIxCC、HackerOne の 2025 AI 統計が重なり、**「AI によって BBP が消える」のではなく「AI を組み込んだ多層外部検証」へ市場が移った**ことが見て取れる。

![バグバウンティ市場再編の主要イベントを 2016 年から 2026 年まで年表で示し、DARPA Cyber Grand Challenge から Bugcrowd の AI 利用率 82% まで主要マイルストーンをカラー分けで配置した時系列図](/blogs/images/security-bounty-hunter-timeline.png)

市場構造も変わった。HackerOne は Bug Bounty 単体ではなく Pentest as a Service、Code、AI Red Teaming、Response を前面に出し、Bugcrowd は Bug Bounty、VDP、PTaaS、Red Team as a Service、ASM を同じ土台で提供している。YesWeHack は Bug Bounty、VDP、Continuous Pentesting、Autonomous Pentest を並べ、Intigriti も VDP＋Bug Bounty＋PTaaS の layered security を勧める。企業が「人間の外部知見」そのものを捨てたわけではないが、**純粋な公開 BBP 一本足打法からは離れている**ことを意味する。

![自動化と AI の進歩が他コストを圧縮しつつ、検証ボトルネック・定番 Web 単価低下・高難度領域への報酬集中・多層化したサービス購買を経由して、最終的にプラットフォーム再武装と二極化に至る再配置を示すフロー図](/blogs/images/security-bounty-hunter-restructure.png)

**解釈**として、この流れは二つの意味を持つ。第一に、公開 BBP の平均的な期待値は下がりやすい。第二に、高難度領域における外部研究者の価値はむしろ上がる。DARPA の AIxCC と 2016 年 CGC は、自動化が「限定された環境」では強いことを示したが、Apple や Intigriti の姿勢は、現実の市場では依然として**証明責任・影響評価・信頼**が主戦場であることを示している。

## 統計で見る市場実態 — 「市場が消えた」は反証される

まず指摘しておきたいのは、**市場の公開統計が非常に不揃い**だという点だ。Google、Microsoft、Meta、Apple のような企業 VRP は比較的明確に年次数字を出すが、プラットフォームはコミュニティ規模や累計値は出しても、**重複率や平均報酬を統一基準で開示しない**ことが多い。以下では非開示を非開示のまま残し、利用可能な一次情報だけを並べる。これ自体が「プラットフォーム限界」の一つでもある。

次の棒グラフは、計測単位が比較可能な一部の公式年次開示だけを抜き出したものだ。**プラットフォーム全体と単一企業 VRP は本来別物**なので、ここでは「市場が消えたかどうか」を見るための存在証明として扱う。

![Google VRP・Microsoft Bounty・Meta Bug Bounty・HackerOne プラットフォーム合計の年次報奨金総額を百万 USD 単位で並べた棒グラフ。HackerOne 2025 が 81M USD で突出し、Google と Microsoft はいずれも 2025 年に 17M USD 前後まで増加していることを示す](/blogs/images/security-bounty-hunter-payouts.png)

### プラットフォーム別の公開統計

| プラットフォーム | 公開された報奨金総額 | 参加者数 | レポート数 | 重複率 | 平均報酬の参考値 | 読み取り |
|---|---|---|---|---|---|---|
| **HackerOne** | $380M+ 累計、2025 年 bug bounty $81M | 1.5M+ 研究者 | 累計 500k+ bugs、2022 年 65,000+ valid | 非開示 | 2021 年 critical 中央値 $3,000、2025 年支払いは前年比 +13% | 市場は縮小ではなく再価格付け。ただし重複率は非開示 |
| **Bugcrowd** | 最新累計は非開示 | 2018 年時点で 80,000 researchers、2026 年調査は 2,000+ hackers が対象 | thousands of submissions ベース、P1 級脆弱性が平均 13 時間ごとに発見 | 非開示 | Priority One Report で P1 単価の継続上昇を公表（公共部門 P1 報酬 +58% など） | 研究者規模の最新公開値が弱く透明性は限定的。ただし P1 単価上昇は続く |
| **Intigriti** | 累計非開示 | 非開示 | 640+ public bug bounty programs、18 業種を分析 | 非開示 | 2024 年時点で public sector の critical 平均 €3,348、manufacturing の medium 平均 €1,150 | マーケット価格の透明化には積極的だが総量統計は限定的 |
| **YesWeHack** | 累計非開示 | 2022 年時点で 35,000+、2026 年時点で 約 130,000 hunters | 2021 年は検出バグ数が倍増、35% が高/重大 | 非開示 | 2021 年の総報奨は +140% YoY、最大支払い €40,000、受理後 24 時間以内報奨 78% | 伸びているが集計の粒度が粗い。支払い速度の開示は比較的良い |

**解釈**として、プラットフォーム比較で見えるのは「衰退」ではなく**透明性の差とセグメンテーション**だ。HackerOne は規模の数値が豊富で、Bugcrowd はインサイト中心、Intigriti は価格ベンチマーク、YesWeHack は運用品質と成長率を前面に出している。各社は同じ Bug Bounty 市場を売っているようで、実際には別の価値提案に寄っている。

### 企業 VRP 別の公開統計

| 企業 / プログラム | 公開年 | 報奨金総額 | 受賞研究者数 | レポート数 | 平均報酬の参考値 | コメント |
|---|---|---|---|---|---|---|
| Google VRP | 2021 | $8.7M | 非開示 | 数千件規模 | 算出不可 | 年次総額が明確に増加軌道へ入った年 |
| Google VRP | 2022 | $12M+ | 非開示 | 2,900+ security issues | 約 $4.1k / issue | Android だけで $4.8M、Chrome は 470 unique reports / $4M |
| Google VRP | 2024 | 約 $12M | 600+ | 一部のみ公開 | <$20k / 受賞研究者 | Cloud・AI・Android・Chrome の強化が進む |
| Google VRP | 2025 | $17.1M | 747 | 一部のみ公開 | 約 $22.9k / 受賞研究者 | 2010 以来累計 $81.6M |
| Microsoft Bounty | 2023 | $13.8M | 345+ | 1,000+ issues | 約 $40k / 受賞研究者 | AI bounty 導入前後の基準年 |
| Microsoft Bounty | 2024 | $16.6M | 343 | 1,000+ issues / year | 約 $48.4k / 受賞研究者 | AI program 含む拡張が進行 |
| Microsoft Bounty | 2025 | $17M | 344 | 非開示 | 約 $49.4k / 受賞研究者 | 過去最高の総額を更新 |
| Meta Bug Bounty | 2024 | $2.3M+ | 約 200 | 約 10,000 reports / 約 600 valid | 約 $3.8k / valid report | 有効率は約 6%。AI/LLM も正式にスコープ入り |
| Apple Security Bounty | 2022 時点累計 | $20M 近く | 非開示 | 非開示 | Product category の平均 約 $40k | 高額 exploit chain に集中 |
| Apple Security Bounty | 2025 時点累計 | $35M+ | 800+ | 非開示 | 算出不可 | 業界最高級の支払いレンジへ再設計 |

ここで重要なのは、**重複率を統一基準で出す企業がほとんどない**点だ。例外的に Meta は総報告数と valid 件数を同時に出しているため、「重複・無効・範囲外を含む負荷」の大きさを直接読み取れる。約 10,000 報告に対して valid は約 600 件 — 企業側の視点では **PoC と優先順位づけのコストが中心問題**であることがわかる。

### 報告数と平均報奨の推移が追える代表例 — Chrome VRP

Google Chrome VRP は、報告数と支払いの両方が年単位で追える貴重な一次資料だ。ここでは「平均報奨」を**総額 ÷ unique valid reports**で算出した参考値として示す。個別支払いの平均そのものではないが、難度の上昇と報酬再価格付けを見るには十分有効だ。

| 年 | unique valid reports | 支払い総額 | 参考平均 / report | 読み取り |
|---|---|---|---|---|
| 2022 | 470 | $4.0M | 約 $8.5k | 量も質も高い成熟期 |
| 2023 | 359 | $2.1M | 約 $5.8k | MiraclePtr などの防御強化で件数・単価が一時調整 |
| 2024 | 337 | $3.4M | 約 $10.1k | 件数は減っても、より高価値な報告へシフト |

この表は、「市場の滅び」ではなく、**低難度バグの量産から高難度の少数精鋭へ報告が移ると、件数が減っても報酬単価が上がりうる**ことを示している。AI と防御の進歩は、平均的なハンターには逆風でも、専門家には追い風になりえる。

## AI が変える作業分解 — 「代替できる」と「代替しにくい」

**事実**として、AI はすでにハンターのワークフローに深く入り込んでいる。Bugcrowd の 2026 年調査では 82% が AI を実用していると回答し、HackerOne の 2023 年レポートでは過半数の研究者が GenAI を hacking tools の作成・使用に活用する意向を示した。2025 年には **560+ valid reports** を自律エージェントが提出したと公表されている。Google は 2025 年に dedicated AI VRP を立ち上げ、2024 年の AI bug bounty では 150+ reports / $55,000+、LLM bugSWAT では 35 reports / $87,000+ を公表した。Meta も LLM の model inversion / extraction を正式にスコープに含めている。

ただし、**AI 発見 = 価値ある報告ではない**。Apple はガイドラインで「AI without proper validation」の理論問題を不適格とし、繰り返せば 180 日の processing pause、複数回なら永久排除もありうると明記した。原文ではこう述べている。

> If you repeatedly submit ineligible reports — including infeasible reports about theoretical issues or those discovered by AI without proper validation — we may pause processing your reports for 180 days.
>
> — [Apple Security Bounty Guidelines](https://security.apple.com/bounty/guidelines/)

Intigriti は 2026 年の公式見解で、AI により**入口（top-of-funnel）が広がり、重複面（duplication surface area）が爆発し、ボトルネックが検証・優先順位づけ・信頼（validation・prioritization・trust）に移る**と述べる。原文の該当箇所はこうだ。

> the baseline goes up, but the top-of-funnel widens faster than most programs can absorb, and the duplication surface area explodes. When the cost of generating findings drops, the bottleneck shifts to validation, prioritization, and trust.
>
> — [Intigriti, "AI: The Future of Bug Bounty"](https://www.intigriti.com/blog/business-insights/ai-future-of-bug-bounty)DARPA の CGC と AIxCC は自動化が脆弱性発見・修正に有望であることを示したが、いずれも比較的制約の強い環境だ。現実の bug bounty では、**再現性・現実の影響・責任ある調整**が依然として人間の重心である。

### AI が代替しやすい作業と代替しにくい作業

| 作業 | 区分 | AI 代替性 | 根拠 |
|---|---|---|---|
| リポジトリ横断のコード探索、variant 検出 | 事実 | 高い | CodeQL は脆弱性の知識を codebase 横断で variant 検出に拡張すると明言し、Semgrep・Snyk・GitHub Advanced Security も SAST/Secrets を自動化 |
| 秘密情報漏えいの発見 | 事実 | 高い | GitHub secret scanning は Git history 全体を自動走査し、新しい secret type 追加時に再走査する |
| Recon の拡張、候補 PoC のひな形生成、報告文ドラフト | 事実 | 高い | HackerOne 2023 では 66% がより良い report 作成、53% が code 作成で GenAI 活用を想定。Bugcrowd 2026 では 82% が AI を使用 |
| 重複候補の提示、初期 triage | 事実 | 中〜高 | HackerOne の 2025 年 AI dedupe では、処理報告の 92% に duplicate recommendation、80–95% の positive accuracy を公表 |
| Prompt injection の網羅的試行、AI アプリのテストケース生成 | 事実 | 中〜高 | HackerOne 2025 では prompt injection valid report が +540%、Google/Meta でも AI 固有問題が正式スコープ |
| 認可回避、IDOR、複雑な業務ロジックの立証 | 解釈 | 低い | HackerOne は access control / IDOR / logic 系の価値上昇を示し、Intigriti は edge cases・contextual abuse は人間領域と述べる |
| クラウド横断の設定連鎖、Kubernetes、組織権限モデルの悪用 | 解釈 | 低〜中 | 2022 年の misconfiguration +150%、improper authorization +45%。Cloud VRP の文脈評価は重い |
| モバイル・カーネル・exploit chain の信頼性確保 | 事実 + 解釈 | 低い | Google Android 2022 の最高報奨は $605,000、Apple は exploit chain で 最大 $2M、ボーナス込みで $5M 超を提示 |
| 協調的開示、優先順位づけ、対企業コミュニケーション | 事実 | 低い | Apple は完全で actionable な報告を要求し、NIST/CISA も受理・評価・連絡を VDP の中核に置く |

### 技術領域別の影響

| 技術領域 | 主要シグナル | AI 代替性 | 市場含意 |
|---|---|---|---|
| Web の定番脆弱性 | XSS は 2024 年比で減少傾向 | 高い | 初心者の旨味が減る |
| API | Google Cloud / 各社 API VRP 拡張、API 対象の public programs 増加 | 中 | 仕様差分探索は AI 向きだが、権限モデルは人間優位 |
| 認可 / IDOR | HackerOne 2025 で有効 IDOR が増加、improper access control 上昇 | 低〜中 | 報酬の中心が残る |
| クラウド | misconfiguration +150%、Cloud VRP で 200+ unique vulns | 中 | 検出補助は自動化、実害立証は人間 |
| Kubernetes | OSS・クラウド・権限境界の複合問題として残存 | 中 | OSS-Fuzz / CodeQL で一部自動化、運用文脈は残る |
| Supply Chain | Google OSS VRP、OSV-SCALIBR patch rewards | 中 | コード側は自動化、依存関係・影響分析は継続的に人間が必要 |
| Mobile | Android / Google Devices に $3.3M〜$4.8M 級 | 低 | 高度化・専門化が進む |
| Kernel | exploit chain と memory safety の残存価値が大きい | 低 | AI では補助できても代替は遠い |
| Crypto / Web3 | 2022 年に平均支払いが $6,443 から $26,728 へ上昇（+315%）、上位層は exploit 1 件で 7 桁ドルの事例も | 低 | 上位層に極端に有利 |
| Business Logic | 2021 に +67%、2025 も価値上昇 | 低 | 人間の文脈理解の牙城 |
| AI アプリ固有脆弱性 | AI report +210%、prompt injection +540%、Google/Meta/Apple が専用枠 | 中 | 入口は増えるが、impact proof で差がつく |

## 仮説検証 — 「滅び」「二極化」「企業吸収」を切り分ける

7 つの仮説を一次資料に照らして判定した。

| 仮説 | 事実としての根拠 | 反証 | 判定 |
|---|---|---|---|
| **滅び** | AI による低品質・AI 生成報告の増加、Apple の厳格化、Intigriti の duplicate 爆発、デデュープ需要の増大 | 主要ベンダーの支払い総額は増加。Google・Microsoft・Apple・HackerOne とも拡大傾向 | **棄却** |
| **二極化** | 高額 exploit chain、crypto の高報酬、招待制イベントや top researcher 集中、Meta の valid 率約 6% | 初心者向け教育や CTF は増えている | **強く支持** |
| **高度化** | AI、Cloud、Access Control、Business Logic、Supply Chain、Mobile の高難度化が公式資料に並ぶ | Web の定番脆弱性はまだ残る | **支持** |
| **企業吸収** | 各プラットフォームが BBP 単体ではなく PTaaS、Red Team、ASM、AI Red Teaming を統合。HackerOne では pentesting engagements +54% | 純粋な公開 BBP も継続している | **部分的に支持** |
| **プラットフォーム限界** | 重複率の非開示、低シグナル流入、dedupe 強化、統計の不透明さ | 市場価格形成や安全な窓口としての価値は残る | **支持** |
| **AI 再武装** | Bugcrowd 82% AI 利用、HackerOne 560+ autonomous valid、Google AI VRP、AIxCC | Apple の未検証 AI 報告排除が示すように、使い方を誤ると逆効果 | **強く支持** |
| **幻想（AI が即座に人間を完全代替）** | 現実のプログラム運用・PoC・協調開示では成立していない | CGC / AIxCC の成果は有望で、限定環境では確実に前進 | **現時点では支持（人間代替は幻想）** |

まとめると、**「滅び」より「高難度化＋二極化＋多層サービス化」**のほうが説明力が高い。市場は縮んでいない。縮んでいるのは、**未熟な作業だけで食べられる部分**だ。

### ハンター階層別の影響

| 階層 | 収益見通し | 主な圧力 | 主な機会 | 総合評価 |
|---|---|---|---|---|
| 初心者 | 厳しい | AI で参入障壁が下がる一方、重複と未検証報告で埋もれやすい。Apple の厳格化は象徴的 | CTF、Bug Hunter University、Dojo、Hacker101 など学習資源は豊富 | 最も打撃が大きい |
| 中級 | 分岐点 | 定番 Web の利幅低下、低難度は AI に侵食 | 認可、API、クラウド、モバイルへ専門化すれば上がれる | 二極化の境界層 |
| トップハンター | 強い | 高い再現性と PoC 品質が常に要求される | 高額 exploit chain、招待制イベント、AI を前提にした速度優位 | 相対的に有利 |
| 企業所属ハンター | 安定化 | 社外 bounty のみでなく社内 AppSec / Red Team に吸収される | 企業は crowd を補完的に使うため、両方の経験が価値になる | 雇用に吸収されやすい |
| AI 活用者 | 二極化 | 未検証 AI 生成物はむしろ不利 | recon、variant 検出、草稿作成、重複回避で優位 | 使い方次第で最も伸びる |

### 企業視点とハンター視点の分離

| 論点 | 企業視点 | ハンター視点 |
|---|---|---|
| AI | ノイズと重複を減らし、検証コストを下げたい | recon・PoC・報告速度を上げたい |
| 報酬 | ROI と社内修正コストを見たい | 時間単価と競合プログラム比較で見たい |
| プログラム形態 | VDP・BBP・PTaaS・Red Team を組み合わせたい | 明確な scope、早い triage、低い duplicate 摩擦を好む |
| 法的安全性 | safe harbor と内部手順が必要 | 曖昧な文言や out-of-scope で萎縮しやすい |
| 品質基準 | 完全で actionable な報告が欲しい | 再現可能なら公平に評価されたい |

## 制度と法的リスク — 「バウンティがあるから安全」ではない

**事実**として、制度面は bug bounty を弱めるよりも、むしろ VDP を標準化する方向へ動いている。CISA の BOD 20-01 は連邦機関に VDP の整備と公表を求め、NIST SP 800-216 は受理・評価・連絡・修正・開示のフレームワークを示した。DOJ は 2022 年、CFAA の起訴方針を改め、good-faith security research を考慮する姿勢を明確にしている。少なくとも米国の政府調達・公共部門では、「安全な報告経路」は制度的に追い風だ。

ただし、これは**無条件の免責ではない**。Apple の terms では (1) 対象外システムへのアクセス、(2) 第三者サービスへの攻撃、(3) 過度な disruption、(4) 修正前の公開、を禁止している。報奨は first complete and actionable report のみに絞られる。Bugcrowd も disclosure terms で duplicate、out of scope、not applicable を扱い、IPA も bug bounty は一つの報告ルートだが詳細はプログラム運営者の取り決めに従うと説明している。ハンターにとっての法的実務は、**「バウンティがあるから安全」ではなく、「scope と safe harbor を読んだ範囲で安全」**だ。

| リスク類型 | 主なトリガー | 影響主体 | 主要な緩和策 |
|---|---|---|---|
| 認可外アクセス | scope 外の資産や第三者系を触る | ハンター、企業 | VDP 文言、rules of engagement、NIST SP 800-216 の受理手順 |
| 修正前公開 | SNS・ブログ・講演で先行公開 | ハンター | Apple などは報奨不適格化。CVD を厳守 |
| 個人情報・本番データ | 実データの取得や保持 | 双方 | 最小化、即時報告、検証方法の制御 |
| AI 生成の未検証報告 | PoC 不足、理論問題、誤検知 | ハンター、プラットフォーム | 人手検証の徹底。Apple は pause 制度、Intigriti は proof 重視 |
| duplicate 紛争 | 先着・既知判断の不透明さ | ハンター | 明確な duplicate policy、メタデータ共有、dedupe 自動支援 |
| 支払い・税務・制裁 | 国別制限、本人確認、税務処理 | ハンター | プラットフォームの payout / KYC ルール理解 |
| 日本での扱い | IPA/JVN とベンダー窓口、プラットフォーム窓口の併存 | 双方 | どの窓口に出すかを事前確認し、運営ルールに従う |

**解釈**として、AI 時代の法的リスクは「攻撃的 AI そのもの」より、**未検証の量産と権限逸脱**に集約される。だからこそ、企業が VDP を整備し、ハンターが scope と proof を厳守することの価値は、以前より高くなっている。

## 結論 — 滅びるのは「ハンター」ではなく、AI 以前の稼ぎ方

**事実**として、主要プラットフォームと主要企業 VRP の支払い総額は増えており、「バグバウンティ市場そのものの滅び」は確認できない。

**解釈**として正しい表現はこうだ。**公開市場の下層が AI によって混雑し、上層が高度化・高単価化し、企業購買が複合サービスへ移ることで、従来型の「Web の定番バグを拾って稼ぐ個人ハンター」が相対的に苦しくなっている**。

**推測**として、今後さらに起こりやすいのは「全面消滅」ではなく、**上位 10〜20% と専門領域への集中、公開 BBP の選別化、社内雇用との往復、AI を使いこなせない層の退出**だ。

### 未解決論点

第一に、プラットフォーム横断で比較可能な duplicate rate がほぼ公開されていないため、低シグナル化の実数比較には限界がある。第二に、AI assist と autonomous report の境界がまだ揺れており、「どこまでが人間の成果か」の定義は今後変わりえる。第三に、企業の予算が Bug Bounty から PTaaS / Red Team / ASM / AI Red Teaming へどの程度移るのかは、各社が採用費目を細かく出していない以上、まだ推定に依存する。

### 企業側の実務含意

VDP を全資産の入口にし、Bug Bounty は認可・ビジネスロジック・クラウド・AI アプリ・モバイルなど自動化しにくい領域へ集中させるのが合理的だ。その上で、CodeQL、Semgrep、Snyk、GitHub Advanced Security、ASM を前段に置き、BBP を「定番脆弱性の代替」ではなく「自動化で残った文脈依存リスクの捕捉装置」として設計するべきだ。AI 報告については、Apple 型の **proof-first** 方針を明文化し、duplicate 対策と triage SLA を強化しないと、プログラムの魅力は落ちる。

### ハンター側の実務含意

**「AI に全部やらせる」発想を捨てる**ことが最も重要だ。勝ち筋は、AI を recon、variant 探索、草稿作成、ドキュメント整理に使いながら、**人間の時間を認可、業務フロー、クラウド構成、exploit chain、AI アプリ固有の実害立証**に振り向けることだ。

専門領域としては、Web の基本問題よりも、API / Authorization / Business Logic / Cloud / Mobile / Kernel / Crypto / AI アプリのほうが、今後も報酬の厚みが残る可能性が高い。これは Google、Apple、HackerOne、Meta の公開データが示す方向と一致している。

要するに、**滅びるのは「ハンター」という職能ではなく、AI 以前の作業分解に依存した稼ぎ方**だ。今後の市場は、低難度の大量提出ではなく、高難度の文脈・証明・調整にお金を払い続けるだろう。だからこそ、この市場を正しく表す言葉は「滅び」ではなく、**再編**である。

## 関連 Wiki

- [Bug Bounty](/blogs/wiki/concepts/bug-bounty/) — BBP / VDP / VRP / PTaaS / Red Team / ASM の関係、主要プラットフォーム・VRP の統計、AI 時代の構造変化、制度面の整理
- [Exposure Management](/blogs/wiki/concepts/exposure-management/) — ASM の上位概念。BBP の前段として位置づけ
- [プロンプトインジェクション](/blogs/wiki/concepts/prompt-injection/) — HackerOne 2025 で valid report が +540% 急増した AI 固有脆弱性

## 参考一次資料

- HackerOne. [2025 Hacker-Powered Security Report — 210% spike in AI vulnerability reports](https://www.hackerone.com/press-release/hackerone-report-finds-210-spike-ai-vulnerability-reports-amid-rise-ai-autonomy)
- HackerOne. [Hackers community page (累計 $380M+、2M+ researchers)](https://www.hackerone.com/hackers)
- HackerOne. [Hackers surpass 300 million all-time earnings on HackerOne platform](https://www.hackerone.com/press-release/hackers-surpass-300-million-all-time-earnings-hackerone-platform)
- HackerOne. [Smart Deduplication with Agentic AI](https://www.hackerone.com/blog/smart-deduplication-agentic-ai)
- HackerOne. [2025 HPSR Researcher Signals](https://www.hackerone.com/blog/2025-hpsr-researcher-signals)
- HackerOne. [Hackers discover over 65,000 software flaws in 2022 (2022 Hacker-Powered Security Report)](https://www.hackerone.com/press-release/hackers-discover-over-65000-software-flaws-2022-according-hackerone-report)
- Bugcrowd. [Inside the Mind of a Hacker 2026 (82% が AI を利用)](https://www.bugcrowd.com/blog/inside-the-mind-of-a-hacker-2026/)
- Bugcrowd. [Industry's largest crowd of elite white hat hackers (2018 年 80,000 researchers)](https://www.bugcrowd.com/press-release/bugcrowd-deploys-industrys-largest-crowd-of-elite-white-hat-hackers/)
- Intigriti. [AI: The Future of Bug Bounty](https://www.intigriti.com/blog/business-insights/ai-future-of-bug-bounty)
- Intigriti. [Bug Bounty Calculator](https://www.intigriti.com/bug-bounty-calculator)
- YesWeHack. [Demand for crowdsourced security booms — YesWeHack bug bounty platform continues to thrive](https://www.yeswehack.com/news/demand-for-crowdsourced-security-booms-yeswehack-bug-bounty-platform-continues-to-thrive)
- Google Security Blog. [Vulnerability Reward Program: 2021 Year in Review](https://security.googleblog.com/2022/02/vulnerability-reward-program-2021-year.html)
- Google Security Blog. [Vulnerability Reward Program: 2022 Year in Review](https://security.googleblog.com/2023/02/vulnerability-reward-program-2022-year.html)
- Google Security Blog. [Vulnerability Reward Program: 2023 Year in Review](https://security.googleblog.com/2024/03/vulnerability-reward-program-2023-year.html)
- Google Blog. [Vulnerability Reward Program: 2024 Year in Review](https://blog.google/security/vulnerability-reward-program-2024-in/)
- Google Blog. [VRP 2025 Year in Review ($17.1M / 747 受賞研究者)](https://blog.google/security/vrp-2025-year-in-review/)
- Microsoft MSRC. [Microsoft Bug Bounty Program Year in Review: $13.8M in Rewards (2023)](https://www.microsoft.com/en-us/msrc/blog/2023/08/microsoft-bug-bounty-program-year-in-review-13-8m-in-rewards)
- Microsoft MSRC. [Microsoft Bounty Program Year in Review: $16.6M in Rewards (2024)](https://www.microsoft.com/en-us/msrc/blog/2024/08/microsoft-bounty-program-year-in-review-16-6m-in-rewards)
- Microsoft MSRC. [Microsoft Bounty Program Year in Review: 17 million in Rewards (2025)](https://www.microsoft.com/en-us/msrc/blog/2025/08/microsoft-bounty-program-year-in-review-17-million-in-rewards)
- Meta Engineering. [Looking back at our Bug Bounty Program in 2024](https://engineering.fb.com/2025/02/13/security/looking-back-at-our-bug-bounty-program-in-2024/)
- Apple Security. [Apple Security Bounty — Upgraded (2022 累計 $20M 近く)](https://security.apple.com/blog/apple-security-bounty-upgraded/)
- Apple Security. [Apple Security Bounty — Evolved (2025 累計 $35M+)](https://security.apple.com/blog/apple-security-bounty-evolved/)
- Apple Security. [Apple Security Bounty Guidelines (AI without proper validation の扱い)](https://security.apple.com/bounty/guidelines/)
- Apple Security. [Apple Security — Terms and Conditions](https://security.apple.com/terms-and-conditions/)
- DARPA. [Cyber Grand Challenge](https://www.darpa.mil/research/programs/cyber-grand-challenge)
- CISA. [BOD 20-01 — Develop and Publish a Vulnerability Disclosure Policy](https://www.cisa.gov/news-events/directives/bod-20-01-develop-and-publish-vulnerability-disclosure-policy)
- NIST. [SP 800-216 — Recommendations for Federal Vulnerability Disclosure Guidelines](https://csrc.nist.gov/pubs/sp/800/216/final)
- GitHub. [About secret scanning](https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning)
- CodeQL. [About CodeQL](https://codeql.github.com/docs/codeql-overview/about-codeql/)
- OSS-Fuzz. [Google OSS-Fuzz](https://google.github.io/oss-fuzz/)
- IPA. [脆弱性関連情報の取扱いに関する研究会報告書](https://www.ipa.go.jp/archive/files/000077982.pdf)
