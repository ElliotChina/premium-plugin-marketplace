# 评分契约（五轴证据锚定）

新运行使用 `company-analysis-rubric-v2.0` 量表、证据锚定评分卡（v4）与共识（v4）：评分者在每个维度选出一个锚点档位，分数、核心质量分与风险动作全部由脚本按冻结规则确定性计算，不存在自由 0–100 打分、多人聚合或卡内自由上限。旧 v1 量表、`grade_band` 等级、置信度公式、`vetoes`/`cap_score` 均已废除，不做旧格式兼容。协调者读输入准备及安装聚合；评分者只读“评分档位规则”“周期评估规则”“风险规则核查”与“评分卡 schema”四节；共享机器机制（哈希、不可变、status 自检、命令面）见[管线机器机制](../pipeline-mechanics.md)。

量表五轴：`industry-quality`（6 维）、`business-quality`（6 维）、`financial-quality`（5 维）、`governance-capital-allocation`（5 维）、`future-prospects`（5 维），共 27 维、各轴权重和 100。只有 business-quality、financial-quality、governance-capital-allocation 三个核心轴进入公司核心质量分 Q；行业质量与未来前景是独立判断轴，不计入 Q。

## 协调者输入准备

1. 用[量表](scoring-rubric.json)逐维比较已核验事实和基准：只有补齐后可能改变该维度判断或证据强度的字段才记为重大缺口。收入、利润、现金等已有事实可直接支持对应财务维度，不以所有行业内部指标齐全为条件。补证按[取数路线](../research/source-access.md)执行。

   维度证据的默认来源（协调者按此分配各方向交付模板的输入提示，跨表维度合并多方向证据）：

   | 量表轴（维度数） | 主要证据来源 |
   |---|---|
   | industry-quality（6） | 行业与同业（04 章）：行业价格与供给、政策与监管量化、同业比较 |
   | business-quality（6） | 业务与护城河（02–03 章）；capital-cash-cycle 兼用财务（07–08 章） |
   | financial-quality（5） | 财务与现金流（05–08 章） |
   | governance-capital-allocation（5） | 资本配置与股东（09–10 章） |
   | future-prospects（5） | 行业与同业（04 章）与业务（02–03 章）的前景证据 |
   | cycle_assessment（3 组件） | 行业与同业（04 章）与风险（11 章）的景气证据 |

   风险与反证（11 章）供各维 `counterevidence` 与六项风险规则核查；审计意见类证据见资本配置（09 章）。
2. 保存 `company-analysis-evidence-coverage-v2` 对象，含事实快照 ID、量表版本及每个维度、每个周期组件、每条风险规则恰好一条记录。记录键为 `dimension_id, assessment, evidence_fact_ids, missing_evidence, supplementation_status, supplementation_notes`。维度与组件终态为 `supported` 或 `inferred`；无法补齐时为 `unassessable`，须逐项列缺口并给出 `completed`、`exhausted`、`not-cost-effective` 或 `not-publicly-available` 等补查终态；风险检查额外允许 `unresolved`。`supported` 要求非空证据且补查为 `not-needed` 或 `completed`；`inferred` 必须有非空缺口。
3. 保存 `assessment_context` 对象，键恰为 `as_of`（YYYY-MM-DD）、`history_period`、`forecast_period`、`industry_profile`、`company_scope`、`segment_basis`。`segment_basis` 每项含 `scope, metric_basis, aggregation_basis, evidence_fact_ids, rationale`，声明分部口径——它是评分摘要与报告可比性的锚。
4. 对同一快照运行评分和估值 `preflight-input`，处理来源登记、原件哈希、结构、单位、期间、小数及必填字段错误。若 `coverage_warnings` 提示全部维度无法评估或大范围重复证据，逐维复核映射；警示本身不改变分数、不阻止有真实缺口的运行。
5. `company_scoring.py freeze --evidence-coverage FILE --assessment-context FILE` 冻结输入并计算 `scoring_input_hash`。已核验披露事实绑定登记来源；两边快照 ID 和完整事实必须相同。向一个隔离子代理交付 `analysis/scoring/input.json`（`scorer-1`）。

