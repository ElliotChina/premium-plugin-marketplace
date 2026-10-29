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
CALCULATOR_VERSION = "company-analysis-valuation-calculator-v2"
SUPPORTED_FAMILIES = frozenset({
    "price-multiple", "yield", "enterprise-multiple",
    "dcf-fcff", "dcf-equity", "residual-income", "rnpv", "embedded-value", "sotp",
})
SENSITIVITY_PARAMETERS = {
    "price-multiple": frozenset({"denominator", "multiple"}),
    "yield": frozenset({"denominator", "yield"}),
    "enterprise-multiple": frozenset({"denominator", "multiple"}),
    "dcf-fcff": frozenset({"wacc", "terminal_growth"}),
    "dcf-equity": frozenset({"cash_flow_shift", "cost_of_equity", "terminal_growth"}),
    "residual-income": frozenset({"eps_shift", "terminal_roe", "cost_of_equity", "terminal_growth"}),
    "rnpv": frozenset({"cash_flow_shift", "probability_of_success", "discount_rate", "terminal_value"}),
    "embedded-value": frozenset({
        "adjusted_net_worth_shift", "value_of_in_force_shift",
        "new_business_value_shift", "new_business_multiple",
    }),
    "sotp": frozenset({"component_value", "debt_like_claims"}),
}
DCF_INPUT_MODES = frozenset({"fcff", "drivers"})
DCF_TERMINAL_MODES = frozenset({"reinvestment-consistent", "gordon", "finite"})
DCF_EQUITY_CASH_FLOW_TYPES = frozenset({"fcfe", "dividend"})
DCF_EQUITY_OPERATING_PARAMETERS = frozenset({"cash_flow_shift"})
RESIDUAL_INCOME_DRIVER_FIELDS = ("base_book_value_per_share_fact_id", "eps", "dividend_per_share")
RESIDUAL_INCOME_OPERATING_PARAMETERS = frozenset({"eps_shift", "terminal_roe"})
RNPV_CASE_FIELDS = ("cash_flows", "probability_of_success", "discount_rate", "terminal_value")
RNPV_OPERATING_PARAMETERS = frozenset({"cash_flow_shift", "probability_of_success"})
EMBEDDED_VALUE_CASE_FIELDS = (
    "adjusted_net_worth", "value_of_in_force", "new_business_value", "new_business_multiple",
)
EMBEDDED_VALUE_OPERATING_PARAMETERS = frozenset({
    "value_of_in_force_shift", "new_business_value_shift",
})
CASE_BASE_FACT_KEYS = {
    "dcf-fcff": "base_revenue_fact_id",
    "residual-income": "base_book_value_per_share_fact_id",
}
DCF_DRIVER_FIELDS = (
    "base_revenue_fact_id", "revenue_growth", "operating_margin", "tax_rate", "sales_to_capital",
)
DCF_DRIVER_SENSITIVITY_PARAMETERS = frozenset({
    "revenue_growth_shift", "operating_margin_shift", "sales_to_capital_shift",
    "wacc", "terminal_growth",
})
DCF_DRIVER_SHIFTS = frozenset({
    "revenue_growth_shift", "operating_margin_shift", "sales_to_capital_shift",
})
DCF_FINITE_SENSITIVITY_PARAMETERS = frozenset({"terminal_value", "wacc"})
GROWTH_CONVERGENCE_TOLERANCE = Decimal("0.02")
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
    _enforce_ordered_scenario_ranges(method_results)
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
        "parameter_derivation": _derivations_by_method(assumptions.get("parameter_derivation", [])),
    }


def _derivations_by_method(value: object) -> dict[str, list[Mapping]]:
    if not isinstance(value, list):
        raise ValuationError("assumptions.parameter_derivation must be a list")
    grouped: dict[str, list[Mapping]] = {}
    for index, entry in enumerate(value):
        item = _mapping(entry, f"assumptions.parameter_derivation[{index}]")
        method_id = _non_empty_string(
            item.get("method_id"), f"assumptions.parameter_derivation[{index}].method_id"
        )
        grouped.setdefault(method_id, []).append(item)
    return grouped


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
    elif family == "dcf-equity":
        result = _calculate_equity_dcf(method, context)
    elif family == "residual-income":
        result = _calculate_residual_income(method, context)
    elif family == "rnpv":
        result = _calculate_rnpv(method, context)
    elif family == "embedded-value":
        result = _calculate_embedded_value(method, context)
    elif family == "sotp":
        result = _calculate_sotp(method, context)
    else:
        raise ValuationError("method.family is not supported")
    if "sensitivity" in method:
        result["sensitivity"] = _sensitivity(method, context)
    derivations = context["parameter_derivation"].get(method["method_id"])
    if derivations:
        result["parameter_derivation"] = derivations
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
    neutral_share = None
    consistency_flags = set()
    for name, scenario in _scenarios(method):
        field = f"{method['method_id']}.{name}"
        if "range" not in scenario:
            raise ValuationError(f"{field} must declare an explicit range case")
        lower_case, upper_case = _case_range(scenario, f"{field}.range")
        lower_price, lower_share, lower_flags = _dcf_metrics(
            method, lower_case, bridge, shares, context, f"{field}.range.lower")
        upper_price, upper_share, upper_flags = _dcf_metrics(
            method, upper_case, bridge, shares, context, f"{field}.range.upper")
        consistency_flags.update(lower_flags)
        consistency_flags.update(upper_flags)
        if name == "neutral":
            neutral_share = {"lower": _format_decimal(lower_share), "upper": _format_decimal(upper_share)}
        scenarios.append(_scenario_output(name, min(lower_price, upper_price), max(lower_price, upper_price), min(lower_price, upper_price), max(lower_price, upper_price), {}))
    result = _method_output(method, scenarios)
    if neutral_share is not None:
        result["terminal_value_share"] = neutral_share
    if consistency_flags:
        result["consistency_flags"] = sorted(consistency_flags)
    return result


