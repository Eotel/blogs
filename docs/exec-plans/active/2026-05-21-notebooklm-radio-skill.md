---
title: notebooklm-radio スキル — Blog から NotebookLM 日本語音声解説を生成
status: in-progress (auto-mode, started 2026-05-21)
date: 2026-05-21
owner: eotel
related:
  upstream: https://github.com/jacob-bd/notebooklm-mcp-cli
  pypi: https://pypi.org/project/notebooklm-mcp-cli/
---

# Goal

`/blog` で公開した記事を入力に、**1 blog post = 1 NotebookLM notebook = 1 Japanese Audio Overview** の関係で
NotebookLM の音声解説（ポッドキャスト風ラジオ）を **日本語で** 自動生成し、ローカルに音声ファイルを保存して
blog 記事フロントマターから再生できるようにする skill / script を作る。

具体的な使い心地（理想形）:

```bash
/notebooklm-radio https://eotel.github.io/blogs/posts/2026/05/2026-05-21-some-slug/
# → 新規 NotebookLM notebook 作成（タイトル: "Eotel Blog: <記事タイトル>"）
# → 当該 URL を source として ingest (--wait)
# → 日本語の Audio Overview を生成 (--language ja)
# → static/audio/<slug>/overview.mp3 に保存
# → 記事フロントマターに audio_url を書き戻して PR
```

---

# Background & Discovery

最初に **PleasePrompto/notebooklm-mcp** を調査したが、これは MCP サーバー専用で
`create_notebook` が無く、`generate_audio` に `language` 引数も無いため
「空 notebook プール運用 + custom_prompt で日本語を祈る」という回りくどい設計が必要だった。

**jacob-bd/notebooklm-mcp-cli** に切り替えることで、構造的な制約がほぼ全て解消する。

## jacob-bd/notebooklm-mcp-cli の重要機能（v0.3.7+）

| 機能 | コマンド | 影響 |
|---|---|---|
| 真の CLI (`nlm`) を提供 | `pip install notebooklm-mcp-cli` で `nlm` バイナリ | **HTTP transport / JSON-RPC curl 不要**。Bash スクリプトから直接叩ける |
| Notebook 新規作成 | `nlm notebook create "Title"` | ✅ プール運用不要。1 blog : 1 notebook が素直に成立 |
| URL ソース投入 + 待機 | `nlm source add <nb> --url <url> --wait` | ✅ `--wait` で ingest 完了までブロック |
| **言語指定** | `nlm audio create <nb> --language ja --format deep_dive --confirm` | ✅ **BCP-47 で直接 ja を渡せる**（CHANGELOG 0.3.7、2026-02-22 追加、PR #59 @beausea） |
| 環境変数で既定言語 | `NOTEBOOKLM_HL=ja` | ✅ 永続的に既定を日本語に。`--language` で個別上書き可 |
| ポーリング | `nlm studio status <nb>` | ✅ artifact の生成進捗 |
| ダウンロード | `nlm download audio <nb> <artifact-id> --output <path>` | ✅ そのまま使える |
| Built-in pipeline | `nlm pipeline run <nb> ingest-and-podcast --url <url>` | 🟡 `services/pipeline.py` に `language` パラメータあり。要検証だが、これで Phase 1 が 1 コマンドになる可能性 |
| 認証 profile | `nlm login --profile blogs` | ✅ 個人 Google アカウントと分離可能 |
| 認証寿命 | cookies ~2-4 週、CSRF auto-refresh | ⚠️ 月 1 回程度 `nlm login` が必要 |
| Internal API 依存 | 公式 API ではない | ⚠️ Google 側の UI 変更で壊れる可能性。upstream に依存 |

## Audio 出力形式

- 形式: `deep_dive`（既定 / 2 ホスト対談）, `brief`, `critique`, `debate`
- 長さ: `short`, `default`, `long`
- 出力ファイル: 既定で MP3（download コマンドが `--output <path>` を受け付ける）
- 生成時間: 公式案内で 1-5 分

## NotebookLM 側の制約（変わらず）

- internal API ベースなので Google が UI を変えると壊れる
- 認証は cookie 抽出（ブラウザ起動 → ログイン → cookie 取得）
- セッション ~20 分、cookies ~2-4 週

---

# Constraints & Non-Goals

## Constraints

