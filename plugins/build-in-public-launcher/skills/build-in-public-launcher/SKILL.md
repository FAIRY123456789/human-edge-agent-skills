---
name: build-in-public-launcher
description: "Turn a finished or nearly finished Skill, plugin, repository, micro-tool, research utility, or AI project into a credible public launch that can earn real users and feedback. Use when the work exists but nobody outside the creator has tried it, the README is weak, the launch has no demo or proof metric, or the user wants a GitHub-first build-in-public plan without fake traction or vanity metrics."
license: MIT
metadata:
  author: Joy T <101039451+FAIRY123456789@users.noreply.github.com>
  tags:
    - product-launch
    - open-source
    - validation
---

# Build in Public Launcher

## Purpose

Launch for evidence, not applause. This Skill turns a finished artifact into a bounded release and feedback loop without inventing adoption.

## Instructions

1. Define the exact user and painful moment the artifact addresses.
2. Audit whether the artifact is actually ready for a stranger: installation, first-run path, example input, example output, license, privacy and security notes, and failure handling.
3. Write a one-line value proposition that names the job, not the technology stack.
4. Build a launch pack using `references/launch-pack.md`.
5. Create one comparison or task-completion demo. Do not cherry-pick an impossible-to-reproduce showcase.
6. Choose one primary proof metric and one secondary distribution metric.
7. Recruit the first testers from existing communities, peers, contributors, or target-user groups. Prefer 10 relevant people over 1,000 generic impressions.
8. Ask testers to perform a task before explaining the solution. Capture confusion and failure.
9. Publish a changelog entry after each evidence-driven revision.
10. Promote measured adoption only after it exists. Never invent stars, users, installs, revenue, benchmarks, or testimonials.

## Default launch horizon

Use a 7-day launch loop:

- Day 1: packaging and smoke test
- Day 2: private testers
- Day 3–4: fix onboarding and failure cases
- Day 5: public release
- Day 6–7: collect issues, repeat use, and outcome evidence

## Output

Return a release-ready checklist, README hero copy, demo plan, tester plan, proof metrics, and 7-day launch schedule.

## Examples

- Input: a working repository with no external users and a confusing README.
- Output: a reproducible demo, a first-tester plan, one utility metric, and explicit stop or iterate criteria.

## Limitations

Do not claim market demand, compatibility, or traction that has not been observed. Publishing, messaging testers, and changing external accounts require the user's explicit authorization.

## Troubleshooting

If no credible metric exists, choose successful task completion or tester confusion as the first measurement. If strangers cannot install the artifact, return to packaging before writing launch copy.
