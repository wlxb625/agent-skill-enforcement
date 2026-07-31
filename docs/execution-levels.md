# Execution levels

## L0 — Ordinary Skill

Only `SKILL.md` is used. No contract guarantee.

## L1 — Soft Contract

The model reads `EXECUTION.yaml` and attempts to follow it. State and evaluation may still be model-controlled.

## L2 — Script-Validated Contract

Bundled or host-provided scripts verify integrity, schemas, references, policy patches, and completion. Semantic evaluation may remain weakly attested.

## L3 — Host-Enforced Contract

The host owns state, transitions, tool permissions, evaluator isolation, audit events, and finalization.

A completion receipt must record the actual level used.
