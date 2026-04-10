#!/usr/bin/env bash
# rqmd-bundle-cleanup.sh
#
# Remove rqmd-ai installed bundle files from a project's .github/ directory.
# Keeps: .github/workflows/, .github/skills/dev/, .github/skills/test/
# Removes: agents/, prompts/, rqmd-bundle.json, all other skills/
#          copilot-instructions.md ONLY if it was installed by rqmd (starts with rqmd header)
#
# Usage:
#   ./scripts/rqmd-bundle-cleanup.sh                  # run in current dir
#   ./scripts/rqmd-bundle-cleanup.sh /path/to/repo    # run in another repo
#   ./scripts/rqmd-bundle-cleanup.sh --dry-run        # preview without removing
#
set -euo pipefail

REPO_ROOT="${1:-.}"
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  REPO_ROOT="${2:-.}"
elif [[ "${2:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

GH="${REPO_ROOT}/.github"
RQMD_HEADER="# rqmd AI Contributor Instructions"

remove() {
  local target="$1"
  if [[ ! -e "$target" ]]; then return; fi
  if [[ "$DRY_RUN" == true ]]; then
    echo "  [dry-run] would remove: ${target#$REPO_ROOT/}"
  else
    if [[ -d "$target" ]]; then
      if git -C "$REPO_ROOT" ls-files --error-unmatch "$target" &>/dev/null 2>&1 || \
         git -C "$REPO_ROOT" ls-files -- "$target" | grep -q .; then
        git -C "$REPO_ROOT" rm -rf "$target" && echo "  removed: ${target#$REPO_ROOT/}"
      else
        rm -rf "$target" && echo "  removed (untracked): ${target#$REPO_ROOT/}"
      fi
    else
      if git -C "$REPO_ROOT" ls-files -- "$target" | grep -q .; then
        git -C "$REPO_ROOT" rm -f "$target" && echo "  removed: ${target#$REPO_ROOT/}"
      else
        rm -f "$target" && echo "  removed (untracked): ${target#$REPO_ROOT/}"
      fi
    fi
  fi
}

echo "rqmd bundle cleanup: ${REPO_ROOT}"
[[ "$DRY_RUN" == true ]] && echo "(dry-run mode — no files will be changed)"
echo ""

# agents/ and prompts/ — always rqmd-owned
remove "${GH}/agents"
remove "${GH}/prompts"

# rqmd metadata file
remove "${GH}/rqmd-bundle.json"

# skills/ — remove all subdirs except dev/ and test/
if [[ -d "${GH}/skills" ]]; then
  for skill_dir in "${GH}/skills"/*/; do
    name="$(basename "$skill_dir")"
    if [[ "$name" == "dev" || "$name" == "test" ]]; then
      echo "  keeping: .github/skills/${name}/"
    else
      remove "${skill_dir%/}"
    fi
  done
fi

# copilot-instructions.md — only remove if it was installed by rqmd
ci_file="${GH}/copilot-instructions.md"
if [[ -f "$ci_file" ]]; then
  first_line="$(head -1 "$ci_file")"
  if [[ "$first_line" == "$RQMD_HEADER" ]]; then
    remove "$ci_file"
  else
    echo "  keeping: .github/copilot-instructions.md (not rqmd-installed — first line: ${first_line:0:60})"
  fi
fi

echo ""
echo "Done."
