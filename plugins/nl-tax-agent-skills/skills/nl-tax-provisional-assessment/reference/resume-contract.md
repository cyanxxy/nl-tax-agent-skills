# Provisional resume compatibility

Load this reference only for a missing/empty progress file, a pre-1.4 progress
file, or a legacy complete profile that lacks the year-scoped AOW field. It is
a compatibility guide for the owning agent, not a state machine.

## Missing state

If `workspace/shared/session-progress.yaml` is missing or empty, return control
to `nl-tax-intake`. Do not create provisional artifacts or reconstruct the
intake-owned state.

## Pre-1.4 progress

Migrate in place as defined by the shared elicitation contract. Add missing
`provisional_2026.subsections.box2`, `annual_2025.subsections.winst`, and
`provisional_2026.subsections.winst_forecast` entries without changing existing
answers, then set version 1.4. Treat provisional `box2` and `winst_forecast` as
generation-gate members.

Mark either subsection `complete` with a stable answered `not applicable`
entry only when profile facts or a user answer establish that it does not
apply. Skip any subsection already marked `complete`.

## Legacy AOW profile

If an otherwise complete profile lacks
`person.aow_by_tax_year.2026.status`, do not restart intake and do not use a
legacy boolean as a substitute. From a sourced, undisputed date of birth and
the reviewed AOW note, record `below_all_year`, `reaches_during_year`, or
`aow_all_year` in the 2026 profile entry and provisional AOW notes with
`source: calculated`. For a transition, also record the month. Normalize the
partner separately when applicable; never copy a 2025 scalar into 2026 unless
its original tax year is unambiguous.

If the date of birth is missing or disputed, ask for that fact and keep the
rate/credit review open. This is conversational profile normalization, not a
script or tax-decision engine.
