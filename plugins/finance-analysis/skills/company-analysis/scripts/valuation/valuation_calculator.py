"""Deterministic valuation arithmetic for company-analysis reports."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import re
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import evidence_contract as _evidence

CALCULATION_SCHEMA = "company-analysis-valuation-calculation-v1"
ASSUMPTIONS_SCHEMA = "company-analysis-valuation-consensus-assumptions-v2"
CALCULATOR_VERSION = "company-analysis-valuation-calculator-v1"
SUPPORTED_FAMILIES = frozenset({"price-multiple", "yield", "enterprise-multiple", "dcf-fcff", "sotp"})
SENSITIVITY_PARAMETERS = {
    "price-multiple": frozenset({"denominator", "multiple"}),
    "yield": frozenset({"denominator", "yield"}),
    "enterprise-multiple": frozenset({"denominator", "multiple"}),
    "dcf-fcff": frozenset({"wacc", "terminal_growth"}),
    "sotp": frozenset({"component_value", "debt_like_claims"}),
}
SCENARIOS = ("conservative", "neutral", "optimistic")
QUANT = Decimal("0.000001")
ZERO = Decimal("0")
ONE = Decimal("1")
UNIT_STANDARD_VERSION = "company-analysis-valuation-units-v1"


def unit_standard(currency: str) -> dict:
    """Declare valuation units before extracting source values."""
    if not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency):
        raise ValueError("currency must be a three-letter uppercase code")
    return {
        "schema_version": UNIT_STANDARD_VERSION,
        "currency": currency,
        "canonical_units": {
            "current_price": f"{currency}/share",
            "per_share_monetary": f"{currency}/share",
            "aggregate_monetary": currency,
            "diluted_shares": "shares",
            "multiple": "x",
            "rate": "fraction",
        },
        "scale_rule": "金额用基础币种单位、股数用实际股数；带倍率的来源数值须在冻结前换算。",
        "share_basis_rule": "每股金额和摊薄股本须对应同一种所估证券；ADR/CDR 等先核实并换算份额比例。",
    }


def canonical_per_share_unit(unit: str, currency: str) -> str | None:
    """Recognize unscaled monetary per-share labels without changing stored facts."""
    if not isinstance(unit, str) or not isinstance(currency, str):
        return None
    currency = currency.strip().upper()
    if not re.fullmatch(r"[A-Z]{3}", currency):
        return None
    label = re.sub(r"\s*/\s*", "/", unit.strip())
    if label in {"元/股", "人民币元/股", "人民币元/share", "CNY元/股", "CNY元/share"}:
        return "CNY/share" if currency == "CNY" else None
    normalized = re.sub(r"\s+", " ", label).casefold()
    if normalized in {"cny yuan/share", "cny yuan per share"}:
        return "CNY/share" if currency == "CNY" else None
    if normalized == "per share":
        return f"{currency}/share"
    match = re.fullmatch(r"([a-z]{3})\s*/\s*share|([a-z]{3}) per share", normalized)
    if match and (match.group(1) or match.group(2)).upper() == currency:
        return f"{currency}/share"
    return None


def looks_per_share(unit: str) -> bool:
    """Detect per-share dimensions, including labels that need explicit conversion."""
    if not isinstance(unit, str):
        return False
    normalized = re.sub(r"\s+", " ", re.sub(r"\s*/\s*", "/", unit.strip())).casefold()
    return "/股" in normalized or "/share" in normalized or "per share" in normalized


def canonical_share_count_unit(unit: str) -> str | None:
    """Recognize an unscaled count of individual shares."""
    if not isinstance(unit, str):
        return None
    return "shares" if unit.strip().casefold() in {"share", "shares", "股"} else None


def canonical_aggregate_money_unit(unit: str, currency: str) -> str | None:
    """Recognize base-currency amounts; scaled units require explicit conversion."""
    if not isinstance(unit, str) or not isinstance(currency, str):
        return None
    currency = currency.strip().upper()
    if not re.fullmatch(r"[A-Z]{3}", currency):
        return None
    label = re.sub(r"\s+", " ", unit.strip()).casefold()
    aliases = {
        "CNY": {"元", "人民币元", "cny元", "cny yuan"},
        "USD": {"美元", "usd dollar", "usd dollars"},
        "HKD": {"港元", "hkd dollar", "hkd dollars"},
    }
    if label == currency.casefold() or label in aliases.get(currency, set()):
        return currency
    return None


def equivalent_aggregate_money_units(left: str, right: str, currency: str) -> bool:
    """Compare value units without treating different numeric scales as aliases."""
    if left == right:
        return True
    return (
        canonical_aggregate_money_unit(left, currency) == currency
        and canonical_aggregate_money_unit(right, currency) == currency
    )


class ValuationError(ValueError):
    """Raised when valuation inputs or assumptions cannot be calculated safely."""


def canonical_calculation_bytes(result: Mapping) -> bytes:
    """Serialize a calculation in the canonical company-analysis JSON form."""
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    return (text + "\n").encode("utf-8")


def calculate_valuation(valuation_input: Mapping, assumptions: Mapping, baseline: Mapping | None = None) -> dict:
    """Calculate deterministic valuation ranges and primary valuation position."""
    context = _context(valuation_input, assumptions)
    _enforce_primary_requirements(context["methods"][context["primary_method_id"]])
    method_results = [
        _calculate_method(method, context)
        for method in sorted(context["methods"].values(), key=lambda item: item["method_id"])
    ]
    _enforce_contiguous_price_ranges(method_results)
    primary_method = context["methods"][context["primary_method_id"]]
    primary_result = next(item for item in method_results if item["method_id"] == context["primary_method_id"])

    result = {
        "schema_version": CALCULATION_SCHEMA,
        "calculator_version": CALCULATOR_VERSION,
        "valuation_input_hash": context["valuation_input_hash"],
        "fact_snapshot_id": context["fact_snapshot_id"],
        "market_snapshot_id": context["market_snapshot_id"],
        "primary_method_id": context["primary_method_id"],
        "cross_check_method_ids": list(context["cross_check_method_ids"]),
        "methods": method_results,
        "primary": _primary_summary(primary_method, primary_result, context),
        "baseline_diff": [],
    }
    if baseline is not None:
        result["baseline_diff"] = _diff_without_baseline(baseline, result)
    return result


def _context(valuation_input: Mapping, assumptions: Mapping) -> dict:
    valuation_input = _mapping(valuation_input, "valuation input")
    assumptions = _mapping(assumptions, "assumptions")
    for key in (
        "valuation_input_hash", "fact_snapshot_id", "market_snapshot_id",
        "calculator_version", "facts", "market",
    ):
        if key not in valuation_input:
            raise ValuationError(f"valuation input.{key} is required")
    if valuation_input["calculator_version"] != CALCULATOR_VERSION:
        raise ValuationError("valuation input.calculator_version is not supported")
    for key in (
        "schema_version", "calculator_version", "valuation_input_hash",
        "primary_method_id", "cross_check_method_ids", "methods",
    ):
        if key not in assumptions:
            raise ValuationError(f"assumptions.{key} is required")
    if assumptions["schema_version"] != ASSUMPTIONS_SCHEMA:
        raise ValuationError("assumptions.schema_version is not supported")
    if assumptions["calculator_version"] != CALCULATOR_VERSION:
        raise ValuationError("assumptions.calculator_version is not supported")
    if assumptions["valuation_input_hash"] != valuation_input["valuation_input_hash"]:
        raise ValuationError("assumptions.valuation_input_hash must match valuation input")

    facts = _validate_fact_records(valuation_input["facts"], "valuation input.facts")
    current_price = _current_price(valuation_input["market"])
    valuation_currency = (
        _non_empty_string(valuation_input["market"].get("valuation_currency"), "market.valuation_currency")
        if "valuation_currency" in valuation_input["market"]
        else (current_price["currency"] if current_price is not None else None)
    )
    if valuation_currency is None:
        raise ValuationError("market needs current_price or valuation_currency")
    if current_price is not None and current_price["currency"] != valuation_currency:
        raise ValuationError("market.current_price.currency must match valuation_currency")
    methods = _methods_by_id(assumptions["methods"])
    primary_method_id = _non_empty_string(assumptions["primary_method_id"], "assumptions.primary_method_id")
    if primary_method_id not in methods:
        raise ValuationError("assumptions.primary_method_id must identify a valuation method")
    cross_check_method_ids = _string_list(assumptions["cross_check_method_ids"], "assumptions.cross_check_method_ids")
    unknown_cross_checks = [method_id for method_id in cross_check_method_ids if method_id not in methods]
    if unknown_cross_checks:
        raise ValuationError("assumptions.cross_check_method_ids must identify valuation methods")

    return {
        "valuation_input_hash": valuation_input["valuation_input_hash"],
        "fact_snapshot_id": valuation_input["fact_snapshot_id"],
        "market_snapshot_id": valuation_input["market_snapshot_id"],
        "facts": facts,
        "market": valuation_input["market"],
        "current_price": current_price,
        "valuation_currency": valuation_currency,
        "methods": methods,
        "primary_method_id": primary_method_id,
        "cross_check_method_ids": cross_check_method_ids,
    }


def _validate_fact_records(facts: object, field: str) -> Mapping[str, Mapping]:
    try:
        return _evidence.validate_fact_records(facts, field=field)
    except _evidence.EvidenceError as exc:
        raise ValuationError(str(exc)) from exc


def _methods_by_id(methods: object) -> dict[str, Mapping]:
    if not isinstance(methods, list) or not methods:
        raise ValuationError("assumptions.methods must be a non-empty list")
    by_id: dict[str, Mapping] = {}
    for index, method in enumerate(methods):
        item = _mapping(method, f"assumptions.methods[{index}]")
        method_id = _non_empty_string(item.get("method_id"), f"assumptions.methods[{index}].method_id")
        if method_id in by_id:
            raise ValuationError("assumptions.methods contains duplicate method_id")
        family = _non_empty_string(item.get("family"), f"assumptions.methods[{index}].family")
        if family not in SUPPORTED_FAMILIES:
            raise ValuationError(f"assumptions.methods[{index}].family is not supported")
        _scenarios(item)
        by_id[method_id] = item
    return by_id


def _calculate_method(method: Mapping, context: Mapping) -> dict:
    family = method["family"]
    if family == "price-multiple":
        result = _calculate_price_multiple(method, context)
    elif family == "yield":
        result = _calculate_yield(method, context)
    elif family == "enterprise-multiple":
        result = _calculate_enterprise_multiple(method, context)
    elif family == "dcf-fcff":
        result = _calculate_dcf(method, context)
    elif family == "sotp":
        result = _calculate_sotp(method, context)
    else:
        raise ValuationError("method.family is not supported")
    if "sensitivity" in method:
        result["sensitivity"] = _sensitivity(method, context)
    current_indicator = _current_indicator(method, context)
    if current_indicator is not None:
        result["current_indicator"] = _format_decimal(current_indicator)
    else:
        result["current_indicator"] = None
    return result


def _calculate_price_multiple(method: Mapping, context: Mapping) -> dict:
    denominator_fact = _per_share_denominator(method, context)
    scenarios = []
    for name, scenario in _scenarios(method):
        denominator = _scenario_decimal(scenario, "denominator", denominator_fact["value"], f"{method['method_id']}.{name}.denominator")
        _positive(denominator, "denominator")
        lower, upper = _range(scenario, f"{method['method_id']}.{name}.range", "multiple")
        prices = (denominator * lower, denominator * upper)
        scenarios.append(_scenario_output(name, lower, upper, min(prices), max(prices), {"denominator": denominator}))
    return _method_output(method, scenarios)


def _calculate_yield(method: Mapping, context: Mapping) -> dict:
    denominator_fact = _per_share_denominator(method, context)
    scenarios = []
    for name, scenario in _scenarios(method):
        denominator = _scenario_decimal(scenario, "denominator", denominator_fact["value"], f"{method['method_id']}.{name}.denominator")
        _positive(denominator, "denominator")
        lower, upper = _range(scenario, f"{method['method_id']}.{name}.range", "yield")
        prices = (denominator / lower, denominator / upper)
        scenarios.append(_scenario_output(name, lower, upper, min(prices), max(prices), {"denominator": denominator}))
    return _method_output(method, scenarios)


def _calculate_enterprise_multiple(method: Mapping, context: Mapping) -> dict:
    denominator_fact = _monetary_denominator(method, context)
    shares = _diluted_shares(method, context)
    bridge = _bridge_values(method, context)
    scenarios = []
    for name, scenario in _scenarios(method):
        denominator = _scenario_decimal(scenario, "denominator", denominator_fact["value"], f"{method['method_id']}.{name}.denominator")
        _positive(denominator, "denominator")
        lower, upper = _range(scenario, f"{method['method_id']}.{name}.range", "multiple")
        lower_price = _enterprise_price(denominator * lower, bridge, shares)
        upper_price = _enterprise_price(denominator * upper, bridge, shares)
        scenarios.append(_scenario_output(name, lower, upper, min(lower_price, upper_price), max(lower_price, upper_price), {
            "denominator": denominator,
        }))
    return _method_output(method, scenarios)


def _calculate_dcf(method: Mapping, context: Mapping) -> dict:
    shares = _diluted_shares(method, context)
    bridge = _bridge_values(method, context)
    scenarios = []
    for name, scenario in _scenarios(method):
        field = f"{method['method_id']}.{name}"
        if "range" not in scenario:
            raise ValuationError(f"{field} must declare an explicit range case")
        lower_case, upper_case = _case_range(scenario, f"{field}.range")
        lower_price = _dcf_price(lower_case, bridge, shares, f"{field}.range.lower")
        upper_price = _dcf_price(upper_case, bridge, shares, f"{field}.range.upper")
        scenarios.append(_scenario_output(name, min(lower_price, upper_price), max(lower_price, upper_price), min(lower_price, upper_price), max(lower_price, upper_price), {}))
    return _method_output(method, scenarios)


def _calculate_sotp(method: Mapping, context: Mapping) -> dict:
    shares = _diluted_shares(method, context)
    scenarios = []
    for name, scenario in _scenarios(method):
        field = f"{method['method_id']}.{name}"
        if "range" not in scenario:
            raise ValuationError(f"{field} must declare an explicit range case")
        lower_case, upper_case = _case_range(scenario, f"{field}.range")
        lower_price = _sotp_price(lower_case, shares, f"{field}.range.lower")
        upper_price = _sotp_price(upper_case, shares, f"{field}.range.upper")
        scenarios.append(_scenario_output(name, min(lower_price, upper_price), max(lower_price, upper_price), min(lower_price, upper_price), max(lower_price, upper_price), {}))
    return _method_output(method, scenarios)


def _method_output(method: Mapping, scenarios: Sequence[dict]) -> dict:
    return {
        "method_id": method["method_id"],
        "family": method["family"],
        "direction": method.get("direction"),
        "scenarios": list(scenarios),
    }


def _enforce_contiguous_price_ranges(method_results: Sequence[Mapping]) -> None:
    """Every method's three scenario price ranges must form one contiguous interval."""
    for result in method_results:
        method_id = result["method_id"]
        by_scenario = {item["scenario"]: item for item in result["scenarios"]}
        if set(by_scenario) != set(SCENARIOS):
            raise ValuationError(f"{method_id} scenarios must include conservative, neutral, and optimistic")
        prices = {
            name: (
                _parse_decimal(by_scenario[name]["price_range"]["lower"], f"{method_id}.{name}.price_range.lower"),
                _parse_decimal(by_scenario[name]["price_range"]["upper"], f"{method_id}.{name}.price_range.upper"),
            )
            for name in SCENARIOS
        }
        if prices["conservative"][1] != prices["neutral"][0] or prices["neutral"][1] != prices["optimistic"][0]:
            raise ValuationError(
                f"{method_id} scenario price ranges must be contiguous: conservative upper "
                f"{prices['conservative'][1]}, neutral {prices['neutral'][0]}..{prices['neutral'][1]}, "
                f"optimistic lower {prices['optimistic'][0]}; adjust scenario parameters until they meet"
            )
        ordered = (
            prices["conservative"][0], prices["conservative"][1],
            prices["neutral"][1], prices["optimistic"][1],
        )
        if not all(left < right for left, right in zip(ordered, ordered[1:])):
            raise ValuationError(f"{method_id} scenario price ranges must be strictly increasing")


