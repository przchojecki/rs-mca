#!/usr/bin/env python3
"""Verify the same-slope one-exchange root-slice algebra.

The mathematical lemma is linear.  If

    ell_{T_y} = (X-y) ell_R,

then

    ell_{T_y1} - ell_{T_y2} = (y2-y1) ell_R.

Consequently any linear row that kills both endpoint locators also kills
ell_R; substituting back then kills X ell_R.  This script checks that
identity exactly in small prime fields and stress-tests the row implication.
It also checks the t=2 determinant-gate formula.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from random import Random


def mul_x_minus_y(poly: list[int], y: int, p: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for i, coeff in enumerate(poly):
        out[i] = (out[i] - y * coeff) % p
        out[i + 1] = (out[i + 1] + coeff) % p
    return out


def dot(row: tuple[int, ...], vec: list[int], p: int) -> int:
    return sum(a * b for a, b in zip(row, vec)) % p


def det2(u: tuple[int, int], v: tuple[int, int], p: int) -> int:
    return (u[0] * v[1] - u[1] * v[0]) % p


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
    check_t2_determinant_gate()
    check_ruled_core_dichotomy()
    check_nonruled_degree_bound()
    check_average_collinearity_corollary()
    print("same-slope root-slice lemma verifier passed")


if __name__ == "__main__":
    main()
