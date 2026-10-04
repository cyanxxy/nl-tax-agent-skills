"""Repository-only exact VAT adjustment arithmetic for accepted inputs.

No taxpayer workflow engine or executable helper is installed in the plugin.
These functions do not establish legal eligibility, elect a method, discover
evidence, generate output files, round portal entries, or attest content review.
Constants are read from the canonical draft knowledge notes for rate parity.
"""

from decimal import Decimal, InvalidOperation
from pathlib import Path
import re

import yaml


NOTES = Path(__file__).resolve().parents[3] / "plugins/nl-tax-agent-skills/skills/nl-tax-shared-resources/knowledge/vat-adjustments"


def load_policy():
    policy = {}
    for filename in ("car-private-use.md", "mixed-deduction.md", "revision.md", "bua.md"):
        content = (NOTES / filename).read_text(encoding="utf-8")
        for block in re.findall(r"```yaml\s*\n(.*?)\n```", content, re.S):
            fragment = (yaml.safe_load(block) or {}).get("vat_adjustment_policy", {})
            duplicates = set(policy) & set(fragment)
            if duplicates:
                raise ValueError(f"Duplicated adjustment policy keys: {sorted(duplicates)}")
            policy.update(fragment)
    if not policy:
        raise ValueError("Missing canonical adjustment policy")
    return policy


POLICY = load_policy()
ZERO = Decimal(0)
ONE = Decimal(1)


def decimal(value, *, signed=False):
    """Reject unknown/locale/nonfinite inputs rather than inventing zero."""
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        raise ValueError("Use an exact decimal string, integer or Decimal")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("Invalid exact decimal") from exc
    if not result.is_finite() or (not signed and result < ZERO):
        raise ValueError("Amount must be finite and nonnegative")
    return result


def fraction(value):
    result = decimal(value)
    if result > ONE:
        raise ValueError("Fraction must be between zero and one")
    return result


def count(value):
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("Count must be a positive integer")
    return value


def accepted_deduction(invoice_vat, business_share, taxable_business_share):
    """Two independently accepted shares, with distinct denominators."""
    return decimal(invoice_vat) * fraction(business_share) * fraction(taxable_business_share)


def turnover_pro_rata(deductible_turnover, relevant_total_turnover):
    """Accepted turnover scope only; upward whole-percent rounding, not euros.

This rule does not apply to actual-use or private-use allocation keys.
"""
    numerator, denominator = map(decimal, (deductible_turnover, relevant_total_turnover))
    if denominator == ZERO or numerator > denominator:
        raise ValueError("Pro-rata needs positive relevant total and numerator <= total")
    if POLICY["turnover_pro_rata_rounding"] != "ceiling":
        raise ValueError("Unsupported canonical pro-rata rounding rule")
    scale = count(POLICY["turnover_pro_rata_percentage_scale"])
    # Use exact integer ratios so Decimal's context cannot round a value just
    # above a whole percent back onto that boundary before the ceiling.
    n_value, n_scale = numerator.as_integer_ratio()
    d_value, d_scale = denominator.as_integer_ratio()
    upper, lower = n_value * scale * d_scale, n_scale * d_value
    percentage = (upper + lower - 1) // lower
    return Decimal(percentage) / Decimal(scale)


def entitlement_delta(invoice_vat, final_deductible_share, prior_net_claim):
    vat = decimal(invoice_vat)
    claimed = decimal(prior_net_claim)
    if claimed > vat:
        raise ValueError("Prior net deduction exceeds this pool's invoice VAT")
    return vat * fraction(final_deductible_share) - claimed


def car_fraction(first_use_year, adjustment_year, purchase_vat_deducted):
    count(first_use_year)
    count(adjustment_year)
    if not isinstance(purchase_vat_deducted, bool) or adjustment_year < first_use_year:
        raise ValueError("Confirm acquisition deduction and first-use chronology")
    key = "car_reduced_fraction" if (
        not purchase_vat_deducted or
        adjustment_year - first_use_year > POLICY["car_following_years"]
    ) else "car_standard_fraction"
    return Decimal(POLICY[key])


def owned_car_cap(operating_vat_deducted, acquisition_vat_deducted,
                  purchase_year, first_use_year, adjustment_year):
    """Plain acquired-and-first-used-same-year cap after acquisition year.

First-acquisition-year, lease and mismatched dates require an accepted cap
instead of this recipe. Neither cap component is reduced a second time for
taxable/exempt use: both inputs are VAT actually deducted.
"""
    for year in (purchase_year, first_use_year, adjustment_year):
        count(year)
    operating = decimal(operating_vat_deducted)
    acquisition = decimal(acquisition_vat_deducted)
    if purchase_year != first_use_year or adjustment_year <= purchase_year:
        raise ValueError("This cap recipe requires a post-acquisition year and matching dates")
    component = ZERO
    if acquisition and adjustment_year - first_use_year <= POLICY["car_following_years"]:
        component = acquisition / Decimal(POLICY["car_acquisition_parts"])
    return operating + component


