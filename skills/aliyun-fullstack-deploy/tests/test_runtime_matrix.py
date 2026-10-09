"""Offline regression tests for Java/Flask/Vue runtime compatibility gating."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("runtime_matrix", ROOT / "scripts/runtime_matrix.py")
runtime_matrix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime_matrix)


class RuntimeMatrixTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        def write(path, text):
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8")
        self.write = write
        write("backend/pom.xml",
              '<project xmlns="http://maven.apache.org/POM/4.0.0">'
              '<properties><java.version>17</java.version></properties></project>')
        write("flask_model/carbon_model_api/requirements-production.txt",
              "-r requirements.txt\ngunicorn==23.0.0\n")
        write("flask_model/carbon_model_api/requirements.txt",
              "Flask==3.1.3\ncatboost==1.2.10\n")
        write("frontend/package.json", '{"name":"demo","scripts":{"build":"vue-cli-service build"}}')
        write("frontend/package-lock.json", '{"lockfileVersion":3}')
        write("frontend/dist/index.html", "<!doctype html>")
        write("flask_model/carbon_model_api/model.pkl", "fake-test-artifact")
        self.contract = {
            "java": {"major": 17, "pom": "backend/pom.xml"},
            "python": {"version": "3.11",
                       "requirements": "flask_model/carbon_model_api/requirements-production.txt"},
            "frontend": {"build": "local"},
            "mysql": {"major": 8},
            "redis": {"major": 7},
            "model_artifacts": ["flask_model/carbon_model_api/*.pkl"]
        }
        self.server = {
            "runtimes": {
                "java": {"version": "17.0.12", "source": "binary"},
                "python": {"version": "3.11.9", "source": "interpreter"},
                "node": {"version": None, "source": "binary"},
                "mysql": {"version": "8.0.39", "source": "server_query"},
                "redis": {"version": "7.4.1", "source": "server_query"}},
            "packages": {"flask": "3.1.3", "catboost": "1.2.10", "gunicorn": "23.0.0"},
            "validation": {"model_smoke_passed": True}
        }

    def checks(self):
        return {c["component"]: c for c in runtime_matrix.generate(
            self.root, self.contract, self.server)["checks"]}

    def test_hnblue_layout_all_runtime_checks_pass_with_evidence(self):
        report = runtime_matrix.generate(self.root, self.contract, self.server)
        self.assertEqual(report["overall"], "PASS")
        self.assertEqual(self.checks()["frontend"]["status"], "PASS")
        self.assertEqual(self.checks()["python_packages"]["status"], "PASS")
        self.assertIn("ECS Node.js is not required", self.checks()["frontend"]["detail"])

    def test_old_java_python_and_missing_packages_need_adaptation(self):
        self.server["runtimes"]["java"]["version"] = "11.0.18"
        self.server["runtimes"]["python"]["version"] = "3.6.8"
        self.server["packages"] = {}
        checks = self.checks()
        self.assertEqual(checks["java"]["status"], "ACTION_REQUIRED")
        self.assertEqual(checks["python"]["status"], "ACTION_REQUIRED")
        self.assertEqual(checks["python_packages"]["status"], "ACTION_REQUIRED")

    def test_binary_database_versions_are_not_server_proof(self):
        self.server["runtimes"]["mysql"]["source"] = "binary"
        self.server["runtimes"]["redis"]["source"] = "binary"
        checks = self.checks()
        self.assertEqual(checks["mysql"]["status"], "REVIEW")
        self.assertEqual(checks["redis"]["status"], "REVIEW")

    def test_missing_or_unverified_model_never_passes_silently(self):
        self.server["validation"]["model_smoke_passed"] = False
        self.assertEqual(self.checks()["model_artifacts"]["status"], "REVIEW")
        (self.root / "flask_model/carbon_model_api/model.pkl").unlink()
        self.assertEqual(self.checks()["model_artifacts"]["status"], "BLOCK")

    def test_unknown_python_contract_requires_review(self):
        self.contract["python"].pop("version")
        self.assertEqual(self.checks()["python"]["status"], "REVIEW")

    def test_server_missing_node_is_valid_when_dist_is_ready(self):
        self.assertEqual(self.checks()["frontend"]["status"], "PASS")
        (self.root / "frontend/dist/index.html").unlink()
        self.assertEqual(self.checks()["frontend"]["status"], "ACTION_REQUIRED")

    def test_unpinned_requirements_are_reported(self):
        self.write("flask_model/carbon_model_api/requirements.txt", "Flask>=3\ncatboost==1.2.10")
        self.assertEqual(self.checks()["python_unpinned"]["status"], "REVIEW")

    def test_requirement_path_escape_is_blocked(self):
        self.write("flask_model/carbon_model_api/requirements-production.txt", "-r ../../../outside.txt")
        with self.assertRaises(ValueError):
            self.checks()

    def test_cli_ready_gate_returns_nonzero_for_unverified_model(self):
        contract = self.root / "contract.json"
        server = self.root / "server.json"
        contract.write_text(json.dumps(self.contract), encoding="utf-8")
        self.server["validation"]["model_smoke_passed"] = False
        server.write_text(json.dumps(self.server), encoding="utf-8")
        cmd = [sys.executable, str(ROOT / "scripts/runtime_matrix.py"), str(self.root),
               "--contract", str(contract), "--server", str(server), "--gate", "ready"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["overall"], "REVIEW")

    def test_probe_has_no_full_package_inventory_by_default(self):
        cmd = [sys.executable, str(ROOT / "scripts/probe_runtime.py"), "--python-bin", sys.executable]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = json.loads(result.stdout)
        self.assertEqual(profile["packages"], {})
        self.assertEqual(profile["runtimes"]["python"]["available"], True)
        self.assertNotIn("password", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
