import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/copyright-forge/scripts/render_diagrams.py"


class RenderDiagramTests(unittest.TestCase):
    @unittest.skipIf(shutil.which("dot") is None, "Graphviz dot not installed")
    def test_graphviz_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "architecture.dot"
            source.write_text("digraph A { rankdir=LR; input -> service -> output; }", encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(SCRIPT), "--dot", str(source), "--output-dir", str(root / "out"), "--formats", "svg,png,pdf"],
                capture_output=True, text=True
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            manifest = json.loads((root / "out/architecture.diagram.json").read_text(encoding="utf-8"))
            self.assertEqual([item["format"] for item in manifest["rendered"]], ["svg", "png", "pdf"])
            self.assertIn("<svg", (root / "out/architecture.svg").read_text(encoding="utf-8"))
            self.assertTrue((root / "out/architecture.png").read_bytes().startswith(b"\x89PNG"))
            self.assertTrue((root / "out/architecture.pdf").read_bytes().startswith(b"%PDF"))

    def test_unsupported_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "architecture.dot"
            source.write_text("digraph A {}", encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(SCRIPT), "--dot", str(source), "--output-dir", str(root / "out"), "--formats", "bmp"],
                capture_output=True, text=True
            )
            self.assertNotEqual(process.returncode, 0)
            self.assertIn("only supports", process.stderr)


if __name__ == "__main__":
    unittest.main()
