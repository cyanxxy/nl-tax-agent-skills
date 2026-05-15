#!/usr/bin/env python3
"""
summarize_box3_provisional_2026.py

Calculate box 3 fictitious return for the 2026 provisional assessment
(voorlopige aanslag 2026).

CRITICAL: This script uses ONLY the fictitious return method.
It does NOT accept or calculate werkelijk rendement (actual return).
If an actual_return parameter is provided, the script exits with an error.

Usage:
    python summarize_box3_provisional_2026.py \\
        --banktegoeden <amount> \\
        --overige <amount> \\
        --schulden <amount> \\
        [--heffingsvrij <amount>] \\
        [--has_partner] \\
        [--allocation-pct <0-100>]

All monetary amounts in EUR (estimated positions as of 1 January 2026).
"""

import argparse
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
import json
import sys


PERC_BANKTEGOEDEN = 0.0128
PERC_OVERIGE_BEZITTINGEN = 0.0600
PERC_SCHULDEN = 0.0270

TAX_RATE = 0.36
HEFFINGSVRIJ_PER_PERSON = 59_357
SCHULDEN_DREMPEL_PER_PERSON = 3_800


def nearest_euro(value):
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def floor_euro(value):
    return int(Decimal(str(value)).to_integral_value(rounding=ROUND_FLOOR))


def aandeel_percentage(grondslag_sparen_en_beleggen, rendementsgrondslag):
    """Return the two-decimal percentage used in Belastingdienst examples.

    The official examples display truncated two-decimal percentages, e.g.
    269,443 / 328,800 * 100 = 81.94% and
    106,943 / 332,600 * 100 = 32.15%.
    """
    if rendementsgrondslag <= 0 or grondslag_sparen_en_beleggen <= 0:
        return 0.0
    percentage = (
        Decimal(str(grondslag_sparen_en_beleggen))
        / Decimal(str(rendementsgrondslag))
        * Decimal("100")
    )
    return float(percentage.quantize(Decimal("0.01"), rounding=ROUND_FLOOR))


def check_prohibited_arguments():
    """
    HARD PROHIBITION: Exit with error if any actual return parameter is provided.

    CRITICAL: Do NOT collect werkelijk rendement for 2026 voorlopige aanslag.
    Do NOT ask the user for actual interest earned, dividends received, or capital gains for 2026.
    The provisional assessment uses ONLY the fictitious return method.
    Werkelijk rendement may become relevant in the annual 2026 return (filed in 2027).
    """
    prohibited_args = [
        "--actual_return", "--actual-return", "--werkelijk",
        "--werkelijk_rendement", "--werkelijk-rendement",
        "--actual", "--real_return", "--real-return",
        "--dividends", "--interest_earned", "--capital_gains",
    ]
    for arg in sys.argv[1:]:
        arg_name = arg.split("=")[0].lower()
        if arg_name in prohibited_args:
            print(
                "ERROR: The 2026 voorlopige aanslag uses ONLY the fictitious return method.\n"
                "\n"
                f"Prohibited parameter detected: {arg}\n"
                "\n"
                "Do NOT provide werkelijk rendement (actual return) data for the provisional assessment.\n"
                "Actual return (werkelijk rendement) may become relevant when you file your\n"
                "annual 2026 return after the year ends (filed in 2027).\n",
                file=sys.stderr,
            )
            sys.exit(1)


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


def calculate_provisional_fictitious(
    banktegoeden,
    overige,
    schulden,
    heffingsvrij,
    has_partner,
    allocation_pct=100.0,
):
    """Calculate provisional 2026 box 3 using the official fictitious step model."""
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


def main():
    check_prohibited_arguments()

    parser = argparse.ArgumentParser(
        description=(
            "Calculate box 3 fictitious return for the 2026 provisional assessment. "
            "Uses ONLY the fictitious method. Werkelijk rendement is NOT accepted."
        )
    )
    parser.add_argument("--banktegoeden", type=float, required=True,
                        help="Estimated banktegoeden as of 1 Jan 2026 in EUR")
    parser.add_argument("--overige", type=float, required=True,
                        help="Estimated overige bezittingen as of 1 Jan 2026 in EUR")
    parser.add_argument("--schulden", type=float, required=True,
                        help="Estimated box 3 debts as of 1 Jan 2026 in EUR")
    parser.add_argument("--heffingsvrij", type=float, default=0,
                        help="Heffingsvrij vermogen in EUR (default: 59357 per person)")
    parser.add_argument("--has_partner", action="store_true",
                        help="Whether taxpayer has a fiscal partner")
    parser.add_argument("--allocation-pct", type=float, default=100.0,
                        help=(
                            "For fiscal partners: taxpayer's share of the "
                            "joint grondslag sparen en beleggen. Default 100."
                        ))

    args = parser.parse_args()

    try:
        result = calculate_provisional_fictitious(
            banktegoeden=args.banktegoeden,
            overige=args.overige,
            schulden=args.schulden,
            heffingsvrij=args.heffingsvrij,
            has_partner=args.has_partner,
            allocation_pct=args.allocation_pct,
        )
    except ValueError as exc:
        parser.error(str(exc))

    output = {
        "assessment_type": "provisional_2026",
        "method": "fictitious_only",
        "peildatum": "2026-01-01",
        "input_note": "All amounts are estimates as of 1 January 2026",
        **result,
        "fictitious_return": result["box3_inkomen"],
        "estimated_tax": result["box3_belasting"],
        "tax_rate": TAX_RATE,
        "percentages_used": {
            "banktegoeden": PERC_BANKTEGOEDEN,
            "overige_bezittingen": PERC_OVERIGE_BEZITTINGEN,
            "schulden": PERC_SCHULDEN,
        },
        "werkelijk_rendement": "NOT_APPLICABLE: provisional assessment uses fictitious method only",
        "rounding_note": "Displayed amounts use portal-style whole-euro rounding.",
    }

    if args.has_partner:
        output["partner_note"] = (
            "Combined heffingsvrij vermogen of EUR 118,714 applied. "
            f"Taxpayer allocation percentage is {args.allocation_pct:.2f}% of the "
            "joint grondslag sparen en beleggen."
        )

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
