#!/usr/bin/env bash
set -euo pipefail

# Cleanup rqmd AI bundle artifacts from a repository's .github directory.
# Keeps:
#   - .github/workflows/
#   - .github/skills/dev/
#   - .github/skills/test/
#   - .github/copilot-instructions.md only when it begins with
#     "# rqmd AI Contributor Instructions"

ROOT="${1:-.}"
GITHUB_DIR="${ROOT%/}/.github"

if [[ ! -d "$GITHUB_DIR" ]]; then
  echo "No .github directory found at: $GITHUB_DIR"
  exit 0
fi

echo "Cleaning: $GITHUB_DIR"

# Remove common rqmd bundle directories/files when present.
rm -rf "$GITHUB_DIR/agents" || true
rm -rf "$GITHUB_DIR/prompts" || true
rm -f "$GITHUB_DIR/rqmd-bundle.json" || true

# Prune skills except dev/test.
if [[ -d "$GITHUB_DIR/skills" ]]; then
  find "$GITHUB_DIR/skills" \
    -mindepth 1 -maxdepth 1 \
    ! -name dev \
    ! -name test \
    -exec rm -rf {} +

  # Remove skills dir if now empty.
  if [[ -z "$(ls -A "$GITHUB_DIR/skills" 2>/dev/null || true)" ]]; then
    rmdir "$GITHUB_DIR/skills" || true
  fi
fi

# Remove copilot-instructions unless it has the expected canonical heading.
COPILOT_FILE="$GITHUB_DIR/copilot-instructions.md"
if [[ -f "$COPILOT_FILE" ]]; then
  FIRST_LINE="$(head -n 1 "$COPILOT_FILE" || true)"
  if [[ "$FIRST_LINE" != "# rqmd AI Contributor Instructions" ]]; then
    rm -f "$COPILOT_FILE"
    echo "Removed non-canonical copilot instructions: $COPILOT_FILE"
  else
    echo "Kept canonical copilot instructions: $COPILOT_FILE"
  fi
fi

echo "Cleanup complete."
