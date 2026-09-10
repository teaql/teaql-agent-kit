import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "progressive-modeling" / "amd-concept-graph"
SPEC = importlib.util.spec_from_file_location("concept_graph_probe", EXPERIMENT / "run.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ConceptGraphProtocolTest(unittest.TestCase):
    def test_group_context_is_projected_to_concepts(self):
        parsed = MODULE.parse(
            "\n".join(
                [
                    "group root_domain",
                    "concept moving_company root",
                    "group operations",
                    "concept move_order entity",
                    "relation moving_company manages move_order",
                ]
            )
        )

        self.assertEqual(parsed["concepts"][1]["group_key"], "operations")
        self.assertEqual(parsed["concepts"][1]["concept_id"], "C002")

    def test_reserved_relation_verb_is_rejected(self):
        parsed = MODULE.parse(
            "\n".join(
                [
                    "group root_domain",
                    "concept moving_company root",
                    "group finance_domain",
                    "concept invoice_document entity",
                    "relation invoice_document references moving_company",
                ]
            )
        )

        self.assertIn("invalid/reserved relation verb: references", parsed["findings"])

    def test_latest_evidence_retains_observed_failures(self):
        parsed = MODULE.parse((EXPERIMENT / "concept-graph.txt").read_text())

        self.assertEqual(len(parsed["groups"]), 14)
        self.assertEqual(len(parsed["concepts"]), 50)
        self.assertEqual(len(parsed["relations"]), 50)
        self.assertEqual(
            parsed["findings"],
            [
                "invalid/reserved relation verb: references",
                "unknown relation endpoint: {'from_term': 'finance', 'verb': 'tracks', 'to_term': 'expense_record'}",
                "unknown relation endpoint: {'from_term': 'finance', 'verb': 'calculates', 'to_term': 'vat_summary'}",
            ],
        )


if __name__ == "__main__":
    unittest.main()
