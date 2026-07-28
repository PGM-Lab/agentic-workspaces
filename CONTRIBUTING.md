# Contributing

This started as one person's working setup. It is shared because the design
choices might be useful to others, and because other people's constraints will
expose the places where those choices are wrong.

## The most useful feedback

In rough order of value:

1. **You tried it and something broke.** A rule that could not survive contact
   with your actual work. Say what you were doing and where it fell apart.
   This is worth more than any suggestion in the abstract.
2. **Your field needs a different unit.** The contract assumes work comes in
   units with a beginning and an end, plus standing areas. If your work does
   not decompose that way, say what it looks like instead.
3. **A template field that is always empty, or always missing.** Templates
   should have exactly the fields people fill in.
4. **A skill that does the wrong thing.** Especially `session-log`, which is
   the piece everything else depends on.
5. **A tool the setup does not survive.** If your agent ignores `AGENTS.md` or
   loads skills differently, that is worth documenting.

## What this is not looking for

- Turning it into an application. The whole point is that these are files.
- A schema, a linter, or required fields. The contract is three files with a
  clear rule each. Every addition has to earn its place.
- Support for every possible agent. The two open standards it builds on
  (`AGENTS.md` and `SKILL.md`) are the compatibility layer. If a tool reads
  those, it works.

## How

Open an issue. Prose is fine, no template to fill in. If you are proposing a
concrete change to a file, a pull request is easier to discuss than a
description of one.

For workspace-specific adaptations, do not send them upstream. Fork or copy.
The repository holds the generic core on purpose; the interesting parts of
your setup will be the parts that are specific to you.

## A note on what you commit

If you send an example taken from your own workspace, strip it first. Names,
institutions, grant numbers, student data, anything under review. The
`examples/` folder here is fictional for that reason.
