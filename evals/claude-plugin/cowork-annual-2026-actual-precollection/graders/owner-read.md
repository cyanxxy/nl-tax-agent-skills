---
type: tool_used
tool: Read
input_match: 'nl-tax-annual-return-2026/'
arm: with-only
---
Owner indicator: the run read files of the owning skill `nl-tax-annual-return-2026`, either its
SKILL.md through the intake handoff or its own reference flow after a direct
Skill invocation. `skill-fired.md` also passes when only the intake router
fires, so this grader is the one that shows the owner actually loaded.
