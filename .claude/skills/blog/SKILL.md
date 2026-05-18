---
name: blog
description: Hugo ブログ記事を新規作成し、PR を作成する
arguments:
  - name: topic
    description: "記事のトピック、タイトル、または GitHub Issue URL"
    required: true
  - name: date
    description: "記事の日付（YYYY-MM-DD 形式）。省略時は本日"
    required: false
---

指定されたトピックで Hugo ブログ記事を作成し、PR を作成してください。

> 短い tip ・コードスニペット中心の軽量記事で、図解や PR レビューが不要な場合は `/gist-writer` を使う方が早い（gist に書いて `import-gists.sh` で取り込まれるフロー）。GitHub Issue 由来 / long-form / 図解入りはこの `/blog` を使う。

## URL 制限（セキュリティ）

**重要: トピックとして GitHub URL が指定された場合、`https://github.com/Eotel/blogs/` 配下の URL のみ受け付ける。**

- 許可: `https://github.com/Eotel/blogs/issues/...`, `https://github.com/Eotel/blogs/pull/...` など
- 拒否: 上記以外のすべての GitHub URL（他のリポジトリ、他のオーナー）
- 拒否された場合はエラーメッセージを表示して処理を中断する:
  「エラー: このスキルで受け付ける URL は https://github.com/Eotel/blogs/ 配下のみです。」

## 手順

### 1. トピックの種類を判定する

トピック引数が以下のいずれかを判定する:

- **GitHub Issue URL**: `https://github.com/Eotel/blogs/issues/{number}` 形式
- **テキストトピック**: 上記以外のテキスト（URL でないもの）
- **許可されていない URL**: 上記以外の URL → エラーで中断

> 旧 `https://github.com/Eotel/blogs/issues/{number}#issuecomment-{id}` 形式（コメント単位 URL）は **サポート対象外**。1 topic = 1 Issue 運用に統一されている。フォーク元 hdknr の歴史的記事は既に `content/posts/` に取り込み済みで、これ以降コメント URL を入力にすることはない。

### 2. GitHub Issue URL の場合（brief として扱う）

Issue を **記事の brief（依頼書）** として扱う。本文の文字数は問わない（タイトル + URL + 0〜1 行で十分）。

1. URL をパースして `owner`, `repo`, `issue_number` を抽出する
2. Issue の情報を取得する:
   ```bash
   gh api /repos/{owner}/{repo}/issues/{issue_number} --jq '{title, body, created_at, html_url}'
   ```
3. **記事タイトル** は Issue タイトルをそのまま使用する
4. **Issue 本文の URL** は一次情報源として「外部 URL のフェッチ方針」に従って `aegis_fetch` で取得する
5. **Issue 本文の文章** は「興味の方向 / 切り口の指示」として尊重する（記事本文にそのままコピーしない）
6. テキストトピックモードと同じく **WebSearch / `aegis_fetch` で調査して** 執筆する
7. フロントマターに `source_url` として Issue の `html_url` を記録する
8. 後段の手順 7（カテゴリ・タグ自動付与）以降は通常通り

### 3. テキストトピックの場合

- トピックに基づいて、技術ブログ記事としてふさわしい内容を作成する
- ユーザーがトピックのみ指定した場合は、WebSearch / `aegis_fetch` で最新情報を調査して記事を作成する
- ユーザーが内容も指定した場合は、その内容をベースに記事を整形する

### 4. 著者 (author) の決定

すべての記事のフロントマターに `author` フィールドを必ず含めること。値は `scripts/authors.json` の `id` を使用する。

決定ロジック（優先順位順）:

1. **プロンプト本文に author 指定がある場合**: 呼び出し元（自動化スクリプト等）がプロンプトに `author id "<id>"` を明示している場合、その値を使用する
2. **GitHub Issue URL がソースの場合**: Issue 作成者の `github_login` を `scripts/authors.json` で `id` に解決する:
   ```bash
   AUTHOR_ID=$(jq -r --arg l "$LOGIN" '.authors[] | select(.github_login == $l) | .id' scripts/authors.json)
   ```
   解決できない投稿者は allowlist 外なので、エラーで中断する
