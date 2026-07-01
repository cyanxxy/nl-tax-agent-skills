#!/usr/bin/env python3
"""
classify_box3_assets.py

Classify assets into box 3 categories: banktegoeden, overige_bezittingen, schulden.
Takes a YAML or JSON file as input.

Usage:
    python3 classify_box3_assets.py <input_file>

Input format (JSON or YAML-style):
    [
        {"name": "ING Spaarrekening", "type_hint": "savings", "value": 50000, "owner": "taxpayer"},
        {"name": "DEGIRO Aandelen", "type_hint": "shares", "value": 30000, "owner": "taxpayer"},
        ...
    ]

Output: classified list with confidence scores, printed as JSON to stdout.
"""

import json
import math
import sys
import os
import re


# Classification keyword rules (lowercase matching)
BANKTEGOEDEN_KEYWORDS = [
    "spaar", "spaargeld", "spaarrekening",
    "bank", "bankrekening", "betaalrekening",
    "rekening",
    "deposit", "deposito",
    "premiedepot",
    "derdengelden", "derdenrekening",
    "savings", "current account",
]

OVERIGE_BEZITTINGEN_KEYWORDS = [
    "aandeel", "aandelen", "aandelenfonds", "aandelenportefeuille",
    "shares", "stock",
    "obligatie", "obligaties", "obligatiefonds", "bonds",
    "belegging", "beleggingsfonds", "beleggingsrekening",
    "beleggingsportefeuille", "indexfonds", "mutual fund", "fund",
    "effecten", "effectenrekening", "effectenportefeuille",
    "etf", "exchange-traded",
    "crypto", "cryptocurrency", "bitcoin", "ethereum",
    "vastgoed", "vastgoedfonds", "vastgoedfondsen",
    "real estate", "property", "onroerend",
    "lening verstrekt", "vordering", "receivable", "loan given",
    "kunst", "art", "collectibles",
]

SCHULDEN_KEYWORDS = [
    "lening", "persoonlijke lening", "personal loan", "loan",
    "schuld", "schulden", "debt",
    "krediet", "credit", "creditcard", "credit card",
    "studie", "studieschuld", "study debt", "bkr",
]

# Type hint mappings (more reliable than name-only matching)
TYPE_HINT_MAP = {
    # Banktegoeden
    "savings": "banktegoeden",
    "current_account": "banktegoeden",
    "deposit": "banktegoeden",
    "bank": "banktegoeden",
    "spaarrekening": "banktegoeden",
    "betaalrekening": "banktegoeden",
    "premiedepot": "banktegoeden",
    "vve_reserve": "banktegoeden",
    "reservefonds_vve": "banktegoeden",
    "notary_third_party_account": "banktegoeden",
    "bailiff_third_party_account": "banktegoeden",
    # Overige bezittingen
    "shares": "overige_bezittingen",
    "bonds": "overige_bezittingen",
    "mutual_fund": "overige_bezittingen",
    "etf": "overige_bezittingen",
    "crypto": "overige_bezittingen",
    "real_estate": "overige_bezittingen",
    "property": "overige_bezittingen",
    "loan_given": "overige_bezittingen",
    "receivable": "overige_bezittingen",
    "investment": "overige_bezittingen",
    "aandelen": "overige_bezittingen",
    "belegging": "overige_bezittingen",
    "vastgoed": "overige_bezittingen",
    # Schulden
    "loan": "schulden",
    "debt": "schulden",
    "credit_card": "schulden",
    "study_debt": "schulden",
    "personal_loan": "schulden",
    "schuld": "schulden",
    "lening": "schulden",
    "krediet": "schulden",
}


BANKTEGOEDEN_EDGE_CASES = [
    ("VvE reserve share", ("vve", "reserve")),
    ("premium deposit", ("premiedepot",)),
    ("notary third-party account", ("notaris", "derdengeld")),
    ("notary third-party account", ("notaris", "derden")),
    ("bailiff third-party account", ("deurwaarder", "derdengeld")),
    ("bailiff third-party account", ("deurwaarder", "derden")),
]


def match_keywords(text, keywords):
    """Check how many keywords match in the given text. Returns match count.

    Matching is word-boundary based so that, for example, "spaar" does not
    match inside "Spaarvarken". Multi-word keywords keep their internal spaces.
    """
    text_lower = text.lower()
    count = 0
    for kw in keywords:
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        if re.search(pattern, text_lower):
            count += 1
    return count


