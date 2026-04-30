#!/usr/bin/env python3
"""
classify_box3_assets.py

Classify assets into box 3 categories: banktegoeden, overige_bezittingen, schulden.
Takes a YAML or JSON file as input.

Usage:
    python classify_box3_assets.py <input_file>

Input format (JSON or YAML-style):
    [
        {"name": "ING Spaarrekening", "type_hint": "savings", "value": 50000, "owner": "taxpayer"},
        {"name": "DEGIRO Aandelen", "type_hint": "shares", "value": 30000, "owner": "taxpayer"},
        ...
    ]

Output: classified list with confidence scores, printed as JSON to stdout.
"""

import json
import sys
import os
import re


# Classification keyword rules (lowercase matching)
BANKTEGOEDEN_KEYWORDS = [
    "spaar", "spaargeld", "spaarrekening",
    "bank", "bankrekening", "betaalrekening",
    "rekening",
    "deposit", "deposito",
    "savings", "current account",
]

OVERIGE_BEZITTINGEN_KEYWORDS = [
    "aandeel", "aandelen", "shares", "stock",
    "obligatie", "obligaties", "bonds",
    "belegging", "beleggingsfonds", "mutual fund", "fund",
    "etf", "exchange-traded",
    "crypto", "cryptocurrency", "bitcoin", "ethereum",
    "vastgoed", "real estate", "property", "onroerend",
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


def match_keywords(text, keywords):
    """Check how many keywords match in the given text. Returns match count."""
    text_lower = text.lower()
    count = 0
    for kw in keywords:
        if kw.lower() in text_lower:
            count += 1
    return count


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
            return TYPE_HINT_MAP[hint_lower], 0.95, flags

    # Step 2: Keyword matching on name + type_hint combined
    combined_text = f"{name} {type_hint}"

    bank_score = match_keywords(combined_text, BANKTEGOEDEN_KEYWORDS)
    overige_score = match_keywords(combined_text, OVERIGE_BEZITTINGEN_KEYWORDS)
    schulden_score = match_keywords(combined_text, SCHULDEN_KEYWORDS)

    scores = {
        "banktegoeden": bank_score,
        "overige_bezittingen": overige_score,
        "schulden": schulden_score,
    }

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
                # Try to parse numeric values
                try:
                    val = int(val)
                except ValueError:
                    try:
                        val = float(val)
                    except ValueError:
                        pass
                current_item[key] = val
        if current_item:
            items.append(current_item)
        if items:
            return items
    except Exception:
        pass

    print("Error: Could not parse input file as JSON or simple YAML.", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python classify_box3_assets.py <input_file>", file=sys.stderr)
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

    # Summary totals
    for cat in ["banktegoeden", "overige_bezittingen", "schulden", "unknown"]:
        results["summary"][cat] = {
            "count": len(results[cat]),
            "total_value": sum(item["value"] for item in results[cat]),
        }

    results["summary"]["manual_review_needed"] = len(results["unknown"]) > 0 or any(
        "MANUAL_REVIEW" in f for f in results["flags"]
    )

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
