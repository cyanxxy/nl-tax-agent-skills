# Rule note: Uitvoeringsregeling inkomstenbelasting 2001 -- structural reference

source_id: law_uitvoeringsregeling_ib_2001
workflow: all
tax_year: all
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

The Uitvoeringsregeling inkomstenbelasting 2001 is the ministerial regulation implementing the Wet IB 2001. It contains detailed operational rules that give effect to the provisions of the parent law.

These are reference notes for workpack preparation -- not final tax advice.

## Scope of the regulation

The Uitvoeringsregeling specifies detailed rules for:

- **Income categorization** -- how specific types of income are classified and which box they belong to
- **Deduction requirements** -- conditions that must be met for deductions to be claimed
- **Evidence standards** -- what documentation a taxpayer must retain to substantiate claims
- **Administrative procedures** -- how certain elections and notifications must be made

## Article inventory

This inventory names the articles of the regulation (BWBR0012031) that
entrepreneur (ZZP) preparation relies on and states what each governs. It carries
no rates or thresholds; year amounts live in the year-specific notes under
`../years/`.

### Article 5 -- aanloopkosten and aanloopverliezen

Hoofdstuk 3, "Belastbare winst uit onderneming; verliezen uit de aanloopfase van
een onderneming". This is the operative rule delegated by article 3.10 Wet IB
2001.

- **Where the deduction lands.** The costs are deducted when determining the
  winst of the **first** calendar year as ondernemer. They are not spread over the
  aanloop years and are not obtained by reopening those years.
- **Look-back period.** The total amount of costs and charges made in the five
  calendar years immediately preceding that first calendar year, in so far as they
  relate to starting the onderneming.
- **Two cumulative conditions.** (a) No revenues stood against those costs in that
  period, and (b) they were not, and could not have been, charged against the
  belastbaar inkomen uit werk en woning.
- **No separate election.** The current text prescribes no verzoek and no voor
  bezwaar vatbare beschikking for this deduction.
- The aanloopfase article is **article 5**, not article 6; article 6 covers bos en
  natuur. Do not cite the wrong one.

### Article 7 -- werkkleding

Gives effect to article 3.16 lid 2 onderdeel c Wet IB 2001, under the delegation
in article 3.16 lid 6.

- Clothing that is **not** exclusively or almost exclusively suitable for wearing
  while earning the profit counts as werkkleding only if it carries one or more
  clearly visible beeldmerken tied to the onderneming with a combined surface of
  at least **70 square centimetres**.
- Clothing that **is** exclusively or almost exclusively suitable for wearing in
  the context of the onderneming qualifies on that ground under article 3.16
  lid 5 onderdeel a, without the logo test.
- The logo test applies to the IB-ondernemer, not only to employees under the
  loonbelasting.

## Relevance to this project

### Evidence checklist validation

The regulation defines what evidence is required to support specific deduction claims. The evidence-indexer skill uses these requirements to validate whether a taxpayer's documentation is complete.

### Deduction eligibility checks

Detailed conditions for claiming deductions (e.g., specific care costs, gifts, own-home interest) are specified in this regulation. Skills that calculate or validate deductions must reference these conditions.

## Developer instruction

When building deduction validation or evidence checks:

1. Consult the topic-specific knowledge files that incorporate rules from this regulation
2. Do not reference this regulation directly for specific thresholds or conditions -- those are extracted into topic-specific files
3. When a user asks "what evidence do I need?", the answer ultimately traces back to this regulation via the evidence-checklist knowledge file
4. If a deduction rule appears ambiguous, note the ambiguity and flag for human review rather than guessing
5. Before applying article 5, ask the taxpayer which calendar year was their
   **first** calendar year as ondernemer, and confirm it. Aanloopkosten belong in
   that year's return and in no other.
6. For each claimed aanloopkosten item, ask whether any revenue stood against it
   in the aanloop period and whether it was already deducted against the
   belastbaar inkomen uit werk en woning -- for example as resultaat uit overige
   werkzaamheden. Both conditions must hold before the cost qualifies. Never
   assume the answer.
7. For article 7, ask whether the clothing is exclusively or almost exclusively
   suitable for business wear; only if it is not does the 70-square-centimetre
   logo test decide the case. Route a borderline surface measurement or a mixed
   set of garments to manual review.
8. Aanloopkosten without documentation, and clothing where the taxpayer cannot
   evidence the beeldmerken, are manual-review items: record the facts and let a
   human decide.

## Common failure

Do not treat this file as the source for specific deduction rules or thresholds. Detailed operational rules from this regulation are incorporated into topic-specific knowledge files (e.g., evidence-checklist, own-home rules). Always use those downstream files for implementation.
