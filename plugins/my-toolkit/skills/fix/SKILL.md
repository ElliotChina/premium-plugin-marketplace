---
name: fix
argument-hint: "[问题描述]"
description: >
  This skill should be used when the user runs "/my-toolkit:fix" to diagnose and fix issues.
  Covers problem diagnosis, root cause analysis, bug fixing, and feature debugging scenarios.
---

# Fix - 问题诊断修复 & 功能调试

系统化的问题定位和修复工作流，覆盖 bug 修复和功能调试。

## 触发方式

用户执行 `/my-toolkit:fix` 命令时激活。传入问题描述或错误信息作为参数。

## 工作流程

### 1. 插件与技能准备

根据问题涉及的技术栈，在每个环节开始前，检查并加载所需插件和技能：

- **通用**：`context7-plugin` — 查阅技术栈最新文档和 API，贯穿修复全周期
- **前端调试**：`chrome-devtools-mcp` — Web 前端功能调试（**前端问题时必选**）
- **UI 组件库**：按需加载 `antd`（Ant Design 组件调试）、`ant-design`（Ant Design 架构决策）、`shadcn`（shadcn/ui 组件调试）
- **React 技术栈**：按需加载 `vercel-react-best-practices`（性能问题排查）、`vercel-composition-patterns`（组件接口问题）

### 2. 环境隔离

> 如果项目使用 Git 且修复涉及多文件变更，启用 `superpowers:using-git-worktrees` 创建隔离开发环境。

如果变更范围较小（单文件修改），可跳过此步骤直接在当前分支工作。

### 3. 根因调查并修复

> 启用 `superpowers:systematic-debugging`，遵循四阶段调试流程（根因调查 → 模式分析 → 假设验证 → 实施），禁止跳过根因调查直接修复。

实施过程中按需使用：

- `context7-plugin` — 查阅框架/库的最新文档和 API
- `code-simplifier` — 修复完成后简化因修复引入的复杂代码

### 4. 代码审查（并发3次）

> 启用 `superpowers:requesting-code-review`，派发 3 个并发代码审查 subagent。

前端项目审查时加载 `web-design-guidelines` — 基于 Web Interface Guidelines 进行 UI/UX 合规审查。

所有 agent 审查完成后，启用 `superpowers:receiving-code-review` 技能合并去重反馈并修复问题。

简单修复（单文件、逻辑清晰）可跳过代码审查。

### 5. 完成验证

> 启用 `superpowers:verification-before-completion`，在声称修复完成前必须运行验证命令并获得通过证据。

前端项目验证时按需使用：

- `chrome-devtools-mcp` — Web 前端功能调试（**前端问题时必选**）
- `playwright` — 执行自动化测试用例
- `agent-browser` — 非测试/调试场景下的页面自动化操作

### 6. 收尾

> 如果使用了 worktree 隔离开发，启用 `superpowers:finishing-a-development-branch` 处理分支收尾。

如需更新项目的 CLAUDE.md，加载 `claude-md-management` 进行编辑管理。
