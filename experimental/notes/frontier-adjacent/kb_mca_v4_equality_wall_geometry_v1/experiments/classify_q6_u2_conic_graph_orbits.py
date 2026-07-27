#!/usr/bin/env python3
"""Classify reduced u=2 conic signature graphs by pole-graph symmetry."""

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

import classify_q6_u2_quartic_graph_orbits as quartic


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "q6_u2_conic_graph_orbits.json"


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def histogram(values: list[object]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value)
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def digest_chain(digests: list[str]) -> str:
    state = hashlib.sha256(b"q6-u2-conic-orbit-chain-v1").digest()
    for item in digests:
        state = hashlib.sha256(state + bytes.fromhex(item)).digest()
    return state.hex()


def raw_conic_cases(
    pole_edges: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    cases = []
    for selected in itertools.combinations(range(15), 5):
        degrees = [0] * 6
        graph_mask = 0
        for index in selected:
            graph_mask |= 1 << index
            left, right = quartic.LEFT_PAIRS[index]
            degrees[left] += 1
            degrees[right] += 1
        if sorted(degrees) != [1, 1, 2, 2, 2, 2]:
            continue

        endpoints = {
            vertex for vertex, degree in enumerate(degrees)
            if degree == 1
        }
        require(
            len(endpoints) == 2,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:39',
        )
        free_mask = 0
        for index, (left, _) in enumerate(pole_edges):
            if left in endpoints:
                free_mask |= 1 << index
        require(
            free_mask.bit_count() == 4,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:44',
        )
        cases.append((free_mask, graph_mask))
    require(
        len(cases) == 465,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:46',
    )
    return cases


def classify_free_pair_orbits(
    partition: tuple[int, ...],
    edges: list[tuple[int, int]],
    maps: list[tuple[list[int], list[int]]],
) -> dict[str, object]:
    paid_cycle_masks = quartic.four_cycle_masks(partition, edges)
    members: dict[int, int] = {}
    cycle_status: dict[int, bool] = {}
    for endpoints in itertools.combinations(range(6), 2):
        free_mask = 0
        for index, (left, _) in enumerate(edges):
            if left in endpoints:
                free_mask |= 1 << index
        require(
            free_mask.bit_count() == 4,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:63',
        )
        canonical = min(
            quartic.transform_mask(free_mask, free_map)
            for free_map, _ in maps
        )
        members[canonical] = members.get(canonical, 0) + 1
        is_cycle_union = free_mask in paid_cycle_masks
        previous = cycle_status.setdefault(canonical, is_cycle_union)
        require(
            previous == is_cycle_union,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:71',
        )

    representatives = []
    for free_mask, orbit_size in sorted(members.items()):
        free_edges = [
            edges[index]
            for index in range(len(edges))
            if free_mask & (1 << index)
        ]
        endpoint_rows = sorted({left for left, _ in free_edges})
        require(
            len(endpoint_rows) == 2,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:81',
        )
        right_neighbors = {
            endpoint: {
                right
                for left, right in free_edges
                if left == endpoint
            }
            for endpoint in endpoint_rows
        }
        shared_right_neighbors = len(
            right_neighbors[endpoint_rows[0]]
            & right_neighbors[endpoint_rows[1]]
        )
        require(
            shared_right_neighbors in (0, 1, 2),
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:94',
        )
        representatives.append(
            {
                "endpoint_rows": endpoint_rows,
                "free_pole_edges": [list(edge) for edge in free_edges],
                "orbit_size": orbit_size,
                "cycle_union": cycle_status[free_mask],
                "shared_right_neighbors": shared_right_neighbors,
                "reciprocal_compatible": shared_right_neighbors != 1,
            }
        )

    paid_orbits = sum(cycle_status.values())
    paid_cases = sum(
        members[key]
        for key, paid in cycle_status.items()
        if paid
    )
    reciprocal_open = [
        representative
        for representative in representatives
        if (
            not representative["cycle_union"]
            and representative["reciprocal_compatible"]
        )
    ]
    return {
        "raw_endpoint_pairs": 15,
        "orbits": len(members),
        "cycle_union_cases": paid_cases,
        "cycle_union_orbits": paid_orbits,
        "open_cases": 15 - paid_cases,
        "open_orbits": len(members) - paid_orbits,
        "reciprocal_open_orbits": len(reciprocal_open),
        "reciprocal_open_cases": sum(
            representative["orbit_size"]
            for representative in reciprocal_open
        ),
        "representatives": representatives,
    }


def classify(partition: tuple[int, ...]) -> dict[str, object]:
    edges = quartic.pole_graph(partition)
    group = quartic.automorphisms(edges)
    maps = quartic.transformation_maps(edges, group)
    cases = raw_conic_cases(edges)
    paid_cycle_masks = quartic.four_cycle_masks(partition, edges)

    members: dict[tuple[int, int], int] = {}
    cycle_status: dict[tuple[int, int], bool] = {}
    for free_mask, graph_mask in cases:
        canonical = min(
            (
                quartic.transform_mask(free_mask, free_map),
                quartic.transform_mask(graph_mask, graph_map),
            )
            for free_map, graph_map in maps
        )
        members[canonical] = members.get(canonical, 0) + 1
        is_cycle_union = free_mask in paid_cycle_masks
        previous = cycle_status.setdefault(canonical, is_cycle_union)
        require(
            previous == is_cycle_union,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:156',
        )

    paid_orbits = sum(cycle_status.values())
    paid_cases = sum(
        members[key]
        for key, paid in cycle_status.items()
        if paid
    )
    open_representatives = []
    for (free_mask, graph_mask), orbit_size in sorted(members.items()):
        if cycle_status[(free_mask, graph_mask)]:
            continue
        common_signature_edges = [
            tuple(quartic.LEFT_PAIRS[index])
            for index in range(len(quartic.LEFT_PAIRS))
            if graph_mask & (1 << index)
        ]
        adjacency = {vertex: set() for vertex in range(6)}
        for left, right in common_signature_edges:
            adjacency[left].add(right)
            adjacency[right].add(left)
        component_sizes = []
        unseen = set(range(6))
        while unseen:
            seed = min(unseen)
            stack = [seed]
            unseen.remove(seed)
            size = 0
            while stack:
                vertex = stack.pop()
                size += 1
                for neighbor in adjacency[vertex]:
                    if neighbor in unseen:
                        unseen.remove(neighbor)
                        stack.append(neighbor)
            component_sizes.append(size)
        signature_graph_type = {
            (6,): "P6",
            (3, 3): "P3_PLUS_C3",
            (2, 4): "P2_PLUS_C4",
        }[tuple(sorted(component_sizes))]
        open_representatives.append(
            {
                "free_pole_edges": [
                    list(edges[index])
                    for index in range(len(edges))
                    if free_mask & (1 << index)
                ],
                "common_signature_edges": [
                    list(edge) for edge in common_signature_edges
                ],
                "signature_graph_type": signature_graph_type,
                "orbit_size": orbit_size,
            }
        )
    post_star_representatives = [
        representative
        for representative in open_representatives
        if representative["signature_graph_type"] != "P3_PLUS_C3"
    ]
    return {
        "partition": list(partition),
        "automorphism_group_size": len(group),
        "raw_cases": len(cases),
        "orbits": len(members),
        "cycle_union_cases": paid_cases,
        "cycle_union_orbits": paid_orbits,
        "open_cases": len(cases) - paid_cases,
        "open_orbits": len(members) - paid_orbits,
        "minimum_orbit_size": min(members.values()),
        "maximum_orbit_size": max(members.values()),
        "orbit_size_sum": sum(members.values()),
        "open_representatives": open_representatives,
        "post_star_geometry_open_cases": sum(
            representative["orbit_size"]
            for representative in post_star_representatives
        ),
        "post_star_geometry_open_orbits": len(post_star_representatives),
        "post_star_geometry_representatives": post_star_representatives,
        "free_pair_quotient": classify_free_pair_orbits(
            partition, edges, maps
        ),
    }


def payload() -> dict[str, object]:
    rows = [classify(partition) for partition in quartic.PARTITIONS]
    data: dict[str, object] = {
        "status": "PROVED_FINITE_REDUCTION_TARGET_OPEN",
        "classification": rows,
        "claims": {
            "pre_star_geometry_labeled_cases": 465,
            "reduced_conic_labeled_cases": 405,
            "P3_PLUS_C3_status": "PROVED_IMPOSSIBLE",
            "surviving_signature_graphs": ["P6", "P2_PLUS_C4"],
            "pole_graph_symmetry_quotient": "PROVED",
            "second_involution_minor_elimination": "OPEN",
            "ramified_conic_branch": "PROVED_EXCLUDED",
            "reduced_conic_orders": ["RECIPROCAL", 4, 5],
            "payment": "NONE",
        },
    }
    canonical = json.dumps(
        data, sort_keys=True, separators=(",", ":")
    ).encode()
    data["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return data


def compact_payload(data: dict[str, object]) -> dict[str, object]:
    """Bind the full enumeration without committing every representative."""
    rows = []
    for row in data["classification"]:
        open_representatives = row["open_representatives"]
        post_star_representatives = row[
            "post_star_geometry_representatives"
        ]
        free_pair = row["free_pair_quotient"]
        free_pair_representatives = free_pair["representatives"]

        open_digests = [digest(rep) for rep in open_representatives]
        post_star_digests = [
            digest(rep) for rep in post_star_representatives
        ]
        free_pair_digests = [
            digest(rep) for rep in free_pair_representatives
        ]

        row_scalars = {
            key: value
            for key, value in row.items()
            if key
            not in {
                "open_representatives",
                "post_star_geometry_representatives",
                "free_pair_quotient",
            }
        }
        free_pair_scalars = {
            key: value
            for key, value in free_pair.items()
            if key != "representatives"
        }
        rows.append(
            {
                **row_scalars,
                "open_orbit_size_histogram": histogram(
                    [rep["orbit_size"] for rep in open_representatives]
                ),
                "open_signature_orbit_histogram": histogram(
                    [
                        rep["signature_graph_type"]
                        for rep in open_representatives
                    ]
                ),
                "open_signature_case_histogram": {
                    signature: sum(
                        rep["orbit_size"]
                        for rep in open_representatives
                        if rep["signature_graph_type"] == signature
                    )
                    for signature in (
                        "P2_PLUS_C4",
                        "P3_PLUS_C3",
                        "P6",
                    )
                },
                "open_representative_digests": open_digests,
                "open_representative_digest_chain": digest_chain(
                    open_digests
                ),
                "post_star_representative_digests": post_star_digests,
                "post_star_representative_digest_chain": digest_chain(
                    post_star_digests
                ),
                "free_pair_quotient": {
                    **free_pair_scalars,
                    "orbit_size_histogram": histogram(
                        [
                            rep["orbit_size"]
                            for rep in free_pair_representatives
                        ]
                    ),
                    "representative_digests": free_pair_digests,
                    "representative_digest_chain": digest_chain(
                        free_pair_digests
                    ),
                },
                "complete_full_row_sha256": digest(row),
            }
        )

    compact: dict[str, object] = {
        "format": "q6-u2-conic-orbit-compact-certificate-v1",
        "status": data["status"],
        "claims": data["claims"],
        "input_universe": {
            "partitions": [list(partition) for partition in quartic.PARTITIONS],
            "left_pairs": [list(pair) for pair in quartic.LEFT_PAIRS],
            "sha256": digest(
                {
                    "partitions": [
                        list(partition) for partition in quartic.PARTITIONS
                    ],
                    "left_pairs": [
                        list(pair) for pair in quartic.LEFT_PAIRS
                    ],
                }
            ),
        },
        "classification": rows,
        "complete_full_payload_sha256": data["payload_sha256"],
    }
    compact["payload_sha256"] = digest(compact)
    return compact


def validate(data: dict[str, object]) -> None:
    require(
        data['status'] == 'PROVED_FINITE_REDUCTION_TARGET_OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:266',
    )
    rows = data["classification"]
    require(
        [row['partition'] for row in rows] == [list(partition) for partition in quartic.PARTITIONS],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:268',
    )
    expected_rows = [
        {
            "automorphism_group_size": 12,
            "orbits": 52,
            "cycle_union_cases": 0,
            "cycle_union_orbits": 0,
            "open_cases": 465,
            "open_orbits": 52,
            "minimum_orbit_size": 3,
            "maximum_orbit_size": 12,
            "free_pair_orbits": 3,
            "free_pair_cycle_union_orbits": 0,
            "free_pair_open_orbits": 3,
            "free_pair_open_cases": 15,
            "free_pair_reciprocal_open_orbits": 2,
            "post_star_geometry_open_cases": 405,
            "post_star_geometry_open_orbits": 46,
        },
        {
            "automorphism_group_size": 32,
            "orbits": 43,
            "cycle_union_cases": 31,
            "cycle_union_orbits": 6,
            "open_cases": 434,
            "open_orbits": 37,
            "minimum_orbit_size": 1,
            "maximum_orbit_size": 16,
            "free_pair_orbits": 4,
            "free_pair_cycle_union_orbits": 1,
            "free_pair_open_orbits": 3,
            "free_pair_open_cases": 14,
            "free_pair_reciprocal_open_orbits": 2,
            "post_star_geometry_open_cases": 378,
            "post_star_geometry_open_orbits": 30,
        },
        {
            "automorphism_group_size": 72,
            "orbits": 13,
            "cycle_union_cases": 0,
            "cycle_union_orbits": 0,
            "open_cases": 465,
            "open_orbits": 13,
            "minimum_orbit_size": 6,
            "maximum_orbit_size": 72,
            "free_pair_orbits": 2,
            "free_pair_cycle_union_orbits": 0,
            "free_pair_open_orbits": 2,
            "free_pair_open_cases": 15,
            "free_pair_reciprocal_open_orbits": 1,
            "post_star_geometry_open_cases": 405,
            "post_star_geometry_open_orbits": 10,
        },
        {
            "automorphism_group_size": 384,
            "orbits": 18,
            "cycle_union_cases": 93,
            "cycle_union_orbits": 6,
            "open_cases": 372,
            "open_orbits": 12,
            "minimum_orbit_size": 3,
            "maximum_orbit_size": 48,
            "free_pair_orbits": 2,
            "free_pair_cycle_union_orbits": 1,
            "free_pair_open_orbits": 1,
            "free_pair_open_cases": 12,
            "free_pair_reciprocal_open_orbits": 1,
            "post_star_geometry_open_cases": 324,
            "post_star_geometry_open_orbits": 10,
        },
    ]
    for row, expected in zip(rows, expected_rows, strict=True):
        require(
            row['raw_cases'] == 465,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:342',
        )
        free_pair_expected = {
            key.removeprefix("free_pair_"): value
            for key, value in expected.items()
            if key.startswith("free_pair_")
        }
        row_expected = {
            key: value
            for key, value in expected.items()
            if not key.startswith("free_pair_")
        }
        for key, value in row_expected.items():
            require(
                row[key] == value,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:354',
            )
        require(
            row['cycle_union_cases'] + row['open_cases'] == 465,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:355',
        )
        require(
            row['cycle_union_orbits'] + row['open_orbits'] == row['orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:356',
        )
        require(
            row['orbit_size_sum'] == 465,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:357',
        )
        require(
            row['minimum_orbit_size'] >= 1,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:358',
        )
        require(
            row['maximum_orbit_size'] <= row['automorphism_group_size'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:359',
        )
        representatives = row["open_representatives"]
        require(
            len(representatives) == row['open_orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:361',
        )
        require(
            sum((rep['orbit_size'] for rep in representatives)) == row['open_cases'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:362',
        )
        post_star = row["post_star_geometry_representatives"]
        require(
            len(post_star) == row['post_star_geometry_open_orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:364',
        )
        require(
            sum((representative['orbit_size'] for representative in post_star)) == row['post_star_geometry_open_cases'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:365',
        )
        require(
            all((representative['signature_graph_type'] in {'P6', 'P2_PLUS_C4'} for representative in post_star)),
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:369',
        )
        encoded = set()
        pole_edges = quartic.pole_graph(tuple(row["partition"]))
        paid_cycle_masks = quartic.four_cycle_masks(
            tuple(row["partition"]), pole_edges
        )
        for representative in representatives:
            free_edges = [tuple(edge) for edge in representative["free_pole_edges"]]
            common_edges = [
                tuple(edge)
                for edge in representative["common_signature_edges"]
            ]
            require(
                len(free_edges) == 4,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:386',
            )
            require(
                len(common_edges) == 5,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:387',
            )
            require(
                len(set(free_edges)) == 4,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:388',
            )
            require(
                len(set(common_edges)) == 5,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:389',
            )
            require(
                representative['signature_graph_type'] in {'P6', 'P3_PLUS_C3', 'P2_PLUS_C4'},
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:390',
            )
            free_mask = sum(
                1 << pole_edges.index(edge)
                for edge in free_edges
            )
            graph_mask = sum(
                1 << quartic.LEFT_PAIRS.index(edge)
                for edge in common_edges
            )
            require(
                free_mask not in paid_cycle_masks,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:401',
            )
            degrees = [0] * 6
            for left, right in common_edges:
                degrees[left] += 1
                degrees[right] += 1
            require(
                sorted(degrees) == [1, 1, 2, 2, 2, 2],
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:406',
            )
            endpoints = {
                vertex for vertex, degree in enumerate(degrees)
                if degree == 1
            }
            require(
                {left for left, _ in free_edges} == endpoints,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:411',
            )
            require(
                representative['orbit_size'] >= 1,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:414',
            )
            require(
                representative['orbit_size'] <= row['automorphism_group_size'],
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:415',
            )
            key = (free_mask, graph_mask)
            require(
                key not in encoded,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:417',
            )
            encoded.add(key)

        free_pair = row["free_pair_quotient"]
        require(
            free_pair['orbits'] == free_pair_expected['orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:421',
        )
        require(
            free_pair['cycle_union_orbits'] == free_pair_expected['cycle_union_orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:422',
        )
        require(
            free_pair['open_orbits'] == free_pair_expected['open_orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:425',
        )
        require(
            free_pair['open_cases'] == free_pair_expected['open_cases'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:426',
        )
        require(
            free_pair['reciprocal_open_orbits'] == free_pair_expected['reciprocal_open_orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:427',
        )
        require(
            free_pair['raw_endpoint_pairs'] == 15,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:430',
        )
        require(
            free_pair['cycle_union_cases'] + free_pair['open_cases'] == 15,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:431',
        )
        require(
            free_pair['cycle_union_orbits'] + free_pair['open_orbits'] == free_pair['orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:432',
        )
        require(
            len(free_pair['representatives']) == free_pair['orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:436',
        )
        require(
            sum((rep['orbit_size'] for rep in free_pair['representatives'])) == 15,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:437',
        )
        seen_endpoint_masks = set()
        for representative in free_pair["representatives"]:
            endpoint_rows = representative["endpoint_rows"]
            free_edges = [
                tuple(edge)
                for edge in representative["free_pole_edges"]
            ]
            require(
                len(endpoint_rows) == 2,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:447',
            )
            require(
                len(set(endpoint_rows)) == 2,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:448',
            )
            require(
                len(free_edges) == 4,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:449',
            )
            require(
                {left for left, _ in free_edges} == set(endpoint_rows),
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:450',
            )
            free_mask = sum(
                1 << pole_edges.index(edge)
                for edge in free_edges
            )
            require(
                representative['cycle_union'] == (free_mask in paid_cycle_masks),
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:455',
            )
            neighbor_sets = []
            for endpoint in endpoint_rows:
                neighbor_sets.append(
                    {
                        right
                        for left, right in free_edges
                        if left == endpoint
                    }
                )
            shared = len(neighbor_sets[0] & neighbor_sets[1])
            require(
                representative['shared_right_neighbors'] == shared,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:468',
            )
            require(
                representative['reciprocal_compatible'] == (shared != 1),
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:469',
            )
            require(
                representative['orbit_size'] >= 1,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:472',
            )
            require(
                free_mask not in seen_endpoint_masks,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:473',
            )
            seen_endpoint_masks.add(free_mask)

    claims = data["claims"]
    require(
        claims['pre_star_geometry_labeled_cases'] == 465,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:477',
    )
    require(
        claims['reduced_conic_labeled_cases'] == 405,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:478',
    )
    require(
        claims['P3_PLUS_C3_status'] == 'PROVED_IMPOSSIBLE',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:479',
    )
    require(
        claims['surviving_signature_graphs'] == ['P6', 'P2_PLUS_C4'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:480',
    )
    require(
        claims['pole_graph_symmetry_quotient'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:481',
    )
    require(
        claims['second_involution_minor_elimination'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:482',
    )
    require(
        claims['ramified_conic_branch'] == 'PROVED_EXCLUDED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:483',
    )
    require(
        claims['reduced_conic_orders'] == ['RECIPROCAL', 4, 5],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:484',
    )
    require(
        claims['payment'] == 'NONE',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:485',
    )

    supplied_hash = data["payload_sha256"]
    unhashed = dict(data)
    del unhashed["payload_sha256"]
    canonical = json.dumps(
        unhashed, sort_keys=True, separators=(",", ":")
    ).encode()
    require(
        supplied_hash == hashlib.sha256(canonical).hexdigest(),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:493',
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
    forged["classification"][0]["raw_cases"] = 464
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["classification"][1]["orbits"] += 1
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["classification"][3]["cycle_union_cases"] += 1
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["claims"]["second_involution_minor_elimination"] = "PROVED"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["claims"]["payment"] = "BOOKED"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["classification"][0]["open_representatives"][0][
        "orbit_size"
    ] = 0
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["classification"][0]["free_pair_quotient"][
        "raw_endpoint_pairs"
    ] = 14
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["classification"][0]["free_pair_quotient"][
        "reciprocal_open_orbits"
    ] = 3
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["claims"]["ramified_conic_branch"] = "OPEN"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["classification"][0]["post_star_geometry_open_orbits"] = 52
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
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_conic_graph_orbits.py:560',
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
    compact = compact_payload(data)
    if args.emit:
        CERTIFICATE.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        checked = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        require(
            checked == compact,
            "committed compact orbit certificate does not match the "
            "regenerated complete enumeration",
        )
    rejected = tamper_selftest(data) if args.tamper_selftest else 0

    for row in data["classification"]:
        partition = "+".join(str(value) for value in row["partition"])
        print(
            f"partition={partition} "
            f"orbits={row['orbits']} "
            f"paid={row['cycle_union_orbits']} "
            f"open={row['open_orbits']} "
            f"post_star_open={row['post_star_geometry_open_orbits']}"
        )
    if args.tamper_selftest:
        print(f"tamper mutations rejected: PASS {rejected}/10")
    print(f"full_payload_sha256={data['payload_sha256']}")
    print(f"compact_payload_sha256={compact['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