def _calculate_equity_dcf(method: Mapping, context: Mapping) -> dict:
    shares = _diluted_shares(method, context)
    cash_flow_type = _equity_cash_flow_type(method)
    scenarios = []
    neutral_share = None
    for name, scenario in _scenarios(method):
        field = f"{method['method_id']}.{name}"
        if "range" not in scenario:
            raise ValuationError(f"{field} must declare an explicit range case")
        lower_case, upper_case = _case_range(scenario, f"{field}.range")
        lower_price, lower_share = _equity_dcf_metrics(
            method, cash_flow_type, lower_case, shares, f"{field}.range.lower")
        upper_price, upper_share = _equity_dcf_metrics(
            method, cash_flow_type, upper_case, shares, f"{field}.range.upper")
        if name == "neutral":
            neutral_share = {"lower": _format_decimal(lower_share), "upper": _format_decimal(upper_share)}
        scenarios.append(_scenario_output(name, min(lower_price, upper_price), max(lower_price, upper_price), min(lower_price, upper_price), max(lower_price, upper_price), {}))
    result = _method_output(method, scenarios)
    if neutral_share is not None:
        result["terminal_value_share"] = neutral_share
    return result


def _equity_cash_flow_type(method: Mapping) -> str:
    cash_flow_type = method.get("cash_flow_type")
    if cash_flow_type not in DCF_EQUITY_CASH_FLOW_TYPES:
        raise ValuationError("dcf-equity cash_flow_type must be fcfe or dividend")
    return cash_flow_type


def _equity_dcf_metrics(
    method: Mapping, cash_flow_type: str, scenario: Mapping, shares: Decimal, field: str,
) -> tuple[Decimal, Decimal]:
    """Per-share equity DCF value and terminal value share; no enterprise bridge."""
    data = _mapping(scenario, field)
    horizon = _dcf_horizon(method)
    cost_of_equity = _parse_decimal(data.get("cost_of_equity"), f"{field}.cost_of_equity")
    terminal_growth = _parse_decimal(data.get("terminal_growth"), f"{field}.terminal_growth")
    if cost_of_equity <= ZERO:
        raise ValuationError(f"{field}.cost_of_equity must be positive")
    if terminal_growth <= -ONE:
        raise ValuationError(f"{field}.terminal_growth must be greater than -1")
    if cost_of_equity <= terminal_growth:
        raise ValuationError(f"{field}.cost_of_equity must exceed terminal_growth")
    flows = _equity_cash_flows(data, cash_flow_type, horizon, field)
    explicit_value = sum(
        cash_flow / ((ONE + cost_of_equity) ** Decimal(index))
        for index, cash_flow in enumerate(flows, start=1)
    )
    terminal_value = flows[-1] * (ONE + terminal_growth) / (cost_of_equity - terminal_growth)
    discounted_terminal = terminal_value / ((ONE + cost_of_equity) ** Decimal(len(flows)))
    equity_value = explicit_value + discounted_terminal
    terminal_share = discounted_terminal / equity_value if equity_value > ZERO else ZERO
    return equity_value / shares, terminal_share


def _equity_cash_flows(data: Mapping, cash_flow_type: str, horizon: int, field: str) -> list[Decimal]:
    values = _list(data.get("cash_flows"), f"{field}.cash_flows")
    if len(values) != horizon:
        raise ValuationError(f"{field}.cash_flows length must equal horizon_years")
    flows = [_parse_decimal(value, f"{field}.cash_flows[{index}]") for index, value in enumerate(values)]
    if cash_flow_type == "dividend" and any(flow < ZERO for flow in flows):
        raise ValuationError(f"{field}.cash_flows dividends must not be negative")
    return flows


def _calculate_residual_income(method: Mapping, context: Mapping) -> dict:
    scenarios = []
    neutral_share = None
    consistency_flags = set()
    for name, scenario in _scenarios(method):
        field = f"{method['method_id']}.{name}"
        if "range" not in scenario:
            raise ValuationError(f"{field} must declare an explicit range case")
        lower_case, upper_case = _case_range(scenario, f"{field}.range")
        lower_price, lower_share, lower_flags = _residual_income_metrics(
            method, lower_case, context, f"{field}.range.lower")
        upper_price, upper_share, upper_flags = _residual_income_metrics(
            method, upper_case, context, f"{field}.range.upper")
        consistency_flags.update(lower_flags)
        consistency_flags.update(upper_flags)
        if name == "neutral":
            neutral_share = {"lower": _format_decimal(lower_share), "upper": _format_decimal(upper_share)}
        scenarios.append(_scenario_output(name, min(lower_price, upper_price), max(lower_price, upper_price), min(lower_price, upper_price), max(lower_price, upper_price), {}))
    result = _method_output(method, scenarios)
    if neutral_share is not None:
        result["terminal_value_share"] = neutral_share
    if consistency_flags:
        result["consistency_flags"] = sorted(consistency_flags)
    return result


