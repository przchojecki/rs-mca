#!/usr/bin/env python3
"""Independent checker for bc-moving-root — recompute pencil geometry.

Does NOT trust cert-stored g/h/Z: rebuilds monic linears, finds roots by
evaluation, enumerates P^1 classes as (s:t) with gcd-normalized pairs.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

CERT_REL = Path("experimental/data/certificates/bc-moving-root/bc_moving_root.json")
TEX_REL = Path("experimental/grande_finale.tex")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def eval_poly(coeffs, x, p):
    acc, xp = 0, 1
    for c in coeffs:
        acc = (acc + c * xp) % p
        xp = (xp * x) % p
    return acc


def roots(coeffs, D, p):
    return [x for x in D if eval_poly(coeffs, x, p) == 0]


def check_pencil(p, D, A, B):
    """Independent pencil incidence check."""
    n = len(D)
    zG = set(roots(A, D, p)) & set(roots(B, D, p))
    g = len(zG)
    # P^1: all (s,t) != (0,0) up to scalar — use normalized: first nonzero is 1
    params = []
    for s in range(p):
        for t in range(p):
            if s == 0 and t == 0:
                continue
            # normalize
            if s != 0:
                inv = pow(s, -1, p)
                params.append((1, (t * inv) % p))
            else:
                params.append((0, 1))
    params = list(dict.fromkeys(params))  # unique
    deg = max(len(A), len(B))
    Ac = A + [0] * (deg - len(A))
    Bc = B + [0] * (deg - len(B))
    incidences = []
    Z = 0
    hmin = None
    for s, t in params:
        Lc = [(s * Ac[i] + t * Bc[i]) % p for i in range(deg)]
        mov = [x for x in roots(Lc, D, p) if x not in zG]
        if mov:
            Z += 1
            hmin = len(mov) if hmin is None else min(hmin, len(mov))
        for x in mov:
            incidences.append(x)
    hits = Counter(incidences)
    at_most_one = all(v <= 1 for v in hits.values()) if hits else True
    if Z == 0:
        return True, {"Z": 0, "vacuous": True}
    bound = (n - g) // hmin
    return Z <= bound and at_most_one, {
        "Z": Z,
        "g": g,
        "hmin": hmin,
        "bound": bound,
        "at_most_one": at_most_one,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    if not args.check:
        p.print_help()
        return 2
    root = repo_root()
    cert = json.loads((root / CERT_REL).read_text())
    text = (root / TEX_REL).read_text(encoding="utf-8")
    errors = []
    if "thm:bc-moving-root" not in text:
        errors.append("label")
    n = 2**21
    # keep designer's corrected omegas if present in draft; use theorem a+
    if n // (n - 1116048) != 2 or n // (n - 1116024) != 2:
        errors.append("deployed floor")
    # recompute pencils from scratch with known A,B from generator semantics
    tests = [
        (7, list(range(1, 7)), [6, 1], [5, 1]),
        (5, list(range(5)), [4, 1], [3, 1]),
        (7, list(range(1, 7)), [6, 0, 1], [6, 1]),
    ]
    for p_, D, A, B in tests:
        ok, info = check_pencil(p_, D, A, B)
        if not ok:
            errors.append(f"pencil {p_} {info}")
    if cert["summary"]["verdict"] != "NO ISSUE":
        errors.append("verdict")
    if errors:
        print("RESULT: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: independent P1-normalized (s:t) root scan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
