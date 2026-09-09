import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = (
    ROOT
    / "experiments"
    / "progressive-modeling"
    / "amd-three-stage"
    / "artifacts"
)


class ProgressiveConceptArtifactTest(unittest.TestCase):
    def load_json(self, name):
        return json.loads((ARTIFACTS / name).read_text(encoding="utf-8"))

    def load_csv(self, name):
        with (ARTIFACTS / name).open(encoding="utf-8", newline="") as source:
            return list(csv.DictReader(source))

    def test_discovery_ids_and_references_are_closed(self):
        discovery = self.load_json("concept-discovery.json")
        group_ids = {group["id"] for group in discovery["groups"]}
        concept_ids = {concept["id"] for concept in discovery["concepts"]}

        self.assertEqual(len(group_ids), len(discovery["groups"]))
        self.assertEqual(len(concept_ids), len(discovery["concepts"]))
        self.assertTrue(all(c["group_id"] in group_ids for c in discovery["concepts"]))
        for source, _, target in discovery["relations"]:
            self.assertIn(source, concept_ids)
            self.assertIn(target, concept_ids)

    def test_csv_projection_matches_discovery(self):
        discovery = self.load_json("concept-discovery.json")
        concepts = self.load_csv("concepts.csv")
        relations = self.load_csv("relations.csv")

        self.assertEqual(len(concepts), len(discovery["concepts"]))
        self.assertEqual(len(relations), len(discovery["relations"]))
        self.assertEqual(
            {row["concept_id"] for row in concepts},
            {concept["id"] for concept in discovery["concepts"]},
        )

    def test_resolution_does_not_recreate_global_names(self):
        discovery = self.load_json("concept-discovery.json")
        resolution = self.load_json("concept-resolution.json")
        existing = {concept["term"] for concept in discovery["concepts"]}

        for item in resolution["resolutions"]:
            replaced = set(item["replaces_ids"])
            for concept in item["concepts"]:
                if concept["term"] in existing:
                    self.assertIn(
                        concept["id"].split("-")[0],
                        replaced,
                        f"recreated existing concept {concept['term']}",
                    )

    def test_object_completion_obeys_reference_boundary(self):
        completion = self.load_json("object-completion-C001.json")
        allowed = {
            "C012",
            "C002",
            "C003",
            "C004",
            "C005-A",
            "C017-A",
            "C017-B",
            "C007-B",
            "C029",
            "C025",
        }
        runtime_fields = {"id", "version", "create_time", "update_time", "audit"}

        self.assertTrue(8 <= len(completion["fields"]) <= 14)
        self.assertFalse(runtime_fields & {field["name"] for field in completion["fields"]})
        for field in completion["fields"]:
            if field["semantic_type"].startswith("reference"):
                self.assertIn(field["target_concept_id"], allowed)
            else:
                self.assertIsNone(field["target_concept_id"])
        self.assertIn(
            "move_status",
            {item["proposed_term"] for item in completion["missing_concepts"]},
        )

    def test_candidate_is_not_misreported_as_complete(self):
        findings = self.load_json("validation-findings.json")
        self.assertEqual(findings["status"], "needs_repair")
        codes = {finding["code"] for finding in findings["findings"]}
        self.assertIn("EMPTY_GROUP", codes)
        self.assertIn("CANONICAL_NAME_REQUIRED", codes)
        self.assertTrue(
            any(finding["severity"] == "error" for finding in findings["findings"])
        )


if __name__ == "__main__":
    unittest.main()
