#!/usr/bin/env bash
# playtest.sh — Build and install both rqmd-cli and rqmd-vscode from local
# source without a release or version bump. Reload VS Code after running.
#
# Usage:
#   ./scripts/playtest.sh          # install both
#   ./scripts/playtest.sh cli      # install rqmd-cli only
#   ./scripts/playtest.sh vscode   # install rqmd-vscode only
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLI_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VSCODE_ROOT="$(cd "$CLI_ROOT/../rqmd-vscode" && pwd)"

bold() { printf '\033[1m%s\033[0m\n' "$*"; }
green() { printf '\033[1;32m%s\033[0m\n' "$*"; }

install_cli() {
    bold "→ Installing rqmd CLI from local source (editable)…"
    (cd "$CLI_ROOT" && uv tool install --editable . --upgrade --force)
    green "  ✔ rqmd CLI installed ($(rqmd --version 2>/dev/null || echo 'unknown version'))"
}

install_vscode() {
    bold "→ Packaging rqmd-vscode extension…"
    (cd "$VSCODE_ROOT" && npx --yes @vscode/vsce package --no-dependencies -o rqmd-local.vsix)
    bold "→ Installing VSIX into VS Code…"
    code --install-extension "$VSCODE_ROOT/rqmd-local.vsix" --force
    green "  ✔ rqmd-vscode extension installed from local build"
}

target="${1:-both}"

case "$target" in
    cli)    install_cli ;;
    vscode) install_vscode ;;
    both)   install_cli; echo; install_vscode ;;
    *)      echo "Usage: $0 [cli|vscode|both]"; exit 1 ;;
esac

echo
green "Done! Reload VS Code (Cmd+Shift+P → 'Developer: Reload Window') to pick up changes."
