# Templates

Copy these; do not import them. They are starting points, and a template you
have not adapted is a sign you have not yet decided what your units are.

```
workspace/    The root of a new workspace: AGENTS.md, CLAUDE.md, README.md
unit/         The three-file contract, plus an optional unit-level AGENTS.md
variants/     Kind-specific README shapes, for when one shape is not enough
```

## Placeholders

Placeholders are in `{curly braces}`. The `new-unit` script substitutes
`{Unit name}`, `{YYYY-MM-DD}` and `{Summary}` automatically; everything else
is filled in by hand.

Delete placeholder lines that do not apply to a unit rather than leaving them
empty. An empty field reads as missing information; a deleted one reads as not
applicable.

## Variants

`unit/README.md` is the generic shape. Real workspaces usually want a few
kind-specific ones, because a project and a person need different fields.
`variants/` holds three to show the pattern:

- `project_README.md` for work with a beginning and an end.
- `area_README.md` for standing responsibilities.
- `person_README.md` for a note about a collaborator.

Add your own. A research workspace might want separate variants for papers,
grants and applications; a consultancy might want one per client tier. Keep
the three-file contract identical across kinds and vary only the README.

Some kinds also want a fourth file. A person you supervise formally, for
instance, may need a `TIMELINE.md` of milestones, which is neither present
state nor past decision and so fits neither `STATUS.md` nor `LOG.md`.
