#!/usr/bin/env python3
"""Unit tests for read-only generation checks and safe no-bundle output."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build_skills
import compose_persona

class GenerationCheckTests(unittest.TestCase):
    def test_compose_check_requires_exact_rendered_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "out.md"
            rendered = "# Exact\n"
            self.assertFalse(compose_persona.output_matches(p, rendered))
            p.write_text(rendered, encoding="utf-8")
            self.assertTrue(compose_persona.output_matches(p, rendered))
            p.write_text("# Stale\n", encoding="utf-8")
            self.assertFalse(compose_persona.output_matches(p, rendered))

    def test_tree_diff_detects_missing_extra_and_changed_without_writing(self):
        with tempfile.TemporaryDirectory() as td:
            expected, actual = Path(td)/"expected", Path(td)/"actual"
            expected.mkdir(); actual.mkdir()
            (expected/"same").write_text("same")
            (expected/"missing").write_text("expected but absent")
            (expected/"changed").write_text("new")
            (actual/"same").write_text("same")
            (actual/"changed").write_text("old")
            (actual/"extra").write_text("extra")
            before = {p.name: p.read_bytes() for p in actual.iterdir()}
            self.assertEqual(build_skills.tree_differences(expected, actual), (["missing"], ["extra"], ["changed"]))
            self.assertEqual(before, {p.name: p.read_bytes() for p in actual.iterdir()})

    def test_no_bundle_refuses_canonical_outside_and_nonempty_targets(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            canonical = root/"skills"
            self.assertIsNotNone(build_skills.no_bundle_path_error(canonical, root, canonical))
            self.assertIsNotNone(build_skills.no_bundle_path_error(root/"nested"/"out", root, canonical))
            out = root/"skills-unbundled"
            out.mkdir(); (out/"keep.txt").write_text("untouched")
            self.assertIsNotNone(build_skills.no_bundle_path_error(out, root, canonical))
            self.assertEqual((out/"keep.txt").read_text(), "untouched")
            empty = root/"skills-lite"
            empty.mkdir()
            self.assertIsNone(build_skills.no_bundle_path_error(empty, root, canonical))

if __name__ == "__main__":
    unittest.main(verbosity=2)
