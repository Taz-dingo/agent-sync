from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class DemoMigrationTest(unittest.TestCase):
    def test_claude_fixture_migrates_to_codex_outputs(self) -> None:
        repo_root = Path(__file__).resolve().parent.parent
        source_dir = repo_root / "fixtures" / "claude-source"
        work_dir = Path(tempfile.mkdtemp(prefix="agent-sync-test-"))
        output_dir = work_dir / "run"

        try:
            subprocess.run(
                [
                    "python3",
                    str(repo_root / "scripts" / "demo_migrate_claude_to_codex.py"),
                    str(source_dir),
                    str(output_dir),
                ],
                check=True,
            )

            agents_md = (output_dir / "target" / "AGENTS.md").read_text(encoding="utf-8")
            report_md = (output_dir / "bundle" / "report.md").read_text(encoding="utf-8")
            refs_env = (output_dir / "bundle" / "payload" / "refs.env.example").read_text(encoding="utf-8")
            memory_md = (output_dir / "bundle" / "payload" / "memory.md").read_text(encoding="utf-8")
            skill_md = (output_dir / "target" / "skills" / "pr-review" / "SKILL.md").read_text(encoding="utf-8")

            self.assertIn("Be concise, direct, and pragmatic.", agents_md)
            self.assertIn("Review correctness first.", agents_md)
            self.assertIn("End with one concrete next manual step when relevant.", agents_md)

            self.assertIn("ANTHROPIC_API_KEY=env:ANTHROPIC_API_KEY", refs_env)
            self.assertIn("GITHUB_TOKEN=env:GITHUB_TOKEN", refs_env)
            self.assertNotIn("sk-ant-demo-secret", refs_env)
            self.assertNotIn("ghp_demo_secret", refs_env)

            self.assertIn("Team prefers short imperative commit messages.", memory_md)
            self.assertIn("name: pr-review", skill_md)
            self.assertIn("skipped `alias proj='cd /Users/alex/src/client-app'` because it is machine-specific", report_md)
            self.assertIn("skipped value for `ANTHROPIC_API_KEY` because secrets must not be copied", report_md)
            self.assertNotIn("/Users/alex/src/client-app", agents_md)
        finally:
            shutil.rmtree(work_dir)


if __name__ == "__main__":
    unittest.main()
