# Agentic evaluation redesign plan

## Goal

Evaluate the plugin as an LLM-driven Cowork collaborator. The agent owns
interpretation, questions, workflow choice, source use, tax reasoning, and
workpack preparation. Optional scripts perform only mechanical acceleration.

Security/privacy changes are outside this plan. No subagents are used.

## Checklist

### Preserve architecture

- [x] Keep existing tax corrections, workflow boundaries, and artifact owners.
- [x] Keep Python optional and subordinate to agent reasoning.
- [x] Leave security/privacy files and behavior unchanged.

### Separate evaluation types

- [x] Reclassify the 21-fixture dataset as a structural contract library.
- [x] Remove model prompts and case-marker requirements from that dataset.
- [x] Remove one-to-one coupling between fixture cases and live benchmark cases.

### Build the agentic benchmark

- [x] Use five natural conversations: informational, annual preparation,
  provisional change, entrepreneur/Winst, and unsupported boundary.
- [x] Use a minimal workspace rather than a full repository copy.
- [x] Retain only one automated hard-contract verifier.
- [x] Require no exact wording, fixed questions, marker files, or fixed outputs.

### Score agent behavior

- [x] Add a weighted rubric for reasoning, correctness/source use, question
  quality, uncertainty, usefulness, progressive loading, and agent ownership.
- [x] Add hard failures for invented facts, workflow/year mixing, false
  submission/final claims, unsupported overreach, and validator-owned reasoning.
- [x] Add a schema-compatible Plugin Eval metric pack that validates the design.
- [x] Align the native Claude prose suite to the same five user journeys.

### Documentation and historical evidence

- [x] Mark the earlier 21-run exact-output benchmark as superseded.
- [x] Retain an honest concise summary of its results and token limitation.
- [x] Document the difference between static analysis, cumulative benchmark
  tokens, Claude inventory, native Claude eval, and a human Cowork UI smoke.

### Verification

- [x] Run focused evaluation-schema and verifier tests.
- [x] Run both complete test suites and all source/workflow validators.
- [x] Run the metric pack and confirm all five design checks pass.
- [x] Run strict Claude package validation and inventory.
- [x] Confirm `PRIVACY.md` and `SECURITY.md` are unchanged.
- [x] Perform a solo final review and commit the redesign.

The redesigned live benchmark is intentionally not executed automatically as
part of this plan. Run it only when fresh model evidence is needed, then grade
the transcript and outputs with the shared rubric.
