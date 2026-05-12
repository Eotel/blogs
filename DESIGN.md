---
name: Eotel's Notebook
description: A hypertext garden. Posts, notes, and wiki by Eotel.
colors:
  iron-sienna: "#a64a2c"
  iron-sienna-soft: "#c46a4a"
  iron-sienna-deep: "#7a3520"
  parchment: "#f6f3ee"
  parchment-warm: "#efeae1"
  parchment-edge: "#e2dccf"
  ink-graphite: "#221f1c"
  ink-graphite-soft: "#3d3934"
  ink-secondary: "#6b6660"
  ink-muted: "#a8a29a"
  ink-divider: "#d8d2c6"
  code-slab-dark: "#1c1a18"
  code-inline-bg: "#ece6d8"
  parchment-dark: "#211f1c"
  parchment-dark-card: "#2c2925"
  parchment-dark-edge: "#3a352f"
  ink-graphite-dark: "#ece6d8"
  ink-secondary-dark: "#a8a29a"
  ink-muted-dark: "#6b6660"
  ink-divider-dark: "#3a352f"
  code-slab-dark-mode: "#2c2925"
  code-inline-bg-dark: "#3a352f"
  iron-sienna-dark: "#d77a55"
typography:
  display:
    fontFamily: "'Newsreader', ui-serif, 'Iowan Old Style', Georgia, 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif"
    fontSize: "clamp(2rem, 4.5vw, 3rem)"
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  display-italic:
    fontFamily: "'Newsreader', ui-serif, 'Iowan Old Style', Georgia, 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif"
    fontSize: "clamp(2rem, 4.5vw, 3rem)"
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "'Newsreader', ui-serif, 'Iowan Old Style', Georgia, 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif"
    fontSize: "clamp(1.5rem, 2.5vw, 2rem)"
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: "-0.005em"
  title:
    fontFamily: "'Newsreader', ui-serif, 'Iowan Old Style', Georgia, 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif"
    fontSize: "1.375rem"
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: "normal"
  body:
    fontFamily: "'Newsreader', ui-serif, 'Iowan Old Style', Georgia, 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: "normal"
  ui:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Hiragino Sans', 'Yu Gothic UI', Roboto, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Hiragino Sans', 'Yu Gothic UI', Roboto, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0.01em"
  code:
    fontFamily: "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Monaco, Consolas, 'Liberation Mono', monospace"
    fontSize: "0.86em"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
rounded:
  sharp: "2px"
  default: "4px"
  pill: "999px"
spacing:
  row-gap: "28px"
  content-gap: "20px"
  gap: "24px"
  gap-2x: "48px"
  section-gap: "64px"
