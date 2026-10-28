"""Single-reviewer (propose-critique-revise) valuation input and consensus contract."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import sys
from typing import TypeVar


_SCRIPT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(_SCRIPT_DIR))
sys.path.insert(0, str(_SCRIPT_DIR.parent))

import evidence_contract as _evidence
import valuation_calculator as _calculator

_CATALOG_PATH = _SCRIPT_DIR.parent.parent / "references" / "valuation" / "valuation-models-v1.json"
_CATALOG: Mapping | None = None


def _catalog() -> Mapping:
    global _CATALOG
    catalog = _CATALOG
    if catalog is None:
        try:
            with _CATALOG_PATH.open("r", encoding="utf-8") as _catalog_file:
                catalog = json.load(_catalog_file)
        except (OSError, ValueError) as exc:
            raise ValuationConsensusError(f"bundled valuation catalog missing or corrupt: {exc}") from exc
        _CATALOG = catalog
    return catalog


INPUT_SCHEMA = "company-analysis-valuation-input-v1"
CARD_SCHEMA = "company-analysis-valuation-reviewer-card-v1"
CRITIQUE_SCHEMA = "company-analysis-valuation-critique-v1"
CRITIQUE_ISSUE_TYPES = frozenset({
    "method-applicability",
    "normalization",
    "scenario-boundary",
    "sensitivity-coverage",
    "invalidation-gap",
    "evidence-link",
})
ASSUMPTIONS_SCHEMA = _calculator.ASSUMPTIONS_SCHEMA
CALCULATOR_VERSION = _calculator.CALCULATOR_VERSION
CATALOG_VERSION = "company-analysis-valuation-model-catalog-v1"
SCENARIOS = ("conservative", "neutral", "optimistic")
ROLES = frozenset({"primary", "cross-check", "exclude"})
FORBIDDEN_KEY_FRAGMENTS = frozenset({
    "target-price",
    "fair-price",
    "price-target",
    "targetprice",
    "fairprice",
    "final-price",
    "final-equity-value",
    "final-per-share-value",
    "url",
    "search-query",
    "browser",
    "new-source",
    "external-source",
})
QUANT = Decimal("0.000001")
ZERO = Decimal("0")


class ValuationConsensusError(ValueError):
    """Raised when valuation consensus inputs are malformed or unresolved."""


def canonical_json_bytes(data: object) -> bytes:
    """Serialize valuation consensus data in canonical company-analysis form."""
    try:
        text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValuationConsensusError("data must be canonical JSON serializable") from exc
    return (text + "\n").encode("utf-8")


def content_hash(data: object) -> str:
    """Return the SHA-256 digest of canonical JSON data."""
    return _evidence.content_hash(data)


def valuation_input_hash(data: Mapping) -> str:
    """Hash a valuation input without its self-referential hash field."""
    valuation_input = _mapping(data, "valuation input")
    content = dict(valuation_input)
    content.pop("valuation_input_hash", None)
    return content_hash(content)


def validate_valuation_input(data: Mapping) -> Mapping:
    """Validate the frozen valuation input contract and its self hash."""
    valuation_input = _exact_keys(data, (
        "schema_version",
        "fact_snapshot_id",
        "market_snapshot_id",
        "model_version",
        "calculator_version",
        "method_catalog_version",
        "valuation_input_hash",
        "facts",
        "market",
        "methods",
    ), "valuation input")
    if valuation_input["schema_version"] != INPUT_SCHEMA:
        raise ValuationConsensusError("valuation input.schema_version is not supported")
    for key in (
        "fact_snapshot_id",
        "market_snapshot_id",
        "model_version",
        "calculator_version",
        "method_catalog_version",
        "valuation_input_hash",
    ):
        _non_empty_string(valuation_input[key], f"valuation input.{key}")
    if valuation_input["calculator_version"] != CALCULATOR_VERSION:
        raise ValuationConsensusError("valuation input.calculator_version is not supported")
    if valuation_input["method_catalog_version"] != CATALOG_VERSION:
        raise ValuationConsensusError("valuation input.method_catalog_version is not supported")

    facts = _validate_fact_records(valuation_input["facts"], "valuation input.facts")
    for fact_id, fact in facts.items():
        if isinstance(fact.get("value"), (bool, float)):
            raise ValuationConsensusError(f"valuation input.facts[{fact_id}].value must not be bool or float")

    valuation_currency = _validate_market(valuation_input["market"])
    _validate_structural_methods(valuation_input["methods"], facts, valuation_currency, valuation_input["market"])
    if valuation_input["valuation_input_hash"] != valuation_input_hash(valuation_input):
        raise ValuationConsensusError("valuation input.valuation_input_hash does not match canonical input content")
    return data


def validate_reviewer_card(card: Mapping, valuation_input: Mapping) -> Mapping:
    """Validate one reviewer card against a frozen valuation input."""
    _scan_forbidden_keys(card, "reviewer card")
    validate_valuation_input(valuation_input)
    data = _exact_keys(card, (
        "schema_version",
        "reviewer_id",
        "fact_snapshot_id",
        "market_snapshot_id",
        "valuation_input_hash",
        "model_id",
        "calculator_version",
        "method_catalog_version",
        "method_judgments",
        "normalizations",
        "scenario_parameters",
        "calibrations",
        "reverse_valuation",
        "sensitivity_factors",
        "invalidation_conditions",
    ), "reviewer card")
    if data["schema_version"] != CARD_SCHEMA:
        raise ValuationConsensusError("reviewer card.schema_version is not supported")
    for key in (
        "reviewer_id",
        "fact_snapshot_id",
        "market_snapshot_id",
        "valuation_input_hash",
        "model_id",
        "calculator_version",
        "method_catalog_version",
    ):
        _non_empty_string(data[key], f"reviewer card.{key}")
    for card_key, input_key in (
        ("fact_snapshot_id", "fact_snapshot_id"),
        ("market_snapshot_id", "market_snapshot_id"),
        ("valuation_input_hash", "valuation_input_hash"),
        ("model_id", "model_version"),
        ("calculator_version", "calculator_version"),
        ("method_catalog_version", "method_catalog_version"),
    ):
        if data[card_key] != valuation_input[input_key]:
            raise ValuationConsensusError(f"reviewer card.{card_key} must match the valuation input")

    facts = _facts_by_id(valuation_input)
    methods = _methods_by_id(valuation_input["methods"])
    _validate_method_judgments(data["method_judgments"], methods, facts)
    _validate_normalizations(data["normalizations"], facts)
    _validate_scenario_parameters(data["scenario_parameters"], methods, valuation_input)
    _validate_calibrations(data["calibrations"], methods, facts)
    _validate_reverse_valuation(data["reverse_valuation"], methods, facts)
    _validate_sensitivity_factors(data["sensitivity_factors"], methods, facts)
    _validate_invalidation_conditions(data["invalidation_conditions"], methods, facts)
    return card


def validate_critique(critique: Mapping, valuation_input: Mapping) -> Mapping:
    """Validate a valuation critique artifact against the frozen valuation input."""
    _scan_forbidden_keys(critique, "critique")
    validate_valuation_input(valuation_input)
    data = _exact_keys(critique, (
        "schema_version",
        "valuation_input_hash",
        "critic_id",
        "target_card",
        "items",
    ), "critique")
    if data["schema_version"] != CRITIQUE_SCHEMA:
        raise ValuationConsensusError("critique.schema_version is not supported")
    if data["valuation_input_hash"] != valuation_input["valuation_input_hash"]:
        raise ValuationConsensusError("critique.valuation_input_hash must match the valuation input")
    _non_empty_string(data["critic_id"], "critique.critic_id")
    _non_empty_string(data["target_card"], "critique.target_card")
    facts = _facts_by_id(valuation_input)
    items = _list(data["items"], "critique.items")
    for index, item in enumerate(items):
        entry = _exact_keys(item, (
            "target",
            "issue_type",
            "argument",
            "counter_evidence_fact_ids",
            "suggested_revision",
        ), f"critique.items[{index}]")
        _non_empty_string(entry["target"], f"critique.items[{index}].target")
        issue_type = _non_empty_string(entry["issue_type"], f"critique.items[{index}].issue_type")
        if issue_type not in CRITIQUE_ISSUE_TYPES:
            raise ValuationConsensusError("critique.items.issue_type is not supported")
        _non_empty_string(entry["argument"], f"critique.items[{index}].argument")
        fact_ids = _unique_string_list(
            entry["counter_evidence_fact_ids"], f"critique.items[{index}].counter_evidence_fact_ids"
        )
        unknown = [fact_id for fact_id in fact_ids if fact_id not in facts]
        if unknown:
            raise ValuationConsensusError(
                "critique.items.counter_evidence_fact_ids must reference facts in the valuation input snapshot"
            )
        unverified = [fact_id for fact_id in fact_ids if facts[fact_id]["status"] != "verified"]
        if unverified:
            raise ValuationConsensusError(
                "critique.items.counter_evidence_fact_ids must reference verified facts"
            )
        _non_empty_string(entry["suggested_revision"], f"critique.items[{index}].suggested_revision")
    return critique


def aggregate_reviewer_card(valuation_input: Mapping, card: Mapping, critique: Mapping) -> dict:
    """Derive deterministic consensus assumptions from one post-critique reviewer card."""
    validate_valuation_input(valuation_input)
    validate_critique(critique, valuation_input)
    validate_reviewer_card(card, valuation_input)
    if critique["target_card"] != card["reviewer_id"]:
        raise ValuationConsensusError("critique.target_card must reference the installed reviewer card")
    method_ids = [method["method_id"] for method in valuation_input["methods"]]
    judgments = {entry["method_id"]: entry for entry in card["method_judgments"]}
    exclusions = _method_exclusions([
        (method_id, card["reviewer_id"], condition)
        for method_id in method_ids
        if not judgments[method_id]["applicable"] and judgments[method_id]["preferred_role"] == "exclude"
        for condition in judgments[method_id]["disable_conditions"]
    ])
    disabled_method_ids = {item["method_id"] for item in exclusions}
    applicable = [
        method_id for method_id in method_ids
        if judgments[method_id]["applicable"] and method_id not in disabled_method_ids
    ]
    primary_method_id = next(
        (method_id for method_id in applicable if judgments[method_id]["preferred_role"] == "primary"),
        None,
    )
    primary_role_fallback = primary_method_id is None and bool(applicable)
    if primary_role_fallback:
        primary_method_id = applicable[0]
    cross_check_method_ids = [
        method_id for method_id in applicable
        if method_id != primary_method_id and judgments[method_id]["preferred_role"] == "cross-check"
    ][:2]
    cross_check_only = [
        method_id for method_id in applicable
        if method_id not in {primary_method_id, *cross_check_method_ids}
    ]
    base = {
        "schema_version": ASSUMPTIONS_SCHEMA,
        "calculator_version": valuation_input["calculator_version"],
        "valuation_input_hash": valuation_input["valuation_input_hash"],
        "primary_method_id": primary_method_id,
        "cross_check_method_ids": cross_check_method_ids,
        "fact_snapshot_id": valuation_input["fact_snapshot_id"],
        "market_snapshot_id": valuation_input["market_snapshot_id"],
        "model_version": valuation_input["model_version"],
        "method_catalog_version": valuation_input["method_catalog_version"],
        "method_exclusions": exclusions,
        "cross_check_only_method_ids": cross_check_only,
        "primary_role_fallback": primary_role_fallback,
        "critique_hash": content_hash(critique),
        "normalizations": deepcopy_json(card["normalizations"]),
        "calibrations": _calibration_audit([card]),
        "reverse_valuation": _reverse_audit([card]),
        "sensitivity_factors": _sensitivity_factor_audit([card]),
        "invalidation_conditions": _invalidation_condition_audit([card]),
    }
    if primary_method_id is None:
        return base | {
            "methods": [],
            "status": "evidence-insufficient",
            "publication_precision_state": "suppressed",
            "primary_range": None,
        }
    selected_method_ids = sorted([primary_method_id, *cross_check_method_ids])
    methods = [
        deepcopy_json(_entry_by_id(card["scenario_parameters"], method_id, "method_id")["method"])
        for method_id in selected_method_ids
    ]
    aggregate_calculation = _calculate(
        valuation_input,
        _calculator_assumptions(valuation_input, primary_method_id, cross_check_method_ids, methods),
    )
    indicative_input = (
        _uses_assumption_input(
            valuation_input,
            {"primary_method_id": primary_method_id, "cross_check_method_ids": cross_check_method_ids},
        )
        or primary_role_fallback
        or _unbound_scenario_evidence(methods)
    )
    return base | {
        "methods": methods,
        "status": "indicative-consensus" if indicative_input else "consensus",
        "publication_precision_state": "indicative" if indicative_input else "precise",
        "primary_range": expected_primary_range(aggregate_calculation, primary_method_id),
    }


def _uses_assumption_input(valuation_input: Mapping, selection: Mapping) -> bool:
    selected = {selection["primary_method_id"], *selection["cross_check_method_ids"]}
    facts = {fact["fact_id"]: fact for fact in valuation_input["facts"]}
    for method in valuation_input["methods"]:
        if method["method_id"] not in selected:
            continue
        fact_ids = [method[key] for key in ("denominator_fact_id", "diluted_shares_fact_id") if key in method]
        fact_ids.extend(method.get("bridge_fact_ids", {}).values())
        if any(
            facts[fact_id]["fact_type"] == "assumption" and facts[fact_id]["status"] == "unverified"
            for fact_id in fact_ids
        ):
            return True
    return False


def _method_exclusions(disable_sources: Sequence[tuple[str, str, Mapping]]) -> list[dict]:
    grouped: dict[tuple[str, str, str, tuple[str, ...]], list[dict]] = {}
    for method_id, reviewer_id, condition in disable_sources:
        evidence_fact_ids = tuple(sorted(condition["evidence_fact_ids"]))
        identity = (method_id, condition["code"], condition["reason"], evidence_fact_ids)
        grouped.setdefault(identity, []).append({"reviewer_id": reviewer_id})
    return [
        {
            "method_id": method_id,
            "code": code,
            "reason": reason,
            "evidence_fact_ids": list(evidence_fact_ids),
            "provenance": sorted(provenance, key=lambda item: item["reviewer_id"]),
        }
        for (method_id, code, reason, evidence_fact_ids), provenance in sorted(grouped.items())
    ]


def _calibration_audit(ordered_cards: Sequence[Mapping]) -> list[dict]:
    return sorted(
        [
            {"reviewer_id": card["reviewer_id"]} | deepcopy_json(item)
            for card in ordered_cards
            for item in card["calibrations"]
        ],
        key=lambda item: (item["method_id"], item["reviewer_id"], item["rationale"]),
    )


def _reverse_audit(ordered_cards: Sequence[Mapping]) -> list[dict]:
    return sorted(
        [
            {"reviewer_id": card["reviewer_id"]} | deepcopy_json(item)
            for card in ordered_cards
            for item in card["reverse_valuation"]
        ],
        key=lambda item: (item["method_id"], item["reviewer_id"], item["interpretation"]),
    )


def _sensitivity_factor_audit(ordered_cards: Sequence[Mapping]) -> list[dict]:
    return sorted(
        [
            {"reviewer_id": card["reviewer_id"]} | deepcopy_json(item)
            for card in ordered_cards
            for item in card["sensitivity_factors"]
        ],
        key=lambda item: (item["method_id"], item["factor"], item["reason"], item["reviewer_id"]),
    )


def _invalidation_condition_audit(ordered_cards: Sequence[Mapping]) -> list[dict]:
    return sorted(
        [
            {"reviewer_id": card["reviewer_id"]} | deepcopy_json(item)
            for card in ordered_cards
            for item in card["invalidation_conditions"]
        ],
        key=lambda item: (item["method_id"], item["code"], item["condition"], item["reviewer_id"]),
    )


def _calculator_assumptions(
    valuation_input: Mapping, primary_method_id: str, cross_check_method_ids: Sequence[str], methods: Sequence[Mapping],
) -> dict:
    return {
        "schema_version": ASSUMPTIONS_SCHEMA,
        "calculator_version": valuation_input["calculator_version"],
        "valuation_input_hash": valuation_input["valuation_input_hash"],
        "primary_method_id": primary_method_id,
        "cross_check_method_ids": list(cross_check_method_ids),
        "methods": list(methods),
    }


def _calculate(valuation_input: Mapping, assumptions: Mapping) -> Mapping:
    try:
        return _calculator.calculate_valuation(valuation_input, assumptions)
    except _calculator.ValuationError as exc:
        raise ValuationConsensusError(str(exc)) from exc


def expected_primary_range(calculation: Mapping, primary_method_id: str) -> dict:
    """Deterministic primary neutral range; recalculations must reproduce it exactly."""
    method = next(item for item in calculation["methods"] if item["method_id"] == primary_method_id)
    scenario = next(item for item in method["scenarios"] if item["scenario"] == "neutral")
    price_range = scenario["price_range"]
    lower = _decimal(price_range["lower"], "primary neutral lower")
    upper = _decimal(price_range["upper"], "primary neutral upper")
    if upper <= ZERO:
        raise ValuationConsensusError("primary neutral range upper must be positive")
    return {
        "lower": price_range["lower"],
        "upper": price_range["upper"],
        "center": _format_decimal((lower + upper) / Decimal("2")),
    }


def _unbound_scenario_evidence(methods: Sequence[Mapping]) -> bool:
    # dcf/sotp scenarios cite evidence per bound; an unbound range stays indicative.
    for method in methods:
        if method["family"] not in {"dcf-fcff", "sotp"}:
            continue
        for scenario in method["scenarios"].values():
            for side in ("lower", "upper"):
                if "evidence_fact_ids" not in scenario["range"][side]:
                    return True
    return False


def _validate_method_judgments(value: object, methods: Mapping[str, Mapping], facts: Mapping[str, Mapping]) -> None:
    entries = _entries_for_methods(value, methods, "reviewer card.method_judgments")
    for index, judgment in enumerate(entries):
        item = _exact_keys(judgment, (
            "method_id",
            "applicable",
            "preferred_role",
            "evidence_fact_ids",
            "rationale",
            "disable_conditions",
        ), f"reviewer card.method_judgments[{index}]")
        if not isinstance(item["applicable"], bool):
            raise ValuationConsensusError("method_judgments.applicable must be a boolean")
        preferred_role = _non_empty_string(item["preferred_role"], "method_judgments.preferred_role")
        if preferred_role not in ROLES:
            raise ValuationConsensusError("method_judgments.preferred_role is not supported")
        if preferred_role == "exclude" and item["applicable"]:
            raise ValuationConsensusError("preferred_role exclude requires applicable=false")
        _verified_evidence_fact_ids(item["evidence_fact_ids"], "method_judgments.evidence_fact_ids", facts)
        _non_empty_string(item["rationale"], "method_judgments.rationale")
        disable_conditions = _list(item["disable_conditions"], "method_judgments.disable_conditions")
        for condition_index, condition in enumerate(disable_conditions):
            data = _exact_keys(
                condition,
                ("code", "reason", "evidence_fact_ids"),
                f"method_judgments.disable_conditions[{condition_index}]",
            )
            _non_empty_string(data["code"], "disable_conditions.code")
            _non_empty_string(data["reason"], "disable_conditions.reason")
            _verified_evidence_fact_ids(data["evidence_fact_ids"], "disable_conditions.evidence_fact_ids", facts)
        if disable_conditions and (item["applicable"] or preferred_role != "exclude"):
            raise ValuationConsensusError(
                "method_judgments with disable_conditions must set applicable=false and preferred_role exclude"
            )


def _validate_normalizations(value: object, facts: Mapping[str, Mapping]) -> None:
    normalizations = _list(value, "reviewer card.normalizations")
    parameter_ids = set()
    for index, normalization in enumerate(normalizations):
        item = _exact_keys(normalization, (
            "parameter_id",
            "kind",
            "value",
            "lower",
            "upper",
            "unit",
            "evidence_fact_ids",
            "rationale",
        ), f"reviewer card.normalizations[{index}]")
        parameter_id = _non_empty_string(item["parameter_id"], "normalizations.parameter_id")
        if parameter_id in parameter_ids:
            raise ValuationConsensusError("normalizations contains duplicate parameter_id")
        parameter_ids.add(parameter_id)
        kind = _non_empty_string(item["kind"], "normalizations.kind")
        if kind not in {"scalar", "interval"}:
            raise ValuationConsensusError("normalizations.kind is not supported")
        if kind == "scalar":
            _decimal(item["value"], "normalizations.value")
            if item["lower"] is not None or item["upper"] is not None:
                raise ValuationConsensusError("scalar normalizations require null bounds")
        else:
            if item["value"] is not None:
                raise ValuationConsensusError("interval normalizations require null value")
            lower = _decimal(item["lower"], "normalizations.lower")
            upper = _decimal(item["upper"], "normalizations.upper")
            if lower > upper:
                raise ValuationConsensusError("normalization interval lower must be less than or equal to upper")
        unit = _non_empty_string(item["unit"], "normalizations.unit")
        if any(scale in unit.casefold() for scale in ("万", "亿", "million", "billion", "trillion")):
            raise ValuationConsensusError("normalizations.unit must be unscaled; rescale the value instead")
        _verified_evidence_fact_ids(item["evidence_fact_ids"], "normalizations.evidence_fact_ids", facts)
        _non_empty_string(item["rationale"], "normalizations.rationale")


def _validate_scenario_parameters(
    value: object, methods: Mapping[str, Mapping], valuation_input: Mapping,
) -> None:
    entries = _entries_for_methods(value, methods, "reviewer card.scenario_parameters")
    for index, entry in enumerate(entries):
        item = _exact_keys(entry, ("method_id", "method"), f"scenario_parameters[{index}]")
        method_id = item["method_id"]
        _validate_method_proposal(item["method"], methods[method_id], valuation_input, f"scenario_parameters[{index}].method")


def _validate_method_proposal(
    method: object, structural_method: Mapping, valuation_input: Mapping, field: str,
) -> None:
    item = _mapping(method, field)
    structural_keys = set(structural_method)
    expected_keys = structural_keys | {"scenarios", "sensitivity"}
    if set(item) != expected_keys:
        raise ValuationConsensusError(f"{field} mapping shapes must match expected calculator method fields")
    for key in structural_keys:
        if item[key] != structural_method[key]:
            raise ValuationConsensusError(f"{field}.{key} structural field must match the valuation input")
    facts = _facts_by_id(valuation_input)
    _validate_scenarios(item, facts, f"{field}.scenarios")
    _validate_sensitivity(item, facts, f"{field}.sensitivity")
    assumptions = _calculator_assumptions(valuation_input, item["method_id"], [], [item])
    _calculate(valuation_input, assumptions)


def _validate_scenarios(method: Mapping, facts: Mapping[str, Mapping], field: str) -> None:
    scenarios = _mapping(method["scenarios"], field)
    if set(scenarios) != set(SCENARIOS):
        raise ValuationConsensusError(f"{field} must contain exactly conservative, neutral, and optimistic")
    family = method["family"]
    if family in {"price-multiple", "enterprise-multiple"}:
        for scenario in SCENARIOS:
            data = _exact_keys(scenarios[scenario], ("denominator", "range"), f"{field}.{scenario}")
            _positive_decimal(data["denominator"], f"{field}.{scenario}.denominator")
            _simple_range(data["range"], f"{field}.{scenario}.range", positive=True)
        _require_shared_boundaries(scenarios, field, yield_family=False)
    elif family == "yield":
        for scenario in SCENARIOS:
            data = _exact_keys(scenarios[scenario], ("denominator", "range"), f"{field}.{scenario}")
            _positive_decimal(data["denominator"], f"{field}.{scenario}.denominator")
            _simple_range(data["range"], f"{field}.{scenario}.range", positive=True)
        _require_shared_boundaries(scenarios, field, yield_family=True)
    elif family == "dcf-fcff":
        for scenario in SCENARIOS:
            data = _exact_keys(scenarios[scenario], ("range",), f"{field}.{scenario}")
            lower, upper = _case_range(data["range"], f"{field}.{scenario}.range")
            _validate_dcf_case(lower, facts, f"{field}.{scenario}.range.lower")
            _validate_dcf_case(upper, facts, f"{field}.{scenario}.range.upper")
    elif family == "sotp":
        for scenario in SCENARIOS:
            data = _exact_keys(scenarios[scenario], ("range",), f"{field}.{scenario}")
            lower, upper = _case_range(data["range"], f"{field}.{scenario}.range")
            _validate_sotp_case(lower, facts, f"{field}.{scenario}.range.lower")
            _validate_sotp_case(upper, facts, f"{field}.{scenario}.range.upper")
    else:
        raise ValuationConsensusError("method.family is not supported")


def _require_shared_boundaries(scenarios: Mapping, field: str, *, yield_family: bool) -> None:
    ranges = {
        scenario: _simple_range(scenarios[scenario]["range"], f"{field}.{scenario}.range", positive=True)
        for scenario in SCENARIOS
    }
    if yield_family:
        thresholds = (
            ranges["optimistic"][0],
            ranges["optimistic"][1],
            ranges["neutral"][1],
            ranges["conservative"][1],
        )
        if ranges["optimistic"][1] != ranges["neutral"][0] or ranges["neutral"][1] != ranges["conservative"][0]:
            raise ValuationConsensusError(f"{field} yield ranges must share scenario boundaries")
    else:
        thresholds = (
            ranges["conservative"][0],
            ranges["conservative"][1],
            ranges["neutral"][1],
            ranges["optimistic"][1],
        )
        if ranges["conservative"][1] != ranges["neutral"][0] or ranges["neutral"][1] != ranges["optimistic"][0]:
            raise ValuationConsensusError(f"{field} ranges must share scenario boundaries")
    if not all(left < right for left, right in zip(thresholds, thresholds[1:])):
        raise ValuationConsensusError(f"{field} scenario ranges must be strictly ordered")


def _validate_sensitivity(method: Mapping, facts: Mapping[str, Mapping], field: str) -> None:
    sensitivity = _mapping(method["sensitivity"], field)
    family = method["family"]
    expected_parameters = _calculator.SENSITIVITY_PARAMETERS[family]
    expected_keys = {"row_parameter", "row_values", "column_parameter", "column_values"}
    if family in {"dcf-fcff", "sotp"}:
        expected_keys.add("base_case")
    if set(sensitivity) != expected_keys:
        raise ValuationConsensusError(f"{field} must be a valid 3x3 sensitivity grid")
    row_parameter = _non_empty_string(sensitivity["row_parameter"], f"{field}.row_parameter")
    column_parameter = _non_empty_string(sensitivity["column_parameter"], f"{field}.column_parameter")
    if row_parameter == column_parameter or {row_parameter, column_parameter} != expected_parameters:
        raise ValuationConsensusError(f"{field} parameters must match method family")
    for key in ("row_values", "column_values"):
        values = _list(sensitivity[key], f"{field}.{key}")
        if len(values) != 3:
            raise ValuationConsensusError(f"{field}.{key} must contain exactly three values")
        for index, value in enumerate(values):
            _decimal(value, f"{field}.{key}[{index}]")
    if family == "dcf-fcff":
        _validate_dcf_case(sensitivity["base_case"], facts, f"{field}.base_case")
    elif family == "sotp":
        _validate_sotp_case(sensitivity["base_case"], facts, f"{field}.base_case")


def _validate_calibrations(value: object, methods: Mapping[str, Mapping], facts: Mapping[str, Mapping]) -> None:
    entries = _entries_for_methods(value, methods, "reviewer card.calibrations")
    for index, calibration in enumerate(entries):
        item = _exact_keys(calibration, (
            "method_id",
            "historical",
            "peers",
            "evidence_fact_ids",
            "rationale",
        ), f"reviewer card.calibrations[{index}]")
        _simple_range(item["historical"], "calibrations.historical", positive=True)
        _simple_range(item["peers"], "calibrations.peers", positive=True)
        _verified_evidence_fact_ids(item["evidence_fact_ids"], "calibrations.evidence_fact_ids", facts)
        _non_empty_string(item["rationale"], "calibrations.rationale")


def _validate_reverse_valuation(value: object, methods: Mapping[str, Mapping], facts: Mapping[str, Mapping]) -> None:
    entries = _entries_for_methods(value, methods, "reviewer card.reverse_valuation")
    for index, reverse in enumerate(entries):
        item = _exact_keys(reverse, (
            "method_id",
            "interpretation",
            "evidence_fact_ids",
            "invalidation_condition",
        ), f"reviewer card.reverse_valuation[{index}]")
        _non_empty_string(item["interpretation"], "reverse_valuation.interpretation")
        _verified_evidence_fact_ids(item["evidence_fact_ids"], "reverse_valuation.evidence_fact_ids", facts)
        _non_empty_string(item["invalidation_condition"], "reverse_valuation.invalidation_condition")


def _validate_sensitivity_factors(value: object, methods: Mapping[str, Mapping], facts: Mapping[str, Mapping]) -> None:
    entries = _entries_for_methods(value, methods, "reviewer card.sensitivity_factors")
    seen = set()
    for index, factor in enumerate(entries):
        item = _exact_keys(factor, (
            "method_id",
            "factor",
            "reason",
            "evidence_fact_ids",
        ), f"reviewer card.sensitivity_factors[{index}]")
        method_id = _non_empty_string(item["method_id"], "sensitivity_factors.method_id")
        if method_id not in methods:
            raise ValuationConsensusError("sensitivity_factors.method_id must identify an input method")
        _non_empty_string(item["factor"], "sensitivity_factors.factor")
        _non_empty_string(item["reason"], "sensitivity_factors.reason")
        _verified_evidence_fact_ids(item["evidence_fact_ids"], "sensitivity_factors.evidence_fact_ids", facts)
        identity = json.dumps(item, ensure_ascii=False, sort_keys=True, allow_nan=False)
        if identity in seen:
            raise ValuationConsensusError("sensitivity_factors must not contain exact duplicates")
        seen.add(identity)


def _validate_invalidation_conditions(value: object, methods: Mapping[str, Mapping], facts: Mapping[str, Mapping]) -> None:
    entries = _entries_for_methods(value, methods, "reviewer card.invalidation_conditions")
    seen = set()
    for index, condition in enumerate(entries):
        item = _exact_keys(condition, (
            "method_id",
            "code",
            "condition",
            "evidence_fact_ids",
        ), f"reviewer card.invalidation_conditions[{index}]")
        method_id = _non_empty_string(item["method_id"], "invalidation_conditions.method_id")
        if method_id not in methods:
            raise ValuationConsensusError("invalidation_conditions.method_id must identify an input method")
        _non_empty_string(item["code"], "invalidation_conditions.code")
        _non_empty_string(item["condition"], "invalidation_conditions.condition")
        _verified_evidence_fact_ids(item["evidence_fact_ids"], "invalidation_conditions.evidence_fact_ids", facts)
        identity = json.dumps(item, ensure_ascii=False, sort_keys=True, allow_nan=False)
        if identity in seen:
            raise ValuationConsensusError("invalidation_conditions must not contain exact duplicates")
        seen.add(identity)


def _validate_structural_methods(methods: object, facts: Mapping[str, Mapping], current_price_currency: str, market: Mapping) -> dict[str, Mapping]:
    items = _list(methods, "valuation input.methods")
    if not items:
        raise ValuationConsensusError("valuation input.methods must be a non-empty list")
    by_id = {}
    for index, method in enumerate(items):
        item = _mapping(method, f"valuation input.methods[{index}]")
        method_id = _non_empty_string(item.get("method_id"), f"valuation input.methods[{index}].method_id")
        if method_id in by_id:
            raise ValuationConsensusError("valuation input.methods contains duplicate method_id")
        family = _non_empty_string(item.get("family"), f"valuation input.methods[{index}].family")
        catalog = _catalog_family(family)
        required_keys = set(catalog["required_method_fields"]) - {"scenarios"}
        optional_keys = set()
        if any(field.startswith("bridge_fact_ids.") for field in catalog.get("optional_method_fields", [])):
            optional_keys.add("bridge_fact_ids")
        expected_keys = required_keys | optional_keys
        if not required_keys <= set(item) <= expected_keys:
            raise ValuationConsensusError(f"valuation input.methods[{index}] has invalid structural keys")
        if item["direction"] != catalog["direction"]:
            raise ValuationConsensusError(f"valuation input.methods[{index}].direction must match method catalog")
        for key in ("denominator_fact_id", "diluted_shares_fact_id"):
            if key in item:
                _validate_fact_reference(
                    item[key],
                    f"valuation input.methods[{index}].{key}",
                    facts,
                    current_price_currency,
                    require_currency=(key == "denominator_fact_id"),
                )
        if "denominator_fact_id" in item:
            denominator = facts[item["denominator_fact_id"]]
            field = f"valuation input.methods[{index}].denominator_fact_id"
            _positive_decimal(denominator["value"], f"{field} fact value")
            if family in {"price-multiple", "yield"}:
                if _calculator.canonical_per_share_unit(denominator["unit"], current_price_currency) is None:
                    raise ValuationConsensusError(f"{field}.unit must be unscaled {current_price_currency}/share")
            else:
                if _calculator.canonical_aggregate_money_unit(denominator["unit"], denominator["currency"]) is None:
                    raise ValuationConsensusError(f"{field}.unit must be an unscaled {denominator['currency']} amount")
                if family == "enterprise-multiple" and "current_enterprise_value" in market:
                    current_ev = market["current_enterprise_value"]
                    if current_ev["currency"] != denominator["currency"]:
                        raise ValuationConsensusError("valuation input.market.current_enterprise_value.currency must match denominator currency")
                    if not _calculator.equivalent_aggregate_money_units(current_ev["unit"], denominator["unit"], denominator["currency"]):
                        raise ValuationConsensusError("valuation input.market.current_enterprise_value.unit must match denominator aggregate monetary unit")
        if "diluted_shares_fact_id" in item:
            shares_fact = facts[item["diluted_shares_fact_id"]]
            _positive_decimal(shares_fact["value"], f"valuation input.methods[{index}].diluted_shares_fact_id fact value")
            if _calculator.canonical_share_count_unit(shares_fact["unit"]) is None:
                raise ValuationConsensusError(f"valuation input.methods[{index}].diluted_shares_fact_id.unit must be shares")
        if "bridge_fact_ids" in item:
            _validate_bridge_fact_ids(item["bridge_fact_ids"], f"valuation input.methods[{index}].bridge_fact_ids", facts, current_price_currency)
        by_id[method_id] = item
    return by_id


def _validate_bridge_fact_ids(value: object, field: str, facts: Mapping[str, Mapping], current_price_currency: str) -> None:
    data = _mapping(value, field)
    allowed = {"debt", "lease_liabilities", "minority_interest", "preferred_claims", "excess_cash"}
    if not set(data) <= allowed:
        raise ValuationConsensusError(f"{field} contains unsupported bridge fact keys")
    fact_ids = list(data.values())
    if len(set(fact_ids)) != len(fact_ids):
        raise ValuationConsensusError(f"{field} must not reference the same fact in two bridge keys")
    for key, fact_id in data.items():
        _validate_fact_reference(fact_id, f"{field}.{key}", facts, current_price_currency, require_currency=True)
        fact = facts[fact_id]
        _positive_decimal(fact["value"], f"{field}.{key} fact value")
        if _calculator.canonical_aggregate_money_unit(fact["unit"], fact["currency"]) is None:
            raise ValuationConsensusError(f"{field}.{key}.unit must be an unscaled {current_price_currency} amount")


def _validate_fact_reference(
    value: object, field: str, facts: Mapping[str, Mapping], current_price_currency: str, *, require_currency: bool,
) -> None:
    fact_id = _non_empty_string(value, field)
    if fact_id not in facts:
        raise ValuationConsensusError(f"{field} must reference a fact in valuation input")
    fact = facts[fact_id]
    if fact["status"] != "verified" and not (
        fact["fact_type"] == "assumption" and fact["status"] == "unverified"
    ):
        raise ValuationConsensusError(f"{field} must reference a verified fact or an explicit assumption")
    currency = fact.get("currency")
    if require_currency and currency != current_price_currency:
        raise ValuationConsensusError(f"{field}.currency must match current price currency")


def _validate_market(market: object) -> str:
    data = _mapping(market, "valuation input.market")
    valuation_currency = None
    if "valuation_currency" in data:
        valuation_currency = _currency_code(data["valuation_currency"], "valuation input.market.valuation_currency")
    if "current_price" not in data and valuation_currency is None:
        raise ValuationConsensusError("valuation input.market needs current_price or valuation_currency")
    for key, value in data.items():
        if key == "valuation_currency":
            continue
        item = _exact_keys(value, ("value", "currency", "unit", "date"), f"valuation input.market.{key}")
        amount = _positive_decimal(item["value"], f"valuation input.market.{key}.value")
        currency = _currency_code(item["currency"], f"valuation input.market.{key}.currency")
        unit = _non_empty_string(item["unit"], f"valuation input.market.{key}.unit")
        date = _non_empty_string(item["date"], f"valuation input.market.{key}.date")
        if key == "current_price":
            if _calculator.canonical_per_share_unit(unit, currency) is None:
                raise ValuationConsensusError("valuation input.market.current_price.unit must be per-share")
            if valuation_currency is not None and currency != valuation_currency:
                raise ValuationConsensusError("valuation input.market.current_price.currency must match valuation_currency")
            valuation_currency = currency
    assert valuation_currency is not None
    return valuation_currency


def _entries_for_methods(value: object, methods: Mapping[str, Mapping], field: str) -> list[Mapping]:
    entries = _list(value, field)
    if len(entries) != len(methods):
        raise ValuationConsensusError(f"{field} must contain exactly one entry per frozen method")
    method_ids = []
    for index, entry in enumerate(entries):
        item = _mapping(entry, f"{field}[{index}]")
        method_ids.append(_non_empty_string(item.get("method_id"), f"{field}[{index}].method_id"))
    if len(set(method_ids)) != len(method_ids):
        raise ValuationConsensusError(f"{field} contains duplicate method_id")
    if set(method_ids) != set(methods):
        raise ValuationConsensusError(f"{field} must contain the same method IDs as valuation input")
    return entries


def _entry_by_id(entries: Sequence[Mapping], item_id: str, key: str) -> Mapping:
    return next(entry for entry in entries if entry[key] == item_id)


def _facts_by_id(valuation_input: Mapping) -> Mapping[str, Mapping]:
    return _validate_fact_records(valuation_input["facts"], "valuation input.facts")


def _methods_by_id(methods: Sequence[Mapping]) -> dict[str, Mapping]:
    return {method["method_id"]: method for method in methods}


def _validate_fact_records(facts: object, field: str) -> Mapping[str, Mapping]:
    try:
        return _evidence.validate_fact_records(facts, field=field)
    except _evidence.EvidenceError as exc:
        raise ValuationConsensusError(str(exc)) from exc


def _catalog_family(family: str) -> Mapping:
    for item in _catalog()["method_families"]:
        if item["family"] == family:
            return item
    raise ValuationConsensusError("valuation input.methods.family is not supported")


def _verified_evidence_fact_ids(value: object, field: str, facts: Mapping[str, Mapping]) -> list[str]:
    fact_ids = _unique_string_list(value, field)
    if not fact_ids:
        raise ValuationConsensusError(f"{field} must not be empty")
    unknown = [fact_id for fact_id in fact_ids if fact_id not in facts]
    if unknown:
        raise ValuationConsensusError(f"{field} must reference facts in the valuation input snapshot")
    unverified = [fact_id for fact_id in fact_ids if facts[fact_id]["status"] != "verified"]
    if unverified:
        raise ValuationConsensusError(f"{field} must reference verified facts in the valuation input snapshot")
    return fact_ids


def _simple_range(value: object, field: str, *, positive: bool) -> tuple[Decimal, Decimal]:
    data = _exact_keys(value, ("lower", "upper"), field)
    lower = _decimal(data["lower"], f"{field}.lower")
    upper = _decimal(data["upper"], f"{field}.upper")
    if positive:
        if lower <= ZERO or upper <= ZERO:
            raise ValuationConsensusError(f"{field} values must be positive")
    if lower > upper:
        raise ValuationConsensusError(f"{field} range lower must be less than or equal to upper")
    return lower, upper


def _case_range(value: object, field: str) -> tuple[Mapping, Mapping]:
    data = _exact_keys(value, ("lower", "upper"), field)
    return _mapping(data["lower"], f"{field}.lower"), _mapping(data["upper"], f"{field}.upper")


def _validate_dcf_case(value: object, facts: Mapping[str, Mapping], field: str) -> None:
    data = _mapping(value, field)
    required = ("fcff", "wacc", "terminal_growth")
    keys = required + (("evidence_fact_ids",) if "evidence_fact_ids" in data else ())
    data = _exact_keys(value, keys, field)
    fcff = _list(data["fcff"], f"{field}.fcff")
    if not fcff:
        raise ValuationConsensusError(f"{field}.fcff must be a non-empty list")
    for index, cash_flow in enumerate(fcff):
        _decimal(cash_flow, f"{field}.fcff[{index}]")
    wacc = _positive_decimal(data["wacc"], f"{field}.wacc")
    terminal_growth = _decimal(data["terminal_growth"], f"{field}.terminal_growth")
    if wacc <= terminal_growth:
        raise ValuationConsensusError(f"{field}.wacc must exceed terminal_growth")
    if "evidence_fact_ids" in data:
        _verified_evidence_fact_ids(data["evidence_fact_ids"], f"{field}.evidence_fact_ids", facts)


def _validate_sotp_case(value: object, facts: Mapping[str, Mapping], field: str) -> None:
    allowed = {"components", "non_operating_assets", "excess_cash", "debt_like_claims", "evidence_fact_ids"}
    data = _mapping(value, field)
    if "components" not in data or not set(data) <= allowed:
        raise ValuationConsensusError(f"{field} must declare components and supported optional fields")
    components = _list(data["components"], f"{field}.components")
    if not components:
        raise ValuationConsensusError(f"{field}.components must be a non-empty list")
    seen = set()
    value_types = set()
    for index, component in enumerate(components):
        item = _mapping(component, f"{field}.components[{index}]")
        component_id = _non_empty_string(item.get("component_id"), f"{field}.components[{index}].component_id")
        if component_id in seen:
            raise ValuationConsensusError(f"{field}.components contains duplicate component_id")
        seen.add(component_id)
        value_type = _non_empty_string(item.get("value_type"), f"{field}.components[{index}].value_type")
        if value_type not in {"equity", "enterprise"}:
            raise ValuationConsensusError(f"{field}.components[{index}].value_type is not supported")
        value_types.add(value_type)
        direct_keys = {"component_id", "value_type", "value"}
        multiple_keys = {"component_id", "value_type", "denominator", "multiple"}
        if set(item) == direct_keys:
            _decimal(item["value"], f"{field}.components[{index}].value")
        elif set(item) == multiple_keys:
            _positive_decimal(item["denominator"], f"{field}.components[{index}].denominator")
            _positive_decimal(item["multiple"], f"{field}.components[{index}].multiple")
        else:
            raise ValuationConsensusError(f"{field}.components[{index}] must declare one value calculation")
    if len(value_types) != 1:
        raise ValuationConsensusError(f"{field}.components value_type must be uniform across components")
    if "evidence_fact_ids" in data:
        _verified_evidence_fact_ids(data["evidence_fact_ids"], f"{field}.evidence_fact_ids", facts)
    for key in ("non_operating_assets", "excess_cash", "debt_like_claims"):
        if key in data:
            value_decimal = _decimal(data[key], f"{field}.{key}")
            if key == "debt_like_claims" and value_decimal < ZERO:
                raise ValuationConsensusError(f"{field}.{key} must not be negative")


def _positive_decimal(value: object, field: str) -> Decimal:
    amount = _decimal(value, field)
    if amount <= ZERO:
        raise ValuationConsensusError(f"{field} must be positive")
    return amount


def _decimal(value: object, field: str) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise ValuationConsensusError(f"{field} must be a finite decimal string, integer, or Decimal")
    if isinstance(value, Decimal):
        decimal = value
    elif isinstance(value, int):
        decimal = Decimal(value)
    elif isinstance(value, str):
        if not value.strip():
            raise ValuationConsensusError(f"{field} must be a non-empty decimal string")
        try:
            decimal = Decimal(value)
        except (InvalidOperation, ValueError) as exc:
            raise ValuationConsensusError(f"{field} must be a finite decimal") from exc
    else:
        raise ValuationConsensusError(f"{field} must be a finite decimal string, integer, or Decimal")
    if not decimal.is_finite():
        raise ValuationConsensusError(f"{field} must be a finite decimal")
    return decimal


def _is_decimal_value(value: object) -> bool:
    if isinstance(value, (bool, float)) or value is None:
        return False
    if isinstance(value, (Decimal, int)):
        return True
    if isinstance(value, str) and value.strip():
        try:
            return Decimal(value).is_finite()
        except (InvalidOperation, ValueError):
            return False
    return False


def _format_decimal(value: Decimal) -> str:
    quantized = value.quantize(QUANT, rounding=ROUND_HALF_UP)
    if quantized == ZERO:
        quantized = abs(quantized)
    return format(quantized, "f")


def _mapping(value: object, field: str) -> Mapping:
    if not isinstance(value, Mapping):
        raise ValuationConsensusError(f"{field} must be a mapping")
    return value


def _exact_keys(value: object, keys: tuple[str, ...], field: str) -> Mapping:
    mapping = _mapping(value, field)
    missing = [key for key in keys if key not in mapping]
    extra = [key for key in mapping if key not in keys]
    if missing or extra:
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(str(key) for key in extra))
        raise ValuationConsensusError(f"{field} has invalid keys: " + "; ".join(details))
    return mapping


def _list(value: object, field: str) -> list:
    if not isinstance(value, list):
        raise ValuationConsensusError(f"{field} must be a list")
    return value


def _non_empty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValuationConsensusError(f"{field} must be a non-empty string")
    return value


def _unique_string_list(value: object, field: str) -> list[str]:
    items = _list(value, field)
    for index, item in enumerate(items):
        _non_empty_string(item, f"{field}[{index}]")
    if len(set(items)) != len(items):
        raise ValuationConsensusError(f"{field} must not contain duplicates")
    return items


def _currency_code(value: object, field: str) -> str:
    currency = _non_empty_string(value, field)
    if len(currency) != 3 or any(character < "A" or character > "Z" for character in currency):
        raise ValuationConsensusError(f"{field} must be a three-letter uppercase code")
    return currency


def _scan_forbidden_keys(value: object, field: str) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValuationConsensusError(f"{field} keys must be strings")
            normalized = key.lower().replace("_", "-")
            for fragment in FORBIDDEN_KEY_FRAGMENTS:
                if fragment in normalized:
                    raise ValuationConsensusError(f"{field} key {normalized} is forbidden")
            _scan_forbidden_keys(child, f"{field}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_forbidden_keys(child, f"{field}[{index}]")


_T = TypeVar("_T")


def deepcopy_json(value: _T) -> _T:
    return json.loads(json.dumps(value, ensure_ascii=False, allow_nan=False))
