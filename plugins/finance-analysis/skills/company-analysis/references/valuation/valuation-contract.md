# 估值契约（提议—批判—修订）

[方法目录](valuation-models.json)定义可执行 family、字段和公式，`company_valuation.py` 是公开入口。新运行的估值为单一提议者：估值者出卡草稿 → 估值批判者逐项挑战 → 估值者原槽位修订一次 → 安装单卡 → 确定性计算。报告数字只取确定性计算。协调者读输入准备、共用输入结构及安装聚合；估值者只读“估值单位”“估值者必读”“公司特征与可执行方法”及本次候选的相关方法族；批判者另读“批判工件”；写作者读报告发布段，增量重算段按需读取。共享机器机制（哈希、不可变、status 自检、命令面）见[管线机器机制](../pipeline-mechanics.md)。

## 估值单位

摘录估值事实前确定币种、所估证券类别及每一份额与普通股的换算关系；运行 `company_valuation.py unit-standard --currency CNY` 查看规范单位。币种用 `CNY` 等三字母代码，人民币不写 `RMB`。

| 用途 | 规范单位 | 输入数值 |
| --- | --- | --- |
| 股价、每股盈利、每股现金流、每股股息和每股分母 | `CNY/share` | 对应一股所估证券的人民币元 |
| 收入、EBIT、FCFF、FCFE、现金、债务、企业价值、SOTP 金额、rNPV 现金流、ANW/VIF/NBV | `CNY` | 人民币元的原始金额 |
| 摊薄股本 | `shares` | 与股价对应的实际股数 |
| PE、PB、EV/EBIT 等倍数 | `x` | `15` 表示 15 倍 |
| 收益率、WACC、永续增长率 | `fraction` | `0.12` 表示 12% |

其他币种用对应代码替换 `CNY`。例如 `3.2 亿元 → 320000000 CNY`、`1.25 亿股 → 125000000 shares`、`2.4 元/股 → 2.4 CNY/share`。`value` 只填换算后的十进制数，在 `methodology` 记录原值、倍率和计算；保留原材料 ID 与定位。跨币种换算还要记录汇率、日期和来源。ADR/CDR、拆股和不同股份类别须先换算到所估份额。

价格倍数和收益率法的每股分母用 `CNY/share`；企业价值倍数、DCF、SOTP 的金额分母和现金债务桥接用 `CNY`。股权 DCF 的年度 `cash_flows` 是归属普通股的整体金额（`CNY`），股息口径同样按整体金额填写；剩余收益模型的 `drivers` 为每股口径（`CNY/share`）。rNPV 的 `cash_flows` 与 `terminal_value` 是成功情景下的整体金额（`CNY`）；内含价值的 `adjusted_net_worth`、`value_of_in_force`、`new_business_value` 均为估值币种的整体金额（`CNY`），P/EV 的分母才是每股内含价值（`CNY/share`）。情景字段即使没有独立 `unit` 键，数值也按这个尺度填写。`元/股`、`人民币元/股` 与 `CNY/share` 是无倍率等值写法；`股` 与 `shares` 也等值。`万元/股`、`亿元`、`万股`、`CNY million` 等带倍率写法必须先核实并同时换算数值和单位，不能只改单位标签。新输入统一写规范单位；预检会识别等值别名并拒绝未换算的尺度。

## 协调者输入准备

