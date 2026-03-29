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

## 工作流程

### 1. 需求探索

> **superpowers 技能**：启用 `brainstorming`，在编码前强制进行需求澄清和设计探索。

分析用户提供的功能描述，执行以下步骤：

- 探索项目上下文，理解现有架构
- 逐个提出澄清问题，确认功能目标、核心价值、边界条件和约束
- 提出 2-3 个实现方案并分析各自权衡
- 逐节呈现设计方案，每节获得用户认可后再继续

如果功能简单明确，可简化探索过程，但仍需确认关键设计决策。

**自我审查**：完成需求探索后，进行 3 轮全面审查与修复。每轮审查以下所有方面，发现问题立即修复后再进入下一轮：
- **完整性**：功能目标、边界条件、异常场景是否都已覆盖，是否有遗漏的澄清问题
- **可行性**：技术方案是否与现有架构兼容，是否引入不必要的复杂度，约束条件是否已充分考虑
- **一致性**：各设计决策之间是否矛盾，与项目现有规范和用户 CLAUDE.md 是否一致

### 2. 编写实现计划

> **superpowers 技能**：启用 `writing-plans`，将确认的设计转化为可执行的实现计划。

在动手编码前，制定详细实现计划：

- 梳理文件结构，识别需要修改/新增的文件
- 将工作拆分为 2-5 分钟的小任务（写失败测试 → 运行 → 最小实现 → 运行测试 → 提交）
- 确定数据结构和接口设计
- 评估对现有代码的影响

**插件与技能准备**：根据功能涉及的技术栈，检查并加载所需插件和技能：

- **通用**：`context7-plugin` — 查阅技术栈最新文档和 API，贯穿开发全周期
- **前端项目必选**：`frontend-design` — Web 页面设计；`ui-ux-pro-max` — 企业级 UI/UX 设计标准（需要时）
- **React 技术栈**：按需加载 `vercel-react-best-practices`（性能优化）、`vercel-composition-patterns`（组件组合模式）、`vercel-react-native-skills`（React Native 开发）
- **UI 组件库**：按需加载 `antd`（Ant Design 组件使用）、`ant-design`（Ant Design 架构决策与主题定制）、`shadcn`（shadcn/ui 组件管理）

将计划呈现给用户确认，确认后再进入实现阶段。

**自我审查**：完成实现计划后，进行 3 轮全面审查与修复。每轮审查以下所有方面，发现问题立即修复后再进入下一轮：
- **任务完整性**：所有设计点是否都有对应的实现任务，是否有遗漏的文件修改或新增
- **依赖与顺序**：任务拆分是否合理，依赖关系是否正确，是否有可以并行的独立任务被串行化
- **风险与影响**：每个任务对现有代码的影响是否已评估，是否有潜在的破坏性变更未被识别

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

实现过程中按需使用：

- `context7-plugin` — 查阅框架/库的最新文档和 API
- `code-simplifier` — 实现完成后简化复杂代码

### 5. 代码审查

> **superpowers 技能**：启用 `requesting-code-review`，在实现完成后派发代码审查子 agent。

- 获取 base 和 head 的 git SHA
- 派发代码审查子 agent 进行全面审查

> **superpowers 技能**：收到审查反馈后，启用 `receiving-code-review`，在实施修改前先理解、验证和评估每条反馈。

- 先完整阅读反馈，用自己的话复述需求
- 验证反馈是否与代码库实际情况一致
- 对不明确或有疑问的反馈先澄清，再实施
- 逐条处理 Critical 和 Important 问题，每条处理后运行验证

前端项目审查时加载 `web-design-guidelines` — 基于 Web Interface Guidelines 进行 UI/UX 合规审查。

**自我审查**：代码审查完成后，进行 3 轮全面审查与修复。每轮审查以下所有方面，发现问题立即修复后再进入下一轮：
- **质量**：是否还有未处理的代码异味、重复代码、过度复杂的逻辑，错误处理是否充分
- **安全与性能**：是否引入安全隐患（XSS、注入等），是否存在性能瓶颈或资源泄漏
- **规范与一致性**：代码风格是否与项目一致，命名是否清晰，变更范围是否超出需求边界

### 6. 完成验证

> **superpowers 技能**：启用 `verification-before-completion`，在声称完成前必须运行验证命令并获得通过证据。

- 运行项目的 lint / build / test 命令
- 读取完整输出，确认结果与声明一致
- 检查边界情况处理

前端项目验证时按需使用：

- `chrome-devtools-mcp` — Web 前端功能调试（**有前端时必选**）
- `playwright` — 执行自动化测试用例
- `agent-browser` — 非测试/调试场景下的页面自动化操作

### 7. 收尾

> **superpowers 技能**：如果使用了 worktree 隔离开发，启用 `finishing-a-development-branch` 处理分支收尾。

简要说明：
- 修改了哪些文件
- 实现了什么功能
- 是否有需要注意的后续事项

根据用户选择执行合并、创建 PR 或保留分支。

如需更新项目的 CLAUDE.md，加载 `claude-md-management` 进行编辑管理。

## 注意事项

- 需求探索阶段必须在设计获得用户认可后才能进入实现
- 修改现有文件前必须先读取理解
- 不添加用户未要求的功能或优化
- 遵循用户 CLAUDE.md 中的开发原则（KISS、YAGNI、DRY、SOLID）
- 实现计划中不允许使用占位符（TODO、TBD、"添加适当错误处理"等）
