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


if __name__ == "__main__":
    unittest.main()
