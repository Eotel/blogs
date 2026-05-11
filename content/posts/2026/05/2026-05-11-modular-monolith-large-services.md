---
title: "Modular Monolith に回帰する大手サービス — Shopify・Amazon Prime Video・Segment の事例"
date: 2026-05-11
lastmod: 2026-05-11
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "Amazon Prime Video、Shopify、Segment、Basecamp が選んだ Modular Monolith アーキテクチャを実例で読み解く。マイクロサービスから戻った理由、monolith / microservice との違い、Packwerk による境界強制、判断軸を整理する。"
categories: ["クラウド/インフラ"]
tags: ["アーキテクチャ", "modular-monolith", "microservices", "shopify", "packwerk"]
---

「マイクロサービスにすればスケールする」「モノリスはもう古い」 ── 2010 年代後半に当たり前のように語られていたこの命題は、2020 年代に入ってから、当事者たち自身の手で書き換えられつつある。Amazon Prime Video が Step Functions + Lambda の分散構成を 1 プロセスに畳み直してコストを 90% 削減し、Segment が 100 を超えるマイクロサービスから単一の Go サービスへ戻り、Shopify が 280 万行の Rails モノリスを「壊さずに」モジュール化する道を選んだ。本稿では、これらの事例から **modular monolith** という選択肢の輪郭を描き、monolith / microservice との違い、利点と欠点、判断軸を整理する。

## なぜ今 modular monolith なのか

2023 年、Amazon Prime Video の Video Quality Analysis (VQA) チームが書いた "Scaling up the Prime Video audio/video monitoring service and reducing costs by 90%" が大きな話題を呼んだ。AWS Step Functions と Lambda、複数の S3 バケットで構成された "教科書どおりのサーバーレス・マイクロサービス" を、単一の ECS タスクに統合することで 90% のコストを削減したという内容で、ステート遷移ごとの S3 経由のフレーム受け渡しを「メモリ上のデータ転送」に置き換えたことが効いた。AWS が自社の主力サービスで「マイクロサービスを止めた」と公言したインパクトは大きく、業界全体が改めて「分散させすぎていないか」を問い直す契機になった。

同時期に、Shopify は "Under Deconstruction: The State of Shopify's Monolith"、Segment は "Goodbye Microservices"、DHH は "The Majestic Monolith" の系譜にあたる発信を通じて、「最初からモノリスを **モジュール化** する」あるいは「マイクロサービスから戻る」道筋を実例として共有してきた。共通するのは、**システム境界とデプロイ境界を一致させない**という発想だ。論理的な責務はきちんと分離するが、物理的なプロセスやデプロイ単位はあえて 1 つに保つ。これが modular monolith の核心である。

## 3 つのアーキテクチャの違い

ここで用語を整理しておく。

### Monolith（モノリス）

1 つのアプリケーションが、ユーザー認証、注文、決済、配送など複数の関心事を内部で分けずに抱えている状態。コントローラ／モデル／ビューといった **技術レイヤ** で分割されていることはあるが、ビジネスドメインを跨ぐ呼び出しが直接行われ、内部 API の概念はない。デプロイは 1 単位。DB も多くの場合 1 つで全テーブルが同居する。

### Modular Monolith（モジュラーモノリス）

外形的にはモノリスと同じ「1 つのデプロイ単位」だが、内部に **明示的なモジュール境界** を持つ。各モジュールは公開された内部 API のみで通信し、他モジュールの内部実装には触れられない。Shopify が `Packwerk` で実現しているのはまさにこれで、Ruby/Rails の constant 参照を静的解析し、「Billing モジュールから Orders モジュールの private な constant を参照していたらビルドを落とす」という強制を入れている。DB は 1 つでも、論理スキーマでモジュールごとに分けることが多い。

### Microservice（マイクロサービス）

1 つのビジネス能力ごとに独立した **プロセス、リポジトリ、デプロイパイプライン、DB** を持つ。サービス間は HTTP / gRPC / イベントバス経由で通信する。各サービスを個別の言語・技術スタックで実装する自由がある一方で、ネットワーク呼び出しのコスト、分散トランザクション、運用の総量が増える。

![モノリス・モジュラーモノリス・マイクロサービスの構造を横並びに比較した図。左から順に、壁のない単一プロセス、内部境界を持つ単一プロセス、独立 DB を持つ複数サービス](/blogs/images/modular-monolith-comparison.png)

