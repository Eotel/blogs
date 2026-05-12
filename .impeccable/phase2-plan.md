# Phase 2 Plan — Hypertext Garden Implementation

> **このファイルは Phase 1 (design docs) PR の中で commit される作業計画書。**
> 新しいセッションで Phase 2 (Hugo template + CSS 実装) を再開するときは、まずこの md を読んでから着手すること。Phase 2 完了後、PR2 で本ファイルを削除するか `done/` 配下に移す。

## 0. 新セッションでの再開手順

1. このリポジトリ (`Eotel/blogs`) の main を pull する。
2. `cat PRODUCT.md DESIGN.md .impeccable/design.json` を読む (または `node .claude/skills/impeccable/scripts/load-context.mjs` を実行)。
3. 本ファイル全体を読む。
4. 「Phase 2 タスクリスト」の順に着手する。

新セッションへの最初の prompt 例:

```
.impeccable/phase2-plan.md を読んで Phase 2 (Hugo template + CSS 実装) を続行してください。
PRODUCT.md / DESIGN.md / .impeccable/design.json が design intent の source of truth。
```

## 1. Context

### North Star

**The Hypertext Garden** — Eotel's Notebook は「丁寧に組まれた、すべてが互いにリンクし合う、作業中のノートブック」として現れる。Medium 級の serif typography、フィルム grain がかかった warm parchment の地、たった 1 色の朱いインク (Iron Sienna)、Scrapbox 並みのリンク密度、この 4 つだけでサイト全体のシグネチャを構成する。

### サイト名変更

- Old: "Eotel blog"
- **New: "Eotel's Notebook"**
- Subtitle: "Posts, notes, and wiki. A working notebook by Eotel."
- (em dash 禁止のため piriod 2 文に分解)

### Anchor references

- Maggie Appleton (maggieappleton.com)
- Andy Matuschak working notes (notes.andymatuschak.org)
- Stripe Press (press.stripe.com)
- Robin Sloan (robinsloan.com)
- Are.na blocks/channels
- Scrapbox bracket-link density

### 確定済み design choices

| 項目 | 値 |
|---|---|
| Signature ink | Iron Sienna `#a64a2c` / `oklch(48% 0.13 35)` |
| Background (light) | Warm parchment `#f6f3ee` + SVG grain overlay 4% multiply |
| Background (dark) | Warm dark `#211f1c` + SVG grain overlay 5% multiply |
| Display + Body font | Newsreader variable (Latin subset, ~50KB) + system Mincho fallback |
| UI font | system sans (既存維持) |
| Code font | ui-monospace stack (既存維持) |
| Body max-width | 680px (旧 720px から微減) |
| 一覧 layout | post-row のデンス行リスト、card 廃止 |
| Section labels | English (Recent Notes / Index / Linked from / etc.) |
| Recent Notes 件数 | 5 件 (hero 1 件 + default 4 件) |
| Backlinks 計算 | MVP は frontmatter の `related_posts` のみ、`[[wiki-term]]` graph は次 PR |
| Dark mode grain | あり |

## 2. Done in Phase 1 (このコミットに含まれる)

- `PRODUCT.md` — Brand Personality を engineer-curious / hypertext-dense / quietly-beautiful に更新。Design Principles を 8 個に拡張 (Hypertext-first / Beautiful as a working notebook / Card を捨てる を追加)。
- `DESIGN.md` — 全面書き換え。Iron Sienna + warm parchment + Newsreader + grain の 4 軸。Named Rules を One-Ink / Warm-Parchment Default / One-Serif / Bilingual-Mincho / Webfont-Subset / Grain-As-Atmosphere に新設、旧 No-Accent / No-Web-Font / Pure-Endpoint Allowance は廃止。13 components 定義。
- `.impeccable/design.json` — colorMeta / typographyMeta / motion / breakpoints / components / narrative を全面再生成。各 component に self-contained HTML + CSS 含む。

## 3. Phase 2 タスクリスト (実行順)

### 3.1. Branch / worktree 準備

- ブランチ名: `design/hypertext-garden-impl`
- ベース: main (Phase 1 PR が merge された後)
- worktree 推奨: `.worktrees/hypertext-garden-impl`

```bash
# Phase 1 PR が main に merge されたあと
git fetch origin
git checkout main
git pull origin main
git worktree add .worktrees/hypertext-garden-impl -b design/hypertext-garden-impl
cd .worktrees/hypertext-garden-impl
```

