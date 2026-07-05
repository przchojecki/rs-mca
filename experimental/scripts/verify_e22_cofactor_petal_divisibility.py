#!/usr/bin/env python3
"""Verify the E22 cofactor petal-divisibility packet."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-cofactor-petal-divisibility/"
    "e22_cofactor_petal_divisibility.json"
)
COFACTOR_CERT = ROOT / (
    "experimental/data/certificates/e22-agreement-cofactor-equations/"
    "e22_agreement_cofactor_equations.json"
)
SCHEMA = "e22-cofactor-petal-divisibility-v1"
DAG_NODE = "e22_cofactor_petal_divisibility"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(cert.get("dependencies") == ["e22_agreement_cofactor_equations"], "bad dependencies")
    dep = json.loads(COFACTOR_CERT.read_text(encoding="utf-8"))
    require(dep.get("dag_node") == "e22_agreement_cofactor_equations", "bad local dependency")
    require(dep.get("status") == "PROVED", "dependency must be PROVED")
    return cert


def trim(poly: list[int] | tuple[int, ...], p: int) -> tuple[int, ...]:
    out = [x % p for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    if len(out) == 1 and out[0] == 0:
        return ()
    return tuple(out)


def poly_add(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim(out, p)


def poly_mul(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    if not a or not b:
        return ()
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out, p)


def locator(points: list[int], p: int) -> tuple[int, ...]:
    out = (1,)
    for x in points:
        out = poly_mul(out, ((-x) % p, 1), p)
    return out


def poly_eval(poly: tuple[int, ...], x: int, p: int) -> int:
    value = 0
    for coeff in reversed(poly):
        value = (value * x + coeff) % p
    return value


def divmod_poly(num: tuple[int, ...], den: tuple[int, ...], p: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    require(bool(den), "division by zero polynomial")
    rem = list(num)
    quot = [0] * max(0, len(num) - len(den) + 1)
    den_lc_inv = pow(den[-1], -1, p)
    while len(rem) >= len(den) and rem:
        coeff = rem[-1] * den_lc_inv % p
        shift = len(rem) - len(den)
        quot[shift] = coeff
        for i, den_i in enumerate(den):
            rem[shift + i] = (rem[shift + i] - coeff * den_i) % p
        rem = list(trim(rem, p))
    return trim(quot, p), trim(rem, p)


def verify_case(case: dict[str, Any]) -> None:
    p = case["p"]
    touched = list(case["touched"])
    touched_locator = locator(touched, p)

    quotient = (7, 5, 0, 3)
    h_poly = poly_mul(touched_locator, quotient, p)
    require(all(poly_eval(h_poly, x, p) == 0 for x in touched), "H_i does not vanish on T_i")
    _q, remainder = divmod_poly(h_poly, touched_locator, p)
    require(remainder == (), "vanishing polynomial not divisible by touched locator")

    partial = touched[:-1]
    bad_h = poly_add(h_poly, locator(partial, p), p)
    require(all(poly_eval(bad_h, x, p) == 0 for x in partial), "bad test polynomial setup failed")
    require(poly_eval(bad_h, touched[-1], p) != 0, "bad test polynomial should miss one point")
    _bad_q, bad_remainder = divmod_poly(bad_h, touched_locator, p)
    require(bad_remainder != (), "nonvanishing polynomial should not be divisible")


def main() -> None:
    cert = load_certificate()
    for case in cert["finite_checks"]:
        verify_case(case)
    print(f"PASS: {DAG_NODE} touched-petal divisibility checks passed")


if __name__ == "__main__":
    main()

