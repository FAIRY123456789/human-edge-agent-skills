# Monorepo and Discovery Strategy

## Recommendation: one canonical repository now

Use one repository: `human-edge-agent-skills`.

GitHub's current Agent Skills workflow explicitly allows a repository to contain multiple skill folders and lets users install one named skill directly:

```bash
gh skill install OWNER/REPOSITORY SKILL
```

This makes a monorepo compatible with skill-level installation while preserving a single public entry point.

Official reference:
https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills

## Why this is better for the current stage

1. One resume/personal-site link.
2. One GitHub star/watch/fork surface instead of splitting weak early traction across many repos.
3. One issue tracker and release history.
4. Cross-skill composition is easier to explain.
5. Individual Skill names/descriptions remain independent discovery metadata.
6. Each skill has a human README and deep link for search engines and social sharing.

## Discovery work inside the monorepo

- Keep `agent-skills` in the repository name or description.
- Give every `SKILL.md` a precise `name` and trigger-rich `description`.
- Give every Skill its own `README.md` with problem keywords.
- Maintain `catalog.json` for future website/plugin indexing.
- Add GitHub topics that cover the repository's high-level theme, not all 18 niches.
- Create releases with 2–4 flagship Skills in the release notes rather than listing everything equally.
- Link directly to `skills/<name>/` when sharing a specific Skill.

Suggested GitHub topics:

`agent-skills`, `ai-agents`, `human-ai`, `vibe-coding`, `codex`, `claude-code`, `github-copilot`, `prompt-engineering`, `build-in-public`, `productivity`, `open-source`.

## When to spin a Skill out

Create a standalone repo only when at least two are true:

- it has independent external users;
- it attracts its own issues or PRs;
- it needs a different release cadence;
- it grows substantial scripts/assets beyond the monorepo norm;
- users primarily discover/share it without the umbrella brand.

Until then, splitting is mostly administrative overhead.
