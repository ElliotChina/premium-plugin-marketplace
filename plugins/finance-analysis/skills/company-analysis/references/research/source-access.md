# 资料来源与取数优先级

## 取数顺序

复用适用的归档资料。**新增取数依次使用 a-stock-data → 妙想 → iFinD → akshare → 官方披露及其他可靠来源，只补缺项、不可用部分或待核验冲突。** a-stock-data 优先用于其覆盖的 A 股及相关市场数据；港美股等未覆盖任务直接从妙想开始；akshare 只在前序技能均未覆盖或需独立交叉核对时补充；仍未覆盖的资料直接查原件。非上市公司优先查审计报表及公开登记、监管资料。关键披露事实核对原件，冲突以核实后的原件为准并记录差异。

## 按资料选择技能

查询参数、依赖和授权按对应技能执行，只读取本次需要的说明。妙想任务先读取 [mx-data](../../../mx-data/SKILL.md) 的共用授权与子能力路由，再按下表读取对应文档。

| 资料 | 技能 | 使用要点 |
|---|---|---|
| A 股行情/K线、财务三表、公告、分红、股东、研报及已覆盖宏观指标 | [a-stock-data](../../../a-stock-data/SKILL.md)，最高优先级 | 先查“端点路由速查”，只读所需函数及共用定义，按需安装依赖并执行内嵌代码；遵循原技能限流和备用源规则。核对市场、交易/报告日期、复权、单位与覆盖，失败或不足即转妙想，已知失效端点跳过。 |
| 财务、行情、估值、股东、已选同业指标 | [妙想金融数据](../../../mx-data/references/finance-data.md) | 精确计算读取 Excel 原始值；Markdown 可能截断或按万/亿展示，核对单位后换算。 |
| 公告、研报、新闻、政策和事件 | [妙想资讯检索](../../../mx-data/references/finance-search.md) | 定位资料，关键事实追到公告、研报或政策原件。 |
| 宏观、景气、利率、汇率和商品价格 | [妙想宏观数据](../../../mx-data/references/macro-data.md) | 明确指标或品种，检查 CSV 的频率、单位、来源及覆盖。 |
| A 股同业发现、初步横向比较 | [妙想可比公司分析](../../../mx-data/references/comparable-company.md)，按需备用 | 核对业务可比性、报告期、指标定义及财务/估值样本；自动解读只作线索。 |
| 前序来源无法取得、返回不足或存在待核验冲突的字段 | [iFinD](../../../ifind-finance-data/SKILL.md) | 只补缺项或冲突；财务/股东用 `stock`，港美股用 `global_stock`，行情用证券/指数服务，宏观用 `edb`，公告用 `news.search_notice`。 |
| 前序技能仍无覆盖或需独立交叉核对的字段 | [akshare](../../../akshare/SKILL.md) | 按“常用接口清单”或接口索引检索，再用 `get_api_doc.py` 核对参数；按需安装 `akshare`、`pandas`，优先用 `robust_fetcher.py` 重试。核对市场覆盖、字段口径、更新日期、复权与单位；关键披露事实仍以原件为准。 |

## 官方原件入口

下表用于原件核验或直接取数，实际字段以目标公司、期间对应的详情页和 PDF 为准。

