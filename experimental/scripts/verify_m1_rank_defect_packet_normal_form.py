#!/usr/bin/env python3
"""Verify the M1 rank-defect packet normal-form identities.

This checks only the local linear algebra in
experimental/notes/m1/m1_rank_defect_packet_normal_form.md.  It does not scan
MCA bad slopes and does not prove the global M1 local limit.
"""

from __future__ import annotations

from itertools import product
from math import comb
from random import Random


PRIMES = (3, 5, 7, 11)
TRIALS_PER_PRIME = 80


def add(u: tuple[int, ...], v: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a + b) % p for a, b in zip(u, v))


def sub(u: tuple[int, ...], v: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a - b) % p for a, b in zip(u, v))


def scale(a: int, v: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a * b) % p for b in v)


def dot(u: tuple[int, ...], v: tuple[int, ...], p: int) -> int:
    return sum(a * b for a, b in zip(u, v)) % p


def matrix_rank(rows: list[tuple[int, ...]], p: int) -> int:
    if not rows:
        return 0
    matrix = [list(row) for row in rows if any(entry % p for entry in row)]
    if not matrix:
        return 0
    width = len(matrix[0])
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
        rank += 1
        if rank == len(matrix):
            break
    return rank


def rref(
    rows: list[tuple[int, ...]], width: int, p: int
) -> tuple[list[list[int]], list[int]]:
    matrix = [
        [entry % p for entry in row]
        for row in rows
        if any(entry % p for entry in row)
    ]
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


def nullspace_basis(rows: list[tuple[int, ...]], width: int, p: int) -> list[tuple[int, ...]]:
    reduced, pivots = rref(rows, width, p)
    pivot_set = set(pivots)
    free_cols = [col for col in range(width) if col not in pivot_set]
    basis: list[tuple[int, ...]] = []
    for free in free_cols:
        vec = [0] * width
        vec[free] = 1
        for row, pivot_col in zip(reduced, pivots):
            vec[pivot_col] = (-row[free]) % p
        basis.append(tuple(vec))
    return basis


def random_combo(
    basis: list[tuple[int, ...]], width: int, rng: Random, p: int
) -> tuple[int, ...]:
    out = (0,) * width
    for vector in basis:
        coeff = rng.randrange(p)
        out = add(out, scale(coeff, vector, p), p)
    return out


def independent_vectors(width: int, rank: int, rng: Random, p: int) -> list[tuple[int, ...]]:
    vectors: list[tuple[int, ...]] = []
    while len(vectors) < rank:
        candidate = tuple(rng.randrange(p) for _ in range(width))
        if matrix_rank(vectors + [candidate], p) == len(vectors) + 1:
            vectors.append(candidate)
    return vectors


def affine_point(
    base: tuple[int, ...], basis: list[tuple[int, ...]], params: tuple[int, ...], p: int
) -> tuple[int, ...]:
    point = base
    for coeff, vector in zip(params, basis):
        point = add(point, scale(coeff, vector, p), p)
    return point


def affine_rank(points: list[tuple[int, ...]], p: int) -> int:
    if not points:
        return -1
    base = points[0]
    return matrix_rank([sub(point, base, p) for point in points[1:]], p)


def in_span(vector: tuple[int, ...], basis: list[tuple[int, ...]], p: int) -> bool:
    return matrix_rank(basis + [vector], p) == matrix_rank(basis, p)


def in_affine(
    point: tuple[int, ...], base: tuple[int, ...], basis: list[tuple[int, ...]], p: int
) -> bool:
    return in_span(sub(point, base, p), basis, p)


def landing(c: tuple[int, ...], coeff_vector: tuple[int, ...], p: int) -> int:
    h = len(c)
    return (coeff_vector[h] + sum(c[m] * coeff_vector[m] for m in range(h))) % p


def hankel_apply(
    sequence: list[int], rows: int, poly: tuple[int, ...], p: int
) -> tuple[int, ...]:
    return tuple(
        sum(sequence[row + col] * coeff for col, coeff in enumerate(poly)) % p
        for row in range(rows)
    )


