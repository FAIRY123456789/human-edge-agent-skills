#!/usr/bin/env python3
"""Read-only, credential-free ECS runtime snapshot; Python 3.6+.

Probe binaries and an explicitly selected Python environment. mysql/redis
binary versions are NOT proof of a running service or remote RDS version.
"""
from __future__ import print_function

import argparse
import json
import platform
import re
import subprocess
import sys
from pathlib import Path


def run(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                universal_newlines=True, timeout=8, check=False)
        if result.returncode:
            return None
        return result.stdout.strip()[:2048]
    except (OSError, subprocess.TimeoutExpired):
        return None


def version(output, service):
    if not output:
        return None
    patterns = {
        "java": [r'(?:version\s*[" ]|openjdk\s+)(\d+(?:\.\d+){0,2})'],
        "mysql": [r'(?:Ver|version)\s+(\d+(?:\.\d+){1,2})'],
        "redis": [r'v=(\d+(?:\.\d+){1,2})'],
    }
    for pattern in patterns.get(service, []):
        found = re.search(pattern, output, re.I)
        if found:
            return found.group(1)
    match = re.search(r'\d+(?:\.\d+){1,2}', output)
    return match.group(0) if match else None


def binary(command, label, source="binary"):
    output = run(command)
    return {"version": version(output, label), "source": source, "available": bool(output)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--python-bin", default="python3", help="Exact ECS Python interpreter or venv executable")
    ap.add_argument("--java-bin", default="java")
    ap.add_argument("--node-bin", default="node")
    ap.add_argument("--mysql-bin", default="mysqld")
    ap.add_argument("--redis-bin", default="redis-server")
    ap.add_argument("--packages", default="", help="Comma-separated package names; never dump entire environment")
    ap.add_argument("--json-out", type=Path)
    args = ap.parse_args()
    py = run([args.python_bin, "-c", "import sys;print('.'.join(map(str,sys.version_info[:3])))"])
    py_entry = {"version": py, "source": "interpreter", "available": bool(py)}
    node = binary([args.node_bin, "--version"], "node")
    java = binary([args.java_bin, "-version"], "java")
    mysql = binary([args.mysql_bin, "--version"], "mysql")
    redis = binary([args.redis_bin, "--version"], "redis")
    packages = {}
    wanted = {part.strip().lower().replace("_", "-").replace(".", "-")
              for part in args.packages.split(",") if part.strip()}
    if py and wanted:
        raw = run([args.python_bin, "-m", "pip", "list", "--format=json",
                   "--disable-pip-version-check"])
        if raw:
            try:
                for item in json.loads(raw):
                    key = item["name"].lower().replace("_", "-").replace(".", "-")
                    if key in wanted:
                        packages[key] = item["version"]
            except (KeyError, ValueError, TypeError):
                pass
    result = {
        "schema_version": 1,
        "platform": {"system": platform.system(), "release": platform.release(),
                     "machine": platform.machine()},
        "runtimes": {"java": java, "python": py_entry, "node": node,
                     "mysql": mysql, "redis": redis},
        "packages": packages,
        "note": "Read-only binary snapshot. Running DB service, model inference and API compatibility NOT TESTED."
    }
    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
