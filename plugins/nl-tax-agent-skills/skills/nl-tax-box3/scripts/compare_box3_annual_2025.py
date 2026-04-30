#!/usr/bin/env python3
"""
compare_box3_annual_2025.py

Compare fictitious vs actual return for box 3 annual 2025.
NOTE: This script is ONLY for the annual 2025 return, NOT for provisional assessments.

Usage:
    python compare_box3_annual_2025.py \\
        --banktegoeden <amount> \\
        --overige <amount> \\
        --schulden <amount> \\
        --heffingsvrij <amount> \\
        --actual_return <amount> \\
        [--has_partner]

All monetary amounts in EUR.

Output: JSON with fictitious_return, actual_return, favorable_method,
        tax_at_fictitious, tax_at_actual.
"""

import argparse
import json
import sys


# 2025 fictitious return percentages
PERC_BANKTEGOEDEN = 0.0036      # 0.36%
PERC_OVERIGE_BEZITTINGEN = 0.0604  # 6.04%
PERC_SCHULDEN = 0.0247          # 2.47%

# Tax rate on box 3 income
TAX_RATE = 0.36                 # 36%

# Default heffingsvrij vermogen per person
HEFFINGSVRIJ_PER_PERSON = 57_000

# Schulden drempel per person
SCHULDEN_DREMPEL_PER_PERSON = 3_700


def calculate_fictitious_return(banktegoeden, overige, schulden, heffingsvrij, has_partner):
    """
    Calculate fictitious box 3 return using category-weighted method.

    Steps:
    1. Apply schulden drempel
    2. Calculate total vermogen (assets minus qualifying debts)
    3. Subtract heffingsvrij vermogen to get rendementsgrondslag
    4. Calculate category weights
    5. Apply fictitious percentages per category
    """
    # Schulden drempel
    drempel = SCHULDEN_DREMPEL_PER_PERSON * (2 if has_partner else 1)
    qualifying_schulden = max(0, schulden - drempel)

    # Total assets
    total_assets = banktegoeden + overige
    total_vermogen = total_assets - qualifying_schulden

    # Heffingsvrij vermogen
    hvv = heffingsvrij if heffingsvrij > 0 else HEFFINGSVRIJ_PER_PERSON * (2 if has_partner else 1)

    # Rendementsgrondslag (cannot be negative)
    grondslag = max(0, total_vermogen - hvv)

    if grondslag == 0:
        return {
            "grondslag": 0,
            "fictitious_return": 0.0,
            "category_weights": {
                "banktegoeden": 0.0,
                "overige_bezittingen": 0.0,
                "schulden": 0.0,
            },
            "details": {
                "total_assets": total_assets,
                "qualifying_schulden": qualifying_schulden,
                "total_vermogen": total_vermogen,
                "heffingsvrij_vermogen": hvv,
            },
        }

    # Category weights use net composition:
    # (bank + overige - schulden) is the denominator before heffingsvrij vermogen.
    weight_bank = banktegoeden / total_vermogen
    weight_overige = overige / total_vermogen
    weight_schulden = qualifying_schulden / total_vermogen

    # Fictitious return per category applied to grondslag
    fict_bank = grondslag * weight_bank * PERC_BANKTEGOEDEN
    fict_overige = grondslag * weight_overige * PERC_OVERIGE_BEZITTINGEN
    fict_schulden = grondslag * weight_schulden * PERC_SCHULDEN

    # Total fictitious return (schulden component reduces the return)
    fictitious_return = fict_bank + fict_overige - fict_schulden

    return {
        "grondslag": grondslag,
        "fictitious_return": round(fictitious_return, 2),
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
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compare fictitious vs actual return for box 3 annual 2025. "
                    "NOTE: ONLY for annual 2025 return, NOT for provisional assessments."
    )
    parser.add_argument("--banktegoeden", type=float, required=True,
                        help="Total banktegoeden (savings/bank accounts) in EUR")
    parser.add_argument("--overige", type=float, required=True,
                        help="Total overige bezittingen (investments etc.) in EUR")
    parser.add_argument("--schulden", type=float, required=True,
                        help="Total schulden (debts, excl. mortgage eigen woning) in EUR")
    parser.add_argument("--heffingsvrij", type=float, default=0,
                        help="Heffingsvrij vermogen in EUR (default: 57000 per person)")
    parser.add_argument("--actual_return", type=float, required=True,
                        help="Total actual return (werkelijk rendement) in EUR")
    parser.add_argument("--has_partner", action="store_true",
                        help="Whether taxpayer has a fiscal partner")

    args = parser.parse_args()

    # Calculate fictitious return
    fict_result = calculate_fictitious_return(
        banktegoeden=args.banktegoeden,
        overige=args.overige,
        schulden=args.schulden,
        heffingsvrij=args.heffingsvrij,
        has_partner=args.has_partner,
    )

    fictitious_return = fict_result["fictitious_return"]
    actual_return = args.actual_return

    # Tax calculations
    tax_at_fictitious = round(max(0, fictitious_return) * TAX_RATE, 2)
    tax_at_actual = round(max(0, actual_return) * TAX_RATE, 2)

    # Determine favorable method
    if tax_at_actual < tax_at_fictitious:
        favorable = "actual_return"
        savings = round(tax_at_fictitious - tax_at_actual, 2)
    elif tax_at_fictitious < tax_at_actual:
        favorable = "fictitious_return"
        savings = round(tax_at_actual - tax_at_fictitious, 2)
    else:
        favorable = "equal"
        savings = 0.0

    output = {
        "assessment_type": "annual_2025",
        "fictitious_return": fictitious_return,
        "actual_return": actual_return,
        "tax_at_fictitious": tax_at_fictitious,
        "tax_at_actual": tax_at_actual,
        "favorable_method": favorable,
        "tax_savings_from_favorable": savings,
        "tax_rate": TAX_RATE,
        "percentages_used": {
            "banktegoeden": PERC_BANKTEGOEDEN,
            "overige_bezittingen": PERC_OVERIGE_BEZITTINGEN,
            "schulden": PERC_SCHULDEN,
        },
        "calculation_details": fict_result,
        "note": "The official filing environment (Belastingdienst) makes the binding calculation. "
                "These figures are for workpack notes only.",
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
