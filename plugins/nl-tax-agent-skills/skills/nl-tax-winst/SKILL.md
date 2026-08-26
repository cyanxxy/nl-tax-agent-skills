---
name: nl-tax-winst
description: "Use when an owning Dutch tax workflow needs the annual 2025 belastbare winst uit onderneming determined from the reviewed profit chain, or one sourced 2026 provisional expected-profit forecast."
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3:*)
---

# NL Tax Winst uit onderneming

Background helper with two modes that are never blended:

- **Annual 2025 profit determination:** determine the belastbare winst uit
  onderneming for an IB-ondernemer by following the ordered chain in
  `winstberekening-2025.md` -- from a finalized profit-and-loss statement and
  finalized balance, through the investeringsaftrek, the ondernemersaftrek and
  the MKB-winstvrijstelling. Return that amount with every line of its
  derivation, its provenance, and its open questions to the annual workflow,
  which owns the box 1 total and every artifact.
- **Provisional 2026 expected-profit forecast:** record the taxpayer's sourced,
  user-reviewed forecast for `Winst uit onderneming` as
  `onderneming.geschatte_winst`. Do not prepare annual accounts, annual
  deductions, a Zvw amount, cessation profit, or final tax; raise the separate
  voorlopige aanslag Zvw with the taxpayer without sizing it.

This helper may be called through a Skill/Task tool or inlined by an owning workflow when no such tool exists. The same output contract applies either way.

## Read first

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second `workspace/`
tree. `_shared/` is the plugin-shared folder at this skill's `../_shared/`.
Read `../_shared/runtime-contract.md` first. Resolve bundled files relative to
this skill directory with the host's skill-resource or file tools. Do not
depend on shell visibility or vendor-specific environment variables.

Select the owning workflow's mode before loading mode-specific material. Never
load both modes for comparison.

For **annual 2025 profit determination**, read the reviewed 2025 knowledge notes
below. They are canonical for every rate, amount, and threshold. Never
paraphrase a figure from memory; return each loaded `source_id` to the owning
workflow so it can append the ID to the active workflow's
`session-progress.yaml` → `sources_loaded_by_workflow` list and mirror it in
top-level `sources_loaded`. Always read the first three. Open each remaining
note when the taxpayer's own facts touch it, and report the exact path when one
cannot be opened:

- `../_shared/knowledge/years/2025/entrepreneur/winstberekening-2025.md` -- the ordered chain, the winst cap, and the line each downstream base is read off
- `../_shared/knowledge/years/2025/entrepreneur/zakelijke-schema-2025.md` -- the winst-en-verliesrekening and balans rubrieken, the entrepreneur questions, the double-entry facts, and the `onderneming.*` identifiers
- `reference/winst-2025.md` -- the annual computation contract this helper follows
- `../_shared/knowledge/years/2025/entrepreneur/ondernemer-criteria.md` -- ondernemer status and the urencriterium
- `../_shared/knowledge/years/2025/entrepreneur/ondernemersaftrek.md` -- the components and their conditions
- `../_shared/knowledge/years/2025/entrepreneur/mkb-winstvrijstelling.md` -- the exemption and its base
- `../_shared/knowledge/years/2025/entrepreneur/investeringsaftrek.md` -- KIA, EIA, MIA, and the desinvesteringsbijtelling
- `../_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md` -- turnover, deductible and beperkt aftrekbare kosten, and the fiscal corrections
- `../_shared/knowledge/years/2025/entrepreneur/afschrijving-en-bedrijfsmiddelen-2025.md` -- vermogensetikettering, depreciation, and the fiscale-reserves boundary
- `../_shared/knowledge/years/2025/entrepreneur/vervoer-2025.md` -- car, bestelauto, private vehicle, and fiets treatment
- `../_shared/knowledge/years/2025/entrepreneur/aanloopfase-en-starters-2025.md` -- aanloopkosten, a first partial year, and the starter reliefs
- `../_shared/knowledge/years/2025/entrepreneur/partner-en-meewerken-2025.md` -- the meewerkende-partner routes and the arbeidsbeloning boundary
- `../_shared/knowledge/years/2025/entrepreneur/samenwerkingsverband-2025.md` -- recognition and routing of vof, maatschap, cv, medegerechtigde, agrarisch, and zeevarenden
- `../_shared/knowledge/years/2025/entrepreneur/row-en-dba-2025.md` -- the bron van inkomen pre-screen and the prepared resultaat uit overige werkzaamheden path
- `../_shared/knowledge/years/2025/entrepreneur/staking-2025.md` -- what a staking is, and where computation stops
- `../_shared/knowledge/years/2025/entrepreneur/verlies-en-verrekening-2025.md` -- a negative outcome and the niet-gerealiseerde zelfstandigenaftrek carry-forward
- `../_shared/knowledge/years/2025/entrepreneur/zvw-2025.md` -- the bijdrage Zorgverzekeringswet and its base
- `../_shared/knowledge/years/2025/entrepreneur/inkomensvoorzieningen-2025.md` -- lijfrente ruimte, AOV premiums, and the oudedagsreserve run-down
- `../_shared/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md` -- portal, channel, deadlines, and the evidence list

