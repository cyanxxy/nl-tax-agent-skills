# Knowledge index

Topic map for the reviewed Dutch income-tax notes bundled with this plugin. Use
it to pick the one or two notes that answer a rule question, then open only
those notes. Every note carries its own `source_ids`, `workflow`, `tax_year`,
and `review_status` header; the note, not this index, is canonical for every
amount, percentage, threshold, and date.

## How to use this index

- Every path below is written relative to the active skill directory (the
  folder that holds the active `SKILL.md`). All skills are siblings, so the same
  `../nl-tax-shared-resources/...` path works from any skill in this plugin.
- Match the question's **year and workflow first**. Annual 2025 notes answer the
  2025 return (aangifte inkomstenbelasting 2025). Provisional 2026 notes answer
  the voorlopige aanslag 2026. Never answer a 2026 question from a 2025 note or
  the reverse; say which year a figure belongs to.
- Then match the **topic** using the key terms column. The terms are the Dutch
  and English words a taxpayer is likely to use.
- If no row fits, a narrow text search for the Dutch term inside
  `../nl-tax-shared-resources/knowledge/` is allowed. Do not search the rest of
  the plugin.
- To cite a source, read the selected note's `source_ids` and look up only those
  entries in `../nl-tax-shared-resources/source-register.yaml`.
- Years other than 2025 (annual) and 2026 (provisional) are not covered. Say so
  instead of answering from model memory.
- Sections headed "Developer instruction" or "Common failure" inside a note are
  guidance for the agent. Apply them; do not quote them to the taxpayer as tax
  rules.

## Annual return 2025 (aangifte inkomstenbelasting 2025)

| Topic | Key terms | Note |
|---|---|---|
| Box 1 rates and brackets | box 1, tax brackets, schijven, AOW age, company car, stock options | `../nl-tax-shared-resources/knowledge/years/2025/annual/box1-rates.md` |
| Tax credits | heffingskortingen, algemene heffingskorting, arbeidskorting, inkomensafhankelijke combinatiekorting, ouderenkorting | `../nl-tax-shared-resources/knowledge/years/2025/annual/credits.md` |
| Personal deductions | persoonsgebonden aftrek, zorgkosten, giften, alimentatie, studiekosten, lijfrentepremie, AOV, verdeling aftrekposten | `../nl-tax-shared-resources/knowledge/years/2025/annual/deductions.md` |
| Own home 2025 | eigen woning, eigenwoningforfait, hypotheekrenteaftrek, tariefsaanpassing, Hillenregeling, moving | `../nl-tax-shared-resources/knowledge/years/2025/annual/own-home.md` |
| Evidence to collect | jaaropgaaf, evidence, checklist | `../nl-tax-shared-resources/knowledge/years/2025/annual/evidence-checklist.md` |
| Filing steps and deadline | filing process, filing deadline, four-step | `../nl-tax-shared-resources/knowledge/years/2025/annual/filing-flow.md` |
| Late filing | penalty, verzuimboete, deadline, aanmaning, belastingrente | `../nl-tax-shared-resources/knowledge/years/2025/annual/late-filing.md` |
| Box 2 income | substantial interest, dividend, regular benefits, disposal benefits | `../nl-tax-shared-resources/knowledge/years/2025/box2/box2-income-guidance.md` |
| Box 2 rates (2025 and 2026) | box 2 rates, aanmerkelijk belang, fiscal partners | `../nl-tax-shared-resources/knowledge/years/2025/box2/box2-rates.md` |
| Box 2 threshold and excessive borrowing 2025 | substantial interest threshold, excessive borrowing, BV | `../nl-tax-shared-resources/knowledge/years/2025/box2/fisin-aanmerkelijk-belang.md` |
| Box 3 fictitious return | forfaitair rendement, heffingsvrij vermogen, peildatum, banktegoeden, overige bezittingen, schulden, drempel schulden | `../nl-tax-shared-resources/knowledge/years/2025/box3/fictitious.md` |
| Box 3 actual return | werkelijk rendement, actual return, rente, dividend, huur, costs | `../nl-tax-shared-resources/knowledge/years/2025/box3/actual-return.md` |
| Box 3 worked examples | worked example, savings only, mixed portfolio, fiscal partners | `../nl-tax-shared-resources/knowledge/years/2025/box3/examples.md` |