components:
  body-surface:
    backgroundColor: "{colors.parchment}"
    textColor: "{colors.ink-graphite}"
    typography: "{typography.body}"
  masthead-title:
    textColor: "{colors.ink-graphite}"
    typography: "{typography.display-italic}"
  masthead-subtitle:
    textColor: "{colors.ink-secondary}"
    typography: "{typography.ui}"
  masthead-rule:
    backgroundColor: "{colors.iron-sienna}"
    height: "2px"
    width: "48px"
  post-row:
    backgroundColor: "transparent"
    textColor: "{colors.ink-graphite}"
    padding: "0 0 28px 0"
  post-row-hero:
    backgroundColor: "transparent"
    textColor: "{colors.ink-graphite}"
    padding: "0 0 36px 0"
  post-row-title:
    textColor: "{colors.ink-graphite}"
    typography: "{typography.title}"
  post-row-title-hero:
    textColor: "{colors.ink-graphite}"
    typography: "{typography.headline}"
  post-row-meta:
    textColor: "{colors.ink-secondary}"
    typography: "{typography.label}"
  post-row-divider:
    backgroundColor: "{colors.ink-divider}"
    height: "1px"
  link-ink:
    textColor: "{colors.iron-sienna}"
  link-ink-hover:
    textColor: "{colors.iron-sienna-deep}"
  index-strip:
    backgroundColor: "transparent"
    textColor: "{colors.ink-graphite}"
    padding: "0"
  index-strip-section:
    textColor: "{colors.ink-secondary}"
    typography: "{typography.label}"
  index-strip-entry:
    textColor: "{colors.ink-graphite}"
    typography: "{typography.ui}"
  tag-flow-entry:
    textColor: "{colors.ink-secondary}"
    typography: "{typography.ui}"
  pagination-button:
    backgroundColor: "transparent"
    textColor: "{colors.iron-sienna}"
    rounded: "{rounded.pill}"
    padding: "10px 20px"
  code-block:
    backgroundColor: "{colors.code-slab-dark}"
    textColor: "#e5dfd0"
    rounded: "{rounded.default}"
    padding: "14px 16px"
  code-inline:
    backgroundColor: "{colors.code-inline-bg}"
    textColor: "{colors.ink-graphite}"
    rounded: "{rounded.sharp}"
    padding: "2px 6px"
    typography: "{typography.code}"
  toc:
    backgroundColor: "{colors.parchment-warm}"
    textColor: "{colors.ink-graphite}"
    rounded: "{rounded.default}"
    padding: "12px 16px"
  keyword-link:
    textColor: "{colors.iron-sienna}"
  blockquote:
    textColor: "{colors.ink-graphite-soft}"
    padding: "0 18px"
  hdknr-chip:
    backgroundColor: "transparent"
    textColor: "{colors.ink-muted}"
    typography: "{typography.label}"
---

# Design System: Eotel's Notebook

## 1. Overview

**Creative North Star: "The Hypertext Garden"**

Eotel's Notebook は「丁寧に組まれた、すべてが互いにリンクし合う、作業中のノートブック」として現れる。Medium 級の serif typography、フィルムで撮ったような grain を持つ warm parchment の地、たった 1 色の朱いインク (Iron Sienna)、そして Scrapbox 並みのリンク密度 — この 4 つだけでサイト全体のシグネチャを構成する。

このシステムは digital garden、TIL (Today I Learned)、learn-in-public の系譜に属する。Maggie Appleton の sienna ink、Andy Matuschak の working notes の側脈構造、Stripe Press の grain がかった本文、Robin Sloan の内輪の声、Are.na の「block は複数の channel に所属する」モデル、Scrapbox の bracket-link 密度 — これらの DNA を取り込んだ上で、日本語の Mincho 系フォールバックと、Hugo + 静的サイトの素朴さで束ねる。

このシステムが拒否するもの:

- SaaS ランディング風の巨大ヒーロー、グラデーション CTA、追従ソーシャル共有ボタン。
- 「ハッカー感」の演出としてのネオン緑ターミナル風配色、紫グラデと光彩エフェクトの「AI ブログ」テンプレ。
- Qiita / Zenn 風の等寸カード 3 列グリッド一覧。
- pure `#ffffff` の薄っぺらい紙地、pure `#000000` の冷たい背景。
- 装飾的グラスモーフィズム、グラデーションテキスト、横ストライプの飾りボーダー。
- 個人テックブログの "PaperMod デフォルトのまま" の見た目。

**Key Characteristics:**

- たった 1 色 (**Iron Sienna**) を全リンク・キーワード・見出し下線に通す One-Ink design。
- 地は warm parchment (`#f6f3ee` / dark: `#211f1c`)、その上に薄い SVG 由来 grain が overlay する。Pure white / pure black は使わない。
- Display + Body 共に **Newsreader** serif variable font。日本語は Hiragino Mincho ProN → Yu Mincho → Noto Serif CJK JP の Mincho stack にフォールバック。
- 一覧は card を捨て、横罫線 1px + 縦余白 28px のデンスな post-row で組む。
- 全 post / Wiki page が双方向リンクされた網の中の 1 ノード。"Linked from" / "Related in Wiki" / "More in <category>" を末尾に常設。
- UI chrome (nav / meta / chip / pagination) は system sans を残し、本文 serif との 2 系統で組む。

## 2. Colors

たった 1 色の朱いインクが、warm parchment と graphite ink の間を縫う。多色は使わない。

