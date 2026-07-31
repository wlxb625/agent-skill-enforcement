# Host integration

A compatible host can implement the following lifecycle:

```text
activate
→ verify_integrity
→ load_policy_layers
→ prepare_current_stage
→ invoke_model_or_tool
→ validate_artifact
→ evaluate_artifact
→ decide_gate
→ transition_or_repair
→ finalize
```

## Minimum L2 support

- execute bundled validators in a sandbox;
- store state outside model-editable context;
- validate schemas and references;
- reject protected policy patches;
- require a completion receipt.

## L3 support

- host-owned state and transitions;
- stage-scoped instruction disclosure;
- least-privilege tools;
- evaluator isolation and attestation;
- append-only audit events;
- final-response hook that verifies completion.

## Fallback

A host that cannot enforce the lifecycle should run in `soft-enforcement` mode and disclose that limitation.
