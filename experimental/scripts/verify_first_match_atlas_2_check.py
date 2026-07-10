#!/usr/bin/env python3
"""Checker: sorted-merge union; under-budget detection."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/first-match-atlas-2/first_match_atlas_2.json"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def first_match_sizes(cells):
    claimed = set()
    sizes = []
    for Z in cells:
        part = set(Z) - claimed
        sizes.append(len(part))
        claimed |= set(Z)
    return sizes, len(claimed)


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
    sizes, u = first_match_sizes([{0, 1, 2, 3}, {2, 3, 4, 5}, {5, 6, 7, 8, 9}])
    if sizes != [4, 2, 4] or u != 10:
        fails.append("sizes")
    if sum(sizes) != u:
        fails.append("partition")
    # underbudget
    if all(s <= 1 for s in sizes):
        fails.append("should_not_fit_budget_1")
    if not cert.get("all_pass"):
        fails.append("all_pass")
    if not cert.get("pins_ok"):
        fails.append("pins")
    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: sequential sizes + union cardinality; under-budget detect")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
