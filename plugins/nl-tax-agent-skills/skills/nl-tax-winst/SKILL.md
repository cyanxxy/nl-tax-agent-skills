---
name: nl-tax-winst
description: "Background helper with two narrow modes: organize annual 2025 business-section evidence without calculating final taxable profit, or return one sourced 2026 provisional expected-profit forecast."
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3:*)
---

# NL Tax Winst uit onderneming

Background helper with two deliberately narrow modes:

- **Annual 2025 preparation-only:** organize facts, evidence, and questions for
  the business section of an eenmanszaak/ZZP return. Require a finalized
  profit-and-loss statement and finalized balance. Do not derive final taxable
  business profit and do not claim the business return is complete.
- **Provisional 2026 expected-profit forecast:** record the taxpayer's sourced,
  user-reviewed forecast for `Winst uit onderneming` as
  `onderneming.geschatte_winst`. Do not prepare annual accounts, deductions,
  Zvw, cessation profit, or final tax.

This helper may be called through a Skill/Task tool or inlined by an owning workflow when no such tool exists. The same output contract applies either way.

## Read first

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second `workspace/`
tree. `_shared/` is the plugin-shared folder at this skill's `../_shared/`.
Resolve bundled files with host file tools (`Read` first, `Glob` or `Grep` if a
path is not obvious). Do not use Bash to discover or read plugin files: in Cowork,
shell commands run in an isolated VM that may not see the plugin cache even when
`Read` and `Glob` can. If the host has already expanded `${CLAUDE_PLUGIN_ROOT}`
or `${CLAUDE_SKILL_DIR}`, those absolute paths are fine for file tools; otherwise
search within the loaded plugin/skill tree and resolve relative to this skill
directory.

Read the reviewed 2025 knowledge notes — they are canonical for every rate,
amount, and threshold. Never paraphrase a figure from memory; read it from these
files and return each `source_id` to the owning workflow so that workflow can
append it to `session-progress.yaml` → `sources_loaded`:

- `../_shared/knowledge/years/2025/entrepreneur/ondernemer-criteria.md`
- `../_shared/knowledge/years/2025/entrepreneur/ondernemersaftrek.md`
- `../_shared/knowledge/years/2025/entrepreneur/mkb-winstvrijstelling.md`
- `../_shared/knowledge/years/2025/entrepreneur/investeringsaftrek.md`
- `../_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md`
- `../_shared/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md`
- `reference/winst-2025.md` — how the pieces fit together for the workpack
- `reference/winst-2026-provisional.md` — bounded expected-profit forecast

There are no bundled calculators for this helper. Its job is classification and
question generation, not completing the taxpayer's accounts or tax computation.

## Do

- Select annual or provisional mode from the owning workflow; never blend them.
- For annual mode, confirm the finalized profit-and-loss statement and balance
  belong to tax year 2025 and are internally identified as final/reviewed.
- Organize official profit-and-loss and balance categories, entrepreneur status,
  hours, investments, and deduction evidence into sourced facts and questions.
  Record candidate deductions only as review facts; do not calculate them.
- For provisional mode, collect one expected-profit forecast for the full 2026
  year, its basis, source provenance, and explicit user review. Return only
  `onderneming.geschatte_winst` plus review notes and open questions.
- Keep outputs suitable for preparation workpacks and manual review.
- When facts are missing, return a structured question packet instead of
  inventing zeros.

## Question packet

Return missing inputs to the calling workflow in this shape:

```yaml
- question_id: "annual.winst.ondernemer.status"
  workflow: "annual_2025"
  section: "winst.ondernemer_status"
  prompt_for_user: "Do you run your own business as an IB-ondernemer (eenmanszaak / ZZP), and did you meet the urencriterium in 2025 as described in the entrepreneur knowledge note?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "KvK registration, urenadministratie, winst-en-verliesrekening"
- question_id: "annual.winst.ondernemersaftrek.startersaftrek"
  workflow: "annual_2025"
  section: "winst.ondernemersaftrek"
  prompt_for_user: "For the regular startersaftrek: in 2020-2024, were you not an IB-ondernemer in at least one calendar year, and was the zelfstandigenaftrek applied at most twice in those years? Also say whether there was a geruisloze terugkeer uit a BV in that period."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "prior-year aangiften or aanslagen, notes on start date and ondernemersaftrek history"
- question_id: "annual.winst.result.omzet_kosten"
  workflow: "annual_2025"
  section: "winst.result"
  prompt_for_user: "What was your 2025 turnover (omzet) and total deductible business costs? A winst-en-verliesrekening or bookkeeping export is ideal."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "winst-en-verliesrekening, balans, facturen"
- question_id: "provisional.winst.expected_profit"
  workflow: "provisional_2026"
  section: "winst_forecast"
  prompt_for_user: "What is your reviewed best estimate of full-year 2026 profit from the enterprise, and what forecast or current bookkeeping supports it?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "current profit forecast, year-to-date bookkeeping, or user-reviewed estimate"
```

The calling skill asks these questions, records the answers with `source`,
`quote`/`evidence_id`, and timestamp under its own workflow notes tree, then
re-runs this helper contract. The annual workflow owns persistence in annual
mode. The provisional workflow owns persistence in provisional mode. The helper
owns no persisted artifact. Do not write caller-owned notes.

## Never

- Do not log in, automate a browser, sign, or submit anything.
- Do not claim that the helper gives binding tax advice or a final assessment.
- Do not turn annual preparation notes into a final taxable-profit computation,
  completed business return, or filing-ready business field map.
- Do not turn the provisional expected-profit forecast into business accounts,
  annual deductions, Zvw, cessation profit, or final tax.
- Do not route complex business cases as standard preparation. Partnerships (VOF,
  maatschap, CV) and profit-share allocation, medegerechtigdheid, DGA/BV winst,
  agrarische ondernemingen, zeevarenden, staking/cessation events,
  herinvesteringsreserve, oudedagsreserve wind-down, and resultaat uit overige
  werkzaamheden all go to manual review.
- Do not treat a btw-ondernemer as automatically an IB-ondernemer.
- Do not write field maps, annual/provisional workpack templates, source
  registers, supported workflow files, or shared eval data.

Return structured facts and open questions to the owning workflow. Do not
persist any final artifact, including shared notes, question packets, session
state, workpacks, or field maps. In either mode, only the calling owning workflow
may read historical helper notes for resume compatibility.
