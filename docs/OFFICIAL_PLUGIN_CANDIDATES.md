# Official Plugin Candidate Classification

本分类在最终 Tier 1 全部通过之后进行。静态与安全通过只说明基础门槛满足，不自动等于适合官方目录；用途边界、误用后果、隐私敏感度、外部状态变更和维护成本同样参与分类。

## A. Official Plugin candidates

| Skill | Why it is a candidate | Packaging note |
|---|---|---|
| build-in-public-launcher | 用途清晰、无默认外部写入、拒绝虚假指标，Quality 94.5 | 适合作为首批候选；发布动作继续要求显式授权 |
| cross-domain-translator | 结构化迁移问题，默认只读、低操作风险 | 保留“类比会失效”的边界说明 |
| deployment-proof | 以证据账本和脱敏为中心，默认不发布、不 push | 封装时突出隐私审查与本地扫描 |
| skill-from-scars | 产生可评测的 Skill 方案，拒绝泛化 prompt，Quality 92.2 | 本地脚手架应继续保持可选 |
| small-server-fit | 核心是评估和计算，不从猜测给采购建议 | 官方包中保持 `NOT MEASURED` 结论可见 |
| vibe-to-spec | 清晰区分推断和阻断项，Quality 92.2 | 记忆只能在宿主合法暴露时使用 |
| voice-dump-to-todo | 默认产出本地任务结构，Quality 93.5 | 外部任务管理器写入不应成为默认能力 |
| voice-with-temperature | 编辑型、低风险、个人特点鲜明且边界稳定 | 适合作为轻量官方候选 |

建议的第一提交批次：`build-in-public-launcher`、`vibe-to-spec`、`voice-dump-to-todo`、`skill-from-scars`、`voice-with-temperature`。它们的用途辨识度最高，且没有生产基础设施、健康或个人财务决策的默认风险。

## B. Community / Experimental Skills

| Skill | Why community-first |
|---|---|
| anti-slop-personal-brand | 强烈的个人审美与职业叙事判断，适合社区迭代，不宜过早标准化 |
| csdn-technical-writing | 平台和作者风格高度具体，CSDN 规则也可能变化 |
| deep-talk-to-podcast | 会处理私密对话，并依赖持续更新的音频平台信息 |
| one-week-founder-mode | 有价值但属于个人生产力实验，主赌注与 kill list 需要更多用户验证 |
| personal-boardroom | 涵盖职业、金钱和生活决策，范围较宽，容易被误解为权威建议 |
| social-signal-and-tact | 已有真实性和反操纵护栏，但涉及权力关系、讨好和社交影响，不适合仅因有趣就提交官方目录 |
| trend-to-microbet | 依赖实时趋势验证，实验性强，适合快速社区更新 |

这些 Skills 建议目前只保留 GitHub 社区版本。进入官方候选前，应补充真实外部用户反馈、误触发案例和边界测试，而不是增加未经验证的使用量数据。

## C. Hold / Rewrite

| Skill | Why hold | Required rewrite or evidence |
|---|---|---|
| aliyun-fullstack-deploy | 能修改生产主机、systemd、Nginx 和发布链接；即使 Tier 1 通过，误用后果仍高 | 建立隔离 VPS 集成测试、发行版矩阵、最小权限执行模型和可重复回滚测试后再评估 |
| student-money-four-buckets | 固定起始比例容易被误当成个性化财务建议，且不同地区、债务和保障条件差异大 | 把比例降级为可选示例，先做现金流和紧急状况分流，强化地区与投资边界测试 |
| fitness-recovery-coach | 涉及疼痛、恢复和重返训练，存在健康误用风险 | 增加红旗症状、紧急转介、适用人群排除、训练负荷边界和经验证的健康信息来源 |

## Packaging readiness

仓库已经达到“为 A 类候选开始官方 Plugin 封装”的阶段，但没有达到“把全部 18 个 Skills 作为一个官方包提交”的阶段。建议先封装第一批 5 个低风险、高辨识度候选，完成目录规范、宿主兼容性和人工体验测试；B 类留在 GitHub 继续收集证据，C 类暂停官方提交。

本次没有发布 Marketplace、没有创建官方目录提交，也没有代表用户向外部平台发送内容。
