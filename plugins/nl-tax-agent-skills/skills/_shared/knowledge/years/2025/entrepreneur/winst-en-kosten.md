# Rule note: Winstbepaling, kosten en administratie 2025

source_ids: bd_zakelijke_kosten_2025, bd_zakelijke_kosten_een_jaar_2025, bd_zakelijke_kosten_meerdere_jaren_2025, bd_beperkt_aftrekbare_kosten_2025, bd_overzicht_aftrekbare_zakelijke_kosten, bd_werkruimte_2025, bd_privevervoermiddel_2025, bd_oudedagsreserve_2025, bd_aov_voor_ondernemers, bd_administratie_bewaren_2025, bd_bijtelling_auto_2025, urib_2001_art_7_werkkleding, law_uitvoeringsregeling_ib_2001, law_wet_inkomstenbelasting_2001, law_awr_artikel_52
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

Winst uit onderneming is turnover minus deductible business costs, computed under
goed koopmansgebruik (art. 3.8 Wet IB 2001). Only costs made within reasonable
limits for the enterprise are deductible; for mixed (business + private) costs
only the business part is deductible. This note is canonical for the 2025 cost
limits, the werkruimte tests, and the bewaarplicht. Investeringsaftrek,
ondernemersaftrek, and MKB-winstvrijstelling that reduce this winst live in
`investeringsaftrek.md`, `ondernemersaftrek.md`, and `mkb-winstvrijstelling.md`.
Four sibling notes own subjects this note only summarises, and the sibling wins
on every detail: `vervoer-2025.md` for all vehicle content,
`afschrijving-en-bedrijfsmiddelen-2025.md` for depreciation, bedrijfsmiddelen and
the fiscale reserves, `zvw-2025.md` for the inkomensafhankelijke bijdrage
Zorgverzekeringswet, and `inkomensvoorzieningen-2025.md` for AOV premiums,
lijfrente and the oudedagsreserve run-down.

These are reference notes for workpack preparation -- not final tax advice.

## Deducting costs

- Costs relating to one year are generally deducted in full in that year
  (wages, rent, light and heating, annual maintenance). For a purchase, ask
  **both** its tax cost basis and how long the enterprise expects to use it:
  - an item costing less than **EUR 450** may generally be deducted at once;
  - an item costing **EUR 450 or more** that is used for longer than one year is
    a durable business asset whose cost is spread through depreciation;
  - the EUR 450 amount is exclusive of deductible VAT and inclusive of VAT when
    the VAT cannot be recovered.
- Do not turn the price threshold alone into a depreciation rule. Costs paid in
  advance that benefit multiple years (for example multi-year rent, insurance,
  interest, or a multi-year campaign) are also allocated across the years of
  expected benefit even when they are not a tangible asset.
- For a depreciation review, record acquisition cost, costs to make the asset
  ready for use, expected residual value, expected useful life, and the date it
  entered use. If any of these is unresolved, preserve the finalized accounts'
  treatment and flag the schedule for manual review rather than inventing it.

### Btw and the EUR 450 threshold

The btw treatment of the threshold is a rule in its own right, not a footnote to
the price:

- **The rule.** The EUR 450 amount is measured **excluding btw** when the btw on
  the purchase can be reclaimed as voorbelasting, and **including btw** when it
  cannot -- for example where the ondernemer performs only vrijgestelde
  prestaties. Ask which of the two applies before testing an invoice against
  EUR 450: the same invoice can fall on either side of the threshold depending
  on the answer.
- **Exactly EUR 450 is the one boundary case.** The bullets above give the
  ordinary treatment on either side of the threshold. The boundary itself is not
  settled: the official pages describe the low-value exception both as an item
  costing "minder dan EUR 450" and as an aanschafwaarde of "EUR 450 of minder".
  A purchase at exactly EUR 450 therefore has no settled treatment in the sources
  -- route that one case to manual review instead of picking a side, and recheck
  the wording before the next filing season.
