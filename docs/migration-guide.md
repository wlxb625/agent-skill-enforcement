# Migrating an existing Skill

## Before

```text
my-skill/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

Keep this structure.

## Migration steps

1. Identify instructions the agent often ignores or replaces with defaults.
2. Move detailed explanations into focused files under `references/`.
3. Separate hard requirements, core methods, quality targets, and preferences in `SKILL.md`.
4. Add prohibited shortcuts and false substitutes.
5. Add current-task interpretation instructions.
6. Add output review and targeted revision instructions.
7. Optionally create `references/adherence.yaml`.
8. Run `asep validate ./my-skill`.

No new top-level package structure is required.
