---
name: gist-writer
description: Hugo ブログ取り込み用の `*.blog.md` Gist を、既存 Wiki をコンテキストにして起こし、`gh gist create` で公開する
arguments:
  - name: topic
    description: "記事のトピック、タイトル、または短いアウトライン"
    required: true
  - name: slug
    description: "ファイル名のスラッグ（英数字とハイフン）。省略時はトピックから自動生成"
    required: false
---

軽量な技術 tip／コードスニペット／短い解説を **Gist 経由でブログに公開**する skill。
既存 `content/wiki/` を**入力コンテキスト**として読み、重複と用語ブレを抑える（karpathy LLM Wiki パターンの "Wiki as input" を実現）。

## いつ `/gist-writer` を使うか

| 状況 | 使うべき skill |
|---|---|
| 短い tip／単発コード／日々の発見 | **`/gist-writer`**（このスキル） |
| GitHub Issue 由来・long-form・図解入りの正式記事 | `/blog` |

`/gist-writer` は publish 時点では **gist** に書き込み、後段は `scripts/import-gists.sh eotel` の次回実行でリポジトリへ取り込まれる。`/blog` のように直接 commit + PR は作らない。

## Gist ファイルのフォーマット

`scripts/import-gists.sh` は `scripts/merge_gist_frontmatter.py` を呼び出して、gist 内のフロントマターと自動生成メタデータを **マージする**。したがって gist ファイルは:

- ファイル名は必ず `<slug>.blog.md`（`.blog.md` サフィックスが publish opt-in マーカー）
- **YAML フロントマターは書いてよい**（任意。書けば執筆時の意図が反映される）
- 本体は H1 タイトル + Markdown 本文

### マージ規則

| キー | 優先順位 | 補足 |
|---|---|---|
| `title` | gist FM > gist description > 先頭 H1 > basename | 書きたい題名を gist FM に置けば確実 |
| `draft` | gist FM > `false` | gist 側で `draft: true` にすると下書き状態で取り込まれる |
| `categories` / `tags` | gist FM > 空配列（後段 `categorize.py` が空なら自動付与） | 自分でタグ確定させたいなら gist FM に書く |
| `aliases` / `source_url` / `description` | gist FM のみ | wiki エイリアスや外部参照をここで持たせる |
| `date` / `lastmod` | gist のタイムスタンプ（auto） | gist FM に書いても無視 |
| `author` / `gist_id` / `gist_url` / `gist_file` | auto | システム情報、上書き不可 |

## 手順

### 1. プロジェクトルートを取得

ハードコードしないこと。

```bash
PROJECT_DIR=$(git rev-parse --show-toplevel)
```

以降のパスは `$PROJECT_DIR` 起点で組み立てる。

### 2. トピック検証とスラッグ決定

- `topic` 引数が GitHub URL の場合、**`https://github.com/Eotel/blogs/` 配下のみ**受け付ける（`/blog` と同じ URL 制限）
  - それ以外の URL は拒否してエラーで中断:
    「エラー: このスキルで受け付ける URL は https://github.com/Eotel/blogs/ 配下のみです。」
- `slug` 引数があればそれを使う。無ければトピックから自動生成（英数字とハイフン、小文字、長すぎる場合は適度に短縮）
- ファイル名は `<slug>.blog.md`

### 3. 既存知識を context に積む（Wiki as input）

karpathy LLM Wiki パターンの最大のギャップ「Wiki が出力にしか使われていない」を埋める段。

1. **Wiki 関連ページの抽出**

   トピックのキーワードを `content/wiki/concepts/`, `content/wiki/tools/`, `content/wiki/guides/` で検索する。

   ```bash
   grep -rli "<keyword>" "$PROJECT_DIR/content/wiki/concepts" "$PROJECT_DIR/content/wiki/tools" "$PROJECT_DIR/content/wiki/guides"
   ```

   ヒットしたページは Read で読み込んで、以下を draft 生成時に活用する:
   - 既存の用語・表記
   - aliases（同義語）
   - 関連リンクの貼り先（記事内に自然に挿入できれば挿入）

