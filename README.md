# Human Edge Agent Skills

> **Human judgment where generic AI is weakest: messy voice, social tact, ambiguous decisions, real-world experiments, and safe shipping.**

English · [简体中文](README.zh-CN.md)

AI is increasingly good at generating possibilities. The scarce part is still human: understanding a relationship, repairing noisy speech from context, deciding what matters this week, translating across fields, preserving a real voice, testing ideas against reality, and knowing when a result has enough proof to show the world.

This repository packages those recurring workflows as portable `SKILL.md` folders.

## Start with four flagship Skills

| Skill | The moment it helps |
|---|---|
| [`vibe-to-spec`](skills/vibe-to-spec/) | You can explain the product aloud, but the coding agent still needs an implementation contract. |
| [`trend-to-microbet`](skills/trend-to-microbet/) | A new AI trend feels urgent, but you need a 48-hour to 7-day test instead of two weeks of FOMO. |
| [`social-signal-and-tact`](skills/social-signal-and-tact/) | The message is factually correct but socially stiff, over-formal, or hard to answer. |
| [`skill-from-scars`](skills/skill-from-scars/) | The same failure happened often enough that it may deserve a tested reusable workflow. |

Each Skill has one job, a trigger-rich `description`, and an independent install path. The rest of the repository is the supporting catalog—not eighteen equally loud claims.

## The 18 Skills

| Skill | Group | One-line job |
|---|---|---|
| [`social-signal-and-tact`](skills/social-signal-and-tact/) | Social & Communication | Human tact for upward communication |
| [`csdn-technical-writing`](skills/csdn-technical-writing/) | Creator & Writing | Long-form Chinese technical writing without AI micro-paragraphs |
| [`student-money-four-buckets`](skills/student-money-four-buckets/) | Young Life | A four-layer student budget that still leaves room for fun |
| [`voice-dump-to-todo`](skills/voice-dump-to-todo/) | Voice Native | Messy speech in, executable to-do out |
| [`fitness-recovery-coach`](skills/fitness-recovery-coach/) | Young Life | Training plans that respect recovery instead of forcing the calendar |
| [`cross-domain-translator`](skills/cross-domain-translator/) | Judgment & Translation | Translate problem structure across domains, not just terminology |
| [`voice-with-temperature`](skills/voice-with-temperature/) | Creator & Writing | Make writing clearer without washing the human out of it |
| [`aliyun-fullstack-deploy`](skills/aliyun-fullstack-deploy/) | Engineering | Canary-first deployment with proof and rollback |
| [`small-server-fit`](skills/small-server-fit/) | Engineering | Know whether the app fits before buying or deploying |
| [`deployment-proof`](skills/deployment-proof/) | Build in Public | Turn invisible deployment work into credible public evidence |
| [`trend-to-microbet`](skills/trend-to-microbet/) | AI Native Bets | See a trend. Place a small bet. Demand evidence. |
| [`vibe-to-spec`](skills/vibe-to-spec/) | Voice Native | Voice chaos to coding-agent contract |
| [`skill-from-scars`](skills/skill-from-scars/) | AI Native Bets | Turn repeated pain into reusable Agent Skills |
| [`build-in-public-launcher`](skills/build-in-public-launcher/) | AI Native Bets | Launch for evidence, not applause |
| [`personal-boardroom`](skills/personal-boardroom/) | Judgment & Translation | One decision, several explicit lenses, one ranked answer |
| [`anti-slop-personal-brand`](skills/anti-slop-personal-brand/) | AI Native Bets | Make the first screen current, real and earned |
| [`deep-talk-to-podcast`](skills/deep-talk-to-podcast/) | Creator & Writing | Turn a meaningful deep talk into a privacy-aware AI podcast |
| [`one-week-founder-mode`](skills/one-week-founder-mode/) | AI Native Bets | One main bet, two microbets, a kill list |

## Two voice-native Skills that work together

`voice-dump-to-todo` and `vibe-to-spec` deliberately share a context-aware ASR repair method, but have different destinations:

- **voice-dump-to-todo** → “What should I do?” → actions, decisions, dependencies, due dates, interactive HTML.
- **vibe-to-spec** → “What should the software do?” → scope, user flow, data/state, constraints, acceptance criteria, implementation order.

Both can use recurring named entities from the active conversation/project context to repair obvious ASR errors. They auto-normalize only high-confidence corrections; ambiguous names remain visible instead of being guessed.

## Install one Skill from the monorepo

GitHub CLI 2.90+ supports browsing and installing a specific Agent Skill from a repository:

GitHub CLI:

```bash
gh skill preview FAIRY123456789/human-edge-agent-skills vibe-to-spec
gh skill install FAIRY123456789/human-edge-agent-skills vibe-to-spec --agent claude-code --scope user
```

Skills CLI / skills.sh ecosystem:

```bash
npx skills add https://github.com/FAIRY123456789/human-edge-agent-skills --skill vibe-to-spec
```

For another compatible host, use the host supported by your current CLI or copy the individual skill directory into that agent's skills location.

## The deployment arc: fit → ship → prove

The original lightweight `safe-shared-vps-deploy` concept has been deduplicated into the stronger [`aliyun-fullstack-deploy`](skills/aliyun-fullstack-deploy/) workflow. It retains the shared-server protection rules and adds release packaging, canary testing, atomic promotion, deeper verification, and rollback tooling.

- [`small-server-fit`](skills/small-server-fit/) asks whether the app and runtime fit a low-cost server before purchase or deployment.
- [`aliyun-fullstack-deploy`](skills/aliyun-fullstack-deploy/) ships to an authorized Alibaba Cloud ECS or comparable Linux VPS through evidence gates.
- [`deployment-proof`](skills/deployment-proof/) turns the redacted result into an honest public case study and career evidence.

## Why one repository instead of 18 repositories?

The public entry point stays simple: one GitHub link on a resume or personal website, one star/watch/fork surface, one release history, and one place for issues. Individual Skills still have their own folder, `SKILL.md`, human-facing README, keywords, deep link, and can be installed individually from the same repository.

The repository includes a release strategy in [`docs/MONOREPO_AND_DISCOVERY.md`](docs/MONOREPO_AND_DISCOVERY.md). The recommended rule is: **start as a monorepo; spin out only a Skill that independently earns enough users or contributors to justify its own lifecycle.**

## Current AI-podcast route

`deep-talk-to-podcast` includes a dated platform selector for source-grounded Audio Overviews, editable AI podcast production, and high-quality generated voices. Because product names and features change quickly, the Skill tells an online agent to verify current official pages before recommending a service.

## Validation

```bash
pip install pyyaml
python scripts/validate_skills.py
```

Seed behavior evals live in [`evals/cases.json`](evals/cases.json).

## Privacy and honesty

- no private project names, personal chat logs, contact information, credentials, or company-confidential data;
- no fake metrics, users, testimonials, stars, installs, or adoption;
- no silent low-confidence named-entity correction;
- no fabricated familiarity in social communication;
- no medical diagnosis in fitness/recovery guidance;
- no destructive production action without normal tool permissions and explicit intent.

## License

MIT.
