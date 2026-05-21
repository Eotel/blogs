#!/usr/bin/env bash
# htmltest.sh — Hugo を build してから htmltest で内部リンクを検証する。
#
# baseURL が https://eotel.github.io/blogs/ なので、href は "/blogs/..." 形式
# になる。htmltest は DirectoryPath をルートとみなして "/blogs/foo/" を
# "<root>/blogs/foo/" として解決するため、Hugo の出力を <root>/blogs/ に
# 配置してから走らせる。
#
# 使い方:
#   scripts/htmltest.sh                # full build + check
#   scripts/htmltest.sh --reuse        # 既存の build を流用 (高速)
#   scripts/htmltest.sh -- --log-level 1   # `--` 以降は htmltest にそのまま渡す
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

BUILD_ROOT=".claude/temp/htmltest"
BUILD_DEST="$BUILD_ROOT/blogs"
REUSE=0
HTMLTEST_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --reuse)
      REUSE=1
      shift
      ;;
    --)
      shift
      HTMLTEST_ARGS+=("$@")
      break
      ;;
    *)
      HTMLTEST_ARGS+=("$1")
      shift
      ;;
  esac
done

if ! command -v hugo >/dev/null 2>&1; then
  echo "error: hugo not on PATH (devenv shell に入っているか確認)" >&2
  exit 1
fi
if ! command -v htmltest >/dev/null 2>&1; then
  echo "error: htmltest not on PATH (devenv shell に入っているか確認)" >&2
  exit 1
fi

if [[ "$REUSE" -eq 0 || ! -d "$BUILD_DEST" ]]; then
  rm -rf "$BUILD_ROOT"
  mkdir -p "$BUILD_ROOT"
  echo "→ hugo --gc --destination $BUILD_DEST"
  hugo --gc --quiet --destination "$BUILD_DEST"
fi

echo "→ htmltest --conf .htmltest.yml ${HTMLTEST_ARGS[*]:-}"
exec htmltest --conf .htmltest.yml "${HTMLTEST_ARGS[@]}"
