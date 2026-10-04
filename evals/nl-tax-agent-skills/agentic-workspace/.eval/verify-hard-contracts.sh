#!/usr/bin/env bash
# Hard artifact boundaries for the live agentic benchmark (0.4 file rules).
# Nothing is written by default; with the taxpayer's consent the plugin keeps
# exactly one workpack file per workflow identity. This script checks only
# those file boundaries; it never scores wording or tax reasoning.
#
# Income tax has two fixed paths. The draft-only extension workflows write one
# file per exact identity (year, assigned period, OSS scheme or international
# return form); the patterns below mirror WORKPACK_PATHS in
# tools/nl_tax_agent_skills/workpack/validate_workpack.py. Such a file passes
# only when its Appendix A records save_consent: given and the workflow that
# its file name encodes.
set -euo pipefail

ANNUAL="workspace/nl-tax-annual-2025-workpack.md"
PROVISIONAL="workspace/nl-tax-provisional-2026-workpack.md"
PERIOD='(Q[1-4]|M(0[1-9]|1[0-2])|Y)'
YEAR='(2025|2026)'
IDENTITY_PATH_RE="^workspace/nl-tax-(vat-${YEAR}-${PERIOD}|vat-correction-${YEAR}-${PERIOD}|icp-${YEAR}-${PERIOD}|oss-(union|non_union)-${YEAR}-Q[1-4]|oss-ioss-${YEAR}-M(0[1-9]|1[0-2])|international-${YEAR}-(migration|nonresident)|annual-2026)-workpack\.md$"

fail() {
  echo "$*" >&2
  exit 1
}

is_identity_workpack() {
  [[ "$1" =~ $IDENTITY_PATH_RE ]]
}

is_workpack_path() {
  [[ "$1" == "$ANNUAL" || "$1" == "$PROVISIONAL" ]] || is_identity_workpack "$1"
}

# The Appendix A workflow that an identity-scoped file name encodes, e.g.
# workspace/nl-tax-vat-correction-2026-Q1-workpack.md -> vat_correction_2026_Q1.
workflow_for_path() {
  local name="${1#workspace/nl-tax-}"
  name="${name%-workpack.md}"
  printf '%s\n' "$name" | tr '-' '_'
}

if [[ -e workspace/eval/current-case.txt ]]; then
  fail "Agentic benchmark must not use an exact case marker."
fi

# R3: under workspace/ only workpack files at their exact paths may exist. This
# rejects every 0.3 ledger path (workspace/taxpayer, shared, annual,
# provisional), standalone field maps, checklists, notes, and copies.
if [[ -d workspace ]]; then
  unexpected=""
  while IFS= read -r -d '' file; do
    is_workpack_path "$file" || unexpected+="$file"$'\n'
  done < <(find workspace -type f -print0)
  if [[ -n "$unexpected" ]]; then
    echo "Only $ANNUAL, $PROVISIONAL, or one consented workpack per VAT/ICP/OSS/international/annual 2026 identity may be written:" >&2
    fail "$unexpected"
  fi
fi

# No second workspace/ tree and no workpack copy, -v2, or dated variant anywhere.
stray=""
while IFS= read -r -d '' entry; do
  entry="${entry#./}"
  if [[ -d "$entry" ]]; then
    stray+="$entry/"$'\n'
  elif ! is_workpack_path "$entry"; then
    stray+="$entry"$'\n'
  fi
done < <(find . -path ./.git -prune -o \
  \( -type d -name workspace ! -path ./workspace -print0 \) -o \
  \( -type f -name 'nl-tax-*workpack*' -print0 \))
if [[ -n "$stray" ]]; then
  echo "Workpacks are never copied and there is one workspace/ tree:" >&2
  fail "$stray"
fi

check_workpack() {
  local file="$1" workflow_pattern="$2" own_stem mention
  [[ -f "$file" ]] || return 0
  grep -Eq '^save_consent:[[:space:]]*given[[:space:]]*$' "$file" \
    || fail "$file exists without a recorded save_consent: given (R1/R2)."
  grep -Eq "^workflow:[[:space:]]*${workflow_pattern}[[:space:]]*$" "$file" \
    || fail "$file does not record its own workflow in Appendix A."
  # Each workflow identity owns only its own file: no other workpack name,
  # including another period, scheme or form of the same kind.
  own_stem="$(basename "$file" .md)"
  while IFS= read -r mention; do
    [[ -z "$mention" || "$mention" == "$own_stem" ]] && continue
    fail "$file names another workpack file $mention; each workflow identity stays separate."
  done < <(grep -oE 'nl-tax-[A-Za-z0-9_-]+-workpack' "$file" | sort -u || true)
}

check_workpack "$ANNUAL" 'annual_2025'
check_workpack "$PROVISIONAL" 'provisional_2026_(request|change|review|stopzetten)'

if [[ -d workspace ]]; then
  while IFS= read -r -d '' file; do
    if is_identity_workpack "$file"; then
      check_workpack "$file" "$(workflow_for_path "$file")"
    fi
  done < <(find workspace -maxdepth 1 -type f -name 'nl-tax-*-workpack.md' -print0)
fi

if [[ -f "$PROVISIONAL" ]]; then
  if grep -Ei 'werkelijk[ _-]*rendement|actual[ _-]*return|box3_actual' "$PROVISIONAL" \
      | grep -Eiv 'werkelijk rendement is not part of provisional 2026|werkelijk rendement may become relevant when filing the annual 2026 return in 2027' \
      | grep -q .; then
    fail "$PROVISIONAL collects werkelijk rendement; provisional Box 3 is fictitious-only."
  fi
fi

echo "AGENTIC HARD-CONTRACT CHECK PASSED"
