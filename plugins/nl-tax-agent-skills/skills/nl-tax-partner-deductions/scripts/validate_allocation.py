#!/usr/bin/env python3
"""Validate fiscal partner allocation splits.

Usage:
    python3 validate_allocation.py [--no-partner] <path-to-allocations.json>

Input JSON format (bare list, backward compatible):
[
  {
    "item": "Box 3 banktegoeden",
    "total": 80000,
    "partner1_share": 50000,
    "partner2_share": 30000,
    "allocatable": true
  }
]

Or the wrapped object shape:
{
  "has_fiscal_partner": true,
  "items": [ ... ]
}

Checks:
    - partner1_share + partner2_share == total
    - No negative values
    - Non-allocatable items are 100% to one partner
    - No shares exceeding total
    - Numeric inputs are real finite numbers (rejects strings, None, NaN, Inf,
      and booleans)
    - Duplicate item names are flagged
    - Fully-empty rows (no total and no shares) are warned about
    - partner2_share > 0 is rejected when no fiscal partner is asserted

Note: `allocatable` is inferred heuristically from the item name when not
provided (see NON_ALLOCATABLE_KEYWORDS). This heuristic is best-effort only;
callers should set `allocatable` explicitly on each item to avoid surprises.
Numeric amounts must be carried as JSON numeric literals — this validator does
NOT parse Dutch-locale number strings (e.g. "1.000,50").
"""

import json
import math
import sys

NON_ALLOCATABLE_KEYWORDS = {
    "employment", "loon", "salary", "dienstbetrekking",
    "pension", "pensioen",
    "arbeidskorting",
}


def _num(value, name, field, errors):
    """Coerce an input to a finite number or record an error and return None.

    Rejects booleans, non-numeric types (strings, None, lists), and NaN/Inf so
    downstream arithmetic cannot crash with a TypeError or silently propagate a
    non-finite value.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"{name}: {field} is not a number ({value!r})")
        return None
    if not math.isfinite(value):
        errors.append(f"{name}: {field} is not a finite number ({value})")
        return None
    return value


def validate_allocations(items, has_fiscal_partner=True):
    errors = []
    warnings = []
    seen_names = {}

    for i, item in enumerate(items):
        name = item.get("item", f"item[{i}]")

        # Duplicate detection (key on item name)
        seen_names[name] = seen_names.get(name, 0) + 1
        if seen_names[name] == 2:
            warnings.append(f"{name}: duplicate item name appears more than once")

        total = _num(item.get("total", 0), name, "total", errors)
        p1 = _num(item.get("partner1_share", 0), name, "partner1_share", errors)
        p2 = _num(item.get("partner2_share", 0), name, "partner2_share", errors)
        allocatable = item.get("allocatable", True)

        # Skip arithmetic if any numeric field failed to parse.
        if total is None or p1 is None or p2 is None:
            continue

        # Fully-empty row (no amounts at all)
        has_total = "total" in item and item.get("total") not in (None, 0)
        has_shares = (
            ("partner1_share" in item and item.get("partner1_share") not in (None, 0))
            or ("partner2_share" in item and item.get("partner2_share") not in (None, 0))
        )
        if not has_total and not has_shares:
            warnings.append(
                f"{name}: no amounts provided — incomplete allocation row"
            )

        # Negative values
        if total < 0:
            warnings.append(f"{name}: total is negative ({total}) — verify this is a debt/deduction")
        if p1 < 0:
            errors.append(f"{name}: partner1_share is negative ({p1})")
        if p2 < 0:
            errors.append(f"{name}: partner2_share is negative ({p2})")

        # No partner asserted but partner2 has a share
        if not has_fiscal_partner and p2 > 0:
            errors.append(
                f"{name}: partner2_share ({p2}) > 0 but no fiscal partner asserted"
            )

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
    argv = sys.argv[1:]
    no_partner = False
    if "--no-partner" in argv:
        no_partner = True
        argv = [a for a in argv if a != "--no-partner"]

    if not argv:
        print(
            "Usage: python3 validate_allocation.py [--no-partner] <path-to-allocations.json>",
            file=sys.stderr,
        )
        sys.exit(1)

    path = argv[0]
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        sys.exit(1)

    has_fiscal_partner = not no_partner

    # Accept either a bare list or a wrapped {has_fiscal_partner, items} object.
    if isinstance(data, dict):
        if "items" not in data or not isinstance(data["items"], list):
            print(
                "Error: object input must contain an 'items' array",
                file=sys.stderr,
            )
            sys.exit(1)
        items = data["items"]
        if "has_fiscal_partner" in data and not no_partner:
            has_fiscal_partner = bool(data["has_fiscal_partner"])
    elif isinstance(data, list):
        items = data
        if not no_partner:
            print(
                "Note: bare-list input assumes a fiscal partner is present; "
                "pass --no-partner or the {has_fiscal_partner, items} shape to "
                "assert otherwise.",
                file=sys.stderr,
            )
    else:
        print(
            "Error: input must be a JSON array of allocation items or an object "
            "with an 'items' array",
            file=sys.stderr,
        )
        sys.exit(1)

    errors, warnings = validate_allocations(items, has_fiscal_partner=has_fiscal_partner)

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
