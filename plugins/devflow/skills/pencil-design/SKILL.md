---
name: pencil-design
argument-hint: "[页面或组件描述]"
description: >
  基于 Pencil 设计体系的 UI 开发技能，将系统化的设计理念和视觉规范融入实际代码实现。
  适用于 Web 应用、移动端、着陆页、仪表板等任何 UI 开发场景，不限制框架和语言。
  当用户提到 "设计界面"、"开发页面"、"做 UI"、"前端界面"、"dashboard"、"管理后台"、
  "移动端界面"、"着陆页"、"数据大屏"、"表单页面"、"列表页面" 等需求时触发。
  也适用于用户需要视觉风格指导、配色方案、布局规范、组件设计等设计决策时。
---

# Pencil Design - 系统化 UI 开发

将 Pencil 的设计理念和视觉规范融入 UI 代码开发，适用于任何前端框架和语言。

## 触发方式

用户执行 `/devflow:pencil-design` 命令，或在对话中涉及 UI 开发和设计决策时激活。

## 核心理念

这个技能不是教如何使用 Pencil 工具，而是将 Pencil 背后的设计体系作为指导思想：

- **设计系统思维**：先梳理组件体系，再逐个实现，保持一致性
- **视觉规范驱动**：用设计令牌和语义化颜色替代随意取值
- **布局模式化**：将常见布局归纳为可复用的模式
- **渐进式构建**：先骨架、再内容、后细节，每步验证
- **不绑定工具和语言**：设计原则适用于 React/Vue/Angular/SwiftUI/Flutter 等任何技术栈

## 工作流程

### 1. 确定设计类型

根据用户需求判断设计类型，读取对应的指南：

| 设计类型 | 参考指南 | 典型场景 |
|----------|----------|----------|
| Web 应用 | `references/guidelines/web-app.md` | 后台管理、仪表板、SaaS |
| 移动端 | `references/guidelines/mobile-app.md` | iOS/Android 应用界面 |
| 着陆页 | `references/guidelines/landing-page.md` | 营销页面、产品介绍 |
| 数据表格 | `references/guidelines/table.md` | 数据列表、报表 |
| 复杂组件系统 | `references/guidelines/design-system.md` | 设计系统、组件库 |

读取对应指南文件，将设计原则融入开发决策。

### 2. 确定视觉风格

根据用户偏好或项目类型，从 `references/style_guides/` 中选择合适的视觉风格。

**选择方式：**

1. 从 `references/style_guides/tags.md` 中找到匹配的标签（选 5-10 个）
2. 根据标签匹配具体样式文件：Web 应用 → `webapp/` 目录，移动端 → `mobile/` 目录
3. 读取选定的样式指南，提取配色方案、字体选择、间距规范

**常见风格推荐：**
- 开发者工具：`terminalminimal`, `terminaltechnicalcrisp`, `industrialtechnical`
- 企业仪表板：`swissclean`, `minimalcorporate`, `scandinavianminimal`
- 奢侈品/高端：`elegantluxury`, `darkclassy`
- 现代简洁：`swisselegant`, `swisscleanexpressive`
- 大胆创意：`brutalisttechnical`, `bauhausdigital`
- 北欧风：`nordicbrutalist`, `scandinavianminimal`

**如果项目已有样式体系**（如 Tailwind 配置、CSS 变量、设计令牌文件），优先沿用，仅用 Pencil 风格指南补全缺失部分。

### 3. 识别技术栈

探索项目结构，确定使用的技术栈和 UI 方案：

- **框架**：React / Vue / Angular / Svelte / Next.js / Nuxt 等
- **样式方案**：Tailwind / CSS Modules / styled-components / SCSS / CSS-in-JS 等
- **组件库**：Ant Design / shadcn/ui / Material UI / Chakra UI 等
- **图标库**：Lucide / Heroicons / Material Symbols 等

所有代码实现必须使用项目已有的技术栈，不引入新依赖。

### 4. 布局规划

根据设计类型选择布局模式。以下模式来自 Pencil 设计体系，可映射到任何框架：

**侧边栏 + 内容区**
```
┌──────────┬────────────────────────────────┐
│          │                                │
│ Sidebar  │     Main Content Area          │
│  240-280 │      flex-grow                  │
│          │                                │
└──────────┴────────────────────────────────┘
```

**头部 + 内容**
```
┌────────────────────────────────────────────┐
│              Header (56-64px)              │
├────────────────────────────────────────────┤
│            Content Area                    │
└────────────────────────────────────────────┘
```

**双栏布局**
```
┌─────────────────────┬─────────────┐
│    Main (flex-grow)  │  Side (固定) │
└─────────────────────┴─────────────┘
```