1. **日本語音声を確実に得る**: `nlm audio create --language ja` を必須化。さらに `NOTEBOOKLM_HL=ja` を `.envrc` でセットしてフォールバックを二重に
2. **1 source : 1 note**: skill 実行ごとに `nlm notebook create` で新規 notebook を作る。同じ post を 2 回回したら警告（既存 notebook を検索して再利用 or skip）
3. **Hugo 記事への紐づけ**: 生成された音声は `static/audio/<slug>/overview.mp3` に置き、記事フロントマターに `audio_url` を追記。partial で `<audio>` を自動レンダリング
4. **既存スキル群との整合**: `.claude/skills/blog/` と同じ Bash ルール（`&&` 不使用、`/tmp` 不使用、`.claude/temp/` 使用、`gh pr create` は `--body-file` 経由、変数代入とコマンドを同一行で繋がない）
5. **Codex 互換**: `.claude/skills/notebooklm-radio/` → `.codex/skills/notebooklm-radio` の symlink
6. **認証情報の隔離**: `nlm login --profile blogs` で blog 専用 profile を作り、ユーザー個人の作業用 NotebookLM と混ぜない

## Non-Goals

- 多言語対応（日本語固定。英語版が欲しくなったらフラグで切替可だが v1 ではしない）
- 音声編集・BGM 付加・章分割
- video / infographic / mindmap など他の studio artifact 生成
- NotebookLM の有料機能を前提とした機能（無料枠で完結）
- 認証の完全自動化（cookie 期限切れ時の `nlm login` 実行は人手）
- Audio Overview の品質スコアリング

---

# Plan of Work

## Phase 0 — 環境準備（1 回限り、人手）

- [ ] **0.1** `uv tool install notebooklm-mcp-cli`（既に uv が入っている前提。無ければ `pipx` フォールバック）
- [ ] **0.2** `nlm login --profile blogs` で Google ログイン（blog 専用 profile を分離）
- [ ] **0.3** `nlm login --check --profile blogs` で認証成功を確認
- [ ] **0.4** `nlm doctor` で installation / auth / browser を診断
- [ ] **0.5** `.envrc` に `export NOTEBOOKLM_HL=ja` を追加（リポジトリ直下、direnv 使用）。`.envrc` が無ければスクリプト側でも `NOTEBOOKLM_HL=ja` を明示
- [ ] **0.6** **検証**: 適当な既存 blog post 1 本で手動 1 周走らせ、`--language ja` が本当に日本語ホストの音声を返すか耳で確認。英語混じりだった場合の挙動を記録

## Phase 1 — シェルスクリプト本体

- [ ] **1.1** `scripts/notebooklm-radio.sh` を作成。引数:
  - `$1`: post URL（`https://eotel.github.io/blogs/posts/YYYY/MM/<slug>/`）または記事 md ファイルパス
  - `--format <deep_dive|brief|critique|debate>` 既定 `deep_dive`
  - `--length <short|default|long>` 既定 `default`
  - `--dry-run`（API は叩かず、対応する notebook タイトル / 出力先パスだけ表示）
- [ ] **1.2** post URL から slug を抽出し、対応する md ファイルを特定 → `title` フロントマター値を取得
- [ ] **1.3** **重複ガード**: `nlm notebook list --json` で `"Eotel Blog: <title>"` 名の notebook が既にあれば、`--force` 指定が無い限り中止
- [ ] **1.4** `nlm notebook create "Eotel Blog: <title>" --profile blogs` → JSON で notebook_id をパース
- [ ] **1.5** `nlm source add <notebook_id> --url <post-url> --wait --profile blogs`
  - ingest が失敗したケース（404 / クロール失敗）はここで検出して exit 3
- [ ] **1.6** `nlm audio create <notebook_id> --language ja --format <fmt> --length <len> --confirm --profile blogs`
  - 戻り値から artifact_id をパース
- [ ] **1.7** `nlm studio status <notebook_id> --profile blogs` を 30 秒間隔で最大 10 分ポーリング
  - 完了したら次へ、タイムアウトしたら exit 4
- [ ] **1.8** `mkdir -p static/audio/<slug>` してから
  `nlm download audio <notebook_id> <artifact_id> --output static/audio/<slug>/overview.mp3 --profile blogs`
