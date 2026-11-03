---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?nl-tax-(?:box1-home|box2|box3|winst|partner-deductions|vat-adjustments)"'
min: 0
max: 0
---
No background helper is invoked. Helpers are agent-invocable on Claude, but
they run only inside an active owning workflow; a rule question has none, so it
belongs to `nl-tax-knowledge`.
