#!/usr/bin/env python3
"""Build deterministic Skills-only archives for the first OpenAI candidates."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "submission-assets" / "openai"
CANDIDATES = ("voice-to-work", "skill-from-scars")
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def included_files(plugin_dir: Path) -> list[Path]:
    files = []
    for path in sorted(plugin_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symlinks are not allowed: {path}")
        relative = path.relative_to(plugin_dir)
        if any(part in IGNORED_NAMES for part in relative.parts):
            continue
        if path.is_file() and path.suffix not in IGNORED_SUFFIXES:
            files.append(path)
    return files


def build_archive(name: str) -> dict[str, object]:
    plugin_dir = REPO_ROOT / "plugins" / name
    archive = OUTPUT_DIR / f"{name}-1.0.0.zip"
    files = included_files(plugin_dir)
    required = {
        "plugin.json",
        ".claude-plugin/plugin.json",
        "README.md",
        "PRIVACY.md",
        "LICENSE",
    }
    relative_names = {path.relative_to(plugin_dir).as_posix() for path in files}
    missing = sorted(required - relative_names)
    if missing:
        raise ValueError(f"{name}: missing required archive files: {missing}")
    if not any(value.startswith("skills/") and value.endswith("/SKILL.md") for value in relative_names):
        raise ValueError(f"{name}: archive has no skills/<name>/SKILL.md")

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for path in files:
            relative = path.relative_to(plugin_dir).as_posix()
            info = zipfile.ZipInfo(relative, FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if path.suffix == ".py" else 0o644) << 16
            handle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    return {
        "plugin": name,
        "version": "1.0.0",
        "archive": archive.relative_to(REPO_ROOT).as_posix(),
        "sha256": digest,
        "files": len(files),
        "bytes": archive.stat().st_size,
        "format": "skills-only plugin archive",
        "submission_status": "READY FOR USER REVIEW; NOT SUBMITTED",
    }


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records = [build_archive(name) for name in CANDIDATES]
    index = {
        "schema_version": 1,
        "candidate_order": list(CANDIDATES),
        "archives": records,
    }
    (OUTPUT_DIR / "PACKAGE_INDEX.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    checksum_lines = [
        f"{record['sha256']}  {Path(str(record['archive'])).name}" for record in records
    ]
    (OUTPUT_DIR / "SHA256SUMS.txt").write_text(
        "\n".join(checksum_lines) + "\n", encoding="utf-8"
    )
    for record in records:
        print(f"BUILT {record['archive']} sha256={record['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
