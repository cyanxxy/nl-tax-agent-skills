# Helper: Box 1 Income and Own Home (Eigen Woning)

Internal read-only helper module for `nl-tax-annual-return` and
`nl-tax-provisional-assessment`. Returns sourced Box 1 income and eigen woning
findings, arithmetic checks, and open-question packets to the owning workflow.
Writes nothing.

## Boundaries

- **Only inside an owning workflow.** Apply only when `nl-tax-annual-return` or
  `nl-tax-provisional-assessment` is active. Never persist files, workpacks,
  field maps, or checklists.
- **Human-only portal & no identifiers.** Follow
  `../nl-tax-shared-resources/runtime-contract.md`: never operate Mijn
  Belastingdienst or collect/record BSN, IBAN, policy, contract, or aanslag
  numbers, or credentials; identify documents by provider + year.
- **Annual and provisional stay separate.** Annual 2025 uses actual 2025
  evidence and 2025 knowledge notes; provisional 2026 uses clearly labeled
  estimates (or `B:` baseline values) and 2026 provisional notes. Never carry an
  annual amount into provisional facts without taxpayer review as a 2026
  estimate.

## Canonical knowledge sources (never paraphrase rates)

Load only the notes matching the active workflow (resolve relative to the active
owning skill directory):

- **Annual 2025:**
  - `../nl-tax-shared-resources/knowledge/years/2025/annual/box1-rates.md` (brackets, AOW rates, bijtelling, stock options)
  - `../nl-tax-shared-resources/knowledge/years/2025/annual/own-home.md` (WOZ peildatum, eigenwoningforfait, tariefsaanpassing cap, Hillen percentage)
  - `../nl-tax-shared-resources/knowledge/own-home/eigenwoningforfait.md` and `../nl-tax-shared-resources/knowledge/own-home/hypotheekrenteaftrek.md` (when own-home details apply)
- **Provisional 2026:**
  - `../nl-tax-shared-resources/knowledge/years/2026/provisional/rates-and-credits.md` (2026 provisional brackets, AOW transition rates, credits)
  - `../nl-tax-shared-resources/knowledge/years/2026/provisional/own-home.md` (2026 WOZ peildatum 1 Jan 2025, 2026 forfait, cap rate, Hillen percentage)
  - `../nl-tax-shared-resources/knowledge/own-home/eigenwoningforfait.md` and `../nl-tax-shared-resources/knowledge/own-home/hypotheekrenteaftrek.md` (when own-home details apply)

Return every consulted `source_id` to the owning workflow for `Sources used` /
Appendix A `sources_loaded`.

## Evidence & input gates

1. Use a value only from a confirmed chat answer (`U:` with quote and date) or
   a `Documents and sources` row (`ev_NNN`). If a required value is still
   missing — or no longer visible verbatim in the conversation or saved
   workpack — return a question packet entry and **stop short of calculating
   that line**; never reconstruct from memory, silently substitute zero, or
   treat a missing value as not applicable.
2. **Annual 2025:** a document closes a gap only when its row is `extracted`
   (not `needs review`) and its tax year is `2025` (flag a wrong-year
   jaaropgaaf as an anomaly and exclude it).
3. **Provisional 2026:** year-end evidence (jaaropgaaf 2026, hypotheek
   jaaroverzicht 2026) is not required. Label every figure as an estimate or
   baseline (`B:`) with its source and any uncertainty note; preserve supplied
   precision or whole euros without inventing arbitrary rounding.

## Box 1 income classification & screening

### Employment, pension, and benefits

- **Employment (`loon uit dienstbetrekking`):** copy `loon`, `fiscaal loon`, or
  `loon voor de loonheffing` verbatim from each jaaropgaaf; never reconstruct
  from generic gross salary or subtract employee-insurance premiums. Credit
  `ingehouden loonheffing`. `Verrekende arbeidskorting` is informational;
  `premie Zvw` is not deductible by an employee.
- **Multiple sources:** collect ALL jaaropgaven/statements, sum taxable wages
  and withheld loonheffing, and flag a review note because combined income can
  push into a higher bracket than individual employers withheld for.
