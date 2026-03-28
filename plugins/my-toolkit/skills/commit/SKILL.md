---
name: commit
user-invocable: true
argument-hint: "[commit message]"
description: >
  This skill should be used when the user runs "/my-toolkit:commit" to commit code changes.
  Provides a structured git commit workflow with conventional commit messages.
---

# Commit - 代码提交

规范的代码提交流程，自动生成结构化的 commit message。

## 触发方式

用户执行 `/my-toolkit:commit` 命令时激活。可选传入 commit message 作为参数。

## 插件设置

开始前，根据提交涉及的内容检查并调整插件状态。

### 判断所需插件

根据提交内容和场景，判断哪些插件需要启用：

- **commit-commands** — 代码提交辅助
- **superpowers** — 提交前验证方法论（推荐启用）

通常不需要额外启用插件。

### 检查当前状态

依次读取以下配置文件，综合判断插件的最终启用/禁用状态：

1. **全局配置** `~/.claude/settings.json` — 用户级别的插件默认状态
2. **项目配置** `.claude/settings.json` — 当前项目级别的覆盖状态

优先级：项目配置 > 全局配置。合并两层配置后，得出各插件的最终生效状态，对比上述需求判断是否需要调整。

### 调整插件状态

若当前状态不符合需求，使用 AskUserQuestion 工具询问用户：

```
根据当前提交需求，建议以下插件调整：
- 启用：[插件列表及原因]
- 禁用：[插件列表及原因]
是否确认调整？
```

用户确认后，修改项目 `.claude/settings.json` 中对应插件的启用/禁用状态。

## 技能加载

根据项目配置加载相关技能：

- **verification-before-completion**（superpowers）— 提交前强制验证（推荐加载）

直接进入提交流程。

## 工作流程

### 1. 检查工作区状态

运行 `git status` 和 `git diff` 了解当前变更：

- 哪些文件被修改/新增/删除
- 具体改动了什么内容
- 是否有未暂存的变更

### 2. 分析变更内容

理解变更的目的和范围：

- 功能新增（feat）
- 问题修复（fix）
- 代码重构（refactor）
- 文档更新（docs）
- 测试相关（test）
- 性能优化（perf）
- 构建/工具（chore）

### 3. 生成 Commit Message

根据变更内容生成规范的 commit message：

格式：
```
type(scope): 简要描述

详细说明（如需要）
```

类型关键词：
- `feat`: 新功能
- `fix`: 修复 bug
- `refactor`: 重构（不改变功能）
- `docs`: 文档变更
- `test`: 测试相关
- `perf`: 性能优化
- `chore`: 构建/工具变更

### 4. 暂存和提交

> **superpowers 技能**：启用 `verification-before-completion`，在提交前确认所有验证已通过。

- 确认测试和 lint 命令已通过（如有）
- 将相关文件添加到暂存区
- 使用生成的 commit message 提交
- 运行 git status 确认提交成功

### 5. 处理 Hook 失败

如果 pre-commit hook 失败：
- 分析失败原因
- 修复问题（不是绕过 hook）
- 重新提交（创建新的 commit，不使用 --amend）

## 注意事项

- 只在用户明确要求时才执行 commit 操作
- 不要使用 --no-verify 跳过 hook
- 不要使用 --amend 修改已有 commit
- 不要 commit 可能包含敏感信息的文件（.env、credentials 等）
- 优先按文件名暂存，避免 git add -A
