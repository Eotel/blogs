---
name: wiki-fact-audit
description: wiki section または個別ページに対して claim 単位の swarm ファクトチェックを実行する。skill 親セッションが claim を抽出し claim-atom-verifier (Haiku) を並列起動する
arguments:
  - name: target
    description: "対象: section 名 (`tools` / `guides` / `concepts`) または `<section>/<slug>` 形式の個別ページ"
    required: true
  - name: flags
    description: "`--since Nd` で lastmod から N 日経過したページのみ（例: `--since 30d`、必ず `d` サフィックス付き） / `--limit N` で先頭 N 件に絞る"
    required: false
---

wiki ナレッジベースに対して **claim 単位のファクトチェック swarm** をまとめて回すスキル。`/wiki-decay refresh` は monolithic な `wiki-fact-checker` を 1 ページずつ呼ぶ。本スキルは **skill 親セッションが orchestrator になり**、ページごとに claim を抽出して `claim-atom-verifier` (Haiku) を並列に Task 起動する。

> **アーキテクチャ要点**: Claude Code の仕様で **subagent は他の subagent を spawn できない**（[公式ドキュメント](https://code.claude.com/docs/en/sub-agents.md)）。そのため claim 単位の fan-out は **skill レベル（親セッション）で行う**。`wiki-fact-checker` (subagent) を介さず、skill 自身が wiki ページを読んで claim を抽出する。

## ワークフロー

### 1. 引数の解析

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
WIKI_ROOT="$REPO_ROOT/content/wiki"
```

`target` を以下のいずれかとして解釈:

- `tools` / `guides` / `concepts` → section 全体（`$WIKI_ROOT/<section>/*.md`）
- `tools/claude-code` → 個別ページ（`$WIKI_ROOT/tools/claude-code.md`）
- それ以外 → エラー

### 2. 対象ページの列挙

```bash
case "$TARGET" in
  */*)  # 個別ページ
    PAGES=("$WIKI_ROOT/$TARGET.md")
    ;;
  *)    # section
    PAGES=("$WIKI_ROOT/$TARGET"/*.md)
    ;;
esac
```

**section 列挙時の skip list（必ず除外）:**

- `_index.md` — Hugo の section landing page。本文ではないので audit 対象外
- `content/wiki/.archive/**` — 退避済みページ
- `*.draft.md` / `draft: true` frontmatter — 公開前 draft

skip list を除外したうえで `--since` / `--limit` を適用する。

**フラグ:**

- `--since Nd`: 各ページの frontmatter `lastmod` を読み、現在日との差が N 日以上のページのみ残す
  - **grammar は厳格に `^[0-9]+d$`**（regex）。`--since 30d` / `--since 90d` のみ受理
  - `--since 30`（単位なし） / `--since 30w`（週） / `--since 30h`（時間） / `--since 30days` はすべて **エラーで終了**（exit 1、メッセージ: `--since must match ^[0-9]+d$`）
  - **reference clock**: `today` は **UTC date-only**（`date -u +%Y-%m-%d`）。`lastmod` も date-only として比較（YAML の `lastmod: 2026-04-06` は `2026-04-06T00:00:00Z` 扱い）
  - `lastmod` が frontmatter に無いページは `--since` 評価から外す（=スキップ扱い、audit しない）
- `--limit N`: filter 後の先頭 N 件に絞る
  - **sort key（必須）**: filter 通過ページを以下で並べてから head N を取る
    1. primary: `lastmod` 昇順（**古いものから先に audit**。decay 観点で重要度が高いため）
    2. secondary（lastmod tie-break）: filename 昇順 (alphabetical)
  - sort 順を固定することで `--limit` の結果が再現可能になる

### 3. 各ページについて claim を抽出 → fan-out（skill 親セッション）

> **オペレーション順序（重要）**: 各ページに対する処理は以下の順番で **厳密に**:
> 1. Read（ページ全文）
> 2. frontmatter parse（title / lastmod / draft 等）
> 3. claim extraction source scope の適用（frontmatter / 内部リンクを除外）
> 4. stub short-circuit 判定（claim_count=0 ならここで page_action 確定、worker dispatch スキップ）
> 5. atomicity による split（1 文 → 最小単位 N claim）
> 6. precedence による claim_type 確定（split 後の各 claim 単位で適用）
> 7. JSON 組み立て + Task dispatch（10〜20 件 / メッセージ）

ページごとに skill 親セッションが以下を実行する:

1. `Read <page absolute path>` でページ全文を読み込む
2. frontmatter から `title` / `lastmod` を取得
3. wiki 向けの claim を行番号付きで列挙する。

   **claim 抽出 source の scope:**

   - **in-scope**: 本文（frontmatter を除いた markdown body）。`##`/`###` 見出し配下の段落・リスト・テーブル・コードブロック内の散文
   - **out-of-scope**: frontmatter (`title` / `description` / `tags` / `aliases` 等の YAML)、`## ソース記事` / `## 関連ページ` 配下の内部リンクリスト、`![alt](path)` の alt テキスト
   - frontmatter の `description` が本文と矛盾する場合のみ、`feature` claim として 1 件起こす（通常は出さない）

   **stub / claim_count=0 ページの short-circuit:**

   本文から抽出できる検証可能な主張が 0 件のページ（典型: `wiki-ingest-backlog-*.md` の自動生成 stub、内部リンクのみのページ）は、その場で以下を確定し **worker dispatch を完全にスキップ** する:

   ```json
   {
     "page_action": "keep",
     "claim_count": 0,
     "reason": "stub-no-claims",
     "claims": [],
     "suggestions": []
   }
   ```

   ここで強引に claim をでっち上げてはならない。worker cost を消費するだけで、audit の信頼性も落ちる。

   **claim_type 一覧（in-scope / out-of-scope 付き）:**

   | claim_type | in-scope の例 | out-of-scope（別 type または skip） |
   |---|---|---|
   | `tool-existence` | **製品の identity / カテゴリ / 帰属の主張**: 「Grafana は X 社の OSS」「Grafana は時系列メトリクス可視化ツール」「公式は ○○ 社」など、ツール / 製品 / 組織が「何者であるか」を述べる | **特定の能力**に踏み込んだ瞬間 → `feature`（例: 「CloudWatch を data source にできる」） |
   | `feature` | **特定の機能・能力**: 「CloudWatch を data source にできる」「PDF にエクスポート可能」「○○ プロトコルをサポート」など | identity / カテゴリのみ (`tool-existence`)、バージョン依存差分 (`version`) |
   | `version` | 「v3.0 で X が追加」「2024-10 リリース」「Node 20 以上が必須」など | 単なる API バージョン参照のみで主張が無いものは claim にしない |
   | `url` | **外部 URL のみ**（`https://grafana.com/...` 等の vendor / spec / repo URL）。Hugo 内部 route (`/blogs/posts/...`)、相対パス、anchor のみのリンクは out-of-scope（=claim にしない、必要なら filesystem で検証） | |
   | `quote` | **鉤括弧「」または `"..."` で囲われた逐語引用 + 識別可能な発話者 / 出典あり**（「Karpathy はこう述べた『...』」など） | 強調用途のみの鉤括弧（発話者なし、emphasis スタイル）→ `feature` 扱い |
   | `metric` | 価格・ベンチマーク値・統計 (「99.9% SLA」「月額 $20」「100ms 以下」) | バージョン番号は → `version` |

   **identity vs feature の判定基準（`tool-existence` vs `feature`）**:

   - 「**A は B である**」型（コピュラ）= `tool-existence`（A の category や identity を述べる）
   - 「**A は X を行う / 持つ / サポートする**」型 = `feature`（A の具体的能力を述べる）
   - 1 文に両方が同居する場合は atomicity split で別 claim に分けたうえで、それぞれを type 付けする（precedence を 1 atom 内で適用するのではなく、split で解消）

   **claim atomicity ルール（1 claim = 1 type）:**

   1 文に複数の主張が同居する場合、**最小の検証単位ごとに別 claim に分割する**。例:

   > 「Grafana は時系列メトリクスの可視化とダッシュボード作成の標準ツール。CloudWatch・Prometheus・Graphite に対応。」(line 14)

   これは以下 3 claim に分割する:

   - line 14, `tool-existence`: 「Grafana という時系列メトリクス可視化ツールが存在する」
   - line 14, `feature`: 「Grafana がダッシュボード作成機能を備える」
   - line 14, `feature`: 「Grafana が CloudWatch / Prometheus / Graphite を data source としてサポート」

   1 claim に複数 type が当てはまる場合の **precedence**: `quote` > `version` > `metric` > `feature` > `tool-existence` > `url`（より具体的 / 検証コストが高い方を優先）。precedence は atomicity split で type が決まらない場合の **tie-breaker** として使う。通常は split で各 atom が 1 type に確定する。

   **multi-subject shared-predicate（複数主体が同じ述語を共有する場合）**:

   例: 「Claude Code、Cursor はローカルの `.env` から平文で API キーを読み込む」

   この種の文は **1 つの multi-subject `feature` claim にまとめる**（per-vendor に split しない）。理由:

   - 述語（`.env` 読み込み挙動）が同一なので、検証コストの大半は共通
   - vendor 数だけ Task を起動するのは worker cost の無駄
   - hint URL は **multi-vendor 用ルール 3** に従い、最も検証コストが低い vendor 1 件分を `expected_source_url` に入れる。worker が残りを WebSearch で補う

   ただし、述語が vendor ごとに微妙に異なる（A は read-only, B は read-write 等）場合は split する。

4. 各 claim ごとに JSON を組み立て `Task` で `claim-atom-verifier` を起動:

   ```json
   {
     "article_path": "<page abs path>",
     "line": 42,
     "claim_type": "tool-existence | feature | version | url | quote | metric",
     "claim_text": "<wiki ページ内の主張>",
     "context_excerpt": "<前後 3〜5 行>",
     "hints": {
       "expected_source_url": "<本文または周辺に URL があればそれを、無ければ orchestrator が推測した vendor 公式 URL、それも無ければ null>",
       "expected_source_url_inferred": false,
       "attributed_author": null,
       "byline_check_required": false
     }
   }
   ```

   **hints.expected_source_url の埋め方:**

   1. 本文 / 周辺 5 行に URL があれば、それをそのままコピー（`expected_source_url_inferred: false`）
   2. 無い場合、orchestrator が **vendor 公式 URL を推測して埋めてよい**。**ただし `expected_source_url_inferred: true` を必ず付ける**。worker はこの flag を見て「ヒントに依存しすぎず WebSearch も併用する」判断ができる
      - **inference depth（重要）**: claim atom ごとに **deepest plausible vendor doc URL** を入れる。例:
        - データソースに関する atom → `https://grafana.com/docs/grafana/latest/datasources/` のように claim 内容に対応する深いドキュメント URL
        - 製品存在 (`tool-existence`) の atom → vendor root (`https://grafana.com/`) でよい
        - 推測の根拠が薄い場合は深掘りせず root に留める（誤誘導を避けるため）
   3. 1 claim が複数 vendor を跨ぐ場合（例: Claude Code + Cursor が両方 `.env` を読む）は、**最も検証コストが低い 1 つ**を `expected_source_url` に入れ、残りは worker が WebSearch で補う前提とする（複数 URL を 1 hint に詰め込まない）
   4. 推測できる手がかりも無い場合のみ `null`（worker が完全に独力で探す）

   `attributed_author` / `byline_check_required` は claim_type が `quote` または「○○ は」「○○ 氏が」のような帰属つき claim の場合のみ埋める。それ以外は `null` / `false`。

5. **1 メッセージあたり 10〜20 件並列**で Task 起動
6. **claim 数の上限**: 1 ページあたり 20 件を超える場合は影響の大きい上位 20 件に絞る
7. **page 並列度**: 同一メッセージ内では同一ページの claim を優先（複数ページの claim を 1 メッセージに混ぜない方が aggregation しやすい）

### 3.5. verdict 衝突の解消（merge / 再検証）

worker からの verdict が揃ったら、**page_action を判定する前に** 以下の整合チェックを行う:

#### (a) 同一事実の verdict が割れたら、より具体的な evidence を優先

同じ事実を扱う複数 claim で verdict が割れる場合:

| パターン | 採用方針 |
|---|---|
| 片方が公式 URL からの逐語抜粋を evidence に含む | 逐語側を採用 |
| 片方が「該当 URL に記述が見つからなかった」のみで `needs_fix` を返した | **採用しない**。`uncertain` 相当に降格 |
| 両方とも具体的 evidence を持つが結論が逆 | **再検証 worker を 1 件追加起動** して三者多数決 |

例（今回の future-undokai 監査の実例）: claim 17 が ACC 協力体制を「スポーツタイムマシン未確認」で `needs_fix`、claim 18 が同じ公式 URL を読んで「明示記載あり」で `verified`。後者の evidence が逐語を含むので **claim 17 の verdict を撤回し `verified` に統合** する。

#### (b) `needs_fix` の根拠が「fetch 失敗」のみなら降格

worker の evidence を読み、以下のパターンに該当する `needs_fix` は **そのまま採用せず `uncertain` に降格** する:

- 「期待 URL を fetch できなかった / SPA / ログイン壁」
- 「該当記述が見つからなかった」のみ（**反証となる別の一次情報を提示していない**）
- 動画・SNS・PDF 内のテキストが根拠で、worker がテキスト本文を取得できなかった

降格後、必要なら **別の検索ヒント / 一次情報** を hint に追加して再検証 Task を起動する。

#### (c) ユーザー / hint 由来の補強情報を必ず反映

orchestrator がユーザーから受け取った追加 URL や、別 claim の verified evidence は、再検証時に必ず `hints.additional_sources` / `hints.verification_notes` として渡す。worker は 1 件単位で文脈を持たないので、orchestrator 側で文脈を補う責務がある。

### 4. ページごとの page_action 判定

skill 親セッションが各ページの worker verdict を集約し、wiki 向けの page_action を決定:

| 集計結果 | page_action |
|---|---|
| 全 claim が `verified` または無視できる `uncertain` | `keep` — lastmod だけ bump で OK |
| 1 つ以上の `needs_fix` がある | `update` — diff 提案を suggestions[] に追加 |
| `incorrect` または `needs_fix` が過半数 | `rewrite` — section 単位の rewrite が必要 |
| 主題自体が陳腐化 | `archive` — `content/wiki/.archive/` への退避を提案 |

worker の `needs_fix` は wiki 向けでは `needs_update` 相当として扱う。

### 5. 全ページの集約

各ページの結果は **単一の per-page schema** に統一する。stub short-circuit / 通常 audit / verdict 衝突解消後の最終形、すべて以下の形:

```json
{
  "page": "content/wiki/tools/foo.md",
  "page_action": "keep | update | rewrite | archive",
  "claim_count": 12,
  "needs_update_count": 1,
  "incorrect_count": 0,
  "summary": "1 行サマリ。stub の場合は 'no substantive claims (stub)'",
  "reason": null
}
```

- `reason` は `page_action` の根拠を簡潔に書く（stub の場合 `"stub-no-claims"`、それ以外は通常 `null`）
- stub short-circuit ページは `claim_count: 0, needs_update_count: 0, incorrect_count: 0, page_action: "keep", reason: "stub-no-claims"`
- 通常 audit ページは `reason: null` で構わない

aggregation JSON は以下:

```json
{
  "audit_target": "tools",
  "checked_at": "20260518T123045Z",
  "pages": [
    { /* per-page schema, 上記と同じ */ }
  ],
  "totals": {
    "keep": 0,
    "update": 0,
    "rewrite": 0,
    "archive": 0
  }
}
```

**timestamp format 固定（path も JSON 内も同じ profile）**:

```bash
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$REPO_ROOT/.claude/temp/wiki-fact-audit-${TIMESTAMP}.json"
```

- format は **ISO 8601 basic, UTC = `YYYYMMDDTHHMMSSZ`** に統一
- `checked_at` (JSON 内) と filename の `<timestamp>` は **同じ文字列**（同一の `$(date -u +%Y%m%dT%H%M%SZ)` 実行結果を再利用）
- `20260518-123045`（local + ハイフン区切り） / `2026-05-18T12:34:56Z`（ISO 8601 extended）等の別 profile は使わない（再現性 / ソート可能性 / file-system safety のため）

### 6. サマリ出力

stdout に以下を表示:

- 1 行目: `wiki-fact-audit: target=<target> (page=<N>)`（flags があれば `--since=...` `--limit=...` も）
- `page_action` 別の件数（`keep` / `update` / `rewrite` / `archive`）
- 状況に応じて 3 つの template から選ぶ

**Template 出力ルール:**

- `update + rewrite + archive >= 1` → **flagged template**（warning ブロック + refresh 案内）
- 全件 `keep` かつ section / multi-page audit → **clean template**（warning 省略）
- 全件 `keep` かつ単一ページ audit → **single-page template**（warning 省略、件数行も省略可）

#### Template 1: flagged (1 件以上修正が必要)

```
wiki-fact-audit: target=tools (page=12)

