---
title: "remark"
description: "unified エコシステム上の Markdown プロセッサ。AST 変換基盤により lint・整形・目次生成・MDX 拡張など書き換え系処理が得意。"
date: 2026-05-16
lastmod: 2026-05-16
aliases: ["remark-cli", "remarkjs"]
related_posts:
  - "/posts/2026/05/2026-05-13-remark-cli-setup-guide/"
tags: ["markdown", "lint", "unified", "ast", "developer-tools"]
---

## 概要

[remark](https://github.com/remarkjs/remark) は [unified](https://unifiedjs.com/) AST 変換基盤の上に乗った Markdown プロセッサ。Markdown を `mdast`（抽象構文木）に読み込み、プラグインで変換し、再び Markdown に書き戻す。CLI 版 `remark-cli` でリポジトリ全体の Markdown を一括処理できる。

## 主なプラグイン

| プラグイン | 役割 |
|---|---|
| `remark-preset-lint-recommended` | 壊れた Markdown（リンク未閉じ、見出し抜けなど）を弾く |
| `remark-preset-lint-consistent` | 箇条書きマーカー・強調記号など表記揺れを統一 |
| `remark-gfm` | GFM 拡張（テーブル・タスクリスト・取り消し線）を mdast で理解 |
| `remark-frontmatter` | YAML / TOML frontmatter を専用ノードとしてパース |
| `remark-toc` | 指定見出し直下に本文の見出しから目次を自動生成・更新 |

## 最小セットアップ

```bash
pnpm add -D remark-cli remark-preset-lint-recommended \
  remark-preset-lint-consistent remark-gfm \
  remark-frontmatter remark-toc
```

`.remarkrc`（JSON）：

```json
{
  "plugins": [
    "remark-preset-lint-recommended",
    "remark-preset-lint-consistent",
    "remark-gfm",
    ["remark-frontmatter", ["yaml"]],
    ["remark-toc", { "heading": "目次|table of contents", "maxDepth": 3 }]
  ],
  "settings": { "bullet": "-", "emphasis": "*", "strong": "*" }
}
```

`package.json` scripts：

```json
{
  "remark:lint": "remark . --frail --quiet",
  "remark:fix": "remark . --output --quiet"
}
```

`--output` でファイルを書き戻す（目次再生成含む）。`--frail` は warning でも exit 1 にする CI 用フラグ。

## 他ツールとの使い分け

| ツール | 強み | 弱み |
|---|---|---|
| **remark** | AST 変換・目次生成・書き換え系 | 設定が多少複雑 |
| markdownlint | pre-baked ルール・導入が速い | 変換系は不可 |
| textlint | 日本語文章品質チェック | Markdown 構造は扱わない |

remark と textlint は**併用しやすい**（remark で構造、textlint で文章品質）。markdownlint と remark-lint は守備範囲が重なるため、どちらか一方に統一するとよい。

## husky / lint-staged / CI 連携

- **pre-commit**: lint-staged で `*.md` だけ走らせる。`--frail` でエラー確認 → `--output` で整形書き戻し
- **CI**: GitHub Actions で `pnpm remark:lint`（`--frail` 付き）
- **VS Code**: `unifiedjs.vscode-remark` 拡張 + `formatOnSave: true` で `.remarkrc` を共有

## LLM 向けドキュメントとしての活用

目次の自動生成・frontmatter の分離・見出し構造の統一により、LLM がファイルを head から読む際のトークン浪費を抑えられる。AI エージェントに参照させる Markdown リポジトリの品質管理として有効。
