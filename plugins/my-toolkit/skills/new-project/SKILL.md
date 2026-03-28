---
name: new-project
user-invocable: true
argument-hint: "[项目名称]"
description: >
  This skill should be used when the user runs "/my-toolkit:new-project" to bootstrap a new project.
  Provides a structured workflow for initializing projects, including tech stack selection, directory
  scaffolding, dependency setup, and initial configuration.
---

# New Project - 新项目启动

引导式创建新项目，从需求分析到项目初始化一步到位。

## 触发方式

用户执行 `/my-toolkit:new-project` 命令时激活。可选传入项目名称作为参数。

## 插件设置

开始前，根据项目实际情况检查并调整插件状态。

### 判断所需插件

根据项目类型和技术栈，判断哪些插件需要启用：

- **context7-plugin** — 查阅所选技术栈的最新文档和 API（推荐启用）
- **frontend-design** — Web 类项目前端页面设计（Web 项目启用）
- **feature-dev** — 功能开发工作流和架构设计 agent（推荐启用）
- **security-guidance** — 安全检查 hook，从项目开始防范安全问题（推荐启用）
- **antd** / **shadcn** — 如使用对应 UI 组件库则启用
- **chrome-devtools-mcp** — Web 项目前端调试（按需启用）
- **superpowers** — 项目初始化验证方法论（推荐启用）

非相关插件建议暂时禁用，减少干扰。

### 检查当前状态

依次读取以下配置文件，综合判断插件的最终启用/禁用状态：

1. **全局配置** `~/.claude/settings.json` — 用户级别的插件默认状态
2. **项目配置** `.claude/settings.json` — 当前项目级别的覆盖状态

优先级：项目配置 > 全局配置。合并两层配置后，得出各插件的最终生效状态，对比上述需求判断是否需要调整。

### 调整插件状态

若当前状态不符合需求，使用 AskUserQuestion 工具询问用户：

```
根据当前项目，建议以下插件调整：
- 启用：[插件列表及原因]
- 禁用：[插件列表及原因]
是否确认调整？
```

用户确认后，修改项目 `.claude/settings.json` 中对应插件的启用/禁用状态。

## 技能加载

根据项目技术栈加载相关技能：

- **vercel-react-best-practices** / **vercel-composition-patterns** — React 项目
- **vercel-react-native-skills** — React Native 项目
- **remotion-best-practices** — 视频动画项目
- **verification-before-completion**（superpowers）— 项目初始化后强制验证

与用户确认技术栈后，主动加载对应技能。

## 工作流程

### 1. 收集项目信息

通过交互式提问了解项目需求：

- 项目名称和简要描述
- 项目类型（Web 应用、API 服务、CLI 工具、库/包、移动应用等）
- 技术栈偏好（语言、框架、数据库）
- 目标平台（浏览器、Node.js、移动端、桌面端）
- 是否需要 TypeScript
- 是否需要 Docker 支持

### 2. 技术栈推荐

根据项目类型和用户偏好，推荐最合适的技术方案。遵循 KISS 原则，优先选择：

- 生态成熟、社区活跃的技术
- 用户熟悉或已在使用的技术栈
- 最简方案，避免过度工程

### 3. 目录结构设计

根据技术栈创建标准目录结构。检查当前工作目录是否已有相关文件，避免覆盖。

### 4. 项目初始化

按顺序执行：

1. 创建目录结构
2. 初始化包管理（package.json / requirements.txt / go.mod 等）
3. 创建配置文件（tsconfig、eslint、prettier 等按需）
4. 创建入口文件和基础代码
5. 创建 .gitignore
6. 创建 README.md（简要说明项目用途和启动方式）
7. 初始化 Git 仓库（如果尚未初始化）

### 5. 安装依赖

安装必要的核心依赖，区分 dependencies 和 devDependencies。

### 6. 验证

> **superpowers 技能**：启用 `verification-before-completion`，在声称项目初始化完成前必须运行验证命令。

运行构建或启动命令验证项目可正常运行，读取完整输出确认成功。

## 注意事项

- 创建文件前先检查目录是否已存在同名项目
- 不要预先安装非核心的依赖，保持初始项目精简
- 根据项目类型合理选择配置文件，不盲目添加
- 所有生成的代码遵循用户 CLAUDE.md 中的开发原则
