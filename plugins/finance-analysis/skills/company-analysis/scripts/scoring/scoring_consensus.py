"""Pure validation contracts for frozen scoring inputs and scorecards."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import evidence_contract as _evidence


INPUT_SCHEMA = "company-analysis-scoring-input-v2"
SCORECARD_SCHEMA = "company-analysis-scorecard-v3"
CONSENSUS_SCHEMA = "company-analysis-scoring-consensus-v3"
BAND_VALUES = frozenset({Decimal("0"), Decimal("25"), Decimal("50"), Decimal("75"), Decimal("100")})
ANCHOR_SCORES = frozenset({"0", "25", "50", "75", "100"})
EVIDENCE_STATUSES = frozenset({"verified", "inferred"})
SUPPLEMENTATION_STATUSES = frozenset({
    "not-needed", "completed", "exhausted", "not-cost-effective", "not-publicly-available",
})


def grade_band(score: float) -> str:
    """Return the fixed qualitative band for a score between zero and 100."""
    numeric = _score(score, "score", nullable=False)
    assert numeric is not None
    if numeric < Decimal("35"):
        return "very-poor"
    if numeric < Decimal("50"):
        return "poor"
    if numeric < Decimal("60"):
        return "weak"
    if numeric < Decimal("70"):
        return "medium"
    if numeric < Decimal("80"):
        return "good"
    if numeric < Decimal("90"):
        return "excellent"
    return "exceptional"


class ScoringError(ValueError):
    """Raised when a frozen scoring input or scorecard is malformed."""


def canonical_json_bytes(data: object) -> bytes:
    """Serialize data in the canonical form used by the scoring contracts."""
    return _evidence.canonical_json_bytes(data)


def content_hash(data: object) -> str:
    """Return the SHA-256 digest of canonical JSON data."""
    return _evidence.content_hash(data)


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


def _nullable_non_empty_string(value: object, field: str) -> str | None:
    return _translate_evidence_error(lambda: _evidence._nullable_non_empty_string(value, field))


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


def _score(value: object, field: str, *, nullable: bool) -> Decimal | None:
    if value is None and nullable:
        return None
    decimal = _decimal_number(value, field)
    if not Decimal("0") <= decimal <= Decimal("100"):
        raise ScoringError(f"{field} must be between 0 and 100")
    return decimal


def _string_list(value: object, field: str) -> list:
    if not isinstance(value, list):
        raise ScoringError(f"{field} must be a list")
    for index, item in enumerate(value):
        _non_empty_string(item, f"{field}[{index}]")
    return value


def _unique_strings(value: object, field: str) -> list:
    items = _string_list(value, field)
    if len(set(items)) != len(items):
        raise ScoringError(f"{field} must not contain duplicates")
    return items


def scoring_input_hash(data: Mapping) -> str:
    """Hash a scoring input without its self-referential hash field."""
    _mapping(data, "scoring input")
    content = dict(data)
    content.pop("scoring_input_hash", None)
    return content_hash(content)


def _validate_fact_records(facts: object, field: str) -> Mapping[str, Mapping]:
    return _translate_evidence_error(lambda: _evidence.validate_fact_records(facts, field=field))


def validate_scoring_input(data: Mapping) -> Mapping:
    """Validate the immutable scoring-rubric input and its content hash."""
    raw = _mapping(data, "scoring input")
    if raw.get("schema_version") != INPUT_SCHEMA:
        raise ScoringError("scoring input.schema_version is not supported")
    keys = (
        "schema_version", "rubric_version", "fact_snapshot_id", "model_version",
        "scoring_input_hash", "facts", "axes", "evidence_coverage",
    )
    scoring_input = _exact_keys(data, keys, "scoring input")
    for field in ("rubric_version", "fact_snapshot_id", "model_version", "scoring_input_hash"):
        _non_empty_string(scoring_input[field], f"scoring input.{field}")

    _validate_fact_records(scoring_input["facts"], field="scoring input.facts")

    axes = scoring_input["axes"]
    if not isinstance(axes, list) or not axes:
        raise ScoringError("scoring input.axes must be a non-empty list")
    axis_ids = set()
    dimension_ids = set()
    for axis_index, axis in enumerate(axes):
        axis_data = _exact_keys(axis, ("axis_id", "label", "dimensions"), f"scoring input.axes[{axis_index}]")
        axis_id = _non_empty_string(axis_data["axis_id"], f"scoring input.axes[{axis_index}].axis_id")
        if axis_id in axis_ids:
            raise ScoringError("scoring input.axes contains duplicate axis_id")
        axis_ids.add(axis_id)
        _non_empty_string(axis_data["label"], f"scoring input.axes[{axis_index}].label")
        dimensions = axis_data["dimensions"]
        if not isinstance(dimensions, list) or not dimensions:
            raise ScoringError(f"scoring input.axes[{axis_index}].dimensions must be a non-empty list")
        axis_weight = Decimal("0")
        for dimension_index, dimension in enumerate(dimensions):
            dimension_data = _exact_keys(dimension, (
                "dimension_id", "label", "weight", "anchors", "raw_metrics", "benchmarks",
                "applicability", "missing_data_rule", "cap_conditions", "overturning_evidence",
            ), f"scoring input.axes[{axis_index}].dimensions[{dimension_index}]")
            dimension_id = _non_empty_string(
                dimension_data["dimension_id"],
                f"scoring input.axes[{axis_index}].dimensions[{dimension_index}].dimension_id",
            )
            if dimension_id in dimension_ids:
                raise ScoringError("scoring input.axes contains duplicate dimension_id")
            dimension_ids.add(dimension_id)
            _non_empty_string(dimension_data["label"], "dimension.label")
            weight = _decimal_number(dimension_data["weight"], "dimension.weight")
            if weight < Decimal("0") or weight > Decimal("100"):
                raise ScoringError("dimension.weight must be between 0 and 100")
            axis_weight += weight
            anchors = _mapping(dimension_data["anchors"], "dimension.anchors")
            if set(anchors) != ANCHOR_SCORES:
                raise ScoringError("dimension.anchors must contain exactly 0, 25, 50, 75, and 100")
            for score, anchor in anchors.items():
                _non_empty_string(anchor, f"dimension.anchors[{score}]")
            for field in ("raw_metrics", "benchmarks", "cap_conditions", "overturning_evidence"):
                _string_list(dimension_data[field], f"dimension.{field}")
            for field in ("applicability", "missing_data_rule"):
                _non_empty_string(dimension_data[field], f"dimension.{field}")
        if axis_weight != Decimal("100"):
            raise ScoringError("dimension weights within each axis must total exactly 100")

    _validate_evidence_coverage(scoring_input["evidence_coverage"], scoring_input, dimension_ids)

    if scoring_input["scoring_input_hash"] != scoring_input_hash(scoring_input):
        raise ScoringError("scoring input.scoring_input_hash does not match canonical input content")
    return data


def _validate_evidence_coverage(value: object, scoring_input: Mapping, dimension_ids: set[str]) -> Mapping:
    coverage = _exact_keys(value, (
        "schema_version", "fact_snapshot_id", "rubric_version", "dimensions",
    ), "evidence_coverage")
    if coverage["schema_version"] != "company-analysis-evidence-coverage-v1":
        raise ScoringError("evidence_coverage.schema_version is not supported")
    for field in ("fact_snapshot_id", "rubric_version"):
        _non_empty_string(coverage[field], f"evidence_coverage.{field}")
        if coverage[field] != scoring_input[field]:
            raise ScoringError(f"evidence_coverage.{field} must match the scoring input")
    dimensions = coverage["dimensions"]
    if not isinstance(dimensions, list):
        raise ScoringError("evidence_coverage.dimensions must be a list")
    known_facts = _known_fact_ids(scoring_input)
    seen = set()
    for index, dimension in enumerate(dimensions):
        item = _exact_keys(dimension, (
            "dimension_id", "assessment", "evidence_fact_ids", "missing_evidence",
            "supplementation_status", "supplementation_notes",
        ), f"evidence_coverage.dimensions[{index}]")
        dimension_id = _non_empty_string(item["dimension_id"], "evidence_coverage.dimension_id")
        if dimension_id in seen or dimension_id not in dimension_ids:
            raise ScoringError("evidence_coverage.dimensions must contain each rubric dimension exactly once")
        seen.add(dimension_id)
        assessment = _non_empty_string(item["assessment"], "evidence_coverage.assessment")
        if assessment not in {"direct-sufficient", "inference-required"}:
            raise ScoringError("evidence_coverage.assessment is not supported")
        fact_ids = _rating_fact_ids(item["evidence_fact_ids"], "evidence_coverage.evidence_fact_ids", known_facts)
        if any(known_facts[fact_id] != "verified" for fact_id in fact_ids):
            raise ScoringError("evidence_coverage.evidence_fact_ids must reference verified facts")
        gaps = _string_list(item["missing_evidence"], "evidence_coverage.missing_evidence")
        supplementation = _non_empty_string(
            item["supplementation_status"], "evidence_coverage.supplementation_status"
        )
        if supplementation not in SUPPLEMENTATION_STATUSES:
            raise ScoringError("evidence_coverage.supplementation_status is not supported")
        _non_empty_string(item["supplementation_notes"], "evidence_coverage.supplementation_notes")
        if assessment == "direct-sufficient":
            if not fact_ids:
                raise ScoringError("direct-sufficient evidence_coverage requires evidence_fact_ids")
            if supplementation not in {"not-needed", "completed"}:
                raise ScoringError("direct-sufficient evidence_coverage has invalid supplementation_status")
        else:
            if not gaps:
                raise ScoringError("inference-required evidence_coverage requires missing_evidence")
            if supplementation == "not-needed":
                raise ScoringError("inference-required evidence_coverage requires a completed supplementation outcome")
    if seen != dimension_ids:
        raise ScoringError("evidence_coverage.dimensions must contain each rubric dimension exactly once")
    return coverage


def _known_fact_ids(scoring_input: Mapping) -> dict[str, str]:
    return {fact["fact_id"]: fact["status"] for fact in scoring_input["facts"]}


def _rating_fact_ids(value: object, field: str, known_facts: Mapping[str, str]) -> list:
    fact_ids = _unique_strings(value, field)
    unknown = [fact_id for fact_id in fact_ids if fact_id not in known_facts]
    if unknown:
        raise ScoringError(f"{field} must reference facts in the scoring input snapshot")
    return fact_ids


def _verified_evidence_fact_ids(value: object, field: str, known_facts: Mapping[str, str]) -> list:
    fact_ids = _rating_fact_ids(value, field, known_facts)
    if not fact_ids:
        raise ScoringError(f"{field} must not be empty")
    unverified = [fact_id for fact_id in fact_ids if known_facts[fact_id] != "verified"]
    if unverified:
        raise ScoringError(f"{field} must reference verified facts in the scoring input snapshot")
    return fact_ids


def _veto_output(veto: Mapping) -> dict:
    return {
        "code": veto["code"],
        "reason": veto["reason"],
        "evidence_fact_ids": sorted(veto["evidence_fact_ids"]),
    }


def validate_scorecard(card: Mapping, scoring_input: Mapping) -> Mapping:
    """Validate a scorecard against the frozen scoring input it cites."""
    validate_scoring_input(scoring_input)
    scorecard = _exact_keys(card, (
        "schema_version", "scorer_id", "rubric_version", "fact_snapshot_id",
        "scoring_input_hash", "model_id", "ratings",
    ), "scorecard")
    if scorecard["schema_version"] != SCORECARD_SCHEMA:
        raise ScoringError("scorecard.schema_version is not supported")
    for field in ("scorer_id", "rubric_version", "fact_snapshot_id", "scoring_input_hash", "model_id"):
        _non_empty_string(scorecard[field], f"scorecard.{field}")
    for scorecard_field, input_field in (
        ("rubric_version", "rubric_version"),
        ("fact_snapshot_id", "fact_snapshot_id"),
        ("scoring_input_hash", "scoring_input_hash"),
        ("model_id", "model_version"),
    ):
        if scorecard[scorecard_field] != scoring_input[input_field]:
            raise ScoringError(f"scorecard.{scorecard_field} must match the scoring input")

    return _validate_scorecard_v3(scorecard, scoring_input)


def _band_value(value: object, field: str) -> Decimal:
    decimal = _decimal_number(value, field)
    if decimal not in BAND_VALUES:
        raise ScoringError(f"{field} must be one of 0, 25, 50, 75, or 100")
    return decimal


def _validate_scorecard_v3(scorecard: Mapping, scoring_input: Mapping) -> Mapping:
    """Validate an anchored-band scorecard; every band must equal a frozen anchor value."""
    ratings = scorecard["ratings"]
    if not isinstance(ratings, list):
        raise ScoringError("scorecard.ratings must be a list")
    rubric_dimensions = {
        dimension["dimension_id"]: dimension
        for axis in scoring_input["axes"]
        for dimension in axis["dimensions"]
    }
    known_facts = _known_fact_ids(scoring_input)
    rating_ids = []
    for index, rating in enumerate(ratings):
        item = _exact_keys(rating, (
            "dimension_id", "band", "ambiguous_with", "weight", "evidence_status",
            "evidence_fact_ids", "rationale", "counterevidence", "data_gaps", "vetoes", "cap_score",
        ), f"scorecard.ratings[{index}]")
        dimension_id = _non_empty_string(item["dimension_id"], f"scorecard.ratings[{index}].dimension_id")
        if dimension_id in rating_ids:
            raise ScoringError("scorecard.ratings contains duplicate dimension_id")
        rating_ids.append(dimension_id)
        if dimension_id not in rubric_dimensions:
            raise ScoringError("scorecard.ratings dimension_id is not in the scoring input")
        if _decimal_number(item["weight"], f"scorecard.ratings[{index}].weight") != _decimal_number(
            rubric_dimensions[dimension_id]["weight"], "rubric dimension.weight"
        ):
            raise ScoringError("scorecard rating weight must equal its frozen rubric weight")
        band = _band_value(item["band"], f"scorecard.ratings[{index}].band")
        if item["ambiguous_with"] is not None:
            ambiguous = _band_value(item["ambiguous_with"], f"scorecard.ratings[{index}].ambiguous_with")
            if abs(band - ambiguous) != Decimal("25"):
                raise ScoringError("scorecard rating ambiguous_with must be an adjacent band")
        evidence_status = _non_empty_string(item["evidence_status"], f"scorecard.ratings[{index}].evidence_status")
        if evidence_status not in EVIDENCE_STATUSES:
            raise ScoringError("scorecard rating evidence_status is not supported")
        evidence_fact_ids = _rating_fact_ids(
            item["evidence_fact_ids"], f"scorecard.ratings[{index}].evidence_fact_ids", known_facts
        )
        _non_empty_string(item["rationale"], f"scorecard.ratings[{index}].rationale")
        _string_list(item["counterevidence"], f"scorecard.ratings[{index}].counterevidence")
        data_gaps = _string_list(item["data_gaps"], f"scorecard.ratings[{index}].data_gaps")
        if evidence_status == "verified":
            if not evidence_fact_ids:
                raise ScoringError("verified band requires verified evidence_fact_ids")
            if any(known_facts[fact_id] != "verified" for fact_id in evidence_fact_ids):
                raise ScoringError("verified band requires verified evidence")
            if data_gaps:
                raise ScoringError("v3 verified rating must not contain data_gaps; use inferred")
        else:
            if not data_gaps:
                raise ScoringError("inferred band requires a non-empty data_gaps list")
            if any(known_facts[fact_id] != "verified" for fact_id in evidence_fact_ids):
                raise ScoringError("inferred band may cite only verified facts")

        vetoes = item["vetoes"]
        if not isinstance(vetoes, list):
            raise ScoringError(f"scorecard.ratings[{index}].vetoes must be a list")
        for veto_index, veto in enumerate(vetoes):
            veto_data = _exact_keys(veto, ("code", "reason", "evidence_fact_ids"), f"vetoes[{veto_index}]")
            _non_empty_string(veto_data["code"], f"vetoes[{veto_index}].code")
            _non_empty_string(veto_data["reason"], f"vetoes[{veto_index}].reason")
            _verified_evidence_fact_ids(
                veto_data["evidence_fact_ids"], f"vetoes[{veto_index}].evidence_fact_ids", known_facts
            )
        cap_score = _score(item["cap_score"], f"scorecard.ratings[{index}].cap_score", nullable=True)
        if cap_score is not None and not vetoes:
            raise ScoringError("scorecard cap_score requires veto evidence from the scoring input snapshot")

    if set(rating_ids) != set(rubric_dimensions) or len(ratings) != len(rubric_dimensions):
        raise ScoringError("scorecard.ratings must contain exactly one rating per rubric dimension")
    return scorecard


def aggregate_scorecard_v3(scoring_input: Mapping, card: Mapping) -> dict:
    """Derive the deterministic anchored-band consensus from one v3 scorecard."""
    validate_scorecard(card, scoring_input)
    known_facts = _known_fact_ids(scoring_input)
    dimensions = []
    ambiguous_dimensions = []
    axes = []
    for axis in scoring_input["axes"]:
        axis_dimensions = []
        for dimension in axis["dimensions"]:
            dimension_id = dimension["dimension_id"]
            rating = next(rating for rating in card["ratings"] if rating["dimension_id"] == dimension_id)
            band = _band_value(rating["band"], "rating.band")
            ambiguous_with = (
                None if rating["ambiguous_with"] is None
                else _band_value(rating["ambiguous_with"], "rating.ambiguous_with")
            )
            veto_sources = []
            for veto_index, veto in enumerate(rating["vetoes"]):
                _verified_evidence_fact_ids(
                    veto["evidence_fact_ids"],
                    f"scorecard.ratings[{dimension_id}].vetoes[{veto_index}].evidence_fact_ids",
                    known_facts,
                )
                veto_sources.append((card["scorer_id"], veto))
            caps = []
            if rating["cap_score"] is not None:
                caps.append({
                    "scorer_id": card["scorer_id"],
                    "dimension_id": dimension_id,
                    "cap_score": rating["cap_score"],
                    "vetoes": [
                        _veto_output(veto)
                        for _, veto in sorted(veto_sources, key=lambda item: (
                            item[1]["code"], item[1]["reason"], tuple(sorted(item[1]["evidence_fact_ids"])),
                        ))
                    ],
                })
            if ambiguous_with is not None:
                ambiguous_dimensions.append({
                    "axis_id": axis["axis_id"],
                    "dimension_id": dimension_id,
                    "band": _rounded_number(band),
                    "ambiguous_with": _rounded_number(ambiguous_with),
                })
            axis_dimensions.append({
                "dimension_id": dimension_id,
                "label": dimension["label"],
                "weight": dimension["weight"],
                "band": _rounded_number(band),
                "ambiguous_with": None if ambiguous_with is None else _rounded_number(ambiguous_with),
                "score": _rounded_number(band),
                "grade_band": grade_band(float(band)),
                "evidence_status": rating["evidence_status"],
                "evidence_fact_ids": sorted(rating["evidence_fact_ids"]),
                "data_gaps": list(rating["data_gaps"]),
                "vetoes": _aggregate_vetoes(veto_sources, dimension_id),
                "caps": caps,
            })
        dimensions.extend(axis_dimensions)
        axes.append(_aggregate_axis_v3(axis, axis_dimensions))
    return {
        "schema_version": CONSENSUS_SCHEMA,
        "scoring_input_hash": scoring_input["scoring_input_hash"],
        "dimensions": dimensions,
        "axes": axes,
        "ambiguous_dimensions": sorted(
            ambiguous_dimensions, key=lambda item: (item["axis_id"], item["dimension_id"])
        ),
    }


def _aggregate_axis_v3(axis: Mapping, axis_dimensions: Sequence[Mapping]) -> dict:
    weights = [_decimal_number(dimension["weight"], "dimension.weight") for dimension in axis_dimensions]
    total_weight = sum(weights, Decimal("0"))
    weighted_sum = sum(
        weight * Decimal(str(dimension["band"])) for weight, dimension in zip(weights, axis_dimensions)
    )
    uncapped_value = weighted_sum / total_weight if total_weight else Decimal("0")
    caps = [cap for dimension in axis_dimensions for cap in dimension["caps"]]
    cap_score = None
    cap_provenance = []
    score = uncapped_value
    if caps:
        minimum_cap = min(Decimal(str(cap["cap_score"])) for cap in caps)
        cap_score = _rounded_number(minimum_cap)
        cap_provenance = [cap for cap in caps if Decimal(str(cap["cap_score"])) == minimum_cap]
        score = min(uncapped_value, minimum_cap)
    inference_share = sum(
        (weight for weight, dimension in zip(weights, axis_dimensions)
         if dimension["evidence_status"] == "inferred"), Decimal("0"),
    )
    inference_penalty = inference_share * Decimal("0.5")
    return {
        "axis_id": axis["axis_id"],
        "label": axis["label"],
        "dimensions": axis_dimensions,
        "uncapped_score": _rounded_number(uncapped_value),
        "cap_score": cap_score,
        "cap_provenance": cap_provenance,
        "score": _rounded_number(score),
        "grade_band": grade_band(float(score)),
        "direct_evidence_percent": _rounded_number(Decimal("100") - inference_share),
        "inference_share_percent": _rounded_number(inference_share),
        "inference_confidence_penalty": _rounded_number(inference_penalty),
        "confidence": _rounded_number(max(Decimal("0"), Decimal("100") - inference_penalty)),
    }


def _rounded_number(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def _aggregate_vetoes(veto_sources: Sequence[tuple[str, Mapping]], dimension_id: str) -> list[dict]:
    grouped: dict[tuple[str, str, tuple[str, ...]], list[dict]] = {}
    for scorer_id, veto in veto_sources:
        evidence_fact_ids = tuple(sorted(veto["evidence_fact_ids"]))
        identity = (veto["code"], veto["reason"], evidence_fact_ids)
        grouped.setdefault(identity, []).append({"scorer_id": scorer_id, "dimension_id": dimension_id})
    return [
        {
            "code": code,
            "reason": reason,
            "evidence_fact_ids": list(evidence_fact_ids),
            "provenance": sorted(provenance, key=lambda item: item["scorer_id"]),
        }
        for (code, reason, evidence_fact_ids), provenance in sorted(grouped.items())
    ]


