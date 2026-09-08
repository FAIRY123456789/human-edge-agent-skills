# Build in Public Launcher

![Human Edge icon](assets/human-edge.svg)

Build in Public Launcher turns a finished or nearly finished project into a bounded, evidence-first launch. It helps assemble a credible README, demo, proof metric, distribution plan, and feedback loop without pretending that attention is adoption.

## Included Skill

- `build-in-public-launcher`: checks launch readiness, selects honest proof, builds a compact launch pack, and defines what to learn after release.

Use it when the artifact exists but the public story, demonstration, or feedback loop is weak. It does not publish posts, submit directories, or act on external accounts by itself.

## Example prompts

- “This repository is ready but has no launch story. Build an evidence-first launch pack from the files I provide.”
- “Audit this README and demo plan. Separate proven facts from claims that still need evidence.”
- “Design a seven-day GitHub-first launch with one useful proof metric and no vanity goals.”

## Install and test

From a clone of the repository:

```bash
claude plugin validate .
claude plugin marketplace add . --scope local
claude plugin install build-in-public-launcher@human-edge-skills --scope local
```

For Cursor local development, copy this complete plugin directory to `~/.cursor/plugins/local/build-in-public-launcher`, reload the Cursor window, and confirm the Skill appears under Customize. Marketplace listing is not implied.

From the repository root:

```bash
python scripts/sync_plugin_packages.py --check
python scripts/validate_plugin_packages.py
```

## Safety and honesty

Do not invent users, testimonials, stars, installs, revenue, benchmarks, or marketplace acceptance. Review private repository details before using them in public copy. Publishing and account actions remain explicit user decisions outside this plugin.

See [PRIVACY.md](PRIVACY.md) for the plugin's data-handling disclosure.

## Source and license

The canonical source is [`skills/build-in-public-launcher`](https://github.com/FAIRY123456789/human-edge-agent-skills/tree/main/skills/build-in-public-launcher). The packaged copy is generated and hash-checked; edit the canonical Skill, then run the sync command from the repository root.

MIT licensed. See `LICENSE`.
