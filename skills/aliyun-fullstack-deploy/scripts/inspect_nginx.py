#!/usr/bin/env python3
"""Summarize effective Nginx server/location ownership from `nginx -T` output."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def blocks(text: str, keyword: str) -> list[str]:
    found: list[str] = []
    for match in re.finditer(rf"(?m)^\s*{re.escape(keyword)}\s*\{{", text):
        depth = 0
        start = match.start()
        for index in range(text.find("{", start), len(text)):
            depth += text[index] == "{"
            depth -= text[index] == "}"
            if depth == 0:
                found.append(text[start:index + 1])
                break
    return found


def values(block: str, directive: str) -> list[str]:
    return [item.strip() for item in re.findall(rf"(?m)^\s*{directive}\s+([^;]+);", block)]


def inspect(text: str, app_path: str = "", protected_roots: list[str] | None = None) -> dict:
    """Return routing ownership and duplicate warnings without changing Nginx."""
    servers = []
    location_owners: dict[str, list[int]] = {}
    for index, block in enumerate(blocks(text, "server"), 1):
        locations = [item.strip() for item in re.findall(r"(?m)^\s*location\s+([^\{]+)\{", block)]
        for location in locations:
            location_owners.setdefault(location, []).append(index)
        servers.append({
            "index": index,
            "listen": values(block, "listen"),
            "server_name": values(block, "server_name"),
            "root": values(block, "root"),
            "locations": locations,
            "contains_app_path": bool(app_path and app_path in block),
        })
    wildcard_80 = [
        server["index"]
        for server in servers
        if any(value.startswith("80") or "0.0.0.0:80" in value for value in server["listen"])
        and any("_" in value for value in server["server_name"])
    ]
    duplicates = sorted(location for location, owners in location_owners.items() if len(owners) > 1 or any(server["locations"].count(location) > 1 for server in servers))
    protected_roots = protected_roots or []
    configured_roots = [root for server in servers for root in server["root"]]
    return {
        "server_count": len(servers),
        "wildcard_port80_servers": wildcard_80,
        "wildcard_server_count": len(wildcard_80),
        "duplicate_wildcard_warning": len(wildcard_80) > 1,
        "duplicate_locations": duplicates,
        "configured_roots": configured_roots,
        "protected_root_presence": {
            protected: any(protected in root for root in configured_roots)
            for protected in protected_roots
        },
        "servers": servers,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--app-path", default="")
    parser.add_argument("--protected-root", action="append", default=[])
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8", errors="replace") if args.input else sys.stdin.read()
    report = inspect(text, args.app_path, args.protected_root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["duplicate_wildcard_warning"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
