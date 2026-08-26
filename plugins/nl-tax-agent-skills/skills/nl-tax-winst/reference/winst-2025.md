# Winst uit onderneming - Annual 2025: Computation Contract

source_ids: bd_ondernemer_criteria_2025, bd_urencriterium_2025, bd_ondernemersaftrek_2025, bd_zelfstandigenaftrek_2025, bd_startersaftrek_2025, bd_startersaftrek_ao_2025, bd_so_aftrek_2025, bd_meewerkaftrek_2025, bd_stakingsaftrek_2025, bd_mkb_winstvrijstelling_2025, bd_kia_2025, bd_eia_2025, bd_eia_mia_vamil_2025, bd_zakelijke_kosten_2025, bd_zakelijke_kosten_een_jaar_2025, bd_zakelijke_kosten_meerdere_jaren_2025, bd_beperkt_aftrekbare_kosten_2025, bd_werkruimte_2025, bd_bijtelling_auto_2025, bd_privevervoermiddel_2025, bd_oudedagsreserve_2025, bd_herinvesteringsreserve, bd_box1_rates_2025, bd_arbeidsinkomen_definition_2025, bd_deduction_rate_cap_2025, bd_zvw_inkomensafhankelijke_bijdrage, bd_zvw_resultaat_overig_werk, bd_aftrekken_lijfrentepremies, bd_verlies_uit_onderneming, bd_verrekenen_ngz, bd_bron_van_inkomen, bd_medegerechtigde, bd_u_staakt_uw_onderneming, bd_administratie_bewaren_2025, bd_ola_ih2025_winstberekening, bd_ondernemer_cijfers_aangifte_2025, bd_aangifte_ondernemers_2025
workflow: annual_return
tax_year: 2025
status: active
review_status: reviewed
last_reviewed: "2026-08-15"

## Contents

- Scope
- What this contract determines
- Required inputs before the chain runs
- The ordered chain
- The winst cap and the niet-gerealiseerde zelfstandigenaftrek
- The tariefsaanpassing
- Zvw and lijfrente: two bases read off different lines
- The vermogensvergelijking self-check
- What the taxpayer types and what the aangifte computes
- When the chain produces a loss
- Resultaat uit overige werkzaamheden
- Per-form routing
- Costs, werkruimte, and car
- Evidence
- Question-packet ids
- Manual-review boundaries

## Scope

Use this contract for a standard full-year Dutch resident annual 2025 workpack
for an IB-ondernemer with an eenmanszaak (the usual ZZP legal form). It is a
workflow contract: it says which inputs have to exist, in which order the lines
are combined, which note owns each rule, and where computation stops and manual
review begins.

The reviewed knowledge notes under `_shared/knowledge/years/2025/entrepreneur/`
are canonical for every amount, percentage, and threshold; read them and never
paraphrase a figure from memory. Where this contract and a knowledge note both
mention a rule, the knowledge note wins. Bare file names below refer to that
directory; cross-scope notes are named with their full path.

Outputs are preparation artifacts the taxpayer reviews themselves. They are not
a filed return, not an assessment, and not final tax advice. This contract
covers tax year 2025 only; never carry a line, a rate, or an amount from it into
another tax year.

## What this contract determines

The helper determines the **belastbare winst uit onderneming** for 2025 and
returns it, with every line of its derivation and the evidence under each line,
to `nl-tax-annual-return`. That amount is the winst component of the box 1
income; the annual workflow owns the box 1 total and every artifact.

Two further outputs travel with it, each labelled with the line it is read off:
the **Zvw bijdrage-inkomen** and the winst component of the **lijfrente
premiegrondslag**. `winstberekening-2025.md` is canonical for the order of the
chain and for which line each of those bases comes from.

## Required inputs before the chain runs

Collect each input below as a fact with its provenance. Every one of them is a
question to the taxpayer, never an assumption, and never a zero the helper
supplies. The zakelijk deel of the aangifte is never prefilled, so an empty box
carries no information.

