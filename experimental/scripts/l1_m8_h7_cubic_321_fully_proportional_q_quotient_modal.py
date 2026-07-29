#!/usr/bin/env python3
"""Factor and certify the fully-proportional h=7 q-quotient endpoints."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import modal


APP_NAME = "l1-m8-h7-cubic-321-fully-proportional-q-quotient"
PRIMES = (8191, 131071, 524287, 2147483647)

app = modal.App(APP_NAME)
image = modal.Image.debian_slim(python_version="3.12").pip_install("sympy==1.14.0")


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


def xgcd(
    left: list[int], right: list[int], prime: int
) -> tuple[list[int], list[int], list[int]]:
    r0, r1 = mod_poly(left, prime), mod_poly(right, prime)
    s0, s1 = [1], [0]
    t0, t1 = [0], [1]
    while r1 != [0]:
        quotient, remainder = divmod_poly(r0, r1, prime)
        r0, r1 = r1, remainder
        s0, s1 = s1, mod_poly(add(s0, multiply(quotient, s1), factor=-1), prime)
        t0, t1 = t1, mod_poly(add(t0, multiply(quotient, t1), factor=-1), prime)
    assert r0 != [0]
    inverse = pow(r0[-1], -1, prime)
    return (
        mod_poly(scale(r0, inverse), prime),
        mod_poly(scale(s0, inverse), prime),
        mod_poly(scale(t0, inverse), prime),
    )


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
    theta_poly = sp.Poly(theta, q, domain=sp.ZZ[b])
    theta_coefficients = [theta_poly.nth(index) for index in range(7)]
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
    x_star = sp.expand(q_star - 24 * d_star * q**2)
    q_j0 = q**2 / 3
    g_j0 = (q_j0 - x * ell + 20 + 8 * q / 3 + d_core) / a
    h_j0 = ell - g_j0
    y_j0 = (ell - 2 * g_j0) / a - x
    v_j0 = g_j0 + x * y_j0 + y_j0**2
    z_d_j0 = d_core - y_j0 * v_j0
    z_r_j0 = (
        r_core
        - g_j0 * h_j0
        + x * q_j0
        + (a + x) * d_core
        + 15
        + 23 * q / 4
        + q**2 / 8
    )
    j0_b = sp.expand(
        96 * q**2 + (216 - 32 * b) * q + 3 * b**2 + 18 * b + 315
    )
    j0_t = sp.expand(-280 * b**2 + 2241 * b + 3465)
    j0_m = sp.expand(29 * b**2 + 234 * b + 81)
    j0_r = sp.expand(5 * b * j0_m)

    def cleared_j0(expression: object, q_degree: int, degree_bound: int) -> object:
        value = sp.cancel(j0_t**q_degree * expression.subs(q, j0_r / j0_t))
        numerator, denominator = sp.fraction(value)
        assert denominator == 1
        polynomial = sp.Poly(sp.expand(numerator), b, domain=sp.ZZ)
        assert polynomial.degree() <= degree_bound
        return polynomial.as_expr()

    def cleared_j0_rational_numerator(
        expression: object, q_degree: int, degree_bound: int
    ) -> object:
        value = sp.cancel(j0_t**q_degree * expression.subs(q, j0_r / j0_t))
        numerator = sp.fraction(value)[0]
        rational = sp.Poly(numerator, b, domain=sp.QQ)
        fixed_denominator, integral = rational.clear_denoms(convert=True)
        content, primitive = integral.primitive()
        for fixed_unit in (int(fixed_denominator), int(content)):
            assert fixed_unit != 0
            assert all(fixed_unit % prime != 0 for prime in PRIMES)
        if primitive.LC() < 0:
            primitive = -primitive
        assert primitive.degree() <= degree_bound
        return primitive.as_expr()

    j0_bhat = cleared_j0(j0_b, 2, 6)
    j0_ehat = cleared_j0(e_g, 2, 7)
    j0_fhat = cleared_j0(a2 * q**2 + a1 * q + a0, 2, 10)
    j0_xhat = cleared_j0(x_star, 3, 11)
    j0_zdhat = cleared_j0_rational_numerator(z_d_j0, 6, 24)
    j0_zrhat = cleared_j0_rational_numerator(z_r_j0, 4, 16)
    v_exceptional = sp.expand(a2 * s0**2 - a1 * s0 * s1 + a0 * s1**2)
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
    leading_value = sp.cancel(theta.subs(q, leading_q))
    leading_numerator = sp.Poly(sp.fraction(leading_value)[0], b, domain=sp.ZZ)

    def coefficients(expression: object, variable: object = b) -> list[int]:
        poly = sp.Poly(expression, variable, domain=sp.ZZ)
        return [int(value) for value in reversed(poly.all_coeffs())]

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
        "j0_T": coefficients(j0_t),
        "j0_Bhat": coefficients(j0_bhat),
        "j0_Ehat": coefficients(j0_ehat),
        "j0_Fhat": coefficients(j0_fhat),
        "j0_Xhat": coefficients(j0_xhat),
        "j0_ZDhat": coefficients(j0_zdhat),
        "j0_ZRhat": coefficients(j0_zrhat),
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


def gcd_certificate(left: list[int], right: list[int], prime: int) -> dict[str, object]:
    left_mod, right_mod = mod_poly(left, prime), mod_poly(right, prime)
    if left_mod == [0] and right_mod == [0]:
        return {"status": "IDENTICALLY_ZERO_PAIR"}
    common, bezout_left, bezout_right = xgcd(left, right, prime)
    return {
        "status": "UNIT" if common == [1] else "HIT",
        "gcd_degree": len(common) - 1,
        "gcd_coefficients_low_to_high": common,
        "bezout_left_low_to_high": bezout_left,
        "bezout_right_low_to_high": bezout_right,
    }


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


def multi_gcd_certificate(polynomials: list[list[int]], prime: int) -> dict[str, object]:
    reduced = [mod_poly(poly, prime) for poly in polynomials]
    if all(poly == [0] for poly in reduced):
        return {"status": "IDENTICALLY_ZERO_FAMILY"}
    common = reduced[0]
    bezout = [[1]]
    for poly in reduced[1:]:
        next_common, left_coefficient, right_coefficient = xgcd(common, poly, prime)
        bezout = [
            mod_poly(multiply(left_coefficient, coefficient), prime)
            for coefficient in bezout
        ]
        bezout.append(right_coefficient)
        common = next_common
    return {
        "status": "UNIT" if common == [1] else "HIT",
        "gcd_degree": len(common) - 1,
        "gcd_coefficients_low_to_high": common,
        "bezout_coefficients_low_to_high": bezout,
    }


@app.function(image=image, cpu=1.0, memory=512, timeout=60, max_containers=4)
def run_prime(prime: int) -> dict[str, object]:
    import sympy as sp

    started = time.monotonic()
    polynomials = source_polynomials()
    digest = input_digest(polynomials)
    u_source = polynomials["U"]
    rho1_source = polynomials["rho_1"]
    rho0_source = polynomials["rho_0"]
    assert isinstance(u_source, list)
    assert isinstance(rho1_source, list)
    assert isinstance(rho0_source, list)
    b = sp.symbols("b")
    u_poly = sp.Poly(
        sum(
            (coefficient % prime) * b**index
            for index, coefficient in enumerate(u_source)
        ),
        b,
        modulus=prime,
    )
    factors = []
    if u_poly.is_zero:
        factorization_status = "ZERO"
        unit = 0
        u_degree = -1
    else:
        factorization_status = "NONZERO"
        unit, raw_factors = sp.factor_list(u_poly)
        u_degree = u_poly.degree()
        for factor, exponent in raw_factors:
            coefficients = [int(value) % prime for value in reversed(factor.all_coeffs())]
            factors.append(
                {
                    "degree": factor.degree(),
                    "exponent": int(exponent),
                    "coefficients_low_to_high": coefficients,
                }
            )
    u_mod = mod_poly(u_source, prime)
    if u_mod == [0]:
        structural_common_gcd: dict[str, object] = {
            "status": "U_IDENTICALLY_ZERO"
        }
    else:
        structural_remainders = {}
        for label in ("D", "Q", "R"):
            q_coefficients = polynomials[f"Z_{label}_q_coefficients"]
            assert isinstance(q_coefficients, list)
            structural_remainders[label] = quotient_filter_remainder(
                q_coefficients, rho1_source, rho0_source, u_source, prime
            )
        structural_common_gcd = multi_gcd_certificate(
            [u_source, *structural_remainders.values()], prime
        )
        structural_common_gcd["filter_remainders_low_to_high"] = (
            structural_remainders
        )

    v_exceptional_source = polynomials["V_E"]
    s1_source = polynomials["S_1"]
    s0_source = polynomials["S_0"]
    assert isinstance(v_exceptional_source, list)
    assert isinstance(s1_source, list)
    assert isinstance(s0_source, list)
    v_exceptional_mod = mod_poly(v_exceptional_source, prime)
    if v_exceptional_mod == [0]:
        exceptional_structural_common_gcd: dict[str, object] = {
            "status": "V_E_IDENTICALLY_ZERO"
        }
    else:
        exceptional_remainders = {}
        x_star_q_coefficients = polynomials["X_star_q_coefficients"]
        assert isinstance(x_star_q_coefficients, list)
        exceptional_remainders["X_E"] = quotient_filter_remainder(
            x_star_q_coefficients,
            s1_source,
            s0_source,
            v_exceptional_source,
            prime,
        )
        for label in ("D", "Q", "R"):
            q_coefficients = polynomials[f"Z_{label}_e_q_coefficients"]
            assert isinstance(q_coefficients, list)
            exceptional_remainders[label] = quotient_filter_remainder(
                q_coefficients,
                s1_source,
                s0_source,
                v_exceptional_source,
                prime,
            )
        exceptional_structural_common_gcd = multi_gcd_certificate(
            [v_exceptional_source, *exceptional_remainders.values()], prime
        )
        exceptional_structural_common_gcd["filter_remainders_low_to_high"] = (
            exceptional_remainders
        )

    singular_h_source = polynomials["singular_affine_H"]
    singular_k_source = polynomials["singular_affine_K"]
    singular_a_source = polynomials["singular_affine_A"]
    assert isinstance(singular_h_source, list)
    assert isinstance(singular_k_source, list)
    assert isinstance(singular_a_source, list)
    assert len(mod_poly(singular_h_source, prime)) - 1 == 4
    assert len(mod_poly(singular_k_source, prime)) - 1 == 4
    singular_affine_gcd = gcd_certificate(
        singular_h_source, singular_k_source, prime
    )
    assert singular_affine_gcd["status"] in {"UNIT", "HIT"}
    common = singular_affine_gcd["gcd_coefficients_low_to_high"]
    assert isinstance(common, list)
    z_affine = sp.symbols("z_affine")
    common_poly = sp.Poly(
        sum(
            (coefficient % prime) * z_affine**index
            for index, coefficient in enumerate(common)
        ),
        z_affine,
        modulus=prime,
    )
    common_unit, common_raw_factors = sp.factor_list(common_poly)
    common_factors = []
    for factor, exponent in common_raw_factors:
        coefficients = [
            int(value) % prime for value in reversed(factor.all_coeffs())
        ]
        common_factors.append(
            {
                "degree": factor.degree(),
                "exponent": int(exponent),
                "coefficients_low_to_high": coefficients,
                "a2_zero_factor": divmod_poly(
                    singular_a_source, coefficients, prime
                )[1]
                == [0],
            }
        )
    singular_affine_gcd["factorization"] = {
        "unit": int(common_unit) % prime,
        "factors": common_factors,
    }
    singular_affine_gcd["legal_factors"] = [
        factor for factor in common_factors if not factor["a2_zero_factor"]
    ]
    singular_affine_gcd["quadratic_subfield_factors"] = [
        factor
        for factor in singular_affine_gcd["legal_factors"]
        if factor["degree"] <= 2
    ]
    singular_affine_gcd["global_status"] = (
        "HIT" if singular_affine_gcd["legal_factors"] else "EMPTY"
    )
    singular_affine_gcd["quadratic_subfield_status"] = (
        "HIT" if singular_affine_gcd["quadratic_subfield_factors"] else "EMPTY"
    )

    j0_labels = ("Bhat", "Ehat", "Fhat", "Xhat", "ZDhat", "ZRhat")
    j0_sources = [polynomials[f"j0_{label}"] for label in j0_labels]
    j0_t_source = polynomials["j0_T"]
    assert all(isinstance(source, list) for source in j0_sources)
    assert isinstance(j0_t_source, list)
    j0_common_gcd = multi_gcd_certificate(j0_sources, prime)
    if j0_common_gcd["status"] == "IDENTICALLY_ZERO_FAMILY":
        j0_common_gcd["factorization"] = {"unit": 0, "factors": []}
        j0_common_gcd["legal_factors"] = []
        j0_common_gcd["quadratic_subfield_factors"] = []
        j0_common_gcd["global_status"] = "INCONCLUSIVE"
        j0_common_gcd["quadratic_subfield_status"] = "INCONCLUSIVE"
    else:
        j0_common = j0_common_gcd["gcd_coefficients_low_to_high"]
        assert isinstance(j0_common, list)
        j0_common_poly = sp.Poly(
            sum(
                (coefficient % prime) * b**index
                for index, coefficient in enumerate(j0_common)
            ),
            b,
            modulus=prime,
        )
        j0_unit, j0_raw_factors = sp.factor_list(j0_common_poly)
        j0_factors = []
        for factor, exponent in j0_raw_factors:
            coefficients = [
                int(value) % prime for value in reversed(factor.all_coeffs())
            ]
            j0_factors.append(
                {
                    "degree": factor.degree(),
                    "exponent": int(exponent),
                    "coefficients_low_to_high": coefficients,
                    "t_zero_factor": divmod_poly(
                        j0_t_source, coefficients, prime
                    )[1]
                    == [0],
                }
            )
        j0_common_gcd["factorization"] = {
            "unit": int(j0_unit) % prime,
            "factors": j0_factors,
        }
        j0_common_gcd["legal_factors"] = [
            factor for factor in j0_factors if not factor["t_zero_factor"]
        ]
        j0_common_gcd["quadratic_subfield_factors"] = [
            factor
            for factor in j0_common_gcd["legal_factors"]
            if factor["degree"] <= 2
        ]
        j0_common_gcd["global_status"] = (
            "HIT" if j0_common_gcd["legal_factors"] else "EMPTY"
        )
        j0_common_gcd["quadratic_subfield_status"] = (
            "HIT" if j0_common_gcd["quadratic_subfield_factors"] else "EMPTY"
        )
    row = {
        "p": prime,
        "digest": digest,
        "U_degree": u_degree,
        "U_factorization": {
            "status": factorization_status,
            "unit": int(unit) % prime,
            "factors": factors,
        },
        "quadratic_subfield_factors": [
            factor for factor in factors if factor["degree"] <= 2
        ],
        "affine_remainder_gcd": gcd_certificate(
            polynomials["rho_1"], polynomials["rho_0"], prime
        ),
        "leading_chart_gcd": gcd_certificate(
            polynomials["leading_relation"],
            polynomials["leading_theta_numerator"],
            prime,
        ),
        "structural_common_gcd": structural_common_gcd,
        "exceptional_structural_common_gcd": exceptional_structural_common_gcd,
        "exceptional_singular_affine_gcd": singular_affine_gcd,
        "exceptional_j0_affine_common_gcd": j0_common_gcd,
        "seconds": round(time.monotonic() - started, 6),
    }
    print("L1_H7_C321_FULLY_PROPORTIONAL_Q_ROW " + json.dumps(row, sort_keys=True), flush=True)
    return row


def write_checkpoint(path: str, result: dict[str, object]) -> None:
    if path:
        destination = Path(path)
        temporary = destination.with_name(destination.name + ".tmp")
        temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        temporary.replace(destination)


@app.local_entrypoint()
def main(output: str = "") -> None:
    result: dict[str, object] = {
        "app": APP_NAME,
        "status": "PARTIAL",
        "rows": [],
        "errors": [],
        "launcher_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    for prime in PRIMES:
        try:
            row = run_prime.remote(prime)
            rows = result["rows"]
            assert isinstance(rows, list)
            rows.append(row)
            digests = {item["digest"] for item in rows}
            assert len(digests) == 1
            result["digest"] = row["digest"]
        except Exception as error:  # Preserve every completed prime row.
            errors = result["errors"]
            assert isinstance(errors, list)
            errors.append({"p": prime, "error": repr(error)})
        write_checkpoint(output, result)
    if len(result["rows"]) == len(PRIMES) and not result["errors"]:
        result["status"] = "COMPLETE"
    write_checkpoint(output, result)
    print("L1_H7_C321_FULLY_PROPORTIONAL_Q_RESULT " + json.dumps(result, sort_keys=True))
