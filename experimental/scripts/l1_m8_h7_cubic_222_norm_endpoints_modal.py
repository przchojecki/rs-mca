#!/usr/bin/env python3
"""Bounded aggregate norm gcds for two h=7 cubic 2+2+2 endpoints."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import modal


APP_NAME = "rs-mca-l1-m8-h7-cubic-222-norm-endpoints"
PRIMES = (8191, 131071, 524287, 2147483647)

app = modal.App(APP_NAME)
image = modal.Image.debian_slim(python_version="3.12")


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


def normalize(poly: list[int], prime: int) -> list[int]:
    out = trim([coefficient % prime for coefficient in poly])
    if out == [0]:
        return out
    inverse = pow(out[-1], -1, prime)
    return [(coefficient * inverse) % prime for coefficient in out]


def remainder(poly: list[int], modulus: list[int], prime: int) -> list[int]:
    out = trim([coefficient % prime for coefficient in poly])
    mod = normalize(modulus[:], prime)
    while out != [0] and len(out) >= len(mod):
        shift = len(out) - len(mod)
        factor = out[-1]
        for index, coefficient in enumerate(mod):
            out[index + shift] = (out[index + shift] - factor * coefficient) % prime
        trim(out)
    return out


def multiply_mod(
    left: list[int], right: list[int], modulus: list[int], prime: int
) -> list[int]:
    return remainder(multiply(left, right), modulus, prime)


def power_x_mod(exponent: int, modulus: list[int], prime: int) -> list[int]:
    result = [1]
    base = remainder([0, 1], modulus, prime)
    power = exponent
    while power:
        if power & 1:
            result = multiply_mod(result, base, modulus, prime)
        base = multiply_mod(base, base, modulus, prime)
        power >>= 1
    return result


def gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    a = normalize(left[:], prime)
    b = remainder(right, a, prime)
    while b != [0]:
        a, b = normalize(b, prime), remainder(a, b, prime)
    return normalize(a, prime)


def endpoint_polynomials() -> dict[str, list[int]]:
    p5 = [360, 1218, 1659, 1147, 407, 60]

    a = [27, 27, 11]
    b = [3, 6, 7, 4, 1]
    s = [9, 9, 2]
    u = [2, 2, 1]
    t = [63, 63, 19]
    d_plus_2_squared = [4, 4, 1]
    e = add(scale(multiply(s, s), 14), scale(b, 75), factor=-1)
    f = add(
        scale(multiply(b, t), 5),
        scale(multiply(d_plus_2_squared, multiply(u, u)), 126),
        factor=-1,
    )
    r12 = add(
        add(scale(multiply(f, f), 105), scale(multiply(multiply(a, f), e), 7)),
        scale(multiply(b, multiply(e, e)), 10),
    )
    assert len(r12) == 13 and r12[-1] == 149868
    return {"x0_p5": p5, "q6x2_r12": r12}


def input_digest(polynomials: dict[str, list[int]]) -> str:
    payload = {
        "primes": PRIMES,
        "polynomials": polynomials,
        "exponent": "8*(p+1)",
    }
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


@app.function(image=image, cpu=1.0, memory=512, timeout=60, max_containers=1)
def run_all() -> dict[str, object]:
    started = time.monotonic()
    polynomials = endpoint_polynomials()
    digest = input_digest(polynomials)
    rows: list[dict[str, object]] = []
    print(
        "L1_H7_C222_NORM_INPUT "
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

    for name, poly in polynomials.items():
        for prime in PRIMES:
            row_started = time.monotonic()
            exponent = 8 * (prime + 1)
            residue = power_x_mod(exponent, poly, prime)
            residue[0] = (residue[0] - 1) % prime
            common = gcd(poly, residue, prime)
            row = {
                "endpoint": name,
                "p": prime,
                "exponent": exponent,
                "gcd_degree": len(common) - 1,
                "gcd_coefficients_low_to_high": common,
                "status": "UNIT" if common == [1] else "HIT",
                "seconds": round(time.monotonic() - row_started, 6),
            }
            rows.append(row)
            print("L1_H7_C222_NORM_ROW " + json.dumps(row, sort_keys=True), flush=True)

    complete = len(rows) == 8
    all_unit = complete and all(row["status"] == "UNIT" for row in rows)
    result = {
        "app": APP_NAME,
        "digest": digest,
        "status": "COMPLETE" if complete else "PARTIAL",
        "all_unit": all_unit,
        "rows": rows,
        "seconds": round(time.monotonic() - started, 6),
    }
    print("L1_H7_C222_NORM_RESULT " + json.dumps(result, sort_keys=True), flush=True)
    return result


@app.local_entrypoint()
def main(output: str = "") -> None:
    result = run_all.remote()
    result["launcher_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output:
        Path(output).write_text(rendered)
        print(f"L1_H7_C222_NORM_CERTIFICATE {output}")
    print(rendered, end="")