- 同评分共用事实快照。逐个候选方法确认币种、所估份额、股本、可用分母、净债务/现金桥接、三情景及敏感性；按[取数路线](../research/source-access.md)补证，再选择有经济意义的可计算方法。DCF 候选在 `methods` 中声明 `input_mode`（主方法用 `drivers`，需有收入基数事实）与 `horizon_years`；驱动模式的三情景案例填写 `revenue_growth`、`operating_margin`、`sales_to_capital` 数组，长度与显式期一致。股权 DCF 候选声明 `cash_flow_type`（`fcfe` 或 `dividend`），案例填写与 `horizon_years` 等长的 `cash_flows` 整体金额；剩余收益候选的案例填写 `drivers.base_book_value_per_share_fact_id`（每股价事实）、`eps` 与 `dividend_per_share` 数组。rNPV 候选声明 `horizon_years`，案例填写与显式期等长的成功情景 `cash_flows`、成功率、折现率与终值；寿险内含价值候选填写净资产、有效业务价值、新业务价值与新业务倍数，规则见[行业专用方法](industry-methods.md)。
- 仍缺计算输入时，用已核验事实和可说明的外部基准形成数值假设：`fact_type: assumption`、`status: unverified`、`audit_status: not-applicable`，填单位、币种、期间，并在方法、来源和可比性字段写锚点、推导及限制。方法适用性、校准和禁用引用仍须指向已核验事实。
- 当前价格来自可核验行情；缺价时提供 `valuation_currency`，仍输出价值区间，当前位置和相对股价空间暂不可判定。EV 倍数缺少当前企业价值时，计算器可用冻结的股价、无倍率股数及同币种现金债务桥接反推；不满足条件时保留区间，不推断当前位置。
- 评分与估值都先 `preflight-input`，处理来源、哈希、结构和经济口径错误，再 `freeze`。冻结会复查登记原件并强制两边事实 ID 与内容相同。按候选顺序先首选、后备选；向提议者（`reviewer-1`）交付字节相同的冻结输入。

路径均为绝对路径，run 已存在且可写。用 `company_valuation.py --help` 及各子命令 `--help` 查看参数；顺序为 `preflight-input → freeze → 提议者 preflight-card → install-critique → 提议者修订并 preflight-card → install-card → aggregate → status`。`unit-standard` 在取证前运行，不写文件。

## 共用输入结构

所有 JSON 为对象，未知顶层键拒绝；全部数值事实与假设用十进制定点字符串（bool 与 float 一律拒绝，保证确定性）。精确 family、情景及 3×3 网格形状见方法目录。

