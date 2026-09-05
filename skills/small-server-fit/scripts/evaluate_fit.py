#!/usr/bin/env python3
"""Calculate small-server RAM and disk margins from explicit measurements."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.profile.read_text(encoding="utf-8"))
    server = data.get("server", {})
    reserved = data.get("reserved", {})
    app = data.get("application", {})
    plan = data.get("plan", {})

    ram = number(server.get("ram_mib"))
    os_ram = number(reserved.get("os_and_services_mib"))
    runtime_peak = number(app.get("peak_runtime_mib"))
    build_peak = number(app.get("peak_build_mib"))
    headroom = number(plan.get("memory_headroom_percent"))
    disk_free = number(server.get("disk_free_gib"))
    disk_safety = number(reserved.get("disk_safety_gib"))
    installed = number(app.get("installed_disk_gib"))
    releases = number(app.get("release_and_rollback_gib"))
    build_on_server = plan.get("build_on_server") is True

    missing = []
    for label, value in [
        ("server.ram_mib", ram),
        ("reserved.os_and_services_mib", os_ram),
        ("application.peak_runtime_mib", runtime_peak),
        ("plan.memory_headroom_percent", headroom),
        ("server.disk_free_gib", disk_free),
        ("reserved.disk_safety_gib", disk_safety),
        ("application.installed_disk_gib", installed),
        ("application.release_and_rollback_gib", releases),
    ]:
        if value is None:
            missing.append(label)
    if build_on_server and build_peak is None:
        missing.append("application.peak_build_mib")

    memory = {"status": "NOT MEASURED"}
    if None not in (ram, os_ram, runtime_peak, headroom) and not (build_on_server and build_peak is None):
        app_peak = max(runtime_peak, build_peak) if build_on_server else runtime_peak
        required = os_ram + app_peak * (1 + headroom / 100)
        memory = {
            "status": "FIT" if required <= ram else "NOT FIT",
            "required_mib": round(required, 1),
            "available_mib": ram,
            "margin_mib": round(ram - required, 1),
        }

    disk = {"status": "NOT MEASURED"}
    if None not in (disk_free, disk_safety, installed, releases):
        required_disk = disk_safety + installed + releases
        disk = {
            "status": "FIT" if required_disk <= disk_free else "NOT FIT",
            "required_gib": round(required_disk, 2),
            "available_gib": disk_free,
            "margin_gib": round(disk_free - required_disk, 2),
        }

    statuses = {memory["status"], disk["status"]}
    overall = "NOT FIT" if "NOT FIT" in statuses else ("NOT MEASURED" if "NOT MEASURED" in statuses else "FIT")
    report = {"overall": overall, "memory": memory, "disk": disk, "missing": missing}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if overall == "NOT FIT" else 2 if overall == "NOT MEASURED" else 0


if __name__ == "__main__":
    sys.exit(main())
