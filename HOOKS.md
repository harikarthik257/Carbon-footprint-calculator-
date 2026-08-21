# Suggested hooks — Urban Carbon Footprint Calculator

Hooks are deterministic — they fire every time, regardless of what Claude "decides" to
do, which is exactly what you want during a fast parallel build where sessions are
editing at once. Register them in `.claude/settings.json` (project-level, so the whole
team/every worktree shares them). Full reference: https://code.claude.com/docs/en/hooks

**Where this actually pays off:** Round 1 (due 15 Aug) only needs a thin prototype —
set these up if it's quick, skip them if it eats into deck time. They matter most for
**Round 2's on-site sprint** (27–30 Aug), where the problem is unknown until the day
of and 2–3 people need to move fast without stepping on each other. Get this working
*before* you're on-site, not during the 24–30 hours.

Each one below is picked for a specific failure mode from the hackathon playbook, not
generically — skip any that don't earn their setup time in your remaining hours.

## 1. Path-guard: keep parallel workstreams from stepping on each other

**Why:** `PRD.md` §6 assigns each worktree its own directory. Telling Claude that in a
prompt is advisory; a hook makes it a hard rule, which matters once you have 3–4
sessions running unattended in worktrees.

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
with exit code 2 if it's outside the workstream this session owns — set
`WORKSTREAM_DIR` as an env var per worktree):

```bash
#!/usr/bin/env bash
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
if [[ -n "$path" && -n "$WORKSTREAM_DIR" && "$path" != "$WORKSTREAM_DIR"* ]]; then
  echo "Blocked: this session owns $WORKSTREAM_DIR, not $path. Flag it for the architect instead." >&2
  exit 2
fi
exit 0
```

## 2. Protect the calculation engine from silent breakage

**Why:** the emission-calculation engine is the "must work perfectly" feature from
`PRD.md` §3. It's also the piece most likely to get quietly broken by a fast edit from
a different workstream late in the build. Run its tests automatically on every edit to
that directory, not just when someone remembers to.

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

**Why:** cheap insurance, zero cognitive cost, keeps four parallel sessions from
producing a messy diff for the architect to review at merge time.

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
`.ts`/`.tsx` — a few lines, skip writing it out here if you're tight on time and just
run formatters manually at integration instead.)

## 4. Block destructive commands

**Why:** boilerplate safety, matters more when several unattended sessions are running
in worktrees than in a single supervised session.

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

## 5. Keep the storyteller fed with fresh demo material

**Why:** the playbook's biggest recurring failure mode is "no demo buffer" — the pitch
gets built from stale, half-remembered features. This appends a one-line summary to
`pitch/DEMO_NOTES.md` every time a session wraps up, so the storyteller always has
current material without asking builders to context-switch.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/log-session-summary.sh" }
        ]
      }
    ]
  }
}
```

## 6. Shared context at the start of every session

**Why:** with several people running their own Claude Code sessions, this keeps the
hero feature and rubric priorities front-of-mind for everyone, not just whoever read
`PRD.md` most recently.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: the Gemini vision + recommendation layer is the hero feature — see PRD.md §3. Do not cut it.'"
          }
        ]
      }
    ]
  }
}
```

## Not recommending (for this event)

- **HTTP/MCP-dispatch hooks** — overkill for a ~24-hour build; the setup cost isn't
  worth it unless you're already fluent with them.
- **Managed/enterprise policy hooks** — team-scale governance, not needed for a
  hackathon team.

## Setup

```bash
mkdir -p .claude/hooks
chmod +x .claude/hooks/*.sh
```

Then merge the JSON blocks above into a single `.claude/settings.json` (one top-level
`"hooks"` object, each event key holding its array of matchers — don't create multiple
top-level `hooks` keys, they need to merge into one object). Commit it so every
worktree and every teammate's session picks it up automatically.
