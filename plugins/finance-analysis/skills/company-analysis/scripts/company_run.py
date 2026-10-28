#!/usr/bin/env python3
"""Small file workflow around the independent scoring and valuation calculators."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import NoReturn

_SCRIPTS_ROOT = Path(__file__).resolve().parent
for _subdir in ("scoring", "valuation"):
    _subdir_path = str(_SCRIPTS_ROOT / _subdir)
    if _subdir_path not in sys.path:
        sys.path.insert(0, _subdir_path)

import company_scoring
import company_valuation
import evidence_contract
import valuation_consensus


CHAPTERS = (
    "独立结论轴、估值与监控", "业务模式质量与增长引擎", "护城河与竞争地位",
    "行业质量、前景、景气度与同业", "五年成长质量", "利润表与盈利能力",
    "资产负债表与营运资本", "现金流与利润含金量", "资本配置与治理",
    "分红、股东结构与增减持", "风险、周期与反证", "估值方法选择",
    "三情景估值指标区间", "动态交叉验证", "分析范围与数据说明",
)
CORE_COVERAGE = (
    ("C01", "五年营业收入年均增速", "05"),
    ("C02", "五年归母利润年均增速", "05"),
    ("C03", "五年归母净资产年均增速", "05"),
    ("C04", "五年总市值年均增速", "05"),
    ("C05", "现金覆盖短期、长期及其他有息债务", "07"),
    ("C06", "主要资产与负债项目分布", "07"),
    ("C07", "应收账款占年营收及变化", "07"),
    ("C08", "销售商品提供劳务收现额除以收入", "08"),
    ("C09", "经营现金流除以归母净利润", "08"),
    ("C10", "三年累计经营现金流除以累计归母净利润", "08"),
    ("C11", "收入、归母利润与ROE趋势", "05–06"),
    ("C12", "主业现金流及其占比", "06–08"),
    ("C13", "毛利率与净利率的同行比较", "06"),
    ("C14", "逐年分红金额与每股分红", "10"),
    ("C15", "股息率及计算口径", "10"),
    ("C16", "十大流通股东及持股占比", "10"),
    ("C17", "股东人数与人均持股金额", "10"),
    ("C18", "回购、大股东与高管增减持", "09–10"),
    ("C19", "营业收入相对总市值", "12–14"),
    ("C20", "归母净利润相对总市值", "12–14"),
    ("C21", "归母净资产与市净率", "12–14"),
    ("C22", "市盈率的行业与历史比较", "12–14"),
    ("C23", "市净率的行业与历史比较", "12–14"),
    ("C24", "ROE与行业ROE比较", "12–14"),
    ("C25", "PR与调整后PE交叉检查", "12–14"),
    ("C26", "现金流折现与三情景敏感性", "12–14"),
    ("C27", "赛道供需、竞争格局与前景", "04"),
    ("C28", "同行市值、ROE、毛利率与净利率比较", "04"),
)
TERMINAL = {"completed", "aborted", "superseded"}
STATUS_LINE = re.compile(r"(?m)^状态[：:]\s*(已完成|结论受限|不适用)\s*$")
CHAPTER_LINE = re.compile(r"(?m)^##\s+(\d{2})\s+(.+?)\s*$")
SOURCE_BRACKET = re.compile(r"\[([^\]\n]+)\]")
SOURCE_TOKEN = re.compile(r"(?<![A-Za-z0-9])S(?:[0-9a-f]{12}|[1-9][0-9]*)(?![A-Za-z0-9])")
SOURCE_RANGE = re.compile(r"S[1-9][0-9]*\s*[-–—~至]\s*(?:S)?[1-9][0-9]*")
SIMPLE_RECONCILIATION = re.compile(
    r"(?<!\d)(\d+(?:\.\d+)?)\s*([+＋−－–-])\s*(\d+(?:\.\d+)?)\s*[=＝]\s*(\d+(?:\.\d+)?)"
)


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ValueError(f"invalid usage: {message}")


def _range_bound_present(body: str, bound: str) -> bool:
    value = Decimal(bound)
    return bound in body or format(value.normalize(), "f") in body


def _valuation_report_consistency(consensus: dict, calculation: dict, body: str) -> list[str]:
    """Cross-check the report text against the deterministic valuation artifacts."""
    errors: list[str] = []
    primary_method_id = consensus.get("primary_method_id")
    try:
        expected_range = valuation_consensus.expected_primary_range(calculation, primary_method_id)
    except (ValueError, StopIteration, KeyError, TypeError) as exc:
        return [f"估值 primary_range 无法复核：{exc}"]
    if consensus.get("primary_range") != expected_range:
        errors.append("consensus primary_range 与确定性计算不一致")
    if not _range_bound_present(body, str(expected_range["lower"])):
        errors.append(f"报告正文缺少主方法中性区间下界 {expected_range['lower']}")
    if not _range_bound_present(body, str(expected_range["upper"])):
        errors.append(f"报告正文缺少主方法中性区间上界 {expected_range['upper']}")
    if consensus.get("publication_precision_state") == "indicative" and not (
        "推断估值区间" in body or "indicative" in body
    ):
        errors.append("估值精度为 indicative；报告必须披露推断估值区间性质")
    return errors


def _json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        stream.write(data)
        temporary = Path(stream.name)
    os.replace(temporary, path)


def _copy_atomic(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("wb", dir=destination.parent, delete=False) as stream:
        with source.open("rb") as original:
            shutil.copyfileobj(original, stream)
        temporary = Path(stream.name)
    os.replace(temporary, destination)


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _research_template(company: str) -> str:
    rows = "\n".join(f"| {number:02d} | {title} | 待填写 | 待填写 |" for number, title in enumerate(CHAPTERS, 1))
    coverage = "\n".join(
        f"| {item_id} | {topic} | {chapters} | 待核对 | 待填写 |"
        for item_id, topic, chapters in CORE_COVERAGE
    )
    return f"""# {company}研究检查表

