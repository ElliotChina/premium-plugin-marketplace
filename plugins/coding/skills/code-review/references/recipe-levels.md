# 档位详细流程（Recipe Levels）

各 effort 档位的完整阶段指令。**以下流程均在评审 agent（fork，见 SKILL.md 执行流程 Phase 1）内执行**；spawn subagent 指 fork 内部操作，fork 内 Agent 工具不可用时改为同上下文顺序执行，不跳过任何角度。所有档位共享同一个评审范围（scope）：`git diff @{upstream}...HEAD` 加 `git diff HEAD`（未提交改动），或传入的 PR / 分支 / 路径目标。

---

## low — 单遍快扫（无 verify）

定位：最少产出，一次 diff 直读。不 spawn subagent，不读整文件。

### Turn 1 — 读 diff

一次工具调用读完统一 diff（`git diff @{upstream}...HEAD; git diff HEAD`，或指定目标）。跳过测试/fixture 的 hunk（`test/`、`spec/`、`__tests__/`、`*_test.*`、`*.test.*`、`fixtures/`、`testdata/`）——该档位不评审测试文件改动。

### Turn 2 — 找 findings

只从 hunk 本身可见的运行时正确性 bug：条件写反/写错、off-by-one、相邻行表明值可能缺失的 null/undefined 解引用、被移除的 guard、falsy-zero 判断、漏 `await`、复制粘贴错变量、catch 吞掉应传播的错误。同样只看 hunk：新代码重复了 diff 上下文里已有的 helper，以及 diff 遗留的死代码。

**不报**风格、命名、性能、缺测试，或 hunk 之外的任何东西。

### 输出

按 SKILL.md「fork 返回契约」最终以 JSON 数组返回（每条含 `file`、`line`、`summary`、`short_summary`、`failure_scenario`，按 severity 排序），数组外附首行摘要。不调用 `ReportFindings`——渲染由主对话负责。无合格发现时空数组。

---

## medium — precision（默认档）

定位：**precision**——surface 出的每条 finding 都应是一个维护者会动手处理的。8 个角度 × 每角度最多 6 候选 → dedup → 1-vote verify。

### Phase 1 — 找候选（3 correctness + 3 cleanup + 1 altitude + 1 conventions，各最多 6 条）

通过 Agent 工具运行 **8 个独立 finder 角度**（角度定义见 `finder-angles.md`），可并行。每个角度产出最多 6 条候选，含 `file`、`line`、一行 `summary`、具体 `failure_scenario`。

凡能说出失败场景的候选一律传递——finder 静默丢弃半信半疑的候选会绕过 verify，是漏报的主因。

### Phase 2 — Dedup + verify

合并全部候选；近似重复（同缺陷、同位置、同理由）只留一条。然后对每条候选启动一个 verifier（Haiku 级 subagent 即可），让它独立复核该问题是否真实：读相关代码，确认失败场景成立，且不是误报清单里的类别。precision 偏置：只有确认真实且值得处理（`CONFIRMED`）的才保留；verify 结论记入 `verdict` 字段。

### Phase 3 — 产出结果

按 SKILL.md「fork 返回契约」产出结构化结果，most-severe first，返回协调上下文（主对话）。

---

## high — recall（subagent 版）

定位：**recall**——一次评审抓全一个细心评审者能抓到的真 bug。抓到真 bug 比避免误报更重要，宁可多报。

### Phase 1 — 找候选（8 角度，同 medium）

与 medium 相同的 8 个 finder 角度（subagent 并行），各最多 6 条候选。目标至少 `min(files_changed, 8)` 条；不足时先扩大到同一 diff 的其他 hunk 再停。真实的发现不足下限时报告实际数量，不为凑数编造。

### Phase 2 — Dedup + verify（recall 偏置）

Dedup 规则同 medium。verify 为 **recall 偏置**：verifier 无法明确证伪（non-REFUTED）的候选一律保留——宁报勿漏。

### Phase 3 — 产出结果（同 medium）

---

## xhigh — 全量深挖（inline 角度）

定位：**recall**——漏掉的 bug 会被发布。宁多报。

### Phase 1 — 找候选（5 correctness + 3 cleanup + 1 altitude + 1 conventions，各最多 8 条）

