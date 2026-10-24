# issue-tracker

多平台工作项管理：向 GitHub Issues、GitLab Issues、阿里云云效（Codeup/Projex）或本地 Markdown 提交、查看、检索需求 / 缺陷 / 任务，支持指派、父子与阻塞关联、代码关联及迭代管理，自动探测代码托管平台并选择对应跟踪器。

设计参考 [mattpocock/skills](https://github.com/mattpocock/skills) 的跟踪器适配模式：主技能只说抽象操作（create / view / list / comment / update / close），每个跟踪器一份适配文档把操作映射为具体命令，零脚本、纯 prompt。

## 使用

安装插件后直接说：

- 「提一个需求：支持导出 PDF」→ 提交到当前项目的跟踪器
- 「提个 bug：登录页超时」
- 「列一下所有未关闭的 bug」
- 「看下 #42」
- 「把这个任务指派给我」
- 「拆成两个子任务挂在这个需求下」
- 「建个 PR 关联这个 bug，合并后自动关闭它」
- 「把这个需求排进下个迭代」
- 「搜一下提到登录超时的工作项」

首次使用时技能会探测 `git remote`（github.com → GitHub、gitlab → GitLab、codeup.aliyun.com → 云效），把对应适配文档写入项目 `.claude/issue-tracker.md`，之后直接读该配置。

## 支持的跟踪器

| 跟踪器 | 通道 | 类型表达 | 首次配置 |
|--------|------|----------|----------|
| GitHub | `gh` CLI | 标签 `type:requirement/bug/task` | 无 |
| GitLab | `glab` CLI | 标签 `type:requirement/bug/task` | 无 |
| 云效 Codeup/Projex | `aliyun devops` CLI（优先委托 alibabacloud-devops 技能） | 原生工作项类型（需求/任务/缺陷） | 需 PAT 令牌 + Projex 项目 ID |
| 本地 Markdown | 仓库内 `.scratch/issues/` 文件 | 文件名与 `Type:` 行 | 无 |

自定义跟踪器：手工把工作流描述写进项目 `.claude/issue-tracker.md`，技能原样遵循。

## 前置条件

- GitHub：[`gh`](https://cli.github.com/) 已安装并登录
- GitLab：[`glab`](https://gitlab.com/gitlab-org/cli) 已安装并登录
- 云效：`aliyun` CLI（`brew install aliyun-cli`）。配置分两处存放：
  - **PAT 令牌与组织 ID** → 用户级环境变量：`ALIBABA_CLOUD_YUNXIAO_ACCESS_TOKEN`、`ALIBABA_CLOUD_YUNXIAO_ORGANIZATION_ID`。macOS/Linux 写入 shell 配置（如 `~/.zshrc`）；Windows 用系统「环境变量」设置或 `setx` 命令持久化。令牌获取见[个人访问令牌](https://help.aliyun.com/zh/yunxiao/developer-reference/obtain-personal-access-token)。令牌是账号凭据，只走环境变量，不写入任何项目文件
  - **Projex 项目 ID** → 项目 `.claude/issue-tracker.md` 顶部注释（`<!-- org: <组织ID>  project: <项目ID> -->`），首次使用时技能会引导补全，随仓库提交供团队共享；不想提交可将该文件加入 `.gitignore`，不影响功能
- 本地 Markdown：无
