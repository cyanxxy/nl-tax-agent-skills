# Knowledge index

Topic map for the Dutch income-tax and VAT notes bundled with this plugin. Use
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
  the voorlopige aanslag 2026. The annual 2026 note (`years/2026/annual/`)
  answers the 2026 annual return (aangifte inkomstenbelasting 2026, based on
  actual figures). Never answer a 2026 question from a 2025 note or the
  reverse, and never answer an annual 2026 question from a provisional 2026
  note or the reverse. Clarify annual versus provisional only for an ambiguous
  2026 income-tax question whose answer depends on that distinction; clear VAT,
  ICP and OSS questions need no income-tax screening. Say which year a figure
  belongs to.
- Then match the **topic** using the key terms column. The terms are the Dutch
  and English words a taxpayer is likely to use.
- If no row fits, a narrow text search for the Dutch term inside
  `../nl-tax-shared-resources/knowledge/` is allowed. Do not search the rest of
  the plugin.
- To cite a source, read the selected note's `source_ids` and look up only those
  entries in `../nl-tax-shared-resources/source-register.yaml`.
- Covered: the reviewed notes for the annual return 2025 and the voorlopige
  aanslag 2026, and the draft notes (review status `needs_review`) for VAT
  returns and corrections, VAT adjustments, ICP, OSS/IOSS, the international
  M and C returns (2025, with 2026 precollection) and the resident annual
  return 2026. Tax years, taxes and scopes not listed in a section below are
  not covered. Say so instead of answering from model memory.
- A draft note supports a rule answer or draft preparation only. Disclose its
  `needs_review` status, link the official source, and never present it as a
  reviewed filing position or as ready for filing.
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

## VAT returns and corrections 2025/2026 (draft preparation)

These source summaries were researched on 2 October 2026 and await human
tax-content review. They support draft preparation only, with no
`review_ready` label or checklist containing entry amounts. State that review
status when answering a VAT rule question and link the official source.

| Topic | Key terms | Note |
|---|---|---|
| VAT return and rubrics | btw-aangifte, btw, VAT, omzetbelasting, period, deadline, reverse charge, rounding, machtigen, eHerkenning, ketenmachtiging | `../nl-tax-shared-resources/knowledge/vat/return-and-rubrics.md` |
| Invoice evidence and input VAT | invoice, factuurstelsel, kasstelsel, input VAT, deduction, foreign VAT, call-off, voorraad op afroep | `../nl-tax-shared-resources/knowledge/vat/invoices-and-deduction.md` |
| KOR and special cases | KOR, kleineondernemersregeling, afmelden, withdrawal, jaaromzet in Nederland, preceding calendar year, exemption, ICP, OSS, private use, logies | `../nl-tax-shared-resources/knowledge/vat/kor-and-special-cases.md` |
| Corrections and suppletie | correction, suppletie, Totaalbedrag eerdere btw-aangifte, betalingskenmerk, naheffingsaanslag, teruggaafbeschikking, bezwaar, Central Liaison Office, jaarglobalisatie, discovery, corrected totals, eight weeks, whole-year | `../nl-tax-shared-resources/knowledge/vat/corrections.md` |

## Topics that span income-tax years

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
conversation, provenance, and resume-record contract for workpack preparation.
`../nl-tax-shared-resources/reference/evidence-types.md` and
`../nl-tax-shared-resources/reference/extraction-boundaries.md` govern how a
shared document is classified and recorded. None of them answers a tax-rule
question.

## Extended draft preparation

The notes below cover VAT adjustments, the opgaaf ICP, OSS and IOSS, the
international M and C returns, and the resident annual income-tax return 2026.
They summarize public research dated 2 October 2026 and await human
tax-content review (`needs_review`). Disclose that status in every answer, and
keep the exact tax year, OSS scheme, and M or C form of the question. The
source register records the year of each authority, including the
investment-services and IOSS customs changes that apply only from 2026.

### VAT adjustments 2025/2026 (draft)