def _score_categories(text):
    """Return per-category keyword scores for the given text."""
    return {
        "banktegoeden": match_keywords(text, BANKTEGOEDEN_KEYWORDS),
        "overige_bezittingen": match_keywords(text, OVERIGE_BEZITTINGEN_KEYWORDS),
        "schulden": match_keywords(text, SCHULDEN_KEYWORDS),
    }


def validate_asset(asset):
    """Validate a single asset's value and owner fields.

    Returns a list of MANUAL_REVIEW flag strings for any data-quality problem.
    Does not classify; complements classify_asset.
    """
    flags = []

    if "value" not in asset or asset.get("value") is None:
        alternate = next(
            (key for key in ("amount", "balance") if asset.get(key) is not None),
            None,
        )
        if alternate is not None:
            flags.append(
                f"MANUAL_REVIEW: value missing; found alternate key '{alternate}'"
            )
        else:
            flags.append("MANUAL_REVIEW: value missing")
    else:
        value = asset.get("value")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            flags.append("MANUAL_REVIEW: value is not numeric")
        elif not math.isfinite(value):
            flags.append("MANUAL_REVIEW: value is not a finite number")
        elif value < 0:
            flags.append("MANUAL_REVIEW: value is negative")

    if not asset.get("owner"):
        flags.append("MANUAL_REVIEW: owner missing")

    return flags


def classify_asset(asset):
    """
    Classify a single asset into a box 3 category.

    Returns: (category, confidence, flags)
        category: 'banktegoeden' | 'overige_bezittingen' | 'schulden' | 'unknown'
        confidence: float 0.0 - 1.0
        flags: list of strings noting any issues
    """
    name = asset.get("name", "")
    type_hint = asset.get("type_hint", "")
    flags = []

    # Step 1: Try type_hint mapping (highest confidence)
    if type_hint:
        hint_lower = type_hint.lower().strip().replace(" ", "_")
        if hint_lower in TYPE_HINT_MAP:
            hint_category = TYPE_HINT_MAP[hint_lower]
            # Cross-check the name's keywords against the hint. If a *different*
            # category scores at least as high as the hint's own category on the
            # name keywords, the hint may be wrong (e.g. "loan receivable from
            # friend" + type_hint "loan" — "receivable" points at
            # overige_bezittingen). Downgrade and flag for manual review.
            name_scores = _score_categories(name)
            name_max = max(name_scores.values())
            if name_max > 0:
                contradicting = [
                    cat
                    for cat, s in name_scores.items()
                    if cat != hint_category and s >= name_scores[hint_category]
                ]
                if contradicting:
                    flags.append(
                        f"MANUAL_REVIEW: type_hint '{type_hint}' contradicts "
                        f"name keywords (name suggests {', '.join(sorted(contradicting))})"
                    )
                    return hint_category, 0.5, flags
            return hint_category, 0.95, flags

    # Step 2: Keyword matching on name + type_hint combined
    combined_text = f"{name} {type_hint}"
    combined_lower = combined_text.lower()

    for label, required_terms in BANKTEGOEDEN_EDGE_CASES:
        if all(term in combined_lower for term in required_terms):
            flags.append(f"Resolved official banktegoeden edge case: {label}")
            return "banktegoeden", 0.85, flags

    scores = _score_categories(combined_text)

    max_score = max(scores.values())

    if max_score == 0:
        flags.append("MANUAL_REVIEW: no keywords matched; classification uncertain")
        return "unknown", 0.0, flags

    # Check for ambiguity (multiple categories with equal top score)
    top_categories = [cat for cat, s in scores.items() if s == max_score]

    if len(top_categories) > 1:
        # Ambiguous — handle special cases
        # "lening" alone could be schulden or overige_bezittingen (loan given)
        if "schulden" in top_categories and "overige_bezittingen" in top_categories:
            # Check for indicators of loan given vs loan taken
            combined_lower = combined_text.lower()
            if any(kw in combined_lower for kw in ["verstrekt", "given", "vordering", "receivable", "uitgeleend"]):
                flags.append("Resolved ambiguity: classified as loan given (overige_bezittingen)")
                return "overige_bezittingen", 0.6, flags
            else:
                flags.append("MANUAL_REVIEW: ambiguous between schulden and overige_bezittingen")
                return "schulden", 0.4, flags

        flags.append(f"MANUAL_REVIEW: ambiguous between {', '.join(top_categories)}")
        return top_categories[0], 0.4, flags

    category = top_categories[0]
    # Confidence based on keyword match strength
    confidence = min(0.5 + (max_score * 0.15), 0.85)

    return category, confidence, flags