3. **テキストトピック（手動実行）の場合**: デフォルトの `eotel` を使用する

### 5. 対象日付を決定する

- 引数で日付（YYYY-MM-DD）が指定されている場合はその日付を使用する
- GitHub Issue URL の場合は Issue の `created_at` を使用する
- それ以外の場合は今日の日付を使用する（`date +%Y-%m-%d`）

### 5.5. Wiki を input に積む（Wiki as input）

karpathy LLM Wiki パターンの "Wiki as input" を実現する段。記事執筆前に既存 Wiki を読み込み、用語ブレ・重複・再説明を抑える。**この手順は省略しない。**

1. **Wiki の関連ページを検索**

   トピックのキーワード（2〜5 個）を抽出し、`content/wiki/{concepts,tools,guides}` を grep する:

   ```bash
   PROJECT_DIR=$(git rev-parse --show-toplevel)
   grep -rli "<keyword>" \
     "$PROJECT_DIR/content/wiki/concepts" \
     "$PROJECT_DIR/content/wiki/tools" \
     "$PROJECT_DIR/content/wiki/guides"
   ```

2. **ヒットしたページを Read**

   Wiki ページ本文と frontmatter（特に `aliases`, `related_posts`, `tags`）を読み込み、以下を draft に反映する:

   - **既存の用語・表記** を尊重する（同じ概念に違う名前を当てない）
   - **`aliases`（同義語）** を確認し、検索性を担保した記述にする
   - **既に詳細に書かれている概念は再説明せず**、Wiki ページへ絶対パス `/blogs/wiki/<section>/<slug>/` でリンクして委ねる
   - **記事内の「関連 Wiki」セクション**（記事末尾推奨）にリンクを集約する

3. **重複トピック早期検出**

   Wiki ヒットがなくても、`content/posts/` 直近 1 年で同じトピックが既に書かれていないかを確認する:

   ```bash
   ls -t "$PROJECT_DIR/content/posts/$(date +%Y)" 2>/dev/null
   grep -rli "<keyword>" "$PROJECT_DIR/content/posts/$(date +%Y)" 2>/dev/null
   ```

   明らかな重複があればユーザーに確認する。

4. **Wiki が薄い・無い場合**

   ヒットしなくても作業は止めない。「これは新しい概念で Wiki に未収録」と認識して書く（後で `/wiki-ingest` がこの記事から拾う）。

### 6. モデルIDを取得する

記事が coding agent による自動執筆の場合、使用したモデルIDをフロントマターに記録する。

auto モードの shell ルール（`$()` 置換禁止）に従い、結果は一時ファイル経由で受け渡す:

```bash
mkdir -p "$PROJECT_DIR/.claude/temp"
python3 "$PROJECT_DIR/scripts/get_model.py" > "$PROJECT_DIR/.claude/temp/model_id.txt"
```

書き出した `.claude/temp/model_id.txt` を Read ツールで読み、フロントマターの `model:` に値を入れる。

- ファイル内容が空の場合はフロントマターから `model` を省略してもよい
- 手動執筆の場合も省略可
- 走行中の agent を判別できなかった場合、スクリプトは無関係な設定からの推測を避けて空を返す

### 7. 記事ファイルを作成する

- ファイルパス: `content/posts/YYYY/MM/YYYY-MM-DD-<slug>.md`
- `<slug>` はトピックから生成する（英数字・ハイフンのみ、小文字）
- 同名ファイルが既に存在する場合はサフィックスを追加する（例: `-2`）

### 8. カテゴリとタグを自動付与する

