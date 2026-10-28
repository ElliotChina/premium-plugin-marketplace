"""Safely persist run-local inputs, scorecards, and scoring consensus."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import traceback
from collections.abc import Mapping
from typing import NoReturn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import artifact_store
import evidence_contract
import scoring_consensus


TERMINAL_RUN_STATUSES = frozenset({"completed", "aborted", "superseded"})

_SCRIPT_DIR = Path(__file__).resolve().parent
_RUBRIC_PATH = _SCRIPT_DIR.parent.parent / "references" / "scoring" / "scoring-rubric-v1.json"
_BUNDLED_RUBRIC: Mapping | None = None


def _bundled_rubric() -> Mapping:
    global _BUNDLED_RUBRIC
    rubric = _BUNDLED_RUBRIC
    if rubric is None:
        try:
            with _RUBRIC_PATH.open("r", encoding="utf-8") as _rubric_file:
                rubric = json.load(_rubric_file)
        except (OSError, ValueError) as exc:
            raise ContractError(f"bundled scoring rubric missing or corrupt: {exc}") from exc
        _BUNDLED_RUBRIC = rubric
    return rubric


class UsageError(ValueError):
    """Raised for malformed command-line usage."""


class ContractError(ValueError):
    """Raised for invalid scoring input or files."""


class StateError(ValueError):
    """Raised when an otherwise-valid operation is unavailable in this state."""

    def __init__(self, message: str, **details: object) -> None:
        super().__init__(message)
        self.details = details


class InputNotFrozen(StateError):
    """Raised when the scoring input has not been frozen yet."""


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
    payload = scoring_consensus.canonical_json_bytes(value)
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
    parser = JsonArgumentParser(prog="company_scoring.py")
    _add_help(parser)
    commands = parser.add_subparsers(dest="command", required=True, parser_class=JsonArgumentParser)

    for command in ("preflight-input", "freeze"):
        freeze = commands.add_parser(command)
        _add_help(freeze)
        freeze.add_argument("--run-dir", required=True)
        freeze.add_argument("--fact-snapshot", required=True)
        freeze.add_argument("--rubric", required=True)
        freeze.add_argument("--evidence-coverage", required=True)
        freeze.add_argument("--model-version", required=True)

    install = commands.add_parser("install-card")
    _add_help(install)
    install.add_argument("--run-dir", required=True)
    install.add_argument("--card", required=True)

    single = commands.add_parser("preflight-card")
    _add_help(single)
    single.add_argument("--run-dir", required=True)
    single.add_argument("--card", required=True)

    aggregate = commands.add_parser("aggregate")
    _add_help(aggregate)
    aggregate.add_argument("--run-dir", required=True)

    status = commands.add_parser("status")
    _add_help(status)
    status.add_argument("--run-dir", required=True)
    return parser


def _absolute_without_symlink(value: str, label: str, *, directory: bool) -> Path:
    path = Path(value).expanduser()
    absolute = Path(os.path.abspath(path))
    if not absolute.exists():
        raise ContractError(f"{label} must exist")
    if absolute.is_symlink() or absolute.resolve() != absolute:
        raise ContractError(f"{label} must not be a symlink")
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
    if not isinstance(data, Mapping):
        raise ContractError(f"{label} must be a JSON object")
    return data


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
    if not isinstance(data, Mapping):
        raise ContractError("run metadata must be a JSON object")
    return data


def _assert_mutable(run_dir: Path) -> None:
    metadata = _read_run_json(run_dir)
    if metadata is not None and metadata.get("status") in TERMINAL_RUN_STATUSES:
        raise StateError("terminal runs cannot be changed")


def _safe_scoring_dir(run_dir: Path, *, create: bool) -> Path:
    scoring = run_dir / "analysis" / "scoring"
    if create:
        descriptor, _identity = artifact_store.open_stable_dir(scoring, create=True)
        os.close(descriptor)
        return scoring
    analysis = scoring.parent
    for directory in (analysis, scoring):
        if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
            raise ContractError("scoring directory must not be a symlink")
        if not directory.exists():
            return scoring
    return scoring


def _safe_artifact(scoring_dir: Path, name: str) -> Path:
    path = scoring_dir / name
    try:
        path.relative_to(scoring_dir)
    except ValueError as exc:
        raise ContractError("artifact path escapes the run directory") from exc
    if path.is_symlink():
        raise ContractError("installed scoring artifact must not be a symlink")
    return path


def _load_artifact_json(scoring_dir: Path, name: str) -> Mapping | None:
    path = _safe_artifact(scoring_dir, name)
    if not path.exists():
        return None
    if not path.is_file():
        raise ContractError(f"installed scoring artifact {name} must be a regular file")
    try:
        data = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractError(f"installed scoring artifact {name} must be valid JSON") from exc
    if not isinstance(data, Mapping):
        raise ContractError(f"installed scoring artifact {name} must be a JSON object")
    return data


def _input_from_sources(
    facts: Mapping, rubric: Mapping, evidence_coverage: Mapping, model_version: str,
) -> dict:
    if rubric != _bundled_rubric():
        raise ContractError("rubric must match the bundled scoring rubric exactly")
    fact_snapshot_id = facts.get("fact_snapshot_id")
    raw_facts = facts.get("facts")
    if not isinstance(fact_snapshot_id, str) or not fact_snapshot_id.strip():
        raise ContractError("fact snapshot ID must be a non-empty string")
    if not isinstance(raw_facts, list):
        raise ContractError("fact snapshot facts must be a list")
    fact_ids: set[str] = set()
    for fact in raw_facts:
        if not isinstance(fact, Mapping) or not isinstance(fact.get("fact_id"), str) or not fact["fact_id"].strip():
            raise ContractError("each fact must have a non-empty fact_id")
        if fact["fact_id"] in fact_ids:
            raise ContractError("fact snapshot contains duplicate fact IDs")
        fact_ids.add(fact["fact_id"])
    if set(rubric) != {"schema_version", "rubric_version", "axes"}:
        raise ContractError("rubric has an unsupported schema")
    if rubric.get("schema_version") != "company-analysis-scoring-rubric-v1":
        raise ContractError("rubric schema is not supported")
    rubric_version = rubric.get("rubric_version")
    if not isinstance(rubric_version, str) or not rubric_version.strip():
        raise ContractError("rubric version must be a non-empty string")
    if not isinstance(rubric.get("axes"), list):
        raise ContractError("rubric axes must be a list")
    if not isinstance(model_version, str) or not model_version.strip():
        raise UsageError("model version must be a non-empty string")
    data = {
        "schema_version": scoring_consensus.INPUT_SCHEMA,
        "rubric_version": rubric_version,
        "fact_snapshot_id": fact_snapshot_id,
        "model_version": model_version,
        "scoring_input_hash": "pending",
        "facts": list(raw_facts),
        "axes": rubric["axes"],
        "evidence_coverage": dict(evidence_coverage),
    }
    data["scoring_input_hash"] = scoring_consensus.scoring_input_hash(data)
    try:
        scoring_consensus.validate_scoring_input(data)
    except scoring_consensus.ScoringError as exc:
        raise ContractError(str(exc)) from exc
    return data


def _load_input(scoring_dir: Path) -> Mapping:
    data = _load_artifact_json(scoring_dir, "input.json")
    if data is None:
        raise InputNotFrozen("scoring input has not been frozen")
    try:
        scoring_consensus.validate_scoring_input(data)
    except scoring_consensus.ScoringError as exc:
        raise ContractError(str(exc)) from exc
    return data


def _card(scoring_dir: Path, scoring_input: Mapping, *, strict: bool) -> tuple[Mapping | None, str | None]:
    try:
        card = _load_artifact_json(scoring_dir, "scorer-1.json")
        if card is not None:
            scoring_consensus.validate_scorecard(card, scoring_input)
            if card.get("scorer_id") != "scorer-1":
                raise ContractError("scorecard scorer_id must be scorer-1")
        return card, None
    except (ContractError, scoring_consensus.ScoringError) as exc:
        if strict:
            raise ContractError(str(exc)) from exc
        return None, str(exc)


def _invalid_status(error: str) -> dict:
    """Return a diagnostic result when the scoring tree itself is unsafe to read."""
    return {
        "status": "invalid",
        "scoring_input_hash": None,
        "valid_cards": 0,
        "slots": [{"slot": 1, "state": "missing", "scorer_id": None, "error": None}],
        "missing_slots": [1],
        "affected_axis_scores": {},
        "consensus_hash": None,
        "error": error,
    }


def _freeze(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    facts = _source_json(args.fact_snapshot, "fact snapshot")
    rubric = _source_json(args.rubric, "rubric")
    evidence_coverage = _source_json(args.evidence_coverage, "evidence coverage")
    scoring_dir = _safe_scoring_dir(run_dir, create=True)
    existing = _load_artifact_json(scoring_dir, "input.json")
    if existing is not None:
        try:
            scoring_consensus.validate_scoring_input(existing)
        except scoring_consensus.ScoringError as exc:
            raise ContractError(str(exc)) from exc
    input_data = _input_from_sources(facts, rubric, evidence_coverage, args.model_version)
    try:
        source_audit = evidence_contract.preflight_shared_facts(run_dir, input_data, "valuation")
    except evidence_contract.EvidenceError as exc:
        raise ContractError(str(exc)) from exc
    artifact_store.atomic_install(scoring_dir, "input.json", input_data)
    result = {"status": "frozen", "scoring_input_hash": input_data["scoring_input_hash"],
              "coverage_warnings": _coverage_warnings(input_data["evidence_coverage"])}
    if source_audit["enabled"]:
        result["source_audit"] = source_audit
    return result


def _preflight_input(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    input_data = _input_from_sources(
        _source_json(args.fact_snapshot, "fact snapshot"),
        _source_json(args.rubric, "rubric"),
        _source_json(args.evidence_coverage, "evidence coverage"),
        args.model_version,
    )
    try:
        source_audit = evidence_contract.preflight_shared_facts(run_dir, input_data, "valuation")
    except evidence_contract.EvidenceError as exc:
        raise ContractError(str(exc)) from exc
    _preflight_install(_safe_scoring_dir(run_dir, create=False), "input.json", input_data)
    result = {"status": "ready", "fact_snapshot_id": input_data["fact_snapshot_id"],
              "scoring_input_hash": input_data["scoring_input_hash"],
              "coverage_warnings": _coverage_warnings(input_data["evidence_coverage"])}
    if source_audit["enabled"]:
        result["source_audit"] = source_audit
    return result


def _coverage_warnings(coverage: Mapping) -> list[str]:
    """Flag suspicious evidence mapping without treating missing data as a blocker."""
    dimensions = coverage["dimensions"]
    warnings = []
    if all(item["assessment"] == "inference-required" for item in dimensions):
        warnings.append("全部评分维度均需推断；请逐维复核已核验事实是否足以直接支持部分判断")
    groups: dict[tuple, list[str]] = {}
    for item in dimensions:
        signature = (tuple(item["evidence_fact_ids"]), tuple(item["missing_evidence"]))
        groups.setdefault(signature, []).append(item["dimension_id"])
    repeated = [ids for ids in groups.values() if len(ids) >= 4]
    if repeated:
        warnings.append("多个不同维度复用完全相同的事实和缺口：" + "；".join(", ".join(ids) for ids in repeated))
    return warnings


def _preflight_card(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    scoring_input = _load_input(_safe_scoring_dir(run_dir, create=False))
    card = _source_json(args.card, "scorecard")
    try:
        scoring_consensus.validate_scorecard(card, scoring_input)
    except scoring_consensus.ScoringError as exc:
        raise StateError(str(exc), issue_type="card-format") from exc
    if card.get("scorer_id") != "scorer-1":
        raise ContractError("scorecard scorer_id must be scorer-1")
    return {"status": "ready", "scoring_input_hash": scoring_input["scoring_input_hash"]}


def _aggregate(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    scoring_dir = _safe_scoring_dir(run_dir, create=False)
    scoring_input = _load_input(scoring_dir)
    card, _ = _card(scoring_dir, scoring_input, strict=True)
    if card is None:
        raise StateError("需要先安装有效的 scorer-1 评分卡")
    try:
        consensus = scoring_consensus.aggregate_scorecard_v3(scoring_input, card)
    except scoring_consensus.ScoringError as exc:
        raise ContractError(str(exc)) from exc
    artifact_store.atomic_install(scoring_dir, "consensus.json", consensus)
    return {
        "status": "aggregated",
        "scoring_input_hash": scoring_input["scoring_input_hash"],
        "consensus_hash": scoring_consensus.content_hash(consensus),
    }


def _install_card(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    _assert_mutable(run_dir)
    scoring_dir = _safe_scoring_dir(run_dir, create=False)
    scoring_input = _load_input(scoring_dir)
    card = _source_json(args.card, "scorecard")
    try:
        scoring_consensus.validate_scorecard(card, scoring_input)
    except scoring_consensus.ScoringError as exc:
        raise ContractError(str(exc)) from exc
    if card.get("scorer_id") != "scorer-1":
        raise ContractError("scorecard scorer_id must be scorer-1")
    _card(scoring_dir, scoring_input, strict=True)
    artifact_store.atomic_install(scoring_dir, "scorer-1.json", card)
    return {"status": "installed", "scorer_id": card["scorer_id"]}


def _preflight_install(scoring_dir: Path, name: str, data: Mapping) -> None:
    path = _safe_artifact(scoring_dir, name)
    payload = scoring_consensus.canonical_json_bytes(data)
    if path.exists():
        if path.is_symlink() or not path.is_file() or path.read_bytes() != payload:
            raise StateError("immutable scoring artifact conflicts with existing content")


def _status(args: argparse.Namespace) -> dict:
    run_dir = _run_dir(args.run_dir)
    try:
        scoring_dir = _safe_scoring_dir(run_dir, create=False)
    except ContractError as exc:
        return _invalid_status(str(exc))
    input_data = None
    input_error = None
    not_frozen = False
    try:
        input_data = _load_input(scoring_dir)
    except InputNotFrozen as exc:
        not_frozen = True
        input_error = str(exc)
    except (ContractError, StateError) as exc:
        input_error = str(exc)
    if input_data is None:
        present = False
        try:
            present = _load_artifact_json(scoring_dir, "scorer-1.json") is not None
        except ContractError:
            present = True
        return {
            "status": "invalid" if present else ("not-frozen" if not_frozen else "invalid"),
            "scoring_input_hash": None,
            "valid_cards": 0,
            "missing_slots": [1],
            "slots": [{"slot": 1, "state": "invalid" if present else "missing", "scorer_id": None,
                       "error": input_error if present else None}],
            "affected_axis_scores": {},
            "consensus_hash": None,
        }
    card, card_error = _card(scoring_dir, input_data, strict=False)
    slots = [{"slot": 1,
              "state": "valid" if card is not None else ("invalid" if card_error is not None else "missing"),
              "scorer_id": card["scorer_id"] if card is not None else None,
              "error": card_error}]
    axis_scores = {axis["axis_id"]: None for axis in input_data["axes"]}
    base = {
        "scoring_input_hash": input_data["scoring_input_hash"],
        "slots": slots,
        "affected_axis_scores": axis_scores,
    }
    if card is None:
        return base | {
            "status": "invalid" if card_error is not None else "incomplete",
            "valid_cards": 0,
            "missing_slots": [1],
        }
    try:
        preview = scoring_consensus.aggregate_scorecard_v3(input_data, card)
    except scoring_consensus.ScoringError as exc:
        return base | {"status": "invalid", "valid_cards": 1, "missing_slots": [], "error": str(exc)}
    for axis in preview["axes"]:
        axis_scores[axis["axis_id"]] = axis["score"]
    persisted = None
    consensus_error = None
    try:
        persisted = _load_artifact_json(scoring_dir, "consensus.json")
    except ContractError as exc:
        consensus_error = str(exc)
    if persisted is None:
        if consensus_error is not None:
            return base | {
                "status": "invalid", "valid_cards": 1, "missing_slots": [],
                "error": consensus_error,
            }
        return base | {"status": "ready", "valid_cards": 1, "missing_slots": []}
    if consensus_error is None:
        try:
            expected = scoring_consensus.aggregate_scorecard_v3(input_data, card)
            if (scoring_consensus.canonical_json_bytes(expected)
                    != scoring_consensus.canonical_json_bytes(persisted)):
                consensus_error = "consensus does not match frozen scoring artifacts"
        except scoring_consensus.ScoringError as exc:
            consensus_error = str(exc)
    if consensus_error is not None:
        return base | {
            "status": "invalid", "valid_cards": 1, "missing_slots": [],
            "affected_axis_scores": {axis_id: None for axis_id in axis_scores},
            "consensus_hash": None, "error": consensus_error,
        }
    for axis in persisted["axes"]:
        axis_scores[axis["axis_id"]] = axis["score"]
    return base | {
        "status": "complete",
        "valid_cards": 1,
        "missing_slots": [],
        "consensus_hash": scoring_consensus.content_hash(persisted),
        "ambiguous_dimensions": persisted.get("ambiguous_dimensions", []),
    }


def _status_guidance(result: dict) -> dict:
    status = result["status"]
    if status == "complete":
        issue_type, next_action = "none", "评分共识已完成；读取共识结果和置信度。"
    elif status == "not-frozen":
        issue_type, next_action = "input-not-frozen", "完成评分与估值输入预检，确认同一事实快照后冻结评分输入。"
    elif status == "incomplete":
        issue_type, next_action = "missing-card", "补齐缺失的真实评分卡；保持冻结输入不变。"
    elif status == "ready":
        issue_type, next_action = "aggregation-pending", "评分卡有效；运行 aggregate 生成共识。"
    else:
        if any(slot["state"] == "invalid" for slot in result.get("slots", [])):
            issue_type, next_action = "card-format", "请评分者修正评分卡的格式或事实引用，再预检。"
        else:
            issue_type, next_action = "artifact-invalid", "根据 error 修复冻结输入或共识工件；不要将格式错误记为证据不足。"
    return {**result, "issue_type": issue_type, "next_action": next_action}


def status(run_dir: str) -> dict:
    """Public read-only status for the run lifecycle (company_run entry)."""
    return _status(argparse.Namespace(run_dir=run_dir))


def _dispatch(args: argparse.Namespace) -> dict:
    if args.command == "preflight-input":
        return _preflight_input(args)
    if args.command == "freeze":
        return _freeze(args)
    if args.command == "preflight-card":
        return _preflight_card(args)
    if args.command == "install-card":
        return _install_card(args)
    if args.command == "aggregate":
        return _aggregate(args)
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
        details = getattr(exc, "details", {})
        _write_json(sys.stderr, _json_error("StateError", str(exc), **details))
        return 2
    except (UsageError, ContractError, artifact_store.ContractError) as exc:
        _write_json(sys.stderr, _json_error(exc.__class__.__name__, str(exc)))
        return 2
    except Exception as exc:
        _write_json(sys.stderr, _json_error("InternalError", "unexpected scoring failure"))
        if debug:
            traceback.print_exc(file=sys.stderr)
        return 1
    _write_json(sys.stdout, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
