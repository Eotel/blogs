---
name: fact-check
description: 既存 blog post に対してファクトチェックを単独実行する。脚注・引用・人名・所属の検証を claim 単位で大量並列化（claim-source-verifier orchestrator + claim-atom-verifier Haiku swarm）
arguments:
  - name: path
    description: "対象ブログ記事のパス（リポジトリルート相対 or 絶対）。例: content/posts/2026/05/2026-05-13-foo.md"
    required: true
  - name: flags
    description: "`--full` で url-liveness / command-syntax / version-date も並列追加"
    required: false
---

既存のブログ記事に対して **公開後の audit** としてファクトチェックを単独実行するスキル。`/blog` の publish フローには既に組み込まれているので、本スキルは **過去記事の見直し** や **手動再検証** が主用途。

> NOTE: `/wiki-ingest` には fact-check 段が無いため、ブログ記事側で本スキルを通したうえで wiki 化する運用がより安全。wiki ページに対する fact-check は `/wiki-fact-audit` または `/wiki-decay refresh` を使う。

## ワークフロー

### 1. 引数の解析

- `path` を絶対パスに正規化する:

  ```bash
  REPO_ROOT="$(git rev-parse --show-toplevel)"
  case "$ARG_PATH" in
    /*) ABS_PATH="$ARG_PATH" ;;
    *)  ABS_PATH="$REPO_ROOT/$ARG_PATH" ;;
  esac
  ```

- **`content/posts/` 配下以外は拒否**（wiki ページは `/wiki-fact-audit` を案内）

### 2. claim-source-verifier (orchestrator) を起動

```
Agent(subagent_type="claim-source-verifier", prompt="記事絶対パス: $ABS_PATH")
```

claim-source-verifier が内部で:

1. 記事から claim を抽出（事実主張 + 言説主張）
2. 各 claim を `claim-atom-verifier` (Haiku) へ並列 fan-out（10〜20 件/メッセージ）
3. 集約 JSON を返却

### 3. `--full` 指定時の追加並列起動

`--full` が指定された場合、claim-source-verifier と同じメッセージ内で以下も並列起動:

```
Agent(subagent_type="url-liveness-checker",    prompt="記事絶対パス: $ABS_PATH")
Agent(subagent_type="command-syntax-verifier", prompt="記事絶対パス: $ABS_PATH")
Agent(subagent_type="version-date-checker",    prompt="記事絶対パス: $ABS_PATH")
```

これで `/blog` の publish フローと同じ 4 観点（脚注/引用/人名/所属 + URL + コマンド + バージョン）が回る。

### 4. 結果の保存と表示

全 agent から返却された JSON をマージし、以下に書き出す:

```
$REPO_ROOT/.claude/temp/fact-check-<slug>.json
```

`<slug>` は記事ファイル名（拡張子なし）から抽出。

ユーザーへは以下のサマリを stdout に表示:

- `verified` / `needs_fix` / `incorrect` / `uncertain` の件数（agent 別）
- `claim-source-verifier` の `by_pattern` 集計（misattribution / citation-mismatch / scare-quote / conflation / over-extension）
- `needs_fix` または `incorrect` がある場合、**冒頭に WARNING を表示** し、line 番号 + claim + 修正案を上位 5 件まで列挙

### 5. 後処理

- ユーザーが「修正する」と応答した場合のみ Edit でファイル修正を行う
- 本スキル自体は **検証のみ**。修正は別フロー（手動 or `/blog` 用の修正フロー）

## 出力例

```
fact-check: content/posts/2026/05/2026-05-13-foo.md

⚠ needs_fix: 3 件 / incorrect: 1 件

[claim-source-verifier]
  verified: 12, needs_fix: 3, incorrect: 1, uncertain: 0
  by_pattern:
    misattribution-author-confusion: 1
    citation-mismatch-empty-footnote: 2
    scare-quote-without-verbatim: 1

[url-liveness-checker]     verified: 8, dead: 0
[command-syntax-verifier]  verified: 5, needs_fix: 0
[version-date-checker]     verified: 4, needs_update: 1

Top issues:
  L42 [misattribution]   "Fowler は X と書いている" → byline 確認: 著者は Clare Sudbery
                          suggestion: 帰属を Sudbery に修正
  L78 [citation-mismatch] "[^duffield] によると Beck は..." → Duffield 記事内に Beck への言及なし
                          suggestion: 引用元を差し替えるか脚注を削除

詳細: .claude/temp/fact-check-foo.json
```

## モデル選択

- 親セッション: Sonnet 4.6 推奨（claim 集約と diff 提案で読解負荷あり）
- claim-source-verifier (orchestrator): 親セッション継承（通常 Sonnet）
- claim-atom-verifier (worker): Haiku 4.5 固定（大量並列化でコスト最適）

## 関連

- `/blog` — publish 前の publish フローに既に組み込み済み（変更不要）
- `/wiki-fact-audit` — wiki ページの batch audit
- `/wiki-decay refresh` — wiki ページの単発 refresh
- `.claude/agents/claim-source-verifier.md` — orchestrator 仕様
- `.claude/agents/claim-atom-verifier.md` — Haiku worker 仕様
