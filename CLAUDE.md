# Eotel's Notebook

Hugo + PaperMod で構築された技術ブログ。GitHub Pages でホスティング。
（フォーク元の hdknr/blogs から派生。Eotel が運用する個人ブログ。historical post は hdknr 由来）

## ツール実行時の許可ルール

- ツール実行（Bash、ファイル操作など）の許可を求めるときは、必ず日本語で説明・確認を行うこと
- 許可を求める際、以下のセキュリティリスクをパーセンテージ(%)で提示すること
  - パスワードや秘密鍵が外に漏れる可能性
  - 外部サーバーにデータが送られる可能性
  - 悪意あるコードが勝手に動く可能性
  - PCの設定が書き換わる可能性

## プロジェクト構成

- `content/posts/YYYY/MM/` — ブログ記事（`YYYY-MM-DD-<slug>.md` 形式、年月別サブフォルダー）
- `content/wiki/` — Wiki ナレッジベース（concepts/, tools/, guides/）
- `.claude/skills/wiki-ingest/` — `/wiki-ingest` スキル定義
- `scripts/categorize.py` — カテゴリ・タグ自動付与スクリプト
- `hugo.toml` — Hugo 設定ファイル
- `.claude/skills/blog/` — `/blog` スキル定義
- `.claude/agents/` — カスタム専門エージェント
- `.codex/agents/` — `.claude/agents/` への symlink（Codex CLI から同じ agent 定義を参照するための共有口）
- `.claude/temp/` — 一時ファイル置き場（.gitignore 済み、`/tmp` の代わりに使用）
- `.worktrees/` — git worktree 置き場（.gitignore 済み、`.claude/` 外なので sensitive file 扱いされない）

## カスタムエージェント

以下の専門エージェントが `.claude/agents/` に定義されている（`.codex/agents/` からも同じものを参照可能）:

### `/blog` のメインフロー（6 並列で起動）

ファクトチェック系（JSON verdict を返す）:

- **claim-source-verifier** — 事実主張（ツール存在・機能仕様・「公式」帰属）を一次情報で裏付け検証
- **url-liveness-checker** — 記事内 URL の HTTP ステータス確認（404 / dead link 検出）
- **command-syntax-verifier** — CLI コマンド・API 呼び出しの構文・フラグを公式仕様と照合
- **version-date-checker** — バージョン番号・リリース日・互換性記述の検証

品質レビュー系（自然文レビュー）:

- **seo-advisor** — SEO 最適化（タイトル改善、タグ提案、内部リンク提案）
- **tech-writer** — 記事品質レビュー（構成、読みやすさ、日本語品質）

### 用途別

- **fact-checker** — 単発の総合ファクトチェック（観点を分けない一括走査）。`/blog` のメインフローでは使わない。**wiki ページのファクトチェックには `wiki-fact-checker` を使う**
- **trend-researcher** — 技術トレンド調査と記事ネタ提案
- **wiki-linter** — Wiki 健全性チェック (`/wiki-lint` から委託、`model: haiku` 固定でコスト最適化)
- **wiki-fact-checker** — 既存 Wiki ページの claim を一次情報照合して JSON verdict を返す (`/wiki-decay refresh` から委託、`model: haiku` 固定)
- **backlog-rescanner** — Wiki ingest backlog の滞留記事を再走査して update_candidate 昇格候補を抽出 (`/wiki-ingest backlog-rescan` から委託、`model: haiku` 固定)

## モデル選択の方針

- `/blog` — Sonnet 4.6 推奨（ファクトチェックは subagent に隔離されているのでメインは執筆に専念）
- `/wiki-ingest` / `/wiki-query` — Sonnet 4.6 推奨（要約・読解中心、Opus は過剰）
- `/wiki-ingest backlog-rescan` — Sonnet 4.6 推奨（探索は `backlog-rescanner` agent が Haiku 4.5 で走り、Sonnet 親は統合判断と Edit/Write のみ担当）
- `/wiki-lint` — 親セッションのモデルは何でもよい（`wiki-linter` subagent が Haiku 4.5 で走る）
- 切り替え: `/model sonnet` または `/model haiku` をスキル実行前に

