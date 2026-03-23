# Target Surfaces

Map behavior to the target's native surfaces instead of imposing a universal file format.

These are heuristics, not a rigid conversion table.

## Codex

Prefer these surfaces when present:

- `AGENTS.md` for repo-scoped instructions
- skill folders with `SKILL.md` for reusable workflows
- local helper scripts bundled with the skill or repo
- project documentation when the target behavior is repo-specific

## Claude Code

Prefer these surfaces when present:

- local skills under the user's skill directory
- project instruction files the runtime already reads
- durable memory or note files kept beside the project
- helper scripts referenced from skills instead of copied inline

## Cursor

Prefer these surfaces when present:

- project rule files and workspace instructions
- reusable snippets or templates stored in-repo
- lightweight supporting scripts for deterministic steps

## OpenClaw and similar file-first agents

Prefer these surfaces when present:

- user instruction markdown files
- memory folders or note files
- local helper scripts and prompt snippets

## Selection Heuristics

- Put durable behavior into the smallest native instruction surface.
- Put reusable procedures into a skill or script, not a long instruction block.
- Put stable context into a memory note, not a generated config file.
- Put machine-specific values into references or placeholders.
- Put unresolved mismatches into the migration report.
- If several targets could work, choose the one that keeps the target easiest to maintain by humans.