def shifted_core(core: tuple[int, ...], shift: int, total_shift: int) -> tuple[int, ...]:
    return (0,) * shift + core + (0,) * (total_shift - shift)


def core_coeff(core: tuple[int, ...], idx: int) -> int:
    if 0 <= idx < len(core):
        return core[idx]
    return 0


def moving_coeffs(
    h: int, moving_rank: int, core: tuple[int, ...], params: tuple[int, ...], p: int
) -> tuple[int, ...]:
    return tuple(
        (
            core_coeff(core, m - moving_rank)
            + sum(params[i] * core_coeff(core, m - i) for i in range(moving_rank))
        )
        % p
        for m in range(h)
    )


def moving_directions(
    h: int, moving_rank: int, core: tuple[int, ...]
) -> list[tuple[int, ...]]:
    return [
        tuple(core_coeff(core, m - i) for m in range(h))
        for i in range(moving_rank)
    ]


def check_affine_span_normal_form(p: int, rng: Random) -> int:
    checked = 0
    for _ in range(TRIALS_PER_PRIME):
        h = rng.randrange(1, 7)
        rank = rng.randrange(0, h + 1)
        base = tuple(rng.randrange(p) for _ in range(h))
        basis = independent_vectors(h, rank, rng, p)
        spanning_points = [base] + [add(base, vector, p) for vector in basis]
        constraints = [point + (1,) for point in spanning_points]
        null_basis = nullspace_basis(constraints, h + 1, p)
        coeff_vector = random_combo(null_basis, h + 1, rng, p)

        assert landing(base, coeff_vector, p) == 0
        for vector in basis:
            assert sum(vector[m] * coeff_vector[m] for m in range(h)) % p == 0
            assert landing(add(base, vector, p), coeff_vector, p) == 0

        sample_count = min(p**rank, 250)
        if p**rank <= sample_count:
            params_iter = product(range(p), repeat=rank)
        else:
            params_iter = (
                tuple(rng.randrange(p) for _ in range(rank)) for _ in range(sample_count)
            )
        for params in params_iter:
            point = affine_point(base, basis, params, p)
            assert landing(point, coeff_vector, p) == 0

        random_coeff_vector = tuple(rng.randrange(p) for _ in range(h + 1))
        theta = tuple(rng.randrange(p) for _ in range(rank))
        point = affine_point(base, basis, theta, p)
        direct = landing(point, random_coeff_vector, p)
        expanded = landing(base, random_coeff_vector, p)
        for coeff, vector in zip(theta, basis):
            expanded += coeff * sum(vector[m] * random_coeff_vector[m] for m in range(h))
        assert direct == expanded % p
        checked += 1
    return checked


def check_full_rank_lift(p: int, rng: Random) -> int:
    checked = 0
    for _ in range(TRIALS_PER_PRIME):
        h = rng.randrange(1, 6)
        base = tuple(rng.randrange(p) for _ in range(h))
        basis = independent_vectors(h, h, rng, p)
        points = [base] + [add(base, vector, p) for vector in basis]
        constraints = [point + (1,) for point in points]
        assert matrix_rank(constraints, p) == h + 1
        assert nullspace_basis(constraints, h + 1, p) == []

        t = rng.randrange(1, 6)
        core_len = rng.randrange(1, 6)
        core = tuple(rng.randrange(p) for _ in range(core_len))
        sequence = [rng.randrange(p) for _ in range(t + h + core_len + 2)]
        lifted = hankel_apply(sequence, t + h, core, p)
        for shift in range(h + 1):
            wide_poly = shifted_core(core, shift, h)
            wide_rows = hankel_apply(sequence, t, wide_poly, p)
            assert wide_rows == lifted[shift : shift + t]
        checked += 1
    return checked


def fixed_root_alpha(
    coeffs: tuple[int, ...], constant: int, p: int
) -> int | None:
    h = len(coeffs)
    for alpha in range(p):
        powers = tuple(pow(alpha, m, p) for m in range(h))
        for lam in range(1, p):
            if coeffs == tuple((lam * power) % p for power in powers) and constant == (
                lam * pow(alpha, h, p)
            ) % p:
                return alpha
    return None


