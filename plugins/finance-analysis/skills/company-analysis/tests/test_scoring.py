"""评分契约确定性测试：量表结构、输入/卡校验、几何聚合、风险规则、敏感性、摘要块。"""

from __future__ import annotations

import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _fixtures as fx  # noqa: E402
import scoring_consensus as sc  # noqa: E402


def aggregate(bands=None, statuses=None, ambiguities=None, rules=None, cycle=None):
    scoring_input = fx.build_input()
    card = fx.build_card(scoring_input, bands=bands, statuses=statuses,
                         ambiguities=ambiguities, rules=rules, cycle=cycle)
    return scoring_input, card, sc.aggregate_scorecard(scoring_input, card)


class RubricStructureTest(unittest.TestCase):
    """T01–T03：量表结构静态校验。"""

    def setUp(self):
        self.rubric = fx.load_rubric()

    def test_five_axes_twenty_seven_dimensions(self):
        self.assertEqual(
            [axis["axis_id"] for axis in self.rubric["axes"]],
            ["industry-quality", "business-quality", "financial-quality",
             "governance-capital-allocation", "future-prospects"],
        )
        sizes = [len(axis["dimensions"]) for axis in self.rubric["axes"]]
        self.assertEqual(sizes, [6, 6, 5, 5, 5])
        self.assertEqual(sum(sizes), 27)

    def test_axis_weights_and_anchors(self):
        anchor_total = 0
        for axis in self.rubric["axes"]:
            self.assertEqual(sum(d["weight"] for d in axis["dimensions"]), 100)
            for dimension in axis["dimensions"]:
                self.assertEqual(
                    set(dimension["anchors"]), {"0", "25", "50", "75", "100"},
                    dimension["dimension_id"],
                )
                anchor_total += 5
        self.assertEqual(anchor_total, 135)

    def test_cycle_components_and_rules(self):
        components = self.rubric["cycle_rubric"]["components"]
        self.assertEqual(
            [(c["component_id"], c["weight"]) for c in components],
            [("demand-orders", 35), ("price-margin", 35), ("inventory-capacity", 30)],
        )
        rules = {r["rule_id"]: r for r in self.rubric["risk_rules"]}
        self.assertEqual(len(rules), 6)
        for rule_id in ("confirmed-material-misstatement", "confirmed-shareholder-expropriation",
                        "uncovered-liquidity-gap", "core-license-loss"):
            self.assertEqual(rules[rule_id]["evidence_requirement"], "verified-facts")
        self.assertEqual(rules["stress-covenant-breach"]["evidence_requirement"],
                         "stress-scenario-allowed")


class ScoringInputTest(unittest.TestCase):
    """T04–T08：冻结输入 v3 校验与哈希。"""

    def test_bundled_rubric_builds_valid_input(self):
        scoring_input = fx.build_input()
        self.assertEqual(sc.validate_scoring_input(scoring_input)["schema_version"],
                         sc.INPUT_SCHEMA)

    def test_hash_deterministic_and_sensitive(self):
        first = fx.build_input()
        second = fx.build_input()
        self.assertEqual(first["scoring_input_hash"], second["scoring_input_hash"])
        changed = fx.build_input()
        changed["model_version"] = "other-model"
        changed["scoring_input_hash"] = sc.scoring_input_hash(changed)
        self.assertNotEqual(first["scoring_input_hash"], changed["scoring_input_hash"])

    def test_rejects_tampered_hash(self):
        scoring_input = fx.build_input()
        scoring_input["scoring_input_hash"] = "0" * 64
        with self.assertRaises(sc.ScoringError):
            sc.validate_scoring_input(scoring_input)

    def test_rejects_foreign_rubric(self):
        rubric = fx.load_rubric()
        rubric["axes"][0]["dimensions"][0]["weight"] = 60
        with self.assertRaises(sc.ScoringError):
            sc.validate_scoring_input(fx.build_input(rubric))

    def test_coverage_must_cover_every_object(self):
        scoring_input = fx.build_input()
        coverage = scoring_input["evidence_coverage"]
        coverage["dimensions"] = coverage["dimensions"][:-1]
        with self.assertRaises(sc.ScoringError):
            sc.validate_scoring_input(scoring_input)

    def test_assessment_context_requires_date_shape(self):
        scoring_input = fx.build_input()
        scoring_input["assessment_context"]["as_of"] = "2026/10/29"
        with self.assertRaises(sc.ScoringError):
            sc.validate_scoring_input(scoring_input)


