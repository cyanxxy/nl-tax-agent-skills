---
name: nl-tax-shared-resources
description: Internal resource bundle for NL Tax Agent Skills; never invoke as a standalone taxpayer workflow.
user-invocable: false
disable-model-invocation: true
---

# NL Tax shared resources

This internal skill packages the shared runtime contract, reviewed knowledge,
source register, workflow registry, templates, and evaluation fixtures required
by the user-facing Dutch tax skills.

Do not invoke it as a standalone workflow and do not answer a taxpayer directly
from this file. An owning skill must select the relevant shared resource, apply
its own workflow and safety boundaries, and keep progressive disclosure intact.
