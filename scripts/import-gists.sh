#!/bin/bash
# Import public gists as Hugo blog posts (multi-author, opt-in by filename).
#
# Opt-in convention:
#   Only files named `*.blog.md` inside a public gist are imported. This lets
#   you keep private notes (`notes.md`, `journal.md`, etc.) in your gist
#   account without risk of them being published. Within one gist, multiple
#   `*.blog.md` files become multiple posts (slug = <gist_id>-<basename>).
#
# Usage:
#   ./scripts/import-gists.sh                # all authors with gist_import:true in authors.json
#   ./scripts/import-gists.sh <author_id>    # single author (id from authors.json)
#   ./scripts/import-gists.sh --all          # iterate every author regardless of gist_import flag
#
# Notes:
#   - Each post's frontmatter records `author: <id>` so themes can render attribution.
#   - Calls the public `users/<login>/gists` endpoint (no token-private gists).

set -euo pipefail

BLOG_DIR="$(cd "$(dirname "$0")/.." && pwd)"
POSTS_DIR="$BLOG_DIR/content/posts"
CACHE_DIR="$BLOG_DIR/.gist-cache"
AUTHORS_FILE="$BLOG_DIR/scripts/authors.json"

mkdir -p "$POSTS_DIR" "$CACHE_DIR"

if [ ! -f "$AUTHORS_FILE" ]; then
    echo "ERROR: authors config not found: $AUTHORS_FILE" >&2
    exit 1
fi

# Resolve which authors to crawl based on argv.
ARG="${1:-}"
case "$ARG" in
    --all)
        AUTHOR_IDS=$(jq -r '.authors[].id' "$AUTHORS_FILE")
        ;;
    "")
        AUTHOR_IDS=$(jq -r '.authors[] | select(.gist_import == true) | .id' "$AUTHORS_FILE")
        ;;
    *)
        AUTHOR_IDS=$(jq -r --arg id "$ARG" '.authors[] | select(.id == $id) | .id' "$AUTHORS_FILE")
        if [ -z "$AUTHOR_IDS" ]; then
            echo "ERROR: author id '$ARG' not found in $AUTHORS_FILE" >&2
            exit 1
        fi
        ;;
esac

if [ -z "$AUTHOR_IDS" ]; then
    echo "No authors selected for crawl. Set gist_import:true in authors.json or pass an author id."
    exit 0
fi

GRAND_TOTAL=0
GRAND_IMPORTED=0
GRAND_SKIPPED=0

