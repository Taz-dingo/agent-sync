# syncskl — Vision

syncskl exists to make **personal, private, highly customized agent/skill behavior** portable.

Not everything should be published to SkillHub:
- private preferences (naming, tone, habits)
- environment-specific defaults (paths, tools, SSH hosts)
- proprietary workflows
- “glue code” between tools (Cursor / Codex / Claude Code / OpenClaw)

**Vision:**
> A single, auditable source of truth that can be synced across devices and injected into any agent runtime.

## What we’re syncing
We sync **behavioral configuration** for agents, expressed as:
- **Facts (SSOT):** strict, machine-readable settings (JSON)
- **Prompts/snippets:** reusable instruction blocks (optional, later)
- **Local skills (private):** scripts and helper tools that shouldn’t be public

## What success looks like
- New machine setup goes from 0 → “feels like home” in minutes.
- Any agent (Cursor, Codex, Claude Code, OpenClaw) can pull the same preferences.
- Changes are versioned and reversible (git).
- Sync is safe: secrets handled deliberately, not accidentally.
