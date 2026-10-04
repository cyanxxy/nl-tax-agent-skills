---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?(?:nl-tax-international-return|nl-tax-intake)"'
---
Plugin-fired indicator: the run loaded the owning skill `nl-tax-international-return` directly,
or the `nl-tax-intake` router that hands off to it. Owner routing itself is
judged from the response by `criteria.md`.
