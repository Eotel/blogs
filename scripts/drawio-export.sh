#!/usr/bin/env bash
# scripts/drawio-export.sh
#
# Wraps the rlespinasse/drawio-desktop-headless Docker image so contributors
# can render static/images/*.drawio without installing draw.io locally.
#
# Usage:
#   drawio-export <input.drawio> [-f png|svg|pdf] [-o <out-dir>] [--scale 2]
#
# All arguments after the wrapper are forwarded to draw.io inside the container;
# $PWD is mounted to /data so relative paths Just Work.
#
# Env:
#   DRAWIO_EXPORT_IMAGE — override the image tag (default: rlespinasse/drawio-desktop-headless:latest)
#   DRAWIO_EXPORT_TIMEOUT — draw.io command timeout (default: 30s)

set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found. Install Docker Desktop (or colima) and retry." >&2
  exit 127
fi

IMAGE="${DRAWIO_EXPORT_IMAGE:-rlespinasse/drawio-desktop-headless:latest}"
HOME_DIR="$PWD/.claude/temp/drawio-home"
TIMEOUT="${DRAWIO_EXPORT_TIMEOUT:-30s}"

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Pulling $IMAGE ..." >&2
  docker pull "$IMAGE"
fi

mkdir -p "$HOME_DIR"

EXPORT_ARGS=("$@")
case " $* " in
  *" -h "*|*" --help "*|*" -V "*|*" --version "*|*" -x "*|*" --export "*) ;;
  *) EXPORT_ARGS=("-x" "${EXPORT_ARGS[@]}") ;;
esac

exec docker run --rm \
  -u "$(id -u):$(id -g)" \
  -e HOME=/data/.claude/temp/drawio-home \
  -e DRAWIO_DESKTOP_COMMAND_TIMEOUT="$TIMEOUT" \
  -w /data \
  -v /etc/passwd:/etc/passwd:ro \
  -v "$PWD:/data" \
  "$IMAGE" \
  "${EXPORT_ARGS[@]}"
