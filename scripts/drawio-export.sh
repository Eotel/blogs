#!/usr/bin/env bash
# scripts/drawio-export.sh
#
# Wraps the rlespinasse/drawio-export Docker image so contributors can render
# static/images/*.drawio without installing draw.io locally.
#
# Usage:
#   drawio-export <input.drawio> [-f png|svg|pdf] [-o <out-dir>] [--scale 2]
#
# All arguments after the wrapper are forwarded to drawio-export inside the
# container; $PWD is mounted to /data so relative paths Just Work.
#
# Env:
#   DRAWIO_EXPORT_IMAGE — override the image tag (default: rlespinasse/drawio-export:latest)

set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "error: docker not found. Install Docker Desktop (or colima) and retry." >&2
  exit 127
fi

IMAGE="${DRAWIO_EXPORT_IMAGE:-rlespinasse/drawio-export:latest}"

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Pulling $IMAGE ..." >&2
  docker pull "$IMAGE"
fi

exec docker run --rm \
  -v "$PWD:/data" \
  -u "$(id -u):$(id -g)" \
  "$IMAGE" \
  "$@"
