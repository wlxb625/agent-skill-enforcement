# Governance and policy layers

## Immutable layer

Contains process invariants, protected thresholds, required gates, permission limits, and completion conditions. It may be updated only through an authorized package version change.

## Adaptive layer

Contains user and project preferences. The model proposes patches; a validator accepts or rejects them.

## Task layer

Contains current-task parameters such as format, deadline, target audience, platform, or prohibited choices.

## Conflict handling

A lower layer cannot override a higher layer. When a patch partially conflicts, the host should apply legal operations and reject protected operations with explicit issue codes.

## Recommended issue codes

- `PROTECTED_PATH_WRITE`;
- `THRESHOLD_DOWNGRADE`;
- `REQUIRED_GATE_REMOVAL`;
- `PERMISSION_ESCALATION`;
- `COMPLETION_RULE_OVERRIDE`.
