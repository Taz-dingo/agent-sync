# Mappings

## Identity

- source: concise, direct, low-fluff collaborator tone from `~/.claude/CLAUDE.md`
- target: repo-scoped tone guidance in `target/AGENTS.md`

## Operating Rules

- source: review for correctness first, avoid unrelated fixes, ask before broad rewrites
- target: durable rules section in `target/AGENTS.md`

## Workflows

- source: handoff includes changed files, risk notes, and next manual step
- target: delivery checklist in `target/AGENTS.md`

## Skills

- source: `~/.claude/skills/pr-review/SKILL.md`
- target: `target/skills/pr-review/SKILL.md`

## Memory

- source: `~/.claude/memory/team-preferences.md`
- target: `bundle/payload/memory.md` for operator review before merging into a real Codex memory surface
