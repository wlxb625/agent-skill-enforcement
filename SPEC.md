# Agent Skill Enforcement Profile (ASEP) 0.3.0-draft

## 1. Scope

ASEP is an optional adherence profile for folder-based Agent Skills. It extends the existing Skill authoring model without replacing its standard structure.

An ASEP-enhanced Skill:

- keeps `SKILL.md` as the primary entry point;
- uses normal `references/`, `scripts/`, and `assets/` directories;
- separates non-optional requirements from general guidance;
- names prohibited substitutions and default-pattern shortcuts;
- asks the agent to interpret requirements for the current task;
- keeps relevant requirements active during generation;
- reviews the actual result for drift and requests targeted revision;
- may include `references/adherence.yaml` for machine validation.

ASEP does not require a workflow engine, state machine, completion receipt, or new top-level package format. Those mechanisms are optional extensions for tasks that need stronger process control.

## 2. Compatibility principle

ASEP MUST extend, not replace, the Agent Skills format.

The only universally required package file remains:

```text
SKILL.md
```

ASEP-enhanced Skills SHOULD use the standard optional directories when applicable:

```text
references/
scripts/
assets/
```

New top-level directories MUST NOT be required when an existing Agent Skills directory can express the same purpose.

## 3. SKILL.md authoring profile

An ASEP-enhanced `SKILL.md` SHOULD make the following concerns explicit. Exact heading names MAY vary by language and domain.

### 3.1 Required references

The Skill SHOULD directly list supporting files that must be read before or during execution.

### 3.2 Core requirements

Non-optional professional methods MUST be separated from preferences and general advice.

Recommended levels:

- `hard`: violation means the result does not follow the Skill;
- `core`: central to the Skill's distinctive method;
- `quality`: important quality target that may admit contextual trade-offs;
- `preference`: adaptable user or project preference.

### 3.3 Prohibited patterns

The Skill SHOULD identify common default patterns, shortcuts, or substitutions that do not satisfy the requirement.

### 3.4 Application instructions

The Skill SHOULD require the agent to translate relevant requirements into decisions for the current task before generating the affected artifact.

### 3.5 Review and revision

The Skill SHOULD instruct the agent to inspect the actual output against the Skill's criteria and revise drifted parts while preserving parts that already comply.

## 4. Optional adherence profile

A Skill MAY include:

```text
references/adherence.yaml
```

The file is optional and supplements, rather than replaces, the Markdown instructions.

Minimal example:

```yaml
profile:
  protocol: ASEP
  spec_version: 0.3.0-draft
  mode: strict
  skill: example-skill

required_references:
  - references/core-requirements.md

requirements:
  - id: primary-method
    level: hard
    statement: The primary domain method that must be followed.
    prohibited_substitutions:
      - a common shortcut that does not satisfy the method

application:
  interpret_for_current_task: true
  keep_relevant_requirements_active: true

review:
  required: true
  criteria: references/quality-criteria.md
  revise_drifted_parts: true
```

## 5. Requirement semantics

Each structured requirement MUST contain:

- a unique `id`;
- a `level`;
- a concrete `statement`.

A requirement MAY also declare:

- `source`: the Markdown file or section that explains it;
- `applies_to`: artifact or task categories;
- `prohibited_substitutions`: easier patterns that do not satisfy it;
- `review_questions`: questions used to detect drift.

A `strict` profile MUST contain at least one `hard` or `core` requirement.

## 6. Required references

Every path in `required_references` MUST exist within the Skill package. `SKILL.md` SHOULD directly mention each required reference so ordinary Skills-compatible agents can discover it through progressive disclosure.

## 7. Application behavior

When `interpret_for_current_task` is true, the agent SHOULD convert relevant abstract requirements into concrete task decisions before generating the affected artifact.

When `keep_relevant_requirements_active` is true, the agent SHOULD reload or reintroduce the subset of requirements relevant to the current artifact, component, or revision. This is intended to reduce requirement loss during long tasks.

ASEP does not dictate the exact internal reasoning format and does not require revealing private chain of thought.

## 8. Review behavior

Review is for detecting Skill drift.

When `review.required` is true, the agent SHOULD compare the actual output—not only its description—against the declared criteria.

For visual or interactive work, review SHOULD inspect rendered output when the host supports it. For code, review SHOULD inspect relevant files and run appropriate deterministic checks. For writing, review SHOULD inspect the completed text rather than only an outline or self-summary.

When `revise_drifted_parts` is true, revision SHOULD target failed requirements while preserving already satisfactory parts.

## 9. Scripts

Deterministic helpers SHOULD be stored in `scripts/`. Scripts MAY validate structure, run tests, render artifacts, capture screenshots, or detect mechanical anti-patterns.

A script cannot by itself guarantee semantic or aesthetic quality. Its role is to strengthen checks that can be made deterministically.

## 10. Assets

Templates, examples, design tokens, screenshots, starter files, and other reusable resources SHOULD remain in `assets/`.

## 11. Optional workflow enforcement

Complex Skills MAY add staged workflows, gates, state, or completion controls. These are optional and MUST NOT be presented as required for the core ASEP adherence profile.

See `docs/optional-workflow-enforcement.md`.

## 12. Conformance

A package conforms to the ASEP core profile when:

- `SKILL.md` has valid Agent Skills frontmatter;
- an optional `references/adherence.yaml` conforms to the schema;
- referenced files and scripts exist;
- requirement IDs are unique;
- a strict profile contains at least one hard or core requirement.

Conformance means the package is well-formed. It does not guarantee that every agent will perfectly follow the Skill.

## 13. Migration from 0.2

ASEP 0.3 changes the project center of gravity:

- standard Agent Skills structure becomes the default;
- `EXECUTION.yaml` is no longer required;
- `constitution/`, `gates/`, `evaluators/`, and `stages/` are no longer core directories;
- `references/adherence.yaml` becomes the optional machine-readable profile;
- Skill adherence during generation becomes the core;
- workflow state, blocking completion, and receipts become optional advanced mechanisms.

See `docs/migration-from-v0.2.md`.