### 3.2. hugo.toml の更新

`title`、`homeInfoParams.Title`、`homeInfoParams.Content`、`params.author` を更新。

```toml
title = "Eotel's Notebook"

[params]
  defaultTheme = 'auto'
  ShowReadingTime = true
  ShowShareButtons = false
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true
  ShowToc = true
  author = 'Eotel'

  [params.homeInfoParams]
    Title = "Eotel's Notebook"
    Content = 'Posts, notes, and wiki. A working notebook by Eotel.'
```

PaperMod のテーマ機能のうち以下を維持: `ShowReadingTime`、`ShowToc`、`ShowCodeCopyButtons`、`ShowBreadCrumbs`、`defaultTheme = 'auto'`、`ShowShareButtons = false`。

### 3.3. SVG grain の配置

`static/images/grain.svg` を新規作成。CSS から `background-image: url(/blogs/images/grain.svg)` で参照。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
  <filter id="n">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="3"/>
    <feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.5 0"/>
  </filter>
  <rect width="100%" height="100%" filter="url(#n)"/>
</svg>
```

または同じものを CSS の data URI として inline する (HTTP 往復削減)。推奨: data URI inline (ファイルサイズ ~600 bytes 程度)。

`body::before` 擬似要素として fixed position で全画面 overlay。`mix-blend-mode: multiply` で 4% (light) / 5% (dark) 強度。

### 3.4. Newsreader font の読み込み

Latin subset を Google Fonts または self-host で読み込む。

**Google Fonts (推奨, 最初は MVP):**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&display=swap">
```

**Self-host (将来):**

- woff2 を `static/fonts/newsreader/` に置く
- `@font-face` で `font-display: swap`、`unicode-range` で Latin のみに制限

挿入箇所: `layouts/partials/extend_head.html`

### 3.5. CSS の追加 (`themes/PaperMod/assets/css/extended/blank.css`)

PaperMod の `extended/blank.css` は theme 同梱の override 入口。ここに新規 CSS を全部追加する。テーマ本体は触らない。

書く内容 (概略):

```css
/* === 1. Token override (上書き) === */
:root {
    --gap: 28px;
    --content-gap: 20px;
    --main-width: 680px;     /* 720 → 680 に微減 */
    --radius: 4px;            /* 8 → 4 に sharper */
    --theme: #f6f3ee;
    --entry: #f6f3ee;
    --primary: #221f1c;
    --secondary: #6b6660;
    --tertiary: #d8d2c6;
    --content: #221f1c;
    --code-block-bg: #1c1a18;
    --code-bg: #ece6d8;
    --border: #d8d2c6;
    --ink: #a64a2c;            /* Iron Sienna */
    --ink-soft: #c46a4a;
    --ink-deep: #7a3520;
    color-scheme: light;
}
:root[data-theme="dark"] {
    --theme: #211f1c;
    --entry: #2c2925;
    --primary: #ece6d8;
    --secondary: #a8a29a;
    --tertiary: #3a352f;
    --content: #ece6d8;
    --code-block-bg: #2c2925;
    --code-bg: #3a352f;
    --border: #3a352f;
    --ink: #d77a55;
    --ink-soft: #c46a4a;
    --ink-deep: #a64a2c;
    color-scheme: dark;
}

/* === 2. Newsreader 読み込み (Google Fonts 経由なら head で、self-host なら ここで @font-face) === */

/* === 3. body 全体に serif body + grain overlay === */
body {
    font-family: 'Newsreader', ui-serif, 'Iowan Old Style', Georgia, 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif;
    font-size: 1.0625rem;
    line-height: 1.7;
}
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml;utf8,<svg...>"); /* grain SVG inline */
    mix-blend-mode: multiply;
    opacity: 0.04;
    pointer-events: none;
    z-index: 1;
}
:root[data-theme="dark"] body::before {
    opacity: 0.05;
}

/* === 4. Heading serif === */
h1, h2, h3, .post-title, .page-header h1, .entry-header h2, .first-entry h1 {
    font-family: 'Newsreader', ui-serif, 'Iowan Old Style', Georgia, 'Hiragino Mincho ProN', 'Yu Mincho', 'Noto Serif CJK JP', serif;
    font-weight: 500;
    letter-spacing: -0.005em;
}

/* === 5. Masthead (新規) === */
.ds-masthead { ... }

/* === 6. Post Row (新規, .post-entry を override) === */
.post-entry {
    /* card 廃止: 罫線 + 縦余白だけ */
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 0 28px 0 !important;
    margin-bottom: 0 !important;
    border-bottom: 1px solid var(--border) !important;
}
.post-entry:active { transform: none !important; }
.entry-link { display: none !important; }    /* card overlay 廃止 */

/* === 7. Pagination (黒ピル → outline ink pill) === */
.pagination a {
    background: transparent !important;
    color: var(--ink) !important;
    border-radius: 999px;
    padding: 10px 20px;
}

/* === 8. Link (全て Iron Sienna) === */
.post-content a:not(.kw-link):not(.anchor) {
    color: var(--ink);
    box-shadow: 0 1px 0 var(--ink-soft);
}
.post-content a:not(.kw-link):not(.anchor):hover {
    color: var(--ink-deep);
    box-shadow: 0 1px 0 var(--ink-deep);
}

/* === 9. Tag pill (背景塗り廃止、text only) === */
.post-tags a {
    background: transparent !important;
    border: none !important;
    color: var(--secondary) !important;
    padding: 0 !important;
}
.post-tags a:hover {
    color: var(--ink) !important;
    text-decoration: underline;
}

/* === 10. TOC (背景を parchment-warm に) === */
.toc {
    background: var(--code-bg);
    border: none !important;
}

/* === 11. Index Strip (新規) === */
.ds-index-strip { ... }

/* === 12. Reading by topic (新規) === */
.ds-reading-by-topic { ... }

/* === 13. Linked from (新規, post single 末尾) === */
.ds-linked-from { ... }

/* === 14. Responsive grid (768px+) === */
@media (min-width: 768px) {
    .home-layout {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 240px;
        gap: 48px;
    }
}
```

