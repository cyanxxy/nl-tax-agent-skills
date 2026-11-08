---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?(?:nl-tax-annual-return-2026|nl-tax-intake)"'
---
Plugin-fired indicator: the run loaded the owning skill `nl-tax-annual-return-2026` directly,
or the `nl-tax-intake` router that hands off to it. Owner routing itself is
judged from the response by `criteria.md`.
