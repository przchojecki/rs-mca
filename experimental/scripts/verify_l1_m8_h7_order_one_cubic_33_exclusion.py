#!/usr/bin/env python3
"""Verify the exact algebra in the m=8, h=7 cubic 3+3 exclusion."""

from __future__ import annotations

from fractions import Fraction
from math import comb


Poly = list[Fraction]


def trim(poly: Poly) -> Poly:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def add(left: Poly, right: Poly) -> Poly:
    out = [Fraction(0)] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] += value
    for index, value in enumerate(right):
        out[index] += value
    return trim(out)


def scale(poly: Poly, scalar: Fraction) -> Poly:
    return trim([scalar * value for value in poly])


def sub(left: Poly, right: Poly) -> Poly:
    return add(left, scale(right, Fraction(-1)))


def mul(left: Poly, right: Poly) -> Poly:
    out = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return trim(out)


def q(index: int) -> Poly:
    return [Fraction(0)] + [
        Fraction(comb(index - 1, degree), index)
        for degree in range(1, index)
    ]


def verify_cleared_second_quadratic() -> None:
    # The coefficient of r in log U is q_j=((1+d)^(j-1)-1)/j.
    q2, q3, q4, q5, q6 = (q(index) for index in range(2, 7))
    s1 = add(add(add(add(q2, q3), q4), q5), q6)
    s2 = add(scale(mul(add(q2, q3), add(q2, q3)), Fraction(1, 2)), mul(q2, q4))

    # 720g(1)+5(r-1)(12+rd)(12+rd(2d+7))=r(q_2r^2+q_1r+q_0).
    # Store a bivariate polynomial as r-coefficients, each a d-polynomial.
    d = [0, 1]
    g = [[1], s1, s2, scale(mul(mul(d, d), d), Fraction(1, 48))]

    def add_bi(left: list[Poly], right: list[Poly]) -> list[Poly]:
        out = [[Fraction(0)] for _ in range(max(len(left), len(right)))]
        for index, value in enumerate(left):
            out[index] = add(out[index], value)
        for index, value in enumerate(right):
            out[index] = add(out[index], value)
        while len(out) > 1 and out[-1] == [0]:
            out.pop()
        return out

    def scale_bi(poly: list[Poly], scalar: Fraction) -> list[Poly]:
        return [scale(coefficient, scalar) for coefficient in poly]

    def mul_bi(left: list[Poly], right: list[Poly]) -> list[Poly]:
        out = [[Fraction(0)] for _ in range(len(left) + len(right) - 1)]
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                out[i + j] = add(out[i + j], mul(a, b))
        return out

    correction = mul_bi(
        [[-1], [1]],
        mul_bi([[12], d], [[12], mul(d, [7, 2])]),
    )
    cleared = add_bi(scale_bi(g, 720), scale_bi(correction, 5))
    assert cleared == [
        [0],
        [720, 2076, 2724, 1956, 744, 120],
        [0, 480, 845, 540, 130],
        [0, 0, 35, 25],
    ]


def verify_l4_and_elimination() -> None:
    d = [0, 1]
    d2 = mul(d, d)
    s = [3, 3, 1]
    S = [9, 9, 2]

    # Sixteen times the scaled l_4 coefficient difference has
    # r-coefficient 4ds and r^2-coefficient d^2.
    l4_r = scale(mul(d, [23, 7, 1]), Fraction(1, 4))
    factorization_r = mul(d, [5, 1])
    assert scale(sub(l4_r, factorization_r), 16) == scale(mul(d, s), 4)
    assert scale(
        sub(scale(d2, Fraction(1, 8)), scale(d2, Fraction(1, 16))), 16
    ) == d2

    # Substitute r=-4s/d into the conic and the second quadratic.
    conic = add(
        add(scale(mul(s, s), 560), scale(mul([27, 27, 11], s), -56)),
        scale([3, 6, 7, 4, 1], 120),
    )
    assert conic == scale(mul(s, S), 32)

    second = add(
        add(
            scale(mul([7, 5], mul(s, s)), 80),
            scale(mul([480, 845, 540, 130], s), -4),
        ),
        [720, 2076, 2724, 1956, 744, 120],
    )
    assert second == scale(mul(mul(d, [2, 1]), S), -8)
    assert mul([3, 2], [3, 1]) == S

    # Mutation controls: either carrying coefficient change breaks replay.
    assert conic != scale(mul(s, [9, 9, 3]), 32)
    assert second != scale(mul(mul(d, [2, 1]), [9, 8, 2]), -8)


def verify_rows_and_norm_obstruction() -> None:
    rows = (
        (8191, 65536),
        (131071, 1048576),
        (524287, 4194304),
        (2147483647, 17179869184),
    )
    for p, n in rows:
        assert n == 8 * (p + 1)
        assert p % 8 == 7
        assert p not in {2, 5, 13}
        inverse_four = pow(4, p - 2, p)
        norms = {9 % p, 9 * inverse_four % p}
        assert norms.isdisjoint({1, p - 1})


def main() -> None:
    verify_cleared_second_quadratic()
    verify_l4_and_elimination()
    verify_rows_and_norm_obstruction()
    print(
        "L1_M8_H7_ORDER_ONE_CUBIC_33_EXCLUSION_PASS "
        "rows=4 identities=7 mutations=2"
    )


if __name__ == "__main__":
    main()