class CoreQualityFormulaTest(unittest.TestCase):
    """T09–T12：几何核心质量分公式（方案算例）。"""

    def _q(self, b, f, g):
        policy = fx.load_rubric()["aggregation_policy"]
        axes = [
            {"axis_id": "business-quality",
             "effective_score": None if b is None else Decimal(b)},
            {"axis_id": "financial-quality",
             "effective_score": None if f is None else Decimal(f)},
            {"axis_id": "governance-capital-allocation",
             "effective_score": None if g is None else Decimal(g)},
        ]
        return sc._core_quality(policy, axes)

    def test_equal_axes(self):
        self.assertEqual(self._q(80, 80, 80).quantize(Decimal("0.1")), Decimal("80.0"))

    def test_weak_financial_axis(self):
        self.assertEqual(self._q(90, 30, 80).quantize(Decimal("0.1")), Decimal("56.6"))

    def test_weak_governance_axis(self):
        self.assertEqual(self._q(90, 90, 30).quantize(Decimal("0.1")), Decimal("72.2"))

    def test_mixed_axes(self):
        self.assertEqual(self._q(85, 80, 75).quantize(Decimal("0.1")), Decimal("80.9"))

    def test_zero_axis_gives_zero_without_renormalization(self):
        self.assertEqual(self._q(90, 0, 80), Decimal("0"))

    def test_null_axis_gives_null(self):
        self.assertIsNone(self._q(90, None, 80))


class AggregationTest(unittest.TestCase):
    """T13–T20：轴分、风险规则作用域、状态推导。"""

    def test_uniform_bands_give_uniform_scores(self):
        _in, _card, consensus = aggregate()
        self.assertEqual(consensus["core_quality"]["score"], 75.0)
        self.assertEqual([axis["effective_score"] for axis in consensus["axis_scores"]],
                         [75.0] * 5)
        self.assertEqual(consensus["risk_state"], "clear")
        self.assertEqual(consensus["assessment_state"], "supported")
        self.assertEqual(consensus["sensitivity_range"], None)
        self.assertEqual(consensus["cycle_assessment"]["intensity_score"], 75.0)

    def test_restricted_rule_caps_dimension_and_axis(self):
        _in, _card, consensus = aggregate(rules=[fx.rule_item("confirmed-material-misstatement",
                                                              "triggered")])
        financial = next(a for a in consensus["axis_scores"] if a["axis_id"] == "financial-quality")
        reporting = next(d for d in financial["dimensions"] if d["dimension_id"] == "reporting-reliability")
        self.assertEqual(reporting["effective_score"], 0.0)
        self.assertEqual(reporting["applied_rules"], ["confirmed-material-misstatement"])
        self.assertEqual(consensus["risk_state"], "restricted")
        self.assertLess(consensus["core_quality"]["score"], 75.0)

    def test_attention_rule_caps_at_25(self):
        _in, _card, consensus = aggregate(rules=[fx.rule_item("stress-covenant-breach",
                                                              "triggered")])
        financial = next(a for a in consensus["axis_scores"] if a["axis_id"] == "financial-quality")
        solvency = next(d for d in financial["dimensions"] if d["dimension_id"] == "solvency-liquidity")
        self.assertEqual(solvency["effective_score"], 25.0)
        self.assertEqual(consensus["risk_state"], "attention")

    def test_unresolved_rule_marks_risk_unassessed(self):
        _in, _card, consensus = aggregate(rules=[fx.rule_item("core-license-loss", "unresolved")])
        self.assertEqual(consensus["risk_state"], "unassessed")

    def test_unassessable_dimension_nulls_axis_and_quality(self):
        _in, _card, consensus = aggregate(
            bands={"customer-unit-economics": None},
            statuses={"customer-unit-economics": "unassessable"},
        )
        business = next(a for a in consensus["axis_scores"] if a["axis_id"] == "business-quality")
        self.assertIsNone(business["effective_score"])
        self.assertIsNone(consensus["core_quality"]["score"])
        self.assertEqual(consensus["assessment_state"], "unavailable")

    def test_noncore_unassessable_keeps_quality(self):
        _in, _card, consensus = aggregate(
            bands={"demand-durability": None},
            statuses={"demand-durability": "unassessable"},
        )
        self.assertEqual(consensus["core_quality"]["score"], 75.0)
        self.assertEqual(consensus["assessment_state"], "supported")

    def test_inferred_core_dimension_is_provisional(self):
        _in, _card, consensus = aggregate(
            statuses={"customer-unit-economics": "inferred"},
        )
        self.assertEqual(consensus["assessment_state"], "provisional")

    def test_sensitivity_range_from_ambiguity(self):
        _in, _card, consensus = aggregate(ambiguities={"customer-unit-economics": 50})
        sensitivity = consensus["sensitivity_range"]
        self.assertIsNotNone(sensitivity)
        self.assertLess(sensitivity["low"], consensus["core_quality"]["score"])
        self.assertGreaterEqual(sensitivity["high"], consensus["core_quality"]["score"])


