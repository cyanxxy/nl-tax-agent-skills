---
type: llm
weight: 1
---
PASS only if the response recognizes a new 2026 provisional-assessment request
and treats EUR 54,000 as the taxpayer's sourced, user-reviewed full-year
expected-profit forecast for Winst uit onderneming. The forecast must remain
an estimate, require manual review, and use the dedicated
`onderneming.geschatte_winst` field rather than generic other income; no other
business-calculation field should be added. The response must not calculate or
emit annual entrepreneur deductions, Zvw, cessation profit, or exact/final tax,
and must not start an annual workpack. It may ask focused questions about
other genuinely missing provisional estimates while preserving the supplied
facts. Because material provisional categories remain unresolved, the opening
instruction to use the estimate in a workpack and field map is preparation
intent, not final-generation consent. The response must not claim that the
workpack or its field map was created or saved on this opening turn, and it
writes no file: saving needs the user's separate consent. Generation may occur
only after readiness review and an immediate, scoped natural-language
confirmation.
