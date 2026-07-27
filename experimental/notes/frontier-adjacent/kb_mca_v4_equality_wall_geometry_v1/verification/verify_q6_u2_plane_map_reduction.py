#!/usr/bin/env python3
"""Verify the exact finite arithmetic in the Q=6,s=6,u=2 reduction."""

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
import copy
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "q6_u2_plane_map_reduction_certificate.json"
PRIME = 101


def determinant3(rows: list[list[int]]) -> int:
    return (
        rows[0][0]
        * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1])
        - rows[0][1]
        * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0])
        + rows[0][2]
        * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0])
    ) % PRIME


def cross(left: list[int], right: list[int]) -> list[int]:
    return [
        (left[1] * right[2] - left[2] * right[1]) % PRIME,
        (left[2] * right[0] - left[0] * right[2]) % PRIME,
        (left[0] * right[1] - left[1] * right[0]) % PRIME,
    ]


def normalize(vector: list[int]) -> list[int]:
    for entry in vector:
        if entry:
            scale = pow(entry, PRIME - 2, PRIME)
            return [(scale * value) % PRIME for value in vector]
    raise VerificationError("cannot normalize the zero vector")


def line_arrangement() -> dict[str, object]:
    source_labels = list(range(1, 7))
    lines = [
        [label * label % PRIME, label, 1]
        for label in source_labels
    ]
    triple_determinants = [
        determinant3([lines[i], lines[j], lines[k]])
        for i, j, k in itertools.combinations(range(6), 3)
    ]
    require(
        all((value != 0 for value in triple_determinants)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:56',
    )

    intersections: list[list[int]] = []
    for i, j in itertools.combinations(range(6), 2):
        point = normalize(cross(lines[i], lines[j]))
        expected = normalize(
            [
                1,
                -(source_labels[i] + source_labels[j]) % PRIME,
                source_labels[i] * source_labels[j] % PRIME,
            ]
        )
        require(
            point == expected,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:68',
        )
        intersections.append(point)
    require(
        len({tuple(point) for point in intersections}) == 15,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:70',
    )
    return {
        "field": PRIME,
        "source_labels": source_labels,
        "evaluation_lines": 6,
        "triple_determinants_checked": len(triple_determinants),
        "triple_concurrency": False,
        "pair_intersections": len(intersections),
        "distinct_split_quadratics": len(
            {tuple(point) for point in intersections}
        ),
    }


def incidence_ledger() -> dict[str, object]:
    common_divisor_degree = 10
    roots_per_common_fiber = 2
    owned_free_edges = 4
    row_quartics = 6
    degree_per_row = 4
    common_incidence = (
        common_divisor_degree * roots_per_common_fiber
    )
    total = common_incidence + owned_free_edges
    require(
        total == row_quartics * degree_per_row,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:94',
    )

    distributions = [
        values
        for values in itertools.product(range(3), repeat=6)
        if sum(values) == owned_free_edges
    ]
    minimum_zero_rows = min(
        sum(value == 0 for value in values)
        for values in distributions
    )
    require(
        minimum_zero_rows == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:105',
    )
    exactly_two_zero_rows = [
        values
        for values in distributions
        if sum(value == 0 for value in values) == 2
    ]
    require(
        all((sorted((value for value in values if value)) == [1, 1, 1, 1] for values in exactly_two_zero_rows)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:111',
    )
    return {
        "common_divisor_degree": common_divisor_degree,
        "roots_per_common_fiber": roots_per_common_fiber,
        "common_incidence": common_incidence,
        "owned_free_edges": owned_free_edges,
        "total_incidence": total,
        "row_quartics": row_quartics,
        "degree_per_row": degree_per_row,
        "edge_distributions_checked": len(distributions),
        "minimum_zero_edge_rows": minimum_zero_rows,
        "two_zero_row_remainder": [1, 1, 1, 1],
        "ramification_counted_divisor_theoretically": True,
    }


def degree_trichotomy() -> dict[str, object]:
    lambda_map_types = [
        [cover, image]
        for cover in range(1, 5)
        for image in range(1, 5)
        if cover * image == 4
    ]
    source_map_types = [
        [cover, image]
        for cover in range(1, 3)
        for image in range(1, 3)
        if cover * image == 2
    ]
    require(
        lambda_map_types == [[1, 4], [2, 2], [4, 1]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:144',
    )
    require(
        source_map_types == [[1, 2], [2, 1]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:145',
    )
    return {
        "lambda_pullback_degree": 4,
        "lambda_map_types": lambda_map_types,
        "source_pullback_degree": 2,
        "source_map_types": source_map_types,
        "repeated_source_value_forces_line_image": True,
        "repeated_source_value_span_cap": 2,
    }


def birational_tree_census() -> dict[str, object]:
    free_edges = [
        (row, edge)
        for row in range(6)
        for edge in range(2)
    ]
    cases_by_distribution: dict[tuple[int, ...], int] = {}
    exact_tree_cases = 0
    maximum_trees_per_edge_choice = 0

    for selected in itertools.combinations(free_edges, 4):
        counts = tuple(
            sum(row == candidate for row, _ in selected)
            for candidate in range(6)
        )
        require(
            sum(counts) == 4,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:171',
        )
        require(
            max(counts) <= 2,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:172',
        )
        tree_count = 24
        for count in counts:
            if count == 2:
                tree_count //= 2
        cases_by_distribution[counts] = (
            cases_by_distribution.get(counts, 0) + tree_count
        )
        exact_tree_cases += tree_count
        maximum_trees_per_edge_choice = max(
            maximum_trees_per_edge_choice, tree_count
        )

    pattern_totals: dict[str, int] = {}
    for distribution, tree_cases in cases_by_distribution.items():
        pattern = "+".join(
            str(value)
            for value in sorted(
                (value for value in distribution if value),
                reverse=True,
            )
        )
        pattern_totals[pattern] = (
            pattern_totals.get(pattern, 0) + tree_cases
        )

    require(
        len(list(itertools.combinations(free_edges, 4))) == 495,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:198',
    )
    require(
        maximum_trees_per_edge_choice == 24,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:199',
    )
    require(
        pattern_totals == {'1+1+1+1': 5760, '2+1+1': 2880, '2+2': 90},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:200',
    )
    require(
        exact_tree_cases == 8730,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:205',
    )
    require(
        exact_tree_cases < 495 * 24,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:206',
    )

    star_edges = list(itertools.combinations(range(6), 2))
    admissible_graphs = 0
    connected_graphs = 0
    disconnected_graphs = 0
    all_simple_vertex_cases = 0
    connected_cases = 0
    disconnected_cases = 0
    for graph_edges in itertools.combinations(star_edges, 5):
        degrees = [0] * 6
        adjacency = [set() for _ in range(6)]
        for left, right in graph_edges:
            degrees[left] += 1
            degrees[right] += 1
            adjacency[left].add(right)
            adjacency[right].add(left)
        if min(degrees) < 1 or max(degrees) > 3:
            continue

        seen: set[int] = set()
        components = 0
        for vertex in range(6):
            if vertex in seen:
                continue
            components += 1
            stack = [vertex]
            seen.add(vertex)
            while stack:
                current = stack.pop()
                for neighbor in adjacency[current]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)

        free_edge_choices = 1
        for degree in degrees:
            owned = degree - 1
            require(
                0 <= owned <= 2,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:244',
            )
            free_edge_choices *= 2 if owned == 1 else 1

        admissible_graphs += 1
        all_simple_vertex_cases += free_edge_choices
        if components == 1:
            connected_graphs += 1
            connected_cases += free_edge_choices
        else:
            require(
                components == 2,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:253',
            )
            disconnected_graphs += 1
            disconnected_cases += free_edge_choices

    require(
        admissible_graphs == 1455,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:257',
    )
    require(
        connected_graphs == 1170,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:258',
    )
    require(
        disconnected_graphs == 285,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:259',
    )
    require(
        connected_cases == exact_tree_cases == 8730,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:260',
    )
    require(
        disconnected_cases == 2400,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:261',
    )
    require(
        all_simple_vertex_cases == 11130,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:262',
    )

    return {
        "free_edge_choices": 495,
        "maximum_trees_per_edge_choice": maximum_trees_per_edge_choice,
        "coarse_tree_case_cap": 495 * 24,
        "exact_tree_cases": exact_tree_cases,
        "tree_cases_by_edge_count_pattern": pattern_totals,
        "admissible_complement_graphs": admissible_graphs,
        "connected_tree_graphs": connected_graphs,
        "disconnected_cyclic_graphs": disconnected_graphs,
        "connected_tree_cases": connected_cases,
        "disconnected_cyclic_cases": disconnected_cases,
        "all_simple_vertex_cases": all_simple_vertex_cases,
        "restriction_kernel_degree": -2,
        "restriction_h0_kernel": 0,
        "restriction_h1_kernel": 0,
        "rational_quartic_delta_budget": 3,
        "maximum_duplicate_normalization_preimages": 3,
        "minimum_distinct_star_vertices_when_unramified": 7,
    }


def payload() -> dict[str, object]:
    data: dict[str, object] = {
        "status": "PROVED_REDUCTION_TARGET_OPEN",
        "line_arrangement": line_arrangement(),
        "incidence_ledger": incidence_ledger(),
        "degree_trichotomy": degree_trichotomy(),
        "birational_tree_census": birational_tree_census(),
        "claims": {
            "u2_star_configuration_pullback": "PROVED",
            "u2_degree_trichotomy": "PROVED",
            "repeated_zero_edge_rank_two_reduction": "PROVED",
            "line_image_quotient_precursor": "PROVED",
            "line_image_same_record_payment": "OPEN",
            "conic_image_pole_quotient_precursor": "PROVED",
            "conic_image_same_record_payment": "OPEN",
            "birational_quartic_image": "OPEN",
            "birational_quartic_simple_vertex_gluing": "PROVED_REDUCTION",
            "birational_quartic_simple_vertex_elimination": "OPEN",
            "birational_quartic_ramified_or_repeated_vertex": "OPEN",
            "u2_cycle_union": "OPEN",
            "u3_cycle_union": "OPEN",
            "same_record_owner_payment": "OPEN",
        },
        "payment": "NONE",
    }
    canonical = json.dumps(
        data, sort_keys=True, separators=(",", ":")
    ).encode()
    data["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return data


def validate(data: dict[str, object]) -> None:
    require(
        data['status'] == 'PROVED_REDUCTION_TARGET_OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:318',
    )
    arrangement = data["line_arrangement"]
    require(
        arrangement['evaluation_lines'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:320',
    )
    require(
        arrangement['triple_determinants_checked'] == 20,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:321',
    )
    require(
        arrangement['triple_concurrency'] is False,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:322',
    )
    require(
        arrangement['pair_intersections'] == 15,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:323',
    )
    require(
        arrangement['distinct_split_quadratics'] == 15,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:324',
    )

    ledger = data["incidence_ledger"]
    require(
        ledger['common_divisor_degree'] == 10,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:327',
    )
    require(
        ledger['roots_per_common_fiber'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:328',
    )
    require(
        ledger['common_incidence'] == 20,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:329',
    )
    require(
        ledger['owned_free_edges'] == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:330',
    )
    require(
        ledger['total_incidence'] == 24,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:331',
    )
    require(
        ledger['minimum_zero_edge_rows'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:332',
    )
    require(
        ledger['two_zero_row_remainder'] == [1, 1, 1, 1],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:333',
    )
    require(
        ledger['ramification_counted_divisor_theoretically'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:334',
    )

    degrees = data["degree_trichotomy"]
    require(
        degrees['lambda_map_types'] == [[1, 4], [2, 2], [4, 1]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:337',
    )
    require(
        degrees['source_map_types'] == [[1, 2], [2, 1]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:338',
    )
    require(
        degrees['repeated_source_value_forces_line_image'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:339',
    )
    require(
        degrees['repeated_source_value_span_cap'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:340',
    )

    tree = data["birational_tree_census"]
    require(
        tree['free_edge_choices'] == 495,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:343',
    )
    require(
        tree['maximum_trees_per_edge_choice'] == 24,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:344',
    )
    require(
        tree['coarse_tree_case_cap'] == 11880,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:345',
    )
    require(
        tree['exact_tree_cases'] == 8730,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:346',
    )
    require(
        tree['tree_cases_by_edge_count_pattern'] == {'1+1+1+1': 5760, '2+1+1': 2880, '2+2': 90},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:347',
    )
    require(
        tree['admissible_complement_graphs'] == 1455,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:352',
    )
    require(
        tree['connected_tree_graphs'] == 1170,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:353',
    )
    require(
        tree['disconnected_cyclic_graphs'] == 285,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:354',
    )
    require(
        tree['connected_tree_cases'] == 8730,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:355',
    )
    require(
        tree['disconnected_cyclic_cases'] == 2400,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:356',
    )
    require(
        tree['all_simple_vertex_cases'] == 11130,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:357',
    )
    require(
        tree['restriction_kernel_degree'] == -2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:358',
    )
    require(
        tree['restriction_h0_kernel'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:359',
    )
    require(
        tree['restriction_h1_kernel'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:360',
    )
    require(
        tree['rational_quartic_delta_budget'] == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:361',
    )
    require(
        tree['maximum_duplicate_normalization_preimages'] == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:362',
    )
    require(
        tree['minimum_distinct_star_vertices_when_unramified'] == 7,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:363',
    )

    claims = data["claims"]
    require(
        claims['u2_star_configuration_pullback'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:366',
    )
    require(
        claims['u2_degree_trichotomy'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:367',
    )
    require(
        claims['repeated_zero_edge_rank_two_reduction'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:368',
    )
    require(
        claims['line_image_quotient_precursor'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:369',
    )
    require(
        claims['line_image_same_record_payment'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:370',
    )
    require(
        claims['conic_image_pole_quotient_precursor'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:371',
    )
    require(
        claims['conic_image_same_record_payment'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:372',
    )
    require(
        claims['birational_quartic_image'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:373',
    )
    require(
        claims['birational_quartic_simple_vertex_gluing'] == 'PROVED_REDUCTION',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:374',
    )
    require(
        claims['birational_quartic_simple_vertex_elimination'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:378',
    )
    require(
        claims['birational_quartic_ramified_or_repeated_vertex'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:379',
    )
    require(
        claims['u2_cycle_union'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:383',
    )
    require(
        claims['u3_cycle_union'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:384',
    )
    require(
        claims['same_record_owner_payment'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:385',
    )
    require(
        data['payment'] == 'NONE',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:386',
    )

    supplied_hash = data["payload_sha256"]
    unhashed = dict(data)
    del unhashed["payload_sha256"]
    canonical = json.dumps(
        unhashed, sort_keys=True, separators=(",", ":")
    ).encode()
    require(
        supplied_hash == hashlib.sha256(canonical).hexdigest(),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:394',
    )


def rehash(data: dict[str, object]) -> None:
    data.pop("payload_sha256", None)
    canonical = json.dumps(
        data, sort_keys=True, separators=(",", ":")
    ).encode()
    data["payload_sha256"] = hashlib.sha256(canonical).hexdigest()


def tamper_selftest(data: dict[str, object]) -> int:
    mutations: list[dict[str, object]] = []

    forged = copy.deepcopy(data)
    forged["line_arrangement"]["triple_concurrency"] = True
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["incidence_ledger"]["roots_per_common_fiber"] = 1
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["degree_trichotomy"]["lambda_map_types"].append([1, 3])
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["claims"]["u2_cycle_union"] = "PROVED"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["birational_tree_census"]["exact_tree_cases"] = 8729
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["payment"] = "BOOKED"
    mutations.append(forged)

    rejected = 0
    for forged in mutations:
        rehash(forged)
        try:
            validate(forged)
        except VerificationError:
            rejected += 1
    require(
        rejected == len(mutations),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:439',
    )
    return rejected


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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_plane_map_reduction.py:459',
        )
    rejected = 0
    if args.tamper_selftest:
        rejected = tamper_selftest(data)

    print("six-line star configuration: PASS")
    print("exact u=2 incidence ledger: PASS")
    print("coefficient-map degree trichotomy: PASS")
    print("birational-quartic simple-vertex census: PASS")
    if args.tamper_selftest:
        print(f"tamper mutations rejected: PASS {rejected}/6")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
