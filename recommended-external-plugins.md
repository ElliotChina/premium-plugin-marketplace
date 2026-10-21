# 外部来源插件清单

市场中通过远程仓库引用的插件(`source` 为 `git-subdir` 或 `url`)分为两组:**外部插件市场推荐**已从 `.claude-plugin/marketplace.json` 移除,仅作推荐记录,可按需从上游仓库直接安装;**外部插件引用**仍由市场配置引用。文末另附**外部 Skill 推荐**,为不含插件壳的单体 Skill,可手动复制到 `~/.claude/skills/` 使用。

## 外部插件市场推荐(18 个,已从市场移除)

| 插件 | 分类 | 说明 | 上游仓库 |
|------|------|------|----------|
| context7-plugin | 开发 | 实时拉取特定版本的库文档和代码示例 | [upstash/context7](https://github.com/upstash/context7) |
| impeccable | 设计 | 前端设计流畅性:23 个命令 + 反模式检测 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) |
| chrome-devtools-mcp | 开发 | Chrome DevTools 自动化、调试与性能分析 | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
| mattpocock-skills | 工程 | grilling、TDD、code review、domain modelling 等工程技能 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| superpowers | 开发 | TDD、调试、协作模式核心技能库 | [obra/superpowers](https://github.com/obra/superpowers) |
| compound-engineering | 开发 | 头脑风暴、计划、调试、审查的复合工程工作流 | [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) |
| ui-ux-pro-max | 设计 | UI/UX 设计智能:样式、色彩、排版、图表数据库 | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| hyperframes | — | HTML 写视频:GSAP 动画、字幕、语音、网页转视频 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) |
| vue-skills | 开发 | Vue.js 开发技能集 | [vuejs-ai/skills](https://github.com/vuejs-ai/skills) |
| document-skills | 生产力 | Excel、Word、PowerPoint、PDF 文档处理套件 | [anthropics/skills](https://github.com/anthropics/skills) |
| obsidian | 生产力 | Obsidian 知识管理技能 | [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) |
| marketing-skills | 生产力 | 41 个营销技能:CRO、SEO、广告、定价等 | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| claude-hud | 监控 | 实时状态栏:上下文用量、活跃工具、Agent 进度 | [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud) |
| agent-browser | 开发 | 浏览器交互自动化:测试、表单、截图、数据提取 | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) |
| slidev | 生产力 | Slidev 幻灯片创建与演示 | [slidevjs/slidev](https://github.com/slidevjs/slidev) |
| taste-skill | 设计 | 网页设计品味技能集:艺术方向、真实图库参考、浏览器三宽度自查 | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) |
| ponytail | 工程 | "懒惰资深开发者"提示词:最小改动、复用优先,附审查/审计命令 | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| sepia | 写作 | 去 AI 味写作技能:write/review/refactor/recreate/hemingway 五种操作,叙事架构层修复,含中文校准 | [Nanako0129/sepia](https://github.com/Nanako0129/sepia) |

## 外部插件引用(4 个,仍在市场中)

| 插件 | 分类 | 说明 | 上游仓库 |
|------|------|------|----------|
| playwright-cli | 开发 | 基于 CLI 的浏览器自动化,token 节省型工作流 | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) |
| remotion | 开发 | React 视频制作:动画、音频、字幕、3D | [remotion-dev/skills](https://github.com/remotion-dev/skills) |
| antd-skill | 开发 | Ant Design v6 组件决策指南与离线 API 查询 | [ant-design/antd-skill](https://github.com/ant-design/antd-skill) |
| shadcn | 设计 | shadcn/ui 组件管理与开发技能 | [shadcn-ui/ui](https://github.com/shadcn-ui/ui) |

## 外部 Skill 推荐(3 个)

| Skill | 分类 | 说明 | 上游仓库 |
|-------|------|------|----------|
| human-writing | 写作 | 活人感中文写作与改稿:材料前置检查、按文体加载规则、禁翻案腔/破折号/黑话,覆盖知乎、公众号、小说等文体 | [KKKKhazix/human-writing](https://github.com/KKKKhazix/human-writing) |
| humanizer-zh | 写作 | blader/humanizer 中文版:31 个检查点消除空话、重复与模板化表达,只润色不改事实与语气 | [op7418/humanizer-zh](https://github.com/op7418/humanizer-zh) |
| excalidraw-diagram-generator | 设计 | 自然语言生成 .excalidraw 图表:流程图、架构图、时序图、ER 图等 9 类,支持云架构图标库 | [github/awesome-copilot](https://github.com/github/awesome-copilot) |
