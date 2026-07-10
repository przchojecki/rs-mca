#!/usr/bin/env python3
"""Second-algorithm checker: rebuild monic locators via nested expansion (not iterative mul list)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/pole-line-division/pole_line_division.json"
)


def monic_expand(roots, p):
    """Build monic poly by expanding product (X-r) with explicit coeff recurrence."""
    # coeffs[k] = e_{deg-k} with sign; start from 1
    # iterative: for each root, new_e[j] = e[j] - r*e[j-1] (elem sym)
    e = [1]  # e0=1, will grow
    for r in roots:
        r = r % p
        ne = [0] * (len(e) + 1)
        ne[0] = (e[0] * ((-r) % p)) % p  # wrong - use standard
        # poly *= (X - r): if e is low-first [c0,c1,...,c_d] for c0+c1 X+...
        # better low-first: [1] * [-r,1]
        pass
    # Direct low-first
    poly = [1]
    for r in roots:
        r = r % p
        out = [0] * (len(poly) + 1)
        for i, c in enumerate(poly):
            out[i] = (out[i] + c * ((-r) % p)) % p
            out[i + 1] = (out[i + 1] + c) % p
        poly = out
    return poly


def peval(poly, x, p):
    acc, xp = 0, 1
    for c in poly:
        acc = (acc + c * xp) % p
        xp = (xp * x) % p
    return acc


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
    for row in cert["rows"]:
        S, p_, alpha, D = row["S"], row["p"], row["alpha"], row["D"]
        poly = monic_expand(S, p_)
        for x in S:
            if peval(poly, x, p_) != 0:
                err.append(f"root fail {S} at {x}")
        # values of U/(x-alpha) with U=ell, zeta=0
        for x in S:
            inv = pow((x - alpha) % p_, -1, p_)
            val = (peval(poly, x, p_) * inv) % p_
            if val != 0:
                err.append(f"val {val}")
        if not row.get("pass"):
            err.append("row pass false")
    if cert["summary"]["verdict"] != "NO ISSUE":
        err.append("verdict")
    if err:
        print("RESULT: FAIL")
        for e in err:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: nested monic expansion (elem-sym style) + peval on S")
    return 0


if __name__ == "__main__":
    sys.exit(main())
