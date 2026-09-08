---
name: cross-domain-translator
description: "Translate a problem, workflow, or project from one professional domain into another while preserving the real structure. Use when someone needs to connect domain expertise with software, AI, product, research, data, policy, operations, or another field. Rebuild actors, objects, states, events, constraints, evidence, metrics, and failure modes instead of merely replacing vocabulary."
license: MIT
metadata:
  author: Joy T <101039451+FAIRY123456789@users.noreply.github.com>
  tags:
    - systems-thinking
    - domain-modeling
    - translation
---

# Cross-Domain Translator

Translate the structure of the problem, not the nouns.

## Workflow

1. Describe the source-domain problem in ordinary language.
2. Extract its structural model using `references/domain-map.md`:
   - actors;
   - objects and data;
   - states;
   - events and actions;
   - decisions;
   - constraints;
   - evidence;
   - success metrics;
   - failure modes.
3. Identify which parts are domain-specific and which are generic information-processing problems.
4. Map generic parts into the target domain.
5. Mark every analogy that could break because of regulation, physical constraints, human incentives, data quality, or different causal mechanisms.
6. Propose the smallest useful bridge: data model, API, workflow, Agent, experiment, prototype, taxonomy, or research question.
7. State what new domain knowledge must be learned before implementation.
8. If the translation is for a resume or interview, explain the transferable structure without pretending the domains are identical.

## Output

Return:

- source-domain problem;
- structural map;
- target-domain translation;
- valid transfer points;
- invalid or risky analogies;
- smallest bridge artifact;
- missing knowledge.

A good translation lets a domain expert recognize their problem and a technical expert see something they can build.
