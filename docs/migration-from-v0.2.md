# Migrating from ASEP 0.2

ASEP 0.2 centered on `EXECUTION.yaml`, custom lifecycle directories, stage locks, gates, and completion receipts.

ASEP 0.3 makes those optional and returns the core package to the normal Agent Skills structure.

Recommended migration:

- move immutable professional rules into `SKILL.md` and `references/core-requirements.md`;
- move evaluator rubrics into `references/quality-criteria.md`;
- move hard failures into `references/anti-patterns.md` and the core requirements section;
- move deterministic validators into `scripts/`;
- express workflow steps directly in `SKILL.md` unless machine state is genuinely required;
- create `references/adherence.yaml` for optional machine-readable requirement metadata.

Legacy lifecycle files may be retained as an advanced extension, but they are no longer required for core conformance.
