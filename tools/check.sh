#!/bin/bash
# Build the site; anything that breaks the build breaks this script.
# Run from the repository root:  tools/check.sh
# CI runs the same steps (.github/workflows/docs.yml).
set -uo pipefail
cd "$(dirname "$0")/.."
PY=${PYTHON:-python3}
[ -x ".venv/bin/python" ] && PY=.venv/bin/python
MK=mkdocs
command -v "$MK" >/dev/null || MK=".venv/bin/mkdocs"
fail=0

echo "== generate"
"$PY" tools/build_docs.py || fail=1

echo "== build (strict)"
if "$MK" build --strict -f docs-site/mkdocs.yml >/dev/null 2>&1; then
  echo "builds clean"
else
  echo "BUILD FAILED: run $MK build --strict -f docs-site/mkdocs.yml to see why"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then echo "PASS"; else echo "FAIL"; fi
exit "$fail"
