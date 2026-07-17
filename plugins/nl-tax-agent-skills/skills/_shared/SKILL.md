---
name: nl-tax-shared-resources
description: Use when an NL Tax Agent Skill needs its internal resource bundle; never invoke it as a standalone taxpayer workflow.
user-invocable: false
disable-model-invocation: true
---

# NL Tax shared resources

This internal skill packages the shared runtime contract, reviewed tax
knowledge, source register, and templates required by the user-facing Dutch tax
skills.

Do not invoke it as a standalone workflow and do not answer a taxpayer directly
from this file. An owning skill must select the relevant shared resource, apply
its own workflow and safety boundaries, and keep progressive disclosure intact.
