---
name: check-env
argument-hint: "[技术栈描述]"
description: This skill should be used when the user asks to "check environment", "check plugins", "check skills", "install missing plugins", "prepare development environment", "check dependencies", or "setup dev environment". Detects the project's tech stack and ensures all required plugins, skills, and MCP tools are installed and properly configured.
---

# 开发环境检查

根据项目技术栈，检查并安装必要的插件、技能和 MCP 工具。

## 工作流程

### 1. 检测技术栈

分析项目目录结构，识别技术栈：

1. 读取项目根目录的 `package.json`、`pyproject.toml`、`build.gradle`、`pom.xml`、`Cargo.toml` 等配置文件
2. 识别主要框架和语言（React/Vue/Angular、Python/Java/Node.js/Swift 等）
3. 识别 UI 组件库（antd/shadcn/MUI 等）
4. 如用户通过参数指定了技术栈，以用户指定为准

输出当前检测到的技术栈摘要。

### 2. 检查插件

根据技术栈，对照 **`references/recommended-plugins.md`** 中的映射规则确定所需插件列表。通过 CLI 和配置文件双重验证，逐一检查状态：

1. 执行 `claude plugin list` 获取当前实际运行时已安装的插件清单
2. 读取以下配置文件中的 `enabledPlugins` 字段，确认启用状态（优先级从高到低）：
   - 项目本地：`.claude/settings.local.json`
   - 项目共享：`.claude/settings.json`
   - 用户全局：`~/.claude/settings.json`
3. 对每个所需插件，综合判断状态：
   - `[OK]` — 在 plugin list 中存在且 enabledPlugins 中值为 `true`
   - `[OFF]` — 在 enabledPlugins 中存在但值为 `false`（已安装未启用）
   - `[MISS]` — 不在 plugin list 中（未安装）

```
插件检查结果：
  [OK]   context7-plugin@premium-plugin-marketplace — 已启用
  [OFF]  frontend-design@claude-plugins-official — 未启用
  [MISS] ui-ux-pro-max@premium-plugin-marketplace — 未安装
```

### 3. 安装和启用缺失插件

对状态为未启用或未安装的插件，使用 Claude Code CLI 处理。默认在项目级别启用（`--scope project`）：

1. **未安装**（不在 enabledPlugins 中）：
   ```bash
   claude plugin install <plugin-name>@<marketplace-name> --scope project
   ```

2. **未启用**（存在但值为 false）：
   ```bash
   claude plugin enable <plugin-name> --scope project
   ```

每个插件操作前需经确认。批量操作时可一次性列出所有待处理的插件，征得同意后统一执行。

如果 marketplace 本身未注册，先添加 marketplace：
```bash
# 支持多种来源：GitHub owner/repo、Git URL、本地路径、远程 marketplace.json URL
claude plugin marketplace add <marketplace-source>
```

### 4. 检查技能

根据技术栈，对照 **`references/recommended-skills.md`** 中的映射规则确定所需技能列表。使用 `skills` CLI 检查已安装状态：

检查方式：

1. 执行 `npx skills list --json` 获取项目级已安装技能
2. 执行 `npx skills list -g --json` 获取全局已安装技能
3. 插件技能随插件启用自动可用，无需额外操作
4. 综合判断状态：
   - `[OK]` — 已安装在项目级、全局级或随插件可用
   - `[MISS]` — 所有来源中均不存在

```
技能检查结果：
  [OK]   vercel-react-best-practices — 可用（全局级）
  [OK]   web-design-guidelines — 可用（全局级）
  [MISS] antd — 未安装
```

### 5. 安装缺失技能

使用 `skills` CLI（`npx skills`）管理技能的安装、更新和移除。默认安装到项目级别：

```bash
# 安装到项目级别（默认，写入 .claude/skills/）
npx skills add <source> --agent claude-code --yes

# 安装到全局级别（写入 ~/.claude/skills/）
npx skills add <source> --agent claude-code --global --yes

# 列出仓库中可用的技能（不安装）
npx skills add <source> --list

# 指定安装特定技能
npx skills add <source> --agent claude-code --skill <skill-name> --yes
```

