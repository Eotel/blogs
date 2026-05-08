#!/bin/bash
# blog-batch.sh — open Issue を 1 topic = 1 記事として bulk で記事化する
#
# Usage:
#   ./scripts/blog-batch.sh [options]
#
# デフォルトでは `wip` ラベルが付いていない open Issue 全部を順次 /blog で記事化する。
# /blog が PR 本文に "Closes #N" を入れるので、PR マージで Issue は自動 close される。
#
# Options:
#   --label LABEL     対象ラベルで絞り込み（例: --label priority:high）
#   --milestone NAME  マイルストーンで絞り込み
#   --search QUERY    任意の gh issue list --search クエリ（--label/--milestone の上位互換）
#   --limit N         処理件数の上限（デフォルト: 全件）
#   --dry-run         対象一覧表示のみ（ブログ作成しない）
#   --skip-review     ファクトチェック・エージェントレビューを省略（高速化）
#   --model MODEL     使用モデル（デフォルト: sonnet）
#   --interval SECS   処理間のインターバル秒数（デフォルト: 5）
#   --overnight       夜間バッチモード（インターバル60秒 + skip-review 自動有効化）
#
# Examples:
#   ./scripts/blog-batch.sh --dry-run                       # 対象 Issue 一覧
#   ./scripts/blog-batch.sh --limit 3                       # 3件だけ処理
#   ./scripts/blog-batch.sh --label priority:high           # 高優先度のみ
#   ./scripts/blog-batch.sh --overnight                     # 全件夜間処理
#   nohup ./scripts/blog-batch.sh --overnight > .claude/temp/batch.log 2>&1 &

set -euo pipefail

BLOG_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO="Eotel/blogs"

# --- オプション解析 ---
LABEL=""
MILESTONE=""
SEARCH=""
LIMIT=0
DRY_RUN=false
SKIP_REVIEW=false
MODEL="sonnet"
INTERVAL=5
OVERNIGHT=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --label)        LABEL="$2"; shift 2 ;;
    --milestone)    MILESTONE="$2"; shift 2 ;;
    --search)       SEARCH="$2"; shift 2 ;;
    --limit)        LIMIT="$2"; shift 2 ;;
    --dry-run)      DRY_RUN=true; shift ;;
    --skip-review)  SKIP_REVIEW=true; shift ;;
    --model)        MODEL="$2"; shift 2 ;;
    --interval)     INTERVAL="$2"; shift 2 ;;
    --overnight)    OVERNIGHT=true; shift ;;
    -h|--help)
      sed -n '2,22p' "$0"
      exit 0
      ;;
    *)              echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# overnight モードのデフォルト
if [[ "$OVERNIGHT" == "true" ]]; then
  if [[ "$INTERVAL" -eq 5 ]]; then
    INTERVAL=60
  fi
  SKIP_REVIEW=true
fi

# --- 検索クエリ組み立て ---
# デフォルトは「wip ラベル除外 + open」。--search が明示指定されたらそれを優先
if [[ -n "$SEARCH" ]]; then
  QUERY="$SEARCH"
else
  QUERY="-label:wip"
  if [[ -n "$LABEL" ]]; then
    QUERY="${QUERY} label:${LABEL}"
  fi
  if [[ -n "$MILESTONE" ]]; then
    QUERY="${QUERY} milestone:\"${MILESTONE}\""
  fi
fi

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="${BLOG_DIR}/.claude/temp/blog-batch-${TIMESTAMP}.log"
REPORT_FILE="${BLOG_DIR}/.claude/temp/blog-batch-report-${TIMESTAMP}.md"

mkdir -p "${BLOG_DIR}/.claude/temp"

# --- 対象 Issue 取得 ---
echo "=== open Issue を取得中... ==="
echo "    検索クエリ: state:open ${QUERY}"

ISSUES_JSON=$(gh issue list --repo "$REPO" \
  --state open \
  --search "$QUERY" \
  --limit 1000 \
  --json number,title,url,labels)

