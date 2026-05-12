---
title: "ArchUnitNET"
description: "Java の ArchUnit を .NET にポートしたアーキテクチャ検証ライブラリ。アーキテクチャ規約を fluent API のテストとして書き、dotnet test で違反を検出する。"
date: 2026-05-12
lastmod: 2026-05-12
aliases: ["ArchUnitNET", "archunit-net"]
related_posts:
  - "/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/"
tags: ["dotnet", "csharp", "modular-monolith", "アーキテクチャ", "テスト"]
---

## 概要

[ArchUnitNET](https://github.com/TNG/ArchUnitNET) は Java の ArchUnit を .NET にポートしたアーキテクチャ検証ライブラリ。TngTech 公式。**アーキテクチャ規約を fluent API でテストとして書き**、`dotnet test` で違反を検出する。.NET エコシステムで [Packwerk](/blogs/wiki/tools/packwerk/) と同じ問題領域を扱うが、「テストランナーに乗せた境界」というアプローチで [NsDepCop](/blogs/wiki/tools/nsdepcop/) とは哲学的に対照的。

## 詳細

### 仕組み

IL を Mono.Cecil で読み、xUnit / NUnit / MSTest のテストとして fluent API で書く。

```csharp
Types.InAssembly(typeof(BillingModule).Assembly)
    .That().ResideInNamespace("Foo.Billing")
    .Should().NotHaveDependencyOn("Foo.Orders.Internal")
    .GetResult().IsSuccessful.Should().BeTrue();
```

違反は `dotnet test` で落ちる。Layer / Slice / Cycle 検出など豊富な検証ルールを持つ。

### NsDepCop との使い分け

- **NsDepCop**: コンパイル時のリンタ（Roslyn analyzer）。エディタで即時フィードバック
- **ArchUnitNET**: テストランナーに乗せた境界。複雑なアーキテクチャ規約をプログラマブルに書ける
- 両立可。エディタ即時 → コンパイル → テストの 3 段階で多層防御を組む構成もある

### 類似ツール: NetArchTest

[NetArchTest](https://github.com/BenMorris/NetArchTest)（v1.3.2、2021-05）も同じく fluent API でアーキテクチャをテストする系統だが、本家リポジトリは数年メンテが止まっており、コミュニティ fork の `NetArchTest.eNhancedEdition` が事実上の後継となっている。

### バージョン

- NuGet: `TngTech.ArchUnitNET` 0.13.3（2026-03 時点）
- リポジトリ: `TNG/ArchUnitNET`
- 公式 Docs: <https://archunitnet.readthedocs.io/en/stable/guide/>

## 関連ページ

- [NsDepCop](/blogs/wiki/tools/nsdepcop/) — .NET の Roslyn analyzer アプローチ
- [Packwerk](/blogs/wiki/tools/packwerk/) — 思想のルーツ
- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/) — 上位アーキテクチャパターン

## ソース記事

- [他言語に Packwerk はあるか — Python・TypeScript・.NET のモジュラーモノリス境界強制ツール 2026 年版](/blogs/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/) — 2026-05-12
