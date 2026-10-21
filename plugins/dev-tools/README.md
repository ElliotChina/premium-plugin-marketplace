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

方案拷问与领域建模技能组。`grill-me` 与 `grill-with-docs` 为手动入口（模型不会自动触发）；`grilling` 与 `domain-modeling` 是可被模型自动调用的参考技能，也供其他技能内部调用：

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

### improve-codebase-architecture（源自 mattpocock/skills，MIT）

架构深化技能：扫描代码库找出「深模块化」重构机会（把浅模块变深模块），生成自包含的 HTML 视觉报告（前后对比图 + 推荐强度徽章），用户选定候选后进入 grilling 拷问循环，过程中用 domain-modeling 同步维护 GLOSSARY 与 ADR。

```bash
/improve-codebase-architecture              # 全库扫描热区
/improve-codebase-architecture <模块/路径>   # 只扫指定方向
```

工作方式：先从 git 历史找热点定范围（YAGNI 优先），子代理有机探索摩擦点（浅模块、无局部性、接缝泄漏、难测试），对候选应用删除测试，然后写 HTML 报告到系统临时目录（不进仓库）并打开。用 codebase-design 的深模块词汇表述每个建议。

### codebase-design（源自 mattpocock/skills，MIT）

深模块设计共享词汇：**module、interface、depth、seam、adapter、leverage、locality** 七个术语及其原则（删除测试、"接口即测试面"、"一个 adapter 是假想接缝，两个才是真接缝"）。设计或重构代码时使用，也是 improve-codebase-architecture 的词汇基础。附 DEEPENING.md（深化手法）与 DESIGN-IT-TWICE.md（双方案并行设计模式）。

### implement（源自 mattpocock/skills，MIT）

spec / ticket 驱动实现技能：按规格或工单实现工作，在预先约定的接缝处用 tdd 红绿循环推进，定期跑类型检查与单测，收尾跑全量测试，完成后用 code-review 审查并提交到当前分支。

```bash
/implement                  # 按用户给出的 spec 实现
/implement PROJ-123         # 拉取工单并实现
```

### tdd（源自 mattpocock/skills，MIT）

测试驱动开发参考：红 → 绿循环中产出值得保留的测试。好测试的标准（验证公共接口行为而非实现细节）、接缝（seam）先行（测试只写在和用户预先约定的接缝上）、反模式清单（实现耦合、同义反复、水平切片）、循环纪律（红先于绿、一次一片、重构不在循环内）。附 tests.md（示例）与 mocking.md（mock 准则）。

### interview-me（源自 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)，MIT）

意图访谈技能：在计划、规格、代码存在之前，一次一个问题（附自己的猜测）逐层澄清用户"真正想要什么"，直到能预测用户对接下来三个问题的反应（约 95% 置信度）。适用于需求欠规格的请求（"给我做个 X"却说不清给谁用、为什么现在做）；确认后产出结构化意图声明（Outcome / User / Why now / Success / Constraint / Out of scope），可保存到 `docs/intent/` 或交给下游规格流程。与 grill 系列互补：interview-me 在动手前澄清意图，grilling 在方案成型后拷问设计。

### idea-refine（源自 addyosmani/agent-skills，MIT）

创意打磨技能：把模糊想法变成经过推敲的方案。通过多视角框架（第一性原理、反脆弱、10/10/10 等）生成变体，用评估标准筛选，交互式问答多轮迭代，ideas 目录（`docs/ideas`）按需创建。附 examples.md（优秀构思示例）、frameworks.md（框架清单）、refinement-criteria.md（评估标准）。与 interview-me 互补：interview-me 澄清"要什么"，idea-refine 展开"可能是什么"。

> 迁移说明：上游附带的 `scripts/idea-refine.sh`（仅 `mkdir -p docs/ideas`）未迁入——避免同步可执行第三方代码，目录初始化由 agent 直接完成，行为等价。

## 安装

```bash
claude plugin install dev-tools@premium-plugin-marketplace
```