def _residual_income_metrics(
    method: Mapping, scenario: Mapping, context: Mapping, field: str,
) -> tuple[Decimal, Decimal, set[str]]:
    """Per-share residual income value with clean-surplus book value roll-forward."""
    data = _mapping(scenario, field)
    horizon = _dcf_horizon(method)
    cost_of_equity = _parse_decimal(data.get("cost_of_equity"), f"{field}.cost_of_equity")
    terminal_growth = _parse_decimal(data.get("terminal_growth"), f"{field}.terminal_growth")
    terminal_roe = _parse_decimal(data.get("terminal_roe"), f"{field}.terminal_roe")
    if cost_of_equity <= ZERO:
        raise ValuationError(f"{field}.cost_of_equity must be positive")
    if terminal_growth <= -ONE:
        raise ValuationError(f"{field}.terminal_growth must be greater than -1")
    if cost_of_equity <= terminal_growth:
        raise ValuationError(f"{field}.cost_of_equity must exceed terminal_growth")
    drivers = _mapping(data.get("drivers"), f"{field}.drivers")
    if set(drivers) != set(RESIDUAL_INCOME_DRIVER_FIELDS):
        raise ValuationError(
            f"{field}.drivers must declare exactly {', '.join(RESIDUAL_INCOME_DRIVER_FIELDS)}"
        )
    base = _per_share_fact(
        context,
        _non_empty_string(
            drivers["base_book_value_per_share_fact_id"],
            f"{field}.drivers.base_book_value_per_share_fact_id",
        ),
        f"{field}.drivers.base_book_value_per_share_fact_id",
    )
    _positive(base["value"], "base book value per share")
    eps = _driver_array(drivers["eps"], horizon, f"{field}.drivers.eps")
    dividends = _driver_array(drivers["dividend_per_share"], horizon, f"{field}.drivers.dividend_per_share")
    if any(dividend < ZERO for dividend in dividends):
        raise ValuationError(f"{field}.drivers.dividend_per_share must not be negative")
    book = base["value"]
    explicit_value = ZERO
    for index, (earnings, dividend) in enumerate(zip(eps, dividends), start=1):
        residual_income = earnings - cost_of_equity * book
        explicit_value += residual_income / ((ONE + cost_of_equity) ** Decimal(index))
        book = book + earnings - dividend
        if book <= ZERO:
            raise ValuationError(f"{field}.drivers book value per share must stay positive")
    terminal_residual_income = (terminal_roe - cost_of_equity) * book
    terminal_value = terminal_residual_income / (cost_of_equity - terminal_growth)
    discounted_terminal = terminal_value / ((ONE + cost_of_equity) ** Decimal(len(eps)))
    value = base["value"] + explicit_value + discounted_terminal
    flags = {"terminal-roe-below-cost-of-equity"} if terminal_roe < cost_of_equity else set()
    terminal_share = discounted_terminal / value if value > ZERO else ZERO
    return value, terminal_share, flags


def _calculate_rnpv(method: Mapping, context: Mapping) -> dict:
    shares = _diluted_shares(method, context)
    scenarios = []
    neutral_share = None
    for name, scenario in _scenarios(method):
        field = f"{method['method_id']}.{name}"
        if "range" not in scenario:
            raise ValuationError(f"{field} must declare an explicit range case")
        lower_case, upper_case = _case_range(scenario, f"{field}.range")
        lower_price, lower_share = _rnpv_metrics(
            method, lower_case, shares, f"{field}.range.lower")
        upper_price, upper_share = _rnpv_metrics(
            method, upper_case, shares, f"{field}.range.upper")
        if name == "neutral":
            neutral_share = {"lower": _format_decimal(lower_share), "upper": _format_decimal(upper_share)}
        scenarios.append(_scenario_output(name, min(lower_price, upper_price), max(lower_price, upper_price), min(lower_price, upper_price), max(lower_price, upper_price), {}))
    result = _method_output(method, scenarios)
    if neutral_share is not None:
        result["terminal_value_share"] = neutral_share
    return result


def _rnpv_metrics(
    method: Mapping, scenario: Mapping, shares: Decimal, field: str,
) -> tuple[Decimal, Decimal]:
    """Per-share risk-adjusted pipeline value and terminal value share."""
    data = _mapping(scenario, field)
    horizon = _dcf_horizon(method)
    flows = _rnpv_cash_flows(data, horizon, field)
    probability = _parse_decimal(data.get("probability_of_success"), f"{field}.probability_of_success")
    if not (ZERO < probability <= ONE):
        raise ValuationError(f"{field}.probability_of_success must be in (0, 1]")
    discount_rate = _parse_decimal(data.get("discount_rate"), f"{field}.discount_rate")
    if discount_rate <= ZERO:
        raise ValuationError(f"{field}.discount_rate must be positive")
    terminal_value = _parse_decimal(data.get("terminal_value"), f"{field}.terminal_value")
    explicit_value = sum(
        cash_flow / ((ONE + discount_rate) ** Decimal(index))
        for index, cash_flow in enumerate(flows, start=1)
    )
    discounted_terminal = terminal_value / ((ONE + discount_rate) ** Decimal(horizon))
    value = probability * (explicit_value + discounted_terminal)
    if value <= ZERO:
        raise ValuationError(f"{field} risk-adjusted value must be positive")
    terminal_share = probability * discounted_terminal / value
    return value / shares, terminal_share


def _rnpv_cash_flows(data: Mapping, horizon: int, field: str) -> list[Decimal]:
    values = _list(data.get("cash_flows"), f"{field}.cash_flows")
    if len(values) != horizon:
        raise ValuationError(f"{field}.cash_flows length must equal horizon_years")
    return [_parse_decimal(value, f"{field}.cash_flows[{index}]") for index, value in enumerate(values)]


def _calculate_embedded_value(method: Mapping, context: Mapping) -> dict:
    shares = _diluted_shares(method, context)
    scenarios = []
    for name, scenario in _scenarios(method):
        field = f"{method['method_id']}.{name}"
        if "range" not in scenario:
            raise ValuationError(f"{field} must declare an explicit range case")
        lower_case, upper_case = _case_range(scenario, f"{field}.range")
        lower_price = _embedded_value_price(lower_case, shares, f"{field}.range.lower")
        upper_price = _embedded_value_price(upper_case, shares, f"{field}.range.upper")
        scenarios.append(_scenario_output(name, min(lower_price, upper_price), max(lower_price, upper_price), min(lower_price, upper_price), max(lower_price, upper_price), {}))
    return _method_output(method, scenarios)


def _embedded_value_price(scenario: Mapping, shares: Decimal, field: str) -> Decimal:
    return _embedded_value_total(_mapping(scenario, field), field) / shares


def _embedded_value_total(data: Mapping, field: str) -> Decimal:
    adjusted_net_worth = _parse_decimal(data.get("adjusted_net_worth"), f"{field}.adjusted_net_worth")
    value_of_in_force = _parse_decimal(data.get("value_of_in_force"), f"{field}.value_of_in_force")
    new_business_value = _parse_decimal(data.get("new_business_value"), f"{field}.new_business_value")
    multiple = _parse_decimal(data.get("new_business_multiple"), f"{field}.new_business_multiple")
    if multiple < ZERO:
        raise ValuationError(f"{field}.new_business_multiple must not be negative")
    total = adjusted_net_worth + value_of_in_force + new_business_value * multiple
    if total <= ZERO:
        raise ValuationError(f"{field} appraisal value must be positive")
    return total


