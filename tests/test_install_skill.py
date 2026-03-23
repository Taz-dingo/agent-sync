from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class InstallSkillTest(unittest.TestCase):
    def test_default_install_layout_without_extras(self) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        temp_root = Path(tempfile.mkdtemp(prefix="agent-sync-install-"))
        destination = temp_root / "agent-sync"

        try:
            subprocess.run(
                [
                    "python3",
                    str(repo_root / "scripts" / "install_skill.py"),
                    "--dest",
                    str(destination),
                ],
                check=True,
            )

            self.assertTrue((destination / "SKILL.md").exists())
            self.assertTrue((destination / "agents" / "openai.yaml").exists())
            self.assertTrue((destination / "references" / "adaptive-migration-playbook.md").exists())
            self.assertTrue((destination / "scripts" / "init_transfer_bundle.py").exists())
            self.assertTrue((destination / "scripts" / "demo_migrate_claude_to_codex.py").exists())
            self.assertFalse((destination / "examples").exists())
            self.assertFalse((destination / "fixtures").exists())
            self.assertFalse((destination / "tests").exists())
        finally:
            shutil.rmtree(temp_root)

    def test_install_with_extras(self) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        temp_root = Path(tempfile.mkdtemp(prefix="agent-sync-install-extra-"))
        destination = temp_root / "agent-sync"

        try:
            subprocess.run(
                [
                    "python3",
                    str(repo_root / "scripts" / "install_skill.py"),
                    "--dest",
                    str(destination),
                    "--include-extras",
                ],
                check=True,
            )

            self.assertTrue((destination / "README.md").exists())
            self.assertTrue((destination / "examples" / "claude-code-to-codex" / "README.md").exists())
            self.assertTrue((destination / "fixtures" / "claude-source" / ".claude" / "CLAUDE.md").exists())
            self.assertTrue((destination / "tests" / "test_demo_migration.py").exists())
        finally:
            shutil.rmtree(temp_root)


if __name__ == "__main__":
    unittest.main()
