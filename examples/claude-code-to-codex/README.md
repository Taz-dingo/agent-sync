# Claude Code -> Codex example

This example shows how `agent-sync` treats a migration from a tuned Claude Code setup on one machine into a Codex-oriented setup on another machine.

It demonstrates four things:

1. inventory the source surfaces
2. normalize them into a temporary transfer bundle
3. map them onto Codex-native target surfaces
4. report what was applied and what was skipped

## Assumed source surfaces

The Claude Code source is assumed to contain:

- a global instruction file with tone and review habits
- one reusable local skill for pull-request review
- a durable memory note with naming and workflow preferences
- shell aliases and absolute paths tied to one workstation
- API keys stored in the shell environment

## Codex target surfaces used

The migration maps those behaviors into:

- `target/AGENTS.md` for repo-scoped durable instructions
- `target/skills/pr-review/SKILL.md` for the reusable review workflow
- bundle payload notes for durable memory and references

## Why this example matters

It shows the intended product interface for the skill:

- start from a source
- end at a target
- keep only portable behavior
- leave secrets and machine-local state behind
