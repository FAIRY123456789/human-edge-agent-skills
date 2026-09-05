# Deployment workflow reference

## Contents

1. Inputs and permissions
2. Project classification
3. Local gate
4. Server gate
5. Canary gate
6. Promotion gate
7. Validation gate
8. Rollback and cleanup

## Inputs and permissions

Collect project root, host/alias, SSH user/port, app name, route, domains, protected paths, runtime constraints, state locations, service name, Nginx ownership, AI provider variables, and validation hooks. Confirm the user owns or administers the target. Credentials stay in Agent, interactive input, environment files, or provider control planes.

## Project classification

| Signal | Type | Build/runtime |
|---|---|---|
| `vite.config.*` + React/Vue | SPA | lock-file install, static `dist` |
| `fastapi` requirements/import | FastAPI | pinned Python venv + one or more Uvicorn workers according to state model |
| Flask/Django marker | Python API | framework-specific WSGI/ASGI command |
| `package.json` server entry | Node API | pinned Node + systemd |
| `pom.xml`/`build.gradle` | Spring Boot | pinned JRE + built JAR |
| uploads/JSON/JSONL | file persistence | shared writable state outside releases |
| migrations/DB URL | database | backup and migration plan required |
| AI client/config | AI-enabled | backend-only secret and offline fallback checks |

## Local gate

Require source tests, production build, dependency locks, import check, artifact/data presence, route inventory, subpath consistency, secret scan, LF scripts, forward ZIP paths, dotfiles, release manifest/checksums, AI completeness, and package inspection. Refuse a package containing `.env`, private keys, Git data, local storage, `node_modules`, `.venv`, caches, or platform-incompatible wheels.

## Server gate

Capture exact OS/kernel/architecture, CPU/memory/disk, user/groups, package manager, firewall/security-group note, SELinux, runtime versions, listening ports, systemd state, Nginx `-T`, directories/owners/modes, current releases, backup capacity, and bounded internal health. Hash protected site entry files before mutation.

Probe Python indices with commands such as `python -m pip index versions <critical-package> --index-url <url>` using timeouts. Choose a source only when critical versions and download tests pass. Retain pip cache for retry.

## Canary gate

Use a unique directory and loopback port. Do not share live writable state unless the test is explicitly safe; use a temporary state root or snapshot. Exercise actual imports and model/data paths, not only health. Test AI offline always; test online with one necessary call when a key is already configured. Store only mode/status, never the key or private question text.

## Promotion gate

Create `/opt/<app>/releases/<version>`, shared state such as `/opt/<app>/shared/storage`, and atomic `current` symlink. Preserve `.env` in shared/root-owned location. Save previous target and config hashes. Stop/restart only the named service. Validate Nginx before reload. Never edit protected root content.

For an SPA subpath `/app/`, prefer an exact redirect for `/app`, an API location before the SPA location, direct static service, and `try_files` to the app's own index. Verify the actual chosen `root`/`alias` expansion.

## Validation gate

Use GET with `--connect-timeout`, `--max-time`, and limited retries. Parse asset names from `index.html`; do not guess hashes. Assert status, MIME, and non-HTML body. Run all domain validation hooks, persistence/report/export checks, tenant isolation, browser desktop/mobile, console/network inspection, protected site comparison, idempotent redeploy, rollback, and reboot recovery.

## Rollback and cleanup

Switch `current` back to the recorded previous target and restart. Do not restore shared state unless corruption is separately proven and the user authorizes data recovery. Re-verify protected sites and application. Remove only canary processes/directories created by the current run after resolving their absolute paths. Retain the release, rollback metadata, redacted log, and at least one verified backup.
