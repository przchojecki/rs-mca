#!/usr/bin/env python3
"""Validate the fully-proportional h=7 q-quotient factor certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LAUNCHER = HERE / "l1_m8_h7_cubic_321_fully_proportional_q_quotient_modal.py"
EXPECTED_LAUNCHER_SHA256 = "3d188f70b21bc60990fceda4478e5d9b2d316e50a9c0c154bf39803224bd8cb6"
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


def source_polynomials() -> dict[str, list[int]]:
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
    r1 = a2**5 * theta_coefficients[1]
    r0 = a2**5 * theta_coefficients[0]
    for degree in range(2, 7):
        r1 += a2 ** (6 - degree) * theta_coefficients[degree] * u[degree]
        r0 += a2 ** (6 - degree) * theta_coefficients[degree] * v[degree]
    r1, r0 = sp.expand(r1), sp.expand(r0)
    univariate = sp.expand(a2 * r0**2 - a1 * r0 * r1 + a0 * r1**2)
    leading_relation = 247 * b**2 - 1575
    leading_q = -sp.Rational(10, 231) * (b**2 + 27)
    leading_numerator = sp.Poly(
        sp.fraction(sp.cancel(theta.subs(q, leading_q)))[0], b, domain=sp.ZZ
    )

    def coefficients(expression: object) -> list[int]:
        return [
            int(value)
            for value in reversed(sp.Poly(expression, b, domain=sp.ZZ).all_coeffs())
        ]

    return {
        "U": coefficients(univariate),
        "R_1": coefficients(r1),
        "R_0": coefficients(r0),
        "leading_relation": coefficients(leading_relation),
        "leading_theta_numerator": [
            int(value) for value in reversed(leading_numerator.all_coeffs())
        ],
    }


def input_digest(polynomials: dict[str, list[int]]) -> str:
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
            row["affine_remainder_gcd"], polynomials["R_1"], polynomials["R_0"], prime
        )
        verify_gcd_certificate(
            row["leading_chart_gcd"],
            polynomials["leading_relation"],
            polynomials["leading_theta_numerator"],
            prime,
        )
        assert row["seconds"] >= 0

    print(
        "L1_M8_H7_C321_FULLY_PROPORTIONAL_Q_QUOTIENT_CERTIFICATE_PASS "
        f"rows={len(rows)} complete={result['status'] == 'COMPLETE'} digest={digest}"
    )


if __name__ == "__main__":
    main()
