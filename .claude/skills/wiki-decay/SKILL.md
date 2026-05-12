---
name: wiki-decay
description: Wiki ページの `lastmod` を section 別の閾値で評価し、touch されずに古びた候補を浮かせる。refresh サブコマンドで wiki-fact-checker agent を起動して claim を再検証する
arguments:
  - name: subcommand
    description: "`report` (default) / `refresh <section>/<slug>` / `simulate --as-of YYYY-MM-DD`"
    required: false
---

Wiki の腐敗 (decay) を検出し、refresh フローに乗せます。**事実は時間で腐る** (バージョン番号 / API 仕様 / 解釈の変化) という前提で、wiki 全体を section 別の rate で評価します。

> NOTE: post の取り込み (`/wiki-ingest`) とは別レーン。`/wiki-ingest` は **新しい post → wiki** の流入を扱い、このスキルは **既存 wiki の老朽化** を扱います。

## サブコマンド

### `/wiki-decay` (= `/wiki-decay report`)

`python3 .claude/skills/wiki-decay/scripts/wiki_decay.py` を叩いて markdown レポートを stdout に出します。section ごとに `stale` / `warming` / `fresh` の数と、stale + warming の上位 N 件を列挙します。

引数:

| flag | 用途 |
|---|---|
| `--json` | machine-readable 出力 (CI / Issue 生成用) |
| `--top N` | section ごとに列挙する件数 (default 10) |
| `--as-of YYYY-MM-DD` | 評価基準日を上書き (将来日でリハーサル) |
| `--threshold-tools SOFT HARD` | tools/ の閾値を上書き (テスト用) |
| `--threshold-guides SOFT HARD` | guides/ |
| `--threshold-concepts SOFT HARD` | concepts/ |
| `--root PATH` | リポジトリルートを明示 |

### `/wiki-decay refresh <section>/<slug>`

指定 wiki ページに対して `wiki-fact-checker` subagent (Haiku 固定) を起動。claim 抽出 → 一次情報照合 → verdict JSON を返します。

verdict の中身に基づき親セッションが:

- `keep` のみ → ユーザー確認の上、`lastmod` だけ bump (false positive 救済)
- `update` / `remove` を含む → diff 案を提示し、ユーザーが Edit で修正する
- 修正後は `lastmod: <today>` を更新し、改めて `/wiki-decay` を回して fresh に戻ったことを確認

### `/wiki-decay simulate --as-of <date>`

`report --as-of <date>` のシンタックスシュガー。将来日で何が stale になるかを事前確認するための簡易シミュレーション。

## 閾値モデル

| Section | Soft warn | Hard stale | 根拠 |
|---|---|---|---|
| `tools/` | 45 d | **90 d** | バージョン・URL・価格の変動が速い |
| `guides/` | 75 d | **150 d** | 手順は drift するが tools ほどではない |
| `concepts/` | 150 d | **300 d** | 抽象概念は最も腐りにくい |

`score = clamp((age - soft) / (hard - soft), 0, 1)`。Issue は score desc / age desc 順で並ぶ。

閾値は `wiki_decay.py:DEFAULT_THRESHOLDS` に定数として固定。チューニングする場合はそこを編集。

## 週次 Issue 起票

`.github/workflows/wiki-decay-report.yml` が **毎週月曜 20:00 UTC** (火曜 05:00 JST) に cron で走り、

```bash
python3 .claude/skills/wiki-decay/scripts/wiki_decay.py --markdown --top 10 > /tmp/report.md
gh issue create --label wiki-decay --title "Wiki decay report (...)" --body-file /tmp/report.md
```

を実行する。`auto-wiki-ingest.yml` (土曜) とずらしてあるので衝突しない。

## frontmatter

**Phase 1–3 では新規フィールドなし。**`lastmod` だけで成立。

Phase 4 以降の opt-in 拡張余地:

- `next_review_at: YYYY-MM-DD` — section default を上書きする per-page review 日
- `review_cadence: tools` — section と別の tier を強制適用 (例: concepts に分類されているが実際は tool 依存度が高い page)

## 設計判断

- **lastmod 一本足**: 134 ページの backfill コストを 0 にするため、専用フィールドを追加しない。git が `lastmod` の真正性を保証する (Edit すれば自動で進む)
- **advisory only**: wiki-lint は pre-push / CI で blocking、decay は **時間依存のため非決定的** に振れる。CI を flap させない設計
- **issue lane (≠ auto PR)**: 自動 PR を出すと毎週 5–10 個の noise になる。Issue は 1 単位/週なので triage しやすい
- **wiki と post backlog の分離**: `wiki-ingest-backlog-*.md` は post 流入の管理、wiki-decay は内部老朽化の管理。混ぜない

## 開発・運用 Tips

- ロジックを変更する場合は `scripts/wiki_decay.py` を編集。SKILL.md は仕様の説明のみ
- 新しい section (例: `recipes/`) を足す場合は `DEFAULT_THRESHOLDS` に追加するだけ
- テスト: `uv run pytest .claude/skills/wiki-decay/scripts/test_wiki_decay.py`
- ローカルでの time-travel: `python3 .../wiki_decay.py --as-of 2026-12-01`
