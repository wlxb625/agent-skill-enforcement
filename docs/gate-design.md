# Gate design

## Do not turn every rule into a gate

Use four enforcement classes:

- hard constraint;
- quality gate;
- preference;
- guidance.

Too many gates encourage form-filling and reduce creative or analytical quality.

## Separate three jobs

1. Validators establish deterministic facts.
2. Evaluators judge meaning or professional quality.
3. Gates control transitions.

## Require evidence

A score without evidence should be rejected or capped. Evidence should point to artifact IDs, sections, scene IDs, test names, citations, or file ranges.

## Support applicability

A dialogue gate should not run on a silent film, but “no dialogue” must be established by a validator rather than a free model claim.

## Prefer repair contracts

A failed gate should identify what to change and what to preserve. This avoids destructive full rewrites.

## Use adversarial checks

Field presence is not quality. Useful semantic checks include:

- deletion test: does removing the claimed climax or argument change the result?
- substitution test: can the key element be replaced without loss?
- causality test: did the action actually cause the outcome?
- counterexample test: is there a simpler explanation?
- comparison test: is the result materially different from rejected history?
