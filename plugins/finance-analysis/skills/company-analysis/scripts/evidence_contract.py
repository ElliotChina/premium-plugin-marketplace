"""Validation contracts for frozen facts and their registered source files."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
import hashlib
import json
from pathlib import Path
import re


FACT_SNAPSHOT_SCHEMA = "company-analysis-fact-snapshot-v1"
FACT_STATUSES = frozenset({"verified", "unverified"})
FACT_KEYS = (
    "fact_id", "metric", "value", "unit", "currency", "period",
    "consolidation_scope", "source_material_id", "source_locator",
    "audit_status", "methodology", "comparability", "fact_type",
    "replaces_fact_id", "content_hash", "status",
)
REQUIRED_FACT_KEYS = tuple(key for key in FACT_KEYS if key != "content_hash")
AUDIT_STATUSES = frozenset({"audited", "unaudited", "not-applicable"})
FACT_TYPES = frozenset({"disclosed", "derived", "assumption"})
LOWER_HEX = frozenset("0123456789abcdef")
REGISTERED_SOURCE_ID = re.compile(r"S(?:[0-9a-f]{12}|[1-9][0-9]*)\Z")
SOURCE_CONTRACT = "registered-v1"


class EvidenceError(ValueError):
    """Raised when a frozen evidence snapshot is malformed."""


def canonical_json_bytes(data: object) -> bytes:
    """Serialize data in the canonical form used by evidence contracts."""
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    return (text + "\n").encode("utf-8")


def content_hash(data: object) -> str:
    """Return the SHA-256 digest of canonical JSON data."""
    return hashlib.sha256(canonical_json_bytes(data)).hexdigest()


def fact_snapshot_hash(data: Mapping) -> str:
    """Hash a fact snapshot without its self-referential hash field."""
    _mapping(data, "fact snapshot")
    content = dict(data)
    content.pop("fact_snapshot_hash", None)
    return content_hash(content)


def validate_fact_records(facts: object, field: str = "fact snapshot.facts") -> Mapping[str, Mapping]:
    """Validate frozen fact records and return them keyed by fact_id."""
    if not isinstance(facts, list):
        raise EvidenceError(f"{field} must be a list")
    fact_ids: dict[str, Mapping] = {}
    replacement_links: list[tuple[int, str]] = []
    for index, fact in enumerate(facts):
        fact_id, replaces_fact_id, item = _validate_fact(fact, index, field)
        if fact_id in fact_ids:
            raise EvidenceError(f"{field} contains duplicate fact_id")
        fact_ids[fact_id] = item
        if replaces_fact_id is not None:
            replacement_links.append((index, replaces_fact_id))
    for index, replaces_fact_id in replacement_links:
        if replaces_fact_id not in fact_ids:
            raise EvidenceError(f"{field}[{index}].replaces_fact_id must reference a fact in the same snapshot")
    return fact_ids


def validate_fact_snapshot(data: Mapping) -> Mapping:
    """Validate an immutable fact snapshot and its content hash."""
    snapshot = _exact_keys(data, (
        "schema_version", "fact_snapshot_id", "fact_snapshot_hash", "facts",
    ), "fact snapshot")
    if snapshot["schema_version"] != FACT_SNAPSHOT_SCHEMA:
        raise EvidenceError("fact snapshot.schema_version is not supported")
    _non_empty_string(snapshot["fact_snapshot_id"], "fact snapshot.fact_snapshot_id")
    _sha256_hex(snapshot["fact_snapshot_hash"], "fact snapshot.fact_snapshot_hash")
    validate_fact_records(snapshot["facts"])
    if snapshot["fact_snapshot_hash"] != fact_snapshot_hash(snapshot):
        raise EvidenceError("fact snapshot.fact_snapshot_hash does not match canonical snapshot content")
    return data


def validate_peer_fact_snapshot_binding(
    peer_input_path: Path, expected_fact_snapshot_id: str, expected_facts: object | None = None,
) -> None:
    """Require an existing sibling subsystem input to use the same frozen facts."""
    if not isinstance(expected_fact_snapshot_id, str) or not expected_fact_snapshot_id.strip():
        raise EvidenceError("expected fact_snapshot_id must be a non-empty string")
    path = Path(peer_input_path)
    for directory in (path.parent.parent, path.parent):
        if directory.is_symlink():
            raise EvidenceError("peer analysis input path must not contain symlinks")
    if not path.exists():
        return
    if path.is_symlink() or not path.is_file():
        raise EvidenceError("peer analysis input must be a regular file")
    try:
        peer_input = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError("peer analysis input must be valid JSON") from exc
    peer_mapping = _mapping(peer_input, "peer analysis input")
    peer_fact_snapshot_id = _non_empty_string(
        peer_mapping.get("fact_snapshot_id"),
        "peer analysis input.fact_snapshot_id",
    )
    if peer_fact_snapshot_id != expected_fact_snapshot_id:
        raise EvidenceError("scoring and valuation must use the same fact_snapshot_id in one run")
    if expected_facts is not None and "facts" in peer_mapping:
        if canonical_json_bytes(peer_mapping["facts"]) != canonical_json_bytes(expected_facts):
            raise EvidenceError("scoring and valuation must use identical facts in one run")


def preflight_shared_facts(run_dir: Path, input_data: Mapping, peer_name: str) -> dict:
    """Audit registered sources and bind scoring and valuation to the same facts."""
    if peer_name not in {"scoring", "valuation"}:
        raise EvidenceError("peer_name must be scoring or valuation")
    source_audit = audit_managed_fact_sources(run_dir, input_data["facts"])
    if source_audit["errors"]:
        raise EvidenceError("source preflight failed: " + "; ".join(source_audit["errors"]))
    validate_peer_fact_snapshot_binding(
        run_dir / "analysis" / peer_name / "input.json",
        input_data["fact_snapshot_id"],
        input_data["facts"],
    )
    return source_audit


def audit_source_ids(manifest: Path, source_ids: Iterable[str]) -> dict:
    """Hash only the registered local originals requested by the caller."""
    ids = sorted(set(source_ids))
    result = {"checked_sources": ids, "url_only_sources": [], "errors": []}
    if not ids:
        return result
    if not manifest.is_file():
        result["errors"].append("sources.json is missing for referenced facts or report citations")
        return result
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        result["errors"].append(f"sources.json cannot be read: {exc}")
        return result
    entries = data.get("sources") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        result["errors"].append("sources.json requires a sources list")
        return result
    by_id: dict[str, list[Mapping]] = {}
    for entry in entries:
        if isinstance(entry, Mapping) and isinstance(entry.get("id"), str):
            by_id.setdefault(entry["id"], []).append(entry)
    company_dir = manifest.parent.resolve()
    for source_id in ids:
        found = by_id.get(source_id, [])
        if len(found) != 1:
            problem = "not registered" if not found else "registered more than once"
            result["errors"].append(f"source {source_id} is {problem} in sources.json")
            continue
        entry = found[0]
        stored = entry.get("file")
        if stored is None:
            if isinstance(entry.get("url"), str) and entry["url"].strip():
                result["url_only_sources"].append(source_id)
            else:
                result["errors"].append(f"source {source_id} has neither a file nor a URL")
            continue
        if not isinstance(stored, str) or not stored or Path(stored).is_absolute():
            result["errors"].append(f"source {source_id} has an invalid relative file path")
            continue
        original = (company_dir / stored).resolve()
        if not original.is_relative_to(company_dir):
            result["errors"].append(f"source {source_id} file escapes the company directory")
        elif not original.is_file():
            result["errors"].append(f"source {source_id} file is missing: {stored}")
        elif not isinstance(entry.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
            result["errors"].append(f"source {source_id} has no valid registered SHA-256")
        else:
            digest = hashlib.sha256()
            try:
                with original.open("rb") as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b""):
                        digest.update(block)
            except OSError as exc:
                result["errors"].append(f"source {source_id} file cannot be read: {exc}")
                continue
            if digest.hexdigest() != entry["sha256"]:
                result["errors"].append(f"source {source_id} file changed since registration: {stored}")
    return result


def referenced_fact_source_ids(facts: Iterable[Mapping]) -> list[str]:
    """List registered-looking provenance, including downgraded evidence leads."""
    return sorted({
        fact["source_material_id"] for fact in facts
        if (fact["fact_type"] == "disclosed" and fact["status"] == "verified")
        or REGISTERED_SOURCE_ID.fullmatch(fact["source_material_id"])
    })


def verified_fact_source_ids(facts: Iterable[Mapping]) -> list[str]:
    """Require intact origins only for facts still presented as verified."""
    return sorted({
        fact["source_material_id"] for fact in facts
        if fact["status"] == "verified" and (
            fact["fact_type"] == "disclosed"
            or REGISTERED_SOURCE_ID.fullmatch(fact["source_material_id"])
        )
    })


def audit_managed_fact_sources(run_dir: Path, facts: Iterable[Mapping]) -> dict:
    """Bind verified disclosures in new runs to registered originals before freeze."""
    metadata = run_dir / "run.json"
    if not metadata.is_file():
        raise EvidenceError("run.json is missing; the fact source audit cannot be skipped")
    try:
        run = json.loads(metadata.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"run.json cannot be read: {exc}") from exc
    if not isinstance(run, Mapping) or run.get("source_contract") != SOURCE_CONTRACT:
        raise EvidenceError("run.json source_contract must be registered-v1; the fact source audit is mandatory")
    facts = list(facts)
    manifest = run_dir.parent.parent / "sources.json"
    required = set(verified_fact_source_ids(facts))
    leads = set(referenced_fact_source_ids(facts)) - required
    result = audit_source_ids(manifest, required)
    lead_audit = audit_source_ids(manifest, leads)
    return {
        "enabled": True,
        **result,
        "unverified_source_ids": sorted(leads),
        "warnings": [f"未核验线索来源待补：{error}" for error in lead_audit["errors"]],
    }


def _mapping(value: object, field: str) -> Mapping:
    if not isinstance(value, Mapping):
        raise EvidenceError(f"{field} must be a mapping")
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
        raise EvidenceError(f"{field} has invalid keys: " + "; ".join(details))
    return mapping


def _non_empty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"{field} must be a non-empty string")
    return value


def _nullable_non_empty_string(value: object, field: str) -> str | None:
    if value is None:
        return None
    return _non_empty_string(value, field)


def _fact_value(value: object, field: str, *, status: str) -> object:
    # Scoring and valuation share one frozen snapshot byte-for-byte: numeric
    # facts carry decimal strings, qualitative facts carry non-empty text.
    if value is None:
        if status == "verified":
            raise EvidenceError(f"{field} must not be null for verified facts")
        return value
    if isinstance(value, str) and value.strip():
        return value
    raise EvidenceError(
        f"{field} must be a non-empty string (numeric facts use decimal strings) or null; "
        "bool and number values are rejected"
    )


def _currency_code(value: object, field: str) -> str | None:
    currency = _nullable_non_empty_string(value, field)
    if currency is None:
        return None
    if len(currency) != 3 or any(character < "A" or character > "Z" for character in currency):
        raise EvidenceError(f"{field} must be a three-letter uppercase code")
    return currency


def _sha256_hex(value: object, field: str) -> str:
    digest = _non_empty_string(value, field)
    if len(digest) != 64 or any(character not in LOWER_HEX for character in digest):
        raise EvidenceError(f"{field} must be a 64-character lowercase SHA-256 hex digest")
    return digest


def _validate_fact(fact: object, index: int, field_prefix: str) -> tuple[str, str | None, Mapping]:
    field = f"{field_prefix}[{index}]"
    item = _mapping(fact, field)
    missing = set(REQUIRED_FACT_KEYS) - set(item)
    extra = set(item) - set(FACT_KEYS)
    if missing or extra:
        raise EvidenceError(
            f"{field} has invalid keys: "
            + "; ".join(filter(None, (
                "missing " + ", ".join(sorted(missing)) if missing else "",
                "unexpected " + ", ".join(sorted(map(str, extra))) if extra else "",
            )))
        )
    fact_id = _non_empty_string(item["fact_id"], f"{field}.fact_id")
    for key in (
        "metric", "period", "consolidation_scope", "source_material_id",
        "source_locator", "methodology", "comparability",
    ):
        _non_empty_string(item[key], f"{field}.{key}")
    status = _non_empty_string(item["status"], f"{field}.status")
    if status not in FACT_STATUSES:
        raise EvidenceError(f"{field}.status is not supported")
    _fact_value(item["value"], f"{field}.value", status=status)
    _nullable_non_empty_string(item["unit"], f"{field}.unit")
    _currency_code(item["currency"], f"{field}.currency")
    audit_status = _non_empty_string(item["audit_status"], f"{field}.audit_status")
    if audit_status not in AUDIT_STATUSES:
        raise EvidenceError(f"{field}.audit_status is not supported")
    fact_type = _non_empty_string(item["fact_type"], f"{field}.fact_type")
    if fact_type not in FACT_TYPES:
        raise EvidenceError(f"{field}.fact_type is not supported")
    if fact_type == "assumption":
        if status != "unverified":
            raise EvidenceError(f"{field}: assumption facts must have status unverified")
        if audit_status != "not-applicable":
            raise EvidenceError(f"{field}: assumption facts must have audit_status not-applicable")
    replaces_fact_id = _nullable_non_empty_string(item["replaces_fact_id"], f"{field}.replaces_fact_id")
    if replaces_fact_id == fact_id:
        raise EvidenceError(f"{field}.replaces_fact_id must identify another fact")
    if "content_hash" in item:
        _sha256_hex(item["content_hash"], f"{field}.content_hash")
    return fact_id, replaces_fact_id, item
