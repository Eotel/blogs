---
slug: 2026-05-11-transaction-strategies-saga-outbox-catalog
title: "ACID から Saga まで — トランザクション戦略 10 種の地図と判断軸"
date: 2026-05-11
lastmod: 2026-05-11
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "分散トランザクションの 10 戦略（ACID・2PC・Saga・Outbox・Inbox・TCC・Event Sourcing・CQRS・補償・Idempotency Key）を一覧比較。判断フローと PostgreSQL + Python による Outbox 実装例つき。"
categories: ["クラウド/インフラ"]
tags: ["分散トランザクション", "saga", "outbox", "tcc", "event-sourcing", "postgresql"]
---

[前回の記事](/blogs/posts/2026/05/2026-05-11-modular-monolith-large-services/)で「modular monolith なら Saga や outbox は要らない」と書いた。逆に言えば、デプロイ単位を分けた瞬間からこれらの仕組みが要る。本稿はその「分けたあとの世界」で使える戦略を一覧で並べ、選び方の地図を示す試みだ。スコープはアプリケーション層のパターンに限定し、DB 内部の MVCC / WAL / 2PL、Raft や Paxos などのコンセンサスアルゴリズム、Spanner の TrueTime、ブロックチェーン的合意は本稿の外に置く。

## トランザクションが守ろうとしている 4 つの性質

教科書の復習から始める。RDB のトランザクションが提供する性質は ACID と呼ばれる。

- **A**tomicity: 全部成功するか全部失敗するか
- **C**onsistency: 事前事後の制約を保つ
- **I**solation: 同時実行されても直列実行と区別できない
- **D**urability: コミットしたら消えない

単一ノードの RDB はこれらを当然のように提供してくれるので、ふだん意識しなくて済む。

分散環境ではこれが崩れる。複数の DB やサービスに書き込みを跨がせると、まず A が脆くなる（片方は書き込み済、片方は失敗）。次に I も脆くなる（中間状態が他から観測される）。CAP 定理が言うのは「ネットワーク分断時に C か A のどちらかを諦める」だが、実務的には PACELC が示すように、分断していない平時でもレイテンシ（L）と一貫性（C）のトレードオフが残る。

つまり分散システムにおける「トランザクション戦略」とは、**どの整合性をどれだけ犠牲にして、どの不変条件を守るか**の設計選択でしかない。整合性には強整合性（書いた瞬間に全ての読み手が同じ値を見る）から結果整合性（しばらく経てば同じ値に収束する）までのスペクトラムがあり、これから紹介する 10 のパターンはその上の異なる地点を占めている。

## 戦略カタログ

各戦略は「概要 / 使いどころ / 落とし穴」の 3 点で短くまとめる。

### ローカル ACID トランザクション

**概要**: 単一 DB に対する `BEGIN ... COMMIT`。複数行・複数テーブルへの書き込みを 1 つの原子操作にまとめる、いちばん古典的で強力な仕組み。

**使いどころ**: 単一 DB（または同一クラスタ内の論理スキーマ）で完結するなら常に第一候補。Shopify や Basecamp のような modular monolith が選んでいるのは結局これだ。

**落とし穴**: 「スケールしないから分散させた」が早すぎる判断であるケースは多い。PostgreSQL や MySQL は今や数 TB と数万 TPS を扱う。本当にスケール限界に達したのか、それともシャーディングや読み取りレプリカで十分なのかを先に検証すべき。

### 2PC / XA（2 フェーズコミット）

**概要**: コーディネータが全参加者に prepare を投げ、全員 OK なら commit、誰かが NG なら abort を投げる古典的な分散トランザクションプロトコル。XA はそのインターフェース規格。

**使いどころ**: 同一データセンター内の RDB と MQ を強整合に揃えたい局面、あるいはレガシーの XA トランザクションマネージャ（JTA / MSDTC など）が既にある環境。

