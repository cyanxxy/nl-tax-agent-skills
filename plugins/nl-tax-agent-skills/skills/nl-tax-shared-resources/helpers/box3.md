# Helper: Box 3 Savings and Investments

Internal read-only helper module for `nl-tax-annual-return` and
`nl-tax-provisional-assessment`. Returns Box 3 asset/debt classification,
step-by-step arithmetic, comparison notes, and open-question packets to the
owning workflow. Writes nothing.

## Boundaries

- **Only inside an owning workflow.** Apply only when `nl-tax-annual-return` or
  `nl-tax-provisional-assessment` is active. Never persist files, workpacks,
  field maps, or checklists.
- **Provisional 2026 is fictitious-only (HARD RULE).** Never collect,
  calculate, offer, or ask for werkelijk rendement in any provisional 2026 flow.
  Keep the two strings distinct:
  - *In-workpack explanatory line:* `Werkelijk rendement is not part of provisional 2026.`
  - *Conversational redirect when asked:* `Werkelijk rendement may become relevant when filing the annual 2026 return in 2027.`
- **Annual 2025 two-method rule:** explain both the fictitious (forfaitair)
  calculation and the optional actual-return (werkelijk rendement) comparison.
  Supplying actual-return data is a data-supply choice, NOT a method election —
  Mijn Belastingdienst computes both and applies the more favorable amount.
  Never recommend or elect a method.
- **Annual and provisional stay separate.** Peildatum 1 January 2025 actuals
  belong to annual 2025; 1 January 2026 estimates belong to provisional 2026.
- **Human-only portal & no identifiers.** Follow
  `../nl-tax-shared-resources/runtime-contract.md`: never operate Mijn
  Belastingdienst or record BSN, IBAN, full account numbers,
  policy/contract/aanslag numbers, or credentials.

## Canonical knowledge sources (never paraphrase rates)

Load only the notes matching the active workflow (resolve relative to the active
owning skill directory):

- **Annual 2025:**
  - `../nl-tax-shared-resources/knowledge/years/2025/box3/fictitious.md` (peildatum, heffingsvrij vermogen, drempel schulden, cash/green exemptions, 3 category rates, tax rate, 6-step model)
  - `../nl-tax-shared-resources/knowledge/years/2025/box3/actual-return.md` (included/excluded items, non-deductible costs, WOZ investment correction)
  - `../nl-tax-shared-resources/knowledge/years/2025/box3/examples.md` (optional worked-example parity check)
- **Provisional 2026 (fictitious only):**
  - `../nl-tax-shared-resources/knowledge/years/2026/provisional/box3-provisional.md` (2026 peildatum, allowances, exemptions, provisional category rates, tax rate)

Return every consulted `source_id` to the owning workflow for `Sources used` /
Appendix A `sources_loaded`.

## Asset & debt classification gate

Classify every row from reviewed facts and the canonical knowledge note — never
by keyword alone. Represent each row with `category`, `status`, `value`, and
`provenance`:

- Only rows with `status: "accepted"`, category in `banktegoeden` |
  `overige_bezittingen` | `schulden`, a finite non-negative value, and
  non-empty provenance enter trusted totals.
- Keep every unresolved, ambiguous, or rejected row in a separate
  `rejected / manual_review` table with a reason (never silently drop or zero).
- **Generic loans:** never assume asset vs debt until direction and exceptions
  are confirmed (e.g., `description: "Loan to friend"`, `category: "unknown"`,
  `status: "manual_review"`).
- **Debt inclusion/exclusion screen:** NEVER use the shortcut "all debts except
  the own-home mortgage." Screen every candidate debt against the canonical
  included list (consumer loans, negative bank balances, qualifying study
  finance, Box 3 financing, repayable benefits, inheritance tax) vs excluded
  list (own-home debt, business debts, most Dutch tax debts, short current
  liabilities, deductible maintenance, non-callable surviving-spouse debt,
  Box 2/ROW-linked debts, debts to a fiscal partner or minor child). Unresolved
  debts stay `manual_review` outside accepted totals.
- **Exemptions:** check cash exemption, green savings/investment exemptions,
  and excluded receivables (partner/minor-child/non-callable inheritance) from
  the canonical knowledge note before totaling.