- **Pensions:** require a **payment-year pension statement** showing taxable
  pension paid and withholding. A UPO is **accrual or projection context only**
  and is never payment-year evidence. AOW from SVB is taxable Box 1 income.
- **Benefits:** UWV (WW, WIA, WAO, Ziektewet), SVB (AOW, Anw), and municipal
  benefits (bijstand) are taxable Box 1 income. **AKW (kinderbijslag) is NOT
  taxable Box 1 income** — never include it.
- **Provisional 2026 estimates:**
  - *Employment:* estimate `fiscaal loon` from YTD payroll plus remaining pay
    (account for raises, job changes, leave, holiday-allowance double-counting,
    bonuses/13th month; or use latest jaaropgaaf as a labeled baseline and ask
    about material 2026 changes).
  - *Pensions & benefits:* use a 2026 payment schedule when available, or
    annualise current taxable payments noting known 2026 changes. For an AOW
    transition year, use the actual start month — never multiply a post-start
    monthly payment by 12. For UWV benefits (WW, WIA), note that WW typically
    decreases or expires during the year; mark all pension/benefit estimates as
    subject to change.

### Edge cases (screen before calculating)

- **Company car (bijtelling):** confirm date of first admission, vehicle/fuel
  regime, cataloguswaarde, and whether private use is substantiated at 500 km or
  fewer before applying rates from `box1-rates.md`. Otherwise mark manual
  review. Note bijtelling is normally already inside jaaropgaaf taxable wage;
  if bijtelling seems incorrect or missing, flag it as a review question.
- **Stock options & equity awards:** for stock options, **tradability** is the
  default tax point; immediate tradability or an exercise-date election needs
  the employer statement and manual review. Never apply the stock-option rule or
  a blanket "taxed at vesting" rule to RSUs, restricted shares, or other equity
  awards — identify the exact instrument and payroll tax event from employer
  statements; keep unclear awards, foreign payroll, or cross-border service
  periods in manual review.
- **Foreign employer without Dutch withholding:** if a foreign employer did not
  withhold Dutch `loonheffing`, the employment income must **still be reported
  in Box 1** — include it and flag foreign employment / cross-border
  implications for review.
- **Severance payments (`ontslagvergoeding` / `transitievergoeding`):** Box 1
  taxable income. Paid as a lump sum, the full amount is taxable in the year
  received (flag large payouts for review because they can push income into a
  higher bracket). If paid into a pre-2014 `stamrecht` transitional arrangement,
  different rules may apply — flag for manual review.
- **Out-of-helper Box 1 items (route, never misclassify as employment wage):**
  self-employment (`winst uit onderneming`) and freelance/side income (`ROW`) go
  to `../nl-tax-shared-resources/helpers/winst.md`; received partner alimony
  (`alimentatie ontvangen`) is Box 1 income — flag if detected.

## Own-home (eigen woning) rules & arithmetic parity

### Screening & complex-home boundary

- One ordinary main residence (hoofdverblijf) may receive a review estimate.
- **Complex own-home cases -> collect facts & route to manual review:** two
  homes, sale/purchase overlap in the same year, temporary double housing
  (`verhuisregeling`), partial-year ownership, divorce use, or bijleenregeling
  / eigenwoningreserve questions. Collect registration, move, listing, sale,
  purchase, vacancy/rental, and mortgage dates.
- **Mortgage qualification:** loan must finance purchase/improvement/maintenance
  of the main residence (max 30-year period). Post-2013 loans require an
  annuitair or lineair repayment schedule. **Pre-2013 transitional rule
  (overgangsrecht):** refinancing a qualifying pre-2013 balance for the same
  amount does not itself forfeit deduction (including aflossingsvrij); test any
  loan increase separately.
- **WOZ peildatum:** annual 2025 uses peildatum **1 January 2024**; provisional
  2026 uses peildatum **1 January 2025** (if unavailable, use latest notice only
  as a clearly labeled fallback estimate with a review item).
