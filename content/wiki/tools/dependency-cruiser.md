---
title: "dependency-cruiser"
description: "JavaScript/TypeScript の依存関係を静的解析して forbidden ルールに照らす検証ツール。Packwerk 思想を TypeScript で最も忠実に再現する単体ツール。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["dependency-cruiser", "dep-cruiser"]
related_posts:
  - "/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/"
tags: ["typescript", "javascript", "modular-monolith", "アーキテクチャ", "静的解析"]
---

## 概要

[dependency-cruiser](https://github.com/sverweij/dependency-cruiser) は JavaScript / TypeScript の依存関係を静的解析して、`.dependency-cruiser.js` に書いたルールに違反したら CI を赤くするツール。TypeScript エコシステムで [Packwerk](/blogs/wiki/tools/packwerk/) 思想に最も哲学的に近い単体ツール。

## 詳細

### 仕組み

Acorn パーサで JS/TS/CoffeeScript の **import/require を静的解析**（ES6/CJS/AMD 対応）。設定ファイルに `forbidden` / `allowed` ルールを宣言する。

```js
// .dependency-cruiser.js（抜粋）
forbidden: [
  {
    name: 'no-cross-feature-internals',
    severity: 'error',
    from: { path: '^src/features/([^/]+)' },
    to: { path: '^src/features/(?!$1)[^/]+/internal' },
  },
]
```

### Packwerk との対比

- 共通点: パッケージ単位の依存方向を CI で強制する
- 違い: Packwerk が「`app/public/` だけ公開」の強い規約を組込で持つのに対し、dependency-cruiser は forbidden ルールに書き下す汎用方式
- 代わりに **循環依存検出・孤立モジュール検出・「shared と称しているが単一参照しかない」検出** など、Packwerk の領分の外にある分析も同じツールで賄える

### TypeScript で Packwerk 思想を再現するスタック

dependency-cruiser だけでは賄えない部分は他のレイヤーで補う。

1. **dependency-cruiser**: CI 厳格な解析
2. **eslint-plugin-boundaries**: エディタ即時フィードバック
3. **TypeScript Project References** (`composite: true`): 型レベルでのビルド分離

この三層を組むのが TypeScript における事実上の Packwerk 相当。

### バージョン

- npm / GitHub: v17.4.0（2026-05 時点、6.6k stars）
- リポジトリ: `sverweij/dependency-cruiser`
- 公式 Docs: <https://github.com/sverweij/dependency-cruiser/blob/main/doc/>

## 関連ページ

- [Packwerk](/blogs/wiki/tools/packwerk/) — 思想のルーツ
- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) — 上位アーキテクチャパターン

## ソース記事

- [他言語に Packwerk はあるか — Python・TypeScript・.NET のモジュラーモノリス境界強制ツール 2026 年版](/blogs/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/) — 2026-05-12
