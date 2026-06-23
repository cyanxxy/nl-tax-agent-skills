#!/usr/bin/env python3
"""Validate and calculate own-home (eigen woning) inputs for Dutch tax.

Takes WOZ-waarde, mortgage interest, and mortgage start year as arguments.
Calculates eigenwoningforfait, checks tariefsaanpassing applicability, and
determines whether the Hillenregeling applies.

Usage:
    python3 validate_own_home_inputs.py \\
        --woz-value 400000 \\
        --mortgage-interest 8500 \\
        --mortgage-start-year 2018 \\
        [--taxable-income 85000] \\
        [--tax-year 2025] \\
        [--ownership-share 100] \\
        [--interest-share 100]

Options:
    --woz-value VALUE           WOZ-waarde in EUR (required)
    --mortgage-interest VALUE   Annual deductible mortgage interest in EUR (required)
    --mortgage-start-year YEAR  Year the mortgage was taken out (required)
    --taxable-income VALUE      Estimated box 1 income BEFORE the eigen-woning
                                result.  The script derives the belastbaar inkomen
                                internally (income + net eigen-woning result after
                                Hillen) before checking the tariefsaanpassing.  If
                                omitted, the tariefsaanpassing check outputs a
                                warning instead of a definitive result.
    --tax-year YEAR             Tax year for the calculation (default: 2025)
    --ownership-share PCT       Home-ownership percentage, 1-100 (default: 100).
                                Scales the WOZ-waarde (eigenwoningforfait side).
    --interest-share PCT        Eigenwoningschuld / deductible-interest share,
                                1-100 (alias: --debt-share).  Scales the
                                deductible mortgage interest independently from
                                ownership.  Defaults to --ownership-share when
                                omitted.

Uses standard library only.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


# ---------------------------------------------------------------------------
# Constants — reviewed 2025 and 2026 parameters
#
# These values duplicate the canonical knowledge pack so this script can act as a
# deterministic calculator. The knowledge notes are canonical; this table is a
# convenience copy. Keep them in sync with the reviewed rule notes (and bump them
# in the same commit a note changes):
#   - eigenwoningforfait brackets: _shared/knowledge/own-home/eigenwoningforfait.md
#                                  (source bd_eigenwoningforfait_2025_2026)
#   - tariefsaanpassing / Hillen:  _shared/knowledge/years/2025/annual/own-home.md
#                                  and years/2026/provisional/own-home.md
#                                  (sources bd_own_home_deduction_cap_2025 / _2026)
# ---------------------------------------------------------------------------

# Eigenwoningforfait percentages by year
EIGENWONINGFORFAIT_TABLE: dict[int, list[tuple[float, float, float, Optional[float]]]] = {
    # Each entry: (lower_bound, upper_bound, percentage, fixed_base).
    # Standard brackets are lower-exclusive and upper-inclusive, except the
    # first bracket which includes zero. The top bracket is strictly above
    # lower_bound and uses fixed_base.
    2025: [
        (0, 12_500, 0.0000, None),
        (12_500, 25_000, 0.0010, None),
        (25_000, 50_000, 0.0020, None),
        (50_000, 75_000, 0.0025, None),
        (75_000, 1_330_000, 0.0035, None),
        (1_330_000, float("inf"), 0.0235, 4_655),
    ],
    2026: [
        (0, 12_500, 0.0000, None),
        (12_500, 25_000, 0.0010, None),
        (25_000, 50_000, 0.0020, None),
        (50_000, 75_000, 0.0025, None),
        (75_000, 1_350_000, 0.0035, None),
        (1_350_000, float("inf"), 0.0235, 4_725),
    ],
}

# Tariefsaanpassing thresholds by year
TARIEFSAANPASSING: dict[int, dict[str, float]] = {
    2025: {
        "schijf3_threshold": 76_817,
        "schijf3_rate": 0.4950,
        "cap_rate": 0.3748,
    },
    2026: {
        "schijf3_threshold": 78_426,
        "schijf3_rate": 0.4950,
        "cap_rate": 0.3756,
    },
}

# Hillenregeling phase-out: year -> percentage of benefit remaining.
# Keep Decimal values for whole-euro rounding; expose floats in results.
HILLENREGELING_REMAINING: dict[int, Decimal] = {
    2025: Decimal("0.76667"),
    2026: Decimal("0.71867"),
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class OwnHomeResult:
    """Structured result of the own-home validation and calculation."""

    tax_year: int
    woz_value: float
    ownership_share_pct: int
    eigenwoningforfait: float
    mortgage_interest: float
    mortgage_start_year: int
    mortgage_regime_post2013: Optional[bool]
    net_eigen_woning: float
    tariefsaanpassing_applies: Optional[bool]
    tariefsaanpassing_amount: Optional[float]
    hillenregeling_applies: bool
    hillenregeling_correction: float
    hillenregeling_remaining_pct: float
    net_after_hillen: float
    warnings: list[str] = field(default_factory=list)
    missing_inputs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "tax_year": self.tax_year,
            "woz_value": self.woz_value,
            "ownership_share_pct": self.ownership_share_pct,
            "eigenwoningforfait": self.eigenwoningforfait,
            "mortgage_interest": self.mortgage_interest,
            "mortgage_start_year": self.mortgage_start_year,
            "mortgage_regime_post2013": self.mortgage_regime_post2013,
            "net_eigen_woning": self.net_eigen_woning,
            "tariefsaanpassing_applies": self.tariefsaanpassing_applies,
            "tariefsaanpassing_amount": self.tariefsaanpassing_amount,
            "hillenregeling_applies": self.hillenregeling_applies,
            "hillenregeling_correction": self.hillenregeling_correction,
            "hillenregeling_remaining_pct": self.hillenregeling_remaining_pct,
            "net_after_hillen": self.net_after_hillen,
            "warnings": self.warnings,
            "missing_inputs": self.missing_inputs,
        }


# ---------------------------------------------------------------------------
# Calculation functions
# ---------------------------------------------------------------------------


def calculate_eigenwoningforfait(woz_value: float, tax_year: int) -> float:
    """Calculate the eigenwoningforfait based on WOZ-waarde and tax year."""
    table = EIGENWONINGFORFAIT_TABLE.get(tax_year)
    if table is None:
        raise ValueError(
            f"No reviewed eigenwoningforfait table is available for {tax_year}."
        )

    for lower, upper, pct, fixed_base in table:
        if fixed_base is not None:
            if woz_value > lower:
                return round(fixed_base + (woz_value - lower) * pct)
            continue

        if (lower == 0 and 0 <= woz_value <= upper) or (lower < woz_value <= upper):
            return round(woz_value * pct)

    raise ValueError(f"WOZ value EUR {woz_value:,.2f} is outside the reviewed table.")


def check_mortgage_qualification(start_year: int) -> Optional[bool]:
    """Report which eigenwoningschuld REGIME applies based on the start year.

    This does not determine whether a specific loan qualifies for interest
    deduction — only which set of rules governs it. The caller must still
    verify the loan meets that regime's requirement.

    Returns True if the post-2013 regime applies (annuitair/lineair repayment
    required), False if the pre-2013 transitional regime applies, None if
    unknown.
    """
    if start_year >= 2013:
        return True  # Post-2013 regime: must be annuitair or lineair
    return False  # Pre-2013 transitional regime: aflossingsvrij may qualify


def calculate_tariefsaanpassing(
    mortgage_interest: float,
    belastbaar_inkomen: Optional[float],
    tax_year: int,
) -> tuple[Optional[bool], Optional[float], list[str]]:
    """Calculate the tariefsaanpassing (rate adjustment) for own-home costs.

    Follows the official Belastingdienst grondslag method. ``belastbaar_inkomen``
    is the belastbaar inkomen uit werk en woning AFTER the eigen-woning result
    (including the Hillenregeling) — NOT the income before the eigen-woning
    deduction. The grondslag is:

        grondslag = min(afgetrokken eigenwoningkosten,
                        belastbaar_inkomen + afgetrokken eigenwoningkosten
                            - drempelbedrag hoogste schijf)
        adjustment = round(grondslag * (schijf3_rate - cap_rate), 2)

    The grondslag is capped at the deducted eigen-woning costs (art. 2.10 lid 2
    Wet IB 2001), so the correction can never exceed rate_diff x the deducted
    costs. It applies only when income WITHOUT the deduction
    (belastbaar_inkomen + costs) exceeds the drempel. The deductible eigen-woning
    costs are the deductible mortgage interest/costs (added back because they were
    already subtracted to reach belastbaar_inkomen).

    Returns (applies, amount, warnings).
    """
    warnings: list[str] = []
    params = TARIEFSAANPASSING.get(tax_year)
    if params is None:
        return (
            None,
            None,
            [
                f"No reviewed tariefsaanpassing parameters are available for {tax_year}."
            ],
        )

    if belastbaar_inkomen is None:
        return (
            None,
            None,
            [
                "WARNING: Taxable income not provided. Cannot determine if "
                "tariefsaanpassing applies. If box 1 income BEFORE the own-home "
                "deduction exceeds EUR "
                f"{params['schijf3_threshold']:,.0f}, the effective deduction "
                "rate for own-home costs is capped at "
                f"{params['cap_rate'] * 100:.2f}%."
            ],
        )

    threshold = params["schijf3_threshold"]
    deductible_costs = max(mortgage_interest, 0.0)
    if deductible_costs == 0:
        return (False, 0.0, warnings)

    # The tariefsaanpassing applies only when box 1 income WITHOUT the own-home
    # deduction exceeds the top-bracket drempel. belastbaar_inkomen is the income
    # AFTER the eigen-woning result, so add the deducted costs back to recover the
    # income-without-deduction figure the rule tests against.
    income_without_deduction = belastbaar_inkomen + deductible_costs
    if income_without_deduction <= threshold:
        return (False, 0.0, warnings)

    # Statutory grondslag (art. 2.10 lid 2 Wet IB 2001): the deducted own-home
    # costs, but only to the extent income-without-deduction exceeds the drempel,
    # and capped at the deducted costs themselves. The correction can therefore
    # never exceed rate_diff x deductible_costs.
    base = min(deductible_costs, income_without_deduction - threshold)
    rate_diff = params["schijf3_rate"] - params["cap_rate"]
    adjustment = round(base * rate_diff, 2)
    warnings.append(
        f"Tariefsaanpassing applies: box 1 income without the own-home deduction "
        f"(EUR {income_without_deduction:,.0f}) exceeds the schijf 3 drempel "
        f"(EUR {threshold:,.0f}). The own-home deduction benefit is reduced by "
        f"EUR {adjustment:,.2f} ({rate_diff * 100:.2f}% of grondslag EUR "
        f"{base:,.2f} — the deductible costs falling in schijf 3, capped at the "
        f"EUR {deductible_costs:,.2f} deducted). The Belastingdienst computes the "
        "definitive figure automatically in the aangifte — verify against your "
        "concept-aanslag."
    )
    return (True, adjustment, warnings)


def calculate_hillenregeling(
    eigenwoningforfait: float,
    mortgage_interest: float,
    tax_year: int,
) -> tuple[bool, float, float]:
    """Calculate the Hillenregeling correction.

    Returns (applies, correction_amount, remaining_percentage).
    """
    remaining_decimal = HILLENREGELING_REMAINING.get(tax_year, Decimal("0"))
    remaining_pct = float(remaining_decimal)

    if eigenwoningforfait <= mortgage_interest:
        # Forfait does not exceed interest — Hillenregeling does not apply
        return (False, 0.0, remaining_pct)

    # Excess forfait that would otherwise be added to income
    excess = eigenwoningforfait - mortgage_interest
    correction = int(
        (Decimal(str(excess)) * remaining_decimal).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP
        )
    )

    return (True, correction, remaining_pct)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def parse_args(argv: list[str]) -> dict:
    """Parse command-line arguments into a dict."""
    result: dict = {
        "woz_value": None,
        "mortgage_interest": None,
        "mortgage_start_year": None,
        "taxable_income": None,
        "tax_year": 2025,
        "ownership_share": 100,
        "interest_share": None,
        "interest_share_provided": False,
    }

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--woz-value" and i + 1 < len(argv):
            result["woz_value"] = float(argv[i + 1])
            i += 2
        elif arg == "--mortgage-interest" and i + 1 < len(argv):
            result["mortgage_interest"] = float(argv[i + 1])
            i += 2
        elif arg == "--mortgage-start-year" and i + 1 < len(argv):
            result["mortgage_start_year"] = int(argv[i + 1])
            i += 2
        elif arg == "--taxable-income" and i + 1 < len(argv):
            result["taxable_income"] = float(argv[i + 1])
            i += 2
        elif arg == "--tax-year" and i + 1 < len(argv):
            result["tax_year"] = int(argv[i + 1])
            i += 2
        elif arg == "--ownership-share" and i + 1 < len(argv):
            result["ownership_share"] = int(argv[i + 1])
            i += 2
        elif arg in ("--interest-share", "--debt-share") and i + 1 < len(argv):
            result["interest_share"] = int(argv[i + 1])
            result["interest_share_provided"] = True
            i += 2
        elif arg in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            sys.exit(1)

    return result


def validate_required(args: dict) -> list[str]:
    """Validate that required arguments are present. Return list of errors."""
    errors: list[str] = []
    if args["woz_value"] is None:
        errors.append("--woz-value is required")
    if args["mortgage_interest"] is None:
        errors.append("--mortgage-interest is required")
    if args["mortgage_start_year"] is None:
        errors.append("--mortgage-start-year is required")
    return errors


def main() -> int:
    args = parse_args(sys.argv[1:])

    errors = validate_required(args)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print("\nRun with --help for usage information.", file=sys.stderr)
        return 1

    woz_value: float = args["woz_value"]
    mortgage_interest: float = args["mortgage_interest"]
    mortgage_start_year: int = args["mortgage_start_year"]
    taxable_income: Optional[float] = args["taxable_income"]
    tax_year: int = args["tax_year"]
    ownership_share: int = args["ownership_share"]
    interest_share_provided: bool = args["interest_share_provided"]
    interest_share: int = (
        args["interest_share"] if interest_share_provided else ownership_share
    )

    all_warnings: list[str] = []
    missing_inputs: list[str] = []

    # --- Ownership / interest share adjustment ---
    if ownership_share < 1 or ownership_share > 100:
        print("ERROR: --ownership-share must be between 1 and 100.", file=sys.stderr)
        return 1
    if interest_share < 1 or interest_share > 100:
        print(
            "ERROR: --interest-share (--debt-share) must be between 1 and 100.",
            file=sys.stderr,
        )
        return 1

    # Home-ownership share scales the WOZ (eigenwoningforfait); the
    # eigenwoningschuld / deductible-interest share scales the interest
    # independently.
    effective_woz = woz_value * (ownership_share / 100)
    effective_interest = mortgage_interest * (interest_share / 100)

    if ownership_share < 100:
        all_warnings.append(
            f"Home-ownership share is {ownership_share}%. The eigenwoningforfait "
            f"uses the taxpayer's share of the WOZ: EUR {effective_woz:,.0f}."
        )
    if interest_share < 100:
        all_warnings.append(
            f"Deductible-interest / eigenwoningschuld share is {interest_share}%. "
            f"Calculations use the taxpayer's share of the interest: "
            f"EUR {effective_interest:,.2f}."
        )

    # Home-ownership share, eigenwoningschuld share, and who actually paid the
    # deductible interest can each differ — always flag this for verification.
    all_warnings.append(
        "Home-ownership share, eigenwoningschuld (debt) share, and who actually "
        "PAID the deductible interest can all differ from one another. Each must "
        "be verified separately against the deed, the mortgage agreement, and the "
        "payment records before relying on these figures."
    )
    if not interest_share_provided:
        missing_inputs.append(
            "interest_share: not explicitly provided. Defaulted to the "
            f"ownership share ({ownership_share}%). Provide --interest-share "
            "(or --debt-share) if the eigenwoningschuld / deductible-interest "
            "share differs from the home-ownership share."
        )

    # --- Eigenwoningforfait ---
    try:
        ewf = calculate_eigenwoningforfait(effective_woz, tax_year)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    # --- Mortgage qualification ---
    qualifies_post2013 = check_mortgage_qualification(mortgage_start_year)
    if qualifies_post2013:
        all_warnings.append(
            f"Mortgage started in {mortgage_start_year} (post-2013). "
            f"Annuitair or lineair repayment is required for interest deduction. "
            f"Verify that the mortgage meets this requirement."
        )

    # --- Net eigen woning (before Hillenregeling) ---
    net_eigen_woning = round(ewf - effective_interest)

    # --- Hillenregeling (computed BEFORE the tariefsaanpassing, because the
    # tariefsaanpassing grondslag is built on the belastbaar inkomen AFTER the
    # eigen-woning result, which includes the Hillen correction) ---
    hillen_applies, hillen_correction, hillen_remaining = calculate_hillenregeling(
        ewf, effective_interest, tax_year
    )

    # Net after Hillenregeling
    if hillen_applies:
        # The correction reduces the effective eigenwoningforfait
        net_after_hillen = round((ewf - hillen_correction) - effective_interest)
        all_warnings.append(
            f"Hillenregeling applies: eigenwoningforfait (EUR {ewf:,}) exceeds "
            f"mortgage interest (EUR {effective_interest:,.2f}). "
            f"Correction of EUR {hillen_correction:,} applied "
            f"({hillen_remaining * 100:.3f}% remaining in {tax_year})."
        )
    else:
        net_after_hillen = net_eigen_woning

    # --- Tariefsaanpassing ---
    # belastbaar inkomen uit werk en woning = income (before the eigen-woning
    # result) + net eigen-woning result after Hillen. Pass that (not the raw
    # pre-EW income) into the official grondslag method.
    belastbaar: Optional[float] = (
        (taxable_income + net_after_hillen) if taxable_income is not None else None
    )
    ta_applies, ta_amount, ta_warnings = calculate_tariefsaanpassing(
        effective_interest, belastbaar, tax_year
    )
    all_warnings.extend(ta_warnings)

    if taxable_income is None:
        missing_inputs.append(
            "taxable_income: not provided. Cannot determine tariefsaanpassing. "
            "Provide --taxable-income (box 1 income before the eigen-woning "
            "result) for a complete calculation."
        )

    # --- Build result ---
    result = OwnHomeResult(
        tax_year=tax_year,
        woz_value=woz_value,
        ownership_share_pct=ownership_share,
        eigenwoningforfait=ewf,
        mortgage_interest=effective_interest,
        mortgage_start_year=mortgage_start_year,
        mortgage_regime_post2013=qualifies_post2013,
        net_eigen_woning=net_eigen_woning,
        tariefsaanpassing_applies=ta_applies,
        tariefsaanpassing_amount=ta_amount,
        hillenregeling_applies=hillen_applies,
        hillenregeling_correction=hillen_correction,
        hillenregeling_remaining_pct=hillen_remaining,
        net_after_hillen=net_after_hillen,
        warnings=all_warnings,
        missing_inputs=missing_inputs,
    )

    # --- Output ---
    print("=== Own Home (Eigen Woning) Validation Summary ===\n")

    print(f"Tax year:               {result.tax_year}")
    print(f"WOZ-waarde:             EUR {result.woz_value:,.0f}")
    if ownership_share < 100:
        print(f"Ownership share:        {result.ownership_share_pct}%")
        print(f"Effective WOZ:          EUR {effective_woz:,.0f}")
    if interest_share < 100:
        print(f"Interest/debt share:    {interest_share}%")
    print(f"Eigenwoningforfait:     EUR {result.eigenwoningforfait:,}")
    print(f"Mortgage interest:      EUR {result.mortgage_interest:,.2f}")
    print(f"Mortgage start year:    {result.mortgage_start_year}")
    if result.mortgage_regime_post2013 is not None:
        if result.mortgage_regime_post2013:
            label = "post-2013 (annuitair/lineair required)"
        else:
            label = "pre-2013 (transitional rules)"
        print(f"Mortgage regime:        {label}")
    print(f"Net eigen woning:       EUR {result.net_eigen_woning:,}")
    print()

    # Tariefsaanpassing
    if result.tariefsaanpassing_applies is True:
        print(f"Tariefsaanpassing:      YES")
        print(f"  Adjustment amount:    EUR {result.tariefsaanpassing_amount:,.2f}")
    elif result.tariefsaanpassing_applies is False:
        print(f"Tariefsaanpassing:      NO (income below threshold)")
    else:
        print(f"Tariefsaanpassing:      UNKNOWN (taxable income not provided)")
    print()

    # Hillenregeling
    if result.hillenregeling_applies:
        print(f"Hillenregeling:         YES")
        print(f"  Correction:           EUR {result.hillenregeling_correction:,}")
        print(f"  Benefit remaining:    {result.hillenregeling_remaining_pct * 100:.3f}%")
        print(f"  Net after Hillen:     EUR {result.net_after_hillen:,}")
    else:
        print(f"Hillenregeling:         NO (mortgage interest >= eigenwoningforfait)")
    print()

    # Warnings
    if result.warnings:
        print("WARNINGS:")
        for w in result.warnings:
            print(f"  - {w}")
        print()

    # Missing inputs
    if result.missing_inputs:
        print("MISSING INPUTS:")
        for m in result.missing_inputs:
            print(f"  - {m}")
        print()

    # JSON output for programmatic consumption
    print("--- JSON OUTPUT ---")
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
