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
        [--has_partner]

All monetary amounts in EUR (estimated positions as of 1 January 2026).
"""

import argparse
import json
import sys


# 2026 provisional fictitious return percentages
# NOTE: These are provisional estimates. Verify against published rates.
PERC_BANKTEGOEDEN = 0.0036      # 0.36% (verify from knowledge pack)
PERC_OVERIGE_BEZITTINGEN = 0.0604  # 6.04% (verify from knowledge pack)
PERC_SCHULDEN = 0.0247          # 2.47% (verify from knowledge pack)

# Tax rate on box 3 income
TAX_RATE = 0.36                 # 36%

# Heffingsvrij vermogen per person
HEFFINGSVRIJ_PER_PERSON = 57_000

# Schulden drempel per person
SCHULDEN_DREMPEL_PER_PERSON = 3_700


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


def calculate_provisional_fictitious(banktegoeden, overige, schulden, heffingsvrij, has_partner):
    """
    Calculate fictitious box 3 return for the 2026 provisional assessment.
    Uses ONLY the fictitious return method. No actual return calculation.
    """
    # Schulden drempel
    drempel = SCHULDEN_DREMPEL_PER_PERSON * (2 if has_partner else 1)
    qualifying_schulden = max(0, schulden - drempel)

    # Total assets
    total_assets = banktegoeden + overige
    total_vermogen = total_assets - qualifying_schulden

    # Heffingsvrij vermogen
    if heffingsvrij > 0:
        hvv = heffingsvrij
    else:
        hvv = HEFFINGSVRIJ_PER_PERSON * (2 if has_partner else 1)

    # Rendementsgrondslag (cannot be negative)
    grondslag = max(0, total_vermogen - hvv)

    if grondslag == 0:
        return {
            "grondslag": 0,
            "fictitious_return": 0.0,
            "estimated_tax": 0.0,
            "details": {
                "total_assets": total_assets,
                "qualifying_schulden": qualifying_schulden,
                "total_vermogen": total_vermogen,
                "heffingsvrij_vermogen": hvv,
                "schulden_drempel": drempel,
            },
        }

    # Category weights use net composition:
    # (bank + overige - schulden) is the denominator before heffingsvrij vermogen.
    weight_bank = banktegoeden / total_vermogen
    weight_overige = overige / total_vermogen
    weight_schulden = qualifying_schulden / total_vermogen

    # Fictitious return per category
    fict_bank = grondslag * weight_bank * PERC_BANKTEGOEDEN
    fict_overige = grondslag * weight_overige * PERC_OVERIGE_BEZITTINGEN
    fict_schulden = grondslag * weight_schulden * PERC_SCHULDEN

    fictitious_return = round(fict_bank + fict_overige - fict_schulden, 2)
    estimated_tax = round(max(0, fictitious_return) * TAX_RATE, 2)

    return {
        "grondslag": grondslag,
        "fictitious_return": fictitious_return,
        "estimated_tax": estimated_tax,
        "category_weights": {
            "banktegoeden": round(weight_bank, 4),
            "overige_bezittingen": round(weight_overige, 4),
            "schulden": round(weight_schulden, 4),
        },
        "category_returns": {
            "banktegoeden": round(fict_bank, 2),
            "overige_bezittingen": round(fict_overige, 2),
            "schulden": round(fict_schulden, 2),
        },
        "details": {
            "total_assets": total_assets,
            "qualifying_schulden": qualifying_schulden,
            "total_vermogen": total_vermogen,
            "heffingsvrij_vermogen": hvv,
            "schulden_drempel": drempel,
        },
    }


def main():
    # FIRST: Check for prohibited actual return parameters
    check_prohibited_arguments()

    parser = argparse.ArgumentParser(
        description="Calculate box 3 fictitious return for the 2026 provisional assessment. "
                    "Uses ONLY the fictitious method. Werkelijk rendement is NOT accepted."
    )
    parser.add_argument("--banktegoeden", type=float, required=True,
                        help="Estimated banktegoeden as of 1 Jan 2026 in EUR")
    parser.add_argument("--overige", type=float, required=True,
                        help="Estimated overige bezittingen as of 1 Jan 2026 in EUR")
    parser.add_argument("--schulden", type=float, required=True,
                        help="Estimated schulden as of 1 Jan 2026 in EUR")
    parser.add_argument("--heffingsvrij", type=float, default=0,
                        help="Heffingsvrij vermogen in EUR (default: 57000/person, 114000 with partner)")
    parser.add_argument("--has_partner", action="store_true",
                        help="Whether taxpayer has a fiscal partner")

    args = parser.parse_args()

    result = calculate_provisional_fictitious(
        banktegoeden=args.banktegoeden,
        overige=args.overige,
        schulden=args.schulden,
        heffingsvrij=args.heffingsvrij,
        has_partner=args.has_partner,
    )

    output = {
        "assessment_type": "provisional_2026",
        "method": "fictitious_only",
        "peildatum": "2026-01-01",
        "input_note": "All amounts are ESTIMATES as of 1 January 2026",
        "grondslag": result["grondslag"],
        "fictitious_return": result["fictitious_return"],
        "estimated_tax": result["estimated_tax"],
        "tax_rate": TAX_RATE,
        "percentages_used": {
            "banktegoeden": PERC_BANKTEGOEDEN,
            "overige_bezittingen": PERC_OVERIGE_BEZITTINGEN,
            "schulden": PERC_SCHULDEN,
            "note": "Verify these percentages against the published 2026 provisional rates",
        },
        "calculation_details": result,
        "werkelijk_rendement": "NOT_APPLICABLE — provisional assessment uses fictitious method only",
    }

    if args.has_partner:
        output["partner_note"] = (
            "Combined heffingsvrij vermogen of EUR 114,000 applied. "
            "Partners may freely allocate box 3 assets and debts between them."
        )

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