主要な属性を表にまとめると次のようになる。

| 観点 | Monolith | Modular Monolith | Microservice |
|------|----------|------------------|--------------|
| デプロイ単位 | 1 | 1 | N |
| プロセス数 | 1 | 1 | N |
| DB | 共有 1 つ | 共有 1 つ（スキーマ分離が一般的） | サービスごと |
| モジュール間通信 | 直接呼び出し | 内部 API | ネットワーク |
| 障害ドメイン | 1 つ | 1 つ | サービス境界で分離 |
| 言語選択 | 単一 | 単一 | サービスごと |
| トランザクション | ローカル ACID | ローカル ACID | 分散・Saga |
| 観測性 | ローカルログ | ローカルログ + モジュールタグ | 分散トレーシング必須 |
| 組織への要求 | 小〜中 | 小〜中 | 多数チームに耐える運用力 |

modular monolith の妙味は、**「将来必要になったら切り出せる準備をしておく」**という選択肢を残しつつ、いま現実に発生している分散コストを払わないことにある。

## 採用事例: 意図的に modular monolith を選んだサービス

### Shopify — 280 万行の Rails モジュラーモノリス

Shopify は世界最大級の Rails アプリケーションのひとつで、2.8M LoC、50 万コミット規模のコードベースを単一のモノリスとして運用し続けている。2017 年に組成された "Break-Core-Up-Into-Multiple-Pieces"（後に "Componentization"）チームが始めたのは、マイクロサービス化ではなく、Rails の慣習的な「コントローラ／モデル／ビュー」というレイヤ分割から、**「Billing」「Orders」「Shipping」といったビジネスドメイン単位の component 分割**への組み換えだった。

