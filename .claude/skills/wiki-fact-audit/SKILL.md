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

- `--since Nd` 指定時: 各ページの frontmatter `lastmod` を読み、現在日との差が N 日以上のページのみ残す
  - **`Nd` フォーマット必須**: `--since 30d`、`--since 90d` のように **必ず末尾に `d` を付ける**
  - 単純数値（例: `--since 30`）は受け付けない（単位曖昧さ回避のため）
- `--limit N` 指定時: 上記フィルタ後の先頭 N 件に絞る

### 3. 各ページについて claim を抽出 → fan-out（skill 親セッション）

ページごとに skill 親セッションが以下を実行する:

1. `Read <page absolute path>` でページ全文を読み込む
2. frontmatter から `title` / `lastmod` を取得
3. wiki 向けの claim を行番号付きで列挙:
   - **ツール存在 / 公式帰属 / 開発元主張**
   - **機能・仕様の有無**
   - **バージョン番号 / リリース日 / 互換性記述**
   - **URL / リポジトリ参照**
   - **逐語引用 (鉤括弧「」または "...")**
   - **数値 (価格 / ベンチマーク / 統計)**
4. 各 claim ごとに JSON を組み立て `Task` で `claim-atom-verifier` を起動:

   ```json
   {
     "article_path": "<page abs path>",
     "line": 42,
     "claim_type": "tool-existence | feature | version | url | quote | metric",
     "claim_text": "<wiki ページ内の主張>",
     "context_excerpt": "<前後 3〜5 行>",
     "hints": {
       "expected_source_url": "<該当行付近の URL があれば、無ければ null>",
       "attributed_author": null,
       "byline_check_required": false
     }
   }
   ```

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

各ページの JSON 出力 (`page_action`, `claims[]`, `suggestions[]`) を 1 つの集約 JSON に統合:

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

### 6. サマリ出力

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