## Arithmetic verification protocol (show every step explicitly)

Double `heffingsvrij vermogen` and `drempel schulden` ONLY after full-year
fiscal partnership is confirmed; an unconfirmed partner is an open question, not
a doubled allowance. Re-confirm any figure not visible verbatim in chat or the
saved workpack.

### Fictitious return (6 official Belastingdienst steps — show each line)

Read all parameters from the canonical note (`fictitious.md` for 2025;
`box3-provisional.md` for 2026), then print every intermediate line:

1. `aftrekbare_schulden = max(0, qualifying_schulden - drempel_schulden)`
   *(Apply threshold only after qualifying debts are summed.)*
2. `belastbaar_rendement = (banktegoeden * bank_pct) + (overige_bezittingen * overige_pct) - (aftrekbare_schulden * schulden_pct)`
   *(Never subtract heffingsvrij vermogen before this step.)*
3. `rendementsgrondslag = banktegoeden + overige_bezittingen - aftrekbare_schulden`
4. `grondslag_sparen_en_beleggen = max(0, rendementsgrondslag - heffingsvrij_vermogen)`
5. `aandeel_in_rendementsgrondslag = taxpayer_share_of_grondslag / rendementsgrondslag` (if `rendementsgrondslag > 0`, else `0`).
   - **Annual 2025 convention:** express as a percentage **truncated toward zero
     to 2 decimal places** (e.g. `53.189% -> 53.18%`), matching official 2025
     examples.
   - **Provisional 2026 convention:** official 2026 guidance mentions 3 decimals
     in text and 2 decimals in examples; state explicitly which convention was
     used and note that the live portal/beschikking is authoritative.
6. `box3_income = belastbaar_rendement * aandeel_in_rendementsgrondslag`
   `box3_tax = box3_income * box3_tax_rate`.

### Annual 2025 actual return (`werkelijk rendement`) — annual 2025 only

- **Branch-applicable inputs only:** for ordinary savings/current/deposit
  accounts, ask for the 1 January 2025 balance (fictitious) and actual 2025
  interest received (actual return) — do **not** ask for a 31 December bank
  balance merely because actual return was offered. Collect year-end /
  acquisition / disposal values only for assets whose value changes count
  (investments, securities, crypto, second homes / Box 3 real estate, etc.).
- **Excluded from actual return:** value changes in the own home (`eigen
  woning`), exempt pension and Box 1 annuity rights (non-exempt periodic
  rights, net annuities, and net pensions may belong in Box 3 -> manual
  review), and exempt life-insurance values including qualifying own-home
  capital insurance (`kapitaalverzekering eigen woning`), whereas non-exempt
  capital insurance values can belong in Box 3.
- **No heffingsvrij vermogen** is deducted from actual return.
- **No costs deducted** (custody, management, transaction, maintenance, bank,
  or adviser fees are excluded), except **interest paid on Box 3 debts** and
  qualifying WOZ investment corrections per `actual-return.md`.
- **Section status:** when complete actual inputs are provided, mark
  `box3_actual` `complete` (or `chat_only` if all from chat) and compare side by
  side, noting the arithmetically lower outcome for user review without
  recommending a method. If the taxpayer declines to supply actual-return data,
  mark `box3_actual` `complete` with `not supplied by choice` (not a gap).
- **Partner allocation:** allocate only the joint `grondslag sparen en
  beleggen` (any split totaling 100%, never individual assets/debts); apply the
  same split percentage to actual return for the comparison.

Record `check_performed_by: checked_by_agent` after verifying row statuses,
finite non-negative values, provenance, and step arithmetic.

## Question packet format

```yaml
- question_id: "annual.box3.peildatum_2025.banktegoeden_total"
  workflow: "annual_2025"
  section: "box3.peildatum"
  prompt_for_user: "What was the total balance across all bank and savings accounts on 1 January 2025? You can also attach bank statements."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "bank statement around 1 January 2025"
- question_id: "provisional.box3.peildatum_2026.overige_bezittingen_total"
  workflow: "provisional_2026"
  section: "box3.peildatum"
  prompt_for_user: "What is your estimate for overige bezittingen on 1 January 2026?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "portfolio statement or estimate"
```
