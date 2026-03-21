# syncskl — Plan

## Phase 0 (done)
- [x] Repo structure: facts + CLI
- [x] Minimal validation (`check`)
- [x] get/search/set

## Phase 1 (v0.1) — Make it "feel like a command"
- [ ] Add `package.json` with `bin` entry so `npx syncskl ...` works
- [ ] Add `syncskl` shell shim instructions (optional)
- [ ] Improve errors (exit codes, JSON parse diagnostics)
- [ ] Add `syncskl doctor` to show repo path, node version, fact file count

## Phase 2 (v0.2) — Profiles + Export
- [ ] Add `profiles/` directory
- [ ] Implement `syncskl export --target ...`
  - start with OpenClaw: generate/update `memory/` and/or `USER.md`-like files
  - then Claude Code / Codex / Cursor

## Phase 3 (v0.3) — Snippets & Private skills
- [ ] Add `snippets/` for reusable prompt fragments
- [ ] Add `skills/` for private scripts (not SkillHub)
- [ ] Implement `syncskl apply` for copying/linking files into expected locations

## Phase 4 (v1) — Hardening
- [ ] JSON Schema validation via a real validator (Ajv)
- [ ] Conflict detection + interactive resolution
- [ ] Optional encryption/secrets integration (documented, explicit)
- [ ] CI: `syncskl check` on PR
