# Rule note: Uitvoeringsbesluit inkomstenbelasting 2001 -- structural reference

source_id: law_uitvoeringsbesluit_ib_2001
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

The Uitvoeringsbesluit inkomstenbelasting 2001 is the government decree (Algemene Maatregel van Bestuur) implementing the Wet IB 2001. It sits between the law and the ministerial regulation in the legal hierarchy and contains rules that require government-level approval.

## Scope of the decree

The Uitvoeringsbesluit specifies detailed rules on:

- **Eigenwoningforfait percentages** -- the imputed rental value rates applied to owner-occupied homes, broken down by WOZ value brackets
- **Box 3 category definitions** -- precise definitions of what constitutes banktegoeden, overige bezittingen, and schulden for box 3 purposes
- **Specific deduction thresholds** -- threshold amounts and caps for certain deductions that are set by government decree rather than by law or ministerial regulation

## Relevance to this project

### Own-home calculations (box 1)

The eigenwoningforfait percentages are defined in this decree. The box1-home skill uses these percentages to calculate the imputed rental value added to box 1 income. Year-specific percentages are in year-specific knowledge files.

### Box 3 asset classification

The decree provides the formal definitions for assigning assets and debts to box 3 categories (Categorie I, II, III). The box3 skill relies on these definitions to correctly categorize a taxpayer's holdings.

### Deduction thresholds

Certain deduction thresholds (e.g., drempel for specific care costs, threshold for gifts) are set at decree level. These are extracted into year-specific knowledge files for use by the relevant skills.

## Developer instruction

When building own-home or box 3 calculations:

1. Use year-specific knowledge files for eigenwoningforfait percentages -- they change annually
2. Use the box 3 category definitions from this decree (via the year-specific box3 knowledge files) to classify assets
3. Do not hard-code thresholds from this decree -- they are year-dependent
4. When a classification is ambiguous (e.g., crypto-assets, rights to periodic payments), flag for human review

## Common failure

Do not look up specific rates or thresholds in this file. This is a structural reference that explains what the Uitvoeringsbesluit covers. Specific rates and thresholds are in year-specific knowledge files under `_shared/knowledge/years/`.
