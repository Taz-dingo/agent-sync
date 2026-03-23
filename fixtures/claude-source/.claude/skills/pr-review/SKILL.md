---
name: pr-review
description: Review pull requests for correctness, risk, and maintainability. Use when the agent needs to inspect a diff and produce prioritized findings.
---

# PR Review

Review in this order:

1. correctness
2. safety and regression risk
3. maintainability
4. polish

## Rules

- Prefer concrete findings over generic commentary.
- Tie each finding to a specific file or behavior.
- Do not suggest unrelated refactors.
