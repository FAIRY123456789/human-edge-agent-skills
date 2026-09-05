#!/usr/bin/env python3
"""Functional smoke tests for the repository's deterministic helpers."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], expected: set[int] = {0}) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode not in expected:
        raise AssertionError(
            f"command returned {result.returncode}, expected {sorted(expected)}: {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def test_voice_todo(temp: Path) -> None:
    payload = {
        "title": "Smoke Todo",
        "tasks": [{"title": "Ship proof", "details": "Generate and inspect HTML", "priority": "P1", "status": "todo"}],
    }
    source = temp / "todo.json"
    output = temp / "todo.html"
    source.write_text(json.dumps(payload), encoding="utf-8")
    run([sys.executable, "skills/voice-dump-to-todo/scripts/render_todo.py", str(source), str(output)])
    page = output.read_text(encoding="utf-8")
    assert "<!doctype html>" in page and "localStorage" in page and "Ship proof" in page


def test_csdn_linter(temp: Path) -> None:
    malformed = temp / "malformed.md"
    malformed.write_text("# Wrong overall title\n\nTiny.\n", encoding="utf-8")
    bad = run([sys.executable, "skills/csdn-technical-writing/scripts/lint_csdn_article.py", str(malformed)], {1})
    assert "Style review" in bad.stdout

    paragraph = "这个段落先给出准确概念，再用自然语言解释运行机制、适用场景和常见误区，让初学者能够理解为什么这样设计以及下一步怎样验证。"
    compliant = temp / "compliant.md"
    compliant.write_text(
        "一篇合规的技术文章\n\n"
        + "\n\n".join(f"# 第{i}部分\n\n{paragraph}" for i in range(1, 5))
        + "\n",
        encoding="utf-8",
    )
    run([sys.executable, "skills/csdn-technical-writing/scripts/lint_csdn_article.py", str(compliant)])


def test_skill_scaffold(temp: Path) -> None:
    spec = {
        "name": "smoke-skill",
        "title": "Smoke Skill",
        "description": "Use when a smoke test needs to confirm that the scaffold produces valid Agent Skill frontmatter and files.",
        "workflow": ["Inspect the input.", "Return a verified result."],
        "eval": {"prompt": "Run the smoke workflow."},
    }
    source = temp / "skill.json"
    output = temp / "generated"
    source.write_text(json.dumps(spec), encoding="utf-8")
    run([sys.executable, "skills/skill-from-scars/scripts/scaffold_skill.py", str(source), str(output)])
    skill_text = (output / "smoke-skill" / "SKILL.md").read_text(encoding="utf-8")
    assert skill_text.startswith("---\nname: smoke-skill\n")
    assert (output / "smoke-skill" / "evals" / "seed.json").is_file()


def test_fit_and_public_audit(temp: Path) -> None:
    profile = {
        "server": {"vcpu": 2, "ram_mib": 2048, "swap_mib": 0, "disk_free_gib": 30},
        "reserved": {"os_and_services_mib": 512, "disk_safety_gib": 5},
        "application": {"steady_rss_mib": 500, "peak_runtime_mib": 700, "peak_build_mib": None, "installed_disk_gib": 2, "release_and_rollback_gib": 3},
        "plan": {"build_on_server": False, "memory_headroom_percent": 25},
    }
    profile_path = temp / "fit.json"
    profile_path.write_text(json.dumps(profile), encoding="utf-8")
    fit = run([sys.executable, "skills/small-server-fit/scripts/evaluate_fit.py", "--profile", str(profile_path)])
    assert json.loads(fit.stdout)["overall"] == "FIT"

    clean = temp / "public.md"
    clean.write_text("Verified on a small Linux VPS; host identity was removed.\n", encoding="utf-8")
    run([sys.executable, "skills/deployment-proof/scripts/audit_public_report.py", str(clean)])
    unsafe = temp / "unsafe.md"
    unsafe.write_text("API_TOKEN=unsafe-placeholder-value\n", encoding="utf-8")
    flagged = run([sys.executable, "skills/deployment-proof/scripts/audit_public_report.py", str(unsafe)], {1})
    assert json.loads(flagged.stdout)["finding_count"] == 1


def test_release_and_ai_contract(temp: Path) -> None:
    project = temp / "project"
    (project / "frontend/dist/assets").mkdir(parents=True)
    (project / "backend/app/ai").mkdir(parents=True)
    (project / "backend/app/api").mkdir(parents=True)
    (project / "frontend/src").mkdir(parents=True)
    (project / "frontend/dist/index.html").write_text('<script src="/assets/app.js"></script>', encoding="utf-8")
    (project / "frontend/dist/assets/app.js").write_text("console.log('ok')", encoding="utf-8")
    (project / "backend/app/ai/client.py").write_text("class Client: pass\n", encoding="utf-8")
    (project / "backend/app/ai/fallback.py").write_text("def fallback(): return None\n", encoding="utf-8")
    (project / "backend/app/api/router.py").write_text("ai_router = True\n", encoding="utf-8")
    (project / "frontend/src/api.ts").write_text("export const assistant = true\n", encoding="utf-8")
    (project / ".env.production.example").write_text("AI_ENABLED=\nAI_API_KEY=\n", encoding="utf-8")

    release_config = {"project_name": "smoke", "version": "test", "includes": ["frontend/dist", ".env.production.example"]}
    config_path = project / "release.json"
    config_path.write_text(json.dumps(release_config), encoding="utf-8")
    built = run([sys.executable, "skills/aliyun-fullstack-deploy/scripts/build_release.py", str(project), "--config", str(config_path)])
    archive = json.loads(built.stdout)["zip"]
    inspected = run([sys.executable, "skills/aliyun-fullstack-deploy/scripts/inspect_release.py", archive])
    assert json.loads(inspected.stdout)["pass"] is True

    contract = {
        "capabilities": ["backend_client", "route_registration", "frontend_entry", "offline_fallback"],
        "required_files": ["backend/app/ai/client.py", "backend/app/ai/fallback.py", "frontend/src/api.ts", ".env.production.example"],
        "text_markers": [{"path": "backend/app/api/router.py", "contains": "ai"}],
        "environment_variables": ["AI_ENABLED", "AI_API_KEY"],
    }
    contract_path = temp / "contract.json"
    contract_path.write_text(json.dumps(contract), encoding="utf-8")
    validated = run([sys.executable, "skills/aliyun-fullstack-deploy/scripts/validate_ai_contract.py", str(project), "--contract", str(contract_path)])
    assert json.loads(validated.stdout)["pass"] is True


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        test_voice_todo(temp)
        test_csdn_linter(temp)
        test_skill_scaffold(temp)
        test_fit_and_public_audit(temp)
        test_release_and_ai_contract(temp)
    print("OK: voice HTML, CSDN lint, Skill scaffold, server fit, public audit, release, and AI contract smoke tests passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"Smoke test failed: {error}", file=sys.stderr)
        raise SystemExit(1)
