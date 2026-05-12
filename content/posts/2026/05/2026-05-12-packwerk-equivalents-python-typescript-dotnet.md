---
slug: 2026-05-12-packwerk-equivalents-python-typescript-dotnet
title: "他言語に Packwerk はあるか — Python・TypeScript・.NET のモジュラーモノリス境界強制ツール 2026 年版"
date: 2026-05-12
lastmod: 2026-05-12
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "Packwerk（Ruby）の他言語版を一次情報で比較。Python は Tach と Import Linter、TypeScript は dependency-cruiser を中心とした三層、.NET は internal + NsDepCop + ArchUnitNET。2026 年版の現在地。"
categories: ["ツール/開発環境"]
tags: ["モジュラーモノリス", "architecture", "python", "typescript", "dotnet", "packwerk", "tach", "dependency-cruiser", "nsdepcop", "archunitnet", "静的解析"]
---

前回の [Modular Monolith に回帰する大手サービス](/blogs/posts/2026/05/2026-05-11-modular-monolith-large-services/) では、Shopify・Amazon Prime Video・Segment の事例から「1 デプロイ単位 + 明示的なモジュール境界」というアーキテクチャの輪郭を描いた。同時に [モジュラーモノリス](/blogs/wiki/concepts/modular-monolith/) の最大の弱点として「境界は気をつけるだけでは崩れる、CI で必ず落とす仕組みが要る」とも書いた。Ruby/Rails 側ではその役割を Shopify の [Packwerk](/blogs/wiki/tools/packwerk/) が担っている。

本稿はその続編として、**Python（Django）・TypeScript（Node.js）・C#（.NET）** で同じ役を担う実装が何で、何が「Packwerk 相当」と呼べて何が呼べないのかを、一次情報で並べる。PHP / Ruby は本家なのでスキップする。

## Packwerk が解いている問題のおさらい

Packwerk が CI に組み込んでブロックしているのは、ざっくり言えば次の 2 種類の違反だ。

1. **依存違反** (`enforce_dependencies`): pack ごとに `package.yml` で「依存して良い相手」を宣言し、それ以外への参照を禁止する。
2. **可視性違反** (`enforce_privacy`): 各 pack の `app/public/` 配下のクラスだけを公開 API として扱い、`app/private/` への外部参照を禁止する。

これらはいずれも、Ruby/Rails のソースを constant 参照レベルで静的解析して検出される。重要なのは、**Ruby に `internal` 修飾子も package private も存在しない**という前提だ。Java の `internal` パッケージや Go の `internal/` ディレクトリのような **言語ネイティブの境界強制機構**がないからこそ、Packwerk のような「外付け」が必要になる。この前提を頭の片隅に置いておくと、他言語に行ったとき何が変わるかが見えやすい。

## Python / Django

Python も Ruby と同じく、言語ネイティブの境界強制機構を持たない。アンダースコア prefix は PEP 8 の弱い慣習にすぎず、`__all__` も `from foo import *` を制限するだけだ。そのため Packwerk と同じ「宣言 + 静的解析 + CI 失敗」型のツールが、独立に 2 つ育っている。

### Tach — Packwerk 哲学に最も近い