1. **Ondernemer status.** Confirmed ondernemerschap voor de inkomstenbelasting
   (`ondernemer-criteria.md`), and the answer to the urencriterium question, plus
   the verlaagd urencriterium where the startersaftrek bij arbeidsongeschiktheid
   is in play.
2. **A finalized profit-and-loss statement for 2025**, identified as final or
   reviewed, with the underlying omzet and kosten per rubriek
   (`zakelijke-schema-2025.md`).
3. **A finalized balance for 2025 with both columns**, begin boekjaar and einde
   boekjaar, asked separately. Never carry a prior year's closing figure into
   the opening column and never enter zero for a column the taxpayer has not
   supplied.
4. **The beperkt aftrekbare kosten** and which of the two available treatments
   the finalized accounts applied (`winst-en-kosten.md`). One treatment or the
   other, never both.
5. **Privegebruik onttrekkingen** for a car, a woning, or a fiets held in the
   onderneming (`vervoer-2025.md`, `afschrijving-en-bedrijfsmiddelen-2025.md`).
6. **Investments and disposals**: the qualifying investments in 2025 and any
   disposal of an asset on which an investeringsaftrek was claimed earlier
   (`investeringsaftrek.md`).
7. **The ondernemersaftrek eligibility answers**: starter history, S&O-verklaring
   from RVO, hours worked by a meewerkende fiscale partner and whether that
   partner was paid (`ondernemersaftrek.md`, `partner-en-meewerken-2025.md`,
   `aanloopfase-en-starters-2025.md`).
8. **Any niet-gerealiseerde zelfstandigenaftrek** from earlier years, with the
   beschikking that fixed it (`verlies-en-verrekening-2025.md`).
9. **The vermogensvergelijking inputs**: opening and closing ondernemingsvermogen,
   priveonttrekkingen en -stortingen, wijzigingen toelaatbare reserves, niet- of
   gedeeltelijk aftrekbare kosten en lasten, and vrijgestelde winstbestanddelen.
10. **Other box 1 income** -- loon, pensioen, or an uitkering -- which the loss
    set-off and the tariefsaanpassing threshold both need, together with the
    "loon Zorgverzekeringswet" shown on each jaaropgaaf (`zvw-2025.md`).
11. **Lijfrente premiums and deposits paid in 2025 with their payment dates**, and
    whether the taxpayer holds an AOV (`inkomensvoorzieningen-2025.md`).

When a required input is missing, ask for it, record it as an open question with
the evidence that would settle it, and leave that line unresolved. Do not
continue the chain past a missing input with a placeholder, a prior-year figure,
or an estimate.

## The ordered chain

Run the lines in the order `winstberekening-2025.md` publishes. Print each line
with its amount, the note the rule came from, and the evidence under it, so the
arithmetic stays traceable for the taxpayer and for a later reviewer.

| Line | Step | Note that owns the rule |
|------|------|-------------------------|
| A | Omzet minus zakelijke kosten under goed koopmansgebruik, after the fiscal corrections = winst uit onderneming | `winst-en-kosten.md`; `afschrijving-en-bedrijfsmiddelen-2025.md` for depreciation, asset labelling and the small-purchase boundary; `vervoer-2025.md` for vehicles; `aanloopfase-en-starters-2025.md` for pre-start costs and a first partial year; `partner-en-meewerken-2025.md` for an arbeidsbeloning to the fiscal partner; `zakelijke-schema-2025.md` for the rubrieken it is built from |
| B | A minus the investeringsaftrek (KIA, EIA, MIA), plus any desinvesteringsbijtelling | `investeringsaftrek.md` |
| C | B minus the ondernemersaftrek | `ondernemersaftrek.md` |
| D | C minus the MKB-winstvrijstelling | `mkb-winstvrijstelling.md` |
| E | The result at line D, being the belastbare winst uit onderneming and a component of box 1 | `winstberekening-2025.md`, with `_shared/knowledge/years/2025/annual/box1-rates.md` for the bracket structure |
| F | The tariefsaanpassing on the grondslagverminderende posten, charged as a belastingvermeerdering | `winstberekening-2025.md`, with `_shared/knowledge/years/2025/annual/deductions.md` |

