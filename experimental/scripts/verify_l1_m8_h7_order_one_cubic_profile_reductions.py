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


def poly_power(poly: list[Q], exponent: int) -> list[Q]:
    out = [Q(1)]
    for _ in range(exponent):
        out = poly_mul(out, poly)
    return out


def reduce_quadratic(poly: list[Q], a: Q, h: Q) -> tuple[Q, Q]:
    u = [Q(0), Q(1)]
    v = [Q(1), Q(0)]
    coefficient = Q(0)
    constant = Q(0)
    for degree, value in enumerate(poly):
        while len(u) <= degree:
            u.append(v[-1] - a * u[-1])
            v.append(h * u[-2])
        coefficient += value * u[degree]
        constant += value * v[degree]
    return coefficient, constant


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


def check_role_factors() -> None:
    a = [Q(1), Q(-1), Q(1)]
    b = [Q(2), Q(-3), Q(-3), Q(2)]
    a3, a6 = poly_power(a, 3), poly_power(a, 6)
    b2, b4 = poly_power(b, 2), poly_power(b, 4)
    factors = (
        poly_add(b2, [50 * value for value in a3]),
        poly_add(poly_add(b4, [-224 * value for value in poly_mul(b2, a3)]), [-578 * value for value in a6]),
        poly_add(poly_add(b4, [-4 * value for value in poly_mul(b2, a3)]), [54 * value for value in a6]),
        poly_add(
            poly_add([125 * value for value in b4], [-2404 * value for value in poly_mul(b2, a3)]),
            [13448 * value for value in a6],
        ),
    )
    assert tuple(len(factor) - 1 for factor in factors) == (6, 12, 12, 12)
    product = [Q(1)]
    for factor in factors:
        product = poly_mul(product, factor)
    assert len(product) - 1 == 42


def check_role_weld() -> None:
    for r, s in ((Q(2), Q(3)), (Q(-5), Q(7)), (Q(11), Q(-4))):
        lam = 1 + r / s
        a = lam**2 - lam + 1
        b = (lam + 1) * (2 * lam - 1) * (lam - 2)
        a0 = s**2 + r * s + r**2
        b0 = (2 * s + r) * (s + 2 * r) * (r - s)
        assert a == a0 / s**2 and b == b0 / s**3
        assert s**6 * (b**2 + 50 * a**3) == b0**2 + 50 * a0**3
        assert s**12 * (b**4 - 224 * b**2 * a**3 - 578 * a**6) == (
            b0**4 - 224 * b0**2 * a0**3 - 578 * a0**6
        )


def cyclo_add(
    left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]
) -> tuple[Q, Q, Q, Q]:
    return tuple(a + b for a, b in zip(left, right))


def cyclo_scale(
    value: tuple[Q, Q, Q, Q], scalar: Q
) -> tuple[Q, Q, Q, Q]:
    return tuple(scalar * item for item in value)


def cyclo_mul(
    left: tuple[Q, Q, Q, Q], right: tuple[Q, Q, Q, Q]
) -> tuple[Q, Q, Q, Q]:
    raw = [Q(0)] * 7
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            raw[i + j] += a * b
    for degree in range(6, 3, -1):
        raw[degree - 4] -= raw[degree]
    return tuple(raw[:4])


def cyclo_power(
    value: tuple[Q, Q, Q, Q], exponent: int
) -> tuple[Q, Q, Q, Q]:
    out = (Q(1), Q(0), Q(0), Q(0))
    for _ in range(exponent):
        out = cyclo_mul(out, value)
    return out


def cyclo_homogeneous_eval(
    coefficients: tuple[int, ...],
    numerator: tuple[Q, Q, Q, Q],
    denominator: tuple[Q, Q, Q, Q],
) -> tuple[Q, Q, Q, Q]:
    zero = (Q(0), Q(0), Q(0), Q(0))
    out = zero
    degree = len(coefficients) - 1
    for exponent, coefficient in enumerate(coefficients):
        term = cyclo_mul(
            cyclo_power(numerator, exponent),
            cyclo_power(denominator, degree - exponent),
        )
        out = cyclo_add(out, cyclo_scale(term, Q(coefficient)))
    return out