- [ ] **1.9** （オプション）`nlm pipeline run <notebook_id> ingest-and-podcast --url <post-url> --language ja --audio-length default --confirm` が
  **1.4 + 1.5 + 1.6 を 1 コマンドにまとめる**経路として動くか実機検証。動けば実装をこちらに寄せる
- [ ] **1.10** 監査ログを `.claude/state/notebooklm-radio-runs.jsonl` に追記（slug, notebook_id, artifact_id, file_path, generated_at, profile, language）

## Phase 2 — Hugo 記事への紐付け

- [ ] **2.1** 該当記事 md のフロントマターに以下を追記（既存値は上書きしない）:
  ```yaml
  audio_url: /audio/<slug>/overview.mp3
  audio_lang: ja
  audio_generated_at: 2026-05-21T12:00:00+09:00
  audio_source: notebooklm
  audio_format: deep_dive
  ```
- [ ] **2.2** `layouts/partials/audio-player.html` を新規作成。`<audio controls preload="metadata">` で表示。再生位置 cookie などは不要
- [ ] **2.3** `layouts/_default/single.html`（PaperMod 上書き）に partial 呼び出しを追加。フロントマターに `audio_url` がある記事のみ表示（既存記事への影響ゼロを保証）
- [ ] **2.4** `hugo --gc` で build エラーが出ないこと、audio_url を持たない既存 783 件で何も変わらないことを確認

## Phase 3 — Skill 化

- [ ] **3.1** `.claude/skills/notebooklm-radio/SKILL.md` を作成。trigger: `/notebooklm-radio <post-url-or-slug>`
- [ ] **3.2** Skill は `scripts/notebooklm-radio.sh` を呼ぶ薄いラッパー + 失敗時のリトライ案内
- [ ] **3.3** `.codex/skills/notebooklm-radio` → `.claude/skills/notebooklm-radio` の symlink を張る（既存 `.codex/agents/` と同じパターン）
- [ ] **3.4** CLAUDE.md の「## カスタムエージェント」近くに「## 音声化スキル」セクションを追加し、運用ルール（言語、profile 分離、cookie 期限切れの兆候）を書く

## Phase 4 — `/blog` との接続（v1 では手動）

- [ ] **4.1** `/blog` PR マージ後に自動で `/notebooklm-radio` を回すかを決定 → **v1 では手動**（cookie 期限切れや NotebookLM 側障害で blog 投稿フロー全体が止まるリスクを避ける）
- [ ] **4.2** `/blog` SKILL.md に「記事公開後の音声化は `/notebooklm-radio <url>` を手動で」と注記
- [ ] **4.3** 将来の自動化のために、`scripts/blog-batch.sh` と同じ命名規則で `scripts/notebooklm-radio-batch.sh`（未実装、v2）の名前を予約しておく

---

# Verification

- **手動 golden path**: 既存 blog 1 本に対して `/notebooklm-radio` → static/audio/<slug>/overview.mp3 が生成 → ブラウザで記事を開いて再生 → 日本語の deep_dive 音声が流れる
- **重複防止**: 同じ post で 2 回実行 → 2 回目は中止（`--force` で上書きできること）
- **失敗系 - ingest**: 存在しない URL を渡した場合 exit 3 + notebook は残骸を残さず削除（or 明示的に「削除してね」と案内）
- **失敗系 - timeout**: studio status が 10 分待っても ready にならない → exit 4 + artifact_id をログに残す
- **失敗系 - 認証切れ**: cookie 期限切れ状態で実行 → `nlm doctor` 由来のエラーメッセージを ユーザーに伝達 + `nlm login --profile blogs` の案内
- **言語検証**: `--language ja` を **わざと外して** 実行し、英語が出ることを確認 → ja 指定の効果を逆向きに保証
- **Hugo build**: `hugo --gc` でエラーなく build。audio_url ありの記事と無い記事が混在しても問題なし
- **既存記事への非破壊**: 783 件の hdknr 由来記事は touch しない（diff で frontmatter が変更されないこと）

---

# Decision Log

