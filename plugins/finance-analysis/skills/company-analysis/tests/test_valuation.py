"""估值契约测试：情景解耦、五档锚点、口径配对、精度三态与发布检查。"""

from __future__ import annotations

import copy
import sys
import unittest
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "valuation"))

import company_run  # noqa: E402
import company_valuation as cv  # noqa: E402
import valuation_consensus as vc  # noqa: E402


def _fact(fact_id: str, value: str, unit: str, currency: str | None = "CNY",
          fact_type: str = "disclosed", status: str = "verified") -> dict:
    return {
        "fact_id": fact_id, "metric": "valuation-input", "value": value, "unit": unit,
        "currency": currency, "period": "2025FY", "consolidation_scope": "consolidated",
        "source_material_id": "S1", "source_locator": "p.1",
        "audit_status": "not-applicable" if fact_type == "assumption" else "audited",
        "methodology": "公司披露口径", "comparability": "可比", "fact_type": fact_type,
        "replaces_fact_id": None, "status": status,
    }


def _facts(eps_fact_type: str = "disclosed", eps_status: str = "verified") -> list[dict]:
    return [
        _fact("f-eps", "2", "CNY/share", fact_type=eps_fact_type, status=eps_status),
        _fact("f-ebit", "100000000", "CNY"),
        _fact("f-shares", "100000000", "shares", currency=None),
        _fact("f-debt", "100000000", "CNY"),
        _fact("f-cash", "50000000", "CNY"),
        _fact("f-fcff", "200000000", "CNY"),
        _fact("f-revenue", "1000000000", "CNY"),
        _fact("f-bvps", "10", "CNY/share"),
    ]


def _price_scenarios() -> dict:
    return {
        "conservative": {"denominator": "2", "range": {"lower": "10", "upper": "13"}},
        "neutral": {"denominator": "2", "range": {"lower": "13", "upper": "17"}},
        "optimistic": {"denominator": "2", "range": {"lower": "17", "upper": "21"}},
    }


def _enterprise_scenarios() -> dict:
    return {
        "conservative": {"denominator": "100000000", "range": {"lower": "21", "upper": "27"}},
        "neutral": {"denominator": "100000000", "range": {"lower": "27", "upper": "35"}},
        "optimistic": {"denominator": "100000000", "range": {"lower": "35", "upper": "43"}},
    }


def _dcf_case(fcff: list[str], wacc: str = "0.09", growth: str = "0.035",
              evidence: bool = True) -> dict:
    case = {
        "fcff": fcff, "wacc": wacc, "terminal_growth": growth,
        "terminal_mode": "gordon",
    }
    if evidence:
        case["evidence_fact_ids"] = ["f-fcff"]
    return case


def _dcf_scenarios(evidence: bool = True) -> dict:
    return {
        "conservative": {"range": {
            "lower": _dcf_case(["180000000", "185000000", "190000000"], evidence=evidence),
            "upper": _dcf_case(["185000000", "190000000", "195000000"], evidence=evidence),
        }},
        "neutral": {"range": {
            "lower": _dcf_case(["190000000", "195000000", "200000000"], evidence=evidence),
            "upper": _dcf_case(["195000000", "200000000", "205000000"], evidence=evidence),
        }},
        "optimistic": {"range": {
            "lower": _dcf_case(["200000000", "205000000", "210000000"], evidence=evidence),
            "upper": _dcf_case(["205000000", "210000000", "215000000"], evidence=evidence),
        }},
    }


def _driver_case(growth: list[str], *, wacc: str = "0.09",
                 terminal_growth: str = "0.03", terminal_roic: str = "0.12",
                 margin: str = "0.2", sales_to_capital: str = "2",
                 terminal_mode: str | None = None, evidence: bool = True) -> dict:
    case = {
        "drivers": {
            "base_revenue_fact_id": "f-revenue",
            "revenue_growth": growth,
            "operating_margin": [margin] * 3,
            "tax_rate": "0.25",
            "sales_to_capital": [sales_to_capital] * 3,
        },
        "wacc": wacc,
        "terminal_growth": terminal_growth,
        "terminal_roic": terminal_roic,
    }
    if terminal_mode is not None:
        case["terminal_mode"] = terminal_mode
    if evidence:
        case["evidence_fact_ids"] = ["f-revenue"]
    return case


def _driver_scenarios(*, terminal_roic: str = "0.12", tail_growth: str = "0.04",
                      evidence: bool = True) -> dict:
    paths = {
        "conservative": ["0.02", "0.02", "0.03"],
        "neutral": ["0.10", "0.07", tail_growth],
        "optimistic": ["0.18", "0.12", "0.045"],
    }
    return {
        name: {"range": {
            "lower": _driver_case(growth, terminal_roic=terminal_roic, evidence=evidence),
            "upper": _driver_case(
                [str(Decimal(value) + Decimal("0.005")) for value in growth],
                terminal_roic=terminal_roic, evidence=evidence,
            ),
        }}
        for name, growth in paths.items()
    }


