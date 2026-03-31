---
name: receiving-plan-review
user-invocable: true
description: >
  Use when receiving implementation plan review feedback from multiple agents, before applying changes.
  Merge deduplicated results, verify against the spec, then apply unified fixes to the plan.
---

# Receiving Plan Review

多个 agent 的计划审查反馈在应用前需要合并和验证。不要盲目接受所有反馈 —— 部分问题可能是误报或过度工程建议。

**核心原则：** 先合并，再对照 spec 验证，最后修复计划。生成一份一致的计划，而非三份拼凑。

## 响应模式

```
当所有 3 个 plan-reviewer agent 完成后：

1. 合并：收集所有问题，去重，识别共识（2+ agent 同时发现的问题）
2. 验证：对照 spec 和实际计划内容交叉检查每个唯一问题
3. 评估：这是真实的缺口、误解，还是过度工程建议？
4. 排序：共识问题优先，然后 Critical → Important → Minor
5. 修复：直接修复计划文件，每次处理一个类别
```

## 合并结果

**共识检测：**
- 2+ agent 同时发现的问题 → 高置信度，很可能是真实问题
- 仅 1 个 agent 发现的问题 → 验证后再处理（可能是误报）

**去重：**
- 不同任务中相同根因 → 合并为一个问题
- 同一任务的重叠问题 → 合并为单个修复

## 不同问题类型的处理

**占位符和 TBD（Critical）：**
- 替换为实际内容（代码、命令或具体细节）
- 如无法确定内容，提交用户处理而非保留占位符

**spec 需求缺少对应任务（Critical）：**
- 在正确的依赖位置添加任务
- 包含完整的步骤结构（测试 → 运行 → 实现 → 运行 → 提交）
- 验证新任务不破坏现有依赖链

**模糊或不可执行的步骤（Important）：**
- 将描述替换为实际代码块和命令
- 确保每个步骤可独立执行

**缺失测试步骤（Important）：**
- 添加失败测试 → 运行 → 实现 → 运行 → 提交的循环
- 包含实际测试代码，而非"为上述内容编写测试"

**依赖问题（Important）：**
- 修正排序以匹配实际依赖关系
- 标记独立任务为可并行
- 验证变更后无循环依赖

**过度工程建议：**
- 评估：spec 是否要求这个？
- 不在 spec 中：跳过
- "锦上添花"但显著增加范围：记录但不添加

**误报：**
- 跳过并附简短理由
- 检查计划描述是否不够清晰 —— 如是，改善表述

## 修复顺序

```
对去重后已验证的问题：
  1. 占位符、TBD、不完整步骤（Critical）
  2. spec 需求缺少对应任务（Critical）
  3. 缺少可执行代码/命令的步骤（Important）
  4. 缺失测试步骤（Important）
  5. 依赖排序问题（Important）
  6. 任务描述清晰度（Minor）
```

修复后验证：
- 每个 spec 需求至少映射到一个任务
- 无剩余占位符
- 所有引用的类型/函数已在先前任务中定义
- 依赖链无循环引用