実装時は `.impeccable/design.json` の各 component の `html` / `css` 値をそのまま流用できる (drop-in)。クラス名のみ `ds-` から PaperMod 互換のものに renames するか、新規クラスを追加する。

### 3.6. `layouts/_default/list.html` 新規作成

PaperMod のデフォルト list (theme 配下) を上書きする。要件:

- Masthead (`layouts/partials/masthead.html` 新規)
- Recent Notes (5 件、hero 1 件): post-entry のデンス行リスト
- 全件一覧 (paginated): home page だけ「Recent Notes 5 件 → 全件」、その他 list ページは件数なしで paginated 全件
- Index Strip aside (768px+ で右脈、それ以下で下脈)
- Reading by Topic (home のみ表示)

注意点:

- hdknr 由来 post を home の Recent Notes には含めない (`.Params.author != "hdknr"` で filter)、ただし `/posts/` 全件には含める。これは PRODUCT.md「歴史的記事と共存する」の解釈。
- カテゴリ list ページでは Index Strip を隠す (`page.Section == "categories"` で分岐)。

### 3.7. `layouts/index.html` (home 専用)

`layouts/_default/list.html` を継承して home だけのレイアウトを追加。

```go-template
{{ define "main" }}
  {{ partial "masthead.html" . }}
  <div class="home-layout">
    <main>
      {{ partial "recent-notes.html" . }}
      {{ partial "reading-by-topic.html" . }}
    </main>
    <aside>
      {{ partial "index-strip.html" . }}
    </aside>
  </div>
{{ end }}
```

### 3.8. `layouts/_default/single.html` 拡張

PaperMod のデフォルト single.html を上書きせず、partial で末尾に挿入する方が安全。

選択肢:

(a) `layouts/_default/single.html` 全面 override (PaperMod の structure を写してから "Linked from / Related in Wiki / More in <category>" を追加)
(b) `layouts/partials/footer.html` を拡張して各 post 末尾に partial を inject (PaperMod の hook が無いのでこの方式は使えない可能性大)

→ **(a) を推奨**。PaperMod の `single.html` を読み取って、必要な partial 呼び出しだけ追加した差分版を `layouts/_default/single.html` に置く。

各 partial:

- `layouts/partials/linked-from.html` — `Site.RegularPages` を走査して `Params.related_posts` に現 page の `RelPermalink` を含む post を抽出
- `layouts/partials/related-in-wiki.html` — `where .Site.RegularPages "Section" "wiki"` の中から `Params.tags` overlap 上位 5 件を抽出 (Hugo の `related` content 機能を使う)
- `layouts/partials/more-in-category.html` — `where .Site.RegularPages "Section" "posts"` の中から 同 category の最新 5 件

