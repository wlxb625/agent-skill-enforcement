# Contributing

Agent Skill Enforcement is an experimental authoring profile for Agent Skills.

Contributions are welcome as documentation, examples, schemas, validator improvements, tests, and evaluation results.

## Principles

- extend the standard Agent Skills structure rather than replacing it;
- keep `SKILL.md` useful to ordinary Skills-compatible agents;
- separate non-optional requirements from preferences;
- prefer concrete requirements over abstract quality labels;
- name default-pattern substitutions that should not count as compliance;
- treat workflow state and completion controls as optional advanced features;
- do not claim that package validation guarantees output quality.

## Pull requests

1. Explain the adherence failure the change addresses.
2. Update documentation and schemas together when semantics change.
3. Add or update valid and invalid fixtures.
4. Run `python -m unittest discover -s tests -v`.
5. Note compatibility impact on ordinary Agent Skills.
