# Agent Skill Enforcement

**Make AI follow the Skill it loaded—not its default habits.**

Agent Skill Enforcement defines **ASEP**, an experimental authoring and validation profile for Agent Skills. It keeps the normal `SKILL.md`, `references/`, `scripts/`, and `assets/` structure, while making the Skill's non-optional methods, prohibited shortcuts, review rules, and revision behavior clearer and harder for an agent to silently ignore.

> Ordinary Skills give an agent methods to read.  
> ASEP helps those methods stay active while the agent interprets, decides, generates, reviews, and revises.

ASEP does **not** replace the Agent Skills format and does not require a new agent runtime. An ASEP-enhanced package is still an ordinary portable Skill. Agents that do not understand ASEP can continue reading its Markdown files; compatible tools can additionally validate the optional machine-readable adherence profile.

This repository is an independent community experiment. It is **not** an official revision of the Agent Skills specification.

[中文说明](README.zh-CN.md) · [Draft specification](SPEC.md) · [Authoring guide](docs/authoring-guide.md) · [Examples](examples/) · [FAQ](docs/faq.md)

## The problem

A Skill may contain excellent professional methods, yet an agent can still load it and produce a result based on familiar defaults.

A web-design Skill may say:

- do not use a card grid as the main composition;
- make scroll change space, focus, or narrative state;
- let images and video carry information;
- do not use repeated fade-ins as the primary motion system.

The agent may still deliver a dark page with large text, cards, gradients, and identical entrance animations. The Skill was activated, but its core methods did not sufficiently control the generation.

ASEP targets that gap:

```text
Skill instructions
→ identify non-optional requirements
→ interpret them for the current task
→ keep relevant requirements active during generation
→ review the actual result against the Skill
→ revise the parts that drifted
```

The agent remains free to choose tools, techniques, and implementation details. It is not free to silently replace the Skill's core methods with easier default patterns.

## What is different

| Capability | Ordinary Agent Skill | ASEP-enhanced Skill |
|---|---|---|
| Standard `SKILL.md` package | Yes | Yes |
| Standard `references/`, `scripts/`, `assets/` | Optional | Reused directly |
| Core requirements | Often mixed into prose | Clearly separated and prioritized |
| Prohibited shortcuts | Often implicit | Explicitly named |
| Task-specific interpretation | Model-dependent | Requested before generation |
| Requirement persistence | May fade during long tasks | Relevant rules are reintroduced when needed |
| Review | Often checks only whether output exists | Checks whether output follows the Skill |
| Revision | Broad regeneration | Targeted correction of drift |
| Extra runtime required | No | No for the core profile |

## Design principles

### Extend, do not replace

ASEP uses the normal Agent Skills structure:

```text
my-skill/
├── SKILL.md
├── references/
│   ├── adherence.yaml          # Optional machine-readable profile
│   ├── core-requirements.md
│   ├── quality-criteria.md
│   └── anti-patterns.md
├── scripts/
│   └── review_adherence.py
└── assets/
    └── templates/
```

Only `SKILL.md` is required by the base format. ASEP's `references/adherence.yaml` is optional: it helps tools validate the Skill's requirement structure, but Markdown remains the primary content an agent reads.

### Constrain outcomes, not creativity

ASEP does not prescribe one implementation. A motion-design Skill can require meaningful spatial change while leaving the agent free to choose sticky scenes, masks, video sequences, SVG, WebGL, or another suitable technique.

### Prevent easy substitutions

A requirement should name the common shortcut that does **not** satisfy it. For example, “scroll narrative” should explicitly reject opacity-only transitions and identical section animations.

### Review for drift, not for paperwork

Review exists to detect when the result has fallen back to the model's default pattern. It is not primarily a proof or receipt system.

## A normal ASEP-enhanced Skill

`SKILL.md` remains the main entry point:

```markdown
## Required references

Before designing, read:

- `references/core-requirements.md`
- `references/anti-patterns.md`
- `references/quality-criteria.md`

## Core requirements

1. Do not use a card grid as the primary page composition.
2. Scroll must change space, focus, information relationships, or narrative state.
3. Images and video must carry content, not only decoration.

## How to apply this Skill

Before implementation, translate each core requirement into a decision for the current page. Keep the relevant requirements active while working on each section.

## Review and revision

Render the result, compare it with the quality criteria, and revise any section that falls back to a prohibited pattern.
```

The optional `references/adherence.yaml` expresses the same requirements in a compact, machine-checkable form:

```yaml
profile:
  protocol: ASEP
  spec_version: 0.3.0-draft
  mode: strict
  skill: cinematic-web-designer

required_references:
  - references/core-requirements.md
  - references/quality-criteria.md
  - references/anti-patterns.md

requirements:
  - id: scroll-narrative
    level: hard
    statement: Scroll must change space, focus, information relationships, or narrative state.
    prohibited_substitutions:
      - opacity-only transitions
      - identical entrance animation on every section

application:
  interpret_for_current_task: true
  keep_relevant_requirements_active: true

review:
  required: true
  criteria: references/quality-criteria.md
  revise_drifted_parts: true
```

## Quick start

Validate an example:

```bash
python -m pip install -e .
asep validate examples/minimal-adherence-skill
asep inspect examples/web-design-adherence-skill
```

Upgrade an existing Skill:

1. keep its current `SKILL.md`, `references/`, `scripts/`, and `assets/`;
2. separate non-optional requirements from general advice;
3. describe prohibited shortcuts and default-pattern substitutions;
4. require current-task interpretation before generation;
5. add review and targeted revision instructions;
6. optionally add `references/adherence.yaml` for validation tooling.

See the [migration guide](docs/migration-guide.md).

## Examples

- [`minimal-adherence-skill`](examples/minimal-adherence-skill/) — the smallest useful profile using the standard Skill structure.
- [`web-design-adherence-skill`](examples/web-design-adherence-skill/) — shows how a design Skill can prevent card-grid and fade-in defaults without dictating one visual solution.
- [`optional-workflow-enforcement`](docs/optional-workflow-enforcement.md) — explains how stages and gates can still be added for tasks that genuinely need process control.

## What ASEP does not guarantee

ASEP cannot make a weak model understand every professional standard, and a purely self-reviewed result can still be judged incorrectly. Its purpose is narrower and practical: reduce the chance that an agent loads a Skill, then quietly returns to its default habits.

## Status

`0.3.0-draft` refocuses the project on **Skill adherence during generation**. Workflow state machines, blocking completion, and receipts are now optional advanced mechanisms rather than the universal core.

## License

MIT. See [LICENSE](LICENSE).
