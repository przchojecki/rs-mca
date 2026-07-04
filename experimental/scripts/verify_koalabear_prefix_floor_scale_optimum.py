#!/usr/bin/env python3
"""Verifier for the KoalaBear prefix-floor scale-optimum certificate.

Deployed row (cor:deployed, [ABF26 sec 6.3]): B = F_p, p = 2^31 - 2^24 + 1;
F = F_{p^6}, q = p^6; D = the multiplicative subgroup of B^x of order
n = 2^21; k = 2^20; target eps* = 2^-128.

prop:graded-prefix-floor admits any map-smooth scale of degree c >= 2; on the
order-2^21 subgroup the power maps phi = X^c are map-smooth exactly for the
dyadic c | n, so c = 2 is the finest admissible scale. For each scale and
each route this certificate records the largest m with

  MCA route:  C(n/c, m) * k > p^w * (q + k),  w = m - ceil((k+1)/c)
  list route: C(n/c, m)     > p^w * T,        w = m - ceil(k/c),
                                              T = floor(q / 2^128)

together with adjacency (m+1 fails). The MCA optimum (c=2, m=558019,
Delta = m*c - k = 67462) moves the deployed unsafe edge from
15331/32768 to 490557/1048576 (+70 agreement steps); the list optimum
(c=2, m=558022, Delta=67468) moves the list edge by +76 steps. Since c=2
is the finest admissible scale and Delta is monotone toward finer scale,
the certificate also exhausts the route's dyadic headroom on this row
(rem:entropy-frontier envelope g*(1/2,31) ~ 0.0321617; achieved
67462/2^21 ~ 0.0321646 via finite-size corrections).

Modes:
  --write            regenerate the certificate JSON deterministically
  --check            verify scales c >= 4, both routes (~6 min)
  --check --full     verify all scales including c = 2 (~35 min)
Every check recomputes both sides of the inequality from the row
parameters in exact integer arithmetic and confirms adjacency; nothing is
trusted from the JSON beyond the frozen m-values under test.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

P = 2**31 - 2**24 + 1
Q = P**6
N = 2**21
K = 2**20
T_LIST = Q // 2**128

HERE = Path(__file__).resolve().parent
CERT = HERE.parent / "data" / "certificates" / "koalabear-prefix-floor-scale-optimum" / "kb_prefix_floor_scale_optimum.json"

M_MCA = {2: 558019, 4: 279007, 8: 139501, 16: 69748, 32: 34871, 64: 17433, 128: 8714, 256: 4355}
M_LIST = {2: 558022, 4: 279009, 8: 139503, 16: 69750, 32: 34874, 64: 17436, 128: 8717, 256: 4357}


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def w_of(route: str, c: int, m: int) -> int:
    return m - ceil_div(K + 1 if route == "mca" else K, c)


def holds(route: str, c: int, m: int) -> bool:
    if m > N // c:
        return False
    w = w_of(route, c, m)
    if w < 0:
        return False
    if route == "mca":
        return comb(N // c, m) * K > P**w * (Q + K)
    return comb(N // c, m) > P**w * T_LIST


def row(route: str, c: int, m: int) -> dict:
    a = m * c
    edge = Fraction(N - a, N)
    return {
        "route": route, "c": c, "N": N // c, "m": m, "w": w_of(route, c, m),
        "Delta": a - K, "agreement_a": a,
        "unsafe_edge_delta_num": edge.numerator, "unsafe_edge_delta_den": edge.denominator,
    }


def payload() -> dict:
    rows = [row("mca", c, m) for c, m in sorted(M_MCA.items())] + \
           [row("list", c, m) for c, m in sorted(M_LIST.items())]
    return {
        "schema": "koalabear-prefix-floor-scale-optimum-v1",
        "object": "graded locator-prefix floor (prop:graded-prefix-floor + thm:A), scale-optimized",
        "sampler": "finite_affine",
        "q_line": str(Q),
        "row": {"base_prime_p": P, "extension_degree": 6, "n": N, "k": K,
                 "domain": "multiplicative subgroup of F_p^x of order 2^21",
                 "target": "2^-128", "list_budget_T": str(T_LIST)},
        "rows": rows,
        "deployed_anchor_mca": {"c": 16, "m": 69748, "w": 4211, "Delta": 67392,
                                 "note": "reproduces rem:exact-frontier / kb_mca_pf exactly"},
        "optimum_mca": {"c": 2, "m": 558019, "Delta": 67462,
                         "new_unsafe_edge": "490557/1048576",
                         "a_steps_closed_vs_deployed": 70},
        "optimum_list": {"c": 2, "m": 558022, "Delta": 67468,
                          "new_unsafe_edge": "245277/524288",
                          "a_steps_closed_vs_deployed": 76},
        "route_exhaustion": "c=2 is the finest map-smooth power scale on the 2-power domain and Delta is monotone toward finer scale, so the dyadic headroom of the graded prefix-floor route is exhausted at this certificate.",
        "nonclaims": [
            "No safe-side claim: this widens the certified unsafe band only.",
            "No claim beyond the graded prefix-floor route; the remaining open band down to delta = 1/4 (import) / 1/6-deep (self-contained) is untouched.",
            "Closed-grid statements on the integer agreement lattice only; no supremum claim.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--full", action="store_true", help="include the c=2 checks (~35 min)")
    args = parser.parse_args()

    if args.write:
        CERT.parent.mkdir(parents=True, exist_ok=True)
        CERT.write_text(json.dumps(payload(), indent=1, sort_keys=True) + "\n")
        print(f"wrote {CERT}")
    if args.check:
        recorded = json.loads(CERT.read_text())
        expected = payload()
        if recorded != expected:
            print("FAIL: certificate JSON does not match deterministic regeneration", file=sys.stderr)
            raise SystemExit(1)
        scales = sorted(M_MCA) if args.full else [c for c in sorted(M_MCA) if c >= 4]
        checks = 0
        for route, table in (("mca", M_MCA), ("list", M_LIST)):
            for c in scales:
                m = table[c]
                if not holds(route, c, m):
                    print(f"FAIL: route={route} c={c} m={m} does not hold", file=sys.stderr)
                    raise SystemExit(1)
                if holds(route, c, m + 1):
                    print(f"FAIL: route={route} c={c} m={m}+1 unexpectedly holds (not adjacent-tight)", file=sys.stderr)
                    raise SystemExit(1)
                checks += 2
        skipped = "" if args.full else " (c=2 skipped; run --check --full for the ~35 min complete pass)"
        print(f"PASS: {checks} inequality checks, all adjacent-tight{skipped}")
    if not (args.write or args.check):
        parser.error("pass --write and/or --check")


if __name__ == "__main__":
    main()
