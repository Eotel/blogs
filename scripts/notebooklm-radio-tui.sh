#!/bin/bash
# notebooklm-radio-tui.sh — fzf-based picker for NotebookLM audio generation.
#
# Walks the user through:
#   1. Select a blog post (fzf with preview; ★ marks posts that already have audio_url)
#   2. Pick language (BCP-47), length, format
#   3. Optionally type a focus prompt
#   4. Confirm and dispatch to scripts/notebooklm-radio.sh
#
# Usage:
#   ./scripts/notebooklm-radio-tui.sh

set -euo pipefail

BLOG_DIR="$(cd "$(dirname "$0")/.." && pwd)"
POSTS_DIR="$BLOG_DIR/content/posts"
RADIO_SH="$BLOG_DIR/scripts/notebooklm-radio.sh"

if ! command -v fzf >/dev/null 2>&1; then
    echo "ERROR: fzf required (brew install fzf)" >&2
    exit 1
fi
if [ ! -x "$RADIO_SH" ]; then
    echo "ERROR: $RADIO_SH not found or not executable" >&2
    exit 1
fi

# ---------------------------------------------------------------
# Build the post index (TAB-separated):
#   <date>\t<star>\t<slug>\t<title>\t<path>
# ---------------------------------------------------------------

# awk script body shared by both build paths. Reads pairs of (file, line) and
# emits one TSV row per file at the boundary. The "current file" state lives in
# the prev/date/title/audio variables; emit() flushes to stdout.
_INDEX_AWK='
    BEGIN { prev=""; date=""; title=""; audio=" " }
    function emit() {
        if (date == "") date="0000-00-00"
        if (title == "") title="(untitled)"
        n = split(prev, parts, "/")
        slug = parts[n]
        sub(/\.md$/, "", slug)
        printf "%s\t%s\t%s\t%s\t%s\n", date, audio, slug, title, prev
    }
    {
        if (file != prev) {
            if (prev != "") emit()
            prev = file
            date = ""; title = ""; audio = " "
        }
        if (content ~ /^date:/) {
            line = content
            sub(/^date:[[:space:]]*/, "", line)
            gsub(/["\047]/, "", line)
            sub(/[[:space:]].*$/, "", line)
            date = line
        } else if (content ~ /^title:/) {
            line = content
            sub(/^title:[[:space:]]*/, "", line)
            sub(/^["\047]/, "", line)
            sub(/["\047]$/, "", line)
            title = line
        } else if (content ~ /^audio_url:/) {
            audio = "\xe2\x98\x85"   # ★ U+2605
        }
    }
    END { if (prev != "") emit() }
'

build_index_rg() {
    # One rg process scans every post in parallel and emits `path\0line` per
    # matching frontmatter key. `--sort path` forces per-file grouping so a
    # single awk pass can flush whenever the path changes. We translate the NUL
    # separator to a TAB before awk because macOS BSD awk does not accept NUL
    # as a field separator (it silently splits on individual bytes instead).
    rg --no-heading --with-filename --no-line-number --null \
       --sort path \
       -g '*.md' \
       '^(date|title|audio_url):' \
       "$POSTS_DIR" \
    | tr '\0' '\t' \
    | awk -F'\t' '{ file=$1; content=$2 } '"$_INDEX_AWK"
}

build_index_awk() {
    # Fallback for environments without ripgrep. Forks one awk per file —
    # slower (~4s for 700 posts) but only stdlib.
    find "$POSTS_DIR" -name "*.md" -type f -print0 | while IFS= read -r -d '' md; do
        awk -v md="$md" '
            BEGIN { fm=0; date=""; title=""; audio=" " }
            /^---[[:space:]]*$/ { fm++; if (fm==2) exit; next }
            fm==1 {
                if ($0 ~ /^date:/) {
                    line=$0
                    sub(/^date:[[:space:]]*/, "", line)
                    gsub(/["\047]/, "", line)
                    sub(/[[:space:]].*$/, "", line)
                    date=line
                } else if ($0 ~ /^title:/) {
                    line=$0
                    sub(/^title:[[:space:]]*/, "", line)
                    sub(/^["\047]/, "", line)
                    sub(/["\047]$/, "", line)
                    title=line
                } else if ($0 ~ /^audio_url:/) {
                    audio="\xe2\x98\x85"
                }
            }
            END {
                if (date == "") date="0000-00-00"
                if (title == "") title="(untitled)"
                n = split(md, parts, "/")
                slug = parts[n]
                sub(/\.md$/, "", slug)
                printf "%s\t%s\t%s\t%s\t%s\n", date, audio, slug, title, md
            }
        ' "$md"
    done
}

build_index() {
    if command -v rg >/dev/null 2>&1; then
        build_index_rg
    else
        build_index_awk
    fi
}

# ---------------------------------------------------------------
# Stage 1: pick post
# ---------------------------------------------------------------

echo "==> blog post index を構築中..." >&2
INDEX=$(build_index | sort -r -t $'\t' -k1)
POST_COUNT=$(printf '%s\n' "$INDEX" | wc -l | tr -d ' ')
echo "    $POST_COUNT 件" >&2

SELECTED=$(printf '%s\n' "$INDEX" | fzf \
    --delimiter=$'\t' \
    --with-nth=1,2,4 \
    --preview="head -40 {5}" \
    --preview-window=right:55%:wrap \
    --bind="scroll-up:up,scroll-down:down,preview-scroll-up:preview-up,preview-scroll-down:preview-down" \
    --header="blog post を選択   ★=audio あり   ↑↓/wheel=移動 / typing=絞り込み / Enter=決定 / Esc=中止" \
    --prompt="post > " \
    --height=90% \
    --layout=reverse \
    --info=inline)

if [ -z "$SELECTED" ]; then
    echo "中止." >&2
    exit 0
fi

DATE=$(printf '%s' "$SELECTED" | awk -F'\t' '{print $1}')
STAR=$(printf '%s' "$SELECTED" | awk -F'\t' '{print $2}')
SLUG=$(printf '%s' "$SELECTED" | awk -F'\t' '{print $3}')
TITLE=$(printf '%s' "$SELECTED" | awk -F'\t' '{print $4}')
MD_PATH=$(printf '%s' "$SELECTED" | awk -F'\t' '{print $5}')

FORCE_ARGS=()
if [ "$STAR" = "★" ]; then
    echo ""
    echo "この post には既に audio_url が設定されています: $SLUG"
    read -r -p "再生成しますか? [y/N] " REGEN
    case "$REGEN" in
        y|Y|yes|YES) FORCE_ARGS+=(--force) ;;
        *) echo "中止."; exit 0 ;;
    esac
fi

# ---------------------------------------------------------------
# Stage 2-4: small fzf pickers for enum-typed options
# ---------------------------------------------------------------

pick_one() {
    local header="$1"
    local prompt="$2"
    local options="$3"
    printf '%s\n' "$options" | fzf \
        --header="$header" \
        --prompt="$prompt > " \
        --height=40% \
        --layout=reverse \
        --no-mouse \
        --info=inline
}

LANGUAGE=$(pick_one "audio 言語 (BCP-47)" "language" "ja
en
en-US
en-GB
zh-CN
ko
es
fr
de
pt-BR
it") || true
LANGUAGE=${LANGUAGE:-ja}

LENGTH=$(pick_one "audio 長さ" "length" "default
short
long") || true
LENGTH=${LENGTH:-default}

FORMAT=$(pick_one "audio 形式" "format" "deep_dive
brief
critique
debate") || true
FORMAT=${FORMAT:-deep_dive}

# ---------------------------------------------------------------
# Stage 5: free-form focus prompt
# ---------------------------------------------------------------

echo ""
echo "==> Focus prompt（ホストに伝える追加指示。空 Enter で省略）"
echo "    例: 「セキュリティ観点を強調」「初学者向けにかみくだいて」"
read -r -e -p "focus > " FOCUS

# ---------------------------------------------------------------
# Stage 6: confirm
# ---------------------------------------------------------------

echo ""
echo "==> 生成内容の確認"
printf '  post     : %s  %s\n' "$DATE" "$TITLE"
printf '  md       : %s\n' "$MD_PATH"
printf '  language : %s\n' "$LANGUAGE"
printf '  length   : %s\n' "$LENGTH"
printf '  format   : %s\n' "$FORMAT"
if [ -n "$FOCUS" ]; then
    printf '  focus    : %s\n' "$FOCUS"
fi
if [ ${#FORCE_ARGS[@]} -gt 0 ]; then
    printf '  flags    : --force (既存 audio を上書き)\n'
fi
echo ""
read -r -p "この内容で notebooklm-radio.sh を実行しますか? [y/N] " CONFIRM

case "$CONFIRM" in
    y|Y|yes|YES) ;;
    *) echo "中止."; exit 0 ;;
esac

# ---------------------------------------------------------------
# Stage 7: dispatch
# ---------------------------------------------------------------

ARGS=(
    "$MD_PATH"
    --format "$FORMAT"
    --length "$LENGTH"
    --language "$LANGUAGE"
)
if [ -n "$FOCUS" ]; then
    ARGS+=(--focus "$FOCUS")
fi
if [ ${#FORCE_ARGS[@]} -gt 0 ]; then
    ARGS+=("${FORCE_ARGS[@]}")
fi

exec "$RADIO_SH" "${ARGS[@]}"