### Entrepreneurs 2025 (winst uit onderneming, zzp)

| Topic | Key terms | Note |
|---|---|---|
| Am I an ondernemer? | ondernemerschap, urencriterium, bron van inkomen | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/ondernemer-criteria.md` |
| Business income versus other work, DBA | resultaat uit overige werkzaamheden, freelance, Wet DBA, schijnzelfstandigheid, opdrachtgevers | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/row-en-dba-2025.md` |
| Profit calculation order | winstberekening, belastbare winst, chain, arbeidsinkomen | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/winstberekening-2025.md` |
| Business costs and records | deducting costs, non-deductible, werkruimte, administratie, bewaarplicht | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/winst-en-kosten.md` |
| Entrepreneur deductions | ondernemersaftrek, zelfstandigenaftrek, startersaftrek, meewerkaftrek, S&O-aftrek, stakingsaftrek | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/ondernemersaftrek.md` |
| MKB profit exemption | MKB-winstvrijstelling | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/mkb-winstvrijstelling.md` |
| Investment deduction | investeringsaftrek, KIA, EIA, MIA, Vamil, desinvesteringsbijtelling | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/investeringsaftrek.md` |
| Depreciation and assets | afschrijving, bedrijfsmiddelen, restwaarde, vermogensetikettering, willekeurige afschrijving | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/afschrijving-en-bedrijfsmiddelen-2025.md` |
| Starting a business | startersaftrek, aanloopkosten, aanloopfase, first partial year | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/aanloopfase-en-starters-2025.md` |
| Cars and transport | bijtelling, rittenregistratie, bestelauto, fiets van de zaak, private vehicle, openbaar vervoer | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/vervoer-2025.md` |
| Pension and disability provisions | jaarruimte, reserveringsruimte, lijfrente, AOV, oudedagsreserve | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/inkomensvoorzieningen-2025.md` |
| Working partner | meewerkende partner, arbeidsbeloning, medeondernemer | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/partner-en-meewerken-2025.md` |
| Partnerships and special forms | vof, maatschap, cv, samenwerkingsverband, medegerechtigde, agrarisch, zeescheepvaart, terbeschikkingstelling | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/samenwerkingsverband-2025.md` |
| Stopping the business | staking, stakingswinst, doorschuiven, stakingslijfrente | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/staking-2025.md` |
| Losses | verlies, verliesverrekening, carry-back, carry-forward, verliesbeschikking, NGZ | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/verlies-en-verrekening-2025.md` |
| Health-insurance contribution | bijdrage Zvw, Zorgverzekeringswet, bijdrage-inkomen | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/zvw-2025.md` |
| Business part of the return | winst-en-verliesrekening, balans, priveonttrekkingen, vermogensvergelijking | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/zakelijke-schema-2025.md` |
| Entrepreneur filing and evidence | winstaangifte, evidence, deadlines | `../nl-tax-shared-resources/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md` |

## Voorlopige aanslag 2026 (provisional assessment)

Box 3 in the voorlopige aanslag 2026 uses the fictitious method only. Never
collect or calculate werkelijk rendement for 2026 here; it may become relevant
when filing the annual 2026 return in 2027.

| Topic | Key terms | Note |
|---|---|---|
| Rates and credits 2026 | box 1 rates 2026, box 3 rates 2026, heffingskortingen, arbeidskorting | `../nl-tax-shared-resources/knowledge/years/2026/provisional/rates-and-credits.md` |
| Own home 2026 | eigenwoningforfait, WOZ, mortgage interest, tariefsaanpassing | `../nl-tax-shared-resources/knowledge/years/2026/provisional/own-home.md` |
| Box 2 in 2026 | box 2, aanmerkelijk, excessive borrowing | `../nl-tax-shared-resources/knowledge/years/2026/provisional/box2.md` |
| Box 2 threshold and excessive borrowing 2026 | substantial interest threshold, excessive borrowing | `../nl-tax-shared-resources/knowledge/years/2026/provisional/fisin-aanmerkelijk-belang.md` |
| Box 3 in 2026 | heffingsvrij vermogen, forfaitair rendement, peildatum, fictitious return | `../nl-tax-shared-resources/knowledge/years/2026/provisional/box3-provisional.md` |
| Expected business profit 2026 | winst uit onderneming, geschatte_winst, forecast, rollover, belastingrente | `../nl-tax-shared-resources/knowledge/years/2026/provisional/winst-provisional-2026.md` |
| Zvw contribution 2026 | bijdrage Zvw, voorlopige aanslag Zorgverzekeringswet | `../nl-tax-shared-resources/knowledge/years/2026/provisional/zvw-provisional-2026.md` |
| How to request one | request, voorlopige aanslag, monthly | `../nl-tax-provisional-assessment/reference/source-projections/request-flow-human.md` |
| How to change one | change, wijzigen, complete dataset | `../nl-tax-provisional-assessment/reference/source-projections/change-flow-human.md` |
| How to stop one | stopzetten, stop, refund | `../nl-tax-provisional-assessment/reference/source-projections/stopzetten-flow-human.md` |
| When to review one | check, too high, too low, review | `../nl-tax-shared-resources/knowledge/years/2026/provisional/review-flow.md` |
| Refund payment timing | teruggaaf, refund, monthly, payment | `../nl-tax-shared-resources/knowledge/years/2026/provisional/refund-payment-timing.md` |
| Prefilled estimate and baseline | VVA, EVA, algorithm register, weegmodule | `../nl-tax-shared-resources/knowledge/years/2026/provisional/vva-eva-baseline-delta.md` |

For request, change, and stopzetten procedures, open the human-subject runtime
projection listed above, not the raw `request-flow.md`, `change-flow.md`, or
`stopzetten-flow.md` notes. The raw notes are maintainer provenance.

## Topics that span both years

| Topic | Key terms | Note |
|---|---|---|
| Fiscal partnership | fiscal partner, married, cohabitation, allocation, separation, death | `../nl-tax-shared-resources/knowledge/partners/fiscal-partnership.md` |
| Eigenwoningforfait tables 2025 and 2026 | eigenwoningforfait, WOZ-waarde | `../nl-tax-shared-resources/knowledge/own-home/eigenwoningforfait.md` |
| Mortgage interest and own-home costs | hypotheekrenteaftrek, mortgage interest, bijleenregeling, temporarily two homes | `../nl-tax-shared-resources/knowledge/own-home/hypotheekrenteaftrek.md` |
| State-pension age | AOW-leeftijd, AOW age, pension | `../nl-tax-shared-resources/knowledge/aow/aow-leeftijd.md` |
| Authorization and representation | machtigen, authorization, representation | `../nl-tax-shared-resources/knowledge/security/machtigen.md` |

## Legal basis (structural orientation only)

These notes name the statute and article behind a rule. Take every amount from
the year notes above, never from a law note.

| Topic | Key terms | Note |
|---|---|---|
| Income Tax Act 2001 | Wet IB 2001, three-box system, article inventory | `../nl-tax-shared-resources/knowledge/laws/wet-inkomstenbelasting-2001.md` |
| Implementing decree | Uitvoeringsbesluit inkomstenbelasting 2001 | `../nl-tax-shared-resources/knowledge/laws/uitvoeringsbesluit-inkomstenbelasting-2001.md` |
| Implementing regulation | Uitvoeringsregeling inkomstenbelasting 2001 | `../nl-tax-shared-resources/knowledge/laws/uitvoeringsregeling-inkomstenbelasting-2001.md` |
| Accelerated depreciation regulation | Uitvoeringsregeling willekeurige afschrijving 2001 | `../nl-tax-shared-resources/knowledge/laws/uitvoeringsregeling-willekeurige-afschrijving-2001.md` |
| Obligation to file | AWR, article 52 | `../nl-tax-shared-resources/knowledge/laws/algemene-wet-inzake-rijksbelastingen.md` |

## Not tax rules

`../nl-tax-shared-resources/knowledge/methods/interactive-elicitation.md` is the
conversation and state contract for workpack preparation. It never answers a
tax-rule question.