def check_fixed_root_hyperplanes(p: int, rng: Random) -> int:
    checked = 0
    for h in range(1, 5):
        all_coeff_points = list(product(range(p), repeat=h))
        for alpha in range(p):
            lam = rng.randrange(1, p)
            coeffs = tuple((lam * pow(alpha, m, p)) % p for m in range(h))
            constant = (lam * pow(alpha, h, p)) % p
            hyperplane = {
                c
                for c in all_coeff_points
                if (constant + sum(coeffs[m] * c[m] for m in range(h))) % p == 0
            }
            fixed_root = {
                c
                for c in all_coeff_points
                if (pow(alpha, h, p) + sum(pow(alpha, m, p) * c[m] for m in range(h)))
                % p
                == 0
            }
            assert hyperplane == fixed_root
            assert fixed_root_alpha(coeffs, constant, p) == alpha
            checked += 1

        for _ in range(12):
            coeffs = tuple(rng.randrange(p) for _ in range(h))
            if all(value == 0 for value in coeffs):
                coeffs = (1,) + (0,) * (h - 1)
            constant = rng.randrange(p)
            alpha = fixed_root_alpha(coeffs, constant, p)
            if alpha is None:
                hyperplane = {
                    c
                    for c in all_coeff_points
                    if (constant + sum(coeffs[m] * c[m] for m in range(h))) % p == 0
                }
                for beta in range(p):
                    fixed_root = {
                        c
                        for c in all_coeff_points
                        if (
                            pow(beta, h, p)
                            + sum(pow(beta, m, p) * c[m] for m in range(h))
                        )
                        % p
                        == 0
                    }
                    assert hyperplane != fixed_root
            checked += 1
    return checked


def check_moving_fiber_dimension_drop(p: int, rng: Random) -> int:
    checked = 0
    for _ in range(TRIALS_PER_PRIME):
        h = rng.randrange(1, 6)
        moving_rank = rng.randrange(1, min(4, h) + 1)
        core_degree = h - moving_rank
        core = tuple(rng.randrange(p) for _ in range(core_degree)) + (1,)

        directions = moving_directions(h, moving_rank, core)
        assert matrix_rank(directions, p) == moving_rank

        packet_rank = rng.randrange(0, h)
        packet_base = tuple(rng.randrange(p) for _ in range(h))
        packet_basis = independent_vectors(h, packet_rank, rng, p)

        all_parameters = list(product(range(p), repeat=moving_rank))
        passing = [
            params
            for params in all_parameters
            if in_affine(
                moving_coeffs(h, moving_rank, core, params, p),
                packet_base,
                packet_basis,
                p,
            )
        ]
        rank = affine_rank(passing, p)
        if rank == moving_rank:
            for direction in directions:
                assert in_span(direction, packet_basis, p)
            assert len(passing) == p**moving_rank
            assert set(passing) == set(all_parameters)
        else:
            assert rank <= moving_rank - 1
            assert len(passing) <= p ** (moving_rank - 1)

        residual_degree_bound = comb(h, moving_rank) * (p ** (moving_rank - 1) - 1)
        if moving_rank == 1:
            assert residual_degree_bound == 0
        else:
            assert residual_degree_bound >= 0
        checked += 1
    return checked


def main() -> None:
    rng = Random(20260630)
    span_checks = 0
    lift_checks = 0
    hyperplane_checks = 0
    fiber_checks = 0

    for p in PRIMES:
        span_checks += check_affine_span_normal_form(p, rng)
        lift_checks += check_full_rank_lift(p, rng)
        hyperplane_checks += check_fixed_root_hyperplanes(p, rng)
        fiber_checks += check_moving_fiber_dimension_drop(p, rng)

    print("M1 rank-defect packet normal-form verifier passed")
    print(f"  primes: {PRIMES}")
    print(f"  affine-span checks: {span_checks}")
    print(f"  full-rank/Hankel-lift checks: {lift_checks}")
    print(f"  fixed-root hyperplane checks: {hyperplane_checks}")
    print(f"  moving-fiber count checks: {fiber_checks}")


if __name__ == "__main__":
    main()
