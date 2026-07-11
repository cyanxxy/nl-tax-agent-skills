#!/usr/bin/env python3
"""
summarize_box3_provisional_2026.py

Calculate box 3 fictitious return for the 2026 provisional assessment
(voorlopige aanslag 2026).

This script uses ONLY the fictitious return method.
Werkelijk rendement is not part of provisional 2026.
If an actual_return parameter is provided, the script exits with an error.

Usage:
    python3 summarize_box3_provisional_2026.py \\
        --rows-json '<already-classified JSON rows>' \\
        [--heffingsvrij <amount>] \\
        [--has_partner] \\
        [--allocation-pct <0-100>]

All monetary amounts in EUR (estimated positions as of 1 January 2026).
"""

import argparse
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_UP
import json
import math
import sys


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


# 2026 provisional box 3 fictitious return percentages and thresholds.
#
# These values duplicate the canonical knowledge pack so this script can act as a
# deterministic calculator. The knowledge notes are canonical; keep these in sync
# with the reviewed rule note and bump them in the same commit it changes:
#   _shared/knowledge/years/2026/provisional/box3-provisional.md
#   (source bd_box3_2026_provisional).
# Decimal constants: all money math below runs in Decimal end-to-end so that
# rounding happens exactly once per output figure (no binary-float drift).
PERC_BANKTEGOEDEN = Decimal("0.0128")
PERC_OVERIGE_BEZITTINGEN = Decimal("0.0600")
PERC_SCHULDEN = Decimal("0.0270")

TAX_RATE = Decimal("0.36")
HEFFINGSVRIJ_PER_PERSON = 59_357
SCHULDEN_DREMPEL_PER_PERSON = 3_800


def nearest_euro(value):
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def floor_euro(value):
    return int(Decimal(str(value)).to_integral_value(rounding=ROUND_FLOOR))


def aandeel_percentage(grondslag_sparen_en_beleggen, rendementsgrondslag):
    """Return the three-decimal percentage from the official 2026 step model.

    The general provisional 2026 instruction says to round the share percentage
    to three decimals.
    """
    if rendementsgrondslag <= 0 or grondslag_sparen_en_beleggen <= 0:
        return 0.0
    percentage = (
        Decimal(str(grondslag_sparen_en_beleggen))
        / Decimal(str(rendementsgrondslag))
        * Decimal("100")
    )
    return float(percentage.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def check_prohibited_arguments():
    """
    Exit with error if any actual-return parameter is provided.

    Werkelijk rendement is not part of provisional 2026.
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
                "Werkelijk rendement is not part of provisional 2026.\n",
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
    total = Decimal(str(total))
    if not has_partner:
        return total
    return total * Decimal(str(allocation_pct)) / Decimal("100")


def calculate_provisional_fictitious(
    banktegoeden,
    overige,
    schulden,
    heffingsvrij,
    has_partner,
    allocation_pct=100.0,
    partner_full_year_confirmed=False,
):
    """Calculate provisional 2026 box 3 using the official fictitious step model."""
    _require_finite_non_negative("banktegoeden", banktegoeden)
    _require_finite_non_negative("overige", overige)
    _require_finite_non_negative("schulden", schulden)
    _require_finite_non_negative("heffingsvrij", heffingsvrij)
    validate_allocation_pct(allocation_pct)
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
        result["partner_allocation_pct"] = allocation_pct
        result["partner_eligibility_note"] = (
            "Doubling of the heffingsvrij vermogen and the schulden drempel "
            "assumes a confirmed full-year (or elected full-year) fiscal "
            "partnership. If the partnership did not last the full year and "
            "full-year partnership was not elected, the doubled allowance and "
            "threshold do not apply."
        )
    return result


def main():
    check_prohibited_arguments()

    parser = argparse.ArgumentParser(
        description=(
            "Calculate box 3 fictitious return for the 2026 provisional assessment. "
            "Uses ONLY the fictitious method. Werkelijk rendement is NOT accepted."
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
                            "Heffingsvrij vermogen override in EUR. 0 or omitted = "
                            "statutory default (EUR 59,357 per person, doubled for a "
                            "confirmed full-year fiscal partner). Note: an explicit "
                            "zero allowance cannot be expressed — 0 always means the "
                            "statutory default."
                        ))
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

    args = parser.parse_args()

    try:
        try:
            rows = json.loads(args.rows_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"rows_json must contain valid JSON: {exc.msg}") from exc
        row_check = normalize_classified_rows(rows)
        if row_check["rejected_rows"]:
            print(
                json.dumps(
                    {
                        "assessment_type": "provisional_2026",
                        "method": "fictitious_only",
                        **row_check,
                        "manual_review_required": True,
                        "result": None,
                        "box3_provisional_actual_return_note": (
                            "Werkelijk rendement is not part of provisional 2026."
                        ),
                        "note": (
                            "Resolve every rejected/manual-review row before "
                            "running provisional box 3 arithmetic."
                        ),
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return
        totals = row_check["trusted_totals"]
        result = calculate_provisional_fictitious(
            banktegoeden=totals["banktegoeden"],
            overige=totals["overige_bezittingen"],
            schulden=totals["schulden"],
            heffingsvrij=args.heffingsvrij,
            has_partner=args.has_partner,
            allocation_pct=args.allocation_pct,
            partner_full_year_confirmed=args.partner_full_year_confirmed,
        )
    except ValueError as exc:
        parser.error(str(exc))

    output = {
        "assessment_type": "provisional_2026",
        "method": "fictitious_only",
        "peildatum": "2026-01-01",
        "input_note": "All amounts are estimates as of 1 January 2026",
        **row_check,
        "manual_review_required": False,
        **result,
        "fictitious_return": result["box3_inkomen"],
        "estimated_tax": result["box3_belasting"],
        "tax_rate": float(TAX_RATE),
        "percentages_used": {
            "banktegoeden": float(PERC_BANKTEGOEDEN),
            "overige_bezittingen": float(PERC_OVERIGE_BEZITTINGEN),
            "schulden": float(PERC_SCHULDEN),
        },
        "box3_provisional_actual_return_note": "Werkelijk rendement is not part of provisional 2026.",
        "rounding_note": "Displayed amounts use portal-style whole-euro rounding.",
    }

    if args.has_partner:
        applied_hvv = result["details"]["heffingsvrij_vermogen"]
        output["partner_note"] = (
            f"Combined heffingsvrij vermogen of EUR {applied_hvv:,.0f} applied"
            f"{' (override via --heffingsvrij)' if args.heffingsvrij > 0 else ''}. "
            f"Taxpayer allocation percentage is {args.allocation_pct:.2f}% of the "
            "joint grondslag sparen en beleggen."
        )

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
