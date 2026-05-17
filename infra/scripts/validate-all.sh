#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PHASES_DIR="$SCRIPT_DIR/../phases"

FAILED=0

for phase_dir in "$PHASES_DIR"/*/; do
  phase_name=$(basename "$phase_dir")
  echo "=== Validating $phase_name ==="

  if terraform -chdir="$phase_dir" init -backend=false -input=false > /dev/null 2>&1; then
    if terraform -chdir="$phase_dir" validate; then
      echo "  PASS"
    else
      echo "  FAIL"
      FAILED=1
    fi
  else
    echo "  FAIL (init failed)"
    FAILED=1
  fi
  echo ""
done

if [ $FAILED -eq 0 ]; then
  echo "All phases validated successfully."
else
  echo "Some phases failed validation."
  exit 1
fi
