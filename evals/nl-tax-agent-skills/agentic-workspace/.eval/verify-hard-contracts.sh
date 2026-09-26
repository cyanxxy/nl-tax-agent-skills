#!/usr/bin/env bash
# Hard artifact boundaries for the live agentic benchmark (0.4 file rules).
# Nothing is written by default; with the taxpayer's consent the plugin keeps
# exactly one workpack file per workflow at a fixed path. This script checks
# only those file boundaries; it never scores wording or tax reasoning.
set -euo pipefail

ANNUAL="workspace/nl-tax-annual-2025-workpack.md"
PROVISIONAL="workspace/nl-tax-provisional-2026-workpack.md"

fail() {
  echo "$*" >&2
  exit 1
}

if [[ -e workspace/eval/current-case.txt ]]; then
  fail "Agentic benchmark must not use an exact case marker."
fi

# R3: under workspace/ only the two fixed workpack files may exist. This
# rejects every 0.3 ledger path (workspace/taxpayer, shared, annual,
# provisional), standalone field maps, checklists, notes, and copies.
if [[ -d workspace ]]; then
  unexpected="$(find workspace -type f ! -path "$ANNUAL" ! -path "$PROVISIONAL" -print)"
  if [[ -n "$unexpected" ]]; then
    echo "Only $ANNUAL and $PROVISIONAL may be written:" >&2
    fail "$unexpected"
  fi
fi

# No second workspace/ tree and no workpack copy, -v2, or dated variant anywhere.
stray="$(find . -path ./.git -prune -o \
  \( -type d -name workspace ! -path ./workspace -print \) -o \
  \( -type f -name 'nl-tax-*workpack*' ! -path "./$ANNUAL" ! -path "./$PROVISIONAL" -print \))"
if [[ -n "$stray" ]]; then
  echo "Workpacks are never copied and there is one workspace/ tree:" >&2
  fail "$stray"
fi

check_workpack() {
  local file="$1" workflow_pattern="$2" other="$3"
  [[ -f "$file" ]] || return 0
  grep -Eq '^save_consent:[[:space:]]*given[[:space:]]*$' "$file" \
    || fail "$file exists without a recorded save_consent: given (R1/R2)."
  grep -Eq "^workflow:[[:space:]]*${workflow_pattern}[[:space:]]*$" "$file" \
    || fail "$file does not record its own workflow in Appendix A."
  if grep -q "$other" "$file"; then
    fail "$file names the other workflow's file $other; annual and provisional stay separate."
  fi
}

check_workpack "$ANNUAL" 'annual_2025' 'nl-tax-provisional-2026-workpack'
check_workpack "$PROVISIONAL" 'provisional_2026_(request|change|review|stopzetten)' \
  'nl-tax-annual-2025-workpack'

if [[ -f "$PROVISIONAL" ]]; then
  if grep -Ei 'werkelijk[ _-]*rendement|actual[ _-]*return|box3_actual' "$PROVISIONAL" \
      | grep -Eiv 'werkelijk rendement is not part of provisional 2026|werkelijk rendement may become relevant when filing the annual 2026 return in 2027' \
      | grep -q .; then
    fail "$PROVISIONAL collects werkelijk rendement; provisional Box 3 is fictitious-only."
  fi
fi

echo "AGENTIC HARD-CONTRACT CHECK PASSED"
