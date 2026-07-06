# Rule note: Ondernemersaftrek 2025

source_ids: bd_ondernemersaftrek_2025, bd_zelfstandigenaftrek_2025, bd_startersaftrek_2025, bd_startersaftrek_ao_2025, bd_meewerkaftrek_2025, bd_stakingsaftrek_2025, bd_so_aftrek_2025, bd_deduction_rate_cap_2025, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-06"
review_status: reviewed

## Rule

The ondernemersaftrek (art. 3.74 Wet IB 2001) is subtracted from the winst uit
onderneming after any investeringsaftrek that reduces the winst and before the
MKB-winstvrijstelling is applied. It is available only to an ondernemer voor de
inkomstenbelasting (see `ondernemer-criteria.md`), never to a medegerechtigde.
For 2025 it is the joint amount of five components:
zelfstandigenaftrek, aftrek voor speur- en ontwikkelingswerk, meewerkaftrek,
startersaftrek bij arbeidsongeschiktheid, and stakingsaftrek. The "gewone"
startersaftrek is not a sixth component -- it is an increase of the
zelfstandigenaftrek (art. 3.76 lid 3). Most components require the urencriterium.

These are reference notes for workpack preparation -- not final tax advice.

## Zelfstandigenaftrek (art. 3.76)

- Zelfstandigenaftrek 2025: **EUR 2,470**.
- Halved to **EUR 1,235** when the ondernemer has reached the AOW-leeftijd at the
  start of the calendar year (see `aow/aow-leeftijd.md` for the AOW-age test).
- Conditions: ondernemer voor de inkomstenbelasting AND meets the urencriterium.
  Not granted over profit earned as medegerechtigde.
- **Winst cap:** the zelfstandigenaftrek is limited to the winst before
  ondernemersaftrek, EXCEPT when the taxpayer is entitled to the startersaftrek.
  The part that cannot be used because of the cap becomes *niet-gerealiseerde
  zelfstandigenaftrek*, set by beschikking, and can be offset in the following
  **9** calendar years (oldest first, only in a year whose winst exceeds that
  year's zelfstandigenaftrek).

The 2025 figure sits on a statutory phase-down path (EUR 3,750 in 2024 ->
EUR 2,470 in 2025 -> EUR 1,200 in 2026). Only EUR 2,470 is used for the 2025
return; do not substitute another year's amount.

## Startersaftrek (art. 3.76 lid 3)

- Startersaftrek 2025: **EUR 2,123** on top of the zelfstandigenaftrek. The
  arithmetic half at AOW-leeftijd is EUR 1,061.50 because the halving covers lid 2
  and lid 3 together; the Belastingdienst publishes the AOW-age startersaftrek as
  **EUR 1,062**.
- Cumulative conditions: (1) entitled to the zelfstandigenaftrek; (2) in one or
  more of the five preceding calendar years the taxpayer was not an ondernemer
  for the inkomstenbelasting; (3) in those five years the zelfstandigenaftrek was
  applied at most twice; (4) no geruisloze terugkeer uit een BV in the relevant
  window. Usable at most three times in the first five years of entrepreneurship.
- When the startersaftrek applies, the winst cap on the zelfstandigenaftrek does
  not apply, so the combined aftrek may exceed the winst and create a loss.

## Aftrek voor speur- en ontwikkelingswerk (S&O) (art. 3.77)

- Base amount 2025: **EUR 15,738**.
- Extra starters amount 2025: **EUR 7,875** on top of the base (total EUR 23,613).
- Conditions: ondernemer meeting the urencriterium, holding an S&O-verklaring
  from RVO (rvo.nl), and spending at least 500 hours in the calendar year on
  recognised speur- en ontwikkelingswerk. The starters increase requires that in
  one or more of the five preceding years the taxpayer was not an ondernemer and
  applied the S&O-aftrek in at most two of those years.

## Meewerkaftrek (art. 3.78)

A percentage of the winst when the fiscal partner works in the enterprise without
(meaningful) pay. Conditions: ondernemer meeting the urencriterium; the fiscal
partner works 525 hours or more in the enterprise; the partner works without any
vergoeding, or with a vergoeding below **EUR 5,000** (such a low vergoeding is
not income for the partner and not deductible for the ondernemer). Table for 2025
(percentage of the joint winst by partner hours):

| Partner hours in the enterprise | Meewerkaftrek |
|---------------------------------|---------------|
| 0 to 525                        | none          |
| 525 to 875                      | 1.25%         |
| 875 to 1,225                    | 2%            |
| 1,225 to 1,750                  | 3%            |
| 1,750 or more                   | 4%            |

## Startersaftrek bij arbeidsongeschiktheid (art. 3.78a)

For a starting ondernemer entitled to an arbeidsongeschiktheidsuitkering who does
not meet the normal urencriterium but does meet the **verlaagd urencriterium of
800 hours** and has not reached AOW-leeftijd at the start of the year. Amounts
2025, each capped at the winst:

- **EUR 12,000** -- not applied in the five preceding years.
- **EUR 8,000** -- applied once in the five preceding years.
- **EUR 4,000** -- applied twice in the five preceding years.

## Stakingsaftrek (art. 3.79)

- Stakingsaftrek 2025: equal to the stakingswinst but **no more than EUR 3,630**.
- Once-per-lifetime maximum: the EUR 3,630 is reduced (not below nil) by
  stakingsaftrek enjoyed in previous years; an unused remainder stays available
  for a later staking.
- Applies when the ondernemer realises profit on the complete cessation of one or
  more whole ondernemingen. A staking event is complex -- prepare the fact and
  route the calculation to manual review.

## Oudedagsreserve

Building up (doteren aan) the oudedagsreserve has not been possible since
1 January 2023; it is not part of the ondernemersaftrek. An existing reserve from
before 2023 is handled under overgangsrecht -- see `winst-en-kosten.md`.

## Tariefsaanpassing (art. 2.10 lid 2)

The ondernemersaftrek and the MKB-winstvrijstelling are grondslagverminderende
posten covered by the tariefsaanpassing: their tax benefit is limited to a
maximum rate of **37.48%** in 2025 for the part of income that would otherwise be
deducted against the 49.50% top rate (box 1 income before these deductions above
the schijf 3 threshold in `../annual/box1-rates.md`). The cap is applied as a
belastingvermeerdering, not by refusing the deduction. See the shared
deduction-rate cap in `../annual/deductions.md` (bd_deduction_rate_cap_2025).

## Developer instruction

1. Apply components only after confirming ondernemer status and the urencriterium
   (verlaagd urencriterium for the startersaftrek bij arbeidsongeschiktheid).
2. Order of calculation: winst uit onderneming after investeringsaftrek, minus
   ondernemersaftrek, then the MKB-winstvrijstelling in
   `mkb-winstvrijstelling.md`.
3. Do not compute the tariefsaanpassing correction from memory; read the top
   bracket threshold from `../annual/box1-rates.md` and the cap from
   `../annual/deductions.md`.
4. Staking, niet-gerealiseerde zelfstandigenaftrek carry-forward, and
   samenwerkingsverband allocation are manual-review items; record the facts and
   direct the taxpayer to verify amounts in Mijn Belastingdienst.
