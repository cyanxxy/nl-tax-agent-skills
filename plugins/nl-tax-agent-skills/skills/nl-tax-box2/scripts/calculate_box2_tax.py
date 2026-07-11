#!/usr/bin/env python3
"""Calculate indicative Dutch Box 2 tax for standard preparation workpacks.

This helper is deliberately narrow: it prepares source-backed amounts for
manual Mijn Belastingdienst entry. It does not decide complex substantial
interest positions, sign returns, submit returns, or replace professional
review where losses or special events are present.

Usage:
    python3 calculate_box2_tax.py input.json
    python3 calculate_box2_tax.py --workflow annual_2025 --tax-year 2025 \
        --substantial-interest-pct 10 --resident-full-year \
        --standard-ab-case --regular-benefits 10000 \
        --disposal-benefit 0 --loss-setoff 0
"""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation, ROUND_FLOOR, ROUND_HALF_UP
import json
import sys
from pathlib import Path
from typing import Any


CENT = Decimal("0.01")
EURO = Decimal("1")
ZERO = Decimal("0")

# Box 2 thresholds and rates. These duplicate the canonical knowledge pack so this
# script can act as a deterministic calculator; the knowledge notes are canonical.
# Keep them in sync with the reviewed rule note and bump them in the same commit it
# changes: _shared/knowledge/years/2025/box2/box2-rates.md
# (source bd_box2_rates_2025_2026).
BOX2_RATES: dict[int, dict[str, Decimal | str]] = {
    2025: {
        "workflow": "annual_2025",
        "threshold": Decimal("67804"),
        "lower_rate": Decimal("0.245"),
        "upper_rate": Decimal("0.31"),
    },
    2026: {
        "workflow": "provisional_2026",
        "threshold": Decimal("68843"),
        "lower_rate": Decimal("0.245"),
        "upper_rate": Decimal("0.31"),
    },
}


NON_NEGATIVE_FIELDS = {
    "regular_benefits",
    "regular_costs",
    "disposal_price",
    "gross_disposal_price",
    "acquisition_price",
    "disposal_costs",
    "fictitious_regular_benefit_bv_loan",
    "loss_setoff",
    "dividend_withholding_tax",
}


def _decimal(value: Any, field_name: str) -> Decimal:
    if value is None or value == "":
        return ZERO
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc
    if not result.is_finite():
        # NaN/inf would otherwise raise InvalidOperation deep inside the
        # comparisons/quantize instead of a clean input error.
        raise ValueError(f"{field_name} must be a finite number")
    return result


def _ensure_non_negative(value: Decimal, field_name: str) -> None:
    if value < ZERO:
        raise ValueError(f"{field_name} must be non-negative")


def _money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _whole_euro_tax(value: Decimal) -> Decimal:
    return value.quantize(EURO, rounding=ROUND_FLOOR)


def _out(value: Decimal) -> float:
    return float(_money(value))


def _add_flag(flags: list[str], flag: str) -> None:
    if flag not in flags:
        flags.append(flag)


def _rate_config(tax_year: int) -> dict[str, Decimal | str]:
    try:
        return BOX2_RATES[int(tax_year)]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("tax_year must be 2025 or 2026") from exc


def calculate_bracket_tax(tax_year: int, taxable_income: float | int | Decimal) -> dict:
    """Return bracket split and gross tax for positive Box 2 income."""
    config = _rate_config(tax_year)
    income = _decimal(taxable_income, "taxable_income")
    if income <= ZERO:
        income = ZERO

    threshold = config["threshold"]
    lower_rate = config["lower_rate"]
    upper_rate = config["upper_rate"]
    assert isinstance(threshold, Decimal)
    assert isinstance(lower_rate, Decimal)
    assert isinstance(upper_rate, Decimal)

    lower_income = min(income, threshold)
    upper_income = max(ZERO, income - threshold)
    lower_tax = _whole_euro_tax(lower_income * lower_rate)
    upper_tax = _whole_euro_tax(upper_income * upper_rate)
    gross_tax = lower_tax + upper_tax

    return {
        "threshold": _out(threshold),
        "lower_rate": float(lower_rate),
        "upper_rate": float(upper_rate),
        "lower_bracket_income": _out(lower_income),
        "upper_bracket_income": _out(upper_income),
        "lower_bracket_tax": _out(lower_tax),
        "upper_bracket_tax": _out(upper_tax),
        "gross_tax": _out(gross_tax),
    }


