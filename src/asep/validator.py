from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json
import re

import yaml
from jsonschema import Draft202012Validator


@dataclass
class Finding:
    level: str
    code: str
    message: str
    path: str | None = None

    def as_dict(self) -> dict[str, Any]:
        data = {"level": self.level, "code": self.code, "message": self.message}
        if self.path:
            data["path"] = self.path
        return data


@dataclass
class ValidationReport:
    package: str
    findings: list[Finding] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    @property
    def valid(self) -> bool:
        return not any(f.level == "error" for f in self.findings)

    def add(self, level: str, code: str, message: str, path: str | None = None) -> None:
        self.findings.append(Finding(level, code, message, path))

    def as_dict(self) -> dict[str, Any]:
        return {
            "package": self.package,
            "valid": self.valid,
            "summary": self.summary,
            "findings": [f.as_dict() for f in self.findings],
        }


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _frontmatter(skill_path: Path) -> tuple[dict[str, Any], str]:
    text = skill_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return {}, text
    return (yaml.safe_load(match.group(1)) or {}), text


def _validate_schema(instance: Any, schema_path: Path, report: ValidationReport, label: str) -> None:
    validator = Draft202012Validator(_load_json(schema_path))
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        location = ".".join(str(x) for x in error.path)
        report.add("error", "SCHEMA_VIOLATION", f"{label}: {error.message}", location or label)


def _check_path(root: Path, rel: str, report: ValidationReport, code: str = "MISSING_REFERENCE") -> bool:
    target = (root / rel).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        report.add("error", "PATH_OUTSIDE_PACKAGE", f"Referenced path leaves package: {rel}", rel)
        return False
    if not target.exists():
        report.add("error", code, f"Referenced path does not exist: {rel}", rel)
        return False
    return True


def validate_package(package: str | Path) -> ValidationReport:
    root = Path(package).resolve()
    report = ValidationReport(str(root))

    if not root.is_dir():
        report.add("error", "PACKAGE_NOT_DIRECTORY", "Package path is not a directory")
        return report

    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        report.add("error", "MISSING_REQUIRED_FILE", "Missing required file: SKILL.md", "SKILL.md")
        return report

    frontmatter, skill_text = _frontmatter(skill_path)
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if not name or not description:
        report.add("error", "INVALID_SKILL_FRONTMATTER", "SKILL.md frontmatter must include name and description", "SKILL.md")

    profile_path = root / "references" / "adherence.yaml"
    if not profile_path.exists():
        report.add("info", "ORDINARY_SKILL", "No references/adherence.yaml found; validated as an ordinary Agent Skill")
        report.summary = {
            "skill": name,
            "profile": None,
            "requirements": 0,
            "required_references": 0,
            "review_scripts": 0,
        }
        return report

    try:
        profile = _load_yaml(profile_path) or {}
    except Exception as exc:
        report.add("error", "INVALID_YAML", f"Could not parse references/adherence.yaml: {exc}", "references/adherence.yaml")
        return report

    schema_root = Path(__file__).resolve().parent / "schemas"
    _validate_schema(profile, schema_root / "adherence.schema.json", report, "references/adherence.yaml")

    declared_name = (profile.get("profile") or {}).get("skill")
    if name and declared_name and name != declared_name:
        report.add("error", "NAME_MISMATCH", f"SKILL.md name '{name}' differs from adherence profile skill '{declared_name}'", "references/adherence.yaml")

    required_refs = profile.get("required_references", []) or []
    for rel in required_refs:
        if _check_path(root, rel, report) and rel not in skill_text:
            report.add("warning", "REFERENCE_NOT_LINKED_FROM_SKILL", f"Required reference is not mentioned directly in SKILL.md: {rel}", rel)

    requirements = profile.get("requirements", []) or []
    seen: set[str] = set()
    levels: dict[str, int] = {"hard": 0, "core": 0, "quality": 0, "preference": 0}
    for item in requirements:
        rid = item.get("id")
        if rid in seen:
            report.add("error", "DUPLICATE_REQUIREMENT", f"Duplicate requirement id: {rid}", "references/adherence.yaml")
        if rid:
            seen.add(rid)
        level = item.get("level")
        if level in levels:
            levels[level] += 1
        source = item.get("source")
        if source:
            rel = source.split("#", 1)[0]
            _check_path(root, rel, report)

    mode = (profile.get("profile") or {}).get("mode")
    if mode == "strict" and levels["hard"] + levels["core"] == 0:
        report.add("error", "STRICT_PROFILE_WITHOUT_CORE_REQUIREMENT", "A strict profile must contain at least one hard or core requirement", "references/adherence.yaml")

    review = profile.get("review") or {}
    criteria = review.get("criteria")
    if criteria:
        _check_path(root, criteria, report)
    scripts = review.get("scripts", []) or []
    for rel in scripts:
        _check_path(root, rel, report, code="MISSING_SCRIPT")
        if not rel.startswith("scripts/"):
            report.add("warning", "NONSTANDARD_SCRIPT_LOCATION", f"Review script should normally be stored under scripts/: {rel}", rel)

    if (root / "EXECUTION.yaml").exists():
        report.add("warning", "LEGACY_WORKFLOW_EXTENSION", "EXECUTION.yaml is treated as an optional legacy/advanced workflow extension in ASEP 0.3", "EXECUTION.yaml")

    report.summary = {
        "skill": name,
        "profile": (profile.get("profile") or {}).get("mode"),
        "spec_version": (profile.get("profile") or {}).get("spec_version"),
        "requirements": len(requirements),
        "levels": levels,
        "required_references": len(required_refs),
        "review_scripts": len(scripts),
        "task_interpretation": (profile.get("application") or {}).get("interpret_for_current_task"),
        "requirement_persistence": (profile.get("application") or {}).get("keep_relevant_requirements_active"),
    }
    return report


def inspect_package(package: str | Path) -> dict[str, Any]:
    root = Path(package).resolve()
    report = validate_package(root)
    profile_path = root / "references" / "adherence.yaml"
    profile = _load_yaml(profile_path) if profile_path.exists() else None
    return {
        "package": str(root),
        "valid": report.valid,
        "summary": report.summary,
        "required_references": (profile or {}).get("required_references", []),
        "requirements": [
            {
                "id": item.get("id"),
                "level": item.get("level"),
                "statement": item.get("statement"),
                "prohibited_substitutions": item.get("prohibited_substitutions", []),
            }
            for item in (profile or {}).get("requirements", [])
        ],
        "application": (profile or {}).get("application"),
        "review": (profile or {}).get("review"),
        "findings": [f.as_dict() for f in report.findings],
    }
