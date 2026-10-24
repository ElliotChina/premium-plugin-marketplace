# 跟踪器适配：GitLab Issues

工作项存放在项目的 GitLab Issues，所有操作用 [`glab`](https://gitlab.com/gitlab-org/cli) CLI 完成。项目从 `git remote -v` 自动推断。

无「首次配置」步骤。

## 类型映射

工作项类型用标签表达：`type:requirement` / `type:bug` / `type:task`。优先级用标签 `priority:P0` ～ `priority:P3` 表达。创建时若标签不存在，先 `glab label create` 再挂上。

状态映射：`open` → opened，`closed` → closed（无中间状态）。

## 操作映射

- **create**：

```bash
glab issue create --title "<标题>" --label "type:<类型>" --description "$(cat <<'EOF'
<正文>
EOF
)"
```

- **view**：`glab issue view <编号> --comments`
- **list**：`glab issue list --per-page 30`（按类型过滤加 `--label "type:bug"`；查已关闭加 `--closed`）
- **comment**：GitLab 称评论为 note：`glab issue note <编号> --message "<内容>"`
- **update**：改标签 `glab issue update <编号> --label "..."` / `--unlabel "..."`；改标题 `glab issue update <编号> --title "..."`。
- **close**：先 `glab issue note <编号> --message "<收尾说明>"`，再 `glab issue close <编号>`（close 不接受收尾评论）；**reopen**：`glab issue reopen <编号>`。
- **assign**：`glab issue update <编号> --assignee @me`；取消指派 `--unassignee`。
- **link**：
  - `parent`：在子 issue 描述顶部写 `Part of #<父编号>` 行（GitLab 无 GitHub 式 sub-issue）。
  - `blocks`：原生阻塞链接是 Premium 功能：`glab issue note <被阻塞编号> --message "/blocked_by #<阻塞编号>"`；免费版在描述顶部写 `Blocked by: #<n>, #<n>` 行。
  - `relates`：`glab issue note <编号> --message "/relates #<目标编号>"`。
- **iteration**：GitLab 用里程碑：`glab issue update <编号> --milestone "<名称>"`；`list` 按里程碑过滤加 `--milestone <名称>`。
- **delete**：默认降级为 close 并评论注明「误报关闭」；用户明确要求真删时用 `glab api "projects/:id/issues/<编号>" -X DELETE`（需维护者权限）。
- **attach**：`glab` CLI 无附件上传，在描述或评论贴图片 URL；本地截图提示用户在网页端编辑器拖拽上传。

多行描述一律用 heredoc。

## 代码关联

创建 MR 时在描述写 `Closes #<编号>` / `Fixes #<编号>`，合并后自动关闭对应 issue；commit message 中同样生效。

## 关键词搜索

`glab issue list --search "<关键词>"` 即全文搜索标题与描述。
