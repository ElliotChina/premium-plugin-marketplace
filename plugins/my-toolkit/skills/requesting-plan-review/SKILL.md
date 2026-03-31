---
name: requesting-plan-review
description: >
  Use after writing an implementation plan to dispatch review agents.
  Verifies the plan is complete, matches the spec, and has proper task decomposition.
  Dispatch after the plan document is written and saved.
---

# Requesting Plan Review

在实现计划编写完成并保存后，派发 plan-reviewer agent 捕捉任务缺口和排序问题，避免在编码阶段浪费时间。每个审查 agent 只接收计划文件路径和 spec 参考，不共享会话历史。

**核心原则：** 糟糕的计划浪费的时间远多于一次好的审查节省的时间。

## 触发时机

**必须触发：**
- 实现计划编写完成并保存后
- 开始代码实现之前

**可选触发：**
- 对现有计划进行重大变更后
- 计划复杂度较高时（5+ 个有相互依赖的任务）

## 如何派发

**1. 派发 plan-reviewer agent：**

使用 Agent 工具，填充 `plan-reviewer.md` 模板。派发前必须将模板中所有 `{占位符}` 替换为实际值：

- `{PLAN_FILE_PATH}` — 已保存的计划文档路径
- `{SPEC_FILE_PATH}` — spec 文档路径（用于交叉验证）

**2. 处理反馈：**
- 立即修复缺失的任务
- 在开始实现前解决依赖问题
- 移除占位符（TBD、TODO、"添加适当的错误处理"等）
- 对审查 agent 的过度工程建议予以拒绝

## 与 new-feature 工作流的集成

在 new-feature 技能中，计划编写完成后同时派发 3 个 agent：
- 每个 agent 独立审查所有维度（完整性、spec 对齐、任务分解、可执行性）
- 每个 agent 读取实际的计划文件，仅输出发现的问题
- 所有 agent 完成后合并和去重结果
- 多个 agent 同时发现的问题视为高置信度
- 在继续之前将统一修复应用到计划
