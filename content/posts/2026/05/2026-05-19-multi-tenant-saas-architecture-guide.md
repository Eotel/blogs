---
slug: 2026-05-19-multi-tenant-saas-architecture-guide
title: "マルチテナント SaaS アーキテクチャ設計ガイド ── silo / bridge / pool から hybrid 運用まで"
date: 2026-05-19
lastmod: 2026-05-19
draft: false
author: "eotel"
model: "claude-opus-4-7"
description: "マルチテナント SaaS の設計を、silo / bridge / pool（AWS）、instance / database / table / row（Google Cloud Spanner）、Azure の multitenant guidance を横並びで読み比べ、いつどのモデルを選ぶかを判断軸として整理する。データ分離・認証・デプロイ・観測性・コスト配賦・コンプライアンス・DR をカバーし、PostgreSQL RLS と Terraform のスニペット付き。"
categories: ["クラウド/インフラ"]
tags: ["マルチテナント", "SaaS", "PostgreSQL", "RLS", "AWS"]
---

「マルチテナント SaaS」と一口に言っても、その実装は単一の設計判断ではなく、コンピュート・データ・認証・観測性・運用にまたがる **分離度合いのポートフォリオ** だ。AWS は silo / bridge / pool という語彙でこれを説明し、Google Cloud Spanner は instance / database / table / row という階層で語り、Azure は「共有された資源から分離された資源までの連続体」として位置づけている。本稿では、これらのベンダーガイダンスを突き合わせながら、実プロダクトに落とすときに直面する判断軸を整理する。

## 起点となる二項分離 ── control plane と data plane

最も役に立つメンタルモデルは、**コントロールプレーン**（テナントのオンボーディング、配置、プロビジョニング、課金、ポリシー管理）と **データプレーン**（リクエストルーティング、DB アクセス、実行、テレメトリ）を分けて考えることだ。Azure の multitenant 解説では、テナントを「デプロイパイプラインの設定として扱う」あるいは「コントロールプレーンが管理するデータとして扱う」の二つの方向性を明示している。AWS と Google Cloud も、テナント → デプロイ、テナント → データのマッピングを runtime の挙動に流し込むパターンを多数記述している。

クラウド・認証プラットフォームを横断して繰り返し現れるトレードオフは一貫している。

> 強い分離は運用負荷とコストを上げる。深い共有は効率を上げるが、アプリケーション側のロジックとプラットフォームコントロールに責任を移す。

この命題が、後述するすべての判断軸を貫いている。

## モデル分類と意思決定マトリクス

業界で使われる用語のマッピングは次のとおり整理できる。

- **Single-tenant**: 1 テナントに専用アプリスタック・専用 DB・専用デプロイスタンプを割り当てる。AWS の **silo**、Spanner の **instance** に対応する
- **Shared schema**: 全テナントが同じテーブルを共有し、`tenant_id` をパーティショニングとアクセスコントロールのキーにする。AWS の **pool**、Spanner の **row** に対応する
- **Separate schema**: インフラは共有するが、論理的に分離されたスキーマ・テーブル・データベースをインスタンス内で割り当てる。Spanner の **table / database** にほぼ対応する。AWS の **bridge model** は silo と pool を混在させる resource-level の設計概念で、separate schema 戦略と厳密には別レイヤだが、「共有インフラ上に論理境界を引く」という観点で近接する
- **Hybrid**: 異なるテナント・サービス・ティアで同時に異なるモデルを使う。AWS と Google Cloud のいずれも、フリーティアとエンタープライズティアで要件が乖離する場合にこれを推奨している

アカデミアでもこの結論は早期に出ていた。Aulbach らは chunk folding などのスキーママッピング手法をマルチテナント DB 向けに提案し、Bezemer と Zaidman は保守性を維持するために「マルチテナントという関心事をベースコードから分離すべき」と論じた。

### モデル別の比較表

