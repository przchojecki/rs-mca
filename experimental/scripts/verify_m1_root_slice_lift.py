#!/usr/bin/env python3
"""Verify the M1 root-slice lift identities.

This is a small checker for experimental/notes/m1/m1_root_slice_lift.md.  It
does not enumerate MCA bad slopes and does not prove the full M1 local limit.
It checks the linear identities used by the note:

  * (X-y)r - (X-x)r = (x-y)r;
  * if a linear row kills two distinct one-root extensions, then it kills the
    core r and Xr;
  * the padded H_{t,j} equations on (r,0) and (0,r) are exactly the rows of
    H_{t+1,j-1}r.
"""

from __future__ import annotations

from random import Random


PRIMES = (5, 7, 11, 17, 29, 43, 97)
TRIALS_PER_PRIME = 250


def add(u: list[int], v: list[int], p: int) -> list[int]:
    return [(a + b) % p for a, b in zip(u, v)]


def sub(u: list[int], v: list[int], p: int) -> list[int]:
    return [(a - b) % p for a, b in zip(u, v)]


def scale(a: int, v: list[int], p: int) -> list[int]:
    return [(a * b) % p for b in v]


def dot(u: list[int], v: list[int], p: int) -> int:
    return sum(a * b for a, b in zip(u, v)) % p


def x_times(poly: list[int]) -> list[int]:
    return [0] + poly


def pad_top(poly: list[int]) -> list[int]:
    return poly + [0]


def mul_x_minus_a(poly: list[int], a: int, p: int) -> list[int]:
    return sub(x_times(poly), scale(a, pad_top(poly), p), p)


def rref(rows: list[list[int]], p: int) -> tuple[list[list[int]], list[int]]:
    matrix = [[entry % p for entry in row] for row in rows if any(x % p for x in row)]
    if not matrix:
        return [], []

    width = len(matrix[0])
    pivot_cols: list[int] = []
    rank = 0
    for col in range(width):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % p:
                pivot = row_idx
                break
        if pivot is None:
            continue

        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, p)
        matrix[rank] = [(entry * inv) % p for entry in matrix[rank]]

        for row_idx in range(len(matrix)):
            if row_idx == rank:
                continue
            factor = matrix[row_idx][col] % p
            if factor:
                matrix[row_idx] = [
                    (entry - factor * pivot_entry) % p
                    for entry, pivot_entry in zip(matrix[row_idx], matrix[rank])
                ]

        pivot_cols.append(col)
        rank += 1
        if rank == len(matrix):
            break

    return matrix[:rank], pivot_cols


def nullspace_basis(constraints: list[list[int]], p: int) -> list[list[int]]:
    """Return a basis for row vectors killing every constraint by dot product."""

    reduced, pivots = rref(constraints, p)
    if not constraints:
        return []
    width = len(constraints[0])
    pivot_set = set(pivots)
    free_cols = [col for col in range(width) if col not in pivot_set]
    basis: list[list[int]] = []

    for free in free_cols:
        vec = [0] * width
        vec[free] = 1
        for row, pivot_col in zip(reduced, pivots):
            vec[pivot_col] = (-row[free]) % p
        basis.append(vec)

    if not basis:
        basis.append([0] * width)
    return basis


def random_combo(basis: list[list[int]], rng: Random, p: int) -> list[int]:
    width = len(basis[0])
    out = [0] * width
    for vector in basis:
        coeff = rng.randrange(p)
        out = add(out, scale(coeff, vector, p), p)
    return out


def hankel_apply(sequence: list[int], rows: int, poly: list[int], p: int) -> list[int]:
    return [
        sum(sequence[row + col] * coeff for col, coeff in enumerate(poly)) % p
        for row in range(rows)
    ]


def check_root_slice_identities(p: int, rng: Random) -> tuple[int, int]:
    implication_hits = 0
    nonzero_row_hits = 0

    for _ in range(TRIALS_PER_PRIME):
        degree = rng.randrange(0, 9)
        core = [rng.randrange(p) for _ in range(degree + 1)]
        if all(coeff == 0 for coeff in core):
            core[rng.randrange(len(core))] = 1

        x = rng.randrange(p)
        y = rng.randrange(p)
        while y == x:
            y = rng.randrange(p)

        core_pad = pad_top(core)
        x_core = x_times(core)
        loc_x = mul_x_minus_a(core, x, p)
        loc_y = mul_x_minus_a(core, y, p)

        assert sub(loc_y, loc_x, p) == scale((x - y) % p, core_pad, p)
        assert loc_x == sub(x_core, scale(x, core_pad, p), p)
        assert loc_y == sub(x_core, scale(y, core_pad, p), p)

        random_row = [rng.randrange(p) for _ in range(len(loc_x))]
        assert (dot(random_row, loc_y, p) - dot(random_row, loc_x, p)) % p == (
            (x - y) * dot(random_row, core_pad, p)
        ) % p
        assert dot(random_row, loc_x, p) == (
            dot(random_row, x_core, p) - x * dot(random_row, core_pad, p)
        ) % p

        basis = nullspace_basis([loc_x, loc_y], p)
        row = random_combo(basis, rng, p)
        assert dot(row, loc_x, p) == 0
        assert dot(row, loc_y, p) == 0
        assert dot(row, core_pad, p) == 0
        assert dot(row, x_core, p) == 0

        for a in range(p):
            loc_a = mul_x_minus_a(core, a, p)
            assert dot(row, loc_a, p) == 0

        implication_hits += 1
        if any(entry % p for entry in row):
            nonzero_row_hits += 1

    return implication_hits, nonzero_row_hits


def check_hankel_lift_identities(p: int, rng: Random) -> int:
    checked = 0

    for _ in range(TRIALS_PER_PRIME):
        t = rng.randrange(1, 8)
        j = rng.randrange(1, 9)
        core = [rng.randrange(p) for _ in range(j)]
        sequence = [rng.randrange(p) for _ in range(t + j + 2)]

        core_pad = pad_top(core)
        x_core = x_times(core)

        wide_core_rows = hankel_apply(sequence, t, core_pad, p)
        wide_x_rows = hankel_apply(sequence, t, x_core, p)
        lifted_rows = hankel_apply(sequence, t + 1, core, p)

        assert wide_core_rows == lifted_rows[:t]
        assert wide_x_rows == lifted_rows[1 : t + 1]

        if all(value == 0 for value in wide_core_rows) and all(
            value == 0 for value in wide_x_rows
        ):
            assert all(value == 0 for value in lifted_rows)
        if all(value == 0 for value in lifted_rows):
            assert all(value == 0 for value in wide_core_rows)
            assert all(value == 0 for value in wide_x_rows)

        checked += 1

    return checked


def main() -> None:
    rng = Random(20260630)
    total_implications = 0
    total_nonzero_rows = 0
    total_lifts = 0

    for p in PRIMES:
        implications, nonzero_rows = check_root_slice_identities(p, rng)
        lifts = check_hankel_lift_identities(p, rng)
        total_implications += implications
        total_nonzero_rows += nonzero_rows
        total_lifts += lifts

    print("M1 root-slice lift verifier passed")
    print(f"  primes: {PRIMES}")
    print(f"  one-exchange implication checks: {total_implications}")
    print(f"  nonzero killing-row samples: {total_nonzero_rows}")
    print(f"  Hankel lift row checks: {total_lifts}")


if __name__ == "__main__":
    main()
