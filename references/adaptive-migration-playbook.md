# Adaptive Migration Playbook

Use this playbook when performing a real migration.

## Principle

Reason from source evidence and target affordances.

Do not start from a prewritten mapping table unless the migration is repetitive enough that the user explicitly wants deterministic automation.

## Step 1: Read The Source

Inspect the actual files that shape behavior.

Ask:

- Which files contain durable instructions?
- Which files contain reusable workflows?
- Which files contain stable memory?
- Which files contain secrets or machine-local state?

## Step 2: Separate Intent From Representation

For each source artifact, ask:

- What behavior does this file create?
- Is that behavior durable or incidental?
- Does the target have a native place for that behavior?

Prefer preserving intent over preserving layout.

## Step 3: Classify

Classify each artifact as one of:

- `portable`
- `portable-with-rewrite`
- `local-only`
- `secret`

## Step 4: Choose Target Surfaces

For each portable behavior, choose the smallest stable target-native surface.

Examples:

- repo-scoped instructions go to `AGENTS.md`
- reusable procedures go to a skill
- durable shared context goes to a memory note
- environment-specific values become references or placeholders

## Step 5: Apply Conservatively

- merge before replacing
- preserve unrelated target content
- keep target-native formatting
- emit a migration note when equivalence is imperfect

## Step 6: Report Clearly

Always report:

- what source evidence you used
- what target files you changed
- what you skipped
- what remains manual

## Evaluation Standard

A migration is successful when:

- the target agent behaves materially closer to the source agent
- secrets were not copied
- machine-specific state did not leak
- the target remains maintainable by humans

A migration is not successful merely because the file tree looks similar.
