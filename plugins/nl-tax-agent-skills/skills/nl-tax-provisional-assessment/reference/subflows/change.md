## Change subflow

Before the first user-facing change reply, state: "Prepare and verify the
complete dataset; the change form requires all applicable categories, not only
the changed item." Do this before baseline or intake follow-up questions, and
repeat the reminder on every collection turn until final confirmation. The
portal may offer to pre-fill figures from the most recent annual return, but it
does not carry forward the current voorlopige-aanslag figures; whether the form
opens blank or pre-filled, prepare and verify every applicable category and
never claim that omitted values default to zero.

### Conversational review checkpoints

1. Is the change subflow confirmed in the conversation, or in Appendix A of a resumed workpack?
2. Is there a baseline available?
   - From a beschikking the user shares, recorded as a `Documents and sources` row
   - From user input (user provides current voorlopige aanslag details)
   - If no baseline at all: ask user to provide the current monthly amount and key figures from their beschikking
3. Does the taxpayer have a fiscal partner? Has partner status changed?

### Data collection steps

1. **Baseline capture** — record the existing voorlopige aanslag details:
   - Monthly payment or refund amount
   - Income categories as submitted
   - Deductions as submitted
   - Box 3 data as submitted
   - Whether the 2026 voorlopige aanslag was extended automatically or opened pre-filled, and which year's figures it rests on
2. **Rollover-trap check** -- a 2026 voorlopige aanslag that was extended automatically or opened pre-filled rests on an earlier year's figures, and no reviewed source recalculates a carried-over business estimate for the new year's ondernemersaftrek. Ask, and record with provenance: which year's figures the current voorlopige aanslag 2026 rests on; what profit estimate it uses and whether that is still the taxpayer's own best estimate for 2026; and whether the taxpayer's own reasoning about the amount still uses a zelfstandigenaftrek from an earlier year. Read both years' amounts from `../nl-tax-shared-resources/knowledge/years/2026/provisional/winst-provisional-2026.md`, never from memory, and flag any calculation still resting on a zelfstandigenaftrek above the 2026 amount: the deduction is overstated, so too little is being paid through the year. An unanswered question stays an open question -- never fill the gap with an assumption and never enter a zero. A change made to the voorlopige aanslag 2025 after the cut-off date stated in that note is not carried into 2026 automatically, so re-derive the estimate from the taxpayer's own current forecast.
3. **Full re-entry of all current estimates** (CRITICAL — not just changes):
   - All income categories (employment, pension/benefit, other, and the dedicated expected-profit forecast when applicable); include the expected-profit forecast in the Box 1 rollup
   - **State the estimate's definition before recording it.** Before recording `onderneming.geschatte_winst`, tell the taxpayer what the single figure means: the winst they expect to earn as ondernemer in 2026, taken **before** the ondernemersaftrek and **before** the MKB-winstvrijstelling, excluding the btw payable and the btw reclaimable, with a minus sign for an expected loss. Record it only after the taxpayer confirms it on those terms. Read the definition, the invulhulp item list, and every 2026 business figure from `../nl-tax-shared-resources/knowledge/years/2026/provisional/winst-provisional-2026.md`; never apply annual deductions, a bijdrage Zvw amount, cessation profit, or final tax, and never build or request a balans or a winst-en-verliesrekening.
   - **Voorlopige aanslag Zorgverzekeringswet** -- whenever there is winst uit onderneming or income from work performed outside employment, raise the separate bijdrage Zvw without waiting to be asked, using `../nl-tax-shared-resources/knowledge/years/2026/provisional/zvw-provisional-2026.md` for every figure. Tell the taxpayer there are two separate aanslagen with separate change routes. No reviewed source establishes whether a change to the income-tax voorlopige aanslag is coupled to the Zvw assessment, so the taxpayer must check the Zvw assessment separately and record what they find. Ask: "Have you (the taxpayer) received a voorlopige aanslag Zorgverzekeringswet for 2026, and what income estimate does it use?", record the answer with provenance or as an open question, and carry the action line "You (the taxpayer) also check your voorlopige aanslag Zorgverzekeringswet 2026 in Mijn Belastingdienst and change it through its own route if its estimate is no longer right." Report it alongside the income-tax dataset and never merged into it: no bijdrage amount; no Zvw field, value, label, note, or row in the income-tax field map; and never subtract it from the profit estimate.
   - All deductions, including the separate own-home components: eigenwoningforfait using WOZ peildatum 1 January 2025, total deductible own-home costs, any Hillen deduction, and `box1_own_home_balance`
   - All standard Box 2 estimates (regular benefits, disposal benefits, costs, withholding tax, partner allocation)
   - All box 3 data (assets and qualifying debts as of 1 January 2026, fictitious method only); apply the official debt inclusion/exclusion screen and keep unresolved debts outside accepted totals
   - On every turn until final confirmation, remind the user: "Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item."
4. **Delta calculation** — compare baseline to current estimates:
   - Per-category: employment, pension/benefit, expected business profit,
     other income, each own-home component, deductions, box 3, and partner
     changes
   - A review direction for the possible future payment/refund effect; only the
     live portal and replacement beschikking determine the actual amount and
     timing
   - The voorlopige aanslag Zorgverzekeringswet as a companion item reported
     beside the table, never as a delta row and never merged into the
     income-tax delta

### Output generation

1. At the generation gate, produce the workpack from `templates/provisional-workpack.md` with change context, including the `Existing baseline, if any` section and the completed `Delta summary` section (baseline vs forecast, under `reference/delta-rules.md`)
2. Include the `Change subflow — full re-entry reminder` section in the body, before `Field map summary`
3. Then continue with `nl-tax-field-mapper`; it alone composes and checks the field map, shows its summary table in the conversation (never the YAML), and writes `Field map summary` and Appendix B only while save consent is active in this conversation
4. Record under `Assumptions` only assumptions the user explicitly accepted; note unavailable baseline fields in the `Delta summary` section as a non-blocking note (under `reference/delta-rules.md`), not as an assumption or a Missing information row

---
