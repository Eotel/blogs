---
title: "Import Linter"
description: "Python のレイヤード設計・依存関係を強制する静的解析ツール。Forbidden / Layers / Independence / Acyclic Siblings などの契約タイプを組み合わせて境界を表現する。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["import-linter", "importlinter"]
related_posts:
  - "/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/"
tags: ["python", "modular-monolith", "アーキテクチャ", "静的解析"]
---

## 概要

[Import Linter](https://github.com/seddonym/import-linter) は Python のモジュール境界強制ツール。`.importlinter` または `pyproject.toml` に **契約（contracts）** を宣言し、CI で違反を検出する。[Packwerk](/blogs/wiki/tools/packwerk/) や [Tach](/blogs/wiki/tools/tach/) と同じ問題領域を扱うが、哲学が少し違っていて、**「契約タイプを選んで組み合わせる」汎用方式**を取る。

## 詳細

### 主要な契約タイプ

- **forbidden**: 特定モジュールからの import を禁止
- **layers**: レイヤード設計（上位→下位の単方向）を強制
- **independence**: 並列なモジュール群が互いに参照しないことを保証
- **acyclic_siblings**: 兄弟モジュール間の循環依存を禁止
- **protected** / **custom** など

「契約の組み合わせで設計を表現する」発想は Packwerk より柔軟だが、その分どう書くかをチームで決める負担も大きい。

### 大規模採用事例: Kraken Technologies

エネルギーリテイラーの Kraken Technologies（Octopus Energy グループ）が、**27,637 モジュール・400 開発者**の Python モノリスに **40 以上の contracts** を載せて全 PR を CI でブロックしている。違反を放置しているレガシー部分は `ignore_imports` で除外しつつ、バーンダウングラフで可視化しながら漸進的に潰していく運用。詳細は [EuroPython のブログ](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/) に書かれている。

### Tach との使い分け

- **新規 Python monolith** → Tach（Packwerk と最も思想が近い、Rust で高速）
- **既存大規模 monolith** → Import Linter（実績豊富、契約タイプの組み合わせで段階移行しやすい）

### バージョン

- PyPI: 2.11（2026-03 時点）
- リポジトリ: `seddonym/import-linter`
- 公式 Docs: <https://import-linter.readthedocs.io/>

## 関連ページ

- [Tach](/blogs/wiki/tools/tach/) — Python のもう一つの境界強制ツール
- [Packwerk](/blogs/wiki/tools/packwerk/) — 思想のルーツ
- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) — 上位アーキテクチャパターン

## ソース記事

- [他言語に Packwerk はあるか — Python・TypeScript・.NET のモジュラーモノリス境界強制ツール 2026 年版](/blogs/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/) — 2026-05-12
