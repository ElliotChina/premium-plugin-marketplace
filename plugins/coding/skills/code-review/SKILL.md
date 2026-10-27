---
name: code-review
description: 多档位代码审查技能。This skill should be used when the user asks to "review my code", "code review", "review the diff", "review this PR", "审查这次改动", "检查代码有没有 bug", "review the last commit", or invokes /code-review with an effort level (low|medium|high|xhigh|max), a PR number, a branch, or a path. Reviews the current diff or a PR target for correctness bugs (plus reuse/simplification/efficiency cleanups) via parallel finder angles and a verify pass.
argument-hint: "[low|medium|high|xhigh|max] [--fix] [--comment] [<pr#>|<branch>|<path>] [--max-findings <n>|all]"
---

# Code Review

审查当前 diff 或指定目标（PR 编号 / 分支 / 路径），找出正确性 bug 和值得做的清理点（复用 / 简化 / 效率）。按 effort 档位调整 finder 数量与验证强度，在 precision 与 recall 之间取舍。

## 参数解析

参数格式：`[low|medium|high|xhigh|max] [--fix] [--comment] [<pr#>|<branch>|<path>] [--max-findings <n>|all]`

1. 第一个匹配档位名的 token 是 effort 档位（`ultra` 不支持，忽略并提示）。
2. `--fix`：评审结束后把确认的 findings 直接修复到工作区。
3. `--comment`：目标是 GitHub PR 时，把 findings 以 inline 评论形式发回 PR。
4. 剩余 token 是评审目标：PR 编号（如 `123`）、分支名或路径；省略时评审当前分支 diff。
5. `--max-findings <n>` 限制报告条数；`all` 表示不限；未给出时沿用用户上次输入（会话记忆可用时），否则用默认上限 32。
6. 未给出档位时默认 **medium**；若本会话之前用过某档位则沿用该档位，并在报告开头用一行说明沿用了哪个档位、如何切换（如 "reusing medium — type /code-review high to change it"）。

## 评审范围（Scope）

scope 由评审 agent（见「执行流程」Phase 1）在评审开始时确定，后续所有阶段以这个 diff 为准：

```bash
git diff @{upstream}...HEAD   # 已提交的改动；无 upstream 时用 git diff main...HEAD
git diff HEAD                  # 未提交的工作区改动（评审常发生在 commit 之前）
```

- 传入 PR 编号时用 `gh pr diff <n>` 获取 diff；传入分支时用 `git diff <branch>...HEAD`；传入路径时只评审该路径下的改动。
- 若范围 diff 为空且工作区有改动，把工作区改动纳入范围；两者都为空时返回空结果并注明无可评审内容，由主对话告知用户。
- 统计 diff 行数与改动文件数（`--shortstat`），用于决定 finder 数量与 findings 下限。

## 档位选择

| 档位 | 定位 | 流程 |
|------|------|------|
| **low** | 最少产出，单遍快扫 | 1 遍 diff 直读，不 verify，不 spawn subagent |
| **medium**（默认） | precision：每条 finding 都值得维护者处理 | 8 个 finder 角度（subagent）→ dedup → 1-vote verify |
| **high** | recall：一次评审尽量抓全真 bug | 8 个 finder 角度（subagent）→ dedup → 1-vote verify（recall 偏置） |
| **xhigh** | recall：全量深挖 | 10 个角度（同上下文顺序执行，不 spawn）→ dedup → 补漏 sweep |
| **max** | recall：最大规模 | 2–8 个 finder subagent（按 diff 规模伸缩）→ 1-vote verify → 补漏 sweep |

各档位的详细阶段指令见 **`references/recipe-levels.md`**，finder 角度定义与误报排除清单见 **`references/finder-angles.md`**。各档位流程均在评审 agent（fork）内执行，表中的 spawn subagent 指 fork 内部的 finder/verifier。

## 执行流程