**落とし穴**: コーディネータが SPOF になり、prepare 後にコーディネータが落ちると参加者のロックが解放されないブロッキング問題が残る。マイクロサービス間で 2PC を使う設計は事実上のアンチパターンで、Pat Helland の有名な小論 [Life Beyond Distributed Transactions](https://www.ics.uci.edu/~cs223/papers/cidr07p15.pdf)（2007）はこの結論を初めて言語化した。

### Saga パターン — Choreography（コレオグラフィ）

**概要**: 各サービスがイベントを購読し、自分の処理が終わったら次のイベントを発火することでフロー全体を駆動する。中央の制御点を置かず、振り付け（choreography）のように各サービスが自律的に動く。

**使いどころ**: サービスを後から増やしやすくしたい、特定サービスに権限を集中させたくないとき。EC の `OrderCreated → InventoryReserved → PaymentCompleted → ShipmentDispatched` の連鎖は典型例。

**落とし穴**: 全体フローが「どこにも書かれていない」状態になる。新メンバーが「注文すると何が起きるのか」を追うとき、コードベース全体を grep する羽目になる。イベントの循環や、サービス追加に伴うイベント順序の暗黙の前提崩れにも注意。

### Saga パターン — Orchestration（オーケストレーション）

**概要**: オーケストレータが状態機械として全体フローを管理し、各サービスに命令（コマンド）を送って応答を集める。ワークフローエンジン（Temporal、Camunda、Step Functions など）がよく担う役割。

**使いどころ**: フローが複雑で可視化したい、SLA を中央で管理したい、補償を統一的に実行したいとき。

**落とし穴**: オーケストレータに業務ロジックが集中して肥大化しがち。AWS Step Functions のように状態遷移ごとに課金されるエンジンを使う場合、**細かすぎる粒度で組むと課金が支配的になる**（[Prime Video の事例](/blogs/posts/2026/05/2026-05-11-modular-monolith-large-services/)が典型）。

![Saga パターンの Choreography と Orchestration を比較した構成図。前者はイベント連鎖、後者は中央オーケストレータが各サービスを統制する](/blogs/images/saga-choreography-vs-orchestration.svg)

### 補償トランザクション（Compensating Transaction）

**概要**: Saga の中で失敗が起きたとき、それまでに成功したステップを「意味的に取り消す」操作。`ReserveStock` に対する `ReleaseStock`、`ChargeCard` に対する `RefundCard` のように、業務的な逆向き操作を用意する。

**使いどころ**: Saga を採用したら必ず必要になる。技術的なロールバック（DB の ROLLBACK）と違い、「決済から 3 分経ったので返金処理を別途走らせる」のような業務的アクションを取ることになる。

**落とし穴**: 補償できない操作（メール送信、決済代行への通知、外部 API への副作用）は本質的に「取り消せない」。設計時点で、各ステップを「保留 → 確定」と分けるか、補償可能な抽象に置き換える必要がある。これが次の TCC につながる。

### Transactional Outbox

**概要**: DB への業務更新と「あとで publish するイベント」の記録を**同一トランザクション**で行う。別プロセスのリレーワーカーが outbox 行を読んでメッセージブローカに送る。

**使いどころ**: DB と Kafka / RabbitMQ / SQS への二重書き込みが避けられない全ての場面。Saga やイベント駆動アーキテクチャを採るなら、ほぼ必須の足回り。

**落とし穴**: 「DB に書いた直後に publish して、失敗したら DB から消す」という素朴な実装は、プロセスがその間にクラッシュすると DB だけ更新されてイベントが失われる。Outbox はこの破綻を構造的に防ぐ。詳細は後段の実装サンプルで。

### Inbox（冪等受信）

**概要**: 受信側に重複検知用のテーブル（inbox）を置き、`event_id` を UNIQUE 制約で記録することで、同じイベントが二度処理されないようにする。

**使いどころ**: メッセージブローカが at-least-once 配送（重複あり）の場合、つまり実質的にすべての本番環境。Kafka は exactly-once セマンティクスを謳うが、その内部もこの種の仕組みで実現されている。

**落とし穴**: Inbox テーブルが無限に膨らむので、TTL や定期的なアーカイブが要る。また、業務処理と Inbox への書き込みを同一トランザクションでやらないと意味がない。

### TCC（Try-Confirm-Cancel）

**概要**: 各サービスが操作を 3 つに分ける。**Try** は将来確定するための資源を予約し（例: 在庫を仮押さえ）、**Confirm** は予約を確定し、**Cancel** は予約を解放する。Saga が事後の補償で巻き戻すのに対し、TCC は事前の予約で確定を遅らせる。

**使いどころ**: 金融系の残高ホールド、ホテル / 航空券の仮押さえ、在庫の確保枠など、業務的に「確定前の状態」を表現できる領域。中国系のオープンソース（Seata、ByteTCC など）でよく実装されている。

**落とし穴**: 全サービスが Try / Confirm / Cancel の 3 つのエンドポイントを提供する必要があり、API 設計の負担が大きい。タイムアウトした Try の自動 Cancel をどう保証するかも非自明（基本はオーケストレータの責務）。

### Event Sourcing

**概要**: アプリケーションの状態を「現在のスナップショット」ではなく「過去に起きたイベントの追記列」として永続化する。現在状態は必要に応じてイベント列をリプレイして組み立てる。

**使いどころ**: 監査要件が強い（金融、医療、会計）、過去の任意時点の状態を再現したい、時間軸の分析を後付けでやりたいといった領域。アグリゲートの粒度がはっきりしている DDD と相性が良い。

**落とし穴**: スキーマ変更（イベントスキーマの版管理）と、リプレイのレイテンシ、スナップショット運用が新しい設計負担として乗る。「現状の読み取りクエリが書きにくい」という弱点は CQRS で補うのが定石。**Event Sourcing は強力だが導入コストが高く、流行で採るとほぼ後悔する**。

### CQRS（Command Query Responsibility Segregation）

**概要**: 書き込みモデルと読み取りモデルを分離する。書き込み側はドメインモデル、読み取り側はクエリ最適化されたビュー（マテリアライズドビューや専用テーブル）を用意する。

**使いどころ**: Event Sourcing と組で使うのが典型。読み取り負荷と書き込み負荷の特性が大きく違う領域、レポーティングが重い領域。

**落とし穴**: 本稿の文脈では「トランザクション戦略」というよりは補助パターン。読み取りモデルの更新がイベント経由になるため、結果整合性が前提になる点だけは押さえておきたい。

### Idempotency Key（冪等性キー）

**概要**: クライアントが生成した一意キーをリクエストヘッダ等で送り、サーバ側で同じキーの再実行を**同じ結果**に短絡させる。Stripe API の `Idempotency-Key` ヘッダが事実上の標準。

**使いどころ**: ネットワーク再送、リトライ、メッセージ重配信のすべてに対応する横串パターン。上記の戦略のどれを採っても、結局これがないと「at-least-once 配送 + 副作用ある処理」が成立しない。

**落とし穴**: キーの保存期間、同じキーで違うペイロードが来たときの扱い、保存テーブルのインデックスサイズなど、地味な運用設計が要る。「重複を弾く」だけでなく「最初の結果をそのまま返す」が本来のセマンティクス。

## 戦略の比較

| 戦略 | 一貫性 | 複雑度 | レイテンシ | 運用負荷 | 代表ユースケース |
|------|--------|--------|------------|----------|------------------|
| ローカル ACID | 強 | 低 | 低 | 低 | 単一 DB の業務処理全般 |
| 2PC / XA | 強 | 中 | 中〜高 | 高 | DB と MQ を同期させたい局面（限定的） |
| Saga (Choreography) | 結果整合性 | 中 | 低 | 中 | EC、注文フロー、疎結合な統合 |
| Saga (Orchestration) | 結果整合性 | 中〜高 | 中 | 中 | 複雑な業務フロー、可視化したいフロー |
| 補償トランザクション | 結果整合性 | 中 | 低〜中 | 中 | Saga と組で必須 |
| Transactional Outbox | 結果整合性 | 低〜中 | 低 | 低〜中 | DB + イベント発行が必要なすべて |
| Inbox（冪等受信） | 結果整合性 | 低 | 低 | 低 | at-least-once 配送の受信側 |
| TCC | 強寄り | 高 | 中 | 高 | 残高ホールド、仮押さえ系 |
| Event Sourcing | 結果整合性 | 高 | 中 | 高 | 監査・時系列重視ドメイン |
| CQRS | 結果整合性 | 中 | 低（読み取り側） | 中 | 読み書きの負荷特性が大きく異なるドメイン |
| Idempotency Key | — | 低 | 低 | 低 | 全戦略の前提となる横串 |

タイトルで「10 種」と書いたのは上記のうち冪等性キー以外の 10 戦略のことで、Idempotency Key は独立した戦略というより全戦略の前提として下に敷く横串パターンとしてカウント外にしている。CQRS も厳密にはトランザクション戦略というより読み書き分離の補助パターンだが、Event Sourcing と組で語られることが多いので一覧には含めた。「強寄り」と書いた TCC は、Try で資源を確保した時点で他の同時更新を排除できるため、純粋な Saga より整合性が強い。Outbox / Inbox / Idempotency Key の 3 つは独立した戦略というより、横串インフラとして全戦略の下に敷くもの（詳細は次節の判断フロー）。

## いつ何を選ぶか — 判断フロー

迷ったらこの順で考える。

![トランザクション戦略の選択フローを示した決定木の図。出発点は「トランザクションが必要」で、単一 DB で完結するならローカル ACID、跨ぐ場合は強整合性必須なら 2PC、そうでなければ補償可能性で Saga か TCC を選ぶ。下部に Outbox・Inbox・Idempotency Key が「どの戦略でも必要な横串パターン」として配置されている](/blogs/images/transaction-strategy-flow.svg)

1. **単一 DB で完結するか？** Yes ならローカル ACID で終わり。マイクロサービスありきで考えない。
2. **強整合性が業務要件か？** 銀行残高の同期、在庫の超過引き当て禁止など、「結果整合性では事故になる」要件があるかを正直に問う。多くは結果整合性で十分。
3. **補償アクションを業務として定義できるか？** Yes なら Saga（Orchestration を第一候補）。
4. **予約状態を持つほうが自然か？** 残高ホールドや座席予約など、確定までに時間が空くなら TCC。
5. **どれを選んでも、Outbox / Inbox / Idempotency Key の 3 点セットは下に敷く。** 例外はほぼない。

避けるべきアンチパターンも併記しておく。

- **「とりあえず Saga」**: 単一 DB で済む処理に Saga を被せると、整合性は弱く、複雑さだけが残る。
- **Outbox なしの publish-after-commit**: 「DB に COMMIT してから publish」は、その間のクラッシュでイベントが消える。確率は低いが、エンタープライズの規模なら年に数回は起きる。
- **マイクロサービス間 2PC**: コーディネータ SPOF、prepare 中のロック保持、サービスの独立デプロイの阻害。ほぼ常に Saga + Outbox の組み合わせが優る。
- **Event Sourcing を「流行っているから」で採る**: 監査要件と時系列要件が両方ないなら、コストに見合わない。

## 最小実装サンプル — Outbox in Python + PostgreSQL

横串の中でいちばん効くのが Transactional Outbox なので、最小実装を載せる。

![Outbox パターンのデータフローを示した図。アプリは orders テーブルへの業務更新と outbox テーブルへの INSERT を同一トランザクション内で行い、COMMIT 後にリレーワーカが SELECT FOR UPDATE SKIP LOCKED で未送信行を取得して Message Broker に publish する。コンシューマ側は inbox テーブルの event_id UNIQUE 制約で重複を排除する](/blogs/images/outbox-dataflow.svg)

### スキーマ

```sql
CREATE TABLE orders (
    id           BIGSERIAL PRIMARY KEY,
    user_id      BIGINT NOT NULL,
    total_cents  BIGINT NOT NULL,
    status       TEXT NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE outbox (
    id            BIGSERIAL PRIMARY KEY,
    event_id      UUID NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    aggregate_id  BIGINT NOT NULL,
    event_type    TEXT NOT NULL,
    payload       JSONB NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at  TIMESTAMPTZ
);

CREATE INDEX outbox_unpublished
    ON outbox (created_at)
    WHERE published_at IS NULL;
```

`outbox_unpublished` は部分インデックスで、未送信行だけを対象にする。送信済みの行を含まないので、relay の SELECT は未送信の規模に対してのみスキャンすればよくなる。`event_id` は consumer 側の inbox で重複排除に使う安定した識別子で、リトライで同じ outbox 行が再 publish されても値が変わらないように DB で割り当てる（broker の自動採番に頼らない）。

### アプリ側: 同一トランザクションで書く

`psycopg` 3 系を使う。

```python
import json
from psycopg import Connection

def create_order(conn: Connection, user_id: int, total_cents: int) -> int:
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO orders (user_id, total_cents, status) "
                "VALUES (%s, %s, 'created') RETURNING id",
                (user_id, total_cents),
            )
            order_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO outbox (aggregate_id, event_type, payload) "
                "VALUES (%s, %s, %s::jsonb)",
                (
                    order_id,
                    "OrderCreated",
                    json.dumps({
                        "order_id": order_id,
                        "user_id": user_id,
                        "total_cents": total_cents,
                    }),
                ),
            )
        return order_id
```

ポイントは `with conn.transaction():` で囲っていること。`orders` の INSERT と `outbox` の INSERT は同じトランザクションに入り、片方だけが永続化されることはない。ここまでで「業務更新したのにイベントが行方不明」「イベントを publish したのに業務が走っていない」という 2 つの破綻が構造的に消える。

### リレーワーカ: SKIP LOCKED で並列に publish

`publish` は「`publish(event_id: str, event_type: str, payload: dict, key: str)` を呼ぶと broker に送ってくれる」コールバックを想定する。`event_id` は consumer が重複排除に使う一意 ID で、broker のヘッダ（Kafka なら `headers`、SQS なら `MessageAttributes`）に乗せて配送する。Kafka なら `confluent-kafka` の `Producer.produce`、SQS なら `boto3.client('sqs').send_message` を薄くラップしたものになる。

```python
import time
from typing import Callable
from psycopg import Connection

PublishFn = Callable[[str, str, dict, str], None]

def relay_worker(conn: Connection, publish: PublishFn, batch: int = 100):
    while True:
        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, event_id, aggregate_id, event_type, payload "
                    "FROM outbox "
                    "WHERE published_at IS NULL "
                    "ORDER BY created_at "
                    "FOR UPDATE SKIP LOCKED "
                    "LIMIT %s",
                    (batch,),
                )
                rows = cur.fetchall()

                for row_id, event_id, agg_id, event_type, payload in rows:
                    publish(str(event_id), event_type, payload, key=str(agg_id))
                    cur.execute(
                        "UPDATE outbox SET published_at = now() WHERE id = %s",
                        (row_id,),
                    )

        if not rows:
            time.sleep(0.5)
```

`FOR UPDATE SKIP LOCKED` は PostgreSQL 9.5 以降で使える。同時に複数のリレーワーカが動いても、お互いがロックしている行を**待たずにスキップ**するので、ワーカ台数で水平スケールできる。`event_id` を必ず broker に乗せて配送するのが肝で、これにより consumer 側で同じイベントが何度届いても同一の値で重複排除できる。

### at-least-once と inbox

このリレー実装は構造的に at-least-once になる。`publish` が成功したあと `UPDATE outbox` 前にプロセスが落ちると、次の起動で同じ行をもう一度 publish するからだ。これを exactly-once に近づけようとすると、`publish` 側と DB 側の分散トランザクションが必要になり、結局 2PC の世界に戻る。

実用的な解決は「at-least-once + 受信側の冪等化」、すなわち consumer 側に inbox テーブルを置き、`event_id` の UNIQUE 制約で重複を弾く。

```sql
CREATE TABLE inbox (
    event_id    UUID PRIMARY KEY,
    received_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

consumer は受信メッセージのヘッダから `event_id`（リレーが outbox の同名カラムから乗せた値）を取り出し、`INSERT INTO inbox (event_id) VALUES (%s) ON CONFLICT DO NOTHING RETURNING event_id` を試み、行が返らなければ「処理済み」として無視する。これと業務更新を同一トランザクションに閉じればよい。outbox / inbox の両方が同じ `event_id` を持つことで、リレーの再 publish と broker の重複配送のどちらも同一の値で検出できる。

## 関連するトピックへの分岐

- **分散ロック**: 「同時に 1 つしか走らせたくない処理」は別問題で、トランザクションパターンよりロックの責務。`SELECT FOR UPDATE` でほぼ事足りるが、サービスを跨ぐ排他は別途必要になることがある。Redis ベースの実装は [redis-py の Lock をサブクラス化してフェンシングトークンを実装する](/blogs/posts/2026/03/2026-03-17-redis-fenced-lock-python/) で扱った。
- **そもそも分散しない選択**: 本稿で並べた仕組みの大半は「分けた瞬間に必要になるもの」だ。逆方向の答えは [Modular Monolith に回帰する大手サービス](/blogs/posts/2026/05/2026-05-11-modular-monolith-large-services/) にある。Saga や Outbox を 1 つも書かずに済むなら、それがいちばん安い。
- **Exactly-once は幻想**: 厳密な exactly-once は「ネットワークありの世界では存在しない」が正しい。実装上は「at-least-once 配送 + 受信側冪等化 = 結果として exactly-once 相当」になる。Kafka の "exactly-once semantics" も内部はこの組み合わせで実現されている。

## まとめ

- 分散トランザクションに銀の弾丸はなく、選び方は **業務要件（強整合性 / 補償可能性 / 予約セマンティクス）** で決まる
- 戦略は積層する。典型スタックは「Saga（Orchestration）+ Outbox + Inbox + Idempotency Key」
- 単一 DB で済むなら迷わずローカル ACID。分けたあとで初めて、上の 9 種類が候補に入る
- Event Sourcing と TCC は強力だが導入コストが高い。「流行っているから」「かっこいいから」では選ばない
- 2PC / XA は今でも RDB と XA リソースの間では有効だが、マイクロサービス間で使うのはほぼ常に間違い

## 参考リンク

- [Pattern: Saga — microservices.io](https://microservices.io/patterns/data/saga.html)
- [Pattern: Transactional outbox — microservices.io](https://microservices.io/patterns/data/transactional-outbox.html)
- [Life Beyond Distributed Transactions: An Apostate's Opinion — Pat Helland (2007)](https://www.ics.uci.edu/~cs223/papers/cidr07p15.pdf)
- [Event Sourcing — martinfowler.com](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS — martinfowler.com](https://martinfowler.com/bliki/CQRS.html)
- [PostgreSQL SELECT FOR UPDATE SKIP LOCKED — PostgreSQL documentation](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE)
- [Idempotency keys — Stripe API reference](https://docs.stripe.com/api/idempotent_requests)
- [TCC for Distributed Transactions — Seata documentation](https://seata.apache.org/docs/dev/mode/tcc-mode/)

## 関連 Wiki

このトピックは Wiki に未収録。後続の `/wiki-ingest` 実行で `content/wiki/concepts/distributed-transaction.md`、`saga-pattern.md`、`transactional-outbox.md` 等として取り込む候補。
