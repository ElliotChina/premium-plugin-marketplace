# dev-tools

开发工具集插件。

## 技能

### code-review

多档位代码审查技能：审查当前 diff 或指定目标（PR 编号 / 分支 / 路径），找出正确性 bug 与清理点（复用 / 简化 / 效率 / 抽象层级 / 仓库规范）。

```bash
/code-review                    # 默认 medium 档，评审当前分支 diff
/code-review high               # recall 偏置，尽量抓全真 bug
/code-review xhigh              # 10 个角度全量深挖 + 补漏 sweep
/code-review low path/to/file   # 快扫单个路径
/code-review 123 --comment      # 评审 PR #123，findings 发为 inline 评论
/code-review --fix              # 评审后把确认的 findings 直接修复到工作区
/code-review --max-findings 5   # 最多报告 5 条
```

工作方式：每个档位由一组独立 finder 角度并行找候选 findings（每个候选必须带具体失败场景），再去重、验证（1-vote verify 或 dedup + sweep），最后按严重程度报告。linter / 类型检查 / CI 能抓到的问题不在评审范围内。

### simplify

代码质量清理技能：审查改动代码中的复用、简化、效率、抽象层级四类问题，然后**直接修复**。只做质量清理，不找 bug（找 bug 用 code-review）。

```bash
/simplify              # 4 个清理角度并行审查当前 diff，逐条修复
/simplify path/to/dir  # 只清理指定路径
```

工作方式：4 个只读 agent 并行从四个角度审查 diff（每条 finding 带具体代价），汇总去重后逐条修复；会改变既有预期行为或超出 diff 范围的跳过并记录原因。修复后运行项目检查确认行为等价。

### security-review

安全审查技能：以资深安全工程师视角审查当前分支待提交改动，只报告高置信度、有真实利用路径的安全漏洞（>80% 置信度）。

```bash
/security-review       # 审查当前分支相对 origin/HEAD 的全部改动
```

工作方式：收集 diff 后，先由子任务结合仓库既有安全模式识别漏洞（输入验证 / 认证授权 / 加密与密钥 / 注入与代码执行 / 数据暴露五类），再对每个漏洞并行启动误报过滤子任务（17 项硬排除 + 12 项先例），置信度低于 8 的丢弃。输出 markdown 报告（severity、category、exploit scenario、fix recommendation）。

### grill 系列（源自 [mattpocock/skills](https://github.com/mattpocock/skills)，MIT）

方案拷问与领域建模技能组，均只响应用户手动调用，模型不会自动触发：

| 技能 | 作用 |
|------|------|
| `grill-me` | 对你的方案 / 决策发起不留情面的多轮追问，直到达成共识 |
| `grill-with-docs` | 同上，追问过程中同步沉淀 GLOSSARY 术语表与 ADR 决策记录 |
| `grilling` | 拷问核心逻辑：把决策映射成设计树，每轮一次性问完当前可问的全部问题 |
| `domain-modeling` | 领域建模：挑战模糊术语、用具体场景压测概念边界、内联更新 GLOSSARY.md、按三条标准克制地提议 ADR |

```bash
/grill-me              # 拷问我目前的方案
/grill-with-docs       # 拷问方案并顺手写文档（GLOSSARY + ADR）
```

## 安装

```bash
claude plugin install dev-tools@premium-plugin-marketplace
```