| モデル | 典型的な実装 | 分離 | コスト効率 | スケーラビリティ | 運用複雑度 | コンプライアンス適性 | 適したケース |
|---|---|---:|---:|---:|---:|---:|---|
| Single-tenant | テナントごとに専用アプリスタック・アカウント/プロジェクト/サブスクリプション・DB | 最高 | 最低 | 良好だがインフラ数がテナント数と比例増加 | 最高 | 最強 | 大企業テナント、個別契約、厳しい residency / audit 要件 |
| Separate schema | アプリは共有、DB は単一インスタンスでテナント別スキーマ/テーブル/DB | 中〜高 | 中 | インスタンス・スキーマ上限まで良好、超えれば sharding | 中〜高 | 良好 | 中規模 B2B で moderate な customization が必要 |
| Shared schema | アプリと共有テーブルを `tenant_id` パーティショニングで使う | 制御次第で最低〜中 | 最高 | テナント密度が最高 | インフラは最低、アプリ規律は最高 | 強い制御で補わない限り弱い | 高頻度 SMB、フリーティア、ホモジニアスな workload |
| Hybrid | 大多数を pool / 例外を silo / separate schema へ | 調整可 | 調整可 | 強い | 中〜高 | 専用フットプリントへ移すことで強くできる | 成熟した SaaS ビジネスの大多数 |

この表のレーティングは、AWS の silo/bridge/pool ガイダンス、Spanner の比較表、そして Azure の「分離を二項ではなく連続体として扱う」考え方を統合した分析的なものだ。Spanner のドキュメントは例えば instance/database パターンを分離・規制要件で最高評価、row パターンを agility と密度で最高評価、と明示しており、ティアごとの組み合わせを推奨している。

### 最も安いモデルを選ばない理由

共有インフラを採用したからといって、テナント分離義務が軽くなることはない。AWS は共有モデルを「分離要件を緩める理由として使ってはならない」と明言しているし、Azure も noisy-neighbor 問題やサービスクォータが共有ストレージモデルではアーキテクチャレベルの関心事になることを警告している。

実務的なルール・オブ・サムはこうだ。

- テナントが本質的に似ていて、authorization 設計が成熟しており、per-tenant 復元やコンプライアンス例外がまれな場合に限り **shared schema** をデフォルトにする
- テナント単位のカスタマイズ、部分バックアップ・エクスポート、スキーマバージョン柔軟性が必要だが専用インフラはコスト過多なら **separate schema** を選ぶ
- 商業価値・規制負担・分離リスクが COGS と運用コストを上回るときは **single-tenant** へ
- プロダクトティアや workload や規制要件が divergent になり始めたら **hybrid** へ移行する

## データ分離と認証 (identity)

### tenant_id を主アクセス経路に置く

shared-schema を採用する場合、`tenant_id` は **二次的なメタデータではなく、主アクセス経路** に組み込む必要がある。Google の row パターン解説は tenant ID を primary key の先頭に置くことを推奨し、AWS の pool ガイダンスもパーティショニングキーをテナントデータのスコーピングとアクセス制御の機構として扱う。

### PostgreSQL での Row-Level Security

PostgreSQL バックエンドで shared-schema を運用するなら、**Row-Level Security (RLS)** が組み込みで最も強い偶発漏洩防止になる。RLS が有効化されたテーブルは、ポリシーが存在しなければデフォルトで deny、つまり通常のアクセスはすべてポリシーで明示的に許可されなければならない。ポリシー式は行単位で評価される。テナントスコーピングと相性が良く、`app.tenant_id` のようなセッション変数とペアにすることで効力を発揮する。

```sql
CREATE TABLE invoice (
  tenant_id    uuid NOT NULL,
  invoice_id   uuid NOT NULL,
  amount_cents bigint NOT NULL,
  status       text NOT NULL,
  PRIMARY KEY (tenant_id, invoice_id)
);

ALTER TABLE invoice ENABLE ROW LEVEL SECURITY;

CREATE POLICY invoice_tenant_isolation
ON invoice
USING (tenant_id = current_setting('app.tenant_id')::uuid)
WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
```

### separate-schema の tenant catalog

separate-schema を採用する場合は、**tenant catalog**（テナント ID から配置先へのマッピング）を持つ。Google Cloud の Spanner ガイダンスは「アプリケーションがテナントのデータ管理パターンと配置先を判定し、それに応じて接続する」必要があると明言している。この catalog にはテナントの tier、region、IdP、feature flag、observability ルーティングメタデータも一緒に持たせるのが筋がよい。

### tenant-aware identity

認証は最初のサインインから tenant-aware であるべきだ。AWS は SaaS identity を「ユーザー identity とテナント identity を first-class な構造体として融合させたもの」と説明し、オンボーディング時にカスタムテナントクレームをユーザー属性に挿入することで、ログイン時に返される JWT に既にテナントコンテキストが含まれる設計を推奨している。これにより、リクエストごとに別のテナント解決サービスへ問い合わせるラウンドトリップを省略でき、レイテンシとボトルネックを減らせる。