def _scenario_output(
    name: str,
    indicator_lower: Decimal,
    indicator_upper: Decimal,
    price_lower: Decimal,
    price_upper: Decimal,
    inputs: Mapping[str, Decimal],
) -> dict:
    output = {
        "scenario": name,
        "indicator_range": {
            "lower": _format_decimal(indicator_lower),
            "upper": _format_decimal(indicator_upper),
        },
        "price_range": {
            "lower": _format_decimal(price_lower),
            "upper": _format_decimal(price_upper),
        },
    }
    if inputs:
        output["inputs"] = {key: _format_decimal(value) for key, value in sorted(inputs.items())}
    return output


def _primary_summary(method: Mapping, method_result: Mapping, context: Mapping) -> dict:
    thresholds = _primary_thresholds(method, method_result)
    current_indicator = _current_indicator(method, context)
    labels = _band_labels(method["family"])
    bands = _bands(thresholds, labels)
    current = context["current_price"]
    current_price = None if current is None else current["value"]
    boundary_prices = _primary_boundary_prices(method, method_result, context)
    conservative_space = None if current_price is None else boundary_prices["conservative_lower"] / current_price - ONE
    optimistic_space = None if current_price is None else boundary_prices["optimistic_lower"] / current_price - ONE
    display_min, display_max = _display_bounds(thresholds)
    return {
        "method_id": method["method_id"],
        "current_indicator": None if current_indicator is None else _format_decimal(current_indicator),
        "current_price": None if current_price is None else _format_decimal(current_price),
        "current_price_date": None if current is None else current["date"],
        "thresholds": [_format_decimal(value) for value in thresholds],
        "display_min": _format_decimal(display_min),
        "display_max": _format_decimal(display_max),
        "bands": bands,
        "current_position": None if current_indicator is None else _classify(current_indicator, thresholds, labels),
        "boundary_prices": {
            "conservative_lower": _format_decimal(boundary_prices["conservative_lower"]),
            "optimistic_lower": _format_decimal(boundary_prices["optimistic_lower"]),
        },
        "spaces": {
            "conservative": None if conservative_space is None else _format_decimal(conservative_space),
            "optimistic": None if optimistic_space is None else _format_decimal(optimistic_space),
        },
    }