def _build_result(
    tax_year: int,
    taxable_income: Decimal,
    dividend_withholding_tax: Decimal,
    components: dict[str, Decimal],
    manual_review_flags: list[str],
    warnings: list[str] | None = None,
) -> dict:
    taxable_for_tax = max(ZERO, taxable_income)
    bracket_split = calculate_bracket_tax(tax_year, taxable_for_tax)
    gross_tax = _decimal(bracket_split["gross_tax"], "gross_tax")
    credit = _money(dividend_withholding_tax)
    net = _money(gross_tax - credit)

    loss_amount = abs(taxable_income) if taxable_income < ZERO else ZERO
    if loss_amount > ZERO:
        _add_flag(manual_review_flags, "box2_loss")

    if components.get("loss_setoff", ZERO) > ZERO:
        _add_flag(manual_review_flags, "loss_setoff_manual_review")

    if credit > gross_tax:
        _add_flag(manual_review_flags, "withholding_exceeds_gross_tax")

    notes = [
        "Indicative Box 2 preparation calculation only; the official filing "
        "environment makes the binding calculation."
    ]
    if loss_amount > ZERO:
        notes.append(
            "Negative Box 2 income can involve loss carry-back or carry-forward "
            "rules and needs manual review."
        )

    component_output = {key: _out(value) for key, value in components.items()}

    return {
        "tax_year": int(tax_year),
        "workflow": BOX2_RATES[int(tax_year)]["workflow"],
        "taxable_income": _out(taxable_income),
        "gross_tax": _out(gross_tax),
        "dividend_withholding_credit": _out(credit),
        "net_payable_or_refund_indicative": _out(net),
        "bracket_split": bracket_split,
        "components": component_output,
        "loss": {
            "is_loss": loss_amount > ZERO,
            "current_year_loss": _out(loss_amount),
            "loss_setoff_applied": _out(components.get("loss_setoff", ZERO)),
        },
        "manual_review_flags": manual_review_flags,
        "warnings": warnings or [],
        "notes": notes,
    }


