---
name: nl-tax-source-refresh
description: Refresh official Dutch tax source snapshots and validate the local knowledge pack. Developer-only.
argument-hint: "[annual|provisional|box3|all] [year]"
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Read Grep Write Edit Bash(python ${CLAUDE_SKILL_DIR}/../nl-tax-source-refresh/scripts/*.py *)
---

# NL Tax Source Refresh

Developer-only maintenance skill that refreshes official source snapshots from allowlisted domains, rebuilds the local knowledge pack, and validates the source register for completeness and freshness.

## When to use

- New tax year begins (rates and credits may change)
- Filing season approaches (check for updated guidance)
- Law amendment published (check wetten.overheid.nl)
- Source register validation fails (missing or stale sources)
- Developer explicitly requests a source refresh

## What this skill does

1. **Read** `source-register.yaml`
2. **For each source entry** matching the requested scope (`annual`, `provisional`, `box3`, `all`):
   a. Check freshness against `freshness_policy`
   b. If stale or forced: fetch from official URL (allowlisted domains only)
   c. Create/update snapshot in knowledge directory
   d. Update snapshot metadata (hash, timestamp, review status)
3. **Validate**:
   - All mandatory sources present
   - No sources missing snapshot files
   - No snapshots without source register entries
   - Freshness policies met
4. **Report** changes and validation results

## Scope arguments

| Argument        | Sources matched                                       |
|-----------------|-------------------------------------------------------|
| `annual`        | Sources with `workflow: annual_return`                |
| `provisional`   | Sources with `workflow: provisional_assessment`       |
| `box3`          | Sources with IDs containing `box3`                    |
| `all`           | Every source in the register                          |

An optional year argument filters by `tax_year` (e.g., `all 2025`).

## Scripts

| Script                         | Purpose                                          |
|-------------------------------|--------------------------------------------------|
| `fetch_sources.py`            | Check freshness and report what needs refreshing |
| `build_snapshots.py`          | Verify snapshot files and compute content hashes |
| `validate_source_register.py` | Validate register entries for correctness        |
| `validate_knowledge_pack.py`  | Cross-reference knowledge files against register |

## Safety

- Only fetches from allowlisted official domains (see `reference/official-domain-allowlist.md`)
- HTTPS only, no redirects to non-allowlisted domains
- Rate limiting: max 1 request per 2 seconds to any single domain
- Never reads or writes `workspace/`, `uploads/`, `evidence/`
- Developer-only: `disable-model-invocation: true`
- Does NOT touch taxpayer data

## Output

This skill prints validation results and change reports to stdout. It does not produce taxpayer-facing output.
