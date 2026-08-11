#!/usr/bin/env bash
# PostToolUse hook on Write|Edit. If the edit touched backend/engine, run its
# tests immediately — this is the "must work perfectly" feature (PRD.md §4),
# it should never break silently mid-build.
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

if [[ "$path" == *"backend/engine"* ]]; then
  cd "$CLAUDE_PROJECT_DIR/backend" 2>/dev/null && \
    python3 -m pytest engine/tests -q || \
    echo "engine tests failed after this edit — check before moving on" >&2
fi
exit 0