2. **最近の posts でタイトル重複チェック**

   ```bash
   ls -t "$PROJECT_DIR/content/posts/$(date +%Y)" 2>/dev/null
   ```

   直近 30 件程度のファイル名と各々の title フロントマターをスキャンして、明らかな重複トピックがあれば user に確認する。

### 3.5. 外部調査（lightweight research）

トピックが外部の概念・ツール・記事に依存する場合、執筆前に **一次情報** を確認する。`/blog` のフルファクトチェック（4 段階）ほど重くなくてよいが、以下のうちトピックに関係するものは押さえる:

| 項目 | 取得方法 |
|---|---|
| 公式ドキュメント・公式記事 | `aegis_fetch` 優先、不可なら `WebFetch`、SPA は `api.fxtwitter.com` 等 |
| GitHub リポジトリの実在 | `gh api /repos/{owner}/{repo} --jq .full_name` |
| 関連 gist や上流のソース | `gh api /gists/{id}` |
| バージョン・最新仕様 | `WebSearch` で公式ドキュメントを参照 |

調査結果は draft 内の引用・参考リンクに反映する。**ハルシネーション防止のため、根拠が取れない主張は書かない**（書きたければ「未確認」と明示する）。

### 3.6. authors.json から author id を解決

```bash
AUTHOR_ID=$(jq -r '.authors[] | select(.gist_import == true) | .id' "$PROJECT_DIR/scripts/authors.json" | head -1)
```

通常 `eotel` が解決される。author は gist FM に書く必要がない（`import-gists.sh` が authors.json で解決する）。表示用にのみ保持。

### 4. Draft 生成

書き込み先: `$PROJECT_DIR/.claude/temp/<slug>.blog.md`

**フォーマット:**

```markdown
---
title: "記事タイトル"
draft: false
categories: ["AI/LLM"]
tags: ["claude", "hooks"]
model: "<model id>"     # 任意。coding agent で執筆した場合に記載
aliases: ["別表記1"]   # 任意。Wiki と用語を揃える時に
source_url: "https://..."  # 任意。外部記事への明示的な参照
---

# 記事タイトル

冒頭 1〜2 段落で「何の話か・誰のためか・何が嬉しいか」を端的に述べる。

## セクション見出し

本文。コード例があればフェンス付きで示す。

## まとめ／参考

- 関連 Wiki: [LLM Wiki パターン](/blogs/wiki/concepts/llm-wiki-pattern/)
- 参考記事: ...
```

ガイドライン:

- **frontmatter は書いてよい**。`import-gists.sh` (経由 `merge_gist_frontmatter.py`) が auto-generated とマージする
- `date` / `lastmod` / `author` / `gist_*` は frontmatter に書かない（書いても無視）
- `categories` は CLAUDE.md のカテゴリ一覧から 1 つだけ。空配列にすると後段 `categorize.py` がキーワードで自動付与
- `tags` は最大 5 つ程度。確信があれば書く、無ければ空配列で `categorize.py` 任せ
- 一行目はフロントマター `---` で開始するか、frontmatter 省略時は `# <タイトル>`（H1）から始める
- 日本語で記述
- drawio 図は使わない（Gist は画像保持に向かない。画像が必要なら `/blog` を選択）
- コードブロックにはシンタックスハイライト指定を付ける
- Wiki ページや既存 post への参照は絶対パス `/blogs/wiki/...` `/blogs/posts/YYYY/MM/<slug>/` で書く
- 200〜600 行程度を目安にする（長文は `/blog` 推奨）

### 5. ローカル検証（自動公開しない）

draft path をユーザーに伝え、**確認を待つ**。

