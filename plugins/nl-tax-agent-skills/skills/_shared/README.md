# Shared Tax Knowledge Pack

This directory contains shared resources used by all NL tax skills.

## Structure

```
_shared/
  source-register.yaml      # Mandatory source registry — every cited source must be listed here
  knowledge/
    platform/                # Claude Code / Agent Skills platform documentation
    laws/                    # Dutch legal backbone (Wet IB 2001, AWR, Uitvoeringsregeling, Uitvoeringsbesluit)
    methods/                 # Rule-authoring methodology (Regelspraak)
    security/                # machtigen (authorization) guidance
    compat/                  # ODB compatibility references (future awareness only)
    own-home/                # Eigen woning, hypotheekrenteaftrek, eigenwoningforfait
    partners/                # Fiscal partnership and allocation
    aow/                     # AOW-leeftijd / state-pension-age reference
    years/
      2025/
        annual/              # Annual return 2025 knowledge (rates, credits, filing flow, deductions)
        box2/                # Box 2 2025 substantial-interest (aanmerkelijk belang) knowledge
        box3/                # Box 3 2025 knowledge (fictitious + actual return)
        entrepreneur/        # Winst uit onderneming 2025 (eenmanszaak / ZZP: ondernemersaftrek, MKB-winstvrijstelling, investeringsaftrek)
      2026/
        provisional/         # Voorlopige aanslag 2026 knowledge (request, change, review, stopzetten)
  templates/                 # Shared output templates
  eval-fixtures/             # Evaluation scenarios and expected outputs
```

## Rules

1. Every rule note must reference at least one `source_id` from `source-register.yaml`.
2. Taxpayer-facing skills read snapshots from `knowledge/`, never live websites.
3. Only `nl-tax-source-refresh` may fetch from official domains.
4. Year-specific files must include `tax_year`, `source_ids`, `last_reviewed`, and `review_status`.
5. No real taxpayer data may appear in any file under `_shared/`.

`source-register.yaml` uses `snapshot_path` as the path to a local reviewed
note. `last_checked` is the date of a human review of that note against its
official source. The `_snapshot-metadata.yaml` files record
`reviewed_note_hash_sha256` for the local reviewed note; they do not hash, fetch,
or archive a remote page body, and URL reachability is tracked separately.
