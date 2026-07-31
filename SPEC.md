# Agent Skill Enforcement Protocol (ASEP) 0.2.0-draft

## 1. Scope

ASEP is an optional enforcement extension for folder-based Agent Skills. An ASEP package remains an ordinary Skill with `SKILL.md`; it adds `EXECUTION.yaml` and related resources that declare when a lifecycle may advance and when completion may be claimed.

This specification defines:

- enforcement metadata and runtime claim levels;
- stage locks and transition rules;
- required artifacts and deterministic validation;
- semantic evaluation and attestation;
- blocking gates and applicability;
- repair and return routes;
- protected rules and bounded adaptation;
- completion receipts and audit evidence.

ASEP does not define domain quality standards. A screenplay Skill, audit Skill, coding Skill, or research Skill supplies its own evaluators and gate criteria.

## 2. Normative language

The terms MUST, MUST NOT, REQUIRED, SHOULD, SHOULD NOT, and MAY are normative.

## 3. Required package files

An Enforced Skill MUST contain:

```text
SKILL.md
EXECUTION.yaml
constitution/immutable.yaml
```

It MAY contain adaptive policy, stage instructions, artifact schemas, validators, evaluators, gate definitions, state scripts, references, and templates.

## 4. Enforcement declaration

`EXECUTION.yaml` MUST contain an `enforcement` object:

```yaml
enforcement:
  protocol: ASEP
  spec_version: "0.2.0-draft"
  kind: enforced-agent-skill
  name: example-skill
  version: "0.2.0"
```

`kind` MUST be `enforced-agent-skill`. A runtime MUST NOT claim ASEP execution when this declaration is absent or invalid.

## 5. Compatibility and fallback

A package declares how it behaves when ASEP is unsupported:

```yaml
compatibility:
  ordinary_skill: true
  fallback_mode: soft-enforcement
  minimum_execution_level: L1
```

Allowed fallback modes:

- `ordinary-skill`: ignore ASEP resources and use `SKILL.md` only;
- `soft-enforcement`: expose the obligations to the model without claiming host enforcement;
- `block`: refuse execution below the required level.

A runtime MUST report the effective level:

- `L0`: ordinary Skill only;
- `L1`: obligations are declared but transitions are model-managed;
- `L2`: bundled scripts or a runner can reject invalid transitions and completion;
- `L3`: the host owns state, permissions, evaluator isolation, gates, and finalization.

A runtime MUST NOT claim a higher level than it actually provided.

## 6. Enforcement lifecycle

The canonical lifecycle is:

```text
activate → prepare → submit → validate → evaluate → gate → transition → finalize
```

A host MAY implement this using a state machine, graph, hooks, scripts, or another execution engine. The semantics, not a specific engine, are normative.

## 7. Stage locks

`state.start_stage` identifies the initial authorized stage. Each stage MAY declare instructions, input/output schemas, allowed tools, gates, and repair limits.

A conforming L2 or L3 runtime MUST reject:

- submission to a stage that is not currently authorized;
- progression when required output is missing or invalid;
- progression when a required gate did not return `PASS`;
- finalization before completion requirements are satisfied.

## 8. Validators, evaluators, and gates

ASEP separates three concepts:

### 8.1 Validator

A validator checks deterministic facts: schema, counts, references, file existence, hashes, stage identity, permission declarations, or other mechanically testable conditions.

### 8.2 Evaluator

An evaluator judges semantic quality. It SHOULD cite evidence locations and MUST declare an attestation level:

```text
self_assessed < separate_context < separate_model < human_verified
```

### 8.3 Gate

A gate combines validator and evaluator results and returns:

- `PASS`: progression is permitted;
- `CONDITIONAL`: repair is required before progression;
- `FAIL`: progression is blocked and execution returns or terminates according to the declared route;
- `NOT_APPLICABLE`: allowed only when the gate declares applicability rules and supplies evidence that those rules are unmet.

A hard failure MUST override aggregate scores.

## 9. Gate composition

Gates MAY use:

- `ALL`: every required component passes;
- `ANY`: at least one valid path passes;
- `WEIGHTED`: a minimum aggregate score is met;
- hard-failure override.

Domain rubrics are not part of the universal protocol.

## 10. Repair routes

A `CONDITIONAL` or `FAIL` result SHOULD produce a repair contract containing:

```yaml
repair:
  failed_dimensions: []
  preserve: []
  must_change: []
  return_to_stage: stage-id
```

A runtime MUST follow the declared transition rather than silently advancing to a later stage.

## 11. Protected rules and bounded adaptation

ASEP MAY use layered policies, but layering is a protection mechanism rather than the primary abstraction.

The immutable layer protects enforcement-critical fields such as required stages, required gates, thresholds, allowed transitions, permissions, and completion conditions. Adaptive and task policies MAY specialize behavior but MUST NOT weaken protected rules.

Recommended priority:

```text
immutable enforcement rules
  > adaptive user/project policy
    > current task policy
      > model-local decisions
```

Policy updates SHOULD be expressed as validated patches and checked for protected-path overlap.

## 12. Completion

Completion MUST be receipt-backed. A receipt MUST include:

- protocol and specification version;
- package and artifact identity;
- effective enforcement level;
- completed required stages;
- required gate results;
- attestation levels;
- artifact hashes or equivalent evidence;
- final marker `ASEP_COMPLETE`.

A runtime MUST NOT issue `ASEP_COMPLETE` when a required stage or gate is missing, failed, stale, or below the declared minimum attestation.

## 13. Audit events

A runtime SHOULD record activation, stage opening, submission, validation, evaluation, gate decision, repair, transition, and finalization events. Audit logs SHOULD bind events to artifact versions or hashes.

## 14. Security

Third-party scripts are untrusted code. Hosts SHOULD use least privilege, sandbox execution, restrict network/filesystem access, and require explicit permission grants. Declaring a tool or permission in `EXECUTION.yaml` does not grant it.

## 15. Conformance

A package-level validator can verify structure, references, graphs, policy boundaries, and receipt requirements. Strong semantic guarantees require host-side evaluator isolation or human verification.

A conforming implementation SHOULD publish valid and invalid fixtures and MUST distinguish package conformance from actual runtime enforcement.

## 16. Legacy draft migration

`Contract Skills 0.1.0-draft` was the early project name. ASEP 0.2.0-draft changes:

- project name to Agent Skill Enforcement;
- top-level `contract_skill` to `enforcement`;
- `kind: contract-skill` to `kind: enforced-agent-skill`;
- CLI `contract-skill` to `asep`;
- completion marker `CONTRACT_COMPLETE` to `ASEP_COMPLETE`;
- fallback `soft-contract` to `soft-enforcement`.

See `docs/migration-from-contract-skills.md`.
