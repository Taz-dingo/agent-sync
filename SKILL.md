---
name: agent-sync
description: Extract, normalize, and apply portable agent context from a source to a target across devices, runtimes, or both. Use when Codex needs to migrate or mirror AI-agent setup between Codex, Claude Code, Cursor, OpenClaw, local skill folders, prompt files, memory files, or project instruction files while filtering secrets and machine-specific state.
---

# Agent Sync

Treat every request as a `source -> target` migration.

Do not start from atomic facts or a permanent preference database unless the user explicitly asks for one. Start from the source environment, extract the behavior that matters, normalize it into a portable bundle, then map it onto the target.

## Core Model

Use this pipeline:

1. Identify the source.
2. Identify the target.
3. Inventory the source surfaces that shape agent behavior.
4. Normalize what you find into a temporary transfer bundle.
5. Filter out secrets and machine-bound state.
6. Map the portable parts onto the target's native surfaces.
7. Apply conservatively and report what changed.

Read `references/source-target-model.md` for the normalization model.
Read `references/target-surfaces.md` for common target mappings.

## Source Inventory

Inspect only the surfaces that affect agent behavior:

- global or project instruction files
- memory files and persistent notes
- local skill folders and helper scripts
- prompt snippets and templates
- runtime configuration that affects tone, workflow, or tool choice
- environment references such as variable names or path conventions

Prefer reading real files over asking the user to restate them.

## Normalize Before Applying

Convert the source into these portable categories:

- `identity`: preferred name, tone, response style, communication habits
- `operating-rules`: durable instructions, constraints, review style, coding defaults
- `workflows`: recurring procedures, checklists, repo conventions, handoff patterns
- `skills`: reusable skill folders, scripts, templates, and references
- `memory`: durable context worth carrying forward
- `references`: env var names, placeholder paths, external dependencies
- `exclusions`: secrets, caches, logs, temporary state, machine-local artifacts

Do not preserve the source literally when the target has a better native representation.

## Safety Rules

- Never sync secrets, tokens, cookies, SSH material, or opaque local databases.
- Sync secret references only, such as env var names.
- Treat absolute paths as machine-specific until proven portable.
- Prefer merge over replace unless the user asks for a hard overwrite.
- Keep target-native formatting instead of forcing a source schema onto the target.
- If a target has no exact equivalent, preserve intent in the closest native surface plus a short migration note.

## Apply Strategy

Use this decision order:

1. Reuse target-native skill and instruction surfaces if they exist.
2. Merge durable behavioral rules before copying any bulky memory.
3. Carry reusable skills and snippets only after removing source-specific assumptions.
4. Append a migration note or report when manual follow-up is required.

When editing files, preserve unrelated target content.

## Working Bundle

For non-trivial migrations, create a temporary transfer bundle with `scripts/init_transfer_bundle.py`.

Use it to record:

- source and target labels
- source inventory
- portability decisions
- target mappings
- final report

Delete the bundle after use unless the user wants it kept as documentation.

## Output Contract

At the end of a migration, report:

- source and target used
- files or directories inspected
- files created or updated
- items skipped and why
- secrets or machine-specific assumptions left unresolved
- suggested next manual step if one remains

## Default Stance

Be pragmatic.

The job is not to preserve every file. The job is to recreate the source agent's useful behavior at the target with the least brittle representation.
