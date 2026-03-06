#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2024-present Deepstaging
# SPDX-License-Identifier: RPL-1.5

# Serves or builds the unified documentation site.
set -euo pipefail
cd "$(dirname "$0")/.."

VENV_DIR=".venv"

if [ ! -f "$VENV_DIR/bin/pip" ]; then
    echo "Creating virtual environment..."
    rm -rf "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/pip" install -r requirements.txt --quiet

REPOS_DIR="$(cd .. && pwd)"

assemble_docs() {
    echo "Assembling docs from sibling repos..."
    rm -rf docs/deepstaging docs/roslyn docs/web
    cp -r "$REPOS_DIR/deepstaging/docs" docs/deepstaging
    cp -r "$REPOS_DIR/roslyn/docs" docs/roslyn
    cp -r "$REPOS_DIR/deepstaging-web/docs" docs/web

    echo "Assembling nav from repo mkdocs configs..."
    "$VENV_DIR/bin/python" build/assemble-nav.py "$REPOS_DIR"
}

CMD="${1:-serve}"
shift 2>/dev/null || true

case "$CMD" in
    serve)
        assemble_docs
        echo "Starting dev server at http://127.0.0.1:8000"
        "$VENV_DIR/bin/zensical" serve "$@"
        ;;
    build)
        assemble_docs
        echo "Building site..."
        "$VENV_DIR/bin/zensical" build --strict "$@"
        echo "Site built to ./site"
        ;;
    *)
        echo "Usage: $0 [serve|build]"
        echo "  serve  - Start local dev server (default)"
        echo "  build  - Build static site"
        exit 1
        ;;
esac
