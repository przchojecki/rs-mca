#!/usr/bin/env python3
"""Independent checker for lower-reserve-unsafe (W34-R1).

Checker route: binary-search ceiling division (NOT (num+den-1)//den),
plus Fraction-based L, plus pure integer U?B* redeploy from cert rows.
"""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/lower-reserve-unsafe/lower_reserve_unsafe.json"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ceil_div_binsearch(num: int, den: int) -> int:
    if den <= 0:
        raise ValueError("den")
    if num <= 0:
        return 0
    lo, hi = 0, num
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * den >= num:
            hi = mid
        else:
            lo = mid + 1
    return lo


def L_frac(n: int, a: int, k: int, B: int) -> int:
    w = a - k - 1
    r = Fraction(comb(n, a), B**w)
    return r.numerator // r.denominator + (0 if r.numerator % r.denominator == 0 else 1)


def P_binsearch(n, a, k, B, q, Gamma):
    L = L_frac(n, a, k, B)
    den_i = q - n + k * (L - 1)
    if den_i <= 0:
        return None
    inner = ceil_div_binsearch(L * (q - n), den_i)
    return ceil_div_binsearch(Gamma * inner, q)


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

    # recompute one toy via binsearch
    P = P_binsearch(16, 10, 6, 5, 17, 17)
    if P is None or P < 1:
        fails.append("P_toy")

    # binsearch ceil agrees with classical on random positives
    for num, den in [(10, 3), (17, 5), (100, 7), (1, 1), (0, 5)]:
        classical = 0 if num <= 0 else (num + den - 1) // den
        if ceil_div_binsearch(num, den) != classical:
            fails.append(f"ceil_{num}_{den}")

    # cert toy rows: gen P must match binsearch
    for r in cert.get("rows", []):
        if r.get("kind") == "toy_SB1":
            Pb = P_binsearch(r["n"], r["a"], r["k"], r["B"], r["q"], r["Gamma"])
            if Pb != r.get("gen", {}).get("P") and Pb != r.get("P"):
                # stored structure: gen.P
                gp = r.get("gen", {}).get("P")
                if Pb != gp:
                    fails.append(f"toy_mismatch_{r['a']}")

    for r in cert.get("rows", []):
        if r.get("kind", "").startswith("deployed_"):
            if not (r["U0"] > r["B_star"] and r["U1"] <= r["B_star"]):
                fails.append(r["kind"])

    if not cert.get("all_pass"):
        fails.append("all_pass")
    if not cert.get("all_deployed_unsafe_quiet"):
        fails.append("deployed")
    # require honest checker_route mention
    cr = cert.get("checker_route", "")
    if "binsearch" not in cr.lower() and "binary" not in cr.lower():
        fails.append("checker_route_not_binsearch")

    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: binary-search ceil_div + Fraction L; integer U?B* redeploy")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
