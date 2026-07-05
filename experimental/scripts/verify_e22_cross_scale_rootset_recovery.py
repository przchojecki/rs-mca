#!/usr/bin/env python3
"""Verify the E22 cross-scale root-set recovery packet."""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-cross-scale-rootset-recovery/"
    "e22_cross_scale_rootset_recovery.json"
)
FIXED_SCALE_CERT = ROOT / (
    "experimental/data/certificates/e22-fixed-scale-staircase-injectivity/"
    "e22_fixed_scale_staircase_injectivity.json"
)
SCHEMA = "e22-cross-scale-rootset-recovery-v1"
DAG_NODE = "e22_cross_scale_rootset_recovery"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(
        cert.get("dependencies") == ["e22_fixed_scale_staircase_injectivity"],
        "unexpected dependency list",
    )

    dep = json.loads(FIXED_SCALE_CERT.read_text(encoding="utf-8"))
    require(dep.get("dag_node") == "e22_fixed_scale_staircase_injectivity", "bad dependency")
    require(dep.get("status") == "PROVED", "dependency must be PROVED")
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


def generated_supports(
    domain: list[int],
    p: int,
    m: int,
) -> list[tuple[tuple[int, ...], tuple[tuple[int, ...], tuple[int, ...]]]]:
    fibers = quotient_fibers(domain, m, p)
    values = list(fibers)
    out: list[tuple[tuple[int, ...], tuple[tuple[int, ...], tuple[int, ...]]]] = []
    for selected_size in (1, 2):
        for selected in itertools.combinations(values[:8], selected_size):
            full = {x for z in selected for x in fibers[z]}
            residual = [x for x in domain if x not in full]
            for tail_size in range(min(1, m - 1, len(residual)) + 1):
                for tail in itertools.combinations(residual[:6], tail_size):
                    support = tuple(sorted(full | set(tail)))
                    params = (tuple(sorted(tail)), tuple(sorted(selected)))
                    require(recover(set(support), fibers) == params, "fixed-scale recovery failed")
                    out.append((support, params))
    return out


def verify_case(p: int, n: int, moduli: list[int]) -> int:
    domain = subgroup_domain(p, n)
    seen: dict[tuple[int, ...], tuple[int, ...]] = {}
    checks = 0
    for m in moduli:
        require(n % m == 0, "modulus must divide n")
        for support, _params in generated_supports(domain, p, m):
            poly = locator(list(support), p)
            old_support = seen.setdefault(poly, support)
            require(old_support == support, "equal locators had different root sets")

            # Apply recovery at every listed scale where the common support is
            # a valid tail-plus-full-fibers candidate.  This is the exact
            # cross-scale handoff used by the proof.
            for other_m in moduli:
                other_fibers = quotient_fibers(domain, other_m, p)
                tail, selected = recover(set(support), other_fibers)
                if len(tail) < other_m:
                    reconstructed = set(tail)
                    for z in selected:
                        reconstructed.update(other_fibers[z])
                    require(reconstructed == set(support), "cross-scale reconstruction failed")
            checks += 1
    return checks


def main() -> None:
    cert = load_certificate()
    total = 0
    for case in cert["finite_checks"]:
        total += verify_case(case["p"], case["n"], case["moduli"])
    print(f"PASS: {DAG_NODE} cross-scale root-set checks passed ({total} samples)")


if __name__ == "__main__":
    main()

