# Source-Target Model

Treat every migration as three layers:

1. `extract`
   - Read the source runtime's real configuration surfaces.
   - Capture only durable behavior, not temporary execution state.

2. `normalize`
   - Reframe the source into a portable bundle.
   - Use categories instead of runtime-specific files.

3. `apply`
   - Map each portable category onto the target's native surfaces.
   - Preserve meaning rather than original file layout.

## Portable Bundle Shape

Use this structure mentally or on disk:

```text
bundle/
  manifest.yaml
  inventory.md
  mappings.md
  report.md
  payload/
    identity.md
    operating-rules.md
    workflows.md
    memory.md
    refs.env.example
    skills/
```

The bundle is temporary. It is a working area, not a long-term database.

## Classification Rules

Classify every source artifact into one of four buckets:

- `portable`: move as-is or nearly as-is
- `portable-with-mapping`: keep intent, rewrite representation for the target
- `local-only`: leave behind because it depends on one machine or one runtime
- `secret`: do not copy; replace with a reference or note

## What Usually Transfers Well

- response style and tone
- review and coding habits
- project conventions
- local skills after path cleanup
- reusable prompt fragments
- stable memory notes

## What Usually Needs Rewriting

- absolute paths
- runtime-specific config formats
- command aliases bound to one shell or workstation
- target files that mix durable instructions with generated state

## What Usually Stays Behind

- caches and logs
- conversation histories unless explicitly requested
- telemetry or analytics files
- editor session state
- opaque local databases without a portable export path
