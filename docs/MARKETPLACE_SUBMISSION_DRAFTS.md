# Marketplace Submission Drafts

日期：2026-09-08（Asia/Shanghai）

**仅为提交草稿。没有填写、发送或发布到 Claude、Cursor 或任何第三方 Marketplace。** 所有采用量、用户数、评分、兼容性和 benchmark 字段均刻意留空，因为当前没有可验证数据。

Repository: `https://github.com/FAIRY123456789/human-edge-agent-skills`

License: MIT

Author: Joy T

## Shared factual evidence

- canonical Skills：18；本轮封装 5 个 Skills / 4 个插件。
- NVIDIA SkillEvaluator 完整 Tier 1：18/18 PASS，0 incomplete、0 CRITICAL、0 HIGH。
- 四个插件均通过 Agent Plugins 1.0 schema、自包含、真实路径和 canonical/package 哈希一致性检查。
- Claude manifest 与 repository marketplace 已通过当前 schema 快照。
- Claude Code 与 Cursor 未安装在本机；实际安装、发现与交互测试为 `NOT TESTED`。
- 插件不包含 MCP servers、hooks、agents、commands、rules 或自动外部写入。

## Plugin listing drafts

### Voice to Work

- Package name: `voice-to-work`
- Path: `plugins/voice-to-work`
- Category: Productivity
- Skills: `voice-dump-to-todo`, `vibe-to-spec`
- Short description: Turn noisy spoken task and product dumps into executable todos or implementation-ready specifications.
- Keywords: `voice-input`, `productivity`, `specifications`, `asr`, `task-management`
- Suggested prompt: “Here is a rough voice transcript about what I need to build. Repair only high-confidence ASR mistakes, show uncertain names, and turn it into an implementation spec.”
- Safety note: Does not silently guess uncertain names and does not write to an external task manager by default.

### Skill From Scars

- Package name: `skill-from-scars`
- Path: `plugins/skill-from-scars`
- Category: Developer Tools
- Skills: `skill-from-scars`
- Short description: Decide whether repeated pain deserves a reusable Agent Skill, then shape it into a testable package.
- Keywords: `agent-skills`, `retrospectives`, `knowledge-capture`, `skill-authoring`, `evaluation`
- Suggested prompt: “This failure has happened three times. Help me decide whether it deserves a Skill, extract the invariant workflow, and define tests without inventing usage claims.”
- Safety note: Treats scaffolding as optional and does not publish or install generated work automatically.

### Build in Public Launcher

- Package name: `build-in-public-launcher`
- Path: `plugins/build-in-public-launcher`
- Category: Productivity
- Skills: `build-in-public-launcher`
- Short description: Turn a finished project into an evidence-first public launch without invented traction or vanity metrics.
- Keywords: `product-launch`, `open-source`, `validation`, `build-in-public`, `evidence`
- Suggested prompt: “Turn this finished project into a launch pack using only evidence I can verify. Mark missing proof explicitly and do not publish anything.”
- Safety note: Rejects fabricated users, installs, testimonials and metrics; publishing always remains a separate explicit action.

### Voice With Temperature

- Package name: `voice-with-temperature`
- Path: `plugins/voice-with-temperature`
- Category: Productivity / Writing
- Skills: `voice-with-temperature`
- Short description: Edit prose for clarity while preserving the writer's lived detail, uncertainty, rhythm, and emotional temperature.
- Keywords: `writing`, `editing`, `voice`, `prose`, `human-voice`
- Suggested prompt: “Edit this draft for clarity, but preserve its awkward honesty, concrete details, uncertainty, and sentence rhythm. Explain any change that alters emotional temperature.”
- Safety note: “Voice” means writing voice, not speech synthesis, cloning, transcription, or audio generation.

## Claude Community Plugins draft

Official route verified on 2026-09-08: the public [Claude community plugins repository](https://github.com/anthropics/claude-plugins-community) is a read-only mirror and points publishers to the [official submission form](https://clau.de/plugin-directory-submission). Do not open a pull request against the mirror.

Suggested first batch: `voice-to-work`, `skill-from-scars`, `build-in-public-launcher`, `voice-with-temperature`.

Draft submission statement:

> Human Edge Skills is an MIT-licensed collection by Joy T. This submission contains four focused plugins built from five canonical Agent Skills. They convert noisy human context into tasks or specifications, extract reusable workflows from repeated failures, prepare evidence-first launches, and preserve human writing voice during editing. NVIDIA SkillEvaluator Tier 1 passed for all 18 canonical Skills with no incomplete, CRITICAL, or HIGH findings. The packages add no MCP servers, hooks, commands, agents, or automatic publishing. Claude Code runtime installation and discovery still require verification on a host with Claude Code installed; no compatibility, adoption, or marketplace-acceptance claim is made.

Before sending the form:

- run the current official Claude validation command rather than copying a possibly stale command from this file;
- test local-scope install, discovery, representative prompts, update, and uninstall;
- choose one plugin per form entry if the form requires individual listings;
- attach only the real repository, plugin path, MIT license and included human-created SVG;
- do not claim inclusion in `claude-community` until Anthropic confirms it.

## Cursor Marketplace draft

Official route verified on 2026-09-08: review the current [Cursor plugins documentation](https://prod.cursor.com/docs/plugins) and start a publisher submission at [Cursor Marketplace publish](https://cursor.com/marketplace/publish) only after local testing.

Draft publisher statement:

> These four MIT-licensed plugins follow the Agent Plugins 1.0 structure and package five self-contained Agent Skills. They include no MCP servers, rules, hooks, commands, agents, platform logos, or automatic external mutations. All canonical Skills passed NVIDIA SkillEvaluator Tier 1. Static schema, path and drift validation passed; Cursor runtime discovery is not yet tested because Cursor is not installed on the validation host.

Before publishing:

- copy each complete plugin directory into the current Cursor-documented local plugin location;
- reload Cursor and verify the expected Skills appear under Customize;
- run representative prompts and confirm no unrelated Skill triggers;
- confirm the marketplace category and image requirements in the live publisher UI;
- submit each plugin as its own focused listing unless Cursor's live form explicitly supports the repository index;
- do not claim approval, installs, active users or ratings before those facts exist.

## Deliberately excluded from this submission batch

- All B-class Community / Experimental Skills stay GitHub-first.
- All C-class Hold / Rewrite Skills stay out of official-directory drafts.
- `social-signal-and-tact`, `student-money-four-buckets`, and `fitness-recovery-coach` are not included merely for novelty: the first involves interpersonal influence, the second personal finance, and the third health/recovery risk.
- `aliyun-fullstack-deploy` is excluded because it can change production infrastructure.

The full A/B/C reasoning remains in `docs/OFFICIAL_PLUGIN_CANDIDATES.md`.
