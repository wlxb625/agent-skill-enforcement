---
name: cinematic-web-designer
description: Design and implement visually distinctive, motion-driven websites where layout, media, and interaction support the content. Use for landing pages, portfolios, campaign sites, and product experiences that should avoid generic AI-generated UI patterns.
license: MIT
metadata:
  version: "0.3.0"
  asep-profile: strict
---

# Cinematic Web Designer

## Required references

Read these files before choosing a visual direction:

- `references/design-principles.md`
- `references/anti-patterns.md`
- `references/quality-criteria.md`

Use `assets/page-concept-template.md` when planning the page.

## Core requirements

1. Do not use a repeated card grid as the primary page composition.
2. Scroll must change space, focus, information relationships, or narrative state—not only opacity.
3. Images and video must carry information or transition the story, not function only as decoration.
4. Different sections must not all use the same entrance animation.
5. Motion must clarify hierarchy, continuity, or meaning rather than exist only to look active.

## How to apply this Skill

Before implementation, convert every relevant core requirement into a concrete decision for the current page. Record the decisions using `assets/page-concept-template.md`.

While building each section, reload the relevant requirements and anti-patterns. Do not replace a difficult requirement with a simpler visual effect merely because it is easier to implement.

## Implementation

Choose the technology that best fits the project. Sticky scenes, masks, video sequences, SVG, canvas, WebGL, and ordinary DOM animation are all acceptable when they serve the content.

## Review and revision

Render and inspect the actual desktop and mobile page. For motion-led sections, inspect the beginning, middle, and end states. Compare the result with `references/quality-criteria.md`.

Preserve successful typography, content, and layout decisions. Revise sections that fall back to the anti-patterns.
