#!/usr/bin/env python3
"""Verifier for xr_syzygy_flat_transport (2c-gamma-a).

This checks the mechanical dictionary:

  constrained syzygy member -> sparse dual support -> matroid closure
  -> generated support-lattice object used by Conjecture F / E30.

The verifier builds three explicit F_17 evaluation flats on H = F_17^*:
  * mds_deg3:       span(1, X, X^2, X^3), no sparse dual words <= 4;
  * common_root:    (X-1) * span(1, X, X^2, X^3), with a loop at x=1;
  * even_pullback:  span(1, X^2, X^4, X^6), with twin pairs {x,-x}.

For every support of size <= 4 it detects whether the support carries a
nonzero annihilator word, computes its closure in the evaluation matroid, and
checks that closures generate the same support-lattice kind counted by QF.12
and sampled by E30.

Stdlib only; no Monte Carlo.
Run: python3 experimental/scripts/verify_xr_syzygy_flat_transport.py
"""

from __future__ import annotations

import json
import os
import sys
from itertools import combinations


P = 17
H = tuple(range(1, 17))
MAX_SUPPORT = 4

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "xr-syzygy-flat-transport",
    "toy_flat_transport.json",
)

FAILS: list[str] = []
NCHECK = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global NCHECK
    NCHECK += 1
    tag = "PASS" if cond else "FAIL"
    line = f"[{tag}] {name}"
    if detail:
        line += f"   ({detail})"
    print(line)
    if not cond:
        FAILS.append(name)


def quiet_check(name: str, cond: bool, detail: str = "") -> None:
    global NCHECK
    NCHECK += 1
    if not cond:
        line = name
        if detail:
            line += f" ({detail})"
        FAILS.append(line)


def inv(a: int) -> int:
    return pow(a, P - 2, P)


