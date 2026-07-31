# Migration from Contract Skills 0.1 draft

The project was renamed because the central idea is **enforcement**, not merely contract description.

## Repository

Rename `contract-skills` to `agent-skill-enforcement`. GitHub automatically redirects old repository URLs after a rename.

## Manifest

Before:

```yaml
contract_skill:
  spec_version: "0.1.0-draft"
  kind: contract-skill
```

After:

```yaml
enforcement:
  protocol: ASEP
  spec_version: "0.2.0-draft"
  kind: enforced-agent-skill
```

## CLI and Python

- command: `contract-skill` → `asep`
- distribution: `contract-skills-validator` → `asep-validator`
- Python module: `contract_skills` → `asep`

## Runtime values

- `soft-contract` → `soft-enforcement`
- `CONTRACT_COMPLETE` → `ASEP_COMPLETE`
- `.contract/state.json` → `.asep/state.json`

This is a breaking draft migration. No compatibility aliases are required before 1.0, but host implementations may accept both forms during transition.
