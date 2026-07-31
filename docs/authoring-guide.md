# Authoring guide

## 1. Start with an existing Skill

Keep `SKILL.md` concise and useful for ordinary hosts. Agent Skill Enforcement should extend, not replace, the basic Skill experience.

## 2. Extract invariants

List rules that must not be weakened by user preference or model interpretation. Put only true invariants in the immutable layer.

## 3. Classify rules

For every rule choose `hard`, `gate`, `preference`, or `guidance`.

## 4. Define stages around durable artifacts

A good stage produces an artifact that can be validated and reviewed. Avoid stages that represent only hidden thought.

## 5. Write output schemas

Schemas should capture evidence and references, not only labels and scores.

## 6. Separate validators, evaluators, and gates

Do not let an evaluator directly advance state. The gate should interpret results according to immutable policy.

## 7. Add repair routes

For each failure, declare whether to retry the current stage, return upstream, request user input, or stop.

## 8. Define completion

List required stages, gates, artifacts, hashes, and minimum evaluator attestation.

## 9. Add negative tests

Create artifacts that should fail: missing evidence, fake IDs, low counts, skipped stages, threshold downgrade patches, and hollow semantic outputs.

## 10. Declare limitations

State which guarantees require host support and which remain model-dependent.
