# agent-sync

`agent-sync` is a local skill for migrating useful agent behavior from a source to a target.

The source and target may be:

- different devices
- different runtimes on one device
- the same runtime on two machines
- a repo-local setup and a global setup

This repo is prompt-first.
It does not treat migration as a permanent facts database or a rigid conversion table.
It treats migration as:

1. read the real source
2. infer the durable behavior
3. recreate that behavior in target-native surfaces

## Install

Install into your Codex skills directory with:

```bash
python3 scripts/install_skill.py
```

By default this installs to `$CODEX_HOME/skills/agent-sync` or `~/.codex/skills/agent-sync` when `CODEX_HOME` is unset.

Useful options:

```bash
python3 scripts/install_skill.py --force
python3 scripts/install_skill.py --dest /custom/path/agent-sync
python3 scripts/install_skill.py --include-extras
```

- default install copies the core skill files only
- `--include-extras` also copies the worked example, fixtures, and tests
- `--force` replaces an existing install directory

## Included

- `SKILL.md` — skill instructions
- `agents/openai.yaml` — UI metadata
- `references/source-target-model.md` — migration model
- `references/target-surfaces.md` — target heuristics
- `references/adaptive-migration-playbook.md` — adaptive decision procedure
- `scripts/init_transfer_bundle.py` — optional scratch bundle scaffold
- `scripts/install_skill.py` — local installer for the skill package
- `examples/claude-code-to-codex/` — worked example
- `fixtures/` + `tests/` — feasibility and regression harness

## Principle

Do not mirror every file.

Recreate the source agent's useful behavior at the target with the least brittle target-native representation.

## Example

See `examples/claude-code-to-codex/README.md` for a worked example that:

- inventories Claude Code source surfaces
- normalizes them into a scratch bundle
- maps them to Codex-native target files
- shows what gets skipped for safety

Run the executable feasibility demo with:

```bash
python3 scripts/demo_migrate_claude_to_codex.py fixtures/claude-source /tmp/agent-sync-demo
python3 -m unittest tests.test_demo_migration
```

## What The Scripts Are For

The scripts in this repo are helpers and evaluation fixtures.

They prove that the migration idea is executable and testable, but they are not the intended product interface. The intended interface is the `agent-sync` skill prompt plus real source and target files.
