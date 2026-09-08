#!/usr/bin/env python3
"""Read-only local deployment preflight with redacted findings."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"(?:api[_-]?key|secret|token)\s*[=:]\s*['\"]?[A-Za-z0-9_\-]{24,}", re.I),
]
SKIP_PARTS = {"node_modules", "__pycache__", "release", "sites-temp"}
DEPLOYMENT_TEXT_SUFFIXES = {".sh", ".service", ".conf", ".example"}
SEARCHABLE_TEXT_SUFFIXES = DEPLOYMENT_TEXT_SUFFIXES | {".py", ".ts", ".tsx", ".js", ".json", ".md"}


def files(root: Path):
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if (
            not path.is_file()
            or any(part.startswith(".") for part in relative.parts)
            or set(relative.parts) & SKIP_PARTS
            or relative.parts[0] == "storage"
        ):
            continue
        yield path


def git_state(root: Path) -> dict:
    if not (root / ".git").exists():
        return {"repository": False, "status": "not-a-git-worktree"}
    return {"repository": True, "status": "present", "dirty_entries": None}


def first_existing(root: Path, candidates: list[str]) -> Path | None:
    return next((root / item for item in candidates if (root / item).exists()), None)


def detect(root: Path) -> dict:
    package = first_existing(root, ["frontend/package.json", "package.json"])
    requirements = first_existing(root, ["backend/requirements.txt", "requirements.txt", "pyproject.toml"])
    package_text = package.read_text(encoding="utf-8", errors="ignore") if package else ""
    req_text = requirements.read_text(encoding="utf-8", errors="ignore") if requirements else ""
    return {
        "vite_spa": any((root / item).exists() for item in ["frontend/vite.config.ts", "frontend/vite.config.js", "vite.config.ts", "vite.config.js"]),
        "react": '"react"' in package_text,
        "vue": '"vue"' in package_text,
        "fastapi": "fastapi" in req_text.lower(),
        "flask": "flask" in req_text.lower(),
        "django": "django" in req_text.lower(),
        "node_api": (root / "package.json").exists() and not (root / "frontend/package.json").exists(),
        "spring_boot": (root / "pom.xml").exists() or (root / "build.gradle").exists(),
        "file_persistence": (root / "storage").exists(),
        "ai_enabled": any((root / item).is_dir() for item in ["backend/app/assistant", "backend/app/ai", "src/ai"]),
        "model_artifacts": (root / "artifacts").is_dir(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    root = args.project_root.resolve()
    if not root.is_dir():
        raise SystemExit(f"project root not found: {root}")

    secret_files: list[str] = []
    crlf_files: list[str] = []
    windows_path_files: list[str] = []
    for path in files(root):
        relative = path.relative_to(root).as_posix()
        payload = path.read_bytes()
        if any(pattern.search(payload) for pattern in SECRET_PATTERNS):
            secret_files.append(relative)
        if path.suffix.lower() in DEPLOYMENT_TEXT_SUFFIXES:
            if b"\r" in payload:
                crlf_files.append(relative)
        if path.suffix.lower() in SEARCHABLE_TEXT_SUFFIXES:
            if re.search(rb"[A-Za-z]:\\", payload):
                windows_path_files.append(relative)

    project_type = detect(root)
    requirements = first_existing(root, ["backend/requirements.txt", "requirements.txt", "pyproject.toml"])
    node_lock = first_existing(root, [
        "frontend/package-lock.json", "frontend/pnpm-lock.yaml", "frontend/yarn.lock",
        "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    ])
    frontend_index = first_existing(root, ["frontend/dist/index.html", "dist/index.html"])
    required = {}
    if any(project_type[item] for item in ["fastapi", "flask", "django"]):
        required["python_dependency_manifest"] = bool(requirements)
    if project_type["vite_spa"] or project_type["react"] or project_type["vue"] or project_type["node_api"]:
        required["node_lockfile"] = bool(node_lock)
    if project_type["vite_spa"]:
        required["frontend_production_build"] = bool(frontend_index)
    if project_type["spring_boot"]:
        required["java_build_descriptor"] = True
    report = {
        "project_root": str(root),
        "git": git_state(root),
        "project_type": project_type,
        "required": required,
        "secret_scan": {"pass": not secret_files, "files": secret_files},
        "line_endings": {"pass": not crlf_files, "crlf_files": crlf_files},
        "windows_paths": {"pass": not windows_path_files, "files": windows_path_files},
    }
    recognized_app = any(project_type[item] for item in ["vite_spa", "react", "vue", "fastapi", "flask", "django", "node_api", "spring_boot"])
    report["pass"] = recognized_app and all(required.values()) and report["secret_scan"]["pass"] and report["line_endings"]["pass"] and report["windows_paths"]["pass"]
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output + "\n", encoding="utf-8", newline="\n")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
