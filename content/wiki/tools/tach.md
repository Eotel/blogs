---
title: "Tach"
description: "Python の modular monolith 境界強制ツール。Packwerk 哲学を最も忠実に Python に持ち込み、Rust 実装で高速。tach.toml に dependencies と public interface を宣言する。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["tach", "tach-org/tach", "gauge-sh/tach"]
related_posts:
  - "/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/"
tags: ["python", "modular-monolith", "アーキテクチャ", "静的解析", "rust"]
---

## 概要

[Tach](https://github.com/tach-org/tach) は Python 向けの modular monolith 境界強制ツール。自己紹介に "A Python tool to maintain a modular package architecture" と明記され、明示的に [Packwerk](/blogs/wiki/tools/packwerk/) と同じ問題領域を狙っている。Rust + Python のハイブリッド実装で、大規模リポジトリでも高速に解析できる。Y Combinator 出身の Gauge が開発。

## 詳細

設定は `tach.toml` 1 つに集約される。

- **依存宣言** (`depends_on`): 各モジュールが import して良い相手を列挙
- **public interface** (`public`): モジュール外に公開するシンボルを限定（Packwerk の `app/public/` に相当）
- **`deprecated`**: 既存の違反を「いずれ消す」とマークして段階的に厳格化

Packwerk の `package.yml` の `dependencies:` と `enforce_privacy` をほぼ 1:1 で写し取ったメンタルモデル。`tach init` で既存リポジトリから初期状態を抽出し、`tach check` を CI に流すフローも Packwerk と同じ。

### Python の言語特性との関係

Python には Go の `internal/` ディレクトリや C# の `internal` キーワードのような **言語ネイティブの境界強制機構が無い**。PEP 8 のアンダースコア規約は弱い慣習にすぎず、`__all__` も `from foo import *` の制限だけ。そのため Packwerk と同じ「宣言 + 静的解析 + CI 失敗」型の外付けツールが必要になり、Tach はその第一候補に位置づけられる。

### バージョン

- PyPI: 0.35.0（2026-05 時点）
- リポジトリ: `tach-org/tach`（旧 `gauge-sh/tach` から移動済み、redirect は機能する）
- 公式 Docs: <https://docs.gauge.sh/>

## 関連ページ

- [Packwerk](/blogs/wiki/tools/packwerk/) — Tach が思想を受け継いだ Ruby 側の原典
- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) — 上位アーキテクチャパターン
- [Import Linter](/blogs/wiki/tools/import-linter/) — Python のもう一つの境界強制ツール（契約タイプを組み合わせる柔軟方式）

## ソース記事

- [他言語に Packwerk はあるか — Python・TypeScript・.NET のモジュラーモノリス境界強制ツール 2026 年版](/blogs/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/) — 2026-05-12