## 記事作成

- `/blog <トピック or GitHub Issue URL>` スキルで記事作成〜PR作成まで自動化
- **URL 制限: `/blog` スキルで受け付ける URL は `https://github.com/Eotel/blogs/` 配下のみ。他リポジトリの URL は拒否する**
- 記事は日本語で記述
- 記事パス: `content/posts/YYYY/MM/YYYY-MM-DD-<slug>.md`
- フロントマター: title, date, lastmod, draft, author, categories, tags（+ source_url）
  - `author` は `scripts/authors.json` の `id` を指定する（デフォルト: `eotel`）
  - 新規記事は `archetypes/default.md` から `author: "eotel"` がセットされる
  - `import-gists.sh` 経由の記事は authors.json で解決された author id がセットされる
- カテゴリは `scripts/categorize.py` のルールに従う
- ビルド確認: `hugo --gc`
- **ダイアグラムは画像化する**: アスキーアート（```` ``` ```` 内のテキスト図）は使わず、PNG で埋め込む。生成経路は図の性質で選ぶ:

  | 図の性質 | 推奨経路 |
  |---|---|
  | コンセプト図・ヒーロー画像・イメージ図・単発の説明図（後から編集しない） | **Codex CLI に gpt-image で直接 PNG 生成** を最優先 |
  | アーキテクチャ図・フロー図・シーケンス図・ER 図など、ソースを残して後から編集したい構造図 | **drawio** で mxgraph XML を書き、PNG にエクスポート |

  - **Codex 経路** (推奨デフォルト): `codex exec` を Bash で直接呼び出して `image_generation` ツール (gpt-image) に PNG を作らせる。ChatGPT subscription auth (`codex login`) で動作する (`codex:rescue` skill 経由 / `codex-companion.mjs task` 経路は `OPENAI_API_KEY` を要求するので使わない)。drawio XML を経由しないので速い:
    ```bash
    codex exec -s workspace-write --skip-git-repo-check "次の図を image_generation ツールで生成して assets/images/<slug>-<diagram>.png に PNG 保存してください。サイズ 1024x1024。図の内容: <自然文記述>"
    ```
    - Codex は `~/.codex/generated_images/<session>/` に一旦保存し、指定パスへ自動コピーする
    - サイズ調整が必要なら `sips -z <h> <w> <path>` を codex 自身に依頼すれば良い
    - Codex CLI が呼び出せない / 未ログインの環境では使えない → drawio へフォールバック
  - **drawio 経路**:
    - drawio ファイル: `assets/images/<name>.drawio`（mxgraph XML を直接書ける。既存ファイルを雛形にする）
    - 環境別の export 手段:
      | 環境 | export 手段 |
      |---|---|
      | ローカル開発 (GUI 版 draw.io インストール済み) | `.claude/skills/drawio/` の skill（APM 管理）が macOS app を自動検出 |
      | **CI / Codex cloud / headless サンドボックス / GUI 未インストール** | **`./scripts/drawio-export.sh` (Docker 経由)** |
    - **`/Applications/draw.io.app/Contents/MacOS/draw.io` が見つからない場合は迷わず Docker スクリプトにフォールバックする** — skill の出力が「CLI not found」になっても諦めず、`./scripts/drawio-export.sh` で再試行すること
    - Docker 経路の使い方:
      ```bash
      ./scripts/drawio-export.sh assets/images/<name>.drawio -f png --scale 2 -o assets/images/
      ```
      - 内部で `rlespinasse/drawio-desktop-headless` を起動する。Docker Desktop / orbstack / colima のいずれかが稼働していれば良い
      - 環境変数 `DRAWIO_EXPORT_IMAGE` でイメージ差し替え、`DRAWIO_EXPORT_TIMEOUT` でタイムアウト変更が可能
    - GUI 版 draw.io がローカルにある場合の直接呼び出し例: `/Applications/draw.io.app/Contents/MacOS/draw.io --export --format png --scale 2 --output assets/images/<name>.png assets/images/<name>.drawio`
  - 記事内参照: `![alt テキスト](/blogs/images/<name>.png)`（絶対パス。`layouts/_default/_markup/render-image.html` が assets を解決して responsive WebP + raster srcset に展開する）
  - alt テキストには図の内容を自然文で記述する（SEO・アクセシビリティ向上）

## 画像最適化

- 画像は `assets/images/` に配置する（`static/` ではない）。`static/` に置いた画像は Hugo image processing の対象外。
- markdown の `![](...)` は `layouts/_default/_markup/render-image.html` フックで処理され、ローカル PNG/JPG は `<picture>` + WebP srcset（480w / 768w / 1024w / 1440w / 原寸）に自動展開される。
- SVG・外部 URL（`http(s)://`）は素の `<img loading="lazy" decoding="async">` のままレンダーされる（SVG は Hugo の image processing 対象外）。
- 参考: https://gohugo.io/content-management/image-processing/