def _driver_price(case: dict) -> Decimal:
    """Independent oracle: rebuild the FCFF path and reinvestment-consistent terminal value."""
    drivers = case["drivers"]
    revenue = Decimal("1000000000")
    tax = Decimal(drivers["tax_rate"])
    flows = []
    nopat = Decimal("0")
    for growth, margin, capital in zip(
        drivers["revenue_growth"], drivers["operating_margin"], drivers["sales_to_capital"],
    ):
        previous = revenue
        revenue = previous * (Decimal("1") + Decimal(growth))
        nopat = revenue * Decimal(margin) * (Decimal("1") - tax)
        flows.append(nopat - (revenue - previous) / Decimal(capital))
    wacc = Decimal(case["wacc"])
    growth = Decimal(case["terminal_growth"])
    roic = Decimal(case["terminal_roic"])
    terminal = nopat * (Decimal("1") + growth) * (Decimal("1") - growth / roic) / (wacc - growth)
    enterprise = sum(
        flow / (Decimal("1") + wacc) ** index for index, flow in enumerate(flows, start=1)
    ) + terminal / (Decimal("1") + wacc) ** len(flows)
    equity = enterprise - Decimal("100000000") + Decimal("50000000")
    return (equity / Decimal("100000000")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def _price_method(method_id: str = "multiple-eps-fy") -> dict:    return {
        "method_id": method_id, "family": "price-multiple",
        "direction": "higher-is-more-expensive", "denominator_fact_id": "f-eps",
    }


def _enterprise_method() -> dict:
    return {
        "method_id": "multiple-ebit", "family": "enterprise-multiple",
        "direction": "higher-is-more-expensive", "denominator_fact_id": "f-ebit",
        "diluted_shares_fact_id": "f-shares",
        "bridge_fact_ids": {"debt": "f-debt", "excess_cash": "f-cash"},
    }


def _dcf_method(input_mode: str = "fcff") -> dict:
    return {
        "method_id": "intrinsic-price-per-share-midcycle", "family": "dcf-fcff",
        "direction": "higher-is-more-expensive", "diluted_shares_fact_id": "f-shares",
        "bridge_fact_ids": {"debt": "f-debt", "excess_cash": "f-cash"},
        "input_mode": input_mode, "horizon_years": 3,
    }


def _finite_case(flows: list[str], terminal_value: str, wacc: str = "0.09",
                 evidence: bool = True) -> dict:
    case = {
        "fcff": flows, "wacc": wacc, "terminal_mode": "finite",
        "terminal_value": terminal_value,
    }
    if evidence:
        case["evidence_fact_ids"] = ["f-fcff"]
    return case


def _finite_scenarios(evidence: bool = True) -> dict:
    paths = {
        "conservative": (["180000000", "185000000", "190000000"], "400000000"),
        "neutral": (["190000000", "195000000", "200000000"], "600000000"),
        "optimistic": (["200000000", "205000000", "210000000"], "800000000"),
    }
    return {
        name: {"range": {
            "lower": _finite_case(flows, terminal, evidence=evidence),
            "upper": _finite_case(
                [str(int(value) + 5000000) for value in flows],
                str(int(terminal) + 50000000), evidence=evidence,
            ),
        }}
        for name, (flows, terminal) in paths.items()
    }


def _finite_price(case: dict) -> Decimal:
    """Independent oracle: discounted explicit FCFF plus a finite residual value."""
    wacc = Decimal(case["wacc"])
    flows = [Decimal(value) for value in case["fcff"]]
    enterprise = sum(
        flow / (Decimal("1") + wacc) ** index for index, flow in enumerate(flows, start=1)
    ) + Decimal(case["terminal_value"]) / (Decimal("1") + wacc) ** len(flows)
    equity = enterprise - Decimal("100000000") + Decimal("50000000")
    return (equity / Decimal("100000000")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def _driver_finite_price(case: dict) -> Decimal:
    """Independent oracle: driver-built FCFF plus an explicit finite residual value."""
    drivers = case["drivers"]
    revenue = Decimal("1000000000")
    tax = Decimal(drivers["tax_rate"])
    flows = []
    for growth, margin, capital in zip(
        drivers["revenue_growth"], drivers["operating_margin"], drivers["sales_to_capital"],
    ):
        previous = revenue
        revenue = previous * (Decimal("1") + Decimal(growth))
        nopat = revenue * Decimal(margin) * (Decimal("1") - tax)
        flows.append(nopat - (revenue - previous) / Decimal(capital))
    wacc = Decimal(case["wacc"])
    enterprise = sum(
        flow / (Decimal("1") + wacc) ** index for index, flow in enumerate(flows, start=1)
    ) + Decimal(case["terminal_value"]) / (Decimal("1") + wacc) ** len(flows)
    equity = enterprise - Decimal("100000000") + Decimal("50000000")
    return (equity / Decimal("100000000")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def _driver_finite_scenarios() -> dict:
    paths = {
        "conservative": (["0.02", "0.02", "0.03"], "400000000"),
        "neutral": (["0.10", "0.07", "0.04"], "600000000"),
        "optimistic": (["0.18", "0.12", "0.045"], "800000000"),
    }
    scenarios = {}
    for name, (growth, terminal) in paths.items():
        cases = {}
        for side, offset, terminal_offset in (("lower", "0", "0"), ("upper", "0.005", "50000000")):
            case = _driver_case([str(Decimal(value) + Decimal(offset)) for value in growth])
            case.pop("terminal_growth")
            case.pop("terminal_roic")
            case["terminal_mode"] = "finite"
            case["terminal_value"] = str(int(terminal) + int(terminal_offset))
            cases[side] = case
        scenarios[name] = {"range": cases}
    return scenarios


def _equity_case(flows: list[str], cost_of_equity: str = "0.10",
                 terminal_growth: str = "0.03", evidence: bool = True) -> dict:
    case = {
        "cash_flows": flows, "cost_of_equity": cost_of_equity,
        "terminal_growth": terminal_growth,
    }
    if evidence:
        case["evidence_fact_ids"] = ["f-eps"]
    return case


def _equity_scenarios(evidence: bool = True) -> dict:
    paths = {
        "conservative": ["150000000", "155000000", "160000000"],
        "neutral": ["170000000", "175000000", "180000000"],
        "optimistic": ["190000000", "195000000", "200000000"],
    }
    return {
        name: {"range": {
            "lower": _equity_case(flows, evidence=evidence),
            "upper": _equity_case([str(int(value) + 5000000) for value in flows], evidence=evidence),
        }}
        for name, flows in paths.items()
    }


def _equity_price(case: dict) -> Decimal:
    """Independent oracle: FCFE discounting with a Gordon terminal value, no bridge."""
    cost_of_equity = Decimal(case["cost_of_equity"])
    growth = Decimal(case["terminal_growth"])
    flows = [Decimal(value) for value in case["cash_flows"]]
    equity = sum(
        flow / (Decimal("1") + cost_of_equity) ** index
        for index, flow in enumerate(flows, start=1)
    )
    terminal = flows[-1] * (Decimal("1") + growth) / (cost_of_equity - growth)
    equity += terminal / (Decimal("1") + cost_of_equity) ** len(flows)
    return (equity / Decimal("100000000")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def _equity_dcf_method(cash_flow_type: str = "fcfe") -> dict:
    return {
        "method_id": f"intrinsic-price-per-share-{cash_flow_type}", "family": "dcf-equity",
        "direction": "higher-is-more-expensive", "cash_flow_type": cash_flow_type,
        "diluted_shares_fact_id": "f-shares", "horizon_years": 3,
    }


def _rim_drivers(eps: list[str], dividends: list[str],
                 base_fact_id: str = "f-bvps") -> dict:
    return {
        "base_book_value_per_share_fact_id": base_fact_id,
        "eps": eps, "dividend_per_share": dividends,
    }


def _rim_case(eps: list[str], dividends: list[str], cost_of_equity: str = "0.10",
              terminal_roe: str = "0.14", terminal_growth: str = "0.03",
              evidence: bool = True) -> dict:
    case = {
        "drivers": _rim_drivers(eps, dividends), "cost_of_equity": cost_of_equity,
        "terminal_growth": terminal_growth, "terminal_roe": terminal_roe,
    }
    if evidence:
        case["evidence_fact_ids"] = ["f-bvps"]
    return case


def _rim_scenarios(evidence: bool = True) -> dict:
    paths = {
        "conservative": (["1.6", "1.7", "1.8"], ["0.5", "0.5", "0.5"]),
        "neutral": (["2.0", "2.2", "2.4"], ["0.6", "0.7", "0.8"]),
        "optimistic": (["2.4", "2.6", "2.8"], ["0.7", "0.8", "0.9"]),
    }
    return {
        name: {"range": {
            "lower": _rim_case(eps, dividends, evidence=evidence),
            "upper": _rim_case(
                [str(Decimal(value) + Decimal("0.1")) for value in eps], dividends,
                evidence=evidence,
            ),
        }}
        for name, (eps, dividends) in paths.items()
    }


def _rim_price(case: dict) -> Decimal:
    """Independent oracle: clean-surplus book roll-forward plus discounted residual income."""
    cost_of_equity = Decimal(case["cost_of_equity"])
    growth = Decimal(case["terminal_growth"])
    terminal_roe = Decimal(case["terminal_roe"])
    book = Decimal("10")
    present_value = Decimal("0")
    eps = [Decimal(value) for value in case["drivers"]["eps"]]
    dividends = [Decimal(value) for value in case["drivers"]["dividend_per_share"]]
    for index, (earnings, dividend) in enumerate(zip(eps, dividends), start=1):
        residual_income = earnings - cost_of_equity * book
        present_value += residual_income / (Decimal("1") + cost_of_equity) ** index
        book = book + earnings - dividend
    terminal = (terminal_roe - cost_of_equity) * book / (cost_of_equity - growth)
    present_value += terminal / (Decimal("1") + cost_of_equity) ** len(eps)
    return (Decimal("10") + present_value).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def _rim_method() -> dict:
    return {
        "method_id": "intrinsic-price-per-share-residual-income", "family": "residual-income",
        "direction": "higher-is-more-expensive", "horizon_years": 3,
    }


def _rnpv_case(cash_flows: list[str], probability_of_success: str = "0.40",
               discount_rate: str = "0.12", terminal_value: str = "500000000",
               evidence: bool = True) -> dict:
    case: dict = {
        "cash_flows": cash_flows,
        "probability_of_success": probability_of_success,
        "discount_rate": discount_rate,
        "terminal_value": terminal_value,
    }
    if evidence:
        case["evidence_fact_ids"] = ["f-fcff"]
    return case


def _rnpv_scenarios(evidence: bool = True) -> dict:
    paths = {
        "conservative": (["-20000000", "40000000", "100000000"], "0.30", "0.13", "300000000"),
        "neutral": (["-20000000", "60000000", "140000000"], "0.40", "0.12", "500000000"),
        "optimistic": (["-20000000", "80000000", "180000000"], "0.50", "0.11", "700000000"),
    }
    scenarios = {}
    for name, (flows, probability, rate, terminal) in paths.items():
        scenarios[name] = {"range": {
            "lower": _rnpv_case(flows, probability, rate, terminal, evidence),
            "upper": _rnpv_case(
                [str(Decimal(value) + Decimal("5000000")) for value in flows],
                str(Decimal(probability) + Decimal("0.02")),
                str(Decimal(rate) - Decimal("0.005")),
                str(Decimal(terminal) + Decimal("50000000")), evidence,
            ),
        }}
    return scenarios


def _rnpv_price(case: dict) -> Decimal:
    """Independent oracle: probability-weighted success-case flows plus residual value."""
    rate = Decimal(case["discount_rate"])
    flows = [Decimal(value) for value in case["cash_flows"]]
    gross = sum(
        flow / (Decimal("1") + rate) ** index for index, flow in enumerate(flows, start=1)
    ) + Decimal(case["terminal_value"]) / (Decimal("1") + rate) ** len(flows)
    value = Decimal(case["probability_of_success"]) * gross
    return (value / Decimal("100000000")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def _rnpv_terminal_share(case: dict) -> Decimal:
    rate = Decimal(case["discount_rate"])
    flows = [Decimal(value) for value in case["cash_flows"]]
    present_value = sum(
        flow / (Decimal("1") + rate) ** index for index, flow in enumerate(flows, start=1)
    )
    discounted_terminal = Decimal(case["terminal_value"]) / (Decimal("1") + rate) ** len(flows)
    return ((discounted_terminal / (present_value + discounted_terminal))
            .quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))


def _rnpv_method() -> dict:
    return {
        "method_id": "intrinsic-price-per-share-rnpv", "family": "rnpv",
        "direction": "higher-is-more-expensive", "diluted_shares_fact_id": "f-shares",
        "horizon_years": 3,
    }


def _ev_case(adjusted_net_worth: str, value_of_in_force: str, new_business_value: str,
             new_business_multiple: str, evidence: bool = True) -> dict:
    case: dict = {
        "adjusted_net_worth": adjusted_net_worth,
        "value_of_in_force": value_of_in_force,
        "new_business_value": new_business_value,
        "new_business_multiple": new_business_multiple,
    }
    if evidence:
        case["evidence_fact_ids"] = ["f-bvps"]
    return case


def _ev_scenarios(evidence: bool = True) -> dict:
    paths = {
        "conservative": ("2000000000", "1000000000", "100000000", "5"),
        "neutral": ("2000000000", "1500000000", "150000000", "10"),
        "optimistic": ("2000000000", "2000000000", "200000000", "15"),
    }
    scenarios = {}
    for name, (net_worth, in_force, new_business, multiple) in paths.items():
        scenarios[name] = {"range": {
            "lower": _ev_case(net_worth, in_force, new_business, multiple, evidence),
            "upper": _ev_case(
                str(Decimal(net_worth) + Decimal("50000000")),
                str(Decimal(in_force) + Decimal("100000000")),
                str(Decimal(new_business) + Decimal("10000000")),
                str(Decimal(multiple) + Decimal("1")), evidence,
            ),
        }}
    return scenarios


def _ev_price(case: dict) -> Decimal:
    """Independent oracle: appraisal value = ANW + VIF + NBV x multiple, per share."""
    total = (
        Decimal(case["adjusted_net_worth"])
        + Decimal(case["value_of_in_force"])
        + Decimal(case["new_business_value"]) * Decimal(case["new_business_multiple"])
    )
    return (total / Decimal("100000000")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def _ev_method() -> dict:
    return {
        "method_id": "intrinsic-price-per-share-embedded-value", "family": "embedded-value",
        "direction": "higher-is-more-expensive", "diluted_shares_fact_id": "f-shares",
    }


def _input(methods: list[dict], *, eps_fact_type: str = "disclosed",
           eps_status: str = "verified", price: str = "30") -> dict:
    data = {
        "schema_version": vc.INPUT_SCHEMA,
        "fact_snapshot_id": "snap-1",
        "market_snapshot_id": "market-1",
        "model_version": "test-model",
        "calculator_version": vc.CALCULATOR_VERSION,
        "method_catalog_version": vc.CATALOG_VERSION,
        "valuation_input_hash": "pending",
        "facts": _facts(eps_fact_type, eps_status),
        "market": {
            "valuation_currency": "CNY",
            "current_price": {
                "value": price, "currency": "CNY", "unit": "CNY/share",
                "date": "2026-10-28",
            },
        },
        "methods": methods,
    }
    data["valuation_input_hash"] = vc.valuation_input_hash(data)
    return data


def _sensitivity(method: dict, base_case: dict | None = None) -> dict:
    if method["family"] == "dcf-fcff" and base_case and "terminal_value" in base_case:
        return {
            "row_parameter": "terminal_value", "row_values": ["400000000", "600000000", "800000000"],
            "column_parameter": "wacc", "column_values": ["0.08", "0.09", "0.10"],
            "base_case": copy.deepcopy(base_case),
        }
    if method["family"] == "dcf-fcff" and method["input_mode"] == "drivers":
        return {
            "row_parameter": "revenue_growth_shift", "row_values": ["-0.02", "0", "0.02"],
            "column_parameter": "wacc", "column_values": ["0.08", "0.09", "0.10"],
            "base_case": copy.deepcopy(base_case) if base_case else _driver_case(["0.10", "0.07", "0.04"]),
        }
    if method["family"] == "dcf-fcff":
        return {
            "row_parameter": "wacc", "row_values": ["0.08", "0.09", "0.10"],
            "column_parameter": "terminal_growth", "column_values": ["0.02", "0.03", "0.04"],
            "base_case": copy.deepcopy(base_case) if base_case else _dcf_case(["195000000", "200000000", "205000000"]),
        }
    if method["family"] == "dcf-equity":
        return {
            "row_parameter": "cash_flow_shift", "row_values": ["-5000000", "0", "5000000"],
            "column_parameter": "cost_of_equity", "column_values": ["0.09", "0.10", "0.11"],
            "base_case": copy.deepcopy(base_case) if base_case else _equity_case(["170000000", "175000000", "180000000"]),
        }
    if method["family"] == "residual-income":
        return {
            "row_parameter": "eps_shift", "row_values": ["-0.1", "0", "0.1"],
            "column_parameter": "cost_of_equity", "column_values": ["0.09", "0.10", "0.11"],
            "base_case": copy.deepcopy(base_case) if base_case else _rim_case(["2.0", "2.2", "2.4"], ["0.6", "0.7", "0.8"]),
        }
    if method["family"] == "rnpv":
        return {
            "row_parameter": "cash_flow_shift", "row_values": ["-10000000", "0", "10000000"],
            "column_parameter": "discount_rate", "column_values": ["0.11", "0.12", "0.13"],
            "base_case": copy.deepcopy(base_case) if base_case else _rnpv_case(
                ["-20000000", "60000000", "140000000"]),
        }
    if method["family"] == "embedded-value":
        return {
            "row_parameter": "value_of_in_force_shift",
            "row_values": ["-100000000", "0", "100000000"],
            "column_parameter": "new_business_multiple", "column_values": ["5", "10", "15"],
            "base_case": copy.deepcopy(base_case) if base_case else _ev_case(
                "2000000000", "1500000000", "150000000", "10"),
        }
    return {
        "row_parameter": "denominator", "row_values": ["1.8", "2", "2.2"],
        "column_parameter": "multiple", "column_values": ["12", "15", "18"],
    }


def _card(data: dict, scenarios: dict[str, dict], *, primary: str, cross: tuple[str, ...] = (),
          fallback: bool = False) -> dict:
    parameters = []
    for method in data["methods"]:
        method_id = method["method_id"]
        proposal = copy.deepcopy(method)
        proposal["scenarios"] = copy.deepcopy(scenarios[method_id])
        neutral_case = scenarios[method_id]["neutral"]["range"]["lower"]
        base_case = None
        if method["family"] in {"dcf-equity", "residual-income", "rnpv", "embedded-value"}:
            base_case = copy.deepcopy(neutral_case)
        elif method["family"] == "dcf-fcff" and neutral_case.get("terminal_mode") == "finite":
            base_case = copy.deepcopy(neutral_case)
        proposal["sensitivity"] = _sensitivity(method, base_case)
        parameters.append({"method_id": method_id, "method": proposal})
    judgments = []
    for method in data["methods"]:
        method_id = method["method_id"]
        if fallback:
            role = "cross-check"
        elif method_id == primary:
            role = "primary"
        elif method_id in cross:
            role = "cross-check"
        else:
            role = "cross-check"
        judgments.append({
            "method_id": method_id, "applicable": True, "preferred_role": role,
            "evidence_fact_ids": ["f-shares"], "rationale": "方法判断",
            "disable_conditions": [],
        })
    return {
        "schema_version": vc.CARD_SCHEMA,
        "reviewer_id": "reviewer-1",
        "fact_snapshot_id": data["fact_snapshot_id"],
        "market_snapshot_id": data["market_snapshot_id"],
        "valuation_input_hash": data["valuation_input_hash"],
        "model_id": data["model_version"],
        "calculator_version": data["calculator_version"],
        "method_catalog_version": data["method_catalog_version"],
        "method_judgments": judgments,
        "normalizations": [],
        "scenario_parameters": parameters,
        "calibrations": [{
            "method_id": method["method_id"],
            "historical": {"lower": "10", "upper": "20"},
            "peers": {"lower": "11", "upper": "21"},
            "evidence_fact_ids": ["f-shares"], "rationale": "历史与同业",
        } for method in data["methods"]],
        "reverse_valuation": [{
            "method_id": method["method_id"],
            "fixed_parameters": [{"parameter": "wacc", "value": "0.09", "unit": "fraction"}],
            "implied_variable": {"name": "revenue_growth", "value": "0.05", "unit": "fraction"},
            "implied_horizon_years": "5",
            "feasibility": {
                "history_comparison": "历史增速 4%",
                "capacity_constraint": "产能可支撑",
                "market_size": "市场空间充足",
                "verdict": "plausible",
            },
            "evidence_fact_ids": ["f-shares"],
            "invalidation_condition": "条件",
        } for method in data["methods"]],
        "parameter_derivation": [{
            "method_id": method["method_id"], "parameter": "wacc", "value": "0.09",
            "formula": "rf + beta * erp",
            "inputs": {"rf": "0.03", "beta": "1.0", "erp": "0.06"},
            "evidence_fact_ids": ["f-shares"],
        } for method in data["methods"]],
        "sensitivity_factors": [{
            "method_id": method["method_id"], "factor": "multiple",
            "reason": "主要变量", "evidence_fact_ids": ["f-shares"],
        } for method in data["methods"]],
        "invalidation_conditions": [{
            "method_id": method["method_id"], "code": "c1", "condition": "条件",
            "evidence_fact_ids": ["f-shares"],
        } for method in data["methods"]],
    }


def _critique(data: dict) -> dict:
    return {
        "schema_version": vc.CRITIQUE_SCHEMA,
        "valuation_input_hash": data["valuation_input_hash"],
        "critic_id": "critic-1",
        "target_card": "reviewer-1",
        "items": [],
    }


def _aggregate(data: dict, scenarios: dict[str, dict], *, primary: str,
               cross: tuple[str, ...] = (), fallback: bool = False) -> dict:
    card = _card(data, scenarios, primary=primary, cross=cross, fallback=fallback)
    consensus = vc.aggregate_reviewer_card(data, card, _critique(data))
    return consensus | {"_calculation": vc._calculate(data, consensus)}


class ScenarioDecouplingTest(unittest.TestCase):
    """T1–T3：情景只需有序，允许间隔与重叠，锚点乱序拒绝。"""

    def test_gapped_scenarios_pass_with_layout(self):
        data = _input([_price_method()])
        scenarios = {"multiple-eps-fy": {
            "conservative": {"denominator": "2", "range": {"lower": "10", "upper": "12"}},
            "neutral": {"denominator": "2", "range": {"lower": "13", "upper": "17"}},
            "optimistic": {"denominator": "2", "range": {"lower": "18", "upper": "21"}},
        }}
        result = _aggregate(data, scenarios, primary="multiple-eps-fy")
        layout = result["_calculation"]["methods"][0]["scenario_layout"]
        self.assertEqual([item["type"] for item in layout], ["gap", "gap"])
        self.assertEqual(result["publication_precision_state"], "supported")

    def test_overlapping_scenarios_pass_with_layout(self):
        data = _input([_price_method()])
        scenarios = {"multiple-eps-fy": {
            "conservative": {"denominator": "2", "range": {"lower": "10", "upper": "16"}},
            "neutral": {"denominator": "2", "range": {"lower": "14", "upper": "20"}},
            "optimistic": {"denominator": "2", "range": {"lower": "18", "upper": "24"}},
        }}
        result = _aggregate(data, scenarios, primary="multiple-eps-fy")
        layout = result["_calculation"]["methods"][0]["scenario_layout"]
        self.assertEqual([item["type"] for item in layout], ["overlap", "overlap"])

    def test_misordered_anchors_rejected(self):
        data = _input([_price_method()])
        scenarios = {"multiple-eps-fy": {
            "conservative": {"denominator": "2", "range": {"lower": "20", "upper": "22"}},
            "neutral": {"denominator": "2", "range": {"lower": "10", "upper": "12"}},
            "optimistic": {"denominator": "2", "range": {"lower": "13", "upper": "14"}},
        }}
        with self.assertRaises(vc.ValuationConsensusError):
            _aggregate(data, scenarios, primary="multiple-eps-fy")


class ClassificationTest(unittest.TestCase):
    """T4：四个外侧锚点决定五档，情景归属独立输出。"""

    def test_five_band_thresholds_and_membership(self):
        data = _input([_price_method()])
        result = _aggregate(data, {"multiple-eps-fy": _price_scenarios()},
                            primary="multiple-eps-fy")
        primary = result["_calculation"]["primary"]
        self.assertEqual(primary["thresholds"], ["10.000000", "13.000000", "17.000000", "21.000000"])
        self.assertEqual(primary["current_position"], "neutral-zone")
        self.assertEqual(primary["scenario_membership"], ["neutral"])
        self.assertEqual(
            [band["position"] for band in primary["bands"]],
            ["below-conservative", "conservative-zone", "neutral-zone",
             "optimistic-zone", "above-optimistic"],
        )

    def test_enterprise_membership_reports_overlap(self):
        data = _input([_price_method()])
        scenarios = {"multiple-eps-fy": {
            "conservative": {"denominator": "2", "range": {"lower": "10", "upper": "16"}},
            "neutral": {"denominator": "2", "range": {"lower": "14", "upper": "20"}},
            "optimistic": {"denominator": "2", "range": {"lower": "18", "upper": "24"}},
        }}
        result = _aggregate(data, scenarios, primary="multiple-eps-fy")
        membership = result["_calculation"]["primary"]["scenario_membership"]
        self.assertEqual(set(membership), {"conservative", "neutral"})


class BasisPairingTest(unittest.TestCase):
    """T5：method_id 的 basis token 必须与方法族口径配对。"""

    def test_enterprise_basis_on_price_family_rejected(self):
        method = _price_method()
        method["method_id"] = "multiple-ebit"
        data = _input([method])
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.validate_valuation_input(data)
        self.assertIn("not allowed for family price-multiple", str(caught.exception))

    def test_missing_basis_rejected(self):
        method = _price_method()
        method["method_id"] = "multiple-ttm"
        data = _input([method])
        with self.assertRaises(vc.ValuationConsensusError):
            vc.validate_valuation_input(data)

    def test_dcf_rejects_basis_token(self):
        method = _dcf_method()
        method["method_id"] = "intrinsic-price-per-share-fcf"
        data = _input([method])
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.validate_valuation_input(data)
        self.assertIn("must not carry a basis token", str(caught.exception))


class PrecisionStateTest(unittest.TestCase):
    """T6–T9：精度三态、终值占比、独立性、回退与分歧。"""

    def test_supported_requires_no_reasons(self):
        result = _aggregate(_input([_price_method()]), {"multiple-eps-fy": _price_scenarios()},
                            primary="multiple-eps-fy")
        self.assertEqual(result["status"], "consensus")
        self.assertEqual(result["publication_precision_state"], "supported")
        self.assertEqual(result["precision_reasons"], [])

    def test_terminal_value_share_caps_at_conditional(self):
        data = _input([_dcf_method()])
        result = _aggregate(data, {"intrinsic-price-per-share-midcycle": _dcf_scenarios()},
                            primary="intrinsic-price-per-share-midcycle")
        share = result["_calculation"]["methods"][0]["terminal_value_share"]
        self.assertGreaterEqual(float(share["upper"]), 0.85)
        self.assertEqual(result["publication_precision_state"], "conditional")
        self.assertIn("terminal-value-share", {item["code"] for item in result["precision_reasons"]})

    def test_unbound_dcf_evidence_caps_at_conditional(self):
        data = _input([_dcf_method()])
        result = _aggregate(
            data, {"intrinsic-price-per-share-midcycle": _dcf_scenarios(evidence=False)},
            primary="intrinsic-price-per-share-midcycle",
        )
        self.assertEqual(result["publication_precision_state"], "conditional")
        self.assertIn("unbound-scenario-evidence", {item["code"] for item in result["precision_reasons"]})

    def test_primary_fallback_is_low_confidence(self):
        result = _aggregate(
            _input([_price_method()]), {"multiple-eps-fy": _price_scenarios()},
            primary="multiple-eps-fy", fallback=True,
        )
        self.assertEqual(result["status"], "low-confidence-consensus")
        self.assertEqual(result["publication_precision_state"], "low-confidence")
        self.assertIn("primary-role-fallback", {item["code"] for item in result["precision_reasons"]})

    def test_non_independent_cross_check_caps_at_conditional(self):
        data = _input([_price_method(), _enterprise_method()])
        scenarios = {
            "multiple-eps-fy": _price_scenarios(),
            "multiple-ebit": _enterprise_scenarios(),
        }
        result = _aggregate(data, scenarios, primary="multiple-eps-fy",
                            cross=("multiple-ebit",))
        self.assertEqual(result["independence"]["state"], "non-independent")
        self.assertEqual(result["publication_precision_state"], "conditional")

    def test_material_divergence_caps_at_conditional(self):
        data = _input([_price_method(), _enterprise_method()], price="30")
        scenarios = {
            "multiple-eps-fy": _price_scenarios(),
            "multiple-ebit": {
                "conservative": {"denominator": "100000000", "range": {"lower": "40", "upper": "45"}},
                "neutral": {"denominator": "100000000", "range": {"lower": "50", "upper": "55"}},
                "optimistic": {"denominator": "100000000", "range": {"lower": "56", "upper": "60"}},
            },
        }
        result = _aggregate(data, scenarios, primary="multiple-eps-fy",
                            cross=("multiple-ebit",))
        self.assertTrue(result["cross_check_divergence"]["is_material"])
        self.assertIn("cross-check-divergence", {item["code"] for item in result["precision_reasons"]})

    def test_direction_conflict_is_low_confidence(self):
        data = _input([_price_method(), _enterprise_method()], price="30")
        scenarios = {
            "multiple-eps-fy": {
                "conservative": {"denominator": "2", "range": {"lower": "4", "upper": "5"}},
                "neutral": {"denominator": "2", "range": {"lower": "5", "upper": "6"}},
                "optimistic": {"denominator": "2", "range": {"lower": "6", "upper": "7"}},
            },
            "multiple-ebit": {
                "conservative": {"denominator": "100000000", "range": {"lower": "40", "upper": "42"}},
                "neutral": {"denominator": "100000000", "range": {"lower": "43", "upper": "45"}},
                "optimistic": {"denominator": "100000000", "range": {"lower": "46", "upper": "48"}},
            },
        }
        result = _aggregate(data, scenarios, primary="multiple-eps-fy",
                            cross=("multiple-ebit",))
        self.assertTrue(result["cross_check_divergence"]["direction_conflict"])
        self.assertEqual(result["publication_precision_state"], "low-confidence")

    def test_assumption_input_caps_at_conditional(self):
        data = _input([_price_method()], eps_fact_type="assumption", eps_status="unverified")
        result = _aggregate(data, {"multiple-eps-fy": _price_scenarios()},
                            primary="multiple-eps-fy")
        self.assertEqual(result["publication_precision_state"], "conditional")
        self.assertIn("assumption-input", {item["code"] for item in result["precision_reasons"]})


class DcfDriversTest(unittest.TestCase):
    """T17–T23：DCF 驱动模式、终值模式、经济一致性与推导链契约。"""

    METHOD = "intrinsic-price-per-share-midcycle"

    def _drivers_aggregate(self, scenarios: dict | None = None) -> dict:
        data = _input([_dcf_method("drivers")])
        return _aggregate(data, {self.METHOD: scenarios or _driver_scenarios()},
                          primary=self.METHOD)

    def test_driver_path_matches_manual_recompute(self):
        result = self._drivers_aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        for scenario in ("conservative", "neutral", "optimistic"):
            cases = _driver_scenarios()[scenario]["range"]
            actual = next(
                item for item in method["scenarios"] if item["scenario"] == scenario
            )["price_range"]
            self.assertEqual(actual["lower"], str(_driver_price(cases["lower"])))
            self.assertEqual(actual["upper"], str(_driver_price(cases["upper"])))

    def test_horizon_mismatch_rejected(self):
        scenarios = _driver_scenarios()
        scenarios["neutral"]["range"]["lower"]["drivers"]["revenue_growth"] = ["0.1", "0.07"]
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            self._drivers_aggregate(scenarios)
        self.assertIn("revenue_growth length must equal horizon_years", str(caught.exception))

    def test_fcff_mode_requires_terminal_nopat_for_reinvestment_consistent(self):
        scenarios = _dcf_scenarios()
        for scenario in scenarios.values():
            for side in ("lower", "upper"):
                scenario["range"][side].pop("terminal_mode")
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            _aggregate(_input([_dcf_method()]), {self.METHOD: scenarios}, primary=self.METHOD)
        self.assertIn("terminal_nopat", str(caught.exception))

    def test_driver_sensitivity_requires_operating_shift(self):
        data = _input([_dcf_method("drivers")])
        card = _card(data, {self.METHOD: _driver_scenarios()}, primary=self.METHOD)
        proposal = card["scenario_parameters"][0]["method"]["sensitivity"]
        proposal["row_parameter"] = "wacc"
        proposal["column_parameter"] = "terminal_growth"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.aggregate_reviewer_card(data, card, _critique(data))
        self.assertIn("operating driver shift", str(caught.exception))

    def test_driver_sensitivity_shift_recomputes_full_path(self):
        result = self._drivers_aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        base = _sensitivity(_dcf_method("drivers"))["base_case"]
        self.assertEqual(method["sensitivity"]["prices"][1][1], str(_driver_price(base)))
        shifted = copy.deepcopy(base)
        shifted["drivers"]["revenue_growth"] = [
            str(Decimal(value) + Decimal("0.02")) for value in base["drivers"]["revenue_growth"]
        ]
        self.assertEqual(method["sensitivity"]["prices"][2][1], str(_driver_price(shifted)))

    def test_terminal_roic_below_wacc_caps_at_conditional(self):
        result = self._drivers_aggregate(_driver_scenarios(terminal_roic="0.08"))
        self.assertEqual(result["publication_precision_state"], "conditional")
        self.assertIn("economic-inconsistency", {item["code"] for item in result["precision_reasons"]})

    def test_growth_not_converged_caps_at_conditional(self):
        result = self._drivers_aggregate(_driver_scenarios(tail_growth="0.10"))
        self.assertEqual(result["publication_precision_state"], "conditional")
        self.assertIn("economic-inconsistency", {item["code"] for item in result["precision_reasons"]})

    def test_driver_base_revenue_assumption_caps_at_conditional(self):
        data = _input([_dcf_method("drivers")])
        for fact in data["facts"]:
            if fact["fact_id"] == "f-revenue":
                fact["fact_type"] = "assumption"
                fact["status"] = "unverified"
                fact["audit_status"] = "not-applicable"
        data["valuation_input_hash"] = vc.valuation_input_hash(data)
        card = _card(data, {self.METHOD: _driver_scenarios(evidence=False)}, primary=self.METHOD)
        card["scenario_parameters"][0]["method"]["sensitivity"]["base_case"].pop("evidence_fact_ids")
        result = vc.aggregate_reviewer_card(data, card, _critique(data))
        self.assertEqual(result["publication_precision_state"], "conditional")
        self.assertIn("assumption-input", {item["code"] for item in result["precision_reasons"]})

    def test_horizon_years_must_be_positive(self):
        method = _dcf_method()
        method["horizon_years"] = 0
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.validate_valuation_input(_input([method]))
        self.assertIn("horizon_years", str(caught.exception))


class FiniteDcfTest(unittest.TestCase):
    """T26–T29：有限期 DCF 的残值、缺值拒绝与固定敏感性参数对。"""

    METHOD = "intrinsic-price-per-share-midcycle"

    def _aggregate(self, scenarios: dict | None = None) -> dict:
        data = _input([_dcf_method()])
        return _aggregate(data, {self.METHOD: scenarios or _finite_scenarios()},
                          primary=self.METHOD)

    def test_finite_terminal_value_matches_oracle(self):
        result = self._aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        for scenario in ("conservative", "neutral", "optimistic"):
            cases = _finite_scenarios()[scenario]["range"]
            actual = next(
                item for item in method["scenarios"] if item["scenario"] == scenario
            )["price_range"]
            self.assertEqual(actual["lower"], str(_finite_price(cases["lower"])))
            self.assertEqual(actual["upper"], str(_finite_price(cases["upper"])))

    def test_finite_requires_terminal_value(self):
        scenarios = _finite_scenarios()
        for scenario in scenarios.values():
            for side in ("lower", "upper"):
                scenario["range"][side].pop("terminal_value")
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            self._aggregate(scenarios)
        self.assertIn("terminal_value", str(caught.exception))

    def test_finite_terminal_value_may_be_zero(self):
        scenarios = _finite_scenarios()
        for side in ("lower", "upper"):
            scenarios["conservative"]["range"][side]["terminal_value"] = "0"
        result = self._aggregate(scenarios)
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        conservative = next(
            item for item in method["scenarios"] if item["scenario"] == "conservative"
        )["price_range"]
        self.assertEqual(conservative["lower"], str(_finite_price(
            scenarios["conservative"]["range"]["lower"])))

    def test_finite_with_drivers_uses_explicit_residual_value(self):
        data = _input([_dcf_method("drivers")])
        scenarios = _driver_finite_scenarios()
        result = _aggregate(data, {self.METHOD: scenarios}, primary=self.METHOD)
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        for scenario in ("conservative", "neutral", "optimistic"):
            actual = next(
                item for item in method["scenarios"] if item["scenario"] == scenario
            )["price_range"]
            self.assertEqual(actual["lower"], str(_driver_finite_price(
                scenarios[scenario]["range"]["lower"])))
            self.assertEqual(actual["upper"], str(_driver_finite_price(
                scenarios[scenario]["range"]["upper"])))

    def test_finite_sensitivity_requires_terminal_value_and_wacc(self):
        data = _input([_dcf_method()])
        card = _card(data, {self.METHOD: _finite_scenarios()}, primary=self.METHOD)
        sensitivity = card["scenario_parameters"][0]["method"]["sensitivity"]
        sensitivity["column_parameter"] = "terminal_growth"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.aggregate_reviewer_card(data, card, _critique(data))
        self.assertIn("terminal_value, wacc", str(caught.exception))


class EquityDcfTest(unittest.TestCase):
    """T30–T33：股权 DCF 的每股价复算、口径配对与敏感性经营参数。"""

    METHOD = "intrinsic-price-per-share-fcfe"

    def _aggregate(self, scenarios: dict | None = None, method: dict | None = None) -> dict:
        method = method or _equity_dcf_method()
        data = _input([method])
        return _aggregate(data, {method["method_id"]: scenarios or _equity_scenarios()},
                          primary=method["method_id"])

    def test_equity_price_matches_oracle(self):
        result = self._aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        for scenario in ("conservative", "neutral", "optimistic"):
            cases = _equity_scenarios()[scenario]["range"]
            actual = next(
                item for item in method["scenarios"] if item["scenario"] == scenario
            )["price_range"]
            self.assertEqual(actual["lower"], str(_equity_price(cases["lower"])))
            self.assertEqual(actual["upper"], str(_equity_price(cases["upper"])))

    def test_dividend_cash_flows_must_not_be_negative(self):
        method = _equity_dcf_method("dividend")
        scenarios = _equity_scenarios()
        scenarios["neutral"]["range"]["lower"]["cash_flows"][0] = "-1000000"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            self._aggregate(scenarios, method)
        self.assertIn("must not be negative", str(caught.exception))

    def test_method_basis_must_equal_cash_flow_type(self):
        method = _equity_dcf_method("dividend")
        method["method_id"] = "intrinsic-price-per-share-fcfe"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.validate_valuation_input(_input([method]))
        self.assertIn("basis must equal cash_flow_type", str(caught.exception))

    def test_sensitivity_requires_cash_flow_shift(self):
        data = _input([_equity_dcf_method()])
        card = _card(data, {self.METHOD: _equity_scenarios()}, primary=self.METHOD)
        sensitivity = card["scenario_parameters"][0]["method"]["sensitivity"]
        sensitivity["row_parameter"] = "cost_of_equity"
        sensitivity["column_parameter"] = "terminal_growth"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.aggregate_reviewer_card(data, card, _critique(data))
        self.assertIn("cash flow shift", str(caught.exception))

    def test_sensitivity_shift_matches_oracle(self):
        result = self._aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        base = _equity_case(["170000000", "175000000", "180000000"])
        self.assertEqual(method["sensitivity"]["prices"][1][1], str(_equity_price(base)))
        shifted = copy.deepcopy(base)
        shifted["cash_flows"] = [
            str(Decimal(value) + Decimal("5000000")) for value in base["cash_flows"]
        ]
        self.assertEqual(method["sensitivity"]["prices"][2][1], str(_equity_price(shifted)))


class ResidualIncomeTest(unittest.TestCase):
    """T34–T38：剩余收益模型的账面滚动、经济一致性与敏感性经营参数。"""

    METHOD = "intrinsic-price-per-share-residual-income"

    def _aggregate(self, scenarios: dict | None = None) -> dict:
        data = _input([_rim_method()])
        return _aggregate(data, {self.METHOD: scenarios or _rim_scenarios()},
                          primary=self.METHOD)

    def test_residual_income_price_matches_oracle(self):
        result = self._aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        for scenario in ("conservative", "neutral", "optimistic"):
            cases = _rim_scenarios()[scenario]["range"]
            actual = next(
                item for item in method["scenarios"] if item["scenario"] == scenario
            )["price_range"]
            self.assertEqual(actual["lower"], str(_rim_price(cases["lower"])))
            self.assertEqual(actual["upper"], str(_rim_price(cases["upper"])))

    def test_terminal_roe_below_cost_of_equity_caps_at_conditional(self):
        scenarios = _rim_scenarios()
        for scenario in scenarios.values():
            for side in ("lower", "upper"):
                scenario["range"][side]["terminal_roe"] = "0.08"
        result = self._aggregate(scenarios)
        self.assertEqual(result["publication_precision_state"], "conditional")
        self.assertIn("economic-inconsistency", {item["code"] for item in result["precision_reasons"]})

    def test_book_value_must_stay_positive(self):
        scenarios = _rim_scenarios()
        for side in ("lower", "upper"):
            scenarios["neutral"]["range"][side]["drivers"]["eps"] = ["-20", "-20", "-20"]
            scenarios["neutral"]["range"][side]["drivers"]["dividend_per_share"] = ["0", "0", "0"]
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            self._aggregate(scenarios)
        self.assertIn("book value per share must stay positive", str(caught.exception))

    def test_dividend_per_share_must_not_be_negative(self):
        scenarios = _rim_scenarios()
        scenarios["neutral"]["range"]["lower"]["drivers"]["dividend_per_share"][0] = "-0.5"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            self._aggregate(scenarios)
        self.assertIn("must not be negative", str(caught.exception))

    def test_base_book_value_assumption_caps_at_conditional(self):
        data = _input([_rim_method()])
        for fact in data["facts"]:
            if fact["fact_id"] == "f-bvps":
                fact["fact_type"] = "assumption"
                fact["status"] = "unverified"
                fact["audit_status"] = "not-applicable"
        data["valuation_input_hash"] = vc.valuation_input_hash(data)
        scenarios = _rim_scenarios(evidence=False)
        card = _card(data, {self.METHOD: scenarios}, primary=self.METHOD)
        card["scenario_parameters"][0]["method"]["sensitivity"]["base_case"].pop("evidence_fact_ids", None)
        result = vc.aggregate_reviewer_card(data, card, _critique(data))
        self.assertEqual(result["publication_precision_state"], "conditional")
        self.assertIn("assumption-input", {item["code"] for item in result["precision_reasons"]})

    def test_sensitivity_requires_operating_parameter(self):
        data = _input([_rim_method()])
        card = _card(data, {self.METHOD: _rim_scenarios()}, primary=self.METHOD)
        sensitivity = card["scenario_parameters"][0]["method"]["sensitivity"]
        sensitivity["row_parameter"] = "cost_of_equity"
        sensitivity["column_parameter"] = "terminal_growth"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.aggregate_reviewer_card(data, card, _critique(data))
        self.assertIn("operating parameter", str(caught.exception))


class RnpvTest(unittest.TestCase):
    """T42–T45：rNPV 的概率加权、风险只计一次与敏感性经营参数。"""

    METHOD = "intrinsic-price-per-share-rnpv"

    def _aggregate(self, scenarios: dict | None = None) -> dict:
        data = _input([_rnpv_method()])
        return _aggregate(data, {self.METHOD: scenarios or _rnpv_scenarios()}, primary=self.METHOD)

    def test_rnpv_matches_oracle(self):
        result = self._aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        for scenario in ("conservative", "neutral", "optimistic"):
            cases = _rnpv_scenarios()[scenario]["range"]
            actual = next(
                item for item in method["scenarios"] if item["scenario"] == scenario
            )["price_range"]
            self.assertEqual(actual["lower"], str(_rnpv_price(cases["lower"])))
            self.assertEqual(actual["upper"], str(_rnpv_price(cases["upper"])))

    def test_terminal_value_share_matches_oracle(self):
        result = self._aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        expected = _rnpv_terminal_share(_rnpv_scenarios()["neutral"]["range"]["lower"])
        self.assertEqual(method["terminal_value_share"]["lower"], str(expected))

    def test_probability_must_be_in_unit_interval(self):
        scenarios = _rnpv_scenarios()
        for side in ("lower", "upper"):
            scenarios["neutral"]["range"][side]["probability_of_success"] = "0"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            self._aggregate(scenarios)
        self.assertIn("probability_of_success", str(caught.exception))

    def test_sensitivity_requires_operating_parameter(self):
        data = _input([_rnpv_method()])
        card = _card(data, {self.METHOD: _rnpv_scenarios()}, primary=self.METHOD)
        sensitivity = card["scenario_parameters"][0]["method"]["sensitivity"]
        sensitivity["row_parameter"] = "discount_rate"
        sensitivity["column_parameter"] = "terminal_value"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.aggregate_reviewer_card(data, card, _critique(data))
        self.assertIn("operating parameter", str(caught.exception))

    def test_cash_flow_shift_recomputes_full_path(self):
        result = self._aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        base_case = copy.deepcopy(_rnpv_scenarios()["neutral"]["range"]["lower"])
        center = method["sensitivity"]["prices"][1][1]
        self.assertEqual(center, str(_rnpv_price(base_case)))
        adjusted = copy.deepcopy(base_case)
        adjusted["cash_flows"] = [
            str(Decimal(value) - Decimal("10000000")) for value in adjusted["cash_flows"]
        ]
        adjusted["discount_rate"] = "0.11"
        self.assertEqual(method["sensitivity"]["prices"][0][0], str(_rnpv_price(adjusted)))


class EmbeddedValueTest(unittest.TestCase):
    """T46–T49：寿险内含价值、新业务价值倍数与敏感性经营参数。"""

    METHOD = "intrinsic-price-per-share-embedded-value"

    def _aggregate(self, scenarios: dict | None = None) -> dict:
        data = _input([_ev_method()])
        return _aggregate(data, {self.METHOD: scenarios or _ev_scenarios()}, primary=self.METHOD)

    def test_embedded_value_matches_oracle(self):
        result = self._aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        for scenario in ("conservative", "neutral", "optimistic"):
            cases = _ev_scenarios()[scenario]["range"]
            actual = next(
                item for item in method["scenarios"] if item["scenario"] == scenario
            )["price_range"]
            self.assertEqual(actual["lower"], str(_ev_price(cases["lower"])))
            self.assertEqual(actual["upper"], str(_ev_price(cases["upper"])))

    def test_negative_multiple_rejected(self):
        scenarios = _ev_scenarios()
        for side in ("lower", "upper"):
            scenarios["neutral"]["range"][side]["new_business_multiple"] = "-1"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            self._aggregate(scenarios)
        self.assertIn("new_business_multiple must not be negative", str(caught.exception))

    def test_nonpositive_appraisal_value_rejected(self):
        scenarios = _ev_scenarios()
        for side in ("lower", "upper"):
            case = scenarios["conservative"]["range"][side]
            case["adjusted_net_worth"] = "0"
            case["value_of_in_force"] = "-100000000"
            case["new_business_value"] = "0"
            case["new_business_multiple"] = "0"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            self._aggregate(scenarios)
        self.assertIn("appraisal value must be positive", str(caught.exception))

    def test_sensitivity_requires_operating_parameter(self):
        data = _input([_ev_method()])
        card = _card(data, {self.METHOD: _ev_scenarios()}, primary=self.METHOD)
        sensitivity = card["scenario_parameters"][0]["method"]["sensitivity"]
        sensitivity["row_parameter"] = "new_business_multiple"
        sensitivity["column_parameter"] = "adjusted_net_worth_shift"
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.aggregate_reviewer_card(data, card, _critique(data))
        self.assertIn("operating parameter", str(caught.exception))

    def test_vif_shift_recomputes_appraisal_value(self):
        result = self._aggregate()
        method = next(
            item for item in result["_calculation"]["methods"] if item["method_id"] == self.METHOD
        )
        base_case = copy.deepcopy(_ev_scenarios()["neutral"]["range"]["lower"])
        self.assertEqual(method["sensitivity"]["prices"][1][1], str(_ev_price(base_case)))
        adjusted = copy.deepcopy(base_case)
        adjusted["value_of_in_force"] = str(
            Decimal(adjusted["value_of_in_force"]) - Decimal("100000000")
        )
        adjusted["new_business_multiple"] = "5"
        self.assertEqual(method["sensitivity"]["prices"][0][0], str(_ev_price(adjusted)))


class MethodIdVocabularyTest(unittest.TestCase):
    """T39–T41：带连字符的 basis token、liquidation 变体与 NAV 可选 basis。"""

    def test_hyphenated_basis_token_accepted(self):
        self.assertEqual(
            cv._method_id_format("intrinsic-price-per-share-residual-income", "method_id"),
            "intrinsic-price-per-share-residual-income",
        )

    def test_rnpv_basis_accepted(self):
        self.assertEqual(
            cv._method_id_format("intrinsic-price-per-share-rnpv", "method_id"),
            "intrinsic-price-per-share-rnpv",
        )

    def test_embedded_value_basis_accepted(self):
        for method_id in (
            "intrinsic-price-per-share-embedded-value",
            "multiple-embedded-value",
        ):
            self.assertEqual(cv._method_id_format(method_id, "method_id"), method_id)

    def test_embedded_value_is_allowed_basis_for_price_multiple(self):
        catalog = vc._catalog()
        family = next(item for item in catalog["method_families"] if item["family"] == "price-multiple")
        vocabulary = catalog["method_id_vocabulary"]
        vc._validate_method_basis("multiple-embedded-value", "price-multiple", family, vocabulary, "method_id")

    def test_rnpv_requires_its_basis_token(self):
        catalog = vc._catalog()
        family = next(item for item in catalog["method_families"] if item["family"] == "rnpv")
        vocabulary = catalog["method_id_vocabulary"]
        with self.assertRaises(vc.ValuationConsensusError):
            vc._validate_method_basis("intrinsic-price-per-share", "rnpv", family, vocabulary, "method_id")

    def test_embedded_value_rejects_other_basis(self):
        catalog = vc._catalog()
        family = next(item for item in catalog["method_families"] if item["family"] == "embedded-value")
        vocabulary = catalog["method_id_vocabulary"]
        with self.assertRaises(vc.ValuationConsensusError):
            vc._validate_method_basis("intrinsic-price-per-share-book", "embedded-value", family, vocabulary, "method_id")

    def test_liquidation_variant_accepted(self):
        self.assertEqual(
            cv._method_id_format("intrinsic-price-per-share-nav-liquidation", "method_id"),
            "intrinsic-price-per-share-nav-liquidation",
        )

    def test_unknown_basis_rejected(self):
        with self.assertRaises(cv.ContractError):
            cv._method_id_format("intrinsic-price-per-share-residuals", "method_id")

    def test_nav_is_optional_basis_for_sotp(self):
        catalog = vc._catalog()
        family = next(item for item in catalog["method_families"] if item["family"] == "sotp")
        vocabulary = catalog["method_id_vocabulary"]
        for method_id in (
            "intrinsic-price-per-share",
            "intrinsic-price-per-share-nav",
            "intrinsic-price-per-share-nav-liquidation",
        ):
            vc._validate_method_basis(method_id, "sotp", family, vocabulary, "method_id")
        with self.assertRaises(vc.ValuationConsensusError):
            vc._validate_method_basis("intrinsic-price-per-share-eps", "sotp", family, vocabulary, "method_id")


class CardContractV2Test(unittest.TestCase):
    """T24–T25：schema v2 的反向估值结构与参数推导链校验。"""

    def test_reverse_valuation_requires_structured_fields(self):
        data = _input([_price_method()])
        card = _card(data, {"multiple-eps-fy": _price_scenarios()}, primary="multiple-eps-fy")
        card["reverse_valuation"][0] = {
            "method_id": "multiple-eps-fy", "interpretation": "隐含预期",
            "evidence_fact_ids": ["f-shares"], "invalidation_condition": "条件",
        }
        with self.assertRaises(vc.ValuationConsensusError):
            vc.aggregate_reviewer_card(data, card, _critique(data))

    def test_parameter_derivation_must_cover_every_method(self):
        data = _input([_price_method()])
        card = _card(data, {"multiple-eps-fy": _price_scenarios()}, primary="multiple-eps-fy")
        card["parameter_derivation"] = []
        with self.assertRaises(vc.ValuationConsensusError) as caught:
            vc.aggregate_reviewer_card(data, card, _critique(data))
        self.assertIn("must cover every input method", str(caught.exception))


class ReportConsistencyTest(unittest.TestCase):
    """T10：check 的精度、情景布局、终值占比与分歧断言。"""

    def _body(self, result: dict, *extra: str) -> str:
        primary_range = result["primary_range"]
        parts = [f"估值区间 {primary_range['lower']}–{primary_range['upper']}", *extra]
        return "\n".join(parts)

    def test_supported_requires_label(self):
        result = _aggregate(_input([_price_method()]), {"multiple-eps-fy": _price_scenarios()},
                            primary="multiple-eps-fy")
        errors = company_run._valuation_report_consistency(
            result, result["_calculation"], self._body(result),
        )
        self.assertTrue(any("证据支持的估值区间" in error for error in errors))
        body = self._body(result, "证据支持的估值区间")
        self.assertEqual(company_run._valuation_report_consistency(
            result, result["_calculation"], body), [])

    def test_gap_requires_disclosure(self):
        data = _input([_price_method()])
        scenarios = {"multiple-eps-fy": {
            "conservative": {"denominator": "2", "range": {"lower": "10", "upper": "12"}},
            "neutral": {"denominator": "2", "range": {"lower": "13", "upper": "17"}},
            "optimistic": {"denominator": "2", "range": {"lower": "18", "upper": "21"}},
        }}
        result = _aggregate(data, scenarios, primary="multiple-eps-fy")
        body = self._body(result, "证据支持的估值区间")
        errors = company_run._valuation_report_consistency(result, result["_calculation"], body)
        self.assertTrue(any("间隔" in error for error in errors))
        body = self._body(result, "证据支持的估值区间", "情景之间存在间隔")
        self.assertEqual(company_run._valuation_report_consistency(
            result, result["_calculation"], body), [])

    def test_conditional_terminal_share_requires_disclosure(self):
        data = _input([_dcf_method()])
        result = _aggregate(data, {"intrinsic-price-per-share-midcycle": _dcf_scenarios()},
                            primary="intrinsic-price-per-share-midcycle")
        body = self._body(result, "条件性估值区间", "关键假设")
        errors = company_run._valuation_report_consistency(result, result["_calculation"], body)
        self.assertTrue(any("终值占比" in error for error in errors))

    def test_conditional_requires_key_assumptions(self):
        data = _input([_price_method()], eps_fact_type="assumption", eps_status="unverified")
        result = _aggregate(data, {"multiple-eps-fy": _price_scenarios()},
                            primary="multiple-eps-fy")
        errors = company_run._valuation_report_consistency(
            result, result["_calculation"], self._body(result, "条件性估值区间"),
        )
        self.assertTrue(any("关键假设" in error for error in errors))
        self.assertEqual(company_run._valuation_report_consistency(
            result, result["_calculation"], self._body(result, "条件性估值区间", "关键假设"),
        ), [])

    def test_low_confidence_requires_direction_disclaimer(self):
        result = _aggregate(
            _input([_price_method()]), {"multiple-eps-fy": _price_scenarios()},
            primary="multiple-eps-fy", fallback=True,
        )
        body = self._body(result, "参考区间")
        errors = company_run._valuation_report_consistency(result, result["_calculation"], body)
        self.assertTrue(any("区间不具备方向判断力" in error for error in errors))

    def test_material_divergence_requires_diagnosis(self):
        data = _input([_price_method(), _enterprise_method()], price="30")
        scenarios = {
            "multiple-eps-fy": _price_scenarios(),
            "multiple-ebit": {
                "conservative": {"denominator": "100000000", "range": {"lower": "40", "upper": "45"}},
                "neutral": {"denominator": "100000000", "range": {"lower": "50", "upper": "55"}},
                "optimistic": {"denominator": "100000000", "range": {"lower": "56", "upper": "60"}},
            },
        }
        result = _aggregate(data, scenarios, primary="multiple-eps-fy",
                            cross=("multiple-ebit",))
        body = self._body(result, "条件性估值区间", "关键假设")
        errors = company_run._valuation_report_consistency(result, result["_calculation"], body)
        self.assertTrue(any("分歧" in error for error in errors))


class ConsensusArtifactTest(unittest.TestCase):
    """T11：聚合共识可直接通过 company_valuation 的工件校验。"""

    def _consensus(self, **input_kwargs) -> tuple[dict, dict]:
        data = _input([_price_method()], **input_kwargs)
        consensus = vc.aggregate_reviewer_card(
            data,
            _card(data, {"multiple-eps-fy": _price_scenarios()}, primary="multiple-eps-fy"),
            _critique(data),
        )
        return data, consensus

    def test_supported_consensus_artifact_roundtrip(self):
        data, consensus = self._consensus()
        self.assertEqual(consensus["publication_precision_state"], "supported")
        cv._validate_consensus_artifact(consensus, data, require_supported=True)

    def test_conditional_consensus_is_not_a_supported_source(self):
        data, consensus = self._consensus(eps_fact_type="assumption", eps_status="unverified")
        cv._validate_consensus_artifact(consensus, data, require_supported=False)
        with self.assertRaises(cv.StateError):
            cv._validate_consensus_artifact(consensus, data, require_supported=True)


if __name__ == "__main__":
    unittest.main()
