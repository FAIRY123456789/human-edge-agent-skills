---
name: aliyun-fullstack-deploy
description: Deploy full-stack apps to user-authorized Alibaba Cloud ECS or comparable Linux VPS hosts with preflight, canary verification, and rollback. Use for production deployment and recovery; never purchase infrastructure or mutate an unauthorized host.
license: MIT
metadata:
  author: Joy T <101039451+FAIRY123456789@users.noreply.github.com>
  tags:
    - deployment
    - alibaba-cloud
    - devops
---

# Aliyun Full-Stack Deploy

## Purpose

Turn a repository and an authorized ECS into a reproducible, rollback-ready release. Move through explicit evidence gates: inspect, contract, preflight, package, canary, promote, verify, and report.

This Skill subsumes the earlier `safe-shared-vps-deploy` workflow: preserve existing sites and services as explicit protected assets, even when the target is not Alibaba Cloud.

## Start with a deployment contract

1. Read repository-level agent instructions and deployment documentation.
2. Confirm the project root, SSH host alias or address, SSH user and port, public route, app and service names, runtime, state locations, protected existing sites, and validation hooks.
3. Confirm the user owns or administers the target. Treat inspection as read-only; ask immediately before the first remote mutation unless the user already authorized deployment.
4. Prefer a dedicated deployment account with access only to the application paths and service controls it needs. Use privilege elevation only for a specifically authorized system change.
5. Keep passwords, tokens, private keys, and database URLs in SSH Agent, interactive input, or server-side environment files. Never print or copy them into the repository, release, command arguments, or report.
6. Read [references/workflow.md](references/workflow.md). If server capacity or runtime choice is uncertain, also read [references/runtime-selection.md](references/runtime-selection.md).
7. Create a server profile from [references/server-profile-template.md](references/server-profile-template.md). Re-run preflight instead of trusting an old profile.

Stop before mutation if the contract lacks a rollback target, persistence plan, protected-site inventory, or success checks.

## Make `release.json` the version-alignment contract

Copy [references/release.json](references/release.json) into the application as
`deploy/release.json`. Replace its example paths and version with observed
HNBLUE values. The contract records the reviewed source revision, immutable
release inputs, lock files, required files, runtime/evidence paths, protected
shared state and rollback layout. It is the input to the read-only gate:

```bash
python scripts/release_preflight.py . \
  --config deploy/release.json --server evidence/ecs-runtime.json \
  --gate plan --json-out evidence/release-preflight.json
```

`PASS`, `ACTION_REQUIRED`, `REVIEW` and `BLOCK` remain explicit. `plan` stops
only on `BLOCK`; `ready` additionally requires SemVer, source provenance, all
lock/required files and a PASS runtime matrix. This gate never installs,
migrates, promotes, edits Nginx or changes an ECS.

## Detect and preflight

Run:

```bash
python scripts/preflight_local.py <project-root>
```

Use the report to classify single-page and static assets, Python, Node.js, or Java APIs, root or subpath routing, state, model artifacts, and AI-provider integration. Resolve missing lockfiles, production build outputs, runtime incompatibility, secret matches, CRLF deployment scripts, and absolute development-machine paths before packaging.

Run `scripts/preflight_remote.sh` over SSH with environment variables that describe the intended app paths. Save its output locally, redact it with `scripts/redact_logs.py`, and inspect captured `nginx -T` output with `scripts/inspect_nginx.py`.

Create a rollback point before every remote mutation. Do not create a second wildcard Nginx server block. Modify only the server block proven to own the route, then require `nginx -t` before reload.

## Runtime compatibility matrix (required before packaging)

Read [references/runtime-compatibility.md](references/runtime-compatibility.md). For Java/Python/Vue hybrids, use an explicit non-secret runtime contract; a sample for HNBLUE-style layouts is [references/runtime-contract.hnblue.example.json](references/runtime-contract.hnblue.example.json).

1. Run `preflight_local.py` and identify nested Maven/Flask paths. On the authorized ECS, run `probe_runtime.py` with the intended Python interpreter and an explicit allowlist of critical pip packages; keep the snapshot private and redact it before sharing.
2. Run `runtime_matrix.py <project> --contract <contract.json> --server <snapshot.json> --gate plan`, or let `release_preflight.py` run it from `deploy/release.json`. Examine every PASS / ACTION_REQUIRED / REVIEW / BLOCK result, including library pins, Java bytecode target, browser artifacts, DB server provenance, native ABI, and model files.
3. Prefer installing an app-specific JRE or Linux venv and repeat the probe. Never auto-upgrade a live database, replace a system-owned runtime, change Nginx for another project, or mutate ECS solely because a comparison indicates drift.
4. `--gate ready` must pass before production promotion; real model load, database connectivity, Java/Flask routes and existing-site checks still require explicit project hooks. The general canary/promotion scripts remain Python/Uvicorn-specific and **must be adapted** for Spring Boot + Flask/Gunicorn.

