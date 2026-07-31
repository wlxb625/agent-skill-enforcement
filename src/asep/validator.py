from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json
import re

import yaml
from jsonschema import Draft202012Validator

TERMINALS = {"COMPLETE", "FAILED", "BLOCKED"}

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
        return {"package": self.package, "valid": self.valid, "summary": self.summary, "findings": [f.as_dict() for f in self.findings]}

def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)

def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)

def _validate_schema(instance: Any, schema_path: Path, report: ValidationReport, label: str) -> None:
    schema = _load_json(schema_path)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        location = ".".join(str(x) for x in error.path)
        report.add("error", "SCHEMA_VIOLATION", f"{label}: {error.message}", location or label)

def _frontmatter_name(skill_path: Path) -> str | None:
    text = skill_path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, flags=re.S)
    if not match:
        return None
    data = yaml.safe_load(match.group(1)) or {}
    return data.get("name")

def _path_exists(root: Path, rel: str, report: ValidationReport, code: str = "MISSING_REFERENCE") -> bool:
    target = root / rel
    if not target.exists():
        report.add("error", code, f"Referenced path does not exist: {rel}", rel)
        return False
    return True

def _prefix_overlap(a: str, b: str) -> bool:
    def norm(x: str) -> str:
        return x.strip().strip("/").replace("[", ".").replace("]", "")
    x, y = norm(a), norm(b)
    return x == y or x.startswith(y + ".") or y.startswith(x + ".")

