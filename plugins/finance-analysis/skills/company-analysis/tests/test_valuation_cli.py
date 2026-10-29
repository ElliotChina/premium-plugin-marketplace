"""估值 CLI 端到端测试：预检、冻结、卡片与批判安装、聚合、状态与重算认证。"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "valuation"))

import _fixtures as fx  # noqa: E402
import company_valuation as cv  # noqa: E402
import evidence_contract  # noqa: E402
import test_valuation as tv  # noqa: E402

SKILL_ROOT = Path(__file__).resolve().parent.parent
COMPANY_VALUATION = str(SKILL_ROOT / "scripts" / "valuation" / "company_valuation.py")
CATALOG_PATH = SKILL_ROOT / "references" / "valuation" / "valuation-models.json"
METHOD_ID = "multiple-eps-fy"


class ValuationCliTest(unittest.TestCase):
    """T12–T16：估值命令面全链路，覆盖三种发布状态与重算源认证。"""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory(prefix="valuation-cli-e2e-")
        cls.work = Path(cls._tmp.name).resolve() / "company"
        cls.work.mkdir()
        started = fx.cli(fx.COMPANY_RUN, "start", "--company-dir", str(cls.work),
                         "--company", "TestCo", "--run-id", "source-base")
        assert started["code"] == 0, started
        source = fx.cli(fx.COMPANY_RUN, "add-source", "--company-dir", str(cls.work),
                        "--url", "https://example.com/annual", "--publisher", "TestCo",
                        "--period", "2025FY", "--locator", "年报全文")
        assert source["code"] == 0, source
        cls.source_id = source["payload"]["source"]["id"]

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def _start(self, run_id: str) -> Path:
        result = fx.cli(fx.COMPANY_RUN, "start", "--company-dir", str(self.work),
                        "--company", "TestCo", "--run-id", run_id)
        self.assertEqual(result["code"], 0, result)
        return Path(result["payload"]["run_dir"])

    def _facts(self, *, eps_fact_type: str = "disclosed", eps_status: str = "verified") -> list[dict]:
        facts = tv._facts(eps_fact_type, eps_status)
        for fact in facts:
            fact["source_material_id"] = self.source_id
        return facts

    def _snapshot(self, run_id: str, facts: list[dict]) -> Path:
        data = {
            "schema_version": evidence_contract.FACT_SNAPSHOT_SCHEMA,
            "fact_snapshot_id": "snap-1",
            "fact_snapshot_hash": "pending",
            "facts": facts,
        }
        data["fact_snapshot_hash"] = evidence_contract.fact_snapshot_hash(data)
        return fx.write_json(self.work / f"{run_id}-snapshot.json", data)

    def _market(self, run_id: str, price: str) -> Path:
        return fx.write_json(self.work / f"{run_id}-market.json", {
            "schema_version": cv.MARKET_SCHEMA,
            "market_snapshot_id": f"{run_id}-market",
            "market": {
                "valuation_currency": "CNY",
                "current_price": {
                    "value": price, "currency": "CNY", "unit": "CNY/share",
                    "date": "2026-10-29",
                },
            },
        })

    def _methods(self, run_id: str, methods: list[dict] | None = None) -> Path:
        return fx.write_json(self.work / f"{run_id}-methods.json", {
            "schema_version": cv.METHOD_CANDIDATES_SCHEMA,
            "methods": methods or [tv._price_method()],
        })

    def _pipeline(self, run_id: str, *, eps_fact_type: str = "disclosed",
                  eps_status: str = "verified", fallback: bool = False,
                  price: str = "30", methods: list[dict] | None = None,
                  scenarios: dict[str, dict] | None = None,
                  primary: str = METHOD_ID) -> tuple[Path, dict]:
        run_dir = self._start(run_id)
        common = [
            "--run-dir", str(run_dir),
            "--fact-snapshot", str(self._snapshot(
                run_id, self._facts(eps_fact_type=eps_fact_type, eps_status=eps_status))),
            "--market-snapshot", str(self._market(run_id, price)),
            "--method-candidates", str(self._methods(run_id, methods)),
            "--method-catalog", str(CATALOG_PATH),
            "--model-version", "test-model",
        ]
        for command in ("preflight-input", "freeze"):
            result = fx.cli(COMPANY_VALUATION, command, *common)
            self.assertEqual(result["code"], 0, (command, result))

        valuation_input = json.loads(
            (run_dir / "analysis" / "valuation" / "input.json").read_text("utf-8"))
        card = tv._card(
            valuation_input,
            scenarios or {METHOD_ID: tv._price_scenarios()},
            primary=primary,
            fallback=fallback,
        )
        card_path = fx.write_json(self.work / f"{run_id}-card.json", card)
        for command in ("preflight-card", "install-card"):
            result = fx.cli(COMPANY_VALUATION, command,
                            "--run-dir", str(run_dir), "--card", str(card_path))
            self.assertEqual(result["code"], 0, (command, result))

        critique_path = fx.write_json(
            self.work / f"{run_id}-critique.json", tv._critique(valuation_input))
        result = fx.cli(COMPANY_VALUATION, "install-critique",
                        "--run-dir", str(run_dir), "--file", str(critique_path))
        self.assertEqual(result["code"], 0, result)

        result = fx.cli(COMPANY_VALUATION, "aggregate", "--run-dir", str(run_dir))
        self.assertEqual(result["code"], 0, result)
        status = fx.cli(COMPANY_VALUATION, "status", "--run-dir", str(run_dir))
        self.assertEqual(status["code"], 0, status)
        return run_dir, status["payload"]

    def _consensus(self, run_dir: Path) -> dict:
        return json.loads(
            (run_dir / "analysis" / "valuation" / "consensus-assumptions.json").read_text("utf-8"))

    def test_supported_pipeline_completes(self):
        run_dir, status = self._pipeline("supported")
        self.assertEqual(status["status"], "complete")
        self.assertEqual(status["precision_state"], "supported")
        consensus = self._consensus(run_dir)
        self.assertEqual(consensus["status"], "consensus")
        self.assertEqual(consensus["precision_reasons"], [])
        self.assertTrue((run_dir / "analysis" / "valuation" / "calculation.json").is_file())
        self.assertTrue((run_dir / "analysis" / "valuation" / "transaction.json").is_file())

    def test_assumption_input_completes_conditional(self):
        run_dir, status = self._pipeline(
            "conditional", eps_fact_type="assumption", eps_status="unverified")
        self.assertEqual(status["status"], "complete-conditional")
        self.assertEqual(status["precision_state"], "conditional")
        consensus = self._consensus(run_dir)
        self.assertEqual(consensus["status"], "conditional-consensus")
        self.assertIn("assumption-input",
                      {reason["code"] for reason in consensus["precision_reasons"]})

    def test_primary_fallback_completes_low_confidence(self):
        run_dir, status = self._pipeline("fallback", fallback=True)
        self.assertEqual(status["status"], "complete-low-confidence")
        self.assertEqual(status["precision_state"], "low-confidence")
        consensus = self._consensus(run_dir)
        self.assertEqual(consensus["status"], "low-confidence-consensus")
        self.assertIn("primary-role-fallback",
                      {reason["code"] for reason in consensus["precision_reasons"]})

    def test_rnpv_pipeline_completes(self):
        method_id = "intrinsic-price-per-share-rnpv"
        run_dir, status = self._pipeline(
            "rnpv",
            methods=[tv._rnpv_method()],
            scenarios={method_id: tv._rnpv_scenarios()},
            primary=method_id,
            price="40",
        )
        self.assertEqual(status["status"], "complete")
        self.assertEqual(status["precision_state"], "supported")
        calculation = json.loads(
            (run_dir / "analysis" / "valuation" / "calculation.json").read_text("utf-8"))
        method = calculation["methods"][0]
        self.assertEqual(method["method_id"], method_id)
        self.assertIn("terminal_value_share", method)
        self.assertEqual(method["terminal_value_share"]["lower"],
                         str(tv._rnpv_terminal_share(
                             tv._rnpv_scenarios()["neutral"]["range"]["lower"])))

    def test_embedded_value_pipeline_completes(self):
        method_id = "intrinsic-price-per-share-embedded-value"
        run_dir, status = self._pipeline(
            "embedded-value",
            methods=[tv._ev_method()],
            scenarios={method_id: tv._ev_scenarios()},
            primary=method_id,
            price="50",
        )
        self.assertEqual(status["status"], "complete")
        self.assertEqual(status["precision_state"], "supported")
        calculation = json.loads(
            (run_dir / "analysis" / "valuation" / "calculation.json").read_text("utf-8"))
        method = calculation["methods"][0]
        self.assertEqual(method["method_id"], method_id)
        self.assertEqual(
            method["scenarios"][1]["price_range"]["lower"],
            str(tv._ev_price(tv._ev_scenarios()["neutral"]["range"]["lower"])),
        )

    def _recalculate(self, run_id: str, source_run: Path, *, baseline_calculation: bool = True) -> dict:
        destination = self._start(run_id)
        source_dir = source_run / "analysis" / "valuation"
        command = [
            COMPANY_VALUATION, "recalculate",
            "--run-dir", str(destination),
            "--source-run-dir", str(source_run),
            "--baseline-input", str(source_dir / "input.json"),
            "--consensus-assumptions", str(source_dir / "consensus-assumptions.json"),
            "--market-snapshot", str(self._market(f"{run_id}-price", "35")),
        ]
        if baseline_calculation:
            command += ["--baseline-calculation", str(source_dir / "calculation.json")]
        result = fx.cli(*command)
        return {"destination": destination, **result}

    def test_recalculation_from_supported_source_completes(self):
        source_run, source_status = self._pipeline("recalc-source")
        self.assertEqual(source_status["status"], "complete")
        result = self._recalculate("recalc-destination", source_run)
        self.assertEqual(result["code"], 0, result)
        self.assertEqual(result["payload"]["status"], "recalculated")
        status = fx.cli(COMPANY_VALUATION, "status", "--run-dir", str(result["destination"]))
        self.assertEqual(status["code"], 0, status)
        self.assertEqual(status["payload"]["status"], "recalculated")
        self.assertEqual(status["payload"]["precision_state"], "supported")
        self.assertTrue(
            (result["destination"] / "analysis" / "valuation" / "valuation-diff.json").is_file())

    def test_recalculation_rejects_conditional_source(self):
        source_run, source_status = self._pipeline(
            "conditional-source", eps_fact_type="assumption", eps_status="unverified")
        self.assertEqual(source_status["status"], "complete-conditional")
        result = self._recalculate("conditional-destination", source_run)
        self.assertNotEqual(result["code"], 0)
        self.assertIn("complete supported aggregate run", result["stderr"])


if __name__ == "__main__":
    unittest.main()
