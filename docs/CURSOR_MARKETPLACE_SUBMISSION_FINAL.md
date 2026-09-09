# Cursor Marketplace Submission Final

**CURSOR_PREFLIGHT = BLOCKED ONLY BY CURSOR RUNTIME TEST**

**CURSOR_RUNTIME = NOT TESTED — CURSOR NOT INSTALLED**

**CURSOR_READY_FOR_SUBMISSION = NO**

**MARKETPLACE = NOT SUBMITTED**

Snapshot date: 2026-09-09 (Asia/Shanghai)

This document contains factual, copyable submission material for the four plugins. It is preparation only. No Cursor Marketplace Submit action was taken.

## Current official preflight

Cursor currently supports the Agent Plugins open standard, accepts a root plugin.json or .cursor-plugin/plugin.json, documents monorepo discovery through .cursor-plugin/marketplace.json, and requires a public Git repository, clear metadata, valid component frontmatter and paths, a README, and local testing. Cursor also states that marketplace plugins are open source and manually reviewed.

Publisher Terms require accurate, non-misleading descriptions; appropriate privacy disclosures; reasonable security practices; publisher support; and a permissive license. The four packages use MIT and now expose a standalone PRIVACY.md from each README.

| Gate | Result | Evidence |
|---|---|---|
| Public repository | PASS | https://github.com/FAIRY123456789/human-edge-agent-skills |
| Root Agent Plugins manifests | PASS 4/4 | Local schema validation and public-clone verification |
| Cursor monorepo marketplace manifest | PASS | .cursor-plugin/marketplace.json; four unique relative sources |
| Names | PASS in repository | Lowercase kebab-case and unique across all four entries |
| Live exact-name collision search | No collision found | Not a guarantee; Cursor decides final uniqueness during review |
| Descriptions and component paths | PASS | Clear, factual descriptions; relative committed paths |
| README, logo, license, author | PASS 4/4 | Committed SVG logo, MIT, Joy T, repository links |
| Privacy and data handling | PASS 4/4 | Standalone PRIVACY.md linked from every plugin README |
| Unrequested capabilities | NONE | No MCP servers, hooks, commands, agents, rules, automatic permissions, or secret declarations |
| Static/security regression | PASS | Canonical, plugin schema, drift, secret, syntax, JSON, link, and smoke checks |
| Cursor runtime discovery and behavior | NOT TESTED | Cursor is absent from the preflight host |

The authenticated publish form was not submitted. If its live fields differ from the manifest fields below, preserve the same factual wording and do not add unverified compatibility, usage, customer, benchmark, or adoption claims.

The repository marketplace manifest contains category and keywords metadata supported by Cursor's plugin reference. They are not presented below as Publisher form fields because the public, unauthenticated live page did not expose a reliable form to confirm those fields.

## Submission 1: voice-to-work

| Field | Copyable value |
|---|---|
| Package name | voice-to-work |
| Display name | Voice to Work |
| Version | 1.0.0 |
| One-line description | Turn noisy spoken task and product dumps into executable todos or implementation-ready specifications. |
| Repository | https://github.com/FAIRY123456789/human-edge-agent-skills |
| Plugin source path | plugins/voice-to-work |
| Included Skills | voice-dump-to-todo; vibe-to-spec |
| License | MIT |
| Author | Joy T |
| Data handling | Local instruction package; publisher collects no data and operates no service. Host processing follows host terms. Optional render_todo.py reads user JSON and writes user-selected local HTML only. |
| Network and permissions | No publisher endpoint, telemetry, network calls, MCP, hooks, commands, agents, rules, secrets, environment variables, or automatic permissions. |
| Validation evidence | NVIDIA Tier 1 PASS; Agent Plugins schema PASS; package self-containment and canonical drift PASS; Gitleaks no leaks; syntax, JSON, links, and smoke tests PASS. |
| Reviewer note | Repairs only high-confidence ASR errors and leaves ambiguous names visible. It does not upload or transcribe audio. |

