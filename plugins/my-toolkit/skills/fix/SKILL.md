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

**插件与技能准备**：根据问题涉及的技术栈，检查并加载所需插件和技能：

- **通用**：`context7-plugin` — 查阅技术栈最新文档和 API，贯穿修复全周期
- **前端调试**：`chrome-devtools-mcp` — Web 前端功能调试（**前端问题时必选**）
- **UI 组件库**：按需加载 `antd`（Ant Design 组件调试）、`ant-design`（Ant Design 架构决策）、`shadcn`（shadcn/ui 组件调试）
- **React 技术栈**：按需加载 `vercel-react-best-practices`（性能问题排查）、`vercel-composition-patterns`（组件接口问题）

### 4. 实施修复

> **superpowers 技能**：启用 `test-driven-development`，先编写失败测试用例再实施修复。

提出修复方案，说明修复思路后与用户确认。修复时遵循：

1. 先编写一个能复现 bug 的失败测试用例
2. 运行测试确认失败原因正确
3. 实施最小修复使测试通过
4. 运行全部测试确认无回归
- 最小改动原则，只修复问题本身
- 不做无关的重构或优化
- 确保修复不会引入新问题
- 如果连续 3 次修复尝试失败，考虑质疑架构设计

实施过程中按需使用：

- `context7-plugin` — 查阅框架/库的最新文档和 API，确认修复方案的正确性
- `code-simplifier` — 修复完成后简化因修复引入的复杂代码

### 5. 代码审查（按需）

> **superpowers 技能**：如果修复涉及 3 个以上文件或逻辑复杂，启用 `requesting-code-review` 派发代码审查子 agent。

- 获取 base 和 head 的 git SHA
- 派发代码审查子 agent 审查修复变更

> **superpowers 技能**：收到审查反馈后，启用 `receiving-code-review`，在实施修改前先理解、验证和评估每条反馈。

- 逐条处理 Critical 和 Important 反馈，每条处理后运行验证

简单修复（单文件、逻辑清晰）可跳过此步骤。

前端项目审查时加载 `web-design-guidelines` — 基于 Web Interface Guidelines 进行 UI/UX 合规审查。

### 6. 验证修复

> **superpowers 技能**：启用 `verification-before-completion`，在声称修复完成前必须运行验证命令并获得通过证据。

- 运行相关测试（如有），读取完整输出确认通过
- 运行 build / lint 命令检查
- 验证修复后问题不再复现

**铁律**：未在本轮运行验证命令，不得声称修复完成。

前端项目验证时按需使用：

- `chrome-devtools-mcp` — Web 前端功能调试（**前端问题时必选**）
- `playwright` — 执行自动化测试用例
- `agent-browser` — 非测试/调试场景下的页面自动化操作

### 7. 总结

简要说明：
- 问题根因
- 修复方式
- 修改了哪些文件

如需更新项目的 CLAUDE.md，加载 `claude-md-management` 进行编辑管理。

## 注意事项

- 不要通过简化或删减现有代码来规避问题
- 如果无法定位根因，如实告知用户，不猜测
- 修复前先读取和理解相关代码，不盲目修改
- 遵循用户 CLAUDE.md 中的原则：遇到无法解决的问题时，绝不通过删减代码来规避
- 禁止跳过根因调查直接修复（systematic-debugging 铁律）
