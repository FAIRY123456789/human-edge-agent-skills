#!/usr/bin/env python3
"""Validate Human Edge plugin packages, manifests, marketplaces, and paths."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator
from jsonschema.validators import validator_for


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "packaging" / "plugin-sources.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "agent-plugin-1.0.0.schema.json"
AGENT_SCHEMA_ID = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
EXPECTED_PLUGINS = {
    "voice-to-work": ["voice-dump-to-todo", "vibe-to-spec"],
    "skill-from-scars": ["skill-from-scars"],
    "build-in-public-launcher": ["build-in-public-launcher"],
    "voice-with-temperature": ["voice-with-temperature"],
}
CLAUDE_SCHEMA_ID = "https://json.schemastore.org/claude-code-plugin-manifest.json"
REQUIRED_METADATA = {
    "version": "1.0.0",
    "license": "MIT",
    "repository": "https://github.com/FAIRY123456789/human-edge-agent-skills",
}


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: root must be an object")
    return value


def ensure_local_path(raw: str, base: Path, *, require_dot: bool = False) -> Path:
    if require_dot and not raw.startswith("./"):
        raise ValueError(f"relative source must start with './': {raw}")
    normalized = raw[2:] if raw.startswith("./") else raw
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or ".." in pure.parts or re.match(r"^[A-Za-z]:", normalized):
        raise ValueError(f"unsafe path: {raw}")
    resolved = (base / Path(*pure.parts)).resolve()
    try:
        resolved.relative_to(REPO_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {raw}") from exc
    if not resolved.exists():
        raise ValueError(f"path does not exist: {raw}")
    return resolved


def assert_metadata(data: dict, name: str, path: Path) -> None:
    if data.get("name") != name:
        raise ValueError(f"{path}: name {data.get('name')!r} != {name!r}")
    for key, expected in REQUIRED_METADATA.items():
        if data.get(key) != expected:
            raise ValueError(f"{path}: {key} {data.get(key)!r} != {expected!r}")
    author = data.get("author")
    if not isinstance(author, dict) or author.get("name") != "Joy T":
        raise ValueError(f"{path}: author.name must be 'Joy T'")
    if "email" in author:
        raise ValueError(f"{path}: optional author email is intentionally omitted")


def validate_agent_manifests(config: dict) -> None:
    schema = load_json(SCHEMA_PATH)
    if schema.get("$id") != AGENT_SCHEMA_ID:
        raise ValueError("vendored Agent Plugins schema has the wrong $id")
    validator = Draft202012Validator(schema)
    for name in config["plugins"]:
        path = REPO_ROOT / "plugins" / name / "plugin.json"
        data = load_json(path)
        errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(error.message for error in errors)
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: Agent Plugins schema failure: {details}")
        assert_metadata(data, name, path.relative_to(REPO_ROOT))
        print(f"PASS Agent Plugins schema: plugins/{name}/plugin.json")


def validate_claude_manifests(config: dict) -> None:
    allowed_components = {"skills"}
    prohibited_components = {
        "agents", "commands", "hooks", "mcpServers", "lspServers", "monitors", "rules"
    }
    for name in config["plugins"]:
        path = REPO_ROOT / "plugins" / name / ".claude-plugin" / "plugin.json"
        data = load_json(path)
        if data.get("$schema") != CLAUDE_SCHEMA_ID:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: wrong Claude schema URL")
        assert_metadata(data, name, path.relative_to(REPO_ROOT))
        found = prohibited_components & set(data)
        if found:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: prohibited components {sorted(found)}")
        extra_components = allowed_components & set(data)
        if extra_components:
            raise ValueError(
                f"{path.relative_to(REPO_ROOT)}: default skills discovery should not be overridden"
            )
        print(f"PASS Claude manifest metadata: plugins/{name}/.claude-plugin/plugin.json")


def validate_with_schema(instance_path: Path, schema_path: Path) -> None:
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    validator_class = validator_for(schema)
    validator_class.check_schema(schema)
    errors = sorted(validator_class(schema).iter_errors(instance), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(error.message for error in errors)
        raise ValueError(f"{instance_path.relative_to(REPO_ROOT)}: schema failure: {details}")
    print(f"PASS live schema: {instance_path.relative_to(REPO_ROOT)}")


def validate_marketplace(path: Path, *, claude: bool) -> None:
    data = load_json(path)
    if data.get("name") != "human-edge-skills":
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: unexpected marketplace name")
    owner = data.get("owner")
    if not isinstance(owner, dict) or owner.get("name") != "Joy T" or "email" in owner:
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: owner must use real name and no email")
    entries = data.get("plugins")
    if not isinstance(entries, list) or len(entries) != 4:
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: expected exactly four plugins")
    names = [entry.get("name") for entry in entries if isinstance(entry, dict)]
    if len(names) != 4 or set(names) != set(EXPECTED_PLUGINS) or len(names) != len(set(names)):
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: wrong or duplicate plugin names")
    for entry in entries:
        name = entry["name"]
        assert_metadata(entry, name, path.relative_to(REPO_ROOT))
        source = entry.get("source")
        if not isinstance(source, str):
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} source must be a string")
        plugin_dir = ensure_local_path(source, REPO_ROOT, require_dot=claude)
        if plugin_dir != (REPO_ROOT / "plugins" / name).resolve():
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} source resolves incorrectly")
        if claude:
            if entry.get("strict") is not True:
                raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} must use strict mode")
        else:
            logo = entry.get("logo")
            if not isinstance(logo, str):
                raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} needs a logo path")
            ensure_local_path(logo, REPO_ROOT)
    print(f"PASS marketplace JSON and paths: {path.relative_to(REPO_ROOT)}")


def validate_self_containment(config: dict) -> None:
    for name, skills in config["plugins"].items():
        plugin_dir = REPO_ROOT / "plugins" / name
        for path in plugin_dir.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"{path.relative_to(REPO_ROOT)}: symlinks are not allowed")
        actual = {
            path.name for path in (plugin_dir / "skills").iterdir() if path.is_dir()
        }
        if actual != set(skills):
            raise ValueError(f"plugins/{name}: packaged skill set is wrong")
        forbidden_dirs = [
            plugin_dir / item
            for item in ("agents", "commands", "hooks", "rules", "monitors")
            if (plugin_dir / item).exists()
        ]
        if forbidden_dirs:
            raise ValueError(f"plugins/{name}: unexpected platform-specific components")
        for required in ("README.md", "LICENSE", "plugin.json", "assets/human-edge.svg"):
            if not (plugin_dir / required).is_file():
                raise ValueError(f"plugins/{name}: missing {required}")
        print(f"PASS self-contained package: plugins/{name}")


def validate_drift() -> None:
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "sync_plugin_packages.py"), "--check"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.returncode:
        raise ValueError(result.stderr.strip() or "plugin skill drift detected")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--claude-schema-dir",
        type=Path,
        help="directory containing current claude-code-plugin-manifest.json and claude-code-marketplace.json",
    )
    args = parser.parse_args()
    try:
        config = load_json(CONFIG_PATH)
        if config.get("plugins") != EXPECTED_PLUGINS:
            raise ValueError("packaging/plugin-sources.json does not match the approved composition")
        validate_agent_manifests(config)
        validate_claude_manifests(config)
        validate_marketplace(REPO_ROOT / ".claude-plugin" / "marketplace.json", claude=True)
        validate_marketplace(REPO_ROOT / ".cursor-plugin" / "marketplace.json", claude=False)
        if args.claude_schema_dir:
            schema_dir = args.claude_schema_dir.resolve()
            manifest_schema = schema_dir / "claude-code-plugin-manifest.json"
            marketplace_schema = schema_dir / "claude-code-marketplace.json"
            for name in config["plugins"]:
                validate_with_schema(
                    REPO_ROOT / "plugins" / name / ".claude-plugin" / "plugin.json",
                    manifest_schema,
                )
            validate_with_schema(
                REPO_ROOT / ".claude-plugin" / "marketplace.json",
                marketplace_schema,
            )
        validate_self_containment(config)
        validate_drift()
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("OK: all four plugin packages passed schema, marketplace, path, and drift checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
