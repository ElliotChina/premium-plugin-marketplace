"""Safely persist run-local valuation inputs, reviews, and recalculations."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
import errno
import json
import os
from pathlib import Path
import re
import stat
import sys
import traceback
import uuid
from typing import Any, NoReturn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import artifact_store
import evidence_contract
import valuation_calculator
import valuation_consensus


TERMINAL_RUN_STATUSES = frozenset({"completed", "aborted", "superseded"})
MARKET_SCHEMA = "company-analysis-market-snapshot-v1"
METHOD_CANDIDATES_SCHEMA = "company-analysis-valuation-method-candidates-v1"
OVERRIDE_SCHEMA = "company-analysis-valuation-overrides-v1"
DIFF_SCHEMA = "company-analysis-valuation-diff-v1"
PROVENANCE_SCHEMA = "company-analysis-valuation-recalculation-provenance-v2"
CONSENSUS_KEYS = (

    "schema_version",
    "calculator_version",
    "valuation_input_hash",
    "primary_method_id",
    "cross_check_method_ids",
    "methods",
    "status",
    "publication_precision_state",
    "precision_reasons",
    "cross_check_divergence",
    "independence",
    "fact_snapshot_id",
    "market_snapshot_id",
    "model_version",
    "method_catalog_version",
    "method_exclusions",
    "cross_check_only_method_ids",
    "primary_role_fallback",
    "critique_hash",
    "normalizations",
    "primary_range",
    "calibrations",
    "reverse_valuation",
    "parameter_derivation",
    "sensitivity_factors",
    "invalidation_conditions",
)
VALUATION_ARTIFACTS = frozenset({
    "input.json",
    "reviewer-1.json",
    "critique.json",
    "consensus-assumptions.json",
    "calculation.json",
    "valuation-diff.json",
    "recalculation-provenance.json",
    "transaction.json",
})

_SCRIPT_DIR = Path(__file__).resolve().parent
_CATALOG_PATH = _SCRIPT_DIR.parent.parent / "references" / "valuation" / "valuation-models.json"
_BUNDLED_CATALOG: Mapping | None = None

def _bundled_catalog() -> Mapping:
    global _BUNDLED_CATALOG
    catalog = _BUNDLED_CATALOG
    if catalog is None:
        try:
            with _CATALOG_PATH.open("r", encoding="utf-8") as _catalog_file:
                catalog = json.load(_catalog_file)
        except (OSError, ValueError) as exc:
            raise ContractError(f"bundled valuation catalog missing or corrupt: {exc}") from exc
        _BUNDLED_CATALOG = catalog
    return catalog

class UsageError(ValueError):
    """Raised for malformed command-line usage."""


class ContractError(ValueError):
    """Raised for invalid valuation inputs or source files."""


class StateError(ValueError):
    """Raised when an otherwise-valid operation is unavailable in this state."""

    def __init__(self, message: str, **details: object) -> None:
        super().__init__(message)
        self.details = details


class HelpRequested(Exception):
    """Keep argparse help inside the JSON protocol."""


class JsonHelpAction(argparse.Action):
    def __init__(self, option_strings, dest=argparse.SUPPRESS, default=argparse.SUPPRESS, help=None):
        super().__init__(option_strings=option_strings, dest=dest, nargs=0, default=default, help=help)

    def __call__(self, parser, namespace, values, option_string=None) -> None:
        raise HelpRequested(parser.format_help())


class JsonArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("add_help", False)
        super().__init__(*args, **kwargs)

    def error(self, message: str) -> NoReturn:
        raise UsageError(message)


def _write_json(stream, value: object) -> None:
    payload = valuation_consensus.canonical_json_bytes(value)
    if hasattr(stream, "buffer"):
        stream.buffer.write(payload)
    else:
        stream.write(payload.decode("utf-8"))
    stream.flush()


def _json_error(error_type: str, message: str, **details: object) -> dict:
    return {"error_type": error_type, "message": message, **details}


def _add_help(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-h", "--help", action=JsonHelpAction, help="show this help message and exit")


def _build_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(prog="company_valuation.py")
    _add_help(parser)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=JsonArgumentParser)

    unit_standard = commands.add_parser("unit-standard")
    _add_help(unit_standard)
    unit_standard.add_argument("--currency", required=True)

    for command in ("preflight-input", "freeze"):
        freeze = commands.add_parser(command)
        _add_help(freeze)
        freeze.add_argument("--run-dir", required=True)
        freeze.add_argument("--fact-snapshot", required=True)
        freeze.add_argument("--market-snapshot", required=True)
        freeze.add_argument("--method-candidates", required=True)
        freeze.add_argument("--method-catalog", required=True)
        freeze.add_argument("--model-version", required=True)

    install = commands.add_parser("install-card")
    _add_help(install)
    install.add_argument("--run-dir", required=True)
    install.add_argument("--card", required=True)

    single = commands.add_parser("preflight-card")
    _add_help(single)
    single.add_argument("--run-dir", required=True)
    single.add_argument("--card", required=True)

    critique = commands.add_parser("install-critique")
    _add_help(critique)
    critique.add_argument("--run-dir", required=True)
    critique.add_argument("--file", required=True)

    aggregate = commands.add_parser("aggregate")
    _add_help(aggregate)
    aggregate.add_argument("--run-dir", required=True)
    aggregate.add_argument("--baseline-input")
    aggregate.add_argument("--baseline-consensus")
    aggregate.add_argument("--baseline-calculation")

    recalculate = commands.add_parser("recalculate")
    _add_help(recalculate)
    recalculate.add_argument("--run-dir", required=True)
    recalculate.add_argument("--source-run-dir", required=True)
    recalculate.add_argument("--baseline-input", required=True)
    recalculate.add_argument("--consensus-assumptions", required=True)
    recalculate.add_argument("--market-snapshot", required=True)
    recalculate.add_argument("--overrides")
    recalculate.add_argument("--baseline-calculation")

    status = commands.add_parser("status")
    _add_help(status)
    status.add_argument("--run-dir", required=True)
    return parser


def _mapping(value: object, field: str) -> Mapping:
    if not isinstance(value, Mapping):
        raise ContractError(f"{field} must be a JSON object")
    return value


def _exact_keys(value: object, keys: tuple[str, ...], field: str) -> Mapping:
    data = _mapping(value, field)
    missing = [key for key in keys if key not in data]
    extra = [key for key in data if key not in keys]
    if missing or extra:
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if extra:
            details.append("unexpected " + ", ".join(str(key) for key in extra))
        raise ContractError(f"{field} has invalid keys: " + "; ".join(details))
    return data


def _non_empty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be a non-empty string")
    return value


def _string_list(value: object, field: str, *, require_non_empty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ContractError(f"{field} must be a list")
    items = []
    for index, item in enumerate(value):
        items.append(_non_empty_string(item, f"{field}[{index}]"))
    if len(set(items)) != len(items):
        raise ContractError(f"{field} must not contain duplicates")
    if require_non_empty and not items:
        raise ContractError(f"{field} must not be empty")
    return items


def _decimal(value: object, field: str, *, positive: bool = False) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise ContractError(f"{field} must be a finite decimal string or integer")
    if isinstance(value, int):
        amount = Decimal(value)
    elif isinstance(value, str):
        if not value.strip():
            raise ContractError(f"{field} must be a non-empty decimal string")
        try:
            amount = Decimal(value)
        except (InvalidOperation, ValueError) as exc:
            raise ContractError(f"{field} must be a finite decimal") from exc
    else:
        raise ContractError(f"{field} must be a finite decimal string or integer")
    if not amount.is_finite():
        raise ContractError(f"{field} must be finite")
    if positive and amount <= Decimal("0"):
        raise ContractError(f"{field} must be positive")
    return amount


def _is_decimal_leaf(value: object) -> bool:
    try:
        _decimal(value, "value")
    except ContractError:
        return False
    return True


def _currency_code(value: object, field: str) -> str:
    currency = _non_empty_string(value, field)
    if len(currency) != 3 or any(character < "A" or character > "Z" for character in currency):
        raise ContractError(f"{field} must be a three-letter uppercase code")
    return currency


def _iso_date(value: object, field: str) -> str:
    text = _non_empty_string(value, field)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise ContractError(f"{field} must be an ISO date") from exc
    if parsed.isoformat() != text:
        raise ContractError(f"{field} must be an ISO date")
    return text


def _iso_datetime(value: object, field: str) -> str:
    text = _non_empty_string(value, field)
    try:
        datetime.fromisoformat(text)
    except ValueError as exc:
        raise ContractError(f"{field} must be an ISO datetime") from exc
    return text


METHOD_ID_PATTERN = re.compile(r"[a-z][a-z0-9-]{2,40}")


def _method_id_format(value: object, field: str) -> str:
    method_id = _non_empty_string(value, field)
    vocabulary = _bundled_catalog().get("method_id_vocabulary")
    if vocabulary is None:
        raise ContractError("bundled valuation catalog lacks method_id_vocabulary")
    if not METHOD_ID_PATTERN.fullmatch(method_id):
        raise ContractError(
            f"{field} must match ^[a-z][a-z0-9-]{{2,40}}$ and use catalog vocabulary tokens, "
            "e.g. multiple-eps-fy or yield-fcf-forward"
        )
    indicator = next(
        (
            token
            for token in sorted(vocabulary["indicator"], key=len, reverse=True)
            if method_id == token or method_id.startswith(token + "-")
        ),
        None,
    )
    if indicator is None:
        raise ContractError(
            f"{field} must start with an indicator token from the catalog vocabulary "
            f"({', '.join(sorted(vocabulary['indicator']))}), e.g. multiple-eps-fy"
        )
    if method_id == indicator:
        return method_id
    remainder = method_id[len(indicator) + 1:]
    basis = next(
        (
            token
            for token in sorted(vocabulary["basis"], key=len, reverse=True)
            if remainder == token or remainder.startswith(token + "-")
        ),
        None,
    )
    if basis is not None:
        remainder = remainder[len(basis) + 1:] if remainder != basis else ""
        if not remainder or remainder in vocabulary["variant"]:
            return method_id
    elif remainder in vocabulary["variant"]:
        return method_id
    raise ContractError(
        f"{field} must follow <indicator>[-<basis>][-<variant>] with single catalog vocabulary tokens, "
        "e.g. multiple-eps-fy, yield-fcf-forward, intrinsic-price-per-share-midcycle"
    )


def _validate_card_method_ids(card: Mapping) -> None:
    for list_key in (
        "method_judgments",
        "scenario_parameters",
        "calibrations",
        "reverse_valuation",
        "parameter_derivation",
        "sensitivity_factors",
        "invalidation_conditions",
    ):
        for index, item in enumerate(card[list_key]):
            _method_id_format(item["method_id"], f"reviewer card.{list_key}[{index}].method_id")


def _content_hash(value: object) -> str:
    return valuation_consensus.content_hash(value)


def _absolute_without_symlink(value: str, label: str, *, directory: bool) -> Path:
    raw = Path(value).expanduser()
    if not raw.is_absolute():
        raise ContractError(f"{label} must be an absolute path")
    absolute = Path(os.path.abspath(raw))
    if not absolute.exists():
        raise ContractError(f"{label} must exist")
    if absolute.is_symlink() or absolute.resolve() != absolute:
        raise ContractError(f"{label} must not be a symlink; use the real path {absolute.resolve()} instead")
    if directory:
        if not absolute.is_dir():
            raise ContractError(f"{label} must be a directory")
    elif not absolute.is_file():
        raise ContractError(f"{label} must be a regular file")
    return absolute


def _run_dir(value: str) -> Path:
    return _absolute_without_symlink(value, "run directory", directory=True)


def _source_json(value: str, label: str) -> Mapping:
    path = _absolute_without_symlink(value, label, directory=False)
    try:
        data = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"{label} must be valid JSON") from exc
    return _mapping(data, label)


def _read_run_json(run_dir: Path) -> Mapping | None:
    path = run_dir / "run.json"
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise ContractError("run metadata must be a regular file")
    try:
        data = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError("run metadata must be valid JSON") from exc
    return _mapping(data, "run metadata")


def _assert_mutable(run_dir: Path) -> None:
    metadata = _read_run_json(run_dir)
    if metadata is not None and metadata.get("status") in TERMINAL_RUN_STATUSES:
        raise StateError("terminal runs cannot be changed")


def _valuation_dir_path(run_dir: Path) -> Path:
    return run_dir / "analysis" / "valuation"


def _safe_valuation_dir(run_dir: Path, *, create: bool) -> Path:
    analysis = run_dir / "analysis"
    valuation = _valuation_dir_path(run_dir)
    if create:
        directory_descriptor, _identity = artifact_store.open_stable_dir(valuation, create=True)
        os.close(directory_descriptor)
        return valuation
    for directory in (analysis, valuation):
        if directory.is_symlink() or directory.exists():
            if directory.is_symlink() or not directory.is_dir():
                raise ContractError("valuation directory must not be a symlink")
        else:
            return valuation
    return valuation


def _safe_artifact(valuation_dir: Path, name: str) -> Path:
    if name not in VALUATION_ARTIFACTS:
        raise ContractError("artifact path escapes the run directory")
    path = valuation_dir / name
    try:
        path.relative_to(valuation_dir)
    except ValueError as exc:
        raise ContractError("artifact path escapes the run directory") from exc
    if path.is_symlink():
        raise ContractError("installed valuation artifact must not be a symlink")
    return path


def _load_artifact_json(valuation_dir: Path, name: str) -> Mapping | None:
    path = _safe_artifact(valuation_dir, name)
    if not path.exists():
        return None
    if path.is_symlink() or not path.is_file():
        raise ContractError(f"installed valuation artifact {name} must be a regular file")
    try:
        data = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"installed valuation artifact {name} must be valid JSON") from exc
    return _mapping(data, f"installed valuation artifact {name}")


def _validate_market_snapshot(snapshot: Mapping) -> Mapping:
    data = _exact_keys(snapshot, ("schema_version", "market_snapshot_id", "market"), "market snapshot")
    if data["schema_version"] != MARKET_SCHEMA:
        raise ContractError("market snapshot.schema_version is not supported")
    _non_empty_string(data["market_snapshot_id"], "market snapshot.market_snapshot_id")
    market = _mapping(data["market"], "market snapshot.market")
    valuation_currency = None
    if "valuation_currency" in market:
        valuation_currency = _currency_code(market["valuation_currency"], "market snapshot.market.valuation_currency")
    if "current_price" not in market and valuation_currency is None:
        raise ContractError("market snapshot needs current_price or valuation_currency")
    for key, raw_record in market.items():
        if key == "valuation_currency":
            continue
        record = _exact_keys(raw_record, ("value", "currency", "unit", "date"), f"market snapshot.market.{key}")
        _decimal(record["value"], f"market snapshot.market.{key}.value", positive=True)
        _currency_code(record["currency"], f"market snapshot.market.{key}.currency")
        unit = _non_empty_string(record["unit"], f"market snapshot.market.{key}.unit")
        _iso_date(record["date"], f"market snapshot.market.{key}.date")
        if key == "current_price" and valuation_calculator.canonical_per_share_unit(unit, record["currency"]) is None:
            raise ContractError("market snapshot.market.current_price.unit must be per-share")
        if key == "current_price" and valuation_currency is not None and record["currency"] != valuation_currency:
            raise ContractError("market snapshot current_price currency must match valuation_currency")
    return snapshot


def _validate_method_candidates(candidates: Mapping) -> Mapping:
    data = _exact_keys(candidates, ("schema_version", "methods"), "method candidates")
    if data["schema_version"] != METHOD_CANDIDATES_SCHEMA:
        raise ContractError("method candidates.schema_version is not supported")
    if not isinstance(data["methods"], list) or not data["methods"]:
        raise ContractError("method candidates.methods must be a non-empty list")
    for index, method in enumerate(data["methods"]):
        _mapping(method, f"method candidates.methods[{index}]")
    return candidates


def _validate_method_catalog(catalog: Mapping) -> Mapping:
    schema_version = catalog.get("schema_version")
    calculator_version = catalog.get("calculator_version")
    if schema_version != valuation_consensus.CATALOG_VERSION:
        raise ContractError("method catalog.schema_version is not supported")
    if calculator_version != valuation_calculator.CALCULATOR_VERSION:
        raise ContractError("method catalog.calculator_version must match the runtime calculator")
    if catalog != _bundled_catalog():
        raise ContractError("method catalog must match the bundled valuation catalog exactly")
    return catalog


def _input_from_sources(
    fact_snapshot: Mapping,
    market_snapshot: Mapping,
    method_candidates: Mapping,
    method_catalog: Mapping,
    model_version: str,
) -> dict:
    try:
        evidence_contract.validate_fact_snapshot(fact_snapshot)
    except evidence_contract.EvidenceError as exc:
        raise ContractError(str(exc)) from exc
    market_snapshot = _validate_market_snapshot(market_snapshot)
    method_candidates = _validate_method_candidates(method_candidates)
    _validate_method_catalog(method_catalog)
    _non_empty_string(model_version, "model version")
    data = {
        "schema_version": valuation_consensus.INPUT_SCHEMA,
        "fact_snapshot_id": fact_snapshot["fact_snapshot_id"],
        "market_snapshot_id": market_snapshot["market_snapshot_id"],
        "model_version": model_version,
        "calculator_version": valuation_calculator.CALCULATOR_VERSION,
        "method_catalog_version": valuation_consensus.CATALOG_VERSION,
        "valuation_input_hash": "pending",
        "facts": list(fact_snapshot["facts"]),
        "market": dict(market_snapshot["market"]),
        "methods": list(method_candidates["methods"]),
    }
    data["valuation_input_hash"] = valuation_consensus.valuation_input_hash(data)
    try:
        valuation_consensus.validate_valuation_input(data)
    except valuation_consensus.ValuationConsensusError as exc:
        raise ContractError(str(exc)) from exc
    return data


def _load_input(valuation_dir: Path) -> Mapping:
    data = _load_artifact_json(valuation_dir, "input.json")
    if data is None:
        raise StateError("valuation input has not been frozen")
    try:
        valuation_consensus.validate_valuation_input(data)
    except valuation_consensus.ValuationConsensusError as exc:
        raise ContractError(str(exc)) from exc
    return data


def _card(valuation_dir: Path, valuation_input: Mapping, *, strict: bool) -> tuple[Mapping | None, str | None]:
    try:
        card = _load_artifact_json(valuation_dir, "reviewer-1.json")
        if card is not None:
            valuation_consensus.validate_reviewer_card(card, valuation_input)
            if card.get("reviewer_id") != "reviewer-1":
                raise ContractError("reviewer card reviewer_id must be reviewer-1")
        return card, None
    except (ContractError, valuation_consensus.ValuationConsensusError) as exc:
        if strict:
            raise ContractError(str(exc)) from exc
        return None, str(exc)


def _calculate(valuation_input: Mapping, assumptions: Mapping, baseline: Mapping | None = None) -> dict:
    try:
        return valuation_calculator.calculate_valuation(valuation_input, assumptions, baseline)
    except valuation_calculator.ValuationError as exc:
        raise ContractError(str(exc)) from exc


def _validate_calculation(data: Mapping, label: str, *, source_input: Mapping | None = None) -> Mapping:
    calculation = _exact_keys(data, (
        "schema_version",
        "calculator_version",
        "valuation_input_hash",
        "fact_snapshot_id",
        "market_snapshot_id",
        "primary_method_id",
        "cross_check_method_ids",
        "methods",
        "primary",
        "baseline_diff",
    ), label)
    if calculation["schema_version"] != valuation_calculator.CALCULATION_SCHEMA:
        raise ContractError(f"{label}.schema_version is not supported")
    if calculation["calculator_version"] != valuation_calculator.CALCULATOR_VERSION:
        raise ContractError(f"{label}.calculator_version is not supported")
    for key in ("valuation_input_hash", "fact_snapshot_id", "market_snapshot_id", "primary_method_id"):
        _non_empty_string(calculation[key], f"{label}.{key}")
    if not isinstance(calculation["cross_check_method_ids"], list):
        raise ContractError(f"{label}.cross_check_method_ids must be a list")
    if not isinstance(calculation["methods"], list) or not calculation["methods"]:
        raise ContractError(f"{label}.methods must be a non-empty list")
    _mapping(calculation["primary"], f"{label}.primary")
    if not isinstance(calculation["baseline_diff"], list):
        raise ContractError(f"{label}.baseline_diff must be a list")
    if source_input is not None:
        for key in ("valuation_input_hash", "fact_snapshot_id", "market_snapshot_id"):
            if calculation[key] != source_input[key]:
                raise StateError(f"{label}.{key} must match the baseline input")
    return calculation


def _validate_consensus_artifact(data: Mapping, baseline_input: Mapping, *, require_supported: bool) -> Mapping:
    consensus = _exact_keys(data, CONSENSUS_KEYS, "consensus assumptions")
    if consensus.get("schema_version") != valuation_consensus.ASSUMPTIONS_SCHEMA:
        raise ContractError("consensus assumptions.schema_version is not supported")
    if consensus.get("calculator_version") != valuation_calculator.CALCULATOR_VERSION:
        raise ContractError("consensus assumptions.calculator_version is not supported")
    for key in ("valuation_input_hash", "fact_snapshot_id", "market_snapshot_id", "model_version", "method_catalog_version"):
        if consensus.get(key) != baseline_input.get(key):
            raise StateError(f"consensus assumptions.{key} must match the baseline input")
    precision = consensus.get("publication_precision_state")
    if require_supported:
        if precision != "supported":
            raise StateError("source consensus must be supported")
    elif precision not in {"supported", "conditional", "low-confidence"}:
        raise ContractError("consensus assumptions.publication_precision_state is not publishable")
    if consensus.get("status") != valuation_consensus.STATUS_BY_PRECISION.get(precision):
        raise ContractError("consensus assumptions.status does not match its precision state")
    _calculate(baseline_input, consensus)
    return consensus


def _diff_wrapper(baseline: Mapping | None, calculation: Mapping) -> dict:
    return {
        "schema_version": DIFF_SCHEMA,
        "baseline_calculation_hash": None if baseline is None else _content_hash(baseline),
        "calculation_hash": _content_hash(calculation),
        "baseline_calculation": None if baseline is None else valuation_consensus.deepcopy_json(baseline),
        "changes": [] if baseline is None else list(calculation["baseline_diff"]),
    }


def _validate_recomputed_calculation(
    baseline_input: Mapping,
    baseline_consensus: Mapping,
    supplied_calculation: Mapping,
    label: str,
) -> Mapping:
    _validate_calculation(supplied_calculation, label, source_input=baseline_input)
    expected_calculation = _calculate(baseline_input, baseline_consensus)
    if (
        valuation_consensus.canonical_json_bytes(expected_calculation)
        != valuation_consensus.canonical_json_bytes(supplied_calculation)
    ):
        raise ContractError(f"{label} does not match its baseline input and consensus")
    return supplied_calculation


def _require_exact_source_artifact(supplied: str, source_path: Path, label: str) -> Mapping:
    supplied_path = _absolute_without_symlink(supplied, label, directory=False)
    try:
        supplied_bytes = supplied_path.read_bytes()
        source_bytes = source_path.read_bytes()
    except OSError as exc:
        raise ContractError(f"{label} could not be read") from exc
    if supplied_bytes != source_bytes:
        raise StateError(f"{label} must byte-match the authenticated source run artifact")
    return _source_json(str(supplied_path), label)


def _effective_currency(market: Mapping) -> str:
    if "valuation_currency" in market:
        return _currency_code(market["valuation_currency"], "market.valuation_currency")
    if "current_price" in market:
        return _currency_code(market["current_price"]["currency"], "market.current_price.currency")
    raise ContractError("market needs current_price or valuation_currency")


def _load_authenticated_recalculation_source(args: argparse.Namespace) -> tuple[Path, Mapping, Mapping, Mapping | None, str | None]:
    source_run = _absolute_without_symlink(args.source_run_dir, "source run directory", directory=True)
    source_status = _status(argparse.Namespace(run_dir=str(source_run)))
    required_hashes = ("consensus_hash", "calculation_hash", "transaction_hash")
    if (
        source_status.get("status") != "complete"
        or source_status.get("precision_state") != "supported"
        or any(not source_status.get(key) for key in required_hashes)
    ):
        raise StateError("source run must be an authenticated complete supported aggregate run")

    source_valuation_dir = _safe_valuation_dir(source_run, create=False)
    source_input_path = _safe_artifact(source_valuation_dir, "input.json")
    source_consensus_path = _safe_artifact(source_valuation_dir, "consensus-assumptions.json")
    source_calculation_path = _safe_artifact(source_valuation_dir, "calculation.json")
    baseline_input = _require_exact_source_artifact(args.baseline_input, source_input_path, "baseline input")
    source_consensus = _validate_consensus_artifact(
        _require_exact_source_artifact(
            args.consensus_assumptions,
            source_consensus_path,
            "consensus assumptions",
        ),
        baseline_input,
        require_supported=True,
    )
    source_calculation = _load_artifact_json(source_valuation_dir, "calculation.json")
    if source_calculation is None:
        raise StateError("authenticated source run is missing calculation.json")
    source_diff = _load_artifact_json(source_valuation_dir, "valuation-diff.json")
    _validate_calculation_against_sources(
        baseline_input, source_consensus, source_calculation, source_diff
    )

    baseline_calculation = None
    if args.baseline_calculation is not None:
        baseline_calculation = _require_exact_source_artifact(
            args.baseline_calculation,
            source_calculation_path,
            "baseline calculation",
        )
    source_calculation_hash = None if baseline_calculation is None else _content_hash(source_calculation)
    return source_run, baseline_input, source_consensus, baseline_calculation, source_calculation_hash


def _load_baseline_triplet(args: argparse.Namespace) -> Mapping | None:
    paths = (args.baseline_input, args.baseline_consensus, args.baseline_calculation)
    if not any(path is not None for path in paths):
        return None
    if any(path is None for path in paths):
        raise UsageError("baseline input, baseline consensus, and baseline calculation are required together")
    baseline_input = _source_json(args.baseline_input, "baseline input")
    try:
        valuation_consensus.validate_valuation_input(baseline_input)
    except valuation_consensus.ValuationConsensusError as exc:
        raise ContractError(str(exc)) from exc
    baseline_consensus = _validate_consensus_artifact(
        _source_json(args.baseline_consensus, "baseline consensus"),
        baseline_input,
        require_supported=True,
    )
    return _validate_recomputed_calculation(
        baseline_input,
        baseline_consensus,
        _source_json(args.baseline_calculation, "baseline calculation"),
        "baseline calculation",
    )


def _assert_fresh_recalculation_run(run_dir: Path) -> None:
    _assert_mutable(run_dir)
    valuation_dir = _safe_valuation_dir(run_dir, create=False)
    if valuation_dir.exists():
        if valuation_dir.is_symlink() or not valuation_dir.is_dir():
            raise ContractError("valuation directory must not be a symlink")
        if any(valuation_dir.iterdir()):
            raise StateError("recalculation destination must be a fresh valuation run")


def _facts_by_id(valuation_input: Mapping) -> dict[str, Mapping]:
    return {fact["fact_id"]: fact for fact in valuation_input["facts"]}


def _method_by_id(consensus: Mapping, method_id: str) -> Mapping:
    for method in consensus.get("methods", []):
        if isinstance(method, Mapping) and method.get("method_id") == method_id:
            return method
    raise ContractError("override path must identify an existing method")


def _resolve_override_target(consensus: Mapping, path: str) -> tuple[Any, Any]:
    parts = path.split(".")
    if len(parts) < 4 or parts[0] != "methods":
        raise ContractError("override path must start with methods.<method_id>")
    method = _method_by_id(consensus, parts[1])
    if parts[2] not in {"scenarios", "sensitivity"}:
        raise ContractError("override path may only target scenarios or sensitivity")
    current: object = method
    for token in parts[2:-1]:
        if isinstance(current, Mapping):
            if token not in current:
                raise ContractError("override path must resolve to an existing leaf")
            current = current[token]
        elif isinstance(current, list):
            if not token.isdigit():
                raise ContractError("override path list indexes must be numeric")
            index = int(token)
            if index >= len(current):
                raise ContractError("override path must resolve to an existing leaf")
            current = current[index]
        else:
            raise ContractError("override path must resolve to an existing leaf")
    final = parts[-1]
    if isinstance(current, Mapping):
        if final not in current:
            raise ContractError("override path must resolve to an existing leaf")
        return current, final
    if isinstance(current, list):
        if not final.isdigit():
            raise ContractError("override path list indexes must be numeric")
        index = int(final)
        if index >= len(current):
            raise ContractError("override path must resolve to an existing leaf")
        return current, index
    raise ContractError("override path must resolve to an existing leaf")


def _validate_override_record(
    overrides: Mapping,
    baseline_input: Mapping,
    consensus: Mapping,
    *,
    enforce_values: bool,
) -> tuple[Mapping, int]:
    data = _exact_keys(overrides, (
        "schema_version",
        "reason",
        "author",
        "created_at",
        "evidence_fact_ids",
        "changed_parameters",
    ), "overrides")
    if data["schema_version"] != OVERRIDE_SCHEMA:
        raise ContractError("overrides.schema_version is not supported")
    _non_empty_string(data["reason"], "overrides.reason")
    _non_empty_string(data["author"], "overrides.author")
    _iso_datetime(data["created_at"], "overrides.created_at")
    evidence_ids = _string_list(data["evidence_fact_ids"], "overrides.evidence_fact_ids", require_non_empty=True)
    facts = _facts_by_id(baseline_input)
    for fact_id in evidence_ids:
        if fact_id not in facts:
            raise ContractError("overrides.evidence_fact_ids must reference baseline input facts")
        if facts[fact_id]["status"] != "verified":
            raise ContractError("overrides.evidence_fact_ids must reference verified facts")
    changed_parameters = data["changed_parameters"]
    if not isinstance(changed_parameters, list) or not changed_parameters:
        raise ContractError("overrides.changed_parameters must be a non-empty list")
    paths = []
    for index, raw_change in enumerate(changed_parameters):
        change = _exact_keys(raw_change, ("path", "value"), f"overrides.changed_parameters[{index}]")
        path = _non_empty_string(change["path"], f"overrides.changed_parameters[{index}].path")
        if path in paths:
            raise ContractError("overrides.changed_parameters contains duplicate paths")
        paths.append(path)
        parent, key = _resolve_override_target(consensus, path)
        current_value = parent[key]
        if not _is_decimal_leaf(current_value):
            raise ContractError("override path must resolve to an existing numeric leaf")
        _decimal(change["value"], f"overrides.changed_parameters[{index}].value")
        if enforce_values and current_value != change["value"]:
            raise ContractError("overrides.changed_parameters must match recalculated consensus")
    return data, len(changed_parameters)


def _apply_overrides(consensus: dict, overrides: Mapping, baseline_input: Mapping) -> tuple[Mapping, int]:
    data, changed_count = _validate_override_record(
        overrides,
        baseline_input,
        consensus,
        enforce_values=False,
    )
    for change in data["changed_parameters"]:
        parent, key = _resolve_override_target(consensus, change["path"])
        parent[key] = change["value"]
    return data, changed_count


def _freeze(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    fact_snapshot = _source_json(args.fact_snapshot, "fact snapshot")
    market_snapshot = _source_json(args.market_snapshot, "market snapshot")
    method_candidates = _source_json(args.method_candidates, "method candidates")
    method_catalog = _source_json(args.method_catalog, "method catalog")
    input_data = _input_from_sources(fact_snapshot, market_snapshot, method_candidates, method_catalog, args.model_version)
    try:
        source_audit = evidence_contract.preflight_shared_facts(run_dir, input_data, "scoring")
    except evidence_contract.EvidenceError as exc:
        raise ContractError(str(exc)) from exc
    valuation_dir = _safe_valuation_dir(run_dir, create=True)
    artifact_store.atomic_install(valuation_dir, "input.json", input_data)
    result = {
        "status": "frozen",
        "valuation_input_hash": input_data["valuation_input_hash"],
        "fact_snapshot_id": input_data["fact_snapshot_id"],
        "market_snapshot_id": input_data["market_snapshot_id"],
        "calculator_version": input_data["calculator_version"],
        "method_catalog_version": input_data["method_catalog_version"],
        "model_version": input_data["model_version"],
    }
    if source_audit["enabled"]:
        result["source_audit"] = source_audit
    return result


def _preflight_input(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    input_data = _input_from_sources(
        _source_json(args.fact_snapshot, "fact snapshot"),
        _source_json(args.market_snapshot, "market snapshot"),
        _source_json(args.method_candidates, "method candidates"),
        _source_json(args.method_catalog, "method catalog"),
        args.model_version,
    )
    try:
        source_audit = evidence_contract.preflight_shared_facts(run_dir, input_data, "scoring")
    except evidence_contract.EvidenceError as exc:
        raise ContractError(str(exc)) from exc
    valuation_dir = _safe_valuation_dir(run_dir, create=False)
    existing_path = _safe_artifact(valuation_dir, "input.json")
    if existing_path.exists() and (
        not existing_path.is_file()
        or existing_path.read_bytes() != valuation_consensus.canonical_json_bytes(input_data)
    ):
        raise StateError("immutable valuation input conflicts with existing content")
    result = {"status": "ready", "fact_snapshot_id": input_data["fact_snapshot_id"],
              "valuation_input_hash": input_data["valuation_input_hash"],
              "market_snapshot_id": input_data["market_snapshot_id"]}
    if source_audit["enabled"]:
        result["source_audit"] = source_audit
    return result


def _preflight_card(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    valuation_input = _load_input(_safe_valuation_dir(run_dir, create=False))
    card = _source_json(args.card, "reviewer card")
    try:
        valuation_consensus.validate_reviewer_card(card, valuation_input)
    except valuation_consensus.ValuationConsensusError as exc:
        raise StateError(str(exc), issue_type="card-format") from exc
    if card.get("reviewer_id") != "reviewer-1":
        raise ContractError("reviewer card reviewer_id must be reviewer-1")
    _validate_card_method_ids(card)
    return {"status": "ready", "valuation_input_hash": valuation_input["valuation_input_hash"]}


def _install_card(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    valuation_dir = _safe_valuation_dir(run_dir, create=False)
    valuation_input = _load_input(valuation_dir)
    card = _source_json(args.card, "reviewer card")
    try:
        valuation_consensus.validate_reviewer_card(card, valuation_input)
    except valuation_consensus.ValuationConsensusError as exc:
        raise ContractError(str(exc)) from exc
    if card.get("reviewer_id") != "reviewer-1":
        raise ContractError("reviewer card reviewer_id must be reviewer-1")
    _validate_card_method_ids(card)
    _card(valuation_dir, valuation_input, strict=True)
    artifact_store.atomic_install(valuation_dir, "reviewer-1.json", card)
    return {"status": "installed", "reviewer_id": card["reviewer_id"]}


def _install_critique(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    valuation_dir = _safe_valuation_dir(run_dir, create=False)
    valuation_input = _load_input(valuation_dir)
    critique = _source_json(args.file, "valuation critique")
    try:
        valuation_consensus.validate_critique(critique, valuation_input)
    except valuation_consensus.ValuationConsensusError as exc:
        raise ContractError(str(exc)) from exc
    artifact_store.atomic_install(valuation_dir, "critique.json", critique)
    return {
        "status": "installed",
        "critic_id": critique["critic_id"],
        "item_count": len(critique["items"]),
        "valuation_input_hash": valuation_input["valuation_input_hash"],
    }


def _aggregate_single(
    valuation_dir: Path, valuation_input: Mapping, card: Mapping, args: argparse.Namespace,
) -> dict:
    critique = _load_artifact_json(valuation_dir, "critique.json")
    if critique is None:
        raise StateError(
            "估值批判工件未安装；先由估值批判者产出批判并运行 install-critique",
            issue_type="critique-missing",
        )
    try:
        consensus = valuation_consensus.aggregate_reviewer_card(valuation_input, card, critique)
    except valuation_consensus.ValuationConsensusError as exc:
        raise ContractError(str(exc)) from exc
    baseline = _load_baseline_triplet(args)

    items: list[tuple[str, Mapping]] = [("consensus-assumptions.json", consensus)]
    calculation = None
    diff = None
    if consensus["publication_precision_state"] in {"supported", "conditional", "low-confidence"}:
        calculation = _calculate(valuation_input, consensus, baseline)
        items.append(("calculation.json", calculation))
        if baseline is not None:
            diff = _diff_wrapper(baseline, calculation)
            items.append(("valuation-diff.json", diff))

    artifacts = {
        "input.json": valuation_input,
        "reviewer-1.json": card,
        "critique.json": critique,
        "consensus-assumptions.json": consensus,
        **({"calculation.json": calculation} if calculation is not None else {}),
        **({"valuation-diff.json": diff} if diff is not None else {}),
    }
    transaction = artifact_store.install_all(valuation_dir, "aggregate", items, artifacts)
    status = {
        "consensus": "complete",
        "conditional-consensus": "complete-conditional",
        "low-confidence-consensus": "complete-low-confidence",
    }.get(consensus["status"], "evidence-insufficient")
    return {
        "status": status,
        "valuation_input_hash": valuation_input["valuation_input_hash"],
        "consensus_hash": _content_hash(consensus),
        "calculation_hash": None if calculation is None else _content_hash(calculation),
        "diff_hash": None if diff is None else _content_hash(diff),
        "transaction_hash": _content_hash(transaction),
        "precision_state": consensus["publication_precision_state"],
        "market_position_status": "available" if "current_price" in valuation_input["market"] else "unavailable",
        "calculation_written": calculation is not None,
        "diff_written": diff is not None,
    }


def _aggregate(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    valuation_dir = _safe_valuation_dir(run_dir, create=False)
    valuation_input = _load_input(valuation_dir)
    card, _ = _card(valuation_dir, valuation_input, strict=True)
    if card is None:
        raise StateError("需要先安装有效的 reviewer-1 估值卡")
    return _aggregate_single(valuation_dir, valuation_input, card, args)


def _recalculate(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_fresh_recalculation_run(run_dir)
    source_run, baseline_input, source_consensus, baseline_calculation, source_calculation_hash = (
        _load_authenticated_recalculation_source(args)
    )
    market_snapshot = _validate_market_snapshot(_source_json(args.market_snapshot, "market snapshot"))
    baseline_currency = _effective_currency(baseline_input["market"])
    new_currency = _effective_currency(market_snapshot["market"])
    if baseline_currency != new_currency:
        raise ContractError(
            f"recalculation cannot change the valuation currency ({baseline_currency} -> {new_currency}); start a new run instead"
        )

    new_input = dict(valuation_consensus.deepcopy_json(baseline_input))
    new_input["market_snapshot_id"] = market_snapshot["market_snapshot_id"]
    new_input["market"] = valuation_consensus.deepcopy_json(market_snapshot["market"])
    new_input["valuation_input_hash"] = valuation_consensus.valuation_input_hash(new_input)
    try:
        valuation_consensus.validate_valuation_input(new_input)
    except valuation_consensus.ValuationConsensusError as exc:
        raise ContractError(str(exc)) from exc

    new_consensus = dict(valuation_consensus.deepcopy_json(source_consensus))
    new_consensus["valuation_input_hash"] = new_input["valuation_input_hash"]
    new_consensus["fact_snapshot_id"] = new_input["fact_snapshot_id"]
    new_consensus["market_snapshot_id"] = new_input["market_snapshot_id"]

    override_data = None
    changed_path_count = 0
    if args.overrides is not None:
        override_data, changed_path_count = _apply_overrides(
            new_consensus,
            _source_json(args.overrides, "overrides"),
            baseline_input,
        )

    new_calculation = _calculate(new_input, new_consensus, baseline_calculation)
    if new_consensus["primary_method_id"] is None:
        raise ContractError("supported source consensus must have a primary method")
    new_consensus.update(valuation_consensus.assess_precision(
        new_input,
        new_consensus["methods"],
        new_consensus["primary_method_id"],
        new_consensus["cross_check_method_ids"],
        new_consensus["primary_role_fallback"],
        new_calculation,
    ))
    try:
        new_consensus["primary_range"] = valuation_consensus.expected_primary_range(
            new_calculation, new_consensus["primary_method_id"]
        )
    except valuation_consensus.ValuationConsensusError as exc:
        raise ContractError(str(exc)) from exc
    diff = _diff_wrapper(baseline_calculation, new_calculation)
    provenance = {
        "schema_version": PROVENANCE_SCHEMA,
        "source_run_id": source_run.name,
        "source_valuation_input_hash": baseline_input["valuation_input_hash"],
        "source_consensus_hash": _content_hash(source_consensus),
        "source_calculation_hash": source_calculation_hash,
        "new_valuation_input_hash": new_input["valuation_input_hash"],
        "new_consensus_hash": _content_hash(new_consensus),
        "override_hash": None if override_data is None else _content_hash(override_data),
        "override_record": None if override_data is None else valuation_consensus.deepcopy_json(override_data),
        "reason": "market-only recalculation" if override_data is None else "explicit assumption override",
    }
    valuation_dir = _safe_valuation_dir(run_dir, create=True)
    items = (
        ("input.json", new_input),
        ("consensus-assumptions.json", new_consensus),
        ("calculation.json", new_calculation),
        ("valuation-diff.json", diff),
        ("recalculation-provenance.json", provenance),
    )
    artifacts = {name: data for name, data in items}
    transaction = artifact_store.install_all(valuation_dir, "recalculate", items, artifacts)

    result = {
        "status": "recalculated",
        "market_position_status": "available" if "current_price" in new_input["market"] else "unavailable",
        "new_valuation_input_hash": new_input["valuation_input_hash"],
        "new_consensus_hash": _content_hash(new_consensus),
        "calculation_hash": _content_hash(new_calculation),
        "diff_hash": _content_hash(diff),
        "provenance_hash": _content_hash(provenance),
        "transaction_hash": _content_hash(transaction),
        "reviewers_reused": False,
        "changed_path_count": changed_path_count,
    }
    if override_data is not None:
        result.update({
            "override_hash": _content_hash(override_data),
            "override_author": override_data["author"],
            "override_reason": override_data["reason"],
            "override_evidence_fact_ids": list(override_data["evidence_fact_ids"]),
        })
    return result


def _validate_diff_artifact(diff: Mapping) -> Mapping:
    diff_data = _exact_keys(
        diff,
        ("schema_version", "baseline_calculation_hash", "calculation_hash", "baseline_calculation", "changes"),
        "valuation diff",
    )
    if diff_data["schema_version"] != DIFF_SCHEMA:
        raise ContractError("valuation diff.schema_version is not supported")
    _non_empty_string(diff_data["calculation_hash"], "valuation diff.calculation_hash")
    baseline = diff_data["baseline_calculation"]
    if baseline is None:
        if diff_data["baseline_calculation_hash"] is not None:
            raise ContractError("valuation diff.baseline_calculation_hash must be null without an embedded baseline")
    else:
        baseline = _mapping(baseline, "valuation diff.baseline_calculation")
        _validate_calculation(baseline, "valuation diff.baseline_calculation")
        if diff_data["baseline_calculation_hash"] != _content_hash(baseline):
            raise ContractError("valuation diff.baseline_calculation_hash must match the embedded baseline")
    if not isinstance(diff_data["changes"], list):
        raise ContractError("valuation diff.changes must be a list")
    return diff_data


def _validate_calculation_against_sources(
    valuation_input: Mapping,
    consensus: Mapping,
    calculation: Mapping,
    diff: Mapping | None,
) -> Mapping | None:
    _validate_calculation(calculation, "calculation", source_input=valuation_input)
    diff_data = None
    baseline = None
    if diff is not None:
        diff_data = _validate_diff_artifact(diff)
        if diff_data["calculation_hash"] != _content_hash(calculation):
            raise ContractError("valuation diff.calculation_hash must match calculation")
        baseline = diff_data["baseline_calculation"]
    expected_calculation = _calculate(valuation_input, consensus, baseline)
    if (
        valuation_consensus.canonical_json_bytes(expected_calculation)
        != valuation_consensus.canonical_json_bytes(calculation)
    ):
        raise ContractError("calculation does not match valuation input, consensus, and embedded baseline")
    if diff is not None:
        expected_diff = _diff_wrapper(baseline, expected_calculation)
        if valuation_consensus.canonical_json_bytes(expected_diff) != valuation_consensus.canonical_json_bytes(diff):
            raise ContractError("valuation diff does not match calculation and embedded baseline")
    return diff_data


def _validate_transaction_marker(marker: Mapping | None, operation: str, artifacts: Mapping[str, Mapping]) -> Mapping:
    if marker is None:
        raise ContractError("transaction marker is required")
    expected = artifact_store.transaction_marker(operation, artifacts)
    marker_data = _exact_keys(marker, ("schema_version", "operation", "artifacts"), "transaction marker")
    if marker_data != expected:
        raise ContractError("transaction marker does not match trusted valuation artifacts")
    return marker_data


def _validate_recalculation_provenance(
    provenance: Mapping,
    valuation_input: Mapping,
    consensus: Mapping,
    diff_data: Mapping,
) -> Mapping:
    provenance_data = _exact_keys(provenance, (
        "schema_version",
        "source_run_id",
        "source_valuation_input_hash",
        "source_consensus_hash",
        "source_calculation_hash",
        "new_valuation_input_hash",
        "new_consensus_hash",
        "override_hash",
        "override_record",
        "reason",
    ), "recalculation provenance")
    if provenance_data["schema_version"] != PROVENANCE_SCHEMA:
        raise ContractError("recalculation provenance.schema_version is not supported")
    source_run_id = _non_empty_string(provenance_data["source_run_id"], "recalculation provenance.source_run_id")
    if "/" in source_run_id or source_run_id in {".", ".."}:
        raise ContractError("recalculation provenance.source_run_id must be a bare run directory name")
    for key in ("source_valuation_input_hash", "source_consensus_hash", "new_valuation_input_hash", "new_consensus_hash"):
        _non_empty_string(provenance_data[key], f"recalculation provenance.{key}")
    if provenance_data["new_valuation_input_hash"] != valuation_input["valuation_input_hash"]:
        raise ContractError("recalculation provenance.new_valuation_input_hash must match input")
    if provenance_data["new_consensus_hash"] != _content_hash(consensus):
        raise ContractError("recalculation provenance.new_consensus_hash must match consensus")
    if provenance_data["source_calculation_hash"] != diff_data["baseline_calculation_hash"]:
        raise ContractError("recalculation provenance.source_calculation_hash must match diff baseline")

    override_record = provenance_data["override_record"]
    if override_record is None:
        if provenance_data["override_hash"] is not None:
            raise ContractError("recalculation provenance.override_hash must be null without override_record")
        if provenance_data["reason"] != "market-only recalculation":
            raise ContractError("recalculation provenance.reason must identify market-only recalculation")
    else:
        override_record = _mapping(override_record, "recalculation provenance.override_record")
        if provenance_data["override_hash"] != _content_hash(override_record):
            raise ContractError("recalculation provenance.override_hash must match override_record")
        try:
            _validate_override_record(override_record, valuation_input, consensus, enforce_values=True)
        except ContractError as exc:
            raise ContractError(f"recalculation provenance.override_record is invalid: {exc}") from exc
        if provenance_data["reason"] != "explicit assumption override":
            raise ContractError("recalculation provenance.reason must identify explicit assumption override")
    return provenance_data


def _invalid_status(error: str, transaction: Mapping | None = None) -> dict:
    return {
        "status": "invalid",
        "input_hash": None,
        "slots": [{"slot": 1, "state": "missing", "reviewer_id": None, "error": None}],
        "missing_slots": [1],
        "precision_state": None,
        "consensus_hash": None,
        "calculation_hash": None,
        "diff_hash": None,
        "provenance_hash": None,
        "transaction_hash": None if transaction is None else _content_hash(transaction),
        "error": error,
    }


def _reauthenticate_recalculation_source(valuation_dir: Path, provenance: Mapping) -> None:
    """Re-bind the recalculation to its live source run; a missing or changed source is invalid."""
    source_run = valuation_dir.parent.parent.parent / provenance["source_run_id"]
    if source_run.is_symlink() or not source_run.is_dir():
        raise ContractError("recalculation source run must be a sibling run directory")
    source_status = _status(argparse.Namespace(run_dir=str(source_run)))
    if source_status.get("status") != "complete" or source_status.get("precision_state") != "supported":
        raise ContractError("recalculation source run must still be a complete supported aggregate run")
    source_valuation_dir = _safe_valuation_dir(source_run, create=False)
    source_input = _load_artifact_json(source_valuation_dir, "input.json")
    source_consensus = _load_artifact_json(source_valuation_dir, "consensus-assumptions.json")
    source_calculation = _load_artifact_json(source_valuation_dir, "calculation.json")
    if source_input is None or source_consensus is None or source_calculation is None:
        raise ContractError("recalculation source run is missing its aggregate artifacts")
    if source_input["valuation_input_hash"] != provenance["source_valuation_input_hash"]:
        raise ContractError("recalculation source input no longer matches the recorded provenance")
    if _content_hash(source_consensus) != provenance["source_consensus_hash"]:
        raise ContractError("recalculation source consensus no longer matches the recorded provenance")
    if (
        provenance["source_calculation_hash"] is not None
        and _content_hash(source_calculation) != provenance["source_calculation_hash"]
    ):
        raise ContractError("recalculation source calculation no longer matches the recorded provenance")


def _status(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    transaction = None
    try:
        valuation_dir = _safe_valuation_dir(run_dir, create=False)
        transaction = _load_artifact_json(valuation_dir, "transaction.json")
    except ContractError as exc:
        return _invalid_status(str(exc))

    try:
        valuation_input = _load_input(valuation_dir)
    except StateError:
        if transaction is not None:
            return _invalid_status("transaction marker exists without a frozen valuation input", transaction)
        return {
            "status": "not-frozen",
            "input_hash": None,
            "slots": [{"slot": 1, "state": "missing", "reviewer_id": None, "error": None}],
            "missing_slots": [1],
            "precision_state": None,
            "consensus_hash": None,
            "calculation_hash": None,
            "diff_hash": None,
            "provenance_hash": None,
            "transaction_hash": None,
        }
    except ContractError as exc:
        return _invalid_status(str(exc), transaction)

    card, card_error = _card(valuation_dir, valuation_input, strict=False)
    slots = [{
        "slot": 1,
        "state": "valid" if card is not None else ("invalid" if card_error is not None else "missing"),
        "reviewer_id": None if card is None else card["reviewer_id"],
        "error": card_error,
    }]
    base = {
        "input_hash": valuation_input["valuation_input_hash"],
        "slots": slots,
        "missing_slots": [] if card is not None else [1],
        "consensus_hash": None,
        "calculation_hash": None,
        "diff_hash": None,
        "provenance_hash": None,
        "transaction_hash": None if transaction is None else _content_hash(transaction),
    }

    try:
        critique = _load_artifact_json(valuation_dir, "critique.json")
        consensus = _load_artifact_json(valuation_dir, "consensus-assumptions.json")
        calculation = _load_artifact_json(valuation_dir, "calculation.json")
        diff = _load_artifact_json(valuation_dir, "valuation-diff.json")
        provenance = _load_artifact_json(valuation_dir, "recalculation-provenance.json")
    except ContractError as exc:
        return {"status": "invalid", **base, "precision_state": None, "error": str(exc)}

    if provenance is not None:
        try:
            if card is not None:
                raise ContractError("recalculation runs must not include reviewer cards")
            if consensus is None or calculation is None or diff is None:
                raise ContractError("recalculation runs require consensus, calculation, and diff artifacts")
            _validate_consensus_artifact(consensus, valuation_input, require_supported=False)
            diff_data = _validate_calculation_against_sources(valuation_input, consensus, calculation, diff)
            assert diff_data is not None
            _validate_recalculation_provenance(provenance, valuation_input, consensus, diff_data)
            _reauthenticate_recalculation_source(valuation_dir, provenance)
            try:
                expected_range = valuation_consensus.expected_primary_range(
                    calculation, consensus["primary_method_id"]
                )
            except valuation_consensus.ValuationConsensusError as exc:
                raise ContractError(str(exc)) from exc
            if consensus["primary_range"] != expected_range:
                raise ContractError("consensus primary_range does not match the deterministic calculation")
            _validate_transaction_marker(transaction, "recalculate", {
                "input.json": valuation_input,
                "consensus-assumptions.json": consensus,
                "calculation.json": calculation,
                "valuation-diff.json": diff,
                "recalculation-provenance.json": provenance,
            })
        except (ContractError, StateError) as exc:
            return {"status": "invalid", **base, "precision_state": None, "error": str(exc)}
        return {
            "status": "recalculated",
            **base,
            "market_position_status": "available" if "current_price" in valuation_input["market"] else "unavailable",
            "precision_state": consensus["publication_precision_state"],
            "consensus_hash": _content_hash(consensus),
            "calculation_hash": _content_hash(calculation),
            "diff_hash": _content_hash(diff),
            "provenance_hash": _content_hash(provenance),
            "transaction_hash": _content_hash(transaction),
        }

    if card is None:
        if any(artifact is not None for artifact in (critique, consensus, calculation, diff, transaction)):
            return {
                "status": "invalid",
                **base,
                "precision_state": None,
                "error": "valuation publication artifacts are incomplete",
            }
        return {
            "status": "invalid" if card_error is not None else "incomplete",
            **base,
            "precision_state": None,
        }

    if critique is None:
        if any(artifact is not None for artifact in (consensus, calculation, diff, transaction)):
            return {
                "status": "invalid", **base, "precision_state": None,
                "error": "估值批判工件缺失",
            }
        return {"status": "critique-missing", **base, "precision_state": None}
    try:
        preview = valuation_consensus.aggregate_reviewer_card(valuation_input, card, critique)
    except (ContractError, valuation_consensus.ValuationConsensusError) as exc:
        return {"status": "invalid", **base, "precision_state": None, "error": str(exc)}
    if consensus is None:
        if any(artifact is not None for artifact in (calculation, diff, transaction)):
            return {
                "status": "invalid", **base,
                "precision_state": preview["publication_precision_state"],
                "error": "valuation publication artifacts are incomplete",
            }
        return {"status": "ready", **base,
                "precision_state": preview["publication_precision_state"]}
    precision_state = preview["publication_precision_state"]
    try:
        expected = valuation_consensus.aggregate_reviewer_card(valuation_input, card, critique)
        if (valuation_consensus.canonical_json_bytes(expected)
                != valuation_consensus.canonical_json_bytes(consensus)):
            raise ContractError("consensus assumptions do not match frozen valuation artifacts")
        precision_state = consensus["publication_precision_state"]
        if precision_state in {"supported", "conditional", "low-confidence"}:
            if calculation is None:
                raise ContractError("publishable consensus requires calculation")
            _validate_calculation_against_sources(valuation_input, consensus, calculation, diff)
        elif calculation is not None:
            raise ContractError("suppressed consensus must not have a calculation")
        elif diff is not None:
            raise ContractError("suppressed consensus must not have a valuation diff")
        artifacts = {
            "input.json": valuation_input,
            "reviewer-1.json": card,
            "critique.json": critique,
            "consensus-assumptions.json": consensus,
            **({"calculation.json": calculation} if calculation is not None else {}),
            **({"valuation-diff.json": diff} if diff is not None else {}),
        }
        _validate_transaction_marker(transaction, "aggregate", artifacts)
    except (ContractError, StateError) as exc:
        return {"status": "invalid", **base, "precision_state": precision_state, "error": str(exc)}
    final_status = {
        "consensus": "complete",
        "conditional-consensus": "complete-conditional",
        "low-confidence-consensus": "complete-low-confidence",
    }.get(consensus["status"], "evidence-insufficient")
    return {
        "status": final_status,
        **base,
        "market_position_status": "available" if "current_price" in valuation_input["market"] else "unavailable",
        "precision_state": precision_state,
        "consensus_hash": _content_hash(consensus),
        "calculation_hash": None if calculation is None else _content_hash(calculation),
        "diff_hash": None if diff is None else _content_hash(diff),
        "provenance_hash": None,
        "transaction_hash": _content_hash(transaction),
    }


def _status_guidance(result: dict) -> dict:
    status = result["status"]
    if status in {"complete", "recalculated", "complete-conditional", "complete-low-confidence"}:
        if result.get("market_position_status") == "unavailable":
            issue_type, next_action = "market-position-unavailable", "价值区间已完成；当前价格位置暂不可判定，仅在取得可核验股价后另开 run 补算。"
        elif status == "complete-low-confidence":
            issue_type, next_action = "none", "参考区间已完成；只能呈现区间，不得给出方向结论，正文须声明“区间不具备方向判断力”。"
        else:
            issue_type, next_action = "none", "估值区间已完成；从 calculation.json 读取区间、精度状态及当前价格位置。"
    elif status == "not-frozen":
        issue_type, next_action = "input-not-frozen", "修正估值输入，完成双预检并冻结共同事实快照。"
    elif status == "incomplete":
        issue_type, next_action = "missing-card", "补齐缺失的真实估值卡草稿；保持冻结输入不变。"
    elif status == "critique-missing":
        issue_type, next_action = "critique-missing", "由估值批判者产出批判工件并运行 install-critique；估值者按批判在原槽位修订草稿后再安装。"
    elif status == "ready":
        issue_type, next_action = "aggregation-pending", "估值卡与批判工件有效；运行 aggregate 生成具体估值区间。"
    elif status == "evidence-insufficient":
        issue_type, next_action = "economic-basis-insufficient", "核对候选方法、事实依据和情景计算；没有可计算方法时补证，不得编造价格或参数。"
    else:
        if any(slot["state"] == "invalid" for slot in result.get("slots", [])):
            issue_type, next_action = "card-format", "请提议者修正估值卡的格式或事实引用，再预检。"
        else:
            issue_type, next_action = "artifact-invalid", "根据 error 修复输入或估值工件；格式错误不代表经济证据不足。"
    return {**result, "issue_type": issue_type, "next_action": next_action}


def status(run_dir: str) -> dict:
    """Public read-only status for the run lifecycle (company_run entry)."""
    return _status(argparse.Namespace(run_dir=run_dir))


def _dispatch(args: argparse.Namespace) -> dict:
    if args.command == "unit-standard":
        currency = _currency_code(args.currency, "currency")
        if currency == "RMB":
            raise ContractError("renminbi currency code must be CNY")
        return valuation_calculator.unit_standard(currency)
    if args.command == "preflight-input":
        return _preflight_input(args)
    if args.command == "freeze":
        return _freeze(args)
    if args.command == "preflight-card":
        return _preflight_card(args)
    if args.command == "install-card":
        return _install_card(args)
    if args.command == "install-critique":
        return _install_critique(args)
    if args.command == "aggregate":
        return _aggregate(args)
    if args.command == "recalculate":
        return _recalculate(args)
    if args.command == "status":
        return _status_guidance(_status(args))
    raise UsageError("unknown command")


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    debug = False
    if "--debug" in arguments:
        arguments.remove("--debug")
        debug = True
    try:
        result = _dispatch(_build_parser().parse_args(arguments))
    except HelpRequested as exc:
        _write_json(sys.stdout, {"help": str(exc)})
        return 0
    except (StateError, artifact_store.StateError) as exc:
        _write_json(sys.stderr, _json_error("StateError", str(exc), **exc.details))
        return 2
    except (UsageError, ContractError, artifact_store.ContractError) as exc:
        _write_json(sys.stderr, _json_error(exc.__class__.__name__, str(exc)))
        return 2
    except Exception:
        _write_json(sys.stderr, _json_error("InternalError", "unexpected valuation failure"))
        if debug:
            traceback.print_exc(file=sys.stderr)
        return 1
    _write_json(sys.stdout, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
