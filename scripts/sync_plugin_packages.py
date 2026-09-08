#!/usr/bin/env python3
"""Synchronize packaged plugin skills from the canonical skills directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "packaging" / "plugin-sources.json"
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def ensure_within(path: Path, root: Path) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Path escapes repository root: {path}") from exc


def included_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not allowed in packaged skills: {path}")
        if any(part in IGNORED_NAMES for part in path.relative_to(root).parts):
            continue
        if path.is_file() and path.suffix not in IGNORED_SUFFIXES:
            files.append(path)
    return files


def file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in included_files(root)
    }


def tree_hash(hashes: dict[str, str]) -> str:
    payload = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def copy_skill(source: Path, destination: Path) -> None:
    ensure_within(source, REPO_ROOT)
    ensure_within(destination, REPO_ROOT)
    if not (source / "SKILL.md").is_file():
        raise ValueError(f"Canonical skill has no SKILL.md: {source}")
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".DS_Store", "Thumbs.db", "__pycache__", "*.pyc", "*.pyo"),
    )


def check_skill(source: Path, destination: Path) -> tuple[bool, str]:
    if not destination.is_dir():
        return False, f"missing packaged directory {destination.relative_to(REPO_ROOT)}"
    source_hashes = file_hashes(source)
    destination_hashes = file_hashes(destination)
    if source_hashes != destination_hashes:
        missing = sorted(set(source_hashes) - set(destination_hashes))
        extra = sorted(set(destination_hashes) - set(source_hashes))
        changed = sorted(
            path
            for path in set(source_hashes) & set(destination_hashes)
            if source_hashes[path] != destination_hashes[path]
        )
        details = []
        if missing:
            details.append(f"missing={missing}")
        if extra:
            details.append(f"extra={extra}")
        if changed:
            details.append(f"changed={changed}")
        return False, "; ".join(details)
    return True, tree_hash(source_hashes)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="replace packaged skill copies")
    mode.add_argument("--check", action="store_true", help="fail if packaged copies drift")
    args = parser.parse_args()

    config = load_config()
    canonical_root = REPO_ROOT / config["canonicalRoot"]
    plugin_root = REPO_ROOT / config["pluginRoot"]
    failures: list[str] = []

    for plugin_name, skill_names in config["plugins"].items():
        plugin_skills = plugin_root / plugin_name / "skills"
        expected = set(skill_names)
        if args.write:
            plugin_skills.mkdir(parents=True, exist_ok=True)
            for existing in plugin_skills.iterdir():
                if existing.is_dir() and existing.name not in expected:
                    ensure_within(existing, plugin_root)
                    shutil.rmtree(existing)
        elif not plugin_skills.is_dir():
            failures.append(f"{plugin_name}: missing skills directory")
            continue

        for skill_name in skill_names:
            source = canonical_root / skill_name
            destination = plugin_skills / skill_name
            if args.write:
                copy_skill(source, destination)
            ok, detail = check_skill(source, destination)
            status = "SYNCED" if ok else "DRIFT"
            print(f"{plugin_name}/{skill_name}: {status} {detail}")
            if not ok:
                failures.append(f"{plugin_name}/{skill_name}: {detail}")

        if plugin_skills.is_dir():
            actual = {path.name for path in plugin_skills.iterdir() if path.is_dir()}
            if actual != expected:
                failures.append(
                    f"{plugin_name}: packaged skills {sorted(actual)} != expected {sorted(expected)}"
                )

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1
    print(f"OK: {len(config['plugins'])} plugin packages match canonical skill content.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
