---
type: regex
target: trace
pattern: '\\?"skill\\?"\s*:\s*\\?"(?:[\w-]+:)?nl-tax-vat-adjustments\\?"|\\?"file_path\\?"\s*:\s*\\?"[^"]*?nl-tax-vat-adjustments/'
arm: with-only
---
Helper indicator: the owning VAT return used the read-only
`nl-tax-vat-adjustments` helper instead of answering the investment-service
revision from memory. Either route passes: a Skill call to the helper (the
runtime contract's preferred route when the host lists it), or a Read of the
helper's SKILL.md or reference files (the inline route on hosts without a
skill tool). A mention of the helper's path inside another file's text does
not count; only the Skill call's `skill` input or a Read call's `file_path`
input matches.
