---
title: "DESIGN.md という文化 — AI エージェントに「ブランドの見た目」を渡す共通フォーマット"
date: 2026-05-11
lastmod: 2026-05-11
draft: false
author: "eotel"
description: "Google Labs が 2026 年 4 月に公開した DESIGN.md の仕様を起点に、AGENTS.md / SKILL.md と並ぶ「外観の SSoT」がどのように立ち上がりつつあるかを整理。refero.design や designmd.app のようなカタログサイト、Impeccable のような上位レイヤ、そして本ブログ (Hugo + PaperMod) に DESIGN.md を置くならどう書くか、までを一本でまとめる。"
categories: ["AI/LLM"]
tags: ["design.md", "agents.md", "skill.md", "claude-code", "design-system", "agent"]
---

エージェントがコードを書けるようになって、次に困るのは「見た目」だ。仕様書のとおりに動くアプリは作れても、出てくる画面はどこか **AI 臭い**。色は派手で、角丸は強すぎ、余白は均一、ヒエラルキーは平坦 — Trilogy AI が「[Visual AI slop](https://trilogyai.substack.com/p/fixing-visual-ai-slop)」と呼んだ症状だ。

この症状の処方箋として、2026 年に入って一気に勢力を伸ばしているのが **DESIGN.md** という文化である。AGENTS.md（振る舞い）と SKILL.md（タスク）に続く第三の `.md` で、コーディングエージェントに「ブランドの見た目」を渡すための共通フォーマット。Google Labs が 4 月 10 日に公式リポジトリ [`google-labs-code/design.md`](https://github.com/google-labs-code/design.md) を Apache-2.0 で公開してから 1 か月で、配布カタログ、検証 CLI、語彙レイヤを含めたエコシステムがすでに動き始めている。

本記事では、Google Labs 仕様の中身、AGENTS.md / SKILL.md との 3 層関係、Impeccable のような上位レイヤ、DESIGN.md カタログサイトのマップ、そして最後に「本ブログ (Hugo + PaperMod) に DESIGN.md を置くなら何を書くか」というサンプル節までを一本にまとめる。

![AGENTS.md / SKILL.md / DESIGN.md という 3 つの指示書が、Claude Code や Cursor などのエージェントを介して最終的なアプリ UI に流れ込む構造を示す概念図。](/blogs/images/design-md-three-layers.png)

## DESIGN.md の中身 — YAML トークン × Markdown 散文の二層構造

Google Labs 版 DESIGN.md は、現時点で **v0.1.0 alpha**（2026-04-21）として公開されている。ファイル名は大文字の `DESIGN.md` が正式表記で、構造はシンプルな二層になっている。

- 上半分は **YAML front matter** — 機械可読のトークン (colors / typography / spacing / rounded / components)
- 下半分は **Markdown 本文** — 人間とエージェントの両方が読む散文 (Overview / Colors / Typography / Layout / Elevation & Depth / Shapes / Components / Do's and Don'ts という正規順)

公式の最小サンプルから抜粋すると、こんな見た目になる。

```markdown
---
name: Heritage
colors:
  primary: "#1A1C1E"
  tertiary: "#B8422E"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
---

## Overview
Architectural Minimalism meets Journalistic Gravitas.

## Colors
- **Primary**: Deep ink for headlines
```

注目したいのは `{colors.tertiary}` のような **トークン参照記法** だ。これによって components ブロックがそのまま CSS 変数や Tailwind の theme と等価な「設計トークンのソース」になる。`tailwind.config.js` を書かずに、Markdown 一枚に閉じる。ビルドパイプラインも要らない。エージェントは front matter を読んでトークンを「事実」として扱い、Markdown 本文を読んで「意図」を読み取る。

検証 CLI は `npx @google/design.md` で動く。

```bash
# 構造を検証
npx @google/design.md lint DESIGN.md

# バージョン間差分
npx @google/design.md diff old.md new.md

# Tailwind / CSS への書き出し
npx @google/design.md export DESIGN.md --format tailwind
```

「DESIGN.md は仕様書ではなくランタイム」という思想がここに表れている。`lint` と `diff` と `export` が標準装備されていることで、デザイントークンの変更が PR レビューでレビュアブルになる。`design.md` は **ドキュメントというより設定ファイルに近い** 位置を狙っていると言える。

## なぜ Markdown なのか — AGENTS.md / SKILL.md との 3 層

Markdown でデザインシステムを書くという発想は、いきなり出てきたわけではない。2025 年から 2026 年にかけて、エージェントに渡す指示書は次のように **役割で分裂** してきた。

| ファイル | 何の SSoT か | 主導 | 出自 |
|---|---|---|---|
| `AGENTS.md` | エージェントの振る舞い（役割・禁止事項・エスカレーション基準） | OpenAI / Google / Sourcegraph / Cursor / Factory | 2025 年に共同策定、12 月に Linux Foundation 寄贈 |
| `SKILL.md` | 個別タスクの能力（再利用可能なスキル定義） | Anthropic | Claude Skills のコア、AWS Agent Toolkit / Strands Agents にも流入 |
| `DESIGN.md` | 外観の SSoT（ビジュアルアイデンティティ） | Google Labs | 2026 年 4 月公開、Apache-2.0 |

The GitHub Blog の [Spec-driven development: Using Markdown as a programming language](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-using-markdown-as-a-programming-language-when-building-with-ai/) が指摘するとおり、**Markdown は人間とエージェントの両方が読める唯一の中庸フォーマット** だ。JSON にすると人間が読まなくなり、純粋な散文にするとエージェントが構造を取りこぼす。front matter の YAML と本文の散文を併走させる二層構造は、3 つの `.md` に共通する設計思想になっている。

仕様駆動開発 (SDD) の文脈では、`requirements.md` / `design.md` / `tasks.md` という 3 層が Kiro 由来で広まった（参照: [Claude Code 時代の仕様書の役割](/blogs/posts/2026/03/2026-03-10-claude-code-spec-driven-dev/)）。そちらの `design.md` は「アーキテクチャ設計書」を指していて、Google Labs の `DESIGN.md`（ビジュアルアイデンティティ）とは別物だ。ややこしいが、両者は補完関係にある — アーキテクチャ設計の `design.md` が「どう作るか」、ビジュアル設計の `DESIGN.md` が「どう見せるか」を分担する。

ハーネスエンジニアリングの観点で言えば、`CLAUDE.md` / `MEMORY.md` / `SKILL.md` の 4 層 SSoT（[ハーネスエンジニアリング](/blogs/wiki/concepts/harness-engineering/) 参照）に、`DESIGN.md` が **第 4〜5 の層** として加わったと整理できる。エージェントは「自分は誰か (AGENTS.md)」「何ができるか (SKILL.md)」「どう見えるか (DESIGN.md)」を Markdown で渡される世界に近づいている。

## Impeccable — DESIGN.md の上に乗る「設計語彙レイヤ」

DESIGN.md が辞書なら、その上に文法を載せたのが [Impeccable](https://github.com/pbakaus/impeccable) だ。Paul Bakaus（元 Google、ex-jQuery UI コアメンテナ）が公開した OSS で、すでに 10,000 stars を超えている。

- 「コンポーネントライブラリでも CSS テーマでもない」と作者は明言している
- 「あなたの意図とエージェントの実行のあいだに挟まる **設計語彙レイヤ** (vocabulary layer)」と位置づけている
- 2 モード: **brand**（デザイン = プロダクト本体: 広告 / ポートフォリオ / 編集系）と **product**（デザイン = プロダクトの補助: アプリ UI / ダッシュボード）
- 20 個の slash command が「設計の文法」を構成し、`/audit` `/refine` `/document` のように直接エージェントを呼び出して使う
- Anthropic の `frontend-design` skill を 7 種のドメイン参照ファイルで拡張する形を取る

導入時にハーネスごとのフォルダ (`.cursor/` `.claude/` `.gemini/` `.codex/` `.agents/` `.github/`) を一括で生成し、どのエージェントからでも同じ語彙が使える。さらに `.impeccable.md` がプロジェクト固有の文脈を自動収集する役を担い、**`DESIGN.md` が見当たらなければ `/document` コマンドで既存コードから seed を起こす** という再帰的な使い方ができる。

雑にまとめると、DESIGN.md が **「色 #1A1C1E / フォント Public Sans」のような事実の塊** なら、Impeccable は **「Visual Hierarchy を保て / Typography を一段ずつ離せ」のようなルールの塊** だ。両者は競合せず、Impeccable が DESIGN.md を読み込んで `/audit` を走らせると、AI Slop が事前に検出できる、というのが現状の到達点である。

## DESIGN.md カタログサイト一覧 — 「ブランドの配布マーケット」が立ち上がる

Google Labs が仕様を公開した数週間後から、**「DESIGN.md を配るサイト」** が複数立ち上がっている。CSS フレームワーク → デザインシステム → コンポーネントライブラリ、と続いたデザイン配布の歴史に、`.md` 一枚の世代が加わったかたちだ。

| サイト / リポジトリ | 内容 | 特徴 |
|---|---|---|
| [`designmd.app/library`](https://designmd.app/library/) | 454+ DESIGN.md コレクション | 公式リファレンス的、Google Labs と整合 |
| [`styles.refero.design`](https://styles.refero.design/) | Refero ライブラリ由来、URL / ブランドからスタイルを抽出 | スクリーンショット起点。`?q=clean+SaaS` のような検索で DESIGN.md をダウンロード可能 |
| [`designmd.ai`](https://designmd.ai/) | コミュニティ系 DESIGN.md コレクション | Cursor / Claude Code 対応をうたう |
| [`getdesign.md`](https://getdesign.md/) | AI コーディングエージェント向け DESIGN.md コレクション | カテゴリ別に整理 |
| [`VoltAgent/awesome-design-md`](https://github.com/voltagent/awesome-design-md) | 55+ サイトの reverse-engineered DESIGN.md | dev-focused サイトのトーンを再現する用途 |
| [`kzhrknt/awesome-design-md-jp`](https://github.com/kzhrknt/awesome-design-md-jp) | 日本語 / CJK 対応の DESIGN.md コレクション | 縦書きや行間のチューニングを含む |

**refero.design** はもともと UI/UX のスクリーンショットライブラリとして大規模なカタログを持っていたサービスで、その派生として `styles.refero.design` が DESIGN.md の自動生成・配布に振り切った。本記事の起点も「`?q=clean+SaaS` で出てくる styles を `DESIGN.md` として落として使えるのか」という素朴な発見だった。`color / type / spacing / components` が画面付きで一覧でき、そこから DESIGN.md と「エージェントが使える Markdown」をダウンロードできる。デザインリファレンスがそのままエージェント向けのインプットになる構造だ。

加えて 2026 年 3 月リリースの **Google Stitch**（Google 製の AI デザインツール）は DESIGN.md を一級市民として読む。つまり「カタログサイトで DESIGN.md を見つけて → Stitch で画面を生成」というラインがそのまま開通しているわけで、**ブランドの配布マーケットがすでにフロー化している** ことになる。

![ブランドや SaaS のスクリーンショットから refero / designmd.app / awesome-design-md などのカタログを経て DESIGN.md が抽出され、Impeccable のような語彙レイヤを介して Claude Code / Cursor / Kiro / Windsurf / Google Stitch といったエージェントに流れ込む流通図。](/blogs/images/design-md-distribution-flow.png)

懸念は少なくない。reverse-engineered DESIGN.md は本質的に **トレードドレスのリバースエンジニアリング** であり、有名 SaaS のスタイルを「公式が許諾していないルート」で配るのに近い。Tailwind UI や shadcn/ui がコンポーネントレベルで起こした議論が、トークンレベルで再演される可能性が高い。

## 批判と限界 — スペック化できないもの

DESIGN.md を礼賛するだけで終わらせない、批判の視点もまとめておく。

- **すべてはスペック化できない**: 色やスペーシングは数値化できる。だがブランドの「トーン」「文化的ニュアンス」「物語の構造」までは Markdown で言語化しきれない。dev.to の [AGENTS.md, SKILL.md, DESIGN.md レビュー記事](https://dev.to/aws-builders/agentsmd-skillmd-designmd-how-ai-instructions-split-into-three-layers-d0g) は、検証可能性 (verifiable) で線を引くべきだと主張している。
- **小規模チームには重い**: 個人プロジェクトでは `CLAUDE.md` に 30 行書けば十分というケースが多い。3 つの `.md` を律儀に維持する負荷は、チーム規模に比例しない。
- **alpha 仕様の不安定さ**: v0.1.0 alpha 段階の語彙は今後 breaking change が入る前提で扱うべきで、自動生成された DESIGN.md を依存先ライブラリのようにバージョン pinning する運用が要る。
- **Hugo / Next.js のテーマ市場との衝突**: テーマやデザインシステムの「販売」が長年してきた仕事を、`.md` 一枚に圧縮するムーブメントでもある。社会学的に見れば、デザインのコモディティ化を加速させるアクターでもある。

## 本ブログに DESIGN.md を置くなら（サンプル節）

最後に、本ブログ（Hugo + PaperMod、`baseURL = 'https://eotel.github.io/blogs/'`、`defaultContentLanguage = 'ja'`、`defaultTheme = 'auto'`）に DESIGN.md を置くなら何を書くかを考えてみる。

このブログの実情は概ねこうだ。

- 日本語比率がおおむね 7 割以上
- コードブロックが多く、等幅フォントの可読性を優先
- ライト / ダーク自動切替、デフォルトは OS 設定に従う
- 図は drawio で書いて PNG 化、本文中で `/blogs/images/...` を絶対パス参照
- 1 記事 1500〜3000 字想定、`tags` で SEO を取り、内部リンクで Wiki と接続

これを最小の DESIGN.md にすると、たとえば次のようになる。

```markdown
---
name: Eotel blog
description: 日本語比率の高い技術ブログ。Hugo + PaperMod、ダーク優先、コード優先。
colors:
  bg: "#1d1e20"
  bg-light: "#ffffff"
  fg: "#e8eaed"
  fg-light: "#1f1f1f"
  accent: "#3367d6"
  code-bg: "#2b2c2f"
typography:
  body:
    fontFamily: "system-ui, -apple-system, 'Helvetica Neue', 'Hiragino Sans', sans-serif"
    fontSize: 1rem
    lineHeight: 1.75
  code:
    fontFamily: "ui-monospace, 'SF Mono', 'JetBrains Mono', monospace"
    fontSize: 0.92rem
spacing:
  scale: [4, 8, 12, 16, 24, 32, 48]
rounded:
  card: 6
  button: 4
components:
  link:
    color: "{colors.accent}"
    textDecoration: underline-dotted
  code-block:
    backgroundColor: "{colors.code-bg}"
    padding: "{spacing.3}"
---

## Overview

技術記事を「コードと図」中心で読む読者を想定する。装飾は最小、ヒエラルキーは控えめ。
日本語の縦組み感（行間 1.75）を保ち、Markdown の見出しは段差を 1 段ずつ取る。

## Do's and Don'ts

- ✅ 引用は左寄せボーダー、本文と地続きにする
- ✅ コードブロックは横スクロール可、折り返し禁止
- ❌ アスキーアートでの図示は禁止（drawio + PNG を使う）
- ❌ 派手なアクセントカラーで本文を装飾しない
```

これを `static/DESIGN.md` に置くか、リポジトリ直下 `/DESIGN.md` に置くかで挙動が変わる。エージェントが拾いやすいのは **リポジトリ直下** だ。Claude Code は `CLAUDE.md` と同様に「ルートの大文字 `.md`」を優先的に読み込むため、`/DESIGN.md` のほうがロード対象になりやすい。

検証は `npx @google/design.md lint DESIGN.md` で通る。テーマ拡張（PaperMod の `assets/css/extended/` への反映）は当然別仕事だが、`DESIGN.md` 側を SSoT にしておけば、CSS 側の手書きと「ぶれた」ときにレビューで止められる。ここを実装する話は別記事に譲りたい。

## まとめ — Markdown がブランドの配布フォーマットになる

AGENTS.md（振る舞い）、SKILL.md（能力）、DESIGN.md（外観）。この 3 枚で、エージェントに渡る情報がきれいに分業されつつある。Markdown は **モデル更新に追従できる唯一のドキュメント形式** で、Claude や GPT のバージョン交代でも陳腐化しない。`.md` 一枚で「ブランドの見た目」を配るという発想は、CSS フレームワーク・デザインシステム・コンポーネントライブラリの系譜に次ぐ世代の入口に見える。

次に来そうな 4 枚目の `.md` を勝手に予想するなら、`VOICE.md`（ブランドボイス・トーン）か `VALUES.md`（プロダクト原則）あたりだろうか。Markdown が「設計の単位」になっていく流れは、しばらく止まりそうにない。

## 参考リンク

- [google-labs-code/design.md](https://github.com/google-labs-code/design.md) — 公式仕様 v0.1.0 (Apache-2.0)
- [designmd.app — DESIGN.md Library](https://designmd.app/library/) — 454+ デザインシステム
- [styles.refero.design](https://styles.refero.design/) — Refero スタイル抽出版（本記事の起点）
- [getdesign.md](https://getdesign.md/) — DESIGN.md コレクション
- [VoltAgent/awesome-design-md](https://github.com/voltagent/awesome-design-md) — 55+ サイトの reverse-engineered DESIGN.md
- [kzhrknt/awesome-design-md-jp](https://github.com/kzhrknt/awesome-design-md-jp) — CJK 対応
- [pbakaus/impeccable](https://github.com/pbakaus/impeccable) / [impeccable.style](https://impeccable.style/) — 設計語彙レイヤ
- [DESIGN.md Explained — Department of Product](https://departmentofproduct.substack.com/p/designmd-explained-the-format-reshaping)
- [Fixing Visual AI Slop — Trilogy AI](https://trilogyai.substack.com/p/fixing-visual-ai-slop)
- [AGENTS.md, SKILL.md, DESIGN.md — dev.to](https://dev.to/aws-builders/agentsmd-skillmd-designmd-how-ai-instructions-split-into-three-layers-d0g)
- [Spec-driven development with Markdown — The GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-using-markdown-as-a-programming-language-when-building-with-ai/)

## 関連 Wiki / 関連記事

- [ハーネスエンジニアリング (concept)](/blogs/wiki/concepts/harness-engineering/) — 4 層 SSoT 設計
- [Agent Skills フォーマット (concept)](/blogs/wiki/concepts/agent-skills-format/) — SKILL.md の標準化
- [Claude Code (tool)](/blogs/wiki/tools/claude-code/) — Claude Code が読む `.md` 群
- [Claude Harness (tool)](/blogs/wiki/tools/claude-harness/) — harness.toml の SSoT 思想
- [Claude Code 時代の仕様書の役割 (post)](/blogs/posts/2026/03/2026-03-10-claude-code-spec-driven-dev/) — requirements/design/tasks の 3 層
- [Anthropic の 3 エージェント・ハーネス設計 (post)](/blogs/posts/2026/03/2026-03-27-anthropic-harness-design-three-agents/) — Planner / Generator / Evaluator
- [ハーネスエンジニアリングとは (post)](/blogs/posts/2026/03/2026-03-09-harness-engineering/) — 基礎概念
