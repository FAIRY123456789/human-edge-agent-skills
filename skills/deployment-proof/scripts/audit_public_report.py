#!/usr/bin/env python3
"""Flag common secrets and infrastructure identifiers before public release."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from pathlib import Path


PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "api-key": re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    "secret-assignment": re.compile(r"(?im)^\s*[A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD|DATABASE_URL)\s*=\s*\S+"),
    "authorization-header": re.compile(r"(?i)Authorization\s*:\s*(?:Bearer|Basic)\s+\S+"),
    "ssh-target": re.compile(r"\b(?:ssh|scp|sftp)\s+(?!-)(?:[^\s@]+@)?[^\s:]+"),
    "windows-user-path": re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s]+"),
    "linux-user-path": re.compile(r"(?m)(?:^|[\s`'\"])/home/[^/\s]+"),
}
IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".log", ".csv", ".sh", ".ps1"}


def public_ips(text: str) -> list[str]:
    found = []
    for candidate in IPV4.findall(text):
        try:
            address = ipaddress.ip_address(candidate)
        except ValueError:
            continue
        if not (address.is_private or address.is_loopback or address.is_link_local or address.is_unspecified):
            found.append(candidate)
    return sorted(set(found))


def iter_files(target: Path):
    if target.is_file():
        yield target
        return
    for path in target.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and ".git" not in path.parts:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.exists():
        raise SystemExit(f"target not found: {target}")

    findings = []
    for path in iter_files(target):
        text = path.read_text(encoding="utf-8", errors="ignore")
        labels = [label for label, pattern in PATTERNS.items() if pattern.search(text)]
        if public_ips(text):
            labels.append("public-ip")
        if labels:
            findings.append({"file": str(path.relative_to(target) if target.is_dir() else path.name), "types": sorted(labels)})

    report = {"pass": not findings, "finding_count": len(findings), "findings": findings}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
