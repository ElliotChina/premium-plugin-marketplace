# 推荐技能

使用 `skills` CLI（`npx skills`）管理技能。通过 `npx skills add <source>` 从 GitHub 仓库安装，支持项目级和全局级两种作用域。

## 前端开发

| 技能 | 来源仓库 | 说明 |
|------|----------|------|
| `web-design-guidelines` | `vercel-labs/agent-skills` | Web Interface Guidelines 合规审查 |

## React 技术栈

| 技能 | 来源仓库 | 说明 |
|------|----------|------|
| `vercel-react-best-practices` | `vercel-labs/agent-skills` | React 性能优化最佳实践 |
| `vercel-composition-patterns` | `vercel-labs/agent-skills` | React 组件组合模式 |
| `vercel-react-native-skills` | `vercel-labs/agent-skills` | React Native 和 Expo 移动端开发最佳实践 |
| `next-best-practices` | `vercel-labs/next-skills` | Next.js 文件约定、RSC 边界、数据模式、路由处理等最佳实践 |
| `playwright-cli` | `microsoft/playwright-cli` | 基于 Playwright 的浏览器自动化与测试 |

## UI 组件库

| 技能 | 来源仓库 | 说明 |
|------|----------|------|
| `antd` | `ant-design/antd-skill` | Ant Design 组件 API 查询与排障 |
| `ant-design` | `ant-design/antd-skill` | Ant Design 架构决策与主题定制 |
| `shadcn` | `shadcn/ui` | shadcn/ui 组件管理 |

## 安装命令

### 项目级安装（推荐）

```bash
# 安装单个技能
npx skills add vercel-labs/agent-skills --agent claude-code --skill <skill-name> --yes

# 安装仓库中所有技能
npx skills add vercel-labs/agent-skills --agent claude-code --yes

# 查看仓库中可用的技能列表
npx skills add vercel-labs/agent-skills --list
```

### 全局级安装

```bash
npx skills add vercel-labs/agent-skills --agent claude-code --skill <skill-name> --global --yes
```

## 技术栈到技能的映射规则

### 所有前端项目

必选：`web-design-guidelines`
推荐: `playwright-cli`

### React 项目

必选：`vercel-react-best-practices`, `vercel-composition-patterns`

### Next.js 项目

必选：`next-best-practices`

### React Native 项目

必选：`vercel-react-native-skills`

### 使用 Ant Design 的项目

必选：`antd`, `ant-design`

### 使用 shadcn 的项目

必选：`shadcn`
