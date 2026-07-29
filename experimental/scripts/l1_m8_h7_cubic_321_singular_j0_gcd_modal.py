#!/usr/bin/env python3
"""Certified four-prime gcd packet for the h=7 cubic 3+2+1 singular J=0 arm."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import modal


APP_NAME = "l1-m8-h7-cubic-321-singular-j0-gcd"
PRIMES = (8191, 131071, 524287, 2147483647)

app = modal.App(APP_NAME)
image = modal.Image.debian_slim(python_version="3.12")


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def add(left: list[int], right: list[int], scale: int = 1) -> list[int]:
    out = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        out[index] += value
    for index, value in enumerate(right):
        out[index] += scale * value
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
        scale=-1,
    )
    p_c = add(
        scale(multiply(power(q, 2), power(a, 4)), 35),
        scale(
            multiply(
                q,
                add(
                    add(
                        scale(multiply(power(t, 2), power(a, 2)), 11),
                        scale(multiply(t, power(a, 3)), 27),
                    ),
                    scale(power(a, 4), 27),
                ),
            ),
            14,
        ),
    )
    p_c = add(
        p_c,
        scale(
            add(
                add(
                    add(
                        add(power(t, 4), scale(multiply(power(t, 3), a), 4)),
                        scale(multiply(power(t, 2), power(a, 2)), 7),
                    ),
                    scale(multiply(t, power(a, 3)), 6),
                ),
                scale(power(a, 4), 3),
            ),
            120,
        ),
    )
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


def xgcd(
    left: list[int], right: list[int], prime: int
) -> tuple[list[int], list[int], list[int]]:
    r0, r1 = mod_poly(left, prime), mod_poly(right, prime)
    s0, s1 = [1], [0]
    t0, t1 = [0], [1]
    while r1 != [0]:
        quotient, remainder = divmod_poly(r0, r1, prime)
        r0, r1 = r1, remainder
        s0, s1 = s1, mod_poly(add(s0, multiply(quotient, s1), scale=-1), prime)
        t0, t1 = t1, mod_poly(add(t0, multiply(quotient, t1), scale=-1), prime)
    inverse = pow(r0[-1], -1, prime)
    return (
        mod_poly(scale(r0, inverse), prime),
        mod_poly(scale(s0, inverse), prime),
        mod_poly(scale(t0, inverse), prime),
    )


@app.function(image=image, cpu=0.125, memory=128, timeout=30, max_containers=1)
def run_all() -> dict[str, object]:
    started = time.monotonic()
    polynomials = source_polynomials()
    digest = input_digest(polynomials)
    rows: list[dict[str, object]] = []
    print(
        "L1_H7_C321_J0_GCD_INPUT "
        + json.dumps(
            {
                "digest": digest,
                "degrees": {name: len(poly) - 1 for name, poly in polynomials.items()},
                "primes": PRIMES,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    for prime in PRIMES:
        row_started = time.monotonic()
        common, bezout_w, bezout_c = xgcd(polynomials["P_W"], polynomials["P_C"], prime)
        row = {
            "p": prime,
            "gcd_degree": len(common) - 1,
            "gcd_coefficients_low_to_high": common,
            "bezout_P_W_low_to_high": bezout_w,
            "bezout_P_C_low_to_high": bezout_c,
            "status": "UNIT" if common == [1] else "HIT",
            "seconds": round(time.monotonic() - row_started, 6),
        }
        rows.append(row)
        print("L1_H7_C321_J0_GCD_ROW " + json.dumps(row, sort_keys=True), flush=True)

    result = {
        "app": APP_NAME,
        "digest": digest,
        "status": "COMPLETE",
        "all_unit": all(row["status"] == "UNIT" for row in rows),
        "rows": rows,
        "seconds": round(time.monotonic() - started, 6),
    }
    print("L1_H7_C321_J0_GCD_RESULT " + json.dumps(result, sort_keys=True), flush=True)
    return result


@app.local_entrypoint()
def main(output: str = "") -> None:
    result = run_all.remote()
    result["launcher_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        Path(output).write_text(rendered)
        print(f"L1_H7_C321_J0_GCD_CERTIFICATE {output}")
    print(rendered, end="")
