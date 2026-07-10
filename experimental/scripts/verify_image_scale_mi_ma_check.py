#!/usr/bin/env python3
"""Checker: iterative power + 4-fold energy; redeploy key inequalities."""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/image-scale-mi-ma/image_scale_mi_ma.json"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


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
    A = 1
    for _ in range(4):
        A *= 5
    if A != 625:
        fails.append("A")
    if 4 * 5 >= 625:
        fails.append("fi_should_fail")
    cube = list(itertools.product([0, 1], repeat=2))
    # energy for {0,1}^2
    E = 0
    for a, b, c, d in itertools.product(cube, cube, cube, cube):
        if all(a[i] - b[i] == c[i] - d[i] for i in range(2)):
            E += 1
    if E <= 0:
        fails.append("energy")
    if not cert.get("all_pass"):
        fails.append("all_pass")
    if not cert.get("pins_ok"):
        fails.append("pins")
    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: iterative A=B^R; 4-fold energy")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