def _enforce_primary_requirements(method: Mapping) -> None:
    if "sensitivity" not in method:
        raise ValuationError("primary method sensitivity must be a valid 3x3 grid")
    if method["family"] in {"dcf-fcff", "sotp"}:
        sensitivity = _mapping(method["sensitivity"], f"{method['method_id']}.sensitivity")
        if "base_case" not in sensitivity:
            raise ValuationError(f"primary {method['family']} sensitivity.base_case is required")
        _validate_model_case(method["family"], sensitivity["base_case"], f"{method['method_id']}.sensitivity.base_case")
        for name, scenario in _scenarios(method):
            if "range" not in scenario:
                raise ValuationError(f"primary {method['family']} scenarios must declare explicit range cases")
            _case_range(scenario, f"{method['method_id']}.{name}.range")


def _primary_thresholds(method: Mapping, method_result: Mapping) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    by_scenario = {item["scenario"]: item for item in method_result["scenarios"]}
    if set(by_scenario) != set(SCENARIOS):
        raise ValuationError("primary method scenarios must include conservative, neutral, and optimistic")

    ranges = {
        name: (
            _parse_decimal(by_scenario[name]["indicator_range"]["lower"], f"{method['method_id']}.{name}.indicator_range.lower"),
            _parse_decimal(by_scenario[name]["indicator_range"]["upper"], f"{method['method_id']}.{name}.indicator_range.upper"),
        )
        for name in SCENARIOS
    }
    if method["family"] == "yield":
        b0, b1 = ranges["optimistic"]
        neutral_lower, b2 = ranges["neutral"]
        conservative_lower, b3 = ranges["conservative"]
        if b1 != neutral_lower or b2 != conservative_lower:
            raise ValuationError("yield primary scenarios must share numeric boundaries")
    else:
        b0, b1 = ranges["conservative"]
        neutral_lower, b2 = ranges["neutral"]
        optimistic_lower, b3 = ranges["optimistic"]
        if b1 != neutral_lower or b2 != optimistic_lower:
            raise ValuationError("primary scenarios must share numeric boundaries")
    thresholds = (b0, b1, b2, b3)
    if not all(left < right for left, right in zip(thresholds, thresholds[1:])):
        raise ValuationError("primary thresholds must be strictly increasing")
    return thresholds


