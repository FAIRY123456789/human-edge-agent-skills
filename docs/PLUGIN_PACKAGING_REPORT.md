# Plugin Packaging Report

日期：2026-09-08（Asia/Shanghai）

状态：**静态封装与发布政策预检完成；Cursor 运行时尚未测试；未向任何 Marketplace 发布或提交。**

## 结论

仓库继续保留 18 个 canonical Skills；其中 5 个低风险、高辨识度候选被复制进 4 个可独立分发的插件。canonical 来源固定为 `skills/`，`packaging/plugin-sources.json` 记录评测基线和映射，脚本负责单向同步与内容哈希检查。

本次封装基于已完成 NVIDIA Tier 1 的提交：

`449ec5c3d1978accb6e683805757e846d3378fe2`

该基线的最终结果为 18/18 PASS、平均 Quality 87.7、4 个 Quality >= 90、0 incomplete、0 CRITICAL、0 HIGH。没有执行 Tier 2、Tier 3、`--llm`、`--llm-verify` 或付费 LLM API。

## Plugin composition

| Plugin | Packaged canonical Skills | Rationale |
|---|---|---|
| `voice-to-work` | `voice-dump-to-todo`, `vibe-to-spec` | 两者共享上下文感知的 ASR 修复方式，但分别输出行动清单与实现规格，组合用途明确。 |
| `skill-from-scars` | `skill-from-scars` | 把重复失败转成可评测 Skill；用途单一、无默认外部写入。 |
| `build-in-public-launcher` | `build-in-public-launcher` | 证据优先的发布准备，明确拒绝虚构采用量和指标。 |
| `voice-with-temperature` | `voice-with-temperature` | 指写作语气与情感温度，不是语音、朗读或音频工具。 |

## Repository structure

```text
.
├── .claude-plugin/marketplace.json
├── .cursor-plugin/marketplace.json
├── packaging/plugin-sources.json
├── schemas/agent-plugin-1.0.0.schema.json
├── scripts/
│   ├── sync_plugin_packages.py
│   └── validate_plugin_packages.py
├── skills/                         # canonical source, all 18 retained
└── plugins/
    ├── voice-to-work/
    ├── skill-from-scars/
    ├── build-in-public-launcher/
    └── voice-with-temperature/
        ├── plugin.json             # Agent Plugins 1.0 manifest
        ├── .claude-plugin/plugin.json
        ├── skills/...              # complete copied Skill folder(s)
        ├── assets/human-edge.svg
        ├── README.md
        ├── PRIVACY.md
        └── LICENSE
```

每个插件都是自包含目录。没有符号链接，也没有依赖仓库外部的 Skill 文件；每份 `references/`、`scripts/` 与 Skill 自带资源均随副本复制。插件没有加入 hooks、agents、commands、MCP servers、rules 或平台特定行为。

每个插件还提供从 README 可直接访问的 `PRIVACY.md`，明确说明发布者不运营数据服务、不收集遥测或用户内容，并按插件实际能力披露本地脚本、网络行为和权限边界。

## Manifest strategy

同一个插件根目录同时放置两份元数据：