- **D-001 (2026-05-21)**: notebooklm 連携には **jacob-bd/notebooklm-mcp-cli** を採用。PleasePrompto/notebooklm-mcp は `create_notebook` / `language` 引数が無いため不採用
- **D-002 (2026-05-21)**: 認証 profile は **`blogs`** で分離。デフォルト profile を blog 用にすると個人作業時に混乱するため
- **D-003 (2026-05-21)**: 音声ファイル置き場は `static/audio/<slug>/`（Hugo image processing 対象外）。`assets/` は image processing 専用に空ける
- **D-004 (2026-05-21)**: `/blog` と `/notebooklm-radio` は **自動連携しない**（v1）。NotebookLM 側障害が blog 公開を止めないため
- **D-005 (2026-05-21)**: pipeline 経路（`nlm pipeline run ingest-and-podcast`）は Phase 1 で実機検証してから採用判断。`--language ja` を pipeline params に渡せるかが分岐点
- **D-006 (2026-05-21)**: 音声形式の既定は **`deep_dive`**（2 ホスト対談、NotebookLM の象徴的フォーマット）。CLI 引数で他に切替可

---

# Risks & Open Questions

- **R-001**: NotebookLM が internal API なので Google 側の UI / endpoint 変更で全停止する可能性 → upstream に依存。回避策は「動かなくなったら手動で UI から生成して put」のドキュメントを書いておく
- **R-002**: cookie ~2-4 週で期限切れ → `nlm login --profile blogs` を月 1 で叩く運用。Skill 実行時に `nlm login --check` を先に走らせ、失敗時に明確な案内
- **R-003**: `--language ja` が UI 上の dropdown 経由ではなく BCP-47 hint しか送らない場合、Gemini 側で英語に引っ張られるケースが残る可能性 → Phase 0.6 で実機検証。ダメなら custom_prompt で「全編日本語で」と上書き
- **R-004**: 生成時間が長く 10 分を超えるケース → タイムアウトを 15 分に伸ばすか、`--length short` を試す
- **R-005**: 無料枠で 1 日あたりの audio 生成数に上限がある可能性 → 上限に当たったら `studio status` がエラーを返すはず。retry-after を尊重
- **Q-001**: `nlm pipeline run ingest-and-podcast` の引数体系は CLI ヘルプで確定したい。`pipeline.py` のソース上は `language` を受け取るが、CLI ラッパーが渡しているかは要確認
- **Q-002**: 音声ファイル拡張子は `.mp3` で良いか？ → `nlm download audio` が出力する形式を実機で確認。`.wav` の場合は静的配信のサイズ的に変換を挟むか検討
- **Q-003**: `notebook create` した notebook は NotebookLM の library に残り続ける → 月数十本溜まる。後始末（`nlm notebook delete --confirm`）を 30 日 retention で回すか手動か

---

# Progress

| Phase | Status | Notes |
|---|---|---|
| 0 — 環境準備 | partial | 0.1 (nlm 既存 v0.5.2) / 0.4 (doctor) / 0.5 (.envrc NOTEBOOKLM_HL=ja) 完了。**0.2 (`nlm login --profile blogs`) と 0.6 (実地音声検証) はユーザー手動** |
| 1 — シェルスクリプト | done | `scripts/notebooklm-radio.sh` + `scripts/notebooklm_radio_frontmatter.py`。dry-run で slug/title/URL 経路の双方を検証済み。1.9 (pipeline) は v0.5.2 で `--language` 非対応のため採用見送り (S-001) |
| 2 — Hugo 紐付け | done | `layouts/partials/audio-player.html` + `layouts/_default/single.html` 改修 + `assets/css/main.css` に `.audio-overview*` 追加。`hugo --gc` で 2495 pages build 確認 |
| 3 — Skill 化 | done | `.claude/skills/notebooklm-radio/SKILL.md` + `.codex/skills/notebooklm-radio` symlink。Claude Code 側のスキル一覧に登場 |
| 4 — `/blog` 接続 | done | CLAUDE.md に「## 音声化スキル」節を追加。自動連携は v1 では行わず手動 |

---

# Surprises & Discoveries

## S-001 (2026-05-21): v0.5.2 でのフラグ差分（plan 起草時の v0.3.7 想定からのズレ）

実機 `nlm --version` → **0.5.2**。plan 起草時に想定していた CLI 構文との差分を列挙する。

