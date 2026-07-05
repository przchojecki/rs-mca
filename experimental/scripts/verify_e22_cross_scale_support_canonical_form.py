#!/usr/bin/env python3
"""Verify the E22 cross-scale support canonical-form packet."""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-cross-scale-support-canonical-form/"
    "e22_cross_scale_support_canonical_form.json"
)
ROOTSET_CERT = ROOT / (
    "experimental/data/certificates/e22-cross-scale-rootset-recovery/"
    "e22_cross_scale_rootset_recovery.json"
)
SCHEMA = "e22-cross-scale-support-canonical-form-v1"
DAG_NODE = "e22_cross_scale_support_canonical_form"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(
        cert.get("dependencies") == ["e22_cross_scale_rootset_recovery"],
        "unexpected dependency list",
    )

    dep = json.loads(ROOTSET_CERT.read_text(encoding="utf-8"))
    require(dep.get("dag_node") == "e22_cross_scale_rootset_recovery", "bad dependency")
    require(dep.get("status") == "PROVED", "dependency must be PROVED")
    return cert


def fibers(n: int, m: int) -> list[frozenset[int]]:
    """Return quotient fibers in exponent coordinates for a cyclic domain."""

    require(n % m == 0, "m must divide n")
    step = n // m
    return [frozenset(range(r, n, step)) for r in range(step)]


def recover(n: int, m: int, support: set[int]) -> tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]:
    full = tuple(fiber for fiber in fibers(n, m) if fiber <= support)
    full_union = set().union(*full) if full else set()
    tail = tuple(sorted(support - full_union))
    selected = tuple(tuple(sorted(fiber)) for fiber in full)
    return tail, selected


def canonical(
    n: int,
    moduli: list[int],
    support: set[int],
) -> dict[int, tuple[tuple[int, ...], tuple[tuple[int, ...], ...]]]:
    out = {}
    for m in moduli:
        tail, selected = recover(n, m, support)
        if len(tail) < m:
            out[m] = (tail, selected)
    return out


def generated_supports(n: int, moduli: list[int]) -> list[tuple[int, set[int], tuple[int, ...]]]:
    supports: list[tuple[int, set[int], tuple[int, ...]]] = []
    for m in moduli:
        f = fibers(n, m)
        for selected_size in (1, 2):
            for selected_indices in itertools.combinations(range(min(len(f), 8)), selected_size):
                full = set().union(*(f[i] for i in selected_indices))
                residual = [x for x in range(n) if x not in full]
                for tail_size in range(min(m - 1, 2, len(residual)) + 1):
                    for tail in itertools.combinations(residual[:8], tail_size):
                        supports.append((m, full | set(tail), tuple(sorted(tail))))
    return supports


def verify_case(n: int, moduli: list[int]) -> int:
    checks = 0
    for original_m, support, original_tail in generated_supports(n, moduli):
        recovered_tail, selected = recover(n, original_m, support)
        require(recovered_tail == original_tail, "original scale tail not recovered")
        reconstructed = set(recovered_tail)
        for fiber in selected:
            reconstructed.update(fiber)
        require(reconstructed == support, "original scale support not reconstructed")

        canon = canonical(n, moduli, support)
        require(original_m in canon, "original scale missing from canonical data")
        require(canon == canonical(n, moduli, set(support)), "canonical data not support-only")

        for m, (tail, full_fibers) in canon.items():
            require(len(tail) < m, "canonical candidate violates tail bound")
            rebuilt = set(tail)
            for fiber in full_fibers:
                rebuilt.update(fiber)
            require(rebuilt == support, "canonical candidate does not rebuild support")

        checks += 1
    return checks


def main() -> None:
    cert = load_certificate()
    total = 0
    for case in cert["finite_checks"]:
        total += verify_case(case["n"], case["moduli"])
    print(f"PASS: {DAG_NODE} canonical support checks passed ({total} supports)")


if __name__ == "__main__":
    main()