**10 个独立 finder 角度在本上下文中顺序执行——不 spawn subagent**。每角度最多 8 条候选。不允许一个角度的结论压制另一个角度：两个角度以不同理由标记同一行时，两条都记录。

除 medium 的 8 个角度外，额外的 correctness 角度包括：

- **Angle D — 语言陷阱专家**：扫描 diff 语言/框架的经典陷阱，例如 JS falsy-zero、`==` 强制转换、闭包捕获循环变量；Python 可变默认参数、late-binding 闭包；Go nil-map 写入、range 变量捕获；SQL 注入；时区/DST 偏移；浮点相等比较。标记 diff 引入的任何实例。
- **Angle E — wrapper/proxy 正确性**：当 PR 新增或修改包装另一类型的类型（cache、proxy、decorator、adapter）时，检查每个方法都路由到被包装实例，而不是绕回 registry/session/global——例如持有 `delegate` 字段的缓存 provider 用 `session.get(...)` 而非 `delegate.get(...)` 解析 ID，会重新进入缓存或递归。同时检查 wrapper 转发了调用方实际用到的所有方法。

### Phase 2 — 仅去重（无 verify）

合并候选，仅去近似重复（同缺陷、同位置、同理由 → 留一条）。**不运行 verifier、不再裁决**。按 severity 排序，不确定不丢弃。

### Phase 3 — 补漏 sweep

以"已拿到去重列表的新评审者"身份再做一遍（同上下文，无 subagent）。重读 diff 与外围函数，**只找列表之外的新缺陷**，不复核已列出的。聚焦第一遍容易漏的：移动/提取代码时丢掉的 guard 或锚点；二线陷阱（dataclass 默认值只求值一次、`hash()` 非确定性、锁范围收窄、有副作用的谓词方法）；测试的 setup/teardown 不对称；配置默认值翻转。

最多补充 8 条候选，每条都不得与已列出的重复。没有新发现就返回空——不凑数。

---

## max — 最大规模

定位：**recall**，xhigh 的 subagent 放大版。

### Phase 0 — 评估规模

按 diff 行数决定 finder subagent 数量：已提交 diff 每约 500 行 1 个，**min 2、max 8**；未提交改动不计入，作为下限，Phase 1 发现额外工作区范围时再扩。在报告开头用一行告知用户评审规模。

### Phase 1 — 找候选（2–8 个 finder subagent）

每个 subagent 覆盖 diff 的一部分文件，内部按 xhigh 的 10 角度流程执行（5 correctness + 3 cleanup + 1 altitude + 1 conventions，各最多 8 条）。规模对齐 diff 大小，不用固定大队列。

### Phase 2 — Dedup + 1-vote verify

Dedup 同前。每条候选一个 verifier，**recall 偏置**：单个 non-REFUTED 票即保留该 finding，不确定不丢。

### Phase 3 — 补漏 sweep（同 xhigh）

---

## 后处理

以下后处理均由主对话在评审 agent 返回 findings 之后执行（fork 只负责评审本身）。

### --fix

报告 findings 后，逐条直接修复到工作区——正确性 bug 与 reuse/simplification/efficiency 清理点同等对待。修复会改变代码既有预期行为（intended behavior）的，跳过并说明原因。修复完成后运行项目的检查命令（若有）确认未破坏现有测试。测试全绿不代表修复被覆盖——逐条确认有测试真正走到被改的代码（找到对应断言），找不到的在该条修复结果中注明"无测试覆盖"。

### --comment

评审目标是 GitHub PR 时，用 `gh` 把每条 finding 发为对应文件/行的 inline PR 评论（`gh api repos/:owner/:repo/pulls/<n>/comments`），正文含问题陈述与失败场景。目标是 GitLab MR 时用 `glab mr note` 发一条汇总评论（glab 不支持行锚定评论）。工具不可用或目标不是 PR 时，打印 findings 并说明 `--comment` 被忽略。

### --max-findings

`<n>` 为正整数：报告前 n 条（most-severe first）；`all`：全部；`default`：回到默认上限 32。截断时在报告首行说明总数与截断数。

### 档位记忆

用户显式输入档位时记住它（会话存储可用则持久化），下次未给档位时沿用，并在报告开头一行说明（如 "reusing high — type /code-review medium to change it"）。`--max-findings` 同理。