def _primary_boundary_prices(method: Mapping, method_result: Mapping, context: Mapping) -> dict[str, Decimal]:
    by_scenario = {item["scenario"]: item for item in method_result["scenarios"]}
    if method["family"] == "price-multiple":
        conservative = _price_multiple_boundary(method, "conservative", context)
        optimistic = _price_multiple_boundary(method, "optimistic", context)
    elif method["family"] == "yield":
        conservative = _yield_boundary(method, "conservative", context)
        optimistic = _yield_boundary(method, "optimistic", context)
    elif method["family"] == "enterprise-multiple":
        conservative = _enterprise_boundary(method, "conservative", context)
        optimistic = _enterprise_boundary(method, "optimistic", context)
    else:
        conservative = _parse_decimal(
            by_scenario["conservative"]["price_range"]["lower"],
            f"{method['method_id']}.conservative.price_range.lower",
        )
        optimistic = _parse_decimal(
            by_scenario["optimistic"]["price_range"]["lower"],
            f"{method['method_id']}.optimistic.price_range.lower",
        )
    return {"conservative_lower": conservative, "optimistic_lower": optimistic}


def _price_multiple_boundary(method: Mapping, scenario_name: str, context: Mapping) -> Decimal:
    denominator_fact = _per_share_denominator(method, context)
    scenario = _scenario_by_name(method, scenario_name)
    denominator = _scenario_decimal(scenario, "denominator", denominator_fact["value"], f"{method['method_id']}.{scenario_name}.denominator")
    lower, _ = _range(scenario, f"{method['method_id']}.{scenario_name}.range", "multiple")
    return denominator * lower


def _yield_boundary(method: Mapping, scenario_name: str, context: Mapping) -> Decimal:
    denominator_fact = _per_share_denominator(method, context)
    scenario = _scenario_by_name(method, scenario_name)
    denominator = _scenario_decimal(scenario, "denominator", denominator_fact["value"], f"{method['method_id']}.{scenario_name}.denominator")
    _, upper = _range(scenario, f"{method['method_id']}.{scenario_name}.range", "yield")
    return denominator / upper


def _enterprise_boundary(method: Mapping, scenario_name: str, context: Mapping) -> Decimal:
    denominator_fact = _monetary_denominator(method, context)
    shares = _diluted_shares(method, context)
    bridge = _bridge_values(method, context)
    scenario = _scenario_by_name(method, scenario_name)
    denominator = _scenario_decimal(scenario, "denominator", denominator_fact["value"], f"{method['method_id']}.{scenario_name}.denominator")
    lower, _ = _range(scenario, f"{method['method_id']}.{scenario_name}.range", "multiple")
    return _enterprise_price(denominator * lower, bridge, shares)


def _band_labels(family: str) -> tuple[str, str, str, str, str]:
    if family == "yield":
        return (
            "clear-overvaluation",
            "optimistic-valuation",
            "neutral-valuation",
            "conservative-valuation",
            "clear-undervaluation",
        )
    return (
        "clear-undervaluation",
        "conservative-valuation",
        "neutral-valuation",
        "optimistic-valuation",
        "clear-overvaluation",
    )


