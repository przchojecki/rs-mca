#!/usr/bin/env bash
# Replay for cap25-v13-identity-frontier.
#
# Zero-arg. Runs the EXISTING, unmodified repo checker script from the repo
# root and exits 0 iff all 12 exact-integer checks PASS (i.e. iff the
# script's own "All exact frontier checks passed." trailer is printed and
# its exit code is 0). This certifies only the lower/unsafe staircase
# L(a0) > threshold; it does not certify the safe side (see README.md).
#
# This script does not regenerate certificate.json and makes no writes
# anywhere in the repository.
set -uo pipefail

# Repo root is derived from this script's own location (repo-relative, no
# machine-local absolute path), since this file lives at
# experimental/data/certificates/cap25-v13-identity-frontier/replay.sh --
# four directories below the repo root.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
SCRIPT="experimental/scripts/towards v13/cap25_v13_frontier_identity_exact_checks.py"

cd "$REPO_ROOT"

# errexit deliberately off around this call so a nonzero exit from the
# checker is captured in $STATUS instead of tearing down this script before
# the explicit checks below can run and report why.
set +e
OUT="$(python3 "$SCRIPT" 2>&1)"
STATUS=$?
set -e

echo "$OUT"

if [ "$STATUS" -ne 0 ]; then
    echo "REPLAY FAIL: checker script exited $STATUS" >&2
    exit 1
fi

if ! grep -q "All exact frontier checks passed\." <<<"$OUT"; then
    echo "REPLAY FAIL: trailer line not found in checker output" >&2
    exit 1
fi

PASS_COUNT="$(grep -c '^PASS ' <<<"$OUT")"
if [ "$PASS_COUNT" -ne 12 ]; then
    echo "REPLAY FAIL: expected 12 PASS lines, found $PASS_COUNT" >&2
    exit 1
fi

echo "REPLAY OK: 12/12 PASS, trailer present, exit 0."
exit 0