Hugo の `related` 機能を有効化するには `hugo.toml` に:

```toml
[related]
  threshold = 80
  toLower = false
  [[related.indices]]
    name = 'tags'
    weight = 100
  [[related.indices]]
    name = 'categories'
    weight = 80
```

### 3.9. `layouts/wiki/single.html` / `list.html` 既存を新トークンに揃える

既存:
- `wiki/single.html` は inline style で `border-top: 1px solid var(--border)` を使っている。inline style はそのままで OK (token は CSS variable で参照されているため自動追従)。
- `wiki/list.html` の中身を再確認、必要なら拡張。

### 3.10. `layouts/partials/extend_head.html` の更新

既存:
```html
<link rel="stylesheet" href="{{ "css/keyword-links.css" | relURL }}">
```

更新後 (Google Fonts route):
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..500&display=swap">
<link rel="stylesheet" href="{{ "css/keyword-links.css" | relURL }}">
```

### 3.11. `static/css/keyword-links.css` を Iron Sienna に更新

既存:
```css
.post-content a.kw-link {
    text-decoration: underline dotted;
    text-decoration-color: var(--secondary, #999);
    ...
}
```

更新後:
```css
.post-content a.kw-link {
    text-decoration: underline dotted;
    text-decoration-color: var(--ink-soft, #c46a4a);
    text-underline-offset: 3px;
    color: inherit;
    background: none;
    box-shadow: none;
    transition: color 150ms cubic-bezier(0.22, 1, 0.36, 1), text-decoration-color 150ms cubic-bezier(0.22, 1, 0.36, 1);
}
.post-content a.kw-link:hover,
.post-content a.kw-link:focus {
    text-decoration-style: solid;
    text-decoration-color: var(--ink-deep, #7a3520);
    color: var(--ink-deep, #7a3520);
}
.post-content a.kw-link--tag {
    text-decoration-color: var(--tertiary, #a8a29a);
}
.post-content a.kw-link--tag:hover,
.post-content a.kw-link--tag:focus {
    text-decoration-color: var(--ink-deep);
}
```

### 3.12. README.md のサイト名差し替え

```diff
- # Eotel blog
+ # Eotel's Notebook
```

### 3.13. CLAUDE.md のサイト名差し替え

```diff
- # Eotel blog
+ # Eotel's Notebook
```

### 3.14. `archetypes/default.md` の確認

新規 post 生成時の archetype に変更不要なら skip。site name はテンプレ内に hard-code されていないはず。

### 3.15. Build verification

```bash
cd .worktrees/hypertext-garden-impl
hugo --gc --minify
```

- ビルドが通ること
- `public/index.html` を開いて masthead + Recent Notes + Index Strip が出ること
- `public/posts/index.html` で全件 paginated が出ること
- `public/posts/2026/05/<latest-post>/index.html` の末尾に Linked from / Related in Wiki / More in <category> が出ること
- `public/wiki/index.html` で 3 列が出ること

### 3.16. Visual verification

```bash
hugo server -D --bind 0.0.0.0
# http://localhost:1313/ を開く
```

確認項目:
- [ ] 地が warm parchment、grain が乗っている
- [ ] Newsreader が読み込まれ、本文が serif に
- [ ] 日本語が Mincho にフォールバック
- [ ] Iron Sienna がリンク / kw-link / pagination に通る
- [ ] post-row のデンス行リスト (card じゃない)
- [ ] hero post に description 2 行、残り 4 件は title + meta だけ
- [ ] Index Strip が右脈 (768px+) または下脈 (<768px) に出る
- [ ] dark mode で grain と Iron Sienna の明度が反転 OK
- [ ] post single 末尾に Linked from / Related in Wiki / More in <category> 表示
- [ ] hdknr post に "via hdknr" chip
- [ ] em dash がコピー内に残っていない
- [ ] `prefers-reduced-motion` でアニメ無効化

### 3.17. PR

ブランチ名: `design/hypertext-garden-impl`
コミットメッセージ: `feat: implement Hypertext Garden design system`
PR タイトル: `Implement Hypertext Garden design system`
PR body: `.impeccable/phase2-plan.md` の Done を抜粋。"Phase 2 implementation of the design direction set in PR #<PR1 番号>". Closes Issue があれば紐付ける (現状は無い)。

PR body は `.claude/temp/pr_body.md` に Write してから `gh pr create --body-file` で渡す (CLAUDE.md ルール)。

## 4. 注意点 / Pitfalls

### 4.1. PaperMod theme を直接 fork しない

`themes/PaperMod/` 直下を直接編集しない。override は:
- `themes/PaperMod/assets/css/extended/blank.css` (theme 同梱の override 入口)
- `layouts/` 配下 (Hugo の lookup order で theme より優先)
- `static/` 配下 (theme より優先)
- `assets/` 配下 (theme より優先、image processing が効く)

### 4.2. PaperMod の token (`--theme` 等) を残す

PaperMod の card / pagination / TOC 等は CSS variable で書かれているので、`:root` で上書きすれば波及する。新規 class を増やすより既存 variable を `extended/blank.css` で再定義する方が侵襲性が低い。

### 4.3. hdknr 由来 post の filter

`.Params.author` で判定。home の Recent Notes には `where .RegularPages "Params.author" "!=" "hdknr"` を使う。`/posts/` 全件には filter を入れない。Archive ページにも入れない。

### 4.4. Hugo の `related` 機能

`hugo.toml` に `[related]` セクションを足す必要あり (3.8 参照)。MVP は `tags` ベース。

### 4.5. Image processing

CLAUDE.md に追記された:
- 画像は `assets/images/` に配置 (`static/` ではない)
- markdown の `![](...)` は `layouts/_default/_markup/render-image.html` で `<picture>` + WebP srcset 展開
- SVG・外部 URL は素の `<img>`

grain SVG は `static/images/grain.svg` か CSS inline data URI のどちらか。CSS background-image なので image processing は不要 → `static/` または inline どちらでも OK。Inline data URI 推奨 (HTTP 往復削減)。

### 4.6. CLS (Cumulative Layout Shift)

Newsreader 読み込み中に system serif が表示されるので `font-display: swap`。`size-adjust: 100%` で system serif と Newsreader のグリフ幅を近似してジャンプを最小化。

### 4.7. lefthook の pre-push

`pre-push` で `hugo --gc` が走るので、build が通らないと push がブロックされる。先にローカルで build 通過確認すること。

## 5. Phase 3 候補 (実装後の polishing)

- `[[wiki-term]]` 構文を本文中に書けるようにする build-time parser (Python script)
- Wiki ページ間の backlink graph 生成 (Hugo の `related` だけでなく明示的な引用関係)
- search 改善 (PaperMod の Fuse.js search を Iron Sienna 化、または別 search に置き換え)
- RSS の OGP / 画像対応
- categories list ページのカスタマイズ (現状は PaperMod デフォルト)
- archives ページの year/month grouping の typography 改善

## 6. Open Questions (Phase 2 中に解決すべき)

- [ ] Newsreader を Google Fonts 経由 vs self-host のどちらにするか。MVP は Google Fonts でいく予定。
- [ ] Hero post の選択ロジック: 単に最新 1 件で OK か、`featured: true` frontmatter フラグで手動 curated もできるようにするか。MVP は最新 1 件で。
- [ ] Index Strip の Wiki 用語 6 個の選び方: lastmod 最新 / 手動 curated / 別ロジック。MVP は lastmod desc で。
- [ ] Reading by Topic のクラウド重み: post 件数 / lastmod 新しさ / 手動。MVP は post 件数で。
- [ ] hdknr filter の文言: home に表示しない後、 "/posts/" でだけ表示するときに「全 783 件、うち最新 N 件」のような件数表示を付けるか。
- [ ] grain SVG の inline data URI 化を CSS で行うか、`static/images/grain.svg` 参照にするか。MVP は inline。

## 7. 参照リンク

- design intent ソース: `PRODUCT.md` `DESIGN.md` `.impeccable/design.json`
- impeccable craft reference: `~/.claude/plugins/cache/impeccable/impeccable/3.0.7/skills/impeccable/reference/craft.md`
- Hugo lookup order: https://gohugo.io/templates/lookup-order/
- PaperMod customization: https://github.com/adityatelange/hugo-PaperMod/wiki/Variables
- Newsreader font: https://fonts.google.com/specimen/Newsreader
- Maggie Appleton notes: https://maggieappleton.com/notes
- Andy Matuschak working notes: https://notes.andymatuschak.org/
