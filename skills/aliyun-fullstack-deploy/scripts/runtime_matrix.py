#!/usr/bin/env python3
"""Compare a project runtime contract with a read-only ECS snapshot.

No installation, SSH, database connection, or production mutation occurs here.
Python 3.8+; only the standard library is required.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


PIN = re.compile(r"^\s*([A-Za-z0-9_.-]+)\s*==\s*([A-Za-z0-9_.+!-]+)\s*(?:;.*)?$")
NUMBERS = re.compile(r"(\d+)(?:\.(\d+))?(?:\.(\d+))?")


def numbers(value):
    match = NUMBERS.search(str(value or ""))
    if not match:
        return ()
    result = [int(x or 0) for x in match.groups()]
    return tuple(result)


def major(value):
    v = numbers(value)
    if not v:
        return None
    return v[1] if len(v) > 1 and v[0] == 1 else v[0]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def safe_file(root, path):
    candidate = (root / path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("path escapes project root") from exc
    return candidate


def first_file(root, candidates):
    return next((root / p for p in candidates if (root / p).is_file()), None)


def java_target(pom):
    if not pom:
        return None
    try:
        root = ET.parse(pom).getroot()
    except ET.ParseError:
        return None
    # The namespaces of Maven POMs vary; strip them for reliable lookup.
    for element in root.iter():
        element.tag = element.tag.split("}")[-1]
    props = root.find("properties")
    if props is None:
        return None
    for name in ("maven.compiler.release", "java.version", "maven.compiler.target"):
        node = props.find(name)
        if node is not None and node.text and node.text.strip().isdigit():
            return int(node.text.strip())
    return None


def requirements_pins(root, path, seen=None):
    seen = set() if seen is None else seen
    target = safe_file(root, path)
    if target in seen:
        return {}, []
    seen.add(target)
    pins, uncertain = {}, []
    for raw in target.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-r ", "--requirement ")):
            nested = line.split(maxsplit=1)[1].strip()
            nested_path = (target.parent / nested).resolve()
            safe_file(root, nested_path.relative_to(root.resolve()))
            more, pending = requirements_pins(root, nested_path.relative_to(root.resolve()), seen)
            for pkg, ver in more.items():
                if pkg in pins and pins[pkg] != ver:
                    uncertain.append(pkg + ": conflicting pins")
                pins[pkg] = ver
            uncertain.extend(pending)
            continue
        match = PIN.match(line)
        if match:
            name, version = match.groups()
            key = name.lower().replace("_", "-").replace(".", "-")
            if key in pins and pins[key] != version:
                uncertain.append(key + ": conflicting pins")
            pins[key] = version
        else:
            # Avoid printing URLs and secrets from dependency declarations.
            name = re.match(r"^[A-Za-z0-9_.-]+", line)
            uncertain.append(name.group(0) if name else "unresolved-dependency-line")
    return pins, sorted(set(uncertain))


def observed(server, name):
    entry = server.get("runtimes", {}).get(name, {})
    return entry if isinstance(entry, dict) else {}


def generate(root, contract, server):
    checks = []
    platform = server.get("platform", {})
    if platform.get("system") and platform["system"].lower() != "linux":
        checks.append(dict(component="ecs_platform", status="BLOCK", detail="Target probe was not collected from Linux ECS.", remedy="Run the read-only probe on the intended Linux ECS."))
    def add(component, status, detail, remedy=""):
        checks.append(dict(component=component, status=status, detail=detail, remedy=remedy))

    java_cfg = contract.get("java", {})
    pom_name = java_cfg.get("pom")
    pom = safe_file(root, pom_name) if pom_name else first_file(
        root, ("backend/pom.xml", "pom.xml", "backend/build.gradle", "build.gradle")
    )
    required_java = java_cfg.get("major") or (java_target(pom) if pom and pom.suffix == ".xml" else None)
    if pom or java_cfg:
        current = major(observed(server, "java").get("version"))
        if required_java is None:
            add("java", "REVIEW", "Java build target is not declared in the contract or POM.",
                "Declare java.major and confirm the JAR bytecode target.")
        elif current is None:
            add("java", "ACTION_REQUIRED", "ECS Java runtime was not detected; project targets Java %s." % required_java,
                "Install a supported JRE side by side; point systemd ExecStart at its absolute path.")
        elif current < int(required_java):
            add("java", "ACTION_REQUIRED", "JRE %s cannot execute Java %s bytecode." % (current, required_java),
                "Install JRE %s beside the system JRE, then rerun the server probe." % required_java)
        else:
            add("java", "PASS", "JRE %s supports the declared Java %s bytecode level; launch test remains required." %
                (current, required_java))

    py_cfg = contract.get("python", {})
    req_name = py_cfg.get("requirements")
    req = safe_file(root, req_name) if req_name else first_file(
        root, ("flask_model/carbon_model_api/requirements-production.txt",
               "flask_model/requirements-production.txt", "backend/requirements-production.txt",
               "backend/requirements.txt", "requirements-production.txt", "requirements.txt")
    )
    py_version = str(py_cfg.get("version", "")).strip()
    if not py_version and (root / ".python-version").is_file():
        py_version = (root / ".python-version").read_text(encoding="utf-8").strip()
    if req or py_cfg:
        current_py = numbers(observed(server, "python").get("version"))
        need_py = numbers(py_version)
        if not need_py:
            add("python", "REVIEW", "Project Python interpreter version is not declared.",
                "Declare python.version using the tested major.minor interpreter.")
        elif not current_py:
            add("python", "ACTION_REQUIRED", "Selected ECS Python interpreter is unavailable.",
                "Install Python %s independently; recreate the Linux venv." % py_version)
        elif current_py[:2] != need_py[:2]:
            add("python", "ACTION_REQUIRED", "ECS Python %s does not match declared Python %s." %
                (".".join(map(str, current_py[:2])), py_version),
                "Select the compatible interpreter by absolute path and rebuild the venv; do not copy Windows wheels.")
        else:
            add("python", "PASS", "Python %s matches the declared interpreter minor version." % py_version)

        if req and req.is_file():
            pins, uncertain = requirements_pins(root, req.relative_to(root))
            installed = {
                k.lower().replace("_", "-").replace(".", "-"): str(v)
                for k, v in server.get("packages", {}).items()
            }
            missing = [name for name in pins if name not in installed]
            mismatched = [name for name, val in pins.items()
                          if name in installed and installed[name] != val]
            if mismatched or missing:
                detail = "%s pinned dependencies missing; %s installed version mismatches." % (len(missing), len(mismatched))
                add("python_packages", "ACTION_REQUIRED", detail,
                    "Install pinned requirements inside the selected ECS venv, then run 'python -m pip check' and re-probe. "
                    "Examples: " + ", ".join((missing + mismatched)[:6]))
            else:
                add("python_packages", "PASS", "%s exact pins match the selected interpreter's installed packages." % len(pins))
            if uncertain:
                add("python_unpinned", "REVIEW", "%s declarations cannot be checked as exact pins." % len(uncertain),
                    "Resolve version constraints or test them in a fresh lockfile-backed venv.")
        else:
            add("python_packages", "BLOCK", "Configured Python requirements file is missing.",
                "Correct the project-relative path in the runtime contract.")

    front_cfg = contract.get("frontend", {})
    package = first_file(root, ("frontend/package.json", "package.json"))
    if package or front_cfg:
        build = front_cfg.get("build", "local")
        lock = first_file(root, ("frontend/package-lock.json", "frontend/pnpm-lock.yaml",
                                 "frontend/yarn.lock", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"))
        if not lock:
            add("frontend_lock", "ACTION_REQUIRED", "No JavaScript dependency lockfile was found.",
                "Generate and commit a supported lockfile; use npm ci or the equivalent.")
        else:
            add("frontend_lock", "PASS", "Dependency lockfile exists.")
        if build == "local":
            dist = first_file(root, ("frontend/dist/index.html", "dist/index.html"))
            if dist:
                add("frontend", "PASS", "Prebuilt static assets exist; ECS Node.js is not required.")
            else:
                add("frontend", "ACTION_REQUIRED", "Static production build is missing.",
                    "Build with the lockfile locally or in CI, and upload dist in the release.")
        else:
            add("frontend", "REVIEW", "Server-side Node build requested.",
                "Verify Node major/ABI and memory before npm ci; prefer local build on small ECS.")

    for service in ("mysql", "redis"):
        desired = contract.get(service, {}).get("major")
        if desired is None:
            continue
        entry = observed(server, service)
        version = entry.get("version")
        got = major(version)
        source = entry.get("source", "unknown")
        if got is None:
            add(service, "ACTION_REQUIRED", "No %s version was detected." % service,
                "Check the actual server or managed service endpoint with authorized read-only credentials.")
        elif got != int(desired):
            add(service, "REVIEW", "%s %s differs from expected major %s (%s observation)." %
                (service, version, desired, source),
                "Plan a tested schema/protocol migration; never automatically upgrade a production database.")
        elif source != "server_query":
            add(service, "REVIEW", "%s binary version %s matches, but the running server was not queried." %
                (service, version),
                "Verify the active service version, connectivity, permissions, and application queries.")
        else:
            add(service, "PASS", "%s running service version %s matches major %s." % (service, version, desired))

    serializer = contract.get("model_serializer", {})
    if serializer:
        model_python = serializer.get("python")
        ecs_python = observed(server, "python").get("version")
        needed = serializer.get("packages", {})
        installed = {k.lower().replace("_", "-"): str(v)
                     for k, v in server.get("packages", {}).items()}
        drift = []
        if model_python and numbers(model_python)[:2] != numbers(ecs_python)[:2]:
            drift.append("Python training/runtime interpreter")
        for name, version in needed.items():
            key = name.lower().replace("_", "-")
            if installed.get(key) != str(version):
                drift.append(key)
        if drift:
            add("model_serializer", "REVIEW", "Recorded model serialization environment differs or is unknown.",
                "Check/re-export the artifact under an approved environment; mismatches: " + ", ".join(drift[:8]))
        else:
            add("model_serializer", "PASS", "Recorded serialization Python and critical library versions match.")
    artifacts = contract.get("model_artifacts", [])
    if artifacts:
        absent = [pattern for pattern in artifacts if not list(root.glob(pattern))]
        if absent:
            add("model_artifacts", "BLOCK", "%s required model artifact patterns have no matches." % len(absent),
                "Include model assets or configure an authorized external model path.")
        elif server.get("validation", {}).get("model_smoke_passed") is True:
            add("model_artifacts", "PASS", "Model artifacts present and a server-side load/inference smoke is recorded.")
        else:
            add("model_artifacts", "REVIEW", "Model artifacts present; pickle/joblib compatibility is unproven.",
                "Load the model and run representative inference in the exact ECS venv during canary.")

    if not checks:
        add("contract", "REVIEW", "No recognizable components or explicit runtime requirements.",
            "Provide a project-specific runtime contract.")

    counts = {state: sum(c["status"] == state for c in checks)
              for state in ("PASS", "ACTION_REQUIRED", "REVIEW", "BLOCK")}
    overall = next((s for s in ("BLOCK", "ACTION_REQUIRED", "REVIEW") if counts[s]), "PASS")
    return {"schema_version": 1, "overall": overall, "counts": counts, "checks": checks,
            "read_only": True, "note": "Runtime checks never replace canary, migrations, or recovery tests."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument("--server", type=Path, required=True, help="JSON from probe_runtime.py")
    parser.add_argument("--contract", type=Path, help="Project-specific non-secret JSON contract")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--gate", choices=("plan", "ready"), default="plan")
    args = parser.parse_args()
    root = args.project_root.resolve()
    if not root.is_dir():
        parser.error("project root is missing")
    try:
        contract = read_json(args.contract) if args.contract else {}
        server = read_json(args.server)
        report = generate(root, contract, server)
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    result = json.dumps(report, ensure_ascii=False, indent=2)
    print(result)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(result + "\n", encoding="utf-8")
    if args.gate == "ready":
        return 0 if report["overall"] == "PASS" else 2
    return 2 if report["overall"] == "BLOCK" else 0


if __name__ == "__main__":
    sys.exit(main())
