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

## Detect and preflight

Run:

```bash
python scripts/preflight_local.py <project-root>
```

Use the report to classify single-page and static assets, Python, Node.js, or Java APIs, root or subpath routing, state, model artifacts, and AI-provider integration. Resolve missing lockfiles, production build outputs, runtime incompatibility, secret matches, CRLF deployment scripts, and absolute development-machine paths before packaging.

Run `scripts/preflight_remote.sh` over SSH with environment variables that describe the intended app paths. Save its output locally, redact it with `scripts/redact_logs.py`, and inspect captured `nginx -T` output with `scripts/inspect_nginx.py`.

Create a rollback point before every remote mutation. Do not create a second wildcard Nginx server block. Modify only the server block proven to own the route, then require `nginx -t` before reload.

## Choose a runtime deliberately

- Python: pin an available interpreter by full path and build a new virtual environment when it differs from the artifact runtime. Install through that virtual-environment interpreter, never bare `pip`. Never ship Windows wheels to Linux.
- Node.js: honor the lockfile with `npm ci`, `pnpm --frozen-lockfile`, or the equivalent command documented by the repository. Prefer building static assets off-server when RAM is tight.
- Java: verify the JRE major against the built artifact and compare the JAR checksum before launch.
- Model artifacts: verify Python and library compatibility with the environment that serialized the model; rebuild the artifact when compatibility is not demonstrated.

Do not change the system runtime merely to satisfy one application when an isolated runtime is possible.

## Build a clean release

Create a small JSON config with `project_name`, immutable `version`, `includes`, and optional `excludes`, then run:

```bash
python scripts/build_release.py <project-root> --config <config.json>
python scripts/inspect_release.py <release.zip>
```

Require portable ZIP entries, UTF-8 LF deployment text, a manifest, checksums, required static and model assets, and no local environment-secret file, private key, Git data, local state, dependency directory, cache, or absolute Windows path.

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

## Report evidence, not confidence

Mark every gate `PASS`, `FAIL`, `NOT TESTED`, or `EXTERNALLY BLOCKED`. Include the public URL, active version and checksum, rollback target, redacted validation evidence, changed files, cleanup, remaining risks, and exact external action required.

Never claim completion while an in-scope check remains unresolved. After deployment, update the redacted server profile, version matrix, failure catalog, and validation record only with lessons demonstrated by evidence.