注: gist は frontmatter を持たないため `hugo --gc` での直接ビルド確認はスキップする。
本番フローでは publish 後の `import-gists.sh` 経由で取り込まれた時点で frontmatter が付与され、Hugo ビルドの整合性は GitHub Pages デプロイ workflow で担保される。

### 6. Gist 公開

ユーザー確認後に publish。`gh gist create` のオプション:

- `--public` を必ず付ける（`users/<login>/gists` API は public のみ返すため、これを忘れると `import-gists.sh` から見えない）
- `-d "<タイトル>"` で description を指定する（`import-gists.sh` の title precedence では description が最優先）
- ファイル名は `<slug>.blog.md`

```bash
GIST_URL=$(gh gist create --public -d "<記事タイトル>" "$PROJECT_DIR/.claude/temp/<slug>.blog.md")
echo "$GIST_URL"
```

`gh gist create` は引数のファイル名（basename）をそのまま gist 内のファイル名として使う。`<slug>.blog.md` で渡せば `.blog.md` サフィックスが保持される。

### 7. 後処理とユーザー案内

1. Gist URL をユーザーに伝える
2. 取り込まれるタイミングを明記:

   ```
   Gist 公開済み: <URL>

   次回 ./scripts/import-gists.sh eotel の実行時に
   content/posts/YYYY/MM/<gist_id>.md として取り込まれます。
   取り込み後、scripts/categorize.py がカテゴリ・タグを自動付与します。
   ```

3. user が即取り込みを希望した場合のみ、以下を案内（自動実行はしない、shared state 変更のため）:

   ```bash
   "$PROJECT_DIR/scripts/import-gists.sh" eotel
   python "$PROJECT_DIR/scripts/categorize.py"
   ```

4. **draft の片付け**: publish 成功後、`$PROJECT_DIR/.claude/temp/<slug>.blog.md` は残しておいてよい（`.claude/temp/` は `.gitignore` 済み）。次回同じ slug で skill を呼ぶ際に上書きする

## Bash コマンドの規約（このリポジトリの auto モード対応）

CLAUDE.md の規約をそのまま適用する:

- **`&&` や `|` でコマンドを繋がない** — 各コマンドは個別の Bash 呼び出しで実行する
- **`/tmp` を使わない** — 一時ファイルは `$PROJECT_DIR/.claude/temp/` に置く
- **`gh gist create` で HEREDOC を使わない** — 内容は事前にファイル化して渡す（このスキルでは `.claude/temp/<slug>.blog.md` を渡せばよいので該当しない）
- **変数代入とコマンドを同一行で繋がない**

## エラーハンドリング

| 状況 | 挙動 |
|---|---|
| `gh` 未認証 | `gh auth status` で確認を促し中断 |
| URL が `https://github.com/Eotel/blogs/` 配下でない | エラーメッセージで中断（手順 2 参照） |
| 既に同 slug の `.claude/temp/` ファイルがある | user に上書き確認を求める |
| `gh gist create` 失敗 | エラー出力をそのまま user に提示し、draft は temp に残す |

## 設計メモ — karpathy LLM Wiki との対応

このスキルが埋めるギャップ:

1. **Wiki を入力として執筆に使う**（手順 3）— `content/wiki/` を grep + Read して context 投入。重複トピックの早期検出と用語の整合に効く
2. **外部一次情報の調査をワークフローに組み込む**（手順 3.5）— ハルシネーション防止と再現性のため、書く前に確認する操作を skill レベルで強制

これらにより `/gist-writer` は「興味のある概念を **調査して書く**」用途に対応する。`/blog` の重いファクトチェックは必要に応じて補完。

残るギャップ（このスキル新設のスコープ外）:

- **Query skill** — wiki への質問 → 回答を wiki に書き戻し
- **`/blog` 側への wiki-as-input 逆輸入**

将来これらを足せば、karpathy パターンの 3 操作（Ingest / Query / Lint）がリポジトリ全体で揃う。
