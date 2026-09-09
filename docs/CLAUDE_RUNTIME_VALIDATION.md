# Claude Code Runtime Validation

Snapshot: 2026-09-09 11:23:43 +08:00.

**CLAUDE_STATIC = PASS**

**CLAUDE_VALIDATE = FAIL**

**CLAUDE_STRICT_VALIDATE = NOT SUPPORTED**

**CLAUDE_RUNTIME_DISCOVERY = FAIL**

**CLAUDE_RUNTIME_BEHAVIOR = FAIL**

These `FAIL` values describe an unavailable required runtime, not a manifest rejection. No `claude plugin validate` command ran because no Claude Code CLI executable was present.

## Environment

| Item | Observed result |
|---|---|
| Windows | Windows 11 Home, 64-bit, version `10.0.26200`, build `26200` |
| Claude Code CLI | **NOT TESTED — executable not found** |
| Claude Desktop | `1.49585.0`; installed and running from the Microsoft Store package |
| Codex | `codex-cli 0.153.4` |

The current process PATH, the official Windows native path `%USERPROFILE%\.local\bin\claude.exe`, the legacy `%USERPROFILE%\.claude\local` path, and the user npm global directory contain no Claude Code CLI. The running `claude.exe` processes resolve to the Electron-based Claude Desktop package; Claude Desktop is not substituted for the Claude Code command-line validator. CLI authentication status therefore cannot be checked.

No third-party Claude gateway, API key, paid API, credit purchase, authentication bypass, marketplace, or submission form was used.

## Official command check

Current official documentation confirms:

- `claude plugin validate <path>` exits `0` on validation success;
- `--strict` is supported and turns warnings into errors;
- local runtime testing uses one or more `--plugin-dir <plugin-root>` flags;
- plugin Skills are invoked as `/plugin-name:skill-name`.

The four normal and four strict validations, four discovery checks, and five representative behavior prompts are **NOT TESTED** on Claude Code because the required executable is absent. No warning output exists to record.

## Required next action

Install the official Claude Code CLI for Windows, or expose an existing official installation at its real path. Then run the four normal validations, four strict validations, load all four directories with `--plugin-dir`, confirm all five namespaced Skills, and run the five representative prompts. Until then Claude submission readiness is **BLOCKED** and `v0.5.0` must not be created.

Official references:

- https://code.claude.com/docs/en/installation
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/plugins