### Primary

- **Iron Sienna** (`#a64a2c`, `oklch(48% 0.13 35)`): 全リンクの文字色、`.kw-link` の dotted underline、masthead の rule 48px、active nav の下線、見出しのキッカー下線、blockquote の薄い縦線 (light mode)、`Linked from` セクション見出しの色。サイト全体に通る唯一のインク。
- **Iron Sienna Soft** (`#c46a4a`): 静かな状態の `.kw-link` underline 半透明扱い用。`color-mix` で 60% 透明にしても代替可。
- **Iron Sienna Deep** (`#7a3520`): hover 時のインク。深く沈める。
- **Iron Sienna (Dark Mode)** (`#d77a55`, `oklch(65% 0.13 35)`): ダークモードでは明度を持ち上げて parchment-dark との contrast を保つ。

### Neutral (Light)

- **Parchment** (`#f6f3ee`, `oklch(96% 0.008 80)`): 主たる紙地。SVG grain overlay と組んで初めて完成する。
- **Parchment Warm** (`#efeae1`): TOC や aside の沈み紙。
- **Parchment Edge** (`#e2dccf`): 微弱な分割面。
- **Ink Graphite** (`#221f1c`): 本文の文字色。pure black の代替。
- **Ink Graphite Soft** (`#3d3934`): blockquote 内本文、二次見出し。
- **Ink Secondary** (`#6b6660`): meta、サブタイトル、divider 上の小ラベル。
- **Ink Muted** (`#a8a29a`): hdknr チップ、非表示寸前の微小ラベル。
- **Ink Divider** (`#d8d2c6`): 横罫線 1px 専用色。

### Neutral (Dark)

- **Parchment Dark** (`#211f1c`): 灯下の紙の地。
- **Parchment Dark Card** (`#2c2925`): TOC や aside の沈み紙 (dark)。
- **Parchment Dark Edge** (`#3a352f`): 微弱な分割面 (dark)。
- **Ink Graphite (Dark)** (`#ece6d8`): 本文。
- **Ink Secondary (Dark)** (`#a8a29a`): meta。
- **Ink Muted (Dark)** (`#6b6660`): 微小ラベル。
- **Ink Divider (Dark)** (`#3a352f`): 罫線。

### Code Slab

- **Code Slab Dark** (`#1c1a18`): light モードでも常に暗いコードブロック背景。warm parchment 上で最も重い面。
- **Code Slab (Dark Mode)** (`#2c2925`): dark モードでは紙地より一段明るい層。
- **Code Inline Bg** (`#ece6d8` / `#3a352f`): 地の文に埋め込まれた `code` のグレイ。warm-tinted。

### Named Rules

**The One-Ink Rule.** サイト全体で使う「色」は Iron Sienna のたった 1 色だけ。それ以外はすべて parchment と ink graphite のニュートラル階調。リンク・キーワード・active nav・見出し下線・blockquote 縦線 — どこに使っても同じインク。category ごとに色を変えるな、tag ごとに色を変えるな、AI 記事だけ紫にするな。インクが 1 本しかないノートだと思え。

**The Warm-Parchment Default.** 新規 CSS で背景に `#ffffff` を書かない。`#000000` も書かない。light は `#f6f3ee` (Parchment)、dark は `#211f1c` (Parchment Dark)。pure white は old PaperMod 由来の互換のためにだけ残し、新規面では使わない。

**The Code Slab Stays Dark Rule.** コードブロックは light/dark どちらでも暗いまま。light モードでは warm parchment の上に `#1c1a18` の重いスラブが浮く。これがページの中で唯一の「黒に近い面」。

### Background Grain (新規)

地は単色 fill ではない。SVG `feTurbulence` (baseFrequency 0.9, numOctaves 1, type fractalNoise) を生成し、`mix-blend-mode: multiply` で 4% 強度の grain として body 全体に overlay する。dark モードでも同形の grain を 5% で乗せる。`prefers-reduced-motion` でも grain は静止画なので影響しない。

## 3. Typography

