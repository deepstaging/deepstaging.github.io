#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2024-present Deepstaging
# SPDX-License-Identifier: RPL-1.5

# Serves the landing page or builds all documentation sites.
set -euo pipefail
cd "$(dirname "$0")/.."

VENV_DIR=".venv"

if [ ! -f "$VENV_DIR/bin/pip" ]; then
    echo "Creating virtual environment..."
    rm -rf "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/pip" install -r requirements.txt --quiet

CMD="${1:-serve}"
shift 2>/dev/null || true

REPOS_DIR="$(cd .. && pwd)"
OUTPUT_DIR="$(pwd)/site"

case "$CMD" in
    serve)
        echo "Starting dev server at http://127.0.0.1:8000 (landing page only)"
        "$VENV_DIR/bin/zensical" serve "$@"
        ;;
    build)
        echo "Building all sites..."
        rm -rf "$OUTPUT_DIR"
        mkdir -p "$OUTPUT_DIR"

        echo "Building Deepstaging docs..."
        "$VENV_DIR/bin/zensical" build --strict \
            -f "$REPOS_DIR/deepstaging/mkdocs.yml"
        mv "$REPOS_DIR/deepstaging/site" "$OUTPUT_DIR/deepstaging"

        echo "Building Roslyn docs..."
        "$VENV_DIR/bin/zensical" build --strict \
            -f "$REPOS_DIR/roslyn/mkdocs.yml"
        mv "$REPOS_DIR/roslyn/site" "$OUTPUT_DIR/roslyn"

        echo "Building Web docs..."
        "$VENV_DIR/bin/zensical" build --strict \
            -f "$REPOS_DIR/deepstaging-web/mkdocs.yml"
        mv "$REPOS_DIR/deepstaging-web/site" "$OUTPUT_DIR/web"

        echo "Building landing page..."
        "$VENV_DIR/bin/zensical" build --strict
        cp -r site/* "$OUTPUT_DIR/"

        echo "All sites built to ./site"
        ;;
    *)
        echo "Usage: $0 [serve|build]"
        echo "  serve  - Start local dev server for landing page (default)"
        echo "  build  - Build all sites into ./site"
        exit 1
        ;;
esac
