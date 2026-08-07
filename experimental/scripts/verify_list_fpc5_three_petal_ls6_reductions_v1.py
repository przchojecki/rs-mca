#!/usr/bin/env python3
"""Exact regression checks for the three-petal guarded LS6 reductions."""

from __future__ import annotations


MOD = 257


def trim(poly: list[int]) -> list[int]:
    out = [value % MOD for value in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def add(left: list[int], right: list[int]) -> list[int]:
    size = max(len(left), len(right))
    return trim(
        [
            (left[i] if i < len(left) else 0)
            + (right[i] if i < len(right) else 0)
            for i in range(size)
        ]
    )


def scale(poly: list[int], scalar: int) -> list[int]:
    return trim([scalar * value for value in poly])


def mul(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x_value in enumerate(left):
        for j, y_value in enumerate(right):
            out[i + j] = (out[i + j] + x_value * y_value) % MOD
    return trim(out)


def divmod_poly(
    numerator: list[int], denominator: list[int]
) -> tuple[list[int], list[int]]:
    remainder = trim(numerator)
    denominator = trim(denominator)
    quotient = [0] * max(1, len(remainder) - len(denominator) + 1)
    inverse = pow(denominator[-1], -1, MOD)
    while remainder != [0] and len(remainder) >= len(denominator):
        shift = len(remainder) - len(denominator)
        coefficient = remainder[-1] * inverse % MOD
        quotient[shift] = coefficient
        for index, value in enumerate(denominator):
            remainder[index + shift] -= coefficient * value
        remainder = trim(remainder)
    return trim(quotient), remainder


def degree(poly: list[int]) -> int:
    return len(trim(poly)) - 1


def extended_gcd(
    left: list[int], right: list[int]
) -> tuple[list[int], list[int], list[int]]:
    old_r, r = trim(left), trim(right)
    old_s, s = [1], [0]
    old_t, t = [0], [1]
    while r != [0]:
        quotient, remainder = divmod_poly(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, add(old_s, scale(mul(quotient, s), -1))
        old_t, t = t, add(old_t, scale(mul(quotient, t), -1))
    leading_inverse = pow(old_r[-1], -1, MOD)
    return (
        scale(old_r, leading_inverse),
        scale(old_s, leading_inverse),
        scale(old_t, leading_inverse),
    )


def inverse_mod(poly: list[int], modulus: list[int]) -> list[int]:
    divisor, coefficient, _ = extended_gcd(poly, modulus)
    assert divisor == [1]
    _, remainder = divmod_poly(coefficient, modulus)
    return remainder


def monic(poly: list[int]) -> list[int]:
    poly = trim(poly)
    return scale(poly, pow(poly[-1], -1, MOD))


def gcd_poly(left: list[int], right: list[int]) -> list[int]:
    left, right = trim(left), trim(right)
    while right != [0]:
        _, remainder = divmod_poly(left, right)
        left, right = right, remainder
    return monic(left)


def check_prefix_ladder() -> int:
    checks = 0
    for ell, a, e in ((7, 2, 2), (9, 2, 4), (11, 3, 7)):
        s = ell - a
        assert a <= e <= s
        l2 = [3, 1] + [0] * (ell - 2) + [1]
        l3 = [11, 2] + [0] * (ell - 2) + [1]
        m_poly = mul(l2, l3)
        e_poly = [5 + index for index in range(e)] + [7]
        leading = e_poly[-1]

        for seed in (0, 19, 43):
            q_poly = [seed + 13 + 2 * index for index in range(e - a)] + [leading]
            tail = [seed + 17 + 3 * index for index in range(s - e + 1)]
            t_poly, remainder = divmod_poly(mul(m_poly, q_poly), e_poly)
            d_poly = add(t_poly, tail)
            v_poly = add(scale(remainder, -1), mul(e_poly, tail))

            quotient, actual_remainder = divmod_poly(mul(d_poly, e_poly), m_poly)
            assert quotient == q_poly
            assert actual_remainder == v_poly
            assert degree(d_poly) == 2 * ell - a
            assert d_poly[-1] == 1
            assert degree(v_poly) <= s
            depth = (2 * ell - a) - (s - e) - 1
            assert depth == ell + e - 1
            assert depth - (e - a) == ell + a - 1
            assert (e - a + 1) + (s - e + 1) == ell - 2 * a + 2
            assert (2 * ell - a) - 2 * (ell - 2 * a + 1) == 3 * a - 2
            checks += 1
    return checks


def check_common_pencil() -> int:
    checks = 0
    for ell, a in ((5, 1), (7, 2), (11, 3)):
        s = ell - a
        p_poly = [7, 3] + [0] * (ell - 2) + [1]
        q_poly = [1 + 2 * index for index in range(s)] + [1]
        for z0, z2, z3, scalar in ((13, 29, 47, 5), (61, 83, 109, 17)):
            m0 = (z0 - z2) * (z0 - z3) % MOD
            e_poly = scale(add(p_poly, [-z0]), scalar)
            l2 = add(p_poly, [-z2])
            l3 = add(p_poly, [-z3])
            v_poly = scale(q_poly, -m0)
            d_poly = scale(
                mul(q_poly, add(p_poly, [z0 - z2 - z3])),
                pow(scalar, -1, MOD),
            )

            assert mul(d_poly, e_poly) == add(mul(mul(l2, l3), q_poly), v_poly)
            assert degree(q_poly) == s > 0
            assert degree(d_poly) == 2 * ell - a
            quotient_d, remainder_d = divmod_poly(d_poly, q_poly)
            quotient_v, remainder_v = divmod_poly(v_poly, q_poly)
            assert remainder_d == [0] and remainder_v == [0]
            assert quotient_d != [0] and quotient_v != [0]
            checks += 1

        # In the aligned case E is constant, so e=0<a and DE is already
        # the degree->s canonical remainder.
        aligned_e = [pow(19, -1, MOD)]
        d_probe = [1] + [0] * (2 * ell - a - 1) + [1]
        assert degree(mul(d_probe, aligned_e)) == 2 * ell - a > s
        checks += 1
    return checks


def check_inverse_source_ratio() -> int:
    ell = 7
    lambda_value = 19
    lambda_inverse = pow(lambda_value, -1, MOD)
    lambda_factor = (lambda_inverse - 1) % MOD
    fixtures = (
        (
            [5, 2, 0, 1, 4, 0, 3, 1],
            [9, 1, 7, 0, 0, 5, 2, 1],
            [13, 4, 1, 0, 6, 3, 0, 1],
        ),
        (
            [11, 6, 2, 0, 5, 1, 4, 1],
            [3, 8, 0, 7, 1, 0, 2, 1],
            [17, 1, 5, 2, 0, 4, 6, 1],
        ),
    )
    checks = 0
    for l1, l2, l3 in fixtures:
        _, ratio = divmod_poly(mul(l1, inverse_mod(l2, l3)), l3)
        inverse_multiplier = add(l1, mul(l2, scale(ratio, lambda_factor)))
        _, residue_l2 = divmod_poly(inverse_multiplier, l2)
        _, residue_l3 = divmod_poly(inverse_multiplier, l3)
        _, expected_l2 = divmod_poly(l1, l2)
        _, expected_l3 = divmod_poly(scale(l1, lambda_inverse), l3)
        assert residue_l2 == expected_l2
        assert residue_l3 == expected_l3
        if degree(ratio) >= 1:
            assert degree(inverse_multiplier) == ell + degree(ratio)
        checks += 1
    return checks


def check_pair_determinant() -> int:
    ell, a, e = 7, 2, 4
    s, j = ell - a, 2 * ell - a
    l2 = [3, 1] + [0] * (ell - 2) + [1]
    l3 = [11, 2] + [0] * (ell - 2) + [1]
    modulus = mul(l2, l3)
    multiplier = [5, 6, 7, 8, 1]
    fixtures: list[tuple[list[int], list[int], list[int]]] = []

    for seed in range(1, 80):
        quotient = [13 + seed, 17 + 2 * seed, 1]
        tail = [19 + 3 * seed, 23 + 5 * seed]
        base, remainder = divmod_poly(mul(modulus, quotient), multiplier)
        locator = add(base, tail)
        value = add(scale(remainder, -1), mul(multiplier, tail))
        if degree(locator) != j or locator[-1] != 1:
            continue
        if gcd_poly(locator, modulus) != [1]:
            continue
        if gcd_poly(locator, quotient) != [1]:
            continue
        if gcd_poly(locator, value) != [1]:
            continue
        fixtures.append((locator, quotient, value))
        if len(fixtures) == 2:
            break

    assert len(fixtures) == 2
    d1, q1, v1 = fixtures[0]
    d2, q2, v2 = fixtures[1]
    determinant = add(mul(d1, q2), scale(mul(d2, q1), -1))
    numerator = add(mul(d2, v1), scale(mul(d1, v2), -1))
    quotient_h, remainder_h = divmod_poly(numerator, modulus)
    assert determinant != [0]
    assert remainder_h == [0] and quotient_h == determinant
    assert degree(determinant) <= ell - 2 * a
    assert degree(gcd_poly(d1, d2)) <= degree(determinant)
    assert degree(q1) == degree(q2) == e - a

    for ell_value, b_value, a_value in ((17, 9, 1), (23, 15, 2), (31, 27, 4)):
        locator_degree = 2 * ell_value - a_value
        core_size = 4 * ell_value + b_value - 2
        intersection = ell_value - 2 * a_value
        johnson = (
            ell_value * (4 * a_value - b_value + 2)
            + a_value * a_value
            + 2 * a_value * b_value
            - 4 * a_value
        )
        assert locator_degree * locator_degree - core_size * intersection == johnson
        assert johnson <= 0
    return 1


def main() -> None:
    prefix_checks = check_prefix_ladder()
    pencil_checks = check_common_pencil()
    ratio_checks = check_inverse_source_ratio()
    pair_checks = check_pair_determinant()
    assert prefix_checks == 9
    assert pencil_checks == 9
    assert ratio_checks == 2
    assert pair_checks == 1
    print(
        "PASS: three-petal LS6 source-ratio exclusion and prefix ladder",
        f"prefix_checks={prefix_checks}",
        f"pencil_checks={pencil_checks}",
        f"ratio_checks={ratio_checks}",
        f"pair_checks={pair_checks}",
    )


if __name__ == "__main__":
    main()
