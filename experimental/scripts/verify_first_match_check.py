#!/usr/bin/env python3
"""Checker: rebuild first-match via indicator matrix over slope axis (not sorted loop)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CERT = Path("experimental/data/certificates/first-match/first_match.json")
TEX = Path("experimental/asymptotic_rs_mca.tex")


def assign_matrix(cells: list[list[int]]):
    """cells as lists; for each slope present, pick min j with membership."""
    sets = [set(C) for C in cells]
    universe = set()
    for C in sets:
        universe |= C
    if not universe:
        return [0] * len(cells), 0
    max_s = max(universe)
    counts = [0] * len(cells)
    for s in range(max_s + 1):
        if s not in universe:
            continue
        for j, C in enumerate(sets):
            if s in C:
                counts[j] += 1
                break
    return counts, len(universe)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if not args.check:
        p.print_help()
        return 2
    root = Path(__file__).resolve().parents[2]
    cert = json.loads((root / CERT).read_text())
    text = (root / TEX).read_text(encoding="utf-8")
    err = []
    if "lem:first-match" not in text:
        err.append("label")
    # Reconstruct oracle cells and recheck
    oracle_cells = [[0, 1, 2, 3], [2, 3, 4, 5], [5, 6, 7, 8, 9]]
    counts, uni = assign_matrix(oracle_cells)
    if sum(counts) != uni:
        err.append("oracle sum")
    # expected first-match: {0,1,2,3}->{0}, {4,5}->{1} wait 5 is in cell1 and cell2
    # s=0,1 ->0; s=2,3->0; s=4->1; s=5->1 (cell1 before cell2); s=6,7,8,9->2
    # counts [4,2,4]
    if counts != [4, 2, 4]:
        err.append(f"oracle counts {counts}")
    stored_oracle = next(r for r in cert["rows"] if r["kind"] == "oracle_overlap")
    if stored_oracle["assigned_counts"] != [4, 2, 4]:
        err.append(f"cert oracle {stored_oracle['assigned_counts']}")
    for row in cert["rows"]:
        if not row["pass"]:
            err.append(row["kind"])
        if not row["sum_equals_union"]:
            err.append(f"sum {row['kind']}")
    if cert["summary"]["verdict"] != "NO ISSUE":
        err.append("verdict")
    if not cert["claim_boundaries"].get("independent_recheck_confirms"):
        err.append("flag")
    if err:
        print("RESULT: FAIL")
        for e in err:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: slope-axis indicator matrix assignment (range loop)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