- `scripts/categorize.py` のルールに基づいて、記事の内容からカテゴリとタグを判定する
- カテゴリは以下から最適なものを1つ選択する:
  - AI/LLM, セキュリティ, クラウド/インフラ, Web開発, プログラミング言語,
    モバイル, データベース, ツール/開発環境, ビジネス/キャリア, 地域/グルメ, その他
- タグは内容に関連するものを最大5つ選択する

## フロントマターのテンプレート

> **重要: `slug:` フィールドは必須**。`.claude/skills/wiki-lint/scripts/wiki_lint.py` の `posts_missing_slug` チェックで fatal 扱いされており、未定義のままだと CI で lint が落ちる。Hugo は title 由来 slug にフォールバックし URL が不安定になるため、`slug:` をファイル名と一致させて明示する（`scripts/check_frontmatter.py` の `POST_REQUIRED` は `title` / `date` / `author` のみで slug は見ない）。

GitHub URL ソースの場合:

```yaml
---
title: "記事タイトル"
slug: "<slug>"           # ファイル名の <slug> 部分と一致させる。必須
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
draft: false
author: "<author id>"   # scripts/authors.json の id。GitHub URL ソースの場合は投稿者の github_login から解決
model: "<model id>"     # coding agent で執筆した場合は自動設定。手動執筆の場合は省略可
source_url: "https://github.com/..."
categories: ["カテゴリ"]
tags: ["tag1", "tag2"]
---
```

テキストトピックの場合:

```yaml
---
title: "記事タイトル"
slug: "<slug>"           # ファイル名の <slug> 部分と一致させる。必須
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
draft: false
author: "eotel"   # 手動実行時のデフォルト
model: "<model id>"     # coding agent で執筆した場合は自動設定。手動執筆の場合は省略可
categories: ["カテゴリ"]
tags: ["tag1", "tag2"]
---
```

## 外部 URL のフェッチ方針

記事作成・ファクトチェックを問わず、外部 URL のコンテンツを取得する際は以下の優先順位に従う:

1. **`aegis_fetch` を優先使用する**
   - セキュリティスキャン（verdict: allow/warn/block）付きでコンテンツを取得できる
   - verdict が "warn" → ユーザーに警告を表示して確認を求める
   - verdict が "block" → コンテンツを使用せず、ユーザーに報告する
   - 取得した HTML/JSON の解析は Claude が直接行う

2. **`aegis_fetch` が利用できない場合は `WebFetch` にフォールバック**
   - MCP 未接続、aegis 未起動などの場合

3. **`aegis_fetch` の大きな結果の扱い**
   - 結果がトークン上限を超えると、ランタイム側（Claude Code なら `~/.claude/projects/.../tool-results/`、Codex CLI も同様にホーム配下に退避）が自動的に外部ファイルへ保存する
   - このパスは保護対象（sensitive file）のため、`cp` や `Grep` でアクセスすると同意確認が発生する
   - **対処: `.claude/temp/` にコピーしてから Read/Grep する**
     ```bash
     cp ~/.claude/projects/.../tool-results/mcp-aegis-aegis_fetch-XXXX.txt .claude/temp/aegis-result.txt
     ```
   - 作業完了後は `.claude/temp/` 内のコピーを削除する
   - **同意プロンプトの恒久対策**: 初回の同意プロンプトで「Yes, and always allow access to tool-results/ from this project」を選択すれば、以降の `tool-results/` へのアクセスは自動許可される

4. **SPA（JavaScript 描画）サイトの場合**
   - `aegis_fetch` / `WebFetch` どちらでも生 HTML からコンテンツを取得できない場合がある
   - X (Twitter) の場合: URL を `api.fxtwitter.com` に変換して JSON API 経由で取得する
   - その他の SPA: `WebSearch` で該当ページの情報を検索する

## 記事の構成ガイドライン

