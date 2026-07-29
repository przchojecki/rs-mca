#!/usr/bin/env python3
"""Independently validate the h=7 cubic 3+2+1 singular-J0 gcd packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LAUNCHER = HERE / "l1_m8_h7_cubic_321_singular_j0_gcd_modal.py"
EXPECTED_LAUNCHER_SHA256 = "39ccbf6493dc3a421935dbbd0b1e31e761c4e13b2c3f48eaa3c6b87d44a987e0"
APP_NAME = "l1-m8-h7-cubic-321-singular-j0-gcd"
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
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return trim(out)


def scale(poly: list[int], value: int) -> list[int]:
    return trim([value * coefficient for coefficient in poly])


def power(poly: list[int], exponent: int) -> list[int]:
    out = [1]
    for _ in range(exponent):
        out = multiply(out, poly)
    return out


def source_polynomials() -> dict[str, list[int]]:
    q = [0, 1]
    a = [2916, 132, 1]
    t = [0, -144]
    b = [87480, 5364, 126, 1]
    p_w = add(
        add(multiply(power(a, 2), b), scale(multiply(power(q, 2), a), 72576)),
        scale(power(q, 3), 1492992),
        factor=-1,
    )
    first = scale(multiply(power(q, 2), power(a, 4)), 35)
    second_inner = add(
        add(
            scale(multiply(power(t, 2), power(a, 2)), 11),
            scale(multiply(t, power(a, 3)), 27),
        ),
        scale(power(a, 4), 27),
    )
    third_inner = add(
        add(
            add(
                add(power(t, 4), scale(multiply(power(t, 3), a), 4)),
                scale(multiply(power(t, 2), power(a, 2)), 7),
            ),
            scale(multiply(t, power(a, 3)), 6),
        ),
        scale(power(a, 4), 3),
    )
    p_c = add(add(first, scale(multiply(q, second_inner), 14)), scale(third_inner, 120))
    assert len(p_w) == 8 and p_w[-1] == 1
    assert len(p_c) == 11 and p_c[-1] == 35
    return {"P_W": p_w, "P_C": p_c}


def input_digest(polynomials: dict[str, list[int]]) -> str:
    payload = {"primes": PRIMES, "polynomials": polynomials}
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--require-all-unit", action="store_true")
    args = parser.parse_args()

    launcher_hash = hashlib.sha256(LAUNCHER.read_bytes()).hexdigest()
    assert launcher_hash == EXPECTED_LAUNCHER_SHA256
    polynomials = source_polynomials()
    result = json.loads(args.certificate.read_text())
    assert result["app"] == APP_NAME
    assert result["launcher_sha256"] == EXPECTED_LAUNCHER_SHA256
    assert result["digest"] == input_digest(polynomials)
    assert result["status"] == "COMPLETE"

    rows = result["rows"]
    assert len(rows) == len(PRIMES)
    assert {row["p"] for row in rows} == set(PRIMES)
    for row in rows:
        prime = row["p"]
        common = mod_poly(row["gcd_coefficients_low_to_high"], prime)
        left = mod_poly(row["bezout_P_W_low_to_high"], prime)
        right = mod_poly(row["bezout_P_C_low_to_high"], prime)
        assert common != [0] and common[-1] == 1
        assert len(common) - 1 == row["gcd_degree"]
        assert divmod_poly(polynomials["P_W"], common, prime)[1] == [0]
        assert divmod_poly(polynomials["P_C"], common, prime)[1] == [0]
        combination = mod_poly(
            add(
                multiply(left, polynomials["P_W"]),
                multiply(right, polynomials["P_C"]),
            ),
            prime,
        )
        assert combination == common
        expected_status = "UNIT" if common == [1] else "HIT"
        assert row["status"] == expected_status
        assert row["seconds"] >= 0

    all_unit = all(row["status"] == "UNIT" for row in rows)
    assert result["all_unit"] is all_unit
    if args.require_all_unit:
        assert all_unit
    print(
        "L1_M8_H7_C321_SINGULAR_J0_GCD_CERTIFICATE_PASS "
        f"rows={len(rows)} all_unit={all_unit} digest={result['digest']}"
    )


if __name__ == "__main__":
    main()
