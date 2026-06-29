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


def main() -> None:
    check_difference_identity()
    check_row_implication()
    check_t2_determinant_gate()
    print("same-slope root-slice lemma verifier passed")


if __name__ == "__main__":
    main()
