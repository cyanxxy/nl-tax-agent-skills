---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?(?:nl-tax-oss|nl-tax-intake)"'
---
Plugin-fired indicator: the run loaded the owning skill `nl-tax-oss` directly,
or the `nl-tax-intake` router that hands off to it. Owner routing itself is
judged from the response by `criteria.md`.
