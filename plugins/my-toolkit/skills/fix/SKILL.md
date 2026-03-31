---
name: fix
user-invocable: true
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

### 1. 信息收集（根因调查）

> **superpowers 技能**：启用 `systematic-debugging`，遵循四阶段调试流程，禁止跳过根因调查直接修复。

根据用户提供的信息，收集必要的上下文：

- 阅读错误信息，复现问题
- 检查最近的代码变更（通过 git log / git diff 查看）
- 在组件边界收集证据，追踪数据流
- 使用 Grep 搜索相关关键词和错误信息
- 使用 LSP 工具追踪代码调用链（go-to-definition、find-references）
- 使用 `context7-plugin` 查阅框架/库文档，确认 API 用法和预期行为

**铁律**：不得在没有根因证据的情况下提出修复方案。

### 2. 模式分析

在根因调查的基础上进行模式分析：

- 寻找同类场景中正常工作的例子
- 对比正常与异常路径的差异
- 识别问题的共性模式

### 3. 假设验证

形成单一假设并最小化验证：

- 提出一个明确的根因假设
- 用最小操作验证假设是否成立
- 如果假设不成立，回到步骤 1 重新收集证据

确认问题根因后，向用户说明：

- 问题的根本原因
- 为什么会出现这个问题
- 影响范围

### 4. 插件与技能准备

根据问题涉及的技术栈，在每个环节开始前，检查并加载所需插件和技能：

- **通用**：`context7-plugin` — 查阅技术栈最新文档和 API，贯穿修复全周期
- **前端调试**：`chrome-devtools-mcp` — Web 前端功能调试（**前端问题时必选**）
- **UI 组件库**：按需加载 `antd`（Ant Design 组件调试）、`ant-design`（Ant Design 架构决策）、`shadcn`（shadcn/ui 组件调试）
- **React 技术栈**：按需加载 `vercel-react-best-practices`（性能问题排查）、`vercel-composition-patterns`（组件接口问题）

### 5. 环境隔离

> **superpowers 技能**：如果项目使用 Git 且修复涉及多文件变更，启用 `using-git-worktrees` 创建隔离开发环境。

- 检查是否已有 `.worktrees/` 或 `worktrees/` 目录
- 创建隔离的 worktree 和修复分支
- 验证测试基线通过

如果变更范围较小（单文件修改），可跳过此步骤直接在当前分支工作。

### 6. 实施修复

> **superpowers 技能**：启用 `test-driven-development`，先编写失败测试用例再实施修复。

提出修复方案，说明修复思路后与用户确认。修复时遵循：

1. 先编写一个能复现 bug 的失败测试用例
2. 运行测试确认失败原因正确
3. 实施最小修复使测试通过
4. 运行全部测试确认无回归

根据修复复杂度选择执行方式：
- **多文件修复**：启用 `subagent-driven-development`，逐任务派发子 agent 执行
- **独立并行修复**：启用 `dispatching-parallel-agents`，将互不依赖的修复并行派发
- **简单修复**：直接执行，无需子 agent

实施过程中遵循：

- 先读后写：修改前充分理解现有代码结构
- 最小改动：只修复问题本身，不做无关的重构或优化
- 向后兼容：不破坏现有功能
- 如果连续 3 次修复尝试失败，考虑质疑架构设计

实施过程中按需使用：

- `context7-plugin` — 查阅框架/库的最新文档和 API，确认修复方案的正确性
- `code-simplifier` — 修复完成后简化因修复引入的复杂代码

### 7. 代码审查

> **superpowers 技能**：启用 `requesting-code-review`，在修复完成后派发代码审查子 agent。

- 获取 base 和 head 的 git SHA
- 同时派发 3 个代码审查 agent，每个 agent 仅输出审查发现的问题，不做修复

前端项目审查时加载 `web-design-guidelines` — 基于 Web Interface Guidelines 进行 UI/UX 合规审查。

3 个 agent 全部完成后，合并审查结果：

- **共识检测**：多个 agent 同时发现的问题 → 高置信度优先处理；仅 1 个 agent 发现的 → 验证后再处理
- **去重**：相同根因的不同表述合并为一个；同一文件/函数的重叠问题合并为单个修复
- **问题类型处理**：
  - 安全漏洞（XSS、注入等）和功能缺陷 → 立即修复
  - 性能瓶颈或资源泄漏 → 评估影响后修复
  - 代码异味、重复代码、过度复杂逻辑 → 重构修复
  - 代码风格和命名不一致 → 对齐项目规范
  - 超出需求范围的变更 → 跳过（回归到需求边界内）
  - 审查 agent 误解上下文的误报 → 跳过并附理由
- **修复顺序**：共识问题优先 → Critical → Important → Minor，每类问题修复后运行验证

如有无法自动解决的矛盾，呈现给用户决策。

> **superpowers 技能**：所有 agent 全部审查完成后，启用 `receiving-code-review`，在实施修改前先理解、验证和评估每条反馈。

- 先完整阅读反馈，用自己的话复述需求
- 验证反馈是否与代码库实际情况一致
- 对不明确或有疑问的反馈先澄清，再实施
- 逐条处理 Critical 和 Important 问题，每条处理后运行验证

简单修复（单文件、逻辑清晰）可跳过代码审查。

### 8. 完成验证

> **superpowers 技能**：启用 `verification-before-completion`，在声称修复完成前必须运行验证命令并获得通过证据。

- 运行项目的 lint / build / test 命令
- 读取完整输出，确认结果与声明一致
- 验证修复后问题不再复现

**铁律**：未在本轮运行验证命令，不得声称修复完成。

前端项目验证时按需使用：

- `chrome-devtools-mcp` — Web 前端功能调试（**前端问题时必选**）
- `playwright` — 执行自动化测试用例
- `agent-browser` — 非测试/调试场景下的页面自动化操作

### 9. 收尾

> **superpowers 技能**：如果使用了 worktree 隔离开发，启用 `finishing-a-development-branch` 处理分支收尾。

简要说明：
- 问题根因
- 修复方式
- 修改了哪些文件
- 是否有需要注意的后续事项

根据用户选择执行合并、创建 PR 或保留分支。

如需更新项目的 CLAUDE.md，加载 `claude-md-management` 进行编辑管理。

## 注意事项

- 不要通过简化或删减现有代码来规避问题
- 如果无法定位根因，如实告知用户，不猜测
- 修复前先读取和理解相关代码，不盲目修改
- 遵循用户 CLAUDE.md 中的原则：遇到无法解决的问题时，绝不通过删减代码来规避
- 禁止跳过根因调查直接修复（systematic-debugging 铁律）
