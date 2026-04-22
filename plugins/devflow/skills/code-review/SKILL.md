---
name: code-review
argument-hint: "[代码路径 / PR 编号 / 变更描述] [并发数]"
description: >
  This skill should be used when the user runs "/devflow:code-review" to review code changes.
  Dispatches review agents (default 1), merges deduplicated feedback, and applies fixes.
  Covers security, correctness, performance, and maintainability.
---

# Code Review - 代码审查

对代码变更进行并发多 agent 审查，自动合并去重反馈并修复问题。

## 触发方式

用户执行 `/devflow:code-review` 命令时激活。参数格式：`[代码路径 / PR 编号 / 变更描述] [并发数]`。

- **审查目标**（必填）：代码路径、PR 编号或变更描述
- **并发数**（可选，默认 1）：同时派发的审查 agent 数量。多个 agent 可提供更广泛的覆盖，但会消耗更多资源

如果用户未明确指定并发数，使用默认值 1。如果并发数为 1，跳过合并去重步骤，直接进入修复。

## 前置条件

- 代码变更已提交（需要 git SHA 进行 diff 比较）
- 如涉及前端项目，预先加载 `web-design-guidelines`

## 工作流程

### 1. 确定 Git 范围

根据输入确定审查范围：

**指定代码路径：**
```bash
# 使用最近的变更作为范围
BASE_SHA=$(git log --oneline -10 | tail -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)
```

**PR 编号：**
```bash
# 获取 PR 的 base 和 head
BASE_SHA=$(gh pr view {PR_NUMBER} --json baseRefOid -q .baseRefOid)
HEAD_SHA=$(gh pr view {PR_NUMBER} --json headRefOid -q .headRefOid)
```

**如无法自动确定范围，使用 `AskUserQuestion` 询问用户指定 base commit。**

确定范围后，验证 diff 是否合理：
```bash
# 检查变更文件数量和行数，确认范围不过大或为空
git diff --stat {BASE_SHA}..{HEAD_SHA}
```
如果变更范围为空或异常大（如超过 50 个文件），重新确认范围。

### 2. 派发审查

启用 `superpowers:requesting-code-review` 技能，按指定并发数派发 `superpowers:code-reviewer` subagent。

替换模板占位符：
- `{WHAT_WAS_IMPLEMENTED}` — 变更内容描述
- `{PLAN_OR_REQUIREMENTS}` — 需求或计划来源
- `{BASE_SHA}` — 起始 commit
- `{HEAD_SHA}` — 结束 commit
- `{DESCRIPTION}` — 变更摘要

### 3. 合并反馈（并发数 > 1 时）

**所有 agent 完成后**，执行合并去重：

1. **合并去重** — 收集所有问题，识别共识（2+ agent 标记同一问题）
2. **验证** — 将每个问题与代码实际情况比对
3. **评估** — 区分真实问题、误解、YAGNI 建议和误报
4. **排序** — 共识问题优先，然后 Critical → Important → Minor

启用 `superpowers:receiving-code-review` 技能处理反馈，遵循其技术验证原则：
- 验证后再实施，不要盲目执行
- 不确定的先问再做
- 技术正确性优先

**并发数 = 1 时**，直接根据单个 agent 的反馈修复，跳过合并去重。

修复顺序、YAGNI 检查规则和禁止行为由 `receiving-code-review` 技能定义，遵循其规则执行。

## 输出

向用户展示审查结果摘要：
- 发现的问题数量（按严重程度分类）
- 已修复的问题及修复方式
- 被驳回的建议及理由
- 最终评估状态
