#!/usr/bin/env python3
"""Verify the E22 fixed-scale staircase injectivity packet."""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-fixed-scale-staircase-injectivity/"
    "e22_fixed_scale_staircase_injectivity.json"
)
SCHEMA = "e22-fixed-scale-staircase-injectivity-v1"
DAG_NODE = "e22_fixed_scale_staircase_injectivity"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(cert.get("dependencies") == [], "fixed-scale node is a DAG leaf")
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


def poly_mul(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def locator(roots: list[int], p: int) -> tuple[int, ...]:
    poly = (1,)
    for root in roots:
        poly = poly_mul(poly, ((-root) % p, 1), p)
    return poly


def subgroup_domain(p: int, n: int) -> list[int]:
    require((p - 1) % n == 0, "n must divide p-1")
    h = pow(primitive_root(p), (p - 1) // n, p)
    domain = [pow(h, j, p) for j in range(n)]
    require(len(set(domain)) == n, "wrong subgroup order")
    return domain


def quotient_fibers(domain: list[int], m: int, p: int) -> dict[int, list[int]]:
    fibers: dict[int, list[int]] = {}
    for x in domain:
        fibers.setdefault(pow(x, m, p), []).append(x)
    return {z: sorted(fiber) for z, fiber in sorted(fibers.items())}


def recover(
    support: set[int],
    fibers: dict[int, list[int]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    selected = tuple(z for z, fiber in fibers.items() if set(fiber) <= support)
    full_union = {x for z in selected for x in fibers[z]}
    tail = tuple(sorted(support - full_union))
    return tail, selected


def verify_case(p: int, n: int, max_selected: int, max_tail_size: int) -> int:
    domain = subgroup_domain(p, n)
    checks = 0
    for m in [d for d in range(2, n + 1) if n % d == 0]:
        fibers = quotient_fibers(domain, m, p)
        values = list(fibers)
        if len(values) < 3:
            continue
        seen: dict[tuple[int, ...], tuple[tuple[int, ...], tuple[int, ...]]] = {}
        for selected_size in range(1, min(max_selected, len(values)) + 1):
            for selected in itertools.combinations(values, selected_size):
                full = {x for z in selected for x in fibers[z]}
                residual = [x for x in domain if x not in full]
                residual_window = residual[: min(len(residual), 10)]
                for tail_size in range(min(max_tail_size, m - 1, len(residual_window)) + 1):
                    for tail in itertools.combinations(residual_window, tail_size):
                        support = full | set(tail)
                        params = (tuple(sorted(tail)), tuple(sorted(selected)))
                        recovered = recover(support, fibers)
                        require(recovered == params, "fixed-scale recovery failed")
                        poly = locator(sorted(support), p)
                        old = seen.setdefault(poly, params)
                        require(old == params, "same locator produced different parameters")
                        checks += 1
    return checks


def main() -> None:
    cert = load_certificate()
    total = 0
    for case in cert["finite_checks"]:
        total += verify_case(
            case["p"],
            case["n"],
            cert["max_selected_fibers"],
            cert["max_tail_size"],
        )
    print(f"PASS: {DAG_NODE} fixed-scale injectivity checks passed ({total} cases)")


if __name__ == "__main__":
    main()