def _bands(thresholds: Sequence[Decimal], labels: Sequence[str]) -> list[dict]:
    b0, b1, b2, b3 = thresholds
    return [
        {"position": labels[0], "lower": None, "upper": _format_decimal(b0), "lower_inclusive": False, "upper_inclusive": False},
        {"position": labels[1], "lower": _format_decimal(b0), "upper": _format_decimal(b1), "lower_inclusive": True, "upper_inclusive": False},
        {"position": labels[2], "lower": _format_decimal(b1), "upper": _format_decimal(b2), "lower_inclusive": True, "upper_inclusive": False},
        {"position": labels[3], "lower": _format_decimal(b2), "upper": _format_decimal(b3), "lower_inclusive": True, "upper_inclusive": True},
        {"position": labels[4], "lower": _format_decimal(b3), "upper": None, "lower_inclusive": False, "upper_inclusive": False},
    ]


def _classify(value: Decimal, thresholds: Sequence[Decimal], labels: Sequence[str]) -> str:
    b0, b1, b2, b3 = thresholds
    if value < b0:
        return labels[0]
    if value < b1:
        return labels[1]
    if value < b2:
        return labels[2]
    if value <= b3:
        return labels[3]
    return labels[4]


def _display_bounds(thresholds: Sequence[Decimal]) -> tuple[Decimal, Decimal]:
    first_gap = thresholds[1] - thresholds[0]
    last_gap = thresholds[-1] - thresholds[-2]
    display_min = thresholds[0] - first_gap
    if thresholds[0] > ZERO:
        # 0 clamp only makes sense on a positive scale; negative thresholds stay.
        if display_min < ZERO:
            display_min = ZERO
        if display_min == thresholds[0]:
            display_min = thresholds[0] / Decimal("2")
    display_max = thresholds[-1] + last_gap
    return display_min, display_max


def _neutral_scenario_decimal(method: Mapping, key: str, default: Decimal) -> Decimal:
    scenario = _scenario_by_name(method, "neutral")
    return _scenario_decimal(scenario, key, default, f"{method['method_id']}.neutral.{key}")


def _current_indicator(method: Mapping, context: Mapping) -> Decimal | None:
    if context["current_price"] is None:
        return None
    family = method["family"]
    if family == "price-multiple":
        denominator = _neutral_scenario_decimal(method, "denominator", _per_share_denominator(method, context)["value"])
        return context["current_price"]["value"] / denominator
    if family == "yield":
        denominator = _neutral_scenario_decimal(method, "denominator", _per_share_denominator(method, context)["value"])
        return denominator / context["current_price"]["value"]
    if family == "enterprise-multiple":
        denominator = _monetary_denominator(method, context)
        denominator_value = _neutral_scenario_decimal(method, "denominator", denominator["value"])
        current_ev = _market_value(context["market"], "current_enterprise_value", required=False)
        if current_ev is None:
            # The method's frozen share count and bridge already define the
            # inverse of its per-share enterprise valuation formula.
            if canonical_aggregate_money_unit(denominator["unit"], denominator["currency"]) is None:
                return None
            bridge_fact_ids = method.get("bridge_fact_ids", {})
            for fact_id in bridge_fact_ids.values():
                bridge_fact = _monetary_fact(context, fact_id, f"{method['method_id']}.bridge_fact_ids")
                if canonical_aggregate_money_unit(bridge_fact["unit"], bridge_fact["currency"]) is None:
                    return None
            bridge = _bridge_values(method, context)
            shares = _diluted_shares(method, context)
            implied_ev = context["current_price"]["value"] * shares
            implied_ev += sum(bridge[key] for key in ("debt", "lease_liabilities", "minority_interest", "preferred_claims"))
            implied_ev -= bridge["excess_cash"]
            return implied_ev / denominator_value
        _reject_per_share_aggregate_unit(current_ev["unit"], "valuation input.market.current_enterprise_value")
        if current_ev["currency"] != denominator["currency"]:
            raise ValuationError("valuation input.market.current_enterprise_value.currency must match denominator currency")
        if not equivalent_aggregate_money_units(current_ev["unit"], denominator["unit"], denominator["currency"]):
            raise ValuationError("valuation input.market.current_enterprise_value.unit must match denominator aggregate monetary unit")
        return current_ev["value"] / denominator_value
    if family in {"dcf-fcff", "sotp"}:
        return context["current_price"]["value"]
    raise ValuationError("method.family is not supported")


def _sensitivity(method: Mapping, context: Mapping) -> dict:
    data = _mapping(method["sensitivity"], f"{method['method_id']}.sensitivity")
    row_parameter = _non_empty_string(data.get("row_parameter"), f"{method['method_id']}.sensitivity.row_parameter")
    column_parameter = _non_empty_string(data.get("column_parameter"), f"{method['method_id']}.sensitivity.column_parameter")
    _validate_sensitivity_parameters(method["family"], row_parameter, column_parameter)
    base_case = _sensitivity_base_case(method, data)
    row_values = [_parse_decimal(value, f"{method['method_id']}.sensitivity.row_values[{index}]") for index, value in enumerate(_list(data.get("row_values"), f"{method['method_id']}.sensitivity.row_values"))]
    column_values = [_parse_decimal(value, f"{method['method_id']}.sensitivity.column_values[{index}]") for index, value in enumerate(_list(data.get("column_values"), f"{method['method_id']}.sensitivity.column_values"))]
    if len(row_values) != 3 or len(column_values) != 3:
        raise ValuationError("sensitivity must be a literal 3x3 grid")
    prices = [
        [_sensitivity_price(method, context, row_parameter, row_value, column_parameter, column_value, base_case) for column_value in column_values]
        for row_value in row_values
    ]
    return {
        "row_parameter": row_parameter,
        "row_values": [_format_decimal(value) for value in row_values],
        "column_parameter": column_parameter,
        "column_values": [_format_decimal(value) for value in column_values],
        "prices": [[_format_decimal(value) for value in row] for row in prices],
    }


def _validate_sensitivity_parameters(family: str, row_parameter: str, column_parameter: str) -> None:
    if row_parameter == column_parameter:
        raise ValuationError("sensitivity row and column parameters must be different")
    expected = SENSITIVITY_PARAMETERS[family]
    if {row_parameter, column_parameter} != expected:
        joined = ", ".join(sorted(expected))
        raise ValuationError(f"{family} sensitivity parameters must be exactly {joined}")


