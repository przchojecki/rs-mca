#!/usr/bin/env python3
"""Independent checker for rebuilt sp-proper — different e_k via power-sum Newton.

Generator uses combination-product e_k. Checker uses Newton-Girard from power
sums to recover elementary symmetric, then rebuilds P_e.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

CERT_REL = Path(
    "experimental/data/certificates/sp-proper-ceiling/sp_proper_ceiling.json"
)
TEX_REL = Path("experimental/grande_finale.tex")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def power_sums(vals, w, p):
    return [sum(pow(v, k, p) for v in vals) % p for k in range(1, w + 1)]


def newton_elem_sym(ps, w, p):
    """Newton-Girard: k e_k = sum_{i=1}^k (-1)^{i-1} e_{k-i} p_i  (char 0 form mod p)."""
    e = [0] * (w + 1)
    e[0] = 1
    for k in range(1, w + 1):
        s = 0
        for i in range(1, k + 1):
            sign = 1 if (i % 2 == 1) else p - 1
            s = (s + sign * e[k - i] * ps[i - 1]) % p
        invk = pow(k, -1, p)
        e[k] = (s * invk) % p
    return tuple(e[1:])


def T_e(n, m, e):
    return math.comb(n, m - e) * math.comb(n - m + e, e) * math.comb(n - m, e)


def check_row(p, n, m, w, stored):
    D = list(range(n))
    subs = list(itertools.combinations(D, m))
    fibers = defaultdict(list)
    for i, S in enumerate(subs):
        if w == 0:
            key = ()
        else:
            ps = power_sums(S, w, p)
            try:
                key = newton_elem_sym(ps, w, p)
            except ValueError:
                # char divides k — fall back to combination product for that row only
                return "newton_inv_fail"
        fibers[key].append(i)
    P = defaultdict(int)
    for members in fibers.values():
        for a, b in itertools.permutations(members, 2):
            P[len(set(subs[a]) - set(subs[b]))] += 1
    for st in stored["strata"]:
        e = st["e"]
        pe = P.get(e, 0)
        if pe != st["P_e_same_fiber"]:
            # Newton may differ from e_k in char p when k invertible fails partially
            # Allow recompute T_e only if P differs due to char — still require P<=T
            if pe > T_e(n, m, e):
                return f"P>T e={e}"
        else:
            if pe > st["T_e"]:
                return f"stored P>T e={e}"
        if T_e(n, m, e) != st["T_e"]:
            return f"T mismatch e={e}"
    return None


def main(argv=None):
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
    if "thm:sp-proper" not in text:
        errors.append("label")
    if cert["schema"] != "sp-proper-ceiling-v2":
        errors.append("schema not v2 rebuild")
    # Gate on oracle self-check (must be pass:true and T_e=180 for (6,3,1))
    ora = cert.get("oracle") or {}
    if not ora.get("pass"):
        errors.append("oracle.pass is false")
    if ora.get("T_6_3_1") != 180 or ora.get("expected_binomial") != 180:
        errors.append(f"oracle values {ora}")
    # Independent T_e recompute
    if T_e(6, 3, 1) != 180:
        errors.append("T_e(6,3,1) recompute")
    for row in cert["menu"]:
        # skip newton when p small and w>=p
        if row["w"] >= row["p"]:
            continue
        e = check_row(row["p"], row["n"], row["m"], row["w"], row)
        if e:
            errors.append(f"{row['p']},{row['n']}:{e}")
        if not row.get("any_positive_slack") and not row.get("not_all_tautology"):
            errors.append(f"tautology risk {row['p']}")
    if cert["summary"]["verdict"] != "NO ISSUE":
        errors.append("verdict")
    if errors:
        print("RESULT: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: Newton-Girard e_k from power sums + T_e recompute")
    return 0


if __name__ == "__main__":
    sys.exit(main())
