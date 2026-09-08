# Skill From Scars

![Human Edge icon](assets/human-edge.svg)

Skill From Scars helps decide whether repeated pain contains a reusable decision procedure or is merely a one-off lesson. When the evidence is strong enough, it structures a focused Agent Skill with references and evaluations instead of publishing a generic prompt.

## Included Skill

- `skill-from-scars`: mines retrospectives, debugging notes, failed prompts, transcripts, and work history for recurring pain; applies a worthiness gate; then scaffolds a testable Skill package.

Use it after the same failure has happened more than once and you have concrete source material. Do not use it to manufacture a Skill topic because a directory needs more content.

## Example prompts

- “Review these three retrospectives. Which repeated failure is generalizable enough to become an Agent Skill?”
- “Apply the worthiness gate to these debugging notes and explain why the result should or should not be packaged.”
- “Turn this repeated deployment mistake into a compact Skill design with evaluation cases, without inventing evidence.”

## Install and test

From a clone of the repository:

```bash
claude plugin validate .
claude plugin marketplace add . --scope local
claude plugin install skill-from-scars@human-edge-skills --scope local
```

For Cursor local development, copy this complete plugin directory to `~/.cursor/plugins/local/skill-from-scars`, reload the Cursor window, and confirm the Skill appears under Customize. Marketplace listing is not implied.

From the repository root:

```bash
python scripts/sync_plugin_packages.py --check
python scripts/validate_plugin_packages.py
```

## Safety and data handling

Retrospectives and logs often contain credentials, internal names, private conversations, or customer data. Redact them before use and before publishing any generated package. The Skill explicitly rejects invented benchmarks, users, compatibility claims, and evidence.

## Source and license

The canonical source is [`skills/skill-from-scars`](https://github.com/FAIRY123456789/human-edge-agent-skills/tree/main/skills/skill-from-scars). The packaged copy is generated and hash-checked; edit the canonical Skill, then run the sync command from the repository root.

MIT licensed. See `LICENSE`.