事实与来源处理遵循[研究流程](../research-workflow.md)。下面的共用事实格式也供估值输入使用。

## 共用事实字段

`analysis/scoring/input.json` 中的新事实使用以下可审计结构：

```json
{
  "fact_id": "<稳定的事实 ID>",
  "metric": "<指标或定性证据名称>",
  "value": "<JSON 标量值>",
  "unit": "<单位或 null>",
  "currency": "CNY",
  "period": "<事实对应期间>",
  "consolidation_scope": "<合并、母公司、分部或其他明确范围>",
  "source_material_id": "<来源文件或资料 ID>",
  "source_locator": "<页码、章节、附注、表格或时间戳>",
  "audit_status": "audited",
  "methodology": "<直接披露或推导方法>",
  "comparability": "<期间与同业可比性说明>",
  "fact_type": "disclosed",
  "replaces_fact_id": null,
  "status": "verified"
}
```

新事实有上述 15 个必填键。历史事实还可含 `content_hash`，仍可读取；整份快照已有内容哈希，新事实无需填写该字段。其他未知键或缺失键会被拒绝。`fact_id`、`metric`、`period`、`consolidation_scope`、`source_material_id`、`source_locator`、`methodology` 和 `comparability` 为非空字符串。`value` 为非空字符串——数值事实用十进制字符串，定性事实用文本；或 null（仅 `status: unverified` 的事实允许 null）。布尔与 JSON 数值一律拒绝——评分与估值共享同一份快照，估值计算按十进制字符串解析。`unit` 和 `currency` 为非空字符串或 null；有币种时使用三个大写字母。`audit_status` 取 `audited`、`unaudited` 或 `not-applicable`；`fact_type` 取 `disclosed`、`derived` 或 `assumption`；`replaces_fact_id` 为 null，或同一事实快照中另一事实的非空 ID；`status` 取 `verified` 或 `unverified`。

定性事实使用字符串值，单位和币种为 null。推导事实须说明方法。分析假设可以冻结（`fact_type: assumption` 必为 `unverified`）；作为档位、风险规则触发和分数上限依据的事实须标为 `verified`（唯一例外：`evidence_requirement: stress-scenario-allowed` 的规则允许引用压力情景假设，见下）。推断档位仍可依据冻结事实与明确的经济推断给出。完整事实内容纳入规范化的 `scoring_input_hash`；不能默认填造来源、捏造事实或使用冻结输入外的依据。

## 评分档位规则

评分者只做一件事：对每个量表维度，把证据与五个锚点的**文字描述**对照，选出最匹配的一档。不做锚点间插值；跨公司分辨率由 27 个维度×5 档的组合与权重承载。

- `band` 只能取该维冻结锚点键 `0/25/50/75/100` 之一，且选择必须由对应锚点描述实质支持；引用的 `evidence_fact_ids`、期间与口径写进 `rationale`。
- `50` 只在证据实质好坏参半（锚点 50 的描述成立）时选择；缺数据本身不是选 50 的理由。
- 证据同时部分匹配两档时，选更接近的一档，并在 `ambiguous_with` 标注相邻档（只允许 `|差|＝25` 的相邻档；单档明确匹配时为 null）。跨档维度进入共识的敏感性区间并使核心轴评估为 `provisional`，不改档位本身。
- 证据三态 `evidence_status`：
  - `supported`——非空且全部 `verified` 的 `evidence_fact_ids`，无 `data_gaps`；
  - `inferred`——非空已核验证据加非空 `data_gaps`，依据冻结事实、业务机制与可比经验作最佳估计；**缺口改变证据状态与敏感性，不改变档位的数学中心**；若唯一理由是缺字段，保持档位不变；
  - `unassessable`——`band` 为 null、`data_gaps` 非空；该维度所在轴分为 null，评估状态为 `unavailable`。缺数据到无法评估时如实标注，不硬猜档位。
