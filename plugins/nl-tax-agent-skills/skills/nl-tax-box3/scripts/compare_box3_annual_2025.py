#!/usr/bin/env python3
"""
compare_box3_annual_2025.py

Compare fictitious vs actual return for box 3 annual 2025.
NOTE: This script is ONLY for the annual 2025 return, NOT for provisional assessments.

Usage:
    python3 compare_box3_annual_2025.py \\
        --rows-json '<already-classified JSON rows>' \\
        --actual_return <amount> \\
        [--heffingsvrij <amount>] \\
        [--has_partner] \\
        [--allocation-pct <0-100>]

All monetary amounts in EUR.

Output: JSON with the official Belastingdienst step fields:
        belastbaar_rendement, rendementsgrondslag,
        grondslag_sparen_en_beleggen, aandeel_in_rendementsgrondslag,
        box3_inkomen, and box3_belasting.
"""

import argparse
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
import json
import math


ACCEPTED_ROW_CATEGORIES = (
    "banktegoeden",
    "overige_bezittingen",
    "schulden",
)


def normalize_classified_rows(rows):
    """Total explicit, source-backed rows without classifying their descriptions."""
    if not isinstance(rows, list):
        raise ValueError("rows must be a list of already-classified mappings")

    totals = {category: Decimal("0") for category in ACCEPTED_ROW_CATEGORIES}
    accepted_rows = []
    rejected_rows = []
    for index, raw_row in enumerate(rows):
        if not isinstance(raw_row, dict):
            rejected_rows.append(
                {
                    "id": f"row-{index + 1}",
                    "row": raw_row,
                    "rejection_reasons": ["row must be a mapping"],
                }
            )
            continue

        row = dict(raw_row)
        reasons = []
        category = row.get("category")
        if category not in ACCEPTED_ROW_CATEGORIES:
            reasons.append(
                "category must be banktegoeden, overige_bezittingen, or schulden"
            )
        if row.get("status") != "accepted":
            reasons.append("status must be accepted")
        provenance = row.get("provenance")
        if not isinstance(provenance, str) or not provenance.strip():
            reasons.append("provenance is required")
        try:
            if isinstance(row.get("value"), bool):
                raise ValueError
            value = Decimal(str(row.get("value")))
            if not value.is_finite() or value < 0:
                raise ValueError
        except (ValueError, TypeError, ArithmeticError):
            reasons.append("value must be a finite non-negative number")
            value = None

        normalized_value = None
        if value is not None:
            normalized_value = float(value)
            if not math.isfinite(normalized_value):
                reasons.append("value must remain finite after normalization")
        candidate_total = None
        if (
            category in ACCEPTED_ROW_CATEGORIES
            and value is not None
            and normalized_value is not None
            and math.isfinite(normalized_value)
        ):
            candidate_total = totals[category] + value
            if not math.isfinite(float(candidate_total)):
                reasons.append("category total must remain finite after normalization")

        if reasons:
            row["rejection_reasons"] = reasons
            rejected_rows.append(row)
            continue

        normalized = {**row, "value": normalized_value}
        accepted_rows.append(normalized)
        totals[category] = candidate_total

    return {
        "trusted_totals": {key: float(value) for key, value in totals.items()},
        "accepted_rows": accepted_rows,
        "rejected_rows": rejected_rows,
        "check_performed_by": "checked_by_script",
    }