## 分析边界与基础预检

| 项目 | 已核验口径、来源或待补内容 |
|---|---|
| 公司及证券类别、上市地 | 待填写 |
| 估值日、投资期限、数据截止日 | 待填写 |
| 审计年报、最新财报与合并范围 | 待填写 |
| 币种、单位、股本及每股口径 | 待填写 |
| 五年历史和最新核心数据 | 待填写 |
| 三张报表勾稽与可比性 | 待填写 |

先核对这些项目；已知错误先修正，缺失项记入下方缺口表，再展开正文。估值输入使用 `company_valuation.py unit-standard` 给出的标准单位。

## 报告蓝图

在取数前填写各章公司专项问题、适用性与主要比较基准；不得预填分数或估值结论。01 结论章的裁决与改判条件在评分和估值完成后回填；15 范围章在输入冻结时即可定稿。

| 章 | 研究问题 | 公司专项重点与取数方向 | 比较基准/适用性 |
|---|---|---|---|
{rows}

## 核心指标覆盖

逐项标为“已展示”“缺口”或“不适用”，最后一列填写正文位置、对应缺口编号或不适用理由。缺少资料不妨碍评分、估值和发布，但不能让指标无声消失；一个项目包含多项指标时逐项交代。

| 编号 | 指标与比较 | 建议章节 | 状态 | 正文位置、缺口编号或不适用理由 |
|---|---|---|---|---|
{coverage}

## 关键数值勾稽

写正文前列出会影响结论的派生数值及代入数，至少核对收入拆分、增长率、现金与有息债务、现金流比率和每股估值；没有可比口径时说明原因。正文出现新的派生数值时补到这里，发布前逐项与正文核对。

| 指标与期间 | 公式及代入数 | 结果、单位与来源 | 正文位置与核对结果 |
|---|---|---|---|

## 研究交接

共用原件先由协调者登记；五个研究方向按来源优先级取数和补证，形成候选事实与来源定位。名额允许时由子代理执行；无法创建时由协调者按相同角色方法完成，在“执行者与原因”列记录。协调者核验并登记最终采用的来源、处理冲突。复杂公司按需增加专项任务时，在下表增一行，并注明所属方向和执行者；未拆分时保留默认五行，行序即交接顺序：行业与同业、财务与现金流可并行启动，业务与护城河、资本配置与股东随后，风险与反证最后汇总。

