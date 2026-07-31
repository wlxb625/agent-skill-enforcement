# Contributing

Agent Skill Enforcement is an experimental specification. Contributions are welcome as issues, RFCs, schemas, conformance fixtures, domain examples, and host adapters.

## Principles

- preserve compatibility with ordinary Agent Skills;
- separate universal execution semantics from domain quality rules;
- do not claim guarantees a content package cannot provide;
- include negative tests for every new enforcement feature;
- prefer small composable primitives over domain-specific core fields.

## Pull requests

1. Explain the problem and proposed behavior.
2. Update specification and schemas together.
3. Add valid and invalid conformance fixtures.
4. Run `python -m unittest discover -s tests -v`.
5. Note backward compatibility impact.

Substantial changes should begin as an RFC under `rfcs/`.
