# Enforcement levels

## L0 — Ordinary Skill

Only `SKILL.md` is used. No ASEP enforcement claim is allowed.

## L1 — Declared Enforcement

The model reads `EXECUTION.yaml` and attempts to follow it, but state and evaluation may still be model-controlled.

## L2 — Script-Enforced

Bundled or host-provided scripts verify integrity, schemas, references, policy patches, transitions, and completion. Semantic evaluation may remain weakly attested.

## L3 — Host-Enforced

The host owns state, transitions, tool permissions, evaluator isolation, audit events, gates, and finalization.

A completion receipt must record the actual level used.