For **provisional 2026 expected-profit forecast**, load
`reference/winst-2026-provisional.md` together with the two 2026 knowledge notes
it names:

- `../_shared/knowledge/years/2026/provisional/winst-provisional-2026.md`
- `../_shared/knowledge/years/2026/provisional/zvw-provisional-2026.md`

Do not load the annual 2025 entrepreneur notes or `reference/winst-2025.md`;
this mode needs one sourced, user-reviewed forecast, not annual rates,
deductions, accounts, or the annual profit chain.

There are no bundled calculators for this helper. The chain is arithmetic the
agent performs itself from the reviewed notes, printing every line and the
evidence under it; it never replaces the taxpayer's own bookkeeping or an
adviser's judgment.

## Do

- Select annual or provisional mode from the owning workflow; never blend them.
- For annual mode, confirm the finalized profit-and-loss statement and finalized
  balance belong to tax year 2025 and are internally identified as
  final/reviewed. Without both, collect facts and questions and leave the chain
  unresolved rather than estimating a line.
- Run the bron van inkomen pre-screen and the category test before collecting any
  figure (`row-en-dba-2025.md`). Loon, winst uit onderneming, and resultaat uit
  overige werkzaamheden are decided per activity on facts the taxpayer confirms.
- Run the chain in `winstberekening-2025.md` strictly in its published order:
  winst uit onderneming, minus investeringsaftrek, minus ondernemersaftrek, minus
  the MKB-winstvrijstelling, giving the belastbare winst uit onderneming. Print
  each line with its amount, the note the rule came from, and the evidence under
  it, so the arithmetic stays traceable.
- Apply the winst cap on the ondernemersaftrek, and check the startersaftrek
  exception before applying it. When the cap bites, report the niet-gerealiseerde
  zelfstandigenaftrek, the beschikking that fixes it, and the fact that it is not
  set off automatically.
- State the tariefsaanpassing qualitatively when the threshold is in play, say
  that ordinary business costs and the investeringsaftrek are not affected, and
  say that the aangifte computes the correction itself. Never present an
  agent-computed correction as the amount that will be assessed.
- Return the belastbare winst uit onderneming to the annual workflow as the winst
  component of box 1, together with the downstream bases and the line each one is
  read off. Re-read the chain note before emitting them instead of recalling them
  from a similar case.
- Keep the computed chain in the workpack narrative. The aangifte computes the
  ondernemersaftrek components, their total, the MKB-winstvrijstelling, the
  kleinschaligheidsinvesteringsaftrek, and the belastbare winst itself from the
  figures and the yes/no answers the taxpayer types, so never return
  `onderneming.belastbare_winst`, `onderneming.zelfstandigenaftrek`,
  `onderneming.startersaftrek`, `onderneming.ondernemersaftrek_totaal`,
  `onderneming.mkb_winstvrijstelling`, or
  `onderneming.kleinschaligheidsinvesteringsaftrek` as manual-entry rows. Present
  each as a computed expectation the taxpayer checks on screen.
- Carry the vermogensvergelijking as a self-check: the winstberekening has to
  reconcile to the saldo of the winst-en-verliesrekening. Ask for the opening and
  the closing ondernemingsvermogen separately, report a mismatch, and never
  adjust a figure to force agreement.
- Recognise the taxpayer's business form and route it, using the per-form table
  in `reference/winst-2025.md`. Recognition, fact collection, and saying which
  reliefs fall away are in scope; the computation for a non-eenmanszaak form is
  not.
- On a negative outcome, say that the MKB-winstvrijstelling made the loss smaller
  and hand the loss to `verlies-en-verrekening-2025.md`. A loss year still
  requires a filed return.
- For provisional mode, collect one expected-profit forecast for the full 2026
  year, its basis, source provenance, and explicit user review. Return only
  `onderneming.geschatte_winst` plus review notes, the separate voorlopige
  aanslag Zvw point, and open questions. Never return a Zvw field or value for
  the income-tax field map; the companion is prose and a separate human check.
- Keep outputs suitable for preparation workpacks and manual review.
- When facts are missing, return a structured question packet instead of
  inventing zeros.

## Handoffs

