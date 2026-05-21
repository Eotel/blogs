---
title: ヘキサゴナルアーキテクチャの実務ガイド ── 原典 inside/outside 原理から DDD・Clean Architecture・フレームワーク別パターンまで
slug: 2026-05-20-hexagonal-architecture-practical-guide
date: 2026-05-20
lastmod: 2026-05-20
draft: false
author: eotel
model: claude-opus-4-7
description: ヘキサゴナルアーキテクチャ（Ports and Adapters）を Cockburn 原典・Martin の Clean Architecture・Palermo
  の Onion・Evans の DDD を一次資料で読み比べ、ORM と Domain Entity、Repository、トランザクション境界、認可、GraphQL
  resolver の論点と、Django・FastAPI・Rails・NestJS・Spring Boot・Go での実装パターンを整理する。
showToc: true
categories:
- Web開発
tags:
- architecture
- hexagonal-architecture
- ports-and-adapters
- ddd
- clean-architecture
- onion-architecture
- modular-monolith
- repository-pattern
- design-pattern
- アーキテクチャ
audio_url: https://github.com/Eotel/blogs/releases/download/audio/2026-05-20-hexagonal-architecture-practical-guide.m4a
audio_lang: ja
audio_generated_at: '2026-05-21T05:19:30Z'
audio_source: notebooklm
audio_format: deep_dive
---

ヘキサゴナルアーキテクチャ（**Ports and Adapters** とも呼ばれる）は「層の名前」ではなく、**アプリケーション核心を inside として守り、外部技術を outside に押し出す**ための設計原理です。本稿では Cockburn の原典、Martin の Clean Architecture、Palermo の Onion Architecture、Evans の DDD、各種フレームワーク公式文書を一次資料として参照しながら、現代実務での適用判断を整理します。

![ヘキサゴナルアーキテクチャ周辺概念の流れを示すタイムライン図。2003 年の Fowler POEAA と Evans DDD から始まり、2005 年 Cockburn の Hexagonal Architecture、2008 年 Palermo の Onion Architecture、2012 年 Martin の Clean Architecture、2015 年 Evans DDD Reference までを年表形式で示す](/blogs/images/hexagonal-architecture-timeline.png)

## エグゼクティブサマリ

**ヘキサゴナルアーキテクチャ**は、Alistair Cockburn が 2005 年の原典で **Ports and Adapters** の別名として提示した設計様式です。意図は「UI なし・DB なしでもアプリケーションを動かせるようにする」ことであり、自動回帰テスト、ヘッドレス実行、外部プログラム連携を容易にすることが原典の動機でした。原典で重要なのは「左と右」ではなく「内側と外側」の非対称であり、六角形は "6 が重要だから" ではなく、一次元の層図から離れて複数のポートを描きやすくするための視覚的比喩です。

Cockburn は原典で次のように intent を明示しています:

> Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases.
>
> — Alistair Cockburn, [Hexagonal architecture (the original 2005 article)](https://alistair.cockburn.us/hexagonal-architecture)

その後、Jeffrey Palermo の [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) は「依存は中心へ向かう」と明示し、Cockburn と前提を共有すると述べました。Robert C. Martin の [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) も Hexagonal・Onion・Screaming などを「ほとんど同じ目的」と位置づけ、Dependency Rule を中核に据えました。Martin の言葉は明快です:

> The overriding rule that makes this architecture work is The Dependency Rule. This rule says that source code dependencies can only point inwards.
>
> — Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

現代実務では、Hexagonal は「アプリケーション核心を、HTTP、GraphQL、CLI、メッセージング、DB、外部 API、フレームワークから切り離すための境界設計」として理解するのが最も実用的です。したがって "ディレクトリの形" ではなく、**依存方向・責務分離・テスト可能性**の設計原則として扱うべきです。

DDD との関係は「競合」ではなく「補完」です。Eric Evans の [DDD Reference (2015)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) は、Layered Architecture を説明したうえで、関連パターンとして Hexagonal Architecture を「同等またはより有効に働く」と明記しています。

実務での最重要論点は次の五つです。第一に、ORM モデルをそのまま Domain Entity とみなすか。第二に、Repository を常に作るべきか。第三に、トランザクション境界をどこに置くか。第四に、認可を adapter 側に置くか、application/domain 側に置くか。第五に、GraphQL resolver を use case の代わりにしてしまわないか。これらは教義ではなく、**複雑性・チーム・フレームワーク制約に応じた設計判断**です。

長寿命の SaaS、複数の入出力チャネルを持つ Web API、外部依存の多い業務システム、モジュラモノリス、将来サービス分割の可能性が高いシステムでは、Hexagonal Architecture は高い費用対効果を持ちます。他方、短命な CRUD 管理画面、小規模な内部ツール、フレームワーク慣習に強く乗るだけで十分なアプリでは、厳密な Hexagonal を全面適用すると過剰設計になりやすいです。Palermo 自身も Onion は小さな Web サイト向きではないと述べています。

## 用語定義と歴史

Hexagonal Architecture は、最初から「Controller / Service / Repository の三層」を意味したわけではありません。Cockburn 原典で中心なのは、**アプリケーション境界をまたぐ会話を port として定義し、その外側の技術差異を adapter に閉じ込める**ことです。

### 用語定義

| 用語 | 原典での意味 | 現代実務での意味 | 留意点 |
|---|---|---|---|
| Hexagonal Architecture | Ports and Adapters の別名。hexagon は視覚比喩であり、6 が本質ではない | 依存を内向きに保ち、外部 I/O を adapters に隔離する設計全般 | 「六角形のフォルダ構成」を意味しない |
| Port | "purposeful conversation" を識別する API。外部装置が差し替わっても会話の目的は変わらない | application service の interface、use case input/output boundary を指すことが多い | port の粒度は固定規格ではない。Cockburn は数の選び方は taste と述べる |
| Adapter | 外部デバイスや技術の信号を port の API に変換するもの。GUI、FIT、SQL、mock DB など | Controller、resolver、CLI handler、repository 実装、外部 API client など | Adapter は business rule を持たないのが原則 |
| Primary actor / primary port | アプリケーションを駆動する側。quiescent state から動かす actor | inbound / driving port とほぼ同義で使われることが多い | これは現代の整理であり、厳密な標準用語集ではない |
| Secondary actor / secondary port | アプリケーションが駆動する側。DB や通知先など | outbound / driven port とほぼ同義で使われることが多い | 「DB 側ポートは常に repository だけ」とは限らない |
| Use case / Application service | Cockburn は use cases をアプリ境界で書くべきだと述べた | Clean Architecture では Use Cases 層、Fowler では Service Layer が近い | 用語が違っても責務は「ユースケースの調停」 |

Port について Cockburn は次のように述べています:

> A port identifies a purposeful conversation. There will typically be multiple adapters for any one port, for various technologies that may plug into that port.
>
> — Alistair Cockburn, [Hexagonal architecture](https://alistair.cockburn.us/hexagonal-architecture)

### 歴史的経緯

2003 年には、Martin Fowler の [*Patterns of Enterprise Application Architecture*](https://martinfowler.com/eaaCatalog/) に Transaction Script、Domain Model、Service Layer、Repository、Unit of Work、Active Record、Data Mapper といった、後の Hexagonal / Clean / Onion で参照され続ける部品概念がすでに整理されていました。Eric Evans の DDD も同時期に、ドメインを中心に据えた layered architecture を提示しています。

Cockburn の 2005 年原典は、この流れの中で「UI 側の漏れ」と「DB 側の漏れ」が実は同じ問題、すなわち business logic と外部相互作用の entanglement だと捉え直し、**inside/outside 非対称**を前面に出しました。彼は layered drawing の問題として、境界線が軽視されやすいことと、ポートが二つ以上ある現実を表現しにくいことを挙げています。

2008 年の Palermo は [Onion Architecture](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) を「長寿命で複雑な業務アプリケーション」に適した named pattern として提案し、Cockburn の Hexagonal Architecture と Onion Architecture が「infrastructure を外在化し adapter を書く」という前提を共有すると明言しました。依存は中心に向かう、DB は中心ではなく外部だ、という表現は、後の Clean Architecture に極めて近いです。

2012 年の Martin は [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) で、Hexagonal、Onion、Screaming、DCI、BCE を「似た目的を持つアーキテクチャ群」とまとめ、共通目的を separation of concerns と規定しました。そのうえで Dependency Rule を中核原理に据えています。したがって、Clean Architecture は Hexagonal を**否定した新概念ではなく、それらを統合した説明枠**と読むのが妥当です。

Evans の 2015 [DDD Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) は、Layered Architecture の節で関連パターンとして Hexagonal Architecture が「同等またはそれ以上に有効」と記し、序文では CQRS / Event Sourcing を DDD システムにおける mainstream options と述べています。これは、DDD コミュニティが Hexagonal や CQRS を外部の流行としてではなく、**DDD と結びつく実装オプション**として受け入れてきたことを示します。

## Ports と Adapters の構造

![Ports and Adapters の構造図。左側に REST Controller・GraphQL Resolver・CLI Command・MQ Consumer が並び、それぞれが入力ポート（inbound）を通じて中央の Application Core 内の Use Case と Domain へ流れる。右側には Repository 実装・外部 API Client・MQ Publisher・Mailer が並び、出力ポート（outbound）から各アダプタへ伸びる構造](/blogs/images/hexagonal-ports-adapters.png)

Cockburn は、アプリケーションが「いくつかの port を通じて外部のものと会話する」と考えます。port は会話の目的を表す API であり、adapter はその API を GUI、HTTP、バッチ、SQL、フラットファイル、mock DB などの具体的信号へ変換します。本質は「技術」ではなく「会話の目的」です。

原典の primary actor は「アプリケーションを駆動する actor」、secondary actor は「アプリケーションが駆動する actor」です。Cockburn 自身は、それに対応して primary ports/adapters を左または上、secondary ports/adapters を右または下に描くと説明していますが、同時に主目的は left-right ではなく inside-outside にあると強調しています。

現代の実装用語に置き換えると、primary は **inbound / driving**、secondary は **outbound / driven** とみなすと、HTTP controller、GraphQL resolver、CLI command、message consumer などを同じ側に、DB/repository 実装、external API client、message publisher、mailer を別側に整理しやすくなります。これは Cockburn の primary/secondary の定義と、Clean Architecture の input/output port 概念を接続した実務上の整理です。

Cockburn は、use case は外側技術の intimate knowledge を含まず、アプリケーション境界で書かれるべきだと述べています。また、port の数は固定ではなく、極端に use case ごとに分けるのも、すべてを左右 2 個に潰すのも最適ではないとして、2〜4 個程度を好むと述べています。port は "教義的な粒度" ではなく、**会話目的に応じて設計するもの**です。

### primary/secondary と inbound/outbound の対応表

| 観点 | primary | secondary |
|---|---|---|
| Cockburn 原典 | アプリを起動・駆動する actor / port / adapter | アプリが問い合わせ・通知する actor / port / adapter |
| 現代実務の呼び方 | inbound / driving | outbound / driven |
| 代表例 | REST、GraphQL、CLI、batch、MQ consumer | DB、cache、search、mailer、payment API、MQ publisher |
| テストダブル | FIT 的 driver、test harness、fake request | mock DB、stub API、fake publisher |

## 技術要素の配置と主要な未解決論点

以下の表は、Cockburn の inside/outside 原理、Clean Architecture の Dependency Rule、Evans / Fowler の Service Layer・Repository・Domain Model を踏まえた**推奨配置の整理**です。HTTP、GraphQL、CLI、メッセージング、DB などは "技術詳細" であり、原則として core の外側に置きます。

### 技術要素の配置表

| 技術要素 | 推奨位置 | 分類 | 推奨理由 | 典型的な誤配置 |
|---|---|---|---|---|
| REST controller | 外側 | inbound adapter | request/response 変換だけを担う。Cockburn でも UI は外側、Martin でも controllers は interface adapters | controller に業務分岐・トランザクション・ORM 直接呼び出しを置く |
| GraphQL resolver | 外側 | inbound adapter | [resolver](https://www.apollographql.com/docs/apollo-server/data/resolvers) は field/data を埋める関数で運搬路。ユースケースを代替しない | resolver に業務ワークフロー全体を埋め込む |
| CLI command | 外側 | inbound adapter | ヘッドレス実行は original intent の一つ | CLI の main から domain/DB を直接組み立てる |
| MQ consumer | 外側 | inbound adapter | transport 依存を閉じ込め、message を command/use case へ変換する | consumer 内で永続化と業務ルールを直書きする |
| Application service / Use case handler | core | input port 実装 / orchestration | PoEAA の [Service Layer (Randy Stafford 寄稿)](https://martinfowler.com/eaaCatalog/serviceLayer.html) は操作境界を定義し、業務応答を調停し、トランザクションを制御する | 単なる「何でも Service」層になり、ドメインが空洞化する |
| Domain entity / aggregate / value object | core | domain model | [Domain Model](https://martinfowler.com/eaaCatalog/domainModel.html) は data と behavior を併せ持つ | getter/setter の入れ物化 |
| Domain service | core | domain | entity/value object に自然に収まらない重要な過程だけを置く | application service の何でも箱になる |
| Repository interface | core | outbound port | domain/app から見た抽象契約。Evans は aggregate root への global access を提供すると説明 | 全テーブルに generic repository を一律生成する |
| Repository implementation | 外側 | outbound adapter | 永続化技術依存を閉じ込める | interface なしで application/domain へ ORM を露出 |
| ORM model / persistence model | 外側寄り | persistence adapter detail | strict hexagonal では domain object と分ける。[Data Mapper](https://martinfowler.com/eaaCatalog/dataMapper.html) はそれを支える | ORM 基底型を domain 全体へ侵入させる |
| DTO / command / query model | 境界 | boundary data | Martin は boundary を跨ぐデータは simple data structures を推奨 | framework request object をそのまま core に渡す |
| Transaction boundary | 通常は application service | orchestration concern | Service Layer は transactions を制御する | controller/resolver/callback に散在 |
| 認証 | 外側 | adapter/framework concern | HTTP / MQ / CLI の入口で扱うのが自然 | domain entity に JWT/HTTP 知識を持ち込む |
| 業務認可 | application/domain | business rule | 価格変更権限や所有者制約は business rule に近い | adapter のロール判定だけで済ませる |

### ORM と Domain Entity の関係

Fowler の [Active Record](https://martinfowler.com/eaaCatalog/activeRecord.html) は「DB の一行を包み、DB アクセスと domain logic を同じ object に持たせる」パターンです。対して [Data Mapper](https://martinfowler.com/eaaCatalog/dataMapper.html) は、object と database を互いに独立に保つための mapper 層です。

Rails は公式に Active Record を MVC の M と位置づけ、それが data と business logic を表す層だと述べます ([Active Record Basics](https://guides.rubyonrails.org/active_record_basics.html))。一方で、Evans / Fowler 系の rich domain model では、複雑な業務ロジックを persistence 機構から自由に保つことに価値があります。Django も loose coupling を掲げていますが、標準 ORM/Model はフレームワーク中心の開発体験を強く支えます。

したがって、**複雑なコアドメインでは「ORM model ≠ Domain Entity」と分ける**のが堅い推奨です。特に、永続化都合の nullable、lazy loading、change tracking、callback がドメイン規則を歪め始めたら、分離の利益が大きくなります。逆に、単純 CRUD では Active Record 型の統合が経済的です。これは "正しさの問題" より "**複雑性に対する投資対効果**" の問題です。

**推奨パターン**

- 複雑な write-side: Plain Domain Entity + mapper/assembler + repository 実装
- 単純 CRUD: ORM model をそのまま使う妥協も可
- 折衷: read-side は ORM/SQL 直、write-side だけ rich domain

**反例**

- `Order` が ORM 基底クラスを継承し、HTTP serializer annotation と DB annotation と domain rule が同居する
- callback で外部 I/O を起こし、ドメイン不変条件よりフレームワーク順序に支配される

### Repository は必須か

Evans は「repository は aggregate root に対する global access を提供する」ものであり、「direct access が本当に必要な aggregate root にだけ用意せよ」と述べています ([DDD Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf))。Microsoft Learn も DDD/CQRS の文脈で「write-side は repository 経由が有効」「query は別チャネルでもよい」と述べつつ、次のように明記しています:

> Repositories shouldn't be mandatory. Custom repositories are useful for the reasons cited earlier […] However, it isn't an essential pattern to implement in a DDD design or even in general .NET development.
>
> — [Designing the infrastructure persistence layer](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design), Microsoft Learn

したがって、Repository は**原理上は有用だが、教義として必須ではない**、が最も厳密です。Repository を使うべきなのは、永続化差し替え、複数データソース、aggregate 単位の不変条件保護、テスト容易性、bounded context の保護が重要な場合です。使わなくてよいのは、ORM context 自体が十分な abstraction を提供し、domain が軽く、抽象追加が本質的利益を生まない場合です。

**推奨パターン**

- aggregate root ごとに小さな repository interface を定義する
- read 側の複雑検索は query service / read model に逃がす
- repository は domain language で命名する

**反例**

- 全テーブル共通の `IRepository<T>` に CRUD を全部生やす
- repository が ORM のメソッド名を隠すだけの薄いラッパになる
- query まで全部 repository に押し込み、巨大化する

### トランザクション境界

PoEAA の [Service Layer (Randy Stafford 寄稿)](https://martinfowler.com/eaaCatalog/serviceLayer.html) は、available operations を定義し、business logic を包み、transactions を制御すると述べています。複数 aggregate を跨ぐトランザクション戦略の選択肢は [トランザクション戦略カタログ — ACID から Saga まで](/blogs/posts/2026/05/2026-05-11-transaction-strategies-saga-outbox-catalog/) を参照。Rails では transaction block が atomic action を提供し、`save`/`destroy` は自動的に transaction に包まれます。Django では [`ATOMIC_REQUESTS`](https://docs.djangoproject.com/en/6.0/topics/db/transactions/) により view ごとの transaction が可能ですが、公式はトラフィック増大時のオーバーヘッドに注意を促しています。Spring の [`@Transactional`](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html) は proxy を通る外部呼び出しでのみ有効です。SQLAlchemy の Session も単一の virtual transaction を追跡します。

以上から、**業務トランザクションの第一候補は application service / use case** です。controller/resolver 単位、HTTP request 単位、ORM callback 単位に置くと、業務境界と一致しないことが増えます。view/request 単位 transaction はフレームワークが与える convenience であって、常に最適な business boundary ではありません。

Rails の [`after_commit`](https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html) は、DB が permanent state になったあとに外部システムへ作用する場所として有用だと公式が説明しています。これは「メール送信・MQ publish・検索 index 更新は commit 前提で動かすほうが安全」という実務判断を支えます。

**推奨パターン**

- use case 開始時に transaction を開き、aggregate 更新をひとかたまりで commit
- 外部通知は commit 後に実行
- 長い処理・ストリーミングレスポンス・複数接続跨ぎは request 全体 transaction を避ける

**反例**

- GraphQL field resolver ごとに transaction を張る
- ORM callback 内で外部 API へ書き込み
- Spring で self-invocation に `@Transactional` を付けて効くと思い込む

### 認可の層配置

FastAPI の [dependency system](https://fastapi.tiangolo.com/tutorial/dependencies/) は、共有ロジック、DB 接続、security、authentication、role requirements に使えると公式が述べます。Martin は entities は page navigation や security の変化に影響されにくい high-level rule であると説明しています。Evans/Fowler 系では domain layer は business rules を表現する場です。

したがって、認可は二層に分けるのが実務上もっとも安定です。**入口での技術的認証・粗い権限制御**は adapter/framework 側、**業務意味を持つ認可**は application/domain 側です。たとえば「JWT が正しいか」は adapter、「請求確定後は営業担当でも値引き変更できない」は business rule です。これを全部 controller に寄せると rule が散り、全部 domain entity に寄せると JWT/HTTP/tenant context が侵入しやすくなります。

### GraphQL resolver と Use Case の境界

Apollo は resolver を「schema の単一 field にデータを入れる関数」と説明し ([Resolvers](https://www.apollographql.com/docs/apollo-server/data/resolvers))、NestJS も GraphQL operation を data に変える instruction だと述べています ([Resolvers](https://docs.nestjs.com/graphql/resolvers))。Cockburn は use case を外部技術に依存せずアプリケーション境界で書くべきだと説明します。

よって、**resolver は use case そのものではなく inbound adapter** と考えるのがよい整理です。root query/mutation resolver は 1 つの use case を起動し、field resolver は読み取り最適化やデータ結合を担う、という切り分けがもっとも崩れにくいです。resolver が transaction、認可、永続化、外部 API 連携、集約不変条件まで抱え始めたら、boundary が壊れています。

## 他アーキテクチャとの比較とフレームワーク別実装パターン

### Hexagonal と近縁概念の比較表

| 類型 | 提唱者 | 目的 | 依存方向 | 中心 | テスト戦略 | よくある誤解 |
|---|---|---|---|---|---|---|
| Hexagonal | [Cockburn, 2005](https://alistair.cockburn.us/hexagonal-architecture) | inside/outside 分離、UI/DB なしでも動く設計 | 具体技術から core へ向かう | application core と ports | mock DB・test harness による isolated test がしやすい | 六角形の数や形が本質だと思うこと |
| Onion | [Palermo, 2008](https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/) | 長寿命業務アプリで coupling を制御 | すべて中心へ | domain model | infrastructure 外在化により core を単体検証しやすい | 小規模サイトにも全面適用すべきだと思うこと |
| Clean | [Robert C. Martin, 2012](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) | separation of concerns を統合説明 | source dependencies は inward | entities / use cases | UI/DB/framework なしで business rules を test | "層の名前" だけ模倣すればよいと思うこと |
| Layered | [Evans/Fowler 系](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) | 関心分離、上位に loose coupling | 通常は下位層依存、ただし上位を隠す | domain layer | 層ごとの分離テスト | 物理配置と論理層を混同すること |
| DDD | [Eric Evans, 2003/2015](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) | 複雑な core domain を model-driven に扱う | アーキテクチャ様式ではない | domain model / bounded context | aggregate・domain rule 中心のテスト | DDD = repository/service/aggregate の定型実装だと思うこと |
| CQRS | [Greg Young の語を Fowler が紹介](https://martinfowler.com/bliki/CQRS.html) | read/write model を分離 | 読みと書きで別経路可 | command model と query model の分離 | write-side と read-side を別々に最適化 | すべての DDD/Hexagonal に必須だと思うこと |

CQRS について Fowler は、安易な全面適用に対して警告しています:

> Despite these benefits, you should be very cautious about using CQRS. Many information systems fit well with the notion of an information base that is updated in the same way that it's read […] adding CQRS to such a system can add significant complexity.
>
> — Martin Fowler, [CQRS](https://martinfowler.com/bliki/CQRS.html)

実務上は、Hexagonal / Onion / Clean を「同じ家族、表現の重点が違う」とみなすのが有効です。DDD はその家族の "中心に何を置くか" を与え、CQRS は必要な場合に read/write を分離する追加戦術です。逆に、Layered は最小の共通祖先に近く、Hexagonal はその layered thinking を inside/outside へ再構成したものと考えると理解しやすいです。

### フレームワーク別の実装パターン比較

| フレームワーク / 言語 | 公式的な自然形 | Hexagonal との相性 | 実装の要点 | 注意点 |
|---|---|---|---|---|
| Django | [loose coupling を掲げるが、full-stack で quick development を重視](https://docs.djangoproject.com/en/6.0/misc/design-philosophies/) | 中 | `views` を adapter、`services/usecases` を追加、ORM model を persistence モデルとして扱うかは複雑性次第 | `ATOMIC_REQUESTS` は便利だが高負荷時に重い |
| FastAPI | [`APIRouter` と DI が強力。複数ファイル構成も公式が推奨](https://fastapi.tiangolo.com/tutorial/bigger-applications/) | 高 | router を inbound adapter、plain Python の use case、DI で repository/client を注入 | DI が強いぶん "Depends の木" がそのまま業務層になると崩れる |
| Rails | [full-stack + strong conventions、Active Record が business logic を含む M](https://rubyonrails.org/) | 中〜低 | controller を adapter に薄くし、複雑 domain は PORO + repository/mapper へ逃がす | AR callback/validation に業務を詰め込みすぎると境界が曖昧 |
| NestJS | [controllers は request を受け、providers に委譲。DI が強い](https://docs.nestjs.com/providers) | 高 | controller/resolver = adapter、provider = use case/service、repository/client = outbound adapter | "service" という名の巨大クラスができやすい |
| Spring Boot | [特定レイアウトは必須でないが best practices がある](https://docs.spring.io/spring-boot/reference/using/structuring-your-code.html) | 高 | `controller` / `application` / `domain` / `infrastructure` を切りやすい。`@Transactional` は use case に置く | [proxy 前提](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)を誤解すると transaction が効かない |
| Go | [`internal`、`cmd`、package 分割が公式 guidance](https://go.dev/doc/modules/layout) | 高 | `cmd/api-server` を adapter、`internal/<context>/{domain,usecase,adapter}` を分ける | repository/interface の増やしすぎより package 単位の責務分離が重要 |
| TypeScript | [file/module ごとの分割が基本](https://nodejs.org/api/modules.html) | 中 | framework 非依存なら interface と composition で明示的に ports/adapters を作る | 公式に単一の canonical architecture はないため、解釈の比率が高い |

フレームワーク相性の観点では、FastAPI、NestJS、Spring Boot、Go は Hexagonal を比較的素直に載せやすいです。Rails と Django は、フレームワークが提供する ORM/Model 中心の開発体験が強く、厳密な Hexagonal にすると "慣習から外れるコスト" が上がります。ここでは「ドメインの複雑さ」が判断軸になります。単純 CRUD に strict separation を強いるのは、しばしば費用倒れです。

## 適用判断とディレクトリ構成とテスト戦略

### 小規模・中規模・大規模別の適用判断

Palermo は Onion が小さな Web サイト向きではないと述べ、Fowler は modular monolith を保ったうえで必要時に microservices へ分ける議論を紹介しています。

| 規模 | 典型例 | 推奨度 | 最小実装 | 過剰設計の兆候 |
|---|---|---|---|---|
| 小規模 | 単純 CRUD、管理画面、短命な内部ツール | 低〜中 | controller/view を薄くし、domain logic だけ別 module に出す | port を endpoint ごとに量産、repository を全テーブルに作る |
| 中規模 | SaaS の 1 ドメイン、課金・認可・通知あり、外部 API 複数 | 高 | use case / domain / outbound adapter を分離。read/write まで分けるかは任意 | DTO と mapper ばかり増え、core が空洞化する |
| 大規模 | 長寿命業務システム、複数チャネル、複数チーム、将来分割前提 | 非常に高 | bounded context 単位で modular monolith 化し、その内部を hexagonal にする | service 分割の夢だけを見て intra-process の責務分離を怠る |

### 良いディレクトリ構成例

Hexagonal でいちばん重要なのは、`controller` / `service` / `repository` を横に置くことではなく、**文脈ごとに core と adapters を寄せる**ことです。Spring Boot 公式も特定 layout を強制せず、必要なら domain-based structure を勧めています。Go 公式も server logic を `internal` に寄せ、command を `cmd` に置く構成を示します。

```text
src/
  billing/
    domain/
      invoice.ts
      money.ts
      policy.ts
    application/
      ports/
        in/
          issue-invoice.ts
        out/
          invoice-repository.ts
          payment-gateway.ts
      usecases/
        issue-invoice-service.ts
    adapters/
      in/
        rest/
          issue-invoice-controller.ts
        graphql/
          invoice-resolver.ts
        cli/
          issue-invoice-command.ts
      out/
        persistence/
          prisma-invoice-repository.ts
          invoice-record.ts
        external/
          stripe-payment-gateway.ts
  shared/
    kernel/
      clock.ts
      id-generator.ts
```

この構成の利点は、`billing` という業務文脈の内側に `domain` / `application` / `adapters` が閉じており、bounded context と implementation detail が混ざりにくいことです。特にモジュラモノリスでは、この形が将来の切り出し候補単位にもなりやすいです（[Linking Modular Architecture to Development Teams](https://martinfowler.com/articles/linking-modular-arch.html)）。

### 悪いディレクトリ構成例

```text
src/
  controllers/
  services/
  repositories/
  models/
  utils/
  common/
  helpers/
```

この形は、見た目は整理されていても、実際には `services` が何でも箱になり、`models` に ORM と domain が混在し、`utils` に本来の業務概念が流れ込みやすいです。結果として、bounded context より技術分類が優先され、変更理由が分散します。Fowler の [Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html) が起きやすい典型です。

境界をディレクトリ規約だけで守りきるのは難しいため、静的解析で強制する選択肢もあります。Ruby なら [Packwerk](/blogs/wiki/tools/packwerk/)、Python は [import-linter](/blogs/wiki/tools/import-linter/)、TypeScript は [dependency-cruiser](/blogs/wiki/tools/dependency-cruiser/)、.NET は [ArchUnitNET](/blogs/wiki/tools/archunitnet/) が代表例です ([他言語に Packwerk はあるか](/blogs/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/) も参照)。

### テスト戦略

Cockburn の original intent には automated regression tests と mock/in-memory database が含まれています。Martin も Clean Architecture の利点として、UI/DB/web server なしで business rules を test できることを挙げています。

Hexagonal で実際に容易になるのは、次の四層のテストです。

| テスト種別 | 対象 | なぜ容易になるか | 具体例 |
|---|---|---|---|
| Domain test | entity、value object、aggregate | フレームワークや DB を持ち込まないため | 割引計算、請求締め、不変条件 |
| Use case test | application service | fake repository / fake gateway を差し替えられるため | 注文確定、返金実行、権限判定付き更新（[private メソッドに業務ロジックを隠さない設計](/blogs/posts/2026/05/2026-05-12-private-methods-testability-coding-agents/) と相性が良い） |
| Adapter contract / slice test | controller、resolver、repository 実装 | 変換責務だけを切り出せるため | Spring [`@WebMvcTest`](https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html)、Django test client / RequestFactory、Nest TestingModule |
| Integration / E2E | 実配線全体 | 少数に絞りやすいため | HTTP + DB + queue の本番同等経路 |

Spring Boot は test slices を正式に提供し、controller や data access を部分的にロードできます。Django は test client と RequestFactory を提供します。NestJS は TestingModule により provider を差し替えられます。これらは Hexagonal の "adapter を薄くし、差し替えやすくする" 発想と相性がよいです。

### 実務上の利点・欠点・アンチパターン

**利点**

Cockburn、Palermo、Martin の三者に共通する利点は、外部詳細の交換容易性、business rule の保護、テスト容易性です。DB を外側 detail とみなせるため、永続化や UI 変更が core の変更を必ずしも要求しません。

**欠点**

Palermo は小さな Web サイトには不向きと述べます。Fowler は [Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html) を anti-pattern と呼び、service 層へ行動を抜きすぎると Domain Model の費用だけ払って利益を失うと批判しています。Microsoft Learn も repository は必須ではないと述べます。つまり、Hexagonal の欠点は「抽象そのもの」ではなく、**抽象を増やして core を貧血化させること**です。

**典型的アンチパターン**

- 1 endpoint = 1 port = 1 service = 1 repository を機械的に生成する
- framework DTO、ORM entity、domain entity をすべて分けた結果、業務コードより mapping のほうが多い
- repository をテーブル単位で作り、aggregate boundary を壊す
- `service` 層に認可、検証、変換、永続化、通知、ユースケースを全部詰め込む
- 「Hexagonal をやっている」と言いつつ、controller から ORM を直接呼ぶ

## 組織への影響と現代的文脈

### 組織・チームへの影響

Matthew Foster (Thoughtworks) による [Linking Modular Architecture to Development Teams](https://martinfowler.com/articles/linking-modular-arch.html) は、modular architecture の期待利益を encapsulation、abstraction、optionality と整理しています。Microservices を多数運用するには、継続的デリバリと product-centered teams への移行が必要だと James Lewis と Martin Fowler は共著の [Microservices (2014)](https://martinfowler.com/articles/microservices.html) で述べています。

Hexagonal は、単に unit test を増やすためだけでなく、**チーム境界を技術都合より業務文脈に近づける**効果があります。adapter ごとの担当分割は可能ですが、中心は domain/use case です。したがって、組織設計としては「フロント担当」「DB 担当」より、「Billing チーム」「Identity チーム」のような product/domain centered team と相性がよいです。

### 設計レビュー用チェックリスト

実プロジェクトで Hexagonal を維持できているかをレビュー時に確認するための実務チェックリストです。各項目は Cockburn、Martin、Evans、Fowler、各公式フレームワーク文書から導いたものです。

- この use case は HTTP、GraphQL、CLI、MQ のどれでも起動できる形に書かれているか
- core で framework 型、ORM 型、request/response 型を参照していないか
- controller / resolver / consumer は変換と委譲に徹しているか
- トランザクション境界は use case に置かれているか
- repository interface は aggregate root 単位で意味を持っているか
- query の都合で aggregate 内部を直接暴いていないか
- 認証と業務認可を混同していないか
- commit 前に外部副作用を起こしていないか
- domain のふるまいが service 層へ流出しすぎていないか
- テストが domain / use case / adapter / integration の四層に分かれているか

### マイクロサービス、SaaS、モジュラモノリス、AI エージェントへの含意

Fowler は [MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html) で「モノリスから慎重に設計し、ソフトウェア内部のモジュラ性に注意を払う」戦略を論じています（"design a monolith carefully, paying attention to modularity within the software"）。modular monolith は良い出発点になりうるが、in-process の良い interface がそのまま service interface になるとは限らない、というのが Fowler の趣旨です。

このため、現代の最有力な適用先は **modular monolith の内部**です ([Modular Monolith に回帰する大手サービス](/blogs/posts/2026/05/2026-05-11-modular-monolith-large-services/) も参照、Shopify・Amazon Prime Video・Segment の事例)。bounded context ごとに hexagonal にしておけば、SaaS での複数チャネル対応 ([マルチテナント SaaS アーキテクチャ設計ガイド](/blogs/posts/2026/05/2026-05-19-multi-tenant-saas-architecture-guide/))、外部課金・IDP・通知連携、バッチ/CLI/管理 UI 追加に耐えやすくなります。microservices にしても、各 service の中身まで自動で整うわけではないので、service 内の hexagonal は依然として有効です。

GitHub Copilot cloud agent は repository を調査し、実装計画を作り、テストカバレッジ改善や技術的負債への対応を自律的に行えると公式が述べています ([About Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent))。GitHub Copilot は `.github/copilot-instructions.md` によるリポジトリ固有 instructions をサポートし、OpenAI Codex も `AGENTS.md` という独自フォーマットの instructions と subagents によるコードベース探索を支援します。

したがって、AI エージェント時代の Hexagonal の効用は、「人間にわかりやすい」だけではありません。**コードベース探索、変更影響範囲の局所化、custom instructions の記述容易性、adapter ごとの contract 明示**という点で、エージェントにも有利です。特に、`billing/application/ports/out/payment-gateway.ts` のような構造は、"どこに副作用があるか" を機械にも人にも伝えやすい設計です。

## 結論と判断基準

ヘキサゴナルアーキテクチャの本質は、**層の名前**ではなく、**アプリケーション核心を inside として守り、外部技術を outside に押し出すこと**です。六角形は絵にすぎません。より本質的なのは、port を「目的ある会話」として定義し、その境界を越えるデータと依存を制御することです。これは Cockburn の原典、Palermo の Onion、Martin の Clean、Evans の DDD が共有する最小公倍数です。

### 実務上の判断基準

次の条件が 3 つ以上当てはまるなら、Hexagonal を強く検討する価値があります。

- 同じ業務機能を REST、GraphQL、CLI、batch、MQ など複数入口から呼ぶ
- DB、外部 API、課金、認証、通知など副作用源が多い
- ドメインルールが複雑で、UI/ORM 変更と独立に保ちたい
- 長寿命システムで、フレームワーク置換や再配線の可能性が高い
- チームが増え、文脈単位のモジュール境界が必要
- テスト高速化と AI エージェント運用のため、局所性を上げたい

逆に、次なら "軽量版" で十分なことが多いです。

- 単純 CRUD が大半
- ドメインルールが薄い
- システム寿命が短い
- フレームワーク慣習から外れるコストが利益を上回る

### 未解決の論点

業界全体でも統一解がない論点を残しておきます。最終的にはチーム事情で変わります。

- ORM object を domain entity とみなすか、persistence model と分けるか
- repository を write-side に限定するか、query にも使うか
- transaction を request 単位で張るか、use case 単位で張るか
- coarse authorization と business authorization をどこで分けるか
- GraphQL field resolver にどこまで read-side logic を持たせるか
- modular monolith の境界を将来の microservice 境界へどこまで流用できるか
- AI エージェント向け instructions と architectural boundaries をどう対応づけるか

## 主要出典

- Alistair Cockburn, *Hexagonal architecture the original 2005 article* — <https://alistair.cockburn.us/hexagonal-architecture>
- Robert C. Martin, *The Clean Architecture* — <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
- Jeffrey Palermo, *The Onion Architecture : part 1* — <https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/>
- Eric Evans, *DDD Reference 2015* — <https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf>
- Martin Fowler, *Service Layer*, *Repository*, *Active Record*, *Data Mapper*, *Unit of Work*, *Anemic Domain Model*, *CQRS* — <https://martinfowler.com/eaaCatalog/>
- Django 公式文書 — <https://docs.djangoproject.com/en/6.0/>
- FastAPI 公式文書 — <https://fastapi.tiangolo.com/>
- Ruby on Rails Guides / API — <https://guides.rubyonrails.org/>
- NestJS 公式文書 — <https://docs.nestjs.com/>
- Spring Framework / Spring Boot 公式文書 — <https://docs.spring.io/>
- Go / TypeScript / Node.js 公式文書 — <https://go.dev/doc/modules/layout>
- Microsoft Learn, DDD/CQRS persistence guidance — <https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design>
- GitHub Copilot 公式文書 — <https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent>

## 関連記事

- [クリーンアーキテクチャという「型」の暴力 ── 過剰な抽象化が現場を壊すメカニズム](/blogs/posts/2026/03/2026-03-03-0617418777ad8f46ddf3f1d9bfbfb06f/) — 本記事が「適用判断とトレードオフ」を整理する立場なのに対し、こちらは過剰適用の害を批判する立場。両方を読むと、Hexagonal / Clean の "どこまでやるか" のレンジが見えやすい
- [Modular Monolith に回帰する大手サービス — Shopify・Amazon Prime Video・Segment の事例](/blogs/posts/2026/05/2026-05-11-modular-monolith-large-services/) — Hexagonal の最有力適用先である modular monolith の実例
- [ACID から Saga まで — トランザクション戦略 10 種の地図と判断軸](/blogs/posts/2026/05/2026-05-11-transaction-strategies-saga-outbox-catalog/) — 複数 aggregate を跨ぐトランザクションの選択肢
- [他言語に Packwerk はあるか — Python・TypeScript・.NET のモジュラーモノリス境界強制ツール 2026 年版](/blogs/posts/2026/05/2026-05-12-packwerk-equivalents-python-typescript-dotnet/) — Hexagonal の境界を静的解析で強制する手段
- [マルチテナント SaaS アーキテクチャ設計ガイド ── silo / bridge / pool から hybrid 運用まで](/blogs/posts/2026/05/2026-05-19-multi-tenant-saas-architecture-guide/) — SaaS で hexagonal を採るときに併走する論点

## 関連 Wiki

- [Modular Monolith](/blogs/wiki/concepts/modular-monolith/)
- [Packwerk](/blogs/wiki/tools/packwerk/) / [import-linter](/blogs/wiki/tools/import-linter/) / [dependency-cruiser](/blogs/wiki/tools/dependency-cruiser/) / [ArchUnitNET](/blogs/wiki/tools/archunitnet/) — 境界強制ツール
