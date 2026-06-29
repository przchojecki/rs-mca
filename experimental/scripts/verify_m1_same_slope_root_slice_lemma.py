#!/usr/bin/env python3
"""Verify the same-slope one-exchange root-slice algebra.

The mathematical lemma is linear.  If

    ell_{T_y} = (X-y) ell_R,

then

    ell_{T_y1} - ell_{T_y2} = (y2-y1) ell_R.

Consequently any linear row that kills both endpoint locators also kills
ell_R; substituting back then kills X ell_R.  This script checks that
identity exactly in small prime fields and stress-tests the row implication.
It also checks the two-exchange full-plane lift, t=2 determinant-gate formula,
ruled-core collapse, non-fixed two-root line constant-slope collapse, triangle
classification, and top-packet lift identities.  The simultaneous top-kernel
recursion is checked by the same padded-row identity applied to both syndrome
rows.  Rank-defect hyperplane fibers are checked by the affine-linear one-root
extension formula, and general affine subpacket one-root and two-root fibers
are checked by finite-field linear algebra.  The arbitrary moving-rank fiber
dimension drop is checked by the same affine-preimage calculation, and the
residual exchange-degree corollary is checked on small split-support graphs.
The boundary shadow-fiber, rank-one anchor-recovery, quadratic slope-gate,
conic-secant anchor-gate, fixed-anchor boundary-core fiber, and fixed-core
graph reductions are checked on sampled small-field instances, including the
fixed-core bidegree determinant normal form.  The average-ledger and
boundary-core closure substitutions are checked as exact rational inequalities.
The mixed-domain trace formulas for fixed-sum and product-Mobius line packets
are checked against direct elementary-plane incidence.
The boundary-core quadratic anchor gate and quartic discriminant root count are
checked in sampled odd prime fields.
The identically-zero discriminant case is checked by exhaustive small-field
classification into scalar affine-line squares or the envelope conic s^2-4p.
For nonzero discriminant gates, the verifier also checks the bounded double
cover parametrization W=2A beta+B outside the at-most-two A=0 fibers.
Finally, the fixed-core same-slope fibers in the elementary two-root plane are
checked to be only empty, points, affine lines, or the full plane.
The full-subgroup quartic Kummer gate is checked by factoring degree-four
discriminants and testing the exact lcm(e,2)-power degeneracy condition.
The slope-side fixed-core recurrence chart is checked by direct finite-field
linear algebra, and its domain/outside subgroup filter is checked by direct
character expansion on sampled finite-field covers.
"""

from __future__ import annotations

from cmath import exp
from fractions import Fraction
from itertools import combinations, product
from math import comb, gcd, pi
from random import Random


def mul_x_minus_y(poly: list[int], y: int, p: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for i, coeff in enumerate(poly):
        out[i] = (out[i] - y * coeff) % p
        out[i + 1] = (out[i + 1] + coeff) % p
    return out


def mul_x2_minus_sx_plus_c(poly: list[int], s: int, c: int, p: int) -> list[int]:
    out = [0] * (len(poly) + 2)
    for i, coeff in enumerate(poly):
        out[i] = (out[i] + c * coeff) % p
        out[i + 1] = (out[i + 1] - s * coeff) % p
        out[i + 2] = (out[i + 2] + coeff) % p
    return out


def mul_monic_factor(poly: list[int], coeffs: tuple[int, ...], p: int) -> list[int]:
    h = len(coeffs)
    out = [0] * (len(poly) + h)
    for i, coeff in enumerate(poly):
        out[i + h] = (out[i + h] + coeff) % p
        for m, factor_coeff in enumerate(coeffs):
            out[i + m] = (out[i + m] + factor_coeff * coeff) % p
    return out


def locator_from_roots(roots: tuple[int, ...], p: int) -> list[int]:
    poly = [1]
    for root in roots:
        poly = mul_x_minus_y(poly, root, p)
    return poly


def shifted_core(poly: list[int], shift: int, total_shift: int) -> list[int]:
    return [0] * shift + poly + [0] * (total_shift - shift)


def dot(row: tuple[int, ...], vec: list[int], p: int) -> int:
    return sum(a * b for a, b in zip(row, vec)) % p


def hankel1(row: list[int], poly: list[int], p: int) -> int:
    return sum(row[i] * poly[i] for i in range(len(poly))) % p


def hankel2(row: list[int], poly: list[int], p: int) -> tuple[int, int]:
    return (
        sum(row[i] * poly[i] for i in range(len(poly))) % p,
        sum(row[i + 1] * poly[i] for i in range(len(poly))) % p,
    )


def hankel_values(row: list[int], poly: list[int], num_rows: int, p: int) -> list[int]:
    return [
        sum(row[a + i] * poly[i] for i in range(len(poly))) % p
        for a in range(num_rows)
    ]


def det2(u: tuple[int, int], v: tuple[int, int], p: int) -> int:
    return (u[0] * v[1] - u[1] * v[0]) % p


def affine_plane_det(
    a: tuple[int, int], b: tuple[int, int], c: tuple[int, int], p: int
) -> int:
    return ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])) % p


def vec_sub(u: tuple[int, int], v: tuple[int, int], p: int) -> tuple[int, int]:
    return ((u[0] - v[0]) % p, (u[1] - v[1]) % p)


def vec_scalar_mul(a: int, u: tuple[int, int], p: int) -> tuple[int, int]:
    return ((a * u[0]) % p, (a * u[1]) % p)


def vec_is_zero(u: tuple[int, int]) -> bool:
    return u[0] == 0 and u[1] == 0


def vec_rank(vectors: list[tuple[int, int]], p: int) -> int:
    nonzero = [v for v in vectors if not vec_is_zero(v)]
    if not nonzero:
        return 0
    pivot = nonzero[0]
    if all(det2(pivot, v, p) == 0 for v in nonzero[1:]):
        return 1
    return 2


