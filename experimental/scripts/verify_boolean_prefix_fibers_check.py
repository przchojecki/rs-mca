#!/usr/bin/env python3
"""Checker: Newton-Girard e_k from power sums; must match maxN/histogram or FAIL."""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/boolean-prefix-fibers/boolean_prefix_fibers.json"
)


def power_sums(vals, w, p):
    return [sum(pow(v, k, p) for v in vals) % p for k in range(1, w + 1)]


def newton_e(ps, w, p):
    e = [0] * (w + 1)
    e[0] = 1
    for k in range(1, w + 1):
        s = 0
        for i in range(1, k + 1):
            sign = 1 if i % 2 == 1 else (p - 1)
            s = (s + sign * e[k - i] * ps[i - 1]) % p
        e[k] = (s * pow(k, -1, p)) % p
    return tuple(e[1:])


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
    # Forbid W19 reuse rows
    banned = {(5, 4, 2, 1), (7, 6, 3, 1), (7, 6, 3, 2), (11, 6, 3, 1), (11, 8, 4, 2)}
    for row in cert["menu"]:
        key = (row["p"], row["n"], row["m"], row["w"])
        if key in banned:
            err.append(f"W19-reuse row {key}")
        C = math.comb(row["n"], row["m"])
        if C != row["C"]:
            err.append("C")
        if str(Fraction(C, row["p"] ** row["w"])) != row["barN"]:
            err.append("barN")
        if row["w"] >= row["p"]:
            continue  # Newton inv fails
        subs = list(itertools.combinations(range(row["n"]), row["m"]))
        fib = defaultdict(list)
        for S in subs:
            try:
                k = newton_e(power_sums(S, row["w"], row["p"]), row["w"], row["p"])
            except Exception as ex:
                err.append(f"newton {ex}")
                continue
            fib[k].append(S)
        Ns = [len(v) for v in fib.values()]
        if sum(Ns) != C:
            err.append(f"sumN {sum(Ns)}!={C}")
        maxN = max(Ns) if Ns else 0
        if maxN != row["maxN"]:
            err.append(f"maxN {maxN} vs {row['maxN']} @ {key}")
        hist = {str(k): Ns.count(k) for k in sorted(set(Ns))}
        if hist != row["histogram"]:
            err.append(f"histogram mismatch @ {key}: {hist} vs {row['histogram']}")
    if cert["summary"]["verdict"] != "NO ISSUE":
        err.append("verdict")
    if not cert["claim_boundaries"].get("independent_recheck_confirms"):
        err.append("flag")
    if err:
        print("RESULT: FAIL")
        for e in err:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: Newton-Girard e_k from power sums; maxN+histogram must match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