**Display + Body Font:** `'Newsreader', ui-serif, 'Iowan Old Style', Georgia, 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif`

Newsreader (Production Type) は screen-first の serif variable font。weight 200–800 / italic axis 付き。Latin subset を web font として 1 ファイル読み込み (~50KB)、日本語は OS の Mincho stack にフォールバックする。`font-display: swap` で CLS を吸収する。

**UI Sans Font:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Hiragino Sans', 'Yu Gothic UI', Roboto, sans-serif`

nav、post meta、chip、pagination、figcaption、aside small は system sans を残す。serif body との 2 系統で組む。

**Mono Font:** `ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Monaco, Consolas, 'Liberation Mono', monospace`

**Character:** 本文は Newsreader の落ち着いたラテン書体に Mincho を重ねる二段組み。記事タイトルは italic axis で英文と日本語混植の表情を持たせる。UI 部分は対照的に flat sans で締める。Medium と Stripe Press の中間。

### Hierarchy

- **Display** (Newsreader 400 / clamp(2rem, 4.5vw, 3rem) / 1.15 / -0.01em): masthead サイトタイトル。italic axis ON。1 ページに 1 つ。
- **Headline** (Newsreader 500 / clamp(1.5rem, 2.5vw, 2rem) / 1.25): 本文 h2、list ページの h1 (カテゴリ名 / "Recent Notes")。
- **Title** (Newsreader 500 / 1.375rem / 1.3): 本文 h3、Hero post の見出し、Recent Notes 内の非 hero post 行のタイトル。
- **Body** (Newsreader 400 / 1.0625rem / 1.7): 本文。serif で 1.7 行送りで日本語を組む。
- **UI** (system sans 400 / 0.9375rem / 1.5): nav、ヘッダーリンク、aside、index strip entry。
- **Label** (system sans 400 / 0.8125rem / 1.5 / 0.01em letter-spacing): post meta、tag pill、figcaption、hdknr chip。
- **Code** (mono 400 / 0.86em / 1.55): インライン `<code>` と コードブロック内。

### Named Rules

**The One-Serif Rule.** Display と Body は同一 family (Newsreader)。italic axis、weight axis で表情を作るが、family を増やさない。Stripe Press / Robin Sloan / Maggie Appleton と同じく「1 つの serif が全部を担う」思想。

**The Bilingual-Mincho Rule.** 日本語は OS の Mincho stack に渡す。`Hiragino Mincho ProN` (macOS / iOS) → `Yu Mincho` (Windows) → `Noto Serif CJK JP` (Linux / Android) の順。Newsreader のラテン文字と Mincho の組み合わせで日本語混植時の高さ差が出るので、`vertical-align` は OS デフォルトに任せ、line-height を 1.7 と広めに取って吸収する。

**The Japanese-Line-Length Rule.** 本文の行長は `max-width: 680px` で固定 (旧 720px から微減)。1.0625rem / Newsreader で日本語約 38-42 字／行。新しい本文型レイアウトを足すときも 680px を超えない。

**The Webfont-Subset Rule.** Newsreader は Latin subset のみ。日本語フォントは Web font として読み込まない (CJK は重すぎる)。Subset 後の Newsreader は 30-50KB を目標。`<link rel="preload">` と `font-display: swap` で読み込み。

## 4. Elevation

このシステムは **flat-with-grain**。`box-shadow` は (Copy ボタンや focus ring を除いて) 装飾用途では使わない。深度は「地のトーン階調 + grain texture + 1px 罫線」だけで表す。

- ライトモードでは「parchment (`#f6f3ee` + grain) = 主紙地」「parchment-warm (`#efeae1`) = TOC / aside / 沈み面」「code slab (`#1c1a18`) = 黒に近い唯一の面」の三層。
- ダークモードでは「parchment-dark (`#211f1c` + grain) = 主紙地」「parchment-dark-card (`#2c2925`) = TOC / aside」「code slab (`#2c2925`) = 紙地より明るい層」と、紙地よりカード / コード面を一段明るくして奥行きを反転させる。
- フォーカスや :active 状態でも影は出さない。focus は Iron Sienna の 2px outline で示す。

