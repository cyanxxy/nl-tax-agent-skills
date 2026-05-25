#!/usr/bin/env python3
"""Render a concise Markdown Box 2 summary for manual-entry workpacks.

Usage:
    python3 summarize_box2_inputs.py input.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from calculate_box2_tax import calculate_from_payload  # noqa: E402
from validate_box2_inputs import validate_box2_input_payload  # noqa: E402


COMPONENT_LABELS = {
    "regular_benefits": "Regular benefits, such as dividends",
    "regular_costs": "Deductible costs against regular benefits",
    "regular_net": "Net regular benefits",
    "disposal_price": "Official net disposal or transfer price",
    "gross_disposal_price": "Gross disposal proceeds before transfer costs",
    "net_disposal_price": "Net disposal or transfer price used",
    "acquisition_price": "Acquisition price",
    "disposal_costs": "Disposal costs used only to derive net price from gross proceeds",
    "disposal_benefit": "Disposal benefit",
    "fictitious_regular_benefit_bv_loan": "Fictitious regular benefit - own BV loan",
    "loss_setoff": "Loss setoff included",
}


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("input JSON must contain an object")
    return data


def _fmt_money(value: Any) -> str:
    return f"EUR {float(value):,.2f}"


def _amount_basis(payload: dict[str, Any]) -> str:
    workflow = payload.get("workflow")
    if workflow == "provisional_2026":
        return "Estimate/baseline-derived for provisional 2026"
    return "Annual 2025 actual from evidence"


def _workflow_label(payload: dict[str, Any], result: dict) -> str:
    workflow = payload.get("workflow") or result.get("workflow")
    if workflow == "provisional_2026":
        return "provisional_2026"
    return "annual_2025"


def render_markdown_summary(payload: dict[str, Any]) -> tuple[str, int]:
    validation = validate_box2_input_payload(payload)
    if validation["errors"]:
        lines = ["# Box 2 input validation", "", "## Errors"]
        lines.extend(f"- {error}" for error in validation["errors"])
        return "\n".join(lines) + "\n", 1

    result = calculate_from_payload(payload)
    workflow = _workflow_label(payload, result)
    basis = _amount_basis(payload)
    split = result["bracket_split"]

    lines = [
        "# Box 2 input summary",
        "",
        f"- Workflow: `{workflow}`",
        f"- Tax year: {result['tax_year']}",
        f"- Amount basis: {basis}",
        "- Product boundary: preparation support for manual Mijn Belastingdienst entry only.",
        "",
        "## Components",
        "",
        "| Component | Basis | Amount |",
        "|---|---|---:|",
    ]

    for key, label in COMPONENT_LABELS.items():
        value = result["components"].get(key)
        if value is None:
            continue
        if float(value) == 0.0 and key not in {
            "regular_benefits",
            "regular_costs",
            "disposal_benefit",
        }:
            continue
        lines.append(f"| {label} | {basis} | {_fmt_money(value)} |")

    lines.extend(
        [
            "",
            "## Indicative tax",
            "",
            f"- Taxable Box 2 income: {_fmt_money(result['taxable_income'])}",
            f"- Lower bracket income: {_fmt_money(split['lower_bracket_income'])} "
            f"at {split['lower_rate'] * 100:.1f}%",
            f"- Upper bracket income: {_fmt_money(split['upper_bracket_income'])} "
            f"at {split['upper_rate'] * 100:.1f}%",
            f"- Gross Box 2 tax: {_fmt_money(result['gross_tax'])}",
            f"- Dividend withholding tax credit: "
            f"{_fmt_money(result['dividend_withholding_credit'])}",
            f"- Net payable/refund-indicative amount: "
            f"{_fmt_money(result['net_payable_or_refund_indicative'])}",
        ]
    )

    if result["loss"]["is_loss"]:
        lines.extend(
            [
                "",
                "## Loss note",
                "",
                f"- Current-year negative Box 2 income: "
                f"{_fmt_money(result['loss']['current_year_loss'])}",
                "- Loss handling is included only as manual-review data.",
            ]
        )

    flags = sorted(set(validation["manual_review_flags"]) | set(result["manual_review_flags"]))
    if flags or validation["warnings"] or result["warnings"]:
        lines.extend(["", "## Manual review", ""])
        for flag in flags:
            lines.append(f"- Flag: `{flag}`")
        for warning in validation["warnings"] + result["warnings"]:
            lines.append(f"- {warning}")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Do not use this helper for login, DigiD handling, browser automation, signing, or submission.",
            "- The official filing environment makes the binding calculation.",
        ]
    )

    return "\n".join(lines) + "\n", 0


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: python3 summarize_box2_inputs.py input.json", file=sys.stderr)
        return 1

    try:
        payload = _load_json(Path(args[0]))
        output, exit_code = render_markdown_summary(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(output, end="")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
