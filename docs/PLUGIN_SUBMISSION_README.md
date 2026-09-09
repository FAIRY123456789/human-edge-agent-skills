# Plugin Submission README

This is the copy-ready source for manually submitting the four Human Edge Agent Skills plugins to Claude and Cursor. Use the exact factual text below, adapt only a platform's required formatting, and do not add unverified compatibility, user, install, revenue, benchmark, review, or acceptance claims.

## Shared publisher fields

| Field | Copyable value |
|---|---|
| Publisher / developer | Joy T |
| GitHub account | `FAIRY123456789` |
| Repository | https://github.com/FAIRY123456789/human-edge-agent-skills |
| Release | https://github.com/FAIRY123456789/human-edge-agent-skills/releases/tag/v0.5.0 |
| Support | https://github.com/FAIRY123456789/human-edge-agent-skills/issues |
| License | MIT |
| Plugin package version | 1.0.0 |
| Repository release version | v0.5.0 |
| Marketplace state | Not submitted to Claude or Cursor |

Each plugin has its own `README.md`, `PRIVACY.md`, `LICENSE`, SVG logo, portable Agent Plugins 1.0 `plugin.json`, Claude manifest, and complete self-contained Skill folder. The publisher operates no hosted service and collects no telemetry or user content. Host-side processing follows the selected host's terms.

## Validation claims you may use

- NVIDIA SkillEvaluator Tier 1: 18/18 canonical Skills passed; 0 incomplete, 0 CRITICAL, 0 HIGH. This retained result was not rerun for v0.5.0 because canonical Skill content did not change.
- Repository checks: Agent Plugins schema 4/4, Claude manifest metadata 4/4, self-containment 4/4, canonical/package drift 5/5, Gitleaks no leaks, syntax/JSON/link/smoke checks passed.
- Codex CLI 0.153.4: 4/4 plugins and 5/5 packaged Skills discovered and behavior-tested.
- Cursor 3.19.13: complete local imports matched repository hashes; 4/4 plugins loaded with zero failures; all 5 Skills appeared in the machine-readable Customize snapshot.
- Cursor prompt behavior: USER VISUAL CHECK REQUIRED. Do not claim prompt-level Cursor PASS until you personally run and record the five checks.
- Claude Code: STATIC VALIDATED only. Claude Code CLI validation, discovery, and behavior are NOT TESTED because the CLI was unavailable. Do not claim Claude runtime compatibility.

## Platform source values

### Cursor

| Field | Value |
|---|---|
| Marketplace repository | `https://github.com/FAIRY123456789/human-edge-agent-skills` |
| Monorepo index | `.cursor-plugin/marketplace.json` |
| Local source root | `plugins/<plugin-name>` |
| Runtime evidence | Cursor 3.19.13; 4/4 plugins and 5/5 Skills discovered; zero load failures |
| Remaining check | Run the five representative prompts in `CURSOR_RUNTIME_TEST_GUIDE.md` and record the visible outputs |

Cursor emitted one non-fatal warning per package and still loaded all four: `.claude-plugin/plugin.json declares an unrecognized $schema, loading anyway: https://json.schemastore.org/claude-code-plugin-manifest.json`. Keep this warning visible. Do not remove Claude metadata merely to silence another host.

### Claude

| Field | Value |
|---|---|
| Marketplace repository | `FAIRY123456789/human-edge-agent-skills` |
| Marketplace index | `.claude-plugin/marketplace.json` |
| Marketplace name | `human-edge-skills` |
| Static package state | 4/4 manifests and package paths validated by repository checks |
| Runtime state | NOT TESTED — Claude Code CLI unavailable |

If a Claude form asks about compatibility testing, answer that the package is statically validated but Claude Code runtime validation has not been completed. Do not substitute the installed Claude Desktop app as Claude Code evidence.

## Plugin 1 — Voice to Work

