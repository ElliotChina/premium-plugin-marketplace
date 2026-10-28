# 评分契约（证据锚定）

新运行使用 `company-analysis-rubric-v1.1` 量表、证据锚定评分卡与共识：评分者在每个维度选出一个锚点档位，分数由脚本按权重确定性计算，不存在自由 0–100 打分与多人聚合。协调者读输入准备及安装聚合；评分者只读“评分档位规则”与“评分卡 schema”两节；共享机器机制（哈希、不可变、status 自检、命令面）见[管线机器机制](../pipeline-mechanics.md)。

## 协调者输入准备

1. 用[量表](scoring-rubric-v1.json)逐维比较已核验事实和基准：只有补齐后可能改变该维度判断或证据强度的字段才记为重大缺口。收入、利润、现金等已有事实可直接支持对应财务维度，不以所有行业内部指标齐全为条件。补证按[取数路线](../research/source-access.md)执行。

   维度证据的默认来源（协调者按此分配各方向交付模板的输入提示，跨表维度合并多方向证据）：

   | 量表轴（维度数） | 主要证据来源 |
   |---|---|
   | industry-quality（7）、industry-outlook（4）、cycle（3） | 行业与同业（04 章）：行业价格与供给、政策与监管量化、同业比较含自由现金流率 |
   | business-model（8） | 业务与护城河（02–03 章）；cash-conversion 与 capital-intensity 兼用财务（07–08 章） |
   | company-quality（7） | business-model-quality、moat-position ← 业务（02–03）；growth-quality、profitability-returns、cash-flow-quality、balance-sheet ← 财务（05–08）；capital-allocation-governance ← 资本配置（09–10） |

   风险与反证（11 章）供各维 `counterevidence` 与 `vetoes`；审计意见类 veto 的事实见资本配置（09 章）。
2. 保存 `company-analysis-evidence-coverage-v1` 对象，含事实快照 ID、量表版本及每个维度恰好一条记录。记录键为 `dimension_id, assessment, evidence_fact_ids, missing_evidence, supplementation_status, supplementation_notes`。终态为 `direct-sufficient` 或 `inference-required`；后者须逐项列缺口、非空补查说明和 `completed`、`exhausted` 或 `not-publicly-available` 等补查终态，不能留下 `pending`。
3. 对同一快照运行评分和估值 `preflight-input`，处理来源登记、原件哈希、结构、单位、期间、小数及必填字段错误。若 `coverage_warnings` 提示全部维度推断或大范围重复证据，逐维复核映射；警示本身不改变分数、不阻止有真实缺口的运行。
4. `company_scoring.py freeze --evidence-coverage FILE` 冻结输入并计算 `scoring_input_hash`。已核验披露事实绑定登记来源；两边快照 ID 和完整事实必须相同。向一个隔离子代理交付 `analysis/scoring/input.json`（`scorer-1`）。

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

新事实有上述 15 个必填键。历史事实还可含 `content_hash`，仍可读取；整份快照已有内容哈希，新事实无需填写该字段。其他未知键或缺失键会被拒绝。`fact_id`、`metric`、`period`、`consolidation_scope`、`source_material_id`、`source_locator`、`methodology` 和 `comparability` 为非空字符串。`value` 为非空十进制字符串，或 null（仅 `status: unverified` 的事实允许 null）；布尔与 JSON 数值一律拒绝——评分与估值共享同一份快照，估值计算按十进制字符串解析。`unit` 和 `currency` 为非空字符串或 null；有币种时使用三个大写字母。`audit_status` 取 `audited`、`unaudited` 或 `not-applicable`；`fact_type` 取 `disclosed`、`derived` 或 `assumption`；`replaces_fact_id` 为 null，或同一事实快照中另一事实的非空 ID；`status` 取 `verified` 或 `unverified`。

定性事实使用字符串值，单位和币种为 null。推导事实须说明方法。分析假设可以冻结；作为档位、否决和分数上限依据的事实须标为 `verified`。推断档位仍可依据冻结事实与明确的经济推断给出。完整事实内容纳入规范化的 `scoring_input_hash`；不能默认填造来源、捏造事实或使用冻结输入外的依据。

## 评分档位规则

评分者只做一件事：对每个量表维度，把证据与五个锚点的**文字描述**对照，选出最匹配的一档。不做锚点间插值；跨公司分辨率由 29 个维度×5 档的组合与权重承载。

- `band` 只能取该维冻结锚点键 `0/25/50/75/100` 之一，且选择必须由对应锚点描述实质支持；引用的 `evidence_fact_ids`、期间与口径写进 `rationale`。
- `50` 只在证据实质好坏参半（锚点 50 的描述成立）时选择；缺数据本身不是选 50 的理由。
- 证据同时部分匹配两档时，选更接近的一档，并在 `ambiguous_with` 标注相邻档（只允许 `|差|＝25` 的相邻档；单档明确匹配时为 null）。跨档维度会列入共识的 `ambiguous_dimensions` 警示，不改分数。
- 缺重大证据时用 `evidence_status: "inferred"` 并逐项写 `data_gaps`，依据冻结事实、业务机制与可比经验作最佳估计——**缺口改变证据状态与置信度，不改变档位的数学中心**；若唯一理由是缺字段，保持档位不变。
- `verified` 档位要求非空且全部 `verified` 的 `evidence_fact_ids`，且不得带 `data_gaps`；`inferred` 档位必须有非空 `data_gaps`，可引用零个或多个已核验事实。
- 否决与上限：`vetoes` 引用已核验的不利经济或治理事实；`cap_score` 非 null 时必须附 veto；缺客户、同业、周期或单位经济性数据本身不能触发上限。
- `weight` 必须等于冻结量表值；评分者不改权重。

