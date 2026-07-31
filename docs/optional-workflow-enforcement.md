# Optional workflow enforcement

Some tasks need more than adherence-oriented authoring.

Examples include audits, regulated reviews, deployment, and multi-stage production processes where a later step must not begin before an earlier check passes.

Such Skills may add:

- explicit workflow steps in `SKILL.md`;
- scripts that validate stage artifacts;
- host-managed state;
- blocking review gates;
- completion controls.

These mechanisms are optional. They should be introduced only when the task genuinely needs process enforcement. A simple design or writing Skill should not require a state machine merely to improve adherence.
