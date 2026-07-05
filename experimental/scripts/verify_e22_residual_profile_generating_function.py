#!/usr/bin/env python3
"""Verify the E22 residual-profile generating-function packet."""

from __future__ import annotations

import json
from math import comb
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-residual-profile-generating-function/"
    "e22_residual_profile_generating_function.json"
)
NESTED_CERT = ROOT / (
    "experimental/data/certificates/e22-overlap-nested-fiber-residual-identity/"
    "e22_overlap_nested_fiber_residual_identity.json"
)
SCHEMA = "e22-residual-profile-generating-function-v1"
DAG_NODE = "e22_residual_profile_generating_function"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(
        cert.get("dependencies") == ["e22_overlap_nested_fiber_residual_identity"],
        "unexpected dependency list",
    )
    dep = json.loads(NESTED_CERT.read_text(encoding="utf-8"))
    require(dep.get("dag_node") == "e22_overlap_nested_fiber_residual_identity", "bad dependency")
    require(dep.get("status") == "PROVED", "dependency must be PROVED")
    return cert


def blocks(n: int, size: int) -> list[frozenset[int]]:
    return [frozenset(range(start, start + size)) for start in range(0, n, size)]


def all_subsets(n: int) -> Iterable[frozenset[int]]:
    for mask in range(1 << n):
        yield frozenset(i for i in range(n) if (mask >> i) & 1)


def union(sets: Iterable[frozenset[int]]) -> frozenset[int]:
    out: set[int] = set()
    for item in sets:
        out.update(item)
    return frozenset(out)


def canonical_tail(support: frozenset[int], n: int, size: int) -> frozenset[int]:
    full = [block for block in blocks(n, size) if block <= support]
    return support - union(full)


def convolve(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            out[i + j] += av * bv
    return out


def tail_coeff(unselected_fibers: int, fine_size: int, tail_size: int) -> int:
    base = [comb(fine_size, a) for a in range(fine_size)]
    poly = [1]
    for _ in range(unselected_fibers):
        poly = convolve(poly, base)
    return poly[tail_size] if tail_size < len(poly) else 0


def parent_profile_counts(parent_count: int, q: int) -> dict[tuple[int, int], int]:
    profile: dict[tuple[int, int], int] = {(0, 0): 1}
    options = [(1, 0, 1)] + [(0, s, comb(q, s)) for s in range(q)]
    for _ in range(parent_count):
        next_profile: dict[tuple[int, int], int] = {}
        for (c0, r0), count0 in profile.items():
            for dc, dr, ways in options:
                key = (c0 + dc, r0 + dr)
                next_profile[key] = next_profile.get(key, 0) + count0 * ways
        profile = next_profile
    return profile


def formula_count(n: int, fine_size: int, coarse_size: int) -> int:
    parent_count = n // coarse_size
    q = coarse_size // fine_size
    fine_count = n // fine_size
    total = 0
    for (complete, residual), selected_ways in parent_profile_counts(
        parent_count, q
    ).items():
        selected_fine = complete * q + residual
        unselected = fine_count - selected_fine
        tail_limit = min(fine_size, coarse_size - fine_size * residual)
        for tail_size in range(max(0, tail_limit)):
            total += selected_ways * tail_coeff(unselected, fine_size, tail_size)
    return total


def brute_count(n: int, fine_size: int, coarse_size: int) -> int:
    total = 0
    for support in all_subsets(n):
        fine_tail = canonical_tail(support, n, fine_size)
        if len(fine_tail) >= fine_size:
            continue
        coarse_tail = canonical_tail(support, n, coarse_size)
        if len(coarse_tail) < coarse_size:
            total += 1
    return total


def verify_pair(n: int, fine_size: int, coarse_size: int) -> None:
    require(
        formula_count(n, fine_size, coarse_size) == brute_count(n, fine_size, coarse_size),
        "generating function count disagrees with brute force",
    )


def main() -> None:
    cert = load_certificate()
    total = 0
    for case in cert["finite_checks"]:
        n = case["n"]
        for fine_size in case["fine_sizes"]:
            for coarse_size in case["coarse_sizes"]:
                if fine_size < coarse_size and coarse_size % fine_size == 0:
                    verify_pair(n, fine_size, coarse_size)
                    total += 1
    print(f"PASS: {DAG_NODE} generating-function checks passed ({total} scale pairs)")


if __name__ == "__main__":
    main()

