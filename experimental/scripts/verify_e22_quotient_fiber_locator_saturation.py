#!/usr/bin/env python3
"""Verify the E22 quotient-fiber locator saturation packet.

The mathematical proof is in the paired roadmap note.  This script checks the
stored certificate metadata and replays small exact finite-field instances of
the factor/full-fiber equivalence.  It is intentionally light and avoids any
large deployed-row enumeration.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-quotient-fiber-locator-saturation/"
    "e22_quotient_fiber_locator_saturation.json"
)
SCHEMA = "e22-quotient-fiber-locator-saturation-v1"
DAG_NODE = "e22_fiber_locator_saturation"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(cert.get("dependencies") == [], "leaf node should have no dependencies")
    return cert


def prime_factors(n: int) -> set[int]:
    factors: set[int] = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise AssertionError(f"no primitive root found for {p}")


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return out


def locator(roots: list[int], p: int) -> list[int]:
    poly = [1]
    for root in roots:
        poly = poly_mul(poly, [(-root) % p, 1], p)
    return poly


def xm_minus_z(m: int, z: int, p: int) -> list[int]:
    return [(-z) % p] + [0] * (m - 1) + [1]


def eval_poly(poly: list[int], x: int, p: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % p
    return acc


def subgroup_domain(p: int, n: int) -> list[int]:
    require((p - 1) % n == 0, "n must divide p-1")
    h = pow(primitive_root(p), (p - 1) // n, p)
    domain = [pow(h, j, p) for j in range(n)]
    require(len(set(domain)) == n, "wrong subgroup order")
    return domain


def verify_case(p: int, n: int) -> int:
    domain = subgroup_domain(p, n)
    checks = 0
    for m in [2**i for i in range(1, n.bit_length()) if 2**i <= n]:
        values = sorted({pow(x, m, p) for x in domain})
        for z in values:
            fiber = [x for x in domain if pow(x, m, p) == z]
            require(len(fiber) == m, f"wrong fiber size for p={p}, n={n}, m={m}")
            require(locator(fiber, p) == xm_minus_z(m, z, p), "bad fiber locator")

            missing_support = [x for x in domain if x != fiber[0]]
            missing_locator = locator(missing_support, p)
            require(
                eval_poly(missing_locator, fiber[0], p) != 0,
                "support missing a fiber point should not be divisible",
            )
            checks += 1
    return checks


def main() -> None:
    cert = load_certificate()
    total = 0
    for case in cert["finite_checks"]:
        total += verify_case(case["p"], case["n"])
    print(f"PASS: {DAG_NODE} quotient-fiber locator checks passed ({total} fibers)")


if __name__ == "__main__":
    main()

