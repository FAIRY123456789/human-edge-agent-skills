# Voice to Work

![Human Edge icon](assets/human-edge.svg)

Voice to Work turns messy spoken input into one of two concrete work products: an executable task list or an implementation-ready software specification. It is designed for voice transcripts and imperfect speech recognition, not for recording or transcribing audio.

## Included Skills

- `voice-dump-to-todo`: separates commitments, decisions, dependencies, due dates, and ideas; it can also render a standalone interactive HTML to-do.
- `vibe-to-spec`: turns a product idea dump into scope, flows, data/state, constraints, acceptance tests, unknowns, and implementation order.

Use this plugin when speech is faster and messier than the structure the final work needs. Choose the to-do Skill for personal execution and the spec Skill for software implementation.

## Example prompts

- “Here is a rough voice transcript. Separate real commitments from ideas, preserve uncertain names, and give me a prioritized to-do list with definitions of done.”
- “Turn this product idea dump into a coding-agent specification. Surface contradictions and unknowns instead of guessing.”
- “This transcript changes priority halfway through. Reconcile the latest intent and tell me what is blocked.”

## Install and test

From a clone of the repository, validate the whole local Claude marketplace:

```bash
claude plugin validate .
claude plugin marketplace add . --scope local
claude plugin install voice-to-work@human-edge-skills --scope local
```

For Cursor local development, copy this complete plugin directory to `~/.cursor/plugins/local/voice-to-work`, reload the Cursor window, and confirm that both Skills appear under Customize. Marketplace listing is not implied.

From the repository root, verify that packaged content still matches the canonical Skills:

```bash
python scripts/sync_plugin_packages.py --check
python scripts/validate_plugin_packages.py
```

## Safety and data handling

The Skills do not upload or transcribe audio. Review sensitive transcripts before sharing them with any host, remove secrets and private names when possible, and keep uncertain ASR repairs visible. Generated plans and specifications should be reviewed before execution.

See [PRIVACY.md](PRIVACY.md) for the plugin's data-handling disclosure.

## Source and license

The canonical sources are [`voice-dump-to-todo`](https://github.com/FAIRY123456789/human-edge-agent-skills/tree/main/skills/voice-dump-to-todo) and [`vibe-to-spec`](https://github.com/FAIRY123456789/human-edge-agent-skills/tree/main/skills/vibe-to-spec). Packaged copies are generated and hash-checked; edit the canonical Skills, then run the sync command from the repository root.

MIT licensed. See `LICENSE`.
