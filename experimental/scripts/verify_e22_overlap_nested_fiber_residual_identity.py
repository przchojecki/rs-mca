#!/usr/bin/env python3
"""Verify the E22 nested-fiber residual identity packet."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-overlap-nested-fiber-residual-identity/"
    "e22_overlap_nested_fiber_residual_identity.json"
)
CANONICAL_CERT = ROOT / (
    "experimental/data/certificates/e22-cross-scale-support-canonical-form/"
    "e22_cross_scale_support_canonical_form.json"
)
SCHEMA = "e22-overlap-nested-fiber-residual-identity-v1"
DAG_NODE = "e22_overlap_nested_fiber_residual_identity"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(
        cert.get("dependencies") == ["e22_cross_scale_support_canonical_form"],
        "unexpected dependency list",
    )
    dep = json.loads(CANONICAL_CERT.read_text(encoding="utf-8"))
    require(dep.get("dag_node") == "e22_cross_scale_support_canonical_form", "bad dependency")
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


def parent_index(block: frozenset[int], coarse_size: int) -> int:
    return min(block) // coarse_size


def verify_pair(n: int, fine_size: int, coarse_size: int) -> int:
    fine_blocks = blocks(n, fine_size)
    coarse_blocks = blocks(n, coarse_size)
    fine_children = {
        c_idx: [block for block in fine_blocks if block <= coarse]
        for c_idx, coarse in enumerate(coarse_blocks)
    }

    checks = 0
    for support in all_subsets(n):
        selected_fine = [block for block in fine_blocks if block <= support]
        selected_set = set(selected_fine)
        fine_tail = canonical_tail(support, n, fine_size)

        coarse_full_from_support = {
            c_idx for c_idx, coarse in enumerate(coarse_blocks) if coarse <= support
        }
        coarse_full_from_children = {
            c_idx
            for c_idx, children in fine_children.items()
            if all(child in selected_set for child in children)
        }
        require(
            coarse_full_from_support == coarse_full_from_children,
            "coarse full-fiber recovery disagrees with fine children",
        )

        residual_fine = [
            block
            for block in selected_fine
            if parent_index(block, coarse_size) not in coarse_full_from_children
        ]
        coarse_tail = canonical_tail(support, n, coarse_size)
        residual_size = len(fine_tail) + fine_size * len(residual_fine)

        require(len(coarse_tail) == residual_size, "residual tail formula failed")
        require(
            (len(coarse_tail) < coarse_size) == (residual_size < coarse_size),
            "raw coarse admissibility criterion failed",
        )
        checks += 1
    return checks


def main() -> None:
    cert = load_certificate()
    total = 0
    for case in cert["finite_checks"]:
        n = case["n"]
        for fine_size in case["fine_sizes"]:
            for coarse_size in case["coarse_sizes"]:
                if fine_size < coarse_size and coarse_size % fine_size == 0:
                    total += verify_pair(n, fine_size, coarse_size)
    print(f"PASS: {DAG_NODE} nested-fiber residual checks passed ({total} supports)")


if __name__ == "__main__":
    main()

