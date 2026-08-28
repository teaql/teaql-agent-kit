import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "tools" / "teaql_workspace.py"
LANGUAGES = ("java", "rust", "golang", "typescript", "swift", "dotnet", "python")


class WorkspaceSourceTest(unittest.TestCase):
    def test_release_mode_accepts_versions_and_rejects_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            runtimes = {name: {"package": name, "version": "1.0.0"} for name in LANGUAGES}
            config = root / "teaql-workspace.yaml"
            config.write_text(json.dumps({"schemaVersion": 1, "runtimeSource": "release", "runtimes": runtimes}))
            ok = subprocess.run([str(SCRIPT), "verify", "--config", str(config)], capture_output=True, text=True)
            self.assertEqual(0, ok.returncode, ok.stderr)
            runtimes["rust"]["path"] = "../teaql-rs"
            config.write_text(json.dumps({"schemaVersion": 1, "runtimeSource": "release", "runtimes": runtimes}))
            bad = subprocess.run([str(SCRIPT), "verify", "--config", str(config)], capture_output=True, text=True)
            self.assertEqual(1, bad.returncode)
            self.assertIn("release mode forbids path overrides", bad.stderr)

    def test_workspace_mode_records_git_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "runtime"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            (repo / "README").write_text("runtime\n")
            subprocess.run(["git", "-C", str(repo), "add", "README"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "init"], check=True)
            runtimes = {name: {"path": "runtime", "version": "dev"} for name in LANGUAGES}
            config = root / "teaql-workspace.yaml"
            config.write_text(json.dumps({"schemaVersion": 1, "runtimeSource": "workspace", "runtimes": runtimes}))
            result = subprocess.run([str(SCRIPT), "apply", "--config", str(config), "--workspace", str(root)], capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            evidence = json.loads((root / ".teaql/runtime-source-evidence.json").read_text())
            self.assertEqual("workspace", evidence["runtimeSource"])
            self.assertFalse(evidence["runtimes"]["java"]["dirty"])
            self.assertEqual(40, len(evidence["runtimes"]["rust"]["commit"]))


if __name__ == "__main__":
    unittest.main()
