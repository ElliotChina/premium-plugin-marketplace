---
name: simplify
description: 代码质量清理技能。This skill should be used when the user asks to "simplify the code", "clean up the changes", "代码简化", "清理重复代码", "reduce duplication", "make the code cleaner", or wants reuse/simplification/efficiency/altitude cleanups applied to the changed code. Reviews the changed code for quality issues, then applies the fixes directly. Quality only — it does not hunt for bugs; use code-review for that.
argument-hint: "[<path>]"
---

# Simplify

改进改动代码的质量，而不是找 bug。审查 diff 中的复用（reuse）、简化（simplification）、效率（efficiency）、抽象层级（altitude）四类问题，然后直接修复发现的问题。不找正确性 bug——那是 code-review 技能的职责。

## 评审范围

运行 `git diff HEAD`（含已暂存与未暂存改动）确定评审范围；传入路径参数时只评审该路径下的改动。若 diff 为空，告知用户没有可清理的改动并停止。

## 执行流程

### Phase 1 — 审查（4 个清理角度并行）

若 Agent 工具可用，在**单条消息**中并行启动 **4 个独立审查 agent**（`Explore` 或 `general-purpose`，只读），每个负责一个角度（见下）。每个 agent 返回 findings，每条含 `file`、`line`、一行 `summary`、具体代价（什么被重复了、浪费了、或更难维护了）。

若 Agent 工具不可用，在本上下文中按顺序逐个过四个角度，单遍完成——不因无法并行而跳过任何角度。

**四个清理角度：**

1. **Reuse（复用）**：新代码重复了代码库或 diff 上下文中已有的 helper / 组件 / 工具函数——应调用现有实现，而不是重写一份。同时检查 diff 自己引入的重复（两处新代码做了同一件事）。
2. **Simplification（简化）**：过度复杂的实现——可合并的嵌套条件、多余的中间变量、没有第二消费者的单用途抽象、可用标准库一行替代的手写循环、过早的参数化/配置化。
3. **Efficiency（效率）**：明显的浪费——循环内的重复计算或重复 I/O、可用一次遍历完成的多遍处理、错误的数据结构（频繁查找用数组而非 Set/Map）、无意义的深拷贝。
4. **Altitude（抽象层级）**：代码放在了错误的层级——高层逻辑下沉进工具函数、底层细节泄漏进高层接口、命名与所在层级不匹配。判断标准：这段代码放到相邻代码的层级里读起来是否突兀。

**不报**：正确性 bug、风格、命名偏好、缺测试覆盖——不在本技能范围内。

### Phase 2 — 修复

等待四个 agent 全部完成后：

1. **去重**：指向同一行或同一机制 findings 只留一条。
2. **逐条直接修复**剩余 findings——四类清理同等对待。
3. **跳过**并记录原因，不与它争辩：
   - 修复会改变代码的既有预期行为（intended behavior）
   - 修复需要改动评审范围之外的大量代码
   - 判断为误报
4. 收尾用一段简短总结：修复了什么、跳过了什么及原因（或确认代码本来就很干净）。

修复完成后，若项目有测试或 lint 命令，运行一次确认没有破坏现有行为；失败则回滚对应修复并说明。

## 硬性规则

- 只清理 diff 涉及的代码；不重构无关代码。
- 修复前后行为必须等价——这是质量清理，不是功能变更。
- 每条修复都能说清"清理前后的代价对比"（少了几行、少了一次重复、少了几个抽象层）。