### Named Rules

**The Flat-By-Default Rule.** カード・パネル・モーダルに drop shadow を載せない。明るさ差と 1px 罫線で段差を表す。ホバー時に shadow を追加するアニメーションも禁じる。

**The Inverted-Layer Rule (Dark).** ダークモードでは沈み面を紙地より明るくする。光源を上ではなく下から見ているメンタルモデル。

**The Grain-As-Atmosphere Rule.** grain は装飾ではなく atmosphere。strength は固定 (light 4% / dark 5%)、scroll で動かさない、page transition で再生成しない、`prefers-reduced-motion` でも静止しているので影響しない。grain を消すと「画面に貼った紙」感が消える。

## 5. Components

### Masthead

サイト名 + 1-2 行サブタイトル + Iron Sienna 2×48px の rule。

- **Title:** Newsreader italic 400、clamp(2rem, 4.5vw, 3rem)、color: Ink Graphite。
- **Subtitle:** system sans 0.9375rem、color: Ink Secondary。2 行まで。
- **Rule:** Iron Sienna fill 2px 高 × 48px 幅、title 下に 16px gap。サイト全体の唯一の「印」。

例:
> Eotel's Notebook
> Posts, notes, and wiki. A working notebook by Eotel.
> ────

### Post Row (Default)

カードを捨てた、罫線 + 縦余白だけのデンス行。

- **Padding:** `0 0 28px 0`、下に 1px Ink Divider 罫線。
- **Title:** Newsreader 500 / 1.375rem。color: Ink Graphite。リンク全体 1 つ。
- **Meta line:** system sans 0.8125rem。`日付 · category · tags · ↗ (source link mark)`。color: Ink Secondary。
- **Hover:** title 文字色を Iron Sienna Deep に。罫線は変えない。
- **Card overlay 廃止:** `.entry-link` 全面オーバーレイは使わない。title 文字そのものがリンク。

### Post Row (Hero, ホームの 1 件目だけ)

- **Padding:** `0 0 36px 0`、下に 1px 罫線。
- **Title:** Newsreader 500 / clamp(1.5rem, 2.5vw, 2rem) (= Headline)。
- **Description:** Newsreader 400 / 1.0625rem (= Body)、line-clamp 2、color: Ink Graphite Soft。
- **Meta line:** Default Post Row と同形。

### Index Strip (Wiki 索引、homepage の右脈 / 下脈)

3 セクション (Concepts / Tools / Guides)、各 6 entry。

- **Section label:** system sans 0.8125rem、letter-spacing 0.04em、uppercase、color: Ink Secondary。
- **Entry:** system sans 0.9375rem、color: Ink Graphite。dotted underline (Iron Sienna Soft 60%)、hover で solid + Iron Sienna Deep。
- **"全件" link:** "→ /wiki/" 形式、system sans 0.8125rem、color: Iron Sienna。
- **Position:** 768px+ では body の右脈に sticky でなく固定 grid セル。768px 未満では post list の下脈に積む。

### Reading by Topic (タイポグラフィッククラウド)

カテゴリ + 人気タグの flow テキスト。

- **Style:** system sans、font-size をエントリ重みで変える (大 1.25rem / 中 1rem / 小 0.875rem)、color: Ink Secondary。
- **Hover:** Iron Sienna に色変え、underline なし。
- **Wrap:** inline-flex で wrap、gap 12px。

### Tag Pill (post meta 内の category / tag chip)

list ページの post-row meta 内で使う chip。

- **Style:** 背景 transparent、文字 Ink Secondary、サイズ Label。区切りは中黒 `·`。
- **Hover:** Iron Sienna text-decoration: underline。

### Pagination Button

PaperMod の黒ピル ("背景塗り") を廃止し、ink outline pill に書き換える。

- **Style:** 背景 transparent、文字 Iron Sienna、padding 10px 20px、rounded pill。
- **Hover:** 文字 Iron Sienna Deep、underline。
- **Active state:** Iron Sienna 2px outline ring。
- **Disabled:** Ink Muted、cursor not-allowed。

