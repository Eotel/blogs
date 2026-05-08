---
name: wiki-query
description: 既存 Wiki と posts に質問を投げて、引用付きで回答する
arguments:
  - name: question
    description: "質問文（自然言語）"
    required: true
  - name: save
    description: "回答を content/wiki/qa/<slug>.md に保存する場合 true"
    required: false
---

`content/wiki/{concepts,tools,guides}` と `content/posts/` を knowledge base として、自然言語の質問に対して **引用付きで** 回答する skill。

karpathy の LLM Wiki パターンの第 3 操作 (Query) に対応する。執筆前の調査と、過去メモの再活用を兼ねる。

## いつ使うか

- 「これって過去に書いた？」を確認したい（重複防止）
- 既存 Wiki に書いた概念を素早く引きたい
- ある概念について自分の過去ノートからまとめたい
- `/blog` を書く前の予習（手順 5.5 の Wiki-as-input を独立に走らせる感覚）

`/wiki-ingest` (出力)、`/wiki-lint` (健全性) と並ぶ第 3 軸。

## 手順

### 1. プロジェクトルートを取得

ハードコードしないこと。

```bash
PROJECT_DIR=$(git rev-parse --show-toplevel)
```

### 2. 質問からキーワードを抽出（2〜5 個）

質問文を分解し、検索に効くキーワードを 2〜5 個程度抽出する。例:

| 質問 | 抽出キーワード |
|---|---|
| 「RAG とプロンプトインジェクションの関係は？」 | `RAG`, `プロンプトインジェクション`, `prompt injection` |
| 「Anolisa は何のツール？」 | `Anolisa`, `anolisa` |
| 「Hugo + GitHub Pages のセットアップ」 | `Hugo`, `GitHub Pages`, `セットアップ` |

英語・日本語の表記揺れも候補に含める。

### 3. Wiki と posts を grep

```bash
# Wiki セクション別に grep（順序重要: concepts/tools/guides の順で見る）
grep -rli "<keyword>" "$PROJECT_DIR/content/wiki/concepts" 2>/dev/null
grep -rli "<keyword>" "$PROJECT_DIR/content/wiki/tools" 2>/dev/null
grep -rli "<keyword>" "$PROJECT_DIR/content/wiki/guides" 2>/dev/null

# Wiki に直接ヒットしなかった場合のみ posts/ も検索
grep -rli "<keyword>" "$PROJECT_DIR/content/posts" 2>/dev/null
```

ヒット件数が多い場合は **直近 1 年（`content/posts/$(date +%Y)`、前年）に絞る**。

### 4. ヒット上位 N ページを Read

優先順位:

1. Wiki ページ（`concepts/` > `tools/` > `guides/` の順）
2. posts（最新の 3〜5 件のみ）

合計 **5〜10 ページ程度** を Read で読み込む。冗長になるので全件は読まない。

### 5. 回答を生成

以下の Markdown フォーマットで回答する。**出典がない主張は書かない**（ハルシネーション防止）。

```markdown
## 回答

{2〜10 段落程度の本文。引用元の Wiki / posts から得られた情報を統合して回答する}

## 参照

### Wiki
- [<タイトル>](/blogs/wiki/concepts/<slug>/) — {1 行要約: 該当箇所がどう関係するか}
- [<タイトル>](/blogs/wiki/tools/<slug>/) — {1 行要約}

### Posts
- [<タイトル>](/blogs/posts/YYYY/MM/<slug>/) ({YYYY-MM-DD}) — {1 行要約}

## 既知の限界

{以下のいずれか該当する場合のみ書く}
- Wiki にこのトピックの記事はない
- 関連 posts は見つかったが Wiki ページにまだ蒸留されていない（`/wiki-ingest` 候補）
- 直近 N ヶ月以降の情報のみで、それより古い情報は確認していない
```

### 6. 出典が見つからない場合

「Wiki / posts に該当する情報はありません」と明示し、外部調査が必要な旨を返す。**外部 URL を一次情報にして勝手に答えない**（このスキルは knowledge base への問い合わせに専念する）。

```markdown
## 回答

このリポジトリの Wiki / posts には該当する情報はありません。

`/blog "<topic>"` または `/gist-writer "<topic>"` で新規調査・執筆するのが適切です。
外部の最新情報が必要な場合は WebSearch / aegis_fetch を直接使ってください。
```

### 7. （任意）Q&A を Wiki に保存

`save: true` が指定された、もしくはユーザーが明示的に依頼した場合:

1. 保存先: `content/wiki/qa/<slug>.md`
   - `<slug>` は質問から生成（英数字とハイフン、小文字、長すぎる場合は短縮）
2. フロントマターは Wiki ページの標準形式に揃える:
   ```yaml
   ---
   title: "<質問の要約>"
   description: "<1 行の答え>"
   date: YYYY-MM-DD
   lastmod: YYYY-MM-DD
   aliases: []
   related_posts:
     - "/posts/YYYY/MM/<slug>/"
   tags: ["qa", "<topic-tag>"]
   ---
   ```
3. 本文は手順 5 で生成した回答をそのまま入れる
4. `hugo --gc` でビルド確認

> v1 は「保存可能」だけ用意。実際に `qa/` カテゴリを使うかはユーザー判断。デフォルトは保存しない。

## ガイドライン

- **回答は日本語**で記述する
- **出典のない主張は書かない**。Wiki / posts から得た事実だけで構成する
- **回答は具体的に**: 単に「Wiki にあります」ではなく要約を含める
- **既存の用語・表記を尊重**: Wiki ページで使われている術語に合わせる（`/gist-writer` / `/blog` の Wiki-as-input と同じ思想）
- **回答の長さ**: 質問のスコープに応じて 5〜30 行程度。冗長にしない
- 内部リンクは絶対パス `/blogs/wiki/...`, `/blogs/posts/YYYY/MM/<slug>/` を使う

## 例

### 例 1: 既存 Wiki にヒット

入力:
```
/wiki-query "MCP って何？"
```

挙動:
1. キーワード抽出: `MCP`, `Model Context Protocol`
2. grep で `content/wiki/concepts/mcp.md` がヒット
3. Read して本文を要約
4. 回答に `/blogs/wiki/concepts/mcp/` への参照を含める

### 例 2: posts のみヒット（Wiki 未蒸留）

入力:
```
/wiki-query "claude code の hooks の使い分け"
```

挙動:
1. Wiki に該当ページなし
2. posts を grep して 3〜5 件ヒット
3. 回答に「Wiki ページはまだないが posts にあり」と明記
4. 「既知の限界」セクションで `/wiki-ingest` 候補として案内

### 例 3: 該当なし

入力:
```
/wiki-query "MetaQuest3 のレビュー"
```

挙動:
- Wiki / posts のいずれにもヒットしない
- 「リポジトリ内に該当情報なし」と明示
- `/blog` / `/gist-writer` の利用、または外部調査を案内

## 関連

- `/wiki-ingest <記事パス | カテゴリ | all>` — 記事から Wiki ページを生成・更新する逆操作（出力側）
- `/wiki-lint` — Wiki の健全性チェック（孤立ページ、欠落リンク、古い記述）
- `/blog`, `/gist-writer` — Wiki を input に積みつつ新規記事を起こす
