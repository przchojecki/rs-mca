#!/usr/bin/env python3
"""Verifier for xr_sunflower_rank_additive (2c-beta-1).

The proof says that a distinct-slope sunflower of agreement supports has no
nontrivial tensor-row syzygy: cancellation on petals forces every constrained
dual word into the common core, and the MDS dual distance then forces it to be
zero.  Therefore m sunflower blocks have stacked rank m*t, hence m <= 2n/t.

This script checks the exact finite-field linear algebra on two packed toy
rows by enumerating every ordered sunflower triple with the chosen core size.

Stdlib only; no Monte Carlo.
Run: python3 experimental/scripts/verify_xr_sunflower_rank_additive.py
"""

from __future__ import annotations

import json
import os
import sys
from itertools import combinations, product


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "xr-sunflower-rank-additive",
    "toy_sunflower_rank.json",
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


def kernel_basis(F: Fp, rows: list[list[int]], ncols: int | None = None) -> list[list[int]]:
    if ncols is None:
        ncols = len(rows[0]) if rows else 0
    if not rows:
        return [[1 if i == j else 0 for i in range(ncols)] for j in range(ncols)]
    R, pivots, _ = rref(F, rows)
    free = [c for c in range(ncols) if c not in pivots]
    basis: list[list[int]] = []
    for fc in free:
        vec = [0] * ncols
        vec[fc] = 1
        for i, pc in enumerate(pivots):
            vec[pc] = F.neg(R[i][fc])
        basis.append(vec)
    return basis


def lincomb(F: Fp, coeffs: tuple[int, ...], vecs: list[list[int]]) -> list[int]:
    out = [0] * len(vecs[0])
    for c, v in zip(coeffs, vecs):
        if c:
            out = [F.add(a, F.mul(c, b)) for a, b in zip(out, v)]
    return out


def support(vec: list[int]) -> set[int]:
    return {i for i, x in enumerate(vec) if x}


def lambda_space(F: Fp, domain: list[int], k: int, T: tuple[int, ...]) -> list[list[int]]:
    cols = list(T)
    equations: list[list[int]] = []
    for d in range(k):
        equations.append([pow(domain[x], d, F.p) for x in cols])
    small_basis = kernel_basis(F, equations, len(cols))
    out: list[list[int]] = []
    for b in small_basis:
        full = [0] * len(domain)
        for coeff, coord in zip(b, cols):
            full[coord] = coeff
        out.append(full)
    return out


def nonzero_combinations(F: Fp, basis: list[list[int]]) -> list[list[int]]:
    out: list[list[int]] = []
    for coeffs in product(range(F.p), repeat=len(basis)):
        if not any(coeffs):
            continue
        out.append(lincomb(F, coeffs, basis))
    return out


def condition_rows(F: Fp, lambdas: list[list[int]], z: int) -> list[list[int]]:
    return [lam + [F.mul(z, x) for x in lam] for lam in lambdas]


def sunflower_triples(n: int, A: int, core_size: int):
    petal_size = A - core_size
    points = tuple(range(n))
    for core in combinations(points, core_size):
        rest0 = tuple(x for x in points if x not in core)
        for petal0 in combinations(rest0, petal_size):
            rest1 = tuple(x for x in rest0 if x not in petal0)
            for petal1 in combinations(rest1, petal_size):
                petal2 = tuple(x for x in rest1 if x not in petal1)
                if len(petal2) != petal_size:
                    continue
                yield tuple(tuple(sorted(core + p)) for p in (petal0, petal1, petal2))


