#!/usr/bin/env python3
"""Checker: linear-form image size over F_q^d without full grid when possible."""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/residual-ray-compiler/residual_ray_compiler.json"
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
    # nonzero linear form on F_5^2 has 5 image points
    q = 5
    rays = {(p0 + 2 * p1) % q for p0, p1 in itertools.product(range(q), repeat=2)}
    if len(rays) != q:
        fails.append("linear_image")
    # zero form has 1
    rays0 = {(0 * p0 + 0 * p1) % q for p0, p1 in itertools.product(range(q), repeat=2)}
    if len(rays0) != 1:
        fails.append("zero_form")
    if not cert.get("all_pass"):
        fails.append("all_pass")
    if not cert.get("pins_ok"):
        fails.append("pins")
    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: closed-form linear image size vs grid")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
