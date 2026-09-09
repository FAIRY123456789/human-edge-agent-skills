# Claude Plugin Submission Final

**CLAUDE_STATIC = STATIC VALIDATED**

**CLAUDE_RUNTIME = NOT TESTED — CLAUDE CODE NOT INSTALLED**

**CLAUDE_RUNTIME_MODEL_TEST = BLOCKED_BY_AUTH**

**CLAUDE_SUBMISSION_READINESS = BLOCKED BY RUNTIME AND USER AUTHENTICATION**

Snapshot: 2026-09-09 (Asia/Shanghai).

The current host has no `claude` executable in PATH, common user installation paths, or installed-app records. No Claude-compatible gateway, API key, paid API, or substitute runtime was used. Therefore this document does not claim Claude discovery, install, model behavior, submission, review, or acceptance.

## Static package state

The repository has a Claude marketplace at `.claude-plugin/marketplace.json`. Each of the four self-contained packages has a non-empty `.claude-plugin/plugin.json` and default `skills/` discovery, with no Claude-only agents, commands, hooks, MCP servers, LSP servers, rules, or monitors.

| Order | Plugin | Display name | Skills | Static result |
|---:|---|---|---|---|
| 1 | `voice-to-work` | Voice to Work | `voice-dump-to-todo`, `vibe-to-spec` | PASS |
| 2 | `skill-from-scars` | Skill From Scars | `skill-from-scars` | PASS |
| 3 | `build-in-public-launcher` | Build in Public Launcher | `build-in-public-launcher` | PASS |
| 4 | `voice-with-temperature` | Voice With Temperature — Preserve Human Writing Voice | `voice-with-temperature` | PASS |

Static PASS means JSON parsing, required metadata, safe relative paths, exact package composition, self-containment, canonical-content drift, privacy links, and absence of prohibited components passed the repository validator. It is not equivalent to `claude plugin validate` or Claude runtime validation.

## Current official route

Anthropic's current Claude Code documentation identifies `claude-plugins-official` as the official marketplace and directs plugin authors to in-app submission forms in Claude.ai or Console. It also permits independent distribution through a publisher's own marketplace. The stage prompt's `claude-community` wording is not used as the final route because it is not the route named by the current official pages. The account owner must choose the applicable form and complete authentication and final confirmation.

Copyable source values:

| Field | Value |
|---|---|
| Repository | `FAIRY123456789/human-edge-agent-skills` |
| Marketplace file | `.claude-plugin/marketplace.json` |
| Author | Joy T |
| License | MIT |
| Privacy | A standalone `PRIVACY.md` exists in every plugin root |
| Support | https://github.com/FAIRY123456789/human-edge-agent-skills/issues |
| Submission state | NOT SUBMITTED |

## Required runtime gate on a Claude-enabled host

Use the exact commands shown by the installed current Claude Code version. The expected current flow to re-confirm is:

```bash
claude --version
claude plugin validate .
claude plugin marketplace add . --scope local
claude plugin install voice-to-work@human-edge-skills --scope local
```

Then repeat install/discovery and the representative cases in `evals/marketplace-plugin-cases.json` for all four plugins. Record version, OS, prompt, observed result, PASS/FAIL, uninstall, and clean reinstall. Do not change `CLAUDE_RUNTIME_MODEL_TEST = BLOCKED_BY_AUTH` until the user's official Claude account is already authenticated and the model run actually succeeds.

## Submission boundary

The manifests are **STATIC VALIDATED**. The Claude package is not yet **RUNTIME VALIDATED** or **READY FOR SUBMISSION** under this project's gate. No form was opened or submitted, and no terms or policy attestations were accepted.

Official references:

- https://code.claude.com/docs/en/plugins
- https://code.claude.com/docs/en/discover-plugins
- https://code.claude.com/docs/en/plugin-marketplaces
- https://platform.claude.com/plugins/submit
