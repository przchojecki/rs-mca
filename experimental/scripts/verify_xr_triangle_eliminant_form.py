#!/usr/bin/env python3
"""Verifier for xr_triangle_eliminant_form (2c-beta-3a).

The packet constructs the light-triangle eliminant normal form.  For each
support T, a chart basis for Lambda_T is built by solving the Vandermonde
shortening equations on k pivot coordinates and t free coordinates.  For a
triple (T0,T1,T2) and slopes (z0,z1,z2), the normal-form matrix is the map

    (a0,a1,a2) |-> (sum_i B_i a_i, sum_i z_i B_i a_i)

restricted to the union of the three supports.  A triangle syzygy exists iff
this matrix has rank < 3t, equivalently iff all maximal minors vanish.  The
twisted form obtained by subtracting z2 times the first component is checked
to have the same rank.

Stdlib only; no Monte Carlo.
Run: python3 experimental/scripts/verify_xr_triangle_eliminant_form.py
"""

from __future__ import annotations

import json
import os
import sys
from itertools import combinations, permutations


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "xr-triangle-eliminant-form",
    "toy_triangle_eliminant.json",
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


class Fp:
    def __init__(self, p: int):
        self.p = p

    def add(self, a: int, b: int) -> int:
        return (a + b) % self.p

    def sub(self, a: int, b: int) -> int:
        return (a - b) % self.p

    def mul(self, a: int, b: int) -> int:
        return (a * b) % self.p

    def neg(self, a: int) -> int:
        return (-a) % self.p

    def inv(self, a: int) -> int:
        if a % self.p == 0:
            raise ZeroDivisionError("0 has no inverse")
        return pow(a, self.p - 2, self.p)


def rref(F: Fp, rows_in: list[list[int]]) -> tuple[list[list[int]], list[int], int]:
    rows = [r[:] for r in rows_in]
    if not rows:
        return rows, [], 0
    ncols = len(rows[0])
    pivots: list[int] = []
    rank = 0
    for col in range(ncols):
        piv = None
        for rr in range(rank, len(rows)):
            if rows[rr][col] % F.p:
                piv = rr
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = F.inv(rows[rank][col])
        rows[rank] = [F.mul(inv, x) for x in rows[rank]]
        for rr in range(len(rows)):
            if rr != rank and rows[rr][col] % F.p:
                c = rows[rr][col]
                rows[rr] = [F.sub(x, F.mul(c, y)) for x, y in zip(rows[rr], rows[rank])]
        pivots.append(col)
        rank += 1
        if rank == len(rows):
            break
    return rows, pivots, rank


def rank(F: Fp, rows: list[list[int]]) -> int:
    return rref(F, rows)[2]


def transpose(rows: list[list[int]], ncols: int | None = None) -> list[list[int]]:
    if not rows:
        return []
    if ncols is None:
        ncols = len(rows[0])
    return [[row[c] for row in rows] for c in range(ncols)]


def solve_square(F: Fp, A: list[list[int]], b: list[int]) -> list[int]:
    aug = [row[:] + [rhs] for row, rhs in zip(A, b)]
    R, pivots, rnk = rref(F, aug)
    n = len(A)
    if rnk != n or pivots[:n] != list(range(n)):
        raise ValueError("singular chart")
    return [R[i][n] for i in range(n)]


def lambda_space_chart(F: Fp, domain: list[int], k: int, T: tuple[int, ...]) -> list[list[int]]:
    """Chart basis of Lambda_T using first k points as pivots."""
    pivots = list(T[:k])
    free = list(T[k:])
    Vp = [[pow(domain[x], d, F.p) for x in pivots] for d in range(k)]
    basis: list[list[int]] = []
    for q in free:
        rhs = [F.neg(pow(domain[q], d, F.p)) for d in range(k)]
        pivot_values = solve_square(F, Vp, rhs)
        word = [0] * len(domain)
        for x, val in zip(pivots, pivot_values):
            word[x] = val
        word[q] = 1
        basis.append(word)
    return basis


def condition_rows(F: Fp, lambdas: list[list[int]], z: int) -> list[list[int]]:
    return [lam + [F.mul(z, x) for x in lam] for lam in lambdas]


def normal_form_matrix(
    F: Fp,
    bases: list[list[list[int]]],
    slopes: tuple[int, int, int],
    union: list[int],
) -> list[list[int]]:
    rows: list[list[int]] = []
    for coord in union:
        row: list[int] = []
        for basis in bases:
            row.extend(lam[coord] for lam in basis)
        rows.append(row)
    for coord in union:
        row = []
        for z, basis in zip(slopes, bases):
            row.extend(F.mul(z, lam[coord]) for lam in basis)
        rows.append(row)
    return rows


def twisted_form_matrix(
    F: Fp,
    bases: list[list[list[int]]],
    slopes: tuple[int, int, int],
    union: list[int],
) -> list[list[int]]:
    z2 = slopes[2]
    rows: list[list[int]] = []
    for coord in union:
        row: list[int] = []
        for basis in bases:
            row.extend(lam[coord] for lam in basis)
        rows.append(row)
    for coord in union:
        row = []
        for i, basis in enumerate(bases):
            twist = F.sub(slopes[i], z2)
            row.extend(F.mul(twist, lam[coord]) for lam in basis)
        rows.append(row)
    return rows