| 研究主题 | 执行者与原因 | 候选事实及来源定位 | 计算、初步判断与反例 | 剩余缺口及交接处理 |
|---|---|---|---|---|
| 行业与同业 | 待填写 | 待填写 | 待填写 | 待填写 |
| 财务与现金流 | 待填写 | 待填写 | 待填写 | 待填写 |
| 业务与护城河 | 待填写 | 待填写 | 待填写 | 待填写 |
| 资本配置与股东 | 待填写 | 待填写 | 待填写 | 待填写 |
| 风险与反证 | 待填写 | 待填写 | 待填写 | 待填写 |

## 数据缺口与补查

每个独立事实缺口一行。记录实际查过的来源与结果；未继续查询时说明理由。未取得资料仍继续评分和估值，用推断及置信度反映限制。报告相应章节使用同一编号列示缺口与影响。

| 编号 | 字段、期间、口径 | 影响章节和结论 | 已查来源、结果或未查理由 | 替代依据与置信度影响 |
|---|---|---|---|---|

## 冻结前反方审视

执行者与方式：待填写。可由独立子代理审视；名额不足时由协调者按同一方法自审并标明。正式章节和输入冻结前，记录最可能改变评分或估值的 1–3 个主张，给出具体反证或替代解释，并写明采纳情况及补证、修正结果。

| 主张或估值假设 | 最强反证与来源 | 对评分或估值的影响 | 裁决及冻结前处理 |
|---|---|---|---|

## 研究中的修正

仅记录改变主体、口径、事实、评分或估值判断的修正；格式和单位别名错误在冻结前预检修复。

## 最终结论审视

完成评分与估值评审和 15 章正文后，核对支持与反对证据、分数与估值区间、缺口与置信度、结论强度及推翻条件。记录审视后的报告修订；实质事实错误须按冻结规则另建 run。