TOTAL=$(echo "$ISSUES_JSON" | jq 'length')

if [[ "$TOTAL" -eq 0 ]]; then
  echo "✅ 対象 Issue はありません"
  exit 0
fi

echo "📋 対象 Issue: ${TOTAL} 件"

if [[ "$LIMIT" -gt 0 ]] && [[ "$LIMIT" -lt "$TOTAL" ]]; then
  PROCESS_COUNT="$LIMIT"
  echo "📌 処理上限: ${LIMIT} 件"
else
  PROCESS_COUNT="$TOTAL"
fi

# --- dry-run: 一覧表示 ---
if [[ "$DRY_RUN" == "true" ]]; then
  echo ""
  echo "=== 対象 Issue 一覧 ==="
  echo ""
  for i in $(seq 0 $((TOTAL - 1))); do
    ISSUE=$(echo "$ISSUES_JSON" | jq -r ".[$i]")
    NUMBER=$(echo "$ISSUE" | jq -r '.number')
    TITLE=$(echo "$ISSUE" | jq -r '.title')
    URL=$(echo "$ISSUE" | jq -r '.url')
    LABELS=$(echo "$ISSUE" | jq -r '[.labels[].name] | join(",")')
    echo "[$((i + 1))/${TOTAL}] #${NUMBER} ${TITLE}"
    echo "    ${URL}"
    [[ -n "$LABELS" ]] && echo "    labels: ${LABELS}"
    echo ""
  done
  echo "=== 記事化するには --dry-run を外して実行してください ==="
  exit 0
fi

# --- ブログ化処理 ---
SKIP_REVIEW_PROMPT=""
if [[ "$SKIP_REVIEW" == "true" ]]; then
  SKIP_REVIEW_PROMPT="ファクトチェックとエージェントレビュー（tech-writer, seo-advisor）は省略してください。"
fi

SUCCESS=0
FAILED=0
SKIPPED=0
declare -a PR_URLS=()
declare -a FAILED_ISSUES=()

# レポートヘッダー
cat > "$REPORT_FILE" <<HEADER
# Blog Batch Report

- **実行日時**: $(date '+%Y-%m-%d %H:%M:%S')
- **検索クエリ**: state:open ${QUERY}
- **対象件数**: ${PROCESS_COUNT} / ${TOTAL}
- **モデル**: ${MODEL}
- **インターバル**: ${INTERVAL}秒
- **レビュー省略**: ${SKIP_REVIEW}

## 処理結果

| # | Issue | ステータス | PR |
|---|-------|-----------|-----|
HEADER

echo ""
echo "=== ブログ化開始 (インターバル: ${INTERVAL}秒) ==="
echo "ログ: ${LOG_FILE}"
echo "レポート: ${REPORT_FILE}"
echo ""

for i in $(seq 0 $((PROCESS_COUNT - 1))); do
  if [[ "$i" -ge "$TOTAL" ]]; then
    break
  fi

  ISSUE=$(echo "$ISSUES_JSON" | jq -r ".[$i]")
  ISSUE_NUMBER=$(echo "$ISSUE" | jq -r '.number')
  ISSUE_TITLE=$(echo "$ISSUE" | jq -r '.title')
  ISSUE_URL=$(echo "$ISSUE" | jq -r '.url')
  NUM=$((i + 1))

  echo "[${NUM}/${PROCESS_COUNT}] $(date '+%H:%M:%S') #${ISSUE_NUMBER} ${ISSUE_TITLE}"
  echo "    ${ISSUE_URL}"

  # /blog に Issue URL を投げる。author 解決と Closes #N 付与は /blog skill 側の責務。
  PROMPT="/blog ${ISSUE_URL}"
  if [[ -n "$SKIP_REVIEW_PROMPT" ]]; then
    PROMPT="${PROMPT}