| 領域 | plan 記述 | v0.5.2 実機 | 対応 |
|---|---|---|---|
| `nlm audio create --language ja` | OK 想定 | ✅ `--language` フラグあり (BCP-47) | そのまま使用 |
| `nlm download audio` 既定拡張子 | `.mp3` 前提 | **`.m4a`** が既定 (`./{notebook_id}_audio.m4a`) | 出力先を `static/audio/<slug>/overview.m4a` に変更。audio タグの type も `audio/mp4` |
| `nlm pipeline run ingest-and-podcast --language ja` | 1.9 で検証予定 | **`--language` フラグ無し**。`--notebook -n` `--input-url -u` のみ受け付ける | Phase 1.9 は **採用見送り**。pipeline は言語固定できないため、3 ステップ手動経路で固定 |
| `nlm notebook create --json` | JSON でパース想定 | **`--json` フラグ無し**。`--profile -p` のみ | stdout パースに切替（typer の TTY 出力はリッチなので、`grep -oE '[a-f0-9-]{36}'` 等で UUID 抽出） |
| `nlm notebook list --json` | OK 想定 | ✅ `--json -j` あり | そのまま使用（重複ガード） |
| `nlm studio status <id> --json` | OK 想定 | ✅ `--json -j` `--full -a` あり | ポーリングは `nlm studio status <nb> --json` を parse |
| `nlm doctor` | Phase 0.4 で確認 | ✅ 実行可能 | 既に default profile が `miura@shaper.co.jp` で認証済を確認 |
| `nlm login --profile blogs` | Phase 0.2 で人手 | profile 未作成 → `Profile not found: blogs` | **未完了**: ユーザーが手動でブラウザログイン要 |

## S-003 (2026-05-21): `nlm download` は `--profile` を受け付けない (v0.5.2)

end-to-end 検証で発覚:

```
nlm download audio <nb> --output <path> --profile blogs
→ Error: No such option: --profile
```

`nlm download` サブコマンド群（audio / video / slide-deck / ...）は v0.5.2 で profile スコープを持たず、
**現在の default profile** をそのまま使う仕様。他の `notebook list` / `audio create` / `source add` 等は `--profile` を受けるのに、`download` だけ抜けている。

→ スクリプトでは download の前に `nlm login switch <profile>` で default を一時切替し、download 後に元に戻す形に修正。
`nlm config get auth.default_profile` で前の値を取得して復元する。

## S-004 (2026-05-21): PyYAML を非依存にするため uv の PEP 723 inline script で起動

devenv 由来の python3 にも homebrew python3 にも `pyyaml` が入っておらず、
`scripts/notebooklm_radio_frontmatter.py` の `import yaml` が失敗。

`pyproject.toml` には PyYAML が宣言されているが `.venv` が作られていない状態。
解決策として:

1. python script に PEP 723 inline metadata を埋め込む (`# /// script` ブロック + `dependencies = ["PyYAML>=6"]`)
2. shebang を `#!/usr/bin/env -S uv run --quiet --no-project --with PyYAML>=6 python3` に
3. shell script からの呼び出しを `uv run --quiet --no-project --with "PyYAML>=6" script.py ...` 経由に

これで `.venv` 構築や `pip install` 不要で frontmatter patch が動く。uv が無い環境用に `python3` フォールバックも残してある。

## S-005 (2026-05-21): `nlm studio status --json` は配列直返し、`tee` が exit code を消す

end-to-end 1 回目で 15 分タイムアウト。原因:

1. **jq クエリ**: `(.artifacts // .)` は `.artifacts` がエラーを raise したとき null フォールバックしない（`//` は null/false 用）。配列直返しを想定して `if type == "array" then . else (.artifacts // []) end` に修正
2. **tee による exit code 消失**: `script.sh 2>&1 | tee log` のように `tee` を後段に置くと、`set -euo pipefail` でも `tee` の exit code (0) が外に出る。コマンド単体の exit を見たい場合は `${PIPESTATUS[0]}` を使うか、`tee` を内側にせず `script.sh > >(tee log) 2>&1` のような書き方にする

修正後の jq クエリで artifact_id="f0ab4602-..." status="completed" を抽出できることを実機で確認した。

## S-002 (2026-05-21): default profile の cookie がもう怪しい

`nlm doctor` は "Cookies: present (42 cookies)" と返すが、`nlm notebook list` を叩くと
`Authentication Error: Authentication expired` で弾かれた。doctor の health check は CSRF / cookie 存在を見るだけで、
実際の API 叩きまではしていない様子。

→ Skill 側のヘルスチェックは「`nlm login --check --profile blogs` の exit code」ではなく
「`nlm notebook list --profile blogs --json` を実際に 1 回叩いて非エラーを確認」する方が信頼できる。
このロジックを `scripts/notebooklm-radio.sh` の preflight に組み込む。

