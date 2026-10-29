"""CLI 端到端测试：start → freeze → 评分卡 → aggregate → status，以及 check 的摘要块核对。"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import _fixtures as fx  # noqa: E402
import company_run  # noqa: E402
import scoring_consensus as sc  # noqa: E402


class CliEndToEndTest(unittest.TestCase):
    """T31–T33：命令面全链路。"""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="scoring-cli-e2e-")
        work = (Path(cls._tmp.name).resolve() / "company")
        work.mkdir()
        cls.work = work

        started = fx.cli(fx.COMPANY_RUN, "start", "--company-dir", str(work),
                         "--company", "TestCo", "--run-id", "r1")
        self_assert = started
        assert self_assert["code"] == 0, self_assert
        cls.run_dir = started["payload"]["run_dir"]

        source = fx.cli(fx.COMPANY_RUN, "add-source", "--company-dir", str(work),
                        "--url", "https://example.com/annual", "--publisher", "TestCo",
                        "--period", "2025FY", "--locator", "年报全文")
        assert source["code"] == 0, source
        cls.source_id = source["payload"]["source"]["id"]

        rubric = fx.load_rubric()
        scoring_input = fx.build_input(rubric)
        for fact_item in scoring_input["facts"]:
            fact_item["source_material_id"] = cls.source_id
        scoring_input["scoring_input_hash"] = sc.scoring_input_hash(scoring_input)

        snapshot = fx.write_json(work / "snapshot.json",
                                 {"fact_snapshot_id": "snap-1", "facts": scoring_input["facts"]})
        coverage = fx.write_json(work / "coverage.json", scoring_input["evidence_coverage"])
        context = fx.write_json(work / "context.json", scoring_input["assessment_context"])
        common = ["--run-dir", cls.run_dir, "--fact-snapshot", str(snapshot),
                  "--rubric", str(fx.RUBRIC_PATH), "--evidence-coverage", str(coverage),
                  "--assessment-context", str(context), "--model-version", "test-model"]

        for command in ("preflight-input", "freeze"):
            result = fx.cli(fx.COMPANY_SCORING, command, *common)
            assert result["code"] == 0, (command, result)
        cls.input_hash = scoring_input["scoring_input_hash"]

        card = fx.build_card(scoring_input)
        card_file = fx.write_json(work / "card.json", card)
        for command in ("preflight-card", "install-card"):
            result = fx.cli(fx.COMPANY_SCORING, command, "--run-dir", cls.run_dir,
                            "--card", str(card_file))
            assert result["code"] == 0, (command, result)
        aggregated = fx.cli(fx.COMPANY_SCORING, "aggregate", "--run-dir", cls.run_dir)
        assert aggregated["code"] == 0, aggregated
        cls.status = fx.cli(fx.COMPANY_SCORING, "status", "--run-dir", cls.run_dir)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_freeze_rejects_duplicate_with_different_content(self):
        changed = json.loads((Path(self.run_dir) / "analysis" / "scoring" / "input.json")
                             .read_text("utf-8"))
        changed["model_version"] = "other"
        staging = Path(self._tmp.name) / "changed-input.json"
        fx.write_json(staging, changed)
        result = fx.cli(fx.COMPANY_SCORING, "freeze",
                        "--run-dir", self.run_dir, "--fact-snapshot", str(staging),
                        "--rubric", str(fx.RUBRIC_PATH),
                        "--evidence-coverage", str(staging),
                        "--assessment-context", str(staging), "--model-version", "test-model")
        self.assertNotEqual(result["code"], 0)

    def test_status_complete_with_quality(self):
        self.assertEqual(self.status["code"], 0)
        payload = self.status["payload"]
        self.assertEqual(payload["status"], "complete")
        self.assertEqual(payload["core_quality"], 75.0)
        self.assertEqual(payload["valid_cards"], 1)

    def test_consensus_on_disk_matches_replay(self):
        consensus = json.loads(
            (Path(self.run_dir) / "analysis" / "scoring" / "consensus.json").read_text("utf-8"))
        self.assertEqual(consensus["core_quality"]["score"], 75.0)
        self.assertEqual(consensus["summary_markdown"].count(sc.SUMMARY_START), 1)
        self.assertEqual(sc.validate_consensus(consensus)["schema_version"], sc.CONSENSUS_SCHEMA)


class ScoringSummaryCheckTest(unittest.TestCase):
    """T34–T35：check 的评分摘要块核对。"""

    def _prepare(self):
        tmp = tempfile.TemporaryDirectory(prefix="scoring-summary-check-")
        self.addCleanup(tmp.cleanup)
        run_dir = Path(tmp.name).resolve() / "run"
        (run_dir / "analysis" / "scoring").mkdir(parents=True)
        scoring_input = fx.build_input()
        card = fx.build_card(scoring_input)
        consensus = sc.aggregate_scorecard(scoring_input, card)
        fx.write_json(run_dir / "analysis" / "scoring" / "input.json", scoring_input)
        fx.write_json(run_dir / "analysis" / "scoring" / "consensus.json", consensus)
        return run_dir, consensus

    def _summary(self, run_dir: Path, body: str) -> list:
        return company_run._scoring_summary_consistency(run_dir, body)

    def test_matching_block_passes(self):
        run_dir, consensus = self._prepare()
        body = f"# 报告\n\n{consensus['summary_markdown']}\n"
        self.assertEqual(self._summary(run_dir, body), [])

    def test_missing_block_fails(self):
        run_dir, _ = self._prepare()
        errors = self._summary(run_dir, "# 报告\n\n没有摘要块\n")
        self.assertEqual(len(errors), 1)
        self.assertIn("恰好一个", errors[0])

    def test_tampered_block_fails(self):
        run_dir, consensus = self._prepare()
        tampered = consensus["summary_markdown"].replace(
            "核心质量分 | 75.0", "核心质量分 | 99.9")
        body = f"# 报告\n\n{tampered}\n"
        errors = self._summary(run_dir, body)
        self.assertEqual(len(errors), 1)
        self.assertIn("不一致", errors[0])

    def test_duplicate_blocks_fail(self):
        run_dir, consensus = self._prepare()
        block = consensus["summary_markdown"]
        errors = self._summary(run_dir, f"# 报告\n\n{block}\n\n{block}\n")
        self.assertEqual(len(errors), 1)
        self.assertIn("恰好一个", errors[0])


if __name__ == "__main__":
    unittest.main()
