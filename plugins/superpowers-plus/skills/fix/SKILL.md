---
name: fix
argument-hint: "[问题描述]"
description: >
  This skill should be used when the user runs "/superpowers-plus:fix" to diagnose and fix issues.
  Covers problem diagnosis, root cause analysis, bug fixing, and feature debugging scenarios.
---

# Fix - 问题诊断修复 & 功能调试

系统化的问题定位和修复工作流，覆盖 bug 修复和功能调试。

## 触发方式

用户执行 `/superpowers-plus:fix` 命令时激活。传入问题描述或错误信息作为参数。

## 执行模式

技能加载后，**立即**使用 `AskUserQuestion` 询问用户选择执行模式：

**全自动**：执行过程中人不介入，直接从问题诊断运行到修复完成。流程中所有需要用户决策的环节一律采用推荐值，并在执行日志中标注 `[auto] ` 前缀说明选择了什么及理由。**禁止在流程中使用 `AskUserQuestion` 或任何交互式提问**，遇到不确定的问题基于上下文自行判断。

**半自动**：在以下关键节点完成后暂停，等待人工审查确认再继续：
- 根因调查完成后（确认根因正确后再动手修复）

记住用户选择的模式，后续步骤据此决定是否在审查节点后暂停。

## 工作流程

> 执行过程中如发现缺少必要的插件、技能或 MCP 工具，运行 `superpowers-plus:check-env` 检查并安装。

### 1. 环境隔离

> 如果项目使用 Git 且修复涉及多文件变更，启用 `superpowers:using-git-worktrees` 创建隔离开发环境。

如果变更范围较小（单文件修改），可跳过此步骤直接在当前分支工作。

### 2. 根因调查并修复

> 启用 `superpowers:systematic-debugging`，遵循四阶段调试流程（根因调查 → 模式分析 → 假设验证 → 实施），禁止跳过根因调查直接修复。

> **半自动暂停点**：如果为半自动模式，在根因调查完成后向用户展示根因分析结果，等待用户确认后再进入修复实施。

实施过程中按需使用：

- `context7-plugin` — 查阅框架/库的最新文档和 API
- `code-simplifier` — 修复完成后简化因修复引入的复杂代码

### 3. 代码审查（并发3次）

> 启用 `superpowers:requesting-code-review`，派发 3 个并发代码审查 subagent。

前端项目审查时加载 `web-design-guidelines` — 基于 Web Interface Guidelines 进行 UI/UX 合规审查。

所有 agent 审查完成后，启用 `superpowers:receiving-code-review` 技能合并去重反馈并修复问题。

简单修复（单文件、逻辑清晰）可跳过代码审查。

### 4. 完成验证

> 启用 `superpowers:verification-before-completion`，在声称修复完成前必须运行验证命令并获得通过证据。

前端项目验证时按需使用：

- `chrome-devtools-mcp` — Web 前端功能调试（**前端问题时必选**）
- `playwright` — 执行自动化测试用例
- `agent-browser` — 非测试/调试场景下的页面自动化操作

### 5. 收尾

> 如果使用了 worktree 隔离开发，启用 `superpowers:finishing-a-development-branch` 处理分支收尾。

如需更新项目的 CLAUDE.md，加载 `claude-md-management` 进行编辑管理。
