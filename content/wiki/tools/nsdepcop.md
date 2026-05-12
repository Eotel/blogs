---
title: "NsDepCop"
description: ".NET の namespace 依存制御ツール。Roslyn analyzer として動き、宣言ファイルに違反する import をリアルタイムで赤線・ビルド失敗にする。Packwerk と最も哲学的に近い .NET ツール。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["nsdepcop", "NsDepCop"]
related_posts:
  - "/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/"
tags: ["dotnet", "csharp", "modular-monolith", "アーキテクチャ", "静的解析", "roslyn"]
---

## 概要

[NsDepCop](https://github.com/realvizu/NsDepCop) は C#/.NET 向けの namespace 依存制御ツール。Roslyn analyzer として動作し、`config.nsdepcop`（XML）に宣言したルールに違反する import を IDE 内でリアルタイムに赤線にし、`dotnet build` で警告またはエラーにする。.NET エコシステムで [Packwerk](/blogs/wiki/tools/packwerk/) と最も哲学的に近いツール。

## 詳細

### 仕組み

- **Roslyn analyzer**（コンパイル時に走る静的解析機構）として動作
- `config.nsdepcop` に namespace 単位の許可/禁止ルールを XML で宣言
- IDE 内でリアルタイムにフィードバック（保存不要）
- `dotnet build` でビルド失敗を起こせるので CI 統合は自然
- `[CheckAssemblyDependencies]` 属性で assembly 間ルールも検査できる

### Packwerk との対比

Packwerk と同じ **「宣言ファイル + 静的解析 + ビルド失敗」** の三点セット。違いはコンパイラに統合されている分、Packwerk より深く言語と一体化していること（CLI ツールではなく Roslyn の一部として動く）。

### .NET における位置づけ

.NET には言語ネイティブで `internal` キーワード + assembly 境界という強力な隔離機構があり、1 module = 1 csproj に分ければ Packwerk の役割の大半をコンパイラが自動で担う。NsDepCop は、

- 1 つの assembly 内で **namespace レベル**の細かい境界を入れたい
- csproj 分割まではしたくない（または既にできない）

というケースで活きる。

### バージョン

- NuGet: 2.7.0（2025-12 公開、最新）
- GitHub Releases: v2.4.0（2024-09）で停止、以降は NuGet 側のみで配布
- リポジトリ: `realvizu/NsDepCop`
- 公式 Docs: <https://github.com/realvizu/NsDepCop/blob/master/doc/Help.md>

## 関連ページ

- [Packwerk](/blogs/wiki/tools/packwerk/) — 思想のルーツ
- [ArchUnitNET](/blogs/wiki/tools/archunitnet/) — .NET のもう一つの境界検証アプローチ（テストランナー駆動）
- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) — 上位アーキテクチャパターン

## ソース記事

- [他言語に Packwerk はあるか — Python・TypeScript・.NET のモジュラーモノリス境界強制ツール 2026 年版](/blogs/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/) — 2026-05-12