class CycleAssessmentTest(unittest.TestCase):
    """T21–T23：周期模块规则。"""

    def test_weak_cycle_requires_empty_components(self):
        cycle = {"applicability": "weak-cycle", "phase": "not-applicable",
                 "direction": "not-applicable", "rationale": "弱周期", "components": []}
        _in, _card, consensus = aggregate(cycle=cycle)
        self.assertIsNone(consensus["cycle_assessment"]["intensity_score"])

    def test_weak_cycle_rejects_component_ratings(self):
        cycle = {"applicability": "weak-cycle", "phase": "not-applicable",
                 "direction": "not-applicable", "rationale": "弱周期",
                 "components": [{"component_id": "demand-orders", "band": 50,
                                 "evidence_fact_ids": ["f-demand-orders"],
                                 "rationale": "判断", "data_gaps": []}]}
        scoring_input = fx.build_input()
        card = fx.build_card(scoring_input, cycle=cycle)
        with self.assertRaises(sc.ScoringError):
            sc.aggregate_scorecard(scoring_input, card)

    def test_unassessable_cycle_uses_unclear(self):
        cycle = {"applicability": "unassessable", "phase": "trough",
                 "direction": "improving", "rationale": "证据不足",
                 "components": []}
        scoring_input = fx.build_input()
        card = fx.build_card(scoring_input, cycle=cycle)
        with self.assertRaises(sc.ScoringError):
            sc.aggregate_scorecard(scoring_input, card)


class ScorecardValidationTest(unittest.TestCase):
    """T24–T28：评分卡负例。"""

    def _mutate(self, mutate):
        scoring_input = fx.build_input()
        card = fx.build_card(scoring_input)
        mutate(card)
        with self.assertRaises(sc.ScoringError):
            sc.aggregate_scorecard(scoring_input, card)

    def test_rejects_wrong_weight(self):
        self._mutate(lambda card: card["ratings"][0].update(weight=50))

    def test_rejects_invalid_band(self):
        self._mutate(lambda card: card["ratings"][0].update(band=80))

    def test_rejects_supported_with_gaps(self):
        self._mutate(lambda card: card["ratings"][0].update(data_gaps=["缺"]))

    def test_rejects_ambiguous_equal_to_band(self):
        self._mutate(lambda card: card["ratings"][0].update(ambiguous_with=75))

    def test_rejects_incomplete_dimension_coverage(self):
        self._mutate(lambda card: card["ratings"].pop())

    def test_rejects_hash_mismatch(self):
        self._mutate(lambda card: card.update(scoring_input_hash="f" * 64))

    def test_rejects_triggered_rule_without_evidence(self):
        self._mutate(lambda card: card["risk_assessments"].append(
            {"rule_id": "core-license-loss", "status": "triggered",
             "evidence_fact_ids": [], "rationale": "无证据触发"}))


class SummaryBlockTest(unittest.TestCase):
    """T29–T30：机器核对摘要块。"""

    def test_summary_block_wellformed_and_reproducible(self):
        _in, _card, consensus = aggregate(ambiguities={"customer-unit-economics": 50})
        summary = consensus["summary_markdown"]
        self.assertTrue(summary.startswith(sc.SUMMARY_START))
        self.assertTrue(summary.endswith(sc.SUMMARY_END))
        self.assertEqual(summary.count(sc.SUMMARY_START), 1)
        self.assertEqual(summary.count(sc.SUMMARY_END), 1)
        again = sc.render_scoring_summary(consensus, fx.assessment_context())
        self.assertEqual(again, summary)

    def test_validate_consensus_roundtrip(self):
        _in, _card, consensus = aggregate()
        self.assertEqual(sc.validate_consensus(consensus)["schema_version"], sc.CONSENSUS_SCHEMA)


if __name__ == "__main__":
    unittest.main()
