# Gemini CLI Gallery Feasibility

**GEMINI_EXTENSION_PACKAGE = FEASIBLE**

**CURRENT MONOREPO GALLERY LISTING = NOT READY**

**GEMINI_RUNTIME = NOT TESTED — CLI NOT INSTALLED**

Snapshot: 2026-09-09 (Asia/Shanghai).

Gemini CLI extensions can include auto-discovered Agent Skills under `skills/`, but a gallery-discoverable extension requires `gemini-extension.json` at the absolute root of the public repository or release archive. The gallery crawler discovers public GitHub repositories carrying the `gemini-cli-extension` topic.

## Desired five-Skill bundle

The five low-risk, already packaged Skills are technically suitable for an independent extension:

1. `voice-dump-to-todo`
2. `vibe-to-spec`
3. `skill-from-scars`
4. `build-in-public-launcher`
5. `voice-with-temperature`

They require no MCP server, hook, remote service, API key, or Gemini-specific runtime dependency.

## Monorepo conflict

The current repository root already has `skills/` containing all 18 canonical Skills. Adding a root `gemini-extension.json` would allow default discovery to expose all 18, including Skills intentionally classified outside the low-risk marketplace set. The current Gemini manifest model does not provide a trustworthy exclusion mechanism for “discover only these five from the existing root skills directory.”

For that reason, this stage does not add a root Gemini manifest, repository topic, release asset, second public repository, or gallery claim.

## Minimum-cost next options

| Option | Cost | Risk | Recommendation |
|---|---:|---|---|
| Dedicated five-Skill extension repository | Moderate | Lowest discovery ambiguity; new lifecycle to maintain | Preferred when the user authorizes a second public repo |
| Self-contained release archive with manifest at archive root | Low–moderate | Direct packaging is feasible, but automatic gallery crawling from a monorepo release must be re-confirmed live | Good experiment before creating a repo; do not claim listing until observed |
| Root manifest in this canonical monorepo | Low | Exposes all 18 and breaks the intended safety classification | Reject |
| Duplicate five Skills under another root subdirectory | Low initially | Creates drift and weakens the canonical source model | Reject |

The safe next experiment is a locally generated archive containing only `gemini-extension.json`, the five Skill folders, license, privacy, and README, followed by local Gemini CLI validation on an installed current version. Do not add the gallery topic or publish the archive until that runtime check passes and the gallery's release-archive discovery behavior is confirmed.

Official references:

- https://geminicli.com/docs/extensions/
- https://geminicli.com/docs/extensions/writing-extensions/
- https://geminicli.com/docs/extensions/releasing/
- https://geminicli.com/docs/extensions/reference/
