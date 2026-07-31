# Authoring guide

## Start from an ordinary Skill

Create or keep the normal structure:

```text
my-skill/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

Do not begin by adding protocol-specific directories.

## 1. Separate requirement strength

Rewrite mixed guidance into four groups:

- hard requirements;
- core methods;
- quality targets;
- preferences.

## 2. Name prohibited substitutions

For each important requirement, ask: what is the easiest default pattern an agent might use while claiming it followed this rule?

Write those substitutions explicitly.

## 3. Link required references directly

List required files in `SKILL.md`. Keep detailed content in `references/` so agents load only what they need.

## 4. Require current-task interpretation

Before generating the relevant artifact, instruct the agent to translate the general requirement into a concrete decision for the current task.

This should be a compact planning artifact, not private chain-of-thought disclosure.

## 5. Keep requirements active

During long tasks, instruct the agent to reload or restate only the requirements relevant to the current component or revision.

## 6. Review actual output

Review rendered pages, complete writing, actual code, or other real artifacts. Do not accept an explanation of the output as a substitute for inspecting it.

## 7. Revise selectively

Preserve compliant parts and repair the parts that drifted from the Skill.

## 8. Add the optional profile

Add `references/adherence.yaml` when machine validation, tooling, or shared templates would be useful.
