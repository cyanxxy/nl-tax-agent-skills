# Rule note: VVA/EVA algorithm-register handling for provisional assessment 2026

source_id: bd_algoritmeregister_vva_eva
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-11"
review_status: reviewed

## Rule

The Belastingdienst algorithm register describes VVA selection rules and EVA business rules. It does not describe a submitted "delta" model. The skill may use a baseline-vs-current comparison as an internal review aid for the taxpayer, but must not present that comparison as Belastingdienst processing logic.

## Key terms

### VVA -- Verzoek Voorlopige Aanslag

A VVA is a request for a provisional assessment submitted by the taxpayer. The taxpayer provides estimated income, deductions, and assets/debts for the current year. The Belastingdienst processes this into a monthly payment or refund schedule.

### EVA -- Eerste Voorlopige Aanslag

An EVA is a first provisional assessment that the Belastingdienst may issue without a taxpayer request, using earlier available data. This later **unsolicited** VA **may be issued**, but it is **not guaranteed**. If one arrives and the taxpayer's situation has changed, it should be reviewed and potentially changed (see review-flow.md and change-flow.md).

## Official algorithm-register scope

The algorithm-register entry describes two official processes:

### VVA selection rules

- A taxpayer-submitted VVA is assessed using selection rules.
- The selection rules help determine whether a request can be accepted automatically or needs manual handling.
- This is an internal Belastingdienst process; the taxpayer does not interact with the rules directly.

### EVA business rules

- EVA uses business rules to estimate a first provisional assessment, based on the most recent definitive or provisional assessment data available to the Belastingdienst.
- If the taxpayer's situation has changed, the EVA should be reviewed and potentially changed (see review-flow.md and change-flow.md).

## Important distinctions

### Provisional assessment is NOT the annual return

- The provisional assessment is **forward-looking**: it estimates what the taxpayer will owe or be refunded for the current year
- The annual return is **backward-looking**: it calculates actual tax based on realized income, deductions, and assets
- These are fundamentally different workflows and must not be conflated

### Provisional assessment is NOT "annual return lite"

- The data collected for a provisional assessment is a subset of what the annual return requires
- Estimates are accepted (and expected) for the provisional assessment
- Precision requirements are lower -- the goal is a reasonable monthly amount, not an exact tax calculation
- Some elements of the annual return (e.g., werkelijk rendement for box 3) do not apply to the provisional assessment

## Weegmodule (weighing module)

The Belastingdienst applies a weegmodule (weighing module) to VVA submissions:

- Business rules evaluate whether submitted estimates can be processed automatically
- Values may be routed to manual handling or follow-up under internal rules
- This is an internal Belastingdienst process -- the taxpayer does not interact with the weegmodule directly

## Developer instruction

When modeling the provisional assessment workflow:

1. Model the user workflow as a forward-looking estimate, not as "annual return lite"
2. When reviewing or changing an existing assessment, compare the current assessment with the user's updated estimates as a workpack review aid only
3. Do not state that the Belastingdienst processes or receives a delta
4. Present any comparison as informational; the official portal recalculates from the complete submitted data
5. Do not reuse annual return data structures or flows for the provisional assessment -- build separate, purpose-built flows
6. Accept estimates and indicate that precision is lower than in the annual return, because final settlement occurs through the 2026 annual return
7. When an EVA is present, use it as the current assessment to review and allow the user to adjust it through a VVA

## Common failure

Do not claim that the Belastingdienst uses or accepts a baseline + forecast + delta submission. A delta summary is only a taxpayer-facing explanation of what changed between the current assessment and the prepared updated estimates.
