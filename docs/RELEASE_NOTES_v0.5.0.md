# Human Edge Agent Skills v0.5.0 — Cursor-Validated Marketplace Candidate

This release advances the repository from static cross-runtime packaging to a real Cursor discovery record while keeping every untested boundary explicit.

## Verified in this release

- NVIDIA SkillEvaluator Tier 1 retained result: 18/18 canonical Skills PASS, 0 incomplete, 0 CRITICAL, 0 HIGH.
- Codex CLI 0.153.4 retained runtime result: 4/4 plugins and 5/5 packaged Skills PASS.
- Cursor 3.19.13: four complete local plugin copies matched repository hashes; Cursor loaded 4/4 plugins with zero failures; its machine-readable Customize state contained all 5 packaged Skills.
- Repository regressions: canonical validation, Agent Plugins and Claude metadata checks, marketplace paths, package self-containment, canonical drift, secrets, syntax, JSON, Markdown links, deterministic OpenAI archives, and smoke tests PASS.

## Honest boundaries

- Cursor's five representative prompt-level behavior checks remain USER VISUAL CHECK REQUIRED. Discovery PASS is not presented as behavior PASS.
- Claude Code CLI validation, discovery, and behavior are NOT TESTED. Claude Desktop is not substituted for Claude Code evidence.
- Cursor retains a non-fatal warning that the Claude manifest declares an unrecognized `$schema`; all four plugins still loaded with zero failures. The Claude schema marker was not removed merely to suppress a different host's warning.
- NVIDIA Tier 1 was not rerun because canonical Skill content did not change.
- No Claude or Cursor Marketplace submission, review, acceptance, or compatibility result is claimed by this release.

## Submission materials

- Copy-ready Claude and Cursor fields: `docs/PLUGIN_SUBMISSION_README.md`
- OpenAI Skills-only candidates: `submission-assets/openai/voice-to-work-1.0.0.zip` and `submission-assets/openai/skill-from-scars-1.0.0.zip`
- Detailed evidence: `docs/CROSS_RUNTIME_MARKETPLACE_STATUS.md`
