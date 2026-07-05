#!/usr/bin/env python3
"""Verify the E22 tail-coset locator algebra packet."""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-tail-coset-locator-algebra/"
    "e22_tail_coset_locator_algebra.json"
)
SCHEMA = "e22-tail-coset-locator-algebra-v1"
DAG_NODE = "e22_tail_coset_locator_algebra"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(cert.get("dependencies") == [], "tail-coset locator node is a DAG leaf")
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


def locator(roots: list[int], p: int) -> tuple[int, ...]:
    poly = (1,)
    for root in roots:
        poly = poly_mul(poly, ((-root) % p, 1), p)
    return poly


def compose_xm(poly: tuple[int, ...], m: int, p: int) -> tuple[int, ...]:
    out = [0] * ((len(poly) - 1) * m + 1)
    for i, coeff in enumerate(poly):
        out[i * m] = coeff
    return trim(out, p)


def subgroup_domain(p: int, n: int) -> list[int]:
    require((p - 1) % n == 0, "n must divide p-1")
    h = pow(primitive_root(p), (p - 1) // n, p)
    domain = [pow(h, j, p) for j in range(n)]
    require(len(set(domain)) == n, "wrong subgroup order")
    return domain


def quotient_fibers(domain: list[int], m: int, p: int) -> dict[int, list[int]]:
    out: dict[int, list[int]] = {}
    for x in domain:
        out.setdefault(pow(x, m, p), []).append(x)
    return {z: sorted(fiber) for z, fiber in sorted(out.items())}


def top_subleading(poly: tuple[int, ...], count: int) -> tuple[int, ...]:
    degree = len(poly) - 1
    return tuple(poly[degree - i] if degree - i >= 0 else 0 for i in range(1, count + 1))


def verify_case(p: int, n: int, max_tail_size: int, max_selected: int) -> int:
    domain = subgroup_domain(p, n)
    checks = 0
    for m in (d for d in range(2, n + 1) if n % d == 0):
        fibers = quotient_fibers(domain, m, p)
        quotient_values = sorted(fibers)
        if len(quotient_values) < 3:
            continue
        tail_q = quotient_values[0]
        candidates = quotient_values[1:]
        for tail_size in range(min(m - 1, max_tail_size) + 1):
            tail = fibers[tail_q][:tail_size]
            tail_locator = locator(tail, p)
            for selected_count in range(1, min(max_selected, len(candidates)) + 1):
                signatures = set()
                for selected in itertools.combinations(candidates, selected_count):
                    roots = list(tail)
                    for z in selected:
                        roots.extend(fibers[z])
                    direct = locator(roots, p)
                    quotient_locator = locator(list(selected), p)
                    staircase = poly_mul(tail_locator, compose_xm(quotient_locator, m, p), p)
                    require(direct == staircase, "tail-coset locator identity failed")
                    signatures.add(top_subleading(staircase, m - 1))
                    checks += 1
                require(len(signatures) == 1, "top coefficients depend on selected quotient values")
    return checks


def main() -> None:
    cert = load_certificate()
    total = 0
    for case in cert["finite_checks"]:
        for n in case["n_values"]:
            total += verify_case(
                case["p"],
                n,
                case["max_tail_size"],
                case["max_selected_fibers"],
            )
    print(f"PASS: {DAG_NODE} tail-coset locator checks passed ({total} cases)")


if __name__ == "__main__":
    main()

