# aliyun-fullstack-deploy

> **Canary-first deployment for small ECS and shared Linux servers**

Deploy React/Vue/Vite applications with Python, Node.js, or Java backends through evidence gates: inspect, package, canary, atomically promote, verify real flows, and roll back without sacrificing existing sites or persistent state.

**Category:** Engineering
**Keywords:** aliyun, ecs, linux-vps, nginx, systemd, canary, rollback, deployment

## Why it exists

A generic “deploy this project” prompt often discovers runtime drift, Nginx ownership, subpath errors, model incompatibility, or overwritten state only after production changes. This Skill makes those risks part of the deployment contract before mutation.

## Preview / install

```bash
gh skill preview FAIRY123456789/human-edge-agent-skills aliyun-fullstack-deploy
gh skill install FAIRY123456789/human-edge-agent-skills aliyun-fullstack-deploy
```

## First prompt

```text
Use $aliyun-fullstack-deploy to inspect this app and my authorized ECS. Show the deployment contract and stop before the first remote mutation.
```

The bundled promotion/canary adapters are tested around a Python layout. Node.js and Java deployments use the same evidence contract but still require project-specific start commands and validation hooks.

This repository claims no external adoption yet. Review every script before use and test on a disposable target before production.

## Compatibility preflight (v0.6.0)

For a Spring Boot + Flask + Vue deployment, first inspect the project's Maven target, Python dependency pins, trained model, frontend lockfile and static build. Then inspect the **authorized ECS** without changing services:

```bash
# On ECS, using the checked-in Skill scripts:
python3 scripts/probe_runtime.py --python-bin /usr/bin/python3.11 \\
  --packages flask,gunicorn,numpy,catboost --json-out ecs-runtime.json

# Locally, after securely retrieving and redacting the snapshot:
python scripts/runtime_matrix.py . \\
  --contract deploy/runtime-contract.json \\
  --server ecs-runtime.json --gate plan
```

Use [the HNBLUE-style contract example](references/runtime-contract.hnblue.example.json) and [runtime compatibility guide](references/runtime-compatibility.md) to define actual requirements. The checker reports PASS / ACTION_REQUIRED / REVIEW / BLOCK; it never installs dependencies or changes production. Recheck the selected Linux venv, test serialized model loading and validate the running MySQL/Redis service before switching a release. Generic canary/promotion shell adapters still target Python/Uvicorn and require project-specific replacements for Java and Flask/Gunicorn.
