# Eotel blog

https://eotel.github.io/blogs/

Hugo + PaperMod で構築された技術ブログ。GitHub Pages でホスティング。

## 開発環境セットアップ

### devenv (推奨)

[devenv](https://devenv.sh) (Nix ベース) で Hugo / Python / lint ツール / drawio export を 1 コマンドで揃えられる。
`lefthook install`・`pip install -r requirements.txt` は `enterShell` で自動実行されるので、下記の brew 手順を踏まずに済む。

```bash
# devenv 本体 (未導入なら)
curl -L https://install.determinate.systems/nix | sh -s -- install
nix profile install nixpkgs#devenv

# shell に入る (初回は数分かかる)
devenv shell
```

direnv 経由で `cd` 時に自動有効化したい場合は、初回だけ devenv 公式の direnvrc を
direnv のユーザー lib に配置する必要がある (これが無いと `use_devenv: command not found` で落ちる):

```bash
mkdir -p ~/.config/direnv/lib
devenv direnvrc > ~/.config/direnv/lib/devenv.sh

# プロジェクトの .envrc を許可
direnv allow
```

devenv shell 内で使える便利スクリプト:

| コマンド | 用途 |
|---|---|
| `hugo-serve` | `hugo server --buildDrafts` を 0.0.0.0 で起動 |
| `hugo-check` | `lefthook pre-push` と同等の build チェック |
| `drawio-export <file.drawio>` | `static/images/*.drawio` を PNG/SVG に変換 (Docker 必須) |
| `wiki-lint` | `wiki_lint.py` のラッパー |

`drawio-export` は [`rlespinasse/drawio-desktop-headless`](https://github.com/rlespinasse/docker-drawio-desktop-headless) Docker イメージを使うので、別途 Docker Desktop か colima を入れておく。
画像の絶対 pin が必要なら `inputs.nixpkgs` を `devenv.yaml` で固定する。

### Lefthook (pre-commit / pre-push フック)

このリポジトリは [lefthook](https://github.com/evilmartians/lefthook) で commit/push 時の lint を自動化している。
**devenv shell に入っていれば `lefthook install` は自動実行される**ので下記は brew 単体運用する場合のみ必要。

```bash
# 初回ツールインストール (devenv を使わない場合)
brew install lefthook shellcheck markdownlint-cli2

# Python lint (ruff/black) は uv または pip 経由で入れる
# ast-grep は別途 `brew install ast-grep` などで導入

# git hooks をインストール
lefthook install
```

#### 何が走るか

- **pre-commit** (staged ファイルのみ・直列パイプ): `ruff --fix` → `black --quiet` → `markdownlint-cli2 --fix` (ここまで auto-fix + 再 stage) → `git secrets` → `shellcheck` → `scripts/check_frontmatter.py` → `ast-grep scan`
- **commit-msg / prepare-commit-msg**: `git secrets` でメッセージを検査
- **pre-push**: `hugo --gc` で build 確認 → `wiki_lint.py` 全体 → `ast-grep scan` 全体
- **CI** (`.github/workflows/lint.yml`): pre-push 相当を PR で再実行（ローカルスキップ対策）

#### 緊急時に hook を bypass する

```bash
LEFTHOOK=0 git commit -m "..."
LEFTHOOK=0 git push
```

#### 手動で hook を走らせる

```bash
lefthook run pre-commit                                    # staged 差分
lefthook run pre-commit --files content/wiki/concepts/rag.md  # 特定ファイル
lefthook run pre-push
```

## スクリプト

### blog-batch.sh — open Issue の一括ブログ化

`wip` ラベルが付いていない open Issue を 1 topic = 1 記事として `claude -p` 経由で順次処理する。`/blog` が PR 本文に `Closes #N` を入れるので、PR マージで Issue は自動 close される。

```bash
# 対象 Issue 一覧を確認（dry-run）
./scripts/blog-batch.sh --dry-run

# 3件だけ処理
./scripts/blog-batch.sh --limit 3

# ラベルで絞り込み
./scripts/blog-batch.sh --label priority:high

# レビュー省略で高速に処理
./scripts/blog-batch.sh --skip-review --limit 5

# opus モデルで処理
./scripts/blog-batch.sh --model opus --limit 3

# 夜間バッチ（帰宅前に実行、翌朝PRレビュー）
nohup ./scripts/blog-batch.sh --overnight > .claude/temp/blog-batch-stdout.log 2>&1 &

# 翌朝：レポート確認
cat .claude/temp/blog-batch-report-*.md
```

#### オプション

| オプション | 説明 | デフォルト |
|---|---|---|
| `--dry-run` | 対象 Issue 一覧表示のみ（ブログ作成しない） | - |
| `--label LABEL` | 対象ラベルで絞り込み | - |
| `--milestone NAME` | マイルストーンで絞り込み | - |
| `--search QUERY` | 任意の `gh issue list --search` クエリ | - |
| `--limit N` | 処理件数の上限 | 全件 |
| `--skip-review` | ファクトチェック・エージェントレビューを省略 | false |
| `--model MODEL` | 使用モデル | sonnet |
| `--interval SECS` | 処理間のインターバル（秒） | 5 |
| `--overnight` | 夜間バッチモード（skip-review + インターバル 60 秒） | - |

#### ブログ化状態の管理

1 topic = 1 Issue 運用。GitHub の Issue open/close で状態を表す:

- **open + ラベルなし** → 未着手（batch 対象）
- **open + `wip` ラベル** → 保留・調査中（batch 対象外）
- **closed** → ブログ化済み（PR の `Closes #N` で自動 close）or 見送り（手動 close + 理由コメント）

ラベルは初回 1 度だけ作成: `bash scripts/setup-labels.sh`

### categorize.py — カテゴリ・タグ自動付与

依存ライブラリ（PyYAML）を初回のみインストール:

```bash
pip install -r requirements.txt
```

実行:

```bash
python scripts/categorize.py
```