def car_forfait(catalogue_including_vat_bpm, applicable_fraction,
                available_units, year_units, taxable_share, accepted_cap):
    """Time availability is an exact integer ratio (e.g. 4 of 12 months).

The division by ``year_units`` happens last so that a time-apportioned
whole-euro result (10000 x 0.027 x 4/12 = 90) stays exact instead of
becoming 89.999... and losing a euro under a taxpayer-favourable floor.
"""
    rate = fraction(applicable_fraction)
    valid = {Decimal(POLICY["car_standard_fraction"]), Decimal(POLICY["car_reduced_fraction"])}
    if rate not in valid:
        raise ValueError("Car forfait fraction lacks parity with its source note")
    available, year = count(available_units), count(year_units)
    if available > year:
        raise ValueError("Available time cannot exceed the year")
    raw = (decimal(catalogue_including_vat_bpm) * rate * Decimal(available)
           * fraction(taxable_share) / Decimal(year))
    return {"uncapped": raw, "adjustment": min(raw, decimal(accepted_cap))}


def actual_private_use(annual_eligible_vat_component, private_distance, total_distance):
    private, total = decimal(private_distance), decimal(total_distance)
    if total == ZERO or private > total:
        raise ValueError("Private-distance allocation needs positive total and private <= total")
    return decimal(annual_eligible_vat_component) * private / total


def later_revision(invoice_vat, original_deductible_share, current_deductible_share,
                   revision_years, year_offset, elapsed_units=1, year_units=1):
    """Signed extra deduction; only later years, measured from original use.

``elapsed_units`` out of ``year_units`` is the elapsed part of the bookyear of
delivery (start of the bookyear to the delivery date), for example 9 of 12
months. The part after delivery belongs to ``disposal_revision`` so that no
part of the window is revised twice. Whole units are taken and divided once,
last, so a month split such as 2/12 stays exact.
"""
    allowed_windows = {POLICY[k] for k in (
        "movable_revision_years", "property_revision_years", "service_revision_years")}
    if isinstance(revision_years, bool) or not isinstance(revision_years, int) or revision_years not in allowed_windows:
        raise ValueError("Revision window lacks parity with the source note")
    count(year_offset)
    if year_offset >= revision_years:
        raise ValueError("Outside the later-year revision window")
    elapsed, year = count(elapsed_units), count(year_units)
    if elapsed > year:
        raise ValueError("Elapsed time cannot exceed the bookyear")
    original, current = fraction(original_deductible_share), fraction(current_deductible_share)
    difference = current - original
    tolerance = Decimal(POLICY["revision_tolerance_fraction"]) * original
    if abs(difference) <= tolerance:
        return ZERO
    # Multiply everything first and divide once, last, to keep exact results exact.
    return (decimal(invoice_vat) * Decimal(elapsed) * difference
            / (Decimal(revision_years) * Decimal(year)))


def disposal_revision(invoice_vat, original_deductible_share,
                      disposal_deductible_share, remaining_units, revision_years,
                      year_units=1):
    """Accepted taxable/exempt sale treatment and the remaining window.

``remaining_units`` counts the remaining part of the revision window in
``year_units`` per year, for example 58 months with ``year_units=12`` for
four years and ten months. All multiplication happens before one division.
"""
    windows = {POLICY["movable_revision_years"], POLICY["property_revision_years"]}
    if isinstance(revision_years, bool) or not isinstance(revision_years, int) or revision_years not in windows:
        raise ValueError("Invalid revision window")
    remaining, year = count(remaining_units), count(year_units)
    if remaining > revision_years * year:
        raise ValueError("Remaining window exceeds complete revision window")
    return (decimal(invoice_vat) * Decimal(remaining)
            * (fraction(disposal_deductible_share) - fraction(original_deductible_share))
            / (Decimal(revision_years) * Decimal(year)))


def bua_repayment(annual_beneficiary_cost_ex_vat, covered_vat_deducted,
                  related_contribution_vat_accounted):
    """Ordinary accepted BUA pool; contributions do not reduce threshold cost."""
    cost, vat, contribution = map(decimal, (annual_beneficiary_cost_ex_vat,
        covered_vat_deducted, related_contribution_vat_accounted))
    if cost <= Decimal(POLICY["bua_threshold_ex_vat"]):
        return ZERO
    return max(ZERO, vat - contribution)


def _margin_tax(gross_margin, confirmed_rate):
    margin, rate = decimal(gross_margin, signed=True), fraction(confirmed_rate)
    if rate == ZERO:
        raise ValueError("Confirm a positive applicable margin-goods rate")
    positive = max(margin, ZERO)
    vat = positive * rate / (ONE + rate)
    return {"gross_margin": margin, "vat": vat,
            "net_taxable_margin": positive - vat,
            "negative_margin": min(margin, ZERO)}


def individual_margin(items, confirmed_rate):
    """One accepted rate pool, never net losses against positive item margins."""
    positive = ZERO
    for sale, linked_purchase in items:
        positive += max(ZERO, decimal(sale) - decimal(linked_purchase))
    return _margin_tax(positive, confirmed_rate)


def global_margin(period_sales, period_purchases, unused_same_year_loss, confirmed_rate):
    """One accepted rate pool; carry losses must be previously unused/accepted."""
    margin = decimal(period_sales) - decimal(period_purchases) - decimal(unused_same_year_loss)
    return _margin_tax(margin, confirmed_rate)


def verify_unique_components(component_ids):
    """Detect accidentally repeated evidence components before aggregation."""
    if any(not isinstance(x, str) or not x for x in component_ids):
        raise ValueError("Each component needs an anonymous nonempty label")
    if len(component_ids) != len(set(component_ids)):
        raise ValueError("An adjustment component was included more than once")
    return True
