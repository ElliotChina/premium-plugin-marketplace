# finance-analysis

股票与金融分析插件，提供 A股/港股/美股行情数据获取（akshare、A股全栈数据）、东财数据库金融/宏观/资讯查询、同花顺 iFinD 数据查询与市场热点发现，以及股票估值、可比公司与多 agent 深度公司分析能力。

## 技能列表

| 技能 | 说明 | 来源 |
|------|------|------|
| akshare | 基于 akshare 库的 A股/港股/美股行情数据获取，内置接口文档索引与离线文档下载脚本 | 自研 |
| stock-valuation | 股票估值分析：混合模式数据采集（最新季报 TTM、业绩预告、快报），PE/PB/PEG 估值与投资分析报告 | 自研 |
| a-stock-data | A股全栈数据工具包：15 层 87 端点、34 数据源，行情 K 线/逐笔/研报/资金面/财务/期货/可转债，自包含内嵌全部可运行代码 | [外部同步](https://github.com/simonlin1212/a-stock-data) |
| mx-data | 妙想数据技能（东方财富数据库）：金融数据查询、公告研报检索、宏观查询、市场热点发现、可比公司分析五个子能力，共用授权 | [妙想技能库](https://ai.eastmoney.com/skills) |
| ifind-finance-data | 同花顺 iFinD 综合金融数据查询：智能选股/选基、投研级数据指标、行情、快查/法智数据库 | 本地收录 |
| company-analysis | 多 agent 深度公司分析：五阶段流程产出 15 章可追溯报告，含三人独立质量评分与三情景估值 | 自研 |

> 「外部同步」技能由 CI 工作流（`.github/workflows/sync-external-skills.yml`）每周检查上游自动更新；其余技能为手动收录，无自动同步，更新需从来源手动复制。

## 配置说明

### mx-data（东财妙想数据库）

凭据从以下任一位置读取，五个子能力（金融数据 / 检索 / 宏观 / 热点 / 可比分析）共用：

1. 环境变量 `EM_API_KEY`
2. `~/.mx-skills/em_api_key` 文件（推荐）

获取方式：查询脚本内联授权检查，直接运行即可；也可手动运行 `python3 scripts/auth.py ensure`，按打印的授权链接完成授权后凭据自动落盘到 `~/.mx-skills/em_api_key`，之后无需重复授权。

### ifind-finance-data

密钥按以下顺序读取：

1. 环境变量 `IFIND_AUTH_TOKEN`（推荐，密钥不落盘）
2. `mcp_config.json` 的 `auth_token` 字段（替换文件中的占位符 `REPLACE_WITH_YOUR_IFIND_MCP_TOKEN`）

密钥获取：iFinD MCP 官网「个人中心 - 密钥」<https://mcp.51ifind.com/#/profile>。

运行环境：Node.js（首选方案，零依赖）或 Python 3 + `requests`。

### Python 依赖

| 技能 | 依赖安装 |
|------|----------|
| akshare | `pip install akshare` |
| stock-valuation | `pip install pandas` |
| a-stock-data | `pip install mootdx requests pandas stockstats numpy baostock xlrd openpyxl`（Python 3.9+） |
| mx-data | `pip install httpx pandas openpyxl` |
| ifind-finance-data | Node.js 零依赖，或 Python 3 + `pip install requests` |
| company-analysis | 无第三方依赖（Python 3 标准库） |

## 版本

见 [plugin.json](.claude-plugin/plugin.json) 的 `version` 字段，插件更新后通过 `/plugin update` 获取。