def _calculate_box2_tax(
    *,
    tax_year: int,
    regular_benefits: float | int | Decimal = 0,
    regular_costs: float | int | Decimal = 0,
    disposal_price: float | int | Decimal = 0,
    gross_disposal_price: float | int | Decimal = 0,
    acquisition_price: float | int | Decimal = 0,
    disposal_costs: float | int | Decimal = 0,
    disposal_benefit: float | int | Decimal | None = None,
    fictitious_regular_benefit_bv_loan: float | int | Decimal = 0,
    loss_setoff: float | int | Decimal = 0,
    dividend_withholding_tax: float | int | Decimal = 0,
) -> dict:
    """Calculate taxable Box 2 income and indicative tax.

    `disposal_price` is the official net transfer/disposal price after sale
    costs. If only gross sale proceeds are available, pass
    `gross_disposal_price`; the helper subtracts disposal costs once to derive
    the net transfer price. An explicit disposal_benefit overrides both paths.
    """
    _rate_config(tax_year)

    amounts = {
        "regular_benefits": _decimal(regular_benefits, "regular_benefits"),
        "regular_costs": _decimal(regular_costs, "regular_costs"),
        "disposal_price": _decimal(disposal_price, "disposal_price"),
        "gross_disposal_price": _decimal(
            gross_disposal_price,
            "gross_disposal_price",
        ),
        "acquisition_price": _decimal(acquisition_price, "acquisition_price"),
        "disposal_costs": _decimal(disposal_costs, "disposal_costs"),
        "fictitious_regular_benefit_bv_loan": _decimal(
            fictitious_regular_benefit_bv_loan,
            "fictitious_regular_benefit_bv_loan",
        ),
        "loss_setoff": _decimal(loss_setoff, "loss_setoff"),
        "dividend_withholding_tax": _decimal(
            dividend_withholding_tax,
            "dividend_withholding_tax",
        ),
    }
    for field_name in NON_NEGATIVE_FIELDS:
        _ensure_non_negative(amounts[field_name], field_name)

    explicit_disposal_benefit = (
        _decimal(disposal_benefit, "disposal_benefit")
        if disposal_benefit is not None
        else None
    )

    if amounts["disposal_price"] > ZERO and amounts["gross_disposal_price"] > ZERO:
        raise ValueError("provide either disposal_price or gross_disposal_price, not both")

    disposal_component_present = any(
        amounts[name] != ZERO
        for name in (
            "disposal_price",
            "gross_disposal_price",
            "acquisition_price",
            "disposal_costs",
        )
    )
    warnings: list[str] = []
    if explicit_disposal_benefit is not None:
        # Keep the components block coherent when a gross price accompanies an
        # explicit benefit: report the derived net price, not a misleading 0.
        if amounts["gross_disposal_price"] > ZERO:
            net_disposal_price = (
                amounts["gross_disposal_price"] - amounts["disposal_costs"]
            )
        else:
            net_disposal_price = amounts["disposal_price"]
        computed_disposal_benefit = explicit_disposal_benefit
    elif amounts["gross_disposal_price"] > ZERO:
        net_disposal_price = amounts["gross_disposal_price"] - amounts["disposal_costs"]
        computed_disposal_benefit = net_disposal_price - amounts["acquisition_price"]
    elif disposal_component_present:
        net_disposal_price = amounts["disposal_price"]
        computed_disposal_benefit = (
            net_disposal_price
            - amounts["acquisition_price"]
        )
        if amounts["disposal_price"] > ZERO and amounts["disposal_costs"] > ZERO:
            warnings.append(
                "disposal_price is treated as the official net transfer price; "
                "disposal_costs are retained for evidence and are not deducted again."
            )
    else:
        net_disposal_price = ZERO
        computed_disposal_benefit = ZERO

    regular_net = amounts["regular_benefits"] - amounts["regular_costs"]
    taxable_income = (
        regular_net
        + computed_disposal_benefit
        + amounts["fictitious_regular_benefit_bv_loan"]
        - amounts["loss_setoff"]
    )

    manual_review_flags: list[str] = []
    if computed_disposal_benefit < ZERO:
        _add_flag(manual_review_flags, "disposal_loss")
    if amounts["fictitious_regular_benefit_bv_loan"] > ZERO:
        _add_flag(manual_review_flags, "excessive_borrowing_bv_loan")
        warnings.append(
            "Fictitious regular benefit for borrowing from own BV needs manual "
            "review against the excessive-borrowing rules."
        )

    components = {
        "regular_benefits": amounts["regular_benefits"],
        "regular_costs": amounts["regular_costs"],
        "regular_net": regular_net,
        "disposal_price": amounts["disposal_price"],
        "gross_disposal_price": amounts["gross_disposal_price"],
        "net_disposal_price": net_disposal_price,
        "acquisition_price": amounts["acquisition_price"],
        "disposal_costs": amounts["disposal_costs"],
        "disposal_benefit": computed_disposal_benefit,
        "fictitious_regular_benefit_bv_loan": amounts[
            "fictitious_regular_benefit_bv_loan"
        ],
        "loss_setoff": amounts["loss_setoff"],
    }

    return _build_result(
        int(tax_year),
        taxable_income,
        amounts["dividend_withholding_tax"],
        components,
        manual_review_flags,
        warnings,
    )


def _validate_percentage(value: float | int | Decimal, field_name: str) -> Decimal:
    pct = _decimal(value, field_name)
    if pct < ZERO or pct > Decimal("100"):
        raise ValueError(f"{field_name} must be between 0 and 100")
    return pct