Long description:

Voice to Work packages two focused Agent Skills. voice-dump-to-todo turns messy spoken notes into actions, decisions, dependencies, and optional local HTML. vibe-to-spec turns a spoken product idea into an implementation contract with scope, flows, state, constraints, acceptance criteria, and build order. Both preserve uncertainty instead of silently guessing ambiguous entities. It is part of the Human Edge Agent Skills project.

## Submission 2: skill-from-scars

| Field | Copyable value |
|---|---|
| Package name | skill-from-scars |
| Display name | Skill from Scars |
| Version | 1.0.0 |
| One-line description | Decide whether repeated pain deserves a reusable Agent Skill, then shape it into a testable package. |
| Repository | https://github.com/FAIRY123456789/human-edge-agent-skills |
| Plugin source path | plugins/skill-from-scars |
| Included Skills | skill-from-scars |
| License | MIT |
| Author | Joy T |
| Data handling | Local instruction package; publisher collects no data and operates no service. Users must redact sensitive retrospectives. Optional scaffold_skill.py reads user JSON and writes a user-selected local Skill folder only. |
| Network and permissions | No publisher endpoint, telemetry, network calls, MCP, hooks, commands, agents, rules, secrets, environment variables, or automatic permissions. |
| Validation evidence | NVIDIA Tier 1 PASS; Agent Plugins schema PASS; package self-containment and canonical drift PASS; Gitleaks no leaks; syntax, JSON, links, and smoke tests PASS. |
| Reviewer note | Applies a worthiness gate before scaffolding and explicitly rejects invented users, benchmarks, compatibility claims, and evidence. |

Long description:

Skill from Scars helps turn repeated operational pain into a narrowly scoped, testable Agent Skill. It first checks whether the pattern is recurring and reusable, then defines triggers, boundaries, workflow, progressive disclosure, and behavior evals. It can optionally create a local starter folder from explicit structured input. It is part of the Human Edge Agent Skills project.

## Submission 3: build-in-public-launcher

| Field | Copyable value |
|---|---|
| Package name | build-in-public-launcher |
| Display name | Build in Public Launcher |
| Version | 1.0.0 |
| One-line description | Turn a finished project into an evidence-first public launch without invented traction or vanity metrics. |
| Repository | https://github.com/FAIRY123456789/human-edge-agent-skills |
| Plugin source path | plugins/build-in-public-launcher |
| Included Skills | build-in-public-launcher |
| License | MIT |
| Author | Joy T |
| Data handling | Local instruction package; publisher collects no data and operates no service. Users must remove private repository, customer, credential, and confidential metric data before drafting public material. |
| Network and permissions | No scripts, publisher endpoint, telemetry, network calls, publishing, account actions, MCP, hooks, commands, agents, rules, secrets, environment variables, or automatic permissions. |
| Validation evidence | NVIDIA Tier 1 PASS; Agent Plugins schema PASS; package self-containment and canonical drift PASS; Gitleaks no leaks; syntax, JSON, links, and smoke tests PASS. |
| Reviewer note | Generates launch preparation only. It does not publish and forbids invented installs, stars, users, testimonials, revenue, benchmarks, or marketplace acceptance. |

Long description:

Build in Public Launcher converts verified project evidence into honest launch assets and a measured distribution plan. It separates facts from claims, blocks fabricated traction, and keeps publishing and account actions outside the plugin as explicit user decisions. It is part of the Human Edge Agent Skills project.

## Submission 4: voice-with-temperature

