# Finder 角度与误报清单

medium/high 档的 8 个角度定义、xhigh/max 的扩展角度，以及 finder 与 verify 阶段共用的误报排除清单。

## 通用要求

每个 finder 角度：

- 独立工作，不参考其他角度的结论；两个角度以不同理由标记同一行时都保留。
- 每条候选给出 `file`、`line`、一行 `summary`、具体 `failure_scenario`（什么输入/状态 → 什么错误行为）。
- 说不出失败场景的候选不产出；能说出的一律产出，裁决交给 verify 阶段。
- 只评审 diff 引入或直接影响的代码。

## 8 个基础角度（medium / high）

### Correctness × 3

1. **条件与边界**：条件写反或写错、off-by-one、循环边界错误、falsy-zero 判断（`if (x)` 在 `x` 可为 `0` 时误判）、被移除的 guard 或校验。
2. **异步与错误路径**：漏 `await`、未处理的 promise rejection、catch 吞掉应传播的错误、错误处理被 diff 删除、并发/竞态。
3. **调用面影响**：被修改函数的所有调用方是否仍然正确——参数语义变化、返回值变化、null/undefined 解引用（相邻行表明值可能缺失时）、复制粘贴错变量、重命名遗漏。

### Cleanup × 3

4. **重复代码**：新代码重复了 diff 上下文或代码库中已有的 helper——应复用而非重写。
5. **死代码**：diff 遗留的不可达代码、注释掉的代码、不再被引用的导出/变量/导入。
6. **简化机会**：过度复杂的实现可用更直接写法等价替换（嵌套条件合并、冗余中间变量、可用标准库一行完成的循环）。

### Altitude × 1

7. **抽象层级**：新代码放在了错误的层级——底层细节泄漏到高层接口、高层逻辑下沉到工具函数、单一用途的过早抽象。判断标准：这段代码放到相邻代码的层级里读起来是否突兀。

### Conventions × 1

8. **仓库规范**：改动是否违反仓库显式文档化的约定——根目录及改动文件所在目录的 CLAUDE.md、CONTRIBUTING.md、风格指南。注意 CLAUDE.md 是写给写代码时的 Claude 的指导，不是所有条款在评审时都适用；只在条款明确覆盖该问题时才标记，并引用来源文件。

## 扩展角度（xhigh / max，追加到 8 个基础角度之上）

### Angle D — 语言陷阱专家

扫描 diff 语言/框架的经典陷阱，标记 diff 引入的任何实例：

- **JavaScript/TypeScript**：falsy-zero、`==` 强制转换、闭包捕获循环变量、`this` 绑定丢失、数组 `sort` 默认字典序。
- **Python**：可变默认参数、late-binding 闭包、`is` 比较值、except 裸捕获。
- **Go**：nil-map 写入、range 变量捕获、`defer` 在循环中、slice 共享底层数组。
- **通用**：SQL 注入、时区/DST 偏移、浮点相等比较、整数除法截断。

### Angle E — wrapper/proxy 正确性

当 PR 新增或修改包装另一类型的类型（cache、proxy、decorator、adapter）：

- 检查每个方法都路由到被包装实例，而不是绕回 registry/session/global。典型 bug：持有 `delegate` 字段的缓存 provider 用 `session.get(...)` 而非 `delegate.get(...)` 解析 ID → 重新进入缓存或无限递归。
- 检查 wrapper 转发了调用方实际用到的所有方法。

## 误报排除清单

finder 与 verify 阶段都遵守。以下类别一律不报：

- **Pre-existing 问题**：diff 之前就存在的问题（除非 diff 使其显著恶化）。
- **看起来像 bug 但不是**：有注释或上下文说明的有意行为。
- **linter/typechecker/compiler 能抓的**：缺 import、类型错误、编译失败、格式问题、换行符。不运行这些工具——CI 会跑。
- **常规代码质量问题**：缺测试覆盖、一般性安全建议、文档不足——除非 CLAUDE.md 明确要求。
- **被显式静默的**：CLAUDE.md 有条款但代码里有 lint ignore / eslint-disable 注释的地方。
- **有意的功能变更**：与改动整体目的直接相关的行为变化。
- **用户未修改的行**：findings 锚定到 diff 修改的行。
- **资深工程师不会提的吹毛求疵**：命名偏好、注释密度、无关紧要的风格。

## verify 规则摘要

| 档位 | verify 方式 | 保留标准 |
|------|------------|---------|
| low | 无 | finder 直出 |
| medium | 每候选 1 个 verifier（subagent） | 确认真实且值得处理（`CONFIRMED`） |
| high | 每候选 1 个 verifier（subagent） | 非 REFUTED 即保留（recall 偏置） |
| xhigh | 无（仅 dedup + sweep） | 全部保留 |
| max | 每候选 1 个 verifier（subagent） | 单个 non-REFUTED 票即保留 |

verifier 职责：独立读相关代码，确认失败场景成立；对照误报排除清单检查；检查 CLAUDE.md 类 findings 的条款是否真的明确覆盖该问题。结论写入 finding 的 `verdict`（`CONFIRMED` / `PLAUSIBLE`）。
