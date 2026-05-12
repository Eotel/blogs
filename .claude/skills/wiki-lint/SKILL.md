---
name: wiki-lint
description: Wiki の健全性チェック（矛盾検出、孤立ページ、欠落リンク、古い記述）
arguments: []
---

Wiki ナレッジベースの健全性をチェックし、問題を報告・修正します。

## 実行方法（推奨: wiki-linter subagent に委託）

このスキルは **`wiki-linter` subagent（Haiku 固定）** に lint 実行を委託する設計。重い LLM 判断は不要で、スクリプト実行 + 結果整形が主な仕事なのでコスト最適化のため subagent 化されている。

```
Agent(subagent_type="wiki-linter", prompt="Wiki の lint を実行してレポートしてください")
```

subagent は内部で `python3 .claude/skills/wiki-lint/scripts/wiki_lint.py` を実行し、結果を **JSON verdict** (`exit_code`, `fatal`, `findings`, `stats`, `raw_report`) として返す。

skill 本体（親セッション）は subagent の verdict を受け取った後:

1. `fatal: true` なら修正フローへ進む（後述「修正の提案」セクション）
2. `findings` の各カテゴリをユーザーに簡潔に提示する
3. ユーザーが修正に同意した場合のみ、親セッション側で `Edit` を適用する

### 直接スクリプトを叩く場合（subagent を介さない）

CI や lefthook、または subagent コストすら避けたい場合は素のスクリプト実行で十分:

```bash
python3 .claude/skills/wiki-lint/scripts/wiki_lint.py
# Codex などの AGENTS.md 系ランタイムから:
python3 .agents/skills/wiki-lint/scripts/wiki_lint.py
```

スクリプトは実行ファイルの親階層を辿って `content/wiki/` を含むリポジトリルートを自動検出する。出力は下記「出力フォーマット」と同じ Markdown を stdout に書き出す。

終了コードは次の通り（lefthook pre-push / CI で利用）:

- **exit 1 (fatal)**: 欠落リンク / `related_posts` 不整合 / フロントマター不備 — 構造的・参照的な不整合
- **exit 0 (advisory のみ)**: 孤立ページ / 古い可能性のあるページ — `/wiki-ingest` 直後の新規ページは一時的に孤立しうるため push を止めない

ロジックを変更したい場合は **必ず `scripts/wiki_lint.py` 側を編集する**（SKILL.md は仕様の説明のみ）。

## チェック項目

### 1. 孤立ページ検出

他のどの Wiki ページからもリンクされていないページを検出する。

- `content/wiki/` 内の全ページを走査
- 各ページの「関連ページ」セクションのリンク先を収集
- どこからもリンクされていないページをリストアップ

### 2. 欠落リンク検出

Wiki ページ内のリンクが存在しないページを指している場合を検出する。

- 各ページの内部リンク（`/blogs/wiki/...`）を抽出
- リンク先のファイルが `content/wiki/` に存在するか確認
- 存在しないリンクをリストアップ

### 3. related_posts の検証

`related_posts` フロントマターで参照しているブログ記事が実在するか確認する。

- 各 Wiki ページの `related_posts` を抽出
- 対応する `content/posts/` のファイルが存在するか確認
- 存在しない参照をリストアップ

### 4. 古い記述の検出

`lastmod` が古い Wiki ページで、ソース記事が更新されている可能性があるものを検出する。

- Wiki ページの `lastmod` と `related_posts` の記事の `lastmod` を比較
- 記事のほうが新しい場合、Wiki ページの更新が必要な可能性をフラグ

### 5. フロントマター整合性

必須フロントマター項目が欠落しているページを検出する。

- 必須: title, description, date, lastmod, related_posts, tags
- 推奨: aliases

## 出力フォーマット

```markdown
## Wiki Lint レポート

### 孤立ページ (X件)
- `concepts/xxx.md` — どこからもリンクされていない

### 欠落リンク (X件)
- `tools/yyy.md` → `/blogs/wiki/concepts/zzz/` — リンク先が存在しない

### related_posts 不整合 (X件)
- `guides/aaa.md` → `/posts/2026/01/bbb/` — 記事が存在しない

### 古い可能性のあるページ (X件)
- `concepts/ccc.md` (lastmod: 2026-01-01) — ソース記事が 2026-03-15 に更新

### フロントマター不備 (X件)
- `tools/ddd.md` — aliases が未設定

### 統計
- 総ページ数: XX
- concepts: XX / tools: XX / guides: XX
```

## 修正の提案

問題が見つかった場合、以下の対応を提案する:

- **孤立ページ**: 関連する Wiki ページに相互リンクを追加
- **欠落リンク**: リンク先ページの作成、またはリンクの削除
- **related_posts 不整合**: 正しいパスに修正、または参照を削除
- **古いページ**: `/wiki-ingest` でソース記事を再読み込みして更新
- **フロントマター不備**: 欠落項目を補完

ユーザーの確認後に修正を実施する。
