#!/usr/bin/env python3
"""Checker: square-image formula + linear |im|=q; require OPEN GAP + MISSING_C."""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/ray-compiler-input/ray_compiler_input.json"
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
    # F_5 squares
    im = {(x * x) % 5 for x in range(5)}
    if len(im) != 3:  # (5+1)/2
        fails.append("square5")
    # linear
    im_l = {(x + 2 * y) % 7 for x, y in itertools.product(range(7), repeat=2)}
    if len(im_l) != 7:
        fails.append("linear7")
    if not cert.get("all_pass"):
        fails.append("all_pass")
    if cert.get("verdict") != "OPEN GAP":
        fails.append("verdict")
    if not cert.get("missing_input", {}).get("id"):
        fails.append("missing_input")
    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: square-image formula; linear surjectivity; MISSING_C present")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