Two order rules must never be relaxed: the investeringsaftrek is subtracted
**before** the ondernemersaftrek, and the MKB-winstvrijstelling base is the
amount **after both** of them. Taking the exemption off an earlier line
overstates it.

The MKB-winstvrijstelling needs no urencriterium, applies automatically, cannot
be waived, and cannot be allocated between fiscal partners.

## The winst cap and the niet-gerealiseerde zelfstandigenaftrek

- The ondernemersaftrek cannot exceed the winst before ondernemersaftrek, that is
  line B. Apply that cap at line C.
- Check the **startersaftrek exception before applying the cap**: where the
  taxpayer is entitled to the startersaftrek the cap does not apply, line C can
  go negative, and the chain can produce a loss.
- The part the cap blocks becomes **niet-gerealiseerde zelfstandigenaftrek**. The
  Belastingdienst fixes it by beschikking on the aanslagbiljet and does not set
  it off automatically. Report the amount, say that the taxpayer keeps the
  running balance and enters it in a later aangifte, and name the beschikking as
  the evidence. `ondernemersaftrek.md` owns the amounts and conditions;
  `verlies-en-verrekening-2025.md` owns the carry-forward window and the set-off
  condition.
- A claimed balance the taxpayer cannot evidence with the beschikking is a
  manual-review item, not an input.
- Do not confuse this cap with the others: it bites on the zelfstandigenaftrek,
  while the startersaftrek bij arbeidsongeschiktheid and the stakingsaftrek carry
  caps of their own, described in `ondernemersaftrek.md`.

## The tariefsaanpassing

State the tariefsaanpassing qualitatively whenever the income threshold is in
play, reading the threshold, the adjustment percentage and the resulting maximum
rate from `winstberekening-2025.md` and
`_shared/knowledge/years/2025/annual/deductions.md`.

- It is charged as a belastingvermeerdering on the aanslag; it does not reduce
  the deduction itself, and lines C, D and E are unchanged by it.
- Ordinary business costs are not affected, and neither is the
  investeringsaftrek. Only the grondslagverminderende posten on the official list
  are reduced, so say that explicitly rather than leaving the scope open.
- The aangifte computes the correction itself. Present the inputs and the
  mechanism; never present a self-computed correction as the amount that will be
  assessed.

## Zvw and lijfrente: two bases read off different lines

This is the most error-prone part of the annual entrepreneur workpack. The two
bases sit on **different lines of the same chain**, so state both explicitly and
re-read the chain note before emitting either.

- **Zvw bijdrage-inkomen** is the belastbare winst uit onderneming: the **end of
  the chain**, after the ondernemersaftrek and after the MKB-winstvrijstelling.
  `zvw-2025.md` is canonical for the percentage, the maximumbijdrage-inkomen,
  the shared ceiling and every exception.
- **The winst component of the lijfrente premiegrondslag** is the winst **before
  the ondernemersaftrek**, and therefore also before the MKB-winstvrijstelling.
  `inkomensvoorzieningen-2025.md` is canonical for the ruimte, the franchise, the
  caps, the timing rules, and for **which year's figures** the premiegrondslag is
  measured over. The chain note fixes the line; that note fixes the year.
- Because the lijfrente base sits earlier in the chain, it is the larger figure
  whenever the ondernemersaftrek or the MKB-winstvrijstelling is positive. That
  difference is deliberate. Never reuse one amount for the other, and label each
  with its line in the workpack.
- The arbeidsinkomen used for the arbeidskorting takes the same line as the
  lijfrente base, not the belastbare winst.
  `_shared/knowledge/years/2025/annual/credits.md` is canonical for it.

An ondernemer receives a **second, separate aanslag for the bijdrage Zvw**
alongside the aanslag inkomstenbelasting, and one return feeds both. Carry that
in the workpack as a plain statement of a second payment obligation:

- Ask whether the taxpayer also had loon, pensioen or an uitkering in 2025 and,
  for each, ask for the "loon Zorgverzekeringswet" on the jaaropgaaf. The ceiling
  is shared across income sources; never assume there was no loon.
- The bijdrage is **never a business cost** and is not deductible anywhere. If
  the bookkeeping already deducted it, flag the correction and route it to manual
  review.
- There is no Zvw entry screen and no Zvw form, so never create a field-map row
  asking the taxpayer to type a bijdrage amount.
- Present the method. Do not predict what the aanslag Zvw will say.

AOV premiums are likewise never a business cost; they belong to the uitgaven voor
inkomensvoorzieningen and are handled outside this chain.

## The vermogensvergelijking self-check

The aangifte's Winstberekening screen reproduces the profit from the movement in
the enterprise's capital and requires the two to agree. For an eenmanszaak the
comparison figure is the saldo winst-en-verliesrekening.
`zakelijke-schema-2025.md` is canonical for the screen and its inputs.

- Carry the reconciliation as an explicit workpack line, as a check on the
  figures and not as a second way to compute the profit.
- Ask for the opening and the closing ondernemingsvermogen separately.
- Where it does not come out, report the mismatch and the components it rests
  on, and route it to manual review. Never adjust the saldo or a balance figure
  to force agreement.
- Do not impose an activa-equals-passiva rule, do not encode a tolerance, and do
  not invent the signed formula the screen uses. Take the sign convention from
  the form's own invulhulp on screen.
- Print each double-entry fact twice in the manual-entry material, once per
  screen path, from a single value in the workpack. The onttrekking for private
  use of a car, a woning or a fiets appears both in the buitengewone baten and in
  the priveonttrekkingen, and the auto bijtelling does not belong under auto- en
  transportkosten.

## What the taxpayer types and what the aangifte computes

This division is load-bearing for the field map.

- **The taxpayer types** the winst-en-verliesrekening rubrieken, both balans
  columns, the priveonttrekkingen en -stortingen, and the answers to the
  eligibility questions. `zakelijke-schema-2025.md` is canonical for those
  `onderneming.*` identifiers, and every one of them is conditional or optional
  in a field map, never required.
- **The aangifte computes** the zelfstandigenaftrek, the startersaftrek, the
  aftrek voor speur- en ontwikkelingswerk, the meewerkaftrek, the stakingsaftrek,
  the total ondernemersaftrek, the kleinschaligheidsinvesteringsaftrek, the
  MKB-winstvrijstelling, the saldo fiscale winstberekening, and the belastbare
  winst -- from the figures and the answers the taxpayer entered.
- Therefore **never emit these as manual-entry rows**:
  `onderneming.belastbare_winst`, `onderneming.zelfstandigenaftrek`,
  `onderneming.startersaftrek`, `onderneming.ondernemersaftrek_totaal`,
  `onderneming.mkb_winstvrijstelling`,
  `onderneming.kleinschaligheidsinvesteringsaftrek`. They are outputs of the
  form, not boxes anyone types into.
- The computed chain belongs in the **workpack narrative**, printed line by line,
  so the taxpayer can check what the portal produces against their own figures.
  If a calculated line appears in a field map at all, it is a review row with its
  inputs named, never an instruction to enter a number.
- Present the zakelijk deel as a **checklist of rubrieken and questions**. The
  screen order is not published; never number the sections as portal steps and
  never claim one section comes before another beyond the data dependencies in
  `zakelijke-schema-2025.md`.

## When the chain produces a loss

- Confirm first that the loss survives the MKB-winstvrijstelling: the exemption
  is applied to a negative amount as well, so the loss at the end of the chain is
  **smaller** than the loss before it. Say plainly that this is a disadvantage
  rather than presenting the exemption as a benefit.
- An ondernemingsverlies is first set off within the same year against positive
  box 1 income such as loon. Only what remains becomes a verlies uit werk en
  woning.