### Code Block

- **Block:** 背景 Code Slab Dark (両モードで暗色)、文字 `#e5dfd0` (warm cream)、rounded `default` (4px)、padding `14px 16px`。grain は重ねない。
- **Copy ボタン:** 右上 hover 時表示。半透明 Ink Graphite 背景、cream text。

### Inline Code

- **Style:** 背景 Code Inline Bg (`#ece6d8` light / `#3a352f` dark)、文字 Ink Graphite、rounded **sharp** (2px)、padding 2px 6px、font-size 0.86em。
- **The Slab Rule.** Block の角は 4px、Inline の角は 2px。同じ "code" でも別物の手触り。

### Blockquote

- **Style:** `border-inline-start: 2px solid var(--iron-sienna-soft)`、padding 0 18px、margin 24px 0、文字 Ink Graphite Soft、italic ON。
- **Note:** 旧版で 3px Primary だった縦線を 2px Iron Sienna Soft に緩めた。引用記号としての semantic 役割は維持、ただし装飾としての強度を 1 段下げる。`border-inline-start: 3px` 以上を新規に流用しない。

### Keyword Link (`.kw-link`, signature)

`scripts/inject_keyword_links.py` で本文に挿入される Wiki 用語の自動リンク。

- **Default:** `text-decoration: underline dotted`、線 Iron Sienna Soft、文字 Ink Graphite。
- **Hover/Focus:** 線が solid に、文字 Iron Sienna Deep。
- **Tag variant** (`.kw-link--tag`): 線 Ink Muted。タグ自動リンクは色を抑え、用語自動リンクと差を付ける。

### TOC

- **Style:** 背景 Parchment Warm、border なし、rounded `default` (4px)、padding 12px 16px。
- **Behavior:** `<details>` で開閉。`summary:focus { outline: 2px solid var(--iron-sienna) }`。

### Linked from (post single 末尾、新規)

post を読み終えた読者向けの被参照リスト。

- **Section header:** "Linked from" (system sans 0.9375rem uppercase letter-spacing 0.04em)、下に Iron Sienna 1px 24px のキッカー線。
- **List:** ul plain、各 entry は post title (UI font) + 日付 (Label)、Iron Sienna underline。
- **Empty state:** "まだ他のページから参照されていません。" を Ink Muted で 1 行。`/wiki/` への誘導を 1 行追加。

### Related in Wiki (post single 末尾、新規)

- **Section header:** "Related in Wiki" (同形)。
- **List:** Wiki entry の title + description (Label)。link は Iron Sienna underline。
- **Source:** post frontmatter の `tags` と `categories` から推論。MVP は手動 mapping table か Hugo の関連コンテンツ機能で十分。

### More in <category> (post single 末尾)

- **Section header:** "More in <カテゴリ名>"。
- **List:** 同 category の他 5 件、Post Row と同形の縮小版 (title + 日付のみ)。

### Wiki Section Footer (既存維持、style 更新)

`layouts/wiki/single.html` 末尾。

- **Style:** Parchment Edge 1px 上罫線、padding-top 24px、UI font。
- **意義:** Wiki 三層の他ページへの導線。Linked from / Related in Wiki と並んで Scrapbox 性を支える 3 つ目の signature。

### Navigation / Header

- **Layout:** flex / space-between、最大幅 1024px。
- **Logo:** "Eotel's Notebook" Newsreader italic 400 / 1.25rem。color: Ink Graphite。
- **Menu Item:** system sans 0.9375rem、項目間 24px。color: Ink Graphite。
- **Active state:** Iron Sienna 2px 下線 + weight 500。
- **Theme toggle:** 既存 PaperMod のものを継承、ただし icon 色を Ink Secondary に下げる。

### hdknr Chip

hdknr 由来 post (`author: hdknr`) の meta 行に表示。

- **Style:** transparent 背景、文字 Ink Muted、Label font、`opacity 0.85`、prefix "via "。
- 例: `2018-03-12 · ツール/開発環境 · via hdknr`

