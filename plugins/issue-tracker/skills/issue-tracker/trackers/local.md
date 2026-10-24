# 跟踪器适配：本地 Markdown

工作项以 Markdown 文件存放在仓库 `.scratch/issues/` 目录。适合个人项目或没有远程仓库的场景。`.scratch/` 应已加入 `.gitignore`（没有则提醒用户加上）。

无「首次配置」步骤。

## 文件约定

- 一个工作项一个文件：`.scratch/issues/<NN>-<type>-<slug>.md`，如 `007-bug-登录超时.md`
- `<NN>` 三位数字编号，创建时扫描目录取最大号 +1，不回收复用
- `<type>` 取 `requirement` / `bug` / `task`
- 文件头部为若干行元数据标记（至少 `Type:` 与 `Status:`，其余按需），正文用通用模板：

```markdown
Type: bug
Status: open
Priority: P1

# <标题>

## 背景
……
```

优先级用头部 `Priority:` 行，取 `P0` ～ `P3`；未提及时不写该行。

## 操作映射

- **create**：按编号规则新建文件，写入 `Type:` 与 `Status: open` 两行（用户提了优先级则加 `Priority:` 行）和正文模板。
- **view**：直接读文件（含底部 `## Comments` 小节）。
- **list**：扫描 `.scratch/issues/*.md`，grep 每个文件的 `Type:` / `Status:` 行，按过滤条件输出编号、类型、状态、标题；关键词全文搜索直接 grep 文件内容。
- **comment**：在文件底部 `## Comments` 小节下追加 `- <日期> <内容>`（无该小节则创建）。
- **update**：直接编辑文件对应内容。
- **close / reopen**：把 `Status:` 行改为 `closed` / `open`，关闭说明作为一条评论追加。
- **assign**：文件头部加一行 `Assignee: <人>`（`@me` 写当前用户的名字），`list` 可按该行过滤。
- **link**：文件头部加对应行，值都是目标工作项编号：`Parent: NN`、`Blocked by: NN, NN`、`Related: NN, NN`。一个工作项被视为解除阻塞，当它 `Blocked by` 列出的编号都已 `closed`。
- **iteration**：文件头部加一行 `Iteration: <名称>`，`list` 可按该行过滤。
- **delete**：与用户确认后直接删除文件。
- **attach**：附件存 `.scratch/issues/attachments/<NN>-<文件名>`，正文用相对路径引用。

## 代码关联

本地跟踪器无自动关联，约定 commit message 引用编号（如 `[007] 修复登录超时`）作为人工线索。