- 見出し（##）を使って構造化する
- コード例がある場合はシンタックスハイライト付きのコードブロックを使用する
- 日本語で記述する
- 冒頭に概要・導入を書く
- 実用的な情報を含める（コマンド例、設定例、コードサンプルなど）
- GitHub Issue からの内容はそのまま活かしつつ、ブログ記事として読みやすく整形する
- **言説 claim には原文逐語を blockquote で埋め込む** (重要): 「X は Y と言っている」「書籍 *Z* でこう書かれている」と書くときは、要約だけで済ませず、原文の英語または日本語の逐語を blockquote (`>`) で本文に並置する。
  - 鉤括弧「...」付きスローガンは特に **逐語の存在確認が必須**。逐語が見つからない場合は鉤括弧を外して paraphrase 形式にする
  - 引用元の **著者 byline** を確認する（martinfowler.com のゲスト記事のように、サイトオーナー≠著者のパターンに注意）
  - 章節への参照（「Clean Code 第 3 章」など）は **章番号と章タイトル両方** を明示する。複数概念の合成を防ぐ
  - 詳細は `.claude/agents/claim-source-verifier.md` の「5 failure pattern」を参照
- **記事末尾に「関連 Wiki」セクションを設ける**（手順 5.5 で見つかった既存 Wiki ページを集約。空なら無くて良い）

  ```markdown
  ## 関連 Wiki

  - [LLM Wiki パターン](/blogs/wiki/concepts/llm-wiki-pattern/)
  - [aegis-fetch](/blogs/wiki/tools/aegis-fetch/)
  ```

### ダイアグラム（図）の作成ルール

アーキテクチャ図やフロー図が必要な場合、**アスキーアートは使わず drawio で画像化する**。SVG を手書きで作るのもアンチパターン — `.drawio` ソースが残らず後から編集できない。

1. drawio ファイルを作成する: `assets/images/<slug>-<diagram-name>.drawio`
   - mxgraph XML を直接 Write ツールで書ける。既存ファイル（例: `assets/images/harness-eval-cycle.drawio`、`assets/images/design-md-three-layers.drawio`）を雛形にすると効率が良い
2. PNG にエクスポートする（環境ごとに使い分け、`--scale 2` で高解像度）:
   - **GUI 版 draw.io がローカルにある macOS 開発機**: `.claude/skills/drawio/` の skill が `/Applications/draw.io.app/...` を自動検出してエクスポートする
   - **CI / Codex cloud / headless サンドボックス / GUI 未インストール**: **`./scripts/drawio-export.sh` (Docker) を使う**
     ```bash
     ./scripts/drawio-export.sh assets/images/<name>.drawio -f png --scale 2 -o assets/images/
     ```
   - skill が「CLI not found」を返した場合は **諦めず Docker スクリプトに自動フォールバック** する（GUI 未インストール環境のシグナルなので）
   - 内部で `rlespinasse/drawio-desktop-headless` を起動する。Docker Desktop / orbstack / colima のいずれかが稼働していれば良い
3. 記事内で絶対パスで参照する:
   ```markdown
   ![図の内容を自然文で記述した alt テキスト](/blogs/images/<name>.png)
   ```
4. **alt テキスト**: 図の内容を自然文で記述する（SEO の画像検索露出 + アクセシビリティ向上）
5. **相対パス（`../../images/`）は使わない**: Hugo のパーマリンク構造で 404 になるため、必ず `/blogs/images/` の絶対パスを使う
6. 既存の drawio ファイル（`assets/images/openclaw-gateway-architecture.drawio` 等）のスタイルを参考にする
7. 配置先は `assets/images/` （`static/` ではない）。`static/` 配下は Hugo image processing の対象外で WebP srcset 展開が効かない

## ファクトチェック & エージェントレビュー（6 並列起動）

記事ファイルを Write した直後、コミット前に **6 つの subagent を 1 つのメッセージで並列起動** する。
**このステップは省略してはならない。** 並列化により context 消費を抑え、観点ごとの verdict が独立して検証可能になる。