## 外部 URL のフェッチ方針

- 記事作成・ファクトチェックを問わず、外部 URL の取得には `aegis_fetch` MCP ツールを優先使用する
- aegis が利用できない場合（MCP 未接続等）は `WebFetch` にフォールバック
- SPA サイト（X/Twitter 等）は `api.fxtwitter.com` 等の代替 API を利用する
- aegis 環境: `~/Projects/aegis`（`docker compose up -d` で起動）
- 詳細は `.claude/skills/blog/SKILL.md` の「外部 URL のフェッチ方針」セクションを参照

## Wiki 管理（LLM Wiki パターン）

- `/wiki-ingest <対象>` — 記事から Wiki ページを自動生成・更新（**新規流入**）
- `/wiki-query "<質問>"` — Wiki と posts に質問を投げて引用付きで回答（**入力 / 検索**）
- `/wiki-lint` — Wiki の健全性チェック（孤立ページ、欠落リンク、古い記述 / + decay advisory）
- `/wiki-decay` — Wiki ページの `lastmod` を section 別閾値で評価し、古びた候補を浮かせる（**老朽化検出**）。週次 cron で Issue 起票も自動化 (`.github/workflows/wiki-decay-report.yml`)
  - 閾値: tools/ 45/90d, guides/ 75/150d, concepts/ 150/300d (soft/hard)
  - `/wiki-decay refresh <section>/<slug>` で `wiki-fact-checker` agent を起動し claim 再検証
- Wiki 構造: `content/wiki/concepts/`（概念）、`content/wiki/tools/`（ツール）、`content/wiki/guides/`（手順）
  - **opt-in セクション**: `content/wiki/qa/` は `/wiki-query --save` 時だけ生成される（v1 ではデフォルト保存しない）
- Wiki ページのフロントマター: title, description, date, lastmod, aliases, related_posts, tags
- Wiki ページは記事の丸コピーではなく、要約・統合した知識として再構成する
- **Wiki content は snapshot ではなく "現時点で通用する知識"**。事実は時間で腐るため、`/wiki-decay` の週次レポートで refresh 対象を triage する運用
- Wiki セクション専用レイアウト: `layouts/wiki/`（single.html, list.html）
- 詳細は `.claude/skills/wiki-ingest/SKILL.md`、`.claude/skills/wiki-query/SKILL.md`、`.claude/skills/wiki-lint/SKILL.md`、`.claude/skills/wiki-decay/SKILL.md` を参照

## Gist 取り込み運用 (multi-author)

