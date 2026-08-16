import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class EvalContractTests(unittest.TestCase):
    def test_self_contained_pvs_cases_exist(self) -> None:
        data = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        by_id = {case["id"]: case for case in data["cases"]}
        for case_id in ("level2-bundled-pvs", "single-skill-offline", "independent-pvs-not-required"):
            self.assertIn(case_id, by_id)
        self.assertFalse(by_id["level2-bundled-pvs"]["expected_output"]["external_install"])
        self.assertEqual(by_id["level2-bundled-pvs"]["expected_output"]["pvs_source"], "bundled")

    def test_eval_file_has_ten_complete_unique_cases(self) -> None:
        path = ROOT / "evals" / "evals.json"
        self.assertTrue(path.is_file(), "缺少 evals/evals.json")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["version"], (ROOT / "VERSION").read_text(encoding="utf-8").strip())
        cases = data["cases"]
        self.assertGreaterEqual(len(cases), 10)
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            with self.subTest(case=case.get("id")):
                for field in ("id", "prompt", "expected_output", "files"):
                    self.assertIn(field, case)
                    self.assertTrue(case[field])

    def test_positive_cases_cover_all_levels(self) -> None:
        data = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        levels = {
            case["expected_output"].get("level")
            for case in data["cases"]
            if case["expected_output"].get("trigger") is True
        }
        self.assertTrue({1, 2, 3, 4}.issubset(levels))

    def test_negative_cases_cover_skill_creation_explanation_and_review(self) -> None:
        data = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        negatives = {
            case["expected_output"].get("exclusion")
            for case in data["cases"]
            if case["expected_output"].get("trigger") is False
        }
        self.assertTrue({"skill_creation", "pure_explanation", "read_only_review"}.issubset(negatives))

    def test_external_and_github_routing_cases_exist(self) -> None:
        data = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        ids = {case["id"] for case in data["cases"]}
        self.assertTrue(
            {
                "github-all-levels-routing",
                "github-plugin-unavailable",
                "level4-capability-installed",
                "level4-capability-missing",
                "level4-install-declined",
                "level4-no-nested-skill",
            }.issubset(ids)
        )


if __name__ == "__main__":
    unittest.main()