def _require_finite_non_negative(name, value):
    """Reject NaN/Inf and negative amounts before any arithmetic runs."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if value < 0:
        raise ValueError(f"{name} must not be negative")


def _require_finite(name, value):
    """Reject NaN/Inf but allow negative values (e.g. actual_return)."""
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")


# 2025 annual box 3 fictitious return percentages and thresholds.
#
# These values duplicate the canonical knowledge pack so this optional mechanical
# arithmetic check can run offline. The knowledge notes are canonical; keep these
# in sync with the reviewed rule note and bump them in the same commit it changes:
#   _shared/knowledge/years/2025/box3/fictitious.md (source bd_box3_2025_calc).
# Decimal constants: all money math below runs in Decimal end-to-end so that
# rounding happens exactly once per output figure (no binary-float drift).
PERC_BANKTEGOEDEN = Decimal("0.0137")
PERC_OVERIGE_BEZITTINGEN = Decimal("0.0588")
PERC_SCHULDEN = Decimal("0.0270")

TAX_RATE = Decimal("0.36")
HEFFINGSVRIJ_PER_PERSON = 57_684
SCHULDEN_DREMPEL_PER_PERSON = 3_800


def nearest_euro(value):
    # ``quantize(Decimal("1"))`` uses the ambient Decimal precision and raises
    # InvalidOperation for otherwise finite values such as 1e308. Converting an
    # integral Decimal is precision-independent and preserves the same HALF_UP
    # whole-euro rule.
    return int(Decimal(str(value)).to_integral_value(rounding=ROUND_HALF_UP))


def floor_euro(value):
    return int(Decimal(str(value)).to_integral_value(rounding=ROUND_FLOOR))


def aandeel_percentage(grondslag_sparen_en_beleggen, rendementsgrondslag):
    """Return the two-decimal percentage used in Belastingdienst examples.

    The official text says to round the percentage, but the published 2025
    examples display 82.45% for 271,116 / 328,800 * 100 and 32.65% for
    108,616 / 332,600 * 100. Truncating toward zero matches those examples.
    """
    if rendementsgrondslag <= 0 or grondslag_sparen_en_beleggen <= 0:
        return 0.0
    percentage = (
        Decimal(str(grondslag_sparen_en_beleggen))
        / Decimal(str(rendementsgrondslag))
        * Decimal("100")
    )
    return float(percentage.quantize(Decimal("0.01"), rounding=ROUND_FLOOR))


def validate_allocation_pct(allocation_pct):
    if isinstance(allocation_pct, bool):
        raise ValueError("allocation_pct must be a finite number between 0 and 100")
    try:
        normalized = Decimal(str(allocation_pct))
    except (ArithmeticError, TypeError, ValueError) as exc:
        raise ValueError(
            "allocation_pct must be a finite number between 0 and 100"
        ) from exc
    if not normalized.is_finite():
        raise ValueError("allocation_pct must be a finite number between 0 and 100")
    if normalized < 0 or normalized > 100:
        raise ValueError("allocation_pct must be between 0 and 100")
    return normalized


def allocated_amount(total, has_partner, allocation_pct):
    allocation_pct = validate_allocation_pct(allocation_pct)
    if not has_partner and allocation_pct != Decimal("100"):
        raise ValueError("allocation_pct can only differ from 100 when has_partner is true")
    total = Decimal(str(total))
    if not has_partner:
        return total
    return total * allocation_pct / Decimal("100")


def calculate_fictitious_box3(
    banktegoeden,
    overige,
    schulden,
    heffingsvrij,
    has_partner,
    allocation_pct=100.0,
    partner_full_year_confirmed=False,
):
    """Calculate fictitious box 3 income using the official step model."""
    _require_finite_non_negative("banktegoeden", banktegoeden)
    _require_finite_non_negative("overige", overige)
    _require_finite_non_negative("schulden", schulden)
    _require_finite_non_negative("heffingsvrij", heffingsvrij)
    allocation_pct = validate_allocation_pct(allocation_pct)
    if has_partner and not partner_full_year_confirmed:
        raise ValueError(
            "has_partner requires --partner-full-year-confirmed "
            "(full-year / elected-full-year fiscal partnership) before doubling "
            "the allowance and debt threshold."
        )
    banktegoeden = Decimal(str(banktegoeden))
    overige = Decimal(str(overige))
    schulden = Decimal(str(schulden))
    heffingsvrij = Decimal(str(heffingsvrij))

    drempel = SCHULDEN_DREMPEL_PER_PERSON * (2 if has_partner else 1)
    aftrekbare_schulden = max(Decimal("0"), schulden - drempel)
    total_assets = banktegoeden + overige

    rendement_bank = banktegoeden * PERC_BANKTEGOEDEN
    rendement_overige = overige * PERC_OVERIGE_BEZITTINGEN
    rendement_schulden = aftrekbare_schulden * PERC_SCHULDEN
    belastbaar_rendement = rendement_bank + rendement_overige - rendement_schulden

    rendementsgrondslag = total_assets - aftrekbare_schulden
    hvv = heffingsvrij if heffingsvrij > 0 else Decimal(
        HEFFINGSVRIJ_PER_PERSON * (2 if has_partner else 1)
    )
    grondslag_sparen_en_beleggen = max(Decimal("0"), rendementsgrondslag - hvv)
    allocated_grondslag = allocated_amount(
        grondslag_sparen_en_beleggen,
        has_partner,
        allocation_pct,
    )

    aandeel_pct = aandeel_percentage(allocated_grondslag, rendementsgrondslag)
    aandeel_fraction = Decimal(str(aandeel_pct)) / Decimal("100")

    belastbaar_rendement_eur = nearest_euro(belastbaar_rendement)
    box3_inkomen = max(0, floor_euro(belastbaar_rendement_eur * aandeel_fraction))
    box3_belasting = floor_euro(box3_inkomen * TAX_RATE)

    result = {
        "belastbaar_rendement": belastbaar_rendement_eur,
        "rendementsgrondslag": nearest_euro(rendementsgrondslag),
        "grondslag_sparen_en_beleggen": nearest_euro(grondslag_sparen_en_beleggen),
        "allocated_grondslag_sparen_en_beleggen": nearest_euro(allocated_grondslag),
        "aandeel_in_rendementsgrondslag": aandeel_pct,
        "box3_inkomen": box3_inkomen,
        "box3_belasting": box3_belasting,
        "details": {
            "banktegoeden": nearest_euro(banktegoeden),
            "overige_bezittingen": nearest_euro(overige),
            "schulden": nearest_euro(schulden),
            "schulden_drempel": nearest_euro(drempel),
            "aftrekbare_schulden": nearest_euro(aftrekbare_schulden),
            "heffingsvrij_vermogen": nearest_euro(hvv),
            "rendement_banktegoeden": nearest_euro(rendement_bank),
            "rendement_overige_bezittingen": nearest_euro(rendement_overige),
            "rendement_schulden": nearest_euro(rendement_schulden),
        },
    }
    if has_partner:
        result["partner_allocation_pct"] = float(allocation_pct)
        result["partner_eligibility_note"] = (
            "Doubling of the heffingsvrij vermogen and the schulden drempel "
            "assumes a confirmed full-year (or elected full-year) fiscal "
            "partnership. If the partnership did not last the full year and "
            "full-year partnership was not elected, the doubled allowance and "
            "threshold do not apply."
        )
    return result


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Compare fictitious vs actual return for box 3 annual 2025. "
            "NOTE: ONLY for annual 2025 return, NOT for provisional assessments."
        )
    )
    parser.add_argument(
        "--rows-json",
        required=True,
        help=(
            "JSON list of already-classified rows. Each row needs category, "
            "status, value, and provenance. Descriptions are never classified."
        ),
    )
    parser.add_argument("--heffingsvrij", type=float, default=0,
                        help=(
                            "Heffingsvrij vermogen in EUR (default: 57684 per "
                            "person). 0 means 'use the statutory default'; an "
                            "explicit zero allowance cannot be expressed."
                        ))
    parser.add_argument("--actual_return", type=float, required=True,
                        help="Total actual return in EUR after applying only permitted components")
    parser.add_argument("--has_partner", action="store_true",
                        help="Whether taxpayer has a fiscal partner")
    parser.add_argument("--partner-full-year-confirmed", action="store_true",
                        help=(
                            "Confirm a full-year (or elected full-year) fiscal "
                            "partnership. Required with --has_partner before the "
                            "allowance and debt threshold are doubled."
                        ))
    parser.add_argument("--allocation-pct", type=float, default=100.0,
                        help=(
                            "For fiscal partners: taxpayer's share of the "
                            "joint grondslag sparen en beleggen. Default 100."
                        ))
    return parser


def compare_tax_methods(fictitious, actual_return_allocated):
    actual_return_for_tax = max(Decimal("0"), Decimal(str(actual_return_allocated)))
    actual_return_for_tax_eur = floor_euro(actual_return_for_tax)
    tax_at_actual = floor_euro(actual_return_for_tax_eur * TAX_RATE)
    tax_at_fictitious = fictitious["box3_belasting"]

    if tax_at_actual < tax_at_fictitious:
        favorable = "actual_return"
        savings = tax_at_fictitious - tax_at_actual
    elif tax_at_fictitious < tax_at_actual:
        favorable = "fictitious_return"
        savings = tax_at_actual - tax_at_fictitious
    else:
        favorable = "equal"
        savings = 0

    return {
        "actual_return_for_tax": actual_return_for_tax_eur,
        "tax_at_fictitious": tax_at_fictitious,
        "tax_at_actual": tax_at_actual,
        "favorable_method": favorable,
        "tax_savings_from_favorable": savings,
    }


def build_output(args, fictitious, actual_return_allocated):
    comparison = compare_tax_methods(fictitious, actual_return_allocated)
    return {
        "assessment_type": "annual_2025",
        **fictitious,
        "fictitious_return": fictitious["box3_inkomen"],
        "actual_return_reported": nearest_euro(args.actual_return),
        "actual_return_allocated": nearest_euro(actual_return_allocated),
        **comparison,
        "tax_rate": float(TAX_RATE),
        "percentages_used": {
            "banktegoeden": float(PERC_BANKTEGOEDEN),
            "overige_bezittingen": float(PERC_OVERIGE_BEZITTINGEN),
            "schulden": float(PERC_SCHULDEN),
        },
        "note": (
            "Actual return is set to EUR 0 for tax comparison if the allocated amount is negative. "
            "For fiscal partners, actual return follows the same allocation percentage as the "
            "grondslag sparen en beleggen. "
            "Displayed amounts use this helper's documented whole-euro working convention. "
            "The official filing environment makes the binding calculation."
        ),
    }


def run(args):
    _require_finite("actual_return", args.actual_return)
    try:
        rows = json.loads(args.rows_json)
    except json.JSONDecodeError as exc:
        raise ValueError(f"rows_json must contain valid JSON: {exc.msg}") from exc
    row_check = normalize_classified_rows(rows)
    if row_check["rejected_rows"]:
        return {
            "assessment_type": "annual_2025",
            **row_check,
            "manual_review_required": True,
            "result": None,
            "note": (
                "Resolve every rejected/manual-review row before running "
                "annual box 3 arithmetic."
            ),
        }
    totals = row_check["trusted_totals"]
    fictitious = calculate_fictitious_box3(
        banktegoeden=totals["banktegoeden"],
        overige=totals["overige_bezittingen"],
        schulden=totals["schulden"],
        heffingsvrij=args.heffingsvrij,
        has_partner=args.has_partner,
        allocation_pct=args.allocation_pct,
        partner_full_year_confirmed=args.partner_full_year_confirmed,
    )
    actual_return_allocated = allocated_amount(
        args.actual_return,
        args.has_partner,
        args.allocation_pct,
    )
    return {
        **build_output(args, fictitious, actual_return_allocated),
        **row_check,
        "manual_review_required": False,
    }


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        output = run(args)
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 1 if output.get("manual_review_required") else 0


if __name__ == "__main__":
    raise SystemExit(main())