def _sensitivity_base_case(method: Mapping, data: Mapping) -> Mapping | None:
    family = method["family"]
    if family not in {"dcf-fcff", "sotp"}:
        return None
    if "base_case" not in data:
        raise ValuationError(f"{method['method_id']}.sensitivity.base_case is required for {family}")
    base_case = _mapping(data["base_case"], f"{method['method_id']}.sensitivity.base_case")
    _validate_model_case(family, base_case, f"{method['method_id']}.sensitivity.base_case")
    return base_case


def _validate_model_case(family: str, value: object, field: str) -> Mapping:
    data = _mapping(value, field)
    if family == "dcf-fcff":
        fcff_values = _list(data.get("fcff"), f"{field}.fcff")
        if not fcff_values:
            raise ValuationError(f"{field}.fcff must be a non-empty list")
        for index, cash_flow in enumerate(fcff_values):
            _parse_decimal(cash_flow, f"{field}.fcff[{index}]")
        wacc = _parse_decimal(data.get("wacc"), f"{field}.wacc")
        terminal_growth = _parse_decimal(data.get("terminal_growth"), f"{field}.terminal_growth")
        if wacc <= ZERO:
            raise ValuationError(f"{field}.wacc must be positive")
        if terminal_growth <= -ONE:
            raise ValuationError(f"{field}.terminal_growth must be greater than -1")
        if wacc <= terminal_growth:
            raise ValuationError(f"{field}.wacc must exceed terminal_growth")
    elif family == "sotp":
        components = _list(data.get("components"), f"{field}.components")
        if not components:
            raise ValuationError(f"{field}.components must be a non-empty list")
    return data


def _sensitivity_price(
    method: Mapping,
    context: Mapping,
    row_parameter: str,
    row_value: Decimal,
    column_parameter: str,
    column_value: Decimal,
    base_case: Mapping | None,
) -> Decimal:
    family = method["family"]
    if family == "price-multiple":
        values = {row_parameter: row_value, column_parameter: column_value}
        denominator = values.get("denominator")
        multiple = values.get("multiple")
        if denominator is None or multiple is None:
            raise ValuationError("price-multiple sensitivity requires denominator and multiple")
        _positive(denominator, "denominator")
        _positive(multiple, "multiple")
        return denominator * multiple
    if family == "yield":
        values = {row_parameter: row_value, column_parameter: column_value}
        denominator = values.get("denominator")
        yield_rate = values.get("yield")
        if denominator is None or yield_rate is None:
            raise ValuationError("yield sensitivity requires denominator and yield")
        _positive(denominator, "denominator")
        _positive(yield_rate, "yield")
        return denominator / yield_rate
    if family == "enterprise-multiple":
        values = {row_parameter: row_value, column_parameter: column_value}
        denominator = values.get("denominator")
        multiple = values.get("multiple")
        if denominator is None or multiple is None:
            raise ValuationError("enterprise-multiple sensitivity requires denominator and multiple")
        _positive(denominator, "denominator")
        _positive(multiple, "multiple")
        return _enterprise_price(denominator * multiple, _bridge_values(method, context), _diluted_shares(method, context))
    if family == "dcf-fcff":
        values = {row_parameter: row_value, column_parameter: column_value}
        assert base_case is not None
        adjusted = dict(base_case)
        if "wacc" in values:
            adjusted["wacc"] = values["wacc"]
        if "terminal_growth" in values:
            adjusted["terminal_growth"] = values["terminal_growth"]
        return _dcf_price(adjusted, _bridge_values(method, context), _diluted_shares(method, context), f"{method['method_id']}.sensitivity")
    if family == "sotp":
        values = {row_parameter: row_value, column_parameter: column_value}
        component_value = values.get("component_value")
        debt_like_claims = values.get("debt_like_claims")
        if component_value is None or debt_like_claims is None:
            raise ValuationError("sotp sensitivity requires component_value and debt_like_claims")
        _positive(component_value, "component value")
        if debt_like_claims < ZERO:
            raise ValuationError("debt_like_claims must not be negative")
        assert base_case is not None
        adjusted = dict(base_case)
        base_value_type = _list(
            base_case.get("components"), f"{method['method_id']}.sensitivity.base_case.components"
        )[0].get("value_type")
        adjusted["components"] = [
            {
                "component_id": "sensitivity-component-value",
                "value_type": base_value_type,
                "value": component_value,
            },
        ]
        adjusted["debt_like_claims"] = debt_like_claims
        return _sotp_price(adjusted, _diluted_shares(method, context), f"{method['method_id']}.sensitivity")
    raise ValuationError(f"{family} sensitivity is not supported")


def _enterprise_price(enterprise_value: Decimal, bridge: Mapping[str, Decimal], shares: Decimal) -> Decimal:
    equity_value = (
        enterprise_value
        - bridge["debt"]
        - bridge["lease_liabilities"]
        - bridge["minority_interest"]
        - bridge["preferred_claims"]
        + bridge["excess_cash"]
    )
    return equity_value / shares


def _dcf_price(scenario: Mapping, bridge: Mapping[str, Decimal], shares: Decimal, field: str) -> Decimal:
    data = _mapping(scenario, field)
    fcff_values = _list(data.get("fcff"), f"{field}.fcff")
    if not fcff_values:
        raise ValuationError(f"{field}.fcff must be a non-empty list")
    fcff = [_parse_decimal(value, f"{field}.fcff[{index}]") for index, value in enumerate(fcff_values)]
    wacc = _parse_decimal(data.get("wacc"), f"{field}.wacc")
    terminal_growth = _parse_decimal(data.get("terminal_growth"), f"{field}.terminal_growth")
    if wacc <= ZERO:
        raise ValuationError("wacc must be positive")
    if terminal_growth <= -ONE:
        raise ValuationError("terminal_growth must be greater than -1")
    if wacc <= terminal_growth:
        raise ValuationError("wacc must exceed terminal_growth")
    explicit_value = sum(
        cash_flow / ((ONE + wacc) ** Decimal(index))
        for index, cash_flow in enumerate(fcff, start=1)
    )
    terminal_value = fcff[-1] * (ONE + terminal_growth) / (wacc - terminal_growth)
    discounted_terminal = terminal_value / ((ONE + wacc) ** Decimal(len(fcff)))
    enterprise_value = explicit_value + discounted_terminal
    return _enterprise_price(enterprise_value, bridge, shares)