- 取り込み対象ユーザーは `scripts/authors.json` の allowlist で管理する
- **公開する gist のファイル名は `*.blog.md` とする**（例: `claude-code-tips.blog.md`）— private なメモ (`notes.md`、`journal.md` 等) と同じ gist 内に共存しても、`*.blog.md` だけが Hugo に取り込まれる
- 1 つの gist に複数の `*.blog.md` を入れた場合、それぞれが個別の post として展開される（slug は `<gist_id>-<basename>`）
- 既存記事 (hdknr 由来の 783 件) は touch しない。新規 crawl 対象は `gist_import:true` のユーザー (= Eotel) のみ
- 一括取り込み: `./scripts/import-gists.sh` ／ ユーザー指定: `./scripts/import-gists.sh eotel`
- **gist 自体を起こす段は `/gist-writer <topic>` スキルを使う**: 既存 `content/wiki/` を input にして `*.blog.md` の draft を `.claude/temp/` に生成し、ユーザー確認後 `gh gist create --public` で公開する。フロントマターは gist 側に書かず、`import-gists.sh` の自動生成に任せる。詳細は `.claude/skills/gist-writer/SKILL.md`
- **gist 自体を起こす段は `/gist-writer <topic>` スキルを使う**: 既存 `content/wiki/` を input にして `*.blog.md` の draft を `.claude/temp/` に生成し、ユーザー確認後 `gh gist create --public` で公開する。フロントマターは gist 側に書かず、`import-gists.sh` の自動生成に任せる。詳細は `.claude/skills/gist-writer/SKILL.md`

## カテゴリ一覧

AI/LLM, セキュリティ, クラウド/インフラ, Web開発, プログラミング言語, モバイル, データベース, ツール/開発環境, ビジネス/キャリア, 地域/グルメ, その他

## Bash コマンドの必須ルール（auto モード対応）

以下のルールに違反するとコマンドが許可パターンにマッチせず、auto モードで処理が停止する。**例外なく守ること。**

- **`&&` や `|` でコマンドを繋がない** — 各コマンドは個別の Bash 呼び出しで実行する
- **`/tmp` を使わない** — 一時ファイルは `.claude/temp/` に置く
- **`gh pr create` で HEREDOC を使わない** — worktree 内の `pr_body.md` に Write ツールで書き出して `--body-file` で渡す
- **`$()` コマンド置換を含む引数を避ける** — 一時ファイル + `--input` 方式を使う
- **変数代入とコマンドを同一行で繋がない** — `BRANCH_NAME=...` と `git worktree add ...` は別々に実行する

詳細な実装例は `.claude/skills/blog/SKILL.md` の「コミット・ブランチ・PR 作成」セクションを参照。

## ブランチ・PR 規約

- ブランチ名: `blog/YYYY-MM-DD-<slug>`
- コミットメッセージ: `Add blog post: <記事タイトル>`
- PR タイトル: `Add blog: <記事タイトル>`
- ソースが GitHub URL の場合、PR 作成後にソース元へリンクを追記する

## ブログ化状態の管理

1 topic = 1 Issue 運用。GitHub の Issue open/close で表す:

- **open + ラベルなし** → 未着手 / 書きたい（batch 対象）
- **open + `wip` ラベル** → 保留・調査中（batch 対象外）
- **closed** → ブログ化済み（PR の `Closes #N` で自動 close）or 見送り（手動 close + 理由コメント）

Issue 作成は軽量で OK（タイトル + URL + 0〜1 行）。本気の執筆は PR 側で行う。

```bash
# 未対応 Issue 一覧
gh issue list --repo Eotel/blogs --state open --search "-label:wip"

# bulk 記事化（wip 除外、open 全部）
./scripts/blog-batch.sh --dry-run     # まず確認
./scripts/blog-batch.sh --limit 3     # 3 件だけ
./scripts/blog-batch.sh --overnight   # 全件夜間処理

# 見送り（重複トピック等）
gh issue close <N> --comment "見送り理由: ..."
```

ラベルは初回 1 度だけ作成: `bash scripts/setup-labels.sh`
