# agent-sync

`agent-sync` is a local skill for migrating useful agent behavior from a source to a target.

The source and target may be:

- different devices
- different runtimes on one device
- the same runtime on two machines
- a repo-local setup and a global setup

This repo no longer treats the problem as a permanent facts database.
It treats the problem as:

1. extract from source
2. normalize into a portable bundle
3. apply to target

## Included

- `SKILL.md` — skill instructions
- `agents/openai.yaml` — UI metadata
- `references/source-target-model.md` — migration model
- `references/target-surfaces.md` — target mapping heuristics
- `scripts/init_transfer_bundle.py` — scaffold a temporary working bundle
- `examples/claude-code-to-codex/` — end-to-end example migration

## Typical use

- migrate Claude Code habits into Codex
- move a tuned Codex setup to a new machine
- copy project-specific agent behavior from one repo into another
- port private local skills between environments

## Example

See `examples/claude-code-to-codex/README.md` for a worked example that:

- inventories Claude Code source surfaces
- normalizes them into a bundle
- maps them to Codex-native target files
- shows what gets skipped for safety

Run the executable demo with:

```bash
python3 scripts/demo_migrate_claude_to_codex.py fixtures/claude-source /tmp/agent-sync-demo
python3 -m unittest tests.test_demo_migration
```

## Principle

Do not mirror every file.

Recreate the source agent's useful behavior at the target with the least brittle target-native representation.
