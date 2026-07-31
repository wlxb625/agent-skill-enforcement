# Agent Skill Enforcement 0.3 Draft

ASEP 0.3 changes the project from a lifecycle-first enforcement protocol into an adherence-first extension of the normal Agent Skills format.

## Main change

The core problem is not only whether an agent completed a workflow. It is whether the agent actually followed the Skill's methods instead of returning to its default patterns.

## Included

- standard `SKILL.md`, `references/`, `scripts/`, and `assets/` compatibility;
- optional `references/adherence.yaml` schema;
- requirement levels;
- prohibited substitutions;
- current-task interpretation;
- requirement persistence during long tasks;
- drift-oriented review and targeted revision;
- updated CLI validator;
- minimal and web-design examples.

## Compatibility

`EXECUTION.yaml` and lifecycle enforcement from 0.2 are no longer required by the core profile. They may still be used as an optional advanced mechanism.