def check_galois_role_packets() -> None:
    units = (1, 3, 5, 7)
    packets = (
        ((2, 6), (1, 0, 1)),
        ((2, 4), (2, -2, 1)),
        ((4, 2), (1, -2, 2)),
        ((1, 2), (2, -4, 6, -4, 1)),
        ((1, 3), (1, -4, 8, -4, 1)),
        ((1, 4), (8, -16, 12, -4, 1)),
        ((1, 5), (1, 0, 6, 0, 1)),
        ((1, 6), (2, -4, 2, 0, 1)),
        ((1, 7), (1, 0, 0, 0, 1)),
        ((2, 1), (1, -4, 6, -4, 2)),
        ((2, 3), (1, 0, 2, -4, 2)),
        ((4, 1), (1, -4, 12, -16, 8)),
    )

    def orbit(pair: tuple[int, int]) -> frozenset[tuple[int, int]]:
        return frozenset(
            ((unit * pair[0]) % 8, (unit * pair[1]) % 8) for unit in units
        )

    all_pairs = {(a, b) for a in range(1, 8) for b in range(1, 8) if a != b}
    all_orbits = {orbit(pair) for pair in all_pairs}
    assert len(all_orbits) == 12
    assert sorted(len(item) for item in all_orbits) == [2, 2, 2] + [4] * 9
    assert {orbit(pair) for pair, _ in packets} == all_orbits

    one = (Q(1), Q(0), Q(0), Q(0))
    zero = (Q(0), Q(0), Q(0), Q(0))
    zeta = (Q(0), Q(1), Q(0), Q(0))
    packet_product = [Q(1)]
    total_degree = 0
    for (a, b), coefficients in packets:
        numerator = cyclo_add(cyclo_power(zeta, b), cyclo_scale(one, Q(-1)))
        denominator = cyclo_add(cyclo_power(zeta, a), cyclo_scale(one, Q(-1)))
        assert cyclo_homogeneous_eval(coefficients, numerator, denominator) == zero
        packet_product = poly_mul(packet_product, [Q(value) for value in coefficients])
        total_degree += len(coefficients) - 1
    assert total_degree == 42

    a = [Q(1), Q(-1), Q(1)]
    b = [Q(2), Q(-3), Q(-3), Q(2)]
    a3, a6 = poly_power(a, 3), poly_power(a, 6)
    b2, b4 = poly_power(b, 2), poly_power(b, 4)
    high_factors = (
        poly_add(b2, [50 * value for value in a3]),
        poly_add(poly_add(b4, [-224 * value for value in poly_mul(b2, a3)]), [-578 * value for value in a6]),
        poly_add(poly_add(b4, [-4 * value for value in poly_mul(b2, a3)]), [54 * value for value in a6]),
        poly_add(
            poly_add([125 * value for value in b4], [-2404 * value for value in poly_mul(b2, a3)]),
            [13448 * value for value in a6],
        ),
    )
    high_product = [Q(1)]
    for factor in high_factors:
        high_product = poly_mul(high_product, factor)
    assert [value / packet_product[-1] for value in packet_product] == [
        value / high_product[-1] for value in high_product
    ]