エンタープライズ SSO の federation は、**OIDC と SAML** が依然として中核選択肢だ。Okta は両方を引き続きサポートしているが、新規 SSO 連携には OIDC を推奨している（OAuth 2.0 を ID トークンで拡張しており、モダンなクラウド・モバイルアプリと相性がよいため）。Auth0 も OIDC と SAML 両対応で、Universal Login を SSO 実装の最も簡便で安全な経路として位置づけている。

identity のトポロジは大別して二系統。

- **共有 identity プレーンの中でテナントを抽象化**: Okta は単一 org 内に group とユーザー抽象でテナントをホスト、Auth0 は B2B organizations 機能でテナント固有の federation とロールを member に提供。安価で運用が単純
- **テナントごとに別 org / organization に分ける**: Okta の hub-and-spoke モデルがこれにあたり、データ residency・ブランディング・パフォーマンス・委任管理の点で分離が強い。代わりにインフラとライフサイクル管理が増える

authorization は **RBAC を起点に、テナントコンテキストとリソース属性が効くところで ABAC へ拡張する** のが綺麗な進化だ。NIST の RBAC モデルは依然として role-based 設計の canonical な基盤で、AWS Verified Permissions は RBAC と ABAC を併用できるので、プロバイダ側のグローバルガードレールとテナント固有のカスタムロールを両立できる。実務では、admin / viewer のような粗い権限を RBAC で、地理・データ分類・プロジェクトオーナーシップ・契約 tier のような文脈判断を ABAC で表現するのが定石になる。

### tenant-aware な認可フロー

