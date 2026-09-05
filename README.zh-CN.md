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
| [`social-signal-and-tact`](skills/social-signal-and-tact/) | Social & Communication | Human tact for upward communication |
| [`csdn-technical-writing`](skills/csdn-technical-writing/) | Creator & Writing | Long-form Chinese technical writing without AI micro-paragraphs |
| [`student-money-four-buckets`](skills/student-money-four-buckets/) | Young Life | A four-layer student budget that still leaves room for fun |
| [`voice-dump-to-todo`](skills/voice-dump-to-todo/) | Voice Native | Messy speech in, executable to-do out |
| [`fitness-recovery-coach`](skills/fitness-recovery-coach/) | Young Life | Training plans that respect recovery instead of forcing the calendar |
| [`cross-domain-translator`](skills/cross-domain-translator/) | Judgment & Translation | Translate problem structure across domains, not just terminology |
| [`voice-with-temperature`](skills/voice-with-temperature/) | Creator & Writing | Make writing clearer without washing the human out of it |
| [`aliyun-fullstack-deploy`](skills/aliyun-fullstack-deploy/) | Engineering | 先金丝雀验证，再原子发布与回滚 |
| [`small-server-fit`](skills/small-server-fit/) | Engineering | 购买或部署前判断项目是否真正适配小服务器 |
| [`deployment-proof`](skills/deployment-proof/) | Build in Public | 把看不见的部署工作变成可信的公开证据 |
| [`trend-to-microbet`](skills/trend-to-microbet/) | AI Native Bets | See a trend. Place a small bet. Demand evidence. |
| [`vibe-to-spec`](skills/vibe-to-spec/) | Voice Native | Voice chaos to coding-agent contract |
| [`skill-from-scars`](skills/skill-from-scars/) | AI Native Bets | Turn repeated pain into reusable Agent Skills |
| [`build-in-public-launcher`](skills/build-in-public-launcher/) | AI Native Bets | Launch for evidence, not applause |
| [`personal-boardroom`](skills/personal-boardroom/) | Judgment & Translation | One decision, several explicit lenses, one ranked answer |
| [`anti-slop-personal-brand`](skills/anti-slop-personal-brand/) | AI Native Bets | Make the first screen current, real and earned |
| [`deep-talk-to-podcast`](skills/deep-talk-to-podcast/) | Creator & Writing | Turn a meaningful deep talk into a privacy-aware AI podcast |
| [`one-week-founder-mode`](skills/one-week-founder-mode/) | AI Native Bets | One main bet, two microbets, a kill list |

## Voice Native：两个 Skill 联动但职责不同

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

第一批不要用“18 个 Skill”作为主要宣传语。更好的传播方式是选择一个真实痛点，用 before/after 证明某一个 Skill 确实改变了结果。

## 校验

```bash
pip install pyyaml
python scripts/validate_skills.py
```

## License

MIT.
