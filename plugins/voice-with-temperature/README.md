# Voice With Temperature

![Human Edge icon](assets/human-edge.svg)

Voice With Temperature edits prose for clarity without washing out the person who wrote it. Here “voice” means writing voice—lived detail, uncertainty, rhythm, specificity, and emotional temperature—not speech, audio, transcription, or voice synthesis.

## Included Skill

- `voice-with-temperature`: diagnoses generic AI smoothing, preserves meaning and texture, and produces a clearer draft plus a concise account of consequential edits.

Use it for essays, reflections, technical writing, speeches, bios, or posts where conventional polishing makes the writing fluent but less true.

## Example prompts

- “Edit this reflection for clarity, but keep the awkward detail and uncertainty that make it mine.”
- “This technical post sounds AI-smoothed. Restore sentence rhythm and specific observations without adding claims.”
- “Give me a light edit and a stronger edit, then explain which emotional choices changed.”

## Install and test

From a clone of the repository:

```bash
claude plugin validate .
claude plugin marketplace add . --scope local
claude plugin install voice-with-temperature@human-edge-skills --scope local
```

For Cursor local development, copy this complete plugin directory to `~/.cursor/plugins/local/voice-with-temperature`, reload the Cursor window, and confirm the Skill appears under Customize. Marketplace listing is not implied.

From the repository root:

```bash
python scripts/sync_plugin_packages.py --check
python scripts/validate_plugin_packages.py
```

## Safety and authorship

The Skill should not invent memories, experiences, expertise, citations, or certainty. Review the result for factual drift and consent before publishing personal or third-party stories. It improves writing; it is not an impersonation or audio-generation tool.

See [PRIVACY.md](PRIVACY.md) for the plugin's data-handling disclosure.

## Source and license

The canonical source is [`skills/voice-with-temperature`](https://github.com/FAIRY123456789/human-edge-agent-skills/tree/main/skills/voice-with-temperature). The packaged copy is generated and hash-checked; edit the canonical Skill, then run the sync command from the repository root.

MIT licensed. See `LICENSE`.
