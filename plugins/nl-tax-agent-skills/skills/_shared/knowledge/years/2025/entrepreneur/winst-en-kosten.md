# Rule note: Winstbepaling, kosten en administratie 2025

source_ids: bd_zakelijke_kosten_2025, bd_beperkt_aftrekbare_kosten_2025, bd_werkruimte_2025, bd_privevervoermiddel_2025, bd_oudedagsreserve_2025, bd_administratie_bewaren_2025, bd_bijtelling_auto_2025, law_wet_inkomstenbelasting_2001, law_awr_artikel_52
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-10"
review_status: reviewed

## Rule

Winst uit onderneming is turnover minus deductible business costs, computed under
goed koopmansgebruik (art. 3.8 Wet IB 2001). Only costs made within reasonable
limits for the enterprise are deductible; for mixed (business + private) costs
only the business part is deductible. This note is canonical for the 2025 cost
limits, the werkruimte and car rules, the oudedagsreserve run-down, and the
bewaarplicht. Investeringsaftrek, ondernemersaftrek, and MKB-winstvrijstelling
that reduce this winst live in `investeringsaftrek.md`,
`ondernemersaftrek.md`, and `mkb-winstvrijstelling.md`.

These are reference notes for workpack preparation -- not final tax advice.

## Deducting costs

- Costs relating to one year are deducted in full in that year (wages, rent,
  light and heating, annual maintenance). An item costing **EUR 450 or more** is
  a bedrijfsmiddel and must be depreciated; below EUR 450 it may be deducted at
  once.

## Non-deductible and limited costs (art. 3.14 - 3.17)

- **Not deductible (0%):** geldboeten (criminal, administrative, EU, dwangsommen)
  and costs of crimes for which the taxpayer is irrevocably convicted; general
  literature (except vakliteratuur); clothing (except werkkleding); personal
  care; telephone subscriptions for the home connection.
- **Werkkleding** counts only if it is (nearly) exclusively suitable to be worn
  in the enterprise, or carries a logo of at least 70 cm2.
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

When a car in the ondernemingsvermogen is also available privately, add a
bijtelling to the winst unless a rittenregistratie shows **500 private kilometres or fewer** in the year; commuting counts as business. Before the
agent presents any company-car rate, confirm the date of first admission,
vehicle regime, emissions/fuel facts, catalogue value, and private-use
evidence. If those facts are not known, withhold the rate and mark the outcome
as manual review. For a car confirmed as first admitted in 2025, the standard bijtelling is **22%** of the
cataloguswaarde, with a **17%** rate for zero-emission cars up to a cataloguswaarde
of EUR 30,000 (22% above that; no cap for hydrogen or solar-cell cars). A
youngtimer (first registered more than 15 years ago) uses **35% of the economic
value** instead of the catalogue value. See bd_bijtelling_auto_2025 for the full
rules.

## AOV premiums

A qualifying private AOV (arbeidsongeschiktheidsverzekering) belongs to the
**private income-provision category**, **not ordinary business costs**. The
agent must not subtract the premium in the winst computation. Inventory the
policy and insurer's annual statement; ambiguous policy types and exact
deductibility remain manual review in Mijn Belastingdienst.

## Private vehicle used for business

When the ondernemer uses a privately owned or privately rented vehicle (car,
motorcycle, bicycle) for business, **EUR 0.23 per business kilometre** is
deductible from the winst in 2025. All running costs are included in this amount
and may not be deducted separately. For the inkomstenbelasting, commuting counts
as business kilometres.

## Oudedagsreserve (overgangsrecht)

Adding to the oudedagsreserve (FOR) has not been possible since 1 January 2023
(paragraaf 3.2.3, art. 3.67-3.73, vervallen). A reserve that existed on
31 December 2022 may remain on the balance sheet and is wound down under the old
rules (overgangsrecht art. 10a.29): it decreases when a lijfrente is purchased,
when it exceeds the ondernemingsvermogen at staking or AOW-leeftijd, when the
ondernemer fails the urencriterium in both the current and the preceding calendar
year, at cessation of the enterprise, or at death. Treat any FOR movement as a
manual-review item.

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
3. Depreciation schedules, the FOR run-down, and complex mixed-use assets are
   manual-review items.