- **Deductible vs non-deductible:** deductible = mortgage interest paid +
  qualifying one-off mortgage financing costs (advice, mortgage-deed notary/
  cadastre, valuation for loan, NHG fee) + qualifying boeterente + periodic
  erfpacht/opstal/beklemming. Non-deductible = principal repayments, home
  insurance, maintenance/renovation, purchase costs (overdrachtsbelasting,
  purchase broker, purchase deed).

- **Provisional 2026 mortgage-interest projection by loan type:**
  - *Annuity (`annuitair`):* interest decreases each year as principal is repaid —
    use the lender's 2026 schedule if available, or estimate from remaining
    balance and interest rate.
  - *Linear (`lineair`):* estimate from remaining balance minus annual principal
    repayment, multiplied by the interest rate.
  - *Interest-only (`aflossingsvrij`, pre-2013 qualifying):* use current annual
    interest.
  - Flag uncertainty if the interest rate is variable or resets during 2026.

### Arithmetic parity check (show every line explicitly)

For one ordinary main residence, after accepting sourced inputs and loading the
year's canonical knowledge note:

1. `eigenwoningforfait = round_whole_euro(WOZ_value * canonical_forfait_rate)`
   (or canonical villa formula above the top WOZ threshold).
2. `total_deductible_own_home_costs = mortgage_interest + qualifying_financing_costs + periodic_erfpacht_opstal_beklemming`.
3. `hillen_deduction`: if `eigenwoningforfait > total_deductible_own_home_costs`,
   compute `(eigenwoningforfait - total_deductible_own_home_costs) * canonical_hillen_pct`;
   otherwise `EUR 0`. (Hillen uses the full deductible-costs total, never
   mortgage interest alone.)
4. Record `box1_balance_components` as ONLY `eigenwoningforfait`,
   `total_deductible_own_home_costs`, and `hillen_deduction`.
5. `box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`.
6. **Tariefsaanpassing (separate `review_adjustments` only — NEVER inside
   `box1_balance_components` or taxable Box 1 income):** follow art. 2.10 lid 2
   Wet IB 2001 using the canonical year schijf 2 boundary (`drempel`), top
   bracket rate, and cap rate:
   - First determine `belastbaar_inkomen_uit_werk_en_woning` — Box 1 taxable
     income **after** `box1_own_home_balance` (after the eigen woning deduction
     and any Hillenregeling adjustment).
   - `grondslag = min(afgetrokken_eigenwoningkosten, max(0, belastbaar_inkomen_uit_werk_en_woning + afgetrokken_eigenwoningkosten - drempel))`
     *(Applies only when Box 1 income **without** the own-home deduction exceeds
     `drempel`; capped at `afgetrokken_eigenwoningkosten` so the correction can
     never exceed `(top_rate - cap_rate) * afgetrokken_eigenwoningkosten`.)*
   - `tariefsaanpassing = grondslag * (top_rate - cap_rate)`.
   - If total Box 1 income is not yet known, emit a warning that
     tariefsaanpassing may apply and must be checked once Box 1 income is
     complete.
7. Record `check_performed_by: checked_by_agent`.

### Missing-data flags

Flag and return an open question when absent from confirmed documents/chat:
`missing_woz`, `missing_mortgage_statement`, `missing_mortgage_start_year`,
`missing_ownership_share`, `missing_move_date` (if applicable), `unverified_woz`.

## Question packet format

Return missing inputs to the owning workflow as:

```yaml
- question_id: "annual.box1.employment.gross_income.employer_1"
  workflow: "annual_2025"
  section: "box1.employment"
  prompt_for_user: "What was your gross 2025 taxable employment income (loon voor de loonheffing) from this employer? You can also share the jaaropgaaf."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "jaaropgaaf 2025"
- question_id: "annual.eigen_woning.woz_2024_for_2025"
  workflow: "annual_2025"
  section: "eigen_woning"
  prompt_for_user: "What is your WOZ-waarde with peildatum 1 January 2024, used for the 2025 return?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "WOZ-beschikking"
```