## 评分卡 schema（company-analysis-scorecard-v3）

卡级键恰为 `schema_version, scorer_id, rubric_version, fact_snapshot_id, scoring_input_hash, model_id, ratings`，其中四个标识字段必须与冻结输入一致。每条 rating 键恰为：

| 键 | 规则 |
|---|---|
| `dimension_id` | 覆盖量表每个维度恰好一次 |
| `band` | 枚举 0/25/50/75/100，等于该维锚点键 |
| `ambiguous_with` | null 或相邻档（\|差\|＝25） |
| `weight` | 等于冻结量表权重 |
| `evidence_status` | `verified` 或 `inferred` |
| `evidence_fact_ids` | 引用快照内事实；verified 时非空全核验 |
| `rationale` | 非空；含口径、期间与锚点对照依据 |
| `counterevidence` | 字符串列表（最强反证） |
| `data_gaps` | inferred 时非空；verified 时必须为空 |
| `vetoes` | 每项 `{code, reason, evidence_fact_ids}`，证据非空全核验 |
| `cap_score` | null 或 0–100；非 null 必须有 veto |

交卡前在不可变目录之外运行 `company_scoring.py preflight-card --run-dir RUN --card FILE`，修正到 `status: ready` 后交回。卡内只允许上表键集，多余键直接拒绝。

## 协调者安装与聚合（确定性计算）

- `install-card` 安装后运行 `aggregate`。聚合算法（`aggregate_scorecard_v3`，纯函数）：
  - 维度分 ＝ 档位值 `band`（cap 不在维度级生效）。
  - 轴分 ＝ `min( Σ(weight × band) ÷ Σweight , 轴内最小 cap_score )`；轴内权重和恒为 100；有 cap 时 `cap_provenance` 记录出处，最严格上限生效、不能被平均抵消。
  - 置信度 ＝ `100 − 0.5 × Σ(inferred 维度权重)`（权重百分点；全部推断时最低 50）。
  - `vetoes` 按身份归并并带出处；`data_gaps` 原样保留。
  - `ambiguous_dimensions`：全部跨档维度的全局警示列表（axis_id、dimension_id、band、ambiguous_with），排序稳定。
  - 输出 `company-analysis-scoring-consensus-v3`，顶层键 `schema_version, scoring_input_hash, dimensions, axes, ambiguous_dimensions`；维度含 `band/ambiguous_with/score/grade_band/evidence_status/evidence_fact_ids/data_gaps/vetoes/caps`，轴含 `uncapped_score/cap_score/cap_provenance/score/grade_band/direct_evidence_percent/inference_share_percent/inference_confidence_penalty/confidence`。
- `status` 状态机：`not-frozen`（未冻结）→ `incomplete`（评分卡未安装）→ `ready`（卡有效未聚合）→ `complete`（consensus 落盘且重放一致）；任何阶段校验失败为 `invalid`。幂等复用规则见[管线机器机制](../pipeline-mechanics.md)。
- 工件保存在本 run 的 `analysis/scoring/`，完成后不可修改。

## 评分解释与报告呈现

评分维度、权重、原始指标、基准、锚点和适用性以 `scoring-rubric-v1.json` 为准。分别呈现行业质量、未来 3–5 年行业前景、当前景气、业务模式质量和公司质量；估值位置单独呈现。行业质量不计入公司质量，当前景气不能替代长期前景，也不把这些轴平均成综合推荐分。七档等级依次为“很差、较差、偏弱、中等、良好、优秀、卓越”，边界由程序给出（35/50/60/70/80/90）。

报告从完成的 `analysis/scoring/consensus.json` 引用各独立判断轴的分数、等级、覆盖率、直接证据比例、推断比例、置信度及否决/上限，不手算总分。每个维度可追溯档位、权重、证据事实和依据；`ambiguous_dimensions` 中的维度如实呈现“证据跨两档、取更接近档”并写明改判条件。**档位之间的差异才是实质差异**：轴分由确定性计算给出，不把同一档位内的微小轴分差解释成实质差距；临近等级边界时说明边界属性。推断项写出已知事实、缺失证据、推断依据和置信度影响。已核验重大否决或上限因素单列，不能被其他高分掩盖。缺数据只影响证据状态和置信度，不能自动降低档位或设置上限。

报告中的估值数字只取自已验证的 `analysis/valuation/calculation.json` 和估值状态，不从估值评审卡手算区间，也不把估值位置转成质量分。结论章只上提会改变总体判断、估值边界或风险结论的评分信息。