### 起動する subagent

| agent | 担当観点 | 出力 |
|---|---|---|
| `claim-source-verifier` | ツール存在・機能仕様・「公式」帰属など事実主張の裏付け | JSON verdict |
| `url-liveness-checker` | 記事内 URL の HTTP ステータス / 404 検出 | JSON verdict |
| `command-syntax-verifier` | CLI コマンド・API 呼び出しの構文・フラグ | JSON verdict |
| `version-date-checker` | バージョン番号・リリース日・互換性記述 | JSON verdict |
| `tech-writer` | 構成・読みやすさ・日本語品質 | 自然文レビュー |
| `seo-advisor` | タイトル / カテゴリ / タグ / 内部リンク | 自然文レビュー |

### 実行方法

`$ARTICLE_PATH` を `$WORKTREE_DIR/content/posts/YYYY/MM/YYYY-MM-DD-<slug>.md` に置き換えて、以下を **必ず 1 つのメッセージで並列起動** する:

```
Agent(subagent_type="claim-source-verifier",   prompt="記事絶対パス: $ARTICLE_PATH")
Agent(subagent_type="url-liveness-checker",    prompt="記事絶対パス: $ARTICLE_PATH")
Agent(subagent_type="command-syntax-verifier", prompt="記事絶対パス: $ARTICLE_PATH")
Agent(subagent_type="version-date-checker",    prompt="記事絶対パス: $ARTICLE_PATH")
Agent(subagent_type="tech-writer",             prompt="記事絶対パス: $ARTICLE_PATH")
Agent(subagent_type="seo-advisor",             prompt="記事絶対パス: $ARTICLE_PATH")
```

- 各 agent は記事を Read してレビューするだけで、ファイル編集はしない
- レビュー対象は `$WORKTREE_DIR` 内のファイル

### JSON verdict スキーマ（fact-check 系 4 agent 共通、claim-source-verifier は拡張あり）

```json
{
  "agent": "claim-source-verifier",
  "article": "content/posts/YYYY/MM/YYYY-MM-DD-slug.md",
  "checked_at": "ISO8601 UTC",
  "claims": [
    {
      "line": 42,
      "claim_type": "factual | discourse | verbatim-quote",
      "claim": "...",
      "verdict": "verified | needs_fix | incorrect | uncertain",
      "failure_pattern": "misattribution-author-confusion | citation-mismatch-empty-footnote | scare-quote-without-verbatim | conceptual-conflation | paraphrase-over-extension | null",
      "evidence": "URL + 逐語引用 + byline 確認結果",
      "suggestion": "needs_fix / incorrect のとき必須"
    }
  ],
  "summary": {
    "verified": 0, "needs_fix": 0, "incorrect": 0, "uncertain": 0,
    "by_pattern": {
      "misattribution-author-confusion": 0,
      "citation-mismatch-empty-footnote": 0,
      "scare-quote-without-verbatim": 0,
      "conceptual-conflation": 0,
      "paraphrase-over-extension": 0
    }
  }
}
```

`claim_type` の意味:
- `factual` — ツール存在・機能仕様・組織所属など客観的事実
- `discourse` — 「誰が何を言ったか / どこに書いたか」の言説主張
- `verbatim-quote` — 鉤括弧で囲まれた逐語引用主張

言説主張 (`discourse` / `verbatim-quote`) は事実主張より厳しく判定される。詳細は `.claude/agents/claim-source-verifier.md` の「5 failure pattern」を参照。

### verdict の集計と反映（skill 本体側で実施）

