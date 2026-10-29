from __future__ import annotations
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "copyright-forge" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from source_safety import InvalidSourcePath, resolve_source

class SourceSafetyTests(unittest.TestCase):
    def test_allow_file_inside_project(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "main.py").write_text("print(1)")
            self.assertEqual(resolve_source(root, "main.py"), root / "main.py")

    def test_reject_parent_directory(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(InvalidSourcePath):
                resolve_source(Path(d), "../outside.py")

    def test_reject_symlink_escape(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "repo"
            root.mkdir()
            external = Path(d) / "secret.py"
            external.write_text("secret")
            (root / "link.py").symlink_to(external)
            with self.assertRaises(InvalidSourcePath):
                resolve_source(root, "link.py")

if __name__ == "__main__":
    unittest.main()
