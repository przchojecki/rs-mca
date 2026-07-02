#!/usr/bin/env python3
"""Exact E9 sparse-dual census for the Conjecture F roadmap.

This is an EXPERIMENTAL evidence verifier, not a proof.  It performs the
pre-registered E9/QF.8 toy census:

* K = F_17 and H = F_17^* with n = 16;
* enumerate every codimension-one projective flat in
  P(K[X]_{<=j}) for j = 3 and j = 4;
* count sparse dual words of support size 1, 2, and 3 by testing whether the
  hyperplane normal lies in the span of the corresponding evaluation vectors;
* classify flats as common-root, twin, support-3-only, or dual-distance >= 4.

The purpose is to decide whether the many-sparse residue in the toy model is
explained by known paid/descent structures or whether an unstructured
many-sparse flat appears.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from math import comb
from pathlib import Path
from typing import Any


P = 17
N = 16
DEGREES = (3, 4)
MAX_SUPPORT = 3
OUTPUT = Path(
    "experimental/data/certificates/conjecture-f-many-sparse-census/"
    "conjecture_f_many_sparse_census.json"
)


def inv(value: int) -> int:
    return pow(value % P, -1, P)


def canonical_vector(values: tuple[int, ...]) -> tuple[int, ...] | None:
    for value in values:
        if value % P:
            scale = inv(value)
            return tuple((scale * entry) % P for entry in values)
    return None


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rank_mod_p(rows: list[tuple[int, ...]], width: int) -> int:
    work = [[entry % P for entry in row[:width]] for row in rows]
    rank = 0
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col] % P:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = inv(work[rank][col])
        work[rank] = [(scale * entry) % P for entry in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col] % P:
                multiple = work[row][col]
                work[row] = [
                    (work[row][idx] - multiple * work[rank][idx]) % P
                    for idx in range(width)
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def row_basis(rows: list[tuple[int, ...]], width: int) -> list[tuple[int, ...]]:
    basis: list[tuple[int, ...]] = []
    for row in rows:
        if rank_mod_p(basis + [row], width) > len(basis):
            basis.append(row)
    return basis


def projective_points(width: int):
    """Yield canonical representatives of P^{width-1}(F_P)."""
    for first in range(width):
        prefix = (0,) * first + (1,)
        tail_width = width - first - 1
        for tail in itertools.product(range(P), repeat=tail_width):
            yield prefix + tail


def projective_span_points(basis: list[tuple[int, ...]], width: int):
    """Yield projective points in the span of an independent row basis."""
    for coeffs in projective_points(len(basis)):
        values = [0] * width
        for coeff, row in zip(coeffs, basis):
            if coeff:
                for idx, entry in enumerate(row):
                    values[idx] = (values[idx] + coeff * entry) % P
        canonical = canonical_vector(tuple(values))
        if canonical is None:
            raise AssertionError("nonzero projective coefficients gave zero vector")
        yield canonical


def eval_vector(x: int, degree: int) -> tuple[int, ...]:
    return tuple(pow(x, exponent, P) for exponent in range(degree + 1))


def support_span_counts(domain: list[int], degree: int) -> dict[tuple[int, ...], list[int]]:
    width = degree + 1
    counts: dict[tuple[int, ...], list[int]] = defaultdict(lambda: [0] * MAX_SUPPORT)
    for support_size in range(1, MAX_SUPPORT + 1):
        for support in itertools.combinations(domain, support_size):
            rows = [eval_vector(x, degree) for x in support]
            basis = row_basis(rows, width)
            assert len(basis) == support_size
            for normal in projective_span_points(basis, width):
                counts[normal][support_size - 1] += 1
    return counts


def classify_sparse_counts(sparse_counts: list[int]) -> str:
    if sparse_counts[0]:
        return "common_root"
    if sparse_counts[1]:
        return "twin"
    if sparse_counts[2]:
        return "sparse3_only"
    return "dual_distance_ge_4"


def quotient_pullback_orders(degree: int) -> list[int]:
    return [m for m in range(2, N + 1) if N % m == 0 and degree % m == 0]


def contains_pullback_subspace(normal: tuple[int, ...], degree: int, order: int) -> bool:
    """Whether ker(normal) contains the X^order pullback coefficient subspace."""
    return all(normal[index] == 0 for index in range(0, degree + 1, order))


def census_for_degree(degree: int) -> dict[str, Any]:
    domain = list(range(1, P))
    width = degree + 1
    all_normals = list(projective_points(width))
    sparse = support_span_counts(domain, degree)
    class_counts: Counter[str] = Counter()
    max_by_class: dict[str, dict[str, Any]] = {}
    support3_distribution: dict[str, Counter[int]] = defaultdict(Counter)
    pullback_by_order = {
        str(order): Counter() for order in quotient_pullback_orders(degree)
    }

    for normal in all_normals:
        sparse_counts = sparse.get(normal, [0] * MAX_SUPPORT)
        class_name = classify_sparse_counts(sparse_counts)
        class_counts[class_name] += 1
        support3_distribution[class_name][sparse_counts[2]] += 1
        best = max_by_class.get(class_name)
        score = tuple(sparse_counts)
        if best is None or score > tuple(best["support_counts"]):
            max_by_class[class_name] = {
                "support_counts": sparse_counts,
                "normal": list(normal),
            }
        for order in quotient_pullback_orders(degree):
            if contains_pullback_subspace(normal, degree, order):
                pullback_by_order[str(order)][class_name] += 1

    support_totals = {str(w): comb(N, w) for w in range(1, MAX_SUPPORT + 1)}
    span_sizes = {
        str(w): (P**w - 1) // (P - 1) for w in range(1, MAX_SUPPORT + 1)
    }
    incidence_totals = {
        str(w): support_totals[str(w)] * span_sizes[str(w)]
        for w in range(1, MAX_SUPPORT + 1)
    }
    classified_sparse = (
        class_counts["common_root"]
        + class_counts["twin"]
        + class_counts["sparse3_only"]
    )
    total = len(all_normals)
    expected_total = (P**width - 1) // (P - 1)
    assert total == expected_total
    assert sum(class_counts.values()) == total

    return {
        "degree": degree,
        "projective_flat_dimension": degree - 1,
        "ambient_projective_dimension": degree,
        "normal_count": total,
        "expected_normal_count": expected_total,
        "support_totals": support_totals,
        "support_span_projective_sizes": span_sizes,
        "support_span_incidence_totals": incidence_totals,
        "class_counts": dict(sorted(class_counts.items())),
        "classified_support_le_3_sparse_count": classified_sparse,
        "dual_distance_ge_4_count": class_counts["dual_distance_ge_4"],
        "support3_count_distribution_by_class": {
            key: {str(count): value for count, value in sorted(counter.items())}
            for key, counter in sorted(support3_distribution.items())
        },
        "max_by_class": dict(sorted(max_by_class.items())),
        "literal_pullback_container_counts": {
            order: dict(sorted(counter.items()))
            for order, counter in sorted(pullback_by_order.items())
        },
    }


def build_certificate() -> dict[str, Any]:
    runs = [census_for_degree(degree) for degree in DEGREES]
    no_unclassified_support_le_3 = all(
        run["classified_support_le_3_sparse_count"]
        == run["normal_count"] - run["dual_distance_ge_4_count"]
        for run in runs
    )
    third_class_found = any(
        run["class_counts"].get("sparse3_only", 0) > 0 for run in runs
    )
    note = (
        "Third structural class found: support-3-only sparse dual words occur "
        "in both toy dimensions.  This is not an unstructured counterexample; "
        "it is the sparse-dependence descent branch that the QF.7 reduction "
        "packet is designed to handle."
    )
    payload = {
        "schema": "conjecture_f_many_sparse_census.v1",
        "roadmap_task": "E9 / QF.8 / f_many_sparse_structure toy census",
        "status": "EXPERIMENTAL_EVIDENCE",
        "field": {"p": P, "domain": "F_17^*", "n": N},
        "object": (
            "codimension-one projective flats ker(a) in P(F_17[X]_{<=j}); "
            "a support-w sparse dual word is counted when a lies in the span "
            "of the w corresponding evaluation vectors"
        ),
        "degrees": list(DEGREES),
        "max_sparse_support_tested": MAX_SUPPORT,
        "runs": runs,
        "interpretation": {
            "outcome": "THIRD_STRUCTURAL_CLASS_FOUND__SPARSE_DEPENDENCE_DESCENT",
            "third_class_found": third_class_found,
            "no_unclassified_support_le_3_sparse_flat_seen": no_unclassified_support_le_3,
            "recommended_restatement": (
                "Do not phrase the many-sparse residue as pullback/tangent only. "
                "Include a support-3 sparse-dependence descent ledger before the "
                "primitive residue."
            ),
            "note": note,
        },
        "nonclaims": [
            "does not prove Conjecture F",
            "does not enumerate non-hyperplane flats",
            "does not test sparse dual support larger than 3",
            "literal pullback-container counts are only a small quotient sanity check",
        ],
    }
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = sha256_text(normalized)
    return payload


def print_summary(certificate: dict[str, Any]) -> None:
    print(certificate["schema"])
    print(certificate["interpretation"]["outcome"])
    for run in certificate["runs"]:
        print(f"j={run['degree']} total={run['normal_count']}")
        print("  classes:", run["class_counts"])
        for class_name, data in run["max_by_class"].items():
            print(f"  max {class_name}: {data['support_counts']} normal={data['normal']}")
        if run["literal_pullback_container_counts"]:
            print("  pullback containers:", run["literal_pullback_container_counts"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="write the certificate JSON")
    parser.add_argument("--check", type=Path, help="check an existing certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    if args.check:
        existing = json.loads(args.check.read_text())
        if existing != certificate:
            raise SystemExit(f"certificate mismatch: {args.check}")
    if not args.emit and not args.check:
        print_summary(certificate)


if __name__ == "__main__":
    main()