while IFS= read -r AUTHOR_ID; do
    [ -z "$AUTHOR_ID" ] && continue

    GH_LOGIN=$(jq -r --arg id "$AUTHOR_ID" '.authors[] | select(.id == $id) | .github_login' "$AUTHORS_FILE")
    if [ -z "$GH_LOGIN" ] || [ "$GH_LOGIN" = "null" ]; then
        echo "WARN: github_login missing for author '$AUTHOR_ID', skipping" >&2
        continue
    fi

    echo ""
    echo "=== Author: ${AUTHOR_ID} (github: ${GH_LOGIN}) ==="

    CACHE_FILE="$CACHE_DIR/gists-${AUTHOR_ID}.jsonl"

    echo "Fetching gist metadata..."
    gh api "users/${GH_LOGIN}/gists" --paginate \
        --jq '.[] | select(.public==true) | {id: .id, owner_login: .owner.login, description: .description, created_at: .created_at, updated_at: .updated_at, files: [.files | to_entries[] | {name: .key, raw_url: .value.raw_url, language: .value.language}]}' \
        > "$CACHE_FILE"

    TOTAL=$(wc -l < "$CACHE_FILE" | tr -d ' ')
    echo "Found ${TOTAL} public gists for ${GH_LOGIN}"
    GRAND_TOTAL=$((GRAND_TOTAL + TOTAL))

    COUNT=0
    SKIPPED=0
    IMPORTED=0

    while IFS= read -r gist_json; do
        COUNT=$((COUNT + 1))

        GIST_ID=$(echo "$gist_json" | jq -r '.id')
        OWNER_LOGIN=$(echo "$gist_json" | jq -r '.owner_login // empty')
        if [ -z "$OWNER_LOGIN" ] || [ "$OWNER_LOGIN" = "null" ]; then
            OWNER_LOGIN="$GH_LOGIN"
        fi
        DESCRIPTION=$(echo "$gist_json" | jq -r '.description // ""')
        CREATED=$(echo "$gist_json" | jq -r '.created_at')
        UPDATED=$(echo "$gist_json" | jq -r '.updated_at')

        # Pick only *.blog.md files (opt-in marker for publishable gist files).
        BLOG_FILES_JSON=$(echo "$gist_json" | jq -c '[.files[] | select(.name | test("\\.blog\\.md$"))]')
        NUM_BLOG_FILES=$(echo "$BLOG_FILES_JSON" | jq 'length')

        if [[ "$NUM_BLOG_FILES" -eq 0 ]]; then
            SKIPPED=$((SKIPPED + 1))
            continue
        fi

        DATE=$(echo "$CREATED" | cut -c1-10)
        YEAR=$(echo "$DATE" | cut -c1-4)
        MONTH=$(echo "$DATE" | cut -c6-7)
        POST_SUBDIR="$POSTS_DIR/$YEAR/$MONTH"
        mkdir -p "$POST_SUBDIR"

        for j in $(seq 0 $((NUM_BLOG_FILES - 1))); do
            FILE_JSON=$(echo "$BLOG_FILES_JSON" | jq -c ".[$j]")
            FILENAME=$(echo "$FILE_JSON" | jq -r '.name')
            RAW_URL=$(echo "$FILE_JSON" | jq -r '.raw_url')

            # Slug: <gist_id> if single .blog.md, else <gist_id>-<basename>
            BASE_NAME="${FILENAME%.blog.md}"
            if [[ "$NUM_BLOG_FILES" -eq 1 ]]; then
                SLUG="$GIST_ID"
            else
                SLUG="${GIST_ID}-${BASE_NAME}"
            fi
            POST_FILE="$POST_SUBDIR/${DATE}-${SLUG}.md"

            if [ -f "$POST_FILE" ]; then
                continue
            fi

            echo "[${COUNT}/${TOTAL}] Importing: ${DESCRIPTION} :: ${FILENAME}"

            CONTENT=$(curl -sL "$RAW_URL" 2>/dev/null || echo "")
            if [ -z "$CONTENT" ]; then
                echo "  WARN: Failed to download ${FILENAME}, skipping"
                continue
            fi

            # Title precedence: gist description > first heading in body > basename
            TITLE="$DESCRIPTION"
            if [ -z "$TITLE" ] || [ "$TITLE" = "$FILENAME" ]; then
                TITLE=$(echo "$CONTENT" | grep -m1 '^#' | sed 's/^#\+\s*//' || echo "$BASE_NAME")
            fi

            # Encode title as a JSON string (valid YAML, since YAML 1.2 ⊃ JSON).
            TITLE_YAML=$(jq -Rn --arg t "$TITLE" '$t')

            BODY="$CONTENT"
            FIRST_HEADING=$(echo "$CONTENT" | grep -m1 '^#' | sed 's/^#\+\s*//' || echo "")
            if [ -n "$FIRST_HEADING" ]; then
                BODY=$(echo "$CONTENT" | sed '0,/^#/{/^#/d;}')
            fi

            cat > "$POST_FILE" << FRONTMATTER
---
title: $TITLE_YAML
date: ${DATE}
lastmod: $(echo "$UPDATED" | cut -c1-10)
draft: false
author: "${AUTHOR_ID}"
gist_id: "${GIST_ID}"
gist_url: "https://gist.github.com/${OWNER_LOGIN}/${GIST_ID}"
gist_file: "${FILENAME}"
categories: []
tags: []
---

$BODY
FRONTMATTER

            IMPORTED=$((IMPORTED + 1))
        done
    done < "$CACHE_FILE"

    echo "  imported: ${IMPORTED}, non-markdown skipped: ${SKIPPED}"
    GRAND_IMPORTED=$((GRAND_IMPORTED + IMPORTED))
    GRAND_SKIPPED=$((GRAND_SKIPPED + SKIPPED))
done <<< "$AUTHOR_IDS"

echo ""
echo "=== Done ==="
echo "Total gists scanned: ${GRAND_TOTAL}"
echo "Posts imported:      ${GRAND_IMPORTED}"
echo "Non-markdown skipped: ${GRAND_SKIPPED}"
echo "Posts dir: ${POSTS_DIR}"
echo ""
echo "Next: python scripts/categorize.py"