- **Cost side only.** This btw rule is about the deductible cost. No official
  page states how btw is treated inside the omzet reported in the aangifte, so
  the agent must not assert one. Take the omzet from the taxpayer's own
  bookkeeping as the accounts present it, and route any question about btw inside
  the omzet to manual review.
- Once a purchase sits above the threshold,
  `afschrijving-en-bedrijfsmiddelen-2025.md` is canonical for what happens next:
  the depreciation method and annual maximum, residual value, the
  afschrijvingsbeperking on buildings, vermogensetikettering, and the fiscale
  reserves. Do not answer a depreciation question from this note alone.

## Non-deductible and limited costs (art. 3.14 - 3.17)

- **Not deductible (0%):** geldboeten (criminal, administrative, EU, dwangsommen)
  and costs of crimes for which the taxpayer is irrevocably convicted; general
  literature (except vakliteratuur); clothing (except werkkleding); personal
  care; telephone subscriptions for the home connection.
- **Werkkleding** counts only if it is (nearly) exclusively suitable to be worn
  in the enterprise, or carries a logo of at least 70 cm2. The logo test comes
  from **artikel 7 Uitvoeringsregeling inkomstenbelasting 2001**, the
  ministeriele regeling that art. 3.16 Wet IB 2001 contemplates: clothing that is
  not exclusively or almost exclusively suitable to be worn in earning the winst
  counts as werkkleding only when it carries one or more clearly visible
  beeldmerken tied to the onderneming, with a combined surface of at least
  70 cm2. The 70 cm2 is a **combined** total across the beeldmerken, not a
  per-logo minimum, and the article applies to an IB-ondernemer, not only to
  employees under the loonbelasting. Werkkleding that passes is 100% deductible;
  clothing that does not is 0%. Ask the taxpayer for the combined logo surface --
  never infer it from a description of the garment.
- **Beperkt aftrekbare kosten (art. 3.15):** for voedsel, drank en genotmiddelen,
  representatie, and congressen/seminars/studiereizen, the first **EUR 5,700** of
  2025 is not deductible; everything above it is. Alternatively the ondernemer
  may elect, per year, to deduct **80%** of these costs instead of applying the
  EUR 5,700 threshold (the 80% figure is the IB-ondernemer rate).
- Travel and accommodation for courses, congresses, and study trips are limited
  to a maximum deduction of **EUR 1,500** unless the nature of the work makes
  attendance necessary.

## Werkruimte in the home (art. 3.16)

Costs of a workspace in a home that belongs to private assets are deductible only
when BOTH tests are met:

- **Zelfstandigheidscriterium:** the workspace is a "naar verkeersopvatting
  zelfstandig gedeelte van de woning" -- own entrance and own sanitary
  facilities, rentable to a third party. A desk in the living room or a converted
  bedroom does not qualify.
- **Inkomenscriterium (relevant income = winst + belastbaar loon + resultaat uit
  overige werkzaamheden):** with a workspace available elsewhere, at least 70%
  ("hoofdzakelijk") of that income must be earned in the home workspace; without
  a workspace elsewhere, at least 70% in or from the home workspace AND at least
  30% ("in belangrijke mate") in it.

## Privegebruik auto van de zaak (art. 3.20)

`vervoer-2025.md` is canonical for every vehicle rule: vermogensetikettering of
the car, the legacy bijtelling windows for cars first admitted before 2025, the
60-month lock, the cap at the actual autokosten, the eigen bijdrage, the
rittenregistratie requirements, the bestelauto regimes, the fiets van de zaak,
and the manual-review boundaries. What follows is only the short form an agent
needs while working through the cost sections; read the sibling note before
answering a vehicle question.

