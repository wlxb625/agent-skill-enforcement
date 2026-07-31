# Contract Skills Specification 0.1.0-draft

## 1. Scope

Contract Skills is an optional execution-contract extension for folder-based Agent Skills. A Contract Skill remains a valid Skill package with `SKILL.md`; it adds `EXECUTION.yaml` and related resources that describe execution obligations.

This specification defines:

- policy layers and precedence;
- stage and transition declarations;
- validators, evaluators, and gates;
- applicability and `NOT_APPLICABLE` handling;
- repair contracts;
- evaluation attestation;
- completion receipts;
- fallback and conformance levels.

It does not define domain quality standards.

## 2. Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

## 3. Required files

A Contract Skill MUST contain:

```text
SKILL.md
EXECUTION.yaml
constitution/immutable.yaml
```

It SHOULD contain:

```text
adaptive/default-policy.yaml
schemas/
gates/
stages/
```

## 4. Identity

`EXECUTION.yaml` MUST declare:

```yaml
contract_skill:
  spec_version: "0.1.0-draft"
  kind: contract-skill
  name: example-skill
  version: "0.1.0"
```

`name` SHOULD match the Skill name in `SKILL.md`.

## 5. Compatibility and fallback

A package MUST declare a fallback mode:

```yaml
compatibility:
  ordinary_skill: true
  fallback_mode: soft-contract
```

Supported fallback modes:

- `ordinary-skill`: ignore Contract Skills extension;
- `soft-contract`: expose contract instructions to the model without claiming hard enforcement;
- `block`: refuse execution when required host capabilities are unavailable.

A host MUST report the actual execution level used.

## 6. Policy layers

The precedence order is:

```text
immutable > adaptive > task > model-local
```

The immutable layer MUST define protected paths and adaptive permissions.

The adaptive layer MUST NOT:

- disable a required stage;
- reduce a protected threshold;
- remove a required gate;
- increase prohibited permissions;
- alter completion requirements;
- modify integrity rules.

Adaptive changes SHOULD be submitted as policy patches with evidence.

## 7. Rule enforcement classes

Every rule SHOULD declare one of:

- `hard`: violation blocks execution;
- `gate`: contributes to a transition decision;
- `preference`: influences generation or ranking but does not block;
- `guidance`: advisory method or heuristic.

Hosts MUST NOT silently promote guidance into a hard rule or demote a hard rule into guidance.

## 8. Stages

Each stage MUST have a unique `id` and MAY declare:

- stage-scoped instruction file;
- input schema;
- output schema;
- required gates;
- allowed tools;
- maximum repair rounds.

A host SHOULD expose only the current stage instructions and required context.

## 9. State ownership

The contract MUST declare who owns state:

```yaml
state:
  controlled_by: host | bundled-script | model
```

`model` ownership is allowed only for L1 soft-contract mode and MUST NOT be described as hard enforcement.

## 10. Validators

Validators inspect deterministic or externally verifiable properties. Common validator types include:

- schema;
- count;
- reference;
- hash;
- file;
- command;
- custom script.

A validator MUST return `valid: true|false` and machine-readable issue codes.

## 11. Evaluators

Evaluators inspect semantic or professional quality. An evaluation SHOULD include:

- evaluator identity;
- target artifact identity and hash;
- rule/rubric hash;
- attestation level;
- scores;
- evidence references;
- hard failures;
- recommendations;
- final status.

Evaluators SHOULD bind claims to the smallest available artifact location.

## 12. Evaluation attestation

Supported attestation levels:

1. `self_assessed`;
2. `separate_context`;
3. `separate_model`;
4. `human_verified`.

A contract MAY require a minimum attestation level. A host MUST NOT claim a stronger level than it can prove.

## 13. Gates

A gate combines validator and evaluator results and returns one of:

- `PASS`;
- `CONDITIONAL`;
- `FAIL`;
- `NOT_APPLICABLE`.

A required gate MUST NOT be treated as passed when its status is missing.

A gate MAY use:

- `ALL` logic;
- `ANY` logic;
- weighted scoring;
- hard-failure override;
- custom deterministic decision logic.

## 14. Applicability

Conditional gates MUST declare applicability rules. `NOT_APPLICABLE` MUST be supported by evidence, not only by a model assertion.

Example:

```yaml
applicability:
  when:
    artifact_fact: has_dialogue
    equals: true
  evidence:
    validator: dialogue-counter
```

## 15. Transitions

All transition targets MUST refer to a declared stage or terminal state. Recommended terminal states:

- `COMPLETE`;
- `FAILED`;
- `BLOCKED`.

A required gate failure MUST route to a repair stage, an upstream stage, or a terminal failure state.

## 16. Repair contracts

A repair contract SHOULD include:

- failed dimensions;
- evidence;
- `must_change`;
- `preserve`;
- return stage;
- maximum rounds.

Repair instructions SHOULD avoid rewriting valid parts without cause.

## 17. Completion

A task is complete only when all declared completion requirements are satisfied.

A completion receipt MUST include:

- contract identity and version;
- task identity;
- actual execution level;
- completed stages;
- gate statuses;
- artifact hashes;
- attestation summary;
- terminal status;
- timestamp.

A receipt MUST NOT claim `CONTRACT_COMPLETE` when required gates are missing, failed, or unverified.

## 18. Audit events

Hosts SHOULD emit append-only events for:

- activation;
- integrity validation;
- stage preparation;
- artifact submission;
- validator result;
- evaluator result;
- gate decision;
- repair;
- policy patch;
- transition;
- completion.

## 19. Integrity

Packages MAY include hashes or signatures for protected files. Hosts that claim protected immutable policy MUST verify integrity before execution.

## 20. Conformance levels

- **L0:** ordinary Skill only;
- **L1:** soft contract;
- **L2:** script-validated contract;
- **L3:** host-enforced contract.

Conformance is capability-based, not package-author-claimed.

## 21. Security

Hosts SHOULD treat third-party scripts as untrusted code, enforce least privilege, and isolate package execution. A Contract Skill MUST NOT gain permissions merely because it declares them.

## 22. Semantic limitation

Structural conformance does not prove semantic quality. A syntactically valid high-scoring evaluation can still be dishonest. Contracts SHOULD use attestation, independent evaluation, adversarial checks, and human review proportional to risk.
