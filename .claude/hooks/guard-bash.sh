#!/usr/bin/env bash
# PreToolUse hook on Bash. Blocks a small set of destructive patterns.
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // empty')

if echo "$cmd" | grep -Eq 'rm -rf (/|~|\$HOME)[[:space:]]*$|git push .*(main|master).*--force'; then
  echo "Blocked: destructive command matched a guard rule ($cmd)." >&2
  exit 2
fi
exit 0
