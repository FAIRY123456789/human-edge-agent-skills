# GitHub Awesome Copilot Submission Final

**AWESOME_COPILOT_PREFLIGHT = READY FOR USER-AUTHORIZED ISSUE SUBMISSION**

**ISSUE STATE = NOT CREATED**

Snapshot: 2026-09-09 (Asia/Shanghai).

The current official contribution guide now supports public third-party external plugins through an issue-based review workflow. This supersedes the older restrictive policy retained in Discussion #1172 for historical transparency. Public v1 submissions must use a public GitHub repository, `source.source: "github"`, a release tag/ref and/or full immutable SHA, and the official external-plugin issue form. Contributors must not edit `plugins/external.json` directly.

Automated intake later runs metadata validation, `vally lint`, and an ephemeral Copilot CLI install smoke test. Neither `vally` nor GitHub Copilot CLI is installed on this host, and no unpinned remote package was executed to imitate those checks.

## Immutable review artifact

The user explicitly approved releasing the Codex-validated package without waiting for Cursor or Claude runtime tests. The public release is [v0.4.0](https://github.com/FAIRY123456789/human-edge-agent-skills/releases/tag/v0.4.0), and its annotated tag resolves to commit `5930dcf59988aaa7a9a2358e6ec37dcd9ec7ee6d`.

- immutable ref: `v0.4.0`;
- full commit SHA: `5930dcf59988aaa7a9a2358e6ec37dcd9ec7ee6d`;
- Awesome Copilot issue creation: **NOT AUTHORIZED IN THIS STAGE; ISSUE NOT CREATED**.

The machine-readable entry drafts in `submission-assets/awesome-copilot/` pin both locators. Cursor local discovery is **RUNTIME VALIDATED** for four plugins and five Skills, but its behavior remains **USER VISUAL CHECK REQUIRED**; Claude Code remains **NOT TESTED** because its CLI is absent. Neither is claimed as GitHub Copilot compatibility evidence. GitHub's automated `vally lint` and Copilot CLI install smoke test will run only after a future, separately authorized issue submission.

## Candidate 1 — skill-from-scars

| Issue field | Copyable value |
|---|---|
| Plugin name | `skill-from-scars` |
| Short description | Decide whether repeated pain deserves a reusable Agent Skill, then shape it into a testable package. |
| Owner/repo | `FAIRY123456789/human-edge-agent-skills` |
| Plugin path | `plugins/skill-from-scars` |
| Immutable ref | `v0.4.0` |
| Full commit SHA | `5930dcf59988aaa7a9a2358e6ec37dcd9ec7ee6d` |
| Plugin version | `1.0.0` |
| License | `MIT` |
| Author | Joy T |
| Author URL | https://github.com/FAIRY123456789 |
| Homepage | https://github.com/FAIRY123456789/human-edge-agent-skills/tree/v0.4.0/plugins/skill-from-scars |
| Keywords | `agent-skills`, `knowledge-capture`, `retrospectives` |

Reviewer notes:

> This developer-focused plugin extracts an invariant decision procedure from repeated engineering failures, applies a 7-dimension worthiness gate, rejects one-off or generic prompt packaging, and creates testable conditions without fabricating users, benchmarks, compatibility, or evidence. It contains one Skill, an optional local standard-library scaffolder, no network integration, and no external account action. Codex runtime validation loaded and invoked the installed Skill on a three-incident Nginx regression pattern.

Why first: it directly improves Agent Skill authoring and evaluation, exposes a specific gap beyond generic coding ability, and has explicit rejection criteria.

## Candidate 2 — voice-to-work

| Issue field | Copyable value |
|---|---|
| Plugin name | `voice-to-work` |
| Short description | Turn noisy spoken task and product dumps into executable todos or implementation-ready specifications. |
| Owner/repo | `FAIRY123456789/human-edge-agent-skills` |
| Plugin path | `plugins/voice-to-work` |
| Immutable ref | `v0.4.0` |
| Full commit SHA | `5930dcf59988aaa7a9a2358e6ec37dcd9ec7ee6d` |
| Plugin version | `1.0.0` |
| License | `MIT` |
| Author | Joy T |
| Author URL | https://github.com/FAIRY123456789 |
| Homepage | https://github.com/FAIRY123456789/human-edge-agent-skills/tree/v0.4.0/plugins/voice-to-work |
| Keywords | `productivity`, `specifications`, `voice-input` |

Reviewer notes:

> This plugin addresses noisy human intent before coding begins. It routes personal execution dumps to `voice-dump-to-todo` and product/system ideas to `vibe-to-spec`; later corrections override earlier intent, and uncertain names remain visible. It consumes supplied text transcripts and does not record, transcribe, identify speakers, use accounts, or call external services. Codex runtime validation loaded and invoked both installed Skills.

Why second: the specification workflow is relevant to Copilot users, but the personal to-do route is broader than a purely developer workflow and may require a stronger reviewer explanation.

## Intentionally excluded from the first issue batch

- `voice-with-temperature`: not included; primarily a writing workflow.
- `build-in-public-launcher`: not included; useful for developer launches but less central than the first two under the collection's “meaningful uplift beyond base-model strengths” rule.

## Future user-controlled sequence

1. Review the pinned `skill-from-scars` intake fields and machine-readable draft.
2. Optionally run `vally lint` and a Copilot CLI smoke test if official, pinned tooling becomes available; record any result without converting `NOT TESTED` into a claim.
3. Only with a new explicit user instruction, open one external-plugin issue for `skill-from-scars`.
4. After reviewing the first intake result, decide whether to authorize a separate `voice-to-work` issue.

No issue, PR, comment, label change, or submission was created.

Official references:

- https://github.com/github/awesome-copilot/blob/main/CONTRIBUTING.md
- https://github.com/github/awesome-copilot/blob/main/eng/external-plugin-validation.mjs
