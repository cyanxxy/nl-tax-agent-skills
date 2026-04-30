#!/usr/bin/env python3
"""Validate fiscal partner allocation splits.

Usage:
    python validate_allocation.py <path-to-allocations.json>

Input JSON format:
[
  {
    "item": "Box 3 banktegoeden",
    "total": 80000,
    "partner1_share": 50000,
    "partner2_share": 30000,
    "allocatable": true
  }
]

Checks:
    - partner1_share + partner2_share == total
    - No negative values
    - Non-allocatable items are 100% to one partner
    - No shares exceeding total
"""

import json
import sys

NON_ALLOCATABLE_KEYWORDS = {
    "employment", "loon", "salary", "dienstbetrekking",
    "pension", "pensioen",
    "arbeidskorting",
}


def validate_allocations(items):
    errors = []
    warnings = []

    for i, item in enumerate(items):
        name = item.get("item", f"item[{i}]")
        total = item.get("total", 0)
        p1 = item.get("partner1_share", 0)
        p2 = item.get("partner2_share", 0)
        allocatable = item.get("allocatable", True)

        # Negative values
        if total < 0:
            warnings.append(f"{name}: total is negative ({total}) — verify this is a debt/deduction")
        if p1 < 0:
            errors.append(f"{name}: partner1_share is negative ({p1})")
        if p2 < 0:
            errors.append(f"{name}: partner2_share is negative ({p2})")

        # Sum check (allow for debts where total may be negative)
        if abs(total) > 0 or abs(p1) > 0 or abs(p2) > 0:
            if abs((p1 + p2) - total) > 0.01:
                errors.append(
                    f"{name}: shares don't sum to total "
                    f"({p1} + {p2} = {p1 + p2}, expected {total})"
                )

        # Shares exceeding total (for positive totals)
        if total > 0:
            if p1 > total:
                errors.append(f"{name}: partner1_share ({p1}) exceeds total ({total})")
            if p2 > total:
                errors.append(f"{name}: partner2_share ({p2}) exceeds total ({total})")

        # Non-allocatable check
        name_lower = name.lower()
        is_non_allocatable = not allocatable or any(
            kw in name_lower for kw in NON_ALLOCATABLE_KEYWORDS
        )
        if is_non_allocatable:
            if p1 > 0 and p2 > 0:
                errors.append(
                    f"{name}: non-allocatable item is split between partners "
                    f"({p1}/{p2}) — must be 100% to one partner"
                )

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_allocation.py <path-to-allocations.json>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(items, list):
        print("Error: input must be a JSON array of allocation items", file=sys.stderr)
        sys.exit(1)

    errors, warnings = validate_allocations(items)

    if errors:
        print("VALIDATION FAILED")
        print()
        print("Errors:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("VALIDATION PASSED")

    if warnings:
        print()
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")

    if not errors and not warnings:
        print("No issues found.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
