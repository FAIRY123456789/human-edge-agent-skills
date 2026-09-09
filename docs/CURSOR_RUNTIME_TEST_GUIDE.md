# Cursor Runtime Test Guide

**CURSOR_DISCOVERY = RUNTIME VALIDATED — 4/4 PLUGINS, 5/5 SKILLS**

**CURSOR_BEHAVIOR = USER VISUAL CHECK REQUIRED**

Updated: 2026-09-09 (Asia/Shanghai)

The validation host is Windows 11 Home x64, version `10.0.26200`, build `26200`. Cursor `3.19.13` is installed. Complete local plugin copies were hash-checked and Cursor's own extension log recorded four plugins loaded with zero failures; its workspace Skill snapshot contained all five packaged Skill names. See [`CURSOR_RUNTIME_VALIDATION.md`](CURSOR_RUNTIME_VALIDATION.md) for the machine-readable evidence and retained warning.

This guide now covers only the remaining human behavior gate before a Cursor Marketplace submission. It follows Cursor's documented local-plugin directory route.

## 1. Prepare the host

1. Open the installed Cursor release and sign in using the intended publisher account.
2. Update this repository and confirm the checkout is at the intended revision.
3. Confirm the four complete source directories exist under `plugins/`.

## 2. Copy the plugins locally

Run these commands from the repository root in PowerShell. They replace only the four named local test copies.

    $cursorLocal = Join-Path $env:USERPROFILE '.cursor\plugins\local'
    New-Item -ItemType Directory -Force -Path $cursorLocal | Out-Null
    Copy-Item -Recurse -Force plugins\voice-to-work (Join-Path $cursorLocal 'voice-to-work')
    Copy-Item -Recurse -Force plugins\skill-from-scars (Join-Path $cursorLocal 'skill-from-scars')
    Copy-Item -Recurse -Force plugins\build-in-public-launcher (Join-Path $cursorLocal 'build-in-public-launcher')
    Copy-Item -Recurse -Force plugins\voice-with-temperature (Join-Path $cursorLocal 'voice-with-temperature')

If the destination already exists, remove that exact named test directory first or verify no stale files remain. Do not delete the parent local directory.

Cursor already detected these four copies without a manual reload in the recorded run. If repeating the test after a change, restart Cursor or run Developer: Reload Window. Open Customize and confirm each plugin and its Skills are discoverable. Team and Enterprise policies may disable local plugin imports; ask the organization administrator if the local entries do not appear.

## 3. Record discovery and prompt checks

Use a new chat for each plugin. Do not grant permissions that the plugin does not declare, and do not publish any output.

| Plugin | Discovery | Minimal prompt | Expected evidence |
|---|---|---|---|
| voice-to-work | Plugin appears; voice-dump-to-todo and vibe-to-spec both appear | Convert a noisy transcript containing “Open Clara brief... maybe Klara?” into tasks, then turn a product dump into a spec. | Ambiguous entity remains visible; todo is actionable; spec includes scope and acceptance criteria. |
| skill-from-scars | Plugin and one Skill appear | Provide three similar failure notes and ask whether they deserve a reusable Skill. | Applies a worthiness gate, produces a bounded workflow, and proposes eval cases without invented users or benchmarks. |
| build-in-public-launcher | Plugin and one Skill appear | Prepare a launch from supplied repository evidence with no usage metrics. | Does not invent installs, stars, testimonials, users, revenue, acceptance, or publish anything. |
| voice-with-temperature | Plugin and one Skill appear | Edit a short personal draft while preserving uncertainty, rhythm, and lived detail. | Improves clarity without inventing memories or expertise; clearly behaves as text editing, not audio or speech. |

For each row, record:

- Cursor version and operating system
- Discovery location and exact displayed Skill names
- Prompt used
- Expected result
- Observed result
- PASS or FAIL
- Screenshot or redacted transcript path, if retained

Any discovery failure, unexpected permission request, network action, invented evidence, or misleading audio behavior is a submission blocker.

## 4. Cleanup

After testing, remove only these exact local test directories if desired:

    voice-to-work
    skill-from-scars
    build-in-public-launcher
    voice-with-temperature

Restart or reload Cursor again. If an installed Marketplace plugin has the same name, Cursor may prioritize that version over a local copy; remove or disable the installed copy before retesting.

## 5. Completion rule

Discovery is complete. Change the behavior and submission-readiness status in this guide and in `CURSOR_MARKETPLACE_SUBMISSION_FINAL.md` only after all five prompt-level checks pass on the current Cursor runtime. Until then the repository status remains:

**USER VISUAL CHECK REQUIRED**

## Official references

- [Cursor Plugins](https://prod.cursor.com/docs/plugins)
- [Cursor Plugin Reference](https://prod.cursor.com/docs/reference/plugins)
- [Cursor Marketplace Publisher Terms](https://cursor.com/marketplace-publisher-terms)
