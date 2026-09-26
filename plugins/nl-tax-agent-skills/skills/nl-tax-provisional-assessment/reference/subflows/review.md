## Review subflow

### Conversational review checkpoints

1. Is the review subflow confirmed in the conversation, or in Appendix A of a resumed workpack?
2. Is there a current voorlopige aanslag available to review?
   - From a beschikking the user shares, recorded as a `Documents and sources` row
   - From user input
3. Was the current voorlopige aanslag issued without a taxpayer request (EVA) or user-submitted (VVA)?
   - EVA: especially important to verify, as it is based on prior-year data that may be outdated
4. Have any life events occurred since the voorlopige aanslag was issued?

### Data collection steps

1. **Current voorlopige aanslag capture** — record all key figures:
   - Monthly payment or refund amount
   - Income figures used
   - Deductions used
   - Box 3 data used
2. **Life event screening** — ask about changes in each category:
   - Income: new job, salary change, retirement, job loss, started/stopped benefits
   - Housing: new mortgage, sold home, refinanced, paid off mortgage
   - Partner: marriage, separation, divorce, partner income changes
   - Deductions: started/stopped alimentatie, changed premiums, other
   - Credits: IACK, ouderenkorting, alleenstaandeouderenkorting, and jonggehandicaptenkorting facts requiring manual review. Alleenstaandeouderenkorting concerns entitlement to an AOW pension for a single person, not children or single-parent status.
   - Box 2: expected dividends, share sales, costs, dividend withholding tax, or partner allocation changed
   - Box 3: corrections to the estimated asset or qualifying debt values on 1 January 2026; apply the official debt inclusion/exclusion screen, and remember that later-year changes do not change the 2026 box 3 peildatum
   - AOW: below all year, reaches during 2026, or AOW all year. For a
     transition, record the month and review the live portal result rather than
     selecting a whole-year table.
3. **Comparison** — for each category, note whether the current voorlopige aanslag figure still matches reality

### Output generation

1. At the generation gate, produce the workpack from `templates/provisional-workpack.md` with review context, including the `Existing baseline, if any` section and the completed `Review questions` section: the category review table, the recommended action summary, and the change-subflow trigger; every `unknown` category has a question under `Open questions`
2. Review produces no field map; `Field map summary` reads "N/A — no field map is produced for this subflow."
3. Record under `Assumptions` only assumptions the user explicitly accepted
4. If changes are needed: explicitly recommend the change subflow, explain what would change, and note that a change collects the complete dataset again rather than only the changed rows

---