def allocate_partner_box2(
    *,
    tax_year: int,
    total_taxable_income: float | int | Decimal,
    taxpayer_pct: float | int | Decimal,
    partner_pct: float | int | Decimal,
    dividend_withholding_tax: float | int | Decimal = 0,
) -> dict:
    """Allocate joint Box 2 taxable income between full-year fiscal partners.

    The indicative split applies the SAME percentages to both the joint taxable
    income and the withheld dividend tax (coupled, proportional allocation). Any
    non-proportional dividend-tax allocation (for example, splitting the withheld
    dividend tax on a different basis than the income) is a manual-review item and
    is not computed here.
    """
    _rate_config(tax_year)
    taxpayer_share = _validate_percentage(taxpayer_pct, "taxpayer_pct")
    partner_share = _validate_percentage(partner_pct, "partner_pct")
    if _money(taxpayer_share + partner_share) != Decimal("100.00"):
        raise ValueError("taxpayer_pct and partner_pct must total 100")

    total_income = _decimal(total_taxable_income, "total_taxable_income")
    withholding = _decimal(dividend_withholding_tax, "dividend_withholding_tax")
    _ensure_non_negative(withholding, "dividend_withholding_tax")

    taxpayer_income = total_income * taxpayer_share / Decimal("100")
    partner_income = total_income * partner_share / Decimal("100")
    taxpayer_credit = withholding * taxpayer_share / Decimal("100")
    partner_credit = withholding * partner_share / Decimal("100")

    taxpayer_result = _build_result(
        int(tax_year),
        taxpayer_income,
        taxpayer_credit,
        {
            "allocated_from_joint_taxable_income": total_income,
            "allocated_share_pct": taxpayer_share,
            "loss_setoff": ZERO,
        },
        [],
    )
    partner_result = _build_result(
        int(tax_year),
        partner_income,
        partner_credit,
        {
            "allocated_from_joint_taxable_income": total_income,
            "allocated_share_pct": partner_share,
            "loss_setoff": ZERO,
        },
        [],
    )

    return {
        "tax_year": int(tax_year),
        "allocation": {
            "taxpayer_pct": _out(taxpayer_share),
            "partner_pct": _out(partner_share),
            "total_taxable_income": _out(total_income),
            "dividend_withholding_tax": _out(withholding),
        },
        "taxpayer": taxpayer_result,
        "partner": partner_result,
    }