1. fact-check 系 4 agent の JSON verdict をマージし、`verdict` ごとに件数をユーザーへ簡潔に報告する
2. **claim-source-verifier の `by_pattern` 集計も別途報告する**。`misattribution-author-confusion` や `citation-mismatch-empty-footnote` が 1 件でもあれば、それは構造的に最重要なので冒頭で警告する
3. verdict ごとの処理方針:
   - **verified**: ノーアクション
   - **needs_fix**: `Edit` で記事を即座に修正（`suggestion` を反映）。言説 claim の場合は **原文逐語を blockquote で本文に追加する** ことを優先
   - **incorrect**: 即座に削除 or `Edit` で修正。ソース無しの独自主張は削除を優先
   - **uncertain**: 件数のみユーザーに報告し、判断を仰ぐ
4. `tech-writer` / `seo-advisor` のレビュー結果は以下の基準でフィルタリング:
   - **即座に反映**: 誤字脱字、表記揺れ、明らかな構成の問題、タグの過不足
   - **ユーザーに確認**: タイトル変更、カテゴリ変更、大幅な構成変更
   - **スキップ**: 好みの問題（文体の微調整など）、既存記事への内部リンク追加（別 PR で対応）
5. 修正後、`git diff` で変更を確認してからコミットへ進む

### 補足

- 単発の総合ファクトチェックを行いたい場合は `fact-checker` agent を直接呼べる（4 観点を 1 agent で走査する用途）
- 各 fact-check agent の検証ルール詳細は `.claude/agents/<agent-name>.md` を参照

## コミット・ブランチ・PR 作成（worktree 方式）

記事作成後、以下の手順で PR を作成する。
**重要: git worktree を使い、メインの作業ディレクトリのブランチを汚さないようにする。**
**重要: コマンドを `&&` で繋がないこと。** `&&` で繋いだ複合コマンドは許可パターンにマッチせず、毎回確認が求められる。各コマンドは個別の Bash 呼び出しとして実行する。

1. ブランチ名を決定する: `blog/YYYY-MM-DD-<slug>`
2. worktree を作成する:
   ```bash
   # メインリポジトリのルートで実行（main ブランチのまま）
   BRANCH_NAME="blog/YYYY-MM-DD-<slug>"
   git worktree add -b "$BRANCH_NAME" ".worktrees/<slug>" main
   ```
3. **worktree の絶対パスを取得する（重要）:**
   ```bash
   git worktree list
   ```
   出力から worktree の絶対パスを読み取り、以降はその絶対パスを `$WORKTREE_DIR` として使う。
   **相対パスから絶対パスを推測してはならない。** Write ツールは存在しないパスにもファイルを作成するため、パスを間違えてもエラーにならず手戻りが発生する。
4. **worktree で lefthook を install する**（pre-push hook を worktree から fire させるため）:
   ```bash
   ( cd "$WORKTREE_DIR" && lefthook install )
   ```
   `lefthook install` は cwd の `git rev-parse --git-path hooks` を解決して hook scripts を書き出すため、**必ず worktree 内で実行する必要がある**（main で install しただけでは worktree から fire しないケースがある — 特に `core.hooksPath` が相対パスで設定されている環境）。`/blog` が新規 worktree を生成する瞬間にはセッション開始フェーズを既に過ぎているため、SessionStart hook の install だけでは間に合わない。subshell でラップしているのは、`cd` がスキルの top-level cwd を汚さないようにするため。install に失敗しても致命ではないが、stderr を確認しておくこと。
5. worktree 内で記事ファイルを作成する:
   - 記事の書き込み先: `$WORKTREE_DIR/content/posts/YYYY/MM/YYYY-MM-DD-<slug>.md`
6. worktree 内で Hugo ビルド確認（`cd` を使わず `--source` で指定）:
   ```bash
   hugo --source "$WORKTREE_DIR" --gc 2>&1 | tail -5
   ```
