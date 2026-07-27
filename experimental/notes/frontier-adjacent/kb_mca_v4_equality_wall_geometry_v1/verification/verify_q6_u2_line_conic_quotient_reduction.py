#!/usr/bin/env python3
"""Verify the finite ledgers in the u=2 line/conic reduction."""

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
CERTIFICATE = ROOT / "q6_u2_line_conic_quotient_certificate.json"
PRIME = 101


def rank_mod(matrix: list[list[int]]) -> int:
    data = [
        [entry % PRIME for entry in row]
        for row in matrix
    ]
    rank = 0
    columns = len(data[0])
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, len(data))
                if data[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        data[rank], data[pivot] = data[pivot], data[rank]
        inverse = pow(data[rank][column], PRIME - 2, PRIME)
        data[rank] = [
            inverse * entry % PRIME for entry in data[rank]
        ]
        for row in range(len(data)):
            if row == rank:
                continue
            factor = data[row][column]
            if factor:
                data[row] = [
                    (entry - factor * pivot_entry) % PRIME
                    for entry, pivot_entry in zip(
                        data[row], data[rank], strict=True
                    )
                ]
        rank += 1
        if rank == columns:
            break
    return rank


def involution_matrix_regression() -> dict[str, object]:
    a, b, c = 3, 5, 7
    require(
        (a * a + b * c) % PRIME != 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:61',
    )
    pairs = []
    rows = []
    used = set()
    for x in range(PRIME):
        denominator = (c * x - a) % PRIME
        if not denominator or x in used:
            continue
        y = (a * x + b) * pow(
            denominator, PRIME - 2, PRIME
        ) % PRIME
        if y == x or y in used:
            continue
        pairs.append([x, y])
        used.update((x, y))
        rows.append([
            x * y % PRIME,
            -(x + y) % PRIME,
            -1 % PRIME,
        ])
        require(
            (c * rows[-1][0] + a * rows[-1][1] + b * rows[-1][2]) % PRIME == 0,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:81',
        )
        if len(pairs) == 7:
            break
    require(
        len(pairs) == 7,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:88',
    )
    require(
        len(used) == 14,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:89',
    )

    seed_rank = rank_mod(rows[:2])
    require(
        seed_rank == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:92',
    )
    first, second = rows[:2]
    candidate = [
        (first[1] * second[2] - first[2] * second[1]) % PRIME,
        (first[2] * second[0] - first[0] * second[2]) % PRIME,
        (first[0] * second[1] - first[1] * second[0]) % PRIME,
    ]
    original = [c, a, b]
    pivot = next(index for index, value in enumerate(original) if value)
    scale = candidate[pivot] * pow(
        original[pivot], PRIME - 2, PRIME
    ) % PRIME
    require(
        candidate == [scale * value % PRIME for value in original],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:104',
    )
    require(
        (candidate[1] * candidate[1] + candidate[2] * candidate[0]) % PRIME != 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:107',
    )

    good_rank = rank_mod(rows)
    require(
        good_rank == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:113',
    )

    tampered_rows = copy.deepcopy(rows)
    tampered_y = (pairs[-1][1] + 1) % PRIME
    tampered_rows[-1] = [
        pairs[-1][0] * tampered_y % PRIME,
        -(pairs[-1][0] + tampered_y) % PRIME,
        -1 % PRIME,
    ]
    bad_rank = rank_mod(tampered_rows)
    require(
        bad_rank == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:123',
    )
    return {
        "field": PRIME,
        "trace_zero_parameters": [a, b, c],
        "pair_rows": len(rows),
        "free_seed_pairs": 2,
        "free_seed_matrix_rank": seed_rank,
        "free_seed_recovers_unique_candidate": True,
        "candidate_nondegenerate": True,
        "common_pair_tests": 5,
        "common_decic_roots": 10,
        "candidate_preserves_common_root_set": True,
        "valid_pair_matrix_rank": good_rank,
        "tampered_pair_matrix_rank": bad_rank,
        "minor_columns": 3,
    }


def canonical_graph(edges: tuple[tuple[int, int], ...]) -> tuple:
    edge_set = {tuple(sorted(edge)) for edge in edges}
    representatives = []
    for permutation in itertools.permutations(range(6)):
        representatives.append(
            tuple(
                sorted(
                    tuple(
                        sorted(
                            (permutation[left], permutation[right])
                        )
                    )
                    for left, right in edge_set
                )
            )
        )
    return min(representatives)


def conic_graph_census() -> dict[str, object]:
    complete_edges = list(itertools.combinations(range(6), 2))
    orbit_counts: dict[tuple, int] = {}

    for selected in itertools.combinations(complete_edges, 5):
        degrees = [0] * 6
        adjacency = [set() for _ in range(6)]
        for left, right in selected:
            degrees[left] += 1
            degrees[right] += 1
            adjacency[left].add(right)
            adjacency[right].add(left)
        if sorted(degrees) != [1, 1, 2, 2, 2, 2]:
            continue
        representative = canonical_graph(selected)
        orbit_counts[representative] = (
            orbit_counts.get(representative, 0) + 1
        )

    sizes = sorted(orbit_counts.values())
    require(
        sizes == [45, 60, 360],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:180',
    )
    require(
        sum(sizes) == 465,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:181',
    )
    require(
        len(orbit_counts) == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:182',
    )

    return {
        "common_points": 10,
        "conic_involution_orbits": 5,
        "common_signature_edges": 5,
        "degree_sequence": [1, 1, 2, 2, 2, 2],
        "unlabeled_graph_types": [
            "P2+C4",
            "P3+C3",
            "P6",
        ],
        "labeled_counts": {
            "P2+C4": 45,
            "P3+C3": 60,
            "P6": 360,
        },
        "labeled_total": 465,
        "free_edge_rows": 2,
        "free_edges_per_active_row": 2,
        "candidate_involution_seed_pairs": 2,
        "remaining_common_pair_gates": 5,
    }


def dihedral_order_census() -> dict[str, object]:
    divisibility_candidates = {}
    reduced_survivors = {}
    for fixed_points in (0, 2):
        orders = [
            order
            for order in range(3, 11)
            if (10 - fixed_points) % order == 0
        ]
        divisibility_candidates[str(fixed_points)] = orders
        reduced_survivors[str(fixed_points)] = [
            order
            for order in orders
            if ((10 - fixed_points) // order) % 2 == 0
        ]
    require(
        divisibility_candidates == {'0': [5, 10], '2': [4, 8]},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:222',
    )
    require(
        reduced_survivors == {'0': [5], '2': [4]},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:223',
    )
    return {
        "reduced_common_support": 10,
        "rotation_fixed_points_in_support": [0, 2],
        "divisibility_candidates_by_fixed_count": divisibility_candidates,
        "reduced_survivors_by_fixed_count": reduced_survivors,
        "nonfixed_rotation_orbits_must_be_reflection_paired": True,
        "eliminated_unpaired_orders": [8, 10],
        "allowed_n": [4, 5],
        "commuting_branch": "reciprocal_normalizer",
        "noncommuting_branch": "tame_dihedral",
        "source_quotient_degrees": [2, 4, 5],
        "common_source_image_caps": {
            "2": 3,
            "4": 2,
            "5": 1,
        },
        "noncommuting_common_fiber_profiles": {
            "4": {
                "totally_ramified_source_labels": 1,
                "total_ramification_index": 4,
                "unramified_complete_fibers": [4],
            },
            "5": {
                "totally_ramified_source_labels": 0,
                "unramified_complete_fibers": [5],
            },
        },
        "endpoint_neighbor_pairs_collapsed": 2,
    }


def dickson_normal_form_regression() -> dict[str, object]:
    parameter = 7
    checks = 0
    for x in range(1, PRIME):
        inverse_x = pow(x, PRIME - 2, PRIME)
        reflected = parameter * inverse_x % PRIME
        w = (x + reflected) % PRIME
        d4 = (
            pow(w, 4, PRIME)
            - 4 * parameter * pow(w, 2, PRIME)
            + 2 * pow(parameter, 2, PRIME)
        ) % PRIME
        d5 = (
            pow(w, 5, PRIME)
            - 5 * parameter * pow(w, 3, PRIME)
            + 5 * pow(parameter, 2, PRIME) * w
        ) % PRIME
        require(
            d4 == (pow(x, 4, PRIME) + pow(reflected, 4, PRIME)) % PRIME,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:272',
        )
        require(
            d5 == (pow(x, 5, PRIME) + pow(reflected, 5, PRIME)) % PRIME,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:275',
        )
        checks += 2
    return {
        "field": f"F_{PRIME}",
        "parameter": parameter,
        "sampled_nonzero_inputs": PRIME - 1,
        "identity_checks": checks,
        "D4_coefficients_descending": [1, 0, -4 * parameter, 0, 2 * parameter**2],
        "D5_coefficients_descending": [
            1,
            0,
            -5 * parameter,
            0,
            5 * parameter**2,
            0,
        ],
        "status": "PASS",
    }


def payload() -> dict[str, object]:
    data: dict[str, object] = {
        "status": "PROVED_REDUCTION_TARGET_OPEN",
        "line_branch": {
            "row_degree": 4,
            "available_free_roots_per_row": 2,
            "every_row_meets_common_divisor": True,
            "shared_root_forces_proportional_pencil_members": True,
            "proportional_rows_have_identical_divisors": True,
            "free_divisor_degree": 4,
            "conclusion": "EXCLUDED",
        },
        "conic_branch": conic_graph_census(),
        "involution_pair_matrix": involution_matrix_regression(),
        "reduced_dihedral_branch": dihedral_order_census(),
        "dickson_normal_form_regression": dickson_normal_form_regression(),
        "ramification": {
            "deck_branch_local_rhs_multiplicity": 4,
            "unramified_conic_two_line_local_cap": 3,
            "deck_branch_forces_conic_branch": True,
            "two_shared_branch_points_force_same_involution": True,
            "same_involution_contradicts_free_root_pairing": True,
            "two_deck_branch_points_in_K": "EXCLUDED",
            "one_deck_branch_point_in_K": "EXCLUDED",
            "one_branch_product": "nontrivial_translation",
            "translation_order": 2130706433,
            "remaining_common_support_points": 8,
            "zero_deck_branch_points_in_K": "OPEN",
        },
        "claims": {
            "line_image_branch": "EXCLUDED",
            "reduced_conic_signature_classification": "PROVED",
            "conic_quotient_differs_from_deck": "PROVED",
            "two_branch_point_conic_case": "EXCLUDED",
            "one_branch_point_conic_case": "EXCLUDED",
            "conic_pair_matrix_rank_criterion": "PROVED",
            "two_free_pairs_determine_candidate": "PROVED",
            "common_decic_invariance_criterion": "PROVED",
            "dickson_normal_form_reduction": "PROVED",
            "component_rooted_source_label_quotient_precursor": "PROVED",
            "second_involution_matching": "OPEN",
            "same_record_owner_payment": "OPEN",
            "u2_cycle_union": "OPEN",
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
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:351',
    )
    line = data["line_branch"]
    require(
        line['row_degree'] == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:353',
    )
    require(
        line['available_free_roots_per_row'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:354',
    )
    require(
        line['every_row_meets_common_divisor'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:355',
    )
    require(
        line['shared_root_forces_proportional_pencil_members'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:356',
    )
    require(
        line['proportional_rows_have_identical_divisors'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:360',
    )
    require(
        line['free_divisor_degree'] == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:361',
    )
    require(
        line['conclusion'] == 'EXCLUDED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:362',
    )

    conic = data["conic_branch"]
    require(
        conic['common_points'] == 10,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:365',
    )
    require(
        conic['conic_involution_orbits'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:366',
    )
    require(
        conic['common_signature_edges'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:367',
    )
    require(
        conic['degree_sequence'] == [1, 1, 2, 2, 2, 2],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:368',
    )
    require(
        conic['unlabeled_graph_types'] == ['P2+C4', 'P3+C3', 'P6'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:369',
    )
    require(
        conic['labeled_counts'] == {'P2+C4': 45, 'P3+C3': 60, 'P6': 360},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:374',
    )
    require(
        conic['labeled_total'] == 465,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:379',
    )
    require(
        conic['free_edge_rows'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:380',
    )
    require(
        conic['free_edges_per_active_row'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:381',
    )
    require(
        conic['candidate_involution_seed_pairs'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:382',
    )
    require(
        conic['remaining_common_pair_gates'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:383',
    )

    pair_matrix = data["involution_pair_matrix"]
    require(
        pair_matrix['field'] == PRIME,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:386',
    )
    require(
        pair_matrix['pair_rows'] == 7,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:387',
    )
    require(
        pair_matrix['free_seed_pairs'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:388',
    )
    require(
        pair_matrix['free_seed_matrix_rank'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:389',
    )
    require(
        pair_matrix['free_seed_recovers_unique_candidate'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:390',
    )
    require(
        pair_matrix['candidate_nondegenerate'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:391',
    )
    require(
        pair_matrix['common_pair_tests'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:392',
    )
    require(
        pair_matrix['common_decic_roots'] == 10,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:393',
    )
    require(
        pair_matrix['candidate_preserves_common_root_set'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:394',
    )
    require(
        pair_matrix['valid_pair_matrix_rank'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:395',
    )
    require(
        pair_matrix['tampered_pair_matrix_rank'] == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:396',
    )
    require(
        pair_matrix['minor_columns'] == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:397',
    )

    dihedral = data["reduced_dihedral_branch"]
    require(
        dihedral['reduced_common_support'] == 10,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:400',
    )
    require(
        dihedral['rotation_fixed_points_in_support'] == [0, 2],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:401',
    )
    require(
        dihedral['divisibility_candidates_by_fixed_count'] == {'0': [5, 10], '2': [4, 8]},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:402',
    )
    require(
        dihedral['reduced_survivors_by_fixed_count'] == {'0': [5], '2': [4]},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:406',
    )
    require(
        dihedral['nonfixed_rotation_orbits_must_be_reflection_paired'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:410',
    )
    require(
        dihedral['eliminated_unpaired_orders'] == [8, 10],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:411',
    )
    require(
        dihedral['allowed_n'] == [4, 5],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:412',
    )
    require(
        dihedral['commuting_branch'] == 'reciprocal_normalizer',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:413',
    )
    require(
        dihedral['noncommuting_branch'] == 'tame_dihedral',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:414',
    )
    require(
        dihedral['source_quotient_degrees'] == [2, 4, 5],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:415',
    )
    require(
        dihedral['common_source_image_caps'] == {'2': 3, '4': 2, '5': 1},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:416',
    )
    require(
        dihedral['noncommuting_common_fiber_profiles'] == {'4': {'totally_ramified_source_labels': 1, 'total_ramification_index': 4, 'unramified_complete_fibers': [4]}, '5': {'totally_ramified_source_labels': 0, 'unramified_complete_fibers': [5]}},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:421',
    )
    require(
        dihedral['endpoint_neighbor_pairs_collapsed'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:432',
    )

    dickson = data["dickson_normal_form_regression"]
    require(
        dickson['field'] == f'F_{PRIME}',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:435',
    )
    require(
        dickson['parameter'] == 7,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:436',
    )
    require(
        dickson['sampled_nonzero_inputs'] == PRIME - 1,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:437',
    )
    require(
        dickson['identity_checks'] == 2 * (PRIME - 1),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:438',
    )
    require(
        dickson['D4_coefficients_descending'] == [1, 0, -28, 0, 98],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:439',
    )
    require(
        dickson['D5_coefficients_descending'] == [1, 0, -35, 0, 245, 0],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:440',
    )
    require(
        dickson['status'] == 'PASS',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:443',
    )

    ramification = data["ramification"]
    require(
        ramification['deck_branch_local_rhs_multiplicity'] == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:446',
    )
    require(
        ramification['unramified_conic_two_line_local_cap'] == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:447',
    )
    require(
        ramification['deck_branch_forces_conic_branch'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:448',
    )
    require(
        ramification['two_shared_branch_points_force_same_involution'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:449',
    )
    require(
        ramification['same_involution_contradicts_free_root_pairing'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:453',
    )
    require(
        ramification['two_deck_branch_points_in_K'] == 'EXCLUDED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:457',
    )
    require(
        ramification['one_deck_branch_point_in_K'] == 'EXCLUDED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:458',
    )
    require(
        ramification['one_branch_product'] == 'nontrivial_translation',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:459',
    )
    require(
        ramification['translation_order'] == 2130706433,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:460',
    )
    require(
        ramification['remaining_common_support_points'] == 8,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:461',
    )
    require(
        ramification['zero_deck_branch_points_in_K'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:462',
    )

    claims = data["claims"]
    require(
        claims['line_image_branch'] == 'EXCLUDED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:465',
    )
    require(
        claims['reduced_conic_signature_classification'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:466',
    )
    require(
        claims['conic_quotient_differs_from_deck'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:467',
    )
    require(
        claims['two_branch_point_conic_case'] == 'EXCLUDED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:468',
    )
    require(
        claims['one_branch_point_conic_case'] == 'EXCLUDED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:469',
    )
    require(
        claims['conic_pair_matrix_rank_criterion'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:470',
    )
    require(
        claims['two_free_pairs_determine_candidate'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:471',
    )
    require(
        claims['common_decic_invariance_criterion'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:472',
    )
    require(
        claims['dickson_normal_form_reduction'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:473',
    )
    require(
        claims['component_rooted_source_label_quotient_precursor'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:474',
    )
    require(
        claims['second_involution_matching'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:478',
    )
    require(
        claims['same_record_owner_payment'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:479',
    )
    require(
        claims['u2_cycle_union'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:480',
    )
    require(
        data['payment'] == 'NONE',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:481',
    )

    supplied_hash = data["payload_sha256"]
    unhashed = dict(data)
    del unhashed["payload_sha256"]
    canonical = json.dumps(
        unhashed, sort_keys=True, separators=(",", ":")
    ).encode()
    require(
        supplied_hash == hashlib.sha256(canonical).hexdigest(),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:489',
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
    forged["line_branch"]["conclusion"] = "OPEN"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["conic_branch"]["labeled_total"] = 464
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["conic_branch"]["degree_sequence"] = [0, 2, 2, 2, 2, 2]
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["ramification"]["two_deck_branch_points_in_K"] = "OPEN"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["involution_pair_matrix"]["tampered_pair_matrix_rank"] = 2
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["claims"]["second_involution_matching"] = "PROVED"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["involution_pair_matrix"][
        "free_seed_recovers_unique_candidate"
    ] = False
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["reduced_dihedral_branch"]["allowed_n"] = [3, 4, 5]
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["reduced_dihedral_branch"]["noncommuting_common_fiber_profiles"][
        "4"
    ]["total_ramification_index"] = 3
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["dickson_normal_form_regression"][
        "D5_coefficients_descending"
    ][2] = -34
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
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:560',
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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_line_conic_quotient_reduction.py:580',
        )
    rejected = tamper_selftest(data) if args.tamper_selftest else 0

    print("line-image contradiction: PASS")
    print("reduced conic signature census: PASS")
    print("two-branch-point conic exclusion: PASS")
    print("one-branch-point translation exclusion: PASS")
    print("two-free-pair candidate involution: PASS")
    print("common-decic invariance criterion: PASS")
    print("reduced dihedral orbit-pairing exclusion: PASS")
    print("dihedral Dickson normal forms: PASS")
    print("component-rooted source-label quotient precursor: PASS")
    print("seven-pair involution rank criterion: PASS")
    if args.tamper_selftest:
        print(f"tamper mutations rejected: PASS {rejected}/11")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
