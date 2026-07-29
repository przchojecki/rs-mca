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
    theta_poly = sp.Poly(theta, q, domain=sp.ZZ[b])
    theta_coefficients = [theta_poly.nth(index) for index in range(7)]
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
    leading_value = sp.cancel(theta.subs(q, leading_q))
    leading_numerator = sp.Poly(sp.fraction(leading_value)[0], b, domain=sp.ZZ)

    def coefficients(expression: object) -> list[int]:
        poly = sp.Poly(expression, b, domain=sp.ZZ)
        return [int(value) for value in reversed(poly.all_coeffs())]

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


@app.function(image=image, cpu=1.0, memory=512, timeout=60, max_containers=4)
def run_prime(prime: int) -> dict[str, object]:
    import sympy as sp

    started = time.monotonic()
    polynomials = source_polynomials()
    digest = input_digest(polynomials)
    b = sp.symbols("b")
    u_poly = sp.Poly(
        sum((coefficient % prime) * b**index for index, coefficient in enumerate(polynomials["U"])),
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
    row = {
        "p": prime,
        "digest": digest,
        "U_degree": u_degree,
        "U_factorization": {
            "status": factorization_status,
            "unit": int(unit) % prime,
            "factors": factors,
        },
        "quadratic_field_eligible_factors": [
            factor for factor in factors if factor["degree"] <= 2
        ],
        "affine_remainder_gcd": gcd_certificate(
            polynomials["R_1"], polynomials["R_0"], prime
        ),
        "leading_chart_gcd": gcd_certificate(
            polynomials["leading_relation"],
            polynomials["leading_theta_numerator"],
            prime,
        ),
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
