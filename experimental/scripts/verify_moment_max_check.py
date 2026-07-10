#!/usr/bin/env python3
"""Independent checker for lem:moment-max sandwich.

Generator route: direct mean of ratios**q.
Checker route: genuine log-sum-exp:
  log(Gord) = logsumexp(q * log(r_i)) - log(L)
  Gord = exp(log(Gord))
then re-check L^{-1} max^q <= Gord <= max^q.

Uses math for logsumexp (max-shift for stability). Not the algebraic
max^q * mean((r/max)^q) rewrite alone.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

CERT = Path("experimental/data/certificates/moment-max/moment_max.json")
TEX = Path("experimental/asymptotic_rs_mca.tex")


def logsumexp(vals: list[float]) -> float:
    """Stable log-sum-exp."""
    if not vals:
        return float("-inf")
    m = max(vals)
    if math.isinf(m) and m < 0:
        return m
    s = sum(math.exp(v - m) for v in vals)
    return m + math.log(s)


def gord_logsumexp(ratios: list[float], q: int) -> float:
    """Gord = (1/L) sum r^q via exp(logsumexp(q log r) - log L)."""
    L = len(ratios)
    # r must be positive for log; zeros contribute 0 to the sum
    pos = [r for r in ratios if r > 0]
    if not pos:
        return 0.0
    logs = [q * math.log(r) for r in pos]
    return math.exp(logsumexp(logs) - math.log(L))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if not args.check:
        p.print_help()
        return 2
    root = Path(__file__).resolve().parents[2]
    cert = json.loads((root / CERT).read_text(encoding="utf-8"))
    text = (root / TEX).read_text(encoding="utf-8")
    err = []
    if "lem:moment-max" not in text:
        err.append("label")
    route = cert.get("checker_route", "")
    if "log-sum-exp" not in route.lower() and "logsumexp" not in route.lower():
        err.append(f"checker_route missing log-sum-exp claim: {route}")
    for row in cert["rows"]:
        ratios, q = row["ratios"], row["q"]
        G = gord_logsumexp(ratios, q)
        # relative tolerance — exp/log path
        tol = 1e-9 * max(1.0, abs(row["Gord_q"]))
        if abs(G - row["Gord_q"]) > tol:
            err.append(f"Gord LSE {G} vs {row['Gord_q']} kind={row['kind']}")
        mx = max(ratios)
        L = len(ratios)
        if not (mx**q / L - 1e-9 <= G <= mx**q + 1e-9):
            err.append(f"sandwich fail {row['kind']}")
        if not row["sandwich_ok"]:
            err.append(f"flag {row['kind']}")
    if cert["summary"]["verdict"] != "NO ISSUE":
        err.append("verdict")
    if not cert["claim_boundaries"].get("independent_recheck_confirms"):
        err.append("flag independent")
    if err:
        print("RESULT: FAIL")
        for e in err:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: genuine log-sum-exp Gord = exp(logsumexp(q*log r)-log L); sandwich")
    return 0


if __name__ == "__main__":
    sys.exit(main())
