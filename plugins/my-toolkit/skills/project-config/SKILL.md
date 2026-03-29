---
name: project-config
user-invocable: true
argument-hint: "[项目名称]"
description: >
  This skill should be used when the user runs "/my-toolkit:project-config" to configure project
  development environment. Provides a structured workflow for plugin and skill setup.
---

# Project Config - 项目配置

引导式配置项目开发环境，包括插件、技能和 CLAUDE.md 的初始化配置。

## 触发方式

用户执行 `/my-toolkit:project-config` 命令时激活。可选传入项目名称作为参数。

## 工作流程

### 1. 获取已经安装的插件和技能

#### 检查已安装插件

1. 读取以下配置文件，获取已安装插件列表：

- **插件安装清单**`~/.claude/plugins/installed_plugins.json` — 所有已经安装的插件，插件名称和安装目录

2. 依次读取以下配置文件，综合判断插件的最终启用/禁用状态：

- **全局插件配置** `~/.claude/settings.json` — 用户级别的插件启用状态
- **项目插件配置** `.claude/settings.json` — 当前项目级别的插件启用状态

优先级：项目配置 > 全局配置。合并两层配置后，得出各插件的最终启用状态

#### 检查已安装技能

1. 读取以下目录，获取已安装技能列表：
- **全局技能配置** `~/.claude/skills/` — 用户级别的已安装技能列表
- **项目技能配置** `.claude/skills/` — 当前项目级别的已安装技能列表
- **插件技能配置** `{plugin-name}/skills/` — 插件下的技能，插件启用后技能才算安装

### 2. 收集项目信息

通过交互式提问了解项目需求，帮助确认需要哪些插件和技能：

- 项目名称和简要描述
- 项目类型（Web 应用、API 服务、CLI 工具、库/包、移动应用等）
- 技术栈偏好（语言、框架、数据库）
- 目标平台（浏览器、Node.js、移动端、桌面端）
- 以及其他可以帮助选择插件和技能的相关信息

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

**重要** 所有配置只在**项目插件配置** `.claude/settings.json` 中进行修改，不修改全局配置，避免影响其他项目。

**插件推荐列表**

**项目管理**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| superpowers | 核心开发技能库：TDD、系统化调试、头脑风暴、计划编写、子 agent 驱动开发、并行任务分发、代码审查、完成前验证等 | **必选**项目开发全周期，推荐始终启用 |

**开发通用**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| context7-plugin | 查阅所选技术栈的最新文档和 API | 项目开发全周期，需查阅框架/库文档时 |
| code-simplifier | 代码简化与重构 | 需要简化复杂代码时 |
| claude-md-management | CLAUDE.md 文档管理 | 编辑和管理 CLAUDE.md 文件时 |

**前端开发**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| frontend-design | Web 类项目前端页面设计 | **有前端时必选**Web 项目前端页面开发 |
| ui-ux-pro-max | 前端 UI/UX 设计方案，提供企业级设计标准 | 需要企业级标准设计方案时 |

**前端调试与测试**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| chrome-devtools-mcp | Web 项目前端调试 | **有前端时必选**Web 项目前端功能调试 |
| agent-browser | 页面自动化操作 | 非测试/调试场景下的页面自动化操作 |
| playwright | 专业页面自动化测试 | 执行自动化测试用例 |

**LSP 服务**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| typescript-lsp | TypeScript Language Server | TypeScript/JavaScript 项目 |
| pyright-lsp | Python Language Server | Python 项目 |
| jdtls-lsp | Java Language Server | Java 项目 |
| swift-lsp | Swift Language Server | Swift 项目 |
| vue-volar | Vue 语言服务支持 | 使用 Vue 框架开发时 |

**安全与质量**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| security-guidance | 安全检查 hook，从项目开始防范安全问题 | 项目初期及开发过程中安全防护 |
非相关插件，如果在全局启用了，需要在项目中禁用，减少干扰。

### 4. 配置技能

1. 如果在**技能推荐列表**里有适合项目的技能但用户未安装，提示用户安装技能。
2. 安装技能使用 `npx skills add <skill-name>` 命令，安装后技能会自动启用，无需额外启用步骤。
2. 如果有以上需求，使用 AskUserQuestion 工具询问用户：
```
根据当前项目，建议以下技能调整：
- 安装：[技能列表及原因]
是否确认调整？
```

**重要** 所有技能只在**项目技能配置** `.claude/skills/` 中进行修改，不修改全局配置，避免影响其他项目。


**技能推荐列表**

**React 开发**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| vercel-react-best-practices | React 和 Next.js 性能优化最佳实践 | React/Next.js 项目开发、代码审查与重构 |
| vercel-composition-patterns | React 组件组合模式，构建可复用、可扩展的组件 API | 组件库开发、重构复杂组件、设计灵活的组件接口 |
| vercel-react-native-skills | React Native 和 Expo 开发最佳实践 | React Native 移动应用开发 |

**UI 组件库**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| antd | Ant Design 组件查询、调试、样式与组合 | 使用 Ant Design 组件库开发时 |
| ant-design | Ant Design 6.x 决策指南、主题令牌、SSR、无障碍 | Ant Design 版本选型、主题定制、架构决策时 |
| shadcn | shadcn/ui 组件管理、调试与组合 | 使用 shadcn/ui 组件库开发时 |

**前端审查**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| web-design-guidelines | 前端代码 UI/UX 合规审查，基于 Web Interface Guidelines | 前端页面设计审查、无障碍检查、用户体验审计 |

**测试自动化**

| 名称 | 说明 | 使用场景 |
|---|---|---|
| playwright-cli | 浏览器自动化交互，支持 Web 测试、表单填写、截图和数据提取 | 自动化测试、页面交互验证 |

### 5. 更新 CLAUDE.md

使用 claude-md-improver 技能优化 CLAUDE.md 内容。
如果 CLAUDE.md 不存在，先使用 /init 创建文件。

## 注意事项

- 根据项目类型合理选择插件和技能，不盲目添加
- 插件安装后，需要使用 reload-plugins 命令刷新配置后才能生效
- 插件和技能安装后提醒用户最好重启 CLAUDE 以确保完全加载
