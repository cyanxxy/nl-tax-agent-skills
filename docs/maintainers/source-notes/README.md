# Maintainer source notes

These reviewed notes support plugin architecture, future compatibility, and
rule-authoring decisions. They are repository evidence for maintainers, not tax
knowledge needed by a taxpayer workflow, so release bundles do not include
them.

- `platform/` records Claude Cowork, Claude plugin, ChatGPT Work, and Codex
  capability research.
- `compat/` records future ODB software-filing considerations; the runtime
  remains manual-entry only.
- `methodology/` records the RegelSpraak authoring approach.

Each directory keeps its reviewed-note hash metadata next to the note. A
`*-pending-review.md` file next to a reviewed note holds drafted corrections
that no human has reviewed yet; it has no hash entry and never counts as
reviewed. A maintainer merges it into the note, re-records the hash, and
deletes it. Recheck
the cited official pages before changing architecture or claiming a newly
available host capability.
