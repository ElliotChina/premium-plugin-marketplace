---
name: review
argument-hint: "[审查目标：代码路径、spec/plan 文件路径、文档文件、PR 编号]"
description: >
  This skill should be used when the user runs "/devflow:review" to review code or documents.
  Supports code review, spec review, plan review, doc review, PR review, and design review.
  Uses concurrent multi-agent review pattern for code, spec, and plan reviews.
---

# Review - 审查

结构化的审查工作流，支持多种审查类型。代码、Spec 和计划审查支持多 agent 并发审查模式。

## 触发方式

用户执行 `/devflow:review` 命令时激活。传入审查目标作为参数。

## 工作流程

### 1. 确定审查类型

根据用户输入判断审查类型：

- **代码审查** — 审查指定文件或目录的代码质量
- **Spec 审查** — 审查需求规格文档的完整性和一致性
- **计划审查** — 审查实现计划的可执行性
- **文档审查** — 审查文档的准确性、完整性和规范性
- **PR 审查** — 通过 gh 命令获取 PR 变更进行审查
- **UI/UX 设计审查** — 审查前端 UI/UX 设计质量

如果范围不明确，主动询问用户。

### 2. 插件与技能准备

根据审查涉及的技术栈，检查并加载所需插件和技能：

- **通用**：`context7-plugin` — 查阅技术栈最新文档和 API，贯穿审查全周期
- **前端项目必选**：`frontend-design` — Web 页面设计；`ui-ux-pro-max` — 企业级 UI/UX 设计标准（需要时）
- **React 技术栈**：按需加载 `vercel-react-best-practices`（性能优化）、`vercel-composition-patterns`（组件组合模式）、`vercel-react-native-skills`（React Native 开发）
- **UI 组件库**：按需加载 `antd`（Ant Design 组件使用）、`ant-design`（Ant Design 架构决策与主题定制）、`shadcn`（shadcn/ui 组件管理）

### 3. 执行审查

根据审查类型，启用对应的编排技能（内部已完成派发并发 agent → 合并反馈 → 修复的全流程）：

**代码审查 / PR 审查：**
- 前端项目审查时加载 `web-design-guidelines` — 基于 Web Interface Guidelines 进行 UI/UX 合规审查
- 启用 `devflow:code-review` 技能（并发数 3）

**Spec 审查：**
- 启用 `devflow:spec-review` 技能（并发数 3）

**计划审查：**
- 启用 `devflow:plan-review` 技能（并发数 3）

**文档审查 / UI/UX 设计审查（直接分析）：**

- **文档审查**：读取文档内容，对照代码验证准确性
- **UI/UX 设计审查**：读取前端代码和组件结构

#### 文档审查关注点

- 内容与代码行为不一致 → 立即修正
- 结构缺失或逻辑混乱 → 重组文档结构
- 示例代码无法运行 → 修正或补充可运行的示例
- 格式不规范、排版不一致 → 统一格式
- 遗漏或过时信息 → 更新至最新状态

#### UI/UX 设计审查关注点

- 无障碍合规性缺失 → 立即修复
- 交互不合理或用户体验问题 → 评估影响后修复
- 视觉层次混乱或信息架构不清 → 重构优化
- 响应式适配缺失 → 补充适配方案
- 设计系统不一致 → 对齐设计规范

完成后按以下格式输出审查报告：

```
## 审查报告

### 严重问题（必须修复）
- [问题说明及修复建议]

### 建议优化（推荐改进）
- [优化建议及理由]

### 亮点（做得好的地方）
- [值得肯定的做法]
```
