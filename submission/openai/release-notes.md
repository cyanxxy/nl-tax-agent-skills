# OpenAI Plugin Directory release 0.5.0

NL Tax Agent Skills is a skills-only plugin for preparing source-traceable Dutch
individual income-tax workpacks for manual Mijn Belastingdienst entry. It
supports annual 2025 preparation, the 2026 voorlopige aanslag request, change,
review, and stopzetten workflows, and read-only rule questions for both years.

This release adds draft-only VAT, ICP, OSS/IOSS, international and annual 2026
preparation. Skills guide the agent's use of the user's evidence and the
bundled references. Preparation remains conversation-first: nothing is
written by default, and saving requires consent. Each saved workpack holds
the evidence, questions, resume record and field map for its workflow and
period, scheme or form.

This submission candidate clarifies that the 2025 deduction-rate-cap threshold
uses Box 1 income before deductions, not aggregate verzamelinkomen. This
correction and the 20 overdue source checks were approved by Mansour Damanpak
on 1 October 2026. Published rates, threshold amounts, and cited sources are
unchanged. Annual 2025 and provisional 2026 remain rigorously separate,
including the box 3 rule that provisional 2026 uses the fictitious method only
and never collects or computes werkelijk rendement.

The package still ships Markdown and YAML only: no scripts, hooks, MCP servers,
or package installs, and no shell or Python is needed. The plugin has no
connected apps, external authentication, portal automation, filing, signing,
or submission capability. That boundary applies even when Chrome, computer
use, connectors, credentials, or user permission are available: the taxpayer
or an authorized human performs every authenticated portal action.

## Draft-only previews in this package

The package also contains draft-only previews of further workflows. They are
not filing-ready: their official sources await human tax-content review, so
they never claim to be complete or ready to file and produce no manual-entry
checklist with amounts. The previews are:

- a ZZP btw-aangifte (VAT return) and a correction or suppletie for one already
  filed period, for 2025 and 2026;
- an opgaaf ICP (EU sales listing) for one confirmed 2025 or 2026 period;
- an OSS Union, OSS non-Union, or IOSS return for one confirmed scheme and
  period, for 2025 and 2026;
- evidenced VAT adjustments (private use of a business car, mixed use,
  revision of investment goods and property, BUA, and the margin scheme),
  prepared by a read-only helper inside the VAT workflow;
- an M-biljet (migration year) or C-biljet (nonresident) income-tax draft for
  2025, and evidence collection for 2026; and
- evidence collection for the resident annual income-tax return 2026, which
  stays incomplete until the year has ended.

Each preview keeps its own workpack file per period, scheme, or form, saved
only with the user's consent. VAT, ICP, and OSS filings are made by the
taxpayer or an authorized human, never by the plugin.
