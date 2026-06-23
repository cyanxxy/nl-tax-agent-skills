#!/usr/bin/env python3
"""Calculate indicative Dutch Box 2 tax for standard preparation workpacks.

This helper is deliberately narrow: it prepares source-backed amounts for
manual Mijn Belastingdienst entry. It does not decide complex substantial
interest positions, sign returns, submit returns, or replace professional
review where losses or special events are present.

Usage:
    python3 calculate_box2_tax.py input.json
    python3 calculate_box2_tax.py --tax-year 2025 --regular-benefits 10000
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
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc


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


def calculate_box2_tax(
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


def _payload_to_calculation_kwargs(payload: dict[str, Any]) -> dict[str, Any]:
    tax_year = payload.get("tax_year")
    if tax_year is None:
        workflow = payload.get("workflow")
        if workflow == "annual_2025":
            tax_year = 2025
        elif workflow == "provisional_2026":
            tax_year = 2026

    return {
        "tax_year": tax_year,
        "regular_benefits": payload.get("regular_benefits", 0),
        "regular_costs": payload.get("regular_costs", 0),
        "disposal_price": payload.get("disposal_price", 0),
        "gross_disposal_price": payload.get("gross_disposal_price", 0),
        "acquisition_price": payload.get("acquisition_price", 0),
        "disposal_costs": payload.get("disposal_costs", 0),
        "disposal_benefit": payload.get("disposal_benefit"),
        "fictitious_regular_benefit_bv_loan": payload.get(
            "fictitious_regular_benefit_bv_loan",
            0,
        ),
        "loss_setoff": payload.get("loss_setoff", 0),
        "dividend_withholding_tax": payload.get("dividend_withholding_tax", 0),
    }


def calculate_from_payload(payload: dict[str, Any]) -> dict:
    """Calculate Box 2 tax and optional partner allocation from a JSON payload."""
    result = calculate_box2_tax(**_payload_to_calculation_kwargs(payload))

    allocation = payload.get("partner_allocation") or payload.get("allocation")
    if allocation:
        if payload.get("full_year_fiscal_partner") is True:
            result["partner_allocation"] = allocate_partner_box2(
                tax_year=result["tax_year"],
                total_taxable_income=result["taxable_income"],
                taxpayer_pct=allocation.get("taxpayer_pct"),
                partner_pct=allocation.get("partner_pct"),
                dividend_withholding_tax=result["dividend_withholding_credit"],
            )
        else:
            # Full-year fiscal-partner status is not confirmed: do NOT emit a
            # computed split. Allocation requires proven eligibility.
            result["partner_allocation_skipped"] = (
                "full_year_fiscal_partner not confirmed; allocation not computed"
            )
            _add_flag(result["manual_review_flags"], "partner_status_unconfirmed")

    return result


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
    parser.add_argument("--tax-year", type=int, choices=sorted(BOX2_RATES))
    parser.add_argument("--regular-benefits", type=float, default=0)
    parser.add_argument("--regular-costs", type=float, default=0)
    parser.add_argument("--disposal-price", type=float, default=0)
    parser.add_argument("--gross-disposal-price", type=float, default=0)
    parser.add_argument("--acquisition-price", type=float, default=0)
    parser.add_argument("--disposal-costs", type=float, default=0)
    parser.add_argument("--disposal-benefit", type=float)
    parser.add_argument("--fictitious-regular-benefit-bv-loan", type=float, default=0)
    parser.add_argument("--loss-setoff", type=float, default=0)
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
                "tax_year": args.tax_year,
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
            if args.taxpayer_pct is not None or args.partner_pct is not None:
                payload["partner_allocation"] = {
                    "taxpayer_pct": args.taxpayer_pct,
                    "partner_pct": args.partner_pct,
                }

        print(json.dumps(calculate_from_payload(payload), indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
