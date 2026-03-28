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

## 插件设置

开始前，根据问题类型检查并调整插件状态。

### 判断所需插件

根据问题涉及的技术栈和环境，判断哪些插件需要启用：

- **chrome-devtools-mcp** — 前端页面问题调试（浏览器相关问题启用）
- **context7-plugin** — 查阅框架文档排查问题（推荐启用）
- **superpowers** — 系统化调试方法论（推荐启用）

非相关插件建议暂时禁用，减少干扰。

### 检查当前状态

依次读取以下配置文件，综合判断插件的最终启用/禁用状态：

1. **全局配置** `~/.claude/settings.json` — 用户级别的插件默认状态
2. **项目配置** `.claude/settings.json` — 当前项目级别的覆盖状态

优先级：项目配置 > 全局配置。合并两层配置后，得出各插件的最终生效状态，对比上述需求判断是否需要调整。

### 调整插件状态

若当前状态不符合需求，使用 AskUserQuestion 工具询问用户：

```
根据当前问题排查，建议以下插件调整：
- 启用：[插件列表及原因]
- 禁用：[插件列表及原因]
是否确认调整？
```

用户确认后，修改项目 `.claude/settings.json` 中对应插件的启用/禁用状态。

## 技能加载

根据问题涉及的技术栈加载相关技能：

- **vercel-react-best-practices** — React 相关问题
- **vercel-react-native-skills** — React Native 相关问题
- **antd** / **ant-design** — Ant Design 相关问题
- **systematic-debugging**（superpowers）— 系统化调试流程
- **requesting-code-review**（superpowers）— 复杂修复的代码审查（修复涉及 3+ 文件或逻辑复杂时启用）
- **receiving-code-review**（superpowers）— 审查反馈处理流程（配合代码审查使用）
- **verification-before-completion**（superpowers）— 修复完成后强制验证

根据问题上下文判断后，主动加载对应技能。

## 工作流程

### 1. 信息收集（根因调查）

> **superpowers 技能**：启用 `systematic-debugging`，遵循四阶段调试流程，禁止跳过根因调查直接修复。

根据用户提供的信息，收集必要的上下文：

- 阅读错误信息，复现问题
- 检查最近的代码变更（通过 git log / git diff 查看）
- 在组件边界收集证据，追踪数据流
- 使用 Grep 搜索相关关键词和错误信息
- 使用 LSP 工具追踪代码调用链（go-to-definition、find-references）

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

### 5. 代码审查（按需）

> **superpowers 技能**：如果修复涉及 3 个以上文件或逻辑复杂，启用 `requesting-code-review` 派发代码审查子 agent。

- 获取 base 和 head 的 git SHA
- 派发代码审查子 agent 审查修复变更

> **superpowers 技能**：收到审查反馈后，启用 `receiving-code-review`，在实施修改前先理解、验证和评估每条反馈。

- 逐条处理 Critical 和 Important 反馈，每条处理后运行验证

简单修复（单文件、逻辑清晰）可跳过此步骤。

### 6. 验证修复

> **superpowers 技能**：启用 `verification-before-completion`，在声称修复完成前必须运行验证命令并获得通过证据。

- 运行相关测试（如有），读取完整输出确认通过
- 运行 build / lint 命令检查
- 验证修复后问题不再复现

**铁律**：未在本轮运行验证命令，不得声称修复完成。

### 7. 总结

简要说明：
- 问题根因
- 修复方式
- 修改了哪些文件

## 注意事项

- 不要通过简化或删减现有代码来规避问题
- 如果无法定位根因，如实告知用户，不猜测
- 修复前先读取和理解相关代码，不盲目修改
- 遵循用户 CLAUDE.md 中的原则：遇到无法解决的问题时，绝不通过删减代码来规避
- 禁止跳过根因调查直接修复（systematic-debugging 铁律）
