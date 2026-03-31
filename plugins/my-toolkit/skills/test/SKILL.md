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

## 工作流程

### 1. 理解测试目标

分析用户提供的测试需求：

- 需要测试的功能/模块
- 测试范围（单元测试、集成测试、E2E）
- 项目现有的测试框架和规范

先读取相关源代码和现有测试用例，了解项目测试风格。

**插件与技能准备**：根据测试范围和技术栈，检查并加载所需插件和技能：

- **通用**：`context7-plugin` — 查阅测试框架文档和 API；`superpowers` — 完成验证方法论（推荐启用）
- **E2E 测试**：`playwright`（MCP 浏览器自动化）或 `playwright-cli`（命令行工具）
- **前端测试**：`chrome-devtools-mcp` — 前端功能测试调试（**前端测试时必选**）
- **React 组件测试**：按需加载 `vercel-react-best-practices`
- **前端 Web 应用测试**：按需加载 `webapp-testing`

### 2. 测试方案设计

确定测试策略：

- 识别核心测试路径（happy path）
- 识别边界条件和异常情况
- 确定测试文件位置和命名
- 选择合适的测试工具和辅助函数

使用 `context7-plugin` 查阅测试框架的最佳实践和 API，确保方案符合框架规范。

### 3. 用例实现

编写测试用例时遵循：

- 覆盖核心需求和关键路径，避免冗余用例
- 遵循项目现有的测试风格和规范
- 测试描述清晰，体现测试意图
- 使用项目已有的测试工具和 fixture

实现过程中按需使用：

- `context7-plugin` — 查阅测试框架的断言 API、mock 工具用法
- `chrome-devtools-mcp` — 前端测试调试，定位测试失败原因

### 4. 运行和验证

> 启用 `superpowers:verification-before-completion`，在声称测试完成前必须运行全部验证命令。

- 运行全部测试用例，读取完整输出确认通过
- 如有失败，分析原因并修复（非猜测性修复）
- 检查测试覆盖率（如果项目有要求）

**铁律**：未在本轮运行测试命令，不得声称测试完成。

E2E 测试验证时按需使用：

- `playwright` / `playwright-cli` — 执行浏览器自动化测试
- `agent-browser` — 非测试/调试场景下的页面自动化操作

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
