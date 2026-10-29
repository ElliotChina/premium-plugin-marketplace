"""Pure validation and aggregation contracts for the v2 five-axis scoring rubric.

单版本替换：只支持 rubric-v2 量表、input-v3 冻结输入、scorecard-v4 评分卡与
consensus-v4 共识；旧 schema 一律拒绝。核心公式 core-quality-geometric-v1：
Q = B^0.4 * F^0.4 * G^0.2（等价于 (B^2 * F^2 * G)^(1/5)，Decimal 固定精度）。
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Context, Decimal, InvalidOperation, ROUND_HALF_UP, localcontext
from pathlib import Path
import re
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import evidence_contract as _evidence


INPUT_SCHEMA = "company-analysis-scoring-input-v3"
SCORECARD_SCHEMA = "company-analysis-scorecard-v4"
CONSENSUS_SCHEMA = "company-analysis-scoring-consensus-v4"
COVERAGE_SCHEMA = "company-analysis-evidence-coverage-v2"
RUBRIC_SCHEMA = "company-analysis-scoring-rubric-v2"
FORMULA_VERSION = "core-quality-geometric-v1"
BAND_VALUES = frozenset({Decimal("0"), Decimal("25"), Decimal("50"), Decimal("75"), Decimal("100")})
ANCHOR_SCORES = frozenset({"0", "25", "50", "75", "100"})
EVIDENCE_STATUSES = frozenset({"supported", "inferred", "unassessable"})
RISK_STATUSES = frozenset({"triggered", "not-triggered", "unresolved"})
COMPANY_ACTION_STATES = frozenset({"restricted", "attention"})
RISK_STATES = frozenset({"restricted", "attention", "clear", "unassessed"})
ASSESSMENT_STATES = frozenset({"supported", "provisional", "unavailable"})
AS_OF_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
CYCLE_APPLICABILITY = frozenset({"applicable", "weak-cycle", "unassessable"})
CYCLE_PHASES = frozenset({
    "trough", "recovery", "expansion", "overheating", "contraction", "unclear", "not-applicable",
})
CYCLE_DIRECTIONS = frozenset({"improving", "stable", "deteriorating", "unclear", "not-applicable"})
SUPPLEMENTATION_STATUSES = frozenset({
    "not-needed", "completed", "exhausted", "not-cost-effective", "not-publicly-available",
})
EXHAUSTED_SUPPLEMENTATION = frozenset({
    "completed", "exhausted", "not-cost-effective", "not-publicly-available",
})
DECIMAL_CONTEXT = Context(prec=50)


class ScoringError(ValueError):
    """Raised when a frozen scoring input, scorecard, or consensus is malformed."""


def canonical_json_bytes(data: object) -> bytes:
    """Serialize data in the canonical form used by the scoring contracts."""
    return _evidence.canonical_json_bytes(data)


def content_hash(data: object) -> str:
    """Return the SHA-256 digest of canonical JSON data."""
    return _evidence.content_hash(data)


def scoring_input_hash(data: Mapping) -> str:
    """Hash a scoring input without its self-referential hash field."""
    _mapping(data, "scoring input")
    content = dict(data)
    content.pop("scoring_input_hash", None)
    return content_hash(content)


def _translate_evidence_error(action):
    try:
        return action()
    except _evidence.EvidenceError as exc:
        raise ScoringError(str(exc)) from exc


def _mapping(value: object, field: str) -> Mapping:
    return _translate_evidence_error(lambda: _evidence._mapping(value, field))


def _exact_keys(value: object, keys: tuple[str, ...], field: str) -> Mapping:
    return _translate_evidence_error(lambda: _evidence._exact_keys(value, keys, field))


def _non_empty_string(value: object, field: str) -> str:
    return _translate_evidence_error(lambda: _evidence._non_empty_string(value, field))


def _decimal_number(value: object, field: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ScoringError(f"{field} must be a number")
    try:
        decimal = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ScoringError(f"{field} must be a finite number") from exc
    if not decimal.is_finite():
        raise ScoringError(f"{field} must be a finite number")
    return decimal


def _string_list(value: object, field: str) -> list:
    if not isinstance(value, list):
        raise ScoringError(f"{field} must be a list")
    for index, item in enumerate(value):
        _non_empty_string(item, f"{field}[{index}]")
    return value


def _validate_fact_records(facts: object, field: str) -> Mapping[str, Mapping]:
    return _translate_evidence_error(lambda: _evidence.validate_fact_records(facts, field=field))


def _rubric_dimension_keys(dimension: Mapping) -> None:
    for field in ("raw_metrics", "benchmarks", "overturning_evidence"):
        _string_list(dimension[field], f"dimension.{field}")
    for field in ("applicability", "missing_data_rule"):
        _non_empty_string(dimension[field], f"dimension.{field}")


def _validate_anchor_block(anchors: object, field: str) -> None:
    block = _mapping(anchors, field)
    if set(block) != ANCHOR_SCORES:
        raise ScoringError(f"{field} must contain exactly 0, 25, 50, 75, and 100")
    for score, anchor in block.items():
        _non_empty_string(anchor, f"{field}[{score}]")


def _validate_axis_entry(axis: object, axis_index: int) -> tuple[str, list[str]]:
    axis_data = _exact_keys(axis, ("axis_id", "label", "dimensions"), f"scoring input.axes[{axis_index}]")
    axis_id = _non_empty_string(axis_data["axis_id"], f"scoring input.axes[{axis_index}].axis_id")
    _non_empty_string(axis_data["label"], f"scoring input.axes[{axis_index}].label")
    dimensions = axis_data["dimensions"]
    if not isinstance(dimensions, list) or not dimensions:
        raise ScoringError(f"scoring input.axes[{axis_index}].dimensions must be a non-empty list")
    axis_weight = Decimal("0")
    dimension_ids = []
    for dimension_index, dimension in enumerate(dimensions):
        field = f"scoring input.axes[{axis_index}].dimensions[{dimension_index}]"
        dimension_data = _exact_keys(dimension, (
            "dimension_id", "label", "weight", "anchors", "raw_metrics", "benchmarks",
            "applicability", "missing_data_rule", "overturning_evidence", "risk_rule_ids",
        ), field)
        dimension_id = _non_empty_string(dimension_data["dimension_id"], f"{field}.dimension_id")
        dimension_ids.append(dimension_id)
        _non_empty_string(dimension_data["label"], f"{field}.label")
        weight = _decimal_number(dimension_data["weight"], f"{field}.weight")
        if weight < Decimal("0") or weight > Decimal("100"):
            raise ScoringError(f"{field}.weight must be between 0 and 100")
        axis_weight += weight
        _validate_anchor_block(dimension_data["anchors"], f"{field}.anchors")
        _rubric_dimension_keys(dimension_data)
        _string_list(dimension_data["risk_rule_ids"], f"{field}.risk_rule_ids")
    if axis_weight != Decimal("100"):
        raise ScoringError("dimension weights within each axis must total exactly 100")
    return axis_id, dimension_ids


def _validate_cycle_rubric(cycle_rubric: object) -> None:
    data = _exact_keys(cycle_rubric, (
        "components", "phase_guide", "direction_guide", "applicability_guide",
    ), "cycle_rubric")
    components = data["components"]
    if not isinstance(components, list) or not components:
        raise ScoringError("cycle_rubric.components must be a non-empty list")
    total_weight = Decimal("0")
    component_ids = []
    for index, component in enumerate(components):
        field = f"cycle_rubric.components[{index}]"
        item = _exact_keys(component, (
            "component_id", "label", "weight", "anchors", "raw_metrics", "benchmarks",
            "applicability", "missing_data_rule", "overturning_evidence",
        ), field)
        component_ids.append(_non_empty_string(item["component_id"], f"{field}.component_id"))
        _non_empty_string(item["label"], f"{field}.label")
        total_weight += _decimal_number(item["weight"], f"{field}.weight")
        _validate_anchor_block(item["anchors"], f"{field}.anchors")
        _rubric_dimension_keys(item)
    if len(set(component_ids)) != len(component_ids):
        raise ScoringError("cycle_rubric.components contains duplicate component_id")
    if total_weight != Decimal("100"):
        raise ScoringError("cycle component weights must total exactly 100")
    for field in ("phase_guide", "direction_guide", "applicability_guide"):
        _non_empty_string(data[field], f"cycle_rubric.{field}")


def _validate_aggregation_policy(policy: object) -> None:
    data = _exact_keys(policy, (
        "formula_version", "core_axes", "core_weights", "formula",
        "null_policy", "decimal_precision", "rounding", "score_decimals",
    ), "aggregation_policy")
    if data["formula_version"] != FORMULA_VERSION:
        raise ScoringError("aggregation_policy.formula_version is not supported")
    core_axes = data["core_axes"]
    if not isinstance(core_axes, list) or len(core_axes) != 3:
        raise ScoringError("aggregation_policy.core_axes must list the three core axes")
    weights = data["core_weights"]
    weights_mapping = _mapping(weights, "aggregation_policy.core_weights")
    if set(weights_mapping) != set(core_axes):
        raise ScoringError("aggregation_policy.core_weights must cover exactly the core axes")
    total = Decimal("0")
    for axis_id, weight in weights_mapping.items():
        value = _decimal_number(weight, f"aggregation_policy.core_weights[{axis_id}]")
        if value <= Decimal("0"):
            raise ScoringError("core weights must be positive")
        total += value
    if total != Decimal("1"):
        raise ScoringError("aggregation_policy core weights must total exactly 1")
    if data["rounding"] != "ROUND_HALF_UP":
        raise ScoringError("aggregation_policy.rounding is not supported")
    for field in ("decimal_precision", "score_decimals"):
        if not isinstance(data[field], int) or isinstance(data[field], bool) or data[field] < 1:
            raise ScoringError(f"aggregation_policy.{field} must be a positive integer")
    for field in ("formula", "null_policy"):
        _non_empty_string(data[field], f"aggregation_policy.{field}")


def _validate_risk_rules(rules: object) -> dict[str, Mapping]:
    if not isinstance(rules, list) or not rules:
        raise ScoringError("risk_rules must be a non-empty list")
    known: dict[str, Mapping] = {}
    for index, rule in enumerate(rules):
        field = f"risk_rules[{index}]"
        data = _exact_keys(rule, (
            "rule_id", "label", "trigger_condition", "evidence_requirement",
            "resolution_basis", "actions",
        ), field)
        rule_id = _non_empty_string(data["rule_id"], f"{field}.rule_id")
        if rule_id in known:
            raise ScoringError("risk_rules contains duplicate rule_id")
        _non_empty_string(data["label"], f"{field}.label")
        for key in ("trigger_condition", "resolution_basis"):
            _non_empty_string(data[key], f"{field}.{key}")
        requirement = _non_empty_string(data["evidence_requirement"], f"{field}.evidence_requirement")
        if requirement not in {"verified-facts", "stress-scenario-allowed"}:
            raise ScoringError(f"{field}.evidence_requirement is not supported")
        actions = data["actions"]
        if not isinstance(actions, list) or not actions:
            raise ScoringError(f"{field}.actions must be a non-empty list")
        for action_index, action in enumerate(actions):
            action_field = f"{field}.actions[{action_index}]"
            scope = _non_empty_string(action.get("scope"), f"{action_field}.scope")
            if scope == "company":
                action_data = _exact_keys(action, ("scope", "state"), action_field)
                if action_data["state"] not in COMPANY_ACTION_STATES:
                    raise ScoringError(f"{action_field}.state is not supported")
                continue
            if scope not in {"dimension", "axis"}:
                raise ScoringError(f"{action_field}.scope is not supported")
            action_data = _exact_keys(action, ("scope", "target", "cap"), action_field)
            _non_empty_string(action_data["target"], f"{action_field}.target")
            cap = action_data["cap"]
            if cap is None:
                raise ScoringError(f"{action_field}.cap is required for dimension and axis actions")
            if not Decimal("0") <= _decimal_number(cap, f"{action_field}.cap") <= Decimal("100"):
                raise ScoringError(f"{action_field}.cap must be between 0 and 100")
        known[rule_id] = data
    return known


def _validate_assessment_context(context: object) -> Mapping:
    data = _exact_keys(context, (
        "as_of", "history_period", "forecast_period", "industry_profile",
        "company_scope", "segment_basis",
    ), "assessment_context")
    as_of = _non_empty_string(data["as_of"], "assessment_context.as_of")
    if not AS_OF_PATTERN.fullmatch(as_of):
        raise ScoringError("assessment_context.as_of must be a YYYY-MM-DD date")
    for field in ("history_period", "forecast_period", "industry_profile", "company_scope"):
        _non_empty_string(data[field], f"assessment_context.{field}")
    segments = data["segment_basis"]
    if not isinstance(segments, list):
        raise ScoringError("assessment_context.segment_basis must be a list")
    for index, segment in enumerate(segments):
        field = f"assessment_context.segment_basis[{index}]"
        item = _exact_keys(segment, (
            "scope", "metric_basis", "aggregation_basis", "evidence_fact_ids", "rationale",
        ), field)
        for key in ("scope", "metric_basis", "aggregation_basis", "rationale"):
            _non_empty_string(item[key], f"{field}.{key}")
        _string_list(item["evidence_fact_ids"], f"{field}.evidence_fact_ids")
    return data


def validate_scoring_input(data: Mapping) -> Mapping:
    """Validate the immutable scoring input v3 and its content hash."""
    raw = _mapping(data, "scoring input")
    if raw.get("schema_version") != INPUT_SCHEMA:
        raise ScoringError("scoring input.schema_version is not supported")
    keys = (
        "schema_version", "rubric_version", "fact_snapshot_id", "model_version",
        "scoring_input_hash", "facts", "axes", "evidence_coverage",
        "cycle_rubric", "aggregation_policy", "risk_rules", "assessment_context",
    )
    scoring_input = _exact_keys(data, keys, "scoring input")
    for field in ("rubric_version", "fact_snapshot_id", "model_version", "scoring_input_hash"):
        _non_empty_string(scoring_input[field], f"scoring input.{field}")

    _validate_fact_records(scoring_input["facts"], field="scoring input.facts")

    axes = scoring_input["axes"]
    if not isinstance(axes, list) or not axes:
        raise ScoringError("scoring input.axes must be a non-empty list")
    axis_ids = []
    dimension_ids = []
    for axis_index, axis in enumerate(axes):
        axis_id, ids = _validate_axis_entry(axis, axis_index)
        if axis_id in axis_ids:
            raise ScoringError("scoring input.axes contains duplicate axis_id")
        axis_ids.append(axis_id)
        dimension_ids.extend(ids)
    if len(set(dimension_ids)) != len(dimension_ids):
        raise ScoringError("scoring input.axes contains duplicate dimension_id")

    known_rules = _validate_risk_rules(scoring_input["risk_rules"])
    for axis in axes:
        for dimension in axis["dimensions"]:
            for rule_id in dimension["risk_rule_ids"]:
                if rule_id not in known_rules:
                    raise ScoringError(
                        f"scoring input dimension {dimension['dimension_id']} cites unknown risk rule"
                    )
                if not any(
                    action["scope"] == "dimension" and action["target"] == dimension["dimension_id"]
                    for action in known_rules[rule_id]["actions"]
                ):
                    raise ScoringError(
                        f"risk rule {rule_id} has no dimension action targeting {dimension['dimension_id']}"
                    )

    _validate_cycle_rubric(scoring_input["cycle_rubric"])
    _validate_aggregation_policy(scoring_input["aggregation_policy"])
    _validate_assessment_context(scoring_input["assessment_context"])
    _validate_evidence_coverage(scoring_input["evidence_coverage"], scoring_input, set(dimension_ids))

    if scoring_input["scoring_input_hash"] != scoring_input_hash(scoring_input):
        raise ScoringError("scoring input.scoring_input_hash does not match canonical input content")
    return data


def _coverage_item(value: object, field: str, object_ids: set[str], seen: set[str],
                   known_facts: Mapping[str, str]) -> None:
    item = _exact_keys(value, (
        "dimension_id", "assessment", "evidence_fact_ids", "missing_evidence",
        "supplementation_status", "supplementation_notes",
    ), field)
    object_id = _non_empty_string(item["dimension_id"], f"{field}.dimension_id")
    if object_id in seen or object_id not in object_ids:
        raise ScoringError(f"{field} must reference each object exactly once")
    seen.add(object_id)
    assessment = _non_empty_string(item["assessment"], f"{field}.assessment")
    if assessment not in EVIDENCE_STATUSES | {"unresolved"}:
        raise ScoringError(f"{field}.assessment is not supported")
    fact_ids = _rating_fact_ids(item["evidence_fact_ids"], f"{field}.evidence_fact_ids", known_facts)
    if any(known_facts[fact_id] != "verified" for fact_id in fact_ids):
        raise ScoringError(f"{field}.evidence_fact_ids must reference verified facts")
    gaps = _string_list(item["missing_evidence"], f"{field}.missing_evidence")
    supplementation = _non_empty_string(item["supplementation_status"], f"{field}.supplementation_status")
    if supplementation not in SUPPLEMENTATION_STATUSES:
        raise ScoringError(f"{field}.supplementation_status is not supported")
    _non_empty_string(item["supplementation_notes"], f"{field}.supplementation_notes")
    if assessment == "supported":
        if not fact_ids:
            raise ScoringError(f"supported {field} requires evidence_fact_ids")
        if supplementation not in {"not-needed", "completed"}:
            raise ScoringError(f"supported {field} has invalid supplementation_status")
    elif assessment == "inferred":
        if not fact_ids:
            raise ScoringError(f"inferred {field} requires verified evidence_fact_ids")
        if not gaps:
            raise ScoringError(f"inferred {field} requires missing_evidence")
        if supplementation == "not-needed":
            raise ScoringError(f"inferred {field} requires a completed supplementation outcome")
    elif assessment == "unassessable":
        if not gaps:
            raise ScoringError(f"unassessable {field} requires missing_evidence")
        if supplementation not in EXHAUSTED_SUPPLEMENTATION:
            raise ScoringError(f"unassessable {field} requires a completed supplementation outcome")
    else:  # unresolved：仅风险检查允许
        if not gaps:
            raise ScoringError(f"unresolved {field} requires missing_evidence")


def _validate_evidence_coverage(value: object, scoring_input: Mapping, dimension_ids: set[str]) -> Mapping:
    coverage = _exact_keys(value, (
        "schema_version", "fact_snapshot_id", "rubric_version",
        "dimensions", "cycle_components", "risk_checks",
    ), "evidence_coverage")
    if coverage["schema_version"] != COVERAGE_SCHEMA:
        raise ScoringError("evidence_coverage.schema_version is not supported")
    for field in ("fact_snapshot_id", "rubric_version"):
        _non_empty_string(coverage[field], f"evidence_coverage.{field}")
        if coverage[field] != scoring_input[field]:
            raise ScoringError(f"evidence_coverage.{field} must match the scoring input")
    known_facts = _known_fact_ids(scoring_input)
    component_ids = {
        component["component_id"] for component in scoring_input["cycle_rubric"]["components"]
    }
    rule_ids = {rule["rule_id"] for rule in scoring_input["risk_rules"]}
    seen_dimensions: set[str] = set()
    for index, dimension in enumerate(coverage["dimensions"]):
        _coverage_item(
            dimension, f"evidence_coverage.dimensions[{index}]",
            dimension_ids, seen_dimensions, known_facts,
        )
    if seen_dimensions != dimension_ids:
        raise ScoringError("evidence_coverage.dimensions must cover each rubric dimension exactly once")
    seen_components: set[str] = set()
    for index, component in enumerate(coverage["cycle_components"]):
        _coverage_item(
            component, f"evidence_coverage.cycle_components[{index}]",
            component_ids, seen_components, known_facts,
        )
    seen_rules: set[str] = set()
    for index, check in enumerate(coverage["risk_checks"]):
        _coverage_item(
            check, f"evidence_coverage.risk_checks[{index}]",
            rule_ids, seen_rules, known_facts,
        )
    return coverage


def _known_fact_ids(scoring_input: Mapping) -> dict[str, str]:
    return {fact["fact_id"]: fact["status"] for fact in scoring_input["facts"]}


def _rating_fact_ids(value: object, field: str, known_facts: Mapping[str, str]) -> list:
    fact_ids = _string_list(value, field)
    if len(set(fact_ids)) != len(fact_ids):
        raise ScoringError(f"{field} contains duplicate fact ids")
    for fact_id in fact_ids:
        if fact_id not in known_facts:
            raise ScoringError(f"{field} cites unknown fact id")
    return fact_ids


def _optional_band(value: object, field: str) -> Decimal | None:
    if value is None:
        return None
    band = _decimal_number(value, field)
    if band not in BAND_VALUES:
        raise ScoringError(f"{field} must be 0, 25, 50, 75, 100, or null")
    return band


def validate_scorecard(scorecard: object, scoring_input: Mapping) -> Mapping:
    """Validate a scorecard v4 against its frozen scoring input."""
    data = _exact_keys(scorecard, (
        "schema_version", "scorer_id", "rubric_version", "fact_snapshot_id",
        "scoring_input_hash", "model_id", "ratings", "cycle_assessment", "risk_assessments",
    ), "scorecard")
    if data["schema_version"] != SCORECARD_SCHEMA:
        raise ScoringError("scorecard.schema_version is not supported")
    for field in ("scorer_id", "model_id"):
        _non_empty_string(data[field], f"scorecard.{field}")
    for field in ("rubric_version", "fact_snapshot_id", "scoring_input_hash"):
        if data[field] != scoring_input[field]:
            raise ScoringError(f"scorecard.{field} must match the scoring input")

    rubric_dimensions = {}
    for axis in scoring_input["axes"]:
        for dimension in axis["dimensions"]:
            rubric_dimensions[dimension["dimension_id"]] = dimension
    known_facts = _known_fact_ids(scoring_input)

    ratings = data["ratings"]
    if not isinstance(ratings, list):
        raise ScoringError("scorecard.ratings must be a list")
    seen: set[str] = set()
    for index, rating in enumerate(ratings):
        field = f"scorecard.ratings[{index}]"
        item = _exact_keys(rating, (
            "dimension_id", "band", "ambiguous_with", "weight", "evidence_status",
            "evidence_fact_ids", "rationale", "counterevidence", "data_gaps",
        ), field)
        dimension_id = _non_empty_string(item["dimension_id"], f"{field}.dimension_id")
        if dimension_id in seen or dimension_id not in rubric_dimensions:
            raise ScoringError(f"{field} must reference each rubric dimension exactly once")
        seen.add(dimension_id)
        rubric = rubric_dimensions[dimension_id]
        band = _optional_band(item["band"], f"{field}.band")
        ambiguous_with = _optional_band(item["ambiguous_with"], f"{field}.ambiguous_with")
        if _decimal_number(item["weight"], f"{field}.weight") != Decimal(str(rubric["weight"])):
            raise ScoringError(f"{field}.weight must match the rubric weight")
        status = _non_empty_string(item["evidence_status"], f"{field}.evidence_status")
        if status not in EVIDENCE_STATUSES:
            raise ScoringError(f"{field}.evidence_status is not supported")
        fact_ids = _rating_fact_ids(item["evidence_fact_ids"], f"{field}.evidence_fact_ids", known_facts)
        if any(known_facts[fact_id] != "verified" for fact_id in fact_ids):
            raise ScoringError(f"{field}.evidence_fact_ids must reference verified facts")
        gaps = _string_list(item["data_gaps"], f"{field}.data_gaps")
        _non_empty_string(item["rationale"], f"{field}.rationale")
        if not isinstance(item["counterevidence"], str):
            raise ScoringError(f"{field}.counterevidence must be a string")
        if status == "unassessable":
            if band is not None:
                raise ScoringError(f"unassessable {field} must have a null band")
            if ambiguous_with is not None:
                raise ScoringError(f"unassessable {field} must not set ambiguous_with")
            if not gaps:
                raise ScoringError(f"unassessable {field} requires data_gaps")
        else:
            if band is None:
                raise ScoringError(f"{status} {field} requires a band")
            if not fact_ids:
                raise ScoringError(f"{status} {field} requires evidence_fact_ids")
            if status == "supported" and gaps:
                raise ScoringError(f"supported {field} must not carry data_gaps")
            if status == "inferred" and not gaps:
                raise ScoringError(f"inferred {field} requires data_gaps")
            if ambiguous_with is not None:
                if ambiguous_with == band:
                    raise ScoringError(f"{field}.ambiguous_with must differ from band")

    if seen != set(rubric_dimensions):
        raise ScoringError("scorecard.ratings must cover every rubric dimension exactly once")
    _validate_cycle_assessment(data["cycle_assessment"], scoring_input, known_facts)
    _validate_risk_assessments(data["risk_assessments"], scoring_input, known_facts)
    return data


def _validate_cycle_assessment(cycle: object, scoring_input: Mapping,
                               known_facts: Mapping[str, str]) -> None:
    data = _exact_keys(cycle, (
        "applicability", "phase", "direction", "rationale", "components",
    ), "cycle_assessment")
    applicability = _non_empty_string(data["applicability"], "cycle_assessment.applicability")
    if applicability not in CYCLE_APPLICABILITY:
        raise ScoringError("cycle_assessment.applicability is not supported")
    phase = _non_empty_string(data["phase"], "cycle_assessment.phase")
    direction = _non_empty_string(data["direction"], "cycle_assessment.direction")
    _non_empty_string(data["rationale"], "cycle_assessment.rationale")
    if applicability == "weak-cycle":
        if phase != "not-applicable" or direction != "not-applicable":
            raise ScoringError("weak-cycle cycle_assessment must use not-applicable phase and direction")
        if data["components"] != []:
            raise ScoringError("weak-cycle cycle_assessment must not rate components")
        return
    if applicability == "unassessable":
        if phase != "unclear" or direction != "unclear":
            raise ScoringError("unassessable cycle_assessment must use unclear phase and direction")
    elif phase not in CYCLE_PHASES - {"unclear", "not-applicable"}:
        raise ScoringError("applicable cycle_assessment must name a market phase")
    if direction not in CYCLE_DIRECTIONS - {"not-applicable"}:
        raise ScoringError("cycle_assessment.direction is not supported")

    component_ids = {
        component["component_id"] for component in scoring_input["cycle_rubric"]["components"]
    }
    components = data["components"]
    if not isinstance(components, list):
        raise ScoringError("cycle_assessment.components must be a list")
    seen: set[str] = set()
    for index, component in enumerate(components):
        field = f"cycle_assessment.components[{index}]"
        item = _exact_keys(component, (
            "component_id", "band", "evidence_fact_ids", "rationale", "data_gaps",
        ), field)
        component_id = _non_empty_string(item["component_id"], f"{field}.component_id")
        if component_id in seen or component_id not in component_ids:
            raise ScoringError(f"{field} must reference each cycle component exactly once")
        seen.add(component_id)
        band = _optional_band(item["band"], f"{field}.band")
        fact_ids = _rating_fact_ids(item["evidence_fact_ids"], f"{field}.evidence_fact_ids", known_facts)
        if any(known_facts[fact_id] != "verified" for fact_id in fact_ids):
            raise ScoringError(f"{field}.evidence_fact_ids must reference verified facts")
        _non_empty_string(item["rationale"], f"{field}.rationale")
        gaps = _string_list(item["data_gaps"], f"{field}.data_gaps")
        if band is None and not gaps:
            raise ScoringError(f"{field} with a null band requires data_gaps")
        if band is not None and gaps:
            raise ScoringError(f"{field} with a band must not carry data_gaps")
    if seen != component_ids:
        raise ScoringError("cycle_assessment.components must cover every cycle component exactly once")


def _validate_risk_assessments(items: object, scoring_input: Mapping,
                               known_facts: Mapping[str, str]) -> None:
    rules = {rule["rule_id"]: rule for rule in scoring_input["risk_rules"]}
    if not isinstance(items, list):
        raise ScoringError("scorecard.risk_assessments must be a list")
    seen: set[str] = set()
    for index, item in enumerate(items):
        field = f"scorecard.risk_assessments[{index}]"
        data = _exact_keys(item, ("rule_id", "status", "evidence_fact_ids", "rationale"), field)
        rule_id = _non_empty_string(data["rule_id"], f"{field}.rule_id")
        if rule_id in seen or rule_id not in rules:
            raise ScoringError(f"{field} must reference each risk rule exactly once")
        seen.add(rule_id)
        status = _non_empty_string(data["status"], f"{field}.status")
        if status not in RISK_STATUSES:
            raise ScoringError(f"{field}.status is not supported")
        fact_ids = _rating_fact_ids(data["evidence_fact_ids"], f"{field}.evidence_fact_ids", known_facts)
        _non_empty_string(data["rationale"], f"{field}.rationale")
        non_verified = any(known_facts[fact_id] != "verified" for fact_id in fact_ids)
        if non_verified and not (
            status == "triggered"
            and rules[rule_id]["evidence_requirement"] == "stress-scenario-allowed"
        ):
            raise ScoringError(f"{field}.evidence_fact_ids must reference verified facts")
        if status == "triggered" and not fact_ids:
            raise ScoringError(f"triggered {field} requires evidence_fact_ids")


def _triggered_actions(scoring_input: Mapping, card: Mapping) -> tuple[dict, dict, list[str], set[str]]:
    """Fold triggered risk rules into dimension caps, axis caps, company states, and a rule-id set."""
    dimension_caps: dict[str, Decimal] = {}
    axis_caps: dict[str, Decimal] = {}
    company_states: list[str] = []
    triggered_ids: set[str] = set()
    rules = {rule["rule_id"]: rule for rule in scoring_input["risk_rules"]}
    for item in card["risk_assessments"]:
        if item["status"] != "triggered":
            continue
        triggered_ids.add(item["rule_id"])
        for action in rules[item["rule_id"]]["actions"]:
            if action["scope"] == "dimension":
                key = action["target"]
                cap = Decimal(str(action["cap"]))
                dimension_caps[key] = min(dimension_caps.get(key, Decimal("100")), cap)
            elif action["scope"] == "axis":
                key = action["target"]
                cap = Decimal(str(action["cap"]))
                axis_caps[key] = min(axis_caps.get(key, Decimal("100")), cap)
            else:
                company_states.append(action["state"])
    return dimension_caps, axis_caps, company_states, triggered_ids


def _score_axes(scoring_input: Mapping, ratings: Mapping[str, Mapping],
                dimension_caps: Mapping[str, Decimal], axis_caps: Mapping[str, Decimal],
                triggered_ids: set[str]) -> list[dict]:
    """Weighted axis scores from band values; caps apply after weighting, unassessable nulls the axis."""
    axis_results = []
    for axis in scoring_input["axes"]:
        raw_total = Decimal("0")
        capped_total = Decimal("0")
        blocked = False
        dimension_results = []
        for dimension in axis["dimensions"]:
            dimension_id = dimension["dimension_id"]
            rating = ratings[dimension_id]
            weight = Decimal(str(dimension["weight"]))
            band = None if rating["band"] is None else Decimal(str(rating["band"]))
            if band is None:
                blocked = True
                raw_score = effective = None
            else:
                cap = dimension_caps.get(dimension_id)
                effective_band = band if cap is None else min(band, cap)
                raw_score = band
                effective = effective_band
                raw_total += weight * band
                capped_total += weight * effective_band
            dimension_results.append({
                "dimension_id": dimension_id,
                "raw_score": raw_score,
                "effective_score": effective,
                "applied_rules": sorted(
                    rule_id for rule_id in dimension["risk_rule_ids"] if rule_id in triggered_ids
                ),
            })
        raw_result = effective_result = None
        if not blocked:
            raw_result = raw_total / Decimal("100")
            effective_result = min(raw_result, capped_total / Decimal("100"))
            if axis["axis_id"] in axis_caps:
                effective_result = min(effective_result, axis_caps[axis["axis_id"]])
        axis_results.append({
            "axis_id": axis["axis_id"],
            "raw_score": raw_result,
            "effective_score": effective_result,
            "dimensions": dimension_results,
        })
    return axis_results


def _core_quality(policy: Mapping, axis_results: list[dict]) -> Decimal | None:
    """Q = product(axis ** weight) over the core axes under fixed Decimal precision."""
    scores = {
        axis_id: next(a["effective_score"] for a in axis_results if a["axis_id"] == axis_id)
        for axis_id in policy["core_axes"]
    }
    if any(score is None for score in scores.values()):
        return None
    if any(score == Decimal("0") for score in scores.values()):
        return Decimal("0")
    weights = policy["core_weights"]
    with localcontext() as context:
        context.prec = int(policy["decimal_precision"])
        value = Decimal(1)
        for axis_id, weight in weights.items():
            value *= scores[axis_id] ** Decimal(str(weight))
    return value


def _sensitivity_range(policy: Mapping, scoring_input: Mapping, ratings: Mapping[str, Mapping],
                       dimension_caps: Mapping, axis_caps: Mapping, triggered_ids: set[str],
                       base_quality: Decimal | None) -> tuple[Decimal, Decimal] | None:
    """Re-aggregate with each ambiguous dimension moved to its alternative band; cap rules unchanged."""
    ambiguous = [
        dimension["dimension_id"]
        for axis in scoring_input["axes"]
        for dimension in axis["dimensions"]
        if ratings[dimension["dimension_id"]]["ambiguous_with"] is not None
    ]
    if base_quality is None or not ambiguous:
        return None
    candidates: list[Decimal | None] = [base_quality]
    for dimension_id in ambiguous:
        alternative = dict(ratings[dimension_id])
        alternative["band"] = str(ratings[dimension_id]["ambiguous_with"])
        scenario = dict(ratings)
        scenario[dimension_id] = alternative
        candidates.append(_core_quality(policy, _score_axes(
            scoring_input, scenario, dimension_caps, axis_caps, triggered_ids,
        )))
    scores = [value for value in candidates if value is not None]
    return min(scores), max(scores)


def _score_value(value: Decimal | None) -> float | None:
    if value is None:
        return None
    return float(value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def aggregate_scorecard(scoring_input: Mapping, scorecard: object) -> dict:
    """Validate a v4 scorecard against the frozen input and derive the deterministic consensus."""
    data = validate_scoring_input(scoring_input)
    card = validate_scorecard(scorecard, data)
    ratings = {rating["dimension_id"]: rating for rating in card["ratings"]}
    dimension_caps, axis_caps, company_states, triggered_ids = _triggered_actions(data, card)
    axis_results = _score_axes(data, ratings, dimension_caps, axis_caps, triggered_ids)
    policy = data["aggregation_policy"]
    quality = _core_quality(policy, axis_results)
    sensitivity = _sensitivity_range(
        policy, data, ratings, dimension_caps, axis_caps, triggered_ids, quality,
    )

    if "restricted" in company_states:
        risk_state = "restricted"
    elif "attention" in company_states:
        risk_state = "attention"
    elif any(item["status"] == "unresolved" for item in card["risk_assessments"]):
        risk_state = "unassessed"
    else:
        risk_state = "clear"

    core_ids = set(policy["core_axes"])
    core_dimension_ids = {
        dimension["dimension_id"]
        for axis in data["axes"] if axis["axis_id"] in core_ids
        for dimension in axis["dimensions"]
    }
    if any(
        axis["effective_score"] is None for axis in axis_results if axis["axis_id"] in core_ids
    ):
        assessment_state = "unavailable"
    elif any(
        ratings[dimension_id]["evidence_status"] == "inferred"
        or ratings[dimension_id]["ambiguous_with"] is not None
        for dimension_id in core_dimension_ids
    ):
        assessment_state = "provisional"
    else:
        assessment_state = "supported"

    cycle = card["cycle_assessment"]
    intensity = None
    if cycle["applicability"] == "applicable":
        weights = {
            component["component_id"]: Decimal(str(component["weight"]))
            for component in data["cycle_rubric"]["components"]
        }
        total = Decimal("0")
        blocked = False
        for component in cycle["components"]:
            if component["band"] is None:
                blocked = True
                break
            total += weights[component["component_id"]] * Decimal(str(component["band"]))
        if not blocked:
            intensity = total / Decimal("100")

    def axis_entry(result: dict) -> dict:
        return {
            "axis_id": result["axis_id"],
            "raw_score": _score_value(result["raw_score"]),
            "effective_score": _score_value(result["effective_score"]),
            "dimensions": [
                {
                    "dimension_id": dimension["dimension_id"],
                    "raw_score": _score_value(dimension["raw_score"]),
                    "effective_score": _score_value(dimension["effective_score"]),
                    "applied_rules": dimension["applied_rules"],
                }
                for dimension in result["dimensions"]
            ],
        }

    consensus = {
        "schema_version": CONSENSUS_SCHEMA,
        "rubric_version": data["rubric_version"],
        "fact_snapshot_id": data["fact_snapshot_id"],
        "scoring_input_hash": data["scoring_input_hash"],
        "model_id": card["model_id"],
        "axis_scores": [axis_entry(result) for result in axis_results],
        "core_quality": {"formula_version": FORMULA_VERSION, "score": _score_value(quality)},
        "sensitivity_range": None if sensitivity is None else {
            "low": _score_value(sensitivity[0]),
            "high": _score_value(sensitivity[1]),
        },
        "risk_state": risk_state,
        "assessment_state": assessment_state,
        "cycle_assessment": {**cycle, "intensity_score": _score_value(intensity)},
        "risk_assessments": card["risk_assessments"],
        "summary_markdown": "",
    }
    consensus["summary_markdown"] = render_scoring_summary(consensus, data["assessment_context"])
    return consensus


SUMMARY_START = "<!-- scoring-summary:start -->"
SUMMARY_END = "<!-- scoring-summary:end -->"


def _fmt(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def render_scoring_summary(consensus: Mapping, assessment_context: Mapping) -> str:
    """Render the machine-checkable scoring summary block; pure and deterministic."""
    lines = [
        SUMMARY_START,
        "| 键 | 值 |",
        "|---|---|",
        f"| rubric_version | {consensus['rubric_version']} |",
        f"| fact_snapshot_id | {consensus['fact_snapshot_id']} |",
        f"| scoring_input_hash | {consensus['scoring_input_hash']} |",
        f"| as_of | {assessment_context['as_of']} |",
        f"| forecast_period | {assessment_context['forecast_period']} |",
    ]
    for axis in consensus["axis_scores"]:
        lines.append(f"| 轴分 {axis['axis_id']} | {_fmt(axis['effective_score'])} |")
    lines.append(f"| 核心质量分 | {_fmt(consensus['core_quality']['score'])} |")
    sensitivity = consensus["sensitivity_range"]
    if sensitivity is None:
        sensitivity_text = "null"
    else:
        sensitivity_text = f"{_fmt(sensitivity['low'])} ~ {_fmt(sensitivity['high'])}"
    lines.append(f"| 敏感性区间 | {sensitivity_text} |")
    cycle = consensus["cycle_assessment"]
    lines.append(f"| 周期适用性 | {cycle['applicability']} |")
    lines.append(f"| 周期阶段 | {cycle['phase']} |")
    lines.append(f"| 周期方向 | {cycle['direction']} |")
    lines.append(f"| 周期强度 | {_fmt(cycle['intensity_score'])} |")
    lines.append(f"| 风险状态 | {consensus['risk_state']} |")
    lines.append(f"| 评估状态 | {consensus['assessment_state']} |")
    for item in consensus["risk_assessments"]:
        lines.append(f"| 风险检查 {item['rule_id']} | {item['status']} |")
    lines.append(SUMMARY_END)
    return "\n".join(lines)


def validate_consensus(consensus: object) -> Mapping:
    """Structural validation for a consensus record reloaded from disk."""
    data = _exact_keys(consensus, (
        "schema_version", "rubric_version", "fact_snapshot_id", "scoring_input_hash",
        "model_id", "axis_scores", "core_quality", "sensitivity_range",
        "risk_state", "assessment_state", "cycle_assessment", "risk_assessments",
        "summary_markdown",
    ), "consensus")
    if data["schema_version"] != CONSENSUS_SCHEMA:
        raise ScoringError("consensus.schema_version is not supported")
    for field in ("rubric_version", "fact_snapshot_id", "scoring_input_hash", "model_id"):
        _non_empty_string(data[field], f"consensus.{field}")
    core = _exact_keys(data["core_quality"], ("formula_version", "score"), "consensus.core_quality")
    if core["formula_version"] != FORMULA_VERSION:
        raise ScoringError("consensus.core_quality.formula_version is not supported")
    if data["risk_state"] not in RISK_STATES:
        raise ScoringError("consensus.risk_state is not supported")
    if data["assessment_state"] not in ASSESSMENT_STATES:
        raise ScoringError("consensus.assessment_state is not supported")
    if not isinstance(data["axis_scores"], list) or not data["axis_scores"]:
        raise ScoringError("consensus.axis_scores must be a non-empty list")
    for index, axis in enumerate(data["axis_scores"]):
        field = f"consensus.axis_scores[{index}]"
        _exact_keys(axis, ("axis_id", "raw_score", "effective_score", "dimensions"), field)
        _non_empty_string(axis["axis_id"], f"{field}.axis_id")
    sensitivity = data["sensitivity_range"]
    if sensitivity is not None:
        _exact_keys(sensitivity, ("low", "high"), "consensus.sensitivity_range")
        for field in ("low", "high"):
            value = sensitivity[field]
            if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ScoringError(f"consensus.sensitivity_range.{field} must be a number")
    _exact_keys(data["cycle_assessment"], (
        "applicability", "phase", "direction", "rationale", "components", "intensity_score",
    ), "consensus.cycle_assessment")
    return data