- `verlies-en-verrekening-2025.md` is canonical for the carry-back and
  carry-forward windows, the verliesbeschikking, the voorlopige verliesverrekening
  and its cap, verdamping, and the niet-gerealiseerde zelfstandigenaftrek. Do not
  restate a window or a percentage here.
- A loss year still requires a filed return. Never treat a loss as a reason to
  skip the aangifte.

## Resultaat uit overige werkzaamheden

Resultaat uit overige werkzaamheden is a **prepared path, not a dead end**.
`row-en-dba-2025.md` is canonical for it.

- **Run the bron van inkomen pre-screen first**, before any category question and
  before any figure is collected, and run it per activity. Record the taxpayer's
  answers and present the outcome as theirs to confirm; never assert the verdict.
  Where the answers point away from a bron van inkomen, state both consequences
  -- the income is not taxed and the costs are not deductible -- and route it to
  manual review.
- Test the categories in order: loon, then winst uit onderneming, then resultaat
  uit overige werkzaamheden as the residual.
- **When the outcome is resultaat uit overige werkzaamheden, prepare it.** The
  resultaat is income minus deductible costs on the winstbepalingsregels, with
  goed koopmansgebruik as the timing framework. Apply `winst-en-kosten.md` for
  the cost rules and `afschrijving-en-bedrijfsmiddelen-2025.md` for depreciation
  and vermogensetikettering.
- **What falls away** is every relief reserved for an ondernemer: the
  ondernemersaftrek, the MKB-winstvrijstelling, the investeringsaftrek, and the
  fiscale reserves. Quantify that difference from the taxpayer's own figures and
  show the two outcomes side by side. Never quote a single euro figure as "what
  it costs" and never present a published example as the taxpayer's own result.
- The urencriterium is irrelevant to this category. Do not ask for an hours count
  in order to settle it, and do not let a failed urencriterium be mistaken for
  the reason the reliefs are missing -- the reason is the category.
- The resultaat is reported in the **privedeel** of the aangifte under inkomsten
  uit overig werk. There is no winst-en-verliesrekening and no balans, so
  `zakelijke-schema-2025.md` does not apply. The field mapper's row is
  `box1.resultaat_overige_werkzaamheden`; do not print a portal click path.
- A **bijdrage Zvw** applies to the resultaat just as it does to winst uit
  onderneming, and two separate assessments follow the one return. `zvw-2025.md`
  is canonical; ask for the "loon Zorgverzekeringswet" on each jaaropgaaf.
- The income is **not divisible between fiscal partners**. Do not offer an
  allocation scenario for it.
- The **belastbaar resultaat uit overige werkzaamheden is a named component of
  the lijfrente premiegrondslag** (art. 3.127 lid 3 Wet IB 2001), alongside the
  winst, the belastbaar loon, and the belastbare periodieke uitkeringen en
  verstrekkingen. Like the winst component it is taken from the **preceding
  calendar year**. `inkomensvoorzieningen-2025.md` is canonical; ask for the
  component separately and never assume it is zero.
- Terbeschikkingstelling van bezittingen and the special categories -- gastouder,
  artiest, beroepssporter, kostgangers, pgb-zorg, huishoudelijke werkzaamheden,
  and vermogensbeheer that goes beyond normal management -- each carry rules this
  contract does not hold. Record the facts and route them to manual review.
- Wet DBA and schijnzelfstandigheid are explanation only. Never rule on an
  arbeidsrelatie, and never treat a modelovereenkomst as proof of
  IB-ondernemerschap.

## Per-form routing

Every IB business form is **recognised and routed**. Recognition, the
per-participant ondernemer tests, the fact and evidence set, and saying which
reliefs apply or fall away are in scope. Computing a share, a reserve, or a
special regime is not. `samenwerkingsverband-2025.md` is canonical; place the
taxpayer in exactly one row per income stream, and note that one taxpayer can
occupy more than one row.