When a car in the ondernemingsvermogen is also available privately, add a
bijtelling to the winst unless a rittenregistratie shows **500 private kilometres or fewer** in the year; commuting counts as business. Before the
agent presents any company-car rate, confirm the date of first admission,
vehicle regime, emissions/fuel facts, catalogue value, and private-use
evidence. If those facts are not known, withhold the rate and mark the outcome
as manual review. For a car confirmed as first admitted in 2025, the standard bijtelling is **22%** of the
cataloguswaarde, with a **17%** rate for zero-emission cars up to a cataloguswaarde
of EUR 30,000 (22% above that; no cap for hydrogen or solar-cell cars); see
bd_bijtelling_auto_2025 for those rates and `vervoer-2025.md` for the full
vehicle rules.

An old car and a claimed zonnecelauto are both **manual review**. A car first
put into use more than 15 years before any day in 2025 is a **screening trigger
only**: route the whole car position to manual review. For such a car the base
switches from the cataloguswaarde to the waarde in het economisch verkeer and a
different percentage applies, but neither the age boundary nor that percentage
is settled across the sources -- article 3.20 lid 1 and article 3.20 lid 5 do
not use the same age, and the Belastingdienst applies a transitional rule on
top -- so neither figure is stated here. The Belastingdienst and the statute
also state the solar-cell condition differently. Do not compute either
outcome -- record the facts and route them, as `vervoer-2025.md` sets out.

## Inkomensafhankelijke bijdrage Zvw is not a business cost

The inkomensafhankelijke bijdrage Zorgverzekeringswet is **not deductible in the
winst**. Art. 3.16 lid 2 onderdeel e Wet IB 2001 excludes the levied
inkomensafhankelijke bijdrage as meant in art. 43 Zorgverzekeringswet -- and any
foreign scheme of the same nature and purport -- when the winst is determined,
and art. 6.18 Wet IB 2001 keeps it out of the uitgaven voor specifieke
zorgkosten, so it is not a persoonsgebonden aftrek item either. The agent must
never subtract the bijdrage from the winst and must never present it as a cost
line in the winst-en-verliesrekening. The same exclusion applies to the
taxpayer's own ingehouden loonbelasting and premies volksverzekeringen.

If the taxpayer's bookkeeping already charged the bijdrage to the winst, correct
the winst upwards and record the correction as a manual-review item.
`zvw-2025.md` is canonical for the percentages, the maximum bijdrage-inkomen,
what the bijdrage is calculated over, and how it is levied and paid; read that
note rather than restating a percentage here.

## AOV premiums

A qualifying private AOV (arbeidsongeschiktheidsverzekering) belongs to the
**private income-provision category**, **not ordinary business costs**. The
agent must not subtract the premium in the winst computation. Inventory the
policy and insurer's annual statement; ambiguous policy types and exact
deductibility remain manual review in Mijn Belastingdienst.

**The payout mirrors the premium.** Where the premium was deductible the payout
is taxed; where the premium was not deductible the payout is not taxed in box 1:

- Premium deductible (a policy paying periodieke uitkeringen on invaliditeit,
  ziekte or ongeval) -> the benefit is reported as **inkomsten uit vroegere
  dienstbetrekking**, not as winst uit onderneming. The insurer withholds
  loonbelasting, which is credited as a voorheffing.
- Premium not deductible (a policy that pays the insured sum in one go) -> the
  lump sum is not reported in box 1, but the money counts towards the box 3
  vermogen.

Never place an AOV benefit in the winst-en-verliesrekening because the policy was
taken out for the business. Ask which policy the taxpayer actually holds and read
the policy type from the insurer's annual statement, not from the product name.
Conditions for deduction, the jaarruimte, and the saldomethode for premiums that
could not be deducted are canonical in `inkomensvoorzieningen-2025.md`.

## Private vehicle used for business

When the ondernemer uses a privately owned or privately rented vehicle (car,
motorcycle, bicycle) for business, **EUR 0.23 per business kilometre** is
deductible from the winst in 2025. All running costs are included in this amount
and may not be deducted separately. For the inkomstenbelasting, commuting counts
as business kilometres. `vervoer-2025.md` is canonical for this rule, for the
kilometre administration it needs, and for the treatment of a scooter, motor or
fiets.

## Oudedagsreserve (overgangsrecht)

