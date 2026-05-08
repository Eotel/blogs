#!/bin/bash
# setup-labels.sh — blog-batch.sh で使う GitHub Issue ラベルを作成する
#
# 1 度だけ実行すれば良い。既存ラベルがあれば skip する（idempotent）。
#
# Usage:
#   bash scripts/setup-labels.sh

set -euo pipefail

REPO="Eotel/blogs"

echo "=== Setting up labels for ${REPO} ==="

gh label create wip \
  --repo "$REPO" \
  --description "保留・調査中。blog-batch.sh から除外される" \
  --color "fbca04" \
  --force

echo "✅ done"