---

# Outcomes & Retrospective

## 2026-05-21: auto-mode による Phase 1–4 完了

**コードレベルの成果物**

- `scripts/notebooklm-radio.sh` (Bash, 実行可) — preflight → 重複ガード → notebook create → source add --wait → audio create --language ja → studio status poll (15 min) → download → frontmatter patch → audit log
- `scripts/notebooklm_radio_frontmatter.py` (Python + pyyaml) — 既存値を上書きしない frontmatter merger
- `layouts/partials/audio-player.html` — `audio_url` がある記事のみ `<audio controls>` を出すガード付き partial
- `layouts/_default/single.html` — partial 呼び出しを `post-meta` 直下、ToC より上に挿入（聴きながら skim 読みできる位置）
- `assets/css/main.css` — `.audio-overview` 周りの最小 CSS（バッジ・メタ行・幅 100% プレイヤー）
- `.claude/skills/notebooklm-radio/SKILL.md` + `.codex/skills/notebooklm-radio` symlink
- `.envrc` に `export NOTEBOOKLM_HL=ja` (要 `direnv allow`)
- `CLAUDE.md` 「## 音声化スキル」節

**検証済み**

- `hugo --gc` で 2495 pages がエラーなく build。audio_url を持たない既存 783 件は出力に変化なし（partial が `with` ガードで no-op になる）
- `scripts/notebooklm-radio.sh ... --dry-run` を URL 経路 / md 経路の双方で実行し、slug / title / notebook_title / 出力パスが一致

**未完了（ユーザー手動）**

- Phase 0.2: `nlm login --profile blogs`（ブラウザ Google ログイン）— **完了 (2026-05-21)**
- Phase 0.6: `--language ja` が実際に日本語ホストの音声を返すか耳で確認 — **要確認**（音声は生成済み: `static/audio/2026-05-08-agent-friendly-cli-for-llm/overview.m4a` 11MB / MPEG-4）
- Phase 2 系の本番検証: 任意の既存 post 1 本で end-to-end を回す — **完了 (2026-05-21)**: `agent-friendly-cli-for-llm` post で notebook 25e5a2f7-... 作成 → ingest → 日本語短尺音声生成 → m4a download → frontmatter patch → hugo build まで通った

**実機で見つかったバグと修正**

| バグ | 兆候 | 修正 |
|---|---|---|
| jq クエリが top-level array に対応していない | poll: artifact= status= が 30 回連続後 timeout | `if type == "array" then . else (.artifacts // []) end` に変更 |
| `nlm download audio` が `--profile` を受け付けない | `No such option: --profile` (S-003) | download 前後で `nlm login switch` を使って default profile を一時切替 |
| `python3` で `import yaml` 失敗 (S-004) | venv 未作成 | PEP 723 inline metadata + `uv run --no-project --with PyYAML>=6` |
| `tee` が exit code を吸収 (S-005) | 15 分タイムアウトしたのに exit 0 | この session では再現のみ。`PIPESTATUS` ベースの修正は follow-up へ |

**判断記録**

- D-005 (pipeline 経路) は v0.5.2 で `nlm pipeline run` が `--language` を受け取らないことが判明したため **採用見送り** (S-001 参照)。3 ステップ手動経路で固定
- D-003 (静的配信先) は当初の plan 通り `static/audio/<slug>/`。ただし拡張子は **`.m4a`**（NotebookLM の既定出力に合わせる）
- 認証ヘルスチェックは `nlm doctor` ではなく `nlm notebook list --json` を実際に叩く方式に修正 (S-002)

---

# Follow-ups (post-completion candidates)

- `/blog` フローへの自動連携（cookie 健康チェックをガードに）
- 1 日 N 本までの quota guard を skill 側で持つ
- 音声を S3 等に外部 hosting して repo サイズを抑える（GitHub Pages の 1GB 制限対策）
- 古い notebook の自動 retention（30 日経過で `nlm notebook delete`）
- 多言語対応（英語版・中国語版を別 frontmatter に持つ）
- `nlm video create --language ja` で動画解説版（実験）

---

# 2026-05-21 追加スコープ: GitHub Release Assets への移行

GitHub Pages の repo 1GB / 帯域 100GB 制限を回避するため、m4a をリポジトリ同梱から
GitHub Release Assets (rolling tag `audio`) に移行した。

