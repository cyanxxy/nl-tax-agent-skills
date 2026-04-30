#!/usr/bin/env python3
"""Validate and calculate own-home (eigen woning) inputs for Dutch tax.

Takes WOZ-waarde, mortgage interest, and mortgage start year as arguments.
Calculates eigenwoningforfait, checks tariefsaanpassing applicability, and
determines whether the Hillenregeling applies.

Usage:
    python validate_own_home_inputs.py \\
        --woz-value 400000 \\
        --mortgage-interest 8500 \\
        --mortgage-start-year 2018 \\
        [--taxable-income 85000] \\
        [--tax-year 2025] \\
        [--ownership-share 100]

Options:
    --woz-value VALUE           WOZ-waarde in EUR (required)
    --mortgage-interest VALUE   Annual deductible mortgage interest in EUR (required)
    --mortgage-start-year YEAR  Year the mortgage was taken out (required)
    --taxable-income VALUE      Estimated box 1 taxable income before eigen woning
                                deduction.  If omitted, tariefsaanpassing check
                                outputs a warning instead of a definitive result.
    --tax-year YEAR             Tax year for the calculation (default: 2025)
    --ownership-share PCT       Ownership percentage, 1-100 (default: 100)

Uses standard library only.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Constants — 2025 and 2026 parameters
# ---------------------------------------------------------------------------

# Eigenwoningforfait percentages by year
EIGENWONINGFORFAIT_TABLE: dict[int, list[tuple[float, float, float, Optional[float]]]] = {
    # Each entry: (lower_bound, upper_bound, percentage, fixed_base)
    # fixed_base is used only for the top bracket (above EUR 1,310,000)
    2025: [
        (0, 12_500, 0.0000, None),
        (12_500, 25_000, 0.0010, None),
        (25_000, 50_000, 0.0020, None),
        (50_000, 75_000, 0.0025, None),
        (75_000, 1_310_000, 0.0035, None),
        (1_310_000, float("inf"), 0.0235, 4_585),
    ],
    2026: [
        # Provisional — use 2025 values as estimates until 2026 is confirmed
        (0, 12_500, 0.0000, None),
        (12_500, 25_000, 0.0010, None),
        (25_000, 50_000, 0.0020, None),
        (50_000, 75_000, 0.0025, None),
        (75_000, 1_310_000, 0.0035, None),
        (1_310_000, float("inf"), 0.0235, 4_585),
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
        # Provisional — may differ from 2025
        "schijf3_threshold": 76_817,
        "schijf3_rate": 0.4950,
        "cap_rate": 0.3748,
    },
}

# Hillenregeling phase-out: year -> percentage of benefit remaining
HILLENREGELING_REMAINING: dict[int, float] = {
    2019: 0.9667,
    2020: 0.9333,
    2021: 0.9000,
    2022: 0.8667,
    2023: 0.8333,
    2024: 0.8000,
    2025: 0.7667,
    2026: 0.7333,
    2027: 0.7000,
    2028: 0.6667,
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
    mortgage_qualifies_post2013: Optional[bool]
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
            "mortgage_qualifies_post2013": self.mortgage_qualifies_post2013,
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
        # Fall back to 2025 table with a warning (caller should note this)
        table = EIGENWONINGFORFAIT_TABLE[2025]

    for lower, upper, pct, fixed_base in table:
        if lower <= woz_value < upper:
            if fixed_base is not None:
                # Top bracket: fixed base + percentage of excess
                return round(fixed_base + (woz_value - lower) * pct)
            return round(woz_value * pct)

    # Should not reach here, but handle gracefully
    return round(woz_value * 0.0035)


def check_mortgage_qualification(start_year: int) -> Optional[bool]:
    """Check if the mortgage qualifies for interest deduction under post-2013 rules.

    Returns True if post-2013 rules apply (annuitair/lineair required),
    False if pre-2013 transitional rules apply, None if unknown.
    """
    if start_year >= 2013:
        return True  # Post-2013: must be annuitair or lineair
    return False  # Pre-2013: transitional rules, aflossingsvrij may qualify


def calculate_tariefsaanpassing(
    mortgage_interest: float,
    taxable_income: Optional[float],
    tax_year: int,
) -> tuple[Optional[bool], Optional[float], list[str]]:
    """Calculate the tariefsaanpassing (rate adjustment) for high earners.

    Returns (applies, amount, warnings).
    """
    warnings: list[str] = []
    params = TARIEFSAANPASSING.get(tax_year)
    if params is None:
        params = TARIEFSAANPASSING[2025]
        warnings.append(
            f"Tariefsaanpassing parameters for {tax_year} not available; "
            f"using 2025 parameters as estimate."
        )

    if taxable_income is None:
        return (
            None,
            None,
            [
                "WARNING: Taxable income not provided. Cannot determine if "
                "tariefsaanpassing applies. If box 1 income before eigen woning "
                f"deduction exceeds EUR {params['schijf3_threshold']:,.0f}, the "
                "effective mortgage interest deduction rate is capped at "
                f"{params['cap_rate'] * 100:.2f}%."
            ],
        )

    threshold = params["schijf3_threshold"]
    if taxable_income <= threshold:
        return (False, 0.0, warnings)

    # Tariefsaanpassing applies
    rate_diff = params["schijf3_rate"] - params["cap_rate"]
    adjustment = round(mortgage_interest * rate_diff, 2)
    warnings.append(
        f"Tariefsaanpassing applies: income EUR {taxable_income:,.0f} exceeds "
        f"schijf 3 threshold EUR {threshold:,.0f}. Mortgage interest deduction "
        f"benefit is reduced by EUR {adjustment:,.2f} "
        f"({rate_diff * 100:.2f}% of EUR {mortgage_interest:,.2f})."
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
    remaining_pct = HILLENREGELING_REMAINING.get(tax_year, 0.0)

    if eigenwoningforfait <= mortgage_interest:
        # Forfait does not exceed interest — Hillenregeling does not apply
        return (False, 0.0, remaining_pct)

    # Excess forfait that would otherwise be added to income
    excess = eigenwoningforfait - mortgage_interest
    correction = round(excess * remaining_pct)

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

    all_warnings: list[str] = []
    missing_inputs: list[str] = []

    # --- Ownership share adjustment ---
    if ownership_share < 1 or ownership_share > 100:
        print("ERROR: --ownership-share must be between 1 and 100.", file=sys.stderr)
        return 1

    effective_woz = woz_value * (ownership_share / 100)
    effective_interest = mortgage_interest * (ownership_share / 100)

    if ownership_share < 100:
        all_warnings.append(
            f"Ownership share is {ownership_share}%. Calculations use the "
            f"taxpayer's share: WOZ EUR {effective_woz:,.0f}, "
            f"interest EUR {effective_interest:,.2f}."
        )

    # --- Eigenwoningforfait ---
    ewf = calculate_eigenwoningforfait(effective_woz, tax_year)

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

    # --- Tariefsaanpassing ---
    ta_applies, ta_amount, ta_warnings = calculate_tariefsaanpassing(
        effective_interest, taxable_income, tax_year
    )
    all_warnings.extend(ta_warnings)

    if taxable_income is None:
        missing_inputs.append(
            "taxable_income: not provided. Cannot determine tariefsaanpassing. "
            "Provide --taxable-income for a complete calculation."
        )

    # --- Hillenregeling ---
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
            f"({hillen_remaining * 100:.2f}% remaining in {tax_year})."
        )
    else:
        net_after_hillen = net_eigen_woning

    # --- Build result ---
    result = OwnHomeResult(
        tax_year=tax_year,
        woz_value=woz_value,
        ownership_share_pct=ownership_share,
        eigenwoningforfait=ewf,
        mortgage_interest=effective_interest,
        mortgage_start_year=mortgage_start_year,
        mortgage_qualifies_post2013=qualifies_post2013,
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
    print(f"Eigenwoningforfait:     EUR {result.eigenwoningforfait:,}")
    print(f"Mortgage interest:      EUR {result.mortgage_interest:,.2f}")
    print(f"Mortgage start year:    {result.mortgage_start_year}")
    if result.mortgage_qualifies_post2013 is not None:
        label = "post-2013 (annuitair/lineair required)" if result.mortgage_qualifies_post2013 else "pre-2013 (transitional rules)"
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
        print(f"  Benefit remaining:    {result.hillenregeling_remaining_pct * 100:.2f}%")
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
