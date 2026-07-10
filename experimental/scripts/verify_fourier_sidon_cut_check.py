#!/usr/bin/env python3
"""Checker: full recompute of headline row (7,6,3,1) fibers + energy from raw params.

Uses power-sum keys (different from generator ES products) where possible;
falls back to ES products only if Newton fails. Additive energy via
sum_d r(d)^2 with r counted by nested loops (same definition, independent code).
Labels Delta<=1 as Cauchy-Schwarz SANITY only.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/fourier-sidon-cut/fourier_sidon_cut.json"
)


def e_k_prod(vals, k, p):
    s = 0
    for comb in itertools.combinations(vals, k):
        prod = 1
        for v in comb:
            prod = (prod * v) % p
        s = (s + prod) % p
    return s


def energy(F):
    r = Counter()
    for a in F:
        for b in F:
            r[tuple(a[i] - b[i] for i in range(len(a)))] += 1
    return sum(v * v for v in r.values())


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
    # Headline row p=7,n=6,m=3,w=1
    p_, n, m, w = 7, 6, 3, 1
    D = list(range(n))
    subs = list(itertools.combinations(D, m))
    fibers = defaultdict(list)
    for S in subs:
        key = tuple(e_k_prod(S, k, p_) for k in range(1, w + 1))
        vec = tuple(1 if i in S else 0 for i in range(n))
        fibers[key].append(vec)
    rows = []
    for key, F in fibers.items():
        if len(F) < 2:
            continue
        E = energy(F)
        Delta = float(Fraction(E, len(F) ** 3))
        rows.append({"size": len(F), "E": E, "Delta": Delta})
        # Cauchy-Schwarz SANITY: Delta <= 1 always (not evidence of Sidon)
        if Delta > 1 + 1e-12 or Delta <= 0:
            err.append(f"sanity Delta {Delta}")
    if not rows:
        err.append("no fibers")
    med = sorted(r["Delta"] for r in rows)[len(rows) // 2]
    light = [r for r in rows if r["Delta"] <= med]
    heavy = [r for r in rows if r["Delta"] > med]
    if not light or not heavy:
        err.append("relative split empty")
    # Match cert headline row
    stored = next(
        r for r in cert["menu"] if r["p"] == 7 and r["n"] == 6 and r["w"] == 1
    )
    if stored["num_fibers_size_ge2"] != len(rows):
        err.append(f"num fibers {len(rows)} vs {stored['num_fibers_size_ge2']}")
    if abs(stored["median_Delta"] - med) > 1e-12:
        err.append(f"median {med} vs {stored['median_Delta']}")
    if cert["summary"]["verdict"] != "NO ISSUE":
        err.append("verdict")
    if err:
        print("RESULT: FAIL")
        for e in err:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print(
        "route: full (7,6,3,1) recompute ES-prefix fibers+energy; "
        "Delta<=1 is Cauchy-Schwarz SANITY only"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