- `weight` 必须等于冻结量表值；评分者不改权重。卡内没有任何自由上限或否决机制。

## 周期评估规则

`cycle_assessment` 是独立于五轴的景气模块，三个组件 `demand-orders`（35）、`price-margin`（35）、`inventory-capacity`（30）：

- `applicability: applicable`——给出 `phase`（trough/recovery/expansion/overheating/contraction，证据不足时 unclear）与 `direction`（improving/stable/deteriorating/unclear），并对三个组件各给一个锚点档位；任一组件档位为 null 时景气强度分为 null。
- `applicability: weak-cycle`——弱周期行业：`phase` 与 `direction` 必须为 `not-applicable`，`components` 必须为空列表，强度分为 null。写清弱周期依据，不硬套周期模板。
- `applicability: unassessable`——`phase` 与 `direction` 必须为 `unclear`，组件仍须逐个给出档位或 null 并列缺口；强度分为 null。
- 周期判断不改任何轴分；它与 `phase_guide`/`direction_guide` 一起用于 04/11 章的景气表述与前景轴的交叉印证。

## 风险规则核查

六项公司级风险规则冻结在量表 `risk_rules` 中，评分者逐条给出 `triggered` / `not-triggered` / `unresolved`：

| rule_id | 触发时动作 |
|---|---|
| confirmed-material-misstatement | reporting-reliability 档位压 0；公司级 restricted |
| confirmed-shareholder-expropriation | shareholder-alignment 档位压 0；公司级 restricted |
| uncovered-liquidity-gap | solvency-liquidity 档位压 0；公司级 restricted |
| core-license-loss | business-resilience 档位压 0；公司级 restricted |
| stress-covenant-breach | solvency-liquidity 档位压 25；公司级 attention |
| material-reporting-uncertainty | reporting-reliability 档位压 25；公司级 attention |

- `triggered` 必须附非空 `evidence_fact_ids` 与理由；五条 `verified-facts` 规则的证据必须全部已核验，`stress-scenario-allowed` 的 stress-covenant-breach 允许引用压力情景假设。
- `unresolved` 写明卡点；任何 unresolved 规则把风险状态压为 `unassessed`（除非已有 restricted/attention）。
- 上限由脚本确定性执行：`min(档位, 维度上限)`，再 `min(轴分, 轴上限)`；已触发规则的出处记录在各维度 `applied_rules`。公司级状态优先级 restricted > attention > unassessed > clear。缺数据本身不能触发规则；规则只能由不利经济或治理事实触发。

## 评分卡 schema（company-analysis-scorecard-v4）

卡级键恰为 `schema_version, scorer_id, rubric_version, fact_snapshot_id, scoring_input_hash, model_id, ratings, cycle_assessment, risk_assessments`，其中四个标识字段必须与冻结输入一致。每条 rating 键恰为：

| 键 | 规则 |
|---|---|
| `dimension_id` | 覆盖量表每个维度恰好一次 |
| `band` | 0/25/50/75/100 之一；unassessable 时为 null |
| `ambiguous_with` | null 或相邻档（\|差\|＝25）；unassessable 时必须为 null |
| `weight` | 等于冻结量表权重 |
| `evidence_status` | `supported`、`inferred` 或 `unassessable` |
| `evidence_fact_ids` | 引用快照内已核验事实；supported/inferred 时非空 |
| `rationale` | 非空；含口径、期间与锚点对照依据 |
| `counterevidence` | 字符串（最强反证，可为空串） |
| `data_gaps` | inferred/unassessable 时非空；supported 时必须为空 |

`cycle_assessment` 键恰为 `applicability, phase, direction, rationale, components`；组件键恰为 `component_id, band, evidence_fact_ids, rationale, data_gaps`，覆盖三个周期组件恰好一次。`risk_assessments` 每项键恰为 `rule_id, status, evidence_fact_ids, rationale`，覆盖六条规则恰好一次。

