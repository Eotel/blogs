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
2. 以下の 2 カテゴリの主張を行番号付きで列挙:
   - **事実主張 (factual claim)**: ツール存在 / 公式帰属 / 機能仕様 / 開発元・組織の所属
   - **言説主張 (discourse claim)**: 著者帰属 / 出典帰属 / 鉤括弧逐語引用 / 章節参照
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
       "attributed_author": "<discourse の場合の帰属対象著者名、無ければ null>",
       "byline_check_required": true
     }
   }
   ```

4. **claim 数の上限**: 30 件を超える場合は影響の大きい上位 30 件に絞る（言説主張 → 事実主張の順に優先）。絞り込み件数を最終サマリに記載

### 3. claim-atom-verifier を並列 fan-out（skill 親セッション）

skill 自身が `Task` ツールで claim-atom-verifier を並列起動する:

```
Task(subagent_type="claim-atom-verifier", prompt="<上記 JSON>")
Task(subagent_type="claim-atom-verifier", prompt="<上記 JSON>")
...
```

- **1 メッセージあたり 10〜20 件並列**（単一メッセージ内に複数の Task 呼び出しを並べる）
- 全 claim が捌けるまで複数メッセージで分割

### 4. `--full` 指定時の追加並列起動

`--full` が指定された場合、Step 3 と同じメッセージ内で以下を追加並列起動:

```
Agent(subagent_type="url-liveness-checker",    prompt="記事絶対パス: $ABS_PATH")
Agent(subagent_type="command-syntax-verifier", prompt="記事絶対パス: $ABS_PATH")
Agent(subagent_type="version-date-checker",    prompt="記事絶対パス: $ABS_PATH")
```

これで `/blog` の publish フローと同じ 4 観点が回る（脚注/引用/人名/所属 = claim swarm + URL + コマンド + バージョン）。

### 5. 集約と保存

skill 親セッションで全 worker / agent の verdict を集約:

- `claim-atom-verifier` の単一 verdict object を `claims[]` 配列に格納
- `summary.verified / needs_fix / incorrect / uncertain` を集計
- `summary.by_pattern` で failure_pattern ごとの件数を集計
- `--full` のときは url-liveness / command-syntax / version-date の verdict も別 key で含める

保存先: `$REPO_ROOT/.claude/temp/fact-check-<slug>.json`

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
