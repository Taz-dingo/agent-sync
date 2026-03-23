---
name: agent-sync
description: Adaptively migrate portable agent context from a source to a target across devices, runtimes, or both. Use when Codex needs to read real source files, infer durable behavior, and recreate that behavior in Codex, Claude Code, Cursor, OpenClaw, local skill folders, prompt files, memory files, or project instruction files while filtering secrets and machine-specific state.
---

# Agent Sync

Treat every request as a `source -> target` migration.

This skill is prompt-first, not mapping-first.

Do not rely on a rigid conversion table unless the user asks for a deterministic exporter. Read the real source surfaces, infer the durable behavior, and recreate that behavior in the target's native surfaces.

## Core Model

Use this reasoning loop:

1. Identify the source.
2. Identify the target.
3. Inspect the source surfaces that actually shape agent behavior.
4. Separate durable behavior from local state.
5. Re-express durable behavior in a portable mental model.
6. Choose the smallest target-native surfaces that preserve intent.
7. Apply conservatively and report what changed.

Read `references/source-target-model.md` for the normalization model.
Read `references/target-surfaces.md` for common target heuristics.
Read `references/adaptive-migration-playbook.md` for the decision procedure.

## Default Stance

Prefer adaptive reasoning over hardcoded mappings.

The job is not to mirror file trees. The job is to recreate the source agent's useful behavior at the target with the least brittle target-native representation.

## What To Inspect

Inspect only the surfaces that affect agent behavior:

- global or project instruction files
- memory files and persistent notes
- local skill folders and helper scripts
- prompt snippets and templates
- runtime configuration that affects tone, workflow, or tool choice
- environment references such as variable names or path conventions

Prefer reading real files over asking the user to restate them.

## Portable Categories

Normalize what you learn into these categories:

- `identity`: preferred name, tone, response style, communication habits
- `operating-rules`: durable instructions, constraints, review style, coding defaults
- `workflows`: recurring procedures, checklists, repo conventions, handoff patterns
- `skills`: reusable skill folders, scripts, templates, and references
- `memory`: durable context worth carrying forward
- `references`: env var names, placeholder paths, external dependencies
- `exclusions`: secrets, caches, logs, temporary state, machine-local artifacts

These categories are for reasoning. They are not a required on-disk schema.

## Safety Rules

- Never sync secrets, tokens, cookies, SSH material, or opaque local databases.
- Sync secret references only, such as env var names.
- Treat absolute paths as machine-specific until proven portable.
- Prefer merge over replace unless the user asks for a hard overwrite.
- Keep target-native formatting instead of forcing a source schema onto the target.
- If a target has no exact equivalent, preserve intent in the closest native surface plus a short migration note.

## Target Selection Heuristic

Use this decision order:

1. Reuse target-native skill and instruction surfaces if they exist.
2. Put durable behavior into the smallest stable target-native surface.
3. Put reusable procedures into a skill or script, not a long instruction block.
4. Carry bulky memory only when it still changes behavior at the target.
5. Append a migration note or report when manual follow-up is required.

When editing files, preserve unrelated target content.

## Working Bundle

For non-trivial migrations, you may create a temporary transfer bundle with `scripts/init_transfer_bundle.py`.

Use it only as scratch space for:

- source and target labels
- source inventory
- portability decisions
- target mappings
- final report

Delete the bundle after use unless the user wants it kept as documentation.

## Role Of Scripts

Treat bundled scripts and examples as helpers, tests, or evaluation fixtures.

Do not let a demo script define the migration logic when the real source and target provide enough evidence for an adaptive migration.

## Output Contract

At the end of a migration, report:

- source and target used
- files or directories inspected
- files created or updated
- items skipped and why
- secrets or machine-specific assumptions left unresolved
- suggested next manual step if one remains
