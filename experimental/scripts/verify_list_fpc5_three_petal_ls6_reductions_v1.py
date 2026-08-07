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


def main() -> None:
    prefix_checks = check_prefix_ladder()
    pencil_checks = check_common_pencil()
    assert prefix_checks == 9
    assert pencil_checks == 9
    print(
        "PASS: three-petal LS6 common-pencil exclusion and prefix ladder",
        f"prefix_checks={prefix_checks}",
        f"pencil_checks={pencil_checks}",
    )


if __name__ == "__main__":
    main()
