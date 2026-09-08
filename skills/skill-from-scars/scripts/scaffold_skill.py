#!/usr/bin/env python3
"""Create a minimal Skill tree from a local JSON design record."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SAFE_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def scaffold(source: Path, output: Path) -> Path:
    if not source.is_file():
        raise FileNotFoundError(f"design record not found: {source}")
    data = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("design record must be a JSON object")
    name_value = data.get("name")
    description_value = data.get("description")
    if not isinstance(name_value, str) or not SAFE_NAME.fullmatch(name_value.strip().lower()):
        raise ValueError("name must use lowercase letters, numbers, and hyphens")
    if not isinstance(description_value, str) or not description_value.strip():
        raise ValueError("description must be a non-empty string")

    name = name_value.strip().lower()
    root = output.resolve() / name
    (root / "references").mkdir(parents=True, exist_ok=True)
    (root / "evals").mkdir(parents=True, exist_ok=True)
    description = description_value.replace('"', '\\"')
    workflow = data.get("workflow", ["Define the workflow."])
    if not isinstance(workflow, list) or not all(isinstance(item, str) for item in workflow):
        raise ValueError("workflow must be a list of strings")
    lines = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(workflow))
    skill_text = (
        "---\nname: {}\ndescription: \"{}\"\n---\n\n# {}\n\n## Instructions\n\n{}\n"
        .format(name, description, data.get("title", name), lines)
    )
    (root / "SKILL.md").write_text(skill_text, encoding="utf-8")
    (root / "evals" / "seed.json").write_text(
        json.dumps(data.get("eval", {}), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return root


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path, nargs="?", default=Path("."))
    args = parser.parse_args()
    print(scaffold(args.source, args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