SUPPORTED_WORKFLOWS = {
    "annual_2025": 2025,
    "provisional_2026": 2026,
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

# Payload keys accepted by the single validated public entrypoint.
_KNOWN_PAYLOAD_KEYS = {
    "tax_year",
    "workflow",
    "regular_benefits",
    "regular_costs",
    "disposal_price",
    "gross_disposal_price",
    "acquisition_price",
    "disposal_costs",
    "disposal_benefit",
    "fictitious_regular_benefit_bv_loan",
    "loss_setoff",
    "loss_setoff_reviewed",
    "loss_setoff_source",
    "dividend_withholding_tax",
    "bv_loan_balance",
    "substantial_interest_pct",
    "partner_allocation",
    "allocation",
    "full_year_fiscal_partner",
    "complex_markers",
    "resident_full_year",
    "standard_ab_case",
    "valuation_dispute",
    "emigration",
    "death",
    "restructurings",
    "treaty_nonresident_issues",
    "informal_capital",
    "non_arm_length_transfers",
    "corporate_tax_heavy_dga_cases",
    "inherited_gifted_ab",
    "fictive_disposal",
    "excessive_borrowing_uncertainty",
}


def _add_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def _require_boolean(
    payload: dict[str, Any],
    field_name: str,
    errors: list[str],
) -> bool | None:
    if field_name not in payload:
        errors.append(f"{field_name} is required and must be a boolean")
        return None
    value = payload[field_name]
    if type(value) is not bool:
        errors.append(f"{field_name} must be a boolean")
        return None
    return value


def _optional_boolean(
    payload: dict[str, Any],
    field_name: str,
    errors: list[str],
) -> bool | None:
    if field_name not in payload:
        return None
    value = payload[field_name]
    if type(value) is not bool:
        errors.append(f"{field_name} must be a boolean")
        return None
    return value


def _normalize_amount(
    payload: dict[str, Any],
    field_name: str,
    errors: list[str],
    *,
    required: bool = False,
    allow_negative: bool = False,
) -> Decimal | None:
    if field_name not in payload or payload[field_name] in (None, ""):
        if required:
            errors.append(f"{field_name} is required")
        return None
    try:
        value = _decimal(payload[field_name], field_name)
    except ValueError as exc:
        errors.append(str(exc))
        return None
    if not allow_negative and value < ZERO:
        errors.append(f"{field_name} must be non-negative")
        return None
    return value


def _validate_allocation(
    payload: dict[str, Any],
    errors: list[str],
    warnings: list[str],
    manual_review_flags: list[str],
) -> dict[str, float] | None:
    allocation = payload.get("partner_allocation") or payload.get("allocation")
    if allocation is None:
        return None
    if not isinstance(allocation, dict):
        errors.append("partner_allocation must be an object")
        return None

    if "taxpayer_pct" not in allocation or "partner_pct" not in allocation:
        errors.append("partner_allocation requires taxpayer_pct and partner_pct")
        return None

    try:
        taxpayer_pct = _validate_percentage(
            allocation.get("taxpayer_pct"), "taxpayer_pct"
        )
        partner_pct = _validate_percentage(
            allocation.get("partner_pct"), "partner_pct"
        )
    except ValueError as exc:
        errors.append(str(exc))
        return None
    if _money(taxpayer_pct + partner_pct) != Decimal("100.00"):
        errors.append("partner allocation percentages must total 100")
        return None

    partner_status = _optional_boolean(payload, "full_year_fiscal_partner", errors)
    if partner_status is not True:
        _add_unique(manual_review_flags, "partner_status_unconfirmed")
        warnings.append(
            "Box 2 allocation requires confirmed full-year fiscal-partner status."
        )
    return {
        "taxpayer_pct": float(taxpayer_pct),
        "partner_pct": float(partner_pct),
    }


def validate_and_normalize_payload(
    payload: dict[str, Any],
) -> tuple[list[str], list[str], dict[str, Any]]:
    """Validate the complete public Box 2 payload before any calculation."""
    errors: list[str] = []
    warnings: list[str] = []
    manual_review_flags: list[str] = []
    if not isinstance(payload, dict):
        return ["input JSON must contain an object"], [], {
            "manual_review_required": False,
            "manual_review_flags": [],
        }

    unknown = sorted(set(payload) - _KNOWN_PAYLOAD_KEYS)
    if unknown:
        errors.append("Unknown payload key(s): " + ", ".join(unknown))

    workflow = payload.get("workflow")
    if not isinstance(workflow, str) or workflow not in SUPPORTED_WORKFLOWS:
        errors.append("workflow is required: annual_2025 or provisional_2026")
        workflow = None

    tax_year = payload.get("tax_year")
    if type(tax_year) is not int or tax_year not in BOX2_RATES:
        errors.append("tax_year is required and must be 2025 or 2026")
        tax_year = None
    if workflow is not None and tax_year is not None:
        expected_year = SUPPORTED_WORKFLOWS[workflow]
        if tax_year != expected_year:
            errors.append(f"{workflow} requires tax_year {expected_year}")

    resident_full_year = _require_boolean(payload, "resident_full_year", errors)
    standard_ab_case = _require_boolean(payload, "standard_ab_case", errors)
    if resident_full_year is False:
        errors.append("resident_full_year must be true for the standard Box 2 helper")
    if standard_ab_case is False:
        errors.append("standard_ab_case must be true for the standard Box 2 helper")

    substantial_interest_pct = _normalize_amount(
        payload, "substantial_interest_pct", errors, required=True
    )
    if substantial_interest_pct is not None:
        if substantial_interest_pct > Decimal("100"):
            errors.append("substantial_interest_pct must be between 0 and 100")
        elif substantial_interest_pct < Decimal("5"):
            errors.append(
                "substantial_interest_pct below 5 requires manual Box 2 review"
            )

    amounts: dict[str, Decimal] = {}
    for field_name in NON_NEGATIVE_FIELDS:
        value = _normalize_amount(
            payload,
            field_name,
            errors,
            required=field_name in {"regular_benefits", "loss_setoff"},
        )
        if value is not None:
            amounts[field_name] = value
    disposal_benefit = _normalize_amount(
        payload,
        "disposal_benefit",
        errors,
        required=True,
        allow_negative=True,
    )
    if disposal_benefit is not None:
        amounts["disposal_benefit"] = disposal_benefit
    bv_loan_balance = _normalize_amount(payload, "bv_loan_balance", errors)
    if bv_loan_balance is not None:
        amounts["bv_loan_balance"] = bv_loan_balance

    def present(field_name: str) -> bool:
        return amounts.get(field_name, ZERO) != ZERO

    if present("disposal_price") and present("gross_disposal_price"):
        errors.append("provide either disposal_price or gross_disposal_price, not both")
    disposal_components_present = any(
        present(name)
        for name in (
            "disposal_price",
            "gross_disposal_price",
            "acquisition_price",
            "disposal_costs",
        )
    )
    if disposal_components_present and not (
        present("disposal_price") or present("gross_disposal_price")
    ):
        errors.append(
            "disposal_price or gross_disposal_price is required when acquisition "
            "price or disposal costs are provided"
        )
    if disposal_components_present and not present("acquisition_price"):
        errors.append("acquisition_price is required when disposal components are provided")
    if present("disposal_price") and present("disposal_costs"):
        warnings.append(
            "disposal_price is treated as the official net transfer price; "
            "disposal_costs are retained for evidence and are not deducted again."
        )

    markers = payload.get("complex_markers", {})
    if not isinstance(markers, dict):
        errors.append("complex_markers must be an object")
        markers = {}
    for marker, description in COMPLEX_MARKERS.items():
        nested = markers.get(marker)
        direct = payload.get(marker)
        for value in (nested, direct):
            if value is not None and type(value) is not bool:
                errors.append(f"{marker} must be a boolean")
                break
        if nested is True or direct is True:
            _add_unique(manual_review_flags, marker)
            warnings.append(f"Manual review required: {description}")

    if amounts.get("fictitious_regular_benefit_bv_loan", ZERO) > ZERO:
        _add_unique(manual_review_flags, "excessive_borrowing_bv_loan")
        warnings.append(
            "Fictitious regular benefit from own-BV borrowing requires manual review."
        )
    if amounts.get("bv_loan_balance", ZERO) > Decimal("500000"):
        _add_unique(manual_review_flags, "excessive_borrowing_check")
        warnings.append("Own-BV borrowing above EUR 500,000 requires manual review.")

    loss_setoff = amounts.get("loss_setoff", ZERO)
    loss_reviewed = _optional_boolean(payload, "loss_setoff_reviewed", errors)
    loss_source = payload.get("loss_setoff_source")
    if loss_source is not None and (
        not isinstance(loss_source, str) or not loss_source.strip()
    ):
        errors.append("loss_setoff_source must be a non-empty string")
    if loss_setoff > ZERO:
        if loss_reviewed is not True or not isinstance(loss_source, str) or not loss_source.strip():
            _add_unique(manual_review_flags, "loss_setoff_manual_review")
            warnings.append(
                "Box 2 loss setoff needs loss_setoff_reviewed: true and a "
                "loss_setoff_source before calculation."
            )

    allocation = _validate_allocation(
        payload, errors, warnings, manual_review_flags
    )
    manual_review_required = bool(manual_review_flags)
    normalized = {
        "workflow": workflow,
        "tax_year": tax_year,
        "substantial_interest_pct": (
            float(substantial_interest_pct)
            if substantial_interest_pct is not None
            else None
        ),
        "resident_full_year": resident_full_year,
        "standard_ab_case": standard_ab_case,
        "amounts": {key: float(_money(value)) for key, value in amounts.items()},
        "partner_allocation": allocation,
        "full_year_fiscal_partner": payload.get("full_year_fiscal_partner"),
        "loss_setoff_reviewed": loss_reviewed,
        "loss_setoff_source": loss_source,
        "manual_review_flags": manual_review_flags,
        "manual_review_required": manual_review_required,
    }
    return errors, warnings, normalized


def _calculate_validated(normalized: dict[str, Any]) -> dict:
    amounts = normalized["amounts"]
    result = _calculate_box2_tax(
        tax_year=normalized["tax_year"],
        regular_benefits=amounts.get("regular_benefits", 0),
        regular_costs=amounts.get("regular_costs", 0),
        disposal_price=amounts.get("disposal_price", 0),
        gross_disposal_price=amounts.get("gross_disposal_price", 0),
        acquisition_price=amounts.get("acquisition_price", 0),
        disposal_costs=amounts.get("disposal_costs", 0),
        disposal_benefit=amounts.get("disposal_benefit"),
        fictitious_regular_benefit_bv_loan=amounts.get(
            "fictitious_regular_benefit_bv_loan", 0
        ),
        loss_setoff=amounts.get("loss_setoff", 0),
        dividend_withholding_tax=amounts.get("dividend_withholding_tax", 0),
    )
    if normalized.get("loss_setoff_reviewed") is True:
        result["manual_review_flags"] = [
            flag
            for flag in result["manual_review_flags"]
            if flag != "loss_setoff_manual_review"
        ]
    allocation = normalized.get("partner_allocation")
    if allocation is not None:
        result["partner_allocation"] = allocate_partner_box2(
            tax_year=result["tax_year"],
            total_taxable_income=result["taxable_income"],
            taxpayer_pct=allocation["taxpayer_pct"],
            partner_pct=allocation["partner_pct"],
            dividend_withholding_tax=result["dividend_withholding_credit"],
        )
    return result


def calculate_from_payload(payload: dict[str, Any]) -> dict:
    """Validate, normalize, and optionally calculate a Box 2 JSON payload."""
    errors, warnings, normalized = validate_and_normalize_payload(payload)
    if errors or normalized.get("manual_review_required"):
        return {
            "errors": errors,
            "warnings": warnings,
            "normalized": normalized,
            "result": None,
            "check_performed_by": "checked_by_script",
        }
    return {
        "errors": [],
        "warnings": warnings,
        "normalized": normalized,
        "result": _calculate_validated(normalized),
        "check_performed_by": "checked_by_script",
    }


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("input JSON must contain an object")
    return data


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate indicative Box 2 tax for annual 2025 or provisional 2026."
    )
    parser.add_argument("input_path", nargs="?", help="Optional JSON input path")
    parser.add_argument("--workflow", choices=sorted(SUPPORTED_WORKFLOWS))
    parser.add_argument("--tax-year", type=int, choices=sorted(BOX2_RATES))
    parser.add_argument("--substantial-interest-pct", type=float)
    parser.add_argument("--resident-full-year", action="store_true", default=None)
    parser.add_argument("--standard-ab-case", action="store_true", default=None)
    parser.add_argument("--regular-benefits", type=float, default=0)
    parser.add_argument("--regular-costs", type=float, default=0)
    parser.add_argument("--disposal-price", type=float, default=0)
    parser.add_argument("--gross-disposal-price", type=float, default=0)
    parser.add_argument("--acquisition-price", type=float, default=0)
    parser.add_argument("--disposal-costs", type=float, default=0)
    parser.add_argument("--disposal-benefit", type=float)
    parser.add_argument("--fictitious-regular-benefit-bv-loan", type=float, default=0)
    parser.add_argument("--loss-setoff", type=float, default=0)
    parser.add_argument("--loss-setoff-reviewed", action="store_true", default=None)
    parser.add_argument("--loss-setoff-source")
    parser.add_argument("--dividend-withholding-tax", type=float, default=0)
    parser.add_argument("--taxpayer-pct", type=float)
    parser.add_argument("--partner-pct", type=float)
    parser.add_argument(
        "--full-year-fiscal-partner",
        action="store_true",
        help=(
            "Confirm full-year (or elected full-year) fiscal partnership. Required "
            "before a partner allocation is actually computed; without it a supplied "
            "--taxpayer-pct/--partner-pct split is skipped and flagged for review."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if args.input_path:
            payload = _load_json(Path(args.input_path))
        else:
            if args.tax_year is None:
                raise ValueError("--tax-year is required when no input JSON is provided")
            payload = {
                "workflow": args.workflow,
                "tax_year": args.tax_year,
                "substantial_interest_pct": args.substantial_interest_pct,
                "resident_full_year": args.resident_full_year,
                "standard_ab_case": args.standard_ab_case,
                "regular_benefits": args.regular_benefits,
                "regular_costs": args.regular_costs,
                "disposal_price": args.disposal_price,
                "gross_disposal_price": args.gross_disposal_price,
                "acquisition_price": args.acquisition_price,
                "disposal_costs": args.disposal_costs,
                "disposal_benefit": args.disposal_benefit,
                "fictitious_regular_benefit_bv_loan": (
                    args.fictitious_regular_benefit_bv_loan
                ),
                "loss_setoff": args.loss_setoff,
                "dividend_withholding_tax": args.dividend_withholding_tax,
                "full_year_fiscal_partner": args.full_year_fiscal_partner,
            }
            if args.loss_setoff_reviewed is not None:
                payload["loss_setoff_reviewed"] = args.loss_setoff_reviewed
            if args.loss_setoff_source is not None:
                payload["loss_setoff_source"] = args.loss_setoff_source
            if args.taxpayer_pct is not None or args.partner_pct is not None:
                # Derive the missing side so `--taxpayer-pct 60` alone works
                # instead of failing "must total 100" via a None->0 coercion.
                taxpayer_pct = args.taxpayer_pct
                partner_pct = args.partner_pct
                if partner_pct is None and taxpayer_pct is not None:
                    partner_pct = 100 - taxpayer_pct
                elif taxpayer_pct is None and partner_pct is not None:
                    taxpayer_pct = 100 - partner_pct
                payload["partner_allocation"] = {
                    "taxpayer_pct": taxpayer_pct,
                    "partner_pct": partner_pct,
                }

        output = calculate_from_payload(payload)
        print(json.dumps(output, indent=2, sort_keys=True))
        return 1 if output["errors"] or output["result"] is None else 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
