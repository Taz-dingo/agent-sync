# agent-sync

**agent-sync** is an installable local skill for **migrating AI agent setup across tools, devices, and runtimes**.

Use it when you want to move or recreate durable agent behavior between:

- **Codex** and **Claude Code**
- **Codex** and **Cursor**
- one machine and another machine
- a global agent setup and a repo-local setup
- one local skill environment and another

In plain terms, `agent-sync` is a **skill for agent migration**:

- migrate agent instructions
- migrate durable memory
- migrate reusable workflows
- migrate local skills
- keep secrets out of the target
- avoid copying machine-specific junk

## What Problem It Solves

Most AI agent setups become fragmented over time:

- instructions live in different files
- local skills drift across machines
- memory notes exist in one tool but not another
- one setup feels "right" and the next one feels broken

`agent-sync` solves that by treating migration as:

1. read the real source
2. infer the durable behavior
3. recreate that behavior in target-native surfaces

This repo is **prompt-first**.
It does **not** treat migration as a permanent facts database or a rigid conversion table.

## Who This Is For

This skill is useful if you are trying to:

- migrate from **Claude Code to Codex**
- migrate from **Codex to Claude Code**
- port **Cursor rules** into another agent environment
- move your private local skills to a new machine
- keep a consistent AI coding assistant style across runtimes
- preserve durable behavior without copying secrets, caches, or machine-local paths

## How It Works

`agent-sync` uses an adaptive migration workflow:

- inspect source files that actually shape agent behavior
- separate durable behavior from local state
- normalize what matters into a portable mental model
- choose the smallest target-native surfaces that preserve intent
- apply conservatively and report what changed

It focuses on migrating:

- agent instructions
- coding and review habits
- reusable workflows
- local skills
- durable memory
- environment references

It avoids migrating:

- secrets and tokens
- SSH material
- absolute machine-specific paths
- caches and logs
- temporary runtime state

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

## Use Cases

Common searches this skill should match:

- `Codex skill for migrating agent setup`
- `Claude Code to Codex migration`
- `AI agent config migration`
- `portable agent memory and instructions`
- `move local skills between machines`
- `sync AI coding assistant behavior`

## Included

Core package contents:

- `SKILL.md` — main skill instructions
- `agents/openai.yaml` — UI metadata for skill-aware hosts
- `references/source-target-model.md` — migration model
- `references/target-surfaces.md` — target heuristics
- `references/adaptive-migration-playbook.md` — adaptive decision procedure
- `scripts/init_transfer_bundle.py` — optional scratch bundle scaffold
- `scripts/install_skill.py` — local installer for the skill package

Optional extras:

- `examples/claude-code-to-codex/` — worked example
- `fixtures/` + `tests/` — feasibility and regression harness

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

## Publishing Notes

If you want people to discover this skill on the web, the README helps, but these matter too:

- GitHub repository name and description
- GitHub topics such as `codex`, `claude-code`, `cursor`, `ai-agents`, `developer-tools`, `skills`
- release notes or demo posts that use the same terms as the README
- examples that explicitly mention source and target runtimes