交卡前在不可变目录之外运行 `company_scoring.py preflight-card --run-dir RUN --card FILE`，修正到 `status: ready` 后交回。卡内只允许上表键集，多余键直接拒绝。

## 协调者安装与聚合（确定性计算）

- `install-card` 安装后运行 `aggregate`。聚合算法（`aggregate_scorecard`，纯函数）：
  - 维度分 ＝ `min(band, 已触发维度上限)`；unassessable 维度为 null。
  - 轴分 ＝ `min( Σ(weight × band) ÷ 100 , Σ(weight × 有效档位) ÷ 100 , 已触发轴上限 )`；任一维度 unassessable 时轴分为 null。
  - 核心质量分 `Q = B^0.4 × F^0.4 × G^0.2`（`core-quality-geometric-v1`，Decimal 精度 50、ROUND_HALF_UP、保存 1 位小数；等价于 `(B² × F² × G)^(1/5)`）。任一核心轴为 0 时 Q＝0，不做几何平均的下界保护；任一核心轴为 null 时 Q＝null，不重归一化。
  - 敏感性区间：对每个 `ambiguous_with` 维度取替代档重算轴分与 Q（上限规则不变），输出全部情景 Q 的 `[low, high]`；无跨档维度或 Q 为 null 时为 null。
  - 风险状态与评估状态按上节规则推导；景气强度分由组件权重与档位计算（任一组件 unassessable 或非 applicable 时为 null）。
  - 输出 `company-analysis-scoring-consensus-v4`，顶层键 `schema_version, rubric_version, fact_snapshot_id, scoring_input_hash, model_id, axis_scores, core_quality, sensitivity_range, risk_state, assessment_state, cycle_assessment, risk_assessments, summary_markdown`；轴含 `axis_id, raw_score, effective_score, dimensions`，维度含 `dimension_id, raw_score, effective_score, applied_rules`。
  - `summary_markdown` 由 `render_scoring_summary` 纯函数生成，用 `<!-- scoring-summary:start -->` 与 `<!-- scoring-summary:end -->` 定界；`check` 用同一函数对正文块逐字节复核。
- `status` 状态机：`not-frozen`（未冻结）→ `incomplete`（评分卡未安装）→ `ready`（卡有效未聚合）→ `complete`（consensus 落盘且重放一致）；任何阶段校验失败为 `invalid`。幂等复用规则见[管线机器机制](../pipeline-mechanics.md)。
- 工件保存在本 run 的 `analysis/scoring/`，完成后不可修改。

## 评分解释与报告呈现

评分维度、权重、原始指标、基准、锚点和适用性以 `scoring-rubric.json` 为准。分别呈现五个独立判断轴、核心质量分 Q、敏感性区间、景气模块与风险状态；估值位置单独呈现。行业质量与未来前景不计入 Q，当前景气不能替代长期前景，也不把这些轴平均成综合推荐分——**正文没有 0–100 的综合“总分”，只有 Q 与其敏感性区间**。

报告从完成的 `analysis/scoring/consensus.json` 引用各轴分数、Q、敏感性区间、风险状态与评估状态，不手算；正文包含且仅包含一个 `summary_markdown` 摘要块（`check` 强制）。每个维度可追溯档位、权重、证据事实、依据与 `applied_rules`。跨档维度如实呈现“证据跨两档、取更接近档”及敏感性区间含义，并写明改判条件。**档位之间的差异才是实质差异**：轴分由确定性计算给出，不把同一档位内的微小轴分差解释成实质差距。`inferred` 项写出已知事实、缺失证据与推断依据；`unassessable` 维度使所在轴分与 Q 如实为 null 并说明补齐条件。已触发的风险规则单列其证据、上限动作与公司级状态，不能被其他高分掩盖；缺数据只影响证据状态，不能自动降低档位或触发规则。

报告中的估值数字只取自已验证的 `analysis/valuation/calculation.json` 和估值状态，不从估值评审卡手算区间，也不把估值位置转成质量分。结论章只上提会改变总体判断、估值边界或风险结论的评分信息。
