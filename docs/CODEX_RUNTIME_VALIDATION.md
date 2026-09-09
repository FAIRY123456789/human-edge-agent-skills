# Codex Runtime Validation

**CODEX_RUNTIME = RUNTIME VALIDATED**

Snapshot: 2026-09-09, Windows, Codex CLI 0.153.4.

This validation used the current authenticated Codex product session. It did not call a paid LLM API, submit a marketplace listing, modify repository content from a model run, or take external account actions.

## Discovery, install, and reinstall

The current CLI uses `codex plugin add`, not the older/stale phrase `codex plugin install`.

```powershell
codex plugin marketplace add . --json
codex plugin list --marketplace human-edge-skills --available --json
codex plugin add voice-to-work@human-edge-skills --json
codex plugin add skill-from-scars@human-edge-skills --json
codex plugin add build-in-public-launcher@human-edge-skills --json
codex plugin add voice-with-temperature@human-edge-skills --json
```

Observed results:

| Check | Result |
|---|---|
| Marketplace registered | PASS: `human-edge-skills` resolved to the local repository root |
| Marketplace discovery | PASS: 4/4 entries discovered at version 1.0.0 |
| Initial install | PASS: 4/4 installed and `enabled=true` |
| Skill discovery | PASS: 5/5 packaged Skills loaded from the Codex plugin cache |
| Uninstall | PASS: 4/4 removed; all four returned to the available list |
| Clean reinstall | PASS: 4/4 reinstalled and `enabled=true` |
| Final cache integrity | PASS: SHA-256 of every cached `plugin.json` matches its repository source |

Final local state: the marketplace remains configured and all four plugins remain installed and enabled.

## Representative behavior runs

Each run used `codex exec --ephemeral --sandbox read-only`, explicitly named the Skill, prohibited file changes and external actions, and loaded the Skill from `C:\Users\Joy T\.codex\plugins\cache\human-edge-skills\...\1.0.0\skills\...\SKILL.md`.

| Plugin / Skill | Prompt under test | Observed result | Result |
|---|---|---|---|
| voice-to-work / voice-dump-to-todo | Poster deadline changed from tomorrow to Friday; send revised document, wait for Chen, decide about competition | Used Friday 2026-09-11, separated actions/waiting/decision, and attached feedback to the send dependency | PASS |
| voice-to-work / vibe-to-spec | Private study dashboard; left navigation, weekly goals, topic switching; no social/payments; persistence undecided | Produced explicit in/out scope, states, persistence boundary, unknowns, acceptance criteria, and `YES_WITH_ASSUMPTIONS` | PASS |
| skill-from-scars | Three Nginx regressions caused by skipping effective-config and legacy-route checks | Scored 12/14, extracted the invariant, hard gates, five discriminating evals, privacy limits, and a real-world maturity test | PASS |
| build-in-public-launcher | Finished, creator-tested open-source project with zero external users | Stated the evidence gap, used unassisted task completion rather than vanity metrics, and kept publication outside the run | PASS |
| voice-with-temperature | Clarify one personal sentence without inspirational copy; writing voice, not audio | Preserved the concrete tension and lived week, made a light edit, and returned the requested edit note | PASS |

These are five representative runtime checks, not a universal performance benchmark. The full reproducible routing set is `evals/marketplace-plugin-cases.json`.

## Non-blocking environment notes

The runtime repeatedly timed out on WebSocket transport and automatically completed over HTTPS. It also reported unrelated warnings from globally installed Skills. None prevented marketplace discovery, installed-cache loading, or final responses. No warning identified a component inside these four packages as missing.

The bundled `plugin-creator` scaffold validator currently insists on `.codex-plugin/plugin.json`; it reported that optional overlay as missing. This is not treated as a package failure because the current OpenAI documentation keeps root `plugin.json` canonical, the user prohibited mechanical duplication, and Codex 0.153.4 actually discovered, installed, and invoked all five Skills without the overlay. The repository's Agent Plugins schema validator and real runtime are the applicable evidence for this portable layout.

## State taxonomy

- Four packages: **STATIC VALIDATED**.
- Codex discovery/install/reinstall and five representative Skill runs: **RUNTIME VALIDATED**.
- OpenAI upload candidates: see `OPENAI_PLUGIN_SUBMISSION_FINAL.md`.
- Marketplace state: **NOT SUBMITTED**; therefore not under review or accepted.
