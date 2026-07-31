from pathlib import Path
import shutil
import tempfile
import unittest
import yaml

from contract_skills.validator import validate_package


ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def test_minimal_example_is_valid(self):
        report = validate_package(ROOT / "examples/minimal-contract-skill")
        self.assertTrue(report.valid, report.as_dict())

    def test_director_profile_is_valid(self):
        report = validate_package(ROOT / "examples/film-director-contract-profile")
        self.assertTrue(report.valid, report.as_dict())

    def test_missing_execution_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "SKILL.md").write_text("---\nname: broken\n---\n", encoding="utf-8")
            (p / "constitution").mkdir()
            (p / "constitution/immutable.yaml").write_text("{}", encoding="utf-8")
            report = validate_package(p)
            self.assertFalse(report.valid)
            self.assertIn("MISSING_REQUIRED_FILE", {f.code for f in report.findings})

    def test_unknown_transition_target_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "skill"
            shutil.copytree(ROOT / "examples/minimal-contract-skill", p)
            execution_path = p / "EXECUTION.yaml"
            execution = yaml.safe_load(execution_path.read_text(encoding="utf-8"))
            execution["transitions"]["draft"]["PASS"] = "ghost-stage"
            execution_path.write_text(yaml.safe_dump(execution, sort_keys=False), encoding="utf-8")
            report = validate_package(p)
            self.assertFalse(report.valid)
            self.assertIn("UNKNOWN_TRANSITION_TARGET", {f.code for f in report.findings})

    def test_adaptive_overlap_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "skill"
            shutil.copytree(ROOT / "examples/minimal-contract-skill", p)
            constitution_path = p / "constitution/immutable.yaml"
            constitution = yaml.safe_load(constitution_path.read_text(encoding="utf-8"))
            constitution["adaptive_permissions"]["allowed_paths"].append("gates.thresholds")
            constitution_path.write_text(yaml.safe_dump(constitution, sort_keys=False), encoding="utf-8")
            report = validate_package(p)
            self.assertFalse(report.valid)
            self.assertIn("ADAPTIVE_PROTECTED_OVERLAP", {f.code for f in report.findings})


if __name__ == "__main__":
    unittest.main()