| Field | Copyable value |
|---|---|
| Package name | voice-with-temperature |
| Display name | Voice With Temperature — Preserve Human Writing Voice |
| Version | 1.0.0 |
| One-line description | Edit written prose for clarity while preserving the writer's lived detail, uncertainty, rhythm, and emotional temperature. |
| Repository | https://github.com/FAIRY123456789/human-edge-agent-skills |
| Plugin source path | plugins/voice-with-temperature |
| Included Skills | voice-with-temperature |
| License | MIT |
| Author | Joy T |
| Data handling | Local instruction package; publisher collects no data and operates no service. Users should obtain consent and remove private details before editing personal or third-party stories. |
| Network and permissions | No scripts, publisher endpoint, telemetry, network calls, audio processing, voice cloning, MCP, hooks, commands, agents, rules, secrets, environment variables, or automatic permissions. |
| Validation evidence | NVIDIA Tier 1 PASS; Agent Plugins schema PASS; package self-containment and canonical drift PASS; Gitleaks no leaks; syntax, JSON, links, and smoke tests PASS. |
| Reviewer note | “Voice” means writing voice. The plugin does not process speech, generate audio, clone voices, or impersonate people. |

Long description:

Voice With Temperature edits text without sanding away the writer's uncertainty, rhythm, lived details, or emotional register. It improves clarity while preventing invented memories, expertise, citations, and confidence. It is a writing tool, not a speech or audio tool, and is part of the Human Edge Agent Skills project.

## Cursor runtime blocker

No Cursor executable was found in PATH, common user installation paths, installed-app records, or running processes on the current Windows host, and none was installed. Complete [CURSOR_RUNTIME_TEST_GUIDE.md](CURSOR_RUNTIME_TEST_GUIDE.md) on a current Cursor release, record all four discovery and prompt checks, and only then change the preflight status.

Current final status: **BLOCKED ONLY BY CURSOR RUNTIME TEST**.

## skills.sh live status

- The current pinned skills CLI 1.5.25 recognized the public repository and listed all 18 Skills with telemetry disabled; `--list` did not install any Skill.
- The public repository page remains partial: it presents one indexed Skill (`vibe-to-spec`) and one real total install.
- The public audit API exposes PASS reports for that indexed Skill from Gen Agent Trust Hub (SAFE with a minor indirect-prompt-injection note), Socket (no alerts), and Snyk (LOW, no issues). A sampled unindexed Skill audit URL returned 404.
- No fake installations or telemetry-generating repetitions were performed.
- **NO MANUAL INDEXING ROUTE FOUND**. The documented leaderboard is driven by anonymous CLI installation telemetry.

## Release and state boundary

Cursor is **STATIC VALIDATED** but not **RUNTIME VALIDATED** or **READY FOR SUBMISSION**. The user explicitly approved publishing [v0.4.0](https://github.com/FAIRY123456789/human-edge-agent-skills/releases/tag/v0.4.0) without waiting for Cursor or Claude runtime; this does not change the Cursor status or create a compatibility claim. The release resolves to `5930dcf59988aaa7a9a2358e6ec37dcd9ec7ee6d`. Nothing was submitted to Cursor, and nothing is under review or accepted there.

## Claude route deferred

No Claude account, API, installation, runtime validation, submission, or marketplace action was used. Current Claude documentation names `claude-plugins-official` as the official marketplace and directs authors to the Claude.ai or Console in-app submission forms; independent repositories can also distribute their own marketplaces. Before any future submission, install a current Claude Code runtime, run the documented plugin validator, test each plugin through the local plugin directory route, and confirm invocation behavior. This work remains intentionally deferred.

## Official references

- [Cursor Plugins](https://prod.cursor.com/docs/plugins)
- [Cursor Plugin Reference](https://prod.cursor.com/docs/reference/plugins)
- [Cursor Marketplace Publisher Terms](https://cursor.com/marketplace-publisher-terms)
- [Cursor Marketplace Publish](https://cursor.com/marketplace/publish)
- [skills CLI documentation](https://www.skills.sh/docs/cli)
- [skills.sh documentation](https://www.skills.sh/docs)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude community submission form](https://platform.claude.com/plugins/submit)
