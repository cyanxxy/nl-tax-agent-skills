# NL Tax Agent Skills

Prepare your Dutch income tax with an assistant that reads your documents,
asks only the questions that matter, and builds a reviewable, source-cited
workpack for manual entry in Mijn Belastingdienst. It covers the **annual
return 2025** and the **voorlopige aanslag 2026** (request, change, review, or
stopzetten), and answers rule questions for both years.

It also prepares **draft-only previews**: ZZP VAT returns and corrections,
ICP declarations, OSS and IOSS returns, M (migration) and C (nonresident)
income-tax returns, and evidence collection for the resident annual return
2026 (see [Draft-only previews](#draft-only-previews) below). Their official
sources await human tax-content review, so these drafts are not filing-ready
and no checklist with filing amounts is produced until that review clears.
You, or someone you have authorized, file VAT, ICP, and OSS returns (for
example in Mijn Belastingdienst Zakelijk); the plugin never does.

> **Not tax advice.** This plugin prepares workpacks and manual-entry guidance
> only. It never logs in, signs, or submits anything, and its output is not an
> official calculation. You review everything and enter it yourself.

## How to use it

Attach or select your documents (jaaropgaaf, mortgage statement, bank
overview, and so on) and ask in plain language:

```text
Help me prepare my 2025 Dutch income-tax workpack. I have my year statement and mortgage summary.
```

```text
Help me request a 2026 voorlopige aanslag. Ask me for the estimates you still need.
```

```text
What is the Box 3 heffingsvrij vermogen for 2025?
```

Everything happens in the conversation. The assistant reads your documents
directly, asks for missing facts, and shows the workpack, in which every amount
names its source. It then maps each amount to its Mijn Belastingdienst field and
can produce a manual-entry checklist. A rule question gets a sourced answer with
the tax year.

If you correct a figure after the workpack is generated, the field map and any
checklist are marked **STALE** and the assistant will not give you checklist
values until you confirm regenerating them, so an old amount is never copied
into the portal.

## Saving your work

The plugin writes nothing unless you ask. Tax preparation can take a few
sessions, so the assistant offers to keep your workpack as a file when the
workflow starts, when you pause, and after the workpack is generated, each at
most once and always as the only question in its reply (tell it not to ask
again and it stops). Say yes, or "save my workpack" at any time, and it keeps
**one file per workflow** (and, for VAT, ICP, and OSS, one per period or
scheme) in a `workspace/` folder inside your working folder:

- `workspace/nl-tax-annual-2025-workpack.md` for the annual 2025 return
- `workspace/nl-tax-provisional-2026-workpack.md` for the 2026 voorlopige aanslag
- `workspace/nl-tax-vat-<year>-<period>-workpack.md` for a draft VAT return
- `workspace/nl-tax-vat-correction-<year>-<period>-workpack.md` for a draft VAT
  correction of one already filed period
- `workspace/nl-tax-icp-<year>-<period>-workpack.md` for a draft ICP declaration
- `workspace/nl-tax-oss-<scheme>-<year>-<period>-workpack.md` for a draft OSS or
  IOSS return, where the scheme is `union`, `non_union`, or `ioss`
- `workspace/nl-tax-international-<year>-<form>-workpack.md` for a draft M or C
  return, where the form is `migration` or `nonresident`
- `workspace/nl-tax-annual-2026-workpack.md` for the draft annual return 2026

The year is 2025 or 2026. The period is the filing period the Belastingdienst
assigned to you: a quarter (`Q1`–`Q4`), a month (`M01`–`M12`), or, for VAT and
ICP only, `Y` for an assigned annual filing period. OSS Union and non-Union
returns are quarterly and IOSS returns are monthly. A period's file never
overwrites another period's file.

That one readable Markdown file holds your facts with their sources, the open
questions, the field map, and the manual-entry checklist. It is your file: to
continue later, attach it or keep it in the working folder. Consent covers the
current conversation: in a new one, the assistant confirms a saved file before
using or updating it, and asks before replacing an older file it did not
resume; it never merges into one. Showing the workpack in the chat creates no
file. In a cloud task whose folder may not outlast the session, it also gives
you the workpack as a download at pauses and at generation: keep that download
to resume. Delete the file whenever you like; the plugin never deletes files.
Say "stop saving" and it stops updating the file.

## What the plugin runs, reads, writes, and fetches

- **Runs:** nothing. The package ships Markdown and YAML only: no scripts,
  hooks, MCP servers, or package installs. No shell or Python is needed, and
  skills pre-approve no shell commands.
- **Reads:** its bundled, source-cited Dutch tax notes, plus the documents,
  folders, and saved workpack you select or attach.
- **Writes:** nothing by default. Only after you agree to save, one workpack
  file per workflow, period, scheme, or form (the paths above) and nothing
  else. Skills pre-approve
  file edits for `./workspace/**` only, and never copy, move, rename, or change
  your documents.
- **Fetches:** nothing by default; skills answer from the bundled notes. When a
  workflow calls for a freshness check, the assistant may read public official
  pages such as belastingdienst.nl. In Claude, the bundled read-only
  `nl-tax-specialist-reviewer` agent may also read public official sources for
  such a freshness check; it writes nothing. The plugin sends your data to no
  one and never opens Mijn Belastingdienst, Mijn Belastingdienst Zakelijk, or
  any other authenticated portal.

The plugin runs inside your AI host, which processes the documents and
conversation you share under its own terms.

## What is supported

| Workflow | Year |
|---|---|
| Annual income-tax return, including Box 1 and own home, Box 2, Box 3, and deductions | 2025 |
| Winst uit onderneming for a straightforward eenmanszaak / ZZP | 2025 |
| Voorlopige aanslag: request, change, review, stopzetten | 2026 |
| Rule questions, including the rules behind the draft-only previews | 2025 / 2026 |
| Draft ZZP VAT return, KOR screening, and correction or suppletie of one filed period (no checklist) | 2025 / 2026, exact assigned period |
| Draft ICP declaration (no checklist) | 2025 / 2026, exact period |
| Draft OSS Union, OSS non-Union (quarter), or IOSS (month) return (no checklist) | 2025 / 2026, exact scheme and period |
| Draft M (migration) or C (nonresident) income-tax return (no checklist) | 2025; 2026 evidence collection only |
| Draft resident annual income-tax evidence collection (no checklist) | 2026, pending year-end |

For Box 3, annual 2025 compares the fictitious and actual-return methods as
information only; provisional 2026 uses the fictitious method only. Other
business forms (VOF, maatschap, CV, DGA/BV, staking), returns for a deceased
person, and tax year 2027 are routed to manual review or blocked. Part-year
residence (emigration or immigration) and nonresidence use the draft migration
(M) or nonresident (C) workflow; disputed residence and treaty questions stay
review blockers.

## Skills

| Skill | Role |
|---|---|
| `nl-tax-intake` | Checks scope and starts the right workflow; writes nothing |
| `nl-tax-knowledge` | Answers 2025 / 2026 rule questions; writes nothing |
| `nl-tax-annual-return` | Prepares the annual 2025 workpack and reads your documents |
| `nl-tax-provisional-assessment` | Prepares the 2026 voorlopige aanslag workpack and reads your documents |
| `nl-tax-annual-return-2026` | Collects draft evidence for the resident annual return 2026 in its own workpack, without reusing the 2025 or provisional forms |
| `nl-tax-vat-return` | Reconciles a period's invoices, input VAT, and rubrics into a draft VAT workpack |
| `nl-tax-vat-correction` | Keeps the filed and revised totals of one filed period and prepares draft correction or suppletie material |
| `nl-tax-icp` | Prepares a draft opgaaf ICP for one period, using customer aliases and reconciling it with VAT rubric 3b |
| `nl-tax-oss` | Prepares a draft OSS Union, OSS non-Union, or IOSS return per scheme and period, with each country's amounts kept separate |
| `nl-tax-international-return` | Prepares a draft M-biljet (emigration or immigration year) or C-biljet (nonresident) from your residence facts and documents |
| `nl-tax-field-mapper` | Maps workpack amounts to Mijn Belastingdienst fields; the only author of the field map |
| `nl-tax-submit-companion` | Builds a manual-entry checklist when you ask for one; for a draft-only preview it lists only the blockers |
| `nl-tax-box1-home`, `nl-tax-box2`, `nl-tax-box3`, `nl-tax-winst`, `nl-tax-partner-deductions`, `nl-tax-vat-adjustments` | Background helpers the workflows consult; they write nothing |

`skills/nl-tax-shared-resources/` holds the source-cited knowledge notes (the
VAT, cross-border, international, and annual 2026 notes still await human
review), the source register, and the shared runtime contract. Install the
plugin as one package: the skills reference each other through sibling paths.

## Draft-only previews

The VAT, ICP, OSS/IOSS, M/C, and annual 2026 workflows produce draft workpacks
only. Their rules come from official sources that a human tax reviewer has not
yet checked, and the exact Mijn Belastingdienst screens for the annual 2026 and
M/C returns are not final. Until that review is done, the assistant never calls
these drafts complete or ready to file, and a requested manual-entry checklist
lists only the blockers, without amounts.

- **VAT.** VAT preparation assumes a Netherlands-established eenmanszaak and a
  confirmed accounting system, rate, and deduction treatment. Evidenced
  calculations for private use of a business car, mixed taxable and exempt
  use, revision of investment goods and property, BUA, and the margin scheme
  go through the read-only `nl-tax-vat-adjustments` helper. Unresolved KOR
  transitions, import goods, and any undecided classification or election (for
  example a property or margin choice) remain review blockers.
- **ICP and OSS.** Each has its own workpack, separate from the domestic VAT
  return, so no amount is silently merged into it. You check and enter your
  customers' real VAT identification numbers yourself in the portal; the
  workpack keeps only an alias for each customer.
- **M and C returns.** The workflow records your residence periods, Dutch and
  foreign income, insurance periods, and the proof needed for qualifying
  nonresident status. Treaty questions specific to a country stay with a human
  tax professional.
- **Annual 2026.** The year 2026 is still open, so the workflow collects actual
  evidence with its coverage dates and leaves year-end documents pending. For
  an estimate of 2026, use the voorlopige aanslag workflow instead.

Example requests: "Prepare a draft ZZP btw-aangifte for Q3 2026 from my sales
and purchase ledgers", "Prepare my Q3 2026 ICP draft", "Prepare my union OSS
draft for Q3 2026", "Prepare my 2025 M-biljet", or "Start my annual 2026
income-tax draft".

## More

- [Privacy](https://github.com/cyanxxy/nl-tax-agent-skills/blob/main/PRIVACY.md):
  what the plugin reads, stores, and sends (it sends nothing), and how to delete
  a saved workpack.
- Install steps and contributor docs: <https://github.com/cyanxxy/nl-tax-agent-skills>. Licensed under Apache-2.0;
see the bundled [LICENSE](LICENSE).
