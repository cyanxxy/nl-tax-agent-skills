# Source Refresh Policy

Freshness policies and refresh triggers for the Dutch Tax Skills source register.

## Current implementation note

`scripts/plan_source_refresh.py <scope> [year] --fetch` (e.g. `plan_source_refresh.py all --fetch`; the scope argument is required) is a plan-only refresh reporter. It validates
freshness and allowlist status, then reports which sources would need manual
refresh. It does not make live HTTP requests and does not rewrite source
snapshots. A real refresh requires a developer to retrieve official content,
review it, update the local snapshot, run `build_snapshots.py`, and pass the
validators.

## Freshness policies

Each source in `source-register.yaml` carries a `freshness_policy` field. It is
**free-text developer guidance** describing when to re-verify the source (for
example `"check after Prinsjesdag; rates are fixed for the calendar year once
published"` or `"check monthly; platform docs may change with new releases"`).

Machine enforcement happens in two places, and they interpret the register
differently — both are intentional:

1. **`validate_knowledge_pack.py` (blocking gate).** Derives a staleness
   threshold from the `freshness_policy` text itself. It first checks the
   canonical tokens below, then falls back to keyword scanning of prose
   policies (first/smallest match wins): `monthly` → 31 days, `quarter` → 92,
   `filing season` → 90, `prinsjesdag` → 120, `annual` / `law change` → 365,
   `on demand` → 730, anything else → 365. Season-opening policies
   (`provisional assessment season` / `january`) are calendar events instead of
   rolling windows: the source is stale only when `last_checked` predates the
   most recent January 1 — one re-attestation per year, when the season opens.
   A mandatory source that is stale under its policy FAILS validation.
2. **`plan_source_refresh.py` (refresh planner).** Thresholds by `source_type`
   (table under "Staleness thresholds" below), not by the policy text. It
   reports which sources a developer should re-verify; it does not block.

In both cases, `last_checked` means the date of human review of the local note
against the official source. The plan report emits URL reachability separately
as `url_reachability: not_checked` with `reachability_checked_at: null` and
`last_retrieved_at: null`. Its `reviewed_note_hash_sha256` is a hash of the local
reviewed note; it does not imply that any remote page body was fetched or
archived.

When writing a `freshness_policy`, include one of the recognized cadence
keywords so the blocking gate derives the intended threshold rather than the
365-day default.

### Canonical policy tokens

These fixed tokens are also accepted in `freshness_policy` (they map to
explicit thresholds in `validate_knowledge_pack.py`):

| Token | Threshold | Meaning |
|-------|-----------|---------|
| `refresh-before-1-dec-and-before-filing-season` | 90 days | Re-verify before 1 December (provisional rates published) and before filing season opens (March). |
| `refresh-annually` | 365 days | Re-verify at least once per calendar year (e.g., legislative texts). |
| `refresh-on-law-change` | 365 days | Refresh when the underlying law is amended (Staatsblad / Koninklijk Besluit publication). |
| `refresh-on-demand` | 730 days | Only refreshed when a developer explicitly requests it. |

## Refresh triggers

The following events should trigger a source refresh:

| Trigger                                | Scope to refresh           |
|----------------------------------------|----------------------------|
| New tax year begins                    | `all` (rates and credits may change) |
| Filing season approaches (February)    | `annual` (check for updated guidance) |
| Provisional season opens (January)     | `provisional`              |
| Law amendment published in Staatsblad  | Sources with `source_type: law` |
| Source register validation fails       | Failed entries only        |
| Developer explicitly requests refresh  | As specified by developer  |
| Belastingdienst portal update detected | Affected `official_guidance` entries |

## Staleness thresholds

These thresholds define when a source is considered stale based on `source_type` and `last_checked`:

| Source type          | Stale if last_checked older than | Rationale                              |
|----------------------|----------------------------------|----------------------------------------|
| `official_rates`     | 90 days before filing season     | Rates must be current when taxpayers file |
| `official_guidance`  | 180 days                         | Guidance pages updated periodically    |
| `official_doctrine`  | 180 days                         | Doctrine may change with filing season |
| `law`                | 365 days                         | Laws change less frequently (Staatsblad cycle) |
| `platform_docs`      | 180 days                         | Platform docs may change with releases |
| `developer_reference`| 180 days                         | Developer portal updated quarterly     |
| `methodology`        | 365 days                         | Methodologies change infrequently      |
| `official_algorithm_register` | 365 days              | Algorithm register updated annually    |

`plan_source_refresh.py` emits machine-readable staleness fields for every checked source: `staleness_threshold_days`, `age_days`, and `expires_on` (the date after which the current `last_checked` attestation is stale for that source type). These fields are generated from the register metadata rather than hand-authored per source.

## Filing season dates (reference)

| Activity                           | Typical date           |
|------------------------------------|------------------------|
| Prinsjesdag (budget announcement)  | 3rd Tuesday of September |
| Provisional rates published        | Late November / early December |
| Provisional assessment season      | January onwards        |
| Annual return portal opens         | 1 March                |
| Annual return deadline             | 1 May (extendable)     |
