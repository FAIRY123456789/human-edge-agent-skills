# Seed Evaluation Set

These are behavior checks, not claims of universal performance improvement.

For each case:

1. Run the prompt without the Skill.
2. Run the same prompt with the Skill available.
3. Score each expected behavior 0 / 1 / 2.
4. Record regressions as well as improvements.

Suggested dimensions: factual restraint, decision quality, context repair, output usability, privacy/safety, and unnecessary complexity.

`marketplace-plugin-cases.json` is the cross-runtime routing set for the four packaged plugins. It contains prompts and pass criteria, not benchmark results. For each runtime, use a clean session with only the named plugin installed and record evidence outside the fixture. The first two OpenAI candidates each have five positive and three negative cases.

CSDN paired regression: see `csdn/README.md` for four technical cases, anchored scoring, raw-output retention and offline execution. CI validates the harness only; it does not assert writing quality.