- 根 `plugin.json` 严格按 [Agent Plugins 1.0 specification](https://agent-plugins.org/specification) 与官方 1.0.0 schema 校验。Cursor 官方文档说明其插件遵循 Agent Plugins 标准，因此没有制造额外的 Cursor 专属插件 manifest。
- `.claude-plugin/plugin.json` 按 [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference) 与 SchemaStore 当前 Claude manifest schema 校验。Claude 的组件仍在插件根目录自动发现，未在 manifest 中重复声明路径。
- 根 `.claude-plugin/marketplace.json` 是该 monorepo 的 Claude marketplace 索引；根 `.cursor-plugin/marketplace.json` 是 Cursor monorepo 索引。两者都只引用真实的 `plugins/` 路径。

这种双 manifest 不是两套实现：Skills 内容只有一套包内副本，两个宿主只读取各自需要的元数据。

## Source-to-package integrity

映射文件：`packaging/plugin-sources.json`

| Plugin / Skill | Canonical-to-package SHA-256 | Result |
|---|---|---|
| `voice-to-work/voice-dump-to-todo` | `463d02214a93f657adc7d8b18c4d4be6ecd93a3990a68c440f96700d7e0fcdd4` | SYNCED |
| `voice-to-work/vibe-to-spec` | `42e903f21dfe3238b822f4efa48caec4162b00e3987c51302822c070b9f1f131` | SYNCED |
| `skill-from-scars/skill-from-scars` | `f19aa3eca2301e71ca4edb0eae01dacc04163efa38c0eda28471e7958634bf4b` | SYNCED |
| `build-in-public-launcher/build-in-public-launcher` | `8f2e8ba0e24a5094ea0f7f3f33839ccc081f799d2df04641adbd854d9e08732c` | SYNCED |
| `voice-with-temperature/voice-with-temperature` | `551b27157b22922fe459defc038b1e68146ef9755e1c077c6342f9d8e704b724` | SYNCED |

`python scripts/sync_plugin_packages.py --write` 只从 canonical 目录写向包内副本；`--check` 不修改文件，并在新增、删除或内容变化时失败。

## Validation matrix

| Check | Scope | Result |
|---|---|---|
| Canonical repository validator | 18 Skills | PASS 18/18 |
| NVIDIA SkillEvaluator complete Tier 1 | 最新 18 份完整 JSON | PASS 18/18; avg 87.7; 0 incomplete/CRITICAL/HIGH |
| Agent Plugins 1.0 JSON Schema | 4 root manifests | PASS 4/4 |
| Claude plugin live schema snapshot | 4 Claude manifests | PASS 4/4 |
| Claude marketplace live schema snapshot | root marketplace | PASS |
| Marketplace JSON and referenced paths | Claude + Cursor indexes | PASS 2/2 |
| Self-contained package check | 4 plugin directories | PASS 4/4 |
| Canonical/package drift check | 5 copied Skills | PASS 5/5 |
| Gitleaks secrets scan | complete `plugins/` tree | PASS; no leaks found |
| Python AST syntax | repository Python files, excluding ignored temporary tools | PASS 17/17 |
| Bash syntax | canonical and packaged shell files | PASS 6/6 |
| JSON parsing | tracked/worktree JSON, excluding ignored temporary tools | PASS 139/139 |
| Deterministic helper smoke tests | voice HTML, writing lint, scaffold, server fit, public audit, release inspection and AI contract | PASS; hidden environment file rejection covered |
| Git whitespace checks | working and committed diffs | PASS |
| Claude Code runtime install/discovery | CLI/app not installed on this host | **NOT TESTED** |
| Cursor runtime install/discovery | CLI/app not installed on this host | **NOT TESTED** |

Schema snapshots downloaded for validation remain under ignored `.tmp/` and are not shipped. The checked-in Agent Plugins schema is an exact local validation dependency; official URLs remain the authority.

## Requested model versus current official behavior

| Initial packaging assumption | Current official documentation | Implemented result |
|---|---|---|
| One portable plugin manifest may be enough | Agent Plugins defines root `plugin.json`; Claude documents `.claude-plugin/plugin.json` | Both metadata files coexist over one shared plugin root |
| Cursor might need a per-plugin proprietary manifest | [Cursor plugins](https://prod.cursor.com/docs/plugins) natively support Agent Plugins and discover root skills | Root Agent Plugins manifest only; no invented Cursor-only component |
| A repository can call its Claude marketplace `claude-community` | [Claude marketplace docs](https://code.claude.com/docs/en/plugin-marketplaces) reserve marketplace names; the [community repository](https://github.com/anthropics/claude-plugins-community) is read-only and directs submissions to an official form | Repository marketplace is honestly named `human-edge-skills`; community submission exists only as a draft |
| Local runtime testing is always available | Claude and Cursor require their installed hosts for install/discovery verification | Static/package validation passed; runtime rows are explicitly `NOT TESTED` |

## Remaining gates

- Install a current Claude Code host and verify repository marketplace add, local-scope install, Skill discovery, and uninstall.
- Install a current Cursor host, copy each complete plugin to its documented local plugin directory, reload, and confirm Skill discovery under Customize.
- Re-run official validators immediately before submission because schemas and directory policies can change.
- Perform human prompt-level checks for trigger clarity and output usefulness. Tier 1 static passing is not a claim of marketplace acceptance or real-world adoption.

The repository is at the **official Plugin packaging stage**, but not yet at the **submission-ready runtime verification gate**. Cursor 的精确状态为 **BLOCKED ONLY BY CURSOR RUNTIME TEST**。No Marketplace action was taken.

Cursor 的人工测试步骤与最终可复制字段分别记录在 [`CURSOR_RUNTIME_TEST_GUIDE.md`](CURSOR_RUNTIME_TEST_GUIDE.md) 和 [`CURSOR_MARKETPLACE_SUBMISSION_FINAL.md`](CURSOR_MARKETPLACE_SUBMISSION_FINAL.md)。

## Official references

- [Agent Plugins specification](https://agent-plugins.org/specification)
- [Agent Plugins 1.0.0 schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Anthropic community plugins repository](https://github.com/anthropics/claude-plugins-community)
- [Cursor plugins](https://prod.cursor.com/docs/plugins)
- [Cursor plugin reference](https://prod.cursor.com/docs/reference/plugins)
- [NVIDIA Tier 1 validation](https://docs.nvidia.com/skills/skillevaluator/tier1-validation)
