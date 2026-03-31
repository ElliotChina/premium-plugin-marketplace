---
name: requesting-spec-review
user-invocable: true
description: >
  Use after writing a spec document (design doc) to dispatch review agents.
  Verifies the spec is complete, consistent, and ready for implementation planning.
  Dispatch after the spec document is written and saved.
---

# Requesting Spec Review

在 spec 文档编写完成并保存后，派发 spec-reviewer agent 捕捉文档缺陷，防止缺陷向下游传递到实现计划和代码。每个审查 agent 只接收 spec 文件路径和项目上下文，不共享会话历史。

**核心原则：** 错误的 spec = 错误的计划 = 错误的代码。从源头修复。

## 触发时机

**必须触发：**
- spec 文档编写完成并保存后
- 调用实现计划编写之前

**可选触发：**
- 对现有 spec 进行重大设计决策变更后

## 如何派发

**1. 派发 spec-reviewer agent：**

使用 Agent 工具，填充 `spec-reviewer.md` 模板。派发前必须将模板中所有 `{占位符}` 替换为实际值：

- `{SPEC_FILE_PATH}` — 已保存的 spec 文档路径
- `{ORIGINAL_REQUEST}` — 用户原始的功能描述
- `{PROJECT_CONTEXT}` — 项目关键架构信息（框架、约定、约束）

**2. 处理反馈：**
- 直接修复 spec 中的缺口和矛盾
- 通过选择一种解释并明确化来解决歧义
- 移除未请求的功能（YAGNI 违规）
- 将修改呈现给用户确认

## 与 new-feature 工作流的集成

在 new-feature 技能中，spec 编写完成后同时派发 3 个 agent：
- 每个 agent 独立审查所有维度（完整性、一致性、清晰度、范围、YAGNI）
- 每个 agent 读取实际的 spec 文件，仅输出发现的问题
- 所有 agent 完成后合并和去重结果
- 多个 agent 同时发现的问题视为高置信度
- 在继续之前将统一修复应用到 spec
