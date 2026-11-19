## Box 2 notes

[If no aanmerkelijk belang, emit exactly these two lines and skip the rest of this section:

> Not applicable -- no substantial interest (aanmerkelijk belang) reported.
> box2.has_aanmerkelijk_belang: no
]

### Substantial-interest status

- Has aanmerkelijk belang: [yes/no/manual review]
- Basis: [generally 5% threshold, assessed with fiscal partner where applicable]
- Evidence/source: [F/U/A/?]
- Complex-case review: [none / valuation dispute / emigration / death / restructuring / treaty or nonresident issue / informal capital / non-arm's-length transfer / DGA corporate-tax issue]

### Regular benefits

| Item | Amount | Src |
|------|--------|-----|
| Gross regular benefits, including dividends (`box2.reguliere_voordelen_bruto`) | EUR [amount] | [F/U/A/?] |
| Costs of regular benefits (`box2.kosten_reguliere_voordelen`) | EUR [amount] | [F/U/A/?] |
| Fictitious regular benefit from BV lending (`box2.fictief_regulier_voordeel_bv_lening`) | EUR [amount] | [F/U/A/? / manual review] |
| Dividend withholding tax to credit (`box2.ingehouden_dividendbelasting`) | EUR [amount] | [F/U/A/?] |

### Disposal benefits

| Item | Amount | Src |
|------|--------|-----|
| Net transfer price (`box2.vervreemdingsprijs`) | EUR [amount] | [F/U/A/?] |
| Acquisition price (`box2.verkrijgingsprijs`) | EUR [amount] | [F/U/A/?] |
| Disposal costs used to derive net transfer price (`box2.vervreemdingskosten`) | EUR [amount] | [F/U/A/?] |
| Disposal benefit (`box2.vervreemdingsvoordeel`) | EUR [amount or "manual review required"] | [C:net-transfer-acquisition / F/U/A/?] |

Standard preparation formula: official net transfer price minus acquisition price. Do not subtract disposal costs from `box2.vervreemdingsprijs`; that field is the official net transfer price. Use `box2.vervreemdingskosten` only to derive net transfer price from gross proceeds, and otherwise keep it as provenance/reconciliation so costs are not deducted twice. Use manual review instead of a calculated amount when valuation, informal capital, non-arm's-length, restructuring, treaty, nonresident, emigration, death, or corporate-tax-heavy DGA facts are present.

### Loss setoff and partner allocation

- Substantial-interest loss to set off (`box2.te_verrekenen_verlies_ab`): EUR [amount] -- Src: [F/U/A/?]
- Fiscal-partner Box 2 allocation (`partner.verdeling_box2_inkomen`): [taxpayer %] / [partner %] -- Src: [F/U/A/?]
- Allocation total equals 100%: [yes/no/manual review]

Note: Box 2 allocation and any reviewed calculation remain preparation notes for manual Mijn Belastingdienst entry; they are not filing or tax advice.