- **Zvw.** An ondernemer receives a second, separate aanslag for the
  inkomensafhankelijke bijdrage Zorgverzekeringswet alongside the aanslag
  inkomstenbelasting, and one return feeds both. In annual mode, hand the
  belastbare winst uit onderneming to `zvw-2025.md` as the bijdrage-inkomen and
  let that note supply the percentage and the maximumbijdrage-inkomen. Ask
  whether the taxpayer also had loon, pensioen, or an uitkering and, for each,
  ask for the "loon Zorgverzekeringswet" on the jaaropgaaf, because the ceiling
  is shared; never assume there was none. Present the method, never a predicted
  assessment amount, and never deduct the bijdrage from the winst. In provisional
  mode, raise the separate voorlopige aanslag Zvw from
  `zvw-provisional-2026.md` without waiting to be asked. Say that the two
  assessments have separate change routes, that coupling is not established in
  the reviewed sources, and that the taxpayer checks the Zvw assessment
  separately and records what they find.
- **Lijfrente.** Hand the winst before the ondernemersaftrek to
  `inkomensvoorzieningen-2025.md` as the winst component of the premiegrondslag.
  The chain note fixes which line that is; `inkomensvoorzieningen-2025.md` fixes
  which year the premiegrondslag is measured over and owns every figure in the
  jaarruimte and the reserveringsruimte. AOV premiums are never a business cost.
- **The two bases are different figures.** The Zvw base sits at the end of the
  chain and the lijfrente base sits earlier, so the lijfrente base is the larger
  amount whenever the ondernemersaftrek or the MKB-winstvrijstelling is positive.
  Label both with their line and never reuse one amount for the other.
- **Resultaat uit overige werkzaamheden is a prepared path, not a dead end.**
  Prepare it as income minus deductible costs on the winstbepalingsregels, using
  `row-en-dba-2025.md` with `winst-en-kosten.md` and
  `afschrijving-en-bedrijfsmiddelen-2025.md`. The ondernemersaftrek, the
  MKB-winstvrijstelling, the investeringsaftrek, and the fiscale reserves are all
  absent; quantify what that costs from the taxpayer's own figures instead of
  describing it. The resultaat is reported in the privedeel under
  `box1.resultaat_overige_werkzaamheden`, it carries a bijdrage Zvw, it never
  opens the zakelijke schema, and it is not divisible between fiscal partners.
  Do not ask for an hours count in order to settle this category.

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
  prompt_for_user: "For the regular startersaftrek: in the calendar years before 2025, were there years in which you were not an IB-ondernemer, and how often has the zelfstandigenaftrek already been applied? Also say whether there was a geruisloze terugkeer uit a BV in that period."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "prior-year aangiften or aanslagen, notes on start date and ondernemersaftrek history"
- question_id: "annual.winst.result.omzet_kosten"
  workflow: "annual_2025"
  section: "winst.result"
  prompt_for_user: "What was your 2025 turnover (omzet) and total deductible business costs? A winst-en-verliesrekening or bookkeeping export is ideal."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "winst-en-verliesrekening, balans, facturen"
- question_id: "annual.winst.vorm.samenwerkingsverband"
  workflow: "annual_2025"
  section: "winst.ondernemingsvorm"
  prompt_for_user: "Do you run the business on your own as an eenmanszaak, or together with others in a vof, maatschap, or cv? Please also say whether you put in only money without running the business, and whether any asset you own privately is used by the business."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "KvK extract, vennootschaps- or maatschapscontract, agreement on assets made available"
- question_id: "annual.winst.investeringsaftrek.investeringen"
  workflow: "annual_2025"
  section: "winst.investeringsaftrek"
  prompt_for_user: "Did the business buy or improve any bedrijfsmiddelen in 2025, and did it sell or transfer an asset on which an investeringsaftrek was claimed earlier? Please list each item with its invoice, date, and amount."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "investment invoices, asset register, RVO verklaring for EIA or MIA"
- question_id: "annual.winst.balans.ondernemingsvermogen"
  workflow: "annual_2025"
  section: "winst.balans"
  prompt_for_user: "What was the ondernemingsvermogen at the start and at the end of the 2025 boekjaar, and what were the priveonttrekkingen and privestortingen? Please give the opening and the closing figure separately."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "finalized balans with both columns, grootboek, private-use records"
- question_id: "annual.winst.verlies.niet_gerealiseerde_zelfstandigenaftrek"
  workflow: "annual_2025"
  section: "winst.verlies"
  prompt_for_user: "Do you carry a niet-gerealiseerde zelfstandigenaftrek balance from an earlier year, and can you show the beschikking that fixed it?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "aanslagbiljet carrying the beschikking, running balance kept from earlier returns"
