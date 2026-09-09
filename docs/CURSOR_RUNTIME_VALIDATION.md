# Cursor Runtime Validation

Snapshot: 2026-09-09 11:23:43 +08:00.

**CURSOR_STATIC = PASS**

**CURSOR_LOCAL_IMPORT = PASS**

**CURSOR_PLUGIN_DISCOVERY = PASS**

**CURSOR_SKILL_DISCOVERY = PASS**

**CURSOR_BEHAVIOR_TEST = USER VISUAL CHECK REQUIRED**

## Environment

| Item | Observed result |
|---|---|
| Windows | Windows 11 Home, 64-bit, version `10.0.26200`, build `26200` |
| Cursor | `3.19.13`, commit `dd066f332fcea7382764400fde902f61920648d0`, x64 |
| Cursor executable | `D:\Program Files\cursor\Cursor.exe` |
| Official shell launcher | `D:\Program Files\cursor\resources\app\bin\cursor.cmd` |
| Codex | `codex-cli 0.153.4` |

## Local import and integrity

Cursor's documented local-development route was used: complete plugin directories were copied to `%USERPROFILE%\.cursor\plugins\local\<plugin-name>`. No symlink was used, no canonical source file changed, and no existing non-empty local plugin directory was overwritten.

| Plugin | Files copied | Repository/local per-file SHA-256 |
|---|---:|---|
| `voice-to-work` | 14 | MATCH |
| `skill-from-scars` | 10 | MATCH |
| `build-in-public-launcher` | 9 | MATCH |
| `voice-with-temperature` | 9 | MATCH |

## Machine-readable discovery evidence

Cursor's official `Cursor Plugins` extension log under `%APPDATA%\Cursor\logs\20260909T104427\...\Cursor Plugins.20260909T104440_4eae1c7a.log` records each `loadUserLocalPlugin <name> loaded` event, followed by:

```text
loadUserLocalPlugins completed in 29.0ms (4 plugins loaded)
loadAllPlugins completed in 693.6ms (claude=true, userLocal=true, marketplace=2 sources, total=4 plugins, failures=0, sourceUnavailable=false)
Plugins reload completed: 4 plugins loaded (0 extension, 0 retained), 0 failures
```

Cursor's workspace state database key `workbench.customize.primitiveSourceSnapshot.skills.v3` contains all five packaged Skill identifiers:

1. `voice-dump-to-todo`
2. `vibe-to-spec`
3. `skill-from-scars`
4. `build-in-public-launcher`
5. `voice-with-temperature`

This is sufficient evidence for 4/4 plugin discovery, 5/5 Skill discovery, and no manifest/path/load failure.

## Unsuppressed warning

Cursor emits this warning once per plugin and continues loading:

```text
<plugin-name>: .claude-plugin/plugin.json declares an unrecognized $schema, loading anyway: https://json.schemastore.org/claude-code-plugin-manifest.json
```

The warning is non-fatal in Cursor 3.19.13. It is retained because removing the Claude schema marker solely to silence a different host would reduce editor validation and cannot be rechecked with Claude Code while that CLI is absent.

## Behavior boundary

The installed desktop shell launcher exposes editor operations but no machine-readable plugin invocation/list command. The available automation surface cannot control native Cursor windows, and no separate official Cursor Agent CLI capable of invoking these local plugins was found. The five representative prompts were therefore **NOT TESTED** in Cursor.

USER VISUAL CHECK REQUIRED: open Cursor, confirm the four local plugins and five Skills in Customize, then run the five prompts in `CURSOR_RUNTIME_TEST_GUIDE.md`. Record observed output without converting a discovery fact into a behavior PASS.

No Cursor Marketplace form was submitted and no terms were accepted.

Official references:

- https://prod.cursor.com/docs/plugins
- https://prod.cursor.com/docs/reference/plugins
