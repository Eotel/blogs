---
title: "remark CLI で Markdown を整える: lint / format / ToC を一通り設定する"
date: 2026-05-13
lastmod: 2026-05-13
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "Node.js プロジェクトに remark-cli を導入して Markdown を lint・整形・目次自動生成まで仕上げる手順。.remarkrc の構成、husky/lint-staged との連携、CI で --frail を使う流れまでを 1 本にまとめる。"
categories: ["ツール/開発環境"]
tags: ["remark", "markdown", "lint", "husky", "github-actions"]
slug: "2026-05-13-remark-cli-setup-guide"
---

## きっかけ — 「AI に参照させやすい Markdown」という視点

remark を真面目に仕込もうと思ったきっかけは、Qiita の [@semba_yui さんの記事](https://qiita.com/semba_yui/items/60246a8831e466b508cc) だった。AI エージェントに Markdown を読ませる用途で目次を自動生成する話で、要点はここに集約されている。

> AI エージェントは大量のファイルを先頭から順に"head"して読むことが多く、無駄なコンテキストでトークンを浪費する

人間向けの執筆ツールという顔をしていた remark が、**LLM 向けのドキュメントパイプライン** としても効くというのは盲点だった。本記事は、その発想を出発点にしつつ、もう少し手前 — **remark CLI をリポジトリに導入して、lint・整形・目次生成・husky 連携・CI まで一通り設定する** ところを順に書く。

## remark エコシステムの全体像

remark は [unified](https://unifiedjs.com/) という AST 変換基盤の上に乗った Markdown プロセッサで、Markdown を `mdast` という抽象構文木に読み込み、プラグインで変換し、また Markdown に書き戻す。CLI 版の `remark-cli` は、設定ファイル (`.remarkrc` / `package.json` の `remarkConfig` / `.remarkrc.js` など) を読んで、`pnpm remark .` のような呼び出しでファイルをまとめて処理してくれる。

つまり、用意するのは次の 3 つだけだ。

1. `remark-cli` — 入口の CLI
2. プラグイン群 — `remark-preset-lint-*` / `remark-gfm` / `remark-frontmatter` / `remark-toc` など
3. 設定ファイル `.remarkrc` — どのプラグインを順に通すかを宣言する

![remark のプラグイン pipeline を通って Markdown が lint・整形・目次付きに変換され、AI エージェントが参照するコンセプト図](/blogs/images/2026-05-13-remark-cli-setup-guide-hero.png)

## 最小セットアップ

まずは依存を入れる。`pnpm` 前提で書くが `npm` でも `yarn` でも同じ。

```bash
pnpm add -D remark-cli \
  remark-preset-lint-recommended \
  remark-preset-lint-consistent \
  remark-gfm \
  remark-frontmatter \
  remark-toc
```

リポジトリ直下に `.remarkrc` を JSON で置く。

```json
{
  "plugins": [
    "remark-preset-lint-recommended",
    "remark-preset-lint-consistent",
    "remark-gfm",
    ["remark-frontmatter", ["yaml"]],
    [
      "remark-toc",
      {
        "heading": "目次|table of contents",
        "maxDepth": 3
      }
    ]
  ],
  "settings": {
    "bullet": "-",
    "emphasis": "*",
    "strong": "*"
  }
}
```

`package.json` 側の `scripts` は普段使う 3 つだけ用意しておく。

```json
{
  "scripts": {
    "remark:lint": "remark . --frail --quiet",
    "remark:fix": "remark . --output --quiet"
  }
}
```

`--output` を付けるとファイルが書き戻され、目次や整形（`.remarkrc` の plugins チェーン）がまとめて反映される。`remark-toc` も同じパスで走るので、`remark:fix` を呼ぶだけで目次の再生成も済む。`--frail` は warning でも exit 1 にする CI 用フラグで、後述する。

## lint preset の選び方

preset は 2 つを併用するのが楽だ。

- `remark-preset-lint-recommended` — Markdown として「壊れている」もの（リンクが閉じていない、見出しの抜け、不正な参照など）を弾く
- `remark-preset-lint-consistent` — スタイル系の表記揺れ（箇条書きのマーカー、強調記号、見出しスタイル）を 1 つに揃える

両方入れた上で、リポジトリ独自に厳しくしたいルールがあれば preset の **後ろ** に個別ルールを並べる。たとえば「死んだリンクを error にする」場合はこう書く。

```json
{
  "plugins": [
    "remark-preset-lint-recommended",
    "remark-preset-lint-consistent",
    ["remark-lint-no-dead-urls", "error"]
  ]
}
```

remark の lint プラグインは `.remarkrc` 上では `[name, level]` または `[name, [level, options]]` という入れ子のタプルで書く。`level` に取れる値は `"off"` / `0`（無効化）、`"warn"` / `"on"` / `1`（警告）、`"error"` / `2`（エラー）の 3 段階。preset 全体を取り込んでから後ろに個別ルールを並べることで、preset の挙動を局所的に上書きできる構成にしやすい。

## GFM / frontmatter / toc を組み合わせる

3 つはそれぞれ役割が違う。

- **`remark-gfm`** — GitHub Flavored Markdown 拡張（テーブル、タスクリスト、取り消し線、自動リンク）を mdast 側で理解させる。これを入れないと表が普通の段落として認識されてしまう
- **`remark-frontmatter`** — YAML / TOML の frontmatter を「ただのテキスト」ではなく `yaml` / `toml` ノードとしてパースする。Hugo / Astro / Docusaurus の Markdown を扱うときは必須
- **`remark-toc`** — `## 目次` や `## Table of Contents` といった見出しの**直下**に、本文の見出しから自動生成した目次を書き込む。元記事の言うとおり、見出しを基準に毎回更新されるので「目次がずれている」状態が消える

`remark-toc` の `heading` オプションは正規表現として解釈される。日本語のリポジトリと英語のリポジトリを跨いで使いたい場合、Qiita 記事と同じく `"目次|table of contents"` を入れておけば両方の見出し名で目次セクションを認識してくれる。

```json
[
  "remark-toc",
  {
    "heading": "目次|table of contents",
    "maxDepth": 3
  }
]
```

`maxDepth` は目次に含める見出しレベルの上限。3 にしておくと `###` までで切れて、長くなりすぎない。

## husky + lint-staged で pre-commit に組み込む

「PR を開いてから CI で気づく」のは遅いので、コミット前に `*.md` だけ走らせる。

```bash
pnpm add -D husky lint-staged
pnpm exec husky init
```

`.husky/pre-commit` を以下に置き換える。

```bash
pnpm lint-staged
```

`package.json` に `lint-staged` 設定を足す。

```json
{
  "lint-staged": {
    "*.md": [
      "remark --frail --quiet",
      "remark --output --quiet"
    ]
  }
}
```

`lint-staged` はステージ済みのファイルパスを各コマンドの末尾に自動で渡す。つまり実行されるのは `remark --frail --quiet path/to/changed.md` のようなコマンドで、リポジトリ全体ではなく変更ファイルだけを対象にできる。順序も大事で、まず `--frail` で lint エラーがあれば即停止し、通った場合だけ `--output` で整形を書き戻す。書き戻された差分は `lint-staged` が再ステージしてくれる。

## CI で `--frail` を使う

CI で警告を見落とさないために `--frail` を使う。元記事はこのフラグの挙動を次のように説明している。

> `--frail`: warning も1で終了する

つまり remark は通常 error のときだけ exit 1 を返すが、`--frail` を付けると warning レベルでも exit 1 になる。「壊れていないけど推奨されない書き方」も全て CI で落としたい場合に効く。

GitHub Actions なら、こんな感じで一段だけ足せばいい。

```yaml
name: lint

on: [push, pull_request]

jobs:
  remark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: pnpm/action-setup@v6
      - uses: actions/setup-node@v6
        with:
          node-version: 22
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm remark:lint
```

ローカルの pre-commit と CI で同じ設定 (`.remarkrc`) を参照する形になるので、ローカルで通ったものが CI で落ちる事故は起きにくい。

## VS Code 連携

エディタ側でも同じルールを当てたい場合は、unified が公式に出している [Remark](https://marketplace.visualstudio.com/items?itemName=unifiedjs.vscode-remark) 拡張を入れる。`.vscode/settings.json` に以下を書くと、保存時に `remark-cli` と同じ整形が走る。

```json
{
  "[markdown]": {
    "editor.defaultFormatter": "unifiedjs.vscode-remark",
    "editor.formatOnSave": true
  }
}
```

`.remarkrc` を共通の設定として参照するので、CLI / pre-commit / エディタの 3 か所で挙動が一致する。

## textlint / markdownlint との立ち位置

似たカテゴリのツールがいくつかある。優劣ではなく目的別の使い分けで考えるとよい。

- **markdownlint** — ルールが pre-baked で導入が一番速い。スタイルの揃え屋として強い。AST 変換はしない
- **textlint** — 日本語表現のチェック（ですます調の混在、冗長な表現など）に強い。技術文書の文章品質を上げる用途で重宝する
- **remark** — AST 変換ができるので、lint だけでなく目次生成・リンク書き換え・Markdown 同士の変換・MDX 拡張など **書き換え系** に強い

remark と textlint は併用しやすい（textlint は文章品質、remark は構造）。markdownlint と remark-lint は守備範囲が重なるので、整形やプラグインで何かしたいなら remark に寄せる方が一貫する。

## まとめ — リポジトリの Markdown を「機械可読」に保つ

remark CLI の設定で得られるのは、ざっくり次の 4 つだ。

1. **構造の機械可読化** — 目次・見出しレベル・リンクの整合性が CI で保証される
2. **表記揺れの解消** — 箇条書きや強調記号がリポジトリ全体で揃う
3. **ワンソース運用** — `.remarkrc` を 1 つ置けば CLI / pre-commit / VS Code で同じ挙動になる
4. **AI が読みやすいドキュメント**: 目次が常に最新で、frontmatter が分離されていて、構造が一定 — つまり LLM のコンテキスト窓を浪費しない

Markdown は LLM 時代に入ってから「人間が読む文書」と「機械が読む文書」の二面性が一気に強くなった。remark を仕込んでおくと、その両方を同じ設定で面倒見られるのが嬉しい。

## 参考リンク

- [AI エージェントにきちんと「参照」させるMarkdown術 〜目次を自動生成してContext効率を上げる〜](https://qiita.com/semba_yui/items/60246a8831e466b508cc) — @semba_yui、本記事のきっかけになった元記事
- [remark — GitHub](https://github.com/remarkjs/remark)
- [unified — 公式サイト](https://unifiedjs.com/)
- [remark-toc — GitHub](https://github.com/remarkjs/remark-toc)
- [remark-preset-lint-recommended — GitHub](https://github.com/remarkjs/remark-lint/tree/main/packages/remark-preset-lint-recommended)
- [remark-preset-lint-consistent — GitHub](https://github.com/remarkjs/remark-lint/tree/main/packages/remark-preset-lint-consistent)
