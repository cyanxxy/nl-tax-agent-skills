#!/usr/bin/env python3
"""Check explicit fiscal-partner allocation percentages.

Usage:
    python3 validate_allocation.py <path-to-allocation.json>

The input must be a wrapped object. The agent determines partner status and
whether each row is allocatable from the reviewed sources; this optional helper
checks only the explicit arithmetic assertions.

{
  "has_fiscal_partner": true,
  "items": [
    {
      "name": "Joint Box 3 base",
      "allocatable": true,
      "taxpayer_pct": 60,
      "partner_pct": 40
    }
  ]
}

Both boolean fields must be JSON booleans. Percentages must be finite JSON
numbers from 0 through 100 and must total 100. A non-allocatable row must be
assigned 100/0 or 0/100. If there is no fiscal partner, partner_pct must be 0.
The helper never classifies a row from its name.
"""

import json
import math
import sys


def _percentage(value, row_name, field, errors):
    """Return an explicit finite numeric percentage, or append an error."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"{row_name}: {field} must be a real finite number")
        return None
    if not math.isfinite(value):
        errors.append(f"{row_name}: {field} must be a real finite number")
        return None
    if value < 0 or value > 100:
        errors.append(f"{row_name}: {field} must be between 0 and 100")
        return None
    return value


def validate(payload):
    """Return arithmetic/type errors for one explicit wrapped payload."""
    errors = []
    if not isinstance(payload, dict):
        return [
            "input must be an object with explicit has_fiscal_partner and items fields"
        ]

    has_fiscal_partner = payload.get("has_fiscal_partner")
    if not isinstance(has_fiscal_partner, bool):
        errors.append("has_fiscal_partner must be a JSON boolean")

    items = payload.get("items")
    if not isinstance(items, list):
        errors.append("items must be an array")
        return errors

    for index, item in enumerate(items):
        row_name = f"item[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{row_name}: must be an object")
            continue

        name = item.get("name")
        if isinstance(name, str) and name.strip():
            row_name = name.strip()

        allocatable = item.get("allocatable")
        if not isinstance(allocatable, bool):
            errors.append(f"{row_name}: allocatable must be a JSON boolean")

        taxpayer_pct = _percentage(
            item.get("taxpayer_pct"), row_name, "taxpayer_pct", errors
        )
        partner_pct = _percentage(
            item.get("partner_pct"), row_name, "partner_pct", errors
        )
        if taxpayer_pct is None or partner_pct is None:
            continue

        if not math.isclose(taxpayer_pct + partner_pct, 100, abs_tol=1e-9):
            errors.append(
                f"{row_name}: taxpayer_pct and partner_pct must total 100"
            )

        if has_fiscal_partner is False and partner_pct != 0:
            errors.append(
                f"{row_name}: partner_pct must be 0 when no fiscal partner asserted"
            )

        if allocatable is False and not (
            (taxpayer_pct == 100 and partner_pct == 0)
            or (taxpayer_pct == 0 and partner_pct == 100)
        ):
            errors.append(
                f"{row_name}: non-allocatable item must be assigned 100% to one partner"
            )

    return errors


def main():
    argv = sys.argv[1:]
    if "-h" in argv or "--help" in argv:
        print("validate_allocation.py — check explicit allocation percentages")
        print("Usage: python3 validate_allocation.py <path-to-allocation.json>")
        return 0
    if len(argv) != 1:
        print(
            "Usage: python3 validate_allocation.py <path-to-allocation.json>",
            file=sys.stderr,
        )
        return 1

    try:
        with open(argv[0], "r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Error loading file: {exc}", file=sys.stderr)
        return 1

    errors = validate(payload)
    if errors:
        print("VALIDATION FAILED")
        print()
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("VALIDATION PASSED")
    print("No issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
