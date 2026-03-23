#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

CORE_FILES = [
    "SKILL.md",
    "agents",
    "references",
    "scripts/init_transfer_bundle.py",
    "scripts/demo_migrate_claude_to_codex.py",
]

EXTRA_FILES = [
    "README.md",
    "examples",
    "fixtures",
    "tests",
]


def codex_home() -> Path:
    value = os.environ.get("CODEX_HOME")
    if value:
        return Path(value).expanduser().resolve()
    return Path.home() / ".codex"


def copy_entry(repo_root: Path, destination_root: Path, relative: str) -> None:
    source = repo_root / relative
    destination = destination_root / relative
    if not source.exists():
        return
    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the agent-sync skill into a Codex skills directory.")
    parser.add_argument("--dest", help="Install destination. Defaults to $CODEX_HOME/skills/agent-sync")
    parser.add_argument("--skill-name", default="agent-sync", help="Installed folder name")
    parser.add_argument("--include-extras", action="store_true", help="Also copy README, examples, fixtures, and tests")
    parser.add_argument("--force", action="store_true", help="Replace an existing install directory")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    install_root = Path(args.dest).expanduser().resolve() if args.dest else codex_home() / "skills" / args.skill_name

    if install_root.exists() and not args.force:
        raise SystemExit(f"Destination already exists: {install_root}\nUse --force to replace it.")

    if install_root.exists() and args.force:
        shutil.rmtree(install_root)

    install_root.mkdir(parents=True, exist_ok=True)

    for relative in CORE_FILES:
        copy_entry(repo_root, install_root, relative)

    if args.include_extras:
        for relative in EXTRA_FILES:
            copy_entry(repo_root, install_root, relative)

    print(f"Installed agent-sync to {install_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