def _sotp_price(scenario: Mapping, shares: Decimal, field: str) -> Decimal:
    data = _mapping(scenario, field)
    components = _list(data.get("components"), f"{field}.components")
    if not components:
        raise ValuationError(f"{field}.components must be a non-empty list")
    total = ZERO
    seen_components = set()
    value_types = set()
    for index, component in enumerate(components):
        component_field = f"{field}.components[{index}]"
        item = _mapping(component, component_field)
        component_id = _non_empty_string(item.get("component_id"), f"{component_field}.component_id")
        if component_id in seen_components:
            raise ValuationError(f"{field}.components contains duplicate component_id")
        seen_components.add(component_id)
        value_type = _non_empty_string(item.get("value_type"), f"{component_field}.value_type")
        if value_type not in {"equity", "enterprise"}:
            raise ValuationError(f"{component_field}.value_type is not supported")
        value_types.add(value_type)
        has_direct_value = "value" in item
        has_multiple_value = "denominator" in item or "multiple" in item
        if has_direct_value == has_multiple_value:
            raise ValuationError(f"{component_field} must declare exactly one value calculation")
        if has_direct_value:
            value = _parse_decimal(item["value"], f"{component_field}.value")
        else:
            denominator = _parse_decimal(item.get("denominator"), f"{component_field}.denominator")
            multiple = _parse_decimal(item.get("multiple"), f"{component_field}.multiple")
            _positive(denominator, "denominator")
            _positive(multiple, "multiple")
            value = denominator * multiple
        total += value
    if len(value_types) != 1:
        raise ValuationError(f"{field}.components value_type must be uniform across components")
    total += _optional_decimal(data, "non_operating_assets", f"{field}.non_operating_assets")
    total += _optional_decimal(data, "excess_cash", f"{field}.excess_cash")
    total -= _optional_decimal(data, "debt_like_claims", f"{field}.debt_like_claims")
    return total / shares


def _bridge_values(method: Mapping, context: Mapping) -> dict[str, Decimal]:
    bridge_fact_ids = _mapping(method.get("bridge_fact_ids", {}), f"{method['method_id']}.bridge_fact_ids")
    values = {
        "debt": ZERO,
        "lease_liabilities": ZERO,
        "minority_interest": ZERO,
        "preferred_claims": ZERO,
        "excess_cash": ZERO,
    }
    for key in tuple(values):
        fact_id = bridge_fact_ids.get(key)
        if fact_id is None:
            continue
        values[key] = _aggregate_monetary_fact(
            context,
            _non_empty_string(fact_id, f"{method['method_id']}.bridge_fact_ids.{key}"),
            f"{method['method_id']}.bridge_fact_ids.{key}",
        )["value"]
    return values


def _per_share_denominator(method: Mapping, context: Mapping) -> dict:
    fact_id = _non_empty_string(method.get("denominator_fact_id"), f"{method['method_id']}.denominator_fact_id")
    fact = _monetary_fact(context, fact_id, f"{method['method_id']}.denominator_fact_id")
    _positive(fact["value"], "denominator")
    if canonical_per_share_unit(fact["unit"], fact["currency"]) is None:
        raise ValuationError("denominator fact unit must be per-share")
    return fact


def _monetary_denominator(method: Mapping, context: Mapping) -> dict:
    fact_id = _non_empty_string(method.get("denominator_fact_id"), f"{method['method_id']}.denominator_fact_id")
    fact = _aggregate_monetary_fact(context, fact_id, f"{method['method_id']}.denominator_fact_id")
    _positive(fact["value"], "denominator")
    return fact


def _aggregate_monetary_fact(context: Mapping, fact_id: str, field: str) -> dict:
    fact = _monetary_fact(context, fact_id, field)
    _reject_per_share_aggregate_unit(fact["unit"], field)
    if canonical_aggregate_money_unit(fact["unit"], fact["currency"]) is None:
        raise ValuationError(f"{field}.unit must be an unscaled {fact['currency']} amount")
    return fact


def _reject_per_share_aggregate_unit(unit: str, field: str) -> None:
    if looks_per_share(unit):
        raise ValuationError(f"{field}.unit must be aggregate monetary, not per-share")


def _monetary_fact(context: Mapping, fact_id: str, field: str) -> dict:
    fact = _fact(context, fact_id, field)
    currency = _non_empty_string(fact.get("currency"), f"{field}.currency")
    if currency != context["valuation_currency"]:
        raise ValuationError(f"{field}.currency must match valuation currency")
    return {
        "value": _parse_decimal(fact.get("value"), f"{field}.value"),
        "currency": currency,
        "unit": _non_empty_string(fact.get("unit"), f"{field}.unit"),
        "period": _non_empty_string(fact.get("period"), f"{field}.date"),
    }


def _diluted_shares(method: Mapping, context: Mapping) -> Decimal:
    fact_id = _non_empty_string(method.get("diluted_shares_fact_id"), f"{method['method_id']}.diluted_shares_fact_id")
    fact = _fact(context, fact_id, f"{method['method_id']}.diluted_shares_fact_id")
    unit = _non_empty_string(fact.get("unit"), f"{method['method_id']}.diluted_shares_fact_id.unit")
    if canonical_share_count_unit(unit) is None:
        raise ValuationError("diluted shares fact unit must be shares")
    _non_empty_string(fact.get("period"), f"{method['method_id']}.diluted_shares_fact_id.date")
    shares = _parse_decimal(fact.get("value"), f"{method['method_id']}.diluted_shares_fact_id.value")
    if shares <= ZERO:
        raise ValuationError("diluted shares must be positive")
    return shares


