#!/usr/bin/env python3
"""Verify the conic-endpoint target arithmetic and design guardrails."""

from __future__ import annotations
class VerificationError(RuntimeError):
    """Raised when an exact verifier condition fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(str(message))


if not __debug__:
    raise RuntimeError(
        "Verifier refuses optimized execution; rerun without Python -O."
    )



import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "pole_disjoint_conic_endpoint_target_certificate.json"


def facet_family(parts: list[set[int]]) -> list[frozenset[int]]:
    blocks: list[frozenset[int]] = []
    for part in parts:
        for point in sorted(part):
            blocks.append(frozenset(part - {point}))
    return blocks


def replication(blocks: list[frozenset[int]], points: range) -> list[int]:
    return [sum(point in block for block in blocks) for point in points]


def maximum_clique_size(
    blocks: list[frozenset[int]], intersection: int
) -> int:
    adjacency = [set() for _ in blocks]
    for left, right in combinations(range(len(blocks)), 2):
        if len(blocks[left] & blocks[right]) == intersection:
            adjacency[left].add(right)
            adjacency[right].add(left)

    best = 0

    def expand(size: int, candidates: list[int]) -> None:
        nonlocal best
        if size + len(candidates) <= best:
            return
        if not candidates:
            best = max(best, size)
            return
        while candidates:
            if size + len(candidates) <= best:
                return
            vertex = candidates.pop()
            expand(
                size + 1,
                [
                    other
                    for other in candidates
                    if other in adjacency[vertex]
                ],
            )
        best = max(best, size)

    expand(0, list(range(len(blocks))))
    return best


def endpoint_arithmetic() -> dict[str, int]:
    a = 12
    regular_roots = 69
    postcritical_degree = 59
    selected_parameters = 2 * postcritical_degree + 2
    coordinate_pole_degree = 2 * a
    locator_degree = a - 1
    vertical_degree = coordinate_pole_degree - 2
    total_incidence = selected_parameters * locator_degree
    active_roots = total_incidence // vertical_degree
    inactive_roots = regular_roots - active_roots
    quotient_t_degree = regular_roots - locator_degree
    quotient_lambda_degree = (
        selected_parameters - vertical_degree
    )
    require(
        selected_parameters == 120,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:80',
    )
    require(
        coordinate_pole_degree == 24,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:81',
    )
    require(
        vertical_degree == 22,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:82',
    )
    require(
        total_incidence == 1320,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:83',
    )
    require(
        active_roots == 60,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:84',
    )
    require(
        inactive_roots == 9,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:85',
    )
    require(
        quotient_t_degree == 58,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:86',
    )
    require(
        quotient_lambda_degree == 98,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:87',
    )
    return {
        "a": a,
        "regular_roots": regular_roots,
        "postcritical_degree": postcritical_degree,
        "selected_parameters": selected_parameters,
        "coordinate_pole_degree": coordinate_pole_degree,
        "locator_degree": locator_degree,
        "vertical_degree": vertical_degree,
        "total_incidence": total_incidence,
        "active_roots": active_roots,
        "inactive_roots": inactive_roots,
        "remainder_degree": inactive_roots,
        "quotient_t_degree": quotient_t_degree,
        "quotient_lambda_degree": quotient_lambda_degree,
    }


def canonical_model() -> dict[str, object]:
    points = range(60)
    first = [
        set(range(12 * group, 12 * (group + 1)))
        for group in range(5)
    ]
    second = [
        {residue + 5 * index for index in range(12)}
        for residue in range(5)
    ]
    blocks = facet_family(first) + facet_family(second)
    require(
        len(blocks) == 120,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:116',
    )
    require(
        len(set(blocks)) == 120,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:117',
    )
    require(
        {len(block) for block in blocks} == {11},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:118',
    )
    degrees = replication(blocks, points)
    require(
        set(degrees) == {22},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:120',
    )
    clique = maximum_clique_size(blocks, 10)
    require(
        clique == 12,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:122',
    )
    return {
        "points": 60,
        "blocks": len(blocks),
        "block_size": 11,
        "replication_min": min(degrees),
        "replication_max": max(degrees),
        "facet_groups": 10,
        "maximum_ten_intersection_clique": clique,
    }


def design_only_counterexample() -> dict[str, object]:
    points = range(60)
    first = [
        frozenset((shift + offset) % 60 for offset in range(11))
        for shift in points
    ]
    second = [
        frozenset((shift + 2 * offset) % 60 for offset in range(11))
        for shift in points
    ]
    blocks = first + second
    require(
        len(blocks) == 120,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:145',
    )
    require(
        len(set(blocks)) == 120,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:146',
    )
    require(
        {len(block) for block in blocks} == {11},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:147',
    )
    degrees = replication(blocks, points)
    require(
        set(degrees) == {22},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:149',
    )
    clique = maximum_clique_size(blocks, 10)
    require(
        clique == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:151',
    )
    return {
        "construction": (
            "translates_of_{0,...,10}_and_{0,2,...,20}_mod_60"
        ),
        "points": 60,
        "blocks": len(blocks),
        "block_size": 11,
        "replication_min": min(degrees),
        "replication_max": max(degrees),
        "maximum_ten_intersection_clique": clique,
        "contains_canonical_facet_family": clique >= 12,
    }


def small_analogue() -> dict[str, object]:
    points = range(8)
    first = [{0, 1, 2, 3}, {4, 5, 6, 7}]
    second = [{0, 2, 4, 6}, {1, 3, 5, 7}]
    blocks = facet_family(first) + facet_family(second)
    degrees = replication(blocks, points)
    require(
        len(blocks) == 16,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:172',
    )
    require(
        len(set(blocks)) == 16,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:173',
    )
    require(
        {len(block) for block in blocks} == {3},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:174',
    )
    require(
        set(degrees) == {6},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:175',
    )
    return {
        "a": 4,
        "q": 2,
        "selected_roots": 9,
        "active_roots": 8,
        "inactive_roots": 1,
        "blocks": len(blocks),
        "block_size": 3,
        "replication": degrees[0],
    }


def payload() -> dict[str, object]:
    result: dict[str, object] = {
        "status": "TARGET_OPEN_DESIGN_ONLY_ROUTE_CUT_PROVED",
        "endpoint_arithmetic": endpoint_arithmetic(),
        "expected_two_template_model": canonical_model(),
        "design_only_counterexample": design_only_counterexample(),
        "small_analogue": small_analogue(),
        "claims": {
            "endpoint_identity": "PROVED_UPSTREAM",
            "endpoint_1_design": "PROVED_UPSTREAM",
            "design_implies_two_templates": "FALSE",
            "source_coupled_endpoint_classification": "OPEN",
            "same_record_owner_payment": "OPEN",
        },
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def validate(data: dict[str, object]) -> None:
    arithmetic = data["endpoint_arithmetic"]
    require(
        arithmetic['selected_parameters'] == 120,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:212',
    )
    require(
        arithmetic['active_roots'] == 60,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:213',
    )
    require(
        arithmetic['inactive_roots'] == 9,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:214',
    )
    require(
        arithmetic['vertical_degree'] == 22,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:215',
    )
    require(
        arithmetic['quotient_t_degree'] == 58,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:216',
    )
    require(
        arithmetic['quotient_lambda_degree'] == 98,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:217',
    )

    model = data["expected_two_template_model"]
    require(
        model['blocks'] == 120,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:220',
    )
    require(
        model['replication_min'] == 22,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:221',
    )
    require(
        model['replication_max'] == 22,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:222',
    )
    require(
        model['maximum_ten_intersection_clique'] == 12,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:223',
    )

    counterexample = data["design_only_counterexample"]
    require(
        counterexample['blocks'] == 120,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:226',
    )
    require(
        counterexample['replication_min'] == 22,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:227',
    )
    require(
        counterexample['replication_max'] == 22,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:228',
    )
    require(
        counterexample['maximum_ten_intersection_clique'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:229',
    )
    require(
        counterexample['contains_canonical_facet_family'] is False,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:230',
    )

    claims = data["claims"]
    require(
        claims['source_coupled_endpoint_classification'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:233',
    )
    require(
        claims['same_record_owner_payment'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:234',
    )

    supplied_hash = data["payload_sha256"]
    unhashed = dict(data)
    del unhashed["payload_sha256"]
    canonical = json.dumps(
        unhashed, sort_keys=True, separators=(",", ":")
    ).encode()
    require(
        supplied_hash == hashlib.sha256(canonical).hexdigest(),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:242',
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    data = payload()
    validate(data)
    if args.emit:
        CERTIFICATE.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        checked = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        require(
            checked == data,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_pole_disjoint_conic_endpoint_target.py:261',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["claims"]["source_coupled_endpoint_classification"] = (
            "PROVED"
        )
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("status tamper was not rejected")

    print("endpoint arithmetic: PASS")
    print("canonical two-template model: PASS")
    print("deployed-parameter design-only route cut: PASS")
    print("small endpoint analogue: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
