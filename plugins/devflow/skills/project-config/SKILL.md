---
name: project-config
argument-hint: "[项目名称和简要描述]"
description: This skill should be used when the user asks to "configure project", "setup dev environment", "initialize project", "setup plugins", "configure development environment", or mentions project setup and configuration. Provides a structured workflow for plugin and skill setup.
---

# Project Config - 项目配置

引导式配置项目开发环境，包括插件、技能和 CLAUDE.md 的初始化配置。

## 工作流程

### 1. 收集项目信息

快速查看现有项目，了解项目情况。如果是新项目，通过交互式提问了解项目需求，帮助确认需要哪些插件和技能：

- 项目名称和简要描述
- 项目类型（Web 应用、API 服务、CLI 工具、库/包、移动应用等）
- 技术栈偏好（语言、框架、数据库）
- 目标平台（浏览器、Node.js、移动端、桌面端）
- 以及其他可以帮助选择插件和技能的相关信息

### 2. 获取已经安装的插件和技能

#### 检查已安装插件

1. 读取以下配置文件，获取已安装插件列表：

- **插件安装清单**`~/.claude/plugins/installed_plugins.json` — 所有已经安装的插件，插件名称和安装目录

2. 依次读取以下配置文件中的 `enabledPlugins` 字段，综合判断插件的最终启用状态：

- **全局配置** `~/.claude/settings.json`
- **项目配置** `.claude/settings.json`
- **本地配置** `.claude/settings.local.json`

`enabledPlugins` 格式为 `{"插件名@来源": true/false}`。优先级：本地 > 项目 > 全局。

3. 结合**插件推荐列表**，筛选出已安装插件和适合当前项目的推荐插件，整理为表格，示例：

**插件检查结果**

| 插件名称 | 已安装 | 全局启用 | 项目启用 | 本地启用 | 最终状态 |
|---|---|---|---|---|---|
| superpowers | ✅ | ✅ | — | — | ✅ 启用 |
| context7-plugin | ✅ | ✅ | ✅ | — | ✅ 启用 |
| chrome-devtools-mcp | ✅ | ✅ | ❌ | — | ❌ 禁用 |
| playwright | ❌ | — | — | — | ❌ 未安装 |
| agent-browser | ❌ | — | — | — | ❌ 未安装 |
| typescript-lsp | ❌ | — | — | — | ❌ 未安装 |

> `—` 表示该层级未显式配置，继承上层状态。

**注意：** 仅展示已安装的插件和适合当前项目的推荐插件，不列出全部插件。

#### 检查已安装技能

1. 读取以下目录，获取已安装技能列表：
- **全局技能配置** `~/.claude/skills/` — 用户级别的已安装技能列表
- **项目技能配置** `.claude/skills/` — 当前项目级别的已安装技能列表
- **插件技能配置** `{plugin-name}/skills/` — 插件下的技能，插件启用后技能才算安装

  
2. 依次读取以下配置文件中的 `skillOverrides` 字段，综合判断技能的最终可见性：

- **全局配置** `~/.claude/settings.json`
- **项目配置** `.claude/settings.json`
- **本地配置** `.claude/settings.local.json`

`skillOverrides` 取值：`"on"`（显示名称和描述）| `"name-only"`（仅显示名称）| `"user-invocable-only"`（对 Claude 隐藏，/菜单可见）| `"off"`（完全隐藏）。优先级：本地 > 项目 > 全局。未配置时以技能 frontmatter 为准。

3. 结合**技能推荐列表**，筛选出已安装技能和适合当前项目的推荐技能，整理为表格，示例：

**技能检查结果**

独立技能（通过 `npx skills add` 安装）：

| 技能名称 | 来源 | 状态 |
|---|---|---|
| slides-revealjs | 项目 `.claude/skills/` | ✅ 已安装 |
| brainstorm | 全局 `~/.claude/skills/` | ✅ 已安装 |
| vercel-react-best-practices | — | ❌ 未安装 |
| antd | — | ❌ 未安装 |

已启用插件的技能：

| 技能名称 | 所属插件 | 状态 |
|---|---|---|
| pdf | document-skills | ✅ 可用 |
| pptx | document-skills | ✅ 可用 |

**注意：** 仅展示已安装的技能和适合当前项目的推荐技能，不列出全部技能。

### 3. 配置插件

1. 如果在**插件推荐列表**里有适合项目的插件但用户未安装，提示用户安装插件。
2. 如果插件已经安装但是没启用，提示用户启用插件。
3. 如果插件已经启用但是不适合当前项目，提示用户禁用插件。
4. 如果有以上需求，使用 AskUserQuestion 工具询问用户：
```
根据当前项目，建议以下插件调整：
- 启用：[插件列表及原因]
- 禁用：[插件列表及原因]
- 安装：[插件列表及原因]
是否确认调整？
```

**重要** 所有配置只在**本地配置** `.claude/settings.local.json` 中进行修改，不修改全局配置，避免影响其他项目。

查阅完整推荐列表，参考 **`references/plugin-recommendations.md`**。

### 4. 配置技能

1. 如果在**技能推荐列表**里有适合项目的技能但用户未安装，提示用户安装技能。
2. 安装技能使用 `npx skills add <skill-name>` 命令，安装后技能会自动启用，无需额外启用步骤。
3. 如果有以上需求，使用 AskUserQuestion 工具询问用户：
```
根据当前项目，建议以下技能调整：
- 安装：[技能列表及原因]
是否确认调整？
```

**重要** 所有技能只在**项目技能配置** `.claude/skills/` 中进行修改，不修改全局配置，避免影响其他项目。

查阅完整推荐列表，参考 **`references/skill-recommendations.md`**。

### 5. 更新 CLAUDE.md

使用 claude-md-improver 技能优化 CLAUDE.md 内容。
如果 CLAUDE.md 不存在，先使用 /init 创建文件。

## 注意事项

- 根据项目类型合理选择插件和技能，不盲目添加
- 插件安装后，需要使用 reload-plugins 命令刷新配置后才能生效
- 技能安装后，需要使用 reload-skills 命令刷新配置后才能生效
- 插件和技能安装后提醒用户最好重启 claude-code 以确保完全加载
