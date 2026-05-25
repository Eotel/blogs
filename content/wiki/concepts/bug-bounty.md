---
title: "Bug Bounty"
description: "外部研究者に成果報酬で脆弱性発見を委ねる crowdsourced security モデル。VDP / VRP / PTaaS / Red Team / ASM など周辺モデルと多層に組み合わされる"
date: 2026-05-20
lastmod: 2026-05-20
aliases: ["バグバウンティ", "BBP", "Bug Bounty Program", "脆弱性報奨金"]
related_posts:
  - "/blogs/posts/2026/05/security-bounty-hunter-reorganization/"
tags: ["bug-bounty", "脆弱性開示", "VRP", "AppSec", "セキュリティ"]
---

## 概要

Bug Bounty Program (BBP) は、ベンダーが社外の研究者に**成果報酬**で未知の脆弱性発見を委ねる仕組み。HackerOne・Bugcrowd・Intigriti・YesWeHack などのプラットフォーム経由で運営される公開・招待制プログラムと、Google VRP・Microsoft Bounty・Apple Security Bounty・Meta Bug Bounty のようなベンダー直営の Vulnerability Reward Program (VRP) がある。

2025 年時点で HackerOne プラットフォームの bug bounty 支払いは年間 8,100 万ドル、Google VRP は 1,710 万ドル、Microsoft Bounty は 1,700 万ドル、Apple は 2020 年以降の累計 3,500 万ドル超を公表しており、市場全体は縮小していない。一方で AI による低品質報告の流入、重複爆発、検証ボトルネック顕在化により、**従来型の「Web 定番バグを拾って稼ぐ個人ハンター」モデル**は急速に再編されている。

## 周辺モデルとの違い

BBP は単独で機能するというより、他の crowdsourced / managed security サービスと組み合わされる。

| モデル | 主目的 | 支払い形態 | 期間 |
|---|---|---|---|
| **Bug Bounty (BBP)** | 未知の実害ある脆弱性の継続発見 | 成果報酬 | 継続 |
| **VDP** (Vulnerability Disclosure Policy) | 安全な報告窓口と受理プロセス | 通常無償、謝辞中心 | 継続 |
| **VRP** (Vendor Reward Program) | ベンダー製品の高影響脆弱性奨励 | 報奨金 | 継続 |
| **Pentest** | 期間限定の体系的評価 | 工数課金 | 時限 |
| **Red Team** | 攻撃者模倣による目的達成演習 | 工数・成果混合 | 時限 |
| **PTaaS** (Pentest as a Service) | 継続的に pentest を再現 | サブスク + 成果 | 継続 |
| **ASM** (Attack Surface Management) | 攻撃面の発見と把握 | サブスク中心 | 継続 |

VDP は「報奨は出ないが安全な報告経路は約束する」もので、CISA BOD 20-01 (2020) は米連邦機関に VDP の整備・公表を義務付けた。NIST SP 800-216 (2023 final) は受理・評価・連絡・修正・開示のフレームワークを示している。

## 主要プラットフォーム

| プラットフォーム | 規模・特徴 |
|---|---|
| **HackerOne** | 累計 $380M+、bug bounty 2025 年支払い $81M (+13% YoY)、AI dedupe で 92% に duplicate recommendation・80–95% positive accuracy |
| **Bugcrowd** | Inside the Mind of a Hacker 2026 で 2,000+ hackers を調査、**82% が AI をワークフローに活用**と報告 |
| **Intigriti** | 640+ public bug bounty programs / 18 業種を分析、Bug Bounty Calculator で価格ベンチマークを開示 |
| **YesWeHack** | 2022 年 35,000+ hackers → 2026 年 約 130,000 hunters、受理後 24 時間以内報奨 78% |

## 主要 VRP の年次推移

