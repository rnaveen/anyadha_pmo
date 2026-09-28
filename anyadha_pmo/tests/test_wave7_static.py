from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "anyadha_pmo"


class TestWave7Static(unittest.TestCase):
    def test_all_doctypes_have_controllers_and_permissions(self):
        for path in APP.glob("*/doctype/*/*.json"):
            data = json.loads(path.read_text())
            if data.get("doctype") != "DocType" or data.get("issingle"):
                continue
            self.assertTrue(path.with_suffix(".py").exists(), path)
            self.assertTrue(data.get("permissions"), path)

    def test_performance_workspace_contains_all_wave6_reports(self):
        path = APP / "performance_mis/workspace/performance_mis/performance_mis.json"
        data = json.loads(path.read_text())
        names = {x.get("link_to") for x in data["links"]}
        for name in (
            "PMO KPI Performance", "PMO KRI Status", "PMO KCI Status",
            "PMO Indicator Readings", "PMO Management MIS", "PMO Performance Reviews",
        ):
            self.assertIn(name, names)

    def test_outcomes_workspace_is_single_public_desk(self):
        outcomes = json.loads(
            (APP / "monitoring_evaluation/workspace/outcomes_and_performance/outcomes_and_performance.json").read_text()
        )
        self.assertEqual(outcomes["name"], "Outcomes and Performance")
        self.assertEqual(outcomes.get("is_hidden"), 0)
        self.assertEqual(outcomes.get("public"), 1)
        names = {x.get("link_to") for x in outcomes["links"]}
        for name in (
            "PMO Indicator", "PMO KPI", "PMO Monitoring Visit",
            "PMO Performance Review", "PMO KPI Performance", "PMO Indicator Readings",
        ):
            self.assertIn(name, names)
        me = json.loads(
            (APP / "monitoring_evaluation/workspace/monitoring_evaluation/monitoring_evaluation.json").read_text()
        )
        perf = json.loads(
            (APP / "performance_mis/workspace/performance_mis/performance_mis.json").read_text()
        )
        self.assertEqual(me.get("is_hidden"), 1)
        self.assertEqual(perf.get("is_hidden"), 1)

    def test_wave7_service_metadata(self):
        from anyadha_pmo.core.services.release import release_metadata
        meta = release_metadata()
        self.assertEqual(meta["app"], "anyadha_pmo")
        self.assertTrue(meta["wave"].startswith("Wave 7"))


if __name__ == "__main__":
    unittest.main()