${SKIP_REVIEW_PROMPT}"
  fi

  RESULT_FILE="${BLOG_DIR}/.claude/temp/blog-batch-result-${ISSUE_NUMBER}.txt"
  STATUS=""
  PR_URL="-"

  if claude -p \
    --model "$MODEL" \
    --permission-mode acceptEdits \
    --max-budget-usd 2.00 \
    "$PROMPT" \
    > "$RESULT_FILE" 2>&1; then
    echo "    ✅ 成功"
    STATUS="✅ 成功"
    SUCCESS=$((SUCCESS + 1))

    # 結果から PR URL を抽出
    EXTRACTED_PR=$(grep -oE 'https://github.com/[^/]+/[^/]+/pull/[0-9]+' "$RESULT_FILE" | tail -1 || true)
    if [[ -n "$EXTRACTED_PR" ]]; then
      PR_URL="$EXTRACTED_PR"
      PR_URLS+=("$EXTRACTED_PR")
    fi
  else
    EXIT_CODE=$?
    if [[ $EXIT_CODE -eq 2 ]]; then
      echo "    ⏭️  スキップ（ブログ化不適と判断）"
      STATUS="⏭️ スキップ"
      SKIPPED=$((SKIPPED + 1))
    else
      echo "    ❌ 失敗 (exit code: ${EXIT_CODE})"
      STATUS="❌ 失敗 (exit ${EXIT_CODE})"
      FAILED=$((FAILED + 1))
      FAILED_ISSUES+=("$ISSUE_URL")
    fi
  fi

  # レポートに行追加
  echo "| ${NUM} | [#${ISSUE_NUMBER}](${ISSUE_URL}) ${ISSUE_TITLE} | ${STATUS} | ${PR_URL} |" >> "$REPORT_FILE"

  # 結果をログに追記
  echo "=== [${NUM}/${PROCESS_COUNT}] $(date '+%Y-%m-%d %H:%M:%S') #${ISSUE_NUMBER} ===" >> "$LOG_FILE"
  cat "$RESULT_FILE" >> "$LOG_FILE" 2>/dev/null
  echo "" >> "$LOG_FILE"
  rm -f "$RESULT_FILE"

  # インターバル（最後の1件では不要）
  if [[ $((i + 1)) -lt "$PROCESS_COUNT" ]] && [[ $((i + 1)) -lt "$TOTAL" ]]; then
    echo "    💤 ${INTERVAL}秒待機..."
    sleep "$INTERVAL"
  fi
done

# --- サマリー ---
SUMMARY="
## サマリー

- ✅ 成功: ${SUCCESS} 件
- ⏭️ スキップ: ${SKIPPED} 件
- ❌ 失敗: ${FAILED} 件
- 完了時刻: $(date '+%Y-%m-%d %H:%M:%S')
"

echo "$SUMMARY" >> "$REPORT_FILE"

# PR 一覧
if [[ ${#PR_URLS[@]} -gt 0 ]]; then
  echo "## 作成された PR（レビュー待ち）" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"
  for pr in "${PR_URLS[@]}"; do
    echo "- ${pr}" >> "$REPORT_FILE"
  done
  echo "" >> "$REPORT_FILE"
fi

# 失敗一覧
if [[ ${#FAILED_ISSUES[@]} -gt 0 ]]; then
  echo "## 失敗した Issue（要リトライ）" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"
  for url in "${FAILED_ISSUES[@]}"; do
    echo "- ${url}" >> "$REPORT_FILE"
  done
  echo "" >> "$REPORT_FILE"
fi

echo ""
echo "=== 完了 $(date '+%H:%M:%S') ==="
echo "✅ 成功: ${SUCCESS} 件"
echo "⏭️  スキップ: ${SKIPPED} 件"
echo "❌ 失敗: ${FAILED} 件"
echo "📄 ログ: ${LOG_FILE}"
echo "📊 レポート: ${REPORT_FILE}"

if [[ ${#PR_URLS[@]} -gt 0 ]]; then
  echo ""
  echo "📋 作成された PR:"
  for pr in "${PR_URLS[@]}"; do
    echo "  ${pr}"
  done
fi
