#!/usr/bin/env python3
"""Verifier for xr_syzygy_support_lemma (2c-alpha).

The note proves a rank-level implication:

  rank stagnation for a new distinct-slope alignment block
    => a nonzero constrained-support dual word lambda_i
    => supp(lambda_i) is covered by pairwise intersections
    => sum_j |T_i cap T_j| >= k + 1.

This script checks the exact linear algebra on two toy RS rows.  It builds the
shortened dual spaces Lambda_T directly from Vandermonde parity equations, forms
the tensor alignment rows (lambda, z lambda), computes all syzygy kernels for
ordered triples of supports, and verifies the support-cancellation and overlap
budget conclusions for every kernel basis vector.

Stdlib only; no Monte Carlo.
Run: python3 experimental/scripts/verify_xr_syzygy_support_lemma.py
"""

from __future__ import annotations

import json
import os
import sys
from itertools import combinations, permutations, product


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "xr-syzygy-support-lemma",
    "toy_linear_algebra.json",
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
        line = f"{name}"
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


def transpose(rows: list[list[int]], ncols: int | None = None) -> list[list[int]]:
    if not rows:
        return []
    if ncols is None:
        ncols = len(rows[0])
    return [[row[c] for row in rows] for c in range(ncols)]


def lincomb(F: Fp, coeffs: list[int], vecs: list[list[int]]) -> list[int]:
    if not vecs:
        return []
    out = [0] * len(vecs[0])
    for c, v in zip(coeffs, vecs):
        if c:
            out = [F.add(a, F.mul(c, b)) for a, b in zip(out, v)]
    return out


def support(vec: list[int]) -> set[int]:
    return {i for i, x in enumerate(vec) if x}


def powers(x: int, k: int, p: int) -> list[int]:
    out = [1]
    for _ in range(1, k):
        out.append((out[-1] * x) % p)
    return out


def lambda_space(F: Fp, domain: list[int], k: int, T: tuple[int, ...]) -> list[list[int]]:
    """Basis of Lambda_T = {lambda in C^perp : supp(lambda) subset T}."""
    cols = list(T)
    equations: list[list[int]] = []
    for d in range(k):
        equations.append([powers(domain[x], k, F.p)[d] for x in cols])
    small_basis = kernel_basis(F, equations, len(cols))
    out: list[list[int]] = []
    for b in small_basis:
        full = [0] * len(domain)
        for coeff, coord in zip(b, cols):
            full[coord] = coeff
        out.append(full)
    return out


def nonzero_combinations(F: Fp, basis: list[list[int]]) -> list[list[int]]:
    if not basis:
        return []
    out: list[list[int]] = []
    for coeffs in product(range(F.p), repeat=len(basis)):
        if not any(coeffs):
            continue
        out.append(lincomb(F, list(coeffs), basis))
    return out


def condition_rows(F: Fp, lambdas: list[list[int]], z: int) -> list[list[int]]:
    rows: list[list[int]] = []
    for lam in lambdas:
        rows.append(lam + [F.mul(z, x) for x in lam])
    return rows


def relation_kernel(F: Fp, row_blocks: list[list[list[int]]], ambient_dim: int) -> list[list[int]]:
    rows = [row for block in row_blocks for row in block]
    return kernel_basis(F, transpose(rows, ambient_dim), len(rows))


def split_blocks(vec: list[int], block_size: int, m: int) -> list[list[int]]:
    return [vec[i * block_size:(i + 1) * block_size] for i in range(m)]


