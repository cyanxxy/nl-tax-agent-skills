# Rule note: Regelspraak methodology for structured rule notes

source_id: regels_overheid_regelspraak
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

Regelspraak is a Dutch methodology for writing rules in a structured, traceable format. It is used by Dutch government agencies for formalizing business rules. This project adopts Regelspraak principles to keep its tax knowledge auditable and maintainable.

## Key principles

### Clear rule statement

Each rule note should have a clear, unambiguous rule statement that describes what the rule says. The rule statement should be understandable on its own, without requiring the reader to consult the source.

### Source traceability

Each rule should reference its legal or official source via source_id. This creates a two-way link:

- From rule back to source: every rule note declares which source it is derived from
- From source forward to rules: the source-register.yaml lists which skills depend on each source

### Testability

Rules should be testable -- given a set of facts about a taxpayer's situation, you can evaluate whether the rule is satisfied or not. If a rule cannot be expressed as a testable condition, it should be decomposed further.

### Traceability chain

The full traceability chain in this project is:

1. Official source (law, regulation, Belastingdienst guidance) -- registered in source-register.yaml
2. Knowledge file (rule note) -- contains the rule statement and developer instructions
3. Skill (SKILL.md) -- references the knowledge files it depends on
4. Workpack output -- the result presented to the user, traceable back through the chain

## Format used in this project

Each rule note follows this structure:

### Header block

```
source_id: <matching id from source-register.yaml>
workflow: <annual_return | provisional_assessment | all>
tax_year: <specific year or all>
status: <active | draft | deprecated>
last_reviewed: "<ISO date>"
review_status: <reviewed | needs-review>
```

### Body sections

- **Rule** -- what the rule says (the core statement)
- **Developer instruction** -- how to implement the rule in the skill
- **Common failure** -- what mistakes to avoid when applying the rule

Additional sections may be included where the topic requires them (e.g., calculation methods, partner allocation rules, evidence requirements).

## Why this matters

Tax rules change annually. By structuring knowledge as discrete, source-traced rule notes:

- Annual updates can be applied systematically (change the year-specific file, verify against source)
- Errors can be traced to their source (which rule note, which source, which skill)
- New tax years can be added by cloning and updating year-specific files
- Auditors (human or automated) can verify that rules match their sources

## Developer instruction

When creating or updating rule notes:

1. Always include the source_id header -- it must match an entry in source-register.yaml
2. Write the Rule section as a clear, self-contained statement
3. Write the Developer instruction section with actionable steps for the skill implementer
4. Write the Common failure section to prevent known mistakes
5. Keep rule notes focused on one topic -- if a file covers multiple unrelated rules, split it
6. When updating for a new tax year, create a new file under the appropriate year directory rather than modifying the existing one

## Common failure

Do not write rule notes without a source_id. Untraceable rules cannot be verified, audited, or systematically refreshed.