其他管理命令：

```bash
# 查看已安装技能
npx skills list          # 项目级
npx skills list -g       # 全局级

# 更新技能
npx skills update        # 更新全部
npx skills update <name> # 更新指定技能

# 移除技能
npx skills remove <name>           # 项目级
npx skills remove <name> --global  # 全局级

# 搜索可用技能
npx skills find [query]
```

对不可用的技能，根据来源类型处理：

1. **插件内技能缺失**：回到步骤 3 检查并安装对应插件
2. **独立技能缺失**：使用 `npx skills add` 安装，优先安装到项目级别；全局通用技能使用 `--global` 安装

### 6. 检查 MCP

根据技术栈，对照 **`references/recommended-mcp.md`** 中的映射规则确定所需 MCP 列表。执行 `claude mcp list` 检查已配置状态。

MCP 配置存在于三个作用域（优先级从高到低）：

| 作用域 | 配置文件 | 用途 |
|--------|----------|------|
| Local | `~/.claude/.claude.local.json` | 当前项目当前用户（默认） |
| User | `~/.claude.json` | 用户全局生效 |
| Project | `.mcp.json`（项目根目录） | 团队共享，可提交至版本控制 |

也可通过 settings.json 中的 `mcpServers` 字段配置，但推荐使用上述专用文件。

```
MCP 检查结果：
  [OK]   deepwiki — 已配置（user 级别）
  [MISS] chrome-devtools-mcp — 未配置
```

### 7. 安装缺失 MCP

使用 Claude Code CLI 添加 MCP server，默认在项目级别配置（`--scope project`，写入 `.mcp.json`）：

```bash
# HTTP 传输
claude mcp add --transport http --scope project <name> <url>

# SSE 传输（URL 需包含 /events 路径）
claude mcp add --transport sse --scope project <name> <url>

# stdio 传输（默认传输类型）
claude mcp add --scope project <name> -- <command> [args...]

# 带环境变量
claude mcp add --scope project -e API_KEY=xxx <name> -- <command>
```

也可通过 JSON 配置直接添加：
```bash
claude mcp add-json <name> --scope project '{"type":"http","url":"https://..."}'
```

### 8. 输出最终报告

汇总所有检查和安装结果：

```
=== 环境检查报告 ===

技术栈：React + TypeScript + Ant Design

插件状态：
  [OK]   context7-plugin — 已启用
  [OK]   frontend-design — 已启用
  [NEW]  ui-ux-pro-max — 刚安装
  [OK]   code-simplifier — 已启用

技能状态：
  [OK]   vercel-react-best-practices — 可用
  [OK]   antd — 可用
  [NEW]  web-design-guidelines — 刚安装

MCP 状态：
  [OK]   deepwiki — 已配置
  [NEW]  chrome-devtools-mcp — 刚配置

操作摘要：
  - 安装了 1 个插件：ui-ux-pro-max
  - 安装了 1 个技能：web-design-guidelines
  - 配置了 1 个 MCP：chrome-devtools-mcp
```

## 错误处理

当检查命令执行失败时，按以下方式处理：

1. **`claude plugin list` 失败**：尝试读取配置文件中的 `enabledPlugins` 作为 fallback；如配置文件也无法读取，标记所有插件为 `[UNKNOWN]` 并提示用户手动检查
2. **`npx skills list` 失败**：检查 `skills` CLI 是否已安装（`npx skills --version`）；如未安装，提示用户跳过技能检查步骤
3. **`claude mcp list` 失败**：尝试直接读取 `.mcp.json` 和 `~/.claude.json` 中的 `mcpServers` 字段作为 fallback
4. **安装命令失败**：记录失败原因并继续检查下一项，在最终报告中汇总所有失败项

## 参考文件

- **`references/recommended-plugins.md`** — 按技术栈推荐的插件列表与映射规则
- **`references/recommended-skills.md`** — 按技术栈推荐的技能列表与映射规则
- **`references/recommended-mcp.md`** — 按技术栈推荐的 MCP 工具列表