1. **Phase 0 — 准备（主对话）**：解析参数（见上），选定档位并沿用/写入档位记忆。fork 可用时主对话不读 diff、不读 references——评审读取的全部内容都留在 fork 内（回退时例外，见 Phase 1）。
2. **Phase 1 — spawn 评审执行者（主对话）**：Agent 工具可用且支持 fork 类型时，用 `subagent_type: "fork"` 启动一个评审 agent（fork 继承对话上下文），prompt 要点：
   - 读取 `${CLAUDE_PLUGIN_ROOT}/skills/code-review/` 下的 `SKILL.md`、`references/recipe-levels.md`、`references/finder-angles.md`，按档位 <X> 的阶段指令执行完整评审；目标为 <PR 编号/分支/路径/当前分支 diff>；`--max-findings` 为 <n/all/未指定>。
   - 评审范围按「评审范围」节在 fork 内确定；档位流程中需要 spawn finder/verifier 的照常执行，fork 内 Agent 工具不可用时改为同上下文顺序执行，不跳过任何角度。
   - **不调用 `ReportFindings`**，按「fork 返回契约」最终以 JSON 数组返回。
   - Agent 工具不可用或无 fork 类型时回退：主对话读取两个 references 文件，在本上下文按该档位阶段指令执行全部阶段。
3. **Phase 2 — 渲染与后处理（主对话）**：把评审 agent 返回的 findings 按「输出契约」渲染；`--fix` 时逐条修复确认的 findings（正确性 bug 与清理点同等对待；会改变既有预期行为的修复跳过）。`--comment` 且目标是 GitHub PR 时，用 `gh` 把 findings 发为 inline 评论。

## 输出契约

契约分两层：**fork 返回契约**（评审 agent → 主对话）与**渲染契约**（主对话 → 宿主 UI）。

**fork 返回契约**：评审 agent 不调用 `ReportFindings`，最终以一个 JSON 数组返回，按 severity 从高到低排列，每条 finding 包含：

- `file` / `line`：文件路径与起始行号（1-based）
- `summary`：一句话陈述缺陷；category 属于清理点时以 `Nit:` 开头
- `short_summary`：压缩到 60 字符以内的标签，无理由或后果从句
- `failure_scenario`：具体输入/状态 → 错误输出或崩溃
- `category`：产生该 finding 的角度的 kebab-case 标签（`correctness`、`simplification`、`efficiency`、`reuse`、`altitude`、`conventions`，或更具体的如 `test-coverage`）
- `verdict`：verify 阶段产出时附带（`CONFIRMED` / `PLAUSIBLE`）

数组外附报告首行摘要一句话（所用档位、必改与 Nit 各多少条、findings 上限）；无可评审内容或无发现时返回空数组加说明。回退为主对话自行执行时，跳过本层，直接按渲染契约输出。

**渲染契约（主对话）**：优先使用 `ReportFindings` 工具（宿主 UI 可渲染结构化结果时）：调用一次，`level` 传当前档位，`findings` 用 fork 返回的 JSON 填入——正确性 bug 在前，清理点沉底；fork 返回的首行摘要在调用前作为一行正文输出。`ReportFindings` 不可用时，输出该 JSON 数组；low 档位可用一行式列表 `path/to/file.ext:123 — 哪里错了 + 具体失败方式`，无发现时输出 `(none)`。

使用 `ReportFindings` 报告时不要再把 findings 重复打印为正文文本，也不要为评审结果创建 artifact——工具调用本身就是报告。

diff 超过 1000 行时，在报告末尾追加一条建议——本次 diff 过大，建议按独立改动拆分后分别评审；该建议不占 findings 名额。

## 硬性规则

- 不运行构建、类型检查或测试——这些由 CI 负责；linter/typechecker 能抓到的问题（缺 import、类型错误、格式）一律不报。
- 本技能不覆盖安全与性能审查：安全用 /security-review；一般性安全/性能建议不在 findings 范围内。
- 每条 finding 必须有具体的失败场景，能说清"什么输入下代码会错"。
- 误报排除清单（pre-existing 问题、风格问题、缺测试覆盖等）见 `references/finder-angles.md`，finder 与 verify 阶段都遵守。
- 只评审 diff 涉及的代码；用户未修改的行上的问题不报。
- 报告中的结论必须引用 `file:line`；引用 CLAUDE.md 约定时注明来源文件。