def _driver_array(value: object, horizon: int, field: str) -> list[Decimal]:
    values = _list(value, field)
    if len(values) != horizon:
        raise ValuationError(f"{field} length must equal horizon_years")
    return [_parse_decimal(entry, f"{field}[{index}]") for index, entry in enumerate(values)]


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
    output = {
        "method_id": method["method_id"],
        "family": method["family"],
        "direction": method.get("direction"),
        "scenarios": list(scenarios),
        "scenario_layout": _scenario_layout(scenarios),
    }
    for key in ("input_mode", "cash_flow_type", "horizon_years"):
        if key in method:
            output[key] = method[key]
    return output


def _scenario_layout(scenarios: Sequence[Mapping]) -> list[dict]:
    """Report gaps and overlaps between adjacent scenario price ranges."""
    by_scenario = {item["scenario"]: item for item in scenarios}
    layout = []
    for left, right in (("conservative", "neutral"), ("neutral", "optimistic")):
        left_upper = _parse_decimal(
            by_scenario[left]["price_range"]["upper"], f"{left}.price_range.upper"
        )
        right_lower = _parse_decimal(
            by_scenario[right]["price_range"]["lower"], f"{right}.price_range.lower"
        )
        if left_upper < right_lower:
            layout.append({
                "between": [left, right],
                "type": "gap",
                "amount": _format_decimal(right_lower - left_upper),
            })
        elif left_upper > right_lower:
            layout.append({
                "between": [left, right],
                "type": "overlap",
                "amount": _format_decimal(left_upper - right_lower),
            })
    return layout


def _enforce_ordered_scenario_ranges(method_results: Sequence[Mapping]) -> None:
    """Scenarios must be ordered; gaps and overlaps between them are allowed."""
    for result in method_results:
        by_scenario = {item["scenario"]: item for item in result["scenarios"]}
        if set(by_scenario) != set(SCENARIOS):
            raise ValuationError(
                f"{result['method_id']} scenarios must include conservative, neutral, and optimistic"
            )
        _scenario_thresholds(result["family"], result)


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
        "scenario_membership": _scenario_membership(method_result, current_price),
        "boundary_prices": {
            "conservative_lower": _format_decimal(boundary_prices["conservative_lower"]),
            "optimistic_lower": _format_decimal(boundary_prices["optimistic_lower"]),
        },
        "spaces": {
            "conservative": None if conservative_space is None else _format_decimal(conservative_space),
            "optimistic": None if optimistic_space is None else _format_decimal(optimistic_space),
        },
    }


def _scenario_membership(method_result: Mapping, price: Decimal | None) -> list[str] | None:
    """Which scenario ranges contain the current price; overlaps can return several."""
    if price is None:
        return None
    names = []
    for item in method_result["scenarios"]:
        lower = _parse_decimal(item["price_range"]["lower"], f"{item['scenario']}.price_range.lower")
        upper = _parse_decimal(item["price_range"]["upper"], f"{item['scenario']}.price_range.upper")
        if lower <= price <= upper:
            names.append(item["scenario"])
    return names


def _enforce_primary_requirements(method: Mapping) -> None:
    if "sensitivity" not in method:
        raise ValuationError("primary method sensitivity must be a valid 3x3 grid")
    if method["family"] in {
        "dcf-fcff", "dcf-equity", "residual-income", "rnpv", "embedded-value", "sotp",
    }:
        sensitivity = _mapping(method["sensitivity"], f"{method['method_id']}.sensitivity")
        if "base_case" not in sensitivity:
            raise ValuationError(f"primary {method['family']} sensitivity.base_case is required")
        _validate_model_case(method, sensitivity["base_case"], f"{method['method_id']}.sensitivity.base_case")
        for name, scenario in _scenarios(method):
            if "range" not in scenario:
                raise ValuationError(f"primary {method['family']} scenarios must declare explicit range cases")
            _case_range(scenario, f"{method['method_id']}.{name}.range")


def _scenario_thresholds(family: str, method_result: Mapping) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    """Four classification anchors taken from the ordered scenario ranges.

    Scenarios need not touch: only the four outer anchors must be strictly ordered.
    """
    method_id = method_result.get("method_id", "method")
    by_scenario = {item["scenario"]: item for item in method_result["scenarios"]}
    ranges = {
        name: (
            _parse_decimal(
                by_scenario[name]["indicator_range"]["lower"],
                f"{method_id}.{name}.indicator_range.lower",
            ),
            _parse_decimal(
                by_scenario[name]["indicator_range"]["upper"],
                f"{method_id}.{name}.indicator_range.upper",
            ),
        )
        for name in SCENARIOS
    }
    if family == "yield":
        thresholds = (
            ranges["optimistic"][0],
            ranges["neutral"][0],
            ranges["neutral"][1],
            ranges["conservative"][1],
        )
        ordering = "optimistic < neutral < conservative"
    else:
        thresholds = (
            ranges["conservative"][0],
            ranges["neutral"][0],
            ranges["neutral"][1],
            ranges["optimistic"][1],
        )
        ordering = "conservative < neutral < optimistic"
    if not all(left < right for left, right in zip(thresholds, thresholds[1:])):
        raise ValuationError(f"{method_id} scenario ranges must be ordered: {ordering}")
    return thresholds


