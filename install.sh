#!/usr/bin/env bash
# Link every skill under skills/ into each agent runtime's skills directory that exists.
# Usage: ./install.sh [--uninstall]
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
MODE="${1:-install}"
linked=0
for dir in "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.hermes/skills"; do
  [ -d "$dir" ] || continue
  for skill in "$REPO"/skills/*/; do
    skill="${skill%/}"; name="$(basename "$skill")"
    if [ "$MODE" = "--uninstall" ]; then
      if [ -L "${dir:?}/${name:?}" ]; then unlink "${dir:?}/${name:?}"; echo "removed $dir/$name"; fi
    else
      ln -sfn "$skill" "$dir/$name"; echo "linked  $dir/$name -> $skill"; linked=$((linked+1))
    fi
  done
done
[ "$MODE" = "--uninstall" ] || echo "install: $linked links; restart the agent so it reloads its skills"