def check_row(
    *,
    p: int,
    n: int,
    k: int,
    A: int,
    core_size: int,
    slopes: tuple[int, int, int],
) -> dict[str, int]:
    F = Fp(p)
    domain = list(range(n))
    t = A - k
    supports = list(combinations(range(n), A))
    lambda_cache = {T: lambda_space(F, domain, k, T) for T in supports}
    word_cache: dict[tuple[int, ...], list[list[int]]] = {}
    core_has_word: dict[tuple[tuple[int, ...], tuple[int, ...]], bool] = {}

    summary = {
        "p": p,
        "n": n,
        "k": k,
        "A": A,
        "t": t,
        "core_size": core_size,
        "supports": len(supports),
        "sunflower_triples": 0,
        "rank_checks": 0,
        "core_subsets_checked": 0,
        "minimum_nonzero_dual_weight": n + 1,
        "maximum_rank_defect": 0,
        "maximum_common_core_support_weight": 0,
    }

    for T, basis in lambda_cache.items():
        quiet_check(f"dim Lambda_T p={p} T={T}", len(basis) == t, f"dim={len(basis)}, t={t}")
        words = nonzero_combinations(F, basis)
        word_cache[T] = words
        local_min = n + 1
        for word in words:
            local_min = min(local_min, len(support(word)))
        summary["minimum_nonzero_dual_weight"] = min(summary["minimum_nonzero_dual_weight"], local_min)
        quiet_check(
            f"MDS dual distance p={p} T={T}",
            local_min >= k + 1,
            f"min_seen={local_min}, k+1={k + 1}",
        )

    for T, words in word_cache.items():
        for core_tuple in combinations(T, core_size):
            core = set(core_tuple)
            core_words = [word for word in words if support(word) <= core]
            summary["core_subsets_checked"] += 1
            summary["maximum_common_core_support_weight"] = max(
                summary["maximum_common_core_support_weight"],
                max((len(support(word)) for word in core_words), default=0),
            )
            core_has_word[(T, core_tuple)] = bool(core_words)
            quiet_check(
                f"no nonzero dual word on core p={p} T={T} core={core_tuple}",
                not core_words,
                f"core_size={core_size}, k+1={k + 1}",
            )

    for triple in sunflower_triples(n, A, core_size):
        summary["sunflower_triples"] += 1
        core = set(triple[0])
        for T in triple[1:]:
            core &= set(T)
        quiet_check(
            f"sunflower core size p={p} triple={triple}",
            len(core) == core_size and all((set(a) & set(b)) == core for a in triple for b in triple if a != b),
            f"core={sorted(core)}",
        )

        blocks = [
            condition_rows(F, lambda_cache[triple[i]], slopes[i])
            for i in range(3)
        ]
        stacked = [row for block in blocks for row in block]
        got_rank = rank(F, stacked)
        expected_rank = 3 * t
        summary["rank_checks"] += 1
        summary["maximum_rank_defect"] = max(summary["maximum_rank_defect"], expected_rank - got_rank)
        quiet_check(
            f"full sunflower rank p={p} triple={triple}",
            got_rank == expected_rank,
            f"rank={got_rank}, expected={expected_rank}",
        )

        core_tuple = tuple(sorted(core))
        for T in triple:
            quiet_check(
                f"no nonzero dual word on core p={p} T={T}",
                not core_has_word[(T, core_tuple)],
                f"core_size={core_size}, k+1={k + 1}",
            )

    check(
        f"toy row p={p}: shortened dual spaces",
        summary["minimum_nonzero_dual_weight"] == k + 1,
        f"supports={summary['supports']}, min_weight={summary['minimum_nonzero_dual_weight']}",
    )
    check(
        f"toy row p={p}: all sunflower triples full rank",
        summary["maximum_rank_defect"] == 0,
        f"triples={summary['sunflower_triples']}, rank_checks={summary['rank_checks']}",
    )
    check(
        f"toy row p={p}: common core carries no dual word",
        summary["maximum_common_core_support_weight"] == 0,
        f"core_size={core_size}, k+1={k + 1}",
    )
    check(
        f"toy row p={p}: dimension cap arithmetic",
        3 * t <= 2 * n,
        f"3t={3 * t}, 2n={2 * n}",
    )

    return summary


def main() -> None:
    summaries = [
        check_row(p=11, n=10, k=2, A=4, core_size=1, slopes=(1, 2, 5)),
        check_row(p=13, n=11, k=3, A=5, core_size=2, slopes=(1, 4, 9)),
    ]
    result = {
        "node": "xr_sunflower_rank_additive",
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
    print(f"\nPASS: {NCHECK} xr_sunflower_rank_additive checks")


if __name__ == "__main__":
    main()