| Field | Copyable value |
|---|---|
| Package name | `voice-to-work` |
| Display name | Voice to Work |
| Version | 1.0.0 |
| Category | Productivity |
| Keywords | `voice-input`, `productivity`, `specifications`, `asr`, `task-management` |
| Source path | `plugins/voice-to-work` |
| Included Skills | `voice-dump-to-todo`, `vibe-to-spec` |
| Short description | Turn messy speech into tasks or build-ready specs. |
| Long description | Convert imperfect voice transcripts into prioritized actions or implementation contracts while preserving corrections, dependencies, and uncertain names. Part of the Human Edge Agent Skills project. |
| Website | https://github.com/FAIRY123456789/human-edge-agent-skills/tree/main/plugins/voice-to-work |
| Privacy | https://github.com/FAIRY123456789/human-edge-agent-skills/blob/main/plugins/voice-to-work/PRIVACY.md |
| Terms / license | https://github.com/FAIRY123456789/human-edge-agent-skills/blob/main/plugins/voice-to-work/LICENSE |
| Data handling | Local instruction package; publisher collects no data and operates no service. Optional `render_todo.py` reads user-supplied JSON and writes user-selected local HTML only. |
| Network / permissions | No publisher endpoint, telemetry, network call, MCP server, hook, command, agent, rule, secret, environment variable, or automatic permission. |
| Reviewer note | Repairs only high-confidence ASR errors and leaves ambiguous names visible. It structures user-supplied text and does not record, upload, transcribe, or identify speakers in audio. |

Starter prompts:

1. Turn this voice transcript into a prioritized to-do list.
2. Turn this product idea dump into an implementation-ready spec.
3. Reconcile later corrections in this transcript without guessing names.

## Plugin 2 — Skill from Scars

| Field | Copyable value |
|---|---|
| Package name | `skill-from-scars` |
| Display name | Skill from Scars |
| Version | 1.0.0 |
| Category | Developer Tools |
| Keywords | `agent-skills`, `retrospectives`, `knowledge-capture`, `skill-authoring`, `evaluation` |
| Source path | `plugins/skill-from-scars` |
| Included Skill | `skill-from-scars` |
| Short description | Turn repeated failures into testable Agent Skills. |
| Long description | Apply a worthiness gate to recurring operational pain, then define a focused Skill with boundaries, progressive disclosure, and behavior evaluations. Part of the Human Edge Agent Skills project. |
| Website | https://github.com/FAIRY123456789/human-edge-agent-skills/tree/main/plugins/skill-from-scars |
| Privacy | https://github.com/FAIRY123456789/human-edge-agent-skills/blob/main/plugins/skill-from-scars/PRIVACY.md |
| Terms / license | https://github.com/FAIRY123456789/human-edge-agent-skills/blob/main/plugins/skill-from-scars/LICENSE |
| Data handling | Local instruction package; publisher collects no data and operates no service. Users must redact sensitive retrospectives. Optional `scaffold_skill.py` writes only a user-selected local Skill folder. |
| Network / permissions | No publisher endpoint, telemetry, network call, MCP server, hook, command, agent, rule, secret, environment variable, or automatic permission. |
| Reviewer note | Applies a worthiness gate before scaffolding and explicitly rejects invented users, benchmarks, compatibility claims, and evidence. |

Starter prompts:

1. Decide whether these repeated failures deserve a reusable Skill.
2. Turn this retrospective pattern into a testable Skill design.
3. Apply a worthiness gate before scaffolding this Skill.

## Plugin 3 — Build in Public Launcher

