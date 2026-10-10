#!/usr/bin/env python3
"""Read-only release contract and ECS version-alignment gate.

The command discovers source provenance, checks declared lock/required files,
and evaluates a supplied runtime snapshot. It never installs, migrates,
promotes, edits a host, or connects to a database.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path

SAFE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def inside(root: Path, raw: str) -> Path:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise ValueError(f"path must be a non-empty project-relative POSIX path: {raw!r}")
    path = (root / raw).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes project root: {raw}") from exc
    return path


def covered(root: Path, includes: list[str], raw: str) -> bool:
    target = inside(root, raw)
    for item in includes:
        source = inside(root, item)
        if source == target:
            return True
        if source.is_dir():
            try:
                target.relative_to(source)
                return True
            except ValueError:
                pass
    return False


def revision(root: Path) -> dict:
    try:
        result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return {"value": None, "source": "unavailable"}
    value = result.stdout.strip()
    return {"value": value or None, "source": "git" if result.returncode == 0 and value else "unavailable"}


def runtime_module():
    path = Path(__file__).with_name("runtime_matrix.py")
    spec = importlib.util.spec_from_file_location("aliyun_runtime_matrix", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load runtime_matrix.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def preflight(root: Path, config_path: Path, server_path: Path | None, gate: str) -> dict:
    config = json_object(config_path)
    checks = []

    def add(component: str, status: str, detail: str, remedy: str = ""):
        checks.append({"component": component, "status": status, "detail": detail, "remedy": remedy})

    schema = config.get("schema_version", 1)
    if schema not in (1, 2):
        add("release_schema", "BLOCK", f"Unsupported schema_version={schema}.", "Use schema_version 2.")
    else:
        add("release_schema", "PASS", f"Release contract schema_version={schema}.")

    name, version = config.get("project_name"), config.get("version")
    if not isinstance(name, str) or not SAFE.fullmatch(name) or not isinstance(version, str) or not SAFE.fullmatch(version):
        add("release_identity", "BLOCK", "project_name/version is missing or unsafe.", "Use safe release labels.")
    elif gate == "ready" and not SEMVER.fullmatch(version):
        add("release_identity", "BLOCK", f"Ready releases require SemVer; got {version!r}.")
    else:
        add("release_identity", "PASS", f"{name} {version} is a safe release identity.")

    includes = config.get("includes")
    if not isinstance(includes, list) or not includes:
        includes = []
        add("release_inputs", "BLOCK", "includes must be a non-empty list.")
    missing = []
    for raw in includes:
        try:
            if not inside(root, raw).exists():
                missing.append(raw)
        except ValueError as exc:
            add("release_inputs", "BLOCK", str(exc))
    if missing:
        add("release_inputs", "BLOCK", "Missing release inputs: " + ", ".join(missing), "Build artifacts before packaging.")
    elif includes:
        add("release_inputs", "PASS", f"{len(includes)} release inputs exist inside the project root.")

    lockfiles = config.get("lockfiles", [])
    if not isinstance(lockfiles, list):
        lockfiles = []
        add("lockfiles", "BLOCK", "lockfiles must be a list.")
    lock_digests, missing_locks, uncovered_locks = {}, [], []
    for raw in lockfiles:
        try:
            path = inside(root, raw)
            if not path.is_file():
                missing_locks.append(raw)
            else:
                lock_digests[raw] = sha256(path)
                if not covered(root, includes, raw):
                    uncovered_locks.append(raw)
        except ValueError as exc:
            add("lockfiles", "BLOCK", str(exc))
    if missing_locks:
        add("lockfiles", "BLOCK", "Missing lock files: " + ", ".join(missing_locks), "Generate and commit lock files.")
    elif uncovered_locks:
        add("lockfiles", "BLOCK", "Lock files not included: " + ", ".join(uncovered_locks), "Include every lock file.")
    elif lockfiles:
        add("lockfiles", "PASS", f"{len(lockfiles)} lock files exist, are hashed and are included.")
    else:
        add("lockfiles", "REVIEW", "No explicit lockfiles declared.", "Declare frontend/Python lock or provenance files.")

    required = config.get("required_files", [])
    if not isinstance(required, list):
        required = []
        add("required_files", "BLOCK", "required_files must be a list.")
    missing_required, uncovered_required = [], []
    for raw in required:
        try:
            path = inside(root, raw)
            if not path.is_file():
                missing_required.append(raw)
            elif not covered(root, includes, raw):
                uncovered_required.append(raw)
        except ValueError as exc:
            add("required_files", "BLOCK", str(exc))
    if missing_required:
        add("required_files", "BLOCK", "Missing required files: " + ", ".join(missing_required))
    elif uncovered_required:
        add("required_files", "BLOCK", "Required files not included: " + ", ".join(uncovered_required))
    elif required:
        add("required_files", "PASS", f"{len(required)} required files exist and are included.")

    contract = {}
    contract_path = config.get("runtime_contract")
    if contract_path:
        try:
            contract = json_object(inside(root, contract_path))
            add("runtime_contract", "PASS", f"Loaded non-secret runtime contract {contract_path}.")
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            add("runtime_contract", "BLOCK", str(exc))
    else:
        add("runtime_contract", "REVIEW", "No runtime_contract declared.", "Declare Java/Python/frontend/database requirements.")

    runtime_report = None
    report_path = config.get("runtime_report")
    if server_path:
        if not contract:
            add("runtime_alignment", "BLOCK", "ECS snapshot supplied without a valid runtime contract.")
        else:
            try:
                runtime_report = runtime_module().generate(root, contract, json_object(server_path))
                state = runtime_report["overall"]
                add("runtime_alignment", "PASS" if state == "PASS" else state, f"Runtime matrix overall={state}; inspect every check.")
            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
                add("runtime_alignment", "BLOCK", f"Unable to evaluate ECS snapshot: {exc}")
    elif report_path:
        try:
            runtime_report = json_object(inside(root, report_path))
            state = runtime_report.get("overall", "REVIEW")
            add("runtime_alignment", "PASS" if state == "PASS" else state, f"Loaded recorded runtime matrix overall={state}.")
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            add("runtime_alignment", "BLOCK", str(exc))
    else:
        add("runtime_alignment", "REVIEW", "No ECS snapshot or runtime report supplied.", "Collect a redacted read-only probe before ready packaging.")

    discovered = revision(root)
    expected = config.get("source_revision")
    if expected and discovered["value"] and expected != discovered["value"]:
        add("source_revision", "BLOCK", "Configured source_revision does not match worktree HEAD.")
    elif discovered["value"]:
        add("source_revision", "PASS", f"Source revision discovered: {discovered['value']}.")
    else:
        add("source_revision", "REVIEW", "Git source revision could not be discovered.", "Build from a Git worktree and record the commit SHA.")

    counts = {state: sum(item["status"] == state for item in checks) for state in ("PASS", "ACTION_REQUIRED", "REVIEW", "BLOCK")}
    overall = next((state for state in ("BLOCK", "ACTION_REQUIRED", "REVIEW") if counts[state]), "PASS")
    return {"schema_version": 1, "gate": gate, "overall": overall, "counts": counts,
            "project_name": name, "version": version, "source_revision": discovered,
            "lockfiles": lock_digests, "required_files": required, "runtime_report": runtime_report,
            "checks": checks, "read_only": True,
            "note": "Evidence gate only; it does not install, migrate, promote or roll back anything."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--server", type=Path)
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--gate", choices=("plan", "ready"), default="plan")
    args = parser.parse_args()
    root = args.project_root.resolve()
    config = args.config.resolve() if args.config.is_absolute() else (root / args.config).resolve()
    server = args.server.resolve() if args.server else None
    if not root.is_dir():
        parser.error(f"project root is missing: {root}")
    if server and not server.is_file():
        parser.error(f"server snapshot is missing: {server}")
    try:
        report = preflight(root, config, server, args.gate)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output + "\n", encoding="utf-8", newline="\n")
    return 0 if (args.gate == "ready" and report["overall"] == "PASS") or (args.gate == "plan" and report["overall"] != "BLOCK") else 2


if __name__ == "__main__":
    raise SystemExit(main())
