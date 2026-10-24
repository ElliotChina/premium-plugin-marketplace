# 跟踪器适配：GitHub Issues

工作项存放在仓库的 GitHub Issues，所有操作用 `gh` CLI 完成。仓库从 `git remote -v` 自动推断。

无「首次配置」步骤。

## 类型映射

工作项类型用标签表达：`type:requirement` / `type:bug` / `type:task`。优先级用标签 `priority:P0` ～ `priority:P3` 表达。创建时若标签不存在，先 `gh label create`（颜色随意）再挂上，多个标签用逗号传给一次 `--label`。

状态映射：`open` → open，`closed` → closed（无中间状态）。

## 操作映射

- **create**：

```bash
gh issue create --title "<标题>" --label "type:<类型>" --body "$(cat <<'EOF'
<正文>
EOF
)"
```

- **view**：`gh issue view <编号> --comments`
- **list**：

```bash
gh issue list --state open --limit 30 --json number,title,labels \
  --jq '[.[] | {number, title, types: [.labels[].name | select(startswith("type:"))]}]'
```

按类型过滤加 `--label "type:bug"`；查已关闭加 `--state closed`。

- **comment**：`gh issue comment <编号> --body "<内容>"`
- **update**：改标签 `gh issue edit <编号> --add-label "..."` / `--remove-label "..."`；改标题或正文用 `gh issue edit <编号> --title "..."` / `--body "..."`。
- **close**：`gh issue close <编号> --comment "<收尾说明>"`；**reopen**：`gh issue reopen <编号>`。
- **assign**：`gh issue edit <编号> --add-assignee <用户名>`（自己用 `@me`）；取消指派 `--remove-assignee`。
- **link**：
  - `parent`：把子 issue 挂到父 issue：`gh issue edit <父编号> --add-sub-issue <子编号>`（`gh` 2.94+；不可用时在子 issue 正文顶部写 `Part of #<父编号>` 行）。
  - `blocks`：原生依赖：`gh api --method POST repos/{owner}/{repo}/issues/<被阻塞编号>/dependencies/blocked_by -F issue_id=<阻塞项数据库ID>`，其中数据库 ID 用 `gh api repos/{owner}/{repo}/issues/<编号> --jq .id` 获取（是数字 ID，不是 `#编号`）；不可用时在正文顶部写 `Blocked by: #<n>, #<n>` 行。
  - `relates`：正文或评论写 `Related to #<目标编号>`。
- **iteration**：GitHub 用里程碑（milestone）：`gh issue edit <编号> --milestone "<名称>"`（不存在时先 `gh api --method POST repos/{owner}/{repo}/milestones -f title="<名称>"` 创建）；`list` 按里程碑过滤加 `--milestone "<名称>"`。
- **delete**：GitHub 不支持删除 issue，降级为 `close` 并评论注明「误报关闭」。
- **attach**：`gh` CLI 无附件上传，在正文或评论贴图片 URL（Markdown `![描述](URL)`）；本地截图提示用户在网页端编辑器拖拽上传。

多行正文一律用 heredoc，不用转义换行。

## 代码关联

创建 PR 时在正文用关键字引用工作项：`Closes #<编号>` / `Fixes #<编号>`，合并后 GitHub 自动关闭对应 issue；commit message 中同样生效。查询单个工作项关联的分支 / PR / commit 用 `gh api repos/{owner}/{repo}/issues/<编号>/timeline`。

## 关键词搜索

`list` 加 `--search "<关键词>"` 即全文搜索标题、正文与评论。
