# syncskl

A small CLI + repo convention to keep a **Single Source of Truth (SSOT)** for agent/skill behavior.

## Goals
- Keep critical facts/preferences in one place (this repo).
- Make changes auditable (git history).
- Make consumption deterministic (strict JSON + schema + checks).

## Layout
- `syncskl/facts/*.json` — SSOT facts (machine-readable, strict)
- `syncskl/schemas/*.schema.json` — JSON Schemas for validation
- `syncskl/bin/syncskl.js` — CLI

## Quick start
```bash
node syncskl/bin/syncskl.js check
node syncskl/bin/syncskl.js get user.preferred_name
node syncskl/bin/syncskl.js search tavily
```

## Commands
- `syncskl get <key>`
- `syncskl search <query>`
- `syncskl set <key> --value <json> [--source <text>]`
- `syncskl check`

## Key rules
- Every fact must have `value` and `meta.source`.
- Conflicts are resolved by explicit updates (never silently overwritten).
- Prefer small, atomic keys.