| Form | Position | Prepared under this contract | Routed to manual review |
|------|----------|------------------------------|-------------------------|
| Eenmanszaak | ondernemer | the full chain, lines A to F | -- |
| Vof vennoot, maatschap maat, cv beherend vennoot | ondernemer where the statutory tests are met, tested per participant | recognition, the per-participant ondernemer tests, the facts and evidence, which reliefs apply, and the fact that each participant files their own aangifte | the winstverdeling, the winstaandeel, the KIA apportionment, buitenvennootschappelijk vermogen, and every per-participant figure |
| Cv stille vennoot, profit-sharing geldverstrekker | medegerechtigde, not ondernemer | recognition, and stating that no ondernemersaftrek and no MKB-winstvrijstelling apply | the whole computation, including the loss cap, which needs a running capital record the taxpayer must produce |
| Pand or lening made available to a connected person's onderneming | resultaatgenieter under the terbeschikkingstellingsregeling | recognition and fact collection only | the resultaat, its own profit-determination regime, the vrijstelling, and the exit |
| Agrarische onderneming | ondernemer with a regime of its own | recognition and fact collection | the landbouwvrijstelling and every agrarian-specific treatment |
| Zeescheepvaart and zeevarenden | ondernemer or crew with a regime of its own | recognition and fact collection | the tonnage regime and the Zvw treatment of a zeevarende |
| DGA with a BV | not an IB-ondernemer for that income | recognition only | the whole corporate-tax interaction |

Further routing rules that go with the table:

- Being a participant is not the same as being an ondernemer. Test each
  participant individually against `ondernemer-criteria.md`; never infer
  ondernemerschap from a KvK registration.
- Whether a samenwerkingsverband is **ongebruikelijk** is never decided here.
  Record the facts and route the decision.
- For the btw a vof, maatschap or cv is itself the ondernemer while the
  participants are not. Btw is outside the workpack; mention it only to prevent
  the taxpayer from reading their btw position as their IB position.
- Entering, leaving, or dissolving a samenwerkingsverband, and a change of legal
  form, are staking-adjacent events. Route them with `staking-2025.md`.

## Costs, werkruimte, and car

- Record the treatment selected in the finalized accounts for
  beperkt-aftrekbare costs and ask a review question if it is unclear. One
  treatment or the other applies, never both.
- For purchases and prepaid costs, do not infer one-year deduction or
  depreciation from price alone. Ask the two separate facts: the cost basis
  (including the correct VAT treatment) and whether the item or cost benefits
  only 2025 or more than one year. Apply the small-purchase boundary and the
  multi-year treatment from `afschrijving-en-bedrijfsmiddelen-2025.md` and
  `winst-en-kosten.md` rather than from a remembered amount.
- Werkruimte in a private-asset home, the private-use-of-a-business-car
  bijtelling, and the private-vehicle kilometre deduction are prepared from the
  knowledge notes (`winst-en-kosten.md`, `vervoer-2025.md`); flag anything
  ambiguous for manual review.
- For a company car, record whether the taxpayer can substantiate **500 private kilometres or fewer**. Confirm the date of first admission, vehicle regime,
  emissions/fuel facts, catalogue value, and private-use evidence before
  showing a rate. When these are not known, withhold the rate and keep the
  bijtelling as manual review.
- A claimed youngtimer or a claimed zonnecelauto is manual review in every case.
  Collect the date of first use, the substantiated value, and the private-use
  evidence, and hand the computation to the taxpayer or their adviser.

## Evidence

- Ask for the finalized profit-and-loss statement, the finalized balance with
  both columns, invoices, the bank jaaroverzicht, investment invoices, and the
  urenadministratie as gaps when missing (see `entrepreneur-aangifte.md`). Never
  assume zeros and never collect the BSN.
- For a material depreciation line, also ask for the asset invoice, in-use date,
  expected useful life, residual value, and opening book value or schedule.
  Preserve unresolved accounting treatment as a review question.
- For the ondernemersaftrek, ask for the urenadministratie, the starter history,
  the RVO S&O-verklaring, and the partner's hours record.