### Anchor Heading

- **Default:** 非表示。
- **On hover (h2..h4):** `inline-flex` で表示、color: Iron Sienna Soft、margin-inline-start 8px、`user-select: none`。

## 6. Do's and Don'ts

### Do:

- **Do** Iron Sienna を全てのリンク・キーワード dotted・active nav 下線・見出しキッカーに使う。それ以外の色を加えない (`The One-Ink Rule`)。
- **Do** 背景に warm parchment (`#f6f3ee` / `#211f1c`) を使い、SVG grain overlay を 4-5% で常に乗せる。
- **Do** Display + Body を Newsreader 1 family で組む。日本語は OS の Mincho stack にフォールバックさせる。
- **Do** 一覧 (home / categories / tags / archives / wiki list) は post-row のデンス行リストで組む。card grid を新設しない。
- **Do** post single の末尾に "Linked from / Related in Wiki / More in <category>" を常設する。空のときは 1 行のメッセージで埋める (省略しない)。
- **Do** 出典・author・日付・source_url を post meta に常時表示する。hdknr 由来は小さな "via hdknr" chip で示す。
- **Do** flat デザインを守る。深度は明度差と 1px 罫線、grain texture だけで表す。
- **Do** コードブロックは light/dark どちらでも暗色スラブにする。warm parchment の上で唯一の重い面。
- **Do** Wiki 用語の `.kw-link` 自動挿入を維持する。本文から Wiki への導線はこの dotted underline が担う。
- **Do** 自動テーマ切替 (`defaultTheme = 'auto'`) を尊重する。
- **Do** `prefers-reduced-motion` を尊重する。grain は静止しているので問題なし。

### Don't:

- **Don't** Iron Sienna 以外のアクセント色を新規に追加しない。category ごとに紫 / 緑 / 青を割り当てない (`The One-Ink Rule` 厳守)。
- **Don't** pure `#ffffff` / `#000000` を新規 CSS で背景・文字に書かない。旧 PaperMod の互換のためにだけ存在し、新規面では parchment 系で組む。
- **Don't** card grid を組まない。等寸カード 3 列で記事を並べない。post-row のデンス行で代替する。
- **Don't** SaaS ランディング風の巨大ヒーロー、グラデーション CTA、追従ソーシャル共有ボタンを追加しない。
- **Don't** 「ハッカー感」のネオン緑ターミナル風配色を新規記事カテゴリ用に作らない。
- **Don't** 紫グラデと光彩エフェクトで AI 関連記事を装飾しない。AI / セキュリティ / クラウド の全カテゴリを Iron Sienna + parchment + grain の同じトーンで束ねる。
- **Don't** 装飾としての `border-left` / `border-right` を 2px より太く使わない。blockquote の 2px は引用記号として例外、それ以外で流用しない。
- **Don't** `background-clip: text` + gradient によるグラデーションテキストを使わない。
- **Don't** 装飾的 `backdrop-filter: blur` を使わない。
- **Don't** ヒーローに「大きな数字 + ラベル + 補助 stats + グラデアクセント」のメトリック テンプレを置かない。
- **Don't** モーダル / ダイアログを新規追加しない。情報は inline / 別ページに置く。
- **Don't** Newsreader 以外の web font を追加しない。日本語フォントを web font としてロードしない (`The Webfont-Subset Rule`)。
- **Don't** hdknr 由来の 783 記事のレイアウトを壊す変更をしない。post-row はデフォルトで 783 件にも適用される。意図的に「沈ませる」のは hdknr chip の `opacity: 0.85` だけ。
- **Don't** em dash (`—`) を本文・UI コピーに使わない。日本語の三点リーダー (`…`)、読点 (`、`)、コロン (`：`)、または括弧で置き換える。masthead サブタイトルなど英文コピーでもピリオド 2 文に分解する。
- **Don't** 絵文字装飾、感嘆符の連打、煽り表現を見出しに入れない。
- **Don't** post-entry のクリッカブル overlay (`.entry-link` 全面オーバーレイ) を新規追加しない。title リンクで十分。
