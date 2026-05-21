#!/bin/bash
# notebooklm-radio.sh — Generate a Japanese NotebookLM Audio Overview for one blog post.
#
# Flow:
#   1. Resolve post URL or md path → slug → title
#   2. Preflight auth (real API call, not just doctor)
#   3. Duplicate guard (skip if "Eotel Blog: <title>" already exists, unless --force)
#   4. Create notebook → add URL source (--wait) → create JA audio → poll → download m4a
#   5. Patch frontmatter (audio_url / audio_lang / audio_generated_at / ...)
#   6. Append audit line to .claude/state/notebooklm-radio-runs.jsonl
#
# Usage:
#   scripts/notebooklm-radio.sh <post-url-or-md-path> [options]
#
# Options:
#   --format <deep_dive|brief|critique|debate>  default: deep_dive
#   --length <short|default|long>               default: default
#   --language <bcp-47>                         default: $NOTEBOOKLM_HL or "ja"
#   --focus <topic>                             optional steering prompt for the host
#   --source-mode <url|text>                    default: text (send local md body via --text;
#                                                              "url" crawls the deployed page)
#   --profile <name>                            default: blogs
#   --force                                     regenerate even if a matching notebook exists
#   --dry-run                                   resolve only (no API calls)
#
# Examples:
#   scripts/notebooklm-radio.sh https://eotel.github.io/blogs/posts/2026/05/2026-05-21-some-slug/
#   scripts/notebooklm-radio.sh content/posts/2026/05/2026-05-21-some-slug.md --length short

set -euo pipefail

BLOG_DIR="$(cd "$(dirname "$0")/.." && pwd)"
STATE_DIR="$BLOG_DIR/.claude/state"
AUDIT_LOG="$STATE_DIR/notebooklm-radio-runs.jsonl"
TEMP_DIR="$BLOG_DIR/.claude/temp"

FORMAT="deep_dive"
LENGTH="default"
LANGUAGE="${NOTEBOOKLM_HL:-ja}"
FOCUS=""
PROFILE="blogs"
SOURCE_MODE="text"
FORCE=0
DRY_RUN=0
POSITIONAL=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --format)       FORMAT="$2"; shift 2 ;;
        --length)       LENGTH="$2"; shift 2 ;;
        --language)     LANGUAGE="$2"; shift 2 ;;
        --focus)        FOCUS="$2"; shift 2 ;;
        --profile)      PROFILE="$2"; shift 2 ;;
        --source-mode)  SOURCE_MODE="$2"; shift 2 ;;
        --force)        FORCE=1; shift ;;
        --dry-run)      DRY_RUN=1; shift ;;
        -h|--help)
            sed -n '2,30p' "$0"
            exit 0
            ;;
        *)
            if [ -z "$POSITIONAL" ]; then
                POSITIONAL="$1"
            else
                echo "ERROR: unexpected extra argument: $1" >&2
                exit 2
            fi
            shift
            ;;
    esac
done

case "$SOURCE_MODE" in
    url|text) ;;
    *) echo "ERROR: --source-mode must be 'url' or 'text' (got: $SOURCE_MODE)" >&2; exit 2 ;;
esac

if [ -z "$POSITIONAL" ]; then
    echo "ERROR: post URL or md path required" >&2
    sed -n '12,21p' "$0" >&2
    exit 2
fi

# ---------------------------------------------------------------
# Resolve slug and md file from URL or path
# ---------------------------------------------------------------

INPUT="$POSITIONAL"
MD_FILE=""
SLUG=""
POST_URL=""

