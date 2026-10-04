# Annual 2026 output contract

Use the shared single-file and provenance rules and the filled workpack
template. Appendix A uses format `nl-tax-workpack`, version `2.0`, plugin
`0.5.0`, workflow `annual_2026`, tax_year `2026` and exactly the flow section
keys. Actual evidence coverage is recorded in profile rows, not inferred from
the workflow name.

Readiness stays `draft`, including after year-end or generation confirmation.
Keep named source-content, annual-schema and missing year-end-evidence blockers
in the status banner, Open questions, Missing information and Appendix A
`sections.<key>.open`. The owner never writes Appendix B; the field mapper
carries these blockers into its own map when it maps. Each unknown has a Q-ID
and a missing-item link; zero and not-applicable positions have evidence. Cite
only consulted source IDs. No provisional forecast may be silently promoted to
final annual evidence. The 2026 Box 3 own-use addition belongs only to the
actual-return comparison, never to the fictitious return.

The field mapper alone writes the map (`annual_return`, tax year 2026);
conceptual `annual2026.*` rows are `internal_routing`. No manual-entry amount
table or checklist is available. Changed facts invalidate confirmation and
mark any previous output stale. No shell, script, runtime grader or browsing
of authenticated portals is required.

The current shared workflow-scopes.yaml maximum_readiness is draft; retain this
ceiling even if individual evidence, source-content or schema checks are
complete. Only a maintainer activation of the exact scope and reviewed map can
change it. Do not offer a checklist containing entry amounts in this bundle.
