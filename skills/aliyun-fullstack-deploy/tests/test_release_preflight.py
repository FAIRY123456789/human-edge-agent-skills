"""Offline tests for release contract and artifact provenance gates."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


release_preflight = load("release_preflight", "release_preflight.py")
build_release = load("build_release", "build_release.py")


class ReleasePreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("frontend/dist/index.html", "<!doctype html>")
        self.write("frontend/package-lock.json", '{"lockfileVersion":3}\n')
        self.write("backend/app.jar", "jar-placeholder\n")
        self.write("flask_model/requirements-production.txt", "Flask==3.1.3\n")
        self.config = {
            "schema_version": 2,
            "project_name": "hnblue",
            "version": "1.2.3",
            "includes": ["frontend/dist", "frontend/package-lock.json", "backend/app.jar", "flask_model/requirements-production.txt"],
            "lockfiles": ["frontend/package-lock.json", "flask_model/requirements-production.txt"],
            "required_files": ["frontend/dist/index.html", "backend/app.jar"],
        }

    def write(self, relative: str, text: str):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_plan_discovers_lock_and_required_file_digests(self):
        config_path = self.root / "release.json"
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        report = release_preflight.preflight(self.root, config_path, None, "plan")
        self.assertEqual(report["overall"], "REVIEW")  # runtime/source evidence is intentionally absent
        self.assertEqual(len(report["lockfiles"]), 2)
        self.assertIn("required_files", report)
        self.assertTrue(all(item["status"] != "BLOCK" for item in report["checks"]))

    def test_missing_lock_file_blocks(self):
        self.config["lockfiles"] = ["frontend/package-lock.json", "frontend/pnpm-lock.yaml"]
        config_path = self.root / "release.json"
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        report = release_preflight.preflight(self.root, config_path, None, "plan")
        self.assertEqual(report["overall"], "BLOCK")
        self.assertIn("Missing lock files", " ".join(item["detail"] for item in report["checks"]))

    def test_ready_refuses_without_runtime_and_source_evidence(self):
        config_path = self.root / "release.json"
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        report = release_preflight.preflight(self.root, config_path, None, "ready")
        self.assertNotEqual(report["overall"], "PASS")
        self.assertEqual(report["checks"][-2]["component"], "runtime_alignment")

    def test_builder_manifest_records_provenance(self):
        config_path = self.root / "release.json"
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        output_root = self.root / "out"
        build_release.build(self.root, config_path, output_root, None, "plan")
        manifest = json.loads((output_root / "hnblue-1.2.3" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 2)
        self.assertEqual(manifest["compatibility"]["overall"], "NOT_RUN")
        self.assertEqual(manifest["lockfiles"], self.config["lockfiles"])
        self.assertTrue(manifest["release_contract_sha256"])

    def test_cli_ready_builder_rejects_without_preflight(self):
        config_path = self.root / "release.json"
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_release.py"), str(self.root), "--config", str(config_path), "--gate", "ready"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ready packaging", result.stderr)


if __name__ == "__main__":
    unittest.main()
