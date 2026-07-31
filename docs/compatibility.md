# Compatibility

ASEP-enhanced Skills remain ordinary Agent Skills.

An agent that only understands the base format can still:

- discover the Skill through frontmatter;
- read `SKILL.md`;
- load linked files from `references/`;
- run helpers from `scripts/`;
- use templates from `assets/`.

`references/adherence.yaml` is an optional companion for tooling. It must not contain the only copy of an essential instruction; important requirements should also be understandable from Markdown.
