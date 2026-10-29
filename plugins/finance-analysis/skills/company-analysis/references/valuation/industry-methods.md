# 行业专用估值方法

通用现金流折现与倍数法在两类公司上会系统性失真：价值几乎全部来自尚未上市销售的在研管线，或来自精算假设下的有效业务与未来新业务。方法目录为此提供 `rnpv` 与 `embedded-value` 两个 family；单位、证据与精度规则仍按[估值契约](valuation-contract.md)，资产基础口径见[资产基础规则](asset-based-rules.md)。

## rNPV（未盈利创新药管线）

### 适用条件

- 未盈利或利润不能代表价值，价值主要由临床、监管与商业化里程碑驱动。
- 主方法：管线资产可以逐项列出成功情景下的净现金流，且各资产的失败风险可以用阶段成功率表达。
- 已商业化、现金流稳定的药企改用 DCF 或 EV/EBITDA；rNPV 只用于剩余在研资产，避免把已上市产品再按概率折一次。
- 授权首付款、里程碑与销售分成按资产归集到对应管线的现金流，不重复计入其他方法。

### 公式与字段

```
风险调整价值 = probability_of_success × ( Σ cash_flow_t ÷ (1 + discount_rate)^t + terminal_value ÷ (1 + discount_rate)^n )
price = 风险调整价值 ÷ diluted_shares
```

- `cash_flows`：成功情景下的年度净现金流（`CNY` 整体金额），长度等于 `horizon_years`，研发投入年份可为负。
- `probability_of_success`：成功情景概率，取值 `(0, 1]`；按阶段历史转化率或资产特定证据给出，来源写入 `parameter_derivation`。
- `discount_rate`：折现率必须为正，反映时间价值与系统性风险。
- `terminal_value`：显式期结束时的剩余价值（`CNY`），可为 0 或负数（专利到期、移交或处置成本）；计算方法结果必须为正。
- method_id 为 `intrinsic-price-per-share-rnpv`。

**同一风险只扣一次。** 临床或监管失败风险要么通过 `probability_of_success` 扣减，要么已包含在风险调整折现率中，不得两者同时计入。若折现率按风险调整口径给出，`probability_of_success` 应设为 1 并在 `rationale` 说明；若按阶段成功率折减，折现率只反映时间价值与系统性风险。

### 情景与敏感性

- 三情景同时调整商业化假设（峰值销售、渗透率、定价、上市时点、专利期）、阶段成功率与折现率；成功率的保守/乐观差异按阶段与适应症的证据给出，不机械加减。
- 一个方法只对应一个资产或一个明确界定的资产组合；组合内各资产分别估值后相加，不得先加总现金流再套一个组合成功率，除非组合成功率本身有依据。
- 敏感性参数取自 `cash_flow_shift`、`probability_of_success`、`discount_rate`、`terminal_value`，且网格必须包含经营参数（`cash_flow_shift` 或 `probability_of_success`）；只变折现率与终值的网格被拒绝。
- 计算器输出中性情景的 `terminal_value_share`；占比 ≥ 75% 须披露，≥ 85% 精度不得为 `supported`。

### 证据与披露

- 成功率来源：适应症、阶段与试验设计对应的历史转化率，或已核验的资产特定证据；纯经验取值须登记为假设事实并接受 `conditional`。
- 现金流推导链写明峰值销售 = 患者数 × 渗透率 × 年治疗费用，以及毛利率、销售费用率、上市年份与专利/独占期到期年份。
- 报告披露管线清单与阶段、成功率来源、折现率、终值假设与占比、摊薄股数与融资节奏、现金跑道与后续融资摊薄风险。
- rNPV 与 DCF 同属 `cashflow-intrinsic` 机制组，二者互为交叉时不构成独立证据，不得据此提高精度。

## 寿险内含价值（EV + 新业务价值）

### 适用条件

- 寿险与长期健康险为主，内含价值（EV）与新业务价值（NBV）有披露或可由精算假设复算。
- 主方法：`embedded-value`，以一年新业务价值乘以新业务倍数计入未来新业务。
- 财险公司不适用内含价值口径，改用剩余收益或股息 DCF；寿险公司的 P/EV 作为交叉方法（`price-multiple` 的 `embedded-value` basis）。

### 公式与字段

```
评估价值 = adjusted_net_worth + value_of_in_force + new_business_value × new_business_multiple
price = 评估价值 ÷ diluted_shares
```

- `adjusted_net_worth`：调整后净资产（`CNY` 整体金额），按市场价值调整可供出售资产等。
- `value_of_in_force`：有效业务价值（VIF），只覆盖存量保单。
- `new_business_value`：最近一个报告期的新业务价值（`CNY` 整体金额）。
- `new_business_multiple`：新业务倍数，必须非负；通常由同业 P/EV 反推或按新业务增长与回报期给定，不是 P/EV 本身。
- 评估价值必须为正；method_id 为 `intrinsic-price-per-share-embedded-value`。
- P/EV 交叉方法用 `multiple-embedded-value`，分母为每股内含价值（`CNY/share`）。

### 情景与敏感性

- 三情景分别调整：净资产（利率与权益市场对资产市值的影响）、VIF（折现率、死亡率/发病率、退保率、费用假设）、NBV（新单规模与新业务价值率）与新业务倍数。
- 敏感性参数取自 `adjusted_net_worth_shift`、`value_of_in_force_shift`、`new_business_value_shift`、`new_business_multiple`，网格必须包含经营参数（`value_of_in_force_shift` 或 `new_business_value_shift`）；只变净资产倍数或仅调倍数的网格被拒绝。
- 精度按通用规则判定：VIF 与 NBV 依赖未核验精算假设、情景未绑定证据或新业务倍数缺乏同业校准时降为 `conditional`。

### 证据与披露

- 优先使用已审阅或已审计的 EV/NBV 披露，注明报告期与计量假设；EV 通常按年度或半年度披露，晚于当前时点时须说明期间差与时点调整。
- VIF 对折现率与假设变更高度敏感；披露假设集、是否发生假设变更及其对 VIF 的影响。
- 报告列出评估价值三项分解、P/EV、新业务倍数及其来源，并说明 VIF（存量）与 NBV 倍数（增量）不重复计算。
- 内含价值是精算口径而非市场价值；P/EV 只作交叉校验，不把同业 P/EV 直接当作本公司合理倍数。
