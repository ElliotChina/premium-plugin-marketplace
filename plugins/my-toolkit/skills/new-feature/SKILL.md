---
name: new-feature
argument-hint: "[功能描述]"
description: >
  This skill should be used when the user runs "/my-toolkit:new-feature" to develop a new feature.
  Provides a structured workflow from requirement analysis, design, implementation to verification.
---

# New Feature - 新功能开发

结构化的新功能开发工作流，从需求到交付全流程引导。

## 触发方式

用户执行 `/my-toolkit:new-feature` 命令时激活。传入功能描述作为参数。

## 执行模式

技能加载后，**立即**使用 `AskUserQuestion` 询问用户选择执行模式：

**全自动**：执行过程中人不介入，直接从需求分析运行到流程结束。流程中所有需要用户决策的环节一律采用推荐值，并在执行日志中标注 `[auto] ` 前缀说明选择了什么及理由。**禁止在流程中使用 `AskUserQuestion` 或任何交互式提问**，遇到不确定的问题基于上下文自行判断。适用于对需求描述有信心、希望快速交付的场景。

**半自动**：在以下关键节点完成后暂停，等待人工审查确认再继续：
- 方案审查完成后
- 计划审查完成后
- 代码审查并修复完成后

半自动模式适用于需求复杂、设计决策关键、或希望对产出质量逐层把控的场景。

记住用户选择的模式，后续步骤据此决定是否在审查节点后暂停。

## 工作流程

### 1. 需求探索

> 启用 `superpowers:brainstorming`，在编码前强制进行需求澄清和设计探索。

如果功能简单明确，可简化探索过程，但仍需确认关键设计决策。

### 2. 方案审查（并发3次）

启用 `my-toolkit:requesting-spec-review` 技能，派发 3 个并发审查 subagent。

所有 agent 审查完成后，启用 `my-toolkit:receiving-spec-review` 技能合并去重反馈并修复问题。

> **半自动暂停点**：如果为半自动模式，向用户展示方案审查结果摘要，等待用户确认后再进入下一步。

### 3. 编写实现计划

> 启用 `superpowers:writing-plans`，将确认的设计转化为可执行的实现计划。

### 4. 审查实现计划（并发3次）

启用 `my-toolkit:requesting-plan-review` 技能，派发 3 个并发审查 subagent。

所有 agent 审查完成后，启用 `my-toolkit:receiving-plan-review` 技能合并去重反馈并修复问题。

> **半自动暂停点**：如果为半自动模式，向用户展示计划审查结果摘要，等待用户确认后再进入下一步。

### 5. 插件与技能准备

根据功能涉及的技术栈，在每个环节开始前，检查并加载所需插件和技能：

- **通用**：`context7-plugin` — 查阅技术栈最新文档和 API，贯穿开发全周期
- **前端项目必选**：`frontend-design` — Web 页面设计；`ui-ux-pro-max` — 企业级 UI/UX 设计标准（需要时）
- **React 技术栈**：按需加载 `vercel-react-best-practices`（性能优化）、`vercel-composition-patterns`（组件组合模式）、`vercel-react-native-skills`（React Native 开发）
- **UI 组件库**：按需加载 `antd`（Ant Design 组件使用）、`ant-design`（Ant Design 架构决策与主题定制）、`shadcn`（shadcn/ui 组件管理）

### 6. 环境隔离

> 如果项目使用 Git 且功能涉及多文件变更，启用 `superpowers:using-git-worktrees` 创建隔离开发环境。

如果变更范围较小（单文件修改），可跳过此步骤直接在当前分支工作。

### 7. 代码实现

> 启用 `superpowers:executing-plans`，根据实现计划执行代码实现。

实现过程中按需使用：

- `context7-plugin` — 查阅框架/库的最新文档和 API
- `code-simplifier` — 实现完成后简化复杂代码

### 8. 代码审查（并发3次）

> 启用 `superpowers:requesting-code-review`，派发 3 个并发代码审查 subagent。

前端项目审查时加载 `web-design-guidelines` — 基于 Web Interface Guidelines 进行 UI/UX 合规审查。

所有 agent 审查完成后，启用 `superpowers:receiving-code-review` 技能合并去重反馈并修复问题。

> **半自动暂停点**：如果为半自动模式，向用户展示代码审查结果摘要和已修复的问题，等待用户确认后再进入下一步。

### 9. 完成验证

> 启用 `superpowers:verification-before-completion`，在声称完成前必须运行验证命令并获得通过证据。

前端项目验证时按需使用：

- `chrome-devtools-mcp` — Web 前端功能调试（**有前端时必选**）
- `playwright` — 执行自动化测试用例
- `agent-browser` — 非测试/调试场景下的页面自动化操作

### 10. 收尾

> 如果使用了 worktree 隔离开发，启用 `superpowers:finishing-a-development-branch` 处理分支收尾。

如需更新项目的 CLAUDE.md，加载 `claude-md-management` 进行编辑管理。
