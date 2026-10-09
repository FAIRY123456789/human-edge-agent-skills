# Runtime compatibility gate (read-only)

Version compatibility is checked **before packaging**, rechecked after installing an
isolated runtime on ECS, and proven by a service and model canary before promotion.
The generic Skill must not change the host's default interpreter, system Java,
database engine, or another site's services to satisfy one application.

## 1. Local project and server probes

Define a project-specific, non-secret JSON contract. Start from
`references/runtime-contract.hnblue.example.json` for a Spring Boot + Flask
project, then adjust every version and model path to observed facts.

Locally, inspect the Maven POM, production Python requirements, lockfile and
model paths. On the **authorized ECS**, upload and run the read-only probe:

```bash
python3 scripts/probe_runtime.py --python-bin /usr/bin/python3.11 \\
  --packages flask,gunicorn,numpy,catboost,scikit-learn \\
  --json-out /tmp/ecs-runtime.json
```

The reported MySQL/Redis version comes from a binary, so it does not prove the
**running** server's version. Managed RDS/Redis must be queried separately
using authorized read-only access. The probe never reads environment secrets,
runs migrations, installs software or changes the machine.

Transfer the redacted JSON to the local machine, then run:

```bash
python scripts/runtime_matrix.py . \\
  --contract deploy/runtime-contract.json \\
  --server ecs-runtime.json \\
  --json-out runtime-report.json --gate plan
```

The Python checker requires only Python 3.8+ on the **analysis** machine.
The ECS probe supports Python 3.6+. In the runtime report:

| Status | Meaning | Required handling |
|---|---|---|
| PASS | Observed constraint matches | Still perform live import/API tests |
| ACTION_REQUIRED | Install/build/configure compatible environment | Re-probe before continuing |
| REVIEW | Insufficient evidence or potential incompatibility | Collect evidence; never silently pass |
| BLOCK | Missing required artifact / untrustworthy input | Stop deployment |

`--gate plan` exits 2 on BLOCK. `--gate ready` exits 2 on **anything**
other than PASS. In both modes the script is read-only.

## 2. Remediation priority

1. For Java, install a supported JRE side-by-side and point the application's
   systemd unit to its **absolute** binary path; do not change another service.
2. For Python, select the compatible interpreter first, create a **new Linux
   venv**, install production requirements in that venv, run
   `python -m pip check` and explicitly load the serialized model.
3. For Vue SPA, respect the local lockfile, run a production build off-server
   and ship `dist`; no Node runtime is needed on the ECS for static assets.
4. For MySQL/Redis, inspect the actual running service and protocol/SQL
   compatibility. Use a backed-up, tested migration plan if incompatible.
   **Never auto-upgrade a live database**.
5. For native wheels (NumPy/CatBoost), verify target Linux architecture,
   interpreter ABI, and availability of compatible distributions. Model pickle
   compatibility requires a real load plus representative inference.

When the OS is obsolete, evaluate a side-by-side runtime first, then an
isolated container only if kernel/architecture permit it, then a tested OS
migration or replacement ECS. A replacement ECS is a last resort, not a
reaction to a Java or Python major-version mismatch.

## 3. Separate generic policy from project-specific execution

`deploy_canary.sh` and `promote_release.sh` in this repository currently
target Python/Uvicorn and the path `backend/requirements.txt`. For
Spring Boot + Flask/Gunicorn, implement and test **project-specific** canary,
systemd commands, model paths and rollback hooks. Do not run those generic
adapters unchanged against HNBLUE. Test Java JAR startup, Flask import,
model inference, DB read/write limits, Redis operations, frontend subpaths,
Nginx and existing protected sites before production promotion.

A server profile may contain `runtimes.mysql.source=server_query` and
`validation.model_smoke_passed=true` **only after** those exact checks
succeeded and their redacted evidence was retained. Never set validation
fields to true just to make the gate green. Deployment evidence must identify
which checks were actually performed and which remain NOT TESTED.

## 4. Compatibility evidence is not capacity evidence

Verify CPU architecture, disk headroom, RAM under load, model memory usage,
restart behavior and timeout limits separately. A version-compatible JAR may
still fail due to low memory, incorrect SQL schema, wrong credentials or
unavailable model assets. Successful runtime comparison authorizes an isolated
canary, not an unconditional public release.
