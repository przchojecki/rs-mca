#!/usr/bin/env python3
"""Independent checker for q-implies-sp — DIFFERENT algorithm from generator.

Generator: DP elementary-symmetric + permutations for ordered pairs.
Checker: direct product formulas for e_k via itertools combinations of products,
and unordered pair enumeration doubled for P_e.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

CERT_REL = Path("experimental/data/certificates/q-implies-sp/q_implies_sp.json")
TEX_REL = Path("experimental/grande_finale.tex")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def e_k_direct(vals: tuple[int, ...], k: int, p: int) -> int:
    """e_k as sum of products over k-subsets (not the DP recurrence)."""
    if k == 0:
        return 1
    s = 0
    for comb in itertools.combinations(vals, k):
        prod = 1
        for v in comb:
            prod = (prod * (v % p)) % p
        s = (s + prod) % p
    return s


def prefix_direct(vals: tuple[int, ...], w: int, p: int) -> tuple[int, ...]:
    return tuple(e_k_direct(vals, k, p) for k in range(1, w + 1))


def check_row(p: int, n: int, m: int, w: int, stored: dict) -> str | None:
    D = list(range(n))
    subs = list(itertools.combinations(D, m))
    C = len(subs)
    fibers: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for i, S in enumerate(subs):
        fibers[prefix_direct(S, w, p)].append(i)
    maxN = max(len(v) for v in fibers.values()) if fibers else 0
    sumN2 = sum(len(v) ** 2 for v in fibers.values())
    # unordered pairs within fiber, then *2 for ordered P_e
    P = defaultdict(int)
    for members in fibers.values():
        for a, b in itertools.combinations(members, 2):
            e = len(set(subs[a]) - set(subs[b]))
            P[e] += 2  # both orders
    sumP = sum(P.values())
    sumPgt = sum(P[e] for e in P if e > w)
    if sumN2 != C + sumP:
        return "identity"
    if sumPgt > (maxN - 1) * C:
        return "ineq"
    if stored["maxN"] != maxN or stored["sumP_e_gt_w"] != sumPgt:
        return f"mismatch maxN={maxN}/{stored['maxN']} Pgt={sumPgt}/{stored['sumP_e_gt_w']}"
    return None


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
    if "thm:q-implies-sp" not in text:
        errors.append("label")
    for row in cert["menu"]:
        e = check_row(row["p"], row["n"], row["m"], row["w"], row)
        if e:
            errors.append(f"{row['p']},{row['n']}:{e}")
    if cert["summary"]["verdict"] != "NO ISSUE":
        errors.append("verdict")
    if errors:
        print("RESULT: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: direct combination-product e_k + unordered pairs*2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