| Field | Copyable value |
|---|---|
| Package name | `build-in-public-launcher` |
| Display name | Build in Public Launcher |
| Version | 1.0.0 |
| Category | Productivity |
| Keywords | `product-launch`, `open-source`, `validation`, `build-in-public`, `evidence` |
| Source path | `plugins/build-in-public-launcher` |
| Included Skill | `build-in-public-launcher` |
| Short description | Build an evidence-first launch without fake traction. |
| Long description | Turn a finished project into an honest launch pack, proof plan, distribution experiment, and learning loop without inventing users, installs, or benchmarks. Part of the Human Edge Agent Skills project. |
| Website | https://github.com/FAIRY123456789/human-edge-agent-skills/tree/main/plugins/build-in-public-launcher |
| Privacy | https://github.com/FAIRY123456789/human-edge-agent-skills/blob/main/plugins/build-in-public-launcher/PRIVACY.md |
| Terms / license | https://github.com/FAIRY123456789/human-edge-agent-skills/blob/main/plugins/build-in-public-launcher/LICENSE |
| Data handling | Local instruction package; publisher collects no data and operates no service. Users must remove private repository, customer, credential, and confidential metric data before drafting public material. |
| Network / permissions | No scripts, publisher endpoint, telemetry, network call, publishing, account action, MCP server, hook, command, agent, rule, secret, environment variable, or automatic permission. |
| Reviewer note | Generates launch preparation only. It does not publish and forbids invented installs, stars, users, testimonials, revenue, benchmarks, or marketplace acceptance. |

Starter prompts:

1. Build an evidence-first launch pack for this finished project.
2. Separate verified proof from claims that still need evidence.
3. Design a small launch experiment without vanity metrics.

## Plugin 4 — Voice With Temperature

| Field | Copyable value |
|---|---|
| Package name | `voice-with-temperature` |
| Display name | Voice With Temperature — Preserve Human Writing Voice |
| Version | 1.0.0 |
| Category | Writing |
| Keywords | `writing`, `editing`, `writing-voice`, `prose`, `human-voice` |
| Source path | `plugins/voice-with-temperature` |
| Included Skill | `voice-with-temperature` |
| Short description | Edit prose without flattening the writer's voice. |
| Long description | Improve written prose while preserving lived detail, uncertainty, sentence rhythm, and emotional register. This plugin edits text; it does not process speech or audio. Part of the Human Edge Agent Skills project. |
| Website | https://github.com/FAIRY123456789/human-edge-agent-skills/tree/main/plugins/voice-with-temperature |
| Privacy | https://github.com/FAIRY123456789/human-edge-agent-skills/blob/main/plugins/voice-with-temperature/PRIVACY.md |
| Terms / license | https://github.com/FAIRY123456789/human-edge-agent-skills/blob/main/plugins/voice-with-temperature/LICENSE |
| Data handling | Local instruction package; publisher collects no data and operates no service. Users should obtain consent and remove private details before editing personal or third-party stories. |
| Network / permissions | No script, publisher endpoint, telemetry, network call, audio processing, voice cloning, MCP server, hook, command, agent, rule, secret, environment variable, or automatic permission. |
| Reviewer note | “Voice” means writing voice. The plugin does not process speech, generate audio, clone voices, or impersonate people. |

Starter prompts:

1. Edit this prose for clarity without flattening my writing voice.
2. Remove AI-sounding polish while keeping concrete lived detail.
3. Give me a light edit and explain the consequential changes.

## Before each manual submission

1. Confirm the live form still matches the current official documentation.
2. Select your own verified publisher identity; do not invent an organization or team.
3. Use the plugin-specific privacy and license URLs, not a generic placeholder.
4. Keep external authentication, hosted service, telemetry, and network access set to none.
5. For Cursor, finish and record the five visual behavior prompts before claiming behavior PASS.
6. For Claude, state that runtime is not tested until the official Claude Code CLI actually validates and invokes the plugins.
7. Review the final preview, policy attestations, availability, and distribution choices yourself before submitting.
8. Treat submission as review pending, never as acceptance or publication.

Detailed evidence: [Cursor runtime](CURSOR_RUNTIME_VALIDATION.md), [Cursor form draft](CURSOR_MARKETPLACE_SUBMISSION_FINAL.md), [Claude static/runtime boundary](CLAUDE_RUNTIME_VALIDATION.md), [Claude form draft](CLAUDE_COMMUNITY_SUBMISSION_FINAL.md), and [OpenAI first-batch package fields](OPENAI_PLUGIN_SUBMISSION_FINAL.md).
