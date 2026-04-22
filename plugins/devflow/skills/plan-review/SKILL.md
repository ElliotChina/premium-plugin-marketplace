---
name: plan-review
argument-hint: "[plan 文件路径] [并发数]"
description: >
  This skill should be used when the user runs "/devflow:plan-review" to review an implementation plan.
  Dispatches review agents (default 1), then merges deduplicated feedback and applies fixes.
  Covers completeness, spec alignment, task decomposition, and buildability checks.
---

# Plan Review - 计划审查

对实现计划进行并发多 agent 审查，自动合并去重反馈并修复问题。

## 触发方式

用户执行 `/devflow:plan-review` 命令时激活。参数格式：`[plan 文件路径] [并发数]`。

- **plan 文件路径**（必填）：实现计划文档的文件路径
- **并发数**（可选，默认 1）：同时派发的审查 agent 数量。多个 agent 可提供更广泛的覆盖，但会消耗更多资源

如果用户未明确指定并发数，使用默认值 1。如果并发数为 1，跳过合并去重步骤，直接进入修复。

## 前置条件

- 实现计划已写完并保存到磁盘
- Spec 文档存在且可引用（用于交叉验证）

## 工作流程

### 1. 派发审查

启用 `devflow:requesting-plan-review` 技能，按指定并发数派发 `devflow:plan-reviewer` subagent。

替换模板占位符：
- `{PLAN_FILE_PATH}` — 实现计划文档路径
- `{SPEC_FILE_PATH}` — Spec 文档路径（用于交叉引用）

### 2. 合并反馈（并发数 > 1 时）

**所有 agent 完成后**，启用 `devflow:receiving-plan-review` 技能处理反馈：

1. **合并去重** — 收集所有问题，识别共识（2+ agent 标记同一问题）
2. **验证** — 将每个问题与 spec 和实际计划内容交叉比对
3. **评估** — 区分真实缺陷、误解、过度工程建议和误报
4. **排序** — 共识问题优先，然后 Critical → Important → Minor
5. **修复** — 直接修改 plan 文件，按类别逐项修复

**并发数 = 1 时**，直接根据单个 agent 的反馈修复，跳过合并去重。

修复优先级、验证标准和禁止行为由 `receiving-plan-review` 技能定义，遵循其规则执行。

## 输出

向用户展示审查结果摘要：
- 发现的问题数量（按严重程度分类）
- 已修复的问题
- 被驳回的建议及理由
- 最终评估状态
