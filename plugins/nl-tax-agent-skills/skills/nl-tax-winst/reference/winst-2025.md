# Winst uit onderneming - Annual 2025: Preparation Notes

source_ids: bd_ondernemer_criteria_2025, bd_urencriterium_2025, bd_ondernemersaftrek_2025, bd_startersaftrek_2025, bd_mkb_winstvrijstelling_2025, bd_kia_2025, bd_eia_2025, bd_zakelijke_kosten_2025, bd_aangifte_ondernemers_2025
workflow: annual_return
tax_year: 2025
status: active
review_status: reviewed
last_reviewed: "2026-07-04"

## Contents

- Scope
- Ondernemer status and urencriterium
- Winst computation order
- Ondernemersaftrek components
- MKB-winstvrijstelling
- Investeringsaftrek
- Costs, werkruimte, and car
- Evidence
- Complex or manual-review markers

## Scope

Use these notes for standard full-year Dutch resident annual 2025 preparation
workpacks for an IB-ondernemer with an eenmanszaak (the usual ZZP legal form).
Outputs are for manual Mijn Belastingdienst entry and review only. The reviewed
knowledge notes under `_shared/knowledge/years/2025/entrepreneur/` are canonical
for every amount, percentage, and threshold; read them and never paraphrase a
figure from memory.

## Ondernemer status and urencriterium

- Confirm the taxpayer is an ondernemer voor de inkomstenbelasting before
  preparing any winst figure (see `ondernemer-criteria.md`). A KvK registration or
  btw-ondernemerschap alone is not enough.
- Record whether the urencriterium is met as a yes/no fact; it gates the
  zelfstandigenaftrek and several other components. For the startersaftrek bij
  arbeidsongeschiktheid the verlaagd urencriterium applies instead.
- If the income looks like resultaat uit overige werkzaamheden rather than winst
  uit onderneming, route it to manual review.

## Winst computation order

Prepare the figures in this order and show each step:

1. Winst uit onderneming = turnover minus deductible business costs.
2. Minus investeringsaftrek that comes ten laste van de winst, including KIA.
3. Minus the ondernemersaftrek (only the components the case qualifies for).
4. Apply the MKB-winstvrijstelling to the result of step 3.

## Ondernemersaftrek components

- Prepare only the components that apply: zelfstandigenaftrek (plus the
  startersaftrek increase where the starter conditions are met), aftrek voor
  speur- en ontwikkelingswerk, meewerkaftrek, and the startersaftrek bij
  arbeidsongeschiktheid. Read the amounts and conditions from `ondernemersaftrek.md`.
- The winst cap on the zelfstandigenaftrek and any niet-gerealiseerde
  zelfstandigenaftrek carry-forward are recorded as review data.
- The tax benefit of the ondernemersaftrek is subject to the tariefsaanpassing;
  read the cap from the shared deduction-rate note.

## MKB-winstvrijstelling

- Applies to every ondernemer with no urencriterium requirement, on the winst
  after investeringsaftrek and ondernemersaftrek. Read the percentage from `mkb-winstvrijstelling.md`;
  it cannot be allocated to a fiscal partner.

## Investeringsaftrek

- Prepare the kleinschaligheidsinvesteringsaftrek from the KIA table in
  `investeringsaftrek.md` when the taxpayer invested in qualifying
  bedrijfsmiddelen for the year. Confirm each asset meets the minimum and is not
  on the exclusion list.
- EIA, MIA, Vamil, and the desinvesteringsbijtelling depend on RVO verklaringen
  and annual lists; treat exact eligibility as manual-review data.

## Costs, werkruimte, and car

- Apply the beperkt-aftrekbare-kosten threshold or the alternative percentage
  election (never both) from `winst-en-kosten.md`, and show which was used.
- Werkruimte in a private-asset home, the private-use-of-a-business-car
  bijtelling, and the private-vehicle kilometre deduction are prepared from the
  knowledge notes; flag anything ambiguous for manual review.
- For a company car, record whether the taxpayer can substantiate **500 private kilometres or fewer**. Confirm the date of first admission, vehicle regime,
  emissions/fuel facts, catalogue value, and private-use evidence before
  showing a rate. When these are not known, withhold the rate and keep the
  bijtelling as manual review.

## Evidence

- Ask for the winst-en-verliesrekening, balans, invoices, bank jaaroverzicht,
  investment invoices, and urenadministratie as gaps when missing (see
  `entrepreneur-aangifte.md`). Never assume zeros and never collect the BSN.

## Complex or manual-review markers

Route the case out of the standard helper path when any of these are present:

- Partnership (VOF, maatschap, CV) or profit-share allocation.
- Medegerechtigdheid or a geldverstrekker position.
- DGA / BV winst or corporate-tax interaction.
- Agrarische onderneming (landbouwvrijstelling) or zeevarende.
- Staking or cessation of the enterprise, herinvesteringsreserve, or
  oudedagsreserve wind-down.
- Emigration, immigration, treaty, nonresident, or partial-year resident issue.
- Resultaat uit overige werkzaamheden rather than winst uit onderneming.
