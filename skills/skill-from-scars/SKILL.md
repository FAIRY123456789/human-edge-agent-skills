---
name: skill-from-scars
description: "Mine repeated pain from transcripts, project retrospectives, debugging logs, failed prompts, deployment notes, or work history and decide whether it deserves to become a reusable Agent Skill. Use when the user wants to turn hard-earned experience into open-source knowledge, avoid publishing generic prompts, generate a SKILL.md package with references and evaluations, or identify which repeated mistakes contain a real decision procedure worth sharing."
license: MIT
metadata:
  author: Joy T <101039451+FAIRY123456789@users.noreply.github.com>
  tags:
    - agent-skills
    - retrospectives
    - knowledge-capture
---

# Skill From Scars

## Purpose

Do not turn every lesson into a Skill. Turn repeated, generalizable pain into a tested workflow whose value can be demonstrated against a baseline.

## Instructions

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
   - required references and scripts;
   - expected output;
   - evaluation case.
6. Draft a compact main instruction file. Put long taxonomies and templates in supporting reference or asset files.
7. Create at least one baseline-versus-Skill evaluation where a normal model is likely to fail.
8. Run privacy and secret checks before public packaging.
9. Use `scripts/scaffold_skill.py` when a local file tree is requested.
10. End with the next real-world test required before calling the Skill mature.

## Requirements

The optional scaffolder requires Python 3 and a local JSON design record. It uses only the Python standard library and does not require an API key.

## Available Scripts

| Script | Purpose | Arguments |
|---|---|---|
| `scripts/scaffold_skill.py` | Create a minimal local Skill tree from an approved design record | `source.json [output-directory]` |

## Output

- candidate list and scores;
- selected Skill concept;
- rejected concepts and why;
- complete Skill package plan;
- seed eval;
- external proof plan.

## Examples

- Input: three deployment retrospectives show repeated failures around environment checks and rollback proof.
- Output: one narrowly scoped Skill candidate, rejected alternatives, a compact package plan, and an evaluation that tests the recovered decision procedure.

After reviewing the design record, scaffold it locally with:

```bash
python scripts/scaffold_skill.py source.json <output-directory>
```

## Limitations

A vivid story is not enough evidence of a reusable Skill. Do not publish private procedures, secrets, one-off preferences, or an untested prompt as mature guidance.

## Troubleshooting

If every candidate looks generic, return to the raw incidents and identify the decision that changed the outcome. If no baseline can expose the failure, keep the lesson as documentation instead of packaging it as a Skill.