実装としては、JWT で tenant claim を運び、API Gateway → Service → Policy Engine → DB のレイヤを通過させる。詳細なステップとキャリアの対応は後述の「[tenant-aware な認可シーケンス](#tenant-aware-な認可シーケンス)」を参照。AWS SaaS identity の JWT-based テナントコンテキスト伝播と、Okta / Auth0 が示すテナント別 federation / role 表現と整合する流れだ。

## ライフサイクル・デリバリ・マイグレーション

### テナントは config か、テナントは data か

テナントライフサイクル自動化の設計は、まず一つの問いから始める。**テナントは「設定」なのか、テナントは「データ」なのか**。Azure は両方のアプローチを認識している。分離度の低い shared 系では、既にデプロイ済みの共有リソースに「テナント設定を追加するだけ」で済むことが多い。分離度が高い stamp や専用 DB では、コントロールプレーンがプログラマブルにインフラをプロビジョニング・設定する必要がある。Azure はテナントごとの手動デプロイ・テスト運用をはっきりとアンチパターンと呼んでいる。

AWS も商業観点から同じことを言っている。オンボーディングは frictionless かつ自動化されているべきで、顧客向け体験が完全セルフサービスでないとしても、運用モデルはテナント増加スパイクに対して運用人員を線形に増やさずに耐えなければならない、と。

ロバストなオンボーディング手順は概ね次のステップを含む。

1. tenant creation
2. placement の決定（リージョン / stamp / shard）
3. identity setup（IdP・SCIM・SSO）
4. secret / key プロビジョニング
5. limits / entitlements の登録
6. テレメトリ・ロギング・課金タグの初期化

Okta の tenant admins、Auth0 organizations、Google Identity Platform の tenants は、いずれも似たライフサイクル境界を提供している。

エンタープライズオンボーディングでは SSO だけでは足りないことが多く、**プロビジョニング**（ユーザー同期）も必要だ。Okta は OIN（Okta Integration Network）経由のアプリ向けに OIDC と SCIM のセットアップを半自動化する機構を提供しており、B2B SaaS オンボーディングのテナント別 toil を減らす方向に寄与する。

### 単一コアプロダクトと controlled variability

shared SaaS のデプロイ戦略は、**コアプロダクトを 1 バージョンに保ち、テナント variability を制御する** ことを前提にすべきだ。AWS SaaS Lens は「テナント固有機能であってもコアプラットフォームへのカスタマイズとして導入する。多くの場合は feature flag を使う。テナント別にコードやバージョンを fork してはならない」と推奨している。これはテナント数が増えてもリリースエンジニアリングを tractable に保つために重要だ。

### zero-downtime delivery の構成要素

アプリケーションのロールアウトの安全な baseline は次の組み合わせ。

- ステートレスサービスへの **rolling deployment**（Kubernetes 標準）。古い pod を健康チェックベースで段階的に新しい pod に置き換え、必要なら自動ロールバック
- AWS DevOps ガイダンスが推奨する **incremental release techniques**（dark launch / canary / two-phase deployment）
- Google Cloud の App Lifecycle Manager などが提供する **tenant-targeted feature flags**（tenant を unit として扱えるので gradual rollout に向く）
- **expand-contract マイグレーション**（additive スキーマ変更を先にデプロイ、コードが新形式に依存した後で破壊的クリーンアップ）

PostgreSQL の logical replication ドキュメントも、replication 中にスキーマ変更を行う場合は subscriber 側に additive 変更を先に適用すべきと明示している。

expand-contract をテナント環境で安全に流す典型的な順序は次のとおり。

| 段階 | 操作 | 役割 |
|---|---|---|
| 1 | Code change | 機能ブランチを完成させる |
| 2 | Build once | 全テナント共通のアーティファクトをビルド |
| 3 | Additive DB migration | subscriber / 新コードが使う列・テーブルを **追加**（既存読み書きは壊さない） |
| 4 | Rolling deploy | アプリを zero-downtime で置き換え |
| 5 | Feature flag off by default | 旧経路で動作確認、flag を OFF のままロールアウト完了 |
| 6 | Internal → canary → gradual rollout | テナントを段階的に新経路へ |
| 7 | Contract migration cleanup | 旧列・旧テーブル・旧フラグを最後に削除 |

### テスト設計は分離モデルを反映する

Azure の multitenant deployment ガイダンスは「すべてのデプロイ後に自動テスト」「テナント分離モデルの明示的テスト」「Chaos Studio による fault injection」を推奨している。実務では少なくとも 4 種類のテストクラスが必要になる。

1. クロステナント漏洩テスト（pool で特に重要）
2. ティア / entitlement テスト
3. マイグレーションリハーサルテスト
4. stamp / shard 単位の failure-domain テスト

このリストはベンダーガイダンスからの統合的推奨であって、標準化された taxonomy ではない点に注意。

### CI/CD トポロジは tenancy モデルに従う

- **shared デプロイメント**: プロダクトコードは共有パイプライン、テナント配置・flag・config 変更はコントロールプレーン workflow にする
- **dedicated / stamped デプロイメント**: アーティファクトパイプラインは共有のまま、stamp / tenant 単位でデプロイをパラメタライズし、契約上の理由がない限り全 stamp が同じビルドを走らせる
- 差分が **挙動**（behavioral）であって **インフラ**（infrastructural）ではない場合は、テナント別ブランチではなく feature flag で表現する

## スケーラビリティ・運用・コスト

### スケール軸はテナント数と per-tenant skew の二つ

Azure の **Deployment Stamps** パターンは、まさに「単一の共有フットプリント内ではテナント数を無限にスケールできない」現実を扱うために存在する。stamp は事前定義された数のテナントをホストし、stamp を追加することで全体をほぼ線形にスケールさせる。プログラマブルにテナントを共有リソースへ配置するときは、リソースキャパシティをモニタリングして上限に近づいたら新インスタンスを追加すべき、とも警告している。

単一の DB やキャッシュドメインが blast radius として受け入れがたくなった時点で、**sharding** が次の手だ。AWS のストレージガイダンスは、シングルインスタンスの上限とリソース contention が二次的 sharding モデルを最終的に強いることを明言しており、テナント → 複数の partition key へのマッピングを担う lookup table を解説している。Azure のコスト配賦ガイダンスはこれを運用面で補強し、リソースタグに shard 識別子を入れ、コストデータを使ってテナントを shard 間で再バランスすることまで提案している。

### DB コネクション管理は隠れたボトルネックの 1 番手

DB-backed SaaS では **コネクション管理** が最初のボトルネックになりやすい。Prisma の現行ドキュメントはこの点を非常に明快に整理している。

- PostgreSQL のコネクション上限はサーバーレス並列下ですぐに到達する
- PgBouncer によりアクティブな backend プロセスを減らす
- **アプリトラフィックは pooled 接続、マイグレーション・スキーマ introspection・管理ツール・長時間ジョブは direct 接続** を使う
- Prisma Client では PgBouncer の transaction mode が前提

### キャッシュもテナント境界に従う

マネージドキャッシュ（ElastiCache Serverless / Memorystore など）は高スループット・低レイテンシを目的に設計されており、プロバイダドキュメントは永続ストアの前段にこれらを置くパターンを明示する。マルチテナント SaaS で重要な含意は、**キャッシュキーと invalidation ルールがストレージや identity と同じテナント境界に従わなければならない** ことだ。共有キャッシュインフラを使うこと自体は問題ではないが、テナントスコーピングを breach してはならない（これはベンダー明文化ではなく、provider isolation ガイダンスからの inference）。

### 観測性は tenant-aware に

AWS SaaS Lens は、ログメッセージとメトリクスにテナントコンテキストを注入する **shared layer / library** を提供することを推奨している。各サービスで手動タグ付けを再実装させないためだ。Azure は Application Insights の tenancy モデル（1 共有 instance / 1 stamp per instance / 1 tenant per instance）を複数提示し、分離 vs 複雑度のトレードオフを示している。Google Cloud は共有 GKE クラスタでのマルチテナントロギングや、共有クラスタプロジェクトから tenant / team プロジェクトへ tenant log をルートする Cloud Logging パターンを記述している。

### コスト配賦は構造から組み立てる

コスト配賦は分析的な後付けではなく、**構造的なタグ付けから始める**。AWS の cost allocation tags、Azure の resource tags と tag inheritance、Google Cloud の labels はいずれも論理オーナーシップを請求データに投影する仕組みだ。Azure の multitenant コストガイダンスは特に実用的で、こう推奨する。

| リソース種別 | 推奨タグ |
|---|---|
| 全リソース | `stamp-id` |
| sharded DB | `shard-id` |
| 専用リソース | `tenant-id` |

**共有リソース全部に「全テナント分」のタグを付けるのは止める** ── これはスケールしない、という警告も忘れずに。

### Billing-grade メータリングは APM データと別物

Application Insights は telemetry sampling を行うため、ダッシュボード用途のメトリクスは sampling 後でも統計的に補正される一方、**請求レベルの精度**（テナント別 chargeback、契約 SLA 計測など）では生イベントの欠落が問題になり得る。Azure の multitenant cost-management ガイダンスは、accurate billing 用途には Event Hubs や Stream Analytics などを使った **専用の telemetry pipeline** を別途用意することを推奨している。SaaS チームが「monitoring データで chargeback を回せる」と過大評価しがちな部分なので、commercial metering は別パイプラインを起こす前提で見積もるべきだ。

### 共有インフラは noisy neighbor を制御できて初めて COGS を下げる

最も重要なコストの洞察は、**共有インフラは、組織が noisy neighbor を抑制し運用を断片化させないでいて初めて COGS を下げる** という点だ。Azure は共有コンポーネントが明示的な allocation ルールを必要とすると述べ、AWS は pool モデルが agility と管理を改善する一方で hybrid / silo は運用複雑度を上げると認めている。Google の Spanner 比較表は包み隠さずこう言う。row は agility とテナント密度で勝ち、instance は分離と規制で勝ち、ビジネス上の解は概ね hybrid tiering になる。

## セキュリティ・コンプライアンス・リカバリ

### 分離は曖昧にできない

マルチテナント SaaS の主要なセキュリティプロパティは **分離** だ。AWS はこれが foundational で optional ではないと明言しており、共有リソースモデルを使うことが分離要件を緩める理由にはならないとも警告している。Google の cluster multitenancy ガイダンス（GKE）も、運用者は互いにテナントを分離し、クラスタリソースを公平に割り当てて 1 テナントが他を damage しないようにする責任を負うと述べている。

### 暗号化は 3 層で計画する

暗号化戦略は **トランスポート**、**保管時 (at rest)**、**鍵管理 (key control)** の 3 層で計画する。AWS は TLS（in transit）と KMS-backed 暗号化（at rest、envelope encryption や multi-Region key を含む）を明確に分けてドキュメント化している。Azure の multitenant Key Vault ガイダンスは「テナントが別 vault や tenant-managed key を要求するか」を主軸にし、リージョナル vault 配置がデータ residency に寄与すると指摘する。Google も Spanner や Cloud SQL での CMEK、リージョン対応の鍵配置、サービスごとの保護を文書化している。

### データ residency は配置とコントロールプレーンの問題

データ residency は DB の設定 1 つで済む話ではなく、**配置とコントロールプレーンの問題** だ。AWS Control Tower は OU レベルで「指定リージョン外でのデータ作成・共有・コピーを抑制する」コントロールをドキュメント化している。Azure は regional vault と region-aware デプロイパターンを推奨し、Spanner は geo-partitioning や per-row placement key で residency 要件と低レイテンシを両立できると説明している。重要なのは、tenant catalog・プロビジョニングロジック・バックアップ/リストア workflow が **同じ residency 境界を尊重しているかどうか** で、ストレージだけ分離してもダメだという点だ。

### コンプライアンス影響はモデルで material に変わる

- **GDPR**: Article 32 は適切な技術的・組織的措置（暗号化や、機密性・整合性・可用性・レジリエンスの確保能力を含む）を要求する。shared tenancy は、これらのコントロールが demonstrably effective かつ auditable な場合に限り GDPR と両立する
- **PCI DSS**: 支払い口座データの保護に関する技術・運用要件のベースラインを定義し、保存口座データの保護、open public networks 上での transmission の暗号化を要求する。**暗号化だけで環境が PCI scope から自動的に外れることはない**。segmentation で scope を縮小できるが、segmentation は real かつ defensible でなければならない
- **SOC 2**: セキュリティ・可用性・処理整合性・機密性・プライバシーに関するコントロールを評価する。マルチテナント SaaS では、テナント分離・論理アクセス・監査ログ・変更管理・バックアップエビデンスのすべてを **共有プラットフォームレベルで説明可能** にする必要がある、というのが実務的な含意

### バックアップ・リストア・DR ── ここで tenancy モデルが non-negotiable になりがち

プラットフォームレベルの recovery と tenant レベルの recovery を、ベンダー資料は明確に区別している。

| モデル | ネイティブバックアップ粒度 | テナント単位リストアの現実性 | DR ポジション |
|---|---|---|---|
| Single-tenant | テナント DB / instance 単位でネイティブ | 最強。リストア = テナントリストア | テナント別に設計・テストしやすい |
| Separate schema | DB 単位でネイティブ、`pg_dump -n` でスキーマレベルエクスポートも可（後述の caveat あり） | 中程度。スキーマを target にできるが依存と非スキーマオブジェクトでクリーンリストアが複雑になる | 良好だが共有 DB なので PITR タイムラインも共有 |
| Shared schema | DB 単位はネイティブ、per-tenant エクスポートは概ねカスタム | 最弱。行単位リストアはアプリレベルの export/import か selective replay tooling | プラットフォーム DR は強いが、テナント固有 recovery は弱い |
| Hybrid | mixed | テナント tier ごとに recovery SLA を合わせる | 高 SLA テナントを専用フットプリントに残しておけば強い |

PostgreSQL は continuous WAL archiving を通じた base backup と PITR をサポートし、`pg_dump -n` で特定スキーマを dump できる。ただし PostgreSQL ドキュメントは **schema-only dump はそれ単体ではクリーンリストアできないことがある**（依存が欠ける可能性）と明示している。Google の Spanner ガイダンスはさらに直截で、individual-tenant backup は instance / database パターンでは素直だが、**table / row パターンではネイティブにはサポートされない** ──「どのデータがどのテナントに属するか DB は知らないので、アプリケーションがバックアップとリストアを実装しなければならない」と言っている。

商業モデルが per-tenant point restore・legal hold・テナント固有バックアップスケジュール・テナント分離された audit エビデンスを約束しているなら、純粋な shared-schema row モデルは substantial なカスタム recovery tooling を作る覚悟がない限り **fit しない**。これは設計判断として直接効いてくるので、契約条件を起点に逆算するのがよい。

## リファレンスアーキテクチャとスニペット

### control plane と data plane の分離

クラウド非依存のリファレンスアーキテクチャは、コントロールプレーンと shared / dedicated データプレーンを明確に分ける。

| レイヤ | 構成要素 | 主な責務 |
|---|---|---|
| Control plane | tenant catalog / provisioning workflow / metering & billing / policy & feature management | テナント配置、課金、ポリシー、機能フラグの真実の源 |
| Edge | DNS / ingress / API gateway | テナント識別、claim 検証、ルーティング |
| Shared stamp | shared app services / shared DB or shard set / shared telemetry | 多数テナントを高密度に収容 |
| Dedicated stamp | dedicated app services / dedicated DB / dedicated telemetry | 大企業・高 SLA・規制テナント向け |

リクエストは Edge から `tenant_id` ベースで shared / dedicated のいずれかへルーティングされる。コントロールプレーンは両方のスタンプにカタログ・ポリシー・フラグを供給し、metering は両側のテレメトリを横断して billing データを生成する。

これは Azure のコントロールプレーンガイダンス、Azure deployment stamps、AWS の hybrid pool-plus-silo デプロイ、Google のテナント配置マッピングパターンを統合した形だ。

### tenant-aware な認可シーケンス

下の表は、リクエストが Edge から DB まで届く間にテナントコンテキストがどう運ばれるかを 1 行ずつ書き出したものだ。

| 順序 | 主体 | 操作 | キャリア |
|---|---|---|---|
| 1 | User → IdP | 認証要求 | パスワード / passkey / federation |
| 2 | IdP → User | JWT 発行 | id, roles, **tenant_id**, attrs |
| 3 | User → Gateway | リクエスト | Authorization: Bearer ... |
| 4 | Gateway → Service | リクエスト転送 | テナント context をヘッダか claim で |
| 5 | Service → Policy Engine | RBAC/ABAC 評価 | 入力に tenant_id, attrs を渡す |
| 6 | Policy → Service | permit/deny + constraints | フィルタやマスキング条件 |
| 7 | Service → DB | tenant-scoped クエリ | RLS / catalog で制約 |
| 8 | DB → Service | rows | RLS で行単位フィルタ済み |
| 9 | Service → User | response | 必要に応じて再マスキング |

この流れは AWS の JWT-based テナントコンテキスト伝播パターン、および Okta / Auth0 のベンダー認証ドキュメントと整合する。

### Terraform で placement と metadata を表現する

Terraform スニペットは **placement と metadata** を表現することに集中する。クラウドごとのリソース構文ではなく、stamp / tenant の区別とタグ付けを明示的に持たせるのがポイントだ。

```hcl
variable "shared_stamps" {
  type = map(object({
    region   = string
    shard_id = string
  }))
}

module "shared_stamp" {
  for_each    = var.shared_stamps
  source      = "./modules/stamp"
  stamp_id    = each.key
  region      = each.value.region
  tenant_mode = "shared_schema"

  tags = {
    stamp_id   = each.key
    shard_id   = each.value.shard_id
    cost_scope = "shared"
  }
}
```

```hcl
variable "dedicated_tenants" {
  type = map(object({
    region = string
  }))
}

module "dedicated_stamp" {
  for_each    = var.dedicated_tenants
  source      = "./modules/stamp"
  stamp_id    = "tenant-${each.key}"
  region      = each.value.region
  tenant_mode = "single_tenant"

  tags = {
    tenant_id  = each.key
    stamp_id   = "tenant-${each.key}"
    cost_scope = "dedicated"
  }
}
```

これは Azure の「stamp / shard / tenant でタグ付けせよ」ガイダンスと、cost allocation 用に infra placement とメタデータを結びつける汎用パターンに沿っている。

### separate-schema パターンの素直な形

```sql
CREATE SCHEMA tenant_acme;

CREATE TABLE tenant_acme.invoice (
  invoice_id   uuid PRIMARY KEY,
  amount_cents bigint NOT NULL,
  status       text NOT NULL
);

-- per-schema エクスポート例
-- pg_dump -n tenant_acme mydb > tenant_acme.sql
```

繰り返しになるが、PostgreSQL は schema-only dump がそれ自体ではクリーンリストアできないことがあると警告している。dump 対象スキーマ外に依存オブジェクトがある場合、リストア前に解決する必要がある。

## まとめ

長文になったので 5 行で要約しておく。

- **分離度はティアと契約から逆算する** ── shared / separate / dedicated を一律で選ばず、テナント segment ごとに business reason を書く
- **共有を選んでも分離義務は減らない** ── pool 化はコストを下げる仕組みであり、コンプライアンス義務を免れる仕組みではない
- **identity を先に tenant-aware にする** ── データパス改修より前に JWT に tenant claim を埋め、catalog を 1 つに集約しておく
- **観測性・コスト・DR は tenancy モデルに従属する** ── 構造的なタグ付け（stamp-id / shard-id / tenant-id）と recovery 定義をモデル別に明文化する
- **expand-contract と feature flag を運用の標準にする** ── テナント単位の段階適用が、shared でも dedicated でも安全な唯一の道

## マイグレーションチェックリスト

shared → separate → dedicated への移行（あるいは逆方向）は、現実には頻発する。最低限のチェックリスト。

- テナント segment ごとの target モデル（shared / separate / dedicated）を定義し、すべての例外には business reason を書く
- tenant catalog を新設または更新し、runtime placement / region / IdP / entitlement tier / shard / telemetry routing をすべて 1 つの source of truth に集約する
- データパスの移行前に **identity を tenant-aware にする**（JWT に明示的な tenant claim を入れる）
- DB 移行では **expand-contract** を採用し、マイグレーションツールは pooled ではなく **direct connection** で接続する
- staging 環境でのリハーサルは「機能的正しさ」だけでなく **テナント segmentation の仮定が崩れていないか** を含めて検証する
- 移行後パスは feature flag で dark-launch し、テナント単位で段階的に有効化する
- ログ・メトリクス・コストメタデータに tenant context を追加 **してから** cutover し、移行前後の挙動を比較できるようにする
- 「テナントリストア」の定義をモデル別に文書化する（dedicated / schema / row-shared でまったく違うものになる）
- 移行に伴う residency / 鍵管理 / audit 含意を、すべてのテナントクラスについて検証する。特に shared ↔ dedicated 間の移動は要注意

## 制限事項と注意点

この記事はクラウド非依存に書いてあるため、サービス固有のクォータ・価格・マネージド DB 機能を網羅していない。具体的な制限、機能の availability、コストモデルは、サービス・リージョン・時期で変動するため、実装前に対象 runtime のドキュメントで再確認すべきだ。本稿の表現がベンダーガイダンスの **要約と推奨の合成** である箇所も多く、引用個所は元ドキュメントへリンクできるよう attribution に留めている。

## 参考文献

主要な一次情報のみ列挙する（本文の「AWS は…」「Azure は…」「Spanner ドキュメントでは…」の引用先）。

- AWS Well-Architected SaaS Lens: [Silo, Pool, and Bridge Models](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/silo-pool-and-bridge-models.html)
- AWS Whitepaper: [SaaS Tenant Isolation Strategies — The Isolation Mindset](https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/the-isolation-mindset.html)
- AWS Prescriptive Guidance: [Multi-tenant access control with RBAC and ABAC (Verified Permissions)](https://docs.aws.amazon.com/prescriptive-guidance/latest/saas-multitenant-api-access-authorization/avp-mt-abac-rbac-examples.html)
- AWS Control Tower: [Data residency controls](https://docs.aws.amazon.com/controltower/latest/controlreference/data-residency-controls.html)
- Azure Architecture Center: [Architect Multitenant Solutions on Azure](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/overview)
- Azure Architecture Center: [Tenancy Models for a Multitenant Solution](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models)
- Azure Architecture Center: [Deployment Stamps pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/deployment-stamp)
- Azure Architecture Center: [Cost Management and Allocation in a Multitenant Solution](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/cost-management-allocation)
- Google Cloud: [Implement multi-tenancy in Spanner](https://cloud.google.com/spanner/docs/implement-multi-tenancy)
- Google Cloud: [GKE — Cluster multi-tenancy best practices](https://cloud.google.com/kubernetes-engine/docs/best-practices/multi-tenancy)
- PostgreSQL: [Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- PostgreSQL: [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
- PostgreSQL: [Logical Replication Restrictions](https://www.postgresql.org/docs/current/logical-replication-restrictions.html)
- Prisma: [Configure Prisma Client with an external connection pooler](https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/databases-connections/pgbouncer)
- NIST: [The NIST Model for Role-Based Access Control](https://www.nist.gov/publications/nist-model-role-based-access-control-towards-unified-standard)
- GDPR Article 32: [Security of processing](https://gdpr-info.eu/art-32-gdpr/)

## 関連 Wiki

- [Modular Monolith（モジュラーモノリス）](/blogs/wiki/concepts/modular-monolith/) — 「システム境界とデプロイ境界を一致させない」発想は、shared schema 内の論理分離にも応用できる
- [Terraform IaC](/blogs/wiki/guides/terraform-iac/) — stamp / shard / tenant の placement と tagging を IaC で表現する実装パターン
- [インシデント対応](/blogs/wiki/guides/incident-response/) — tenancy モデル別の DR 設計と blast radius を運用面から補強
- [AI Agent Secret Management](/blogs/wiki/guides/ai-agent-secret-management/) — テナント固有 secret / 鍵プロビジョニングの設計と直結
- [Framework-defined Infrastructure](/blogs/wiki/concepts/framework-defined-infrastructure/) — コントロールプレーンをフレームワーク側に押し出す発想として参照可能
- [Supabase](/blogs/wiki/tools/supabase/) — PostgreSQL RLS をマルチテナント分離の主機構として採用する BaaS の代表例