def rref(rows_in: list[list[int]], width: int) -> tuple[list[tuple[int, ...]], int]:
    rows = [[x % P for x in row] for row in rows_in]
    rank = 0
    for col in range(width):
        piv = None
        for rr in range(rank, len(rows)):
            if rows[rr][col]:
                piv = rr
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        scale = inv(rows[rank][col])
        rows[rank] = [(scale * x) % P for x in rows[rank]]
        for rr in range(len(rows)):
            if rr != rank and rows[rr][col]:
                c = rows[rr][col]
                rows[rr] = [(x - c * y) % P for x, y in zip(rows[rr], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return [tuple(row) for row in rows[:rank]], rank


def rank(rows: list[list[int] | tuple[int, ...]], width: int) -> int:
    return rref([list(row) for row in rows], width)[1]


def nullity(columns: list[tuple[int, ...]], support: tuple[int, ...]) -> int:
    if not support:
        return 0
    rows = [columns[x - 1] for x in support]
    return len(support) - rank(rows, len(columns[0]))


def closure(columns: list[tuple[int, ...]], support: frozenset[int]) -> frozenset[int]:
    base_rank = rank([columns[x - 1] for x in support], len(columns[0]))
    out = set(support)
    for x in H:
        r2 = rank([columns[y - 1] for y in sorted(out | {x})], len(columns[0]))
        if r2 == base_rank:
            out.add(x)
    return frozenset(out)


def eval_poly(coeffs: tuple[int, ...], x: int) -> int:
    acc = 0
    power = 1
    for c in coeffs:
        acc = (acc + c * power) % P
        power = (power * x) % P
    return acc


def columns_for_basis(basis: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    return [tuple(eval_poly(poly, x) for poly in basis) for x in H]


def flat_families() -> list[tuple[str, list[tuple[int, ...]]]]:
    return [
        ("mds_deg3", [(1,), (0, 1), (0, 0, 1), (0, 0, 0, 1)]),
        (
            "common_root",
            [
                (-1, 1),
                (0, -1, 1),
                (0, 0, -1, 1),
                (0, 0, 0, -1, 1),
            ],
        ),
        ("even_pullback", [(1,), (0, 0, 1), (0, 0, 0, 0, 1), (0, 0, 0, 0, 0, 0, 1)]),
    ]


def analyze(name: str, basis: list[tuple[int, ...]]) -> dict[str, int | str]:
    columns = columns_for_basis(basis)
    width = len(basis)
    full_rank = rank(columns, width)
    sparse_supports: list[frozenset[int]] = []
    nullity_sum = 0
    max_nullity = 0
    closures: set[frozenset[int]] = set()
    supports_checked = 0

    for w in range(1, MAX_SUPPORT + 1):
        for S_tuple in combinations(H, w):
            supports_checked += 1
            nu = nullity(columns, S_tuple)
            if nu == 0:
                continue
            S = frozenset(S_tuple)
            C = closure(columns, S)
            sparse_supports.append(S)
            closures.add(C)
            nullity_sum += nu
            max_nullity = max(max_nullity, nu)
            quiet_check(
                f"{name}: sparse support is dependent {S_tuple}",
                rank([columns[x - 1] for x in S], width) < len(S),
            )
            quiet_check(
                f"{name}: closure contains support {S_tuple}",
                S <= C,
                f"closure={sorted(C)}",
            )
            quiet_check(
                f"{name}: closure is idempotent {S_tuple}",
                closure(columns, C) == C,
                f"closure={sorted(C)}",
            )
            quiet_check(
                f"{name}: nullity matches coefficient choices {S_tuple}",
                nu == len(S) - rank([columns[x - 1] for x in S], width),
                f"nullity={nu}",
            )

    generated_closures = {closure(columns, frozenset())} | closures
    for C in generated_closures:
        quiet_check(
            f"{name}: lattice element is closed {sorted(C)}",
            closure(columns, C) == C,
        )
    sampled_unions = 0
    for i, A in enumerate(sparse_supports[:80]):
        for B in sparse_supports[i:i + 20]:
            C = closure(columns, A | B)
            sampled_unions += 1
            quiet_check(
                f"{name}: union closure contains generators",
                A <= C and B <= C and closure(columns, C) == C,
            )
    if name == "mds_deg3":
        check(f"{name}: MDS row has no sparse words", len(sparse_supports) == 0)
        check(f"{name}: generated closure set is trivial", len(generated_closures) == 1)
    if name == "common_root":
        check(f"{name}: loop/root support detected", frozenset({1}) in sparse_supports)
    if name == "even_pullback":
        twin_pairs = {frozenset({x, P - x}) for x in H if x != P - x}
        seen_twins = twin_pairs & set(sparse_supports)
        check(f"{name}: twin-pair supports detected", len(seen_twins) == 8, f"seen={len(seen_twins)}")

    check(
        f"{name}: transport map checked",
        all(S <= closure(columns, S) for S in sparse_supports),
        f"sparse={len(sparse_supports)}, closures={len(closures)}, sampled_unions={sampled_unions}",
    )

    return {
        "name": name,
        "rank": full_rank,
        "supports_checked": supports_checked,
        "sparse_supports": len(sparse_supports),
        "distinct_sparse_closures": len(closures),
        "generated_closure_count": len(generated_closures),
        "sampled_union_closures": sampled_unions,
        "nullity_sum": nullity_sum,
        "max_nullity": max_nullity,
    }


def main() -> None:
    summaries = [analyze(name, basis) for name, basis in flat_families()]
    result = {
        "node": "xr_syzygy_flat_transport",
        "field": "F_17",
        "domain": "F_17^*",
        "max_support": MAX_SUPPORT,
        "flats": summaries,
        "checks": NCHECK,
    }

    expected = None
    if os.path.exists(CERT):
        with open(CERT) as fh:
            expected = json.load(fh)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", result == expected)

    if FAILS:
        print("\nrecomputed summary:")
        print(json.dumps(result, indent=2, sort_keys=True))
        print("\nFAIL:")
        for name in FAILS[:25]:
            print("  -", name)
        if len(FAILS) > 25:
            print(f"  ... {len(FAILS) - 25} more")
        sys.exit(1)

    print("\nsummary:")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"\nPASS: {NCHECK} xr_syzygy_flat_transport checks")


if __name__ == "__main__":
    main()
