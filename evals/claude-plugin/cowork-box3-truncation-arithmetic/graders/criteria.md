---
type: llm
weight: 1
---
PASS only if the response runs the 2025 Box 3 fictitious-return calculation
using the canonical 2025 parameters and all 6 official Belastingdienst steps
explicitly:

- Subtract the EUR 3,800 debt threshold first: aftrekbare schulden = EUR 6,200.
- Belastbaar rendement = EUR 100,000 * 1.37% (EUR 1,370.00) + EUR 50,000 * 5.88%
  (EUR 2,940.00) - EUR 6,200 * 2.70% (EUR 167.40) = EUR 4,142.60.
- Rendementsgrondslag = EUR 100,000 + EUR 50,000 - EUR 6,200 = EUR 143,800.
- Grondslag sparen en beleggen = EUR 143,800 - EUR 57,684 = EUR 86,116.
- Aandeel in de rendementsgrondslag = 86,116 / 143,800 = 59.88595...%,
  truncated toward zero to 2 decimals = 59.88% (rounding up to 59.89% is a FAIL).
- Voordeel uit sparen en beleggen = EUR 4,142.60 * 59.88% = EUR 2,480.59 (or
  EUR 2,480 if truncated/rounded to whole euros at that step), and Box 3 tax at
  36% = EUR 893.01 (or EUR 892–893 with whole-euro rounding).
- Acknowledge that the user declined werkelijk rendement for now (not a gap,
  and note that supplying actual-return data is not a binding method election).
- Stay focused on Box 3 without dumping a 14-phase full-return survey, and
  write no file.
