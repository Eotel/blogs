---
name: wiki-ingest
description: ブログ記事を読み込んで Wiki ページを自動生成・更新する
arguments:
  - name: target
    description: "対象の指定。記事パス（content/posts/...）、カテゴリ名、または 'all'（全記事一括）"
    required: true
---

指定されたブログ記事を読み込み、Wiki ページ（コンセプト・ツール・ガイド）を自動生成・更新します。

## Wiki ページの分類基準

### concepts/ — 技術概念・用語

- 技術的な概念、パターン、アーキテクチャの解説
- 例: RAG、プロンプトエンジニアリング、ゼロトラスト、マイクロサービス
- ファイル名: `<concept-slug>.md`

### tools/ — ツール・サービス・ライブラリ

- 具体的なツール、サービス、フレームワーク、ライブラリの情報
- 例: Hugo、Docker、Terraform、PaperMod テーマ
- ファイル名: `<tool-slug>.md`

### guides/ — How-to・手順まとめ

- 複数記事にまたがる実践的な手順や設定のまとめ
- 例: Hugo + GitHub Pages セットアップ、AI コーディングエージェントのカスタマイズ
- ファイル名: `<guide-slug>.md`

## Wiki ページのフロントマター

```yaml
---
title: "ページタイトル"
description: "1行の概要説明"
date: YYYY-MM-DD        # 初回作成日
lastmod: YYYY-MM-DD     # 最終更新日
aliases: ["別名1", "別名2"]  # 検索用の別名（オプション）
related_posts:           # ソースとなったブログ記事
  - "/posts/YYYY/MM/slug/"
tags: ["tag1", "tag2"]   # 関連タグ
---
```

## Ingest 処理の手順

### 1. 対象記事を特定する

- **記事パス指定**: そのファイルを読み込む
- **カテゴリ指定**: `content/posts/` から該当カテゴリの記事を検索
- **`all`**: `content/posts/` の全記事を対象にする（バッチ処理）

### 1.5. 既存 Wiki との重複・統合先を確認する

Wiki ページを作成・更新する前に、必ず専用スクリプトで ingest 計画を出す。これは Karpathy の LLM Wiki パターンに沿って、記事を 1:1 で Wiki 化せず、既存の概念・ツール・ガイドページへ知識を統合するための前段チェック。

```bash
python3 .claude/skills/wiki-ingest/scripts/wiki_ingest_plan.py <target>
```

代表例:

```bash
# 全記事。ただし前回 ingest 日以降だけを対象にする
python3 .claude/skills/wiki-ingest/scripts/wiki_ingest_plan.py all --since-file .claude/wiki-last-ingest.txt

# 単一記事
python3 .claude/skills/wiki-ingest/scripts/wiki_ingest_plan.py content/posts/2026/05/example.md

# カテゴリ
python3 .claude/skills/wiki-ingest/scripts/wiki_ingest_plan.py "AI/LLM"

# 機械処理用
python3 .claude/skills/wiki-ingest/scripts/wiki_ingest_plan.py all --format json
```

スクリプトは `.claude/temp/wiki_ingest_index.sqlite` に SQLite FTS5 trigram のローカル全文検索 index を作り、各記事を次の状態に分類する。

- **covered**: 既存 Wiki の `related_posts` に既に含まれる。原則スキップ。
- **stale_candidate**: `related_posts` には含まれるが、記事の `lastmod` が Wiki より新しい。既存ページを更新候補にする。
- **update_candidate**: 既存 Wiki への統合候補が強い。新規ページを作らず、候補ページを更新する。
- **review_candidate**: 既存 Wiki への統合候補があるが弱い。候補ページを読んで統合か新規か判断する。
- **new_candidate**: 強い候補なし。`concepts/`、`tools/`、`guides/` のいずれかに新規ページを作る。

`new_candidate` であっても、記事の丸コピーや「1 blog = 1 wiki」にはしない。記事から概念・ツール・手順として再利用できる知識だけを抽出し、既存ページと接続する。

計画を機械的に適用する場合は `wiki_ingest_apply.py` を使う。

```bash
# 通常運用: 高信頼の update_candidate だけ既存 Wiki に related_posts / ソース記事を追記
python3 .claude/skills/wiki-ingest/scripts/wiki_ingest_apply.py all --since-file .claude/wiki-last-ingest.txt --policy safe

# 全記事対応: 高信頼候補は既存 Wiki に統合し、低信頼・新規候補は backlog Wiki に集約
python3 .claude/skills/wiki-ingest/scripts/wiki_ingest_apply.py all --policy all
```

`--policy all` は全記事を対象にできるが、低信頼候補を無理に既存ページへ混ぜない。`review_candidate` / `new_candidate` のうち高信頼統合できなかったものは `content/wiki/guides/wiki-ingest-backlog.md` に集約し、後で人間またはエージェントが個別ページへ蒸留する。

### 2. 記事を分析する

各記事について以下を抽出する:

- **キーエンティティ**: 記事で主に扱っている概念、ツール、手順
- **カテゴリとタグ**: フロントマターから取得
- **要約**: 記事の主要な情報を3-5文で要約

### 3. Wiki ページを生成・更新する

抽出したエンティティごとに:

1. **既存ページの確認**: `wiki_ingest_plan.py` の候補を起点に、`content/wiki/` 内に該当ページが既にあるか確認
2. **新規作成**: なければ適切なサブディレクトリにページを作成
3. **更新**: あれば `related_posts` に記事を追加し、内容を補完・更新
4. **相互参照**: 関連する Wiki ページ同士をリンクで繋ぐ

### 4. Wiki ページの内容構成

```markdown
## 概要

{エンティティの簡潔な説明 — 2-3文}

## 詳細

{記事群から抽出した詳細情報}

## 関連ページ

- [関連 Wiki ページ](/blogs/wiki/section/slug/)

## ソース記事

- [記事タイトル](/blogs/posts/YYYY/MM/slug/) — YYYY-MM-DD
```

### 5. インデックスの更新

処理完了後、各セクションの `_index.md` のリンクが最新状態であることを確認する。

## バッチ処理（`all` 指定時）

全記事を一括処理する場合:

1. カテゴリごとにグループ化して処理する
2. 1カテゴリ処理するごとに進捗を報告する
3. 重複するエンティティは統合する
4. 処理完了後に全体の統計を報告する（作成ページ数、更新ページ数）

## 注意事項

- Wiki ページは日本語で記述する
- 記事の内容を丸ごとコピーしない — 要約・統合して知識として再構成する
- 1つの Wiki ページが長くなりすぎないようにする（目安: 200行以内）
- `hugo --gc` でビルドが通ることを確認する
