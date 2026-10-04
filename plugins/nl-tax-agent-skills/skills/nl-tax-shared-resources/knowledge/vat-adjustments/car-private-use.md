# Rule note: VAT private use of a business car

source_ids: bd_vat_car_private_use, bd_vat_car_commuting, bd_vat_car_policy, bd_vat_car_ib_2025, bd_vat_car_ib_2026
workflow: all
tax_year: 2025, 2026
status: preparation_only
last_verified: "2026-10-02"
review_status: needs_review

Agent researched official sources on 2 October 2026; human tax-content review
is required. These are VAT rules for both years, separate from income-tax
bijtelling. An IB no-bijtelling conclusion is not proof of no VAT private use.
VAT commuting includes travel between home and a fixed workplace; ordinary
customer-site travel is not automatically commuting.

## Forfait and cap

When actual private use cannot be established, the standard forfait is 2.7%
of catalogue value including VAT/BPM; it is 1.5% when no acquisition VAT was
deducted or after the fourth year following the entrepreneur's first-use year.
Thus first use in 2021 means 2.7% through 2025, then 1.5% in 2026. A used car's
original registration year alone does not establish the entrepreneur's window.
Lease, employment contributions, and different purchase/first-use dates need
their own evidence.

Raw annual VAT = catalogue value × applicable fraction × time available for
private use in that year × taxable-use fraction. Use the same taxable/exempt
allocation as the deduction; do not apply it again to an already reduced cap.
For an owned car in the four years after purchase, the maximum is operating/
maintenance VAT actually deducted that year plus one fifth of acquisition VAT
actually deducted. After the acquisition component expires, or without
acquisition deduction, the cap is operating/maintenance VAT actually deducted.
Take the lower of raw forfait and applicable cap. In acquisition year, or with
lease and differing dates, return raw arithmetic and a specific cap-basis
question if the established source treatment does not settle the cap; never
silently reuse a post-acquisition-year cap.

## Actual use

Accept reliable actual-use evidence, including corroborated administrative
evidence rather than assuming only a mileage log is admissible. For a plain
owned car without user contributions, the private fraction is private distance
including commuting divided by total distance.

If confirmed private use consists only of commuting (woon-werkverkeer), the
cited source (bd_vat_car_commuting) allows a shorter method: private distance
= the home-to-fixed-workplace distance × the number of times that distance is
driven in the year, compared at year end with the total distance driven for
taxable business activities. For the number of working days, the same source
allows 214 working days a year, which already accounts for holidays, sickness,
and incidental home working. Apply the 214 days pro rata when fewer than five
days a week are worked or when the private use starts or stops during the year.
Working days are not trips: convert the confirmed working days into the number
of times the home-to-workplace distance is driven (an outward and a return
journey on one working day drive it twice) and record that conversion. The
source example reports 5,000/30,000 × EUR 1,500 = EUR 250 in the last VAT
return of the year. Without any record showing the private use, the forfait
applies instead.

Multiply the source-confirmed
annual VAT cost component (current deductible operating VAT plus applicable
annual acquisition component) by that fraction. Establish acquisition-component
timing separately; do not multiply the full newly deducted purchase VAT by the
private fraction as a replacement for an annual use component. Taxable/exempt
use and private use are different allocations.

The no-administration forfait uses VAT private-use rubric 1d with a zero
left-column base; actual-use calculations need the tax base supported by the
cost evidence. The owner aggregates at year end. Employee payments require
cost/normal-value analysis; do not run the plain no-contribution formula.

## Canonical repository parity data

This data describes the rules above; repository graders read it and do not ship
inside the installed plugin as executable code.

```yaml
vat_adjustment_policy:
  car_standard_fraction: '0.027'
  car_reduced_fraction: '0.015'
  car_following_years: 4
  car_acquisition_parts: 5
```

## Official sources

- bd_vat_car_private_use: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/btw_en_de_auto/privegebruik_auto_van_de_zaak/
- bd_vat_car_commuting: https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/btw_aftrekken/btw_en_de_auto/privegebruik_auto_van_de_zaak/woon_werkverkeer
- bd_vat_car_policy: https://zoek.officielebekendmakingen.nl/stcrt-2020-35053.html
- bd_vat_car_ib_2025: https://www.belastingdienst.nl/wps/wcm/connect/fisin/fisin2025/winst_uit_onderneming
- bd_vat_car_ib_2026: https://www.belastingdienst.nl/wps/wcm/connect/fisin/fisin2026/winst_uit_onderneming
