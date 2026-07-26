"""Safety checks for the agent-followed workshop bootstrap instructions."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SetupDocumentationSafetyTest(unittest.TestCase):
    def test_bootstrap_preserves_existing_workspace(self):
        bootstrap = (ROOT / "BOOTSTRAP.md").read_text(encoding="utf-8")

        self.assertIn("Never delete an existing workspace", bootstrap)
        self.assertIn("timestamped backup", bootstrap)
        self.assertNotIn("delete it first", bootstrap)
        self.assertNotIn("delete the folder", bootstrap)

    def test_archive_fallbacks_use_unique_temp_directories(self):
        bootstrap = (ROOT / "BOOTSTRAP.md").read_text(encoding="utf-8")

        self.assertIn('mktemp -d "${TMPDIR:-/tmp}/unlockai-bootstrap.XXXXXX"', bootstrap)
        self.assertIn("[guid]::NewGuid()", bootstrap)
        self.assertGreaterEqual(bootstrap.count("Cache-Control"), 2)
        self.assertNotIn("/tmp/unlockai.tgz", bootstrap)
        self.assertNotIn('$env:TEMP\\unlockai.zip', bootstrap)


class WindowsSetupDocumentationTest(unittest.TestCase):
    """Windows-specific regressions found in workshop acceptance testing."""

    def test_windows_download_backs_up_before_moving(self):
        """Move-Item onto an existing folder nests the archive inside it instead
        of replacing it, so the backup must happen first, in the block itself."""
        for name in ("BOOTSTRAP.md", "SETUP.md"):
            doc = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(doc=name):
                self.assertIn("-backup-", doc)
                backup_at = doc.index("-backup-")
                move_at = doc.index('Move-Item -LiteralPath (Join-Path $extractPath')
                self.assertLess(backup_at, move_at)

    def test_no_move_item_force_onto_target(self):
        """-Force is what made a re-run silently nest the folder and still
        report success."""
        for name in ("BOOTSTRAP.md", "SETUP.md", "DEBUG.md"):
            doc = (ROOT / name).read_text(encoding="utf-8")
            with self.subTest(doc=name):
                self.assertNotIn('unlockai-social-media" -Force', doc)

    def test_windows_never_uses_tilde_with_git(self):
        """PowerShell does not expand ~ for native programs: `git clone ... ~/x`
        creates a folder literally named ~."""
        setup = (ROOT / "SETUP.md").read_text(encoding="utf-8")
        windows_section = setup[setup.index("**Windows (PowerShell) — if you already have git:**"):]
        self.assertNotIn("~/Downloads", windows_section)
        self.assertIn('Join-Path $HOME "Downloads\\unlockai-social-media"', windows_section)

    def test_setup_offers_a_windows_path_without_git(self):
        setup = (ROOT / "SETUP.md").read_text(encoding="utf-8")
        self.assertIn("**Windows (PowerShell) — no git:**", setup)
        self.assertIn("Expand-Archive", setup)

    def test_windows_helper_scripts_are_documented_and_present(self):
        for script in ("check-setup.ps1", "get-workspace.ps1"):
            with self.subTest(script=script):
                self.assertTrue((ROOT / "windows" / script).is_file())
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("windows/README.md", readme)


if __name__ == "__main__":
    unittest.main()
