# NVIDIA SkillEvaluator Tier 1 Report

评测日期：2026-09-08（Asia/Shanghai）

评测对象：`skills/` 下全部 18 个 Agent Skills。

## 结论

- 基础 Tier 1：18/18 通过。
- 完整 Tier 1：18/18 通过。
- 完整扫描证据：0 个 incomplete，0 个 CRITICAL，0 个 HIGH。
- Quality 等级：A 级 4 个，B 级 14 个，C 级 0 个。
- 平均 Quality：87.7。
- Quality >= 90：4 个，正好覆盖四个旗舰 Skills。
- 本次没有运行 `--llm`、`--llm-verify`、Tier 2 或 Tier 3，也没有调用付费 LLM API。

这里的 “Security” 汇总 NVIDIA Security Scan（SkillSpector）、Code Risk Analysis（Semgrep 与 Bandit）、Secrets Detection（Gitleaks）以及 Code Integrity & Hygiene。`Final` 使用 SkillEvaluator 的最终 `overall_status`，不是人工改写的结论。

## 逐 Skill 最终结果

| Skill | Schema | PII | License | Security | Unicode | Lint | Quality | Score | Grade | Final |
|---|---|---|---|---|---|---|---|---:|---|---|
| aliyun-fullstack-deploy | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 85.5 | B | PASS |
| anti-slop-personal-brand | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 86.5 | B | PASS |
| build-in-public-launcher | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 94.5 | A | PASS |
| cross-domain-translator | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 89.0 | B | PASS |
| csdn-technical-writing | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 80.8 | B | PASS |
| deep-talk-to-podcast | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 87.8 | B | PASS |
| deployment-proof | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 83.8 | B | PASS |
| fitness-recovery-coach | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 87.8 | B | PASS |
| one-week-founder-mode | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 86.5 | B | PASS |
| personal-boardroom | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 87.8 | B | PASS |
| skill-from-scars | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 92.2 | A | PASS |
| small-server-fit | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 82.0 | B | PASS |
| social-signal-and-tact | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 87.8 | B | PASS |
| student-money-four-buckets | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 87.0 | B | PASS |
| trend-to-microbet | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 85.8 | B | PASS |
| vibe-to-spec | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 92.2 | A | PASS |
| voice-dump-to-todo | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 93.5 | A | PASS |
| voice-with-temperature | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 87.8 | B | PASS |

## 旗舰目标

| Flagship Skill | Target | Final | Result |
|---|---:|---:|---|
| vibe-to-spec | >= 90 | 92.2 | MET |
| voice-dump-to-todo | >= 90 | 93.5 | MET |
| skill-from-scars | >= 90 | 92.2 | MET |
| build-in-public-launcher | >= 90 | 94.5 | MET |

## 对 80–89 分 Skills 的审查

14 个 B 级 Skill 都已逐项复核，没有低于 80 的 Skill。保留 B 级而没有机械扩写的主要原因如下：

- 指南型 Skills（anti-slop-personal-brand、cross-domain-translator、deep-talk-to-podcast、fitness-recovery-coach、one-week-founder-mode、personal-boardroom、social-signal-and-tact、student-money-four-buckets、trend-to-microbet、voice-with-temperature）刻意保持紧凑。部分没有为了评分增加独立的 Examples、Troubleshooting 或 Requirements 标题；其边界、流程和输出已经在现有领域结构中表达。
- 脚本型 Skills（aliyun-fullstack-deploy、csdn-technical-writing、deployment-proof、small-server-fit）受到 “Available Scripts 表格” 和 `run_script` 字面调用启发式影响。`run_script` 不是跨 Agent 平台的真实统一 API，因此没有写入虚假调用；实际可运行命令仍使用本地相对路径。
- SkillEvaluator 0.2.1 的 Quality 检查会对缺少顶层 `version` 给出 MEDIUM advisory，而同版本的 Semantic Version 检查通过。把版本放进官方 metadata 结构会被 SkillSpector 2.11.1 当作路径引用，造成 incomplete evidence；因此没有增加旧式顶层字段，也没有 suppress 该 advisory。
- 所有长分类、模板和平台细节继续保留在 `references/`，没有为分数堆砌关键词或拉长主说明文件。

## 保留的非阻断安全告警

`aliyun-fullstack-deploy` 最终只剩 MEDIUM：未声明通用预授权工具范围、临时 canary 使用 `nohup`、生产切换使用 `systemctl`、以及对明确目标 URL 的健康检查。它们符合该 Skill 的真实部署用途；删除会使验证和回滚失真。该 Skill 因实际生产变更能力被归入 Hold / Rewrite，而不是官方目录候选。

少数本地脚本型 Skills 保留 SkillSpector 的 LP3 MEDIUM，因为增加宽泛 `Bash` 权限会扩大预授权面并被扫描器评为 HIGH。这里选择在工作流中逐次取得用户授权，而不是为了消除提示授予宽权限。

## 运行环境与命令

- Python 3.13.15
- uv 0.12.10
- NVIDIA SkillEvaluator 0.2.1
- Semgrep 1.176.1
- NVIDIA SkillSpector 2.11.1，静态模式 `--no-llm`
- Gitleaks 8.30.1

基础命令：

```bash
skillevaluator validate ./skills \
  --type skill \
  --checks schema,pii,license,quality,unicode,lint \
  --no-dedup \
  --continue-on-failure \
  -r json \
  -o eval-results/nvidia-tier1
```

完整 Tier 1：

```bash
skillevaluator validate ./skills \
  --type skill \
  --no-dedup \
  --continue-on-failure \
  -r json \
  -o eval-results/nvidia-tier1-full
```

Windows 上 Semgrep 1.176.1 的 Python 前端在本机触发原生 IPC 与证书存储错误。最终扫描使用临时兼容启动器：仍由同一 Semgrep CLI 生成规则和目标计划，再以单任务方式调用同一安装包内的 `semgrep-core.exe`；没有改规则、过滤结果或 suppress。兼容启动器只存在于评测临时目录，不属于发布包。

## 原始证据

- `eval-results/nvidia-tier1/`：基础检查的原始、按时间戳命名的 JSON；最新一轮为修复后结果，早期结果用于保留修复轨迹。
- `eval-results/nvidia-tier1-full/`：按 Skill 保存完整 Tier 1 的全部时间戳 JSON 与 SkillEvaluator 生成的 `BENCHMARK.md`。早期重试包含扫描器不可用或 Windows 证书存储故障的 incomplete 记录；每个目录中时间戳最新的 JSON（2026-09-08 12:16:48 至 12:19:02）是最终证据，18/18 均为 `passed`、0 incomplete、0 CRITICAL、0 HIGH。重试记录被保留为排障证据，没有删除或覆盖。

评测依据：

- [NVIDIA SkillEvaluator repository](https://github.com/NVIDIA/SkillEvaluator)
- [Tier 1 validation](https://docs.nvidia.com/skills/skillevaluator/tier1-validation)
- [Installation](https://docs.nvidia.com/skills/skillevaluator/installation)
- [Reports](https://docs.nvidia.com/skills/skillevaluator/reports)
