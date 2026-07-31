from pathlib import Path
import shutil
import tempfile
import unittest
import yaml

from asep.validator import validate_package

ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def test_minimal_example_is_valid(self):
        report = validate_package(ROOT / "examples/minimal-adherence-skill")
        self.assertTrue(report.valid, report.as_dict())

    def test_web_design_example_is_valid(self):
        report = validate_package(ROOT / "examples/web-design-adherence-skill")
        self.assertTrue(report.valid, report.as_dict())

    def test_ordinary_skill_without_profile_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "SKILL.md").write_text("---\nname: ordinary-skill\ndescription: A normal Skill.\n---\n# Skill\n", encoding="utf-8")
            report = validate_package(p)
            self.assertTrue(report.valid, report.as_dict())
            self.assertIn("ORDINARY_SKILL", {f.code for f in report.findings})

    def test_missing_skill_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = validate_package(tmp)
            self.assertFalse(report.valid)
            self.assertIn("MISSING_REQUIRED_FILE", {f.code for f in report.findings})

    def test_missing_required_reference_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "skill"
            shutil.copytree(ROOT / "examples/minimal-adherence-skill", p)
            profile_path = p / "references/adherence.yaml"
            profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
            profile["required_references"].append("references/missing.md")
            profile_path.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8")
            report = validate_package(p)
            self.assertFalse(report.valid)
            self.assertIn("MISSING_REFERENCE", {f.code for f in report.findings})

    def test_duplicate_requirement_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "skill"
            shutil.copytree(ROOT / "examples/minimal-adherence-skill", p)
            profile_path = p / "references/adherence.yaml"
            profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
            profile["requirements"].append(dict(profile["requirements"][0]))
            profile_path.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8")
            report = validate_package(p)
            self.assertFalse(report.valid)
            self.assertIn("DUPLICATE_REQUIREMENT", {f.code for f in report.findings})

    def test_strict_profile_needs_hard_or_core_requirement(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "skill"
            shutil.copytree(ROOT / "examples/minimal-adherence-skill", p)
            profile_path = p / "references/adherence.yaml"
            profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
            for requirement in profile["requirements"]:
                requirement["level"] = "quality"
            profile_path.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8")
            report = validate_package(p)
            self.assertFalse(report.valid)
            self.assertIn("STRICT_PROFILE_WITHOUT_CORE_REQUIREMENT", {f.code for f in report.findings})


if __name__ == "__main__":
    unittest.main()