| 资料类型 | 首选及备用入口 | 关键核验事项 |
|---|---|---|
| 沪市财报、公告、治理 | [上交所上市公司公告](https://www.sse.com.cn/disclosure/listedinfo/announcement/)；备用：[巨潮](https://www.cninfo.com.cn/new/index)、公司投资者关系页 | 按代码、日期和公告类型定位原件。 |
| 深市财报、公告、治理 | [深交所上市公司公告](https://www.szse.cn/disclosure/listed/notice/index.html)；备用：[巨潮](https://www.cninfo.com.cn/new/index)、公司投资者关系页 | 使用信息披露中的上市公司公告入口，核对报告期。 |
| 北交所披露 | [北交所上市公司公告](https://www.bse.cn/disclosure/vocational.html)；备用：巨潮、公司投资者关系页 | 核对上市市场和公告期间。 |
| 股价、历史市值、股本 | [上交所公司概况与成交统计](https://www.sse.com.cn/assortment/stock/list/info/company/)、[深交所行情](https://www.szse.cn/market/trend/index.html)；备用：[上交所行情报表](https://www.sse.com.cn/market/price/report/)、[深交所市场数据](https://www.szse.cn/market/periodical/index.html)、股本变动公告 | 历史市值用同日价格和当期总股本，核对送转、回购、融资及证券类别。 |
| 分红、股东、增减持 | 对应市场定期报告及分红、权益变动、回购公告；备用：公司投资者关系页 | 区分分红预案与实施，股东数据标明报告期；XBRL 摘要核对原 PDF。 |
| 同业财务、行业估值 | 同业同期间原件、[上交所行业 PE](https://www.sse.com.cn/market/stockdata/price/sh/)；备用：[深交所专题统计](https://www.szse.cn/market/subject/index.html)、适用的中证指数资料 | 统一行业分类、报告期、亏损样本及静态/滚动口径；行业 PB 序列按实际覆盖处理。 |
| 行业需求、产量、景气 | [国家统计局](https://data.stats.gov.cn/)、[工信部运行监测](https://www.miit.gov.cn/jgsj/yxj/xxfb/)；备用：主管部门、行业协会公开原始统计 | 核对行业定义和频率；行业统计作为基准，公司事实仍须公司证据。 |
| 无风险利率、股息比较 | [中债收益率曲线](https://yield.chinabond.com.cn/)；备用：[财政部收益率曲线](https://yield.chinabond.com.cn/cbweb-czb-web/czb/moreInfo?locale=cn_ZH&nameType=1) | 匹配估值日、期限、币种及到期/即期利率口径。 |
| 港股披露 | [港交所披露易](https://www.hkexnews.hk/homelcititlesearch.html)；备用：发行人投资者关系页 | A/H 股分别核对主体、准则、股本、币种和价格。 |

## 取数与核验规则

1. 查询明确市场、法定名称/代码、指标、绝对期间、财年/TTM、币种和合并范围；同口径字段合并请求。
2. 检查实际返回的实体、字段、期间、单位和完整性；摘要或片段中的关键事实核对原件后采用。
3. 按[研究交接](../research-workflow.md#研究交接)自主取数，交付查询条件、结果、来源定位、核验时间及剩余缺项；协调者核验、去重并用 `add-source` 登记最终来源，同一原件只归档一次。
4. 妙想的 `EM_API_KEY` 与共享凭据流程见[共用授权协议](../../../mx-data/references/auth_protocol.md)；各子能力共用同一用户凭据，只注入当前进程，不依赖包内默认值。iFinD 及 a-stock-data 的专用接口按各自技能配置，凭据不进入日志或报告；akshare 无需凭据，按技能说明安装并定期更新接口文档。工具列表未显示入口时按原技能检查脚本和实际返回。

## 缺项处理

| 情况 | 处理与记录 |
|---|---|
| 服务不可用或需授权 | `access-unavailable`：记录实际失败，同轮复用结果并换补充来源。动态页通过浏览器公开详情/下载入口获取；PDF 失败可重试一次后换入口，抓取空白仍须核查页面。 |
| 返回缺项、截断或口径不符 | 针对缺项补查或修正期间、范围、币种；服务不提供记 `not-offered`，与技术故障区分。 |
| 尚未披露或原件未披露 | 核对披露日及原件附注，分别记录；原件未披露记 `not-publicly-disclosed`。替代数据或假设标明身份和依据。 |
| 已有充分资料或无需补查 | 写明“已有充分数据”；影响很小的非关键字段可记 `not-material`，说明理由并结束补查。 |
| 最终仍有缺口 | 逐项记录缺项、已查结果或未查理由、替代依据和影响；降低置信度，继续完成数字评分、具体估值区间及报告发布。 |
