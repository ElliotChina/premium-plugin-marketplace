# thinking

思维工具插件：覆盖"想清楚"的完整链条——**澄清意图 → 发散方案 → 拷问打磨 → 沉淀术语与决策**。技能均不绑定产品领域，任何需要把模糊想法变成清晰方案的场景可用。

## 技能

### interview-me（源自 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)，MIT）

意图访谈技能：在计划、规格、代码存在之前，一次一个问题（附自己的猜测）逐层澄清用户"真正想要什么"，直到能预测用户对接下来三个问题的反应（约 95% 置信度）。适用于需求欠规格的请求（"给我做个 X"却说不清给谁用、为什么现在做）；确认后产出结构化意图声明（Outcome / User / Why now / Success / Constraint / Out of scope），可保存到 `docs/intent/` 或交给下游规格流程。

### idea-refine（源自 addyosmani/agent-skills，MIT）

创意打磨技能：把模糊想法变成经过推敲的方案。通过多视角框架（第一性原理、反脆弱、10/10/10 等）生成变体，用评估标准筛选，支持交互式问答或 `scripts/idea-refine.sh` 初始化 ideas 目录后多轮迭代。附 examples.md（优秀构思示例）、frameworks.md（框架清单）、refinement-criteria.md（评估标准）。与 interview-me 互补：interview-me 澄清"要什么"，idea-refine 展开"可能是什么"。

### grill 系列（源自 [mattpocock/skills](https://github.com/mattpocock/skills)，MIT）

方案拷问技能组。`grill-me` 与 `grill-with-docs` 为手动入口（模型不会自动触发）；`grilling` 是可被模型自动调用的拷问原语，也供其他技能内部调用：

| 技能 | 作用 |
|------|------|
| `grill-me` | 对你的方案 / 决策发起不留情面的多轮追问，直到达成共识 |
| `grill-with-docs` | 同上，追问过程中同步沉淀 GLOSSARY 术语表与 ADR 决策记录 |
| `grilling` | 拷问核心逻辑：把决策映射成设计树，每轮一次性问完当前可问的全部问题 |

```bash
/grill-me              # 拷问我目前的方案
/grill-with-docs       # 拷问方案并顺手写文档（GLOSSARY + ADR）
```

### domain-modeling（源自 [mattpocock/skills](https://github.com/mattpocock/skills)，MIT）

领域建模技能：挑战模糊术语、用具体场景压测概念边界、内联更新 `GLOSSARY.md`、按三条标准克制地提议 ADR。可与 grill 系列配合（grill-with-docs 内部即引用其规范）。

## 关联插件

- **coding** 插件的 `improve-codebase-architecture` 技能会调用本插件的 `grilling` 与 `domain-modeling`：两插件同装时其拷问与文档环节完整可用，单装本插件不受影响。
- 方案敲定后的正式需求沉淀（PRD）在 **product-plan** 插件。

## 安装

```bash
claude plugin install thinking@premium-plugin-marketplace
```