| 输入 | schema 与精确顶层键 |
|---|---|
| 事实快照 | `company-analysis-fact-snapshot-v1`；`schema_version, fact_snapshot_id, fact_snapshot_hash, facts`。事实的 15 个键及值域见[共用事实字段](../scoring/scoring-contract.md#共用事实字段)，不另维护副本。 |
| 市场快照 | `company-analysis-market-snapshot-v1`；`schema_version, market_snapshot_id, market`。`market` 至少有 `valuation_currency` 或 `current_price`；前者为 ISO 币种，其他记录键为 `value, currency, unit, date`，股价须同币种。 |
| 方法候选 | `company-analysis-valuation-method-candidates-v1`；`schema_version, methods`。非空公司专项方法列表受方法目录约束。 |
| 冻结输入 | `company-analysis-valuation-input-v1`；`schema_version, fact_snapshot_id, market_snapshot_id, model_version, calculator_version, method_catalog_version, valuation_input_hash, facts, market, methods`。哈希为去掉自身字段后规范 JSON 的 SHA-256。 |

## 估值者必读（提议者）

只用自己的 ID、冻结输入及相关方法族，独立判断每个候选方法的适用性、正常化、三情景、历史/同业校准、反向估值、敏感性和失效条件。证据引用冻结事实 ID，区分披露与假设；不浏览、扩展事实。最终价值由计算器给出，卡片不提交目标价、公允价或最终每股价值。

提议者的工作分两段：先按上述要求出**草稿**；批判工件安装后，逐条处理批判项——采纳的在受影响条目的 `rationale` 写明调整依据，不采纳的逐条给出反驳理由（也写入相应 `rationale` 或 `sensitivity_factors` 的说明），在原槽位修订草稿。**至多一轮实质修订**，修订必须发生在安装之前（工件不可变），不得新增事实、不得放宽自身的禁用条件。

method_id 按方法目录 `method_id_vocabulary` 命名，语法 `<indicator>[-<basis>][-<variant>]`，各段取词表 token：`indicator` 表价值指标（`multiple`、`yield`、`intrinsic-price-per-share`），`basis` 表分母或价值基础（如 `eps`、`book`、`revenue`、`ebitda`、`ebit`、`fcf`、`fcfe`、`dividend`、`nav`、`ffo`、`residual-income`、`rnpv`、`embedded-value`），`variant` 表期间或口径（`ttm`、`fy`、`forward`、`normalized`、`midcycle`、`liquidation`）。带连字符的 basis token（`residual-income`、`embedded-value`）按最长匹配解析。四条治理规则：同一方法在不同角色下用同一 ID，不因主/交叉身份换名；禁止公司名、数据源与流程词；`basis` 用单 token；同 `basis` 出现歧义时用期间或口径 `variant` 区分。非规范写法会被 `preflight-card` 与 `install-card` 拒绝。

评审卡 — schema `company-analysis-valuation-reviewer-card-v2`；键恰为 `schema_version, reviewer_id, fact_snapshot_id, market_snapshot_id, valuation_input_hash, model_id, calculator_version, method_catalog_version, method_judgments, normalizations, scenario_parameters, calibrations, reverse_valuation, parameter_derivation, sensitivity_factors, invalidation_conditions`。各列表项键分别为：

  - `method_judgments`: `method_id, applicable, preferred_role, evidence_fact_ids, rationale, disable_conditions`；禁用项为 `code, reason, evidence_fact_ids`。
  - `normalizations`: `parameter_id, kind, value, lower, upper, unit, evidence_fact_ids, rationale`。
  - `scenario_parameters`: `method_id, method`。
  - `calibrations`: `method_id, historical, peers, evidence_fact_ids, rationale`。
  - `reverse_valuation`: `method_id, fixed_parameters, implied_variable, implied_horizon_years, feasibility, evidence_fact_ids, invalidation_condition`。`fixed_parameters` 为 `{parameter, value, unit}` 列表且非空，写明固定了哪些变量；`implied_variable` 为 `{name, value, unit}`，不得与固定变量重名；`implied_horizon_years` 为正数；`feasibility` 为 `{history_comparison, capacity_constraint, market_size, verdict}`，`verdict ∈ plausible / stretched / implausible`。不得把一组可能解释写成市场唯一预期。
  - `parameter_derivation`: `method_id, parameter, value, formula, inputs, evidence_fact_ids`；`inputs` 为非空映射（代入参数名 → 数值字符串）。每个冻结方法至少一行，同一方法的 `(method_id, parameter)` 不得重复，用于审计关键参数从哪里来、按什么公式代入。
  - `sensitivity_factors`: `method_id, factor, reason, evidence_fact_ids`。
  - `invalidation_conditions`: `method_id, code, condition, evidence_fact_ids`。

`normalizations.kind` 与数值形状、三情景键、情景排序、规范单位及 3×3 敏感性网格均按方法目录填写：price/yield/企业倍数情景的 `denominator` 必填；dcf-fcff、dcf-equity、residual-income、rnpv、embedded-value、sotp 情景只接受显式上下界（无单点情景）且 `sensitivity.base_case` 必填；SOTP 同一案例全部组件须共用一个 `value_type`；收益率法的指标区间排序与价格倍数相反。**情景只要求有序，不要求首尾衔接**：保守情景低于中性、中性低于乐观，四个外侧锚点（保守下界、中性下界、中性上界、乐观上界；收益率族方向相反）严格递增即通过；相邻情景之间允许间隔或重叠，计算器输出 `scenario_layout` 记录幅度，报告须在 13 章说明成因。不得为消除间隔或重叠反向调整 FCFF、WACC、增长率或组件值。各情景 `denominator` 不一致须在 `rationale` 说明理由，不属于格式错误。所有候选都提供可计算情景，供确定性选择。每个冻结方法在上述各按方法列表中恰好一条；方法结构字段与冻结输入逐一相等；每个方法提案在卡校验时实跑一次计算器验证可算。

DCF 方法在冻结输入中声明 `input_mode`（`drivers` 或 `fcff`）与正整数 `horizon_years`。`drivers` 模式由计算器按 `revenue_t = revenue_0 × Π(1+growth_i)`、`EBIT_t = revenue_t × margin_t`、`NOPAT_t = EBIT_t × (1−tax_rate)`、`reinvestment_t = (revenue_t − revenue_{t−1}) ÷ sales_to_capital_t`、`FCFF_t = NOPAT_t − reinvestment_t` 生成现金流，案例含 `drivers.base_revenue_fact_id`、`revenue_growth`、`operating_margin`、`tax_rate`、`sales_to_capital`，各数组长度须等于 `horizon_years`；主方法 DCF 优先使用该模式，仅在再投资假设可单独复核时才用 `fcff` 显式列表。`fcff` 模式接受显式年度 `fcff` 列表。案例级 `terminal_mode` 默认 `reinvestment-consistent`（`TV_n = NOPAT_n × (1+g) × (1 − g ÷ ROIC_T) ÷ (WACC − g)`，需 `terminal_nopat` 或驱动路径得到 NOPAT_n，且 `terminal_roic` 必填）；`gordon`（`TV_n = FCFF_n × (1+g) ÷ (WACC − g)`）仅在再投资假设已单独说明时使用，且不接受 `terminal_nopat`/`terminal_roic`；`finite`（`TV_n = terminal_value`，可为 0 或负数以计入移交、复垦等处置成本）用于矿山、收费公路、特许经营等有限期资产，必须显式给出 `terminal_value`，不读取 `terminal_growth`。增长型终值要求 `wacc > terminal_growth > −1`；有限期模式只要求正的 `wacc`。有限期 DCF 的敏感性网格固定为 `terminal_value` 与 `wacc`。

`dcf-equity` 按股权现金流直接折现到每股，不做企业价值桥接。方法声明 `cash_flow_type`（`fcfe` 或 `dividend`），method_id 的 basis token 必须与之一致（`intrinsic-price-per-share-fcfe` / `intrinsic-price-per-share-dividend`）。案例键为 `cash_flows`、`cost_of_equity`、`terminal_growth`（可选 `evidence_fact_ids`），`cash_flows` 为与 `horizon_years` 等长的归属普通股整体金额；股息口径不接受负股息。终值 `TV_n = CF_n × (1+g) ÷ (Ke − g)`，`price = equity_value ÷ diluted_shares`，要求 `Ke > terminal_growth > −1`。融资需求（外部股权发行、摊薄）由 `cash_flows` 或 `diluted_shares_fact_id` 反映，不得忽略。敏感性参数取自 `cash_flow_shift`、`cost_of_equity`、`terminal_growth`，且必须包含 `cash_flow_shift`。

`residual-income` 按每股价口径计算。案例键为 `drivers`（恰为 `base_book_value_per_share_fact_id`、`eps`、`dividend_per_share`）、`cost_of_equity`、`terminal_growth`、`terminal_roe`（可选 `evidence_fact_ids`）；两个数组长度等于 `horizon_years`，股息不得为负。清洁盈余滚动 `B_t = B_{t−1} + EPS_t − DPS_t`，`RI_t = EPS_t − Ke × B_{t−1}`，终值 `TV_n = (terminal_roe − Ke) × B_n ÷ (Ke − g)`，价值 `B_0 + Σ RI_t ÷ (1+Ke)^t + TV_n ÷ (1+Ke)^n`。账面价值必须保持为正，否则拒绝计算。`terminal_roe < Ke` 记 `terminal-roe-below-cost-of-equity`，触发 `economic-inconsistency` 并将精度降为 `conditional`。敏感性参数取自 `eps_shift`、`terminal_roe`、`cost_of_equity`、`terminal_growth`，且必须包含经营参数（`eps_shift` 或 `terminal_roe`）。

`rnpv` 用于未盈利创新药管线。方法声明 `horizon_years` 与 `diluted_shares_fact_id`；案例键为 `cash_flows`、`probability_of_success`、`discount_rate`、`terminal_value`（可选 `evidence_fact_ids`），`cash_flows` 为与显式期等长的成功情景净现金流，可为负；成功率取 `(0, 1]`，折现率必须为正，终值可为 0 或负数（专利到期、移交或处置成本），风险调整价值必须为正。价值 `PoS × (Σ CF_t ÷ (1+r)^t + TV_n ÷ (1+r)^n)`，`price = 价值 ÷ diluted_shares`。**同一临床或监管风险只扣一次**：要么体现在 `probability_of_success`，要么已包含在折现率中，不得同时计入。敏感性参数取自 `cash_flow_shift`、`probability_of_success`、`discount_rate`、`terminal_value`，且必须包含经营参数（`cash_flow_shift` 或 `probability_of_success`）。规则见[行业专用方法](industry-methods.md)。

`embedded-value` 用于寿险。方法声明 `diluted_shares_fact_id`，无 `horizon_years`；案例键为 `adjusted_net_worth`、`value_of_in_force`、`new_business_value`、`new_business_multiple`（可选 `evidence_fact_ids`），前三项为估值币种的整体金额，新业务倍数不得为负。评估价值 `ANW + VIF + NBV × 新业务倍数`，`price = 评估价值 ÷ diluted_shares`；评估价值必须为正。P/EV 交叉方法用 `price-multiple` 的 `embedded-value` basis（`multiple-embedded-value`）。敏感性参数取自 `adjusted_net_worth_shift`、`value_of_in_force_shift`、`new_business_value_shift`、`new_business_multiple`，且必须包含经营参数（`value_of_in_force_shift` 或 `new_business_value_shift`）。规则见[行业专用方法](industry-methods.md)。

`disable_conditions` 只写估值日已发生且由已核验事实证明的禁用条件；有禁用项时同时填 `applicable=false`、`preferred_role=exclude`。未来可能发生的监控条件写在 `invalidation_conditions`，不能提前禁用当前方法。

交卡前在不可变目录之外运行 `company_valuation.py preflight-card --run-dir RUN --card FILE`，修正到 `status: ready`。格式、遗漏网格或引用错误由提议者在原槽位修正。

## 批判工件（company-analysis-valuation-critique-v1）

估值批判者读冻结输入、方法目录、估值契约相关节与协调者提供的**草稿卡路径**，产出批判工件；不产替代卡、不计算价格、不扩展证据。键恰为 `schema_version, valuation_input_hash, critic_id, target_card, items`：

| 键 | 规则 |
|---|---|
| `schema_version` | `company-analysis-valuation-critique-v1` |
| `valuation_input_hash` | 必须与冻结输入一致 |
| `critic_id` | 非空；批判者是独立专职子代理，不与提议者同一人 |
| `target_card` | 必须等于所批判草稿卡的 `reviewer_id`（aggregate 强制核对，不一致即拒绝） |
| `items` | 列表，可为空（无实质问题） |

每条 item 键恰为 `target, issue_type, argument, counter_evidence_fact_ids, suggested_revision`：`target` 指向卡内字段路径（如 `method_judgments[multiple-eps-fy].applicable`、`scenario_parameters[multiple-eps-ttm].method.scenarios.neutral.range`）；`issue_type` 枚举 `method-applicability / normalization / scenario-boundary / sensitivity-coverage / invalidation-gap / evidence-link / derivation-gap / basis-mismatch / economic-inconsistency`；`argument` 非空；`counter_evidence_fact_ids` 引用冻结**已核验**事实（结构类问题可为空列表）；`suggested_revision` 非空。批判优先攻击：方法适用性误判、正常化参数依据、情景边界经济含义、敏感性网格缺口、失效条件缺失、证据引用不实、推导链跳步、method_id 口径与 family 不配对、情景参数与经济逻辑相悖。

协调者运行 `install-critique --file` 安装到 `critique.json`；校验失败退回批判者修正。安装估值卡前，协调者核对批判工件的 `target_card` 与所批判草稿一致、安装卡确为该草稿的修订版。**aggregate 强制要求 critique.json 已安装**——批判环结构上不可跳过。批判与提议者不同人；无批判名额时协调者读批判者 agent 文件自审并在工件 `critic_id` 注明。

## 协调者安装与聚合（单卡确定性选择）

- 安装顺序：批判工件先装（`install-critique`），提议者修订草稿后 `install-card`，再 `aggregate`。
- 方法选择算法（`aggregate_reviewer_card`，按冻结候选序）：
  1. 禁用并集：`applicable=false` 且 `preferred_role=exclude` 的 `disable_conditions` 全部生效，剔除对应方法。
  2. 主方法 ＝ 首个 `applicable` 且 `preferred_role=primary` 的方法；不存在则回退到首个 `applicable` 方法并记 `primary_role_fallback: true`（精度降为 `low-confidence`）。
  3. 交叉方法 ＝ 其余 `applicable` 且 `preferred_role=cross-check` 的方法，按候选序至多两个。
  4. 无任何可用方法 → `evidence-insufficient`（待修复状态：修方法或有依据的输入假设，不得编造）。
- 精度三态：`supported`（关键参数均有已核验事实绑定、无主方法回退、交叉方法独立且分歧不重大、终值占比 < 85%、无经济一致性告警）、`conditional`（依赖未核验假设、情景边界未绑定证据、终值占比 ≥ 85%、交叉方法不独立或分歧重大、DCF 经济一致性告警）、`low-confidence`（主方法回退，或交叉方法与主方法方向相反）。`precision_reasons` 逐条记录触发原因：`assumption-input`、`unbound-scenario-evidence`、`terminal-value-share`、`non-independent-cross-check`、`cross-check-divergence`、`economic-inconsistency`、`primary-role-fallback`、`cross-check-direction-conflict`。情景证据为可选键，只能引用已核验事实；绑定即承诺区间有证据支撑，未绑定则视为推断。
- 经济一致性：DCF 计算器输出 `consistency_flags`。稳定期 `ROIC_T < WACC` 记 `terminal-roic-below-wacc`，显式期最后一年增速与 `terminal_growth` 偏离超过 2 个百分点记 `growth-not-converged`；剩余收益模型 `terminal_roe < cost_of_equity` 记 `terminal-roe-below-cost-of-equity`。任一存在即触发 `economic-inconsistency`，精度降为 `conditional`。`ROIC_T ≤ terminal_growth` 或 `WACC ≤ terminal_growth` 直接拒绝，不进入计算；剩余收益的 `Ke ≤ terminal_growth` 同样拒绝。
- 结论强度：`supported` 可给明确位置判断与方向表述；`conditional` 可给位置判断，须同时写明依赖的关键假设与改判条件，不使用“低估/高估”的绝对措辞；`low-confidence` 只呈现参考区间，正文声明“区间不具备方向判断力”，不得给方向结论。
- 终值占比：`calculation.json` 的 DCF 与 rNPV 方法输出 `terminal_value_share`；≥75% 报告须披露“终值占比”，≥85% 精度不得为 `supported`。
- 交叉分歧：`cross_check_divergence` 计算主方法与交叉方法中性区间的重叠、中枢价差比与方向冲突；`is_material`（无重叠或价差比 > 40%）时报告须在 14 章给出分歧诊断。`independence` 按方法族机制组判定（`market-multiples`、`cashflow-intrinsic`、`asset-revaluation` 等）；主方法与交叉方法同组时标为 `non-independent`，不得据此提高精度。
- 情景参数与正常化直通提议者卡（无跨人合并）；`consensus-assumptions.json` 为 `company-analysis-valuation-consensus-assumptions-v2` schema，含 `primary_role_fallback`、`critique_hash`（批判工件哈希，写入共识供审计）、`precision_reasons`、`cross_check_divergence`、`independence` 与 `parameter_derivation`（推导链直通，供报告 13 章使用），不含投票与离散度字段。反向估值审计按 `implied_variable.name` 排序。
- `aggregate` 内完成确定性计算并写 `consensus-assumptions.json`、`calculation.json`、`transaction.json`（有基线时另写 `valuation-diff.json`）；事务绑定各工件规范内容哈希。数值、币种和单位遵循估值契约；最终区间由计算器给出。
- `status` 状态机：`not-frozen` → `incomplete`（卡未安装）→ `critique-missing`（卡有效但批判工件未装）→ `ready`（卡与批判齐备未聚合）→ `complete` / `complete-conditional` / `complete-low-confidence`（共识落盘且重放一致）；`evidence-insufficient` 为待修复；任何校验失败为 `invalid`。重算 run 的状态为 `recalculated`。

## 报告读取与发布

| 可发布状态 | 展示要求 |
|---|---|
| `complete` / `recalculated`，`precision_state: supported` | 证据支持的估值区间 |
| `complete-conditional`，`precision_state: conditional` | 条件性估值区间，列明关键假设与改判条件 |
| `complete-low-confidence`，`precision_state: low-confidence` | 参考区间，正文声明“区间不具备方向判断力” |

三级都须经 `status` 重算验证，具有非空 `consensus_hash, calculation_hash, transaction_hash`；重算还需 `diff_hash, provenance_hash`。聚合后已有验证且工件未变时直接读取；工件改变、报错或最终发布时重新验证，最终 `company_run.py publish` 内含此检查。其余状态包括 `ready` 均非完整报告终态。

报告读取 `consensus-assumptions.json` 的主/交叉方法、禁用并集、假设、失效条件、`precision_reasons`、`cross_check_divergence`、`independence` 与 `parameter_derivation`，读取 `calculation.json` 的情景、每股桥接、敏感性、`scenario_layout`、`scenario_membership`、`terminal_value_share`、`consistency_flags`、五档位置及空间；有基线时读 `valuation-diff.json`。只为披露假设依据读取冻结 `input.json`，不从评审卡或批判卡手算。`primary_role_fallback` 为 true 或依赖假设输入时如实披露限制。缺股价时保留区间和边界价格，当前位置与空间为 null。数据缺失不删除评分或估值。

**报告必须得出估值**：`check`/`publish` 把无可交付区间的估值状态（含 `evidence-insufficient`）记为错误。因此提议者不得把全部候选方法禁用排除；证据不足以支撑某方法参数时，用假设事实（`fact_type: assumption`）承接并接受 `conditional` 或 `low-confidence` 精度披露，而不是放弃该方法。正文呈现各方法按序排列的三情景区间与主方法五档位置；存在间隔或重叠时如实标注，并披露终值占比、重大交叉分歧和精度状态；`low-confidence` 不得给方向结论。01 结论章的估值位置数字后须紧跟一句当前位置判读（落点与离边界距离），见[报告规范](../report-format.md)。

这些生成文件及最后写入的 `transaction.json` 均在本 run 的 `analysis/valuation/`，结构由程序维护，无需人工填写。事务绑定各工件规范内容 SHA-256。`aggregate` 的基线输入、共识、计算三个参数须同时提供，并由程序认证；基线共识须达到 `consensus`＋`supported`。

## 公司特征与可执行方法

先依据盈利能力、资本强度、周期性、金融属性、分部差异和数据充分性选择候选方法，拒绝负分母、周期峰谷、会计失真或缺乏经济意义的方法。当前方法目录执行 `price-multiple`、`yield`、`enterprise-multiple`、`dcf-fcff`、`dcf-equity`、`residual-income`、`rnpv`、`embedded-value` 和 `sotp`。方法目录为每个 family 声明 `allowed_basis`（`sotp` 另列可选 basis `nav`），method_id 的 basis token 必须落在允许集合内；`dcf-fcff` 与普通 `sotp` 不携带 basis token，`dcf-equity` 的 basis token 必须等于 `cash_flow_type`，`residual-income` 固定携带 `residual-income` token，`rnpv` 固定携带 `rnpv` token，`embedded-value` 固定携带 `embedded-value` token。资产基础价值（调整后 NAV、清算价值）不新增 family：金额经 `sotp` 汇总，method_id 用可选 basis `nav`，清算口径再加 `liquidation` 变体，规则见[资产基础规则](asset-based-rules.md)；未盈利创新药与寿险的口径见[行业专用方法](industry-methods.md)。口径不配对的写法在预检即被拒绝。

| 公司特征 | 主方法 | 交叉方法 |
|---|---|---|
| 稳定盈利、分红政策与资本需求匹配 | 股息 DCF（`cash_flow_type: dividend`） | PE、反向估值 |
| 盈利但分红不代表分配能力 | 股权 DCF（`cash_flow_type: fcfe`） | EV/EBIT、FCFF DCF |
| 非金融、现金流可预测 | FCFF DCF | EV/EBITDA、反向估值 |
| 银行 | 剩余收益（RIM） | P/B、股息率 |
| 寿险 | 内含价值（EV + 新业务价值） | P/EV、P/B |
| 保险（非寿险） | 剩余收益或股息 DCF | P/B、EV/EBITDA |
| 未盈利创新药、管线驱动 | rNPV | 现金/管线价值、同业授权交易对价 |
| 重资产、周期 | 正常化 EV/EBIT 或中周期 DCF | P/B、NAV |
| 多业务集团 / 控股平台 | SOTP | 集团整体倍数 |
| 资产持有型（地产、资源） | 调整后 NAV | P/NAV、清算价值 |
| 矿山、收费公路、特许经营 | 有限期 DCF（`terminal_mode: finite`） | EV/EBITDA、NAV |

DDM、FCFE、RIM 与 FCFF DCF 在一致假设下可相互推导，不构成独立证据；它们与 `dcf-fcff` 同属 `cashflow-intrinsic` 机制组。rNPV 是概率加权后的现金流折现，同样归入该组，与 DCF 互为交叉时按非独立处理。内含价值同属 `cashflow-intrinsic`，而 P/EV 属 `market-multiples`，两者交叉视为独立。

校准必须引用公司正常化历史、同期可比公司，以及情景中的可持续增长、回报率、利润率、现金转换和资产负债表风险。PE/ROE 只能辅助筛查。超额现金、债务、租赁、少数股东和优先索偿依目录桥接，不能重复计入。保守/乐观边界是情景边界，不是目标价格。

辅助交叉检查可计算 `PE/ROE = 正常化 PE ÷ ROE 百分点数`；例如 15 倍 PE 和 15% ROE 得 1.0，1.0–1.5 只是粗筛区间。价值桥接（`总市值 − 超额现金 + 有息负债 + 重大租赁负债 + 其他类债务索偿`）只能作为 denominator 的推导依据写入 `rationale`，不得用作价格倍数的 denominator；method_id 只写一个 basis token（如 `multiple-eps-normalized`），不得写“调整后”等修饰词。只扣超额现金，重大少数股东权益及优先股须单独处理，避免债务或租赁重复计算；金融机构通常不适合该桥接。周期性强、杠杆高、早期或业务集中的公司，三情景边界应有经济依据并充分反映不确定性。DCF、相对估值、企业价值和每股结果的可执行公式以方法目录及计算器为准。

分部加总估值只在分部披露足够时使用；各分部采用适当方法，并扣除总部费用、少数股东权益和净债务。相对估值与 DCF 的可执行公式及每股换算均以方法目录及计算器为准；当前股价未经核验时只输出价值区间，不计算相对股价空间。

## 增量重算

仅在增量重算时读取本节。`recalculate` 写入新可写 run，不复制评审/批判卡、不改源 run。`--source-run-dir` 指向已通过 `status` 验证的 `complete + supported` 聚合 run；CLI 再验其卡、批判工件、共识、计算及事务。`--baseline-input`、`--consensus-assumptions` 须逐字节匹配源工件；可选 `--baseline-calculation` 也须匹配，供差异比较。

新市场快照只替换市场事实、生成新 input hash，共识参数保持不变；估值币种不得改变（`valuation_currency` 或股价币种与源 run 不同即拒绝），换币种须另建 run。修改参数须提供 overrides：schema `company-analysis-valuation-overrides-v1`，精确键为 `schema_version, reason, author, created_at, evidence_fact_ids, changed_parameters`；变更项为 `path, value`，仅指向既有数值叶，证据引用基线 verified fact。

命令参数用 `recalculate --help` 查询。新 run 自动生成输入、共识、计算、差异、`recalculation-provenance.json` 与事务，记录源 run 目录名（`source_run_id`）、源哈希、override 记录和理由；只有显式差异基线才记录 `source_calculation_hash`，否则为 null。共识中的 `primary_range` 按新计算重写为确定性中性区间。`status` 会重新认证源 run：同目录下该 run 必须仍存在、状态仍为 `complete + supported`，其 input/consensus/calculation 哈希与 provenance 记录一致，否则重算 run 转 `invalid`。须达到 `recalculated` 及上面的发布门槛，篡改的自洽共识不能充当源运行。

