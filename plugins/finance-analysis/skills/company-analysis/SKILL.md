---
name: company-analysis
description: 对一家公司做多 agent 深度分析：五阶段研究管线产出 15 章可追溯报告，含证据锚定质量评分、提议—批判—修订估值评审与三情景估值。**当用户要求全面深度分析某家公司、出具公司研究报告或研究级估值报告、评估公司质量与投资风险时使用**；单点行情或财务数据取数由 a-stock-data、mx-data 技能承接，本技能不用于快速单指标查询。
compatibility: "required_tools: Bash"
---

# 公司分析

分别回答：**公司质量如何？当前价格处在什么估值位置？** 默认交付 15 章可追溯的 Markdown 报告；用户只问单项时按问题缩小范围。

## 脚本入口与调用

`<skill-root>` 为本文件所在技能目录的绝对路径，`scripts/` 相对该目录。本文 `python` 指 Python 3 解释器；从任意工作目录用 `python <skill-root>/scripts/<入口脚本> <子命令> …` 调用。

| 入口脚本 | 用途 |
|---|---|
| `scripts/company_run.py` | 创建运行、登记资料、检查及发布报告 |
| `scripts/scoring/company_scoring.py` | 评分输入预检、冻结、评审卡安装及共识汇总 |
| `scripts/valuation/company_valuation.py` | 估值输入预检、冻结、评审卡安装及估值计算/汇总 |

阶段 3、4 的 `preflight-input`、`freeze`、`install-card`、`install-critique`（估值）、`aggregate` 分别通过评分或估值入口执行；参数用 `python <skill-root>/<入口脚本> <子命令> --help` 查看。本技能仅上述三个 CLI 为入口；`scoring_consensus.py`、`valuation_consensus.py`、`valuation_calculator.py`、`evidence_contract.py`、`artifact_store.py` 是入口导入的内部模块（前两个分别位于 `scripts/scoring/`、`scripts/valuation/`，`valuation_calculator.py` 与 `valuation_consensus.py` 同目录，`evidence_contract.py`、`artifact_store.py` 位于 `scripts/`）。

## 五个阶段

