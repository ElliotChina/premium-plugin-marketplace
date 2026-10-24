# product-design

产品与设计技能插件：覆盖产品工作的完整链条——**澄清意图 → 发散方案 → 拷问打磨 → 沉淀术语决策 → 沉淀正式 PRD**。

## 技能

### interview-me（源自 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)，MIT）

意图访谈技能：在计划、规格、代码存在之前，一次一个问题（附自己的猜测）逐层澄清用户"真正想要什么"，直到能预测用户对接下来三个问题的反应（约 95% 置信度）。适用于需求欠规格的请求（"给我做个 X"却说不清给谁用、为什么现在做）；确认后产出结构化意图声明（Outcome / User / Why now / Success / Constraint / Out of scope），可保存到 `docs/intent/` 或交给下游规格流程。

### idea-refine（源自 addyosmani/agent-skills，MIT）

创意打磨技能：把模糊想法变成经过推敲的方案。通过多视角框架（第一性原理、反脆弱、10/10/10 等）生成变体，用评估标准筛选，支持交互式问答或 `scripts/idea-refine.sh` 初始化 ideas 目录后多轮迭代。附 examples.md（优秀构思示例）、frameworks.md（框架清单）、refinement-criteria.md（评估标准）。与 interview-me 互补：interview-me 澄清"要什么"，idea-refine 展开"可能是什么"。

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

### requirement-prd（自研）

需求期 PRD 撰写技能：为单个未上线需求撰写结构化需求文档，完全独立使用。从对话上下文综合成文（系统化澄清交给 interview-me / grilling），按需求形态套用规范化骨架——单功能需求按功能类型裁剪、跨模块流程需求用流程骨架、全局定义增量按全局规范表结构起草拟新增条目、横切通用能力与新模块各有对应骨架。行为级章节（流程 / 字段 / 规则 / 状态 / 权限 / 异常 / 验收）一律写目标行为，验收场景可衡量可推演，拿不准的规则以待确认标记求证。文档存 `docs/requirements/`（进行中直接放根目录、文件名带 `MM-DD-` 日期前缀，已合并归档至 `archive/<年-月>/`；或贴入任务系统工作项），未上线前不进主 PRD；章节与表头固定规范，与主流主 PRD 体系天然对齐，上线确认后可零转换融入。

### project-prd（自研）

PRD 体系管理技能：在软件项目中建立并持续维护一套 Git 友好、AI 可检索的产品需求文档体系——四层 `prd/` 目录（产品总览 / 全局规范 / 业务模块 / 跨模块流程）。核心纪律：主 PRD 只描述当前生产环境，增量需求在外部任务系统管理、上线后才融入；持续更新不做版本副本，历史交给 Git Commit 与 Tag。覆盖三类工作流：初始化 prd/ 体系、融合已上线需求（含跨模块影响检查）、PRD 质量检查。内置完整管理规范（`references/prd-spec.md`）、12 类标准文档模板库（`references/templates/`，每类模板独立成文件，按文档类型分轻量化 / 规则化 / 精细化三档严格程度）与交付前机械检查脚本（`scripts/prd-check.py`，ERROR/WARN 分级：悬空链接、索引登记、占位符与指引残留、结构体量嫌疑）。承接本插件链条末端：interview-me / idea-refine 澄清发散，grill 系列打磨，domain-modeling 沉淀术语，project-prd 沉淀正式需求文档。

装好即用，在目标项目里对 Claude 直接说：

- **"初始化 PRD 目录"** → 新建 docs/prd/ 体系并套用模板
- **"给 XX 需求写个 PRD"** → 撰写需求期 PRD（规范化结构，上线后可顺畅融入主 PRD）
- **"XX 功能已上线，把它合并进 PRD"** → 融合增量需求（含跨模块影响检查与提交前门禁）
- **"检查一下 PRD"** → 质量审查，输出问题清单

## 关联插件

coding 插件的 `improve-codebase-architecture` 技能会调用本插件的 `grilling` 与 `domain-modeling`：两插件同装时其拷问与文档环节完整可用，单装本插件不受影响。

原型相关技能已拆分至 `prototype-design` 插件（`prototype-app` 可执行镜像原型 / `prototype` 即抛式发散对比）。

## 安装

```bash
claude plugin install product-design@premium-plugin-marketplace
```