| Topic | Key terms | Note |
|---|---|---|
| BUA gifts and staff facilities | BUA, relatiegeschenk, personeelsvoorziening, gifts, staff | `../nl-tax-shared-resources/knowledge/vat-adjustments/bua.md` |
| VAT private use of a business car | private use, business car, woon-werkverkeer, commuting, working days, forfait | `../nl-tax-shared-resources/knowledge/vat-adjustments/car-private-use.md` |
| Margin goods, individual and global methods, reconciliation | margeregeling, margin, individual, global, jaarsaldo, negative annual balance, vaststelling, KOR | `../nl-tax-shared-resources/knowledge/vat-adjustments/margin.md` |
| Direct attribution and taxable/exempt pro-rata | pro-rata, direct attribution, exempt, vrijgestelde, VvE, herziening | `../nl-tax-shared-resources/knowledge/vat-adjustments/mixed-deduction.md` |
| VAT business/private use beyond cars | private use, withdrawal, gratis, computer, gift, staff, property | `../nl-tax-shared-resources/knowledge/vat-adjustments/private-use.md` |
| Property VAT classification and bounded adjustment support | onroerend, verhuur, levering, property, rental, option | `../nl-tax-shared-resources/knowledge/vat-adjustments/property.md` |
| VAT revision of capital goods and investment services | herziening, investeringsgoed, investeringsdienst, revision, capital goods, doorlevering, Uitvoeringsbeschikking omzetbelasting 1968, KOR, VvE, onroerende | `../nl-tax-shared-resources/knowledge/vat-adjustments/revision.md` |

### ICP and OSS 2025/2026 (draft)

| Topic | Key terms | Note |
|---|---|---|
| Opgaaf ICP: period, transactions and reconciliation | opgaaf ICP, ICP, intracommunautaire prestaties, voorraad op afroep, call-off, nieuw vervoermiddel, rubric 3b, btw-id, triangular | `../nl-tax-shared-resources/knowledge/vat-cross-border/icp.md` |
| OSS Union, non-Union and IOSS preparation | OSS, IOSS, eenloketsysteem, Unieregeling, niet-Unieregeling, Invoerregeling, btw-melding, ECB, Northern Ireland, distance sales, three years | `../nl-tax-shared-resources/knowledge/vat-cross-border/oss.md` |

### International M and C returns (draft)

| Topic | Key terms | Note |
|---|---|---|
| 2025 migration and nonresident return scope | migration, nonresident, M form, m-biljet, c-biljet, emigratie, immigratie, buitenlands belastingplichtige, 30%-regeling, partiële buitenlandse belastingplicht, te conserveren inkomen, conserverende aanslag, revisierente, belastingrente, middenkoers, heffingsvrij vermogen | `../nl-tax-shared-resources/knowledge/international/scope-and-forms-2025.md` |
| Qualifying nonresident preparation for 2025 | kwalificerend buitenlands belastingplichtige, 90%-eis, inkomensverklaring, qualifying nonresident, C form, arbeidskorting, aftrekposten | `../nl-tax-shared-resources/knowledge/international/qualification-2025.md` |
| 2026 international precollection | precollection, m-biljet, c-biljet, emigratie, immigratie, 30%-regeling, partiële buitenlandse belastingplicht, provisional, residence | `../nl-tax-shared-resources/knowledge/international/precollection-2026.md` |
| International insurance and treaty review | treaty, tie-breaker, social insurance, SVB, AOW, residence, emigration | `../nl-tax-shared-resources/knowledge/international/insurance-and-treaty-review.md` |

### Annual return 2026 (aangifte inkomstenbelasting 2026, draft)

This note answers the 2026 annual return, which uses actual 2026 figures. For
the voorlopige aanslag 2026, use the provisional 2026 notes above.

| Topic | Key terms | Note |
|---|---|---|
| Annual income-tax 2026 preparation | annual income-tax 2026 preparation, aangifte inkomstenbelasting 2026, jaaropgaaf, zelfstandigenaftrek, startersaftrek, urencriterium, MKB-winstvrijstelling, MKB exemption, tariefsaanpassing, medegerechtigde, AOW, Box 3, werkelijk rendement, tegenbewijs, actual return, bijtelling eigen gebruik, own use, second home, WOZ, forfait, partial foreign tax liability, 30%-regeling, expat ruling, private movements | `../nl-tax-shared-resources/knowledge/years/2026/annual/preparation.md` |
