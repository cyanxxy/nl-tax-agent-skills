## Phase 2A — Winst uit onderneming preparation-only

Organize business-section facts and questions for an IB-ondernemer with an
eenmanszaak. This is preparation-only: it does not establish final taxable
business profit and does not claim a complete business return. If the taxpayer
has no onderneming, emit the canonical "not applicable" line and continue.

Invoke or inline `nl-tax-winst`. Require a finalized profit-and-loss statement
and finalized balance for 2025. Preserve their evidence provenance and append
only actually consulted entrepreneur `source_id`s to
`sources_loaded_by_workflow.annual_2025` and the active `sources_loaded` mirror.

### 2A.1 Ondernemer status and urencriterium

- Confirm the taxpayer is an ondernemer voor de inkomstenbelasting with an eenmanszaak; a KvK registration or btw-ondernemerschap alone is not enough (see `ondernemer-criteria.md`).
- Record `business.has_onderneming` as `true`/`false` in the profile (the template's boolean enum); route to manual review when the status is unclear or when the income looks like resultaat uit overige werkzaamheden.
- Record hours and candidate-deduction evidence as review facts, without deciding the final deduction.

### 2A.2 Finalized accounts and review packet

- Organize the finalized profit-and-loss categories and finalized balance
  categories exactly as supplied; do not recalculate the accounts.
- Review material purchases and prepaid costs with two independent questions:
  the tax cost basis and whether the item/cost benefits only 2025 or more than
  one year. Do not treat EUR 450 by itself as a complete depreciation decision.
  Record the supplied depreciation schedule and its acquisition cost, in-use
  date, useful life, and residual value; unresolved treatment remains a focused
  review question.
- Record open reconciliation, classification, hours, investment, and candidate
  deduction questions. Do not apply ondernemersaftrek, MKB-winstvrijstelling,
  KIA, Zvw, cessation profit, or final tax.
- Keep the annual field map `readiness: draft` and add the blocker
  `business-section schema review`. No `onderneming.*` amount is filing-ready
  until a complete reviewed zakelijke schema exists.

### 2A.3 Manual-review triggers

- Require manual review for partnerships (VOF, maatschap, CV) and profit-share allocation, medegerechtigdheid, DGA/BV winst, agrarische ondernemingen, zeevarenden, staking/cessation events, herinvesteringsreserve, oudedagsreserve wind-down, and resultaat uit overige werkzaamheden.
- Do not calculate these complex positions; record the facts and route to terminal professional review.

---
