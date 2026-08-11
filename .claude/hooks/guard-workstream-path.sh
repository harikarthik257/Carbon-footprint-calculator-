#!/usr/bin/env bash
# PreToolUse hook on Write|Edit. Blocks edits outside $WORKSTREAM_DIR if that
# env var is set for this session (set it per worktree). No-op if unset, so
# it's safe to leave registered even for a single-session solo run.
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

if [[ -n "$path" && -n "$WORKSTREAM_DIR" && "$path" != "$WORKSTREAM_DIR"* ]]; then
  echo "Blocked: this session owns $WORKSTREAM_DIR, not $path. Flag it for the architect instead of editing directly." >&2
  exit 2
fi
exit 0