If any required version remains unknown, report REVIEW or ACTION_REQUIRED; do not treat the absence of detected errors as compatibility proof.

## Choose a runtime deliberately

- Python: pin an available interpreter by full path and build a new virtual environment when it differs from the artifact runtime. Install through that virtual-environment interpreter, never bare `pip`. Never ship Windows wheels to Linux.
- Node.js: honor the lockfile with `npm ci`, `pnpm --frozen-lockfile`, or the equivalent command documented by the repository. Prefer building static assets off-server when RAM is tight.
- Java: verify the JRE major against the built artifact and compare the JAR checksum before launch.
- Model artifacts: verify Python and library compatibility with the environment that serialized the model; rebuild the artifact when compatibility is not demonstrated.

Do not change the system runtime merely to satisfy one application when an isolated runtime is possible.

## Build a clean release

Create `deploy/release.json` from the checked-in template. Then run the ready
gate and build:

```bash
python scripts/release_preflight.py <project-root> --config deploy/release.json \
  --server evidence/ecs-runtime.json --gate ready \
  --json-out evidence/release-preflight.json
python scripts/build_release.py <project-root> --config deploy/release.json \
  --preflight-report evidence/release-preflight.json --gate ready
python scripts/inspect_release.py <release.zip>
```

The builder refuses a missing/non-PASS ready report, missing lock/required file,
source drift or a path outside the project. Its schema-versioned manifest
records source revision, lock files, contract/evidence digests and gate result.
Require portable ZIP entries, UTF-8 LF deployment text, checksums, required
static/model assets, and no environment-secret file, private key, Git data,
local state, dependency directory, cache or absolute Windows path.

For AI-enabled apps, copy [references/ai-contract.example.json](references/ai-contract.example.json), define an explicit JSON contract, and run `scripts/validate_ai_contract.py`. The contract must cover the backend client, route registration, frontend entry, environment-variable names, and offline and failure behavior without containing secret values.

## Canary before production

Upload the verified archive by checksum and extract it outside the production path. Use a unique loopback port and isolated temporary state or a safe read-only snapshot.

The bundled `scripts/deploy_canary.sh` is a Python and FastAPI adapter. For Node.js or Java, preserve the same invariants: isolated directory, loopback binding, one disposable process, bounded readiness check, isolated state, and captured logs.

Canary proof must include the homepage, actual JavaScript and CSS assets, core APIs, one complete user flow, persistence or report export when applicable, AI offline behavior, and AI online behavior only when a key is already configured on the server. A health endpoint alone is never sufficient.

## Promote atomically

Use version directories such as `/opt/<app>/releases/<version>`, shared state outside releases, and an atomic `current` symlink. Preserve the existing server-side environment file. Back up systemd and Nginx configuration before a validated, idempotent edit.

Use `scripts/promote_release.sh` for its supported Python layout only after the canary passes. For other runtimes, implement the same atomic switch and automatic service-health rollback rather than editing the active release in place.

For a subpath, align the frontend build base, client router base, API base, upload and download URLs, Nginx location semantics, deep-route fallback, health URL, and documentation.

## Verify and roll back

Run bounded GET checks; do not treat a HEAD 405 as a GET failure. `scripts/verify_deployment.sh` verifies real asset bodies and MIME types and supports a project-specific `VERIFY_HOOK`.

Verify systemd state, one intended backend process, loopback binding, writable shared state, page HTML, actual hashed assets, deep-route refresh, browser console and network activity, mobile layout, core data and API flows, report or upload flows, AI fallback, protected existing sites, idempotent redeploy, rollback, and post-rollback data preservation.

Automatically roll back for service or readiness failure, JavaScript-as-HTML, core API 500, Nginx validation failure, protected-site regression, missing model or AI import, unwritable persistence, failed export, or browser white screen. Do not restore shared state unless corruption is proven and data recovery is separately authorized.

Capture rollback evidence before and after the switch: previous/candidate
release names, ZIP/JAR/model SHA-256, `current` target, systemd status, Nginx
`-t`, bounded core-flow responses and the exact rollback command. A symlink
rollback is not a database backup; schema/data recovery needs a separate,
tested and authorized backup plan.

## Report evidence, not confidence

Mark every gate `PASS`, `FAIL`, `NOT TESTED`, or `EXTERNALLY BLOCKED`. Include the public URL, active version and checksum, rollback target, redacted validation evidence, changed files, cleanup, remaining risks, and exact external action required.

Never claim completion while an in-scope check remains unresolved. After deployment, update the redacted server profile, version matrix, failure catalog, and validation record only with lessons demonstrated by evidence.