keep:    8
update:  3
rewrite: 1
archive: 0

⚠ 修正が必要:
  tools/claude-code.md      [update]    needs_update=2, incorrect=0
  tools/codex-cli.md        [update]    needs_update=1, incorrect=1
  tools/legacy-foo.md       [rewrite]   needs_update=3, incorrect=2

詳細: .claude/temp/wiki-fact-audit-20260518T123045Z.json

修正対応: /wiki-decay refresh tools/claude-code を実行して個別に対応してください
```

#### Template 2: clean (section / multi-page だが全件 keep)

```
wiki-fact-audit: target=guides --since=30d --limit=1 (page=1)

keep:    1
update:  0
rewrite: 0
archive: 0

✓ 全ページ verified / 修正対応不要（lastmod bump 推奨）

詳細: .claude/temp/wiki-fact-audit-20260518T123045Z.json
```

#### Template 3: single-page (個別ページ audit で keep)

```
wiki-fact-audit: target=tools/grafana (page=1)

✓ keep — 全 claim verified（claim_count=4）

詳細: .claude/temp/wiki-fact-audit-20260518T123045Z.json
```

これ以外の文言 / 並び順は使わない（template の drift を防ぐため）。

## /wiki-decay との関係

| シナリオ | 推奨 skill |
|---|---|
| 週次の老朽化レポート（cron） | `/wiki-decay`（既存） |
| 1 ページだけ monolithic に refresh したい | `/wiki-decay refresh <section>/<slug>`（既存、`wiki-fact-checker` 呼び出し） |
| section をまとめて claim 単位 swarm で fact-check したい | **`/wiki-fact-audit <section>`**（本 skill） |
| lastmod が古いページだけ batch fact-check したい | **`/wiki-fact-audit <section> --since 90d`**（本 skill） |

## モデル選択

- 親セッション: Sonnet 4.6 推奨（複数ページの claim 抽出と集約で読解負荷あり）
- claim-atom-verifier (worker): Haiku 4.5 固定

`/wiki-decay refresh` (monolithic `wiki-fact-checker` を呼ぶ) は Haiku 完結だが、本 skill は **skill 親セッションが orchestrator になる** ため Sonnet 推奨。Haiku で回したいなら 1 ページずつ `/wiki-decay refresh` を使う。

## なぜ skill レベルで fan-out するのか

Claude Code の subagent は **他の subagent を spawn できない**（無限ネスト防止のため）。
もし `wiki-fact-checker` (subagent) から `claim-atom-verifier` への `Task` を呼んでも本番では動かない。

本 skill は **skill（親セッション）が orchestrator になる** ことで、subagent ではなく親セッションが Task fan-out を発行する。これは公式仕様で許可されている使い方。

## 関連

- `/wiki-decay` / `/wiki-decay refresh` — 老朽化スコアリングと単発 refresh（monolithic `wiki-fact-checker` を呼ぶ）
- `/fact-check` — ブログ記事側の単独 audit（同じ swarm pattern）
- `.claude/agents/claim-atom-verifier.md` — Haiku worker 仕様
