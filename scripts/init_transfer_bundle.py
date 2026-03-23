#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


MANIFEST = """source: {source}
target: {target}
status: draft
"""

INVENTORY = """# Inventory

## Source surfaces

- 

## Portable items

- 

## Local-only items

- 

## Secrets and references

- 
"""

MAPPINGS = """# Mappings

## Identity

- source:
- target:

## Operating Rules

- source:
- target:

## Workflows

- source:
- target:

## Skills

- source:
- target:

## Memory

- source:
- target:
"""

REPORT = """# Migration Report

## Summary

- source: {source}
- target: {target}

## Applied Changes

- 

## Skipped Items

- 

## Follow-up

- 
"""

PAYLOAD_FILES = {
    "identity.md": "# Identity\n\n- \n",
    "operating-rules.md": "# Operating Rules\n\n- \n",
    "workflows.md": "# Workflows\n\n- \n",
    "memory.md": "# Memory\n\n- \n",
    "refs.env.example": "# Example references only\n# API_KEY=env:API_KEY\n",
}


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a temporary source-target transfer bundle.")
    parser.add_argument("output_dir", help="Directory to create for the working bundle")
    parser.add_argument("--source", default="unknown-source", help="Source label")
    parser.add_argument("--target", default="unknown-target", help="Target label")
    args = parser.parse_args()

    root = Path(args.output_dir).expanduser().resolve()
    payload = root / "payload"
    skills = payload / "skills"

    root.mkdir(parents=True, exist_ok=True)
    payload.mkdir(parents=True, exist_ok=True)
    skills.mkdir(parents=True, exist_ok=True)

    write_file(root / "manifest.yaml", MANIFEST.format(source=args.source, target=args.target))
    write_file(root / "inventory.md", INVENTORY)
    write_file(root / "mappings.md", MAPPINGS)
    write_file(root / "report.md", REPORT.format(source=args.source, target=args.target))

    for name, content in PAYLOAD_FILES.items():
        write_file(payload / name, content)

    print(f"Created transfer bundle at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
