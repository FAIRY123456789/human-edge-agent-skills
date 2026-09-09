# Cross-Runtime Marketplace Status

Snapshot: 2026-09-09 (Asia/Shanghai). Public main at the start of this stage: `0d04b00707308378e78921f3d86c2a26d431d9eb`.

| Target | Static | Runtime | Submission readiness | External state |
|---|---|---|---|---|
| NVIDIA Tier 1, 18 canonical Skills | STATIC VALIDATED: 18/18 | Not a runtime test | Complete evidence retained | Not applicable |
| Codex, four plugins / five Skills | STATIC VALIDATED | RUNTIME VALIDATED on Codex CLI 0.153.4 | First two OpenAI uploads ready for user action | NOT SUBMITTED |
| Cursor, four plugins | STATIC VALIDATED | NOT TESTED: Cursor absent | BLOCKED by runtime | NOT SUBMITTED |
| Claude Code, four plugins | STATIC VALIDATED | NOT TESTED: CLI absent; model test BLOCKED_BY_AUTH | BLOCKED by runtime/auth | NOT SUBMITTED |
| OpenAI Universal Plugins Directory | Two deterministic Skills-only uploads validated | Codex runtime evidence available | `OPENAI_READY_FOR_USER_SUBMISSION` | NOT SUBMITTED |
| GitHub Awesome Copilot | Two candidate field sets pinned to `v0.4.0` | Copilot CLI / vally NOT TESTED | Ready for separately authorized issue submission | ISSUE NOT CREATED |
| skills.sh | CLI 1.5.25 discovers 18 | Directory indexes 1 Skill | Organic indexing only | 1 real total install |
| Gemini CLI Gallery | Five-Skill extension design feasible | NOT TESTED: CLI absent | Current monorepo gallery route rejected | NOT LISTED |

## Official-spec differences found

- Current Codex uses `codex plugin add`, while older wording may say `install`.
- Codex repository marketplaces use `.agents/plugins/marketplace.json`; the portable root `plugin.json` remains canonical, so no duplicated `.codex-plugin/plugin.json` overlay was needed.
- The local `plugin-creator` scaffold validator still requires its generated `.codex-plugin/plugin.json` layout. It is narrower than the documented portable-root route and was not used to override successful root-manifest schema and Codex runtime evidence.
- OpenAI has a documented Skills-only conversion path for Claude-compatible archives; final account identity, Apps Management access, availability, policy attestations, and `Submit for Review` remain user actions.
- Current Claude Code docs name `claude-plugins-official` and in-app Claude.ai/Console submission forms; the stage prompt's `claude-community` label is therefore treated as a generic community-submission goal, not a current marketplace identifier.
- GitHub Awesome Copilot now has a public external-plugin issue workflow. The older restrictive announcement is explicitly outdated. Direct edits to `plugins/external.json` are not the submission route.
- Gemini Gallery discovery requires a root manifest and repository topic; adding the manifest to this monorepo would expose all 18 root Skills rather than the intended five.

## Release decision

The user explicitly lifted the earlier cross-runtime release gate and approved publishing without waiting for Cursor or Claude runtime. [v0.4.0](https://github.com/FAIRY123456789/human-edge-agent-skills/releases/tag/v0.4.0) is public and resolves to `5930dcf59988aaa7a9a2358e6ec37dcd9ec7ee6d`. The release truthfully records NVIDIA Tier 1 18/18 and Codex runtime 4/4 plugins plus 5/5 Skills PASS; Cursor and Claude runtime remain **NOT TESTED**. No Marketplace or Awesome Copilot issue was submitted.

Detailed skills.sh evidence, including the directory URL and per-provider audit availability, is in `SKILLS_SH_STATUS.md`.

## State vocabulary

- **STATIC VALIDATED**: files, schemas, paths, privacy/security, and package composition passed without a host model run.
- **RUNTIME VALIDATED**: the named host actually discovered, installed, invoked, removed, and/or reinstalled the package as recorded.
- **READY FOR SUBMISSION**: the package and copy are ready for the user's final identity/policy actions.
- **SUBMITTED**, **UNDER REVIEW**, **ACCEPTED**: none applies to any target in this stage.
