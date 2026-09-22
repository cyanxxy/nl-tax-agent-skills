# Missing Information Register

This file tracks information that is needed but not yet provided. Items here block workpack completion or reduce confidence.

## Format

Each entry should include:

- **ID:** missing item number (e.g., M001)
- **Category:** income / deduction / box3 / partner / own-home / evidence / other
- **Workflow:** annual_2025 / provisional_2026 / both
- **Description:** what information is missing
- **Needed for:** which workpack section or field requires this
- **Blocking:** yes (workpack cannot be completed) / no (workpack can proceed with reduced confidence)
- **Suggested action:** how the user can provide this information
- **Status:** open / provided / not_applicable

## Template

| ID | Category | Workflow | Description | Needed for | Blocking | Suggested action | Status |
|----|----------|----------|------------|------------|----------|-----------------|--------|
| M001 | evidence | annual_2025 | Jaaropgaaf 2025 from employer | Box 1 income | Yes | Upload annual salary statement | Open |

## Rules

1. Every field with `value: null` in the field map should have a corresponding missing-info entry.
2. Blocking items must be resolved before the workpack is marked ready for review.
3. Non-blocking items reduce field confidence but do not prevent workpack generation.
