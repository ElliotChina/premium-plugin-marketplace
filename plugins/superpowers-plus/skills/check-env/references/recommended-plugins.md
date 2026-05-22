# 推荐插件

## 通用开发

| 插件名 | marketplace 来源 | 说明 |
|--------|------------------|------|
| `context7-plugin` | `premium-plugin-marketplace` | 查阅技术栈最新文档和 API |
| `code-simplifier` | `claude-plugins-official` | 简化和优化代码 |
| `claude-md-management` | `claude-plugins-official` | CLAUDE.md 文件管理 |

## 开发工作流

| 插件名 | marketplace 来源 | 说明 |
|--------|------------------|------|
| `superpowers` | `premium-plugin-marketplace` | 核心开发技能库（TDD、调试、协作） |
| `superpowers-plus` | `premium-plugin-marketplace` | superpowers 加强扩展 |
| `compound-engineering` | `premium-plugin-marketplace` | AI 驱动的开发工具集 |

## 前端开发

| 插件名 | marketplace 来源 | 说明 |
|--------|------------------|------|
| `frontend-design` | `claude-plugins-official` | 高质量前端界面设计 |
| `ui-ux-pro-max` | `premium-plugin-marketplace` | 企业级 UI/UX 设计标准 |

## 浏览器自动化与测试

| 插件名 | marketplace 来源 | 说明 |
|--------|------------------|------|
| `agent-browser` | `premium-plugin-marketplace` | 浏览器自动化（页面交互、截图、表单填写） |
| `chrome-devtools-mcp` | `premium-plugin-marketplace` | Chrome DevTools 调试（需 MCP 配置） |
| `playwright` | `claude-plugins-official` | Playwright 测试运行 |

## 代码审查与质量

| 插件名 | marketplace 来源 | 说明 |
|--------|------------------|------|
| `security-guidance` | `claude-plugins-official` | 安全审查 |

## LSP 语言服务

| 插件名 | marketplace 来源 | 说明 |
|--------|------------------|------|
| `typescript-lsp` | `claude-plugins-official` | TypeScript/JavaScript 语言服务 |
| `jdtls-lsp` | `claude-plugins-official` | Java 语言服务 |
| `pyright-lsp` | `claude-plugins-official` | Python 语言服务 |
| `swift-lsp` | `claude-plugins-official` | Swift 语言服务 |
| `vue-volar` | `premium-plugin-marketplace` | Vue.js 语言服务 |

## 技术栈到插件的映射规则

### 所有项目

必选：`context7-plugin`, `code-simplifier`, `superpowers`, `superpowers-plus`
推荐：`claude-md-management`, `security-guidance`, `compound-engineering`

### 前端项目

必选：`frontend-design`, `agent-browser`, `chrome-devtools-mcp`
推荐：`ui-ux-pro-max`

### React项目

必选：`typescript-lsp`

### Node.js项目

必选：`typescript-lsp`

### Vue项目

必选：`typescript-lsp`, `vue-volar`

### Python项目

必选：`pyright-lsp`

### Java项目

必选：`jdtls-lsp`

### 全栈项目

必选：根据前后端技术栈合并
推荐：合并前后端推荐列表
