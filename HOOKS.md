# Suggested hooks — Urban Carbon Footprint Calculator

Hooks are deterministic — they fire every time, regardless of what Claude "decides" to
do, which is exactly what you want when several sessions might be editing at once, or
when you just want a rule enforced without having to remember it. Register them in
`.claude/settings.json` (project-level, so every worktree/session shares them). Full
reference: https://code.claude.com/docs/en/hooks

Each one below is picked for a specific failure mode — skip any that don't earn their
setup time.

## 1. Path-guard: keep parallel sessions from stepping on each other

**Why:** useful if you ever run more than one Claude Code session against this repo at
once (e.g. one worktree per feature). A no-op for a single session, since it only
blocks when `WORKSTREAM_DIR` is set.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-workstream-path.sh" }
        ]
      }
    ]
  }
}
```

`.claude/hooks/guard-workstream-path.sh` (reads the target path from stdin JSON, blocks
with exit code 2 if it's outside the directory this session owns — set
`WORKSTREAM_DIR` as an env var per worktree):

```bash
#!/usr/bin/env bash
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
if [[ -n "$path" && -n "$WORKSTREAM_DIR" && "$path" != "$WORKSTREAM_DIR"* ]]; then
  echo "Blocked: this session owns $WORKSTREAM_DIR, not $path." >&2
  exit 2
fi
exit 0
```

## 2. Protect the calculation engine from silent breakage

**Why:** the emission-calculation engine is the "must work perfectly" part of this
app (`PRD.md` §2) — the one piece where a quiet regression would be worst. Run its
tests automatically on every edit to that directory, not just when someone remembers to.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/test-engine-on-change.sh" }
        ]
      }
    ]
  }
}
```

```bash
#!/usr/bin/env bash
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
if [[ "$path" == *"backend/engine"* ]]; then
  cd "$CLAUDE_PROJECT_DIR/backend" && pytest engine/tests -q || \
    echo "engine tests failed after this edit — check before moving on" >&2
fi
exit 0
```

## 3. Auto-format on save

**Why:** cheap insurance, zero cognitive cost, keeps diffs clean.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-changed.sh" }
        ]
      }
    ]
  }
}
```

(Script: run `ruff format <path>` if it's a `.py` file, `eslint --fix <path>` if it's
`.ts`/`.tsx` — a few lines, or just run formatters manually if you're not writing it
out.)

## 4. Block destructive commands

**Why:** cheap safety net, matters more with unattended sessions.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-bash.sh" }
        ]
      }
    ]
  }
}
```

```bash
#!/usr/bin/env bash
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // empty')
if echo "$cmd" | grep -Eq 'rm -rf (/|~|\$HOME)|git push .*(main|master).*--force'; then
  echo "Blocked: destructive command matched a guard rule." >&2
  exit 2
fi
exit 0
```

## 5. Shared context at the start of every session

**Why:** keeps the core feature front-of-mind at the start of every session, not just
whoever read `PRD.md` most recently.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: the Gemini vision + recommendation layer is the core feature — see PRD.md §2. Do not cut it.'"
          }
        ]
      }
    ]
  }
}
```

## Not recommending

- **HTTP/MCP-dispatch hooks** — overkill for this project's size; not worth the setup
  cost unless you're already fluent with them.
- **Managed/enterprise policy hooks** — team-scale governance, not needed for a
  single-developer project.

## Setup

```bash
mkdir -p .claude/hooks
chmod +x .claude/hooks/*.sh
```

Then merge the JSON blocks above into a single `.claude/settings.json` (one top-level
`"hooks"` object, each event key holding its array of matchers — don't create multiple
top-level `hooks` keys, they need to merge into one object). Commit it so every
worktree/session picks it up automatically.
