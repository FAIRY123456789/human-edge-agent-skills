# voice-dump-to-todo

> **Messy speech in, executable to-do out**

Repair high-confidence ASR errors from context, extract actions/decisions/waiting items, and render a standalone interactive desktop to-do.

**Category:** Voice Native
**Keywords:** voice, asr, todo, productivity, local-html

## Use it when

The task described in [`SKILL.md`](SKILL.md) keeps recurring and a generic assistant response would miss the workflow, guardrails, or output contract encoded here.

## Preview / install

```bash
gh skill preview FAIRY123456789/human-edge-agent-skills voice-dump-to-todo
gh skill install FAIRY123456789/human-edge-agent-skills voice-dump-to-todo

# Or via the Skills CLI ecosystem
npx skills add https://github.com/FAIRY123456789/human-edge-agent-skills --skill voice-dump-to-todo
```

Inspect `SKILL.md` and any `references/`, `assets/`, or `scripts/` before installing. Agent Skills can contain executable resources.

## Proof status

This repository does not claim external adoption yet. The next evidence target is real task completion by external users, followed by repeat use, useful issues/PRs, or measurable workflow improvement.
