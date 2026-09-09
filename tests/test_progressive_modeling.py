import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = REPO_ROOT / "experiments" / "progressive-modeling"
SKILL = REPO_ROOT / "skills" / "build-teaql-app" / "SKILL.md"
PROTOCOL = (
    REPO_ROOT
    / "skills"
    / "build-teaql-app"
    / "references"
    / "progressive-modeling.md"
)
PLAN = PROTOCOL.with_name("progressive-modeling-plan.md")


def model_objects(path: Path):
    root = ET.parse(path).getroot()
    return root, {child.tag: child for child in root if not child.tag.startswith("_")}


def semantic_element(element):
    return (
        element.tag,
        element.attrib,
        (element.text or "").strip(),
        tuple(semantic_element(child) for child in element),
    )


class ProgressiveModelingTest(unittest.TestCase):
    def test_skill_links_to_protocol_and_plan(self):
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("references/progressive-modeling.md", skill)
        self.assertIn("references/progressive-modeling-plan.md", skill)
        self.assertTrue(PROTOCOL.is_file())
        self.assertTrue(PLAN.is_file())

    def test_stage_two_only_extends_stage_one(self):
        stage_one_root, stage_one = model_objects(EXPERIMENT / "stage-1" / "model.xml")
        stage_two_root, stage_two = model_objects(EXPERIMENT / "stage-2" / "model.xml")

        self.assertEqual(stage_one_root.attrib, stage_two_root.attrib)
        self.assertGreater(len(stage_one), 1, "foundation must include a business object")
        self.assertTrue(stage_one.keys() <= stage_two.keys())
        for name, element in stage_one.items():
            self.assertEqual(
                semantic_element(element),
                semantic_element(stage_two[name]),
                f"completed object {name} was rewritten",
            )

    def test_stage_two_references_resolve(self):
        _, objects = model_objects(EXPERIMENT / "stage-2" / "model.xml")
        known_types = {
            "createTime",
            "updateTime",
            "string",
            "number",
            "integer",
            "long",
            "id",
        }
        for object_name, element in objects.items():
            for field_name, value in element.attrib.items():
                if field_name.startswith("_") or not value.endswith("()"):
                    continue
                target = value[:-2]
                self.assertIn(
                    target,
                    objects.keys() | known_types,
                    f"unresolved reference {object_name}.{field_name} -> {target}",
                )


if __name__ == "__main__":
    unittest.main()