**卡片网格**
- 等宽：每个卡片 flex-grow，gap 控制间距
- 网格：CSS Grid，`grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`

### 5. 设计令牌映射

将 Pencil 的设计令牌概念映射到项目实际的样式系统中：

| 设计意图 | Pencil 令牌 | 映射方式 |
|----------|-------------|----------|
| 页面背景 | `$--background` | `bg-background` / `var(--background)` |
| 主文本 | `$--foreground` | `text-foreground` / `var(--foreground)` |
| 次要文本 | `$--muted-foreground` | `text-muted-foreground` |
| 卡片背景 | `$--card` | `bg-card` |
| 边框 | `$--border` | `border-border` |
| 主色 | `$--primary` | `bg-primary` / `text-primary` |
| 次色 | `$--secondary` | `bg-secondary` |
| 危险色 | `$--destructive` | `bg-destructive` |
| 成功色 | 语义色 | `text-green-600` / `var(--success)` |
| 警告色 | 语义色 | `text-amber-600` / `var(--warning)` |
| 错误色 | 语义色 | `text-red-600` / `var(--error)` |

如果项目没有设计令牌系统，根据选定的样式指南创建 CSS 变量或 Tailwind 配置。

### 6. 间距体系

统一使用一致的间距值，避免随意取值：

| 上下文 | 间距 | 说明 |
|--------|------|------|
| 页面分区 | 24-32px | 主要区域之间的间隔 |
| 卡片网格 | 16-24px | 卡片之间的间隔 |
| 表单字段 | 16px | 表单项之间的间隔 |
| 表单行内 | 16px | 同行字段之间的间隔 |
| 按钮组 | 12px | 按钮之间的间隔 |
| 卡片内边距 | 24px | 卡片内容到卡片边缘 |
| 页面内边距 | 32px | 内容到页面边缘 |
| 紧凑区域 | 8-12px | 小元素之间的间隔 |

### 7. 组件设计原则

从 Pencil 设计体系中提炼的通用组件设计原则：

**按钮层级**
一个区域一个主要操作，视觉权重按优先级递减：

| 优先级 | 样式 | 用途 |
|--------|------|------|
| 1 | 实心主色 | 主操作（保存、提交、创建） |
| 2 | 次要 | 备选操作 |
| 3 | 描边 | 三级操作、取消 |
| 4 | 幽灵 | 内联操作、导航 |
| 5 | 危险色 | 删除、移除 |

**对齐规范**
- 卡片/弹窗内的按钮组：右对齐
- 表单提交按钮：右对齐
- 工具栏：主操作左对齐，次操作右对齐
- 危险操作：取消在左，危险在右

**表格设计**
- 列数控制在 4-7 列
- 主标识列（如名称）：200-250px
- 邮箱/URL：flex-grow
- 状态/标签：100-120px
- 日期：120-150px
- 操作列：80-100px

**表单设计**
- 标签在输入框上方
- 相关字段放同一行（如姓+名）
- 错误信息紧跟输入框下方
- 必填项明确标记

### 8. 实现和验证

实现过程中遵循以下步骤：

1. **搭建骨架**：先建立页面布局结构，确保布局正确
2. **填充内容**：逐个实现各区域的组件和内容
3. **应用样式**：统一设计令牌、间距、排版
4. **验证效果**：
   - 启动开发服务器查看实际效果
   - 检查视觉层次是否清晰
   - 检查间距是否一致
   - 检查响应式表现
   - 检查交互状态（hover/focus/disabled）

### 9. 如需使用 Pencil MCP

当用户需要先在 .pen 文件中做可视化设计时，使用 Pencil MCP 工具：
- `get_guidelines({ category: "guide", name: "Design System" })` 加载组件组合指南
- `get_guidelines({ category: "style", name: "风格名" })` 加载视觉样式
- `batch_design` 执行设计操作
- `get_screenshot` 验证设计结果

详细操作参考 `references/guidelines/design-system.md`。

## 参考文件

| 文件 | 用途 |
|------|------|
| `references/guidelines/design-system.md` | 组件组合模式和插槽用法 |
| `references/guidelines/web-app.md` | Web 应用设计原则（16 条法则） |
| `references/guidelines/mobile-app.md` | 移动端设计规范 |
| `references/guidelines/landing-page.md` | 着陆页设计指南 |
| `references/guidelines/table.md` | 表格设计指南 |
| `references/guidelines/code.md` | 从设计生成代码的工作流 |
| `references/guidelines/tailwind.md` | Tailwind CSS 实现指南 |
| `references/style_guides/tags.md` | 191 个样式标签参考 |
| `references/style_guides/webapp/*.md` | 20 个 Web 应用样式指南 |
| `references/style_guides/mobile/*.md` | 20 个移动端样式指南 |