def _coerce_scalar(val):
    """Coerce a simple-YAML scalar string to a number when it is numeric.

    Handles plain integers/decimals and comma thousand separators (e.g.
    "50,000" -> 50000, "1.234.567" -> 1234567, Dutch "50.000,50" -> 50000.5).
    Genuinely non-numeric text is returned unchanged; downstream validate_asset
    then flags it for manual review rather than crashing on arithmetic.
    """
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    stripped = val.strip()
    # Plain comma thousand separators: 50,000 / 1,234,567
    if re.fullmatch(r"-?\d{1,3}(,\d{3})+", stripped):
        return int(stripped.replace(",", ""))
    # Dot thousand separators: 50.000 / 1.234.567
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+", stripped):
        return int(stripped.replace(".", ""))
    # Dutch locale with decimal comma: 50.000,50 or 50000,50
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})*,\d+", stripped) or re.fullmatch(
        r"-?\d+,\d+", stripped
    ):
        return float(stripped.replace(".", "").replace(",", "."))
    return val


def load_input(file_path):
    """Load input from a JSON or YAML-style file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Try JSON first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Try simple YAML-like parsing (list of dicts with - key: value syntax)
    # For full YAML support, the knowledge pack would need PyYAML,
    # but we stick to standard library only.
    # Attempt a basic parse for simple YAML lists.
    try:
        # If it looks like YAML, try a minimal parse
        items = []
        current_item = {}
        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- "):
                if current_item:
                    items.append(current_item)
                current_item = {}
                line = line[2:].strip()
            if ":" in line:
                key, _, val = line.partition(":")
                key = key.strip().strip('"').strip("'")
                val = val.strip().strip('"').strip("'")
                # Coerce numeric values (incl. thousand separators); leave
                # non-numeric text as-is for downstream manual-review flagging.
                val = _coerce_scalar(val)
                current_item[key] = val
        if current_item:
            items.append(current_item)
        if items:
            return items
    except Exception as exc:
        print(f"Warning: simple-YAML fallback parse failed: {exc}", file=sys.stderr)

    print("Error: Could not parse input file as JSON or simple YAML.", file=sys.stderr)
    sys.exit(1)


def main():
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("classify_box3_assets.py — classify assets into box 3 categories")
        print("Usage: python3 classify_box3_assets.py <input_file>  (JSON or simple YAML list)")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Usage: python3 classify_box3_assets.py <input_file>", file=sys.stderr)
        print("", file=sys.stderr)
        print("Input file should be JSON or simple YAML with a list of assets.", file=sys.stderr)
        print("Each asset: {name, type_hint, value, owner}", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    assets = load_input(input_file)

    if not isinstance(assets, list):
        print("Error: Input must be a list of asset objects.", file=sys.stderr)
        sys.exit(1)

    results = {
        "banktegoeden": [],
        "overige_bezittingen": [],
        "schulden": [],
        "unknown": [],
        "summary": {},
        "flags": [],
    }

    for asset in assets:
        category, confidence, flags = classify_asset(asset)
        flags = list(flags) + validate_asset(asset)
        classified = {
            "name": asset.get("name", "unnamed"),
            "value": asset.get("value", 0),
            "owner": asset.get("owner", "unknown"),
            "type_hint": asset.get("type_hint", ""),
            "classified_as": category,
            "confidence": confidence,
        }
        if flags:
            classified["flags"] = flags
            results["flags"].extend(
                [f"{asset.get('name', 'unnamed')}: {f}" for f in flags]
            )

        results[category].append(classified)

    # Summary totals (skip non-numeric values flagged for manual review)
    for cat in ["banktegoeden", "overige_bezittingen", "schulden", "unknown"]:
        results["summary"][cat] = {
            "count": len(results[cat]),
            "total_value": sum(
                item["value"]
                for item in results[cat]
                if isinstance(item["value"], (int, float))
                and not isinstance(item["value"], bool)
                and math.isfinite(item["value"])
            ),
        }

    results["summary"]["manual_review_needed"] = len(results["unknown"]) > 0 or any(
        "MANUAL_REVIEW" in f for f in results["flags"]
    )

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
