---
schema_version: "1.1"
name: cowork-oss-country-corrections-no-offset
description: OSS Union current-period country balances and nonduplicated historical correction
tags:
- cowork
- extended
- draft
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: OSS Union current-period country balances and nonduplicated historical correction;
  chat only with named gaps and maximum readiness draft.
---
Prepare my Union OSS Q3 2026 return in chat. Netherlands identification and Union registration for this period are confirmed. Current supplies are DE taxable base EUR 1,000 at 19% (VAT EUR 190) and BE base EUR 1,000 at 21% (VAT EUR 210); I verified the country/category rates against official evidence on 30 September 2026. For DE in 2024 Q4 I originally filed VAT EUR 300, the correct target is zero, and I already reported a correction of minus EUR 60. The original due date was 31 January 2025 and I intend to report the remaining correction on 2 October 2026. Can I pay EUR 160 by offsetting Germany's EUR 50 refund against Belgium, and also subtract the old credit note from current sales? Keep it in chat, no file and no portal action.
