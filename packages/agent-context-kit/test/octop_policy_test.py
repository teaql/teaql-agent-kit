import importlib.util
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


PLUGIN = Path(__file__).resolve().parents[1] / "integrations" / "octop"
spec = importlib.util.spec_from_file_location("octop_read_policy", PLUGIN / "policy.py")
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


@unittest.skipUnless(os.name == "posix", "requires POSIX local filesystem semantics")
class OctopReadPolicyTest(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.root = self.base / "project"
        self.root.mkdir()
        self.excluded = self.root / "generated"
        self.excluded.mkdir()
        self.protected = self.excluded / "private.txt"
        self.protected.write_text("protected file contents")
        self.marker = self.excluded / policy.MARKER

    def test_marker_is_checked_before_reading_and_removed_policy_takes_effect(self):
        self.assertIsNone(policy.read_denial(self.root, str(self.protected)))
        self.marker.write_text("Use docs/api.md")
        reason = policy.read_denial(self.root, str(self.protected))
        self.assertIn("Use docs/api.md", reason)
        self.assertNotIn("protected file contents", reason)
        self.assertIn("Use docs/api.md", policy.read_denial(self.root, str(self.excluded / "missing")))
        self.marker.unlink()
        self.assertIsNone(policy.read_denial(self.root, str(self.protected)))

    def test_symlinks_check_both_ancestors_and_never_read_outside_guidance(self):
        self.marker.write_text("Use docs/api.md")
        alias = self.root / "alias.txt"
        alias.symlink_to(self.protected)
        self.assertIn("Use docs/api.md", policy.read_denial(self.root, str(alias)))
        outside = self.base / "outside"
        outside.mkdir()
        (outside / policy.MARKER).write_text("external marker contents")
        (outside / "file").touch()
        (self.root / "link").symlink_to(outside, target_is_directory=True)
        self.assertEqual(policy.read_denial(self.root, str(self.root / "link/file")), policy.OUTSIDE)
        self.marker.unlink()
        self.marker.symlink_to(outside / policy.MARKER)
        reason = policy.read_denial(self.root, str(self.protected))
        self.assertIn(policy.GUIDANCE, reason)
        self.assertNotIn("external marker contents", reason)

    def test_outer_marker_wins_and_bad_marker_still_denies(self):
        self.marker.write_text("inner guidance")
        outer = self.root / policy.MARKER
        outer.write_bytes(b"\xff")
        reason = policy.read_denial(self.root, str(self.protected))
        self.assertIn(policy.GUIDANCE, reason)
        self.assertNotIn("inner guidance", reason)
        outer.write_text("界" * 800)
        guidance = policy.read_denial(self.root, str(self.protected)).splitlines()[-1]
        self.assertLessEqual(len(guidance.encode()) + len(policy.EXCLUDED), policy.GUIDANCE_BYTES)

    def test_invalid_and_out_of_scope_paths_fail_closed(self):
        for file_path in (None, "generated/private.txt", str(self.root / "../outside"), str(self.base / "outside")):
            with self.subTest(file_path=file_path):
                self.assertEqual(policy.read_denial(self.root, file_path), policy.OUTSIDE)
        self.assertEqual(policy.read_denial(self.root, str(self.root / "missing")), policy.UNVERIFIED)
