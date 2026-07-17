#!/usr/bin/env python3
"""Check arithmetic for explicit, agent-reviewed own-home amounts.

The agent decides eligibility, qualification, ownership allocation, and the
eigenwoningforfait before calling this optional helper. The helper only checks
addition, Hillen, the own-home balance, and the separate rate adjustment.

Usage:
    python3 validate_own_home_inputs.py \
        --tax-year 2025 \
        --eigenwoningforfait 4000 \
        --mortgage-interest 3500 \
        --qualifying-financing-costs 300 \
        --periodic-erfpacht-opstal-beklemming 300 \
        [--taxable-income 85000]

Uses standard library only.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP, localcontext
from typing import Optional


def _euro(value: float) -> int:
    """Round to whole euros, half up (Belastingdienst convention)."""
    return int(Decimal(str(value)).to_integral_value(rounding=ROUND_HALF_UP))


def _cents(value) -> float:
    """Round to cents, half up (Belastingdienst convention)."""
    decimal_value = Decimal(str(value))
    integer_digits = max(1, decimal_value.adjusted() + 1) if decimal_value else 1
    with localcontext() as context:
        context.prec = max(28, integer_digits + 4)
        rounded = decimal_value.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    return float(rounded)


def _finite_float(value, field_name: str, *, non_negative: bool) -> float:
    """Normalize a direct arithmetic input or raise a stable ValueError."""
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a finite number")
    try:
        normalized = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{field_name} must be a finite number") from exc
    if not math.isfinite(normalized):
        raise ValueError(f"{field_name} must be a finite number")
    if non_negative and normalized < 0:
        raise ValueError(f"{field_name} must not be negative")
    return normalized


# ---------------------------------------------------------------------------
# Constants — reviewed 2025 and 2026 parameters
#
# These values duplicate the canonical knowledge pack so this optional mechanical
# arithmetic check can run offline. The knowledge notes are canonical; this table
# is a convenience copy. Keep them in sync with the reviewed rule notes (and bump
# them in the same commit a note changes):
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

STRUCTURED_AMOUNT_KEYS = {
    "eigenwoningforfait",
    "mortgage_interest",
    "qualifying_financing_costs",
    "periodic_erfpacht_opstal_beklemming",
}
STRUCTURED_OPTIONAL_KEYS = {"taxable_income"}
STRUCTURED_KEYS = STRUCTURED_AMOUNT_KEYS | STRUCTURED_OPTIONAL_KEYS | {"tax_year"}


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
    woz_value = _finite_float(woz_value, "woz_value", non_negative=True)
    table = EIGENWONINGFORFAIT_TABLE.get(tax_year)
    if table is None:
        raise ValueError(
            f"No reviewed eigenwoningforfait table is available for {tax_year}."
        )

    for lower, upper, pct, fixed_base in table:
        if fixed_base is not None:
            if woz_value > lower:
                return _euro(fixed_base + (woz_value - lower) * pct)
            continue

        if (lower == 0 and 0 <= woz_value <= upper) or (lower < woz_value <= upper):
            return _euro(woz_value * pct)

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
    deductible_costs: float,
    belastbaar_inkomen: Optional[float],
    tax_year: int,
) -> tuple[Optional[bool], Optional[float], list[str]]:
    """Calculate the tariefsaanpassing (rate adjustment) for own-home costs.

    Follows the official Belastingdienst grondslag method. ``deductible_costs``
    is the aftrekbare kosten eigen woning (art. 3.120: the gross deductible
    mortgage interest/costs) — NOT the net eigen-woning saldo. Art. 2.10 lid 2
    applies the correction to these deductible costs, so it can apply even when
    the Hillenregeling leaves a positive eigen-woning result: the official
    Hillen example computes the grondslag as belastbaar inkomen + aftrekbare
    kosten - drempel with the gross costs added back.
    ``belastbaar_inkomen`` is the belastbaar inkomen uit werk en woning AFTER
    the eigen-woning result (including the Hillenregeling) — NOT the income
    before the eigen-woning deduction. The grondslag is:

        grondslag = min(afgetrokken eigenwoningkosten,
                        belastbaar_inkomen + afgetrokken eigenwoningkosten
                            - drempelbedrag hoogste schijf)
        adjustment = round(grondslag * (schijf3_rate - cap_rate), 2)

    The grondslag is capped at the deductible eigen-woning costs (art. 2.10
    lid 2 Wet IB 2001), so the correction can never exceed rate_diff x the
    deductible costs. It applies only when income WITHOUT the deduction
    (belastbaar_inkomen + costs) exceeds the drempel.

    Returns (applies, amount, warnings).
    """
    warnings: list[str] = []
    deductible_costs = _finite_float(
        deductible_costs,
        "deductible_costs",
        non_negative=True,
    )
    if belastbaar_inkomen is not None:
        belastbaar_inkomen = _finite_float(
            belastbaar_inkomen,
            "belastbaar_inkomen",
            non_negative=False,
        )
    params = TARIEFSAANPASSING.get(tax_year)
    if params is None:
        return (
            None,
            None,
            [
                f"No reviewed tariefsaanpassing parameters are available for {tax_year}."
            ],
        )

    if deductible_costs == 0:
        # No deductible eigen-woning costs, so there is nothing for the rate
        # adjustment to correct — regardless of income.
        return (False, 0.0, warnings)

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
    rate_diff_dec = Decimal(str(params["schijf3_rate"])) - Decimal(str(params["cap_rate"]))
    rate_diff = float(rate_diff_dec)
    adjustment = _cents(Decimal(str(base)) * rate_diff_dec)
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
    eigenwoningforfait = _finite_float(
        eigenwoningforfait,
        "eigenwoningforfait",
        non_negative=True,
    )
    mortgage_interest = _finite_float(
        mortgage_interest,
        "mortgage_interest",
        non_negative=True,
    )
    if tax_year not in HILLENREGELING_REMAINING:
        raise ValueError(
            f"No reviewed Hillenregeling percentage is available for {tax_year}."
        )
    remaining_decimal = HILLENREGELING_REMAINING[tax_year]
    remaining_pct = float(remaining_decimal)

    if eigenwoningforfait <= mortgage_interest:
        # Forfait does not exceed interest — Hillenregeling does not apply
        return (False, 0.0, remaining_pct)

    # Excess forfait that would otherwise be added to income
    excess = eigenwoningforfait - mortgage_interest
    correction = int(
        (Decimal(str(excess)) * remaining_decimal).to_integral_value(
            rounding=ROUND_HALF_UP
        )
    )

    return (True, correction, remaining_pct)


def _money(value: Decimal) -> str:
    """Render a reviewed amount consistently in structured output."""
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _fits_float(value: Decimal) -> bool:
    """Return whether legacy helpers and money output can represent this amount."""
    try:
        value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return math.isfinite(float(value))
    except (ArithmeticError, OverflowError, ValueError):
        return False


def _structured_error_result(errors: list[str]) -> dict:
    """Return the stable structured-output shape when inputs cannot be checked."""
    return {
        "errors": errors,
        "total_deductible_own_home_costs": None,
        "box1_balance_components": {},
        "hillen_deduction": None,
        "box1_own_home_balance": None,
        "review_adjustments": {},
        "check_performed_by": "checked_by_script",
    }


def validate(payload: dict) -> dict:
    """Check arithmetic for explicit, already-reviewed ordinary-home amounts.

    The agent owns evidence completeness, tax-year matching, eligibility,
    qualification, ownership allocation, and complex-home decisions. This
    function accepts only the amounts resulting from those decisions and checks
    their addition, Hillen calculation, own-home balance, and separate
    tariefsaanpassing review value.
    """
    if not isinstance(payload, dict):
        return _structured_error_result(["payload must be a mapping"])

    errors: list[str] = []
    unknown = sorted(set(payload) - STRUCTURED_KEYS)
    if unknown:
        errors.append("unknown keys: " + ", ".join(unknown))

    missing = sorted((STRUCTURED_AMOUNT_KEYS | {"tax_year"}) - set(payload))
    if missing:
        errors.append("missing required keys: " + ", ".join(missing))

    tax_year = payload.get("tax_year")
    if isinstance(tax_year, bool) or not isinstance(tax_year, int):
        errors.append("tax_year must be an integer")
    elif tax_year not in HILLENREGELING_REMAINING or tax_year not in TARIEFSAANPASSING:
        errors.append(f"no reviewed own-home parameters are available for {tax_year}")

    amounts: dict[str, Decimal] = {}
    for key in sorted(STRUCTURED_AMOUNT_KEYS | STRUCTURED_OPTIONAL_KEYS):
        if key not in payload or payload[key] is None:
            continue
        try:
            amount = Decimal(str(payload[key]))
        except Exception:
            errors.append(f"{key} must be a finite amount")
            continue
        if not amount.is_finite() or not _fits_float(amount):
            errors.append(f"{key} must be a finite amount")
        elif amount < 0 and key != "taxable_income":
            errors.append(f"{key} must not be negative")
        else:
            amounts[key] = amount

    if errors:
        return _structured_error_result(errors)

    total_costs = sum(
        (
            amounts["mortgage_interest"],
            amounts["qualifying_financing_costs"],
            amounts["periodic_erfpacht_opstal_beklemming"],
        ),
        Decimal("0"),
    )
    forfait = amounts["eigenwoningforfait"]
    if not _fits_float(total_costs) or not _fits_float(forfait - total_costs):
        return _structured_error_result(
            ["accepted amounts produce a total outside the supported numeric range"]
        )
    hillen_applies, hillen_amount, hillen_remaining = calculate_hillenregeling(
        float(forfait), float(total_costs), tax_year
    )
    hillen = Decimal(str(hillen_amount))
    balance = forfait - total_costs - hillen

    taxable_income = amounts.get("taxable_income")
    if taxable_income is not None and not _fits_float(taxable_income + balance):
        return _structured_error_result(
            ["accepted amounts produce a total outside the supported numeric range"]
        )
    belastbaar = float(taxable_income + balance) if taxable_income is not None else None
    adjustment_applies, adjustment_amount, warnings = calculate_tariefsaanpassing(
        float(total_costs), belastbaar, tax_year
    )

    return {
        "errors": [],
        "total_deductible_own_home_costs": _money(total_costs),
        "box1_balance_components": {
            "eigenwoningforfait": _money(forfait),
            "total_deductible_own_home_costs": _money(total_costs),
            "hillen_deduction": _money(hillen),
        },
        "hillen_deduction": _money(hillen),
        "hillen_applies": hillen_applies,
        "hillen_remaining_percentage": str(
            Decimal(str(hillen_remaining)) * Decimal("100")
        ),
        "box1_own_home_balance": _money(balance),
        "review_adjustments": {
            "tariefsaanpassing": {
                "applies": adjustment_applies,
                "amount": None if adjustment_amount is None else _money(Decimal(str(adjustment_amount))),
                "warnings": warnings,
            }
        },
        "check_performed_by": "checked_by_script",
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def parse_args(argv: list[str]) -> dict:
    """Parse only explicit, already-reviewed ordinary-home amounts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tax-year", required=True, type=int)
    parser.add_argument("--eigenwoningforfait", required=True)
    parser.add_argument("--mortgage-interest", required=True)
    parser.add_argument("--qualifying-financing-costs", required=True)
    parser.add_argument(
        "--periodic-erfpacht-opstal-beklemming",
        required=True,
    )
    parser.add_argument(
        "--taxable-income",
        help=(
            "Box 1 taxable income before applying the accepted own-home balance; "
            "used only for the separate tariefsaanpassing check"
        ),
    )
    args = parser.parse_args(argv)
    return {
        key: value
        for key, value in vars(args).items()
        if value is not None
    }


def main(argv: Optional[list[str]] = None) -> int:
    result = validate(parse_args(sys.argv[1:] if argv is None else argv))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
