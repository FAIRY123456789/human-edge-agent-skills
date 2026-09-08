#!/usr/bin/env python3
"""Inspect a release directory or ZIP without exposing matched secret values."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


SECRET_PATTERNS = [
    re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"(?:api[_-]?key|secret|token)\s*[=:]\s*['\"]?[A-Za-z0-9_-]{24,}", re.I),
]
FORBIDDEN_PARTS = {"node_modules", "__pycache__"}
DEPLOY_SUFFIXES = {".sh", ".service", ".conf", ".example"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(root: Path, zip_names: list[str], required_files: list[str] | None = None) -> dict:
    children = [item for item in root.iterdir() if item.is_dir()]
    package = children[0] if len(children) == 1 and not (root / "manifest.json").exists() else root
    failures: list[str] = []
    manifest_path = package / "manifest.json"
    checksum_path = package / "checksums.sha256"
    for path, label in ((manifest_path, "manifest"), (checksum_path, "checksums")):
        if not path.is_file():
            failures.append(f"missing:{label}")
    if any("\\" in name for name in zip_names):
        failures.append("zip-backslash-path")

    secret_files: list[str] = []
    crlf_files: list[str] = []
    forbidden_files: list[str] = []
    for path in package.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(package)
        if (
            any(part.startswith(".") for part in relative.parts)
            or set(relative.parts) & FORBIDDEN_PARTS
            or relative.parts[0] == "storage"
        ):
            forbidden_files.append(relative.as_posix())
        payload = path.read_bytes()
        if any(pattern.search(payload) for pattern in SECRET_PATTERNS):
            secret_files.append(relative.as_posix())
        if path.suffix.lower() in DEPLOY_SUFFIXES and b"\r" in payload:
            crlf_files.append(relative.as_posix())
    if secret_files:
        failures.append("secret-pattern")
    if crlf_files:
        failures.append("crlf-deployment-text")
    if forbidden_files:
        failures.append("forbidden-content")

    checksum_mismatches: list[str] = []
    if checksum_path.is_file():
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            if "  " not in line:
                checksum_mismatches.append("<malformed-checksum-line>")
                continue
            expected, relative = line.split("  ", 1)
            target = package / relative
            if not target.is_file() or sha256(target) != expected:
                checksum_mismatches.append(relative)
    if checksum_mismatches:
        failures.append("checksum-mismatch")

    required_files = required_files or []
    missing_required = [item for item in required_files if not (package / item).is_file()]
    if missing_required:
        failures.append("missing-required-file")

    index = package / "frontend" / "dist" / "index.html"
    missing_assets: list[str] = []
    if index.is_file():
        for asset in re.findall(r'(?:src|href)="([^"]+/assets/[^"]+)"', index.read_text(encoding="utf-8")):
            relative = asset.lstrip("/").split("/assets/", 1)[1]
            if not (package / "frontend" / "dist" / "assets" / relative).is_file():
                missing_assets.append(asset)
    if missing_assets:
        failures.append("missing-static-assets")
    return {
        "pass": not failures,
        "package": str(package),
        "failures": failures,
        "secret_files": secret_files,
        "crlf_files": crlf_files,
        "forbidden_files": forbidden_files,
        "checksum_mismatches": checksum_mismatches,
        "missing_required": missing_required,
        "missing_assets": missing_assets,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("release", type=Path)
    parser.add_argument("--required-file", action="append", default=[])
    args = parser.parse_args()
    release = args.release.resolve()
    if release.is_file():
        with zipfile.ZipFile(release) as archive:
            names = archive.namelist()
            unsafe = [
                name for name in names
                if "\\" in name
                or PurePosixPath(name).is_absolute()
                or ".." in PurePosixPath(name).parts
                or any(":" in part for part in PurePosixPath(name).parts)
            ]
            if unsafe:
                report = {
                    "pass": False,
                    "release": str(release),
                    "failures": ["unsafe-zip-path"],
                    "unsafe_zip_entries": unsafe,
                }
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 1
            with tempfile.TemporaryDirectory() as temp:
                archive.extractall(temp)
                report = inspect(Path(temp), names, args.required_file)
                report["release"] = str(release)
    else:
        report = inspect(release, [], args.required_file)
        report["release"] = str(release)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
