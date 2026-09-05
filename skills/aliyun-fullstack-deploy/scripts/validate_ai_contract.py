#!/usr/bin/env python3
"""Validate project-specific AI packaging requirements without embedding provider details."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PurePosixPath


def safe_relative(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts and "\\" not in value


def contains(root: Path, relative: str, needle: str) -> bool:
    path = root / relative
    return path.is_file() and needle.casefold() in path.read_text(encoding="utf-8", errors="ignore").casefold()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--contract", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))

    required_files = contract.get("required_files", [])
    text_markers = contract.get("text_markers", [])
    env_names = contract.get("environment_variables", [])
    errors: list[str] = []

    if not all(isinstance(item, str) and safe_relative(item) for item in required_files):
        errors.append("contract-required-files-must-be-safe-relative-paths")
        required_files = []
    if not all(
        isinstance(item, dict)
        and isinstance(item.get("path"), str)
        and safe_relative(item["path"])
        and isinstance(item.get("contains"), str)
        and item["contains"]
        for item in text_markers
    ):
        errors.append("contract-text-markers-invalid")
        text_markers = []
    if not all(isinstance(item, str) and item and "=" not in item for item in env_names):
        errors.append("environment-variables-must-be-names-not-values")
        env_names = []

    checks = {f"file:{item}": (root / item).is_file() for item in required_files}
    checks.update({
        f"marker:{item['path']}:{item['contains']}": contains(root, item["path"], item["contains"])
        for item in text_markers
    })

    env_candidates = [root / ".env.production.example", root / ".env.example"]
    env_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in env_candidates if path.is_file())
    checks.update({f"env-name:{name}": name in env_text for name in env_names})

    required_capabilities = {"backend_client", "route_registration", "frontend_entry", "offline_fallback"}
    capabilities = set(contract.get("capabilities", []))
    missing_capabilities = sorted(required_capabilities - capabilities)
    if missing_capabilities:
        errors.append("missing-capabilities:" + ",".join(missing_capabilities))

    report = {"pass": not errors and all(checks.values()), "errors": errors, "checks": checks}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
