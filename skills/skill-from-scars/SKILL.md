---
name: skill-from-scars
description: "Mine repeated pain from transcripts, project retrospectives, debugging logs, failed prompts, deployment notes, or work history and decide whether it deserves to become a reusable Agent Skill. Use when the user wants to turn hard-earned experience into open-source knowledge, avoid publishing generic prompts, generate a SKILL.md package with references/evals, or identify which repeated mistakes contain a real decision procedure worth sharing."
---

# Skill From Scars

Do not turn every lesson into a Skill. Turn repeated, generalizable pain into a tested workflow.

## Workflow

1. Collect the raw scar: failed runs, repeated corrections, incident notes, long conversations, or a recurring manual procedure.
2. Extract candidate pains. Merge variants that share the same underlying failure.
3. Score each candidate with `references/skill-worthiness.md`.
4. Reject candidates that are:
   - one-off personal preferences with no external user;
   - generic advice the base model already handles well;
   - private procedures that cannot be safely generalized;
   - impossible to evaluate;
   - mostly branding with no behavior change.
5. For the strongest candidate, define:
   - trigger;
   - painful failure mode;
   - decision procedure;
   - hard gates;
   - required references/scripts;
   - expected output;
   - evaluation case.
6. Draft a compact `SKILL.md`. Put long taxonomies and templates in `references/` or `assets/`.
7. Create at least one baseline-vs-skill eval where a normal model is likely to fail.
8. Run privacy and secret checks before public packaging.
9. Use `scripts/scaffold_skill.py` when a local file tree is requested.
10. End with the next real-world test required before calling the Skill mature.

## Output

- candidate list and scores;
- selected Skill concept;
- rejected concepts and why;
- complete Skill package plan;
- seed eval;
- external proof plan.