- For the Zvw ceiling, ask for each 2025 jaaropgaaf and the "loon
  Zorgverzekeringswet" printed on it.
- For a niet-gerealiseerde zelfstandigenaftrek or a verliesbeschikking, ask for
  the aanslagbiljet that carries the beschikking.
- Collect only what the chain needs. Do not record a BSN, an aanslagnummer, a
  policy number, or a bank account number from any document.

## Question-packet ids

Raise missing inputs to the owning workflow as question-packet entries, using the
shape in `SKILL.md`. The id inventory for annual mode:

| question_id | What it settles |
|-------------|-----------------|
| `annual.winst.ondernemer.status` | Ondernemerschap voor de inkomstenbelasting and the urencriterium answer |
| `annual.winst.vorm.samenwerkingsverband` | Which business form applies, and whether privately owned assets are used by the business |
| `annual.winst.result.omzet_kosten` | Omzet and deductible costs from the finalized winst-en-verliesrekening |
| `annual.winst.kosten.beperkt_aftrekbaar` | Which treatment the accounts applied to the beperkt aftrekbare kosten |
| `annual.winst.prive.onttrekkingen` | Privegebruik of a car, woning, or fiets, and the priveonttrekkingen en -stortingen |
| `annual.winst.investeringsaftrek.investeringen` | Qualifying investments in 2025 and any disposal of a previously claimed asset |
| `annual.winst.ondernemersaftrek.startersaftrek` | Starter history for the regular startersaftrek |
| `annual.winst.ondernemersaftrek.so_verklaring` | An RVO S&O-verklaring and the recognised research hours |
| `annual.winst.ondernemersaftrek.meewerkende_partner` | Partner hours in the onderneming and whether the partner was paid |
| `annual.winst.balans.ondernemingsvermogen` | Opening and closing ondernemingsvermogen and the vermogensvergelijking inputs |
| `annual.winst.verlies.niet_gerealiseerde_zelfstandigenaftrek` | An earlier-year balance and the beschikking that fixed it |
| `annual.winst.zvw.loon_zorgverzekeringswet` | Other income and the loon Zorgverzekeringswet on each jaaropgaaf |
| `annual.winst.lijfrente.premies` | Lijfrente premiums and deposits with their payment dates, and any AOV |
| `annual.winst.row.inkomsten_en_kosten` | Income and costs for work outside employment and outside an onderneming |

Keep the ids stable: the owning workflow records answers against them and
re-runs this contract.

## Manual-review boundaries

Record the facts collected so far and route the case out of the chain, without
computing, when any of these is present:

- Staking or cessation of the whole or part of an onderneming, doorschuiving, a
  stakingslijfrente, a herinvesteringsreserve, a kostenegalisatiereserve
  movement, or an oudedagsreserve movement (`staking-2025.md`,
  `afschrijving-en-bedrijfsmiddelen-2025.md`, `inkomensvoorzieningen-2025.md`).
- Terbeschikkingstelling van bezittingen, including the vrijstelling and the
  exit.
- The medegerechtigde loss cap, and whether a samenwerkingsverband is
  ongebruikelijk.
- Any winstaandeel, KIA apportionment, or other per-participant figure in a vof,
  maatschap, or cv, and any buitenvennootschappelijk vermogen.
- DGA or BV winst and any corporate-tax interaction.
- An agrarische onderneming or a zeevarende position.
- A claimed youngtimer or zonnecelauto bijtelling.
- Willekeurige afschrijving.
- Emigration, immigration, treaty, nonresident, or partial-year resident issues.
- A borderline ondernemer-versus-resultaat-uit-overige-werkzaamheden
  qualification: surface the criteria, collect the taxpayer's facts against each,
  state what each outcome costs, and route the decision itself.
- A niet-gerealiseerde zelfstandigenaftrek or other carry-forward the taxpayer
  cannot evidence, and any component amount they cannot evidence at all.

Preparation only. **You (the taxpayer) or an authorized human** open Mijn
Belastingdienst, type every value, review it, sign, and send. This plugin never
opens or operates the portal.
