#!/usr/bin/env python3
"""Second-algorithm checker: recompute contradiction table + one Boolean |A-A| via set of sums."""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

CERT = Path("experimental/data/certificates/bsg-quasicube/bsg_quasicube.json")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if not args.check:
        p.print_help()
        return 2
    root = Path(__file__).resolve().parents[2]
    cert = json.loads((root / CERT).read_text())
    err = []
    # Recompute all (c,eps) contradiction rows from rule eps < c/2
    chain = cert["contradiction_chain"]
    for row in chain["rows"]:
        expected = row["eps"] < 0.5 * row["c"]
        if bool(row["formal_contradiction"]) != expected:
            err.append(f"contradiction row {row}")
        if abs(row["threshold_eps"] - 0.5 * row["c"]) > 1e-15:
            err.append("threshold")
    # Recompute one Boolean sample: full cube n=3
    A = list(itertools.product([0, 1], repeat=3))
    diffs = set()
    for a, b in itertools.product(A, A):
        diffs.add(tuple(a[i] - b[i] for i in range(3)))
    dsize, nA = len(diffs), len(A)
    if dsize * dsize < nA**3:
        err.append("cube n=3 quasicube fail")
    # Match cert sample if present
    sample = next((s for s in cert["boolean_samples"] if s["family"] == "full_cube_n3"), None)
    if sample:
        if sample["diff_size"] != dsize or sample["size"] != nA:
            err.append(f"sample mismatch {sample} vs {dsize},{nA}")
        if not sample["quasicube_holds"]:
            err.append("sample flag")
    if not all(s["quasicube_holds"] for s in cert["boolean_samples"]):
        err.append("some sample fails")
    if cert["summary"]["verdict"] != "NO ISSUE":
        err.append("verdict")
    if err:
        print("RESULT: FAIL")
        for e in err:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: recompute eps<c/2 table + independent cube difference set")
    return 0


if __name__ == "__main__":
    sys.exit(main())
