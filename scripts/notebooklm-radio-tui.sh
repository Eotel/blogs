#!/bin/bash
# notebooklm-radio-tui.sh — fzf-based picker for NotebookLM audio generation.
#
# Walks the user through:
#   1. Select a blog post (fzf with preview; ★ marks posts that already have audio_url)
#   2. Pick language (BCP-47)
#   3. Pick length
#   4. Pick format
#   5. Optionally type a focus prompt
#   6. Confirm and dispatch to scripts/notebooklm-radio.sh
#
# Each stage past the first supports going back: Esc on an fzf picker, ":b"
# on the focus prompt, or "n" on the final confirm rewinds one step. Ctrl-C
# (or ":q" / "q") aborts the whole script.
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
# Stage helpers — each returns: 0=advance, 1=back, 2=abort.
# Globals listed in the "Sets:" comments are mutated in place so the
# step machine below can dispatch with positional/global state.
# ---------------------------------------------------------------

# Sets: DATE STAR SLUG TITLE MD_PATH FORCE_ARGS
# Going "back" from stage 2 lands here and re-shows the picker.
stage_select_post() {
    local selected
    selected=$(printf '%s\n' "$INDEX" | fzf \
        --delimiter=$'\t' \
        --with-nth=1,2,4 \
        --preview="head -40 {5}" \
        --preview-window=right:55%:wrap \
        --bind="scroll-up:up,scroll-down:down,preview-scroll-up:preview-up,preview-scroll-down:preview-down" \
        --header="blog post を選択   ★=audio あり   ↑↓/wheel=移動 / typing=絞り込み / Enter=決定 / Esc=中止" \
        --prompt="post > " \
        --height=90% \
        --layout=reverse \
        --info=inline) || return 2
    [ -z "$selected" ] && return 2

    DATE=$(printf '%s' "$selected" | awk -F'\t' '{print $1}')
    STAR=$(printf '%s' "$selected" | awk -F'\t' '{print $2}')
    SLUG=$(printf '%s' "$selected" | awk -F'\t' '{print $3}')
    TITLE=$(printf '%s' "$selected" | awk -F'\t' '{print $4}')
    MD_PATH=$(printf '%s' "$selected" | awk -F'\t' '{print $5}')

    FORCE_ARGS=()
    if [ "$STAR" = "★" ]; then
        echo ""
        echo "この post には既に audio_url が設定されています: $SLUG"
        local regen
        read -r -p "再生成しますか? [y]es / [n]o (post 選び直し) / [q]uit > " regen
        case "$regen" in
            y|Y|yes|YES) FORCE_ARGS+=(--force) ;;
            q|Q|quit|QUIT) return 2 ;;
            *) return 1 ;;  # re-display post picker
        esac
    fi
    return 0
}

# Generic single-select picker with Esc=back / Ctrl-C=abort.
# Args: var_name header prompt options default
#
# Implementation note: `--expect=esc` rebinds Esc from "abort" to
# "accept with key=esc" — fzf then prints "esc\n" as the first line of
# stdout, with the (empty) selection on the second line. Real abort
# (Ctrl-C / Ctrl-G) still produces exit code != 0.
stage_pick() {
    local var_name="$1" header="$2" prompt="$3" options="$4" default="$5"
    local out rc=0 key sel
    out=$(printf '%s\n' "$options" | fzf \
        --header="$header   Enter=決定 / Esc=戻る / Ctrl-C=中止" \
        --prompt="$prompt > " \
        --expect=esc \
        --height=40% \
        --layout=reverse \
        --no-mouse \
        --info=inline) || rc=$?
    if [ "$rc" -ne 0 ]; then
        return 2
    fi
    key=$(printf '%s\n' "$out" | sed -n '1p')
    sel=$(printf '%s\n' "$out" | sed -n '2p')
    if [ "$key" = "esc" ]; then
        return 1
    fi
    sel=${sel:-$default}
    printf -v "$var_name" '%s' "$sel"
    return 0
}

# Sets: FOCUS. ":b" → back, ":q" → abort, empty Enter → no focus.
stage_focus() {
    echo ""
    echo "==> Focus prompt（ホストに伝える追加指示）"
    echo "    例: 「セキュリティ観点を強調」「初学者向けにかみくだいて」"
    echo "    Enter=省略 / :b=戻る / :q=中止"
    read -r -e -p "focus > " FOCUS
    case "$FOCUS" in
        :b|:back) FOCUS=""; return 1 ;;
        :q|:quit) return 2 ;;
    esac
    return 0
}

# Final review. y → run, n/empty → back to focus, q → abort.
stage_confirm() {
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
    local ans
    read -r -p "[y]es 実行 / [n]o focus に戻る / [q]uit 中止 > " ans
    case "$ans" in
        y|Y|yes|YES) return 0 ;;
        q|Q|quit|QUIT) return 2 ;;
        *) return 1 ;;
    esac
}

# ---------------------------------------------------------------
# Build the index once
# ---------------------------------------------------------------

echo "==> blog post index を構築中..." >&2
INDEX=$(build_index | sort -r -t $'\t' -k1)
POST_COUNT=$(printf '%s\n' "$INDEX" | wc -l | tr -d ' ')
echo "    $POST_COUNT 件" >&2

# Mutable state filled in by stage_*
DATE=""
STAR=""
SLUG=""
TITLE=""
MD_PATH=""
LANGUAGE=""
LENGTH=""
FORMAT=""
FOCUS=""
FORCE_ARGS=()

LANG_OPTIONS="ja
en
en-US
en-GB
zh-CN
ko
es
fr
de
pt-BR
it"
LENGTH_OPTIONS="default
short
long"
FORMAT_OPTIONS="deep_dive
brief
critique
debate"

# ---------------------------------------------------------------
# Step machine — each stage may return: advance(0), back(1), abort(2)
# ---------------------------------------------------------------

abort() { echo "中止." >&2; exit 0; }

step=1
while true; do
    rc=0
    case "$step" in
        1) stage_select_post || rc=$?
           case "$rc" in 0) step=2 ;; 1) step=1 ;; 2) abort ;; esac ;;
        2) stage_pick LANGUAGE "audio 言語 (BCP-47)" "language" "$LANG_OPTIONS" "ja" || rc=$?
           case "$rc" in 0) step=3 ;; 1) step=1 ;; 2) abort ;; esac ;;
        3) stage_pick LENGTH "audio 長さ" "length" "$LENGTH_OPTIONS" "default" || rc=$?
           case "$rc" in 0) step=4 ;; 1) step=2 ;; 2) abort ;; esac ;;
        4) stage_pick FORMAT "audio 形式" "format" "$FORMAT_OPTIONS" "deep_dive" || rc=$?
           case "$rc" in 0) step=5 ;; 1) step=3 ;; 2) abort ;; esac ;;
        5) stage_focus || rc=$?
           case "$rc" in 0) step=6 ;; 1) step=4 ;; 2) abort ;; esac ;;
        6) stage_confirm || rc=$?
           case "$rc" in 0) break ;; 1) step=5 ;; 2) abort ;; esac ;;
    esac
done

# ---------------------------------------------------------------
# Dispatch
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
