# Rule note: ALEF methodology reference

source_id: regels_overheid_regelspraak
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

ALEF (Agile Law Execution Framework) is a Dutch methodology for executable legislation, used by the Belastingdienst and other government agencies. This project borrows ALEF principles as style guidance for structuring tax rules, without implementing ALEF formally.

## ALEF overview

ALEF provides a framework for translating legislation into executable decision logic. It is used by the Dutch Tax and Customs Administration (Belastingdienst) to build systems that apply tax law consistently and traceably.

### Key concepts

- **Rule decomposition** -- complex legal provisions are broken down into discrete, individually testable rules
- **Decision tables** -- rules with multiple conditions and outcomes are expressed as structured tables rather than nested prose
- **Traceability to legal source** -- every executable rule maintains a direct link to the article or paragraph of law it implements
- **Separation of concerns** -- fact-finding (what evidence exists) is separated from rule application (what the law says about those facts)

## How this project uses ALEF principles

This project does not implement ALEF as a formal framework. It borrows the following principles:

### Decompose complex tax topics into discrete, testable rules

Each knowledge file covers one topic. Within that topic, individual rules are stated as clear conditions with defined outcomes. A rule like "box 3 tax is calculated as forfaitair rendement times the box 3 rate" is decomposed into: asset categorization, weighted return calculation, heffingsvrij vermogen deduction, and rate application.

### Maintain source traceability

Every rule note includes a source_id linking to source-register.yaml. Every source register entry links to the official publication. This mirrors ALEF's requirement that executable rules trace back to law.

### Separate fact-finding from rule application

- **Fact-finding** (evidence collection) is handled by the evidence-indexer skill. It determines what documents and data the taxpayer has.
- **Rule application** (calculation and validation) is handled by the domain skills (box1-home, box3, partner-deductions). They apply rules to the collected facts.

This separation prevents the calculation skills from making assumptions about what evidence exists, and prevents the evidence skill from making tax law judgments.

### Make assumptions explicit

When a rule note makes an assumption (e.g., "this applies to resident taxpayers only" or "this assumes the taxpayer is not a fiscal partner"), the assumption is stated explicitly in the rule body or developer instruction section.

## Developer instruction

When structuring tax rules in this project:

1. Break complex calculations into named steps -- each step should be independently verifiable
2. When a rule has multiple conditions, consider whether a structured list or table is clearer than nested prose
3. Always state which legal source the rule derives from
4. Keep evidence collection (what do we know?) separate from rule application (what does the law say about what we know?)
5. State assumptions explicitly -- do not embed unstated prerequisites in calculation logic

## Common failure

Do not combine fact-finding and rule application in a single step. If a skill needs to both collect evidence and apply a rule, it should do these as separate, sequential operations so that each can be verified independently.
