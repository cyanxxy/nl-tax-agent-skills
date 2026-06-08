#!/usr/bin/env python3
"""
compare_box3_annual_2025.py

Compare fictitious vs actual return for box 3 annual 2025.
NOTE: This script is ONLY for the annual 2025 return, NOT for provisional assessments.

Usage:
    python3 compare_box3_annual_2025.py \\
        --banktegoeden <amount> \\
        --overige <amount> \\
        --schulden <amount> \\
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


# 2025 annual box 3 fictitious return percentages and thresholds.
#
# These values duplicate the canonical knowledge pack so this script can act as a
# deterministic calculator. The knowledge notes are canonical; keep these in sync
# with the reviewed rule note and bump them in the same commit it changes:
#   _shared/knowledge/years/2025/box3/fictitious.md (source bd_box3_2025_calc).
PERC_BANKTEGOEDEN = 0.0137
PERC_OVERIGE_BEZITTINGEN = 0.0588
PERC_SCHULDEN = 0.0270

TAX_RATE = 0.36
HEFFINGSVRIJ_PER_PERSON = 57_684
SCHULDEN_DREMPEL_PER_PERSON = 3_800


def nearest_euro(value):
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


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
    if allocation_pct < 0 or allocation_pct > 100:
        raise ValueError("allocation_pct must be between 0 and 100")


def allocated_amount(total, has_partner, allocation_pct):
    validate_allocation_pct(allocation_pct)
    if not has_partner and allocation_pct != 100:
        raise ValueError("allocation_pct can only differ from 100 when has_partner is true")
    if not has_partner:
        return total
    return total * (allocation_pct / 100)


def calculate_fictitious_box3(
    banktegoeden,
    overige,
    schulden,
    heffingsvrij,
    has_partner,
    allocation_pct=100.0,
):
    """Calculate fictitious box 3 income using the official step model."""
    validate_allocation_pct(allocation_pct)
    drempel = SCHULDEN_DREMPEL_PER_PERSON * (2 if has_partner else 1)
    aftrekbare_schulden = max(0.0, schulden - drempel)
    total_assets = banktegoeden + overige

    rendement_bank = banktegoeden * PERC_BANKTEGOEDEN
    rendement_overige = overige * PERC_OVERIGE_BEZITTINGEN
    rendement_schulden = aftrekbare_schulden * PERC_SCHULDEN
    belastbaar_rendement = rendement_bank + rendement_overige - rendement_schulden

    rendementsgrondslag = total_assets - aftrekbare_schulden
    hvv = heffingsvrij if heffingsvrij > 0 else HEFFINGSVRIJ_PER_PERSON * (2 if has_partner else 1)
    grondslag_sparen_en_beleggen = max(0.0, rendementsgrondslag - hvv)
    allocated_grondslag = allocated_amount(
        grondslag_sparen_en_beleggen,
        has_partner,
        allocation_pct,
    )

    aandeel_pct = aandeel_percentage(allocated_grondslag, rendementsgrondslag)
    aandeel_fraction = aandeel_pct / 100

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
        result["partner_allocation_pct"] = allocation_pct
    return result


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Compare fictitious vs actual return for box 3 annual 2025. "
            "NOTE: ONLY for annual 2025 return, NOT for provisional assessments."
        )
    )
    parser.add_argument("--banktegoeden", type=float, required=True,
                        help="Total banktegoeden in EUR on 1 January 2025")
    parser.add_argument("--overige", type=float, required=True,
                        help="Total overige bezittingen in EUR on 1 January 2025")
    parser.add_argument("--schulden", type=float, required=True,
                        help="Total box 3 debts in EUR on 1 January 2025")
    parser.add_argument("--heffingsvrij", type=float, default=0,
                        help="Heffingsvrij vermogen in EUR (default: 57684 per person)")
    parser.add_argument("--actual_return", type=float, required=True,
                        help="Total actual return in EUR after applying only permitted components")
    parser.add_argument("--has_partner", action="store_true",
                        help="Whether taxpayer has a fiscal partner")
    parser.add_argument("--allocation-pct", type=float, default=100.0,
                        help=(
                            "For fiscal partners: taxpayer's share of the "
                            "joint grondslag sparen en beleggen. Default 100."
                        ))
    return parser


def compare_tax_methods(fictitious, actual_return_allocated):
    actual_return_for_tax = max(0.0, actual_return_allocated)
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
        savings = 0.0

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
        "tax_rate": TAX_RATE,
        "percentages_used": {
            "banktegoeden": PERC_BANKTEGOEDEN,
            "overige_bezittingen": PERC_OVERIGE_BEZITTINGEN,
            "schulden": PERC_SCHULDEN,
        },
        "note": (
            "Actual return is set to EUR 0 for tax comparison if the allocated amount is negative. "
            "For fiscal partners, actual return follows the same allocation percentage as the "
            "grondslag sparen en beleggen. "
            "Displayed amounts use portal-style whole-euro rounding. "
            "The official filing environment makes the binding calculation."
        ),
    }


def run(args):
    fictitious = calculate_fictitious_box3(
        banktegoeden=args.banktegoeden,
        overige=args.overige,
        schulden=args.schulden,
        heffingsvrij=args.heffingsvrij,
        has_partner=args.has_partner,
        allocation_pct=args.allocation_pct,
    )
    actual_return_allocated = allocated_amount(
        args.actual_return,
        args.has_partner,
        args.allocation_pct,
    )
    return build_output(args, fictitious, actual_return_allocated)


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        output = run(args)
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
