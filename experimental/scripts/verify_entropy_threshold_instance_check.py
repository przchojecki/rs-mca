#!/usr/bin/env python3
"""Checker: independently compute BOTH bisection and Newton g*; do not trust agree flag."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/entropy-threshold-instance/entropy_threshold_instance.json"
)


def H2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)


def gstar_bisect(rho, beta, it=120):
    lo, hi = 0.0, 1.0 - rho
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if H2(rho + mid) >= beta * mid:
            lo = mid
        else:
            hi = mid
    return lo


def gstar_newton(rho, beta, it=50):
    def f(g):
        return H2(rho + g) - beta * g

    def fp(g):
        x = rho + g
        return math.log2((1 - x) / x) - beta

    g = min(0.05, (1 - rho) / 2)
    lo, hi = 0.0, 1.0 - rho - 1e-15
    for _ in range(it):
        der = fp(g)
        if abs(der) < 1e-18:
            break
        g2 = g - f(g) / der
        if g2 <= lo or g2 >= hi:
            g2 = 0.5 * (lo + hi)
        if f(g2) >= 0:
            lo = g2
        else:
            hi = g2
        g = g2
    return lo


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
    for row in cert["grid"]:
        gb = gstar_bisect(row["rho"], row["beta"])
        gn = gstar_newton(row["rho"], row["beta"])
        if abs(gb - gn) > 1e-8:
            err.append(f"BN disagree {row['rho']},{row['beta']}: {gb} {gn}")
        if abs(gb - row["g_bisection"]) > 1e-9:
            err.append(f"bisect vs cert {row}")
        if abs(gn - row["g_newton"]) > 1e-8:
            err.append(f"newton vs cert {row}")
        # Do not trust row['agree']; recompute
        if abs(gb - gn) > 1e-8:
            err.append("agree false")
        if abs(row["beta"] - 31) < 0.1 and abs(row["rho"] - 0.5) < 0.01:
            err.append("deployed row")
    # worked toy g*
    toy = cert["worked_toy"]
    g = gstar_bisect(toy["rho"], toy["beta"])
    if abs(g - toy["gstar"]) > 1e-9:
        err.append(f"toy g* {g} vs {toy['gstar']}")
    if cert["summary"]["verdict"] != "NO ISSUE":
        err.append("verdict")
    if err:
        print("RESULT: FAIL")
        for e in err:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: independent Newton AND bisection for every grid row (not trust agree flag)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