## 構成

- 単一 release tag `audio` (https://github.com/Eotel/blogs/releases/tag/audio)
- アセット名: `<slug>.m4a` (1 post = 1 asset, `--clobber` で上書き可)
- URL: `https://github.com/Eotel/blogs/releases/download/audio/<slug>.m4a`
- ローカル cache: `static/audio/<slug>/overview.m4a` (`.gitignore` 済)
- 環境変数で repo / tag を上書き可: `NOTEBOOKLM_RADIO_REPO` / `NOTEBOOKLM_RADIO_RELEASE_TAG`

## script 上の変更

- `AUDIO_URL_PATH="/audio/$SLUG/overview.m4a"` → `AUDIO_URL="https://github.com/$GH_REPO/releases/download/$RELEASE_TAG/$ASSET_NAME"`
- Step 5b として `gh release upload "$RELEASE_TAG" "$STAGE/$ASSET_NAME" --clobber --repo "$GH_REPO"` を挿入
- 失敗時はローカル cache を残してリトライ案内
- audit log に `release_url` フィールド追加

## 既存 5 件のマイグレーション (2026-05-21)

```
2026-05-08-agent-friendly-cli-for-llm.m4a       10M
2026-05-18-minna-de-tsukuru-future-undokai.m4a  22M
2026-05-20-hexagonal-architecture-practical-guide.m4a  34M
2026-05-21-enzo-mari-autoprogettazione.m4a      14M
2026-05-21-knowledge-pipeline-over-harness.m4a  36M
```

すべて release `audio` に upload 済、frontmatter の audio_url も release URL に書き換え済。
ローカル `static/audio/` は削除 + `.gitignore` 追加。

## 注意点

- **`gh release delete audio` は厳禁** — 全 post の音声リンクが切れる
- release ページに 1 つだけ表示される (`--latest=false` を指定したので「最新リリース」プレビューから除外)
- repo を fork した人は自分の `<fork>/releases/tag/audio` を作る必要あり (環境変数で切替可)

---

# 2026-05-21 追加スコープ: TUI ピッカー

ユーザー要望「post を絞り込んで言語/長さ/focus を選べる simple な CLI/TUI が欲しい」を受けて、fzf ベースの対話ツールを追加した。

## 成果物

- `scripts/notebooklm-radio-tui.sh` — fzf 単独で完結する対話 TUI
- `scripts/notebooklm-radio.sh` に `--language <bcp-47>` / `--focus <topic>` フラグを増設
- `audio create --focus` パラメータを v0.5.2 で確認済み（NotebookLM 側の生成プロンプトに反映される）

## TUI のフロー

1. `find content/posts/**/*.md` → frontmatter から date / title / audio_url 有無を抜く index を構築（717 件、~1秒）
2. 日付降順で fzf 起動。`★` カラムで既に audio がある post を一目で識別。preview pane に先頭 40 行
3. 言語 / 長さ / 形式の 3 つは fzf の単純リストピッカーで選択（default を先頭に置いて Enter 即決定可能）
4. focus は `read -r -e` の free-form 入力（空 Enter で省略）
5. 内容を表示して `y/N` 確認
6. `exec ./scripts/notebooklm-radio.sh ... --language ... --focus ... [--force]`

## 設計判断

- **Go ではなく bash + fzf**: プロジェクト全体が bash スクリプトで統一されているのと、コンパイル不要で iterate しやすいため。fzf 単体で post 検索・選択肢ピッカーの両方を兼ねるので外部依存は fzf のみ
- **gum は使わない**: 未インストール。fzf の `--header` / `--prompt` だけで十分視認性は出る
- **★ 検出**: frontmatter の `audio_url:` 行を grep するだけ。Hugo build せずに済む
- **再生成は明示的に確認**: ★ 付き post を選んだ瞬間「再生成しますか?」を出し、yes なら `--force` を自動付与

## 既知の細かい改善余地（follow-up）

- index 構築をキャッシュ化（ファイルの mtime を見てインクリメンタル更新）
- fzf の preview pane で `bat` があれば syntax highlight
- 多選択モード（複数 post を batch で audio 化）
- focus を fzf で過去入力から呼び出す（`.claude/state/notebooklm-radio-runs.jsonl` の focus フィールドを source に）