2020 年に OSS として公開された [Packwerk](https://github.com/Shopify/packwerk) は、その境界をビルド時に強制するための静的解析ツールだ。コンポーネントごとに `public/` と `private/` のような可視性を定義し、違反したら CI を赤くする。Packwerk 公開時点で約 48 packages、そのうち 30 件で境界強制が導入されていた、と公開されている。Shopify が選んだのは「壊して分散させる」のではなく、**モノリスの内側に境界線を入れていく**道だった。

### GitHub — Rails monolith のパッケージ分割と Trilogy

GitHub も 10 年以上 Rails モノリスとして運用されており、社内では `github/github` リポジトリが中心に据えられている。同社は MySQL ドライバ `Trilogy` の公開、Rails のメインライン貢献、`Vitess` 採用などの周辺技術投資を通じて、**モノリスをスケールさせ続ける**選択を取ってきた。アプリケーション内では Rails Engine やパッケージ単位での内部分割を進めつつ、Pages や Actions などの周辺機能は別サービスとして切り出す **"Citadel" 型** ── DHH が「Majestic Monolith が育つと Citadel になる」と呼んだ形 ── に近い。

## 回帰事例: Microservice から戻ってきたサービス

### Amazon Prime Video — Step Functions から ECS 単一プロセスへ（2023）

冒頭で触れた事例。VQA チームの video/audio monitoring サービスは元々、フレーム抽出 → 各種品質チェッカー → 集約という流れを **Step Functions のステートマシン + 個別の Lambda + S3 バケット** で組んでいた。

ボトルネックは 2 つあった。

1. **Step Functions のステート遷移単価**。毎秒数本のストリームを多数のステップで処理すると、オーケストレーション課金が支配的になった。
2. **S3 経由のフレーム受け渡し**。Tier-1 課金のオブジェクト数が膨れ上がった。

新しい構成では、これらの分散コンポーネントを **単一の ECS タスク** に押し込み、フレームの受け渡しを **インメモリ** に変更した。マイクロサービスの基本前提だった「独立スケール」を諦め、垂直スケールのほうがワークロードに合っていることを認めた格好だ。この事例の整理は同時期に [S3 Files の GA で消えるアーキテクチャ層](/blogs/posts/2026/04/2026-04-09-s3-files-ga-architecture/) で書いた「層の消失」の議論とも通じる。

注意点として、Prime Video 本体（カタログ、CDN、再生）は依然として多数のサービスから成る分散構成であり、**統合されたのはあくまで「監視ワークロード 1 つ」**である。この事例の正しい教訓は「マイクロサービスをやめろ」ではなく、「**ワークロードごとに適切なサイズを選び直せ**」だった。

### Segment — 100 を超えるマイクロサービスから 1 つの monolith へ（2018）

カスタマーデータ基盤の Segment は、2015 年に Centrifuge と呼ぶイベント配信基盤の前段として、各 destination（Google Analytics, Mixpanel, …）ごとに **個別のマイクロサービス + 個別のキュー**を持つ構成に移行した。ハイパーグロース期に destination が毎月 3 つ増え、最終的に 100 以上のサービスが乱立。Alexandra Noonan の "Goodbye Microservices"（2018）はその撤退記録だ。

問題は技術ではなく **運用の総量** だった。100 個の destination はそれぞれ独立した依存パッケージのバージョン管理、独立したオンコールローテーション、独立したリリースを要求し、destination の人気度（QPS）が極端に偏っていたため、リソース効率も悪かった。Segment は全 destination コードを単一リポジトリ・単一バージョン・単一サービスに統合し、運用負荷を激減させた。代償として、「ある destination のバグで他の destination まで落ちる」という障害ドメインの広がりを受け入れている。

### Basecamp / 37signals — "The Majestic Monolith" の継続

DHH は 2016 年の "The Majestic Monolith" 以来、約 12 名のプログラマで 6 プラットフォーム（Web、各種モバイル／デスクトップアプリ、Email）を支えるための現実的な手段として、majestic monolith を擁護し続けてきた。後年 "The Citadel" として、メインの monolith の周りに必要に応じて別プロセス（Action Cable のリアルタイム配信、画像変換など）を **足していく** モデルを提案している。

注目すべきは、彼らがこの 20 年で離れていないこと自体だ。Basecamp 3、Basecamp 4、HEY と、技術スタック（Hotwire など）を更新しながら、デプロイ単位を増やさない方向にずっとコミットしている。

## 利点と欠点

### Modular Monolith の利点

- **デプロイの単純さ**: 1 つの artifact、1 つの kubernetes Deployment（または ECS Service）、1 つの DB マイグレーション順序。「どのサービスとどのサービスを同時にロールバックすればよいか」を考えなくてよい。
- **トランザクションの一貫性**: モジュール間を跨ぐ操作も、ローカル DB トランザクションで完結できる。Saga パターンや outbox を組まなくてよい。
- **レイテンシ**: モジュール間呼び出しがメモリ内のメソッド呼び出しで済む。ネットワーク往復・直列化のコストがゼロ。Prime Video の事例はこのメリットを「フレーム転送のインメモリ化」として最大化したケース。
- **観測性**: 1 プロセスの中の話なので、スタックトレース 1 本で原因に辿り着ける。分散トレーシングを真面目に運用しなくてよい。
- **オンボーディング**: 新メンバーは 1 つのリポジトリを clone するだけで全体像が見える。
- **言語の利点を活かしきれる**: Rails / Spring / Django / Phoenix など、フレームワークの "happy path" に乗れる。

### Modular Monolith の欠点

- **垂直スケールの限界**: 1 プロセスが扱える QPS、メモリ、CPU には物理的な天井がある。マルチプロセス化・シャーディングはできるが、本質的にはレプリケーションでしかない。
- **言語・ランタイム固定**: モジュールごとに別の言語を使う、という選択肢が事実上消える。
- **障害ドメインの集中**: 1 つのモジュールのバグやリーク（メモリ・コネクションプール枯渇）が全体に波及する。Segment の事例はこのリスクを正面から受け入れた例。
- **モジュール境界の腐敗**: 「気をつける」だけでは時間とともに境界が崩れる。Shopify の Packwerk のような **境界強制ツール** を CI に組み込まないと、いつの間にか巨大な泥団子に戻る。

### Microservice 本来の出番

逆に、microservice が本当にハマる場面は次のような条件が複数重なるときだ。

- **チーム数が多い**: 数十〜数百チームが同じコードベースを触り、リリースを直列化できない。
- **コンポーネントごとにスケール特性が極端に違う**: 検索だけ別言語・別ハード、機械学習推論だけ GPU、など。
- **障害ドメインを物理的に分離する必要がある**: 決済が落ちても閲覧は続けたい、など SLO の質が違う。
- **独立した規制要件**: 一部のコンポーネントだけ別リージョン・別 VPC・別アカウントに置く必要がある。

これらが揃わない段階で「将来のスケールに備えて」と早すぎる分散を始めると、Segment や Prime Video のような撤退コストを払うことになる。Martin Fowler が "MonolithFirst" で書いた "you should not start with microservices" は、この見立てを 10 年前に言語化していた。

## どう選ぶか — 判断軸

1. **組織規模（Conway's Law）**: チームが 1〜2 つなら monolith / modular monolith でほぼ間違いない。10 を超えてから microservice を本気で検討する。
2. **スケールの形**: 全体が均一にスケールするのか、特定機能だけが突出するのか。後者なら **その機能だけを切り出す** "Citadel" モデルが第一候補。最初から全部割らない。
3. **障害ドメイン要件**: 「決済が落ちたとき他は生きていてほしい」レベルの SLO 差があるか。なければ無理に分けない。
4. **modulith として育てる**: 最初から modular monolith として書き、Packwerk / Architecture tests / Java の `module-info` / Go の internal package など、**言語ネイティブの境界強制機構** を CI に入れる。境界を守りきれているモジュールは、いつでも独立サービスとして切り出せる。
5. **逆方向の許容**: 切り出したサービスをモノリスに戻す勇気を持つ。Segment と Prime Video が示したのは、「戻す」も等しく正しい判断ということ。

「マイクロサービス」と「モノリス」を二項対立で語る時代は終わっていて、実務的にはその間にある **modular monolith** をデフォルトに据え、本当に必要なところだけ切り出すというのが、2020 年代後半のマジョリティの結論に近い。

## まとめ

- Modular monolith は「1 つのデプロイ単位」と「明示的なモジュール境界」を両立させるアーキテクチャ
- Shopify、GitHub、Basecamp など、最初から意図的に採用している大手は多い
- Amazon Prime Video（監視ワークロード）、Segment は、過剰なマイクロサービス化からの **撤退** で大きな成果を出した
- 利点はデプロイ・トランザクション・レイテンシ・観測性。欠点は垂直スケール限界・障害ドメイン集中・境界腐敗
- 判断軸は「組織規模 × スケールの形 × 障害ドメイン要件」。デフォルトを modular monolith に置き、必要箇所だけ切り出すのが現実的

## 参考リンク

- [Scaling up the Prime Video audio/video monitoring service and reducing costs by 90% (Prime Video Tech blog — Wayback Machine)](https://web.archive.org/web/20231230202019/https://www.primevideotech.com/video-streaming/scaling-up-the-prime-video-audio-video-monitoring-service-and-reducing-costs-by-90)
- [Prime Video Switched from Serverless to EC2 and ECS — InfoQ](https://www.infoq.com/news/2023/05/prime-ec2-ecs-saves-costs/)
- [Return of the Monolith: Amazon Dumps Microservices for Video Monitoring — The New Stack](https://thenewstack.io/return-of-the-monolith-amazon-dumps-microservices-for-video-monitoring/)
- [Deconstructing the Monolith: Designing Software that Maximizes Developer Productivity — Shopify Engineering](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity)
- [Under Deconstruction: The State of Shopify's Monolith — Shopify Engineering](https://shopify.engineering/shopify-monolith)
- [Enforcing Modularity in Rails Apps with Packwerk — Shopify Engineering](https://shopify.engineering/enforcing-modularity-rails-apps-packwerk)
- [Shopify/packwerk (GitHub)](https://github.com/Shopify/packwerk)
- [Goodbye Microservices: From 100s of problem children to 1 superstar — Alexandra Noonan / Twilio (旧 Segment)](https://www.twilio.com/en-us/blog/developers/best-practices/goodbye-microservices)
- [Why Segment Returned to a Monolith from Microservices — InfoQ](https://www.infoq.com/news/2018/07/segment-microservices/)
- [The Majestic Monolith — Signal v. Noise (DHH)](https://signalvnoise.com/svn3/the-majestic-monolith/)
- [The Majestic Monolith can become The Citadel — Signal v. Noise (DHH)](https://signalvnoise.com/svn3/the-majestic-monolith-can-become-the-citadel/)
- [Building Basecamp 4 — HEY world (DHH, Wayback Machine)](https://web.archive.org/web/2021/https://world.hey.com/dhh/building-basecamp-4-405a347f)
- [MonolithFirst — martinfowler.com](https://martinfowler.com/bliki/MonolithFirst.html)

## 関連 Wiki

このトピックは Wiki に未収録。後続の `/wiki-ingest` 実行で `content/wiki/concepts/modular-monolith.md` 等として取り込まれる予定。