| 审视项目 | 发现及依据 | 报告修订或保留理由 |
|---|---|---|
"""


def start(args: argparse.Namespace) -> dict:
    company_dir = Path(args.company_dir).expanduser().resolve()
    company_dir.mkdir(parents=True, exist_ok=True)
    (company_dir / "sources").mkdir(exist_ok=True)
    (company_dir / "reports").mkdir(exist_ok=True)
    sources = company_dir / "sources.json"
    if not sources.exists():
        _write_json(sources, {"sources": []})
    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", run_id):
        raise ValueError("run id must be a short filename-safe identifier")
    run_dir = company_dir / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "analysis").mkdir()
    (run_dir / "reports").mkdir()
    (run_dir / "staging").mkdir()
    company = args.company or company_dir.name
    _write_json(run_dir / "run.json", {
        "run_id": run_id, "company": company, "status": "active",
        "source_contract": evidence_contract.SOURCE_CONTRACT,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    (run_dir / "analysis" / "research.md").write_text(_research_template(company), encoding="utf-8")
    return {"run_dir": str(run_dir), "research": str(run_dir / "analysis" / "research.md"),
            "sources": str(sources), "report_draft": str(run_dir / "staging" / "analysis.md")}


def add_source(args: argparse.Namespace) -> dict:
    company_dir = Path(args.company_dir).expanduser().resolve()
    manifest = company_dir / "sources.json"
    if not manifest.is_file():
        raise ValueError("company sources.json is missing; start a run first")
    if not args.file and not args.url:
        raise ValueError("provide --file or --url")
    source = Path(args.file).expanduser().resolve() if args.file else None
    if source and not source.is_file():
        raise ValueError("source file does not exist")
    digest = _sha(source) if source else hashlib.sha256(
        f"{args.url}\n{args.period}\n{args.locator}".encode("utf-8")
    ).hexdigest()
    source_id = "S" + digest[:12]
    data = _json(manifest)
    entries = data.get("sources")
    if not isinstance(entries, list):
        raise ValueError("sources.json requires a sources list")
    existing = next((item for item in entries if isinstance(item, dict) and item.get("id") == source_id), None)
    if existing:
        if source and existing.get("sha256") != digest:
            raise ValueError("source id collision")
        audit = evidence_contract.audit_source_ids(manifest, [source_id])
        restored = False
        stored = existing.get("file")
        if audit["errors"] and source and isinstance(stored, str):
            target = (company_dir / stored).resolve()
            if target.parent == company_dir / "sources" and not target.exists():
                _copy_atomic(source, target)
                audit = evidence_contract.audit_source_ids(manifest, [source_id])
                restored = True
        if audit["errors"]:
            raise ValueError("; ".join(audit["errors"]))
        return {"source": existing, "already_recorded": True, "restored": restored}
    stored = None
    if source:
        try:
            stored = str(source.relative_to(company_dir))
        except ValueError:
            stored_path = company_dir / "sources" / (source_id + source.suffix.lower())
            stored_path.parent.mkdir(exist_ok=True)
            if stored_path.exists():
                if _sha(stored_path) != digest:
                    raise ValueError("source id collision")
            else:
                _copy_atomic(source, stored_path)
            stored = str(stored_path.relative_to(company_dir))
    entry = {"id": source_id, "title": args.title or (source.name if source else args.url),
             "publisher": args.publisher, "period": args.period, "url": args.url,
             "locator": args.locator, "file": stored, "sha256": digest if source else None,
             "recorded_at": datetime.now(timezone.utc).isoformat()}
    entries.append(entry)
    _write_json(manifest, data)
    return {"source": entry, "already_recorded": False}


def _report_source_ids(body: str) -> tuple[list[str], list[str]]:
    """Accept separate or grouped source citations; reject ambiguous ranges."""
    cited: set[str] = set()
    errors: list[str] = []
    for bracket in SOURCE_BRACKET.findall(body):
        cited.update(SOURCE_TOKEN.findall(bracket))
        if SOURCE_RANGE.search(bracket):
            errors.append(f"来源范围引用 [{bracket}] 请逐项列出编号")
    return sorted(cited), errors


def check(args: argparse.Namespace) -> dict:
    run_dir = Path(args.run_dir).expanduser().resolve()
    metadata = _json(run_dir / "run.json")
    report = Path(args.report).expanduser().resolve()
    body = report.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    if not re.search(r"(?m)^#\s+.+", body):
        errors.append("缺少报告标题")
    matches = list(CHAPTER_LINE.finditer(body))
    if [int(m.group(1)) for m in matches] != list(range(1, 16)):
        errors.append("需要按 01–15 顺序设置独立二级章节")
    elif len({m.group(2).strip() for m in matches}) != 15:
        errors.append("01–15 章需有各自可区分的标题")
    states = {"已完成": 0, "结论受限": 0, "不适用": 0}
    if len(matches) == 15:
        for index, match in enumerate(matches):
            chapter = body[match.end(): matches[index + 1].start() if index < 14 else len(body)]
            found = STATUS_LINE.search(chapter)
            if not found:
                errors.append(f"第 {index + 1:02d} 章缺少状态")
                continue
            states[found.group(1)] += 1
            if found.group(1) == "结论受限" and not re.search(r"(?m)^###\s+缺口与影响\s*$", chapter):
                errors.append(f"第 {index + 1:02d} 章缺少逐项缺口与影响表")
            if found.group(1) == "结论受限" and not re.search(r"(?m)^\|\s*G\d{2}-\d{2}\s*\|", chapter):
                errors.append(f"第 {index + 1:02d} 章缺口表缺少独立编号行")
            if found.group(1) == "不适用" and "替代" not in chapter:
                warnings.append(f"第 {index + 1:02d} 章请说明替代检查")
    if "来源清单" not in body:
        errors.append("缺少来源清单")
    if "覆盖率" not in body:
        errors.append("缺少覆盖率核对")
    count_line = re.search(
        r"已完成[：:]\s*(\d+)\s*[；;]\s*结论受限[：:]\s*(\d+)\s*[；;]\s*不适用[：:]\s*(\d+)", body
    )
    if not count_line:
        errors.append("覆盖率核对须列出已完成、结论受限、不适用的章数")
    elif [int(value) for value in count_line.groups()] != list(states.values()):
        errors.append("覆盖率计数与逐章状态不一致")
    if "待填写" in body or "待分析" in body:
        errors.append("报告仍有未完成占位符")
    research = run_dir / "analysis" / "research.md"
    if not research.is_file():
        warnings.append("研究检查表缺失")
    else:
        research_text = research.read_text(encoding="utf-8")
        if "待填写" in research_text:
            warnings.append("研究检查表仍有待填写项；请核对基础数据与逐项补查")
        report_gaps = set(re.findall(r"\bG\d{2}-\d{2}\b", body))
        research_gaps = set(re.findall(r"\bG\d{2}-\d{2}\b", research_text))
        registered_gaps = {
            match.group(1) for match in re.finditer(r"(?m)^\|\s*(G\d{2}-\d{2})\s*\|", research_text)
        }
        if report_gaps - research_gaps:
            warnings.append("报告部分缺口尚未对应研究检查表：" + ", ".join(sorted(report_gaps - research_gaps)))
        for line in research_text.splitlines():
            if re.match(r"^\|\s*G\d{2}-\d{2}\s*\|", line):
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) not in (5, 6) or any(not cell or cell == "待填写" for cell in cells):
                    warnings.append(f"缺口 {cells[0]} 的补查记录不完整")
        if "## 核心指标覆盖" in research_text:
            coverage_rows = {}
            for line in research_text.splitlines():
                if re.match(r"^\|\s*C\d{2}\s*\|", line):
                    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                    if len(cells) == 5:
                        coverage_rows[cells[0]] = cells
            for item_id, _, _ in CORE_COVERAGE:
                cells = coverage_rows.get(item_id)
                if cells is None or cells[3] not in {"已展示", "缺口", "不适用"} or not cells[4] or cells[4] == "待填写":
                    warnings.append(f"核心指标 {item_id} 尚未明确展示、缺口或不适用状态")
                elif cells[3] == "缺口":
                    gap_ids = set(re.findall(r"\bG\d{2}-\d{2}\b", cells[4]))
                    if not gap_ids or not gap_ids <= registered_gaps or not gap_ids <= report_gaps:
                        warnings.append(f"核心指标 {item_id} 的缺口未同时对应研究检查表和报告")
        if "## 关键数值勾稽" in research_text:
            number_section = research_text.split("## 关键数值勾稽", 1)[1].split("\n## ", 1)[0]
            number_rows = "\n".join(
                line for line in number_section.splitlines()
                if line.startswith("|") and not re.match(r"^\|\s*(指标与期间|[-: ])", line)
            )
            if not number_rows:
                warnings.append("关键数值勾稽表尚未记录计算与正文核对")
            for match in SIMPLE_RECONCILIATION.finditer(number_rows):
                left, operation, right, result = match.groups()
                calculated = Decimal(left) + Decimal(right) if operation in {"+", "＋"} else Decimal(left) - Decimal(right)
                if abs(calculated - Decimal(result)) > Decimal("0.02"):
                    warnings.append(f"关键数值勾稽不一致：{match.group(0)}")
    sources = run_dir.parent.parent / "sources.json"
    sources_missing = not sources.is_file()
    if not sources_missing:
        try:
            if not _json(sources).get("sources"):
                warnings.append("来源清单尚未记录原件")
        except (OSError, ValueError) as exc:
            errors.append(f"来源清单文件无法读取：{exc}")
    cited_sources, citation_errors = _report_source_ids(body)
    errors.extend(citation_errors)
    fact_sources: list[str] = []
    verified_sources: set[str] = set()
    if metadata.get("source_contract") == evidence_contract.SOURCE_CONTRACT:
        frozen_facts: list[list] = []
        for kind in ("scoring", "valuation"):
            frozen = run_dir / "analysis" / kind / "input.json"
            if frozen.is_file():
                try:
                    facts = _json(frozen).get("facts")
                    if not isinstance(facts, list):
                        raise ValueError("facts must be a list")
                    ids = evidence_contract.referenced_fact_source_ids(facts)
                    verified_sources.update(evidence_contract.verified_fact_source_ids(facts))
                except (OSError, ValueError, KeyError, TypeError) as exc:
                    errors.append(f"{kind} 冻结事实无法核对：{exc}")
                else:
                    frozen_facts.append(facts)
                    fact_sources.extend(ids)
        if len(frozen_facts) == 2 and (
            evidence_contract.canonical_json_bytes(frozen_facts[0])
            != evidence_contract.canonical_json_bytes(frozen_facts[1])
        ):
            errors.append("评分与估值冻结事实内容不一致")
    else:
        errors.append("run.json source_contract 必须为 registered-v1；冻结事实审计不可跳过")
    fact_sources = sorted(set(fact_sources))
    advisory_sources = set(fact_sources) - verified_sources
    required_sources = verified_sources | (set(cited_sources) - advisory_sources)
    audit = evidence_contract.audit_source_ids(sources, required_sources)
    errors.extend(audit["errors"])
    advisory_audit = evidence_contract.audit_source_ids(sources, advisory_sources - required_sources)
    warnings.extend("未核验线索来源待补：" + error for error in advisory_audit["errors"])
    if sources_missing and not (required_sources or advisory_sources):
        warnings.append("来源清单文件缺失")
    unlisted = sorted(set(fact_sources) - set(cited_sources))
    if unlisted:
        warnings.append("冻结事实的来源未列入报告引用：" + ", ".join(unlisted))
    scoring = company_scoring.status(str(run_dir))
    valuation = company_valuation.status(str(run_dir))
    if scoring.get("status") != "complete":
        errors.append(f"评分未完成：{scoring.get('status')}")
    if valuation.get("status") not in {"complete", "complete-indicative", "recalculated"}:
        errors.append(f"估值没有可交付区间：{valuation.get('status')}")
    else:
        try:
            consensus = _json(run_dir / "analysis" / "valuation" / "consensus-assumptions.json")
            calculation = _json(run_dir / "analysis" / "valuation" / "calculation.json")
        except (OSError, ValueError) as exc:
            errors.append(f"估值工件无法读取：{exc}")
        else:
            errors.extend(_valuation_report_consistency(consensus, calculation, body))
    return {"valid": not errors, "errors": errors, "warnings": warnings,
            "chapter_states": states, "scoring_status": scoring.get("status"),
            "valuation_status": valuation.get("status"), "report": str(report),
            "run_id": metadata.get("run_id"), "cited_sources": cited_sources,
            "fact_sources": fact_sources, "url_only_sources": audit["url_only_sources"]}


def publish(args: argparse.Namespace) -> dict:
    run_dir = Path(args.run_dir).expanduser().resolve()
    metadata_path = run_dir / "run.json"
    metadata = _json(metadata_path)
    report = Path(args.report).expanduser().resolve()
    installed = run_dir / "reports" / "analysis.md"
    if metadata.get("status") in TERMINAL:
        if installed.is_file() and _sha(installed) == _sha(report):
            return {"report": str(installed), "already_published": True}
        raise ValueError("completed run is immutable")
    result = check(args)
    if not result["valid"]:
        return result
    if installed.exists() and _sha(installed) != _sha(report):
        raise ValueError("a different report already exists in this run")
    if not installed.exists():
        _copy_atomic(report, installed)
    latest = None
    if not args.no_latest:
        latest = run_dir.parent.parent / "reports" / "latest.md"
        _copy_atomic(installed, latest)
    metadata.update({"status": "completed", "report_sha256": _sha(installed),
                     "published_at": datetime.now(timezone.utc).isoformat(),
                     "latest_updated": not args.no_latest})
    _write_json(metadata_path, metadata)
    return {"report": str(installed), "latest": str(latest) if latest else None,
            "warnings": result["warnings"], "already_published": False}


def main() -> int:
    parser = JsonArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=JsonArgumentParser)
    started = commands.add_parser("start", help="create one lightweight analysis run")
    started.add_argument("--company-dir", required=True)
    started.add_argument("--company")
    started.add_argument("--run-id")
    source = commands.add_parser("add-source", help="record one source and optional local file")
    source.add_argument("--company-dir", required=True)
    source.add_argument("--file")
    source.add_argument("--url")
    source.add_argument("--title")
    source.add_argument("--publisher", required=True)
    source.add_argument("--period", required=True)
    source.add_argument("--locator", required=True)
    for name in ("check", "publish"):
        action = commands.add_parser(name)
        action.add_argument("--run-dir", required=True)
        action.add_argument("--report", required=True)
        if name == "publish":
            action.add_argument("--no-latest", action="store_true")
    args = parser.parse_args()
    try:
        result = {"start": start, "add-source": add_source,
                  "check": check, "publish": publish}[args.command](args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("valid", True) else 1
    except (OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