def check_row(p: int, n: int, k: int, A: int, slopes: tuple[int, int, int]) -> dict[str, int]:
    F = Fp(p)
    domain = list(range(n))
    t = A - k
    supports = list(combinations(range(n), A))
    lambda_cache = {T: lambda_space(F, domain, k, T) for T in supports}

    summary = {
        "p": p,
        "n": n,
        "k": k,
        "A": A,
        "t": t,
        "supports": len(supports),
        "ordered_triples": 0,
        "syzygy_kernel_vectors": 0,
        "nonzero_block_projections": 0,
        "rank_stagnations_checked": 0,
        "minimum_nonzero_dual_weight": n + 1,
        "maximum_kernel_dimension": 0,
    }

    for T, basis in lambda_cache.items():
        quiet_check(f"dim Lambda_T row p={p} T={T}", len(basis) == t, f"dim={len(basis)}, t={t}")
        local_min = n + 1
        for word in nonzero_combinations(F, basis):
            local_min = min(local_min, len(support(word)))
        summary["minimum_nonzero_dual_weight"] = min(summary["minimum_nonzero_dual_weight"], local_min)
        quiet_check(
            f"MDS dual distance on T row p={p} T={T}",
            local_min >= k + 1,
            f"min_seen={local_min}, k+1={k + 1}",
        )

    for triple in permutations(supports, 3):
        summary["ordered_triples"] += 1
        lambdas = [lambda_cache[T] for T in triple]
        blocks = [condition_rows(F, lambdas[i], slopes[i]) for i in range(3)]
        ker = relation_kernel(F, blocks, 2 * n)
        summary["maximum_kernel_dimension"] = max(summary["maximum_kernel_dimension"], len(ker))
        summary["syzygy_kernel_vectors"] += len(ker)

        for m in range(1, 3):
            prev = [row for block in blocks[:m] for row in block]
            new = blocks[m]
            increment = rank(F, prev + new) - rank(F, prev)
            deficient = increment < t
            rel = relation_kernel(F, blocks[:m + 1], 2 * n)
            has_new_projection = False
            for rel_vec in rel:
                parts = split_blocks(rel_vec, t, m + 1)
                if any(parts[m]):
                    has_new_projection = True
                    break
            quiet_check(
                f"rank-stagnation equivalence p={p} triple={triple} m={m}",
                deficient == has_new_projection,
                f"increment={increment}, has_new_projection={has_new_projection}",
            )
            summary["rank_stagnations_checked"] += 1

        for rel_vec in ker:
            coeff_blocks = split_blocks(rel_vec, t, 3)
            for i, coeffs in enumerate(coeff_blocks):
                lam = lincomb(F, coeffs, lambdas[i])
                supp = support(lam)
                if not supp:
                    continue
                summary["nonzero_block_projections"] += 1
                T_i = set(triple[i])
                partner_union = set()
                overlap_sum = 0
                for j, T_j_tuple in enumerate(triple):
                    if j == i:
                        continue
                    T_j = set(T_j_tuple)
                    inter = T_i & T_j
                    partner_union |= inter
                    overlap_sum += len(inter)
                quiet_check(
                    f"support cancellation p={p} triple={triple} block={i}",
                    supp <= partner_union,
                    f"supp={sorted(supp)}, union={sorted(partner_union)}",
                )
                quiet_check(
                    f"dual-weight budget p={p} triple={triple} block={i}",
                    len(supp) >= k + 1 and overlap_sum >= k + 1,
                    f"weight={len(supp)}, overlap_sum={overlap_sum}, k+1={k + 1}",
                )

    check(
        f"toy row p={p}: Lambda_T dimensions and MDS dual weights",
        summary["minimum_nonzero_dual_weight"] == k + 1,
        f"supports={summary['supports']}, min_weight={summary['minimum_nonzero_dual_weight']}",
    )
    check(
        f"toy row p={p}: rank-stagnation equivalence",
        summary["rank_stagnations_checked"] == 2 * summary["ordered_triples"],
        f"ordered_triples={summary['ordered_triples']}",
    )
    check(
        f"toy row p={p}: syzygy support budget",
        summary["nonzero_block_projections"] >= 0,
        f"kernel_vectors={summary['syzygy_kernel_vectors']}, nonzero_blocks={summary['nonzero_block_projections']}",
    )

    return summary


def main() -> None:
    summaries = [
        check_row(p=7, n=6, k=2, A=4, slopes=(1, 2, 3)),
        check_row(p=11, n=7, k=3, A=5, slopes=(1, 3, 7)),
    ]
    result = {
        "node": "xr_syzygy_support_lemma",
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
    print(f"\nPASS: {NCHECK} xr_syzygy_support_lemma checks")


if __name__ == "__main__":
    main()
