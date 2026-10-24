# 跟踪器适配：阿里云云效（Codeup / Projex 工作项）

工作项存放在云效 Projex 项目的[工作项](https://help.aliyun.com/zh/yunxiao/user-guide/work-item-overview)中，通过 `aliyun devops` CLI 操作。

**注意**：Codeup 代码库 ≠ Projex 项目，工作项不属于代码库，无法从 `git remote` 推断目标项目，必须完成下面的「首次配置」。

## 首次配置

1. **认证检查**（令牌安全：只检查存在性，**NEVER** 让用户在对话或命令行粘贴明文令牌、**NEVER** 用 `echo` 读取令牌值）：

```bash
[ -n "$ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN" ] && echo "token ok" || echo "token missing"
[ -n "$ALIBABA_CLOUD_YUNXIAO_ORGANIZATION_ID" ] && echo "org ok" || echo "org missing"
```

缺失时引导用户到[个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)获取（需项目协作 R/W 权限），并配置环境变量：

```bash
export ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN=<令牌>
export ALIBABA_CLOUD_YUNXIAO_ORGANIZATION_ID=<组织 ID>
```

Windows 下持久化改用 `setx ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN <令牌>`（当前会话即时生效用 PowerShell 的 `$env:<名称>=<值>`），其余平台写入 shell 配置文件。

2. **确定目标项目**：向用户询问 Projex 项目 ID（工作项列表页 URL 中 `projectId=` 或 `space=` 参数的值）。拿到后把组织 ID 与项目 ID 写进 `.claude/issue-tracker.md` 顶部，形如：

```markdown
<!-- org: <组织ID>  project: <项目ID> -->
```

## 类型映射

云效工作项原生分需求 / 任务 / 缺陷，与统一类型一一对应；优先级（P0～P3）映射为项目工作项的原生优先级字段，字段标识以 `projex-get-workitem-type-field-config` 查询结果为准。各项目的类型 ID 不同，创建前先查：

```bash
aliyun devops projex-list-workitem-types --organization-id <组织ID> --space-id <项目ID>
```

从中取 `requirement` → 需求、`bug` → 缺陷、`task` → 任务的类型 ID 记到配置注释里（下次免查）。状态由云效工作流管理，`open`/`in-progress`/`closed` 映射为项目工作流中语义对应的初始 / 进行 / 终结状态，具体状态标识用 `projex-get-workitem-workflow` 查。

## 操作映射

各命令参数以 `aliyun devops <命令> --help` 实际输出为准；不确定参数名时先查再调。以下命令都需 `--organization-id`。

- **create**：`aliyun devops projex-create-workitem`，传项目 ID（`--space-id`）、标题（subject）、描述（description）、类型 ID（workitemTypeId）。
- **view**：`aliyun devops projex-get-workitem --work-item-id <ID>`，评论用 `projex-list-workitem-comments`。
- **list**：`aliyun devops projex-search-workitems`，按类型 ID / 状态过滤，或传关键词全文搜索，参数以 `--help` 为准。
- **comment**：`aliyun devops projex-create-workitem-comment`。
- **update**：`aliyun devops projex-update-workitem`，改状态传工作流状态标识，改内容传对应字段。
- **close / reopen**：同为 `projex-update-workitem`，把状态设为工作流的终态 / 回到进行中。
- **assign**：`projex-update-workitem` 更新负责人字段；字段标识（负责人常为 `handle`）以 `projex-get-workitem-type-field-config` 查询结果为准。
- **link**：云效原生支持工作项关联（含父子）：用 `projex-create-workitem-relation-record` 建立关联，关系类型与参数以 `--help` 为准；无原生阻塞关系的项目，在描述末尾注明「阻塞于 <编号>」。
- **iteration**：迭代归属是工作项字段，创建（`projex-create-workitem`）或更新（`projex-update-workitem`）时设置，迭代字段标识同样以字段配置查询为准；`projex-search-workitems` 支持按迭代过滤，参数以 `--help` 为准。
- **delete**：`aliyun devops projex-delete-workitem --work-item-id <ID>`。不可逆，执行前必须与用户确认。
- **attach**：`aliyun devops projex-create-workitem-attachment` 上传附件；参数以 `--help` 为准。

## 代码关联

Codeup 代码库与 Projex 项目同组织时，commit message 注明工作项编号（如 `#<编号>`）即自动关联；合并请求描述同样生效。合并后工作项是否自动流转由项目工作流配置决定，未自动关闭时用 update 手动收尾。

## 优先走 alibabacloud-devops 技能

若当前会话可用技能列表中有 `alibabacloud-devops`，把上述意图（创建工作项 / 搜索工作项 / 更新工作项）直接委托给它执行——它内置意图分类、参数校验与结果核验，比裸调 CLI 更稳。本适配文档的参数说明仅在无该技能时作为直接路径。
