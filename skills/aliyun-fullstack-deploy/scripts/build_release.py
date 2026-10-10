#!/usr/bin/env python3
"""Build a deterministic, Linux-compatible release directory and ZIP from JSON config."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import shutil
import stat
import subprocess
import sys
import zipfile
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_EXCLUDES = {"node_modules", "__pycache__"}
TEXT_SUFFIXES = {".sh", ".service", ".conf", ".example", ".py", ".js", ".ts", ".tsx", ".json", ".md"}
SAFE_LABEL = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,79}$")
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ignored(excludes: set[str]):
    def callback(_directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name.startswith(".") or any(fnmatch.fnmatch(name, pattern) for pattern in excludes) or name.endswith((".pyc", ".pyo"))
        }
    return callback


def safe_reset(target: Path, output_root: Path) -> None:
    target_resolved = target.resolve()
    root_resolved = output_root.resolve()
    if target_resolved.parent != root_resolved or target_resolved == root_resolved:
        raise RuntimeError(f"unsafe release target: {target_resolved}")
    if target.exists():
        def remove_readonly(function, path, _error_info):
            Path(path).chmod(stat.S_IWRITE | stat.S_IREAD)
            function(path)

        shutil.rmtree(target, onerror=remove_readonly)


def assert_contained_tree(source: Path, root: Path) -> None:
    candidates = [source]
    if source.is_dir():
        candidates.extend(source.rglob("*"))
    for candidate in candidates:
        try:
            candidate.resolve().relative_to(root)
        except ValueError as error:
            raise ValueError(f"release input resolves outside project root: {candidate}") from error


def safe_relative(root: Path, raw: str) -> Path:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise ValueError(f"path must be a non-empty project-relative POSIX path: {raw!r}")
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"path escapes project root: {raw}") from error
    return candidate


def covered(root: Path, includes: list[str], raw: str) -> bool:
    target = safe_relative(root, raw)
    for item in includes:
        source = safe_relative(root, item)
        if source == target:
            return True
        if source.is_dir():
            try:
                target.relative_to(source)
                return True
            except ValueError:
                pass
    return False


def worktree_revision(root: Path) -> str | None:
    try:
        result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    value = result.stdout.strip()
    return value if result.returncode == 0 and value else None


def verify_contract(root: Path, config: dict, gate: str, preflight_arg: Path | None) -> dict:
    """Check reproducibility controls before resetting the staging directory."""
    schema = config.get("schema_version", 1)
    if schema not in (1, 2):
        raise ValueError(f"unsupported release contract schema_version={schema}")
    includes = config.get("includes")
    if not isinstance(includes, list) or not includes:
        raise ValueError("includes must be a non-empty list of project-relative paths")
    for item in includes:
        safe_relative(root, item)
    for label in ("lockfiles", "required_files"):
        entries = config.get(label, [])
        if not isinstance(entries, list):
            raise ValueError(f"{label} must be a list")
        for item in entries:
            path = safe_relative(root, item)
            if not path.is_file():
                raise FileNotFoundError(f"{label} entry missing: {item}")
            if not covered(root, includes, item):
                raise ValueError(f"{label} entry is not included: {item}")

    preflight_path = preflight_arg
    if preflight_path is None and config.get("preflight_report"):
        preflight_path = safe_relative(root, config["preflight_report"])
    if preflight_path and not preflight_path.is_absolute():
        preflight_path = (root / preflight_path).resolve()
    preflight = None
    if preflight_path:
        if not preflight_path.is_file():
            if gate == "ready":
                raise FileNotFoundError(f"preflight report missing: {preflight_path}")
        else:
            preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
            if gate == "ready" and preflight.get("overall") != "PASS":
                raise ValueError(f"preflight gate is {preflight.get('overall', 'UNKNOWN')}; ready requires PASS")
    elif gate == "ready":
        raise ValueError("ready packaging requires --preflight-report or config.preflight_report")
    expected = config.get("source_revision")
    actual = worktree_revision(root)
    if expected and actual and expected != actual:
        raise ValueError("configured source_revision does not match worktree HEAD")
    if gate == "ready" and not (expected or actual):
        raise ValueError("ready packaging requires a discovered or configured source revision")
    return {"schema_version": schema, "preflight_path": str(preflight_path) if preflight_path else None,
            "preflight": preflight, "source_revision": actual or expected,
            "lockfiles": list(config.get("lockfiles", [])), "required_files": list(config.get("required_files", []))}


def build(project_root: Path, config_arg: Path, output_arg: Path | None = None,
          preflight_arg: Path | None = None, gate: str = "plan") -> Path:
    """Build one release and return its staging directory."""
    root = project_root.resolve()
    config_path = config_arg if config_arg.is_absolute() else root / config_arg
    config = json.loads(config_path.read_text(encoding="utf-8"))
    name = config["project_name"]
    version = config["version"]
    if not isinstance(name, str) or not SAFE_LABEL.fullmatch(name):
        raise ValueError("project_name must be a safe 1-80 character label")
    if not isinstance(version, str) or not SAFE_LABEL.fullmatch(version):
        raise ValueError("version must be a safe 1-80 character label")
    if gate == "ready" and not SEMVER.fullmatch(version):
        raise ValueError("ready packaging requires a SemVer version")
    contract = verify_contract(root, config, gate, preflight_arg)
    package_name = f"{name}-{version}"
    output_root = (output_arg or root / "release").resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    staging = output_root / package_name
    zip_path = output_root / f"{package_name}.zip"
    safe_reset(staging, output_root)
    staging.mkdir()
    excludes = DEFAULT_EXCLUDES | set(config.get("excludes", []))

    includes = config.get("includes")
    if not isinstance(includes, list) or not includes:
        raise ValueError("includes must be a non-empty list of project-relative paths")
    for relative in includes:
        if not isinstance(relative, str) or not relative or "\\" in relative:
            raise ValueError(f"release input must be a forward-slash relative path: {relative!r}")
        source = (root / relative).resolve()
        try:
            source.relative_to(root)
        except ValueError as error:
            raise ValueError(f"release input escapes project root: {relative}") from error
        if not source.exists():
            raise FileNotFoundError(f"release input missing: {relative}")
        assert_contained_tree(source, root)
        destination = staging / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination, ignore=ignored(excludes))
        else:
            shutil.copy2(source, destination)

    for path in staging.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8-sig")
        path.write_text(text.replace("\r\n", "\n").replace("\r", "\n"), encoding="utf-8", newline="\n")
        if path.suffix == ".sh":
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    notes = staging / "RELEASE_NOTES.md"
    if not notes.exists():
        notes.write_text(f"# {package_name}\n\nBuilt for audited canary deployment and atomic promotion.\n", encoding="utf-8", newline="\n")

    entries = []
    for path in sorted(staging.rglob("*")):
        if path.is_file() and path.name not in {"manifest.json", "checksums.sha256"}:
            entries.append({"path": path.relative_to(staging).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    contract_digest = sha256(config_path)
    evidence = {}
    if contract["preflight_path"] and Path(contract["preflight_path"]).is_file():
        evidence["preflight_report_sha256"] = sha256(Path(contract["preflight_path"]))
    manifest = {
        "schema_version": 2,
        "project_name": name,
        "version": version,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_revision": contract["source_revision"],
        "release_contract_sha256": contract_digest,
        "lockfiles": contract["lockfiles"],
        "required_files": contract["required_files"],
        "evidence": evidence,
        "compatibility": {"gate": gate, "overall": (contract["preflight"] or {}).get("overall", "NOT_RUN"), "read_only": True},
        "files": entries,
    }
    manifest_path = staging / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    checksum_entries = entries + [{"path": "manifest.json", "sha256": sha256(manifest_path)}]
    (staging / "checksums.sha256").write_text("".join(f"{item['sha256']}  {item['path']}\n" for item in checksum_entries), encoding="utf-8", newline="\n")

    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(staging.rglob("*")):
            if path.is_file():
                archive.write(path, f"{package_name}/{path.relative_to(staging).as_posix()}")
    result = {"staging": str(staging), "zip": str(zip_path), "zip_sha256": sha256(zip_path), "file_count": len(entries) + 2,
              "source_revision": contract["source_revision"], "gate": gate}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return staging


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--preflight-report", type=Path, help="Redacted release_preflight.py JSON report")
    parser.add_argument("--gate", choices=("plan", "ready"), default="plan")
    args = parser.parse_args()
    build(args.project_root, args.config, args.output_root, args.preflight_report, args.gate)
    return 0


if __name__ == "__main__":
    sys.exit(main())