| 企業 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Google VRP | $8.7M | $12M+ | — | 約 $12M (600+ 研究者) | **$17.1M (747 研究者)** |
| Microsoft Bounty | — | — | $13.8M (345+) | $16.6M (343) | **$17M (344)** |
| Meta Bug Bounty | — | — | — | **$2.3M+ / 10,000 報告 / 600 valid** | — |
| Apple Security Bounty | — | 累計 $20M 近く | — | — | **累計 $35M+ / 800+ 研究者** |

Meta は 2024 年に「nearly 10,000 bug reports / nearly 600 valid reports」と総数と有効数を併記して公開している例外的なケースで（valid 比率は wiki 側の概算で約 6%）、**重複・無効・範囲外を含む負荷の大きさ**を直接読み取れる。

## AI 時代の構造変化

- **発見の母数は増えるが、検証のボトルネックが顕在化**: Intigriti は 2026 年のブログで、引用した Chris Holt の言葉として「the top-of-funnel widens faster than most programs can absorb, and the duplication surface area explodes」と紹介し、続けて編集側の論として「the bottleneck shifts to validation, prioritization, and trust」と公式に述べている。
- **未検証 AI 報告は不適格化**: Apple は guidelines で「AI without proper validation」の理論問題を不適格とし、繰り返せば 180 日 processing pause、複数回なら永久排除もありうると明記。
- **AI 固有スコープの拡大**: HackerOne 2025 で **AI report +210%、prompt injection +540%、自律エージェントによる valid report 560+**。Google は dedicated AI VRP、Meta は LLM の model inversion / extraction を正式スコープに含めた。
- **再価格付け**: Chrome VRP では 2022 → 2024 で reports 数は 470 → 337 と減ったが、参考平均報奨は約 $8.5k → $10.1k に上昇。低難度の量産から高難度の少数精鋭にシフトしている。

## 報酬が残りやすい技術領域

AI 代替性の低い領域に報酬が集中する傾向がある。

- **認可 / IDOR / Business Logic** — Intigriti は「edge cases・contextual abuse は人間領域」と述べる
- **クラウド設定連鎖 / Kubernetes** — Google Cloud VRP は 400+ triaged / 200+ unique
- **Mobile / Kernel / exploit chain** — Apple は exploit chain で最大 $2M、ボーナス込み $5M 超を提示
- **Crypto / Web3** — 2022 年に平均支払いが $6,443 → $26,728 (+315%) に上昇
- **AI アプリ固有脆弱性** — 入口は広いが、impact proof で差がつく

## 制度面

bug bounty は法的な無条件免責ではない。プログラム scope と safe harbor の範囲内でのみ有効。

- **CISA BOD 20-01** (2020): 米連邦機関に VDP 公表を義務付け
- **NIST SP 800-216** (2023 final): VDP の受理・評価・連絡・修正・開示フレームワーク
- **DOJ CFAA 起訴方針改定** (2022): good-faith security research を起訴対象から外す方針を明確化
- **Apple terms**: 対象外システムへのアクセス、第三者サービスへの攻撃、過度な disruption、修正前の公開は禁止、報奨は **first complete and actionable report** のみ
- **日本**: IPA / JVN とベンダー窓口、グローバルプラットフォーム窓口が並立。どの窓口に出すかは事前確認が必要

## 関連ページ

- [Exposure Management](/blogs/wiki/concepts/exposure-management/) — ASM の上位概念。BBP は自動化で残った文脈依存リスクの捕捉装置として位置付けると合理的
- [プロンプトインジェクション](/blogs/wiki/concepts/prompt-injection/) — HackerOne 2025 で valid report +540% と急増している AI 固有脆弱性
- [AI エージェント](/blogs/wiki/concepts/ai-agent/) — HackerOne の 560+ autonomous valid reports を提出した自律エージェントの背景

## ソース記事

- [バグバウンティは本当に終わったのか — HackerOne・Google・Apple の一次資料で読む 2026 年の再編](/blogs/posts/2026/05/security-bounty-hunter-reorganization/) — 2026-05-20
