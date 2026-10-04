# Annual 2026 flow

Load `../nl-tax-shared-resources/knowledge/years/2026/annual/preparation.md`
and its exact source-register entries before tax treatment. Read only the
note needed for the current topic; current general guidance cannot prove a
future annual screen. Use the section keys in `../nl-tax-shared-resources/reference/workflow-scopes.yaml`.
As the runtime contract says, every path in this file resolves relative to the
skill directory that holds `SKILL.md`, not relative to this `reference/` folder.

If someone other than the taxpayer prepares or files the return, read
`../nl-tax-shared-resources/knowledge/security/machtigen.md` and add its
authorization-check step to the workpack; never collect credentials, codes or
sessions.

1. `annual_scope`: confirm annual income tax 2026, resident all year, no deceased
   taxpayer, whether the year has ended, actual coverage dates, missing final
   annual statements and filing notice. Route a migration (M) or nonresident (C)
   case to the international owner.
2. `household`: taxpayer and partner aliases, ages and AOW month, partnership
   dates, children and sourced eligibility facts. Do not compute allocations or
   credits from resident 2025 rules.
3. `income`: actual wages, pension, benefits and other-work income, withholding,
   exempt or foreign elements, original period, sources and refunds. Split
   actual amounts from forecasts.
4. `business`: IB entrepreneurship and legal form, hours, final profit-and-loss
   account and balance sheet, capital movements and private withdrawals,
   inventory, assets and depreciation, investments and disposals, tax
   corrections, prior deduction decisions, and profit before and after each
   deduction. Ordinary reconciled sole-trader draft profit can be prepared; do
   not reuse the 2025 zakelijke screen schema. Special reserves, cessation and
   partnerships need topic-specific review. Keep Zvw separate.
5. `home`: periods, mortgage conditions and interest, WOZ value and valuation
   date, purchases and sales, deductible cost evidence, rental and
   multiple-home treatment.
6. `box2`: before collecting foreign Box 2 items, apply the expat-ruling
   question in step 7. Then collect ownership and substantial-interest (AB)
   status, dividends and withholding, disposals, acquisition cost, loans and
   losses, and partner allocation inputs; unresolved valuations stay open.
7. `box3`: first ask whether the taxpayer already used the expat ruling
   (30%-regeling) on their wages before 2024, whether the ruling still runs in
   2026 (and until which date), and
   whether the taxpayer chooses transitional partial foreign tax liability
   (partiële buitenlandse belastingplicht) for 2026, the last year it is
   available. While this is unresolved, keep foreign Box 2 and Box 3 items as
   evidence, not as Dutch-reportable amounts. Eligibility and the choice are a
   named human-review item; never apply the choice by default. Then collect
   1 January assets, debts and categories; actual receipts, paid Box 3 debt
   interest, beginning and end values and capital movements over the whole
   year. For property collect WOZ dates, use, rental and unusable days, and the
   economic rental value or the explicitly chosen 5.06% method; include the
   2026 own-use addition in the actual-return comparison only, never in the
   fictitious return. Reporting the actual return is optional. Final bank and
   debt forfaits remain unconfirmed; do not call provisional percentages final.
8. `deductions_credits`: evidence and conditions for gifts, care costs,
   maintenance payments, income provisions, carried deductions, relevant credits
   and AOW or social-insurance facts. Use the exact 2026 topic source before any
   calculation; otherwise prepare evidence and leave a topic review blocker
   rather than recall rules.
9. `reconciliation`: reconcile each box, prepayments and withholding, prior
   decisions, remaining gaps and review status. Give no final assessment
   estimate without complete reviewed rates, credits and annual schema. Saving
   and resuming remain available.
10. `confirm`: contextual review of the sourced draft and explicit confirmation
    to generate it; all review blockers remain. The field mapper alone owns the
    map.
