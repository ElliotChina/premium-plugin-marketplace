# Premium Plugin Marketplace

个人精选的 Claude Code 插件市场集合，提供 28+ 高质量插件，涵盖开发、设计、测试、金融、视频等多个领域。

## 特性

- **28+ 精选插件** - 涵盖前端开发、设计、测试、生产力、金融等
- **10 个本地插件** - 深度定制的个人开发工具集
- **18+ 外部插件** - 来自 Vercel、Microsoft、Anthropic 等团队的优质插件
- **持续更新** - 跟随社区最新版本，保持技能同步

## 插件列表

### 本地插件

| 插件 | 说明 | 分类 |
|------|------|------|
| **devflow** | 个人工具箱：项目配置、功能测试、文档更新、PRD、原型设计、Pencil UI、Unsplash 图片、Reveal.js 幻灯片 | 开发 |
| **superpowers-plus** | 代码 / Spec / Plan 的并发多 agent 审查，派遣审查 agent、合并去重反馈、修复问题 | 开发 |
| **finance-analysis** | A股/港股/美股行情数据获取（akshare）和全面的股票估值分析 | 金融 |
| **frontend-web** | UI 设计审查、可访问性审计等 Web 开发技能 | 设计 |
| **frontend-react** | 组合模式、最佳实践和视图转场等 React 开发技能 | 开发 |
| **frontend-react-native** | 动画、列表性能、UI 组件和状态管理等移动端开发技能 | 开发 |
| **frontend-next** | RSC、异步模式、数据获取、路由等 Next.js 最佳实践 | 开发 |
| **test-web** | Playwright 测试专家能力 | 测试 |
| **image** | Unsplash 图片搜索下载 | 设计 |
| **slide** | Reveal.js 幻灯片制作 | 生产力 |

### 外部插件

| 插件 | 说明 | 作者 |
|------|------|------|
| **agent-browser** | 浏览器交互自动化：测试、表单填写、截图、数据提取 | Vercel |
| **chrome-devtools-mcp** | Chrome DevTools 深度集成，性能分析和调试 | Chrome DevTools Team |
| **playwright-cli** | 基于 CLI 的高效浏览器自动化，适合 token 节省型工作流 | Microsoft |
| **context7-plugin** | 实时文档查询，获取最新的 API 文档和代码示例 | Upstash |
| **document-skills** | Excel、Word、PowerPoint、PDF 文档处理套件 | Anthropic |
| **marketing-skills** | 41 个营销技能：CRO、文案、SEO、广告、定价策略等 | Corey Haines |
| **obsidian** | Obsidian 知识管理集成 | Steph Ango |
| **superpowers** | TDD、调试、协作模式等核心技能库 | Jesse Vincent |
| **compound-engineering** | AI 驱动的开发工具，每次使用都更智能 | Every Inc. |
| **vue-volar** | Vue.js 语言服务器集成 (Volar) | Piebald LLC |
| **ui-ux-pro-max** | 专业 UI/UX 设计数据库：样式、色彩、排版、图表等 | nextlevelbuilder |
| **impeccable** | 前端设计流畅性：23 个命令 + 反模式检测 | Paul Bakaus |
| **claude-hud** | 实时状态栏：上下文用量、活跃工具、Agent 进度 | Jarrod Watts |
| **remotion** | React 视频制作最佳实践：动画、音频、字幕、3D | Remotion |
| **hyperframes** | HTML 写视频：GSAP 动画、字幕、语音、音频可视化 | HeyGen |
| **antd-skill** | Ant Design v6 组件决策指南和离线 API 查询 | Ant Design |
| **shadcn** | shadcn/ui 组件管理：添加、搜索、调试、样式定制 | shadcn |
| **slidev** | Slidev 幻灯片创建与演示 | Anthony Fu |

## 目录结构

```
premium-plugin-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # 插件市场清单
├── plugins/                      # 本地插件
│   ├── devflow/
│   ├── superpowers-plus/
│   ├── finance-analysis/
│   ├── frontend-web/
│   ├── frontend-react/
│   ├── frontend-react-native/
│   ├── frontend-next/
│   ├── test-web/
│   ├── image/
│   └── slide/
└── README.md
```

## 快速开始

### 方法一：Git 克隆

```bash
git clone https://github.com/ElliotChina/premium-plugin-marketplace.git

claude marketplace add /path/to/premium-plugin-marketplace
```

### 方法二：直接添加

```bash
claude marketplace add https://github.com/ElliotChina/premium-plugin-marketplace
```

## 本地技能来源与更新

以下技能从外部仓库下载到本地，更新时需从源仓库同步：

| 插件 | 技能 | 来源仓库 |
|------|------|----------|
| test-web | playwright-expert | [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/playwright-expert) |
| frontend-web | web-design-guidelines | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) |
| frontend-react | composition-patterns | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns) |
| frontend-react | react-best-practices | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) |
| frontend-react | react-view-transitions | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-view-transitions) |
| frontend-react-native | react-native-skills | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-native-skills) |
| frontend-next | next-best-practices | [vercel-labs/next-skills](https://github.com/vercel-labs/next-skills/tree/main/skills/next-best-practices) |

### 同步方法

```bash
# 单文件技能
curl -s "https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill-name>/SKILL.md" \
  -o plugins/<plugin-name>/skills/<skill-name>/SKILL.md

# 多文件技能（需同步 SKILL.md 及 rules/ 或 references/ 子目录）
curl -s "https://api.github.com/repos/<owner>/<repo>/contents/skills/<skill-name>" \
  | jq -r '.[].name'
```

## 插件分类

### 按领域分类

- **前端开发** - frontend-web, frontend-react, frontend-react-native, frontend-next, vue-volar, antd-skill, shadcn
- **测试与自动化** - test-web, agent-browser, playwright-cli, chrome-devtools-mcp
- **设计与 UI** - ui-ux-pro-max, impeccable, image
- **文档与内容** - document-skills, obsidian, slide, slidev
- **视频制作** - remotion, hyperframes
- **开发工作流** - devflow, superpowers, superpowers-plus, compound-engineering, context7-plugin, claude-hud
- **金融分析** - finance-analysis
- **营销** - marketing-skills

### 按来源分类

- **本地插件** (10) - devflow, superpowers-plus, finance-analysis, frontend-web, frontend-react, frontend-react-native, frontend-next, test-web, image, slide
- **外部插件** (18) - agent-browser, chrome-devtools-mcp, playwright-cli, context7-plugin, document-skills, marketing-skills, obsidian, superpowers, compound-engineering, vue-volar, ui-ux-pro-max, impeccable, claude-hud, remotion, hyperframes, antd-skill, shadcn, slidev

## 许可证

MIT License

---

**维护者**: [elliot](https://github.com/ElliotChina)
