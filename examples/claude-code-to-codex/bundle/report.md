# Migration Report

## Summary

- source: `claude-code@macbook-pro`
- target: `codex@workstation`

## Applied Changes

- created `target/AGENTS.md` with durable tone, review, and handoff behavior
- created `target/skills/pr-review/SKILL.md` for the reusable review workflow
- preserved durable memory as `bundle/payload/memory.md`
- recorded env var references in `bundle/payload/refs.env.example`

## Skipped Items

- skipped shell aliases because they depend on one workstation layout
- skipped absolute paths because they are machine-specific
- skipped API values because secrets must not be copied
- skipped conversation history because it is transient state

## Follow-up

- review `bundle/payload/memory.md` and merge any still-useful items into the real target memory surface
- replace placeholder env references with target-specific setup docs if needed
