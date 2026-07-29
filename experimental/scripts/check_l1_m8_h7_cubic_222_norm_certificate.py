#!/usr/bin/env python3
"""Validate a remote h=7 cubic 2+2+2 aggregate norm certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LAUNCHER = HERE / "l1_m8_h7_cubic_222_norm_endpoints_modal.py"
EXPECTED_LAUNCHER_SHA256 = "d3b4aacf170e13fecdf36718f8566bd597beacf4965aa1584077dbe61db9f695"
APP_NAME = "rs-mca-l1-m8-h7-cubic-222-norm-endpoints"
PRIMES = (8191, 131071, 524287, 2147483647)
ENDPOINTS = ("x0_p5", "q6x2_r12")


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


def input_digest() -> str:
    payload = {
        "primes": PRIMES,
        "polynomials": endpoint_polynomials(),
        "exponent": "8*(p+1)",
    }
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()

    launcher_hash = hashlib.sha256(LAUNCHER.read_bytes()).hexdigest()
    assert launcher_hash == EXPECTED_LAUNCHER_SHA256
    result = json.loads(args.certificate.read_text())
    assert result["app"] == APP_NAME
    assert result["launcher_sha256"] == EXPECTED_LAUNCHER_SHA256
    assert result["digest"] == input_digest()
    assert result["status"] == "COMPLETE"

    rows = result["rows"]
    expected = {(endpoint, prime) for endpoint in ENDPOINTS for prime in PRIMES}
    actual = {(row["endpoint"], row["p"]) for row in rows}
    assert len(rows) == 8 and actual == expected and len(actual) == len(rows)
    for row in rows:
        assert row["exponent"] == 8 * (row["p"] + 1)
        assert row["gcd_degree"] == 0
        assert row["gcd_coefficients_low_to_high"] == [1]
        assert row["status"] == "UNIT"
        assert row["seconds"] >= 0
    assert result["all_unit"] is True
    print(
        "L1_M8_H7_CUBIC_222_NORM_CERTIFICATE_PASS "
        f"rows={len(rows)} digest={result['digest']}"
    )


if __name__ == "__main__":
    main()