- question_id: "annual.winst.zvw.loon_zorgverzekeringswet"
  workflow: "annual_2025"
  section: "winst.zvw"
  prompt_for_user: "Did you also have loon, pension, or a benefit in 2025? If so, what is the 'loon Zorgverzekeringswet' shown on each jaaropgaaf?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "2025 jaaropgaaf per employer or benefits agency"
- question_id: "annual.winst.lijfrente.premies"
  workflow: "annual_2025"
  section: "winst.inkomensvoorzieningen"
  prompt_for_user: "Did you pay lijfrente premiums or deposits in 2025, and did you hold an arbeidsongeschiktheidsverzekering? Please give the amounts and the exact payment dates."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "insurer statements with payment dates, bank statements, policy summary"
- question_id: "annual.winst.row.inkomsten_en_kosten"
  workflow: "annual_2025"
  section: "winst.resultaat_overige_werkzaamheden"
  prompt_for_user: "For work you did outside employment and outside a business of your own: what did you invoice or receive in 2025, and what costs did you make for that work?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "invoices or payment statements, cost receipts, purchase invoices for assets used"
- question_id: "provisional.winst.expected_profit"
  workflow: "provisional_2026"
  section: "winst_forecast"
  prompt_for_user: "What is your reviewed best estimate of full-year 2026 profit from the enterprise, and what forecast or current bookkeeping supports it?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "current profit forecast, year-to-date bookkeeping, or user-reviewed estimate"
- question_id: "provisional.winst.zvw.voorlopige_aanslag"
  workflow: "provisional_2026"
  section: "winst_forecast"
  prompt_for_user: "Did you also receive a separate voorlopige aanslag Zorgverzekeringswet for 2026, and which income is it based on? It has its own change route; whether an income-tax change is coupled to it is not established, so check it separately."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "the voorlopige aanslag Zvw 2026 letter or the copy in the taxpayer's own portal"
```

The calling skill asks these questions, records the answers with `source`,
`quote`/`evidence_id`, and timestamp under its own workflow notes tree, then
re-runs this helper contract. The annual workflow owns persistence in annual
mode. The provisional workflow owns persistence in provisional mode. The helper
owns no persisted artifact. Do not write caller-owned notes.

## Never

- Do not claim that the helper gives binding tax advice or a final assessment.
  The aangifte the taxpayer files and the aanslag they receive stay
  authoritative, and the chain in the workpack is what they check against them.
- Do not compute a stakingswinst, a herinvesteringsreserve or
  kostenegalisatiereserve movement, an oudedagsreserve release, or a
  stakingslijfrente. Record the facts and route them to manual review.
- Do not compute a terbeschikkingstellingsresultaat or apply the
  terbeschikkingstellingsvrijstelling.
- Do not apply the medegerechtigde loss cap or decide whether a
  samenwerkingsverband is ongebruikelijk. Both need running records this helper
  does not hold.
- Do not compute a winstaandeel, a KIA apportionment, buitenvennootschappelijk
  vermogen, or any other per-participant figure for a vof, maatschap, or cv.
  Recognising and routing the form is in scope; splitting the profit is not.
- Do not compute DGA/BV winst or a corporate-tax interaction.
- Do not compute a youngtimer bijtelling or a claimed zonnecelauto outcome.
- Do not decide a borderline ondernemer-versus-resultaat-uit-overige-werkzaamheden
  qualification. Put the criteria to the taxpayer, collect their facts against
  each one, state what each outcome costs in reliefs, and route the decision
  itself to manual review.
- Do not treat a btw-ondernemer, a KvK registration, the KOR, the absence of
  loondienst, or a modelovereenkomst as proof of IB-ondernemerschap.
- Do not turn the provisional expected-profit forecast into business accounts,
  annual deductions, a Zvw amount, cessation profit, or final tax.
- Do not return a chain output the aangifte computes as a manual-entry
  field-map row, and never widen the single supported provisional business field.
- Do not write field maps, annual/provisional workpack templates, source
  registers, supported workflow files, or shared eval data.

Return structured facts and open questions to the owning workflow. Do not
persist any final artifact, including shared notes, question packets, session
state, workpacks, or field maps. In either mode, only the calling owning workflow
may read historical helper notes for resume compatibility.

Authenticated-portal boundary: Never use a browser, Claude in Chrome, computer
use, screen interaction, a connector, or another tool to open or operate an
authenticated tax portal; never log in, enter or change values, click controls,
sign, send, submit, retrieve private account data, or ask for, accept, store, or
process credentials or sessions. Those actions remain human-only even with
taxpayer permission or available credentials.