def _fact(context: Mapping, fact_id: str, field: str) -> Mapping:
    try:
        return context["facts"][fact_id]
    except KeyError as exc:
        raise ValuationError(f"{field} must reference a fact in valuation input") from exc


def _current_price(market: object) -> dict | None:
    current_price = _market_value(market, "current_price", required=False)
    if current_price is None:
        return None
    if canonical_per_share_unit(current_price["unit"], current_price["currency"]) is None:
        raise ValuationError("market.current_price.unit must be per-share")
    _positive(current_price["value"], "current price")
    return current_price


def _market_value(market: object, key: str, *, required: bool) -> dict | None:
    market_data = _mapping(market, "valuation input.market")
    if key not in market_data:
        if required:
            raise ValuationError(f"valuation input.market.{key} is required")
        return None
    value = _mapping(market_data[key], f"valuation input.market.{key}")
    return {
        "value": _parse_decimal(value.get("value"), f"valuation input.market.{key}.value"),
        "currency": _non_empty_string(value.get("currency"), f"valuation input.market.{key}.currency"),
        "unit": _non_empty_string(value.get("unit"), f"valuation input.market.{key}.unit"),
        "date": _non_empty_string(value.get("date"), f"valuation input.market.{key}.date"),
    }


def _scenarios(method: Mapping) -> list[tuple[str, Mapping]]:
    scenarios = _mapping(method.get("scenarios"), f"{method.get('method_id', 'method')}.scenarios")
    missing = [name for name in SCENARIOS if name not in scenarios]
    if missing:
        raise ValuationError("method.scenarios must include conservative, neutral, and optimistic")
    return [(name, _mapping(scenarios[name], f"{method.get('method_id', 'method')}.scenarios.{name}")) for name in SCENARIOS]


def _scenario_by_name(method: Mapping, scenario_name: str) -> Mapping:
    return _mapping(method["scenarios"][scenario_name], f"{method['method_id']}.scenarios.{scenario_name}")


def _case_range(scenario: Mapping, field: str) -> tuple[Mapping, Mapping]:
    data = _mapping(scenario.get("range"), field)
    lower = _mapping(data.get("lower"), f"{field}.lower")
    upper = _mapping(data.get("upper"), f"{field}.upper")
    return lower, upper


def _scenario_decimal(scenario: Mapping, key: str, default: Decimal, field: str) -> Decimal:
    if key not in scenario:
        return default
    return _parse_decimal(scenario[key], field)


def _range(scenario: Mapping, field: str, label: str) -> tuple[Decimal, Decimal]:
    data = _mapping(scenario.get("range"), field)
    lower = _parse_decimal(data.get("lower"), f"{field}.lower")
    upper = _parse_decimal(data.get("upper"), f"{field}.upper")
    _positive(lower, label)
    _positive(upper, label)
    if upper < lower:
        raise ValuationError(f"{label} range upper must be greater than or equal to lower")
    return lower, upper


def _optional_decimal(data: Mapping, key: str, field: str) -> Decimal:
    if key not in data:
        return ZERO
    return _parse_decimal(data[key], field)


def _mapping(value: object, field: str) -> Mapping:
    if not isinstance(value, Mapping):
        raise ValuationError(f"{field} must be a mapping")
    return value


def _list(value: object, field: str) -> list:
    if not isinstance(value, list):
        raise ValuationError(f"{field} must be a list")
    return value


def _string_list(value: object, field: str) -> list:
    items = _list(value, field)
    for index, item in enumerate(items):
        _non_empty_string(item, f"{field}[{index}]")
    if len(set(items)) != len(items):
        raise ValuationError(f"{field} must not contain duplicates")
    return items


def _non_empty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValuationError(f"{field} must be a non-empty string")
    return value


def _parse_decimal(value: object, field: str) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise ValuationError(f"{field} must be a decimal string, integer, or Decimal")
    if isinstance(value, Decimal):
        decimal = value
    elif isinstance(value, int):
        decimal = Decimal(value)
    elif isinstance(value, str):
        if not value.strip():
            raise ValuationError(f"{field} must be a non-empty decimal string")
        try:
            decimal = Decimal(value)
        except (InvalidOperation, ValueError) as exc:
            raise ValuationError(f"{field} must be a finite decimal") from exc
    else:
        raise ValuationError(f"{field} must be a decimal string, integer, or Decimal")
    if not decimal.is_finite():
        raise ValuationError(f"{field} must be a finite decimal")
    return decimal


def _positive(value: Decimal, label: str) -> None:
    if value <= ZERO:
        raise ValuationError(f"{label} must be positive")


def _format_decimal(value: Decimal) -> str:
    try:
        quantized = value.quantize(QUANT, rounding=ROUND_HALF_UP)
    except InvalidOperation as exc:
        raise ValuationError("value cannot be represented at valuation precision") from exc
    if quantized == ZERO:
        quantized = abs(quantized)
    return format(quantized, "f")


_MISSING = object()


def _diff_without_baseline(baseline: Mapping, result: Mapping) -> list[dict]:
    baseline_content = dict(_mapping(baseline, "baseline"))
    result_content = dict(result)
    baseline_content.pop("baseline_diff", None)
    result_content.pop("baseline_diff", None)
    diff: list[dict] = []
    _diff_values(baseline_content, result_content, "$", diff)
    return sorted(diff, key=lambda item: item["path"])


def _diff_values(left: object, right: object, path: str, diff: list[dict]) -> None:
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        for key in sorted(set(left) | set(right)):
            child_path = f"{path}.{key}" if str(key).isidentifier() else f'{path}["{key}"]'
            _diff_values(left.get(key, _MISSING), right.get(key, _MISSING), child_path, diff)
        return
    if isinstance(left, list) and isinstance(right, list):
        for index in range(max(len(left), len(right))):
            left_value = left[index] if index < len(left) else _MISSING
            right_value = right[index] if index < len(right) else _MISSING
            _diff_values(left_value, right_value, f"{path}[{index}]", diff)
        return
    if left != right:
        diff.append({
            "path": path,
            "baseline": None if left is _MISSING else left,
            "value": None if right is _MISSING else right,
        })
