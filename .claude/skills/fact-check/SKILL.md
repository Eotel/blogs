---
name: fact-check
description: 既存 blog post に対してファクトチェックを単独実行する。skill 自身が claim を抽出 → claim-atom-verifier (Haiku) を claim 単位で並列 fan-out する swarm を回す
arguments:
  - name: path
    description: "対象ブログ記事のパス（リポジトリルート相対 or 絶対）。例: content/posts/2026/05/2026-05-13-foo.md"
    required: true
  - name: flags
    description: "`--full` で url-liveness / command-syntax / version-date も並列追加"
    required: false
---

既存のブログ記事に対して **公開後の audit** としてファクトチェックを単独実行するスキル。`/blog` の publish フローには既に `claim-source-verifier` (monolithic) が組み込まれているので、本スキルは **過去記事の見直し** や **手動再検証** で claim 単位の swarm が必要なときに使う。

> **アーキテクチャ要点**: Claude Code の仕様で **subagent は他の subagent を spawn できない**（[公式ドキュメント](https://code.claude.com/docs/en/sub-agents.md)）。そのため claim 単位の fan-out は **skill レベル（親セッション）で行う**。skill 自身が claim を抽出して `Task` で `claim-atom-verifier` を大量並列起動する。

> **subagent context で起動された場合の fail-safe**: 本 skill が subagent context（`Task` の中）から呼ばれた場合、`claim-atom-verifier` 等への dispatch は不可能。その際は dispatch を試みず、以下の確定手順で完了する:
>
> 1. claim 抽出までは完了する
> 2. 組み立てた dispatch_plan を **sidecar ファイル** `$REPO_ROOT/.claude/temp/fact-check-${SLUG}.dispatch.json` に下記スキーマで書き出す（**canonical な `fact-check-${SLUG}.json` は touch しない** — 既存 audit を破壊しないため）:
>
>    ```json
>    {
>      "status": "aborted",
>      "abort_reason": "subagent-context-dispatch-forbidden",
>      "article_path": "<ABS_PATH>",
>      "slug": "<SLUG>",
>      "checked_at": "<YYYYMMDDTHHMMSSZ>",
>      "dispatch_plan": [
>        {
>          "subagent_type": "claim-atom-verifier",
>          "message_index": 1,
>          "payload": { /* §2 input-contract JSON object: article_path, line, claim_type, claim_text, context_excerpt, hints */ }
>        },
>        {
>          "subagent_type": "url-liveness-checker",
>          "message_index": 1,
>          "payload": { "prompt": "記事絶対パス: <ABS_PATH>" }
>        }
>      ],
>      "next_action": "parent session で /fact-check を再実行してください"
>    }
>    ```
>
>    `dispatch_plan` の各要素は **必ず `subagent_type` + `message_index` + `payload`** の 3 フィールドを持つ。`payload` の中身は `subagent_type` ごとに異なる（claim-atom-verifier は input-contract JSON、それ以外は `{prompt: "..."}`）。`message_index` は 1-based で、`--full` の 3 agent は `message_index: 1` 固定。
>
>    既存の `.dispatch.json` がある場合は **上書き OK**（canonical 同様、最新の実行が正）
>
> 3. stdout に「subagent context のため verdict 未取得。dispatch_plan を `.dispatch.json` に保存。parent から再実行してください」を表示
> 4. **黙って simulate verdict を返してはならない**（実際の検証を行わないまま `verified` が記録されると audit 信頼性が崩れるため）。canonical な `fact-check-${SLUG}.json` への書き出しは fail-safe 時には絶対に行わない

## ワークフロー

### 1. 引数の解析

- `path` を絶対パスに正規化:

  ```bash
  REPO_ROOT="$(git rev-parse --show-toplevel)"
  case "$ARG_PATH" in
    /*) ABS_PATH="$ARG_PATH" ;;
    *)  ABS_PATH="$REPO_ROOT/$ARG_PATH" ;;
  esac
  ```

- **`content/posts/` 配下以外は拒否**（wiki ページは `/wiki-fact-audit` を案内）

### 2. 記事を読み込み claim を抽出（skill 親セッションで実行）

skill 自身が以下を実行する:

1. `Read $ABS_PATH` で記事全文を読み込む
2. 以下の 3 カテゴリの主張を行番号付きで列挙（`claim_type` enum と一致）:

   | claim_type | 定義 | 例 (in-scope) | 例 (out-of-scope) |
   |---|---|---|---|
   | `factual` | ツール / 製品 / 組織 / 人物の **存在・帰属・所属・機能仕様**。発話者帰属を伴わない事実 | 「Karpathy は OpenAI 初期メンバー」「Grafana は OSS」「CloudWatch を data source にできる」 | 「X はこう言った」型は → `discourse` |
   | `discourse` | **発話者・出典への帰属を伴う主張**。著者 paraphrase / 章節参照 / 出典帰属 | 「Fowler はこう書いている」「Beck の TDD by Example p.42 によれば」「Duffield 記事で Beck の発言が紹介されている」 | 鉤括弧 + 識別可能な発話者 + 逐語 → `verbatim-quote` |
   | `verbatim-quote` | **鉤括弧「」または `"..."` の逐語引用 + 識別可能な発話者 / 出典あり**。`discourse` の特殊形 | 「Karpathy「12 月からコードを 1 行も書いていない」」 | 強調用途のみの鉤括弧（発話者なし） → `factual` 扱い |

   **factual vs discourse の precedence**:

   - 「**A は B である / B 社の OSS / B プロトコルをサポート**」型 = `factual`（A の identity / affiliation / capability）
   - 「**A はこう述べた / A の本によれば / A の paraphrase**」型 = `discourse`（発話帰属が claim の核）
   - 両方を含む文は atomicity で split し、それぞれを type 付け（precedence を 1 claim 内で適用するのではなく、split で解消）
   - 鉤括弧 + 識別可能な発話者の逐語があるなら `verbatim-quote` を最優先（precedence: `verbatim-quote` > `discourse` > `factual`）
3. 各 claim ごとに以下の JSON 構造を組み立てる:

   ```json
   {
     "article_path": "<ABS_PATH>",
     "line": 42,
     "claim_type": "factual | discourse | verbatim-quote",
     "claim_text": "<記事内の主張の逐語または短い paraphrase>",
     "context_excerpt": "<前後 3〜5 行の本文抜粋>",
     "hints": {
       "expected_source_url": "<該当行付近の URL or 脚注先 URL、無ければ null>",
       "attributed_author": "<帰属対象著者名、無ければ null>",
       "byline_check_required": true
     }
   }
   ```

   **`hints.attributed_author` の埋め方**:

   - `discourse` / `verbatim-quote` で発話者 / 出典が特定できる場合は人名 / 書名 / 媒体名を入れる
   - `factual` でも「Karpathy は OpenAI 初期メンバー」のように **人物の identity 主張** で人名が登場する場合は埋める（worker が byline で人名確認できる）
   - 該当なしは `null`
   - **複数候補がある場合（媒体 + 人名など）**: 検証コストが低い方 = 最終発話者の人名 を採用。媒体名は `expected_source_url` 側で表現する。例: 「Fortune 誌が Karpathy について報じた」→ `attributed_author: "Andrej Karpathy"`, `expected_source_url: "https://fortune.com/.../karpathy..."`
   - **発話者が記事内で曖昧な場合**（"元ツイートの筆者" 等）: `attributed_author: "(unidentified — <記事内表記>)"` の形で記載し、`hints.verification_notes` に identity 解決の必要性を明記。さらに `claim_type` は `verbatim-quote` ではなく **`discourse` に下げる**（識別可能発話者の要件を満たさないため）

   **`hints.byline_check_required` の埋め方（**rule**）**:

   ```
   byline_check_required = (claim_type ∈ {discourse, verbatim-quote})
                          OR (claim_type == "factual" AND attributed_author != null)
   ```

   それ以外（attributed_author が null の factual 等）は `false`。worker は `true` のとき byline / 著者欄を必ず確認する。

4. **claim 数の上限**: 30 件を超える場合は以下の手順で **上位 30 件を keep**（残りは drop、最終サマリに drop 件数を記載）:
   1. 全 discourse / verbatim-quote claim を **先に keep**（誤帰属・脚注空洞は影響大のため）
   2. discourse + verbatim-quote の合計が 30 件を超える場合、その中を以下の **severity sort key で並べてから先頭 30 件**:
      - primary: `attributed_author != null` を先に（発話帰属が明確な方が検証価値が高い）
      - secondary: `expected_source_url != null` を先に（hint があれば worker cost が下がる）
      - tertiary: `line` 昇順（記事内の早い位置を先に）
   3. discourse + verbatim-quote の合計が 30 件未満なら、残り枠を factual claim で line 番号昇順に埋める
   4. drop された claim は JSON に以下を記録（audit trail）:
      - `dropped_claims_count`: int（drop 件数）
      - `dropped_claims_lines`: int[]（drop された claim の line 番号、昇順）

### 3. claim-atom-verifier を並列 fan-out（skill 親セッション）

skill 自身が `Task` ツールで claim-atom-verifier を並列起動する（**注: Claude Code の dispatch ツールは `Task` のみ。`Agent` という別ツールは存在しない**）:

```
Task(subagent_type="claim-atom-verifier", prompt="<上記 JSON>")
Task(subagent_type="claim-atom-verifier", prompt="<上記 JSON>")
...
```

- **1 メッセージあたり 10〜20 件並列**（単一メッセージ内に複数の Task 呼び出しを並べる）
- 全 claim が捌けるまで複数メッセージで分割

### 4. `--full` 指定時の追加並列起動

`--full` が指定された場合、以下を `Task` で追加並列起動（`Agent` というツールは存在しない、すべて `Task`）:

```
Task(subagent_type="url-liveness-checker",    prompt="記事絶対パス: $ABS_PATH")
Task(subagent_type="command-syntax-verifier", prompt="記事絶対パス: $ABS_PATH")
Task(subagent_type="version-date-checker",    prompt="記事絶対パス: $ABS_PATH")
```

**dispatch ルール（claim 数が 20 件超で複数メッセージに分割される場合）**:

- `--full` の 3 agent は **最初のメッセージにのみ 1 度だけ** 同梱する（per-article 検証なので 1 回起動すれば十分）
- 最初のメッセージは `claim-atom-verifier × N` + `--full agent × 3` = N+3 並列。並列上限を超える場合は claim を後続メッセージに回し、3 agent は最初のメッセージ固定

これで `/blog` の publish フローと同じ 4 観点が回る（脚注/引用/人名/所属 = claim swarm + URL + コマンド + バージョン）。

### 4.5. verdict 衝突の解消（merge / 再検証）

集約の前に、worker verdict の整合チェックを行う:

#### (a) 同一事実の verdict が割れたら、より具体的な evidence を優先

| パターン | 採用方針 |
|---|---|
| 片方が公式 URL からの逐語抜粋を evidence に含む | 逐語側を採用 |
| 片方が「該当 URL に記述が見つからなかった」のみで `needs_fix` を返した | **採用しない**。`uncertain` 相当に降格 |
| 両方とも具体的 evidence を持つが結論が逆 | **再検証 worker を 1 件追加起動**して三者多数決 |

#### (b) `needs_fix` の根拠が「fetch 失敗」のみなら降格

以下のパターンに該当する `needs_fix` は **そのまま採用せず `uncertain` に降格**:

- 「期待 URL を fetch できなかった / SPA / ログイン壁」
- 「該当記述が見つからなかった」のみ（**反証となる別の一次情報を提示していない**）
- 動画・SNS・PDF 内のテキストが根拠で、worker がテキスト本文を取得できなかった

降格後、必要なら別の検索ヒント / 一次情報を hint に追加して再検証 Task を起動する。

#### (c) ユーザー / hint 由来の補強情報を必ず反映

orchestrator がユーザーから受け取った追加 URL や別 claim の verified evidence は、再検証時に `hints.additional_sources` / `hints.verification_notes` として渡す。worker は 1 件単位で文脈を持たないので、orchestrator 側で文脈を補う責務がある。

> (本ルールは `/wiki-fact-audit` と共有。`/wiki-fact-audit` 側でルールが更新されたら本 skill 側も同期する。)

### 5. 集約と保存

skill 親セッションで全 worker / agent の verdict を以下の **fixed schema** で集約する:

```json
{
  "article_path": "<ABS_PATH>",
  "slug": "<basename without .md>",
  "checked_at": "20260518T123045Z",
  "claims": [ /* claim-atom-verifier の単一 verdict object 配列 */ ],
  "summary": {
    "verified": 0,
    "needs_fix": 0,
    "incorrect": 0,
    "uncertain": 0,
    "by_pattern": {
      "misattribution-author-confusion": 0,
      "citation-mismatch-empty-footnote": 0,
      "scare-quote-without-verbatim": 0,
      "conceptual-conflation": 0,
      "paraphrase-over-extension": 0
    },
    "claim_type_counts": {
      "factual": 0,
      "discourse": 0,
      "verbatim-quote": 0
    }
  },
  "dropped_claims_count": 0,
  "dropped_claims_lines": [],
  "full_extras": {
    "url-liveness-checker":    { "verified": 0, "dead": 0, "verdicts": [] },
    "command-syntax-verifier": { "verified": 0, "needs_fix": 0, "verdicts": [] },
    "version-date-checker":    { "verified": 0, "needs_update": 0, "verdicts": [] }
  }
}
```

- `full_extras` は `--full` 指定時のみ含める（無指定なら key ごと省略 or `null`）
- `checked_at` は `date -u +%Y%m%dT%H%M%SZ`（ISO 8601 basic UTC）
- claim_type_counts は claim_type ごとの件数

**SLUG の決定（必須順序）**:

1. 記事 frontmatter に `slug:` フィールドがあれば、その値をそのまま使う（典型: `karpathy-llm-wiki`）
2. 無ければ、ファイル名 basename から `.md` を取り除き、**かつ先頭の `YYYY-MM-DD-` 日付プレフィックスも取り除く**（例: `2026-04-05-karpathy-llm-wiki.md` → `karpathy-llm-wiki`）
3. 日付プレフィックスが取り除けない（typo / 古い形式）場合は `.md` だけを取り除いた値を使う

```bash
SLUG="$(slug_from_frontmatter "$ABS_PATH" || basename_without_date "$ABS_PATH")"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$REPO_ROOT/.claude/temp/fact-check-${SLUG}.json"
```

(疑似コード。実装は orchestrator が frontmatter parser を持っていれば slug を、無ければ basename を使う)

**既存ファイルの取り扱い**:

- デフォルトは **上書き**（idempotent。同じ slug は同じパスに常に最新版が乗る）
- audit trail が必要な場合のみ、上書き前に既存ファイルを `fact-check-${SLUG}.prev-${TIMESTAMP}.json` にリネーム退避
- 退避時は JSON 内に `prior_run_archived_to: "<filename>"` を追加

### 6. サマリ出力

ユーザーへ以下を stdout に表示:

- `verified` / `needs_fix` / `incorrect` / `uncertain` の件数
- `by_pattern` 集計（misattribution / citation-mismatch / scare-quote / conflation / over-extension）
- `needs_fix` / `incorrect` がある場合、**冒頭に WARNING** を表示し、line 番号 + claim + 修正案を上位 5 件まで列挙

```
fact-check: content/posts/2026/05/2026-05-13-foo.md

⚠ needs_fix: 3 件 / incorrect: 1 件

[claim swarm]
  verified: 12, needs_fix: 3, incorrect: 1, uncertain: 0
  by_pattern:
    misattribution-author-confusion: 1
    citation-mismatch-empty-footnote: 2
    scare-quote-without-verbatim: 1

[url-liveness-checker]     verified: 8, dead: 0          ← --full のみ
[command-syntax-verifier]  verified: 5, needs_fix: 0     ← --full のみ
[version-date-checker]     verified: 4, needs_update: 1  ← --full のみ

Top issues:
  L42 [misattribution]   "Fowler は X と書いている" → byline 確認: 著者は Clare Sudbery
                          suggestion: 帰属を Sudbery に修正
  L78 [citation-mismatch] "[^duffield] によると Beck は..." → Duffield 記事内に Beck への言及なし
                          suggestion: 引用元を差し替えるか脚注を削除

詳細: .claude/temp/fact-check-foo.json
```

### 7. 後処理

- ユーザーが「修正する」と応答した場合のみ Edit でファイル修正
- 本スキル自体は **検証のみ**。修正は別フロー

## モデル選択

- 親セッション: Sonnet 4.6 推奨（claim 抽出と集約で読解負荷あり）
- claim-atom-verifier (worker): Haiku 4.5 固定（大量並列化でコスト最適）
- `--full` のときの url-liveness / command-syntax / version-date: 各 agent の既定モデル

## なぜ skill レベルで fan-out するのか

Claude Code の subagent は **他の subagent を spawn できない**（無限ネスト防止のため）。
そのため、もし `claim-source-verifier` (subagent) が内部で `Task` を呼び出しても本番では動かない。

このスキルは **skill（親セッション）が orchestrator になる** ことで、subagent ではなく親セッションが Task fan-out を発行する。これは公式仕様で許可されている使い方。

## 関連

- `/blog` — publish 前の publish フローに既に組み込み済み（monolithic claim-source-verifier を呼ぶ、変更不要）
- `/wiki-fact-audit` — wiki ページの batch audit（同じ swarm pattern）
- `/wiki-decay refresh` — wiki ページの単発 refresh（monolithic wiki-fact-checker を呼ぶ）
- `.claude/agents/claim-atom-verifier.md` — Haiku worker 仕様
