# Contract Skills

**Execution contracts for portable Agent Skills.**

Contract Skills is an experimental extension to the open [Agent Skills](https://github.com/agentskills/agentskills) folder format. It preserves the familiar `SKILL.md` package model while adding machine-readable execution obligations: immutable policies, adaptive policy boundaries, stages, validators, evaluators, quality gates, repair routes, audit records, and completion receipts.

> Ordinary Skill: “Here is how you should do it.”  
> Contract Skill: “The task is complete only after these conditions are satisfied.”

This repository is an independent community experiment. It is **not** an official revision of the Agent Skills specification.

[中文说明](README.zh-CN.md) · [Specification](SPEC.md) · [Authoring guide](docs/authoring-guide.md) · [Migration guide](docs/migration-guide.md) · [FAQ](docs/faq.md)

## Why this exists

Agent Skills package reusable instructions, scripts, references, and templates. In many hosts, however, the model still decides how completely to follow those instructions. A model may skip a stage, reinterpret a threshold, perform self-evaluation, or declare completion without proving that the required process ran.

Contract Skills adds an optional `EXECUTION.yaml` contract beside `SKILL.md` so a compatible host—or a script-capable agent—can enforce more of the process.

## What is different

| Capability | Ordinary Agent Skill | Contract Skill |
|---|---|---|
| Portable folder package | Yes | Yes |
| `SKILL.md` instructions | Yes | Yes |
| Machine-readable stages | Optional prose | Required contract |
| Rule priority | Usually prompt-based | Explicit policy layers |
| Immutable professional rules | Not standardized | Declared and protected |
| Adaptive user policy | Informal memory | Patch-based and bounded |
| Validators and evaluators | Optional | Separated concepts |
| Quality gates | Advisory | Can block transition |
| Repair routing | Informal | Declared transition |
| Completion | Model says it is done | Receipt-backed completion |
| Auditability | Host-dependent | Contract-level events |

## Design principle

Contract Skills does **not** define what “good” means in every profession.

It defines how a Skill author can turn professional standards into executable declarations:

- **Validator** — checks deterministic facts such as schema, counts, references, hashes, or required files.
- **Evaluator** — judges semantic quality and binds findings to evidence.
- **Gate** — combines validator and evaluator results to decide `PASS`, `CONDITIONAL`, or `FAIL`.
- **Repair contract** — states what must change, what should be preserved, and where execution returns.

The core specification defines **how to gate**. Domain packages define **what to gate**.

## Package layout

```text
my-contract-skill/
├── SKILL.md                         # Existing Agent Skills entry point
├── EXECUTION.yaml                   # Contract Skills extension
├── constitution/
│   └── immutable.yaml               # Protected rules and policy priority
├── adaptive/
│   ├── default-policy.yaml          # User/project preferences
│   └── policy.schema.json
├── stages/                          # Stage-scoped instructions
├── gates/                           # Domain and system gates
├── evaluators/                      # Semantic rubrics
├── schemas/                         # Artifact and evaluation schemas
├── scripts/                         # Optional deterministic checks
└── references/                      # Existing Skill resources
```

## Quick start

### 1. Install the reference validator

```bash
python -m pip install -e .
```

### 2. Validate the minimal example

```bash
contract-skill validate examples/minimal-contract-skill
```

### 3. Inspect the contract

```bash
contract-skill inspect examples/minimal-contract-skill
```

### 4. Upgrade an existing Skill

Keep the original `SKILL.md`, then add:

1. `EXECUTION.yaml`;
2. an immutable policy file;
3. stage-specific outputs and schemas;
4. validators, evaluators, and gates;
5. failure/repair transitions;
6. a completion receipt requirement.

See [Migration guide](docs/migration-guide.md).

## Execution levels

Contract Skills can degrade gracefully depending on host support:

- **L0 — Ordinary Skill:** host reads `SKILL.md` only.
- **L1 — Soft Contract:** the model reads the contract but the host does not enforce lifecycle hooks.
- **L2 — Script-Validated Contract:** the host can run bundled validation/state scripts.
- **L3 — Host-Enforced Contract:** the host owns state transitions, policy protection, evaluator isolation, and finalization.

A package must never claim L3 enforcement when it only ran in L1 or L2.

## Core policy hierarchy

```text
Immutable contract policy
    > Adaptive user/project policy
        > Current task policy
            > Model-local decisions
```

The adaptive layer may personalize the process but must not reduce protected thresholds, skip required stages, disable gates, or expand permissions prohibited by the immutable layer.

## Important limitation

A content package can enforce structure, state, counts, references, permissions, required checks, and completion conditions. It cannot, by itself, prove that a semantic evaluator was honest or truly isolated from the generator. Evaluation attestation therefore has explicit trust levels:

```text
self_assessed < separate_context < separate_model < human_verified
```

See [Semantic evaluation limitations](docs/semantic-evaluation-limitations.md).

## Examples

- [`minimal-contract-skill`](examples/minimal-contract-skill/) — a three-stage generic example.
- [`film-director-contract-profile`](examples/film-director-contract-profile/) — shows domain gates such as climax force, thematic necessity, and character age fit. These are examples, not part of the universal standard.

## Status

`0.1.0-draft` is an experimental specification intended for discussion, prototyping, and conformance testing. Breaking changes are expected before `1.0`.

## License

MIT. See [LICENSE](LICENSE).
