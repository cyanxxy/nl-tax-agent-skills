---
name: nl-tax-knowledge
description: "Use when the user asks how a Dutch tax rule works for 2025 or 2026: boxes 1-3, eigen woning, voorlopige aanslag, zzp, btw/VAT, ICP, OSS or migration. Answers from sourced notes; writes no files."
argument-hint: "[tax-rule question]"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# NL Tax Knowledge

Answer Dutch individual income-tax and VAT (btw) rule questions from the
source-cited notes bundled with this plugin. The income-tax notes for the annual
2025 return and the voorlopige aanslag 2026 are reviewed. The VAT, VAT
adjustment, ICP, OSS/IOSS, international (M/C) and annual 2026 notes are draft
notes with review status `needs_review`. This skill is a read-only lookup
that writes nothing: it never creates or updates `workspace/` files, workpacks,
field maps, or checklists.

## Always-on authenticated-portal boundary

Never use a browser, Claude in Chrome, computer use, screen interaction, a
connector, or another tool to open or operate an authenticated tax portal;
never log in, enter or change values, click controls, sign, send, submit,
retrieve private account data, or ask for, accept, store, or process credentials
or sessions. Those actions remain human-only even with taxpayer permission or
available credentials. Describe every portal step with an explicit human
subject, such as "You (the taxpayer)".

## Scope

- Covered (reviewed notes): the annual income-tax return for 2025 and the
  voorlopige aanslag (provisional assessment) for 2026, including supported
  sole-trader topics.
- Covered (draft notes with review status `needs_review`; disclose that status
  in every answer): the btw-aangifte (VAT return) and suppletie (VAT
  correction) for 2025 and 2026, VAT adjustments (private use, pro-rata
  deduction, herziening, property, BUA and the margeregeling), the opgaaf ICP,
  OSS and IOSS, the 2025 M-biljet (migration year: emigratie or immigratie) and
  C-biljet (nonresident) returns with 2026 precollection, and the resident
  annual income-tax return for 2026 (aangifte inkomstenbelasting 2026).
- Not covered: tax years other than 2025 and 2026, corporate tax, payroll tax,
  and foreign tax rules. OSS destination-country rates come only from
  evidence the user or an adviser supplies. Say that the bundled notes do not
  cover the question; do not fill the gap from model memory.
- If the user asks to prepare, organize, request, change, review, or stop a
  workpack, that is preparation intent. Continue with the plugin's preparation
  workflow in the same conversation instead of answering here.

## Look up the answer

Resolve every path below relative to this skill directory with the host's file
or skill-resource tools. Python and shell access are not needed. The resource
and portal rules in `../nl-tax-shared-resources/runtime-contract.md` apply;
read it when a question touches a portal procedure, a Box 3 method comparison,
or a partner allocation.

1. Read `../nl-tax-shared-resources/knowledge-index.md`.
2. Match the question's year and workflow first, then its topic. Open only the
   one or two notes the index names for it.
3. For how to request, change, or stop a voorlopige aanslag 2026, open the
   human-subject runtime projections the index lists under
   `../nl-tax-provisional-assessment/reference/source-projections/`. Never open
   the raw `request-flow.md`, `change-flow.md`, or `stopzetten-flow.md` notes.
4. If the index does not settle the choice, search for the Dutch or English
   term only inside `../nl-tax-shared-resources/knowledge/`. Do not search or
   list the rest of the plugin, and never read test, eval, fixture, or
   repository files.
5. Read the selected note's `source_ids` header, then search
   `../nl-tax-shared-resources/source-register.yaml` for only those entries to
   get each source's title and official URL. Do not read the complete register.
6. If a named path cannot be opened, report that exact path and say the plugin
   may be installed incompletely. Do not guess other filenames.

## Answer

- VAT notes marked `needs_review` are draft source summaries: disclose their
  review status, link the official source, and do not present them as reviewed
  filing positions. No VAT return preparation starts for an informational
  question. Keep the year and accounting system explicit; KOR is separate
  from IB entrepreneur status.

- Answer from the note and its matched source entries, not model memory. State
  which tax year every amount, percentage, or threshold belongs to, and name the
  official source when it helps the user check it.
- Keep 2025 annual, 2026 provisional and 2026 annual rules separate. Never
  answer a 2026 question from a 2025 note or the reverse, and never answer an
  annual 2026 question from a voorlopige aanslag 2026 note or the reverse.
  Clarify annual versus provisional only when a 2026 income-tax question is
  ambiguous and that distinction changes the answer. A clear VAT, ICP or OSS
  question needs no income-tax workflow screening.
- Apply each note's "Developer instruction" and "Common failure" sections as
  guidance, and state any manual-review or unsupported boundary the note sets.
- Box 3, voorlopige aanslag 2026 (not the annual 2026 return): fictitious
  method only. If the user asks about werkelijk rendement for the voorlopige
  aanslag 2026, say: "Werkelijk rendement may become relevant when filing the
  annual 2026 return in 2027." For a question about werkelijk rendement in the
  annual 2026 return, answer from the annual 2026 draft note instead and
  disclose its `needs_review` status.
- Box 3, annual 2025: explain the fictitious and actual-return comparison as
  information only. The official filing environment performs the binding
  comparison and uses the more favorable amount; do not recommend or select a
  method.
- Fiscal partners: explain which items can be allocated and how the rules work.
  Never call one split best, optimal, or recommended; the partners choose.
- A short illustration with figures the user supplies is fine. Label it as an
  illustration from the cited rule, not a workpack or filing position.
- Answer directly. Ask no screening questions and collect no personal data,
  BSN, or documents. A short offer to prepare a workpack later is fine.
- Keep file loading and lookups invisible. Do not mention skill names, paths,
  or the index unless the user asks where the information comes from.

For VAT, VAT adjustment, ICP, OSS/IOSS, international (M/C) and annual 2026
questions, use the draft notes the knowledge index lists for that topic and the
exact tax year of the source. Disclose that the note awaits human review
(`needs_review`), link the official source, and never describe a draft note as
a reviewed filing position or as ready for filing. A general rule question does
not start a workpack. The source and schema gates for preparation remain in the
owning workflow skill.