Adding to the oudedagsreserve (FOR) has not been possible since 1 January 2023
(paragraaf 3.2.3, art. 3.67-3.73, vervallen). A reserve that existed on
31 December 2022 may remain on the balance sheet and is wound down under the old
rules (overgangsrecht art. 10a.29): it decreases when a lijfrente is purchased,
when it exceeds the ondernemingsvermogen at staking or AOW-leeftijd, when the
ondernemer fails the urencriterium in both the current and the preceding calendar
year, at cessation of the enterprise, or at death. Treat any FOR movement as a
manual-review item. `inkomensvoorzieningen-2025.md` is canonical for the
run-down conditions and for the lijfrente that can absorb a release.

## Administratie and bewaarplicht

- Article 52(1), (2), and (4) AWR is the legal basis for the administration
  duty and the seven-year retention period (`law_awr_artikel_52`).
- Fiscale bewaarplicht: **7 years** for the administratie (basisgegevens such as
  the grootboek, debtor/creditor and purchase/sales records); **10 years** for
  data on onroerende zaken.
- Keep an hours administration (agenda, offertes, urenbriefjes, facturen) to
  support the urencriterium, and keep proof of all costs.

## Resultaat uit overige werkzaamheden

If the taxpayer is not an ondernemer for the inkomstenbelasting and not in
employment, the income is resultaat uit overige werkzaamheden (art. 3.90). Costs
follow the same rules, but there is no ondernemersaftrek, no
MKB-winstvrijstelling, and no investeringsaftrek. Keep it as manual-review data;
do not calculate it as a standard entrepreneur case.

## Developer instruction

1. Record turnover and costs as collected; apply the EUR 5,700 threshold or the
   80% election to the beperkt aftrekbare kosten -- never both -- and show which
   was used.
2. Do not compute the exact car bijtelling or werkruimte outcome from memory;
   collect the inputs and read the rates here and in bd_bijtelling_auto_2025,
   flagging anything ambiguous for manual review in Mijn Belastingdienst.
3. For every cost near or above EUR 450, ask whether it benefits only 2025 or is
   used/benefits multiple years. Depreciation schedules, the FOR run-down, and
   complex mixed-use assets are manual-review items.
4. Before testing a purchase against EUR 450, ask whether the taxpayer reclaims
   the btw on that invoice. Reclaimable btw -> test the amount excluding btw. No
   right to deduct the btw -> test the amount including btw. A purchase at
   exactly EUR 450 goes to manual review.
5. State the btw rule for the cost side only. Do not tell the taxpayer how btw is
   treated inside the omzet -- no official page states it. Take the omzet from
   the taxpayer's bookkeeping as the accounts present it and route any
   btw-in-omzet question to manual review.
6. For clothing, ask two things: whether the garment is exclusively or almost
   exclusively suitable to be worn in the enterprise, and the combined surface of
   the beeldmerken. Apply artikel 7 Uitvoeringsregeling inkomstenbelasting 2001
   to the answer; never assume a logo surface.
7. Never deduct the inkomensafhankelijke bijdrage Zvw from the winst, and never
   list it as a business cost. If the bookkeeping already charged it, correct the
   winst upwards and record the correction. Read `zvw-2025.md` for the
   percentages and the bijdrage-inkomen; do not restate them from this note.
8. For an AOV, read the policy type from the insurer's annual statement, keep the
   premium out of the winst, and apply the mirror rule to any payout: deductible
   premium -> the periodic benefit is taxed as inkomsten uit vroegere
   dienstbetrekking; a non-deductible lump-sum policy -> the lump sum is not
   reported in box 1 but counts towards the box 3 vermogen. The detail lives in
   `inkomensvoorzieningen-2025.md`.
9. Route every vehicle question to `vervoer-2025.md` and every depreciation,
   bedrijfsmiddel or fiscale-reserve question to
   `afschrijving-en-bedrijfsmiddelen-2025.md`. Do not answer either subject from
   this note alone, and do not compute a youngtimer or zonnecelauto outcome.