def validate_package(package: str | Path) -> ValidationReport:
    root = Path(package).resolve()
    report = ValidationReport(str(root))
    if not root.is_dir():
        report.add("error", "PACKAGE_NOT_DIRECTORY", "Package path is not a directory")
        return report

    for rel in ["SKILL.md", "EXECUTION.yaml", "constitution/immutable.yaml"]:
        if not (root / rel).exists():
            report.add("error", "MISSING_REQUIRED_FILE", f"Missing required file: {rel}", rel)
    if not report.valid:
        return report

    execution = _load_yaml(root / "EXECUTION.yaml") or {}
    constitution = _load_yaml(root / "constitution/immutable.yaml") or {}
    schema_root = Path(__file__).resolve().parent / "schemas"
    _validate_schema(execution, schema_root / "execution.schema.json", report, "EXECUTION.yaml")
    _validate_schema(constitution, schema_root / "constitution.schema.json", report, "constitution/immutable.yaml")

    skill_name = _frontmatter_name(root / "SKILL.md")
    enforcement_name = execution.get("enforcement", {}).get("name")
    if not skill_name:
        report.add("error", "INVALID_SKILL_FRONTMATTER", "SKILL.md must have YAML frontmatter with name")
    elif enforcement_name and skill_name != enforcement_name:
        report.add("warning", "NAME_MISMATCH", f"SKILL.md name '{skill_name}' differs from enforcement name '{enforcement_name}'")

    policy_layers = execution.get("policy_layers", {})
    immutable_rel = policy_layers.get("immutable")
    if immutable_rel:
        _path_exists(root, immutable_rel, report)
    adaptive = policy_layers.get("adaptive") or {}
    for key in ("default", "schema", "patch_schema"):
        rel = adaptive.get(key)
        if rel:
            _path_exists(root, rel, report)

    stage_ids: list[str] = []
    stage_map: dict[str, dict[str, Any]] = {}
    gate_refs: set[str] = set()
    for stage in execution.get("stages", []):
        sid = stage.get("id")
        if not sid:
            continue
        if sid in stage_map:
            report.add("error", "DUPLICATE_STAGE", f"Duplicate stage id: {sid}")
        stage_ids.append(sid)
        stage_map[sid] = stage
        for key in ("instruction", "input_schema", "output_schema"):
            rel = stage.get(key)
            if rel:
                _path_exists(root, rel, report)
        for gate_id in stage.get("gates", []) or []:
            gate_refs.add(gate_id)

    start = execution.get("state", {}).get("start_stage")
    if start not in stage_map:
        report.add("error", "INVALID_START_STAGE", f"Start stage is not declared: {start}")

    transitions = execution.get("transitions", {}) or {}
    for source, mapping in transitions.items():
        if source not in stage_map:
            report.add("error", "UNKNOWN_TRANSITION_SOURCE", f"Transition source is not a declared stage: {source}")
        for status, target in (mapping or {}).items():
            if target not in stage_map and target not in TERMINALS:
                report.add("error", "UNKNOWN_TRANSITION_TARGET", f"{source}.{status} targets unknown stage: {target}")

    if start in stage_map:
        seen = {start}
        queue = [start]
        terminal_reached = False
        while queue:
            current = queue.pop(0)
            for target in (transitions.get(current) or {}).values():
                if target in TERMINALS:
                    terminal_reached = True
                elif target in stage_map and target not in seen:
                    seen.add(target)
                    queue.append(target)
        for sid in stage_ids:
            if sid not in seen:
                report.add("warning", "UNREACHABLE_STAGE", f"Stage is not reachable from start: {sid}")
        if not terminal_reached:
            report.add("error", "NO_REACHABLE_TERMINAL", "No terminal state is reachable from the start stage")

    gate_files = execution.get("gates", []) or []
    gate_ids: set[str] = set()
    for rel in gate_files:
        if not _path_exists(root, rel, report):
            continue
        gate = _load_yaml(root / rel) or {}
        _validate_schema(gate, schema_root / "gate.schema.json", report, rel)
        gid = gate.get("id")
        if gid in gate_ids:
            report.add("error", "DUPLICATE_GATE", f"Duplicate gate id: {gid}", rel)
        if gid:
            gate_ids.add(gid)
        if gate.get("stage") not in stage_map:
            report.add("error", "GATE_UNKNOWN_STAGE", f"Gate {gid} references undeclared stage {gate.get('stage')}", rel)
        for target in (gate.get("transitions") or {}).values():
            if target not in stage_map and target not in TERMINALS:
                report.add("error", "GATE_UNKNOWN_TARGET", f"Gate {gid} targets unknown stage {target}", rel)
        for evaluator in gate.get("evaluators", []) or []:
            rubric = evaluator.get("rubric")
            if rubric:
                _path_exists(root, rubric, report)

    for gid in sorted(gate_refs - gate_ids):
        report.add("error", "MISSING_GATE_DEFINITION", f"Stage references undefined gate: {gid}")

    protected = constitution.get("protected_paths", []) or []
    allowed = constitution.get("adaptive_permissions", {}).get("allowed_paths", []) or []
    for a in allowed:
        for p in protected:
            if _prefix_overlap(a, p):
                report.add("error", "ADAPTIVE_PROTECTED_OVERLAP", f"Adaptive allowed path overlaps protected path: {a} <-> {p}")

    completion = execution.get("completion", {}) or {}
    receipt = completion.get("receipt_schema")
    if receipt:
        _path_exists(root, receipt, report)
    for sid in completion.get("requires_stages", []) or []:
        if sid not in stage_map:
            report.add("error", "COMPLETION_UNKNOWN_STAGE", f"Completion requires unknown stage: {sid}")
    for gid in completion.get("requires_gates", []) or []:
        if gid not in gate_ids:
            report.add("error", "COMPLETION_UNKNOWN_GATE", f"Completion requires unknown gate: {gid}")

    report.summary = {
        "enforcement_name": enforcement_name,
        "package_version": execution.get("enforcement", {}).get("version"),
        "spec_version": execution.get("enforcement", {}).get("spec_version"),
        "stages": len(stage_ids),
        "gates": len(gate_ids),
        "fallback_mode": execution.get("compatibility", {}).get("fallback_mode"),
        "state_owner": execution.get("state", {}).get("controlled_by"),
    }
    return report

def inspect_package(package: str | Path) -> dict[str, Any]:
    root = Path(package).resolve()
    execution = _load_yaml(root / "EXECUTION.yaml")
    return {
        "package": str(root),
        "enforcement": execution.get("enforcement"),
        "compatibility": execution.get("compatibility"),
        "state": execution.get("state"),
        "stages": [{"id": s.get("id"), "gates": s.get("gates", []), "output_schema": s.get("output_schema")} for s in execution.get("stages", [])],
        "completion": execution.get("completion"),
    }
