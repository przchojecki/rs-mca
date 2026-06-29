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
ruled-core collapse, triangle classification, and top-packet lift identities.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
from math import comb
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


def check_two_root_line_classification() -> None:
    for p in (3, 5, 7, 11, 17):
        pairs = [(x, y) for x in range(p) for y in range(x + 1, p)]
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
                external_roots = [
                    beta
                    for beta in external
                    if det2(
                        hankel_core_value(u_seq, beta, p),
                        hankel_core_value(v_seq, beta, p),
                        p,
                    )
                    == 0
                ]
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
                    continue

                active_slopes: set[int] = set()
                for beta in external:
                    a_beta = hankel_core_value(u_seq, beta, p)
                    b_beta = hankel_core_value(v_seq, beta, p)
                    z = slope_for_active_pair(a_beta, b_beta, p)
                    if z is not None:
                        active_slopes.add(z)

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


def main() -> None:
    check_difference_identity()
    check_row_implication()
    check_higher_slack_root_slice_lift()
    check_two_exchange_full_plane_lift()
    check_two_root_line_classification()
    check_t2_determinant_gate()
    check_ruled_core_dichotomy()
    check_hankel_ruled_core_collapse()
    check_one_exchange_triangle_classification()
    check_top_packet_lifted_kernel()
    check_top_packet_compression_ledger()
    check_boundary_off_external_anchor_corollary()
    check_nonruled_degree_bound()
    check_average_collinearity_corollary()
    print("same-slope root-slice lemma verifier passed")


if __name__ == "__main__":
    main()
