# Rule note: Uitvoeringsbesluit inkomstenbelasting 2001 -- structural reference

source_id: law_uitvoeringsbesluit_ib_2001
workflow: all
tax_year: all
status: active
last_reviewed: "2026-07-11"
review_status: reviewed

## Rule

The Uitvoeringsbesluit inkomstenbelasting 2001 is the government decree (Algemene Maatregel van Bestuur) implementing the Wet IB 2001. It sits between the law and the ministerial regulation in the legal hierarchy and contains rules that require government-level approval.

## Scope of the decree

The Uitvoeringsbesluit specifies detailed rules on:

- **Box 3 category definitions** -- precise definitions of what constitutes banktegoeden, overige bezittingen, and schulden for box 3 purposes
- **Specific deduction thresholds** -- threshold amounts and caps for certain deductions that are set by government decree rather than by law or ministerial regulation

## Relevance to this project

### Box 3 asset classification

The decree provides the formal definitions for assigning assets and debts to box 3 categories (Categorie I, II, III). The box3 skill relies on these definitions to correctly categorize a taxpayer's holdings.

### Deduction thresholds

Certain deduction thresholds (e.g., drempel for specific care costs, threshold for gifts) are set at decree level. These are extracted into year-specific knowledge files for use by the relevant skills.

## Developer instruction

When building own-home or box 3 calculations:

1. Attribute the eigenwoningforfait and its table to article 3.112 Wet IB 2001,
   then use year-specific knowledge files for the applicable year
2. Use the box 3 category definitions from this decree (via the year-specific box3 knowledge files) to classify assets
3. Do not hard-code thresholds from this decree -- they are year-dependent
4. When a classification is ambiguous (e.g., crypto-assets, rights to periodic payments), flag for human review

## Common failure

Do not look up specific rates or thresholds in this file. This is a structural reference that explains what the Uitvoeringsbesluit covers. Specific rates and thresholds are in year-specific knowledge files under `_shared/knowledge/years/`.
