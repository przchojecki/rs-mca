#!/usr/bin/env python3
"""Exact finite-field regression for the literal rooted high-load precursor extraction rank precursor.

The script reconstructs the exact-agreement control used by the uploaded
the finite owner-rooting and projected-energy reductions packet.  For every retained support S and actual owner z it finds
the degree-<k explaining polynomial h and verifies that

    B_S = [1, t, ..., t^(k-1), U_z(t)]_{t in S}

has rank k, while the first k columns have a nonzero Vandermonde minor and an
ambient-generic final column would give rank k+1.

This certifies the *literal* rank alternative.  It deliberately does not claim
that the rank loss is beyond the ordinary witness-interpolation baseline.
"""

from __future__ import annotations

import argparse
import itertools
from dataclasses import dataclass


def eval_poly(coefficients: tuple[int, ...], x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * x + coefficient) % p
    return value


def inv_mod(x: int, p: int) -> int:
    if x % p == 0:
        raise ZeroDivisionError
    return pow(x % p, p - 2, p)


def rank_mod(matrix: list[list[int]], p: int) -> int:
    if not matrix:
        return 0
    a = [[entry % p for entry in row] for row in matrix]
    rows = len(a)
    cols = len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col] % p), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = inv_mod(a[rank][col], p)
        a[rank] = [(scale * x) % p for x in a[rank]]
        for r in range(rows):
            if r == rank or a[r][col] == 0:
                continue
            factor = a[r][col]
            a[r] = [(x - factor * y) % p for x, y in zip(a[r], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def determinant_mod(matrix: list[list[int]], p: int) -> int:
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("determinant requires a square matrix")
    a = [[entry % p for entry in row] for row in matrix]
    det = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        pivot_value = a[col][col]
        det = det * pivot_value % p
        scale = inv_mod(pivot_value, p)
        for r in range(col + 1, n):
            factor = a[r][col] * scale % p
            for c in range(col, n):
                a[r][c] = (a[r][c] - factor * a[col][c]) % p
    return det % p


def line_values(
    p: int, domain: list[int], roots: list[int], amplitude_shift: int = 0
) -> tuple[list[int], list[int]]:
    anchor_polynomial = (3, 2)
    direction_polynomial = (5, 1)
    amplitudes = [
        ((index + 1) ** 2 + 3 * (index + 1) + amplitude_shift) % p or 1
        for index in range(len(domain))
    ]
    anchor: list[int] = []
    direction: list[int] = []
    for index, x in enumerate(domain):
        anchor.append(
            (eval_poly(anchor_polynomial, x, p) - amplitudes[index] * roots[index]) % p
        )
        direction.append(
            (eval_poly(direction_polynomial, x, p) + amplitudes[index]) % p
        )
    return anchor, direction


@dataclass(frozen=True)
class Witness:
    support: tuple[int, ...]
    owner: int
    polynomial: tuple[int, ...]


def exact_witnesses(
    p: int,
    domain: list[int],
    k: int,
    agreement: int,
    anchor: list[int],
    direction: list[int],
) -> list[Witness]:
    rows: list[Witness] = []
    for owner in range(p):
        received = [
            (anchor[index] + owner * direction[index]) % p
            for index in range(len(domain))
        ]
        for polynomial in itertools.product(range(p), repeat=k):
            complete = tuple(
                index
                for index, x in enumerate(domain)
                if eval_poly(polynomial, x, p) == received[index]
            )
            if len(complete) == agreement:
                rows.append(Witness(complete, owner, tuple(polynomial)))
    return rows


def rim_free_greedy(witnesses: list[Witness], agreement: int) -> list[Witness]:
    # First retain one exact owner/polynomial record per support.  The uploaded
    # control has unique noncommon owners on the retained family.
    by_support: dict[tuple[int, ...], Witness] = {}
    for row in witnesses:
        by_support.setdefault(row.support, row)

    retained: list[Witness] = []
    used_rims: set[tuple[int, ...]] = set()
    for support in sorted(by_support):
        rims = set(itertools.combinations(support, agreement - 1))
        if rims & used_rims:
            continue
        retained.append(by_support[support])
        used_rims |= rims
    return retained


def block_for(
    witness: Witness,
    p: int,
    domain: list[int],
    k: int,
    anchor: list[int],
    direction: list[int],
) -> list[list[int]]:
    matrix: list[list[int]] = []
    for index in witness.support:
        t = domain[index]
        received = (anchor[index] + witness.owner * direction[index]) % p
        matrix.append([pow(t, j, p) for j in range(k)] + [received])
    return matrix


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run the regression")
    parser.parse_args()

    p = 17
    domain = list(range(1, 9))
    roots = [0, 0, 0, 0, 1, 1, 1, 1]
    k = 2
    agreement = 4
    anchor, direction = line_values(p, domain, roots, amplitude_shift=0)

    witnesses = exact_witnesses(p, domain, k, agreement, anchor, direction)
    retained = rim_free_greedy(witnesses, agreement)
    if not retained:
        raise AssertionError("expected a nonempty retained family")

    total_actual_rank = 0
    total_generic_rank = 0
    for witness in retained:
        matrix = block_for(witness, p, domain, k, anchor, direction)
        actual_rank = rank_mod(matrix, p)
        vandermonde_minor = [row[:k] for row in matrix[:k]]
        det = determinant_mod(vandermonde_minor, p)

        # Verify the last column equals evaluation of the printed witness
        # polynomial on every retained row.
        for row_index, support_index in enumerate(witness.support):
            t = domain[support_index]
            expected = eval_poly(witness.polynomial, t, p)
            if matrix[row_index][-1] != expected:
                raise AssertionError((witness, t, matrix[row_index][-1], expected))

        if det == 0:
            raise AssertionError("Vandermonde minor unexpectedly vanished")
        if actual_rank != k:
            raise AssertionError((witness, actual_rank, k))
        if agreement < k + 1:
            raise AssertionError("generic rank k+1 requires agreement >= k+1")

        total_actual_rank += actual_rank
        total_generic_rank += k + 1

    deficiency = total_generic_rank - total_actual_rank
    if deficiency != len(retained):
        raise AssertionError((deficiency, len(retained)))

    print("PASS")
    print(f"field=F_{p} domain_size={len(domain)} k={k} agreement={agreement}")
    print(f"retained_blocks={len(retained)}")
    print(f"actual_block_sum_rank={total_actual_rank}")
    print(f"ambient_generic_block_sum_rank={total_generic_rank}")
    print(f"printed_rank_deficiency={deficiency}")
    for witness in retained:
        print(
            "support=" + str(witness.support)
            + " owner=" + str(witness.owner)
            + " polynomial=" + str(witness.polynomial)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