def _primary_thresholds(method: Mapping, method_result: Mapping) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    return _scenario_thresholds(method["family"], method_result)


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
            "above-optimistic",
            "optimistic-zone",
            "neutral-zone",
            "conservative-zone",
            "below-conservative",
        )
    return (
        "below-conservative",
        "conservative-zone",
        "neutral-zone",
        "optimistic-zone",
        "above-optimistic",
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
    if family in {
        "dcf-fcff", "dcf-equity", "residual-income", "rnpv", "embedded-value", "sotp",
    }:
        return context["current_price"]["value"]
    raise ValuationError("method.family is not supported")


def _sensitivity(method: Mapping, context: Mapping) -> dict:
    data = _mapping(method["sensitivity"], f"{method['method_id']}.sensitivity")
    row_parameter = _non_empty_string(data.get("row_parameter"), f"{method['method_id']}.sensitivity.row_parameter")
    column_parameter = _non_empty_string(data.get("column_parameter"), f"{method['method_id']}.sensitivity.column_parameter")
    base_case = _sensitivity_base_case(method, data)
    _validate_sensitivity_parameters(method, row_parameter, column_parameter, base_case)
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


def _validate_sensitivity_parameters(
    method: Mapping, row_parameter: str, column_parameter: str, base_case: Mapping | None,
) -> None:
    if row_parameter == column_parameter:
        raise ValuationError("sensitivity row and column parameters must be different")
    family = method["family"]
    if family == "dcf-fcff" and base_case is not None and _terminal_mode(
        base_case, f"{method['method_id']}.sensitivity.base_case"
    ) == "finite":
        if {row_parameter, column_parameter} != DCF_FINITE_SENSITIVITY_PARAMETERS:
            raise ValuationError("dcf-fcff finite sensitivity parameters must be exactly terminal_value, wacc")
        return
    if family == "dcf-fcff" and _dcf_input_mode(method) == "drivers":
        selected = {row_parameter, column_parameter}
        if not selected <= DCF_DRIVER_SENSITIVITY_PARAMETERS:
            joined = ", ".join(sorted(DCF_DRIVER_SENSITIVITY_PARAMETERS))
            raise ValuationError(f"dcf-fcff driver sensitivity parameters must come from {joined}")
        if not selected & DCF_DRIVER_SHIFTS:
            raise ValuationError("dcf-fcff driver sensitivity must include an operating driver shift")
        return
    if family == "dcf-equity":
        selected = {row_parameter, column_parameter}
        if not selected <= SENSITIVITY_PARAMETERS[family]:
            joined = ", ".join(sorted(SENSITIVITY_PARAMETERS[family]))
            raise ValuationError(f"dcf-equity sensitivity parameters must come from {joined}")
        if not selected & DCF_EQUITY_OPERATING_PARAMETERS:
            raise ValuationError("dcf-equity sensitivity must include a cash flow shift")
        return
    if family == "residual-income":
        selected = {row_parameter, column_parameter}
        if not selected <= SENSITIVITY_PARAMETERS[family]:
            joined = ", ".join(sorted(SENSITIVITY_PARAMETERS[family]))
            raise ValuationError(f"residual-income sensitivity parameters must come from {joined}")
        if not selected & RESIDUAL_INCOME_OPERATING_PARAMETERS:
            raise ValuationError("residual-income sensitivity must include an operating parameter")
        return
    if family == "rnpv":
        selected = {row_parameter, column_parameter}
        if not selected <= SENSITIVITY_PARAMETERS[family]:
            joined = ", ".join(sorted(SENSITIVITY_PARAMETERS[family]))
            raise ValuationError(f"rnpv sensitivity parameters must come from {joined}")
        if not selected & RNPV_OPERATING_PARAMETERS:
            raise ValuationError("rnpv sensitivity must include an operating parameter")
        return
    if family == "embedded-value":
        selected = {row_parameter, column_parameter}
        if not selected <= SENSITIVITY_PARAMETERS[family]:
            joined = ", ".join(sorted(SENSITIVITY_PARAMETERS[family]))
            raise ValuationError(f"embedded-value sensitivity parameters must come from {joined}")
        if not selected & EMBEDDED_VALUE_OPERATING_PARAMETERS:
            raise ValuationError("embedded-value sensitivity must include an operating parameter")
        return
    expected = SENSITIVITY_PARAMETERS[family]
    if {row_parameter, column_parameter} != expected:
        joined = ", ".join(sorted(expected))
        raise ValuationError(f"{family} sensitivity parameters must be exactly {joined}")


def _sensitivity_base_case(method: Mapping, data: Mapping) -> Mapping | None:
    family = method["family"]
    if family not in {
        "dcf-fcff", "dcf-equity", "residual-income", "rnpv", "embedded-value", "sotp",
    }:
        return None
    if "base_case" not in data:
        raise ValuationError(f"{method['method_id']}.sensitivity.base_case is required for {family}")
    base_case = _mapping(data["base_case"], f"{method['method_id']}.sensitivity.base_case")
    _validate_model_case(method, base_case, f"{method['method_id']}.sensitivity.base_case")
    return base_case


def _validate_model_case(method: Mapping, value: object, field: str) -> Mapping:
    family = method["family"]
    data = _mapping(value, field)
    if family == "dcf-fcff":
        _dcf_case_shape(method, data, field)
    elif family == "dcf-equity":
        _equity_dcf_case_shape(method, data, field)
    elif family == "residual-income":
        _residual_income_case_shape(method, data, field)
    elif family == "rnpv":
        _rnpv_case_shape(method, data, field)
    elif family == "embedded-value":
        _embedded_value_case_shape(data, field)
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
        adjusted = _dcf_case_with_parameter(base_case, values)
        return _dcf_price(
            method, adjusted, _bridge_values(method, context),
            _diluted_shares(method, context), context, f"{method['method_id']}.sensitivity",
        )
    if family == "dcf-equity":
        values = {row_parameter: row_value, column_parameter: column_value}
        assert base_case is not None
        adjusted = _equity_case_with_parameter(base_case, values)
        return _equity_dcf_metrics(
            method, _equity_cash_flow_type(method), adjusted,
            _diluted_shares(method, context), f"{method['method_id']}.sensitivity",
        )[0]
    if family == "residual-income":
        values = {row_parameter: row_value, column_parameter: column_value}
        assert base_case is not None
        adjusted = _residual_income_case_with_parameter(base_case, values)
        return _residual_income_metrics(
            method, adjusted, context, f"{method['method_id']}.sensitivity",
        )[0]
    if family == "rnpv":
        values = {row_parameter: row_value, column_parameter: column_value}
        assert base_case is not None
        adjusted = _rnpv_case_with_parameter(base_case, values)
        return _rnpv_metrics(
            method, adjusted, _diluted_shares(method, context), f"{method['method_id']}.sensitivity",
        )[0]
    if family == "embedded-value":
        values = {row_parameter: row_value, column_parameter: column_value}
        assert base_case is not None
        adjusted = _embedded_value_case_with_parameter(base_case, values)
        return _embedded_value_price(
            adjusted, _diluted_shares(method, context), f"{method['method_id']}.sensitivity",
        )
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


def _dcf_price(
    method: Mapping, scenario: Mapping, bridge: Mapping[str, Decimal],
    shares: Decimal, context: Mapping, field: str,
) -> Decimal:
    return _dcf_metrics(method, scenario, bridge, shares, context, field)[0]


def _dcf_metrics(
    method: Mapping, scenario: Mapping, bridge: Mapping[str, Decimal],
    shares: Decimal, context: Mapping, field: str,
) -> tuple[Decimal, Decimal, set[str]]:
    """Per-share price, terminal value share, and deterministic consistency flags."""
    data = _mapping(scenario, field)
    wacc = _parse_decimal(data.get("wacc"), f"{field}.wacc")
    if wacc <= ZERO:
        raise ValuationError("wacc must be positive")
    input_mode = _dcf_input_mode(method)
    horizon = _dcf_horizon(method)
    flags: set[str] = set()
    growth_path: list[Decimal] | None = None
    if input_mode == "fcff":
        fcff_values = _list(data.get("fcff"), f"{field}.fcff")
        if len(fcff_values) != horizon:
            raise ValuationError(f"{field}.fcff length must equal horizon_years")
        fcff = [_parse_decimal(value, f"{field}.fcff[{index}]") for index, value in enumerate(fcff_values)]
        terminal_nopat = (
            _parse_decimal(data["terminal_nopat"], f"{field}.terminal_nopat")
            if "terminal_nopat" in data else None
        )
    else:
        fcff, terminal_nopat, growth_path = _driver_fcff(data, context, horizon, field)
    terminal_mode = _terminal_mode(data, field)
    if terminal_mode == "finite":
        # Finite-life assets carry an explicit residual value; it may be zero or negative.
        terminal_value = _parse_decimal(data.get("terminal_value"), f"{field}.terminal_value")
    else:
        terminal_growth = _parse_decimal(data.get("terminal_growth"), f"{field}.terminal_growth")
        if terminal_growth <= -ONE:
            raise ValuationError("terminal_growth must be greater than -1")
        if wacc <= terminal_growth:
            raise ValuationError("wacc must exceed terminal_growth")
        if terminal_mode == "gordon":
            if "terminal_roic" in data or "terminal_nopat" in data:
                raise ValuationError(f"{field} gordon terminal value does not accept terminal_roic or terminal_nopat")
            terminal_value = fcff[-1] * (ONE + terminal_growth) / (wacc - terminal_growth)
        else:
            terminal_roic = _parse_decimal(data.get("terminal_roic"), f"{field}.terminal_roic")
            if terminal_roic <= ZERO:
                raise ValuationError(f"{field}.terminal_roic must be positive")
            if terminal_roic <= terminal_growth:
                raise ValuationError(f"{field}.terminal_roic must exceed terminal_growth")
            if terminal_nopat is None or terminal_nopat <= ZERO:
                raise ValuationError(f"{field}.terminal_nopat must be positive for reinvestment-consistent terminal value")
            terminal_value = (
                terminal_nopat * (ONE + terminal_growth)
                * (ONE - terminal_growth / terminal_roic)
                / (wacc - terminal_growth)
            )
            if terminal_roic < wacc:
                flags.add("terminal-roic-below-wacc")
        if growth_path is not None and abs(growth_path[-1] - terminal_growth) > GROWTH_CONVERGENCE_TOLERANCE:
            flags.add("growth-not-converged")
    explicit_value = sum(
        cash_flow / ((ONE + wacc) ** Decimal(index))
        for index, cash_flow in enumerate(fcff, start=1)
    )
    discounted_terminal = terminal_value / ((ONE + wacc) ** Decimal(len(fcff)))
    enterprise_value = explicit_value + discounted_terminal
    # Non-positive enterprise value makes the share meaningless; report zero and let other checks catch it.
    terminal_share = discounted_terminal / enterprise_value if enterprise_value > ZERO else ZERO
    return _enterprise_price(enterprise_value, bridge, shares), terminal_share, flags


def _dcf_input_mode(method: Mapping) -> str:
    mode = method.get("input_mode")
    if mode not in DCF_INPUT_MODES:
        raise ValuationError("dcf-fcff input_mode must be fcff or drivers")
    return mode


def _dcf_horizon(method: Mapping) -> int:
    horizon = method.get("horizon_years")
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon <= 0:
        raise ValuationError("dcf-fcff horizon_years must be a positive integer")
    return horizon


def _terminal_mode(data: Mapping, field: str) -> str:
    mode = data.get("terminal_mode", "reinvestment-consistent")
    if mode not in DCF_TERMINAL_MODES:
        raise ValuationError(f"{field}.terminal_mode must be reinvestment-consistent, gordon, or finite")
    return mode


def _dcf_case_shape(method: Mapping, data: Mapping, field: str) -> None:
    horizon = _dcf_horizon(method)
    mode = _dcf_input_mode(method)
    terminal_mode = _terminal_mode(data, field)
    flow_key = "fcff" if mode == "fcff" else "drivers"
    common = {"wacc", "terminal_mode", "evidence_fact_ids"}
    wacc = _parse_decimal(data.get("wacc"), f"{field}.wacc")
    if wacc <= ZERO:
        raise ValuationError(f"{field}.wacc must be positive")
    required = {flow_key, "wacc"}
    if terminal_mode == "finite":
        required.add("terminal_value")
        if not required <= set(data) <= required | common:
            raise ValuationError(f"{field} has invalid finite case keys")
        _parse_decimal(data["terminal_value"], f"{field}.terminal_value")
    else:
        required.add("terminal_growth")
        if terminal_mode == "reinvestment-consistent":
            required.add("terminal_nopat" if mode == "fcff" else "terminal_roic")
        if not required <= set(data) <= required | common:
            raise ValuationError(f"{field} has invalid {terminal_mode} case keys")
        terminal_growth = _parse_decimal(data["terminal_growth"], f"{field}.terminal_growth")
        if terminal_growth <= -ONE:
            raise ValuationError(f"{field}.terminal_growth must be greater than -1")
        if wacc <= terminal_growth:
            raise ValuationError(f"{field}.wacc must exceed terminal_growth")
        if terminal_mode == "reinvestment-consistent":
            if mode == "fcff":
                if _parse_decimal(data["terminal_nopat"], f"{field}.terminal_nopat") <= ZERO:
                    raise ValuationError(f"{field}.terminal_nopat must be positive")
            else:
                roic = _parse_decimal(data["terminal_roic"], f"{field}.terminal_roic")
                if roic <= terminal_growth:
                    raise ValuationError(f"{field}.terminal_roic must exceed terminal_growth")
    if mode == "fcff":
        flows = _list(data["fcff"], f"{field}.fcff")
        if len(flows) != horizon:
            raise ValuationError(f"{field}.fcff length must equal horizon_years")
        for index, value in enumerate(flows):
            _parse_decimal(value, f"{field}.fcff[{index}]")
    else:
        _validate_driver_values(data["drivers"], horizon, f"{field}.drivers")


def _equity_dcf_case_shape(method: Mapping, data: Mapping, field: str) -> None:
    horizon = _dcf_horizon(method)
    cash_flow_type = _equity_cash_flow_type(method)
    required = {"cash_flows", "cost_of_equity", "terminal_growth"}
    if not required <= set(data) <= required | {"evidence_fact_ids"}:
        raise ValuationError(f"{field} has invalid dcf-equity case keys")
    _equity_cash_flows(data, cash_flow_type, horizon, field)
    cost_of_equity = _parse_decimal(data["cost_of_equity"], f"{field}.cost_of_equity")
    terminal_growth = _parse_decimal(data["terminal_growth"], f"{field}.terminal_growth")
    if cost_of_equity <= ZERO:
        raise ValuationError(f"{field}.cost_of_equity must be positive")
    if terminal_growth <= -ONE:
        raise ValuationError(f"{field}.terminal_growth must be greater than -1")
    if cost_of_equity <= terminal_growth:
        raise ValuationError(f"{field}.cost_of_equity must exceed terminal_growth")


def _residual_income_case_shape(method: Mapping, data: Mapping, field: str) -> None:
    horizon = _dcf_horizon(method)
    required = {"drivers", "cost_of_equity", "terminal_growth", "terminal_roe"}
    if not required <= set(data) <= required | {"evidence_fact_ids"}:
        raise ValuationError(f"{field} has invalid residual-income case keys")
    drivers = _mapping(data["drivers"], f"{field}.drivers")
    if set(drivers) != set(RESIDUAL_INCOME_DRIVER_FIELDS):
        raise ValuationError(
            f"{field}.drivers must declare exactly {', '.join(RESIDUAL_INCOME_DRIVER_FIELDS)}"
        )
    _non_empty_string(
        drivers["base_book_value_per_share_fact_id"],
        f"{field}.drivers.base_book_value_per_share_fact_id",
    )
    _driver_array(drivers["eps"], horizon, f"{field}.drivers.eps")
    dividends = _driver_array(drivers["dividend_per_share"], horizon, f"{field}.drivers.dividend_per_share")
    if any(dividend < ZERO for dividend in dividends):
        raise ValuationError(f"{field}.drivers.dividend_per_share must not be negative")
    cost_of_equity = _parse_decimal(data["cost_of_equity"], f"{field}.cost_of_equity")
    terminal_growth = _parse_decimal(data["terminal_growth"], f"{field}.terminal_growth")
    _parse_decimal(data["terminal_roe"], f"{field}.terminal_roe")
    if cost_of_equity <= ZERO:
        raise ValuationError(f"{field}.cost_of_equity must be positive")
    if terminal_growth <= -ONE:
        raise ValuationError(f"{field}.terminal_growth must be greater than -1")
    if cost_of_equity <= terminal_growth:
        raise ValuationError(f"{field}.cost_of_equity must exceed terminal_growth")


def _rnpv_case_shape(method: Mapping, data: Mapping, field: str) -> None:
    horizon = _dcf_horizon(method)
    required = set(RNPV_CASE_FIELDS)
    if not required <= set(data) <= required | {"evidence_fact_ids"}:
        raise ValuationError(f"{field} has invalid rnpv case keys")
    _rnpv_cash_flows(data, horizon, field)
    probability = _parse_decimal(data["probability_of_success"], f"{field}.probability_of_success")
    if not (ZERO < probability <= ONE):
        raise ValuationError(f"{field}.probability_of_success must be in (0, 1]")
    discount_rate = _parse_decimal(data["discount_rate"], f"{field}.discount_rate")
    if discount_rate <= ZERO:
        raise ValuationError(f"{field}.discount_rate must be positive")
    _parse_decimal(data["terminal_value"], f"{field}.terminal_value")


def _embedded_value_case_shape(data: Mapping, field: str) -> None:
    required = set(EMBEDDED_VALUE_CASE_FIELDS)
    if not required <= set(data) <= required | {"evidence_fact_ids"}:
        raise ValuationError(f"{field} has invalid embedded-value case keys")
    _embedded_value_total(data, field)


def _validate_driver_values(drivers: object, horizon: int, field: str) -> None:
    data = _mapping(drivers, field)
    if set(data) != set(DCF_DRIVER_FIELDS):
        raise ValuationError(f"{field} must declare exactly {', '.join(DCF_DRIVER_FIELDS)}")
    _non_empty_string(data["base_revenue_fact_id"], f"{field}.base_revenue_fact_id")
    for key in ("revenue_growth", "operating_margin", "sales_to_capital"):
        values = _list(data[key], f"{field}.{key}")
        if len(values) != horizon:
            raise ValuationError(f"{field}.{key} length must equal horizon_years")
        for index, value in enumerate(values):
            _parse_decimal(value, f"{field}.{key}[{index}]")
    tax_rate = _parse_decimal(data["tax_rate"], f"{field}.tax_rate")
    if tax_rate < ZERO or tax_rate >= ONE:
        raise ValuationError(f"{field}.tax_rate must be in [0, 1)")


def _driver_fcff(
    data: Mapping, context: Mapping, horizon: int, field: str,
) -> tuple[list[Decimal], Decimal, list[Decimal]]:
    drivers = _mapping(data.get("drivers"), f"{field}.drivers")
    if set(drivers) != set(DCF_DRIVER_FIELDS):
        raise ValuationError(f"{field}.drivers must declare exactly {', '.join(DCF_DRIVER_FIELDS)}")
    base = _aggregate_monetary_fact(
        context,
        _non_empty_string(drivers["base_revenue_fact_id"], f"{field}.drivers.base_revenue_fact_id"),
        f"{field}.drivers.base_revenue_fact_id",
    )
    _positive(base["value"], "base revenue")
    growth = [
        _parse_decimal(value, f"{field}.drivers.revenue_growth[{index}]")
        for index, value in enumerate(_list(drivers["revenue_growth"], f"{field}.drivers.revenue_growth"))
    ]
    margins = [
        _parse_decimal(value, f"{field}.drivers.operating_margin[{index}]")
        for index, value in enumerate(_list(drivers["operating_margin"], f"{field}.drivers.operating_margin"))
    ]
    sales_to_capital = [
        _parse_decimal(value, f"{field}.drivers.sales_to_capital[{index}]")
        for index, value in enumerate(_list(drivers["sales_to_capital"], f"{field}.drivers.sales_to_capital"))
    ]
    tax_rate = _parse_decimal(drivers["tax_rate"], f"{field}.drivers.tax_rate")
    if not (len(growth) == len(margins) == len(sales_to_capital) == horizon):
        raise ValuationError(f"{field}.drivers arrays must equal horizon_years")
    if not (ZERO <= tax_rate < ONE):
        raise ValuationError(f"{field}.drivers.tax_rate must be in [0, 1)")
    revenue_previous = base["value"]
    fcff: list[Decimal] = []
    nopat: list[Decimal] = []
    for index in range(horizon):
        if growth[index] <= -ONE:
            raise ValuationError(f"{field}.drivers.revenue_growth[{index}] must be greater than -1")
        if not (ZERO < margins[index] < ONE):
            raise ValuationError(f"{field}.drivers.operating_margin[{index}] must be in (0, 1)")
        if sales_to_capital[index] <= ZERO:
            raise ValuationError(f"{field}.drivers.sales_to_capital[{index}] must be positive")
        revenue = revenue_previous * (ONE + growth[index])
        ebit = revenue * margins[index]
        net_operating_profit = ebit * (ONE - tax_rate)
        reinvestment = (revenue - revenue_previous) / sales_to_capital[index]
        fcff.append(net_operating_profit - reinvestment)
        nopat.append(net_operating_profit)
        revenue_previous = revenue
    return fcff, nopat[-1], growth


def _dcf_case_with_parameter(base_case: Mapping, values: Mapping[str, Decimal]) -> Mapping:
    data = dict(base_case)
    for key in ("wacc", "terminal_growth", "terminal_value"):
        if key in values:
            if key not in data:
                raise ValuationError(f"sensitivity parameter {key} is not valid for the base case")
            data[key] = values[key]
    if "drivers" in data:
        drivers = dict(_mapping(data["drivers"], "sensitivity.base_case.drivers"))
        for parameter, key in (
            ("revenue_growth_shift", "revenue_growth"),
            ("operating_margin_shift", "operating_margin"),
            ("sales_to_capital_shift", "sales_to_capital"),
        ):
            if parameter in values:
                drivers[key] = [
                    _parse_decimal(value, f"sensitivity.base_case.drivers.{key}") + values[parameter]
                    for value in _list(drivers[key], f"sensitivity.base_case.drivers.{key}")
                ]
        data["drivers"] = drivers
    return data


def _equity_case_with_parameter(base_case: Mapping, values: Mapping[str, Decimal]) -> Mapping:
    data = dict(base_case)
    for key in ("cost_of_equity", "terminal_growth"):
        if key in values:
            data[key] = values[key]
    if "cash_flow_shift" in values:
        data["cash_flows"] = [
            _parse_decimal(value, "sensitivity.base_case.cash_flows") + values["cash_flow_shift"]
            for value in _list(data["cash_flows"], "sensitivity.base_case.cash_flows")
        ]
    return data


def _residual_income_case_with_parameter(base_case: Mapping, values: Mapping[str, Decimal]) -> Mapping:
    data = dict(base_case)
    for key in ("cost_of_equity", "terminal_growth", "terminal_roe"):
        if key in values:
            data[key] = values[key]
    if "eps_shift" in values:
        drivers = dict(_mapping(data["drivers"], "sensitivity.base_case.drivers"))
        drivers["eps"] = [
            _parse_decimal(value, "sensitivity.base_case.drivers.eps") + values["eps_shift"]
            for value in _list(drivers["eps"], "sensitivity.base_case.drivers.eps")
        ]
        data["drivers"] = drivers
    return data


def _rnpv_case_with_parameter(base_case: Mapping, values: Mapping[str, Decimal]) -> Mapping:
    data = dict(base_case)
    for key in ("probability_of_success", "discount_rate", "terminal_value"):
        if key in values:
            data[key] = values[key]
    if "cash_flow_shift" in values:
        data["cash_flows"] = [
            _parse_decimal(value, "sensitivity.base_case.cash_flows") + values["cash_flow_shift"]
            for value in _list(data["cash_flows"], "sensitivity.base_case.cash_flows")
        ]
    return data


def _embedded_value_case_with_parameter(base_case: Mapping, values: Mapping[str, Decimal]) -> Mapping:
    data = dict(base_case)
    for parameter, key in (
        ("adjusted_net_worth_shift", "adjusted_net_worth"),
        ("value_of_in_force_shift", "value_of_in_force"),
        ("new_business_value_shift", "new_business_value"),
    ):
        if parameter in values:
            data[key] = _parse_decimal(data[key], f"sensitivity.base_case.{key}") + values[parameter]
    if "new_business_multiple" in values:
        data["new_business_multiple"] = values["new_business_multiple"]
    return data


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


def _per_share_fact(context: Mapping, fact_id: str, field: str) -> dict:
    fact = _monetary_fact(context, fact_id, field)
    if canonical_per_share_unit(fact["unit"], fact["currency"]) is None:
        raise ValuationError(f"{field}.unit must be per-share")
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
