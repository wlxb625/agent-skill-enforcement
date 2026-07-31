# Semantic evaluation limitations

Machine-readable evaluation files can prove that fields, references, hashes, and score thresholds are present. They cannot alone prove that a semantic judge was honest.

A generator can fabricate:

- high scores;
- plausible evidence;
- fake context IDs;
- claims of independent review.

Mitigations include:

- host-issued evaluator nonces;
- artifact and rubric hashes;
- isolated evaluator context;
- separate models;
- adversarial evaluators;
- human review;
- random audit sampling;
- negative conformance tests.

Attestation is evidence about the evaluation process, not a guarantee of correctness.
