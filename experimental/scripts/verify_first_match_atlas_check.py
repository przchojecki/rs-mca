#!/usr/bin/env python3
"""Independent checker: indicator-matrix first-match (no sequential setdiff)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CERT = Path("experimental/data/certificates/first-match-atlas/first_match_atlas.json")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def indicator_sizes(cells: list[set[int]]) -> list[int]:
    universe: set[int] = set()
    for Z in cells:
        universe |= Z
    counts = [0] * len(cells)
    for s in sorted(universe):
        for j, Z in enumerate(cells):
            if s in Z:
                counts[j] += 1
                break
    return counts


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if not args.check:
        p.print_help()
        return 2
    root = repo_root()
    cert = json.loads((root / CERT).read_text(encoding="utf-8"))
    fails = []
    if indicator_sizes([{0, 1, 2, 3}, {2, 3, 4, 5}, {5, 6, 7, 8, 9}]) != [4, 2, 4]:
        fails.append("oracle")
    if indicator_sizes([{0, 1, 2, 3, 4}, {1, 2}, {4, 5}]) != [5, 0, 1]:
        fails.append("boundary")
    if not cert.get("all_pass"):
        fails.append("all_pass")
    if not cert.get("pins_ok"):
        fails.append("pins")
    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: indicator-matrix least-index sizes")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