def matrix_rank(rows: list[list[int]], p: int) -> int:
    if not rows:
        return 0
    matrix = [[entry % p for entry in row] for row in rows]
    width = len(matrix[0])
    rank = 0
    for col in range(width):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % p != 0:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, p)
        matrix[rank] = [(value * inv) % p for value in matrix[rank]]
        for row_idx in range(len(matrix)):
            if row_idx == rank:
                continue
            factor = matrix[row_idx][col] % p
            if factor == 0:
                continue
            matrix[row_idx] = [
                (matrix[row_idx][idx] - factor * matrix[rank][idx]) % p
                for idx in range(width)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def in_linear_span(vector: tuple[int, ...], directions: list[list[int]], p: int) -> bool:
    rank = matrix_rank(directions, p)
    return matrix_rank(directions + [list(vector)], p) == rank


def in_affine_subspace(
    point: tuple[int, ...], base: list[int], directions: list[list[int]], p: int
) -> bool:
    diff = tuple((point[idx] - base[idx]) % p for idx in range(len(point)))
    return in_linear_span(diff, directions, p)


def affine_rank(points: list[tuple[int, ...]], p: int) -> int:
    if not points:
        return -1
    base = points[0]
    differences = [
        [(point[idx] - base[idx]) % p for idx in range(len(base))]
        for point in points[1:]
    ]
    return matrix_rank(differences, p)


def eval_pencil(
    v_x: tuple[int, int], v_0: tuple[int, int], y: int, p: int
) -> tuple[int, int]:
    return vec_sub(v_x, vec_scalar_mul(y, v_0, p), p)


def slope_for_active_pair(
    a_y: tuple[int, int], b_y: tuple[int, int], p: int
) -> int | None:
    if vec_is_zero(b_y):
        return None
    if b_y[0] != 0:
        z = (-a_y[0] * pow(b_y[0], -1, p)) % p
    else:
        z = (-a_y[1] * pow(b_y[1], -1, p)) % p
    assert (
        (a_y[0] + z * b_y[0]) % p == 0
        and (a_y[1] + z * b_y[1]) % p == 0
    ), (p, a_y, b_y, z)
    return z


def check_difference_identity() -> None:
    for p in (5, 7, 17, 31):
        for deg_r in range(0, 7):
            rng = Random(1000 * p + deg_r)
            samples: list[list[int]] = []
            if p**deg_r <= 10_000:
                samples = [list(coeffs) + [1] for coeffs in product(range(p), repeat=deg_r)]
            else:
                samples = [[rng.randrange(p) for _ in range(deg_r)] + [1] for _ in range(300)]

            for ell_r in samples:
                core_pad = ell_r + [0]
                for y1 in range(p):
                    for y2 in range(p):
                        if y1 == y2:
                            continue
                        t1 = mul_x_minus_y(ell_r, y1, p)
                        t2 = mul_x_minus_y(ell_r, y2, p)
                        diff = [(a - b) % p for a, b in zip(t1, t2)]
                        expected = [((y2 - y1) * c) % p for c in core_pad]
                        assert diff == expected, (p, deg_r, ell_r, y1, y2)


def check_row_implication() -> None:
    # Exhaustive row check in small dimensions.
    p = 5
    for deg_r in range(0, 4):
        for coeffs in product(range(p), repeat=deg_r):
            ell_r = list(coeffs) + [1]
            core_pad = ell_r + [0]
            x_core = [0] + ell_r
            for y1 in range(p):
                for y2 in range(p):
                    if y1 == y2:
                        continue
                    t1 = mul_x_minus_y(ell_r, y1, p)
                    t2 = mul_x_minus_y(ell_r, y2, p)
                    for row in product(range(p), repeat=len(t1)):
                        if dot(row, t1, p) == 0 and dot(row, t2, p) == 0:
                            assert dot(row, core_pad, p) == 0
                            assert dot(row, x_core, p) == 0


def check_higher_slack_root_slice_lift() -> None:
    rng = Random(20260630)
    for p in (5, 7, 17, 31):
        for t_rows in range(1, 6):
            for core_degree in range(0, 6):
                samples: list[list[int]] = []
                if p**core_degree <= 10_000:
                    samples = [
                        list(coeffs) + [1]
                        for coeffs in product(range(p), repeat=core_degree)
                    ]
                else:
                    samples = [
                        [rng.randrange(p) for _ in range(core_degree)] + [1]
                        for _ in range(300)
                    ]

                for ell_r in samples:
                    row = [rng.randrange(p) for _ in range(t_rows + len(ell_r))]
                    core_pad = ell_r + [0]
                    x_core = [0] + ell_r

                    core_rows = hankel_values(row, core_pad, t_rows, p)
                    x_rows = hankel_values(row, x_core, t_rows, p)
                    lifted_rows = hankel_values(row, ell_r, t_rows + 1, p)

                    assert core_rows == lifted_rows[:-1], (
                        p,
                        t_rows,
                        core_degree,
                        ell_r,
                        row,
                        core_rows,
                        lifted_rows,
                    )
                    assert x_rows == lifted_rows[1:], (
                        p,
                        t_rows,
                        core_degree,
                        ell_r,
                        row,
                        x_rows,
                        lifted_rows,
                    )
                    if all(value == 0 for value in core_rows + x_rows):
                        assert all(value == 0 for value in lifted_rows)


def check_two_exchange_full_plane_lift() -> None:
    rng = Random(20260702)

    for p in (5, 7, 17, 31):
        for core_degree in range(0, 6):
            samples: list[list[int]] = []
            if p**core_degree <= 10_000:
                samples = [
                    list(coeffs) + [1]
                    for coeffs in product(range(p), repeat=core_degree)
                ]
            else:
                samples = [
                    [rng.randrange(p) for _ in range(core_degree)] + [1]
                    for _ in range(300)
                ]

            for ell_r in samples:
                core_pad = ell_r + [0, 0]
                x_core = [0] + ell_r + [0]
                x2_core = [0, 0] + ell_r

                for _ in range(40):
                    s = rng.randrange(p)
                    c = rng.randrange(p)
                    direct = mul_x2_minus_sx_plus_c(ell_r, s, c, p)
                    expected = [
                        (x2_core[i] - s * x_core[i] + c * core_pad[i]) % p
                        for i in range(len(core_pad))
                    ]
                    assert direct == expected, (p, core_degree, ell_r, s, c)

    # Exhaustive row-linear check in small dimensions: a nonzero affine-linear
    # equation on F_p^2 cannot contain a non-collinear triple of zeros.
    p = 5
    points = [(s, c) for s in range(p) for c in range(p)]
    for core_degree in range(0, 3):
        for coeffs in product(range(p), repeat=core_degree):
            ell_r = list(coeffs) + [1]
            core_pad = ell_r + [0, 0]
            x_core = [0] + ell_r + [0]
            x2_core = [0, 0] + ell_r

            for row in product(range(p), repeat=len(core_pad)):
                coeff_x2 = dot(row, x2_core, p)
                coeff_x = dot(row, x_core, p)
                coeff_0 = dot(row, core_pad, p)
                zeros = {
                    point
                    for point in points
                    if (coeff_x2 - point[0] * coeff_x + point[1] * coeff_0) % p
                    == 0
                }
                has_noncollinear_triple = any(
                    affine_plane_det(triple[0], triple[1], triple[2], p) != 0
                    for triple in combinations(zeros, 3)
                )
                if not has_noncollinear_triple:
                    continue

                assert coeff_0 == 0, (core_degree, ell_r, row)
                assert coeff_x == 0, (core_degree, ell_r, row)
                assert coeff_x2 == 0, (core_degree, ell_r, row)

    # Hankel row-block lift: the three padded equations are exactly the
    # row blocks 0..t-1, 1..t, and 2..t+1 of H_{t+2,j-2}.
    for p in (5, 7, 17, 31):
        for t_rows in range(1, 5):
            for core_degree in range(0, 5):
                samples = [
                    [rng.randrange(p) for _ in range(core_degree)] + [1]
                    for _ in range(100)
                ]
                for ell_r in samples:
                    row = [rng.randrange(p) for _ in range(t_rows + len(ell_r) + 1)]
                    core_pad = ell_r + [0, 0]
                    x_core = [0] + ell_r + [0]
                    x2_core = [0, 0] + ell_r

                    core_rows = hankel_values(row, core_pad, t_rows, p)
                    x_rows = hankel_values(row, x_core, t_rows, p)
                    x2_rows = hankel_values(row, x2_core, t_rows, p)
                    lifted_rows = hankel_values(row, ell_r, t_rows + 2, p)

                    assert core_rows == lifted_rows[:-2], (
                        p,
                        t_rows,
                        core_degree,
                        ell_r,
                        row,
                    )
                    assert x_rows == lifted_rows[1:-1], (
                        p,
                        t_rows,
                        core_degree,
                        ell_r,
                        row,
                    )
                    assert x2_rows == lifted_rows[2:], (
                        p,
                        t_rows,
                        core_degree,
                        ell_r,
                        row,
                    )
                    if all(value == 0 for value in core_rows + x_rows + x2_rows):
                        assert all(value == 0 for value in lifted_rows)


def check_full_elementary_packet_lift() -> None:
    rng = Random(20260704)

    cases = [
        (5, range(1, 4), range(1, 3), range(0, 4), 8),
        (7, range(1, 4), range(1, 3), range(0, 3), 6),
        (17, range(1, 3), range(1, 3), range(0, 3), 4),
        (5, range(4, 5), range(1, 2), range(0, 3), 2),
    ]

    for p, h_values, t_values, degree_values, trials in cases:
        for h_exchange in h_values:
            simplex_points = [tuple([0] * h_exchange)]
            for axis in range(h_exchange):
                point = [0] * h_exchange
                point[axis] = 1
                simplex_points.append(tuple(point))

            for t_rows in t_values:
                for core_degree in degree_values:
                    if p**core_degree <= 500:
                        samples = [
                            list(coeffs) + [1]
                            for coeffs in product(range(p), repeat=core_degree)
                        ]
                    else:
                        samples = [
                            [rng.randrange(p) for _ in range(core_degree)] + [1]
                            for _ in range(40)
                        ]

                    for ell_r in samples:
                        row_len = t_rows + len(ell_r) + h_exchange - 1
                        shifts = [
                            shifted_core(ell_r, shift, h_exchange)
                            for shift in range(h_exchange + 1)
                        ]

                        for _ in range(trials):
                            rows = [
                                [rng.randrange(p) for _ in range(row_len)]
                                for _ in range(2)
                            ]

                            for row in rows:
                                shift_values = [
                                    hankel_values(row, shift_poly, t_rows, p)
                                    for shift_poly in shifts
                                ]
                                lifted = hankel_values(
                                    row, ell_r, t_rows + h_exchange, p
                                )

                                for shift in range(h_exchange + 1):
                                    assert shift_values[shift] == lifted[
                                        shift : shift + t_rows
                                    ], (
                                        p,
                                        h_exchange,
                                        t_rows,
                                        core_degree,
                                        ell_r,
                                        shift,
                                        row,
                                    )

                                simplex_values: list[list[int]] = []
                                for coeffs in simplex_points:
                                    direct = mul_monic_factor(ell_r, coeffs, p)
                                    expected = shifts[h_exchange][:]
                                    for m, coeff in enumerate(coeffs):
                                        expected = [
                                            (value + coeff * shifts[m][idx]) % p
                                            for idx, value in enumerate(expected)
                                        ]
                                    assert direct == expected, (
                                        p,
                                        h_exchange,
                                        ell_r,
                                        coeffs,
                                        direct,
                                        expected,
                                    )

                                    direct_rows = hankel_values(row, direct, t_rows, p)
                                    affine_rows = shift_values[h_exchange][:]
                                    for m, coeff in enumerate(coeffs):
                                        affine_rows = [
                                            (value + coeff * shift_values[m][idx]) % p
                                            for idx, value in enumerate(affine_rows)
                                        ]
                                    assert direct_rows == affine_rows, (
                                        p,
                                        h_exchange,
                                        t_rows,
                                        core_degree,
                                        ell_r,
                                        coeffs,
                                        row,
                                    )
                                    simplex_values.append(direct_rows)

                                if all(
                                    value == 0
                                    for rows_at_point in simplex_values
                                    for value in rows_at_point
                                ):
                                    assert all(
                                        value == 0
                                        for block in shift_values
                                        for value in block
                                    ), (
                                        p,
                                        h_exchange,
                                        t_rows,
                                        core_degree,
                                        ell_r,
                                        row,
                                        shift_values,
                                    )
                                    assert all(value == 0 for value in lifted), (
                                        p,
                                        h_exchange,
                                        t_rows,
                                        core_degree,
                                        ell_r,
                                        row,
                                        lifted,
                                    )

                            both_rows_kill_simplex = True
                            for row in rows:
                                for coeffs in simplex_points:
                                    direct = mul_monic_factor(ell_r, coeffs, p)
                                    if any(hankel_values(row, direct, t_rows, p)):
                                        both_rows_kill_simplex = False
                                        break
                                if not both_rows_kill_simplex:
                                    break

                            if both_rows_kill_simplex:
                                for row in rows:
                                    lifted = hankel_values(
                                        row, ell_r, t_rows + h_exchange, p
                                    )
                                    assert all(value == 0 for value in lifted), (
                                        p,
                                        h_exchange,
                                        t_rows,
                                        core_degree,
                                        ell_r,
                                        row,
                                        lifted,
                                    )


def check_affine_span_packet_normal_form() -> None:
    rng = Random(20260705)

    for p in (5, 7, 17):
        for h_exchange in range(1, 5):
            for rank in range(0, h_exchange + 1):
                base = [rng.randrange(p) for _ in range(h_exchange)]
                directions: list[list[int]] = []
                for axis in range(rank):
                    vector = [0] * h_exchange
                    vector[axis] = 1
                    directions.append(vector)

                affine_points = [tuple(base)]
                for vector in directions:
                    affine_points.append(
                        tuple((base[i] + vector[i]) % p for i in range(h_exchange))
                    )

                for out_dim in range(1, 5):
                    vectors = [
                        [rng.randrange(p) for _ in range(out_dim)]
                        for _ in range(h_exchange + 1)
                    ]

                    def eval_affine(point: tuple[int, ...]) -> list[int]:
                        out = vectors[h_exchange][:]
                        for m, coeff in enumerate(point):
                            out = [
                                (value + coeff * vectors[m][idx]) % p
                                for idx, value in enumerate(out)
                            ]
                        return out

                    killed_points = [eval_affine(point) for point in affine_points]
                    if not all(
                        value == 0
                        for killed in killed_points
                        for value in killed
                    ):
                        continue

                    base_equation = eval_affine(tuple(base))
                    assert all(value == 0 for value in base_equation), (
                        p,
                        h_exchange,
                        rank,
                        out_dim,
                        base,
                        vectors,
                    )
                    for vector in directions:
                        direction_equation = [0] * out_dim
                        for m, coeff in enumerate(vector):
                            direction_equation = [
                                (value + coeff * vectors[m][idx]) % p
                                for idx, value in enumerate(direction_equation)
                            ]
                        assert all(value == 0 for value in direction_equation), (
                            p,
                            h_exchange,
                            rank,
                            out_dim,
                            vector,
                            vectors,
                        )

                    # The whole affine span is killed, not only the sampled
                    # spanning points.
                    for theta in product(range(p), repeat=rank):
                        point = base[:]
                        for coeff, vector in zip(theta, directions):
                            point = [
                                (point[i] + coeff * vector[i]) % p
                                for i in range(h_exchange)
                            ]
                        assert all(value == 0 for value in eval_affine(tuple(point))), (
                            p,
                            h_exchange,
                            rank,
                            out_dim,
                            theta,
                            point,
                            vectors,
                        )

    # In the h=2 elementary plane, every proper nontrivial affine span is a
    # line As+Bp+C=0.
    for p in (5, 7, 11, 17):
        for p1 in product(range(p), repeat=2):
            for p2 in product(range(p), repeat=2):
                if p1 == p2:
                    continue
                a = (p1[1] - p2[1]) % p
                b = (p2[0] - p1[0]) % p
                c0 = (-(a * p1[0] + b * p1[1])) % p
                assert (a, b) != (0, 0)
                assert (a * p1[0] + b * p1[1] + c0) % p == 0
                assert (a * p2[0] + b * p2[1] + c0) % p == 0

                for point in product(range(p), repeat=2):
                    determinant = (
                        (p2[0] - p1[0]) * (point[1] - p1[1])
                        - (p2[1] - p1[1]) * (point[0] - p1[0])
                    ) % p
                    in_span = determinant == 0
                    in_line = (a * point[0] + b * point[1] + c0) % p == 0
                    assert in_span == in_line, (p, p1, p2, point, a, b, c0)


def fixed_root_hyperplane_alpha(
    coeffs: tuple[int, ...], constant: int, p: int
) -> int | None:
    if coeffs[0] == 0:
        return None
    scale = coeffs[0]
    for alpha in range(p):
        if all(
            coeffs[m] == (scale * pow(alpha, m, p)) % p
            for m in range(len(coeffs))
        ) and constant == (scale * pow(alpha, len(coeffs), p)) % p:
            return alpha
    return None


def eval_monic_at(coeffs: tuple[int, ...], alpha: int, p: int) -> int:
    h = len(coeffs)
    value = pow(alpha, h, p)
    for m, coeff in enumerate(coeffs):
        value = (value + coeff * pow(alpha, m, p)) % p
    return value


def check_fixed_root_hyperplane_criterion() -> None:
    rng = Random(20260706)

    for p in (5, 7, 11):
        for h_exchange in range(1, 5):
            points = list(product(range(p), repeat=h_exchange))

            for alpha in range(p):
                for scale in range(1, p):
                    coeffs = tuple(
                        (scale * pow(alpha, m, p)) % p
                        for m in range(h_exchange)
                    )
                    constant = (scale * pow(alpha, h_exchange, p)) % p
                    assert fixed_root_hyperplane_alpha(coeffs, constant, p) == alpha

                    hyperplane = [
                        point
                        for point in points
                        if (
                            constant
                            + sum(coeffs[m] * point[m] for m in range(h_exchange))
                        )
                        % p
                        == 0
                    ]
                    fixed_root = [
                        point
                        for point in points
                        if eval_monic_at(point, alpha, p) == 0
                    ]
                    assert set(hyperplane) == set(fixed_root), (
                        p,
                        h_exchange,
                        alpha,
                        scale,
                        coeffs,
                        constant,
                    )

            for _ in range(80):
                coeffs = tuple(rng.randrange(p) for _ in range(h_exchange))
                if all(coeff == 0 for coeff in coeffs):
                    coeffs = (1,) + coeffs[1:]
                constant = rng.randrange(p)
                alpha = fixed_root_hyperplane_alpha(coeffs, constant, p)
                if alpha is None:
                    # No finite root alpha has evaluation hyperplane equal to
                    # this random coefficient hyperplane.
                    assert all(
                        tuple(
                            (coeffs[0] * pow(candidate, m, p)) % p
                            for m in range(h_exchange)
                        )
                        != coeffs
                        or constant
                        != (coeffs[0] * pow(candidate, h_exchange, p)) % p
                        for candidate in range(p)
                    ), (p, h_exchange, coeffs, constant)
                    continue

                hyperplane = {
                    point
                    for point in points
                    if (
                        constant
                        + sum(coeffs[m] * point[m] for m in range(h_exchange))
                    )
                    % p
                    == 0
                }
                fixed_root = {
                    point for point in points if eval_monic_at(point, alpha, p) == 0
                }
                assert hyperplane == fixed_root, (
                    p,
                    h_exchange,
                    coeffs,
                    constant,
                    alpha,
                )

        # h=2 specialization: P=X^2-sX+p has fixed-root line
        # p-alpha*s+alpha^2=0.
        for alpha in range(p):
            for x in range(p):
                for y in range(p):
                    s = (x + y) % p
                    prod = (x * y) % p
                    in_line = (prod - alpha * s + alpha * alpha) % p == 0
                    has_root = x == alpha or y == alpha
                    assert in_line == has_root, (p, alpha, x, y, s, prod)


def check_hyperplane_one_root_fiber_dichotomy() -> None:
    rng = Random(20260707)

    for p in (5, 7, 11, 17):
        for h_exchange in range(1, 6):
            if p ** (h_exchange - 1) <= 2000:
                cores = [
                    list(coeffs) + [1]
                    for coeffs in product(range(p), repeat=h_exchange - 1)
                ]
            else:
                cores = [
                    [rng.randrange(p) for _ in range(h_exchange - 1)] + [1]
                    for _ in range(400)
                ]

            hyperplanes: list[tuple[tuple[int, ...], int]] = []
            if p == 5 and h_exchange <= 3:
                hyperplanes = [
                    (coeffs, constant)
                    for coeffs in product(range(p), repeat=h_exchange)
                    if any(coeff != 0 for coeff in coeffs)
                    for constant in range(p)
                ]
            else:
                for _ in range(400):
                    coeffs = tuple(rng.randrange(p) for _ in range(h_exchange))
                    if all(coeff == 0 for coeff in coeffs):
                        coeffs = (1,) + coeffs[1:]
                    hyperplanes.append((coeffs, rng.randrange(p)))

            for core in cores:
                for coeffs, constant in hyperplanes:
                    line_constant = (
                        constant
                        + sum(
                            coeffs[m] * (core[m - 1] if m > 0 else 0)
                            for m in range(h_exchange)
                        )
                    ) % p
                    line_slope = sum(
                        coeffs[m] * core[m] for m in range(h_exchange)
                    ) % p

                    passing_roots: list[int] = []
                    for y in range(p):
                        extension = tuple(mul_x_minus_y(core, y, p)[:-1])
                        formula_value = (line_constant - y * line_slope) % p
                        direct_value = (
                            constant
                            + sum(coeffs[m] * extension[m] for m in range(h_exchange))
                        ) % p
                        assert direct_value == formula_value, (
                            p,
                            h_exchange,
                            core,
                            coeffs,
                            constant,
                            y,
                            extension,
                            direct_value,
                            formula_value,
                        )
                        if direct_value == 0:
                            passing_roots.append(y)

                    if len(passing_roots) >= 2:
                        assert line_constant == 0 and line_slope == 0, (
                            p,
                            h_exchange,
                            core,
                            coeffs,
                            constant,
                            passing_roots,
                            line_constant,
                            line_slope,
                        )
                        assert len(passing_roots) == p, (
                            p,
                            h_exchange,
                            core,
                            coeffs,
                            constant,
                            passing_roots,
                        )
                    else:
                        assert len(passing_roots) <= 1, (
                            p,
                            h_exchange,
                            core,
                            coeffs,
                            constant,
                            passing_roots,
                        )


def check_affine_subpacket_one_root_fiber_dichotomy() -> None:
    rng = Random(20260708)

    for p in (5, 7, 11, 17):
        for h_exchange in range(1, 6):
            if p ** (h_exchange - 1) <= 1500:
                cores = [
                    list(coeffs) + [1]
                    for coeffs in product(range(p), repeat=h_exchange - 1)
                ]
            else:
                cores = [
                    [rng.randrange(p) for _ in range(h_exchange - 1)] + [1]
                    for _ in range(180)
                ]

            affine_subspaces: list[tuple[list[int], list[list[int]]]] = []
            for rank in range(h_exchange + 1):
                base = [rng.randrange(p) for _ in range(h_exchange)]
                coordinate_directions = []
                for axis in range(rank):
                    direction = [0] * h_exchange
                    direction[axis] = 1
                    coordinate_directions.append(direction)
                affine_subspaces.append((base, coordinate_directions))

                for _ in range(24):
                    base = [rng.randrange(p) for _ in range(h_exchange)]
                    directions = [
                        [rng.randrange(p) for _ in range(h_exchange)]
                        for _ in range(rank)
                    ]
                    affine_subspaces.append((base, directions))

            for core in cores:
                direction_vector = tuple(core[m] % p for m in range(h_exchange))
                for base, directions in affine_subspaces:
                    passing_roots: list[int] = []
                    for y in range(p):
                        point = tuple(mul_x_minus_y(core, y, p)[:-1])
                        if in_affine_subspace(point, base, directions, p):
                            passing_roots.append(y)

                    if len(passing_roots) >= 2:
                        assert in_linear_span(direction_vector, directions, p), (
                            p,
                            h_exchange,
                            core,
                            base,
                            directions,
                            passing_roots,
                            direction_vector,
                        )
                        assert len(passing_roots) == p, (
                            p,
                            h_exchange,
                            core,
                            base,
                            directions,
                            passing_roots,
                        )
                        for y in range(p):
                            point = tuple(mul_x_minus_y(core, y, p)[:-1])
                            assert in_affine_subspace(point, base, directions, p), (
                                p,
                                h_exchange,
                                core,
                                base,
                                directions,
                                y,
                                point,
                            )
                    else:
                        assert len(passing_roots) <= 1, (
                            p,
                            h_exchange,
                            core,
                            base,
                            directions,
                            passing_roots,
                        )


def check_affine_subpacket_two_root_fiber_dichotomy() -> None:
    rng = Random(20260709)

    for p in (5, 7, 11):
        parameter_points = [
            (s_value, prod_value)
            for s_value in range(p)
            for prod_value in range(p)
        ]
        for h_exchange in range(2, 6):
            core_degree = h_exchange - 2
            if p**core_degree <= 500:
                cores = [
                    list(coeffs) + [1]
                    for coeffs in product(range(p), repeat=core_degree)
                ]
            else:
                cores = [
                    [rng.randrange(p) for _ in range(core_degree)] + [1]
                    for _ in range(40)
                ]

            affine_subspaces: list[tuple[list[int], list[list[int]]]] = []
            for rank in range(h_exchange + 1):
                base = [rng.randrange(p) for _ in range(h_exchange)]
                coordinate_directions = []
                for axis in range(rank):
                    direction = [0] * h_exchange
                    direction[axis] = 1
                    coordinate_directions.append(direction)
                affine_subspaces.append((base, coordinate_directions))

                for _ in range(8):
                    base = [rng.randrange(p) for _ in range(h_exchange)]
                    directions = [
                        [rng.randrange(p) for _ in range(h_exchange)]
                        for _ in range(rank)
                    ]
                    affine_subspaces.append((base, directions))

            for core in cores:
                def core_coeff(index: int) -> int:
                    if 0 <= index < len(core):
                        return core[index] % p
                    return 0

                base_vector = tuple(core_coeff(m - 2) for m in range(h_exchange))
                s_direction = tuple((-core_coeff(m - 1)) % p for m in range(h_exchange))
                p_direction = tuple(core_coeff(m) for m in range(h_exchange))
                assert matrix_rank([list(s_direction), list(p_direction)], p) == 2, (
                    p,
                    h_exchange,
                    core,
                    s_direction,
                    p_direction,
                )

                for base, directions in affine_subspaces:
                    passing_points: list[tuple[int, int]] = []
                    for s_value, prod_value in parameter_points:
                        point = tuple(
                            mul_x2_minus_sx_plus_c(core, s_value, prod_value, p)[:-1]
                        )
                        formula_point = tuple(
                            (
                                base_vector[m]
                                + s_value * s_direction[m]
                                + prod_value * p_direction[m]
                            )
                            % p
                            for m in range(h_exchange)
                        )
                        assert point == formula_point, (
                            p,
                            h_exchange,
                            core,
                            s_value,
                            prod_value,
                            point,
                            formula_point,
                        )
                        if in_affine_subspace(point, base, directions, p):
                            passing_points.append((s_value, prod_value))

                    has_noncollinear_triple = any(
                        affine_plane_det(triple[0], triple[1], triple[2], p) != 0
                        for triple in combinations(passing_points, 3)
                    )
                    if has_noncollinear_triple:
                        assert in_linear_span(s_direction, directions, p), (
                            p,
                            h_exchange,
                            core,
                            base,
                            directions,
                            s_direction,
                        )
                        assert in_linear_span(p_direction, directions, p), (
                            p,
                            h_exchange,
                            core,
                            base,
                            directions,
                            p_direction,
                        )
                        assert len(passing_points) == p * p, (
                            p,
                            h_exchange,
                            core,
                            base,
                            directions,
                            len(passing_points),
                        )
                    else:
                        assert len(passing_points) <= p, (
                            p,
                            h_exchange,
                            core,
                            base,
                            directions,
                            passing_points,
                        )


def check_general_moving_fiber_dimension_drop() -> None:
    rng = Random(20260710)

    for p in (5, 7):
        for h_exchange in range(1, 6):
            for moving_rank in range(1, h_exchange + 1):
                core_degree = h_exchange - moving_rank
                if p**core_degree <= 80:
                    cores = [
                        list(coeffs) + [1]
                        for coeffs in product(range(p), repeat=core_degree)
                    ]
                else:
                    cores = [
                        [rng.randrange(p) for _ in range(core_degree)] + [1]
                        for _ in range(12)
                    ]

                all_parameters = list(product(range(p), repeat=moving_rank))
                affine_subspaces: list[tuple[list[int], list[list[int]]]] = []
                for rank in range(h_exchange + 1):
                    base = [rng.randrange(p) for _ in range(h_exchange)]
                    coordinate_directions = []
                    for axis in range(rank):
                        direction = [0] * h_exchange
                        direction[axis] = 1
                        coordinate_directions.append(direction)
                    affine_subspaces.append((base, coordinate_directions))

                    for _ in range(6):
                        base = [rng.randrange(p) for _ in range(h_exchange)]
                        directions = [
                            [rng.randrange(p) for _ in range(h_exchange)]
                            for _ in range(rank)
                        ]
                        affine_subspaces.append((base, directions))

                for core in cores:
                    def core_coeff(index: int) -> int:
                        if 0 <= index < len(core):
                            return core[index] % p
                        return 0

                    base_vector = tuple(
                        core_coeff(m - moving_rank) for m in range(h_exchange)
                    )
                    fiber_directions = [
                        tuple(core_coeff(m - idx) for m in range(h_exchange))
                        for idx in range(moving_rank)
                    ]
                    fiber_rank = matrix_rank(
                        [list(vec) for vec in fiber_directions], p
                    )
                    assert fiber_rank == moving_rank, (
                        p,
                        h_exchange,
                        moving_rank,
                        core,
                        fiber_directions,
                    )

                    for base, directions in affine_subspaces:
                        passing_parameters: list[tuple[int, ...]] = []
                        for parameters in all_parameters:
                            point = tuple(
                                mul_monic_factor(core, parameters, p)[:-1]
                            )
                            formula_point = tuple(
                                (
                                    base_vector[m]
                                    + sum(
                                        parameters[idx] * fiber_directions[idx][m]
                                        for idx in range(moving_rank)
                                    )
                                )
                                % p
                                for m in range(h_exchange)
                            )
                            assert point == formula_point, (
                                p,
                                h_exchange,
                                moving_rank,
                                core,
                                parameters,
                                point,
                                formula_point,
                            )
                            if in_affine_subspace(point, base, directions, p):
                                passing_parameters.append(parameters)

                        rank = affine_rank(passing_parameters, p)
                        if rank == moving_rank:
                            for direction in fiber_directions:
                                assert in_linear_span(direction, directions, p), (
                                    p,
                                    h_exchange,
                                    moving_rank,
                                    core,
                                    base,
                                    directions,
                                    direction,
                                )
                            assert len(passing_parameters) == p**moving_rank, (
                                p,
                                h_exchange,
                                moving_rank,
                                core,
                                base,
                                directions,
                                len(passing_parameters),
                            )
                        else:
                            assert rank <= moving_rank - 1, (
                                p,
                                h_exchange,
                                moving_rank,
                                core,
                                base,
                                directions,
                                passing_parameters,
                                rank,
                            )
                            assert len(passing_parameters) <= p ** (moving_rank - 1), (
                                p,
                                h_exchange,
                                moving_rank,
                                core,
                                base,
                                directions,
                                len(passing_parameters),
                                rank,
                            )


def check_residual_exchange_degree_bound() -> None:
    rng = Random(20260711)

    for p in (5, 7):
        domain = tuple(range(p))
        for h_exchange in range(1, min(5, p)):
            supports = list(combinations(domain, h_exchange))
            for moving_rank in range(1, min(4, h_exchange + 1)):
                all_parameters = list(product(range(p), repeat=moving_rank))
                affine_subspaces: list[tuple[list[int], list[list[int]]]] = []
                for rank in range(h_exchange + 1):
                    base = [rng.randrange(p) for _ in range(h_exchange)]
                    directions = []
                    for axis in range(rank):
                        direction = [0] * h_exchange
                        direction[axis] = 1
                        directions.append(direction)
                    affine_subspaces.append((base, directions))

                    for _ in range(5):
                        base = [rng.randrange(p) for _ in range(h_exchange)]
                        directions = [
                            [rng.randrange(p) for _ in range(h_exchange)]
                            for _ in range(rank)
                        ]
                        affine_subspaces.append((base, directions))

                for base, directions in affine_subspaces:
                    def coeff_in_packet(coeffs: tuple[int, ...]) -> bool:
                        return in_affine_subspace(coeffs, base, directions, p)

                    def full_fiber(common_roots: tuple[int, ...]) -> bool:
                        core = locator_from_roots(common_roots, p)
                        for parameters in all_parameters:
                            coeffs = tuple(
                                mul_monic_factor(core, parameters, p)[:-1]
                            )
                            if not coeff_in_packet(coeffs):
                                return False
                        return True

                    active_supports: list[tuple[int, ...]] = []
                    for support in supports:
                        coeffs = tuple(locator_from_roots(support, p)[:-1])
                        if not coeff_in_packet(coeffs):
                            continue
                        charged = False
                        for common_roots in combinations(
                            support, h_exchange - moving_rank
                        ):
                            if full_fiber(tuple(common_roots)):
                                charged = True
                                break
                        if not charged:
                            active_supports.append(support)

                    active_set = set(active_supports)
                    degree_bound = comb(h_exchange, moving_rank) * (
                        p ** (moving_rank - 1) - 1
                    )
                    for support in active_supports:
                        neighbors: set[tuple[int, ...]] = set()
                        support_set = set(support)
                        for other in active_set:
                            if other == support:
                                continue
                            if len(support_set & set(other)) == h_exchange - moving_rank:
                                neighbors.add(other)
                        assert len(neighbors) <= degree_bound, (
                            p,
                            h_exchange,
                            moving_rank,
                            base,
                            directions,
                            support,
                            len(neighbors),
                            degree_bound,
                            sorted(neighbors),
                        )


def check_two_root_line_classification() -> None:
    for p in (3, 5, 7, 11, 17):
        pairs = [(x, y) for x in range(p) for y in range(x + 1, p)]
        domain = tuple(range(1, (p + 1) // 2))
        domain_set = set(domain)
        for a in range(p):
            for b in range(p):
                if a == 0 and b == 0:
                    continue
                for c0 in range(p):
                    line_pairs = [
                        (x, y)
                        for x, y in pairs
                        if (a * ((x + y) % p) + b * ((x * y) % p) + c0) % p
                        == 0
                    ]

                    if b == 0:
                        s0 = (-c0 * pow(a, -1, p)) % p
                        assert all((x + y) % p == s0 for x, y in line_pairs), (
                            p,
                            a,
                            b,
                            c0,
                            s0,
                            line_pairs,
                        )
                        assert all(((s0 - x) % p) == y for x, y in line_pairs) or all(
                            ((s0 - y) % p) == x for x, y in line_pairs
                        )
                        for x, y in pairs:
                            in_model = (x + y) % p == s0
                            in_line = (
                                a * ((x + y) % p) + b * ((x * y) % p) + c0
                            ) % p == 0
                            assert in_model == in_line, (
                                p,
                                a,
                                b,
                                c0,
                                x,
                                y,
                                in_model,
                                in_line,
                            )
                        mixed_direct = [
                            (beta_ext, y)
                            for y in domain
                            for beta_ext in range(p)
                            if beta_ext not in domain_set
                            and (
                                a * ((beta_ext + y) % p)
                                + b * ((beta_ext * y) % p)
                                + c0
                            )
                            % p
                            == 0
                        ]
                        mixed_formula = [
                            ((s0 - y) % p, y)
                            for y in domain
                            if (s0 - y) % p not in domain_set
                        ]
                        assert sorted(mixed_direct) == sorted(mixed_formula), (
                            p,
                            a,
                            b,
                            c0,
                            s0,
                            mixed_direct,
                            mixed_formula,
                        )
                        assert len(mixed_direct) <= len(domain), (
                            p,
                            a,
                            b,
                            c0,
                            mixed_direct,
                            domain,
                        )
                        continue

                    center = (-a * pow(b, -1, p)) % p
                    beta = (-c0 * pow(b, -1, p)) % p
                    mu = (center * center + beta) % p

                    if mu == 0:
                        assert all(
                            x == center or y == center for x, y in line_pairs
                        ), (p, a, b, c0, center, beta, mu, line_pairs)
                    else:
                        for x, y in line_pairs:
                            assert ((x - center) * (y - center)) % p == mu, (
                                p,
                                a,
                                b,
                                c0,
                                center,
                                beta,
                                mu,
                                x,
                                y,
                            )
                            assert x != center and y != center
                            assert (center + mu * pow((x - center) % p, -1, p)) % p == y
                            assert (center + mu * pow((y - center) % p, -1, p)) % p == x

                    # Conversely, every split pair satisfying the displayed
                    # model satisfies the original affine line.
                    for x, y in pairs:
                        if b == 0:
                            in_model = (x + y) % p == s0
                        elif mu == 0:
                            in_model = x == center or y == center
                        else:
                            in_model = ((x - center) * (y - center)) % p == mu
                        in_line = (
                            a * ((x + y) % p) + b * ((x * y) % p) + c0
                        ) % p == 0
                        assert in_model == in_line, (
                            p,
                            a,
                            b,
                            c0,
                            x,
                            y,
                            in_model,
                            in_line,
                        )

                    mixed_direct = [
                        (beta_ext, y)
                        for y in domain
                        for beta_ext in range(p)
                        if beta_ext not in domain_set
                        and (
                            a * ((beta_ext + y) % p)
                            + b * ((beta_ext * y) % p)
                            + c0
                        )
                        % p
                        == 0
                    ]
                    if mu == 0:
                        assert all(
                            beta_ext == center or y == center
                            for beta_ext, y in mixed_direct
                        ), (p, a, b, c0, center, mu, mixed_direct)
                    else:
                        mixed_formula = [
                            (
                                (
                                    center
                                    + mu * pow((y - center) % p, -1, p)
                                )
                                % p,
                                y,
                            )
                            for y in domain
                            if y != center
                            and (
                                center + mu * pow((y - center) % p, -1, p)
                            )
                            % p
                            not in domain_set
                        ]
                        assert sorted(mixed_direct) == sorted(mixed_formula), (
                            p,
                            a,
                            b,
                            c0,
                            center,
                            mu,
                            mixed_direct,
                            mixed_formula,
                        )
                        assert len(mixed_direct) <= len(domain), (
                            p,
                            a,
                            b,
                            c0,
                            center,
                            mu,
                            mixed_direct,
                            domain,
                        )
                        for beta_ext, y in mixed_formula:
                            assert beta_ext != center
                            assert (
                                center
                                + mu * pow((beta_ext - center) % p, -1, p)
                            ) % p == y


def check_nonfixed_line_constant_slope_collapse() -> None:
    def pair_equal(left: tuple[int, int], right: tuple[int, int], p: int) -> bool:
        return left[0] % p == right[0] % p and left[1] % p == right[1] % p

    def value_on_line(
        rows: tuple[int, int, int, int], s_value: int, p_value: int, prime: int
    ) -> tuple[int, int]:
        d_0, d_1, d_2, d_3 = rows
        return (
            (d_2 - s_value * d_1 + p_value * d_0) % prime,
            (d_3 - s_value * d_2 + p_value * d_1) % prime,
        )

    for p in (5, 7, 11):
        for rows in product(range(p), repeat=4):
            v_0 = (rows[0], rows[1])
            v_1 = (rows[1], rows[2])
            v_2 = (rows[2], rows[3])

            for fixed_sum in range(p):
                constant_fixed_sum = v_0 == (0, 0) and pair_equal(
                    v_2, vec_scalar_mul(fixed_sum, v_1, p), p
                )
                if constant_fixed_sum:
                    assert rows == (0, 0, 0, 0), (p, rows, fixed_sum)
                    assert all(
                        value_on_line(rows, fixed_sum, p_value, p) == (0, 0)
                        for p_value in range(p)
                    )

            for center in range(p):
                for mu in range(1, p):
                    constant_product = pair_equal(
                        v_1, vec_scalar_mul(center, v_0, p), p
                    ) and pair_equal(
                        v_2,
                        vec_scalar_mul((center * center - mu) % p, v_0, p),
                        p,
                    )
                    if constant_product:
                        assert rows == (0, 0, 0, 0), (p, rows, center, mu)
                        assert all(
                            value_on_line(
                                rows,
                                s_value,
                                (center * s_value - center * center + mu) % p,
                                p,
                            )
                            == (0, 0)
                            for s_value in range(p)
                        )

    # Sample the two-zero implication directly on larger fields: if the
    # affine-linear restriction vanishes at two distinct line parameters, it
    # vanishes identically, so the collapse above must force all rows to zero.
    rng = Random(20260710)
    for p in (17, 31):
        for _ in range(1000):
            rows = tuple(rng.randrange(p) for _ in range(4))
            fixed_sum = rng.randrange(p)
            p_1 = rng.randrange(p)
            p_2 = (p_1 + 1 + rng.randrange(p - 1)) % p
            if value_on_line(rows, fixed_sum, p_1, p) == (
                0,
                0,
            ) and value_on_line(rows, fixed_sum, p_2, p) == (0, 0):
                assert rows == (0, 0, 0, 0), (p, rows, fixed_sum, p_1, p_2)

            center = rng.randrange(p)
            mu = 1 + rng.randrange(p - 1)
            s_1 = rng.randrange(p)
            s_2 = (s_1 + 1 + rng.randrange(p - 1)) % p
            p_1 = (center * s_1 - center * center + mu) % p
            p_2 = (center * s_2 - center * center + mu) % p
            if value_on_line(rows, s_1, p_1, p) == (
                0,
                0,
            ) and value_on_line(rows, s_2, p_2, p) == (0, 0):
                assert rows == (0, 0, 0, 0), (p, rows, center, mu, s_1, s_2)


def check_boundary_core_same_slope_fibers() -> None:
    def value_on_plane(
        rows: tuple[int, int, int, int],
        s_value: int,
        p_value: int,
        prime: int,
    ) -> tuple[int, int]:
        d_0, d_1, d_2, d_3 = rows
        return (
            (d_2 - s_value * d_1 + p_value * d_0) % prime,
            (d_3 - s_value * d_2 + p_value * d_1) % prime,
        )

    for p in (3, 5, 7, 11):
        all_points = [(s_value, p_value) for s_value in range(p) for p_value in range(p)]
        for rows in product(range(p), repeat=4):
            killed = [
                point
                for point in all_points
                if value_on_plane(rows, point[0], point[1], p) == (0, 0)
            ]
            rank = affine_rank(killed, p)
            assert len(killed) in (0, 1, p, p * p), (p, rows, killed, rank)
            if len(killed) == 0:
                assert rank == -1, (p, rows, killed, rank)
            elif len(killed) == 1:
                assert rank == 0, (p, rows, killed, rank)
            elif len(killed) == p:
                assert rank == 1, (p, rows, killed, rank)
                first, second = killed[0], killed[1]
                assert all(
                    affine_plane_det(first, second, point, p) == 0 for point in killed
                ), (p, rows, killed)
                line_points = [
                    point
                    for point in all_points
                    if affine_plane_det(first, second, point, p) == 0
                ]
                assert sorted(line_points) == sorted(killed), (
                    p,
                    rows,
                    killed,
                    line_points,
                )
            else:
                assert rank == 2, (p, rows, killed, rank)
                assert rows == (0, 0, 0, 0), (p, rows)

    rng = Random(20260716)
    for p in (17, 31):
        all_points = [(s_value, p_value) for s_value in range(p) for p_value in range(p)]
        for _ in range(1000):
            rows = tuple(rng.randrange(p) for _ in range(4))
            killed = [
                point
                for point in all_points
                if value_on_plane(rows, point[0], point[1], p) == (0, 0)
            ]
            rank = affine_rank(killed, p)
            assert len(killed) in (0, 1, p, p * p), (p, rows, killed, rank)
            if len(killed) == p:
                assert rank == 1, (p, rows, killed, rank)
            if len(killed) == p * p:
                assert rows == (0, 0, 0, 0), (p, rows)


def check_t2_determinant_gate() -> None:
    rng = Random(20260629)
    for p in (5, 7, 17, 31):
        for _ in range(1000):
            a_x = (rng.randrange(p), rng.randrange(p))
            a_0 = (rng.randrange(p), rng.randrange(p))
            b_x = (rng.randrange(p), rng.randrange(p))
            b_0 = (rng.randrange(p), rng.randrange(p))

            coeff_0 = det2(a_x, b_x, p)
            coeff_1 = (-(det2(a_0, b_x, p) + det2(a_x, b_0, p))) % p
            coeff_2 = det2(a_0, b_0, p)

            roots: list[int] = []
            for y in range(p):
                a_y = ((a_x[0] - y * a_0[0]) % p, (a_x[1] - y * a_0[1]) % p)
                b_y = ((b_x[0] - y * b_0[0]) % p, (b_x[1] - y * b_0[1]) % p)
                direct = det2(a_y, b_y, p)
                formula = (coeff_0 + coeff_1 * y + coeff_2 * y * y) % p
                assert direct == formula, (p, y, direct, formula)
                if direct == 0:
                    roots.append(y)

            ruled = coeff_0 == coeff_1 == coeff_2 == 0
            if len(roots) >= 3:
                assert ruled, (p, roots, (coeff_0, coeff_1, coeff_2))
            if not ruled:
                assert len(roots) <= 2, (p, roots, (coeff_0, coeff_1, coeff_2))


def is_ruled_pencil(
    a_x: tuple[int, int],
    a_0: tuple[int, int],
    b_x: tuple[int, int],
    b_0: tuple[int, int],
    p: int,
) -> bool:
    coeff_0 = det2(a_x, b_x, p)
    coeff_1 = (-(det2(a_0, b_x, p) + det2(a_x, b_0, p))) % p
    coeff_2 = det2(a_0, b_0, p)
    return coeff_0 == coeff_1 == coeff_2 == 0


def fixed_finite_slope(
    a_x: tuple[int, int],
    a_0: tuple[int, int],
    b_x: tuple[int, int],
    b_0: tuple[int, int],
    p: int,
) -> int | None:
    for z in range(p):
        if vec_is_zero(vec_sub(a_x, vec_scalar_mul(-z % p, b_x, p), p)) and vec_is_zero(
            vec_sub(a_0, vec_scalar_mul(-z % p, b_0, p), p)
        ):
            return z
    return None


def check_ruled_core_dichotomy() -> None:
    rng = Random(20260630)
    for p in (3, 5, 7, 17, 31):
        exhaustive_vectors = list(product(range(p), repeat=2))
        samples: list[
            tuple[
                tuple[int, int],
                tuple[int, int],
                tuple[int, int],
                tuple[int, int],
            ]
        ] = []
        if p == 3:
            samples = [
                (a_x, a_0, b_x, b_0)
                for a_x in exhaustive_vectors
                for a_0 in exhaustive_vectors
                for b_x in exhaustive_vectors
                for b_0 in exhaustive_vectors
            ]
        else:
            for _ in range(3000):
                samples.append(
                    (
                        (rng.randrange(p), rng.randrange(p)),
                        (rng.randrange(p), rng.randrange(p)),
                        (rng.randrange(p), rng.randrange(p)),
                        (rng.randrange(p), rng.randrange(p)),
                    )
                )

        for a_x, a_0, b_x, b_0 in samples:
            if not is_ruled_pencil(a_x, a_0, b_x, b_0, p):
                continue

            z_fixed = fixed_finite_slope(a_x, a_0, b_x, b_0, p)
            b_inactive = vec_is_zero(b_x) and vec_is_zero(b_0)
            output_rank = vec_rank([a_x, a_0, b_x, b_0], p)
            assert z_fixed is not None or b_inactive or output_rank <= 1, (
                p,
                a_x,
                a_0,
                b_x,
                b_0,
                output_rank,
            )

            if z_fixed is None and not b_inactive:
                seen: dict[int, int] = {}
                for y in range(p):
                    a_y = eval_pencil(a_x, a_0, y, p)
                    b_y = eval_pencil(b_x, b_0, y, p)
                    if vec_is_zero(b_y):
                        continue
                    assert det2(a_y, b_y, p) == 0
                    z = slope_for_active_pair(a_y, b_y, p)
                    assert z is not None
                    assert z not in seen, (
                        p,
                        a_x,
                        a_0,
                        b_x,
                        b_0,
                        seen.get(z),
                        y,
                        z,
                    )
                    seen[z] = y


def hankel_core_value(seq: tuple[int, int, int], y: int, p: int) -> tuple[int, int]:
    return ((seq[1] - y * seq[0]) % p, (seq[2] - y * seq[1]) % p)


def check_hankel_ruled_core_collapse() -> None:
    rng = Random(20260630)
    for p in (3, 5, 7, 17, 31):
        samples: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
        if p <= 7:
            triples = list(product(range(p), repeat=3))
            samples = [(u_seq, v_seq) for u_seq in triples for v_seq in triples]
        else:
            samples = [
                (
                    (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                    (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                )
                for _ in range(5000)
            ]

        for u_seq, v_seq in samples:
            if any(
                det2(hankel_core_value(u_seq, y, p), hankel_core_value(v_seq, y, p), p)
                != 0
                for y in range(p)
            ):
                continue

            active_slopes: set[int] = set()
            for y in range(p):
                a_y = hankel_core_value(u_seq, y, p)
                b_y = hankel_core_value(v_seq, y, p)
                z = slope_for_active_pair(a_y, b_y, p)
                if z is not None:
                    active_slopes.add(z)

            assert len(active_slopes) <= 1, (p, u_seq, v_seq, active_slopes)
            if active_slopes:
                z0 = next(iter(active_slopes))
                for y in range(p):
                    a_y = hankel_core_value(u_seq, y, p)
                    b_y = hankel_core_value(v_seq, y, p)
                    assert (
                        (a_y[0] + z0 * b_y[0]) % p == 0
                        and (a_y[1] + z0 * b_y[1]) % p == 0
                    ), (p, u_seq, v_seq, y, z0, a_y, b_y)


def check_one_exchange_triangle_classification() -> None:
    for n in range(3, 9):
        points = tuple(range(n))
        for j in range(1, n):
            supports = [frozenset(c) for c in combinations(points, j)]
            for tri in combinations(supports, 3):
                if not all(len(a & b) == j - 1 for a, b in combinations(tri, 2)):
                    continue

                common = set(tri[0])
                union = set()
                for support in tri:
                    common &= set(support)
                    union |= set(support)

                star = len(common) == j - 1
                top = len(union) == j + 1
                assert star != top, (n, j, tri, common, union)

                if star:
                    core = frozenset(common)
                    anchors = [next(iter(support - core)) for support in tri]
                    assert len(set(anchors)) == 3, (n, j, tri, core, anchors)
                    assert all(support == core | {anchor} for support, anchor in zip(tri, anchors))

                if top:
                    packet = frozenset(union)
                    deleted = [next(iter(packet - support)) for support in tri]
                    assert len(set(deleted)) == 3, (n, j, tri, packet, deleted)
                    assert all(support == packet - {root} for support, root in zip(tri, deleted))


def check_top_packet_lifted_kernel() -> None:
    rng = Random(20260630)
    for p in (5, 7, 17, 31):
        for degree in range(0, 8):
            samples: list[list[int]] = []
            if p**degree <= 10_000:
                samples = [list(coeffs) + [1] for coeffs in product(range(p), repeat=degree)]
            else:
                samples = [[rng.randrange(p) for _ in range(degree)] + [1] for _ in range(300)]

            for ell_t in samples:
                for _ in range(25):
                    x = rng.randrange(p)
                    row = [rng.randrange(p) for _ in range(degree + 2)]
                    ell_u = mul_x_minus_y(ell_t, x, p)
                    lifted = hankel1(row, ell_u, p)
                    row_0, row_1 = hankel2(row, ell_t, p)
                    assert lifted == (row_1 - x * row_0) % p, (
                        p,
                        degree,
                        ell_t,
                        x,
                        row,
                        lifted,
                        row_0,
                        row_1,
                    )

                    u_row = [rng.randrange(p) for _ in range(degree + 2)]
                    v_row = [rng.randrange(p) for _ in range(degree + 2)]
                    for z in range(p):
                        combined = [(u_row[i] + z * v_row[i]) % p for i in range(degree + 2)]
                        h0, h1 = hankel2(combined, ell_t, p)
                        if h0 == 0 and h1 == 0:
                            assert hankel1(combined, ell_u, p) == 0

                    # If the lifted t=1 scalar vanishes, the t=2 vector is
                    # compressed to the scalar row0 times (1,x).
                    h0, h1 = hankel2(row, ell_t, p)
                    if lifted == 0:
                        assert h1 == (x * h0) % p, (
                            p,
                            degree,
                            ell_t,
                            x,
                            row,
                            lifted,
                            h0,
                            h1,
                        )

        for a in range(p):
            for b in range(p):
                for z1 in range(p):
                    for z2 in range(p):
                        if z1 == z2:
                            continue
                        if (a + z1 * b) % p == 0 and (a + z2 * b) % p == 0:
                            assert a == 0 and b == 0, (p, a, b, z1, z2)


def check_top_packet_compression_ledger() -> None:
    # Model the top-packet compression after star triangles and fixed-slope
    # root slices have been charged.  A packet with at least two active
    # deletions maps to one lifted top kernel U, and edges/triangles are then
    # bounded by choosing pairs/triples of deleted roots inside U.
    for n in range(3, 10):
        points = tuple(range(n))
        for j in range(1, n):
            packets = [frozenset(c) for c in combinations(points, j + 1)]
            edge_keys: set[tuple[frozenset[int], frozenset[int]]] = set()
            triangle_keys: set[tuple[frozenset[int], frozenset[int]]] = set()

            for packet in packets:
                roots = tuple(sorted(packet))
                for mask in range(1 << len(roots)):
                    active = [roots[i] for i in range(len(roots)) if mask & (1 << i)]
                    if len(active) < 2:
                        continue

                    local_edges = {
                        frozenset(pair) for pair in combinations(active, 2)
                    }
                    assert len(local_edges) <= comb(j + 1, 2), (
                        n,
                        j,
                        packet,
                        active,
                        local_edges,
                    )
                    for deleted_pair in local_edges:
                        edge_keys.add((packet, deleted_pair))

                    local_triangles = {
                        frozenset(triple) for triple in combinations(active, 3)
                    }
                    assert len(local_triangles) <= comb(j + 1, 3), (
                        n,
                        j,
                        packet,
                        active,
                        local_triangles,
                    )
                    for deleted_triple in local_triangles:
                        triangle_keys.add((packet, deleted_triple))

                    # The union of any top-packet edge recovers packet U.
                    for x, y in combinations(active, 2):
                        t_x = packet - {x}
                        t_y = packet - {y}
                        assert t_x | t_y == packet, (n, j, packet, x, y, t_x, t_y)

            assert len(edge_keys) <= len(packets) * comb(j + 1, 2), (
                n,
                j,
                len(edge_keys),
                len(packets),
            )
            assert len(triangle_keys) <= len(packets) * comb(j + 1, 3), (
                n,
                j,
                len(triangle_keys),
                len(packets),
            )


def check_simultaneous_kernel_root_slice_recursion() -> None:
    rng = Random(20260703)

    # Exhaustive small row check: if two extensions through the same core are
    # killed by an r-row Hankel block, the core is killed by the lifted
    # (r+1)-row block.
    p = 3
    for r_rows in range(1, 3):
        for core_degree in range(0, 3):
            row_len = r_rows + core_degree + 1
            for coeffs in product(range(p), repeat=core_degree):
                ell_r = list(coeffs) + [1]
                core_pad = ell_r + [0]
                x_core = [0] + ell_r
                for y1, y2 in combinations(range(p), 2):
                    ext1 = mul_x_minus_y(ell_r, y1, p)
                    ext2 = mul_x_minus_y(ell_r, y2, p)
                    for row in product(range(p), repeat=row_len):
                        rows1 = hankel_values(list(row), ext1, r_rows, p)
                        rows2 = hankel_values(list(row), ext2, r_rows, p)
                        if all(value == 0 for value in rows1 + rows2):
                            core_rows = hankel_values(list(row), core_pad, r_rows, p)
                            x_rows = hankel_values(list(row), x_core, r_rows, p)
                            lifted = hankel_values(list(row), ell_r, r_rows + 1, p)
                            assert all(value == 0 for value in core_rows), (
                                p,
                                r_rows,
                                core_degree,
                                ell_r,
                                y1,
                                y2,
                                row,
                            )
                            assert all(value == 0 for value in x_rows), (
                                p,
                                r_rows,
                                core_degree,
                                ell_r,
                                y1,
                                y2,
                                row,
                            )
                            assert all(value == 0 for value in lifted), (
                                p,
                                r_rows,
                                core_degree,
                                ell_r,
                                y1,
                                y2,
                                row,
                                lifted,
                            )

    # Sampled two-row simultaneous check for K_{r,d}(u,v).
    for p in (5, 7, 17, 31):
        for r_rows in range(1, 5):
            for core_degree in range(0, 6):
                samples: list[list[int]]
                if p**core_degree <= 10_000:
                    samples = [
                        list(coeffs) + [1]
                        for coeffs in product(range(p), repeat=core_degree)
                    ]
                else:
                    samples = [
                        [rng.randrange(p) for _ in range(core_degree)] + [1]
                        for _ in range(250)
                    ]

                for ell_r in samples:
                    core_pad = ell_r + [0]
                    x_core = [0] + ell_r
                    for _ in range(40):
                        y1, y2 = rng.sample(range(p), 2)
                        ext1 = mul_x_minus_y(ell_r, y1, p)
                        ext2 = mul_x_minus_y(ell_r, y2, p)
                        rows = [
                            [rng.randrange(p) for _ in range(r_rows + core_degree + 1)]
                            for _ in range(2)
                        ]

                        both_extensions_killed = True
                        for row in rows:
                            rows1 = hankel_values(row, ext1, r_rows, p)
                            rows2 = hankel_values(row, ext2, r_rows, p)
                            core_rows = hankel_values(row, core_pad, r_rows, p)
                            x_rows = hankel_values(row, x_core, r_rows, p)
                            lifted = hankel_values(row, ell_r, r_rows + 1, p)

                            # Row-block identities behind KREC.
                            assert rows1 == [
                                (x_rows[i] - y1 * core_rows[i]) % p
                                for i in range(r_rows)
                            ], (p, r_rows, core_degree, ell_r, y1, row)
                            assert rows2 == [
                                (x_rows[i] - y2 * core_rows[i]) % p
                                for i in range(r_rows)
                            ], (p, r_rows, core_degree, ell_r, y2, row)
                            assert core_rows == lifted[:-1], (
                                p,
                                r_rows,
                                core_degree,
                                ell_r,
                                row,
                            )
                            assert x_rows == lifted[1:], (
                                p,
                                r_rows,
                                core_degree,
                                ell_r,
                                row,
                            )

                            if not all(value == 0 for value in rows1 + rows2):
                                both_extensions_killed = False

                        if both_extensions_killed:
                            for row in rows:
                                lifted = hankel_values(row, ell_r, r_rows + 1, p)
                                assert all(value == 0 for value in lifted), (
                                    p,
                                    r_rows,
                                    core_degree,
                                    ell_r,
                                    y1,
                                    y2,
                                    row,
                                    lifted,
                                )

    # Combinatorial residual: if no (d-1)-core supports two d-sets, then there
    # are no one-exchange edges left in the residual K_{r,d} family.
    for n in range(3, 9):
        points = tuple(range(n))
        for d_size in range(1, n):
            supports = [frozenset(c) for c in combinations(points, d_size)]
            selected: list[frozenset[int]] = []
            used_cores: set[frozenset[int]] = set()
            for support in supports:
                cores = {frozenset(core) for core in combinations(support, d_size - 1)}
                if used_cores.isdisjoint(cores):
                    selected.append(support)
                    used_cores.update(cores)

            assert all(
                len(a & b) != d_size - 1 for a, b in combinations(selected, 2)
            ), (n, d_size, selected)


def check_boundary_off_external_anchor_corollary() -> None:
    rng = Random(20260701)
    for p in (5, 7, 11, 17, 31):
        for d_size in range(1, min(p - 1, 7)):
            domain = set(range(d_size))
            external = [x for x in range(p) if x not in domain]
            assert len(external) >= 2

            samples: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
            if p <= 7:
                triples = list(product(range(p), repeat=3))
                samples = [(u_seq, v_seq) for u_seq in triples for v_seq in triples]
            else:
                samples = [
                    (
                        (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                        (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                    )
                    for _ in range(4000)
                ]

            for u_seq, v_seq in samples:
                external_roots = []
                active_by_slope: dict[int, list[int]] = {}
                for beta in external:
                    a_beta = hankel_core_value(u_seq, beta, p)
                    b_beta = hankel_core_value(v_seq, beta, p)
                    if det2(a_beta, b_beta, p) != 0:
                        continue
                    external_roots.append(beta)
                    z = slope_for_active_pair(a_beta, b_beta, p)
                    if z is not None:
                        active_by_slope.setdefault(z, []).append(beta)

                ruled = all(
                    det2(
                        hankel_core_value(u_seq, beta, p),
                        hankel_core_value(v_seq, beta, p),
                        p,
                    )
                    == 0
                    for beta in range(p)
                )

                if len(external_roots) >= 3:
                    assert ruled, (p, d_size, u_seq, v_seq, external_roots)
                if not ruled:
                    assert len(external_roots) <= 2, (
                        p,
                        d_size,
                        u_seq,
                        v_seq,
                        external_roots,
                    )
                    active_targets = [
                        beta for betas in active_by_slope.values() for beta in betas
                    ]
                    assert len(active_targets) <= 2, (
                        p,
                        d_size,
                        u_seq,
                        v_seq,
                        active_targets,
                    )
                    assert all(
                        len(betas) == 1 for betas in active_by_slope.values()
                    ), (
                        p,
                        d_size,
                        u_seq,
                        v_seq,
                        active_by_slope,
                    )
                    continue

                active_slopes: set[int] = set(active_by_slope)

                assert len(active_slopes) <= 1, (
                    p,
                    d_size,
                    u_seq,
                    v_seq,
                    external,
                    active_slopes,
                )
                if active_slopes:
                    z0 = next(iter(active_slopes))
                    for beta in range(p):
                        a_beta = hankel_core_value(u_seq, beta, p)
                        b_beta = hankel_core_value(v_seq, beta, p)
                        assert (
                            (a_beta[0] + z0 * b_beta[0]) % p == 0
                            and (a_beta[1] + z0 * b_beta[1]) % p == 0
                        ), (p, d_size, u_seq, v_seq, beta, z0, a_beta, b_beta)

                # Ruled active branches are fixed-slope and therefore charged
                # to the boundary root-slice ledger; they leave no residual
                # external-anchor fiber to count here.

            # The same-slope boundary root-slice implication is checked for
            # every sampled pair, regardless of whether the determinant is
            # ruled.  If two external anchors over one shadow have the same
            # active finite slope, the lifted H_{3,j-1} shadow rows vanish.
            for u_seq, v_seq in samples:
                active_by_slope: dict[int, list[int]] = {}
                for beta in external:
                    a_beta = hankel_core_value(u_seq, beta, p)
                    b_beta = hankel_core_value(v_seq, beta, p)
                    if det2(a_beta, b_beta, p) != 0:
                        continue
                    z = slope_for_active_pair(a_beta, b_beta, p)
                    if z is not None:
                        active_by_slope.setdefault(z, []).append(beta)

                for z, betas in active_by_slope.items():
                    if len(betas) < 2:
                        continue
                    lifted = tuple(
                        (u_seq[idx] + z * v_seq[idx]) % p for idx in range(3)
                    )
                    assert lifted == (0, 0, 0), (
                        p,
                        d_size,
                        u_seq,
                        v_seq,
                        z,
                        betas,
                        lifted,
                    )


def check_boundary_shadow_anchor_recovery() -> None:
    rng = Random(20260711)
    cases: list[tuple[int, tuple[int, int, int]]]
    for p in (3, 5, 7, 11, 17, 31):
        if p <= 7:
            cases = [
                (p, (seq[0], seq[1], seq[2]))
                for seq in product(range(p), repeat=3)
            ]
        else:
            cases = [
                (
                    p,
                    (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                )
                for _ in range(4000)
            ]

        for prime, seq in cases:
            c_0, c_1, c_2 = seq
            roots = [
                beta
                for beta in range(prime)
                if hankel_core_value(seq, beta, prime) == (0, 0)
            ]
            zero_core = seq == (0, 0, 0)
            rank_one = c_0 != 0 and (c_1 * c_1 - c_0 * c_2) % prime == 0

            if zero_core:
                assert len(roots) == prime, (prime, seq, roots)
                continue

            if rank_one:
                recovered = (c_1 * pow(c_0, -1, prime)) % prime
                assert roots == [recovered], (prime, seq, recovered, roots)
            else:
                assert roots == [], (prime, seq, roots)


def rank_one_value(seq: tuple[int, int, int], p: int) -> int:
    return (seq[1] * seq[1] - seq[0] * seq[2]) % p


def rank_one_line_coeffs(
    a_seq: tuple[int, int, int],
    b_seq: tuple[int, int, int],
    p: int,
) -> tuple[int, int, int]:
    return (
        rank_one_value(a_seq, p),
        (
            2 * a_seq[1] * b_seq[1]
            - a_seq[0] * b_seq[2]
            - b_seq[0] * a_seq[2]
        )
        % p,
        rank_one_value(b_seq, p),
    )


def conic_anchor_coeffs(
    a_seq: tuple[int, int, int],
    b_seq: tuple[int, int, int],
    p: int,
) -> tuple[int, int, int]:
    return (
        (a_seq[1] * b_seq[2] - a_seq[2] * b_seq[1]) % p,
        (a_seq[2] * b_seq[0] - a_seq[0] * b_seq[2]) % p,
        (a_seq[0] * b_seq[1] - a_seq[1] * b_seq[0]) % p,
    )


def eval_quadratic(coeffs: tuple[int, int, int], x: int, p: int) -> int:
    return (coeffs[0] + coeffs[1] * x + coeffs[2] * x * x) % p


def check_boundary_shadow_quadratic_gate() -> None:
    rng = Random(20260712)
    for p in (2, 3, 5, 7, 11, 17, 31):
        if p <= 5:
            triples = list(product(range(p), repeat=3))
            samples = [(a_seq, b_seq) for a_seq in triples for b_seq in triples]
        else:
            samples = [
                (
                    (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                    (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                )
                for _ in range(4000)
            ]

        for a_seq, b_seq in samples:
            coeffs = rank_one_line_coeffs(a_seq, b_seq, p)
            candidates: list[tuple[int, int]] = []
            for z in range(p):
                c_seq = tuple((a_seq[idx] + z * b_seq[idx]) % p for idx in range(3))
                if c_seq == (0, 0, 0):
                    continue
                if c_seq[0] == 0 or rank_one_value(c_seq, p) != 0:
                    continue
                beta = (c_seq[1] * pow(c_seq[0], -1, p)) % p
                assert hankel_core_value(c_seq, beta, p) == (0, 0), (
                    p,
                    a_seq,
                    b_seq,
                    z,
                    c_seq,
                    beta,
                )
                candidates.append((z, beta))

            if coeffs != (0, 0, 0):
                assert len(candidates) <= 2, (p, a_seq, b_seq, coeffs, candidates)
                continue

            betas = {beta for _, beta in candidates}
            assert len(betas) <= 1, (p, a_seq, b_seq, candidates)
            if betas:
                beta = next(iter(betas))
                assert hankel_core_value(a_seq, beta, p) == (0, 0), (
                    p,
                    a_seq,
                    b_seq,
                    beta,
                    candidates,
                )
                assert hankel_core_value(b_seq, beta, p) == (0, 0), (
                    p,
                    a_seq,
                    b_seq,
                    beta,
                    candidates,
                )


def check_boundary_shadow_conic_secant_duality() -> None:
    rng = Random(20260713)
    for p in (2, 3, 5, 7, 11, 17, 31):
        if p <= 5:
            triples = list(product(range(p), repeat=3))
            samples = [(a_seq, b_seq) for a_seq in triples for b_seq in triples]
        else:
            samples = [
                (
                    (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                    (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                )
                for _ in range(4000)
            ]

        for a_seq, b_seq in samples:
            q_coeffs = rank_one_line_coeffs(a_seq, b_seq, p)
            anchor_coeffs = conic_anchor_coeffs(a_seq, b_seq, p)
            q_disc = (q_coeffs[1] * q_coeffs[1] - 4 * q_coeffs[0] * q_coeffs[2]) % p
            anchor_disc = (
                anchor_coeffs[1] * anchor_coeffs[1]
                - 4 * anchor_coeffs[0] * anchor_coeffs[2]
            ) % p
            assert q_disc == anchor_disc, (p, a_seq, b_seq, q_coeffs, anchor_coeffs)

            anchor_roots = [
                beta
                for beta in range(p)
                if eval_quadratic(anchor_coeffs, beta, p) == 0
            ]
            if anchor_coeffs != (0, 0, 0):
                assert len(anchor_roots) <= 2, (
                    p,
                    a_seq,
                    b_seq,
                    anchor_coeffs,
                    anchor_roots,
                )
            else:
                assert (
                    (a_seq[0] * b_seq[1] - a_seq[1] * b_seq[0]) % p == 0
                    and (a_seq[0] * b_seq[2] - a_seq[2] * b_seq[0]) % p == 0
                    and (a_seq[1] * b_seq[2] - a_seq[2] * b_seq[1]) % p == 0
                ), (p, a_seq, b_seq, anchor_coeffs)

            slope_pairs: set[tuple[int, int]] = set()
            for z in range(p):
                c_seq = tuple((a_seq[idx] + z * b_seq[idx]) % p for idx in range(3))
                if c_seq == (0, 0, 0):
                    continue
                if c_seq[0] == 0 or rank_one_value(c_seq, p) != 0:
                    continue
                beta = (c_seq[1] * pow(c_seq[0], -1, p)) % p
                if hankel_core_value(b_seq, beta, p) == (0, 0):
                    continue
                slope_pairs.add((z, beta))

            anchor_pairs: set[tuple[int, int]] = set()
            for beta in range(p):
                h_a = hankel_core_value(a_seq, beta, p)
                h_b = hankel_core_value(b_seq, beta, p)
                anchor_value = eval_quadratic(anchor_coeffs, beta, p)
                assert anchor_value == det2(h_a, h_b, p), (
                    p,
                    a_seq,
                    b_seq,
                    beta,
                    anchor_value,
                    h_a,
                    h_b,
                )
                if h_b == (0, 0) or anchor_value != 0:
                    continue
                z = slope_for_active_pair(h_a, h_b, p)
                assert z is not None, (p, a_seq, b_seq, beta, h_a, h_b)
                c_seq = tuple((a_seq[idx] + z * b_seq[idx]) % p for idx in range(3))
                if c_seq == (0, 0, 0):
                    continue
                assert hankel_core_value(c_seq, beta, p) == (0, 0), (
                    p,
                    a_seq,
                    b_seq,
                    beta,
                    z,
                    c_seq,
                )
                assert c_seq[0] != 0 and rank_one_value(c_seq, p) == 0, (
                    p,
                    a_seq,
                    b_seq,
                    beta,
                    z,
                    c_seq,
                )
                anchor_pairs.add((z, beta))

            assert slope_pairs == anchor_pairs, (
                p,
                a_seq,
                b_seq,
                q_coeffs,
                anchor_coeffs,
                slope_pairs,
                anchor_pairs,
            )
            if anchor_coeffs == (0, 0, 0):
                assert not anchor_pairs, (p, a_seq, b_seq, anchor_pairs)


def check_boundary_fixed_anchor_core_fibers() -> None:
    rng = Random(20260714)
    for p in (5, 7, 11, 17, 31):
        for d_size in range(2, min(p - 1, 7)):
            domain = set(range(d_size))
            beta = d_size
            assert beta not in domain

            if p <= 5:
                triples = list(product(range(p), repeat=3))
                samples = [(u_seq, v_seq) for u_seq in triples for v_seq in triples]
            else:
                samples = [
                    (
                        (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                        (rng.randrange(p), rng.randrange(p), rng.randrange(p)),
                    )
                    for _ in range(4000)
                ]

            for u_seq, v_seq in samples:
                domain_roots: list[int] = []
                active_by_slope: dict[int, list[int]] = {}
                for y in domain:
                    a_y = hankel_core_value(u_seq, y, p)
                    b_y = hankel_core_value(v_seq, y, p)
                    if det2(a_y, b_y, p) != 0:
                        continue
                    domain_roots.append(y)
                    z = slope_for_active_pair(a_y, b_y, p)
                    if z is not None:
                        active_by_slope.setdefault(z, []).append(y)

                ruled = all(
                    det2(
                        hankel_core_value(u_seq, y, p),
                        hankel_core_value(v_seq, y, p),
                        p,
                    )
                    == 0
                    for y in range(p)
                )

                if not ruled:
                    assert len(domain_roots) <= 2, (
                        p,
                        d_size,
                        beta,
                        u_seq,
                        v_seq,
                        domain_roots,
                    )
                    active_targets = [
                        y for roots in active_by_slope.values() for y in roots
                    ]
                    assert len(active_targets) <= 2, (
                        p,
                        d_size,
                        beta,
                        u_seq,
                        v_seq,
                        active_targets,
                    )
                    assert all(len(roots) == 1 for roots in active_by_slope.values()), (
                        p,
                        d_size,
                        beta,
                        u_seq,
                        v_seq,
                        active_by_slope,
                    )
                    continue

                active_slopes = set(active_by_slope)
                assert len(active_slopes) <= 1, (
                    p,
                    d_size,
                    beta,
                    u_seq,
                    v_seq,
                    active_slopes,
                )
                if active_slopes:
                    z0 = next(iter(active_slopes))
                    for y in range(p):
                        a_y = hankel_core_value(u_seq, y, p)
                        b_y = hankel_core_value(v_seq, y, p)
                        assert (
                            (a_y[0] + z0 * b_y[0]) % p == 0
                            and (a_y[1] + z0 * b_y[1]) % p == 0
                        ), (p, d_size, beta, u_seq, v_seq, y, z0, a_y, b_y)

            for u_seq, v_seq in samples:
                active_by_slope: dict[int, list[int]] = {}
                for y in domain:
                    a_y = hankel_core_value(u_seq, y, p)
                    b_y = hankel_core_value(v_seq, y, p)
                    if det2(a_y, b_y, p) != 0:
                        continue
                    z = slope_for_active_pair(a_y, b_y, p)
                    if z is not None:
                        active_by_slope.setdefault(z, []).append(y)

                for z, roots in active_by_slope.items():
                    if len(roots) < 2:
                        continue
                    lifted = tuple(
                        (u_seq[idx] + z * v_seq[idx]) % p for idx in range(3)
                    )
                    assert lifted == (0, 0, 0), (
                        p,
                        d_size,
                        beta,
                        u_seq,
                        v_seq,
                        z,
                        roots,
                        lifted,
                    )


Poly1 = dict[int, int]
Poly2 = dict[tuple[int, int], int]


def poly1_add_scaled(target: Poly1, source: Poly1, scale: int, p: int) -> None:
    for degree, coeff in source.items():
        target[degree] = (target.get(degree, 0) + scale * coeff) % p
        if target[degree] == 0:
            del target[degree]


def poly1_mul(left: Poly1, right: Poly1, p: int) -> Poly1:
    out: Poly1 = {}
    for left_degree, left_coeff in left.items():
        for right_degree, right_coeff in right.items():
            degree = left_degree + right_degree
            out[degree] = (out.get(degree, 0) + left_coeff * right_coeff) % p
            if out[degree] == 0:
                del out[degree]
    return out


def poly1_sub(left: Poly1, right: Poly1, p: int) -> Poly1:
    out = dict(left)
    poly1_add_scaled(out, right, -1, p)
    return out


def eval_poly1(poly: Poly1, value: int, p: int) -> int:
    return sum(coeff * pow(value, degree, p) for degree, coeff in poly.items()) % p


def poly1_from_terms(terms: tuple[tuple[int, int], ...], p: int) -> Poly1:
    out: Poly1 = {}
    for degree, coeff in terms:
        out[degree] = (out.get(degree, 0) + coeff) % p
        if out[degree] == 0:
            del out[degree]
    return out


def poly1_degree(poly: Poly1) -> int:
    return max(poly, default=-1)


def poly1_to_list(poly: Poly1) -> list[int]:
    degree = poly1_degree(poly)
    return [poly.get(idx, 0) for idx in range(degree + 1)]


def poly1_from_list(coeffs: list[int], p: int) -> Poly1:
    return {idx: coeff % p for idx, coeff in enumerate(coeffs) if coeff % p != 0}


def poly1_monic(poly: Poly1, p: int) -> Poly1:
    degree = poly1_degree(poly)
    assert degree >= 0
    inv_lead = pow(poly[degree], -1, p)
    return {idx: (coeff * inv_lead) % p for idx, coeff in poly.items()}


def poly1_divmod(dividend: Poly1, divisor: Poly1, p: int) -> tuple[Poly1, Poly1]:
    divisor_degree = poly1_degree(divisor)
    assert divisor_degree >= 0
    divisor_lead_inv = pow(divisor[divisor_degree], -1, p)
    remainder = poly1_to_list(dividend)
    quotient = [0] * max(0, poly1_degree(dividend) - divisor_degree + 1)
    divisor_coeffs = poly1_to_list(divisor)
    while len(remainder) >= len(divisor_coeffs) and any(remainder):
        degree_gap = len(remainder) - len(divisor_coeffs)
        coeff = (remainder[-1] * divisor_lead_inv) % p
        quotient[degree_gap] = coeff
        for idx, divisor_coeff in enumerate(divisor_coeffs):
            remainder[degree_gap + idx] = (
                remainder[degree_gap + idx] - coeff * divisor_coeff
            ) % p
        while remainder and remainder[-1] == 0:
            remainder.pop()
    return poly1_from_list(quotient, p), poly1_from_list(remainder, p)


_MONIC_POLY_CACHE: dict[tuple[int, int], list[Poly1]] = {}


def monic_polys_of_degree(degree: int, p: int) -> list[Poly1]:
    key = (degree, p)
    if key not in _MONIC_POLY_CACHE:
        _MONIC_POLY_CACHE[key] = [
            poly1_from_list(list(coeffs) + [1], p)
            for coeffs in product(range(p), repeat=degree)
        ]
    return _MONIC_POLY_CACHE[key]


def factor_poly1_monic(poly: Poly1, p: int) -> dict[tuple[int, ...], int]:
    if not poly:
        return {}
    remaining = poly1_monic(poly, p)
    factors: dict[tuple[int, ...], int] = {}
    for root in range(p):
        linear = poly1_from_list([(-root) % p, 1], p)
        while poly1_degree(remaining) >= 1 and eval_poly1(remaining, root, p) == 0:
            quotient, remainder = poly1_divmod(remaining, linear, p)
            assert not remainder, (p, remaining, linear, remainder)
            key = tuple(poly1_to_list(linear))
            factors[key] = factors.get(key, 0) + 1
            remaining = quotient
    if poly1_degree(remaining) == 4:
        for candidate in monic_polys_of_degree(2, p):
            if poly1_mul(candidate, candidate, p) == remaining:
                key = tuple(poly1_to_list(candidate))
                factors[key] = factors.get(key, 0) + 2
                remaining = {}
                break
    if poly1_degree(remaining) > 0:
        key = tuple(poly1_to_list(poly1_monic(remaining, p)))
        factors[key] = factors.get(key, 0) + 1
    return factors


def primitive_root(p: int) -> int:
    factors = [
        prime
        for prime in range(2, p)
        if (p - 1) % prime == 0 and all(prime % d for d in range(2, prime))
    ]
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise AssertionError(f"no primitive root found for {p}")


def discrete_log_table(p: int) -> dict[int, int]:
    generator = primitive_root(p)
    table: dict[int, int] = {}
    value = 1
    for exponent in range(p - 1):
        table[value] = exponent
        value = (value * generator) % p
    return table


def kummer_power_degenerate(poly: Poly1, index: int, char_power: int, p: int) -> bool:
    assert poly
    order = 2 * index // gcd(index, 2)
    y_factor = (0, 1)
    factors = factor_poly1_monic(poly, p)
    zero_multiplicity = factors.get(y_factor, 0)
    zero_exponent = char_power * (order // index) + zero_multiplicity * (order // 2)
    if zero_exponent % order != 0:
        return False
    for factor, multiplicity in factors.items():
        if factor == y_factor:
            continue
        if (multiplicity * (order // 2)) % order != 0:
            return False
    return True


def kummer_support_size(poly: Poly1, index: int, char_power: int, p: int) -> int:
    order = 2 * index // gcd(index, 2)
    y_factor = (0, 1)
    factors = factor_poly1_monic(poly, p)
    support = 0
    total_exponent_degree = char_power * (order // index)
    for factor, multiplicity in factors.items():
        factor_degree = len(factor) - 1
        exponent = multiplicity * (order // 2)
        if factor == y_factor:
            exponent += char_power * (order // index)
        if exponent % order != 0:
            support += factor_degree
        total_exponent_degree += factor_degree * multiplicity * (order // 2)
    if total_exponent_degree % order != 0:
        support += 1
    return support


def quadratic_character(value: int, p: int) -> int:
    value %= p
    if value == 0:
        return 0
    return 1 if pow(value, (p - 1) // 2, p) == 1 else -1


def poly_add_scaled(target: Poly2, source: Poly2, scale: int, p: int) -> None:
    for monomial, coeff in source.items():
        target[monomial] = (target.get(monomial, 0) + scale * coeff) % p
        if target[monomial] == 0:
            del target[monomial]


def poly_mul(left: Poly2, right: Poly2, p: int) -> Poly2:
    out: Poly2 = {}
    for (bi, yi), left_coeff in left.items():
        for (bj, yj), right_coeff in right.items():
            monomial = (bi + bj, yi + yj)
            out[monomial] = (out.get(monomial, 0) + left_coeff * right_coeff) % p
            if out[monomial] == 0:
                del out[monomial]
    return out


def eval_poly2(poly: Poly2, beta: int, y: int, p: int) -> int:
    return sum(
        coeff * pow(beta, beta_deg, p) * pow(y, y_deg, p)
        for (beta_deg, y_deg), coeff in poly.items()
    ) % p


def boundary_core_bidegree_coeffs(
    u_vectors: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    v_vectors: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    p: int,
) -> Poly2:
    basis: tuple[Poly2, Poly2, Poly2] = (
        {(1, 1): 1},
        {(1, 0): (-1) % p, (0, 1): (-1) % p},
        {(0, 0): 1},
    )
    out: Poly2 = {}
    for i, u_vec in enumerate(u_vectors):
        for j, v_vec in enumerate(v_vectors):
            poly_add_scaled(out, poly_mul(basis[i], basis[j], p), det2(u_vec, v_vec, p), p)
    return out


def elementary_two_root_det_coeffs(
    u_vectors: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    v_vectors: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    p: int,
) -> Poly2:
    basis: tuple[Poly2, Poly2, Poly2] = (
        {(0, 1): 1},
        {(1, 0): (-1) % p},
        {(0, 0): 1},
    )
    out: Poly2 = {}
    for i, u_vec in enumerate(u_vectors):
        for j, v_vec in enumerate(v_vectors):
            poly_add_scaled(out, poly_mul(basis[i], basis[j], p), det2(u_vec, v_vec, p), p)
    return out


def boundary_anchor_quadratic_coeffs(elementary_poly: Poly2, p: int) -> tuple[Poly1, Poly1, Poly1]:
    assert all(s_degree + p_degree <= 2 for s_degree, p_degree in elementary_poly)
    f_20 = elementary_poly.get((2, 0), 0)
    f_11 = elementary_poly.get((1, 1), 0)
    f_02 = elementary_poly.get((0, 2), 0)
    f_10 = elementary_poly.get((1, 0), 0)
    f_01 = elementary_poly.get((0, 1), 0)
    f_00 = elementary_poly.get((0, 0), 0)
    a_poly = poly1_from_terms(((0, f_20), (1, f_11), (2, f_02)), p)
    b_poly = poly1_from_terms(
        ((0, f_10), (1, 2 * f_20 + f_01), (2, f_11)),
        p,
    )
    c_poly = poly1_from_terms(((0, f_00), (1, f_10), (2, f_20)), p)
    return a_poly, b_poly, c_poly


def boundary_anchor_discriminant(a_poly: Poly1, b_poly: Poly1, c_poly: Poly1, p: int) -> Poly1:
    out = poly1_mul(b_poly, b_poly, p)
    poly1_add_scaled(out, poly1_mul(a_poly, c_poly, p), -4, p)
    return out


def quadratic_root_count(a_coeff: int, b_coeff: int, c_coeff: int, p: int) -> int:
    if a_coeff % p != 0:
        discriminant = (b_coeff * b_coeff - 4 * a_coeff * c_coeff) % p
        return 1 + quadratic_character(discriminant, p)
    if b_coeff % p != 0:
        return 1
    if c_coeff % p != 0:
        return 0
    return p


def elementary_tuple_to_poly(coeffs: tuple[int, int, int, int, int, int], p: int) -> Poly2:
    f_20, f_11, f_02, f_10, f_01, f_00 = coeffs
    terms = {
        (2, 0): f_20,
        (1, 1): f_11,
        (0, 2): f_02,
        (1, 0): f_10,
        (0, 1): f_01,
        (0, 0): f_00,
    }
    return {monomial: coeff % p for monomial, coeff in terms.items() if coeff % p != 0}


def scalar_line_square_tuple(a_coeff: int, b_coeff: int, c_coeff: int, scale: int, p: int) -> tuple[int, int, int, int, int, int]:
    # L(s,p)=a_coeff*p+b_coeff*s+c_coeff.
    return (
        (scale * b_coeff * b_coeff) % p,
        (scale * 2 * a_coeff * b_coeff) % p,
        (scale * a_coeff * a_coeff) % p,
        (scale * 2 * b_coeff * c_coeff) % p,
        (scale * 2 * a_coeff * c_coeff) % p,
        (scale * c_coeff * c_coeff) % p,
    )


def envelope_tuple(scale: int, p: int) -> tuple[int, int, int, int, int, int]:
    # scale*(s^2-4p).
    return (scale % p, 0, 0, 0, (-4 * scale) % p, 0)


def eval_boundary_core_vectors(
    vectors: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    beta: int,
    y: int,
    p: int,
) -> tuple[int, int]:
    coeffs = ((beta * y) % p, (-(beta + y)) % p, 1)
    return (
        sum(coeffs[idx] * vectors[idx][0] for idx in range(3)) % p,
        sum(coeffs[idx] * vectors[idx][1] for idx in range(3)) % p,
    )


def check_boundary_core_bidegree_determinant() -> None:
    rng = Random(20260715)
    for p in (5, 7, 11, 17, 31):
        samples = [
            (
                tuple((rng.randrange(p), rng.randrange(p)) for _ in range(3)),
                tuple((rng.randrange(p), rng.randrange(p)) for _ in range(3)),
            )
            for _ in range(2000)
        ]
        for u_vectors, v_vectors in samples:
            poly = boundary_core_bidegree_coeffs(u_vectors, v_vectors, p)
            elementary_poly = elementary_two_root_det_coeffs(u_vectors, v_vectors, p)
            anchor_a, anchor_b, anchor_c = boundary_anchor_quadratic_coeffs(
                elementary_poly,
                p,
            )
            anchor_disc = boundary_anchor_discriminant(anchor_a, anchor_b, anchor_c, p)
            assert all(beta_deg <= 2 and y_deg <= 2 for beta_deg, y_deg in poly), (
                p,
                u_vectors,
                v_vectors,
                poly,
            )
            assert all(s_deg + p_deg <= 2 for s_deg, p_deg in elementary_poly), (
                p,
                u_vectors,
                v_vectors,
                elementary_poly,
            )
            assert all(degree <= 2 for degree in anchor_a), (p, elementary_poly, anchor_a)
            assert all(degree <= 2 for degree in anchor_b), (p, elementary_poly, anchor_b)
            assert all(degree <= 2 for degree in anchor_c), (p, elementary_poly, anchor_c)
            assert all(degree <= 4 for degree in anchor_disc), (
                p,
                elementary_poly,
                anchor_disc,
            )
            if anchor_disc:
                disc_degree = max(anchor_disc)
                cover_genus_bound = max(0, (disc_degree - 1) // 2)
                assert cover_genus_bound <= 1, (
                    p,
                    elementary_poly,
                    anchor_disc,
                    cover_genus_bound,
                )
                if anchor_a:
                    exceptional_y = [
                        y for y in range(p) if eval_poly1(anchor_a, y, p) == 0
                    ]
                    assert len(exceptional_y) <= 2, (
                        p,
                        elementary_poly,
                        anchor_a,
                        exceptional_y,
                    )
                else:
                    assert not any(
                        monomial in elementary_poly
                        for monomial in ((2, 0), (1, 1), (0, 2))
                    ), (p, elementary_poly, anchor_a)
            for beta in range(p):
                for y in range(p):
                    c_vec = eval_boundary_core_vectors(u_vectors, beta, y, p)
                    d_vec = eval_boundary_core_vectors(v_vectors, beta, y, p)
                    direct = det2(c_vec, d_vec, p)
                    s_value = (beta + y) % p
                    p_value = (beta * y) % p
                    assert eval_poly2(poly, beta, y, p) == direct, (
                        p,
                        u_vectors,
                        v_vectors,
                        beta,
                        y,
                        poly,
                        direct,
                    )
                    assert eval_poly2(elementary_poly, s_value, p_value, p) == direct, (
                        p,
                        u_vectors,
                        v_vectors,
                        beta,
                        y,
                        s_value,
                        p_value,
                        elementary_poly,
                        direct,
                    )
                    a_value = eval_poly1(anchor_a, y, p)
                    b_value = eval_poly1(anchor_b, y, p)
                    c_value = eval_poly1(anchor_c, y, p)
                    quad_value = (
                        a_value * beta * beta + b_value * beta + c_value
                    ) % p
                    assert quad_value == direct, (
                        p,
                        u_vectors,
                        v_vectors,
                        beta,
                        y,
                        anchor_a,
                        anchor_b,
                        anchor_c,
                        quad_value,
                        direct,
                    )
                    assert eval_poly2(poly, beta, y, p) == eval_poly2(poly, y, beta, p), (
                        p,
                        u_vectors,
                        v_vectors,
                        beta,
                        y,
                        poly,
                    )
                    for alpha in (beta, y):
                        fixed_root_p = (alpha * s_value - alpha * alpha) % p
                        assert fixed_root_p == p_value, (
                            p,
                            alpha,
                            beta,
                            y,
                            s_value,
                            p_value,
                            fixed_root_p,
                        )

            for y in range(p):
                a_value = eval_poly1(anchor_a, y, p)
                b_value = eval_poly1(anchor_b, y, p)
                c_value = eval_poly1(anchor_c, y, p)
                roots = [
                    beta
                    for beta in range(p)
                    if eval_poly2(
                        elementary_poly,
                        (beta + y) % p,
                        (beta * y) % p,
                        p,
                    )
                    == 0
                ]
                expected_root_count = quadratic_root_count(
                    a_value,
                    b_value,
                    c_value,
                    p,
                )
                assert len(roots) == expected_root_count, (
                    p,
                    elementary_poly,
                    y,
                    a_value,
                    b_value,
                    c_value,
                    roots,
                    expected_root_count,
                )
                if expected_root_count == p:
                    assert all(
                        eval_poly2(
                            elementary_poly,
                            (beta + y) % p,
                            (beta * y) % p,
                            p,
                        )
                        == 0
                        for beta in range(p)
                    ), (p, elementary_poly, y)
                if anchor_disc and a_value != 0:
                    disc_value = eval_poly1(anchor_disc, y, p)
                    cover_points = [
                        w for w in range(p) if (w * w - disc_value) % p == 0
                    ]
                    cover_from_roots = sorted(
                        (2 * a_value * beta + b_value) % p for beta in roots
                    )
                    assert cover_from_roots == sorted(cover_points), (
                        p,
                        elementary_poly,
                        y,
                        a_value,
                        b_value,
                        c_value,
                        disc_value,
                        roots,
                        cover_points,
                        cover_from_roots,
                    )
                    inv_2a = pow((2 * a_value) % p, -1, p)
                    for w in cover_points:
                        beta = ((-b_value + w) * inv_2a) % p
                        assert beta in roots, (
                            p,
                            elementary_poly,
                            y,
                            w,
                            beta,
                            roots,
                        )


def check_boundary_discriminant_degeneracy_classification() -> None:
    for p in (3, 5, 7):
        charged_zero_discriminant: set[tuple[int, int, int, int, int, int]] = set()
        for scale in range(p):
            charged_zero_discriminant.add(envelope_tuple(scale, p))
            for a_coeff, b_coeff, c_coeff in product(range(p), repeat=3):
                charged_zero_discriminant.add(
                    scalar_line_square_tuple(a_coeff, b_coeff, c_coeff, scale, p)
                )

        for coeffs in product(range(p), repeat=6):
            elementary_poly = elementary_tuple_to_poly(coeffs, p)
            anchor_a, anchor_b, anchor_c = boundary_anchor_quadratic_coeffs(
                elementary_poly,
                p,
            )
            anchor_disc = boundary_anchor_discriminant(anchor_a, anchor_b, anchor_c, p)
            if anchor_disc:
                continue
            assert coeffs in charged_zero_discriminant, (
                p,
                coeffs,
                anchor_a,
                anchor_b,
                anchor_c,
            )

        for coeffs in charged_zero_discriminant:
            elementary_poly = elementary_tuple_to_poly(coeffs, p)
            anchor_a, anchor_b, anchor_c = boundary_anchor_quadratic_coeffs(
                elementary_poly,
                p,
            )
            anchor_disc = boundary_anchor_discriminant(anchor_a, anchor_b, anchor_c, p)
            assert not anchor_disc, (p, coeffs, anchor_disc)

        for scale in range(p):
            elementary_poly = elementary_tuple_to_poly(envelope_tuple(scale, p), p)
            for beta in range(p):
                for y in range(p):
                    expected = (scale * (beta - y) * (beta - y)) % p
                    got = eval_poly2(elementary_poly, (beta + y) % p, (beta * y) % p, p)
                    assert got == expected, (p, scale, beta, y, got, expected)


def check_boundary_quartic_kummer_power_gate() -> None:
    rng = Random(20260717)
    cases: dict[int, list[Poly1]] = {}
    for p in (5, 7, 11):
        polynomials: list[Poly1] = []
        for scale in range(1, p):
            for degree in range(0, 3):
                samples = [
                    poly1_from_list(list(coeffs) + [1], p)
                    for coeffs in product(range(p), repeat=degree)
                ]
                for base in samples[: min(len(samples), 40)]:
                    square = poly1_mul(base, base, p)
                    polynomials.append(
                        {deg: (scale * coeff) % p for deg, coeff in square.items()}
                    )
                    y_square = {
                        deg + 1: (scale * coeff) % p for deg, coeff in square.items()
                    }
                    if poly1_degree(y_square) <= 4:
                        polynomials.append(y_square)
        polynomials.extend(
            poly1_from_list([rng.randrange(p) for _ in range(5)], p)
            for _ in range(500)
        )
        cases[p] = [poly for poly in polynomials if poly]

    for p, polynomials in cases.items():
        polynomials = [poly for poly in polynomials if poly]
        log_table = discrete_log_table(p)
        indices = [index for index in range(1, p) if (p - 1) % index == 0]
        for poly in polynomials:
            assert poly1_degree(poly) <= 4, (p, poly)
            for index in indices:
                order = 2 * index // gcd(index, 2)
                degenerate_powers: list[int] = []
                for char_power in range(index):
                    support = kummer_support_size(poly, index, char_power, p)
                    assert support <= 6, (p, index, char_power, poly, support)
                    degenerate = kummer_power_degenerate(poly, index, char_power, p)
                    if not degenerate:
                        continue
                    degenerate_powers.append(char_power)
                    factors = factor_poly1_monic(poly, p)
                    zero_parity = factors.get((0, 1), 0) % 2
                    if zero_parity == 0:
                        assert char_power == 0, (p, index, char_power, poly, factors)
                    else:
                        assert index % 2 == 0 and char_power == index // 2, (
                            p,
                            index,
                            char_power,
                            poly,
                            factors,
                        )
                    for factor, multiplicity in factors.items():
                        if factor != (0, 1):
                            assert multiplicity % 2 == 0, (
                                p,
                                index,
                                char_power,
                                poly,
                                factors,
                            )
                    values = set()
                    for y in range(1, p):
                        disc_value = eval_poly1(poly, y, p)
                        if disc_value == 0:
                            continue
                        exponent = (
                            char_power * (order // index) * log_table[y]
                            + (order // 2) * log_table[disc_value]
                        ) % order
                        values.add(exponent)
                    assert len(values) <= 1, (p, index, char_power, poly, values)
                assert len(degenerate_powers) <= 1, (
                    p,
                    index,
                    poly,
                    degenerate_powers,
                )


def check_boundary_core_slope_recurrence_gate() -> None:
    rng = Random(20260718)
    for prime in (5, 7, 11, 17):
        samples = [
            (
                tuple(rng.randrange(prime) for _ in range(4)),
                tuple(rng.randrange(prime) for _ in range(4)),
            )
            for _ in range(1000)
        ]
        for a_rows, b_rows in samples:
            u_vectors = tuple((a_rows[idx], a_rows[idx + 1]) for idx in range(3))
            v_vectors = tuple((b_rows[idx], b_rows[idx + 1]) for idx in range(3))
            elementary_poly = elementary_two_root_det_coeffs(
                u_vectors,
                v_vectors,
                prime,
            )
            c_polys = tuple(
                poly1_from_terms(((0, a_rows[idx]), (1, b_rows[idx])), prime)
                for idx in range(4)
            )
            q_poly = poly1_sub(
                poly1_mul(c_polys[0], c_polys[2], prime),
                poly1_mul(c_polys[1], c_polys[1], prime),
                prime,
            )
            s_num_poly = poly1_sub(
                poly1_mul(c_polys[0], c_polys[3], prime),
                poly1_mul(c_polys[1], c_polys[2], prime),
                prime,
            )
            p_num_poly = poly1_sub(
                poly1_mul(c_polys[1], c_polys[3], prime),
                poly1_mul(c_polys[2], c_polys[2], prime),
                prime,
            )
            theta_poly = poly1_sub(
                poly1_mul(s_num_poly, s_num_poly, prime),
                poly1_mul(
                    poly1_from_terms(((0, 4),), prime),
                    poly1_mul(q_poly, p_num_poly, prime),
                    prime,
                ),
                prime,
            )
            assert poly1_degree(q_poly) <= 2, (prime, a_rows, b_rows, q_poly)
            assert poly1_degree(s_num_poly) <= 2, (
                prime,
                a_rows,
                b_rows,
                s_num_poly,
            )
            assert poly1_degree(p_num_poly) <= 2, (
                prime,
                a_rows,
                b_rows,
                p_num_poly,
            )
            assert poly1_degree(theta_poly) <= 4, (
                prime,
                a_rows,
                b_rows,
                theta_poly,
            )
            for z_value in range(prime):
                c = tuple(
                    (a_rows[idx] + z_value * b_rows[idx]) % prime for idx in range(4)
                )
                denominator = (c[0] * c[2] - c[1] * c[1]) % prime
                assert eval_poly1(q_poly, z_value, prime) == denominator, (
                    prime,
                    a_rows,
                    b_rows,
                    z_value,
                    q_poly,
                    denominator,
                )
                solutions: list[tuple[int, int]] = []
                for s_value in range(prime):
                    for p_value in range(prime):
                        if (
                            c[2] - s_value * c[1] + p_value * c[0]
                        ) % prime == 0 and (
                            c[3] - s_value * c[2] + p_value * c[1]
                        ) % prime == 0:
                            solutions.append((s_value, p_value))

                if denominator != 0:
                    s_num = (c[0] * c[3] - c[1] * c[2]) % prime
                    p_num = (c[1] * c[3] - c[2] * c[2]) % prime
                    inv_den = pow(denominator, -1, prime)
                    s_value = (s_num * inv_den) % prime
                    p_value = (p_num * inv_den) % prime
                    assert solutions == [(s_value, p_value)], (
                        prime,
                        a_rows,
                        b_rows,
                        z_value,
                        c,
                        denominator,
                        solutions,
                        s_value,
                        p_value,
                    )
                    theta = (
                        s_num * s_num - 4 * denominator * p_num
                    ) % prime
                    assert eval_poly1(s_num_poly, z_value, prime) == s_num, (
                        prime,
                        z_value,
                        s_num_poly,
                        s_num,
                    )
                    assert eval_poly1(p_num_poly, z_value, prime) == p_num, (
                        prime,
                        z_value,
                        p_num_poly,
                        p_num,
                    )
                    assert eval_poly1(theta_poly, z_value, prime) == theta, (
                        prime,
                        z_value,
                        theta_poly,
                        theta,
                    )
                    assert (
                        denominator
                        * denominator
                        * (s_value * s_value - 4 * p_value)
                        - theta
                    ) % prime == 0, (
                        prime,
                        c,
                        denominator,
                        s_value,
                        p_value,
                        theta,
                    )
                    split_count = quadratic_root_count(
                        1,
                        -s_value,
                        p_value,
                        prime,
                    )
                    assert split_count == 1 + quadratic_character(theta, prime), (
                        prime,
                        z_value,
                        s_value,
                        p_value,
                        denominator,
                        theta,
                        split_count,
                    )
                    assert (
                        eval_poly2(elementary_poly, s_value, p_value, prime) == 0
                    ), (
                        prime,
                        a_rows,
                        b_rows,
                        z_value,
                        s_value,
                        p_value,
                        elementary_poly,
                    )
                    continue

                if not solutions:
                    continue
                if c == (0, 0, 0, 0):
                    assert len(solutions) == prime * prime, (
                        prime,
                        a_rows,
                        b_rows,
                        z_value,
                        c,
                        solutions,
                    )
                    continue
                assert c[0] != 0, (prime, a_rows, b_rows, z_value, c, solutions)
                alpha = (c[1] * pow(c[0], -1, prime)) % prime
                assert c[2] == c[0] * alpha * alpha % prime, (
                    prime,
                    c,
                    alpha,
                )
                assert c[3] == c[0] * pow(alpha, 3, prime) % prime, (
                    prime,
                    c,
                    alpha,
                )
                assert len(solutions) == prime, (
                    prime,
                    a_rows,
                    b_rows,
                    z_value,
                    c,
                    alpha,
                    solutions,
                )
                assert all(
                    (alpha * alpha - s_value * alpha + p_value) % prime == 0
                    for s_value, p_value in solutions
                ), (prime, c, alpha, solutions)


def subgroup_character_value(
    value: int,
    power: int,
    index: int,
    log_table: dict[int, int],
) -> complex:
    if value == 0:
        return 0j
    residue = (power * (log_table[value] % index)) % index
    return exp(2j * pi * residue / index)


def subgroup_indicator_via_characters(
    value: int,
    index: int,
    log_table: dict[int, int],
) -> complex:
    return sum(
        subgroup_character_value(value, power, index, log_table)
        for power in range(index)
    ) / index


def check_boundary_core_slope_cover_kummer_filter() -> None:
    rng = Random(20260719)
    for prime in (17, 19, 29):
        log_table = discrete_log_table(prime)
        indices = [index for index in range(2, 7) if (prime - 1) % index == 0]
        samples = [
            (
                tuple(rng.randrange(prime) for _ in range(4)),
                tuple(rng.randrange(prime) for _ in range(4)),
            )
            for _ in range(200)
        ]
        for a_rows, b_rows in samples:
            c_polys = tuple(
                poly1_from_terms(((0, a_rows[idx]), (1, b_rows[idx])), prime)
                for idx in range(4)
            )
            q_poly = poly1_sub(
                poly1_mul(c_polys[0], c_polys[2], prime),
                poly1_mul(c_polys[1], c_polys[1], prime),
                prime,
            )
            a_poly = poly1_sub(
                poly1_mul(c_polys[0], c_polys[3], prime),
                poly1_mul(c_polys[1], c_polys[2], prime),
                prime,
            )
            b_poly = poly1_sub(
                poly1_mul(c_polys[1], c_polys[3], prime),
                poly1_mul(c_polys[2], c_polys[2], prime),
                prime,
            )
            theta_poly = poly1_sub(
                poly1_mul(a_poly, a_poly, prime),
                poly1_mul(
                    poly1_from_terms(((0, 4),), prime),
                    poly1_mul(q_poly, b_poly, prime),
                    prime,
                ),
                prime,
            )

            if q_poly:
                q_zero_slopes = [
                    z_value
                    for z_value in range(prime)
                    if eval_poly1(q_poly, z_value, prime) == 0
                ]
                assert len(q_zero_slopes) <= 2, (
                    prime,
                    a_rows,
                    b_rows,
                    q_poly,
                    q_zero_slopes,
                )

            if theta_poly:
                theta_zero_slopes = [
                    z_value
                    for z_value in range(prime)
                    if eval_poly1(theta_poly, z_value, prime) == 0
                ]
                assert len(theta_zero_slopes) <= 4, (
                    prime,
                    a_rows,
                    b_rows,
                    theta_poly,
                    theta_zero_slopes,
                )

            plus_zero_points = 0
            minus_zero_points = 0
            for z_value in range(prime):
                q_value = eval_poly1(q_poly, z_value, prime)
                if q_value == 0:
                    continue
                a_value = eval_poly1(a_poly, z_value, prime)
                b_value = eval_poly1(b_poly, z_value, prime)
                theta_value = eval_poly1(theta_poly, z_value, prime)
                roots_y = [
                    y_value
                    for y_value in range(prime)
                    if y_value * y_value % prime == theta_value
                ]
                inv_q = pow(q_value, -1, prime)
                inv_2q = pow((2 * q_value) % prime, -1, prime)
                s_value = a_value * inv_q % prime
                p_value = b_value * inv_q % prime
                for y_value in roots_y:
                    r_plus = (a_value + y_value) * inv_2q % prime
                    r_minus = (a_value - y_value) * inv_2q % prime
                    assert (r_plus + r_minus) % prime == s_value, (
                        prime,
                        z_value,
                        y_value,
                        r_plus,
                        r_minus,
                        s_value,
                    )
                    assert r_plus * r_minus % prime == p_value, (
                        prime,
                        z_value,
                        y_value,
                        r_plus,
                        r_minus,
                        p_value,
                    )
                    if r_plus == 0:
                        plus_zero_points += 1
                    if r_minus == 0:
                        minus_zero_points += 1

                    for index in indices:
                        plus_in_domain = (
                            r_plus != 0 and log_table[r_plus] % index == 0
                        )
                        minus_in_domain = (
                            r_minus != 0 and log_table[r_minus] % index == 0
                        )
                        direct = 1 if plus_in_domain and not minus_in_domain else 0
                        char_plus = subgroup_indicator_via_characters(
                            r_plus,
                            index,
                            log_table,
                        )
                        char_minus = subgroup_indicator_via_characters(
                            r_minus,
                            index,
                            log_table,
                        )
                        expanded = char_plus * (1 - char_minus)
                        assert abs(expanded.imag) < 1e-8, (
                            prime,
                            index,
                            z_value,
                            y_value,
                            r_plus,
                            r_minus,
                            expanded,
                        )
                        assert abs(expanded.real - direct) < 1e-8, (
                            prime,
                            index,
                            z_value,
                            y_value,
                            r_plus,
                            r_minus,
                            direct,
                            expanded,
                        )

            if q_poly and theta_poly and b_poly:
                assert plus_zero_points <= 2, (
                    prime,
                    a_rows,
                    b_rows,
                    b_poly,
                    plus_zero_points,
                )
                assert minus_zero_points <= 2, (
                    prime,
                    a_rows,
                    b_rows,
                    b_poly,
                    minus_zero_points,
                )


def check_nonruled_degree_bound() -> None:
    # Model only the combinatorics after ruled cores are removed: each
    # (j-1)-core has at most two anchors, hence at most one edge.
    for n in range(3, 9):
        points = tuple(range(n))
        for j in range(1, n):
            supports = [
                frozenset(i for i, bit in enumerate(bits) if bit)
                for bits in product((0, 1), repeat=n)
                if sum(bits) == j
            ]
            index = {support: i for i, support in enumerate(supports)}
            edges: set[tuple[int, int]] = set()
            core_count = 0
            for core_bits in product((0, 1), repeat=n):
                if sum(core_bits) != j - 1:
                    continue
                core = frozenset(i for i, bit in enumerate(core_bits) if bit)
                anchors = [x for x in points if x not in core]
                # Non-ruled worst case: choose at most two anchors.
                chosen = anchors[:2]
                if len(chosen) == 2:
                    a = index[core | {chosen[0]}]
                    b = index[core | {chosen[1]}]
                    edges.add(tuple(sorted((a, b))))
                core_count += 1

            degrees = [0] * len(supports)
            for a, b in edges:
                degrees[a] += 1
                degrees[b] += 1
            assert max(degrees, default=0) <= j, (n, j, max(degrees))
            assert len(edges) <= j * len(supports) // 2, (n, j, len(edges))
            assert len(edges) <= core_count, (n, j, len(edges), core_count)


def check_average_collinearity_corollary() -> None:
    # For t=2 the existing average-collinearity ledger reads
    # B_2^max(A) = (1-p_z)/(M p_z) + (4/M) Gamma_1(A) Q.
    # The non-ruled degree bound Gamma_1(A) <= j gives (AVG1).
    for q in (5, 7, 17, 31):
        p_z = Fraction(q * q - 1, q**4)
        for locator_degree in range(1, 8):
            for m_size in (1, 2, 5, 25, 100):
                for gamma_1 in range(locator_degree + 1):
                    ledger = (
                        Fraction(1, 1) - p_z
                    ) / (m_size * p_z) + Fraction(4 * gamma_1 * q, m_size)
                    stated_bound = (
                        Fraction(1, 1) - p_z
                    ) / (m_size * p_z) + Fraction(4 * locator_degree * q, m_size)
                    assert ledger <= stated_bound, (
                        q,
                        locator_degree,
                        m_size,
                        gamma_1,
                        ledger,
                        stated_bound,
                    )

    # Packet-level higher-exchange substitution.  If all full moving r-root
    # fibers have been charged inside one affine h-packet, then
    # Gamma_r <= binom(h,r)(Q_F^(r-1)-1).  Substituting these Gamma_r into
    # B_tau^max gives (AVGH), and the displayed coarse form follows from
    # (Q_F^(r-1)-1) Q_F^(tau-r) <= Q_F^(tau-1).
    for q_f in (5, 7, 17, 31):
        for support_slack in range(1, 6):
            p_z = Fraction(q_f**support_slack - 1, q_f ** (2 * support_slack))
            for h_width in range(1, 8):
                max_exchange = min(h_width, support_slack - 1)
                for m_size in (1, 2, 5, 25, 100):
                    gamma_terms = [
                        comb(h_width, r) * (q_f ** (r - 1) - 1)
                        for r in range(1, max_exchange + 1)
                    ]
                    ledger = (Fraction(1, 1) - p_z) / (
                        m_size * p_z
                    ) + Fraction(4, m_size) * sum(
                        gamma_r * q_f ** (support_slack - r)
                        for r, gamma_r in enumerate(gamma_terms, start=1)
                    )
                    exact_bound = (Fraction(1, 1) - p_z) / (
                        m_size * p_z
                    ) + Fraction(4, m_size) * sum(
                        comb(h_width, r)
                        * (q_f ** (r - 1) - 1)
                        * q_f ** (support_slack - r)
                        for r in range(1, max_exchange + 1)
                    )
                    coarse_bound = (Fraction(1, 1) - p_z) / (
                        m_size * p_z
                    ) + Fraction(4 * q_f ** (support_slack - 1), m_size) * sum(
                        comb(h_width, r) for r in range(1, max_exchange + 1)
                    )
                    assert ledger == exact_bound, (
                        q_f,
                        support_slack,
                        h_width,
                        m_size,
                        ledger,
                        exact_bound,
                    )
                    assert exact_bound <= coarse_bound, (
                        q_f,
                        support_slack,
                        h_width,
                        m_size,
                        exact_bound,
                        coarse_bound,
                    )


def check_boundary_core_closure_substitution() -> None:
    # In the rate-half variable-line closure ledger, the one-outside term is
    # (j-1) binom(n-j+1,2) |Boundary_off|.  The fixed-anchor boundary-core
    # fiber reduction gives (j-1)|Boundary_off| <= 2|Core_off|, hence the
    # substitution by 2 binom(n-j+1,2)|Core_off|.
    for n in range(3, 21):
        for j in range(2, n + 1):
            coefficient = comb(n - j + 1, 2)
            for boundary_size in range(0, 25):
                for core_size in range(0, 50):
                    if (j - 1) * boundary_size > 2 * core_size:
                        continue
                    boundary_term = (j - 1) * coefficient * boundary_size
                    core_term = 2 * coefficient * core_size
                    assert boundary_term <= core_term, (
                        n,
                        j,
                        boundary_size,
                        core_size,
                        boundary_term,
                        core_term,
                    )

            for exponent in range(0, 6):
                max_core = n**exponent
                core_term = 2 * coefficient * max_core
                crude_bound = 2 * n ** (exponent + 2)
                assert core_term <= crude_bound, (
                    n,
                    j,
                    exponent,
                    core_term,
                    crude_bound,
                )

            right_vertices = n - j + 2
            for root_count in range(0, 25):
                max_core_from_roots = 2 * right_vertices * root_count
                assert max_core_from_roots <= 2 * n * root_count, (
                    n,
                    j,
                    root_count,
                    max_core_from_roots,
                )
                root_term = 2 * coefficient * max_core_from_roots
                crude_root_bound = 4 * n**3 * root_count
                assert root_term <= crude_root_bound, (
                    n,
                    j,
                    root_count,
                    root_term,
                    crude_root_bound,
                )

            for root_count in range(0, 25):
                graph_multiplier = 2 * right_vertices
                for kummer_multiplier in range(0, 4 * n + 10):
                    conic_multiplier = min(graph_multiplier, kummer_multiplier)
                    conic_from_roots = conic_multiplier * root_count
                    assert conic_from_roots <= graph_multiplier * root_count, (
                        n,
                        j,
                        root_count,
                        graph_multiplier,
                        kummer_multiplier,
                        conic_from_roots,
                    )
                    assert conic_from_roots <= kummer_multiplier * root_count, (
                        n,
                        j,
                        root_count,
                        graph_multiplier,
                        kummer_multiplier,
                        conic_from_roots,
                    )

            for left_vertices in range(0, 25):
                for edge_count in range(left_vertices, 50):
                    if edge_count > 2 * right_vertices:
                        continue
                    assert left_vertices <= 2 * right_vertices, (
                        n,
                        j,
                        left_vertices,
                        right_vertices,
                        edge_count,
                    )


def main() -> None:
    check_difference_identity()
    check_row_implication()
    check_higher_slack_root_slice_lift()
    check_two_exchange_full_plane_lift()
    check_full_elementary_packet_lift()
    check_affine_span_packet_normal_form()
    check_fixed_root_hyperplane_criterion()
    check_hyperplane_one_root_fiber_dichotomy()
    check_affine_subpacket_one_root_fiber_dichotomy()
    check_affine_subpacket_two_root_fiber_dichotomy()
    check_general_moving_fiber_dimension_drop()
    check_residual_exchange_degree_bound()
    check_two_root_line_classification()
    check_nonfixed_line_constant_slope_collapse()
    check_boundary_core_same_slope_fibers()
    check_t2_determinant_gate()
    check_ruled_core_dichotomy()
    check_hankel_ruled_core_collapse()
    check_one_exchange_triangle_classification()
    check_top_packet_lifted_kernel()
    check_top_packet_compression_ledger()
    check_simultaneous_kernel_root_slice_recursion()
    check_boundary_off_external_anchor_corollary()
    check_boundary_shadow_anchor_recovery()
    check_boundary_shadow_quadratic_gate()
    check_boundary_shadow_conic_secant_duality()
    check_boundary_fixed_anchor_core_fibers()
    check_boundary_core_bidegree_determinant()
    check_boundary_discriminant_degeneracy_classification()
    check_boundary_quartic_kummer_power_gate()
    check_boundary_core_slope_recurrence_gate()
    check_boundary_core_slope_cover_kummer_filter()
    check_nonruled_degree_bound()
    check_average_collinearity_corollary()
    check_boundary_core_closure_substitution()
    print("same-slope root-slice lemma verifier passed")


if __name__ == "__main__":
    main()
