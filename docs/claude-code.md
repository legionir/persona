# Using the library in Claude Code

| Path | What it is |
|---|---|
| `skills/<name>/SKILL.md` | 218 Agent Skills (190 roles + 28 composite audits), loaded when the task matches |
| `agents/<name>.md` | 190 subagents, one per role persona. SUPERVISOR = read-only tools (`Read, Grep, Glob`); EXECUTOR = inherits all tools |
| `.claude/skills`, `.claude/agents` | symlinks to the above, so opening this repo in Claude Code works immediately |
| `.claude-plugin/` | plugin + marketplace manifests |

## Install

**As a plugin (all projects):**
```
/plugin marketplace add legionir/persona
/plugin install persona@persona
```

**Into another project:**
```bash
cp -rL skills/<name> /path/to/project/.claude/skills/
cp agents/<name>.md /path/to/project/.claude/agents/
```

## Use

- Skills trigger automatically from their description, or invoke by name (`/qa-lead`).
- Subagents: "use the qa-lead agent to review this release" or `@agent-qa-lead`.

## Regenerate

`make claude-code` (runs `scripts/build_claude_code.py`; `--check` is part of `make check`).
Agents are derived from `skills/`, so run `make skills` first when personas change.
