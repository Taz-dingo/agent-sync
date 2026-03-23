#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path


WORKING_STYLE_HEADER = "## Working Style"
CODE_REVIEW_HEADER = "## Code Review"
HANDOFF_HEADER = "## Handoff"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section_bullets(markdown: str, header: str) -> list[str]:
    if header not in markdown:
        return []
    remainder = markdown.split(header, 1)[1]
    next_header = remainder.find("\n## ")
    block = remainder if next_header == -1 else remainder[:next_header]
    return [line[2:].strip() for line in block.splitlines() if line.startswith("- ")]


def parse_secret_refs(env_text: str) -> list[str]:
    refs: list[str] = []
    for line in env_text.splitlines():
        match = re.match(r"\s*export\s+([A-Z0-9_]+)=(.*)", line)
        if not match:
            continue
        name = match.group(1)
        if any(token in name for token in ["KEY", "TOKEN", "SECRET", "PASSWORD"]):
            refs.append(name)
    return refs


def parse_local_only(zshrc_text: str) -> list[str]:
    local_only: list[str] = []
    for line in zshrc_text.splitlines():
        if "/Users/" in line or "alias " in line:
            local_only.append(line.strip())
    return local_only


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a demo Claude Code -> Codex migration.")
    parser.add_argument("source_dir", help="Fixture source directory")
    parser.add_argument("output_dir", help="Directory where bundle and target will be created")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    source_root = Path(args.source_dir).expanduser().resolve()
    output_root = Path(args.output_dir).expanduser().resolve()
    bundle_root = output_root / "bundle"
    target_root = output_root / "target"

    claude_md = source_root / ".claude" / "CLAUDE.md"
    memory_md = source_root / ".claude" / "memory" / "team-preferences.md"
    skill_md = source_root / ".claude" / "skills" / "pr-review" / "SKILL.md"
    zshrc = source_root / ".zshrc"
    env_exports = source_root / ".env.exports"

    required = [claude_md, memory_md, skill_md, zshrc, env_exports]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"Missing required source files: {', '.join(missing)}")

    subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "init_transfer_bundle.py"),
            str(bundle_root),
            "--source",
            "claude-code-fixture",
            "--target",
            "codex-fixture",
        ],
        check=True,
    )

    claude_text = read_text(claude_md)
    memory_text = read_text(memory_md)
    skill_text = read_text(skill_md)
    zshrc_text = read_text(zshrc)
    env_text = read_text(env_exports)

    working_style = section_bullets(claude_text, WORKING_STYLE_HEADER)
    code_review = section_bullets(claude_text, CODE_REVIEW_HEADER)
    handoff = section_bullets(claude_text, HANDOFF_HEADER)
    local_only = parse_local_only(zshrc_text)
    secret_refs = parse_secret_refs(env_text)
    memory_items = [line[2:].strip() for line in memory_text.splitlines() if line.startswith("- ")]

    inventory = f"""# Inventory

## Source surfaces

- `{claude_md}` contains durable tone, review, and handoff behavior.
- `{memory_md}` contains stable team preferences.
- `{skill_md}` contains a reusable review workflow.
- `{zshrc}` contains aliases and machine-bound paths.
- `{env_exports}` contains secret-bearing environment exports.

## Portable items

{bullets(working_style + code_review + handoff + memory_items + ['Reusable pr-review skill'])}

## Local-only items

{bullets(local_only)}

## Secrets and references

{bullets([f'Keep {name} as an env reference only' for name in secret_refs])}
"""
    write(bundle_root / "inventory.md", inventory + "\n")

    mappings = f"""# Mappings

## Identity

- source: concise and direct collaboration tone from `{claude_md}`
- target: `target/AGENTS.md`

## Operating Rules

- source: working style and code review sections from `{claude_md}`
- target: `target/AGENTS.md`

## Workflows

- source: handoff section from `{claude_md}`
- target: `target/AGENTS.md`

## Skills

- source: `{skill_md}`
- target: `target/skills/pr-review/SKILL.md`

## Memory

- source: `{memory_md}`
- target: `bundle/payload/memory.md`
"""
    write(bundle_root / "mappings.md", mappings)

    write(bundle_root / "payload" / "identity.md", "# Identity\n\n" + bullets(working_style[:2]) + "\n")
    write(bundle_root / "payload" / "operating-rules.md", "# Operating Rules\n\n" + bullets(working_style + code_review) + "\n")
    write(bundle_root / "payload" / "workflows.md", "# Workflows\n\n" + bullets(handoff) + "\n")
    write(bundle_root / "payload" / "memory.md", "# Memory\n\n" + bullets(memory_items) + "\n")
    write(
        bundle_root / "payload" / "refs.env.example",
        "# Example references only\n" + "\n".join(f"{name}=env:{name}" for name in secret_refs) + "\n",
    )

    agents_md = "# AGENTS.md\n\n## Working Style\n\n" + bullets(working_style) + "\n\n## Code Review\n\n" + bullets(code_review) + "\n\n## Handoff\n\n" + bullets(handoff) + "\n"
    write(target_root / "AGENTS.md", agents_md)
    write(target_root / "skills" / "pr-review" / "SKILL.md", skill_text)

    report_lines = [
        "# Migration Report",
        "",
        "## Summary",
        "",
        "- source: `claude-code-fixture`",
        "- target: `codex-fixture`",
        "",
        "## Applied Changes",
        "",
        "- created `target/AGENTS.md` from durable Claude instructions",
        "- copied reusable review skill into `target/skills/pr-review/SKILL.md`",
        "- preserved stable team preferences in `bundle/payload/memory.md`",
        "- recorded secret references in `bundle/payload/refs.env.example`",
        "",
        "## Skipped Items",
        "",
    ]
    report_lines.extend(f"- skipped `{item}` because it is machine-specific" for item in local_only)
    report_lines.extend(f"- skipped value for `{name}` because secrets must not be copied" for name in secret_refs)
    report_lines.extend([
        "",
        "## Follow-up",
        "",
        "- review `bundle/payload/memory.md` before merging it into a real target memory surface",
    ])
    write(bundle_root / "report.md", "\n".join(report_lines) + "\n")

    print(f"Migrated fixture from {source_root} to {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
