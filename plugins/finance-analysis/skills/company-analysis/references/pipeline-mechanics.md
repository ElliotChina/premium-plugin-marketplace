# 管线机器机制

三个 CLI 脚本是本文件规则的唯一执行器；脚本只负责执行，人工校对与把控以本文件与两份契约为准。评分与估值的业务规则分别见[评分契约](scoring/scoring-contract.md)与[估值契约](valuation/valuation-contract.md)。

## 规范 JSON 与内容哈希

- 规范形式：`json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"`；NaN 与 Infinity 一律拒绝。
- `content_hash` ＝ 规范字节的 SHA-256。
- 自引用哈希：评分输入的 `scoring_input_hash` 与估值输入的 `valuation_input_hash`，都是**去掉自身哈希字段后整个对象**的 `content_hash`；构造时先置 `"pending"` 再回填。
- 所有工件按规范形式落盘；`status` 重放聚合与计算，并与落盘内容的规范 JSON 形式逐字节比对（键序或空白差异视为同一内容）。

## 工件不可变与原子安装

- 文件名固定白名单。评分侧 `analysis/scoring/`：`input.json`、`scorer-1.json`、`consensus.json`。估值侧 `analysis/valuation/`：`input.json`、`reviewer-1.json`、`critique.json`、`consensus-assumptions.json`、`calculation.json`、`valuation-diff.json`、`recalculation-provenance.json`、`transaction.json`。
- 安装语义：同内容重装为幂等空操作；内容不同抛 StateError 拒绝。**修订必须发生在安装之前**——先批判草稿、再修订、最后安装。已安装卡发现问题时本 run 无法修复或发布，只能新建 run 重做。
- 原子性：临时文件写入并 fsync 后以 rename/link 发布；估值侧目录一律经 `dir_fd`＋`O_NOFOLLOW` 打开，拒绝符号链接路径替换；路径含符号链接的输入文件直接拒绝。
- 终态 run（`run.json` 的 `status` ∈ completed/aborted/superseded）拒绝一切写操作。

## 事实快照与两侧绑定

- 事实记录的 15 个必填键见[共用事实字段](scoring/scoring-contract.md#共用事实字段)。
- 评分与估值的冻结输入必须同一 `fact_snapshot_id` 且 `facts` 数组逐字节一致（两侧互相校验，先冻结的一侧固定基准）。
- 已核验披露事实绑定 `sources.json` 登记来源与原件哈希；未登记来源的事实不能通过预检。

## status 自检原理

`status` 是内建验证器：重新加载全部工件 → 重放聚合与确定性计算 → 与落盘结果逐字节比对 → 校验 `transaction.json` 的哈希标记。`company_run.py publish` 内含的 `check` 调用两侧 `status` 并要求评分 `complete`、估值 `complete`/`complete-conditional`/`complete-low-confidence`/`recalculated`；另核对报告正文呈现主方法中性区间上下界、共识 `primary_range` 与确定性计算一致、精度状态（supported/conditional/low-confidence）与终值占比、情景间隔或重叠、重大交叉分歧均已按规则披露，以及报告包含且仅包含一个与共识 `summary_markdown` 逐字节一致的评分摘要块。机器检查不替代实质复核。

## 命令面

| 脚本 | 命令 | 写入工件 |
|---|---|---|
| `company_run.py` | `start`、`add-source`、`check`、`publish` | run 目录、sources.json、报告 |
| `company_scoring.py` | `preflight-input`、`freeze`、`preflight-card`、`install-card`、`aggregate`、`status` | `input.json`、`scorer-1.json`、`consensus.json` |
| `company_valuation.py` | `unit-standard`、`preflight-input`、`freeze`、`preflight-card`、`install-card`、`install-critique`、`aggregate`、`recalculate`、`status` | `input.json`、`reviewer-1.json`、`critique.json`、`consensus-assumptions.json`、`calculation.json`、`valuation-diff.json`、`recalculation-provenance.json`、`transaction.json` |

- 输出协议：`company_scoring.py` 与 `company_valuation.py` 的 stdout 为 JSON 结果，stderr 为 JSON 错误（`error_type`/`message`/明细字段）；退出码 0＝成功、2＝用法/契约/状态错误、1＝内部错误；`--debug` 附堆栈。`company_run.py` 的 stdout 为缩进 JSON 结果；出错时 stderr 为 `{"error": …}`，非零退出码即失败，不支持 `--debug`。
- 预检命令一律不写文件（干跑）；`--help` 以 JSON 输出。

