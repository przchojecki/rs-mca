#!/usr/bin/env python3
"""Validate the fully-proportional h=7 q-quotient factor certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LAUNCHER = HERE / "l1_m8_h7_cubic_321_fully_proportional_q_quotient_modal.py"
EXPECTED_LAUNCHER_SHA256 = "06e941be7bd231d993a63ebb83c0855f0798524a10e86249e9796f9b7a02f3c0"
APP_NAME = "l1-m8-h7-cubic-321-fully-proportional-q-quotient"
PRIMES = (8191, 131071, 524287, 2147483647)


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def add(left: list[int], right: list[int], factor: int = 1) -> list[int]:
    out = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] += value
    for index, value in enumerate(right):
        out[index] += factor * value
    return trim(out)


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            out[i + j] += left_value * right_value
    return trim(out)


def scale(poly: list[int], value: int) -> list[int]:
    return trim([value * coefficient for coefficient in poly])


def power(poly: list[int], exponent: int) -> list[int]:
    out = [1]
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def mod_poly(poly: list[int], prime: int) -> list[int]:
    return trim([coefficient % prime for coefficient in poly])


def divmod_poly(
    numerator: list[int], denominator: list[int], prime: int
) -> tuple[list[int], list[int]]:
    remainder = mod_poly(numerator, prime)
    divisor = mod_poly(denominator, prime)
    assert divisor != [0]
    quotient = [0] * max(1, len(remainder) - len(divisor) + 1)
    inverse = pow(divisor[-1], -1, prime)
    while remainder != [0] and len(remainder) >= len(divisor):
        shift = len(remainder) - len(divisor)
        factor = remainder[-1] * inverse % prime
        quotient[shift] = (quotient[shift] + factor) % prime
        for index, coefficient in enumerate(divisor):
            remainder[index + shift] = (
                remainder[index + shift] - factor * coefficient
            ) % prime
        trim(remainder)
    return trim(quotient), remainder


def multiply_mod(
    left: list[int], right: list[int], modulus: list[int], prime: int
) -> list[int]:
    return divmod_poly(multiply(left, right), modulus, prime)[1]


def power_mod(
    poly: list[int], exponent: int, modulus: list[int], prime: int
) -> list[int]:
    out = [1]
    base = mod_poly(poly, prime)
    while exponent:
        if exponent & 1:
            out = multiply_mod(out, base, modulus, prime)
        base = multiply_mod(base, base, modulus, prime)
        exponent //= 2
    return out


def source_polynomials() -> dict[str, object]:
    import sympy as sp

    b, q = sp.symbols("b q")
    p = 40 * b * (b**2 - 6 * b + 27) + 42 * q * (11 * b + 15)
    d_star = (
        3 * q * (40 * b**2 - 253 * b + 1155)
        - 20 * b * (11 * b**2 + 81 * b + 414)
    )
    q_star = (
        720 * b * (360 + 1098 * q + 191 * q**2 - 10 * q**3)
        + (12 * q - 44 * b - 294) * q * p
    )
    k_star = 240 * b * q * (b - 6) - p
    e_g = k_star - 720 * b * q**2
    l_star = 135 * b * (b**2 + 6 * b + 105 + 8 * q) - 6 * p
    f_star = d_star * k_star - 30 * b * q_star
    j_star = 150 * b * q_star - 3 * d_star**2 - 5 * p * d_star
    theta = sp.expand(5 * e_g * d_star**2 * l_star - 6 * j_star * f_star)
    a2 = 63 * (1575 - 247 * b**2)
    a1 = 9240 * b**2 * (9 - b**2)
    a0 = 400 * b**2 * (9 - b**2) * (b**2 + 27)
    theta_q = sp.Poly(theta, q, domain=sp.ZZ[b])
    theta_coefficients = [theta_q.nth(index) for index in range(7)]
    u = {1: sp.Integer(1), 2: -a1}
    v = {1: sp.Integer(0), 2: -a0}
    for degree in range(3, 7):
        u[degree] = sp.expand(-a1 * u[degree - 1] - a2 * a0 * u[degree - 2])
        v[degree] = sp.expand(-a1 * v[degree - 1] - a2 * a0 * v[degree - 2])
    rho1 = a2**5 * theta_coefficients[1]
    rho0 = a2**5 * theta_coefficients[0]
    for degree in range(2, 7):
        rho1 += a2 ** (6 - degree) * theta_coefficients[degree] * u[degree]
        rho0 += a2 ** (6 - degree) * theta_coefficients[degree] * v[degree]
    rho1, rho0 = sp.expand(rho1), sp.expand(rho0)
    univariate = sp.expand(a2 * rho0**2 - a1 * rho0 * rho1 + a0 * rho1**2)

    x = (b + 15) / 4
    a = -(b + 3) / 2
    ell = (b**2 + 6 * b + 105 + 8 * q) / 16
    d_core = d_star / (3600 * b)
    q_core = q_star / (72 * d_star)
    g_core = -f_star / (600 * b * e_g)
    y_core = (ell - 2 * g_core) / a - x
    v_core = g_core + x * y_core + y_core**2
    r_core = -q * p / (2880 * b)
    z_d = d_core - y_core * v_core
    z_q = q_core - a * g_core - x * ell + 20 + 8 * q / 3 + d_core
    z_r = (
        r_core
        - g_core * (ell - g_core)
        + x * q_core
        + (a + x) * d_core
        + 15
        + 23 * q / 4
        + q**2 / 8
    )

    e2 = -720 * b
    e1 = 240 * b**2 - 1902 * b - 630
    e0 = -40 * b * (b**2 - 6 * b + 27)
    s1 = sp.expand(a2 * e1 - e2 * a1)
    s0 = sp.expand(a2 * e0 - e2 * a0)
    z_affine = sp.symbols("z_affine")
    a_affine = 1575 - 247 * z_affine
    c_affine = -800 * z_affine**2 + 8929 * z_affine - 11025
    n_affine = 40 * z_affine**2 + 51 * z_affine - 2835
    h_affine = sp.expand(
        n_affine**2 - 163**2 * z_affine * (z_affine + 27) ** 2
    )
    k_affine = sp.expand(
        42 * a_affine * n_affine
        + 163 * (z_affine + 27) ** 2 * c_affine
    )
    v_exceptional = sp.expand(a2 * s0**2 - a1 * s0 * s1 + a0 * s1**2)
    x_star = sp.expand(q_star - 24 * d_star * q**2)
    g_exceptional = -(d_star**2) * l_star / (720 * b * j_star)
    y_exceptional = (ell - 2 * g_exceptional) / a - x
    v_structural_exceptional = (
        g_exceptional + x * y_exceptional + y_exceptional**2
    )
    z_d_exceptional = d_core - y_exceptional * v_structural_exceptional
    z_q_exceptional = (
        q_core - a * g_exceptional - x * ell + 20 + 8 * q / 3 + d_core
    )
    z_r_exceptional = (
        r_core
        - g_exceptional * (ell - g_exceptional)
        + x * q_core
        + (a + x) * d_core
        + 15
        + 23 * q / 4
        + q**2 / 8
    )

    leading_relation = 247 * b**2 - 1575
    leading_q = -sp.Rational(10, 231) * (b**2 + 27)
    leading_numerator = sp.Poly(
        sp.fraction(sp.cancel(theta.subs(q, leading_q)))[0], b, domain=sp.ZZ
    )

    def coefficients(expression: object, variable: object = b) -> list[int]:
        return [
            int(value)
            for value in reversed(
                sp.Poly(expression, variable, domain=sp.ZZ).all_coeffs()
            )
        ]

    def numerator_q_coefficients(
        expression: object, total_degree_bound: int
    ) -> list[list[int]]:
        numerator = sp.fraction(sp.cancel(expression))[0]
        rational = sp.Poly(numerator, b, q, domain=sp.QQ)
        if rational.is_zero:
            return [[0]]
        denominator, integral = rational.clear_denoms(convert=True)
        content, primitive = integral.primitive()
        for fixed_unit in (int(denominator), int(content)):
            assert fixed_unit != 0
            assert all(fixed_unit % prime != 0 for prime in PRIMES)
        if primitive.LC() < 0:
            primitive = -primitive
        assert primitive.total_degree() <= total_degree_bound
        q_poly = sp.Poly(primitive.as_expr(), q, domain=sp.ZZ[b])
        return [
            coefficients(q_poly.nth(index)) for index in range(q_poly.degree() + 1)
        ]

    x_star_q_coefficients = numerator_q_coefficients(x_star, 5)
    while len(x_star_q_coefficients) < 4:
        x_star_q_coefficients.append([0])
    assert len(x_star_q_coefficients) == 4
    v_exceptional_coefficients = coefficients(v_exceptional)
    assert len(v_exceptional_coefficients) - 1 <= 16

    return {
        "U": coefficients(univariate),
        "rho_1": coefficients(rho1),
        "rho_0": coefficients(rho0),
        "leading_relation": coefficients(leading_relation),
        "leading_theta_numerator": [
            int(value) for value in reversed(leading_numerator.all_coeffs())
        ],
        "Z_D_q_coefficients": numerator_q_coefficients(z_d, 18),
        "Z_Q_q_coefficients": numerator_q_coefficients(z_q, 10),
        "Z_R_q_coefficients": numerator_q_coefficients(z_r, 15),
        "S_1": coefficients(s1),
        "S_0": coefficients(s0),
        "singular_affine_A": coefficients(a_affine, z_affine),
        "singular_affine_H": coefficients(h_affine, z_affine),
        "singular_affine_K": coefficients(k_affine, z_affine),
        "V_E": v_exceptional_coefficients,
        "X_star_q_coefficients": x_star_q_coefficients,
        "Z_D_e_q_coefficients": numerator_q_coefficients(z_d_exceptional, 27),
        "Z_Q_e_q_coefficients": numerator_q_coefficients(z_q_exceptional, 13),
        "Z_R_e_q_coefficients": numerator_q_coefficients(z_r_exceptional, 21),
    }


def input_digest(polynomials: dict[str, object]) -> str:
    payload = {"primes": PRIMES, "polynomials": polynomials}
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def verify_gcd_certificate(
    packet: dict[str, object], left: list[int], right: list[int], prime: int
) -> None:
    left_mod, right_mod = mod_poly(left, prime), mod_poly(right, prime)
    if packet["status"] == "IDENTICALLY_ZERO_PAIR":
        assert left_mod == [0] and right_mod == [0]
        return
    common = mod_poly(packet["gcd_coefficients_low_to_high"], prime)
    bezout_left = mod_poly(packet["bezout_left_low_to_high"], prime)
    bezout_right = mod_poly(packet["bezout_right_low_to_high"], prime)
    assert common != [0] and common[-1] == 1
    assert len(common) - 1 == packet["gcd_degree"]
    assert divmod_poly(left_mod, common, prime)[1] == [0]
    assert divmod_poly(right_mod, common, prime)[1] == [0]
    combination = mod_poly(
        add(multiply(bezout_left, left_mod), multiply(bezout_right, right_mod)),
        prime,
    )
    assert combination == common
    assert packet["status"] == ("UNIT" if common == [1] else "HIT")


def quotient_filter_remainder(
    q_coefficients: list[list[int]],
    rho1: list[int],
    rho0: list[int],
    univariate: list[int],
    prime: int,
) -> list[int]:
    modulus = mod_poly(univariate, prime)
    assert modulus != [0]
    degree = len(q_coefficients) - 1
    negative_rho0 = mod_poly(scale(rho0, -1), prime)
    out = [0]
    for exponent, coefficient in enumerate(q_coefficients):
        term = divmod_poly(mod_poly(coefficient, prime), modulus, prime)[1]
        term = multiply_mod(
            term,
            power_mod(negative_rho0, exponent, modulus, prime),
            modulus,
            prime,
        )
        term = multiply_mod(
            term,
            power_mod(rho1, degree - exponent, modulus, prime),
            modulus,
            prime,
        )
        out = divmod_poly(add(out, term), modulus, prime)[1]
    return out


def verify_multi_gcd_certificate(
    packet: dict[str, object], family: list[list[int]], prime: int
) -> None:
    common = mod_poly(packet["gcd_coefficients_low_to_high"], prime)
    bezout = packet["bezout_coefficients_low_to_high"]
    assert common != [0] and common[-1] == 1
    assert len(common) - 1 == packet["gcd_degree"]
    assert len(bezout) == len(family)
    combination = [0]
    for coefficient, polynomial in zip(bezout, family):
        assert divmod_poly(polynomial, common, prime)[1] == [0]
        combination = mod_poly(
            add(combination, multiply(mod_poly(coefficient, prime), polynomial)),
            prime,
        )
    assert combination == common
    assert packet["status"] == ("UNIT" if common == [1] else "HIT")


def verify_structural_common_gcd(
    packet: dict[str, object], polynomials: dict[str, object], prime: int
) -> None:
    u_source = polynomials["U"]
    rho1_source = polynomials["rho_1"]
    rho0_source = polynomials["rho_0"]
    assert isinstance(u_source, list)
    assert isinstance(rho1_source, list)
    assert isinstance(rho0_source, list)
    u_mod = mod_poly(u_source, prime)
    if packet["status"] == "U_IDENTICALLY_ZERO":
        assert u_mod == [0]
        return
    assert u_mod != [0]

    remainders = {}
    for label in ("D", "Q", "R"):
        q_coefficients = polynomials[f"Z_{label}_q_coefficients"]
        assert isinstance(q_coefficients, list)
        remainders[label] = quotient_filter_remainder(
            q_coefficients, rho1_source, rho0_source, u_source, prime
        )
    assert packet["filter_remainders_low_to_high"] == remainders

    family = [u_mod, remainders["D"], remainders["Q"], remainders["R"]]
    verify_multi_gcd_certificate(packet, family, prime)


def verify_exceptional_structural_common_gcd(
    packet: dict[str, object], polynomials: dict[str, object], prime: int
) -> None:
    v_exceptional_source = polynomials["V_E"]
    s1_source = polynomials["S_1"]
    s0_source = polynomials["S_0"]
    assert isinstance(v_exceptional_source, list)
    assert isinstance(s1_source, list)
    assert isinstance(s0_source, list)
    v_exceptional_mod = mod_poly(v_exceptional_source, prime)
    if packet["status"] == "V_E_IDENTICALLY_ZERO":
        assert v_exceptional_mod == [0]
        return
    assert v_exceptional_mod != [0]

    remainders = {}
    x_star_q_coefficients = polynomials["X_star_q_coefficients"]
    assert isinstance(x_star_q_coefficients, list)
    remainders["X_E"] = quotient_filter_remainder(
        x_star_q_coefficients,
        s1_source,
        s0_source,
        v_exceptional_source,
        prime,
    )
    for label in ("D", "Q", "R"):
        q_coefficients = polynomials[f"Z_{label}_e_q_coefficients"]
        assert isinstance(q_coefficients, list)
        remainders[label] = quotient_filter_remainder(
            q_coefficients,
            s1_source,
            s0_source,
            v_exceptional_source,
            prime,
        )
    assert packet["filter_remainders_low_to_high"] == remainders

    family = [
        v_exceptional_mod,
        remainders["X_E"],
        remainders["D"],
        remainders["Q"],
        remainders["R"],
    ]
    verify_multi_gcd_certificate(packet, family, prime)


def verify_exceptional_singular_affine_gcd(
    packet: dict[str, object], polynomials: dict[str, object], prime: int
) -> None:
    h_source = polynomials["singular_affine_H"]
    k_source = polynomials["singular_affine_K"]
    a_source = polynomials["singular_affine_A"]
    assert isinstance(h_source, list)
    assert isinstance(k_source, list)
    assert isinstance(a_source, list)
    assert len(mod_poly(h_source, prime)) - 1 == 4
    assert len(mod_poly(k_source, prime)) - 1 == 4
    assert packet["status"] in {"UNIT", "HIT"}
    verify_gcd_certificate(packet, h_source, k_source, prime)

    common = mod_poly(packet["gcd_coefficients_low_to_high"], prime)
    factorization = packet["factorization"]
    factors = factorization["factors"]
    product = [factorization["unit"] % prime]
    for factor in factors:
        coefficients = mod_poly(factor["coefficients_low_to_high"], prime)
        assert coefficients[-1] == 1
        assert len(coefficients) - 1 == factor["degree"]
        assert factor["exponent"] >= 1
        assert factor["a2_zero_factor"] == (
            divmod_poly(a_source, coefficients, prime)[1] == [0]
        )
        product = mod_poly(
            multiply(product, power(coefficients, factor["exponent"])), prime
        )
    assert product == common
    eligible = [
        factor
        for factor in factors
        if factor["degree"] <= 2 and not factor["a2_zero_factor"]
    ]
    assert packet["ambient_quadratic_eligible_factors"] == eligible
    assert packet["ambient_status"] == ("HIT" if eligible else "EMPTY")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    launcher_hash = hashlib.sha256(LAUNCHER.read_bytes()).hexdigest()
    assert launcher_hash == EXPECTED_LAUNCHER_SHA256
    polynomials = source_polynomials()
    digest = input_digest(polynomials)
    result = json.loads(args.certificate.read_text())
    assert result["app"] == APP_NAME
    assert result["launcher_sha256"] == EXPECTED_LAUNCHER_SHA256
    assert result["status"] in {"PARTIAL", "COMPLETE"}
    rows = result["rows"]
    assert len(rows) <= len(PRIMES)
    assert len({row["p"] for row in rows}) == len(rows)
    assert {row["p"] for row in rows}.issubset(PRIMES)
    if rows:
        assert result["digest"] == digest
    if args.require_complete:
        assert result["status"] == "COMPLETE"
        assert len(rows) == len(PRIMES)
        assert not result["errors"]

    for row in rows:
        prime = row["p"]
        assert row["digest"] == digest
        factorization = row["U_factorization"]
        factors = factorization["factors"]
        u_mod = mod_poly(polynomials["U"], prime)
        if factorization["status"] == "ZERO":
            assert u_mod == [0]
            assert factorization["unit"] % prime == 0
            assert not factors
            assert row["U_degree"] == -1
        else:
            assert factorization["status"] == "NONZERO"
            product = [factorization["unit"] % prime]
            for factor in factors:
                coefficients = mod_poly(factor["coefficients_low_to_high"], prime)
                assert coefficients[-1] == 1
                assert len(coefficients) - 1 == factor["degree"]
                assert factor["exponent"] >= 1
                product = mod_poly(
                    multiply(product, power(coefficients, factor["exponent"])), prime
                )
            assert product == u_mod
            assert row["U_degree"] == len(u_mod) - 1
        eligible = [factor for factor in factors if factor["degree"] <= 2]
        assert row["quadratic_field_eligible_factors"] == eligible
        verify_gcd_certificate(
            row["affine_remainder_gcd"],
            polynomials["rho_1"],
            polynomials["rho_0"],
            prime,
        )
        verify_gcd_certificate(
            row["leading_chart_gcd"],
            polynomials["leading_relation"],
            polynomials["leading_theta_numerator"],
            prime,
        )
        verify_structural_common_gcd(
            row["structural_common_gcd"], polynomials, prime
        )
        verify_exceptional_structural_common_gcd(
            row["exceptional_structural_common_gcd"], polynomials, prime
        )
        verify_exceptional_singular_affine_gcd(
            row["exceptional_singular_affine_gcd"], polynomials, prime
        )
        assert row["seconds"] >= 0

    print(
        "L1_M8_H7_C321_FULLY_PROPORTIONAL_Q_QUOTIENT_CERTIFICATE_PASS "
        f"rows={len(rows)} complete={result['status'] == 'COMPLETE'} digest={digest}"
    )


if __name__ == "__main__":
    main()