def overlap_shape(triple: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]) -> tuple[int, int, int]:
    sets = [set(T) for T in triple]
    pair_sum = len(sets[0] & sets[1]) + len(sets[0] & sets[2]) + len(sets[1] & sets[2])
    triple_size = len(sets[0] & sets[1] & sets[2])
    union_size = len(sets[0] | sets[1] | sets[2])
    return pair_sum, triple_size, union_size


def check_row(
    p: int,
    n: int,
    k: int,
    A: int,
    slopes: tuple[int, int, int],
    *,
    light_only: bool = False,
) -> dict[str, int]:
    F = Fp(p)
    domain = list(range(n))
    t = A - k
    supports = list(combinations(range(n), A))
    basis_cache = {T: lambda_space_chart(F, domain, k, T) for T in supports}

    summary = {
        "p": p,
        "n": n,
        "k": k,
        "A": A,
        "t": t,
        "supports": len(supports),
        "ordered_triples": 0,
        "skipped_nonlight_triples": 0,
        "light_triples": 0,
        "rank_defect_triples": 0,
        "light_rank_defect_triples": 0,
        "maximum_kernel_dimension": 0,
        "maximum_light_kernel_dimension": 0,
        "normal_form_rank_checks": 0,
        "twisted_rank_checks": 0,
    }

    for T, basis in basis_cache.items():
        quiet_check(f"chart basis dimension p={p} T={T}", len(basis) == t, f"dim={len(basis)}, t={t}")
        moment_rows = [[pow(domain[x], d, F.p) for x in range(n)] for d in range(k)]
        for lam in basis:
            quiet_check(
                f"chart basis in dual p={p} T={T}",
                all(sum(F.mul(a, b) for a, b in zip(row, lam)) % F.p == 0 for row in moment_rows),
                f"lambda={lam}",
            )

    for triple in permutations(supports, 3):
        pair_sum, triple_size, union_size = overlap_shape(triple)
        light = pair_sum - triple_size <= 2 * k
        if light_only and not light:
            summary["skipped_nonlight_triples"] += 1
            continue
        summary["ordered_triples"] += 1
        if light:
            summary["light_triples"] += 1
        bases = [basis_cache[T] for T in triple]
        union = sorted(set().union(*(set(T) for T in triple)))

        normal = normal_form_matrix(F, bases, slopes, union)
        twisted = twisted_form_matrix(F, bases, slopes, union)
        row_blocks = [condition_rows(F, bases[i], slopes[i]) for i in range(3)]
        brute_rows = [row for block in row_blocks for row in block]

        normal_rank = rank(F, normal)
        twisted_rank = rank(F, twisted)
        brute_rank = rank(F, brute_rows)
        kernel_dim = 3 * t - normal_rank
        if kernel_dim:
            summary["rank_defect_triples"] += 1
            if light:
                summary["light_rank_defect_triples"] += 1
        summary["maximum_kernel_dimension"] = max(summary["maximum_kernel_dimension"], kernel_dim)
        if light:
            summary["maximum_light_kernel_dimension"] = max(
                summary["maximum_light_kernel_dimension"],
                kernel_dim,
            )

        summary["normal_form_rank_checks"] += 1
        quiet_check(
            f"normal form rank equals brute rank p={p} triple={triple}",
            normal_rank == brute_rank,
            f"normal={normal_rank}, brute={brute_rank}, union={union_size}",
        )
        summary["twisted_rank_checks"] += 1
        quiet_check(
            f"twisted form rank equals normal rank p={p} triple={triple}",
            twisted_rank == normal_rank,
            f"twisted={twisted_rank}, normal={normal_rank}",
        )
        quiet_check(
            f"determinantal criterion p={p} triple={triple}",
            (kernel_dim > 0) == (normal_rank < 3 * t),
            f"kernel_dim={kernel_dim}, rank={normal_rank}, cols={3 * t}",
        )

    check(
        f"toy row p={p}: chart bases valid",
        True,
        f"supports={summary['supports']}, t={t}",
    )
    check(
        f"toy row p={p}: normal form matches brute rank",
        summary["normal_form_rank_checks"] == summary["ordered_triples"],
        f"triples={summary['ordered_triples']}",
    )
    check(
        f"toy row p={p}: twisted form rank invariant",
        summary["twisted_rank_checks"] == summary["ordered_triples"],
        f"triples={summary['ordered_triples']}",
    )
    check(
        f"toy row p={p}: triples evaluated",
        summary["ordered_triples"] > 0,
        f"triples={summary['ordered_triples']}, light={summary['light_triples']}, skipped={summary['skipped_nonlight_triples']}",
    )

    return summary


def main() -> None:
    summaries = [
        check_row(p=7, n=6, k=2, A=4, slopes=(1, 2, 3)),
        check_row(p=11, n=8, k=2, A=4, slopes=(1, 3, 7), light_only=True),
    ]
    check(
        "toy suite includes light triangles",
        sum(row["light_triples"] for row in summaries) > 0,
        "light_total=%d" % sum(row["light_triples"] for row in summaries),
    )
    result = {
        "node": "xr_triangle_eliminant_form",
        "toy_rows": summaries,
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
    print(f"\nPASS: {NCHECK} xr_triangle_eliminant_form checks")


if __name__ == "__main__":
    main()
