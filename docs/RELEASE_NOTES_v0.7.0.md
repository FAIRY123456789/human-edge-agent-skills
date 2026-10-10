# Human Edge Agent Skills v0.7.0 — Reproducible ECS Release Contracts

## Changes

- Added the read-only `release_preflight.py` gate for HNBLUE-style Java,
  Python/Flask, Vue, model and database deployments.
- Added `references/release.json` for source revision, lock files, required
  artifacts, runtime reports, protected shared state, rollback layout and
  redacted evidence.
- Strengthened `build_release.py` with plan/ready gates, SemVer enforcement for
  publishable artifacts, source-revision checks and provenance in `manifest.json`.
- Recorded lock-file and preflight evidence digests; wildcard excludes such as
  `.env.*` are honored.
- Documented evidence capture for atomic promotion and rollback without
  implicitly restoring shared state or databases.

## Verification scope

CI runs offline Python syntax, compatibility and release-contract tests. No
production ECS credentials, migrations or service mutations are used. Real
database queries, model loading, Java/Flask flows, Nginx validation and
rollback remain authorized canary checks.

## Honest boundaries

This release does not auto-upgrade Java, Python, MySQL, Redis or the host OS;
repair dependency drift; or claim a successful HNBLUE deployment. A `ready`
package means only that supplied redacted evidence passed its declared checks.
