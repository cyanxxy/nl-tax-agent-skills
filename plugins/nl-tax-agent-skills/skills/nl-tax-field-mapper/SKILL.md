---
name: nl-tax-field-mapper
description: Use when a workpack needs a manual-entry field map.
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 *.py:*)
---

# NL Tax Field Mapper

Convert an existing workpack into a field map the taxpayer can follow while manually filling the official portal.

Use mapping principles, the matching field reference, and the field-map template. Trace every value to evidence, estimate, baseline, calculation, profile path, or assumption.

Write only the matching `field-map.yaml`. Validate with `scripts/validate_field_map.py`. Never merge annual/provisional maps, map credentials, or include werkelijk-rendement fields in provisional 2026.
