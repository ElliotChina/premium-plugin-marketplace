---
name: ui
user-invocable: true
argument-hint: "[页面或组件描述]"
description: >
  This skill should be used when the user runs "/my-toolkit:ui" to design UI prototypes and interfaces.
  Provides guidance for UI/UX design, wireframing, and frontend implementation.
---

# UI - 原型/UI 设计

引导式的 UI 设计和原型开发，从设计思路到界面实现。

## 触发方式

用户执行 `/my-toolkit:ui` 命令时激活。传入页面或组件描述作为参数。

## 插件设置

开始前，根据设计需求检查并调整插件状态。

### 判断所需插件

根据设计范围和技术栈，判断哪些插件需要启用：

- **frontend-design** — 前端页面设计（推荐启用）
- **ui-ux-pro-max** — 企业级 UI/UX 设计标准和数据库（推荐启用）
- **context7-plugin** — 查阅 UI 框架最新文档（按需启用）
- **chrome-devtools-mcp** — 设计稿对比和调试（按需启用）
- **superpowers** — 设计探索和需求澄清方法论（推荐启用）

非相关插件建议暂时禁用，减少干扰。

### 检查当前状态

依次读取以下配置文件，综合判断插件的最终启用/禁用状态：

1. **全局配置** `~/.claude/settings.json` — 用户级别的插件默认状态
2. **项目配置** `.claude/settings.json` — 当前项目级别的覆盖状态

优先级：项目配置 > 全局配置。合并两层配置后，得出各插件的最终生效状态，对比上述需求判断是否需要调整。

### 调整插件状态

若当前状态不符合需求，使用 AskUserQuestion 工具询问用户：

```
根据当前 UI 设计需求，建议以下插件调整：
- 启用：[插件列表及原因]
- 禁用：[插件列表及原因]
是否确认调整？
```

用户确认后，修改项目 `.claude/settings.json` 中对应插件的启用/禁用状态。

## 技能加载

根据项目技术栈和设计需求加载相关技能：

- **shadcn** — 使用 shadcn/ui 组件库
- **antd** / **ant-design** — 使用 Ant Design 组件库
- **web-design-guidelines** — Web 设计规范审查
- **a11y-debugging**（chrome-devtools-mcp）— 无障碍调试和检测
- **brainstorming**（superpowers）— 设计前的创意探索和需求澄清
- **vercel-react-best-practices** / **vercel-composition-patterns** — React 项目

与用户确认技术栈和设计方向后，主动加载对应技能。

## 工作流程

### 1. 设计探索

> **superpowers 技能**：启用 `brainstorming`，在设计前系统化探索需求。

收集设计相关信息：

- 探索项目现有的设计系统和组件库
- 逐个提出澄清问题：设计目标、目标用户、使用场景
- 提出 2-3 个设计方案并分析权衡
- 逐节呈现设计思路，每节获得用户认可后再继续
- 功能范围和交互要求
- 设计风格偏好（参考站点、品牌色等）
- 技术栈（React、Vue、HTML/CSS 等）

### 2. 设计分析

在动手前进行设计思考：

- 信息架构和页面布局
- 用户操作流程
- 组件拆分和复用
- 响应式策略
- 无障碍考虑

### 3. 方案输出

根据需求选择合适的输出方式：

- **HTML 原型**：快速出可交互的静态原型
- **组件代码**：基于项目框架实现可复用组件
- **设计说明**：布局结构、配色方案、交互细节的文字描述

### 4. 实现原则

遵循以下设计原则：

- 移动优先，逐步增强
- 一致的间距、字号、配色体系
- 清晰的视觉层次和信息架构
- 合理的交互反馈
- 符合无障碍标准

### 5. 确认和迭代

将设计成果呈现给用户，根据反馈调整优化。

## 注意事项

- 先了解项目现有的设计系统或组件库
- 输出代码要符合项目技术栈
- 遵循 Web Interface Guidelines 和无障碍标准
- 不过度设计，保持简洁实用