def quadratic_ext_mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (
        left[0] * right[0] + 2 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def quadratic_ext_poly_mul(
    left: tuple[tuple[int, int], ...], right: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, int], ...]:
    out = [(0, 0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            product = quadratic_ext_mul(a, b)
            out[i + j] = (out[i + j][0] + product[0], out[i + j][1] + product[1])
    return tuple(out)


def check_official_frobenius_role_packets() -> None:
    signed_quadratics = (
        (((1, 0), (0, 1), (1, 0)), (1, 0, 0, 0, 1), 1),
        (((2, -1), (0, 1), (1, 0)), (2, 4, 2, 0, 1), 1),
        (((3, 2), (0, 0), (1, 0)), (1, 0, 6, 0, 1), 1),
        (((4, 2), (2, 0), (1, 0)), (8, 16, 12, 4, 1), 1),
        (((3, 2), (2, 1), (1, 0)), (1, 4, 8, 4, 1), 1),
        (((2, 1), (2, 1), (1, 0)), (2, 4, 6, 4, 1), 1),
        (((2, 1), (2, 0), (2, 0)), (1, 4, 6, 4, 2), 2),
        (((2, 1), (2, 2), (2, 0)), (1, 0, 2, 4, 2), 2),
        (((2, 1), (4, 2), (4, 0)), (1, 4, 12, 16, 8), 2),
    )
    for plus, expected, scalar in signed_quadratics:
        minus = tuple((a, -b) for a, b in plus)
        product = quadratic_ext_poly_mul(plus, minus)
        assert product == tuple((scalar * value, 0) for value in expected)

    base_quadratics = ((2, 2, 1), (1, 0, 1), (1, 2, 2))
    assert 2 * (len(base_quadratics) + 2 * len(signed_quadratics)) == 42
    for prime in (8191, 131071, 524287, 2147483647):
        assert prime % 8 == 7
        square_root = pow(2, (prime + 1) // 4, prime)
        assert square_root * square_root % prime == 2
        for coefficients in base_quadratics:
            discriminant = (coefficients[1] ** 2 - 4 * coefficients[0] * coefficients[2]) % prime
            assert pow(discriminant, (prime - 1) // 2, prime) == prime - 1
        for plus, _, _ in signed_quadratics:
            for sign in (1, -1):
                coefficients = [
                    (a + sign * b * square_root) % prime for a, b in plus
                ]
                discriminant = (
                    coefficients[1] ** 2 - 4 * coefficients[0] * coefficients[2]
                ) % prime
                assert pow(discriminant, (prime - 1) // 2, prime) == prime - 1


def scaled_quadratic_core(x: Q, y: Q, q: Q, d: Q) -> dict[str, Q]:
    a = 6 - 2 * x
    u = x + y
    l2 = 15 + q / 2
    l3 = 20 + q * (d + 8) / 3
    l4 = 15 + q * (d**2 + 7 * d + 23) / 4 + q**2 / 8
    k6 = (
        1
        + q * (10 * d**4 + 62 * d**3 + 163 * d**2 + 237 * d + 213) / 60
        + q**2 * (13 * d**2 + 55 * d + 76) / 72
        + q**3 / 48
    )
    g2 = (l2 - x**2 - a * (2 * x + y)) / 2
    v = g2 + x * y + y**2
    s = l3 + 2 * y * v - 2 * x * g2 - a * (v + x * u + g2)
    r = a * (3 * y**2 + 2 * x * y + g2)
    delta = y * v
    l5 = -6 * d * k6 / (q - d)
    c4 = g2**2 + a * u * g2 + v * (a * (x - y) - 2 * x * y) + s * x - l4
    c5 = v * (g2 * (a - 2 * y) - a * y * u) + s * g2 - l5
    e6 = delta * ((y - a) * v - s) - k6
    e4 = delta * (g2**2 + a * u * g2 - y * (a + x) * v - l4) - x * k6
    e5 = (q - d) * (y**2 * v**2 * (g2 + a * u) + g2 * k6) - 6 * d * k6 * delta
    rd = delta * r
    sd = y * (y - a) * v**2 - k6
    return locals()


def check_scaled_quadratic_core() -> None:
    for values in (
        (Q(2), Q(3), Q(5), Q(7)),
        (Q(-1), Q(4), Q(9), Q(2)),
        (Q(5, 2), Q(-3, 2), Q(11), Q(-4)),
    ):
        z = scaled_quadratic_core(*values)
        assert z["e4"] == z["delta"] * z["c4"] + z["x"] * z["e6"]
        assert z["e5"] == -(z["q"] - z["d"]) * (
            z["delta"] * z["c5"] + z["g2"] * z["e6"]
        )
        assert z["sd"] == z["delta"] * z["s"] + z["e6"]
        for alpha, beta, gamma in ((Q(1), Q(2), Q(3)), (Q(2), Q(-1), Q(5))):
            transported = alpha * z["rd"] ** 2 + beta * z["rd"] * z["sd"] + gamma * z["sd"] ** 2
            original = z["delta"] ** 2 * (
                alpha * z["r"] ** 2 + beta * z["r"] * z["s"] + gamma * z["s"] ** 2
            )
            correction = z["e6"] * (
                beta * z["rd"] + gamma * (2 * z["delta"] * z["s"] + z["e6"])
            )
            assert transported == original + correction


def check_coefficient_matrix_router() -> None:
    for values in (
        (Q(2), Q(3), Q(5), Q(7)),
        (Q(-1), Q(4), Q(9), Q(2)),
        (Q(5, 2), Q(-3, 2), Q(11), Q(-4)),
    ):
        z = scaled_quadratic_core(*values)
        h = z["g2"] + z["a"] * z["u"]
        w = z["y"] * (z["a"] + z["x"]) * z["v"] + z["l4"]
        j = (z["q"] - z["d"]) * z["g2"] - 6 * z["d"] * z["delta"]
        determinant = z["g2"] * j + z["x"] * (z["q"] - z["d"]) * z["delta"]
        assert j * z["e4"] + z["x"] * z["e5"] == z["delta"] * (
            determinant * h - w * j
        )

    for y, q, d in ((Q(3), Q(5), Q(7)), (Q(-2), Q(11), Q(4))):
        z = scaled_quadratic_core(Q(0), y, q, d)
        c0 = (
            96 * y**3
            - 144 * y**2
            + (720 + 24 * q) * y
            + q**2
            + 4 * q * (d**2 + 7 * d + 8)
            - 660
        )
        assert c0 == -16 * z["e4"] / z["delta"]
        h = z["g2"] + z["a"] * z["u"]
        j = (q - d) * z["g2"] - 6 * d * z["delta"]
        m = 6 * z["g2"] - z["l3"] - z["delta"]
        f5 = (q - d) * z["delta"] * h + j * m
        assert z["delta"] * f5 == z["e5"] + j * z["e6"]

    for q, d in ((Q(5), Q(7)), (Q(11), Q(-4))):
        ell = 15 + q / 2
        v = ell * (ell + 36) / 36
        l4 = 15 + q * (d**2 + 7 * d + 23) / 4 + q**2 / 8
        fj = d * (q**2 + 132 * q + 2916) + 144 * q
        fw = q**3 + 126 * q**2 + (5364 - 504 * d - 72 * d**2) * q + 87480
        assert fj == 144 * (q - d + d * v)
        assert fw == -288 * (l4 - ell * v)


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

    x, q, d = Q(2), Q(5), Q(3)
    c = d**2 + 3 * d + 3
    quotient_a = 3 * x**2 - q / 2
    quotient_h = 3 * q * c / 4 + q**2 / 8
    z = x**2 + q / 6
    p_poly = [Q(0), Q(1)]
    ell_poly = [z, Q(-2, 3)]
    eta_poly = [-q * (d + 2) / 6, -x]
    p_image = poly_add(
        poly_add(
            poly_mul(poly_mul(ell_poly, ell_poly), p_poly),
            [6 * x * value for value in poly_mul(ell_poly, eta_poly)],
        ),
        [-(4 * x**2 / 3) * value for value in poly_mul(p_poly, p_poly)],
    )
    coefficient, constant = reduce_quadratic(p_image, quotient_a, quotient_h)
    expected_coefficient = (
        -60 * x**4 - 8 * q * x**2 + 8 * q * (d + 2) * x + 4 * q * c + q**2
    )
    expected_constant = -12 * x * q * (d + 2) * z
    assert (12 * coefficient, 12 * constant) == (
        expected_coefficient,
        expected_constant,
    )

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
    check_role_factors()
    check_role_weld()
    check_galois_role_packets()
    check_official_frobenius_role_packets()
    check_scaled_quadratic_core()
    check_coefficient_matrix_router()
    check_affine_color_compiler()
    note = NOTE.read_text()
    for anchor in (
        "D_b=0",
        "P_5(d)",
        "R_12(d)",
        "common monic quadratic",
        "Lambda_321(lambda)",
        "B^4-224B^2A^3-578A^6",
        "B_0^4-224B_0^2A_0^3-578A_0^6",
        "3*2+9*4=42",
        "disjunction",
        "lambda^p=(beta/gamma)lambda",
        "E_5=(q-d)(Y^2V^2(G_2+AU)+G_2K_6)-6dK_6D=0",
        "Delta K_6+(q-d)D^2W=0",
        "K_8(P,Q)",
        "Theta_8(T)",
        "alpha B_6-A_6 beta=0",
        "delta^2-a alpha delta-h alpha^2=0",
        "LOCAL_ONLY",
    ):
        assert anchor in note
    print(
        "L1_M8_H7_ORDER_ONE_CUBIC_PROFILE_REDUCTIONS_PASS "
        "linear_samples=2 x0_samples=3 q6x2_samples=3 "
        "common_quadratic=1 role_polynomial=1 role_factors=4 role_weld=1 "
        "galois_role_packets=12 "
        "frobenius_role_packets=21 "
        "scaled_quadratic_core=1 "
        "coefficient_matrix_router=1 "
        "affine_color_shapes=7 affine_formula=1 quotient_weld=1"
    )


if __name__ == "__main__":
    main()
