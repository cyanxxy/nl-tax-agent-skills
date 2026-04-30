# Source Refresh Policy

Freshness policies and refresh triggers for the Dutch Tax Skills source register.

## Freshness policies

Each source in `source-register.yaml` carries a `freshness_policy` field. The refresh pipeline interprets these policies as follows:

### refresh-before-1-dec-and-before-filing-season

Must be refreshed at two checkpoints per year:

1. **Before 1 December** -- when provisional rates are typically published for the upcoming year. This ensures that provisional assessment skills have current rates before taxpayers begin requesting voorlopige aanslagen.
2. **Before filing season starts (March)** -- when the Belastingdienst opens the annual return portal. This ensures annual return skills have the final published rates.

### refresh-annually

Must be refreshed at least once per calendar year. Suitable for sources that change infrequently but should be re-verified yearly (e.g., legislative texts that only change via Staatsblad publication).

### refresh-on-law-change

Refresh when the underlying law is amended. The trigger is a new publication in the Staatsblad or a Koninklijk Besluit on wetten.overheid.nl. This policy applies to legislative sources like the Wet IB 2001 and its uitvoeringsregelingen.

### refresh-on-demand

Only refreshed when explicitly requested by a developer. Used for sources that rarely change or where automated checking adds no value.

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

## Filing season dates (reference)

| Activity                           | Typical date           |
|------------------------------------|------------------------|
| Prinsjesdag (budget announcement)  | 3rd Tuesday of September |
| Provisional rates published        | Late November / early December |
| Provisional assessment season      | January onwards        |
| Annual return portal opens         | 1 March                |
| Annual return deadline             | 1 May (extendable)     |
