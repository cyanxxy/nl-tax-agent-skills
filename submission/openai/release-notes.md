# OpenAI Plugin Directory release 0.3.1

NL Tax Agent Skills is a skills-only plugin for preparing source-traceable Dutch
individual income-tax workpacks for manual Mijn Belastingdienst entry. It
supports annual 2025 preparation, the 2026 voorlopige aanslag request, change,
review, and stopzetten workflows, and read-only rule questions for both years.

This release removes all executable code from the plugin. The package ships
Markdown and YAML only: no scripts, hooks, MCP servers, or package installs, and
no shell or Python is needed. Every arithmetic and structural check is now an
agent checklist recorded as `checked_by_agent`. The directory short description
is now "Conversational Dutch tax prep", within the 30-character submission limit.

No tax rule, rate, threshold, or cited source changed. Four sources were
re-verified against the live Belastingdienst pages and still match.

Annual 2025 and provisional 2026 remain rigorously separate, including the box 3
rule that provisional 2026 uses the fictitious method only and never collects or
computes werkelijk rendement.

The plugin has no connected apps, external authentication, portal automation,
filing, signing, or submission capability. That boundary applies even when
Chrome, computer use, connectors, credentials, or user permission are available:
the assistant creates an explicitly human-owned checklist, and the taxpayer or
an authorized human performs every authenticated portal action. The release
passes 451 repository tests and validates all 237 registered sources without
errors or warnings.
