# Premium Claude Tools Marketplace

个人精选的 Claude Code 插件市场集合，提供高质量的插件、技能和工具，帮助你更高效地使用 Claude Code。

## ✨ 特性

- 🎨 **10+ 精选插件** - 涵盖开发、设计、生产力等多个领域
- 🔧 **开箱即用** - 简单配置即可使用所有功能
- 📦 **统一管理** - 一个市场集中管理所有插件
- 🚀 **持续更新** - 跟随最新版本，确保功能完善

## 📦 包含的插件

### 🌐 浏览器自动化
- **agent-browser** - 浏览器交互自动化，支持测试、表单填写、截图等
- **chrome-devtools-mcp** - Chrome DevTools 深度集成，性能分析和调试

### 🔍 开发工具
- **context7-plugin** - 实时文档查询，获取最新的 API 文档和代码示例
- **vue-volar** - Vue.js 语言服务器，提供智能代码补全

### 📄 文档处理
- **document-skills** - Excel、Word、PowerPoint、PDF 文档处理套件
- **obsidian** - Obsidian 知识管理集成

### 🎨 设计辅助
- **ui-ux-pro-max** - 专业 UI/UX 设计智能助手，包含样式、色彩、排版等数据库

### 💼 营销技能
- **marketing-skills** - 33 个营销技能：CRO、文案、SEO、广告、定价策略等

### 🛠️ 开发最佳实践
- **superpowers** - TDD、调试、协作模式等核心技能库

## 📁 目录结构

```
premium-claude-tools/
├── .claude-plugin/          # 插件市场配置
│   └── marketplace.json     # 插件清单配置
└── README.md               # 本文件
```

## 🚀 快速开始

### 方法一：使用 Git 克隆

```bash
# 1. 克隆仓库
git clone https://github.com/ElliotChina/premium-claude-tools.git

# 2. 在 Claude Code 中添加市场
claude marketplace add /path/to/premium-claude-tools
```

### 方法二：直接添加

```bash
# 直接通过 GitHub URL 添加市场
claude marketplace add https://github.com/ElliotChina/premium-claude-tools
```

## 📖 使用说明

### 查看已安装的插件

```bash
claude plugin list
```

### 启用/禁用插件

```bash
# 启用插件
claude plugin enable <plugin-name>

# 禁用插件
claude plugin disable <plugin-name>
```

### 更新市场

```bash
# 拉取最新更新
git pull origin main

# 重新加载市场
claude marketplace reload
```

## 🔧 插件分类

### 按功能分类

- **开发工具** (Development)
  - agent-browser
  - chrome-devtools-mcp
  - context7-plugin
  - vue-volar
  - superpowers

- **生产力** (Productivity)
  - document-skills
  - obsidian
  - marketing-skills

- **设计** (Design)
  - ui-ux-pro-max

### 按类型分类

- **MCP 服务器** - 提供额外的工具和能力
- **技能包** - 特定领域的专业知识和最佳实践
- **语言服务器** - 代码智能补全和导航

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [Claude Code 官方文档](https://docs.claude.com/en/docs/claude-code)
- [Claude 插件开发指南](https://github.com/anthropics/claude-plugins-official)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star！

---

**维护者**: [elliot](https://github.com/ElliotChina)
