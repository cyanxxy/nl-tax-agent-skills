#!/usr/bin/env python3
"""Validate structured Box 2 inputs for standard NL tax preparation support.

The validator separates hard input errors from manual-review routing. Complex
substantial-interest situations are flagged for review without making the CLI
fail; malformed input exits nonzero.

Usage:
    python3 validate_box2_inputs.py input.json
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
import sys
from pathlib import Path
from typing import Any


SUPPORTED_WORKFLOWS = {
    "annual_2025": 2025,
    "provisional_2026": 2026,
}

MONETARY_NON_NEGATIVE_FIELDS = {
    "regular_benefits",
    "regular_costs",
    "disposal_price",
    "gross_disposal_price",
    "acquisition_price",
    "disposal_costs",
    "fictitious_regular_benefit_bv_loan",
    "loss_setoff",
    "dividend_withholding_tax",
    "bv_loan_balance",
}

COMPLEX_MARKERS = {
    "valuation_dispute": "Valuation dispute for shares or transfer price.",
    "emigration": "Emigration or immigration can trigger special Box 2 rules.",
    "death": "Death during the year needs estate and succession review.",
    "restructurings": "Merger, split, share-for-share exchange, or restructuring.",
    "treaty_nonresident_issues": "Treaty, nonresident, or partial-year residence issue.",
    "informal_capital": "Informal capital or shareholder contribution issue.",
    "non_arm_length_transfers": "Transfer may not be at arm's length.",
    "corporate_tax_heavy_dga_cases": "DGA case depends heavily on corporate-tax analysis.",
    "inherited_gifted_ab": "Inherited or gifted substantial interest.",
    "fictive_disposal": "Potential fictive disposal event.",
    "excessive_borrowing_uncertainty": "Uncertain excessive-borrowing position.",
}

STANDARD_BOUNDARY_FLAGS = {
    "resident_full_year": "Taxpayer is not confirmed as a full-year Dutch resident.",
    "standard_ab_case": "Substantial-interest position is not marked as a standard case.",
}

# Every payload key this validator (or the sibling calculator) consumes. Keys
# outside this set are silently ignored downstream — usually a typo'd amount
# field that would default to 0 — so flag them.
KNOWN_PAYLOAD_KEYS = (
    MONETARY_NON_NEGATIVE_FIELDS
    | set(COMPLEX_MARKERS)
    | set(STANDARD_BOUNDARY_FLAGS)
    | {
        "workflow",
        "tax_year",
        "disposal_benefit",
        "substantial_interest_pct",
        "partner_allocation",
        "allocation",
        "full_year_fiscal_partner",
        "complex_markers",
    }
)


def _decimal(value: Any, field_name: str) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{field_name} must be numeric")
    if not result.is_finite():
        # NaN/inf would raise InvalidOperation inside later comparisons
        # instead of a clean validation error.
        raise ValueError(f"{field_name} must be a finite number")
    return result


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _add_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def _is_truthy_flag(value: Any) -> bool:
    """Interpret a marker flag: strings like "no"/"false" must not count as set."""
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "ja", "1"}
    return bool(value)


def _workflow_year(payload: dict[str, Any], errors: list[str]) -> tuple[str | None, int | None]:
    workflow = payload.get("workflow")
    tax_year = payload.get("tax_year")

    if workflow is None:
        errors.append("workflow is required: annual_2025 or provisional_2026")
    elif not isinstance(workflow, str) or workflow not in SUPPORTED_WORKFLOWS:
        # isinstance guard: an unhashable value (YAML list) must produce a
        # validation error, not a TypeError traceback.
        errors.append("workflow must be annual_2025 or provisional_2026")
        workflow = None

    parsed_year: int | None = None
    if tax_year is None:
        errors.append("tax_year is required")
    else:
        try:
            parsed_year = int(tax_year)
        except (TypeError, ValueError):
            errors.append("tax_year must be 2025 or 2026")

    if workflow in SUPPORTED_WORKFLOWS and parsed_year is not None:
        expected_year = SUPPORTED_WORKFLOWS[workflow]
        if parsed_year != expected_year:
            errors.append(f"{workflow} requires tax_year {expected_year}")

    if parsed_year is not None and parsed_year not in SUPPORTED_WORKFLOWS.values():
        errors.append("tax_year must be 2025 or 2026")

    return workflow, parsed_year


def _validate_money_fields(payload: dict[str, Any], errors: list[str]) -> dict[str, Decimal]:
    amounts: dict[str, Decimal] = {}
    for field_name in MONETARY_NON_NEGATIVE_FIELDS:
        try:
            value = _decimal(payload.get(field_name), field_name)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if value is None:
            continue
        if value < Decimal("0"):
            errors.append(f"{field_name} must be non-negative")
            continue
        amounts[field_name] = value

    if "disposal_benefit" in payload and payload.get("disposal_benefit") is not None:
        try:
            value = _decimal(payload.get("disposal_benefit"), "disposal_benefit")
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if value is not None:
                amounts["disposal_benefit"] = value

    return amounts


def _validate_partner_allocation(
    payload: dict[str, Any],
    errors: list[str],
    manual_review_flags: list[str],
    warnings: list[str],
) -> None:
    allocation = payload.get("partner_allocation") or payload.get("allocation")
    if not allocation:
        return
    if not isinstance(allocation, dict):
        errors.append("partner_allocation must be an object")
        return

    try:
        taxpayer_pct = _decimal(allocation.get("taxpayer_pct"), "taxpayer_pct")
        partner_pct = _decimal(allocation.get("partner_pct"), "partner_pct")
    except ValueError as exc:
        errors.append(str(exc))
        return
    if taxpayer_pct is None or partner_pct is None:
        errors.append("partner_allocation requires taxpayer_pct and partner_pct")
        return
    if taxpayer_pct < 0 or taxpayer_pct > 100 or partner_pct < 0 or partner_pct > 100:
        errors.append("partner allocation percentages must be between 0 and 100")
        return
    if _money(taxpayer_pct + partner_pct) != Decimal("100.00"):
        errors.append("partner allocation percentages must total 100")
        return

    full_year_partner = payload.get("full_year_fiscal_partner")
    if full_year_partner is False:
        _add_unique(manual_review_flags, "not_full_year_fiscal_partner")
        warnings.append(
            "Box 2 allocation is only standard for full-year fiscal partners."
        )
    elif full_year_partner is not True:
        # Missing/unconfirmed partner status is NOT a supported standard case:
        # the indicative split must prove full-year fiscal-partner eligibility.
        _add_unique(manual_review_flags, "partner_status_unconfirmed")
        warnings.append(
            "Box 2 allocation requires confirmed full-year fiscal-partner status; "
            "set full_year_fiscal_partner: true to proceed as a standard case."
        )


def validate_box2_input_payload(payload: dict[str, Any]) -> dict:
    """Validate a Box 2 JSON payload and return errors/warnings/flags."""
    errors: list[str] = []
    warnings: list[str] = []
    manual_review_flags: list[str] = []

    if not isinstance(payload, dict):
        return {
            "errors": ["input JSON must contain an object"],
            "warnings": [],
            "manual_review_flags": [],
            "manual_review_required": False,
            "supported_standard_case": False,
            "normalized": {},
        }

    workflow, tax_year = _workflow_year(payload, errors)
    amounts = _validate_money_fields(payload, errors)

    unknown_keys = sorted(set(payload) - KNOWN_PAYLOAD_KEYS)
    if unknown_keys:
        warnings.append(
            "Unknown payload key(s) ignored by the Box 2 scripts (typo?): "
            + ", ".join(unknown_keys)
        )

    if "substantial_interest_pct" not in payload:
        errors.append("substantial_interest_pct is required for Box 2 preparation")
    else:
        try:
            pct = _decimal(payload.get("substantial_interest_pct"), "substantial_interest_pct")
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if pct is not None:
                if pct < 0 or pct > 100:
                    errors.append("substantial_interest_pct must be between 0 and 100")
                elif pct < 5:
                    _add_unique(manual_review_flags, "below_standard_substantial_interest_threshold")
                    warnings.append(
                        "Declared interest is below 5%; confirm whether Box 2 applies."
                    )

    # Presence = a NONZERO amount, matching calculate_box2_tax.py (which tests
    # `> ZERO`): an explicit `disposal_price: 0` must not trigger "not both" or
    # the acquisition-price requirement here while the calculator ignores it.
    zero = Decimal("0")

    def _present(field_name: str) -> bool:
        return amounts.get(field_name, zero) != zero

    if _present("disposal_price") and _present("gross_disposal_price"):
        errors.append("provide either disposal_price or gross_disposal_price, not both")

    disposal_component_names = {
        "disposal_price",
        "gross_disposal_price",
        "acquisition_price",
        "disposal_costs",
    }
    disposal_components_present = {
        name for name in disposal_component_names if _present(name)
    }
    has_any_disposal_price = (
        _present("disposal_price") or _present("gross_disposal_price")
    )
    if disposal_components_present and not has_any_disposal_price:
        errors.append(
            "disposal_price or gross_disposal_price is required when acquisition price "
            "or disposal costs are provided"
        )
    if disposal_components_present and not _present("acquisition_price"):
        errors.append("acquisition_price is required when disposal components are provided")
    if _present("disposal_price") and _present("disposal_costs"):
        warnings.append(
            "disposal_price is treated as the official net transfer price; "
            "disposal_costs are retained for evidence and are not deducted again."
        )

    markers = payload.get("complex_markers") or {}
    if markers and not isinstance(markers, dict):
        errors.append("complex_markers must be an object")
        markers = {}
    for marker, description in COMPLEX_MARKERS.items():
        if _is_truthy_flag(markers.get(marker)) or _is_truthy_flag(payload.get(marker)):
            _add_unique(manual_review_flags, marker)
            warnings.append(f"Manual review required: {description}")

    resident_full_year = payload.get("resident_full_year")
    if resident_full_year is False:
        _add_unique(manual_review_flags, "resident_full_year")
        warnings.append(STANDARD_BOUNDARY_FLAGS["resident_full_year"])

    standard_ab_case = payload.get("standard_ab_case")
    if standard_ab_case is False:
        _add_unique(manual_review_flags, "standard_ab_case")
        warnings.append(STANDARD_BOUNDARY_FLAGS["standard_ab_case"])

    if amounts.get("fictitious_regular_benefit_bv_loan", Decimal("0")) > 0:
        _add_unique(manual_review_flags, "excessive_borrowing_bv_loan")
        warnings.append(
            "Fictitious regular benefit from borrowing above the own-BV threshold "
            "needs review before manual entry."
        )

    if amounts.get("bv_loan_balance", Decimal("0")) > Decimal("500000"):
        _add_unique(manual_review_flags, "excessive_borrowing_check")
        warnings.append(
            "Borrowing from own BV exceeds EUR 500,000 baseline; check whether a "
            "fictitious regular benefit must be included."
        )

    if amounts.get("loss_setoff", Decimal("0")) > 0:
        _add_unique(manual_review_flags, "loss_setoff_manual_review")
        warnings.append("Box 2 loss setoff requires manual review.")

    _validate_partner_allocation(payload, errors, manual_review_flags, warnings)

    supported_standard_case = not manual_review_flags and not errors
    normalized = {
        "workflow": workflow,
        "tax_year": tax_year,
        "amounts": {key: float(_money(value)) for key, value in amounts.items()},
    }

    return {
        "errors": errors,
        "warnings": warnings,
        "manual_review_flags": manual_review_flags,
        "manual_review_required": bool(manual_review_flags),
        "supported_standard_case": supported_standard_case,
        "normalized": normalized,
    }


def validate_json_file(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    return validate_box2_input_payload(data)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if "-h" in args or "--help" in args:
        print("validate_box2_inputs.py — validate a box 2 inputs JSON payload")
        print("Usage: python3 validate_box2_inputs.py input.json")
        return 0
    if len(args) != 1:
        print("Usage: python3 validate_box2_inputs.py input.json", file=sys.stderr)
        return 1

    try:
        result = validate_json_file(Path(args[0]))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
