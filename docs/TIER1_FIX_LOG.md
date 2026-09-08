# NVIDIA Tier 1 Fix Log

日期：2026-09-08

## Baseline

首次基础运行发现 18/18 个 Skill 都因缺少 `metadata.author` 产生 HIGH Schema 问题，因此 0/18 通过。初始 Quality 范围为 77.2–85.5；`csdn-technical-writing`、`skill-from-scars` 和 `small-server-fit` 低于 80。外部扫描器还发现未固定版本的 `npx` 安装入口、含糊的路径式斜杠写法、部署脚本的敏感文件处理与回滚删除问题，以及少量静态解析误判。

## CRITICAL / HIGH fixes

| Area | Baseline finding | Fix | Final evidence |
|---|---|---|---|
| All 18 Skills | Schema HIGH: missing external-author identity | 使用仓库 Git 提交者的真实身份补充 `metadata.author`，并声明仓库真实 MIT 许可 | Schema 18/18 PASS；0 HIGH |
| Aliyun release handling | SkillSpector PE3 HIGH around credential-file paths | 发布构建默认排除全部隐藏文件；包检查拒绝任意隐藏路径；本地预检不读取隐藏文件 | SkillSpector complete；max issue MEDIUM |
| Aliyun rollback | SkillSpector TM1 HIGH on forced removal of `current` link | 改为仅允许 `unlink` 已验证的符号链接；非符号链接立即拒绝 | Security PASS；0 HIGH |
| Aliyun verification | Shell pattern combined `curl` and hash pipeline into SC2 HIGH | 改为有界递增索引保存受保护 URL 的验证结果，移除易误判管道 | Security PASS；0 HIGH |
| Aliyun privilege scope | root checks and broad tool declaration raised risk | 移除脚本对 root 的硬要求，改为专用部署账号与按需提权；没有为消除 LP3 而授予宽泛 Bash 预授权 | Aggregate risk MEDIUM；0 HIGH |
| build-in-public-launcher | MP3 HIGH matched the phrase “Clear statement” as “Clear state” | 改写为 “Explicit disclosure of validation gaps”，语义不变且不触发状态修改规则 | SkillSpector complete；0 HIGH |
| skill-from-scars | AE1 HIGH from unresolved shorthand and a nonexistent asset-directory reference | 用自然语言描述资源类别，仅保留真实脚本路径和参数占位符 | SkillSpector complete；0 HIGH |
| social-signal-and-tact | 合并公开仓库更新后，SkillSpector 把礼物/礼貌与本地/时令的斜杠速记误判为文件路径 | 改为等价自然语言 “gift and courtesy” 与 “local or seasonal”，保留原有社交语义和新内容 | SkillSpector `--no-llm` complete；Security PASS |
| All README install snippets | RP1 MEDIUM: unpinned `npx skills add` supply-chain surface | 移除未固定版本入口；保留仓库已有的 GitHub CLI 和手动复制路径 | 对应 RP1 不再出现 |

没有使用 baseline suppression、allowlist suppression 或关闭 Schema、PII、License、Security 检查来取得通过。

## Quality and maintainability fixes

- 为全部 18 个 Skill 增加真实作者、MIT 许可和少量用途标签；没有增加虚假的 compatibility、usage、install、user 或 benchmark 数据。
- 把会被当作本地路径的 `A/B` 式速记改为 “A and B” 或 “A or B”，保留真实 Markdown 链接。
- 为四个旗舰 Skill 补充紧凑的 Purpose、Instructions、Examples、Limitations 和 Troubleshooting；脚本型旗舰增加真实脚本参数表。
- `skill-from-scars` 与 `voice-dump-to-todo` 的 Python 脚本重构为有输入验证、函数边界和 `main()` 的可测试结构。
- `csdn-technical-writing` 的 linter 同样增加输入验证、函数边界和命名阈值常量。
- 删除未固定版本的 README 安装命令，避免在安装时执行随时间漂移的第三方包。
- 长规则和模板继续放在 `references/` 或 `assets/`；主说明保持明显低于 500 行。

Quality 变化摘要：

| Skill | Baseline | Final |
|---|---:|---:|
| build-in-public-launcher | 85.5 | 94.5 |
| vibe-to-spec | 85.5 | 92.2 |
| voice-dump-to-todo | 80.2 | 93.5 |
| skill-from-scars | 78.5 | 92.2 |
| csdn-technical-writing | 77.2 | 80.8 |
| small-server-fit | 78.5 | 82.0 |

其余 Skills 均保持或提升到 80–89 的 B 级区间。没有低于 80 的最终结果。

## Verification performed

- 基础 Tier 1：`schema,pii,license,quality,unicode,lint`，18/18 PASS。
- 完整 Tier 1：默认 11 个检查，18/18 PASS。
- 完整报告：0 incomplete，0 CRITICAL，0 HIGH。
- Python 静态语法解析：11 个脚本通过。
- Bash `-n`：6 个脚本通过（使用 Git for Windows Bash）。
- 四个旗舰 Quality：94.5、92.2、93.5、92.2，全部达到 >= 90。

## Stage 3 marketplace-policy regression

- 为四个插件增加独立 `PRIVACY.md`，披露真实的数据收集、网络、脚本和权限边界；每个 README 直接链接该文件。
- 插件校验器现在要求 `PRIVACY.md` 存在并由 README 链接。此改动没有 suppress Schema、PII、License 或 Security，也没有修改 canonical Skill 内容。
- 2026-09-08 14:37:27 至 14:39:39 再次运行完整 NVIDIA Tier 1：18/18 PASS、平均 Quality 87.7、4 个 Quality >= 90、0 incomplete、0 CRITICAL、0 HIGH。
- 首次回归尝试因 Windows GBK 无法解码外部扫描器 UTF-8 输出而退出 1；设置 `PYTHONUTF8=1` 与 `PYTHONIOENCODING=utf-8` 后，同一检查集合正常完成。中断尝试没有生成 JSON 报告。

## Tool provenance

- SkillEvaluator 0.2.1：从 NVIDIA 官方仓库源码包安装；SHA-256 `97C981595485BF5A928DB1C72890F7BE4D7C8194804131E7249E9517E1CBB5A2`。
- SkillSpector 2.11.1 安装源码包：SHA-256 `326CCDF5E52EED6238D106D2C92BEF513DB781ADB83F658336D63DFEA10D1ACD`。
- Gitleaks 8.30.1 Windows archive：SHA-256 `D29144DEFF3A68AA93CED33DDDF84B7FDC26070ADD4AA0F4513094C8332AFC4E`。
- 安装与扫描工具均位于工作区临时目录，没有被加入发布仓库。
