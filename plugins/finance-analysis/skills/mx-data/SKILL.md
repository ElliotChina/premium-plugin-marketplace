---
name: mx-data
description: 基于东方财富妙想数据库的金融数据技能，按任务分五个子能力：①自然语言查询金融数据——A港美股票、基金、债券的实时行情、公司信息、估值、财务报表，适用投资研究、交易复盘、市场监控、行业分析、信用研究、财报审计、资产配置；②检索最新公告、研报、财经新闻和交易所动态，适用资讯查找、事件跟踪、公告精读、舆情监控；③自然语言查询全球宏观经济数据，适用宏观研究、市场分析、政策解读；④A股市场热点发现——"今日热点、热门股票、活跃赛道"等市场级热点的结构化报告；⑤可比公司分析——同业可比公司选取、多维度估值对比，输出主题化 Excel 报告。凭据经 EM_API_KEY 环境变量或授权流程获取后五个子能力共用。仅在需要调用数据接口取数时使用：市场热点类泛化问题用子能力④而非②，单一标的的深度诊断用①而非④；A股概念解释、投资观点讨论、策略问答等无需取数的话题不要加载本 skill。
version: 1.0.0
license: proprietary
origin: 妙想技能库 https://ai.eastmoney.com/skills （五技能合并收录：mx-finance-data / mx-finance-search / mx-macro-data / stock-market-hotspot-discovery / comparable-company-analysis）
---

# 妙想数据技能（东方财富数据库）

五个子能力共用一套东财数据授权与脚本目录，按任务选择对应子能力执行。

## 授权（各子能力共用）

依赖 `EM_API_KEY`。授权检查已内联到各查询脚本，**直接执行查询脚本，不要先单独运行 `scripts/auth.py ensure`**，也不要把授权做成独立前置步骤。凭据按 `EM_API_KEY` 环境变量、`~/.mx-skills/em_api_key` 文件的顺序读取，不使用内置兜底 key。授权协议细节见 [references/auth_protocol.md](references/auth_protocol.md)。

## 子能力路由

| 任务 | 子能力文档 | 脚本 |
|------|-----------|------|
| 自然语言查询金融数据：行情、公司信息、估值、财务报表 | [references/finance-data.md](references/finance-data.md) | `scripts/get_finance_data.py` |
| 检索公告、研报、财经新闻与交易所动态 | [references/finance-search.md](references/finance-search.md) | `scripts/finance_search.py` |
| 查询全球宏观经济数据：国民经济核算、价格指数、货币金融、财政收支等 | [references/macro-data.md](references/macro-data.md) | `scripts/get_macro_data.py` |
| A股市场热点发现：今日热点、热门股票、活跃赛道 | [references/hotspot-discovery.md](references/hotspot-discovery.md) | `scripts/hotspot_discovery.py` |
| 可比公司分析：同业估值对比与 Excel 报告输出 | [references/comparable-company.md](references/comparable-company.md) | `scripts/comparable_company.py` |

## 触发边界

- "今日市场热点、热门股票、活跃赛道"等**市场级热点**泛化问题 → 子能力④（热点发现），不要用子能力②（检索）
- **单一标的**的深度诊断或指标计算 → 子能力①（金融数据），不要用子能力④（热点发现）
- 分析公司投资价值、估值对比 → 子能力⑤（可比公司分析）或本地 stock-valuation 技能

## 执行流程

1. 按上表确定子能力，读取对应子能力文档
2. 按文档中的参数与示例调用脚本，直接取数
