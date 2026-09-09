#!/usr/bin/env python3
"""Validate Human Edge plugin packages, manifests, marketplaces, and paths."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

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
OPENAI_DISPLAY_NAMES = {
    "voice-to-work": "Voice to Work",
    "skill-from-scars": "Skill from Scars",
    "build-in-public-launcher": "Build in Public Launcher",
    "voice-with-temperature": "Voice With Temperature — Preserve Human Writing Voice",
}
CODEX_CATEGORIES = {
    "voice-to-work": "Productivity",
    "skill-from-scars": "Developer Tools",
    "build-in-public-launcher": "Productivity",
    "voice-with-temperature": "Writing",
}
AWESOME_CANDIDATES = {
    "skill-from-scars": "plugins/skill-from-scars",
    "voice-to-work": "plugins/voice-to-work",
}
AWESOME_RELEASE_REF = "v0.4.0"
AWESOME_RELEASE_SHA = "5930dcf59988aaa7a9a2358e6ec37dcd9ec7ee6d"


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
        extension = data.get("extensions", {}).get("com.openai")
        if not isinstance(extension, dict) or not isinstance(extension.get("interface"), dict):
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: missing extensions.com.openai.interface")
        interface = extension["interface"]
        if interface.get("displayName") != OPENAI_DISPLAY_NAMES[name]:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: wrong OpenAI display name")
        for key in (
            "shortDescription", "longDescription", "developerName", "category",
            "websiteURL", "privacyPolicyURL", "termsOfServiceURL", "logo",
        ):
            if not isinstance(interface.get(key), str) or not interface[key].strip():
                raise ValueError(f"{path.relative_to(REPO_ROOT)}: missing OpenAI interface.{key}")
        if "Part of the Human Edge Agent Skills project." not in interface["longDescription"]:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: long description lacks project context")
        for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
            parsed = urlparse(interface[key])
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError(f"{path.relative_to(REPO_ROOT)}: interface.{key} must be HTTPS")
        prompts = interface.get("defaultPrompt")
        if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: defaultPrompt must contain 1-3 prompts")
        if any(not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 128 for prompt in prompts):
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: invalid or overlong defaultPrompt")
        ensure_local_path(interface["logo"], path.parent)
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


def validate_codex_marketplace(config: dict) -> None:
    path = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
    data = load_json(path)
    if data.get("name") != "human-edge-skills":
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: unexpected marketplace name")
    interface = data.get("interface")
    if not isinstance(interface, dict) or interface.get("displayName") != "Human Edge Skills":
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: wrong interface.displayName")
    entries = data.get("plugins")
    if not isinstance(entries, list) or len(entries) != len(EXPECTED_PLUGINS):
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: expected exactly four plugins")
    names = [entry.get("name") for entry in entries if isinstance(entry, dict)]
    if names != list(EXPECTED_PLUGINS):
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: plugin order or names are wrong")
    for entry in entries:
        name = entry["name"]
        source = entry.get("source")
        if not isinstance(source, dict) or source.get("source") != "local":
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} must use a local source")
        source_path = source.get("path")
        if not isinstance(source_path, str):
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} source.path must be a string")
        plugin_dir = ensure_local_path(source_path, REPO_ROOT, require_dot=True)
        if plugin_dir != (REPO_ROOT / "plugins" / name).resolve():
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} source resolves incorrectly")
        policy = entry.get("policy")
        if not isinstance(policy, dict):
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} needs a policy")
        if policy.get("installation") != "AVAILABLE" or policy.get("authentication") != "ON_INSTALL":
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} has unexpected policy values")
        if "products" in policy:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} must not add product gating")
        if entry.get("category") != CODEX_CATEGORIES[name]:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {name} has the wrong category")
    print(f"PASS Codex marketplace JSON and paths: {path.relative_to(REPO_ROOT)}")


def validate_marketplace_evals() -> None:
    path = REPO_ROOT / "evals" / "marketplace-plugin-cases.json"
    data = load_json(path)
    cases = data.get("cases")
    if not isinstance(cases, list) or len(cases) != 24:
        raise ValueError(f"{path.relative_to(REPO_ROOT)}: expected exactly 24 cases")
    ids: set[str] = set()
    counts: dict[tuple[str, str], int] = {}
    required_fields = {
        "id", "plugin", "skill", "polarity", "prompt", "expected_route",
        "expected_output_shape", "safety_behavior", "pass_criteria",
    }
    for case in cases:
        if not isinstance(case, dict) or not required_fields.issubset(case):
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: case has missing fields")
        case_id = case["id"]
        if not isinstance(case_id, str) or case_id in ids:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: duplicate or invalid case id")
        ids.add(case_id)
        plugin = case["plugin"]
        polarity = case["polarity"]
        if plugin not in EXPECTED_PLUGINS or polarity not in {"positive", "negative"}:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: invalid plugin or polarity")
        for field in ("prompt", "expected_route", "expected_output_shape", "safety_behavior"):
            if not isinstance(case[field], str) or not case[field].strip():
                raise ValueError(f"{path.relative_to(REPO_ROOT)}: {case_id} has invalid {field}")
        criteria = case["pass_criteria"]
        if not isinstance(criteria, list) or len(criteria) < 2 or any(
            not isinstance(item, str) or not item.strip() for item in criteria
        ):
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {case_id} has weak pass criteria")
        counts[(plugin, polarity)] = counts.get((plugin, polarity), 0) + 1
    for plugin in ("voice-to-work", "skill-from-scars"):
        if counts.get((plugin, "positive")) != 5 or counts.get((plugin, "negative")) != 3:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: {plugin} must have 5 positive and 3 negative cases")
    print(f"PASS marketplace eval set: {len(cases)} cases with required OpenAI coverage")


def validate_openai_archives() -> None:
    output_dir = REPO_ROOT / "submission-assets" / "openai"
    index = load_json(output_dir / "PACKAGE_INDEX.json")
    records = index.get("archives")
    if index.get("candidate_order") != ["voice-to-work", "skill-from-scars"]:
        raise ValueError("submission-assets/openai/PACKAGE_INDEX.json: wrong candidate order")
    if not isinstance(records, list) or len(records) != 2:
        raise ValueError("submission-assets/openai/PACKAGE_INDEX.json: expected two archives")
    for record in records:
        name = record.get("plugin")
        if name not in {"voice-to-work", "skill-from-scars"}:
            raise ValueError("submission-assets/openai/PACKAGE_INDEX.json: unexpected plugin")
        archive_path = ensure_local_path(str(record.get("archive")), REPO_ROOT)
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        if digest != record.get("sha256"):
            raise ValueError(f"{archive_path.relative_to(REPO_ROOT)}: SHA-256 mismatch")
        with zipfile.ZipFile(archive_path) as handle:
            names = handle.namelist()
            for raw in names:
                pure = PurePosixPath(raw)
                if pure.is_absolute() or ".." in pure.parts:
                    raise ValueError(f"{archive_path.relative_to(REPO_ROOT)}: unsafe member {raw}")
            required = {"plugin.json", ".claude-plugin/plugin.json", "README.md", "PRIVACY.md", "LICENSE"}
            if not required.issubset(names):
                raise ValueError(f"{archive_path.relative_to(REPO_ROOT)}: missing root files")
            if not any(raw.startswith("skills/") and raw.endswith("/SKILL.md") for raw in names):
                raise ValueError(f"{archive_path.relative_to(REPO_ROOT)}: missing Skill")
        print(f"PASS OpenAI upload archive: {archive_path.relative_to(REPO_ROOT)}")


def validate_awesome_copilot_drafts() -> None:
    draft_dir = REPO_ROOT / "submission-assets" / "awesome-copilot"
    allowed_fields = {
        "name", "description", "version", "author", "homepage",
        "keywords", "license", "repository", "source",
    }
    for name, plugin_path in AWESOME_CANDIDATES.items():
        path = draft_dir / f"{name}.json"
        data = load_json(path)
        if set(data) != allowed_fields:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: unexpected or missing top-level fields")
        if data.get("name") != name:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: wrong plugin name")
        if data.get("version") != "1.0.0" or data.get("license") != "MIT":
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: wrong version or license")
        if data.get("repository") != REQUIRED_METADATA["repository"]:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: wrong repository")
        if data.get("homepage") != f"{REQUIRED_METADATA['repository']}/tree/{AWESOME_RELEASE_REF}/{plugin_path}":
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: homepage is not release-pinned")
        author = data.get("author")
        if author != {"name": "Joy T", "url": "https://github.com/FAIRY123456789"}:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: wrong author metadata")
        keywords = data.get("keywords")
        if not isinstance(keywords, list) or keywords != sorted(keywords) or any(
            not isinstance(keyword, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", keyword)
            for keyword in keywords
        ):
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: keywords must be sorted lowercase tags")
        source = data.get("source")
        expected_source = {
            "source": "github",
            "repo": "FAIRY123456789/human-edge-agent-skills",
            "path": plugin_path,
            "ref": AWESOME_RELEASE_REF,
            "sha": AWESOME_RELEASE_SHA,
        }
        if source != expected_source:
            raise ValueError(f"{path.relative_to(REPO_ROOT)}: wrong immutable source locator")
        print(f"PASS Awesome Copilot intake draft: {path.relative_to(REPO_ROOT)}")


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
        for required in ("README.md", "PRIVACY.md", "LICENSE", "plugin.json", "assets/human-edge.svg"):
            if not (plugin_dir / required).is_file():
                raise ValueError(f"plugins/{name}: missing {required}")
        readme = (plugin_dir / "README.md").read_text(encoding="utf-8")
        if "[PRIVACY.md](PRIVACY.md)" not in readme:
            raise ValueError(f"plugins/{name}: README must link PRIVACY.md")
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
        validate_codex_marketplace(config)
        validate_marketplace(REPO_ROOT / ".claude-plugin" / "marketplace.json", claude=True)
        validate_marketplace(REPO_ROOT / ".cursor-plugin" / "marketplace.json", claude=False)
        validate_marketplace_evals()
        validate_openai_archives()
        validate_awesome_copilot_drafts()
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
