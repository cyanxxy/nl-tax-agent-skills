---
name: nl-tax-shared-resources
description: "Internal resource bundle for the NL Tax Agent Skills plugin: runtime contracts, reviewed tax notes, the source register, and document-reading rules. Never invoked as a skill; the plugin's other skills read its files by path."
compatibility: "Plugin-only: requires the complete nl-tax-agent-skills plugin. Reads shared files from sibling skill folders such as nl-tax-shared-resources, so it does not work when installed or uploaded as a single skill."
user-invocable: false
disable-model-invocation: true
---

# NL Tax shared resources

This internal skill packages the shared runtime contract, reviewed tax
knowledge, source register, and document-reading references required by the
user-facing Dutch tax skills.

Do not invoke it as a standalone workflow and do not answer a taxpayer directly
from this file. An owning skill must select the relevant shared resource, apply
its own workflow and safety boundaries, and keep progressive disclosure intact.

Start every tax-rule lookup at
[`knowledge-index.md`](knowledge-index.md): it maps each topic, year, and
workflow to the one reviewed note that answers it.

When an owning workflow reads a document the user shares, it classifies it with
[`reference/evidence-types.md`](reference/evidence-types.md) and takes values
only within
[`reference/extraction-boundaries.md`](reference/extraction-boundaries.md).
