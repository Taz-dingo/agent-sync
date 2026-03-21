# syncskl — Spec (v0 → v1)

## Problem
User-specific agent customizations are scattered and hard to keep consistent across:
- multiple devices
- multiple agent runtimes (Cursor, Codex, Claude Code, OpenClaw)

Publishing to a public hub is often undesirable (privacy, proprietary workflows).

## Goals
1. **Single Source of Truth (SSOT)** in a git repo.
2. **Fast sync** across devices (git pull).
3. **Deterministic consumption** by any agent runtime (stable CLI + strict JSON).
4. **Auditable changes** (diffs, blame, history).

## Non-goals (for now)
- Being a general public skill marketplace (SkillHub exists)
- Solving secret management perfectly (we’ll define clear boundaries first)
- Deep IDE integration (Cursor/VSCode extensions) in v0

## Repository layout
- `facts/` — strict JSON facts (machine readable)
- `bin/syncskl.js` — CLI
- `schemas/` — schemas / validation rules

Planned additions:
- `snippets/` — prompt fragments/instructions (Markdown or txt)
- `skills/` — private scripts (optional)
- `profiles/` — runtime-specific mapping (cursor/codex/claude/openclaw)

## CLI requirements
### Commands
- `syncskl check`
  - validate JSON parse
  - validate required meta fields
  - detect duplicate keys across files
- `syncskl get <key>`
  - output JSON value to stdout
- `syncskl search <query>`
  - return list of matching facts
- `syncskl set <key> --value <json> [--source <text>] [--confidence ...] [--file <path>]`
  - safe write with updated_at

### Output conventions
- Machine-readable JSON for `get` and `search`
- Human-readable status lines for `set` and `check` (OK/ERROR)

## Fact format
Each fact is an atomic key → entry.

```json
{
  "facts": {
    "some.key": {
      "value": {"any": "json"},
      "meta": {
        "source": "where this came from",
        "confidence": "confirmed|likely|tentative",
        "updated_at": "YYYY-MM-DD",
        "expires_at": "optional",
        "tags": ["optional"]
      }
    }
  }
}
```

## Cross-agent integration (planned)
We’ll support exporting/compiling syncskl content into formats different runtimes can consume:
- Cursor rules / project instructions
- Claude Code instructions
- Codex system instructions
- OpenClaw memory + scripts

This likely becomes:
- `syncskl export --target cursor|claude-code|codex|openclaw --profile <name>`

## Secrets policy (planned)
- Default rule: **no secrets in repo**.
- If secrets are needed, store only references (e.g. `env:OPENAI_API_KEY`) and provide documentation.
