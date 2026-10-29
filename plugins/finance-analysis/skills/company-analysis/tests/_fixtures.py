"""合成冻结输入、评分卡与 run 目录，供评分契约测试复用。"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS / "scoring"))

import scoring_consensus  # noqa: E402

PLUGIN_ROOT = SKILL_ROOT.parent.parent
RUBRIC_PATH = SKILL_ROOT / "references" / "scoring" / "scoring-rubric.json"
COMPANY_RUN = str(SCRIPTS / "company_run.py")
COMPANY_SCORING = str(SCRIPTS / "scoring" / "company_scoring.py")


def load_rubric() -> dict:
    return json.loads(RUBRIC_PATH.read_text("utf-8"))


def rubric_dimensions(rubric: dict) -> list[str]:
    return [d["dimension_id"] for axis in rubric["axes"] for d in axis["dimensions"]]


def rubric_weights(rubric: dict) -> dict:
    return {
        d["dimension_id"]: d["weight"]
        for axis in rubric["axes"] for d in axis["dimensions"]
    }


def dimension_axis(rubric: dict) -> dict:
    return {
        d["dimension_id"]: axis["axis_id"]
        for axis in rubric["axes"] for d in axis["dimensions"]
    }


def fact(fid: str, source_id: str = "S1", status: str = "verified",
         fact_type: str = "disclosed") -> dict:
    return {
        "fact_id": fid, "metric": "qualitative-support", "value": "1", "unit": "ratio",
        "currency": None, "period": "2025FY", "consolidation_scope": "consolidated",
        "source_material_id": source_id, "source_locator": "p.1", "audit_status": "audited",
        "methodology": "公司披露口径", "comparability": "同业可比", "fact_type": fact_type,
        "replaces_fact_id": None, "status": status,
    }


def coverage_item(oid: str, assessment: str = "supported", gaps: list | None = None) -> dict:
    return {
        "dimension_id": oid, "assessment": assessment,
        "evidence_fact_ids": [] if assessment == "unassessable" else [f"f-{oid}"],
        "missing_evidence": gaps if gaps is not None else (
            ["证据缺失"] if assessment in {"inferred", "unassessable"} else []
        ),
        "supplementation_status": "not-needed" if assessment == "supported" else (
            "exhausted" if assessment == "unassessable" else "completed"
        ),
        "supplementation_notes": "证据充分" if assessment == "supported" else "已穷尽补查",
    }


def assessment_context() -> dict:
    return {
        "as_of": "2026-10-29", "history_period": "2021-2025", "forecast_period": "2026-2028",
        "industry_profile": "制造业", "company_scope": "合并报表",
        "segment_basis": [{
            "scope": "整体", "metric_basis": "收入", "aggregation_basis": "合并",
            "evidence_fact_ids": [], "rationale": "单一业务",
        }],
    }


def build_input(rubric: dict | None = None) -> dict:
    rubric = rubric or load_rubric()
    ids = rubric_dimensions(rubric)
    components = [c["component_id"] for c in rubric["cycle_rubric"]["components"]]
    rules = [r["rule_id"] for r in rubric["risk_rules"]]
    facts = [fact(f"f-{oid}") for oid in ids + components + rules]
    coverage = {
        "schema_version": scoring_consensus.COVERAGE_SCHEMA,
        "fact_snapshot_id": "snap-1",
        "rubric_version": rubric["rubric_version"],
        "dimensions": [coverage_item(d) for d in ids],
        "cycle_components": [coverage_item(c) for c in components],
        "risk_checks": [coverage_item(r) for r in rules],
    }
    data = {
        "schema_version": scoring_consensus.INPUT_SCHEMA,
        "rubric_version": rubric["rubric_version"],
        "fact_snapshot_id": "snap-1",
        "model_version": "test-model",
        "scoring_input_hash": "pending",
        "facts": facts,
        "axes": rubric["axes"],
        "evidence_coverage": coverage,
        "cycle_rubric": rubric["cycle_rubric"],
        "aggregation_policy": rubric["aggregation_policy"],
        "risk_rules": rubric["risk_rules"],
        "assessment_context": assessment_context(),
    }
    data["scoring_input_hash"] = scoring_consensus.scoring_input_hash(data)
    return data


def rating(dim: str, band, weight: int, status: str = "supported",
           ambiguous=None, gaps: list | None = None) -> dict:
    return {
        "dimension_id": dim, "band": band, "ambiguous_with": ambiguous, "weight": weight,
        "evidence_status": status,
        "evidence_fact_ids": [] if band is None else [f"f-{dim}"],
        "rationale": f"{dim} 判断", "counterevidence": "",
        "data_gaps": gaps if gaps is not None else (
            ["证据缺失"] if status in {"inferred", "unassessable"} else []
        ),
    }


def build_card(scoring_input: dict, bands: dict | None = None,
               statuses: dict | None = None, ambiguities: dict | None = None,
               rules: list | None = None, cycle: dict | None = None) -> dict:
    rubric = load_rubric()
    weights = rubric_weights(rubric)
    dims = rubric_dimensions(rubric)
    bands = bands or {}
    statuses = statuses or {}
    ambiguities = ambiguities or {}
    ratings = []
    for dim in dims:
        band = bands.get(dim, 75)
        status = statuses.get(dim, "unassessable" if band is None else "supported")
        ratings.append(rating(dim, band, weights[dim], status=status,
                              ambiguous=ambiguities.get(dim),
                              gaps=None if status == "supported" else ["证据缺失"]))
    components = [c["component_id"] for c in rubric["cycle_rubric"]["components"]]
    cycle = cycle if cycle is not None else {
        "applicability": "applicable", "phase": "expansion", "direction": "improving",
        "rationale": "订单回暖",
        "components": [{
            "component_id": c, "band": 75, "evidence_fact_ids": [f"f-{c}"],
            "rationale": f"{c} 判断", "data_gaps": [],
        } for c in components],
    }
    rule_items = rules
    if rule_items is None:
        rule_items = [{
            "rule_id": r["rule_id"], "status": "not-triggered",
            "evidence_fact_ids": [f"f-{r['rule_id']}"], "rationale": f"{r['rule_id']} 排除",
        } for r in rubric["risk_rules"]]
    return {
        "schema_version": scoring_consensus.SCORECARD_SCHEMA,
        "scorer_id": "scorer-1",
        "rubric_version": scoring_input["rubric_version"],
        "fact_snapshot_id": scoring_input["fact_snapshot_id"],
        "scoring_input_hash": scoring_input["scoring_input_hash"],
        "model_id": "test-model",
        "ratings": ratings,
        "cycle_assessment": cycle,
        "risk_assessments": rule_items,
    }


def rule_item(rule_id: str, status: str) -> dict:
    return {
        "rule_id": rule_id, "status": status,
        "evidence_fact_ids": [f"f-{rule_id}"] if status == "triggered" else [f"f-{rule_id}"],
        "rationale": f"{rule_id} {status}",
    }


def write_json(path: Path, data: dict) -> Path:
    path.write_text(json.dumps(data, ensure_ascii=False), "utf-8")
    return path


def fresh_run_dir(base: Path) -> Path:
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    return base


def cli(*args: str) -> dict:
    result = subprocess.run(
        [sys.executable, *args], capture_output=True, text=True,
    )
    payload = None
    if result.stdout.strip():
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            pass
    return {"code": result.returncode, "payload": payload,
            "stdout": result.stdout, "stderr": result.stderr}