if [[ "$INPUT" == http://* || "$INPUT" == https://* ]]; then
    POST_URL="$INPUT"
    # URL like https://eotel.github.io/blogs/posts/YYYY/MM/<slug>/
    # Strip trailing slash, take last path segment.
    STRIPPED="${INPUT%/}"
    SLUG="${STRIPPED##*/}"
    # Derive YYYY/MM from URL path so we don't have to glob.
    if [[ "$STRIPPED" =~ /posts/([0-9]{4})/([0-9]{2})/ ]]; then
        YEAR="${BASH_REMATCH[1]}"
        MONTH="${BASH_REMATCH[2]}"
        MD_FILE="$BLOG_DIR/content/posts/$YEAR/$MONTH/$SLUG.md"
    else
        # Fallback: glob for the slug under content/posts/*/*/
        MD_CANDIDATES=$(find "$BLOG_DIR/content/posts" -name "$SLUG.md" -type f)
        if [ -z "$MD_CANDIDATES" ]; then
            echo "ERROR: could not locate md file for slug: $SLUG" >&2
            exit 3
        fi
        MD_FILE=$(echo "$MD_CANDIDATES" | head -1)
    fi
else
    # Treat as filesystem path (absolute or relative to repo root)
    if [[ "$INPUT" == /* ]]; then
        MD_FILE="$INPUT"
    else
        MD_FILE="$BLOG_DIR/$INPUT"
    fi
    SLUG=$(basename "$MD_FILE" .md)
    # Construct canonical post URL from path so we have something to feed NotebookLM
    REL_PATH="${MD_FILE#$BLOG_DIR/content/}"
    PATH_NO_EXT="${REL_PATH%.md}"
    POST_URL="https://eotel.github.io/blogs/${PATH_NO_EXT%/$SLUG}/$SLUG/"
fi

if [ ! -f "$MD_FILE" ]; then
    echo "ERROR: md file not found: $MD_FILE" >&2
    exit 3
fi

# Extract title from YAML frontmatter (first `title:` line in the leading --- block).
# Strip surrounding single or double quotes (yaml.safe_dump may rewrite with single).
TITLE=$(awk 'BEGIN{fm=0} /^---$/{fm++; if(fm==2) exit; next} fm==1 && /^title:/{sub(/^title:[[:space:]]*/, ""); gsub(/^["\x27]|["\x27]$/, ""); print; exit}' "$MD_FILE")

if [ -z "$TITLE" ]; then
    echo "ERROR: could not extract title from $MD_FILE" >&2
    exit 3
fi

NOTEBOOK_TITLE="Eotel Blog: $TITLE"

# Local cache lives under static/audio/ (gitignored). The canonical URL is the
# GitHub Release Asset published under the `audio` tag.
AUDIO_OUT_DIR="$BLOG_DIR/static/audio/$SLUG"
AUDIO_OUT_PATH="$AUDIO_OUT_DIR/overview.m4a"
RELEASE_TAG="${NOTEBOOKLM_RADIO_RELEASE_TAG:-audio}"
GH_REPO="${NOTEBOOKLM_RADIO_REPO:-Eotel/blogs}"
ASSET_NAME="$SLUG.m4a"
AUDIO_URL="https://github.com/$GH_REPO/releases/download/$RELEASE_TAG/$ASSET_NAME"

echo "[notebooklm-radio] slug:           $SLUG"
echo "[notebooklm-radio] md:             $MD_FILE"
echo "[notebooklm-radio] post URL:       $POST_URL"
echo "[notebooklm-radio] title:          $TITLE"
echo "[notebooklm-radio] notebook title: $NOTEBOOK_TITLE"
echo "[notebooklm-radio] local cache:    $AUDIO_OUT_PATH"
echo "[notebooklm-radio] release asset:  $AUDIO_URL"
echo "[notebooklm-radio] format/length:  $FORMAT / $LENGTH"
echo "[notebooklm-radio] language:       $LANGUAGE"
echo "[notebooklm-radio] source mode:    $SOURCE_MODE"
if [ -n "$FOCUS" ]; then
    echo "[notebooklm-radio] focus:          $FOCUS"
fi
echo "[notebooklm-radio] profile:        $PROFILE"

if [ "$DRY_RUN" -eq 1 ]; then
    echo "[notebooklm-radio] dry-run: stopping before any API call"
    exit 0
fi

# ---------------------------------------------------------------
# Preflight: real auth check + tool availability
# ---------------------------------------------------------------

if ! command -v nlm >/dev/null 2>&1; then
    echo "ERROR: nlm CLI not found. Install with: uv tool install notebooklm-mcp-cli" >&2
    exit 5
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "ERROR: jq required but not found" >&2
    exit 5
fi

mkdir -p "$STATE_DIR" "$TEMP_DIR"

PREFLIGHT_OUT="$TEMP_DIR/notebooklm-preflight-$$.json"
if ! nlm notebook list --profile "$PROFILE" --json >"$PREFLIGHT_OUT" 2>&1; then
    echo "ERROR: auth preflight failed for profile '$PROFILE'." >&2
    echo "  Try: nlm login --profile $PROFILE" >&2
    cat "$PREFLIGHT_OUT" >&2
    rm -f "$PREFLIGHT_OUT"
    exit 6
fi

# ---------------------------------------------------------------
# Duplicate guard
# ---------------------------------------------------------------

EXISTING_ID=$(jq -r --arg t "$NOTEBOOK_TITLE" '.[]? | select(.title == $t) | .id' "$PREFLIGHT_OUT" | head -1)
rm -f "$PREFLIGHT_OUT"

REUSE_EXISTING=0
if [ -n "$EXISTING_ID" ] && [ "$FORCE" -ne 1 ]; then
    echo "[notebooklm-radio] notebook already exists: $EXISTING_ID"
    # Check if a completed audio artifact is already there. If so, reuse it
    # (download + upload + patch) instead of failing — covers the common case
    # of a previous run that died mid-way (e.g. parallel-session race).
    EXISTING_ARTIFACT=$(nlm studio status "$EXISTING_ID" --json --profile "$PROFILE" 2>/dev/null \
        | jq -r '
            (if type == "array" then . else (.artifacts // []) end) as $arts
            | ($arts | map(select((.type // "") == "audio" and ((.status // "") | ascii_downcase | test("completed|ready|done")))))
            | sort_by(.created_at // .createdAt // "")
            | (last // {})
            | .id // ""
        ' 2>/dev/null || echo "")

    if [ -n "$EXISTING_ARTIFACT" ]; then
        echo "[notebooklm-radio] reusing existing notebook (completed audio: $EXISTING_ARTIFACT)"
        echo "[notebooklm-radio] skipping notebook/source/audio creation; jumping to download"
        NOTEBOOK_ID="$EXISTING_ID"
        ARTIFACT_ID="$EXISTING_ARTIFACT"
        STATUS="completed"
        REUSE_EXISTING=1
    else
        echo "  No completed audio artifact yet. Options:"
        echo "    - wait for the existing run to finish, then re-run this script"
        echo "    - pass --force to start over with a new notebook"
        exit 0
    fi
fi

# ---------------------------------------------------------------
# Steps 1-4: skipped entirely when reusing an existing notebook that already
# has a completed audio artifact. Jump straight to Step 5 (download).
# ---------------------------------------------------------------

if [ "$REUSE_EXISTING" -eq 1 ]; then
    echo "[notebooklm-radio] notebook id:    $NOTEBOOK_ID  (reused)"
    echo "[notebooklm-radio] artifact:       $ARTIFACT_ID  (reused, completed)"
else

CREATE_OUT="$TEMP_DIR/notebooklm-create-$$.txt"
nlm notebook create "$NOTEBOOK_TITLE" --profile "$PROFILE" >"$CREATE_OUT" 2>&1
NOTEBOOK_ID=$(grep -oE '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}' "$CREATE_OUT" | head -1)

if [ -z "$NOTEBOOK_ID" ]; then
    echo "ERROR: could not parse notebook id from create output:" >&2
    cat "$CREATE_OUT" >&2
    rm -f "$CREATE_OUT"
    exit 7
fi
rm -f "$CREATE_OUT"
echo "[notebooklm-radio] notebook id:    $NOTEBOOK_ID"

# ---------------------------------------------------------------
# Step 2: source add (URL) with --wait
# ---------------------------------------------------------------

SOURCE_ADD_FAILED=0
case "$SOURCE_MODE" in
    text)
        # Strip the leading YAML frontmatter block, prepend the title as an H1
        # so NotebookLM has a clear document title, and send via --text.
        # awk is used instead of sed because BSD sed lacks reliable range-then-skip semantics.
        BODY=$(awk 'BEGIN{fm=0} /^---[[:space:]]*$/{fm++; if(fm<=2) next} fm>=2{print}' "$MD_FILE")
        TEXT_CONTENT="# $TITLE

$BODY"
        if ! nlm source add "$NOTEBOOK_ID" \
                --text "$TEXT_CONTENT" \
                --title "$TITLE" \
                --wait \
                --profile "$PROFILE"; then
            SOURCE_ADD_FAILED=1
            echo "ERROR: text-mode source add failed for notebook $NOTEBOOK_ID" >&2
        fi
        ;;
    url)
        if ! nlm source add "$NOTEBOOK_ID" --url "$POST_URL" --wait --profile "$PROFILE"; then
            SOURCE_ADD_FAILED=1
            echo "ERROR: source add / ingest failed for $POST_URL" >&2
            echo "  Likely cause: the post is not yet deployed to GitHub Pages." >&2
            echo "  Retry with: $0 \"$INPUT\" --source-mode text" >&2
        fi
        ;;
esac

if [ "$SOURCE_ADD_FAILED" -ne 0 ]; then
    echo "  Notebook left behind (delete with: nlm notebook delete $NOTEBOOK_ID --confirm --profile $PROFILE)" >&2
    exit 8
fi

# ---------------------------------------------------------------
# Step 3: audio create (Japanese)
# ---------------------------------------------------------------

AUDIO_OUT="$TEMP_DIR/notebooklm-audio-$$.txt"
AUDIO_ARGS=(
    "$NOTEBOOK_ID"
    --language "$LANGUAGE"
    --format "$FORMAT"
    --length "$LENGTH"
    --confirm
    --profile "$PROFILE"
)
if [ -n "$FOCUS" ]; then
    AUDIO_ARGS+=(--focus "$FOCUS")
fi
nlm audio create "${AUDIO_ARGS[@]}" >"$AUDIO_OUT" 2>&1
rm -f "$AUDIO_OUT"

# ---------------------------------------------------------------
# Step 4: poll studio status until audio artifact is ready
# ---------------------------------------------------------------

ARTIFACT_ID=""
STATUS=""
DEADLINE=$(( $(date +%s) + 900 ))   # 15 min

while [ "$(date +%s)" -lt "$DEADLINE" ]; do
    STATUS_JSON=$(nlm studio status "$NOTEBOOK_ID" --json --profile "$PROFILE" 2>/dev/null || true)
    if [ -n "$STATUS_JSON" ]; then
        # `nlm studio status --json` returns a flat top-level array of artifacts
        # in v0.5.2. Earlier/later versions may wrap in `.artifacts`, so handle
        # both by normalizing to an array first.
        ARTIFACT_LINE=$(echo "$STATUS_JSON" | jq -r '
            (if type == "array" then . else (.artifacts // []) end) as $arts
            | ($arts | map(select((.type // .kind // "") | test("audio"; "i"))))
            | sort_by(.created_at // .createdAt // .updated_at // "")
            | (last // {})
            | "\(.id // .artifact_id // "") \(.status // .state // "")"
        ' 2>/dev/null || echo "")
        ARTIFACT_ID=$(echo "$ARTIFACT_LINE" | awk '{print $1}')
        STATUS=$(echo "$ARTIFACT_LINE" | awk '{print $2}')
        echo "[notebooklm-radio] poll: artifact=$ARTIFACT_ID status=$STATUS"
        case "$STATUS" in
            ready|READY|completed|COMPLETED|done|DONE)
                break
                ;;
            failed|FAILED|error|ERROR)
                echo "ERROR: studio generation failed (status=$STATUS, artifact=$ARTIFACT_ID)" >&2
                exit 9
                ;;
        esac
    fi
    sleep 30
done

if [ -z "${ARTIFACT_ID:-}" ] || [ -z "${STATUS:-}" ]; then
    echo "ERROR: timed out waiting for audio artifact (15min)" >&2
    exit 9
fi

case "$STATUS" in
    ready|READY|completed|COMPLETED|done|DONE) ;;
    *)
        echo "ERROR: artifact $ARTIFACT_ID is not ready (status=$STATUS)" >&2
        exit 9
        ;;
esac

fi   # end of "if [ \"\$REUSE_EXISTING\" -eq 1 ]; ... else ..."

# ---------------------------------------------------------------
# Step 5: download audio (m4a)
# ---------------------------------------------------------------

mkdir -p "$AUDIO_OUT_DIR"

# `nlm download` does NOT accept --profile (verified through 0.6.10), so we
# must temporarily switch the global default. To stay safe when multiple
# script instances run in parallel (e.g. the TUI fired into background several
# times), serialize the switch-download-restore block behind an mkdir lock.
LOCK_DIR="$STATE_DIR/profile-switch.lock"
LOCK_DEADLINE=$(( $(date +%s) + 900 ))
LOCK_HELD=0

while [ "$(date +%s)" -lt "$LOCK_DEADLINE" ]; do
    if mkdir "$LOCK_DIR" 2>/dev/null; then
        echo $$ > "$LOCK_DIR/pid"
        LOCK_HELD=1
        break
    fi
    OTHER_PID=$(cat "$LOCK_DIR/pid" 2>/dev/null || echo "?")
    if [ "$OTHER_PID" != "?" ] && ! kill -0 "$OTHER_PID" 2>/dev/null; then
        echo "[notebooklm-radio] stale lock (PID $OTHER_PID dead) — clearing" >&2
        rm -rf "$LOCK_DIR"
        continue
    fi
    echo "[notebooklm-radio] waiting for profile lock (held by PID $OTHER_PID)..." >&2
    sleep 5
done

if [ "$LOCK_HELD" -ne 1 ]; then
    echo "ERROR: could not acquire profile-switch lock within 15 min" >&2
    exit 11
fi

trap 'rm -rf "$LOCK_DIR" 2>/dev/null; trap - EXIT INT TERM' EXIT INT TERM

PREV_DEFAULT_PROFILE=$(nlm config get auth.default_profile 2>/dev/null | tr -d '[:space:]')
if [ -z "$PREV_DEFAULT_PROFILE" ]; then
    PREV_DEFAULT_PROFILE="default"
fi

RESTORE_PROFILE=0
if [ "$PREV_DEFAULT_PROFILE" != "$PROFILE" ]; then
    nlm login switch "$PROFILE" >/dev/null
    RESTORE_PROFILE=1
fi

DOWNLOAD_EXIT=0
# nlm 0.6.10 sometimes mangles the audio download URL (appends an `s512` image
# size hint that yields HTTP 404). The failure is transient — a fresh
# `nlm download audio` call regenerates the URL and usually succeeds. Retry up
# to 4 times with short backoff before giving up.
#
# --id is omitted on purpose: each notebook has exactly one audio in our flow
# (--force creates a new notebook rather than appending), so letting nlm pick
# the latest audio is correct, and --id is independently broken for some text-
# mode artifacts in 0.6.10.
for ATTEMPT in 1 2 3 4; do
    DOWNLOAD_EXIT=0
    nlm download audio "$NOTEBOOK_ID" \
        --output "$AUDIO_OUT_PATH" || DOWNLOAD_EXIT=$?
    if [ "$DOWNLOAD_EXIT" -eq 0 ] && [ -s "$AUDIO_OUT_PATH" ]; then
        if [ "$ATTEMPT" -gt 1 ]; then
            echo "[notebooklm-radio] download succeeded on attempt $ATTEMPT" >&2
        fi
        break
    fi
    if [ "$ATTEMPT" -lt 4 ]; then
        echo "[notebooklm-radio] download attempt $ATTEMPT failed (exit $DOWNLOAD_EXIT) — retrying in 5s" >&2
        rm -f "$AUDIO_OUT_PATH"
        sleep 5
    fi
done

if [ "$RESTORE_PROFILE" -eq 1 ]; then
    nlm login switch "$PREV_DEFAULT_PROFILE" >/dev/null
fi

rm -rf "$LOCK_DIR"
trap - EXIT INT TERM

if [ "$DOWNLOAD_EXIT" -ne 0 ]; then
    echo "ERROR: nlm download audio failed (exit $DOWNLOAD_EXIT)" >&2
    exit 10
fi

if [ ! -s "$AUDIO_OUT_PATH" ]; then
    echo "ERROR: download produced empty file: $AUDIO_OUT_PATH" >&2
    exit 10
fi

echo "[notebooklm-radio] audio saved:    $AUDIO_OUT_PATH"

# ---------------------------------------------------------------
# Step 5b: upload to GitHub Release Assets (single rolling tag)
# ---------------------------------------------------------------

if ! command -v gh >/dev/null 2>&1; then
    echo "ERROR: gh CLI required for release upload (https://cli.github.com)" >&2
    exit 12
fi

# Stage with the canonical asset name so gh uploads it with the slug-based
# basename. `--clobber` overwrites if a previous run produced the same asset.
UPLOAD_STAGE="$TEMP_DIR/notebooklm-radio-upload-$$"
mkdir -p "$UPLOAD_STAGE"
cp "$AUDIO_OUT_PATH" "$UPLOAD_STAGE/$ASSET_NAME"

if ! gh release upload "$RELEASE_TAG" "$UPLOAD_STAGE/$ASSET_NAME" \
        --clobber \
        --repo "$GH_REPO"; then
    echo "ERROR: gh release upload failed for $ASSET_NAME" >&2
    echo "  Local audio kept at: $AUDIO_OUT_PATH" >&2
    echo "  Retry manually: gh release upload $RELEASE_TAG $UPLOAD_STAGE/$ASSET_NAME --clobber --repo $GH_REPO" >&2
    exit 12
fi

rm -rf "$UPLOAD_STAGE"
echo "[notebooklm-radio] uploaded:       $AUDIO_URL"

# ---------------------------------------------------------------
# Step 6: patch frontmatter (audio_url points at the release asset)
# ---------------------------------------------------------------

GENERATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if command -v uv >/dev/null 2>&1; then
    uv run --quiet --no-project --with "PyYAML>=6" \
        "$BLOG_DIR/scripts/notebooklm_radio_frontmatter.py" \
        --md "$MD_FILE" \
        --audio-url "$AUDIO_URL" \
        --audio-lang "$LANGUAGE" \
        --audio-generated-at "$GENERATED_AT" \
        --audio-source notebooklm \
        --audio-format "$FORMAT"
else
    python3 "$BLOG_DIR/scripts/notebooklm_radio_frontmatter.py" \
        --md "$MD_FILE" \
        --audio-url "$AUDIO_URL" \
        --audio-lang "$LANGUAGE" \
        --audio-generated-at "$GENERATED_AT" \
        --audio-source notebooklm \
        --audio-format "$FORMAT"
fi

# ---------------------------------------------------------------
# Step 7: audit log
# ---------------------------------------------------------------

mkdir -p "$STATE_DIR"
jq -n \
    --arg slug "$SLUG" \
    --arg nb "$NOTEBOOK_ID" \
    --arg artifact "$ARTIFACT_ID" \
    --arg file "$AUDIO_OUT_PATH" \
    --arg release_url "$AUDIO_URL" \
    --arg ts "$GENERATED_AT" \
    --arg profile "$PROFILE" \
    --arg lang "$LANGUAGE" \
    --arg fmt "$FORMAT" \
    --arg len "$LENGTH" \
    --arg url "$POST_URL" \
    --arg focus "$FOCUS" \
    --arg src "$SOURCE_MODE" \
    '{slug:$slug, notebook_id:$nb, artifact_id:$artifact, audio_path:$file, release_url:$release_url, generated_at:$ts, profile:$profile, language:$lang, format:$fmt, length:$len, source_url:$url, focus:$focus, source_mode:$src}' \
    >>"$AUDIT_LOG"

echo "[notebooklm-radio] done."
echo "  - frontmatter audio_url: $AUDIO_URL"
echo "  - local cache (gitignored): $AUDIO_OUT_PATH"
echo "  - next: git add the .md change, commit, push → GitHub Pages deploy"
