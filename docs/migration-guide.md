# Migrating an existing Agent Skill

## Before

```text
my-skill/
├── SKILL.md
├── scripts/
├── references/
└── templates/
```

## After

```text
my-skill/
├── SKILL.md
├── EXECUTION.yaml
├── constitution/immutable.yaml
├── adaptive/default-policy.yaml
├── stages/
├── gates/
├── evaluators/
├── schemas/
├── scripts/
├── references/
└── templates/
```

## Migration questions

1. Which steps are genuinely mandatory?
2. Which rules are professional invariants?
3. Which rules are only preferences or guidance?
4. What artifact proves each stage happened?
5. What can be checked deterministically?
6. What requires semantic evaluation?
7. What evidence must support a score?
8. What happens after failure?
9. What must be true before final delivery?
10. What can the host actually enforce?

## Common mistake

Do not copy an entire domain checklist into immutable policy. Protect only the rules that must never be weakened. Domain-specific quality rubrics belong in gates and evaluators.
