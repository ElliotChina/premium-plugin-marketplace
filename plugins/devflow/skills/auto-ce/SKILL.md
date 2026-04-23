---
name: auto-ce
description: 从头脑风暴到代码实现的端到端自动化工作流，串联 compound-engineering 全流水线（brainstorm → plan → work → review → test）。当用户需要从需求到代码的完整开发流程时触发，例如"帮我从头做一个功能"、"完整实现 XXX"、"用 CE 流程做"。即使用户没有明确提到 compound-engineering 或 auto-ce，只要意图是从零开始完整实现一个功能，就应该使用此 skill。
argument-hint: "[功能描述]"
disable-model-invocation: true
---

## 前置条件

本 skill 依赖以下插件，运行前确认已安装：
- **compound-engineering**（必需）— 版本3.0.0以上，提供 ce-brainstorm / ce-plan / ce-doc-review / ce-work / ce-review / ce-test-browser / ce-test-xcode 等核心能力
- **ralph-loop**（可选）— 提供迭代循环控制，缺失时自动跳过

## 流水线规则

如果任务为非软件类，停止流水线并告知用户。
每一步完成后验证输出产物已生成（文件存在、代码已修改等）。任何步骤验证失败时最多重试 **2 次**，仍未通过则停止流水线并向用户报告具体问题。不要跳过任何步骤直接进入实现。

## 为什么按这个顺序执行

这个流水线的设计理念是"思考先行，实现随后"：先通过 ce-brainstorm 把模糊的想法变成清晰的需求文档，然后通过 ce-doc-review 发现需求中的逻辑漏洞，接着用 ce-plan 把需求拆解为可执行的任务，再次 ce-doc-review 确保 plan 质量。只有在这四步都完成后才开始写代码（ce-work）。代码审查使用 autofix 模式自动修复问题，修复后立即持久化到 git（步骤 8），确保审查成果不会丢失在 working tree 中。残余问题自动移交到 tracker 或 PR body（步骤 9），保证所有发现都有持久化记录，不会因为会话结束而丢失。最后通过 ce-test-browser / ce-test-xcode 验证功能正确性。跳过前面的思考阶段直接写代码是产生低质量输出的最常见原因。

## 步骤

1. **头脑风暴**
   `/compound-engineering:ce-brainstorm [feature idea or problem to explore]`
   记录所有产物文件路径供后续步骤使用。

2. **需求文档审查**
   `/compound-engineering:ce-doc-review mode:headless <brainstorm-path>`
   确认需求文档无关键问题。

3. **迭代循环（可选）**
   如果 `ralph-loop` 插件可用，运行：
   `/ralph-loop:ralph-loop "<目标描述>" --max-iterations 3 --completion-promise "DONE"`
   循环范围覆盖步骤 4（制定计划）到步骤 10（功能验证），每次迭代从 plan 开始重新执行完整实现流程。
   不可用或执行失败则跳过，继续步骤 4。

4. **制定计划**
   `/compound-engineering:ce-plan <brainstorm-path>`
   记录所有产物文件路径供后续步骤使用。

5. **计划文档审查**
   `/compound-engineering:ce-doc-review mode:headless <plan-path>`
   确认计划无关键问题。发现问题则回到步骤 4 重新 plan，再重复本步骤（最多重试 2 次，仍未通过则停止流水线并向用户报告）。

6. **实现代码**
   `/compound-engineering:ce-work <plan-path>`
   验证有文件被创建或修改。如果没有代码变更，不要进入步骤 7。

7. **代码审查（自动修复）**
   `/compound-engineering:ce-code-review mode:autofix <plan-path>`
   传入步骤 4 的计划文件路径，验证实现完整性并自动修复发现的问题。
   读取 skill 输出的 Residual Actionable Work 摘要。

8. **持久化审查修复**
   运行 `git status --short` 检查步骤 7 是否产生了文件变更。
   - 如果有变更：仅 stage 审查修复的文件，提交 `fix(review): apply autofix feedback`，然后 push 当前分支。如果上游不存在，动态解析可写远程：优先 `origin`，否则取 `git remote` 返回的第一个远程，执行 `git push --set-upstream <remote> HEAD`。
   - 如果没有变更：明确记录无审查修复需要持久化。

   不要在审查修复变更仍仅存在于 working tree 时继续执行后续步骤。

9. **残余问题移交**
   仅当步骤 7 报告了一个或多个 residual `downstream-resolver` 发现时执行（跳过条件：报告 `Residual actionable work: none.`）。不向用户提问，自主完成：

   1. 以**非交互模式**加载 `references/tracker-defer.md`，传入步骤 7 的 residual actionable findings。
   2. 收集结构化返回：`{ filed: [...], failed: [...], no_sink: [...] }`。
   3. 组装 `## Residual Review Findings` markdown 区块：
      - `filed` 中的每一项：列出严重级别、file:line、标题、tracker 工单 URL 链接。
      - `failed` 中的每一项：列出严重级别、file:line、标题、失败原因。
      - `no_sink` 中的每一项：列出严重级别、file:line、标题，作为 PR body 或回退文件的持久化记录。
   4. 检测当前分支的 PR：
      ```bash
      gh pr view --json number,url,body,state
      ```
   5. 如果存在 open PR，将 `## Residual Review Findings` 区块追加或替换到 PR body 中：
      ```bash
      gh pr edit PR_NUMBER --body-file BODY_FILE
      ```
   6. 如果没有 open PR，创建回退文件 `docs/residual-review-findings/<branch-or-head-sha>.md`，仅 stage 该文件，提交 `docs(review): record residual review findings` 并 push。push 规则同步骤 8。
   7. 如果两条路径都失败，停止并报告失败的命令，不要静默继续。

10. **功能验证**
    `/compound-engineering:ce-test-browser` 测试 Web 应用
    `/compound-engineering:ce-test-xcode` 测试 iOS 应用（需要使用 XcodeBuildMCP，如未安装则跳过）
    以上都不适用时，使用你认为合适的测试方法验证功能正确性。
    如果测试失败，报告问题并回到步骤 6 重新实现，再重复步骤 7、8、9 和 10（最多重试 2 次，仍未通过则停止流水线并向用户报告）。

11. **收尾**
    输出 `<promise>DONE</promise>` 表示流水线完成。
    如果步骤 3 启动了 ralph-loop，运行 `/ralph-loop:cancel-ralph`。
