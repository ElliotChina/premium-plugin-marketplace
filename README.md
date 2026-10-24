# Premium Plugin Marketplace

个人精选的 Claude Code 插件市场集合，包含 19 个高质量插件，涵盖前端开发、设计、测试、金融、视频等多个领域。

## 特性

- **19 个精选插件** - 15 个本地维护 + 4 个外部引用
- **持续更新** - 本地技能跟随上游仓库同步
- **按需裁剪** - 已移除的外部插件见[外部插件推荐](recommended-external-plugins.md)，可随时从上游仓库自行安装

## 插件列表

### 本地插件（15 个）

| 插件 | 说明 | 分类 |
|------|------|------|
| **dev-tools** | 开发工具集：多档位代码审查（effort 级别 × finder 角度 × verify，支持 `--fix`/`--comment`）、代码质量清理（simplify）、安全审查（security-review） | 开发 |
| **issue-tracker** | 多平台工作项管理：向 GitHub / GitLab / 云效 Codeup / 本地 Markdown 提交、查看、检索需求 / 缺陷 / 任务，自动探测托管平台 | 开发 |
| **finance-analysis** | 股票与金融分析：集成 akshare、A股全栈数据、东方财富与同花顺 iFinD 多源行情/宏观/资讯数据，提供股票估值、多 agent 深度公司分析与可比公司分析 | 金融 |
| **frontend-web** | UI 设计审查、可访问性审计等 Web 开发技能 | 设计 |
| **frontend-react** | 组合模式、最佳实践和视图转场等 React 开发技能 | 开发 |
| **frontend-next** | RSC、异步模式、数据获取、路由等 Next.js 最佳实践 | 开发 |
| **vue-volar** | Vue.js 语言服务（Volar），启动时动态探测 TypeScript SDK 路径，支持 monorepo 嵌套项目 | 开发 |
| **product-design** | 产品与设计技能集：意图访谈、创意打磨、方案拷问、领域建模、PRD 体系管理、需求 PRD 撰写 | 生产力 |
| **prototype-design** | 原型设计：prototype-app 可执行镜像原型（生产零耦合、随代码库归档）+ prototype 即抛式发散对比 | 设计 |
| **devops** | DevOps 技能集：CI/CD 流水线、生产发布、可观测性与插桩 | 开发 |
| **writing** | 中文写作：humanizer-zh 去 AI 味润色与 human-writing 活人感写作 | 生产力 |
| **image** | Unsplash 图片搜索下载 | 设计 |
| **slide** | Reveal.js 幻灯片制作 | 生产力 |
| **excalidraw** | 自然语言生成 Excalidraw 图表：流程图、架构图、思维导图等（来自 [awesome-copilot](https://github.com/github/awesome-copilot)） | 设计 |
| **deepwiki** | AI 驱动的 GitHub 仓库文档查询 | 开发 |

### 外部引用插件（4 个）

以下插件由市场配置直接引用上游仓库，安装市场时自动拉取：

| 插件 | 说明 | 作者 |
|------|------|------|
| **playwright-cli** | 基于 CLI 的高效浏览器自动化，适合 token 节省型工作流 | Microsoft |
| **remotion** | React 视频制作最佳实践：动画、音频、字幕、3D | Remotion |
| **antd-skill** | Ant Design v6 组件决策指南和离线 API 查询 | Ant Design |
| **shadcn** | shadcn/ui 组件管理与开发技能 | shadcn |

其余曾收录的外部插件已移出市场，完整清单与上游仓库见[外部插件推荐](recommended-external-plugins.md)。

## 目录结构

```
premium-plugin-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # 插件市场清单
├── plugins/                      # 本地插件
│   ├── deepwiki/
│   ├── dev-tools/
│   ├── devops/
│   ├── excalidraw/
│   ├── finance-analysis/
│   ├── frontend-next/
│   ├── frontend-react/
│   ├── frontend-web/
│   ├── image/
│   ├── issue-tracker/
│   ├── product-design/
│   ├── prototype-design/
│   ├── slide/
│   ├── vue-volar/
│   └── writing/
├── recommended-external-plugins.md
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

以下技能从外部仓库下载到本地，由 CI 工作流定时同步：

| 插件 | 技能 | 来源仓库 |
|------|------|----------|
| frontend-web | web-design-guidelines | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) |
| frontend-react | composition-patterns | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns) |
| frontend-react | react-best-practices | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) |
| frontend-react | react-view-transitions | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-view-transitions) |

完整清单（28 条映射，含 mattpocock / addyosmani / emilkowalski 等上游）见 [.github/sync-skills-mapping.json](.github/sync-skills-mapping.json)。

### 同步方法

```bash
# 单文件技能
curl -s "https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<skill-name>/SKILL.md" \
  -o plugins/<plugin-name>/skills/<skill-name>/SKILL.md

# 多文件技能（需同步 SKILL.md 及 rules/ 或 references/ 子目录）
curl -s "https://api.github.com/repos/<owner>/<repo>/contents/skills/<skill-name>" \
  | jq -r '.[].name'
```

同步映射配置见 [.github/sync-skills-mapping.json](.github/sync-skills-mapping.json)，由 CI 工作流自动执行。

## 许可证

MIT License

---

**维护者**: [elliot](https://github.com/ElliotChina)
