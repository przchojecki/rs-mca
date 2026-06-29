#!/usr/bin/env python3
"""Exact p=257 quotient-periodic locator matrix (toy-case database).

Generalizes `p257_locator_certificate.py` (which checks one cell,
`N=16, rho=1/2, t=1`) to the full computationally-feasible matrix of smooth
quotient scales over `F_257`.  `F_257^*` is cyclic of order `256 = 2^8`
(257 is the Fermat prime `2^8+1`), so it has a clean dyadic tower of subgroups.

For each cell `(N, rho, t)` with quotient order `N in {2,4,8,16}`, rate
`rho in {1/2,1/4}` and slack `t in {1,2}` we set

    a   = 256 / N                 (the locator exponent X^a; fiber size)
    ell = rho * N + t             (number of fibers chosen; = k/a + t)
    k   = (ell - t) * a           (code degree, = rho * 256)

and, over the unique order-`N` subgroup `Q_N <= F_257^*`, enumerate *every*
`ell`-subset `A` of `Q_N` (exact, no sampling).  For each `A` the whole-fiber
locator is

    L_A(X) = prod_{b in A} (X^a - b) = sum_{j=0}^{ell} c_j X^{a j},

i.e. `prod_{b in A}(Y - b)` evaluated at `Y = X^a`.  We check:

* `c_ell = 1` (monic top term at degree `a*ell`);
* the slope `c_{ell-1} = -e_1(A) = -sum(A)` (Vieta), recorded as `z = -sum(A)`;
* `L_A` vanishes at every `b in A` as a polynomial in `Y` (certifies the exact
  coefficient arithmetic; equivalently `L_A` vanishes on its `ell*a` roots
  `{x : x^a in A}`, the whole-fiber support);
* the power map `x -> x^a` is exactly `a`-to-1 onto `Q_N`, so the support has
  size `ell*a`.

and record, per cell, the restricted-sumset / slope statistics that the M1/L1
quotient-periodic ledger consumes: the number of distinct slopes
`z = -sum(A)` (the restricted sumset size over `Q_N`), whether slope `0`
occurs, and the slope-multiplicity histogram.

Script output standard (agents.md):
  1. inputs        -> "inputs" block + per-cell N,rho,t,a,ell,k
  2. object        -> "object"
  3. result        -> "cells" + "summary"
  4. proof cert    -> deterministic JSON (sorted keys); --check re-verifies
  5. theorem id    -> "theorem_id"
  6. PROVED/EXPERIMENTAL/COUNTEREXAMPLE -> "status"

This is a LOCATOR / restricted-sum table, not an MCA bad-slope exhaustion: at
n=256 the MCA support enumeration C(256, support) is astronomical, so only the
locator object is exhausted here.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from math import comb
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

STATUS = "PROVED"
THEOREM_ID = "agents.md L1/L3 toy-case (q=257); tex/RS_disproof_v3.tex V2 (ex:257), lem:locator"
OBJECT = "p=257 quotient-periodic locator matrix"

P = 257
N_FULL = P - 1            # 256, the order of F_257^*
BASE = 2                  # 2 has multiplicative order 16 in F_257^*
BASE_ORDER = 16

GRID_N: Tuple[int, ...] = (2, 4, 8, 16)
GRID_RHO: Tuple[Tuple[int, int], ...] = ((1, 2), (1, 4))
GRID_T: Tuple[int, ...] = (1, 2)


def order_n_subgroup(order: int) -> List[int]:
    """The unique order-`order` subgroup of F_257^* (order must divide 16)."""
    if BASE_ORDER % order != 0:
        raise ValueError(f"order {order} does not divide base order {BASE_ORDER}")
    generator = pow(BASE, BASE_ORDER // order, P)
    values = [pow(generator, i, P) for i in range(order)]
    if len(set(values)) != order or pow(generator, order, P) != 1:
        raise ValueError(f"failed to build order-{order} subgroup")
    return sorted(values)


def multiply_by_y_minus_b(coeffs: List[int], b_value: int) -> List[int]:
    out = [0] * (len(coeffs) + 1)
    for degree, coeff in enumerate(coeffs):
        out[degree] = (out[degree] - b_value * coeff) % P
        out[degree + 1] = (out[degree + 1] + coeff) % P
    return out


def locator_coeffs(a_values: Sequence[int]) -> List[int]:
    """Coefficients of prod_{b}(Y - b); coeffs[j] is the coeff of X^{a*j}."""
    coeffs = [1]
    for b_value in a_values:
        coeffs = multiply_by_y_minus_b(coeffs, b_value)
    return coeffs


def poly_eval(coeffs: Sequence[int], y_value: int) -> int:
    acc = 0
    for coeff in reversed(coeffs):
        acc = (acc * y_value + coeff) % P
    return acc


def cell_spec(num: int, den: int, big_n: int, t: int) -> Dict[str, Any]:
    a_exp = N_FULL // big_n
    if (num * big_n) % den != 0:
        return {"feasible": False, "a": a_exp,
                "reason": f"rho*N = {num*big_n}/{den} is not an integer"}
    ell = (num * big_n) // den + t
    k_deg = (ell - t) * a_exp
    if ell < 1 or ell > big_n:
        return {"feasible": False, "a": a_exp, "ell": ell, "k": k_deg,
                "reason": f"ell = {ell} not in [1, N={big_n}]"}
    return {"feasible": True, "a": a_exp, "ell": ell, "k": k_deg}


def run_cell(num: int, den: int, big_n: int, t: int) -> Dict[str, Any]:
    spec = cell_spec(num, den, big_n, t)
    row: Dict[str, Any] = {
        "N": big_n, "rho": f"{num}/{den}", "t": t,
        "a": spec.get("a"), "ell": spec.get("ell"), "k": spec.get("k"),
    }
    if not spec["feasible"]:
        row["feasible"] = False
        row["reason"] = spec["reason"]
        return row

    a_exp, ell = spec["a"], spec["ell"]
    subgroup = order_n_subgroup(big_n)
    subgroup_set = set(subgroup)

    # The power map x -> x^a must be exactly a-to-1 onto Q_N (so |support| = ell*a).
    fiber_counts = Counter(pow(x, a_exp, P) for x in range(1, P))
    fiber_ok = (set(fiber_counts) == subgroup_set
                and all(fiber_counts[b] == a_exp for b in subgroup))

    slope_counts: Counter = Counter()
    subsets = 0
    all_ok = fiber_ok
    for a_subset in itertools.combinations(subgroup, ell):
        subsets += 1
        coeffs = locator_coeffs(a_subset)
        z_value = (-sum(a_subset)) % P                       # slope = -e_1(A)
        top_ok = coeffs[ell] == 1
        slope_ok = coeffs[ell - 1] == z_value                # Vieta: c_{ell-1} = -e_1
        vanish_ok = all(poly_eval(coeffs, b) == 0 for b in a_subset)
        if not (top_ok and slope_ok and vanish_ok):
            all_ok = False
        slope_counts[z_value] += 1

    multiplicity_hist = Counter(slope_counts.values())
    row.update({
        "feasible": True,
        "fiber_size": a_exp,
        "power_map_a_to_one_ok": fiber_ok,
        "support_size": ell * a_exp,
        "subsets_checked": subsets,
        "expected_subsets": comb(big_n, ell),
        "subsets_match_expected": subsets == comb(big_n, ell),
        "all_subsets_ok": all_ok,
        "slope_dimension": t,                                # locator has e_1..e_t above the code
        "restricted_sumset_size": len(slope_counts),         # distinct z = -sum(A)
        "unique_slope_count": len(slope_counts),
        "zero_slope_seen": 0 in slope_counts,
        # restricted sumset lives in F_257, so "full" coverage means 257 slopes
        "slope_coverage_full": len(slope_counts) == P,
        "slope_multiplicity_histogram": {
            str(m): c for m, c in sorted(multiplicity_hist.items())
        },
    })
    return row


def build_certificate() -> Dict[str, Any]:
    cells: List[Dict[str, Any]] = []
    for num, den in GRID_RHO:
        for big_n in GRID_N:
            for t in GRID_T:
                cells.append(run_cell(num, den, big_n, t))

    feasible = [c for c in cells if c.get("feasible")]
    all_ok = all(c["all_subsets_ok"] for c in feasible)

    # Cross-check against the committed single-cell p257 certificate.
    p257_row = next(
        (c for c in feasible
         if c["N"] == 16 and c["rho"] == "1/2" and c["t"] == 1),
        None,
    )
    cross_check = None
    if p257_row is not None:
        cross_check = {
            "cell": "N=16, rho=1/2, t=1",
            "subsets_checked": p257_row["subsets_checked"],
            "expected_subsets_11440": p257_row["subsets_checked"] == 11440,
            "unique_slopes_256": p257_row["unique_slope_count"] == 256,
            "support_size_144": p257_row["support_size"] == 144,
            "zero_slope_absent": p257_row["zero_slope_seen"] is False,
            "all_ok": p257_row["all_subsets_ok"],
            "reproduces_p257_locator_certificate": (
                p257_row["subsets_checked"] == 11440
                and p257_row["unique_slope_count"] == 256
                and p257_row["support_size"] == 144
                and p257_row["zero_slope_seen"] is False
                and p257_row["all_subsets_ok"]
            ),
        }

    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "inputs": {
            "p": P,
            "domain": "F_257^*",
            "n": N_FULL,
            "subgroup_tower": "Q_N = unique order-N subgroup of F_257^*, N in {2,4,8,16}",
            "grid_N": list(GRID_N),
            "grid_rho": [f"{a}/{b}" for a, b in GRID_RHO],
            "grid_t": list(GRID_T),
            "object_checked": "whole-fiber locator prod_{b in A}(X^a - b), exact mod-257",
            "scope": "locator / restricted-sum table only; not MCA bad-slope exhaustion",
        },
        "cells": cells,
        "summary": {
            "total_cells": len(cells),
            "feasible_cells": len(feasible),
            "infeasible_cells": len(cells) - len(feasible),
            "all_feasible_cells_ok": all_ok,
            "cross_check_p257": cross_check,
        },
    }


def render(cert: Dict[str, Any]) -> str:
    return json.dumps(cert, indent=2, sort_keys=True) + "\n"


def print_text(cert: Dict[str, Any]) -> None:
    print(OBJECT)
    print(f"Status: {STATUS}")
    print(f"Theorem/problem ID: {THEOREM_ID}")
    print("Object: whole-fiber locator restricted-sum statistics over F_257.")
    print()
    header = (
        f"{'rho':>4} {'N':>3} {'t':>2} {'a':>4} {'ell':>4} {'k':>4} "
        f"{'subsets':>8} {'supp':>5} {'slopes':>7} {'zero':>5} {'hist'}"
    )
    print(header)
    for c in cert["cells"]:
        if not c.get("feasible"):
            print(f"{c['rho']:>4} {c['N']:>3} {c['t']:>2} "
                  f"{'-':>4} {'-':>4} {'-':>4} {'infeasible':>8}  ({c['reason']})")
            continue
        hist = ",".join(f"{k}:{v}" for k, v in c["slope_multiplicity_histogram"].items())
        print(f"{c['rho']:>4} {c['N']:>3} {c['t']:>2} {c['a']:>4} {c['ell']:>4} "
              f"{c['k']:>4} {c['subsets_checked']:>8} {c['support_size']:>5} "
              f"{c['unique_slope_count']:>7} {str(c['zero_slope_seen']):>5} {{{hist}}}")
    print()
    summary = cert["summary"]
    print(f"feasible cells: {summary['feasible_cells']}/{summary['total_cells']}")
    print(f"all feasible cells pass: {summary['all_feasible_cells_ok']}")
    cross = summary["cross_check_p257"]
    if cross is not None:
        print("cross-check vs p257_locator_certificate.py "
              f"(N=16, rho=1/2, t=1): {cross['reproduces_p257_locator_certificate']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="p=257 quotient-periodic locator matrix.")
    parser.add_argument("--format", choices=("text", "json"), default="text",
                        help="output format for stdout")
    parser.add_argument("--output", type=Path,
                        help="write the generated certificate JSON to this path")
    parser.add_argument("--check", type=Path,
                        help="compare a stored certificate file with a fresh run")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cert = build_certificate()
    rendered = render(cert)

    if args.check is not None:
        existing = args.check.read_text(encoding="utf-8")
        if existing != rendered:
            raise SystemExit(f"certificate mismatch: {args.check}")
        print(f"certificate matches: {args.check}")
        return 0

    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")

    if args.format == "json":
        print(rendered, end="")
    else:
        print_text(cert)

    return 0 if cert["summary"]["all_feasible_cells_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
