# Cross-Runtime Marketplace Status

Snapshot: 2026-09-09 11:23:43 +08:00. Public main at the start of this stage: `50193b967c8edbf9a3e74255dfcfff2cf31eb5c8`.

| Validator / host | Static validated | Manifest validated | Runtime discovered | Behavior tested |
|---|---|---|---|---|
| NVIDIA SkillEvaluator, 18 canonical Skills | STATIC VALIDATED: 18/18 | Not applicable | Not applicable | Not applicable |
| Codex CLI 0.153.4, 4 plugins / 5 Skills | STATIC VALIDATED | PASS 4/4 | RUNTIME VALIDATED: 4/4 plugins, 5/5 Skills | RUNTIME VALIDATED: 5/5 |
| Claude Code | STATIC VALIDATED | NOT TESTED: Claude Code CLI absent | NOT TESTED | NOT TESTED |
| Cursor 3.19.13, 4 plugins / 5 Skills | STATIC VALIDATED | PASS 4/4 repository schema checks | RUNTIME VALIDATED: 4/4 plugins, 5/5 Skills | USER VISUAL CHECK REQUIRED |

| Submission target | Readiness | External state |
|---|---|---|
| OpenAI Universal Plugins Directory | READY FOR SUBMISSION: two deterministic Skills-only uploads | NOT SUBMITTED |
| Claude | BLOCKED: official CLI validate and runtime not completed | NOT SUBMITTED |
| Cursor Marketplace | BLOCKED: representative behavior test requires user visual check | NOT SUBMITTED |
| GitHub Awesome Copilot | READY FOR SUBMISSION: two field sets pinned to `v0.4.0` | ISSUE NOT CREATED |

## Official-spec differences found

- Current Codex uses `codex plugin add`, while older wording may say `install`.
- Codex repository marketplaces use `.agents/plugins/marketplace.json`; the portable root `plugin.json` remains canonical, so no duplicated `.codex-plugin/plugin.json` overlay was needed.
- The local `plugin-creator` scaffold validator still requires its generated `.codex-plugin/plugin.json` layout. It is narrower than the documented portable-root route and was not used to override successful root-manifest schema and Codex runtime evidence.
- OpenAI has a documented Skills-only conversion path for Claude-compatible archives; final account identity, Apps Management access, availability, policy attestations, and `Submit for Review` remain user actions.
- Current Claude Code docs name `claude-plugins-official` and in-app Claude.ai/Console submission forms; the stage prompt's `claude-community` label is therefore treated as a generic community-submission goal, not a current marketplace identifier.
- GitHub Awesome Copilot now has a public external-plugin issue workflow. The older restrictive announcement is explicitly outdated. Direct edits to `plugins/external.json` are not the submission route.
- Gemini Gallery discovery requires a root manifest and repository topic; adding the manifest to this monorepo would expose all 18 root Skills rather than the intended five.

## Release decision

The historical [v0.4.0](https://github.com/FAIRY123456789/human-edge-agent-skills/releases/tag/v0.4.0) release remains immutable at `5930dcf59988aaa7a9a2358e6ec37dcd9ec7ee6d`.

`v0.5.0` was **not created**. Cursor plugin and Skill discovery passed, but Cursor behavior remains **USER VISUAL CHECK REQUIRED** and the required Claude Code CLI validation/discovery is **BLOCKED** because only Claude Desktop is installed. The release gate therefore does not pass.

All repository regressions passed: canonical validator 18/18, Agent Plugins schema 4/4, Claude manifest metadata 4/4, Cursor marketplace manifest, package drift 5/5, Gitleaks 8.30.1 on `plugins/`, tracked Python syntax 18/18, Bash syntax 6/6, operational JSON parse 21/21, 110 relative-link targets across 108 Markdown files, deterministic OpenAI ZIP rebuild, and functional smoke tests. The retained NVIDIA raw JSON has a known local ACL mismatch and was not re-parsed. NVIDIA Tier 1 was not re-run because canonical Skill content did not change.

Detailed skills.sh evidence, including the directory URL and per-provider audit availability, is in `SKILLS_SH_STATUS.md`.

## State vocabulary

- **STATIC VALIDATED**: files, schemas, paths, privacy/security, and package composition passed without a host model run.
- **RUNTIME VALIDATED**: the named host actually discovered, installed, invoked, removed, and/or reinstalled the package as recorded.
- **READY FOR SUBMISSION**: the package and copy are ready for the user's final identity/policy actions.
- **SUBMITTED**, **UNDER REVIEW**, **ACCEPTED**: none applies to any target in this stage.
