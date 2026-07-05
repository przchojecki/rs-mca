#!/usr/bin/env python3
"""Verify the E22 agreement cofactor-equation packet."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-agreement-cofactor-equations/"
    "e22_agreement_cofactor_equations.json"
)
SCHEMA = "e22-agreement-cofactor-equations-v1"
DAG_NODE = "e22_agreement_cofactor_equations"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(cert.get("dependencies") == [], "cofactor-equation node is a DAG leaf")
    return cert


def trim(poly: list[int], p: int) -> tuple[int, ...]:
    out = [x % p for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def poly_mul(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out, p)


def poly_add(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim(out, p)


def poly_scale(poly: tuple[int, ...], scalar: int, p: int) -> tuple[int, ...]:
    return trim([scalar * coeff for coeff in poly], p)


def poly_eval(poly: tuple[int, ...], x: int, p: int) -> int:
    value = 0
    for coeff in reversed(poly):
        value = (value * x + coeff) % p
    return value


def locator(points: list[int], p: int) -> tuple[int, ...]:
    out = (1,)
    for x in points:
        out = poly_mul(out, ((-x) % p, 1), p)
    return out


def interpolate(points: list[tuple[int, int]], p: int) -> tuple[int, ...]:
    poly: tuple[int, ...] = (0,)
    for i, (x_i, y_i) in enumerate(points):
        basis: tuple[int, ...] = (1,)
        denom = 1
        for j, (x_j, _y_j) in enumerate(points):
            if i == j:
                continue
            basis = poly_mul(basis, ((-x_j) % p, 1), p)
            denom = denom * (x_i - x_j) % p
        term = poly_scale(basis, y_i * pow(denom, -1, p), p)
        poly = poly_add(poly, term, p)
    return poly


def verify_case(case: dict[str, Any]) -> int:
    p = case["p"]
    core = list(case["core"])
    background = list(case["background"])
    petal = list(case["petal"])
    scalar = case["scalar"]

    z_core = core[:2]
    z_background = background[:2]
    z_all = z_core + z_background
    core_not_z = [x for x in core if x not in set(z_core)]

    l_z = locator(z_all, p)
    l_z_not_c = locator(z_background, p)
    l_c_not_z = locator(core_not_z, p)
    l_core = locator(core, p)

    # Choose U by the cofactor equation on the petal agreement points, then
    # build f=U L_Z and verify both the original petal agreement and the
    # cancelled cofactor equation.
    values = [
        (x, scalar * poly_eval(l_c_not_z, x, p) * pow(poly_eval(l_z_not_c, x, p), -1, p) % p)
        for x in petal
    ]
    u_poly = interpolate(values, p)
    f_poly = poly_mul(u_poly, l_z, p)

    checks = 0
    for x in petal:
        require(
            poly_eval(f_poly, x, p) == scalar * poly_eval(l_core, x, p) % p,
            "constructed codeword does not agree with petal value",
        )
        left = poly_eval(u_poly, x, p) * poly_eval(l_z_not_c, x, p) % p
        right = scalar * poly_eval(l_c_not_z, x, p) % p
        require(left == right, "cofactor equation failed after cancellation")
        checks += 1
    return checks


def main() -> None:
    cert = load_certificate()
    total = sum(verify_case(case) for case in cert["finite_checks"])
    print(f"PASS: {DAG_NODE} cofactor equations checked ({total} petal agreements)")


if __name__ == "__main__":
    main()

