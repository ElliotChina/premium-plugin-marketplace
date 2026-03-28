---
name: test
user-invocable: true
argument-hint: "[测试目标]"
description: >
  This skill should be used when the user runs "/my-toolkit:test" to write and run tests.
  Provides guidance for feature testing, covering test design, implementation, and execution.
---

# Test - 功能测试

引导式的功能测试开发，从测试设计到用例实现。

## 触发方式

用户执行 `/my-toolkit:test` 命令时激活。传入要测试的功能或模块名称作为参数。

## 插件设置

开始前，根据测试类型检查并调整插件状态。

### 判断所需插件

根据测试范围和方式，判断哪些插件需要启用：

- **playwright** — E2E 测试 MCP 服务器（浏览器自动化测试）
- **playwright-cli** — E2E 测试命令行工具
- **chrome-devtools-mcp** — 前端功能测试调试
- **context7-plugin** — 查阅测试框架文档
- **superpowers** — 完成验证方法论（推荐启用）

非相关插件建议暂时禁用，减少干扰。

### 检查当前状态

依次读取以下配置文件，综合判断插件的最终启用/禁用状态：

1. **全局配置** `~/.claude/settings.json` — 用户级别的插件默认状态
2. **项目配置** `.claude/settings.json` — 当前项目级别的覆盖状态

优先级：项目配置 > 全局配置。合并两层配置后，得出各插件的最终生效状态，对比上述需求判断是否需要调整。

### 调整插件状态

若当前状态不符合需求，使用 AskUserQuestion 工具询问用户：

```
根据当前测试需求，建议以下插件调整：
- 启用：[插件列表及原因]
- 禁用：[插件列表及原因]
是否确认调整？
```

用户确认后，修改项目 `.claude/settings.json` 中对应插件的启用/禁用状态。

## 技能加载

根据测试场景加载相关技能：

- **vercel-react-best-practices** — React 组件测试
- **webapp-testing** — 前端 Web 应用测试
- **verification-before-completion**（superpowers）— 完成前强制验证

与用户确认测试范围后，主动加载对应技能。

## 工作流程

### 1. 理解测试目标

分析用户提供的测试需求：

- 需要测试的功能/模块
- 测试范围（单元测试、集成测试、E2E）
- 项目现有的测试框架和规范

先读取相关源代码和现有测试用例，了解项目测试风格。

### 2. 测试方案设计

确定测试策略：

- 识别核心测试路径（happy path）
- 识别边界条件和异常情况
- 确定测试文件位置和命名
- 选择合适的测试工具和辅助函数

### 3. 用例实现

编写测试用例时遵循：

- 覆盖核心需求和关键路径，避免冗余用例
- 遵循项目现有的测试风格和规范
- 测试描述清晰，体现测试意图
- 使用项目已有的测试工具和 fixture

### 4. 运行和验证

> **superpowers 技能**：启用 `verification-before-completion`，在声称测试完成前必须运行全部验证命令。

- 运行全部测试用例，读取完整输出确认通过
- 如有失败，分析原因并修复（非猜测性修复）
- 检查测试覆盖率（如果项目有要求）

**铁律**：未在本轮运行测试命令，不得声称测试完成。

### 5. 总结

简要说明：
- 编写了哪些测试用例
- 覆盖了哪些场景
- 测试运行结果

## 注意事项

- 先了解项目现有测试框架和风格再动手
- 只创建必要的用例，不为凑覆盖率写冗余测试
- 测试用例与代码行为不一致时，先判断根因再处理
- 遵循用户 CLAUDE.md 中的测试原则
