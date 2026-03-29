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

**插件与技能准备**：根据设计需求和技术栈，检查并加载所需插件和技能：

- **通用**：`frontend-design` — 前端页面设计（**必选**）；`ui-ux-pro-max` — 企业级 UI/UX 设计标准（需要时）；`context7-plugin` — 查阅 UI 框架最新文档
- **React 技术栈**：按需加载 `vercel-react-best-practices`（性能优化）、`vercel-composition-patterns`（组件组合模式）
- **UI 组件库**：按需加载 `antd`（Ant Design 组件使用）、`ant-design`（Ant Design 架构决策）、`shadcn`（shadcn/ui 组件管理）

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

实现过程中按需使用：

- `context7-plugin` — 查阅 UI 框架/组件库的最新 API 和最佳实践
- `chrome-devtools-mcp` — 设计稿对比和前端调试

### 4. 实现原则

遵循以下设计原则：

- 移动优先，逐步增强
- 一致的间距、字号、配色体系
- 清晰的视觉层次和信息架构
- 合理的交互反馈
- 符合无障碍标准

### 5. 确认和迭代

将设计成果呈现给用户，根据反馈调整优化。

加载 `web-design-guidelines` — 基于 Web Interface Guidelines 进行 UI/UX 合规审查，确保设计符合无障碍标准。

## 注意事项

- 先了解项目现有的设计系统或组件库
- 输出代码要符合项目技术栈
- 遵循 Web Interface Guidelines 和无障碍标准
- 不过度设计，保持简洁实用
