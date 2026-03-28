---
name: new-feature
user-invocable: true
argument-hint: "[功能描述]"
description: >
  This skill should be used when the user runs "/my-toolkit:new-feature" to develop a new feature.
  Provides a structured workflow from requirement analysis, design, implementation to verification.
---

# New Feature - 新功能开发

结构化的新功能开发工作流，从需求到交付全流程引导。

## 触发方式

用户执行 `/my-toolkit:new-feature` 命令时激活。传入功能描述作为参数。

## 插件设置

开始前，根据功能涉及的领域检查并调整插件状态。

### 判断所需插件

根据功能涉及的技术栈和模块，判断哪些插件需要启用：

- **context7-plugin** — 查阅框架和库的最新文档（推荐启用）
- **frontend-design** — 涉及前端页面开发时启用
- **feature-dev** — 完整的功能开发工作流和架构审查 agent（推荐启用）
- **code-simplifier** — 功能开发完成后简化代码（按需启用）
- **chrome-devtools-mcp** — 前端功能调试时启用
- **antd** / **shadcn** — 涉及对应 UI 组件库时启用
- **superpowers** — 功能开发方法论和计划编写（推荐启用）

非相关插件建议暂时禁用，减少干扰。

### 检查当前状态

依次读取以下配置文件，综合判断插件的最终启用/禁用状态：

1. **全局配置** `~/.claude/settings.json` — 用户级别的插件默认状态
2. **项目配置** `.claude/settings.json` — 当前项目级别的覆盖状态

优先级：项目配置 > 全局配置。合并两层配置后，得出各插件的最终生效状态，对比上述需求判断是否需要调整。

### 调整插件状态

若当前状态不符合需求，使用 AskUserQuestion 工具询问用户：

```
根据当前功能开发，建议以下插件调整：
- 启用：[插件列表及原因]
- 禁用：[插件列表及原因]
是否确认调整？
```

用户确认后，修改项目 `.claude/settings.json` 中对应插件的启用/禁用状态。

## 技能加载

根据功能涉及的技术栈加载相关技能：

- **vercel-react-best-practices** / **vercel-composition-patterns** — React 相关功能
- **vercel-react-native-skills** — React Native 相关功能
- **antd** / **ant-design** — Ant Design 相关功能
- **brainstorming**（superpowers）— 功能开发前的创意探索和需求澄清
- **writing-plans**（superpowers）— 多步骤任务的计划编写
- **test-driven-development**（superpowers）— TDD 工作流（用户确认启用后加载）
- **subagent-driven-development**（superpowers）— 逐任务执行实现计划
- **dispatching-parallel-agents**（superpowers）— 并行分发独立任务
- **using-git-worktrees**（superpowers）— 创建隔离开发环境
- **requesting-code-review**（superpowers）— 代码审查请求流程
- **receiving-code-review**（superpowers）— 审查反馈处理流程
- **verification-before-completion**（superpowers）— 完成前强制验证

与用户确认技术范围后，主动加载对应技能。

## 工作流程

### 1. 需求探索

> **superpowers 技能**：启用 `brainstorming`，在编码前强制进行需求澄清和设计探索。

分析用户提供的功能描述，执行以下步骤：

- 探索项目上下文，理解现有架构
- 逐个提出澄清问题，确认功能目标、核心价值、边界条件和约束
- 提出 2-3 个实现方案并分析各自权衡
- 逐节呈现设计方案，每节获得用户认可后再继续

如果功能简单明确，可简化探索过程，但仍需确认关键设计决策。

### 2. 编写实现计划

> **superpowers 技能**：启用 `writing-plans`，将确认的设计转化为可执行的实现计划。

在动手编码前，制定详细实现计划：

- 梳理文件结构，识别需要修改/新增的文件
- 将工作拆分为 2-5 分钟的小任务（写失败测试 → 运行 → 最小实现 → 运行测试 → 提交）
- 确定数据结构和接口设计
- 评估对现有代码的影响

将计划呈现给用户确认，确认后再进入实现阶段。

### 3. 环境隔离

> **superpowers 技能**：如果项目使用 Git 且功能涉及多文件变更，启用 `using-git-worktrees` 创建隔离开发环境。

- 检查是否已有 `.worktrees/` 或 `worktrees/` 目录
- 创建隔离的 worktree 和功能分支
- 验证测试基线通过

如果变更范围较小（单文件修改），可跳过此步骤直接在当前分支工作。

### 4. 代码实现

> **superpowers 技能**：使用 AskUserQuestion 工具询问用户是否启用 `test-driven-development`（TDD）工作流：
> - **启用 TDD**：对每个实现任务严格遵循 RED（编写失败测试）→ GREEN（最小实现使测试通过）→ REFACTOR（在测试通过前提下清理代码）循环
> - **不启用 TDD**：按常规流程实现，完成后统一编写或运行测试
>
> 根据任务复杂度选择执行方式：
> - **多任务计划**：启用 `subagent-driven-development`，逐任务派发子 agent 执行，每个任务完成后进行规范审查和代码质量审查
> - **独立并行任务**：启用 `dispatching-parallel-agents`，将互不依赖的任务并行派发
> - **简单任务**：直接执行，无需子 agent

实现过程中遵循：

- 先读后写：修改前充分理解现有代码结构
- 最小改动：只添加必要的代码，不过度设计
- 向后兼容：不破坏现有功能
- 遵循项目现有代码风格和规范

### 5. 代码审查

> **superpowers 技能**：启用 `requesting-code-review`，在实现完成后派发代码审查子 agent。

- 获取 base 和 head 的 git SHA
- 派发代码审查子 agent 进行全面审查

> **superpowers 技能**：收到审查反馈后，启用 `receiving-code-review`，在实施修改前先理解、验证和评估每条反馈。

- 先完整阅读反馈，用自己的话复述需求
- 验证反馈是否与代码库实际情况一致
- 对不明确或有疑问的反馈先澄清，再实施
- 逐条处理 Critical 和 Important 问题，每条处理后运行验证

### 6. 完成验证

> **superpowers 技能**：启用 `verification-before-completion`，在声称完成前必须运行验证命令并获得通过证据。

- 运行项目的 lint / build / test 命令
- 读取完整输出，确认结果与声明一致
- 检查边界情况处理

### 7. 收尾

> **superpowers 技能**：如果使用了 worktree 隔离开发，启用 `finishing-a-development-branch` 处理分支收尾。

简要说明：
- 修改了哪些文件
- 实现了什么功能
- 是否有需要注意的后续事项

根据用户选择执行合并、创建 PR 或保留分支。

## 注意事项

- 需求探索阶段必须在设计获得用户认可后才能进入实现
- 修改现有文件前必须先读取理解
- 不添加用户未要求的功能或优化
- 遵循用户 CLAUDE.md 中的开发原则（KISS、YAGNI、DRY、SOLID）
- 实现计划中不允许使用占位符（TODO、TBD、"添加适当错误处理"等）