1. **范围与蓝图。** 用 `python <skill-root>/scripts/company_run.py start --company-dir <绝对路径> --company <名称>` 创建 run。公司目录命名 `<工作区根>/companies/<证券简称>-<市场>-<代码>`（如 `companies/贵州茅台-SH-600519`，市场取 `SH`/`SZ`/`HK`/`US`），`--company` 始终显式传交易所官方简称。按自动生成的 `analysis/research.md` 骨架填写 15 行公司专项蓝图和六项基础预检，锁定主体、期间、币种和证券份额并复用归档原件。协调者读取[研究流程](references/research-workflow.md)；摘录估值事实前确定[规范单位](references/valuation/valuation-contract.md#估值单位)。
2. **研究与反方审视。** 按研究流程的名额优先级先分五个研究方向（研究员最高），评审名额（评分一位、估值提议与批判两位）在研究启动后创建，依依赖顺序分派 agent（类型 `finance-analysis:researcher-*`）：第一层[行业与同业](../../agents/researcher-industry.md)与[财务与现金流](../../agents/researcher-financial.md)并行，第二层[业务与护城河](../../agents/researcher-business.md)与[资本配置与股东](../../agents/researcher-capital.md)接收前层交付，第三层[风险与反证](../../agents/researcher-risk.md)汇集全部方向报告；无法分派的方向由协调者读同一 agent 文件按同一方法完成。研究员按各自交付模板把方向报告写入 run，按[取数路线](references/research/source-access.md)自主取证，协调者核验、去重和登记，形成 02–11 章底稿与估值候选，再按[反方审视 agent](../../agents/challenger.md)（类型 `finance-analysis:challenger`）审视并裁决。
3. **预检与冻结。** 按[评分契约](references/scoring/scoring-contract.md#协调者输入准备)逐维匹配事实与缺口，按[估值契约](references/valuation/valuation-contract.md#协调者输入准备)准备方法、三情景和敏感性。两边对同一事实快照运行 `preflight-input`，修正来源、结构和经济口径错误，再分别 `freeze`。正式章节在冻结后写，避免输入修正导致重写。
4. **独立评审。** 启动 [scorer](../../agents/scorer.md)（类型 `finance-analysis:scorer`）对冻结评分输入做证据锚定档位评分；启动 [valuer](../../agents/valuer.md)（类型 `finance-analysis:valuer`）出估值卡草稿，再由 [valuation-critic](../../agents/valuation-critic.md)（类型 `finance-analysis:valuation-critic`）逐项批判，valuer 在原槽位修订一次。安装顺序不可乱：评分侧直接 `install-card`；估值侧先 `install-critique`（批判工件）、待提议者修订草稿后再 `install-card`——卡一经安装即不可变。结构错误由安装前的 `preflight-card` 拦下并在原槽位修正；`install-card` 执行同样的严格校验，失败即拒绝安装。随后分别 `aggregate` 完成确定性聚合与计算；已安装卡若仍发现问题，本 run 无法修复或发布，只能新建 run 重做，原 run 保留。只从完成的共识与确定性计算读取结果。
5. **写作与交付。** 按[报告规范](references/report-format.md)勾稽正文数值、写完 15 章，完成最终结论审视。`company_run.py publish` 内含最终检查；需要提前排错时单独运行 `check`。输出为 `runs/<run-id>/reports/analysis.md` 和公司级 `reports/latest.md`；HTML 等展示版本按需使用独立发布技能。

## 关键约束

- 完整分析始终完成证据锚定评分与提议—批判—修订的估值评审；评分者、估值者与估值批判者是不同的专职子代理，都只使用冻结输入（批判者另读提议者草稿，属设计使然）；协调者和研究者不转任评审。
- 质量评分与估值独立。缺数据影响证据状态、假设和敏感性区间，仍须给数字分数与具体估值区间；补查记录不全产生警示，不阻止发布。无可核验股价时给价值区间，当前位置暂不可判定。
- 披露事实、推导、假设与结论分别标明；关键数值有单位、期间、范围、审计状态和原件定位。等值单位别名及草稿格式在原 run 处理；事实数值、倍率、币种、证券份额或经济含义实质改变才新建 run。已完成 run 保留原件和结果。
- 各章用问题小节、窄表与短列表展现完整证据链，图表按需使用；一项独立缺口一行，连接研究记录与受影响章节。具体章节、状态和交付字段以报告规范为准。

## 分析方法

02–11 章各有独立方法，执行时仍按五个研究方向分层研究，不为每章另建子代理。完整分析读取所属方向全部章节；单项问题读取相关章节及必要的依赖。共用[指标、期间、财务历史及行业适配](references/research/methods/common-metrics.md)，取数按[资料路线](references/research/source-access.md)。

| 章 | 方向 | 方法 |
|---|---|---|
| 02 | 业务与护城河 | [业务模式质量与增长引擎](references/research/methods/02-business-model.md) |
| 03 | 业务与护城河 | [护城河与竞争地位](references/research/methods/03-moat-competition.md) |
| 04 | 行业与同业 | [行业质量、前景、景气度与同业](references/research/methods/04-industry-peers.md) |
| 05 | 财务与现金流 | [五年成长质量](references/research/methods/05-growth-quality.md) |
| 06 | 财务与现金流 | [利润表与盈利能力](references/research/methods/06-income-profitability.md) |
| 07 | 财务与现金流 | [资产负债表与营运资本](references/research/methods/07-balance-sheet.md) |
| 08 | 财务与现金流 | [现金流与利润含金量](references/research/methods/08-cashflow.md) |
| 09 | 资本配置与股东 | [资本配置与治理](references/research/methods/09-capital-allocation.md) |
| 10 | 资本配置与股东 | [分红、股东结构与增减持](references/research/methods/10-shareholder-returns.md) |
| 11 | 风险与反证 | [风险、周期与反证](references/research/methods/11-risks.md) |

## 按职责读取

协调者按阶段读取流程、研究方法及契约的协调者段落；研究者只读对应方向负责的章节方法、共用口径和取数路线。评分者只读冻结输入和评分契约的“评分档位规则”“周期评估规则”“风险规则核查”“评分卡 schema”四节；估值者只读冻结输入、估值契约的“估值单位”“估值者必读（提议者）”，以及方法目录中本次候选的相关方法族。重算和 HTML 资料只在对应任务出现时读取。评分量表、估值方法目录和计算脚本保留各自的权威职责。