[Tach](https://github.com/tach-org/tach)（PyPI: 0.34.1、2026-04 時点）は Y Combinator 出身の Gauge が開発しているツールで、自己紹介に "A Python tool to maintain a modular package architecture" と書かれている通り、明示的に modular monolith をターゲットにしている。実装は Rust + Python のハイブリッドで、大規模リポジトリでも高速。

設定は `tach.toml` 1 つに集約され、

- **依存宣言** (`depends_on`): 各モジュールが import して良い相手を列挙
- **public interface** (`public`): モジュール外に公開するシンボルを限定
- **`deprecated`**: 既存の違反を「いずれ消す」とマークして段階的に厳格化

という構成になっている。これは Packwerk の `package.yml` の `dependencies:` と `enforce_privacy` をほぼ 1:1 で写し取ったメンタルモデルだ。`tach init` で既存リポジトリから初期状態を抽出し、`tach check` を CI に流すフローも Packwerk と同じ。**Packwerk 哲学を Python に持ち込むなら、現時点でこれが第一候補**になる。

### Import Linter — 大規模実績で勝負する古参

[Import Linter](https://github.com/seddonym/import-linter)（PyPI: 2.11、2026-03 時点、約 1,030 stars）はもう一つの本命。哲学は少し違っていて、**「契約タイプ」を選んで組み合わせる**汎用方式を取る。

- `forbidden`: 特定モジュールからの import を禁止
- `layers`: レイヤード設計（上位→下位の単方向）を強制
- `independence`: 並列なモジュール群が互いに参照しないことを保証
- `acyclic_siblings`: 兄弟モジュール間の循環依存を禁止

エネルギーリテイラーの Kraken Technologies（Octopus Energy 系列）が、**27,637 モジュール・400 開発者**の Python モノリスに **40 以上の contracts** を載せて全 PR を CI でブロックしている事例を [EuroPython のブログ](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/) で公開している。違反を放置しているレガシー部分は `ignore_imports` で除外しつつ、バーンダウングラフで可視化しながら漸進的に潰していく運用だ。**「契約の組み合わせで設計を表現する」発想は Packwerk より柔軟だが、その分どう書くかをチームで決める負担も大きい**。

### Django 特有の運用

Django 専用の Packwerk 相当 OSS は、2026 年現在ほぼ存在しない。普及している運用は、Django の `INSTALLED_APPS` を **そのまま package 境界として使い、Import Linter または Tach を適用する**パターンだ。

- 各 Django app の `models.py` は private 扱い（他 app から ForeignKey で参照しない、ID 経由で疎結合化）
- 各 app に `services.py` か `selectors.py` を置き、ここを public API とする
- 跨ぐデータは Python dataclass / Pydantic などの DTO に詰め替える

このパターンは Makimo の [Modular Monolith in Django](https://makimo.com/blog/modular-monolith-in-django/) や [kokospapa8/majestic-monolith-django](https://github.com/kokospapa8/majestic-monolith-django) などで紹介されている。Tach の `public` 宣言と組み合わせると、Django のディレクトリ規約と Packwerk 的な可視性管理がきれいに重なる。

### 紛らわしいもの: deptry / Ruff / vulture

並べて誤解されがちだが、これらは Packwerk 相当ではない。

- **deptry**: `pyproject.toml` の依存宣言と実際の import 文の整合性チェック専門。**外部パッケージの過不足検出**であって内部モジュール境界には触らない。
- **Ruff の `SLF001` (private-member-access)**: クラスの `_attr` 参照を検出するだけで、モジュール越境の `_func` import は対象外。
- **vulture**: dead code 検出ツール。境界違反検出ではない。

これらは Import Linter / Tach と「併用する」ものであり、置き換え候補ではない。

## TypeScript / Node.js

TypeScript には Packwerk の役割を単独で担うデファクトが存在しない。代わりに**静的解析・型ビルド・ランタイム DI・モノレポ**といった複数のレイヤーで部分的に解いてきた歴史があり、現実のスタックは何枚かを重ねることで Packwerk 相当を再現する。

### dependency-cruiser — Packwerk に最も近い単体ツール

[dependency-cruiser](https://github.com/sverweij/dependency-cruiser)（v17.4.0、2026-05、6.6k stars）が TypeScript 側で Packwerk に最も哲学的に近い。Acorn パーサで JS/TS の import/require を静的解析し、`.dependency-cruiser.js` に書いた `forbidden` ルールに違反したら CI を赤くする。

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

Packwerk が `app/public/` の規約で表現するものを、dependency-cruiser は forbidden ルールの DSL に書き下す。代わりに**循環依存検出・孤立モジュール検出・「shared と称しているが単一参照しかない」検出**など、Packwerk の領分の外にある分析も同じツールで賄える。CI 統合は ESLint 形式の出力＋終了コード、可視化は dot / mermaid / JSON。

### eslint-plugin-boundaries — エディタ即時 DX

[eslint-plugin-boundaries](https://github.com/javierbrea/eslint-plugin-boundaries)（v6.0.2、2026-03）は ESLint プラグインなので、保存するたびにエディタ内で違反が赤線になる。ファイルパスから "element types"（controller / service / model など）を推定し、`boundaries/element-types` ルールで「どの type からどの type を import して良いか」を宣言する。

dependency-cruiser との関係は補完的だ。「**エディタで即フィードバックは eslint-plugin-boundaries、CI 詳細解析は dependency-cruiser**」という二段構えが定石になっている。

### Nx と Turborepo — モノレポの境界

[Nx の `@nx/enforce-module-boundaries`](https://nx.dev/features/enforce-module-boundaries) は、プロジェクトごとに `tags: ["scope:client", "scope:shared"]` 等を付与し、ESLint ルールでタグ間の依存制約を表現する。モノレポでパッケージ数が増えた場合の管理コストには注意が必要で、dependency-cruiser を CI 補完として併用する記述も少なくない。

[Turborepo Boundaries](https://turborepo.dev/docs/reference/boundaries)（experimental）は別アプローチで、**`package.json` の `dependencies` に未宣言の cross-package import** をエラーにする。pnpm / npm の workspace を「Packwerk の pack に最も近い表現」として使うための機構と言える。

### TypeScript Project References — 型レベルのソフト境界

`tsconfig.json` の `composite: true` + `references` を使えば、別プロジェクトを `.d.ts` 経由でしか参照できなくなる。これは**型レベルのソフト境界**で、循環参照は構造的に不可能になる一方、強制力は CI ツールほど強くない。dependency-cruiser と組み合わせて初めて Packwerk 並みの厳格さに届く。

### Next.js / Hono / NestJS / AdonisJS — フレームワーク側の機構

ここは誤解の余地が大きいので慎重に扱う。

- **Next.js (App Router)** には [private folders](https://nextjs.org/docs/app/getting-started/project-structure) (`_folder`)、route groups (`(group)`)、[`server-only`](https://www.npmjs.com/package/server-only) パッケージがある。`server-only` を import するファイルがクライアントコンポーネントから読まれるとビルドが落ちる。これは **「サーバ/クライアントの境界」を build-time に強制する**という点で、Packwerk の `private/` に最も近い「言語/フレームワーク側で持っている境界機構」だ。
- **Hono** は micro framework なので、`app.route('/book', bookApp)` で別 Hono インスタンスをマウントするモジュール分割パターンを提供するが、**境界強制は提供しない**。dependency-cruiser 等の外付けが必須。
- **NestJS** の `@Module({ imports, providers, exports })` は **DI スコープのランタイム境界**だ。`providers` に登録していないサービスは DI から解決できないが、TypeScript の import 自体は通る。静的な物理境界としては効かない。
- **AdonisJS** は公式ドキュメントの自己紹介が "The batteries-included TypeScript framework"（[adonisjs.com](https://adonisjs.com/) 確認、2026-05-12）で、**「modular monolith framework」と謳ってはいない**。IoC Container と Service Providers のライフサイクル制御は Laravel 系で modular なコードベースを書く土台として優秀だが、import 境界の静的強制ではない。

結論として、TypeScript で Packwerk 思想を最も忠実に再現するなら、**dependency-cruiser（CI 厳格）+ eslint-plugin-boundaries（エディタ即時）+ TypeScript Project References（ビルド分離）の三層**を組むのが現実解で、フレームワーク選択（Next.js / Hono / NestJS / AdonisJS）はそれと直交する。

## C# / .NET

.NET の景色は Ruby や Python とかなり違う。**言語仕様に組み込まれた `internal` 修飾子と assembly 境界**が、Packwerk が解いている問題の大半をすでに解いているからだ。

### まず言語ネイティブ機構を使い切る

C# の `internal` キーワードは、Go の `internal/` パッケージとほぼ同じ意味で「**同一 assembly 内からのみ可視**」を表す。1 module = 1 csproj/assembly に分けてしまえば、`internal` で隠したクラスは他モジュールから**コンパイル時に参照不可能**になる。これは Ruby に存在しない非常に強い隔離で、Packwerk の `enforce_privacy` の大半をコンパイラが自動で担う。

テスト assembly にだけ internal を見せたい場合は [`InternalsVisibleTo`](https://learn.microsoft.com/en-us/dotnet/fundamentals/runtime-libraries/system-runtime-compilerservices-internalsvisibletoattribute) 属性、csproj 側なら `<InternalsVisibleTo Include="MyModule.Tests" />` を使う。**Packwerk が CI で検出している違反の 7 割くらいは、csproj を割って `internal` を活用するだけで消える**、というのが .NET の実情だ。

### NsDepCop — Roslyn analyzer による namespace 強制

それでも assembly を割らない（割れない）場合、あるいは namespace レベルの細かい境界を入れたい場合は [NsDepCop](https://github.com/realvizu/NsDepCop)（NuGet: 2.7.0、2025-12 時点）が **Packwerk に最も哲学的に近い**ツールだ。Roslyn analyzer として動作し、`config.nsdepcop`（XML）に namespace ルールを宣言すると、

- IDE 内でリアルタイムに赤線が引かれる
- `dotnet build` で警告 or エラーになる
- `[CheckAssemblyDependencies]` 属性で assembly 間ルールも検査できる

という挙動になる。Packwerk と同じ「宣言ファイル + 静的解析 + ビルド失敗」だが、コンパイラに統合されている分、Packwerk より深く言語と一体だ。なお GitHub Releases ページは v2.4.0（2024-09）までだが NuGet 配布は継続中で、最新版は v2.7.0（2025-12 公開）。README にも「以降のバージョンは NuGet 側で公開する」と明記されている。

### ArchUnitNET / NetArchTest — 「アーキテクチャをテストとして書く」

もうひとつの主要アプローチが、Java の ArchUnit 系統だ。

- [ArchUnitNET](https://github.com/TNG/ArchUnitNET)（NuGet: 0.13.3、2026-03、TngTech 公式）
- [NetArchTest](https://github.com/BenMorris/NetArchTest)（v1.3.2、2021-05、本家は数年止まっており、コミュニティ fork の `NetArchTest.eNhancedEdition` が事実上の後継）

これらは IL を Mono.Cecil で読み、xUnit / NUnit / MSTest のテストとして fluent API で書く。

```csharp
Types.InAssembly(typeof(BillingModule).Assembly)
    .That().ResideInNamespace("Foo.Billing")
    .Should().NotHaveDependencyOn("Foo.Orders.Internal")
    .GetResult().IsSuccessful.Should().BeTrue();
```

違反は `dotnet test` で落ちる。NsDepCop が「コンパイル時のリンタ」なら、こちらは「**テストランナーに乗せた境界**」だ。チームがすでに xUnit / NUnit に慣れていれば、こちらの方が導入抵抗は低い。

### MediatR + Vertical Slice Architecture — 設計パターン側の支援

ツールではなく**設計パターン**として、MediatR を使った Vertical Slice Architecture が定着している。各モジュールを「Endpoint + Handler + Validator + Persistence の縦切り」で構成し、モジュール間通信は MediatR の `IRequest` / `INotification` のみに限定する。Jimmy Bogard 発、Milan Jovanović・Anton Martyniuk らが普及させてきた構成だ。

ただし MediatR は 2024〜25 年に有償化されており、Anton Martyniuk らが「MediatR なしで同じ構成を組む」記事を出している。**MediatR は推奨スタックというより「歴史的に普及した一つの実装」**として捉えると良い。

### dotnet/eShop と modular monolith の公式サンプル状況

Microsoft の現行リファレンスアーキテクチャ [dotnet/eShop](https://github.com/dotnet/eShop)（10.4k stars）は .NET Aspire を用いた **services-based** 構成で、modular monolith バリアントは公式には提供されていない。GitHub Discussions の [#263 "Best Practices for Modular monolith"](https://github.com/dotnet/eShop/discussions/263) が 2024-03-09 にオープンされ、industry が modular monolith から始めるのが主流である現状を踏まえて公式サンプルを求める声が続いているが、2026-05 時点で対応のサンプルは出ていない。

実質のリファレンスはコミュニティ側にあり、

- [kgrzybek/modular-monolith-with-ddd](https://github.com/kgrzybek/modular-monolith-with-ddd)（13.6k stars）— DDD ベースの完成度の高いサンプル
- [ardalis/modulith](https://github.com/ardalis/modulith)（v1.1.2、2024-10）— `dotnet new` テンプレート

このあたりが事実上の出発点になっている。

### .NET の三層

まとめると、.NET で Packwerk 相当を組むときの典型構成は次の三層だ。

1. **言語ネイティブ層**: csproj 分割 + `internal` + `InternalsVisibleTo`
2. **静的解析層**: NsDepCop（namespace 強制を Roslyn analyzer で）
3. **テスト層**: ArchUnitNET または NetArchTest（より複雑なアーキテクチャ規約をテストとして表現）

Ruby に対して 1 つ余計に「言語ネイティブ層」が乗っているのが、.NET の最大の特徴だ。

## 横断比較表

各言語の「Packwerk 相当」を 1 枚にまとめると次のようになる。

| 言語 | Packwerk 相当（最近似） | 解析の哲学 | 言語ネイティブの境界 | 代表的な実績 |
|------|------|------|------|------|
| Ruby | **Packwerk** | 規約 + 静的解析 + CI | なし | Shopify 2.8M LoC |
| Python | **Tach** / Import Linter | 宣言 + 静的解析 + CI | なし | Kraken Technologies 27.6k modules |
| TypeScript | **dependency-cruiser** | 汎用 forbidden ルール | (Project References のみソフト) | Next.js の `server-only` / `_folder` が build-time 強制 |
| .NET | **NsDepCop** + ArchUnitNET | Roslyn analyzer / アーキテクチャテスト | `internal` + assembly（強い） | コミュニティに `kgrzybek/modular-monolith-with-ddd` |
| Go | `internal/` ディレクトリ | 言語仕様 | あり | 言語に組み込み |
| Java | ArchUnit / `module-info` | テスト + JPMS | あり | Spring 系大型 |

それぞれのツールが「同じ問題」を「違うレイヤー」で解いていることがわかる。

## どう選ぶか

実務で迷ったときの優先順位はだいたいこうだ。

1. **言語ネイティブの境界があれば、まず使い切る**。.NET の `internal` + csproj、Go の `internal/`、Java の `module-info` は、外付けツールより圧倒的に強い。CI 構成も増えない。
2. **言語ネイティブが無い場合（Ruby / Python / TypeScript）**は、「宣言ファイル + 静的解析 + CI 失敗」型のツールを 1 つ採用する。Ruby → Packwerk、Python → Tach か Import Linter、TS → dependency-cruiser。
3. **「テストで書く」か「宣言で書く」か**は好み。Packwerk / Tach / NsDepCop は宣言派、ArchUnit / ArchUnitNET / NetArchTest はテスト派。両立可だがメンテ対象を増やさない方が無難。
4. **エディタ即時フィードバックだけに頼らない**。eslint-plugin-boundaries や Roslyn analyzer はエディタで赤くなるが、エディタを開かない人もいる。**最終的な砦は CI が落ちること**で、これが Packwerk の本質。
5. **既存違反は ignore + バーンダウン**。Packwerk の `deprecated_references`、Tach の `deprecated`、Import Linter の `ignore_imports` のように、既存違反を凍結して新規違反だけブロックする機構があるツールを選ぶ。最初から全部直そうとすると入らない。

## まとめ

- Packwerk は Ruby に internal が無いから生まれた。同じ前提の **Python（Tach / Import Linter）と TypeScript（dependency-cruiser ほか三層）** には、それぞれ独立に同等品が育っている。
- **.NET は言語ネイティブの `internal` + assembly 分割**で Packwerk の役割の大半をコンパイラが担う。NsDepCop と ArchUnitNET / NetArchTest が残りを埋める。Microsoft 公式の modular monolith リファレンスは 2026-05 時点で未公開。
- フレームワーク（Hono / Next.js / NestJS / AdonisJS）の選択は、境界強制ツールの選択と直交する。`server-only` や `_folder` のような **フレームワーク側のビルド時境界**だけは独自の強みなので併用する価値がある。
- 重要なのは **CI で必ず落ちること** と、**既存違反を凍結して新規だけ止める** こと。これが守れていれば、ツールの好みは派閥の話に留まる。

## 関連 Wiki

- [Modular Monolith（モジュラーモノリス）](/blogs/wiki/concepts/modular-monolith/) — 1 デプロイ単位＋明示的境界の上位アーキテクチャパターン
- [Packwerk](/blogs/wiki/tools/packwerk/) — Ruby/Rails 向けの本家ツール

## 参考リンク

### Python

- [Tach (GitHub)](https://github.com/tach-org/tach)
- [Tach Docs (gauge.sh)](https://docs.gauge.sh/)
- [Import Linter (GitHub)](https://github.com/seddonym/import-linter)
- [Import Linter Contract Types](https://import-linter.readthedocs.io/en/latest/contract_types.html)
- [Kraken Technologies' Python monolith (EuroPython blog)](https://blog.europython.eu/kraken-technologies-how-we-organize-our-very-large-pythonmonolith/)
- [Modular Monolith in Django (Makimo)](https://makimo.com/blog/modular-monolith-in-django/)
- [kokospapa8/majestic-monolith-django](https://github.com/kokospapa8/majestic-monolith-django)

### TypeScript

- [dependency-cruiser (GitHub)](https://github.com/sverweij/dependency-cruiser)
- [eslint-plugin-boundaries (GitHub)](https://github.com/javierbrea/eslint-plugin-boundaries)
- [Nx — Enforce Module Boundaries](https://nx.dev/features/enforce-module-boundaries)
- [Turborepo Boundaries (experimental)](https://turborepo.dev/docs/reference/boundaries)
- [TypeScript Project References](https://www.typescriptlang.org/docs/handbook/project-references.html)
- [Next.js — Project Structure & Private Folders](https://nextjs.org/docs/app/getting-started/project-structure)
- [server-only (npm)](https://www.npmjs.com/package/server-only)
- [NestJS — Modules](https://docs.nestjs.com/modules)
- [AdonisJS](https://adonisjs.com/)
- [Hono — Routing](https://hono.dev/docs/api/routing)

### .NET

- [NsDepCop (GitHub)](https://github.com/realvizu/NsDepCop)
- [NsDepCop on NuGet](https://www.nuget.org/packages/NsDepCop)
- [ArchUnitNET (GitHub)](https://github.com/TNG/ArchUnitNET)
- [ArchUnitNET Docs](https://archunitnet.readthedocs.io/en/stable/guide/)
- [NetArchTest (GitHub)](https://github.com/BenMorris/NetArchTest)
- [Microsoft Learn — InternalsVisibleToAttribute](https://learn.microsoft.com/en-us/dotnet/fundamentals/runtime-libraries/system-runtime-compilerservices-internalsvisibletoattribute)
- [dotnet/eShop (GitHub)](https://github.com/dotnet/eShop)
- [dotnet/eShop Discussion #263 — Best Practices for Modular monolith](https://github.com/dotnet/eShop/discussions/263)
- [kgrzybek/modular-monolith-with-ddd](https://github.com/kgrzybek/modular-monolith-with-ddd)
- [ardalis/modulith](https://github.com/ardalis/modulith)
- [Milan Jovanović — Vertical Slice Architecture](https://www.milanjovanovic.tech/blog/vertical-slice-architecture)
- [Anton Martyniuk — Building Modular Monolith with VSA in .NET](https://antondevtips.com/blog/building-a-modular-monolith-with-vertical-slice-architecture-in-dotnet)

### Packwerk と比較

- [Shopify/packwerk (GitHub)](https://github.com/Shopify/packwerk)
- [Enforcing Modularity in Rails Apps with Packwerk — Shopify Engineering](https://shopify.engineering/enforcing-modularity-rails-apps-packwerk)
- [Modular Monolith に回帰する大手サービス（前記事）](/blogs/posts/2026/05/2026-05-11-modular-monolith-large-services/)
