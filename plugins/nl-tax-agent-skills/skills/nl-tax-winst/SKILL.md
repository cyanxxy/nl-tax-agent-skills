---
name: nl-tax-winst
description: Internal helper for nl-tax-annual-return — returns winst uit onderneming (eenmanszaak / ZZP) facts and questions. Not a standalone workflow; invoked as a sub-step for the 2025 annual return only.
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3:*)
---

# NL Tax Winst uit onderneming

Background helper for winst uit onderneming preparation notes for the **2025
annual return**. It supports the standard IB-ondernemer with an **eenmanszaak**
(the usual ZZP legal form): winst uit onderneming, ondernemersaftrek,
MKB-winstvrijstelling, and kleinschaligheidsinvesteringsaftrek.

Use this skill only for source-backed preparation support for `annual_2025`.
There is no provisional entrepreneur flow: never prepare winst uit onderneming for
a 2026 voorlopige aanslag.

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

There are no bundled calculators for this helper. Compute the ordering (winst →
minus investeringsaftrek such as KIA → minus ondernemersaftrek →
MKB-winstvrijstelling) by hand from the sourced amounts;
if the host ever adds a script under an already-resolved plugin
`skills/.../scripts/` path, run it only when Bash can reach that path, and always
keep the declarative fallback of continuing manually from the sourced inputs and
rules. Never copy bundled scripts into `workspace/`, and never execute a `.py`
under `workspace/`, `uploads/`, or `evidence/`.

## Do

- Confirm the taxpayer is an ondernemer voor de inkomstenbelasting with an
  eenmanszaak, and record whether the urencriterium (or, for the startersaftrek
  bij arbeidsongeschiktheid, the verlaagd urencriterium) is met.
- Prepare the winst uit onderneming: turnover minus deductible business costs,
  then investeringsaftrek such as KIA, then ondernemersaftrek, then the
  MKB-winstvrijstelling, in that order.
- Prepare the ondernemersaftrek components the case qualifies for
  (zelfstandigenaftrek, startersaftrek, S&O-aftrek, meewerkaftrek), reading the
  2025 amounts from the knowledge notes.
- Prepare the kleinschaligheidsinvesteringsaftrek from the KIA table when the
  taxpayer invested in qualifying bedrijfsmiddelen.
- Note the beperkt-aftrekbare-kosten threshold (or the 80% election), werkruimte
  conditions, the private-use-of-a-business-car bijtelling, and the private-vehicle
  kilometre deduction where they apply — as preparation notes, not final figures.
- Keep outputs suitable for preparation workpacks and review questions.
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
```

The calling skill asks these questions, records the answers with `source`,
`quote`/`evidence_id`, and timestamp under its own annual notes tree, then re-runs
this helper contract. Do not write caller-owned notes.

## Never

- Do not log in, automate a browser, sign, or submit anything.
- Do not claim that the helper gives binding tax advice or a final assessment.
- Do not prepare winst uit onderneming for a 2026 voorlopige aanslag; the
  entrepreneur unlock is annual 2025 only.
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
state, workpacks, or field maps. The annual workflow owns all workspace
persistence and may read historical helper notes for resume compatibility only.
