---
name: receiving-spec-review
user-invocable: true
description: >
  Use when receiving spec review feedback from multiple agents, before applying changes.
  Merge deduplicated results, verify against the original spec and user intent,
  then apply unified fixes.
---

# Receiving Spec Review

多个 agent 的 spec 审查反馈在应用前需要合并和验证。不要盲目接受所有反馈 —— 部分问题可能是审查 agent 缺乏完整上下文导致的误报。

**核心原则：** 先合并，再验证，最后修复。生成一份一致的 spec，而非三份拼凑。

## 响应模式

```
当所有 3 个 spec-reviewer agent 完成后：

1. 合并：收集所有问题，去重，识别共识（2+ agent 同时发现的问题）
2. 验证：对照实际 spec 文件和用户原始请求检查每个唯一问题
3. 评估：这是真实的缺口、误解，还是 YAGNI 建议？
4. 排序：共识问题优先，然后 Critical → Important → Minor
5. 修复：直接修复 spec 文件，每次处理一个类别
```

## 合并结果

**共识检测：**
- 2+ agent 同时发现的问题 → 高置信度，很可能是真实问题
- 仅 1 个 agent 发现的问题 → 验证后再处理（可能是误报）

**去重：**
- 相同根因的不同表述 → 合并为一个问题
- 不同章节的重叠问题 → 检查是否共享同一根因

## 不同问题类型的处理

**真实缺口（缺失章节、占位符、TBD）：**
- 直接在 spec 文件中修复
- 验证修复与用户原始意图一致

**矛盾：**
- 选择与用户既定目标匹配的版本
- 如不确定哪个正确，提交用户决策

**歧义：**
- 选择一种解释并明确化
- 验证选择与 spec 其余部分一致

**YAGNI 建议：**
- 评估：用户是否真的需要这个？
- 未请求的：跳过
- 潜在有用但非现在：记录但不加入 spec

**误报（审查 agent 误解上下文）：**
- 跳过并附简短理由
- 检查 spec 本身是否因表述不清导致误解 —— 如是，改善表述

## 修复顺序

```
对去重后已验证的问题：
  1. 占位符和 TBD（Critical）
  2. 章节间矛盾（Critical）
  3. 可能导致错误实现的模糊需求（Important）
  4. 缺失的范围边界（Important）
  5. 术语不一致（Minor）
```

修复后验证：
- 所有修复彼此一致
- 未引入新的矛盾
- 每个需求仍能映射到用户的原始请求
