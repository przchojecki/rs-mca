#!/usr/bin/env python3
"""Exact-rational checks for the h=7 cubic profile reductions."""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "notes/l1/l1_m8_h7_order_one_cubic_profile_reductions.md"


def poly_add(left: list[Q], right: list[Q]) -> list[Q]:
    out = [Q(0)] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += value
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(left: list[Q], right: list[Q]) -> list[Q]:
    out = [Q(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def poly_rem(poly: list[Q], divisor: list[Q]) -> list[Q]:
    out = poly[:]
    while len(out) >= len(divisor):
        scalar = out[-1] / divisor[-1]
        shift = len(out) - len(divisor)
        for i, value in enumerate(divisor):
            out[i + shift] -= scalar * value
        while len(out) > 1 and out[-1] == 0:
            out.pop()
    return out


def poly_gcd(left: list[Q], right: list[Q]) -> list[Q]:
    a, b = left[:], right[:]
    while b != [0]:
        a, b = b, poly_rem(a, b)
    leader = a[-1]
    return [value / leader for value in a]


def evaluate(poly: list[Q], value: Q) -> Q:
    out = Q(0)
    for coefficient in reversed(poly):
        out = out * value + coefficient
    return out


def linear_data(x: Q, b: Q, q: Q, d: Q) -> dict[str, Q]:
    a = x + 3
    k = 6 * x - 3 + q / 2
    c = (b + k) / 3
    t0 = 12 * x - 16 - q * (d + 2) / 6
    t1 = 2 - x
    t = t1 * b + t0
    g = (
        1
        + q * (10 * d**4 + 62 * d**3 + 163 * d**2 + 237 * d + 213) / 60
        + q**2 * (13 * d**2 + 55 * d + 76) / 72
        + q**3 / 48
    )
    h = x**2 - 8 - q / 6
    k0 = 48 - 12 * x**2 + q * (-d**2 - 3 * d + 5) / 4 - q**2 / 24
    divisor = b**2 + 3 * h * b + 3 * k0

    p2 = 36 - 2 * b
    p3 = 216 - 18 * b + 3 * t
    p4 = 1296 - 144 * b + 2 * b**2 + 24 * t
    sum_v = p2 - 6 * a + 3 * c
    sum_v2 = p4 - 2 * a * p3 + (a**2 + 2 * c) * p2 - 12 * a * c + 3 * c**2
    l4 = (sum_v**2 - sum_v2) / 2 + (6 - 3 * a) * t + c * b
    l5 = t * (3 * a**2 - 12 * a + b - 3 * c) + 2 * c * b * (3 - a) + 6 * c**2
    l6 = (
        t**2
        + t * (-a * b - 12 * c + 6 * a**2 + 3 * a * c - a**3)
        + c * b * (b + a**2 - 6 * a)
        + c**2 * (36 - 6 * a - 2 * b)
        + c**3
    )
    hnf4 = 15 + q * (d**2 + 7 * d + 23) / 4 + q**2 / 8

    a5 = -x * (x**2 + q / 6)
    b5 = (
        12 * x**3
        + 6
        + q * (d**2 + 5 * d + 11 + (1 - d**2 - 3 * d) * x - (d + 2) * x**2) / 2
        + q**2 * (d + 5 - x) / 12
    )
    c3 = Q(4, 27)
    c2 = (4 * x**2 - 2 * x - 15) / 3
    p0 = -x**3 + 3 * x**2 + 30 + (x - 1) * q / 2
    m = x**2 - 9
    n = 18 - 6 * x
    c1 = -2 * x * t0 + t1 * p0 + k * m / 3 + (2 * k * n - k**2) / 9
    c0 = t0**2 + t0 * p0 + k**2 * n / 9 + k**3 / 27
    a6 = c1 + 4 * h**2 / 3 - 4 * k0 / 9 - 3 * h * c2
    b6 = c0 + 4 * h * k0 / 3 - 3 * k0 * c2 - g
    return locals()


def check_linear_remainders() -> None:
    for x, b, q, d in ((Q(2), Q(7), Q(5), Q(3)), (Q(-1), Q(4), Q(7), Q(2))):
        z = linear_data(x, b, q, d)
        assert 3 * (z["l4"] - z["hnf4"]) == z["divisor"]
        assert z["l5"] - (z["a5"] * b + z["b5"]) == 2 * (1 - x) * z["divisor"] / 3
        assert z["a5"] == -x * (x**2 + q / 6)
        assert z["l6"] == z["c3"] * b**3 + z["c2"] * b**2 + z["c1"] * b + z["c0"]
        assert z["l6"] - z["g"] - (z["a6"] * b + z["b6"]) == (
            z["c3"] * (b - 3 * z["h"]) + z["c2"]
        ) * z["divisor"]


def x0_data(d: Q, q: Q) -> dict[str, Q]:
    a = 11 * d**2 + 27 * d + 27
    b = d**4 + 4 * d**3 + 7 * d**2 + 6 * d + 3
    c = 13 * d**2 + 34 * d + 33
    e = 5 * d**4 + 21 * d**3 + 37 * d**2 + 32 * d + 15
    p = 5 * d**3 + 16 * d**2 + 18 * d + 10
    p5 = 60 * d**5 + 407 * d**4 + 1147 * d**3 + 1659 * d**2 + 1218 * d + 360
    g = (
        1
        + q * (10 * d**4 + 62 * d**3 + 163 * d**2 + 237 * d + 213) / 60
        + q**2 * (13 * d**2 + 55 * d + 76) / 72
        + q**3 / 48
    )
    b5 = 6 + q * (d**2 + 5 * d + 11) / 2 + q**2 * (d + 5) / 12
    m5 = (q - d) * b5 + 6 * d * g
    j = 25 * q**2 + 10 * c * q + 24 * e
    conic = 35 * q**2 + 14 * a * q + 120 * b
    return locals()


def check_x0() -> None:
    for d, q in ((Q(1), Q(2)), (Q(4), Q(-3)), (Q(-5, 2), Q(7))):
        z = x0_data(d, q)
        assert 120 * z["m5"] == q * (d + 2) * z["j"]
        assert 25 * z["conic"] - 35 * z["j"] == -10 * (2 * d + 3) * (
            35 * (d + 2) * q + 12 * z["p"]
        )
        if d != -2:
            q0 = -12 * z["p"] / (35 * (d + 2))
            w = x0_data(d, q0)
            assert 35 * (d + 2) ** 2 * w["conic"] == -24 * (d + 3) * w["p5"]


def check_q6x2() -> None:
    for d, x in ((Q(1), Q(2)), (Q(-3), Q(1)), (Q(5, 2), Q(-2))):
        y = x**2
        q = -6 * y
        a = 11 * d**2 + 27 * d + 27
        b = d**4 + 4 * d**3 + 7 * d**2 + 6 * d + 3
        s = d**2 + 3 * d + 3
        u = d**2 + 2 * d + 2
        quartic = 5 * d**4 + 21 * d**3 + 37 * d**2 + 32 * d + 15
        conic = 105 * y**2 - 7 * a * y + 10 * b
        e0 = -2 * quartic / 5 + (13 * d**2 + 33 * d + 33) * y - 21 * y**2
        g = (
            1
            + q * (10 * d**4 + 62 * d**3 + 163 * d**2 + 237 * d + 213) / 60
            + q**2 * (13 * d**2 + 55 * d + 76) / 72
            + q**3 / 48
        )
        b5 = (
            12 * x**3
            + 6
            + q * (d**2 + 5 * d + 11 + (1 - d**2 - 3 * d) * x - (d + 2) * x**2) / 2
            + q**2 * (d + 5 - x) / 12
        )
        branch = (d + 2) * e0 - x * (d + 6 * y) * (s - y)
        assert (q - d) * b5 + 6 * d * g == 3 * x**2 * branch
        assert e0 + 2 * u * (d + 6 * y) / 5 == -conic / 5

        e = 14 * (2 * d**2 + 9 * d + 9) ** 2 - 75 * b
        f = 5 * b * (19 * d**2 + 63 * d + 63) - 126 * (d + 2) ** 2 * u**2
        cy = [10 * b, -7 * a, Q(105)]
        sy = [s, Q(-1)]
        qy = poly_add(
            [Q(-4) * (d + 2) ** 2 * u**2],
            [25 * value for value in poly_mul([Q(0), Q(1)], poly_mul(sy, sy))],
        )
        assert poly_rem(qy, cy) == [2 * f / 63, 2 * e / 63]
        assert q == -6 * x**2
    assert 105 * 31**2 + 7 * 11 * 31 * 19 + 10 * 19**2 == 149868


def check_common_quadratic() -> None:
    u, v, y, z, b = Q(2), Q(3), Q(5), Q(-1), Q(7)
    a = y - z
    factor = [v, u, Q(1)]
    g = poly_mul(factor, [-y, Q(1)])
    f = poly_mul(factor, [-z, Q(1)])
    f[0] += b
    product = poly_mul(f, g)
    coeffs = tuple(reversed(product[:-1]))
    g3, g2, g1, _ = g
    compiled = (
        2 * g1 + a,
        g1**2 + 2 * g2 + a * (u + g1),
        2 * g3 + 2 * g1 * g2 + a * (v + u * g1 + g2) + b,
        g2**2 + 2 * g1 * g3 + a * (v * g1 + u * g2 + g3) + b * g1,
        2 * g2 * g3 + a * (v * g2 + u * g3) + b * g2,
        g3**2 + a * v * g3 + b * g3,
    )
    assert coeffs == compiled
    lam = Q(1) + a * evaluate(factor, y) / b
    assert evaluate(f, y) == lam * b
    assert a * (3 * y**2 + 2 * g1 * y + g2) == (lam - 1) * b


def check_role_polynomial() -> None:
    c = [Q(1)] * 8
    c_prime = [Q(index) for index in range(1, 8)]
    derivative_factor = poly_mul([Q(-1), Q(1)], c_prime)
    assert poly_gcd(c, derivative_factor) == [Q(1)]
    assert 7 * 7 == 49 and 49 - 7 == 42 and 7 * 6 == 42


def color_orbit(subset: frozenset[int], reflect: bool) -> frozenset[frozenset[int]]:
    rotations = {
        frozenset((value + shift) % 8 for value in subset) for shift in range(8)
    }
    if reflect:
        mirrored = frozenset((-value) % 8 for value in subset)
        rotations.update(
            frozenset((value + shift) % 8 for value in mirrored)
            for shift in range(8)
        )
    return frozenset(rotations)


def check_affine_color_compiler() -> None:
    subsets = [frozenset(values) for values in combinations(range(8), 3)]
    cyclic = {color_orbit(subset, False) for subset in subsets}
    unoriented = {color_orbit(subset, True) for subset in subsets}
    assert len(subsets) == 56
    assert len(cyclic) == 7 and all(len(item) == 8 for item in cyclic)
    assert len(unoriented) == 5  # Euclidean classes; affine chirality remains.

    theta = [Q(1)]
    for factor in (
        [Q(50), Q(1)],
        [Q(-578), Q(-224), Q(1)],
        [Q(54), Q(-4), Q(1)],
        [Q(13448), Q(-2404), Q(125)],
    ):
        theta = poly_mul(theta, factor)
    assert len(theta) - 1 == 7

    roots = (Q(-2), Q(-1), Q(3))
    p = roots[0] * roots[1] + roots[0] * roots[2] + roots[1] * roots[2]
    eta = roots[0] * roots[1] * roots[2]
    a, ell = Q(2), Q(3)
    values = tuple(a * value**2 + ell * value for value in roots)
    e1 = sum(values)
    e2 = values[0] * values[1] + values[0] * values[2] + values[1] * values[2]
    e3 = values[0] * values[1] * values[2]
    p_direct = e2 - e1**2 / 3
    q_direct = e3 - e1 * e2 / 3 + 2 * e1**3 / 27
    p_formula = ell**2 * p - 3 * a * ell * eta - a**2 * p**2 / 3
    q_formula = (
        a**3 * (eta**2 + 2 * p**3 / 27)
        - a**2 * ell * p * eta
        + 2 * a * ell**2 * p**2 / 3
        + ell**3 * eta
    )
    assert (p_direct, q_direct) == (p_formula, q_formula)
    assert 224**2 + 4 * 578 == 4 * 81**2 * 2
    assert (-4) ** 2 - 4 * 54 == -200
    assert 2404**2 - 4 * 125 * 13448 == -(2 * 486) ** 2

    for lam in (Q(2), Q(-1), Q(3, 2)):
        e1, e2, e3 = 1 + lam, lam, Q(0)
        p = e2 - e1**2 / 3
        q = e3 - e1 * e2 / 3 + 2 * e1**3 / 27
        a = lam**2 - lam + 1
        b = (lam + 1) * (2 * lam - 1) * (lam - 2)
        assert p == -a / 3 and q == b / 27
        assert 27 * a**3 * q**2 + b**2 * p**3 == 0


def main() -> None:
    check_linear_remainders()
    check_x0()
    check_q6x2()
    check_common_quadratic()
    check_role_polynomial()
    check_affine_color_compiler()
    note = NOTE.read_text()
    for anchor in (
        "D_b=0",
        "P_5(d)",
        "R_12(d)",
        "common monic quadratic",
        "Lambda_321(lambda)",
        "K_8(P,Q)",
        "Theta_8(T)",
        "alpha B_6-A_6 beta=0",
        "LOCAL_ONLY",
    ):
        assert anchor in note
    print(
        "L1_M8_H7_ORDER_ONE_CUBIC_PROFILE_REDUCTIONS_PASS "
        "linear_samples=2 x0_samples=3 q6x2_samples=3 "
        "common_quadratic=1 role_polynomial=1 "
        "affine_color_shapes=7 affine_formula=1"
    )


if __name__ == "__main__":
    main()
