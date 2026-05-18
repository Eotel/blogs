---
name: wiki-fact-audit
description: wiki section または個別ページに対してファクトチェックを batch 実行する。`/wiki-decay refresh` の複数ページ版で、wiki-fact-checker orchestrator が claim-atom-verifier (Haiku) へ fan-out する
arguments:
  - name: target
    description: "対象: section 名 (`tools` / `guides` / `concepts`) または `<section>/<slug>` 形式の個別ページ"
    required: true
  - name: flags
    description: "`--since 30d` で lastmod から N 日経過したページのみ / `--limit N` で先頭 N 件に絞る"
    required: false
---

wiki ナレッジベースに対して **claim 単位のファクトチェック swarm** をまとめて回すスキル。`/wiki-decay refresh` は 1 ページずつだが、本スキルは section 単位/フィルタ単位の batch audit を行う。

> NOTE: 老朽化スコアリング自体は `/wiki-decay` の責務。本スキルは「decay スコアに関係なく fact-check だけ batch で回したい」「特定 section を一気に検証したい」ケース用の独立エントリ。

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

- `--since N` 指定時: 各ページの frontmatter `lastmod` を読み、現在日との差が N 日以上のページのみ残す
- `--limit N` 指定時: 上記フィルタ後の先頭 N 件に絞る

### 3. wiki-fact-checker を順次起動

```
Agent(subagent_type="wiki-fact-checker", prompt="<page1 絶対パス>")
Agent(subagent_type="wiki-fact-checker", prompt="<page2 絶対パス>")
...
```

- **1 メッセージあたり最大 5 件まで並列**（wiki-fact-checker 自身が内部で claim-atom-verifier に fan-out するため、二重並列を抑制）
- 5 件超は次のメッセージで起動

### 4. 結果の集約

各 wiki-fact-checker の JSON 出力 (`page_action`, `claims[]`, `suggestions[]`) を 1 つの集約 JSON に統合:

```json
{
  "audit_target": "tools",
  "checked_at": "ISO8601",
  "pages": [
    {
      "page": "content/wiki/tools/foo.md",
      "page_action": "keep | update | rewrite | archive",
      "claim_count": 12,
      "needs_update_count": 1,
      "incorrect_count": 0,
      "summary": "..."
    }
  ],
  "totals": {
    "keep": 0,
    "update": 0,
    "rewrite": 0,
    "archive": 0
  }
}
```

保存先: `$REPO_ROOT/.claude/temp/wiki-fact-audit-<timestamp>.json`

### 5. サマリ出力

stdout に以下を表示:

- `page_action` 別の件数（`keep` / `update` / `rewrite` / `archive`）
- `update` 以上の page 一覧（重要度順）
- 修正対応が必要な page については `/wiki-decay refresh <section>/<slug>` を実行するよう案内

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

詳細: .claude/temp/wiki-fact-audit-20260518-123045.json

修正対応: /wiki-decay refresh tools/claude-code を実行して個別に対応してください
```

## /wiki-decay との関係

| シナリオ | 推奨 skill |
|---|---|
| 週次の老朽化レポート（cron） | `/wiki-decay`（既存） |
| 1 ページだけ refresh したい | `/wiki-decay refresh <section>/<slug>`（既存） |
| section をまとめて fact-check したい | **`/wiki-fact-audit <section>`**（本 skill） |
| lastmod が古いページだけ batch fact-check したい | **`/wiki-fact-audit <section> --since 90d`**（本 skill） |

## モデル選択

- 親セッション: 何でも良い（集約・サマリ出力のみ）
- wiki-fact-checker (orchestrator): Haiku 4.5 固定
- claim-atom-verifier (worker): Haiku 4.5 固定

セッション全体が Haiku で完結するためコスト効率が良い。

## 関連

- `/wiki-decay` / `/wiki-decay refresh` — 老朽化スコアリングと単発 refresh
- `/fact-check` — ブログ記事側の単独 audit
- `.claude/agents/wiki-fact-checker.md` — orchestrator 仕様
- `.claude/agents/claim-atom-verifier.md` — Haiku worker 仕様
