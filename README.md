# Agent Skill Enforcement

**A portable enforcement layer for Agent Skills.**

Agent Skill Enforcement defines the **Agent Skill Enforcement Protocol (ASEP)**: an experimental extension that turns Skill instructions into lifecycle obligations that can block progression and completion.

> Ordinary Skills describe how work should be done.  
> Enforced Skills control whether the work may advance or be declared complete.

ASEP preserves the familiar folder-based Agent Skill model and its `SKILL.md` entry point. It adds a machine-readable `EXECUTION.yaml` that declares stage locks, required artifacts, validators, semantic evaluators, blocking gates, repair routes, protected rules, audit events, and receipt-backed completion.

This repository is an independent community experiment. It is **not** an official revision of the Agent Skills specification.

[中文说明](README.zh-CN.md) · [ASEP specification](SPEC.md) · [Authoring guide](docs/authoring-guide.md) · [Migration guide](docs/migration-guide.md) · [FAQ](docs/faq.md)

## The problem

A normal Skill can contain excellent methods and professional requirements, while the model may still skip stages, lower thresholds, ignore failed reviews, or announce completion without proving that the required process ran.

ASEP makes those requirements executable at the lifecycle level:

```text
activate
→ open allowed stage
→ submit required artifact
→ validate deterministic facts
→ evaluate semantic quality
→ apply blocking gate
   ├─ PASS: advance
   ├─ CONDITIONAL: repair
   └─ FAIL: return or stop
→ finalize only with a valid completion receipt
```

## What is different

| Capability | Ordinary Agent Skill | ASEP Enforced Skill |
|---|---|---|
| Portable folder package | Yes | Yes |
| `SKILL.md` instructions | Yes | Yes |
| Machine-readable lifecycle | Usually prose | Declared in `EXECUTION.yaml` |
| Stage progression | Model-controlled | Can be stage-locked |
| Required artifacts | Advisory | Schema-validated |
| Quality checks | Optional advice | Gates can block transition |
| Failed review | Model may continue | Declared repair/return route |
| Protected thresholds | Not standardized | Lower layers cannot weaken them |
| Completion | Model says “done” | Requires `ASEP_COMPLETE` receipt |
| Auditability | Host-dependent | Lifecycle events and evidence |

## Enforcement primitives

- **Stage lock** — only the currently authorized stage may run.
- **Validator** — checks deterministic facts such as schema, counts, references, hashes, or required files.
- **Evaluator** — judges semantic quality and binds findings to evidence.
- **Gate** — combines results and returns `PASS`, `CONDITIONAL`, or `FAIL`.
- **Repair route** — declares what must change, what should be preserved, and where execution returns.
- **Protected rule** — cannot be weakened by adaptive policy, task policy, or model-local decisions.
- **Completion receipt** — proves that required stages and gates were satisfied at the claimed enforcement level.

ASEP defines **how enforcement is expressed**. Each domain Skill defines **what professional standards are enforced**.

## Package layout

```text
my-enforced-skill/
├── SKILL.md
├── EXECUTION.yaml
├── constitution/
│   └── immutable.yaml
├── adaptive/
│   ├── default-policy.yaml
│   └── policy.schema.json
├── stages/
├── gates/
├── evaluators/
├── schemas/
├── scripts/
└── references/
```

## Minimal declaration

```yaml
enforcement:
  protocol: ASEP
  spec_version: "0.2.0-draft"
  kind: enforced-agent-skill
  name: evidence-brief
  version: "0.2.0"

state:
  controlled_by: bundled-script
  start_stage: draft

transitions:
  draft:
    PASS: review
    FAIL: FAILED
  review:
    PASS: final
    CONDITIONAL: draft
    FAIL: FAILED
  final:
    PASS: COMPLETE

completion:
  terminal_stage: COMPLETE
  receipt_schema: schemas/completion-receipt.schema.json
```

## Quick start

```bash
python -m pip install -e .
asep validate examples/minimal-enforced-skill
asep inspect examples/minimal-enforced-skill
```

## Enforcement levels

- **L0 — Ordinary Skill:** the host reads only `SKILL.md`; no ASEP claim is allowed.
- **L1 — Declared Enforcement:** the model reads ASEP declarations, but the host does not own transitions.
- **L2 — Script-Enforced:** bundled validators/state scripts can block invalid transitions and completion.
- **L3 — Host-Enforced:** the host owns state, permissions, evaluator isolation, gates, and finalization.

A package must never claim stronger enforcement than the runtime actually provided.

## Important limitation

A package can strongly enforce deterministic structure, state, permissions, required checks, and completion conditions. It cannot, by itself, prove that a semantic evaluator was honest or isolated from the generator. ASEP therefore records evaluation attestation:

```text
self_assessed < separate_context < separate_model < human_verified
```

## Examples

- [`minimal-enforced-skill`](examples/minimal-enforced-skill/) — a generic three-stage example.
- [`film-director-enforcement-profile`](examples/film-director-enforcement-profile/) — domain-specific gates for screenplay creation. Those gates are examples, not universal ASEP requirements.

## Status

`0.2.0-draft` is a breaking draft rename from the briefly published `Contract Skills 0.1.0-draft`. The new name makes the core purpose explicit: **enforcement, not merely contract description**. See [migration notes](docs/migration-from-contract-skills.md).

## License

MIT. See [LICENSE](LICENSE).
