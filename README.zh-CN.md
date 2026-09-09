# Human Edge Agent Skills

> **把通用 AI 最容易做平、做假或做错的部分，变成可复用工作流：混乱语音、人情分寸、模糊判断、小步实验与安全上线。**

简体中文 · [English](README.md)

这套 Skill 的重点不是让 AI “更会说”，而是把人在现实工作中仍然稀缺的部分固化下来：判断关系、从上下文修复语音识别错误、把模糊想法变成可执行规格、判断一个热点值不值得追、把踩坑变成知识成果、保护个人文字的温度，并且让项目最终接受真实世界验证。

## 先从四个旗舰 Skill 开始

| Skill | 最适合的真实时刻 |
|---|---|
| [`vibe-to-spec`](skills/vibe-to-spec/) | 你能把产品想法讲出来，但 Coding Agent 仍需要明确的实现合同。 |
| [`trend-to-microbet`](skills/trend-to-microbet/) | 新热点让人焦虑，但你更需要一个 48 小时到 7 天的小实验。 |
| [`social-signal-and-tact`](skills/social-signal-and-tact/) | 信息本身没错，但表达太僵、太正式，或者让对方不容易回复。 |
| [`skill-from-scars`](skills/skill-from-scars/) | 同一种失败反复发生，已经值得沉淀成一个可测试的 Skill。 |

每个 Skill 只承担一个清楚的工作，拥有独立触发描述、README、深链接和安装入口。其余内容是完整目录，而不是 18 个同样响亮的宣传口号。

## 18 个 Skill

| Skill | 类别 | 解决的问题 |
|---|---|---|
| [`social-signal-and-tact`](skills/social-signal-and-tact/) | 社交与沟通 | 为向上沟通补足人情分寸 |
| [`csdn-technical-writing`](skills/csdn-technical-writing/) | 创作与写作 | 写出连贯的中文技术长文，避免 AI 式碎片短段 |
| [`student-money-four-buckets`](skills/student-money-four-buckets/) | 青年生活 | 用四层预算兼顾学生生活的必要开支、成长和乐趣 |
| [`voice-dump-to-todo`](skills/voice-dump-to-todo/) | 语音原生 | 把混乱口述整理成可执行的待办事项 |
| [`fitness-recovery-coach`](skills/fitness-recovery-coach/) | 青年生活 | 制定尊重恢复状态、而不是强行服从日历的训练计划 |
| [`cross-domain-translator`](skills/cross-domain-translator/) | 判断与转译 | 跨领域迁移问题结构，而不只是替换术语 |
| [`voice-with-temperature`](skills/voice-with-temperature/) | 创作与写作 | 让文字更清楚，同时保留真实的人味和情绪温度 |
| [`aliyun-fullstack-deploy`](skills/aliyun-fullstack-deploy/) | 工程 | 先金丝雀验证，再原子发布与回滚 |
| [`small-server-fit`](skills/small-server-fit/) | 工程 | 购买或部署前判断项目是否真正适配小服务器 |
| [`deployment-proof`](skills/deployment-proof/) | 公开构建 | 把看不见的部署工作变成可信的公开证据 |
| [`trend-to-microbet`](skills/trend-to-microbet/) | AI 原生实验 | 发现趋势，小步下注，用证据决定是否继续 |
| [`vibe-to-spec`](skills/vibe-to-spec/) | 语音原生 | 把混乱口述转成 Coding Agent 可执行的实现合同 |
| [`skill-from-scars`](skills/skill-from-scars/) | AI 原生实验 | 把反复踩过的坑沉淀成可复用的 Agent Skill |
| [`build-in-public-launcher`](skills/build-in-public-launcher/) | AI 原生实验 | 为获得真实证据而发布，而不是只追求掌声 |
| [`personal-boardroom`](skills/personal-boardroom/) | 判断与转译 | 用多个明确视角审视同一决策，给出排序后的答案 |
| [`anti-slop-personal-brand`](skills/anti-slop-personal-brand/) | AI 原生实验 | 让个人品牌首屏呈现当下、真实且有依据的价值 |
| [`deep-talk-to-podcast`](skills/deep-talk-to-podcast/) | 创作与写作 | 把有意义的深度对话转成重视隐私的 AI 播客 |
| [`one-week-founder-mode`](skills/one-week-founder-mode/) | AI 原生实验 | 一项主实验、两项微实验，再配一份停止事项清单 |

## 语音原生：两个 Skill 联动但职责不同

`voice-dump-to-todo` 负责把混乱语音变成“我要做什么”；`vibe-to-spec` 负责把混乱语音变成“这个软件应该怎么做”。

两者都会优先读取当前上下文中高频、地位明显的专有名词。当 ASR 把一个已经明确出现过的名字识别成同音词，而且替换后语义明显更连贯时，可以自动规范化。中等置信度会留下假设，低置信度不会猜。

## 部署闭环：适配 → 上线 → 证明

早期的 `safe-shared-vps-deploy` 与更完整的部署 Skill 近重复，因此本仓库只保留更强的 [`aliyun-fullstack-deploy`](skills/aliyun-fullstack-deploy/)：继承“保护服务器上已有站点”的原则，并加入脱敏打包、金丝雀、原子切换、真实流程验收和回滚脚本。

- [`small-server-fit`](skills/small-server-fit/)：在购买服务器或开始部署前，评估运行时与资源是否匹配。
- [`aliyun-fullstack-deploy`](skills/aliyun-fullstack-deploy/)：面向已授权阿里云 ECS 或类似 Linux VPS，按证据门槛完成上线。
- [`deployment-proof`](skills/deployment-proof/)：把脱敏后的上线证据整理成 GitHub 案例、简历表达和面试故事。

## 单仓库策略

建议所有 Skill 先放在一个仓库 `human-edge-agent-skills`。这样简历、个人网站和社交分享只有一个入口。每个 Skill 仍然有独立目录、独立 `SKILL.md`、独立 README 和深链接，也可以从同一仓库单独安装。

只有当某一个 Skill 已经独立获得明显安装量、Issue、PR、复用或社区传播后，再考虑拆成独立仓库。

## 建议第一批重点测试

1. `vibe-to-spec`
2. `trend-to-microbet`
3. `social-signal-and-tact`
4. `skill-from-scars`

第一批不要用“18 个 Skill”作为主要宣传语。更好的传播方式是选择一个真实痛点，用前后对比证明某一个 Skill 确实改变了结果。

## 校验

```bash
pip install pyyaml
python scripts/validate_skills.py
```

## 许可证

MIT.
