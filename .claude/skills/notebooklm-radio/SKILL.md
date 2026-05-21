---
name: notebooklm-radio
description: 公開済みの blog post から NotebookLM Audio Overview (日本語ポッドキャスト) を生成し、記事フロントマターに紐付ける
arguments:
  - name: target
    description: "対象 post の URL (`https://eotel.github.io/blogs/posts/YYYY/MM/<slug>/`) または md ファイルパス (`content/posts/YYYY/MM/<slug>.md`)"
    required: true
  - name: format
    description: "音声形式: deep_dive (既定) / brief / critique / debate"
    required: false
  - name: length
    description: "長さ: short / default (既定) / long"
    required: false
  - name: force
    description: "true なら同タイトルの notebook が既存でも上書き再生成"
    required: false
---

公開済みの blog post から NotebookLM の **日本語 Audio Overview** を生成し、GitHub Release Assets
(`audio` rolling tag) に upload して、記事 frontmatter に `audio_url` を埋め込んでください。

実装は 2 層:

- **`scripts/notebooklm-radio-tui.sh`** — fzf ベースの対話 TUI。post を絞り込み・プレビューしながら選び、言語/長さ/形式/focus を fzf ピッカーで決め、最後に確認して dispatch。**ターミナルから手動で使うときはこちらを推奨**
- **`scripts/notebooklm-radio.sh`** — フラグ駆動の本体。`/notebooklm-radio <target>` 経由や cron / batch から呼ぶ用

配信先:
- ローカル cache: `static/audio/<slug>/overview.m4a` (`.gitignore` 済、再 upload 用に保持)
- 公開 URL: `https://github.com/Eotel/blogs/releases/download/audio/<slug>.m4a`

## いつ使うか

- `/blog` で公開済みの記事に音声解説を後付けしたいとき
- 既に公開された他の post を音声化したいとき（hdknr 由来の歴史記事を含む）

## いつ使わないか

- まだ PR がマージされていない記事（NotebookLM は公開 URL を ingest するので、本番反映前は失敗する）
- 多言語化したいとき（v1 は日本語固定）

## 前提条件

1. `nlm` CLI がインストール済み (`uv tool install notebooklm-mcp-cli`)
2. `nlm login --profile blogs` で blog 専用 profile を作成済み
3. `.envrc` に `export NOTEBOOKLM_HL=ja` が設定済み（フォールバック）
4. `direnv allow` 済み

`nlm doctor` は cookie の存在しか見ないため、
**真の認証チェックは `nlm notebook list --profile blogs --json` を実機で叩く** こと。
スクリプトの preflight はこれを実装している。

## 標準手順（推奨: TUI）

```bash
./scripts/notebooklm-radio-tui.sh
```

これで以下が順に出る:

1. fzf で 700+ 件の post を絞り込み・プレビュー（★ = audio あり）
2. fzf で言語 (ja / en / en-US / zh-CN / ko / es / fr / de / pt-BR / it ...) を選択
3. fzf で長さ (short / default / long) を選択
4. fzf で形式 (deep_dive / brief / critique / debate) を選択
5. focus プロンプトを自由入力（例: 「セキュリティ観点を強調」「初学者向け」）。空 Enter で省略可
6. 内容確認 y/N
7. `notebooklm-radio.sh` を exec で起動

★ が既に付いた post を選ぶと「再生成しますか?」と聞かれ、`--force` 付きで実行される。

## フラグ経路（スクリプト直叩き）

```bash
# URL 指定
./scripts/notebooklm-radio.sh https://eotel.github.io/blogs/posts/2026/05/2026-05-21-some-slug/

# ファイルパス指定
./scripts/notebooklm-radio.sh content/posts/2026/05/2026-05-21-some-slug.md

# dry-run (slug 解決・タイトル抽出までで停止)
./scripts/notebooklm-radio.sh <target> --dry-run

# 言語切替（既定は $NOTEBOOKLM_HL or ja）
./scripts/notebooklm-radio.sh <target> --language en-US

# focus topic を与える
./scripts/notebooklm-radio.sh <target> --focus "セキュリティ観点を強調"

# 短尺・別形式
./scripts/notebooklm-radio.sh <target> --length short --format brief

# 既存 notebook があっても再生成
./scripts/notebooklm-radio.sh <target> --force
```

完了後:

```bash
hugo --gc
# 該当記事を localhost で開き、ヘッダー直下に "音声解説" バッジ付きの <audio> プレイヤーがあるか確認
```

## 失敗時の対処

| エラー | 原因 | 対処 |
|---|---|---|
| `Profile not found: blogs` | profile 未作成 | `nlm login --profile blogs` でブラウザログイン |
| `Authentication expired` | cookie 期限切れ (~2-4 週) | 同上 (`nlm login --profile blogs`) |
| `source add / ingest failed` | URL が公開前 or NotebookLM がクロール失敗 | 公開反映を待つ。Hugo build → push → Pages 反映後に再実行 |
| `timed out waiting for audio artifact` | 15 分以内に生成完了せず | `nlm studio status <nb> --profile blogs` で状況確認。生成中なら `--id <artifact-id>` で download を直叩き |
| `download produced empty file` | artifact_id mismatch | `nlm studio status <nb> --json` で正しい artifact_id を取得し直す |

## 設計上のメモ

- 1 post = 1 notebook（NotebookLM library に溜まり続けるため、月次で `nlm notebook list --profile blogs` を棚卸し）
- 出力拡張子は `.m4a` (mime `audio/mp4`)。NotebookLM の既定出力に合わせている
- `/blog` との自動連携はしない（cookie 期限切れで blog 公開フロー全体が止まるリスク回避）
- 音声形式は `deep_dive` 既定（NotebookLM の象徴的 2 ホスト対談）

## 配信: GitHub Release Assets (rolling tag `audio`)

m4a はリポジトリには commit せず、固定の release `audio` に asset として upload する。

- URL 形式: `https://github.com/Eotel/blogs/releases/download/audio/<slug>.m4a`
- ローカル cache: `static/audio/<slug>/overview.m4a` (`.gitignore` 済)
- 初回 1 回だけ release を作る: `gh release create audio --title "Eotel Blog Audio Overviews" --notes-file <notes.md> --latest=false`
- 以後は script が `gh release upload audio <file> --clobber` で同一 tag に追加し続ける
- リリース管理: 単一 tag のみ。**`gh release delete audio` を絶対に走らせない**（全 post の音声リンクが切れる）
- repo を fork した人向け: `NOTEBOOKLM_RADIO_REPO=<owner/repo>` / `NOTEBOOKLM_RADIO_RELEASE_TAG=<tag>` で URL 先を切替可能

GitHub Pages の 1GB 制限を回避し、帯域も無料。`gh release upload` には repo write 権限が要るので、GH_TOKEN の scope は `repo` を含める。

## 並列実行の制約

`nlm login switch` がグローバル設定をいじる仕様なので、download 段は `static/audio/.../profile-switch.lock` の mkdir-based atomic lock で直列化される。同じ post を複数セッションから同時に回しても download 自体は安全（順番に処理される）が、生成中の notebook が重複作成される。**並列で叩くなら別 post に限ること。**

詳細設計と背景は `docs/exec-plans/active/2026-05-21-notebooklm-radio-skill.md` を参照。