7. **worktree 内で wiki-lint を実行**（CI と同じ fatal チェックをローカルで先取り）:
   ```bash
   python3 "$WORKTREE_DIR/.claude/skills/wiki-lint/scripts/wiki_lint.py"
   ```
   `wiki_lint.py` はスクリプト自身の絶対パスからリポジトリルートを自動検出するため、worktree 内のスクリプトを直接呼べば worktree が root として評価される。exit code 0 を確認する。`slug:` 欠落や frontmatter 不備などはここで止める。
   **なぜここで明示的に走らせるのか**: `lefthook.yml` の pre-push にも wiki-lint は登録されているが、`core.hooksPath = .git/hooks` が相対パスで設定されている環境では worktree から `git push` した際に hook が解決できず fire しないことがある（前述の手順 4 と SessionStart hook で `lefthook install` を試みているが、install 失敗時の保険として skill 内で先に lint を呼ぶことで二重ガードになる）。
8. worktree 内でコミット・プッシュ（`cd` を使わず `git -C` で指定）:
   ```bash
   git -C "$WORKTREE_DIR" add content/posts/YYYY/MM/YYYY-MM-DD-<slug>.md
   git -C "$WORKTREE_DIR" commit -m "Add blog post: <記事タイトル>"
   git -C "$WORKTREE_DIR" push -u origin "$BRANCH_NAME"
   ```
9. PR を作成する（`--head` でブランチを明示指定し、`cd` を使わない）:
   PR 本文は worktree 内に書き出し、`--body-file` で渡す。worktree は `.claude/` の外にあるため、Write ツールで直接書き込める。

   **PR 本文には必ず `Closes #<issue_number>` を含める**（Issue URL がソースの場合）。マージ時に GitHub が自動で Issue を close する。
   ```markdown
   ## Summary

   <記事の要約 1〜3 文>

   Closes #<issue_number>

   ## Test plan

   - [x] hugo --gc でビルド成功
   - [x] ファクトチェック完了
   - [x] tech-writer / seo-advisor レビュー反映
   ```

   ```bash
   # Write ツールで $WORKTREE_DIR/pr_body.md に PR 本文を書き出す
   gh pr create --repo Eotel/blogs --head "$BRANCH_NAME" --title "Add blog: <記事タイトル>" --body-file "$WORKTREE_DIR/pr_body.md"
   ```
   **注意: `cd "$WORKTREE_DIR" && gh pr create` は使わないこと。** `cd` で始まるコマンドは `Bash(gh:*)` の許可パターンにマッチせず、毎回確認が求められる。`--head` フラグでブランチを指定すれば worktree 内にいる必要はない。
   **注意: `--body "$(cat <<'EOF'...)"` 方式は使わないこと。** HEREDOC 内の `#` 付き行がセキュリティチェック（"quoted newline followed by #-prefixed line"）に引っかかり、毎回確認が求められる。
10. PR の URL をユーザーに伝える
11. **PR がマージされたら worktree を削除する。** ユーザーがマージを指示・確認した直後に `git worktree remove --force "$WORKTREE_DIR"` を実行する（`pr_body.md` 等の未追跡ファイルが残るため `--force` が必要）。

## ソース Issue の自動 close

Issue URL がソースの場合、PR 本文の `Closes #<issue_number>` により **PR マージ時に GitHub が自動で Issue を close する**。手動コメント追記やリアクション付与は不要。

ブログ化を見送る場合（重複トピック等）は、Issue を手動で close + 理由をコメントで残す:
```bash
gh issue close <issue_number> --comment "重複のため見送り: #<別Issue>"
```

## 後処理

1. 作成した PR の URL をユーザーに伝える
2. PR マージ後、worktree を自動削除する（`pr_body.md` 等の未追跡ファイルが残るため `--force` が必要）:
   ```bash
   git worktree remove --force "$WORKTREE_DIR"
   ```

> Wiki 取り込みは GitHub Actions（`.github/workflows/auto-wiki-ingest.yml`）が週次でまとめて実行する。/blog 単体では Wiki 更新を行わない。手動で即時反映したい場合は `/wiki-ingest <記事パス>` を実行する。
