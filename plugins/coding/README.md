# coding

开发过程工具集：多档位代码审查、质量清理、安全审查、TDD 与 spec/ticket 驱动实现、bug/性能诊断、深模块设计、后台调研。

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

### improve-codebase-architecture（源自 mattpocock/skills，MIT）

架构深化技能：扫描代码库找出「深模块化」重构机会（把浅模块变深模块），生成自包含的 HTML 视觉报告（前后对比图 + 推荐强度徽章），用户选定候选后进入 grilling 拷问循环，过程中用 domain-modeling 同步维护 GLOSSARY 与 ADR。

```bash
/improve-codebase-architecture              # 全库扫描热区
/improve-codebase-architecture <模块/路径>   # 只扫指定方向
```

工作方式：先从 git 历史找热点定范围（YAGNI 优先），子代理有机探索摩擦点（浅模块、无局部性、接缝泄漏、难测试），对候选应用删除测试，然后写 HTML 报告到系统临时目录（不进仓库）并打开。用 codebase-design 的深模块词汇表述每个建议。

> 依赖说明：grilling 与 domain-modeling 现位于 product-design 插件，同装两个插件时拷问与文档环节完整可用；单装本插件时技能主体（扫描 + HTML 报告）不受影响，拷问环节降级为普通追问。

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

### research（源自 mattpocock/skills，MIT）

后台研究技能：拉起后台 agent 对照一手信源（官方文档、源码、规范）调查问题，结论写成单个 Markdown 文件并逐条标注出处，不阻塞当前工作。

### diagnosing-bugs（源自 mattpocock/skills，MIT）

系统化诊断循环：针对难复现的 bug 与性能回退，按假设驱动的流程定位根因。含人机协作复现模板 `scripts/hitl-loop.template.sh`（复制后按场景改写步骤，agent 执行、用户在终端按提示操作，输出回喂 agent）。

### performance-optimization（源自 addyosmani/agent-skills，MIT）

性能优化技能：覆盖前端、后端、查询与数据库的性能问题。流程为测量 → 定位单一瓶颈 → 修复 → 复测；反模式清单（N+1 查询、无界取数、索引失效、连接池耗尽、缓存缺失、图片优化、重渲染、包体积）各附 worked fix，详见技能内 `references/optimization-patterns.md` 与插件 `references/performance-checklist.md`。

## 安装

```bash
claude plugin install coding@premium-plugin-marketplace
```
