# Human Edge Agent Skills v0.6.0 — ECS Runtime Compatibility Gates

## Changes

- Added a read-only runtime snapshot for Java, Python, Node, MySQL/Redis
  binaries and explicitly selected Python packages.
- Added project-to-server compatibility matrix for nested Maven projects,
  production Python requirements (including `-r`), locked frontend assets,
  database engine majors, and serialized-model artifacts.
- Added explicit PASS / ACTION_REQUIRED / REVIEW / BLOCK results and
  planning versus deployment-readiness exit gates.
- Added an HNBLUE-style non-secret runtime contract, compatibility guidance,
  and regression tests covering version drift, absent artifacts, false
  database assurance, frontend builds and unsafe requirement paths.
- Updated Skill and CI documentation. Existing release, canary and rollback
  adapters remain available with their documented runtime-specific limits.

## Verification scope

CI runs syntax checks, repository smoke tests and the new offline compatibility
test suite. No production ECS credentials are used. Real database version and
model unpickling tests still require an authorized server-side canary.

## Operational safety

Checks never install packages or mutate ECS. Remediation favors per-app
Java paths and Python virtual environments. Production database upgrades,
host OS changes, Nginx edits and canary promotion remain separate, authorized
operations. This version does not claim automatic repair of arbitrary
Java/Python dependencies or a successful deployment to HNBLUE.
