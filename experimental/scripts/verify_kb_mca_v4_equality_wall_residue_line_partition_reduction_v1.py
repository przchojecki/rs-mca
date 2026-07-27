#!/usr/bin/env python3
"""Verify the KoalaBear equality-wall residue-line partition reduction."""

from __future__ import annotations

import argparse
import copy
import itertools
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_equality_wall_locator_cylinder_reduction_v1 as parent
import verify_kb_mca_v4_next_slack_source_plane_closure_v1 as plane

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-equality-wall-residue-line-partition-reduction-v1"
)
CERT_PATH = CERT_DIR / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_equality_wall_residue_line_partition_reduction_v1.schema.json"
)

ARCH = parent.ARCH
PARTITION_DIGEST = parent.PARTITION_DIGEST
R = parent.R
SOURCE_SIZE = parent.SOURCE_SIZE
E = parent.E
C = parent.C
H = parent.H
CARRIER_SIZE = parent.CARRIER_SIZE
LOCATOR_DEGREE = parent.LOCATOR_DEGREE
B_REMAINING = parent.B_REMAINING
CODE_REDUNDANCY = parent.N - parent.K
CARRIER_CODE_DIMENSION = CARRIER_SIZE - CODE_REDUNDANCY
OUTSIDE_ROOTS = CARRIER_SIZE - LOCATOR_DEGREE
UNRESTRICTED_ONE_SWAP_COUNT = OUTSIDE_ROOTS + 1
COARSE_MAX_EXACT_SWAP_COMPONENT = 1 + OUTSIDE_ROOTS // C
MAX_EXACT_SWAP_COMPONENT = 1 + OUTSIDE_ROOTS // E
FIELD_P = parent.sweep.P
SOURCE_MAP_POINT_CAP = B_REMAINING // CARRIER_SIZE
UNWEIGHTED_LINE_CAP = 68
UNWEIGHTED_GLOBAL_POINT_CAP = (
    (UNWEIGHTED_LINE_CAP - 1) * FIELD_P + UNWEIGHTED_LINE_CAP
)
UNWEIGHTED_LINE_CHARGE = UNWEIGHTED_GLOBAL_POINT_CAP * CARRIER_SIZE
UNWEIGHTED_LINE_MARGIN = B_REMAINING - UNWEIGHTED_LINE_CHARGE
ADJACENT_UNWEIGHTED_LINE_CAP = UNWEIGHTED_LINE_CAP + 1
ADJACENT_GLOBAL_POINT_CAP = (
    (ADJACENT_UNWEIGHTED_LINE_CAP - 1) * FIELD_P
    + ADJACENT_UNWEIGHTED_LINE_CAP
)
ADJACENT_UNWEIGHTED_LINE_CHARGE = (
    ADJACENT_GLOBAL_POINT_CAP * CARRIER_SIZE
)
ADJACENT_UNWEIGHTED_LINE_DEFICIT = (
    ADJACENT_UNWEIGHTED_LINE_CHARGE - B_REMAINING
)
MIN_COMPONENTS_IN_69_POINT_FALSIFIER = (
    ADJACENT_UNWEIGHTED_LINE_CAP + MAX_EXACT_SWAP_COMPONENT - 1
) // MAX_EXACT_SWAP_COMPONENT
TWO_POINT_COMPONENT_COMMON_ZERO_SIZE = (
    CARRIER_SIZE - LOCATOR_DEGREE - E
)
MIN_COMPONENT_COMMON_ZERO_SIZE = (
    CARRIER_SIZE
    - LOCATOR_DEGREE
    - (MAX_EXACT_SWAP_COMPONENT - 1) * E
)
TWO_POINT_COMPONENT_QUOTIENT_DEGREE_CAP = E - C
MAX_COMPONENT_QUOTIENT_DEGREE_CAP = (
    (MAX_EXACT_SWAP_COMPONENT - 1) * E - C
)
SOURCE_RATIONAL_DEGREE_THRESHOLD = (SOURCE_SIZE - 1) // 2
ACTUAL_SOURCE_MAP_DEGREE_EXCESS = E - SOURCE_RATIONAL_DEGREE_THRESHOLD
DEEP_ERROR_SUPPORT_THRESHOLD = 349_525
FROBENIUS_EFFECTIVE_MULTIPLIER_THRESHOLD = 9_208
MIN_COMPONENT_MOVING_BLOCK_WEIGHT = E + C
TWO_POINT_PER_MOVING_BLOCK_WEIGHT_FLOOR = E - C
TARGET_PACKET_SIZE = 69
TARGET_PAIR_COUNT = TARGET_PACKET_SIZE * (TARGET_PACKET_SIZE - 1) // 2
MIN_PAIR_SECANT_EXCHANGE_WEIGHT = 2 * C
SOURCE_AND_PAIR_FORBIDDEN_PARAMETER_CAP = SOURCE_SIZE + TARGET_PAIR_COUNT
FULL_DOMAIN_SOURCE_UNIT_FORBIDDEN_PARAMETER_CAP = (
    SOURCE_SIZE + TARGET_PACKET_SIZE * CARRIER_SIZE + TARGET_PAIR_COUNT
)
SOURCE_SELECTOR_SECANT_POLYNOMIAL_DEGREE_CAP = (
    SOURCE_SIZE + CARRIER_SIZE - LOCATOR_DEGREE - C
)
SELECTOR_KERNEL_DIMENSION = 8
MIN_FUNDAMENTAL_CIRCUITS_IN_69_POINT_PACKET = (
    TARGET_PACKET_SIZE - 1 - SELECTOR_KERNEL_DIMENSION
)
MAX_FUNDAMENTAL_EDGE_CIRCUIT_SIZE = SELECTOR_KERNEL_DIMENSION + 1
MIN_ACTUAL_RECORD_CIRCUIT_SIZE = 3
MAX_ACTUAL_RECORD_CIRCUIT_SIZE = SELECTOR_KERNEL_DIMENSION + 2
MINIMAL_CIRCUIT_SELECTOR_RANK_CAP_OFFSET = (
    SELECTOR_KERNEL_DIMENSION + 2
)
THREE_RECORD_CIRCUIT_SELECTOR_RANK_CAP = (
    MINIMAL_CIRCUIT_SELECTOR_RANK_CAP_OFFSET
    - MIN_ACTUAL_RECORD_CIRCUIT_SIZE
)
THREE_RECORD_CIRCUIT_COMMON_ZERO_FLOOR = (
    CARRIER_SIZE - (MIN_ACTUAL_RECORD_CIRCUIT_SIZE * LOCATOR_DEGREE) // 2
)

Failure = parent.Failure
need = parent.need
seal = parent.seal
dump = parent.dump
load = parent.load
file_digest = parent.file_digest
residue = parent.residue

UPSTREAM_CERTIFICATES = {
    "equality_wall_locator_cylinder": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-equality-wall-locator-cylinder-reduction-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '3ca9175475b752b2478e36e308594aa9a973c1f6fcd6d888a95068f0d89c7453'
        ),
    }
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_locator_cylinder_reduction_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_reciprocal_kernel_plane_sweep_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_source_interpolation_pencil_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_complement_locator_linearization_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_residue_line_partition_reduction_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_next_slack_source_plane_closure_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_c5_twist_frobenius9208_adapter_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_tangent_deep_owner_adapter_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_tangent_deep_source_rational_adapter_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_tangent_source_adapter_v1.md"
    ),
    "experimental/notes/thresholds/split_locator_star_flat_intersection.md",
    (
        "experimental/data/certificates/rank16-active-pencil-cap130/"
        "RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT.md"
    ),
    (
        "experimental/data/certificates/rank16-active-pencil-cap130/"
        "RANK16_WEIGHTED_GRID_EXTACTIC_DPW_CAP130.md"
    ),
    (
        "experimental/notes/m1/"
        "m1_kb_branch3_actual_core_mds_rank_ladder_v1.md"
    ),
    (
        "experimental/notes/m1/"
        "m1_kb_rank9_projective_source_load_v1.md"
    ),
]


def source_bindings() -> list[dict[str, str]]:
    bindings = []
    for index, path_text in enumerate(SOURCE_PATHS):
        path = ROOT / path_text
        need(path.is_file(), f"missing source: {path_text}")
        bindings.append(
            {
                "binding_id": (
                    f"SOURCE_{index:02d}_{path.stem.upper().replace('-', '_')}"
                ),
                "hash": file_digest(path),
                "hash_kind": "SHA256",
                "path": path_text,
            }
        )
    return bindings


def upstream_bindings() -> dict[str, dict[str, str]]:
    bindings = {}
    for key, contract in UPSTREAM_CERTIFICATES.items():
        path = ROOT / contract["path"]
        need(path.is_file(), f"missing upstream certificate: {key}")
        certificate = load(path)
        need(
            certificate.get("payload_sha256")
            == contract["payload_sha256"],
            f"upstream payload mismatch: {key}",
        )
        bindings[key] = {**contract, "file_sha256": file_digest(path)}
    return bindings


def polynomial_gcd(polynomials: list[list[int]], prime: int) -> list[int]:
    nonzero = [residue.trim(poly) for poly in polynomials if residue.trim(poly) != [0]]
    need(nonzero, "gcd of all-zero polynomial family")
    result = nonzero[0]
    for polynomial in nonzero[1:]:
        result = residue.gcd_poly(result, polynomial, prime)
    return residue.trim(result)


def add_poly(
    left: list[int], right: list[int], prime: int
) -> list[int]:
    length = max(len(left), len(right))
    return residue.trim(
        [
            (
                (left[index] if index < len(left) else 0)
                + (right[index] if index < len(right) else 0)
            )
            % prime
            for index in range(length)
        ]
    )


def scale_poly(
    polynomial: list[int], scalar: int, prime: int
) -> list[int]:
    return residue.trim(
        [scalar * coefficient % prime for coefficient in polynomial]
    )


def combine_polynomials(
    polynomials: list[list[int]],
    coefficients: tuple[int, ...],
    prime: int,
) -> list[int]:
    result = [0]
    for coefficient, polynomial in zip(coefficients, polynomials):
        result = add_poly(
            result, scale_poly(polynomial, coefficient, prime), prime
        )
    return result


def projective_triples(prime: int) -> list[tuple[int, int, int]]:
    triples = []
    for first in range(3):
        prefix = [0] * first + [1]
        for tail in itertools.product(range(prime), repeat=2 - first):
            triples.append(tuple([*prefix, *tail]))
    return triples


def one_root_pencil_control(
    prime: int,
    source_size: int,
    carrier_size: int,
    locator_degree: int,
) -> dict[str, Any]:
    need(source_size + carrier_size <= prime, "field too small")
    need(locator_degree <= carrier_size, "locator exceeds carrier")
    source = list(range(source_size))
    carrier = list(range(source_size, source_size + carrier_size))
    core = carrier[: locator_degree - 1]
    moving_roots = carrier[locator_degree - 1 :]
    _, inverse = plane.evaluation_inverse(prime, source_size)
    locators = [
        residue.locator([*core, root], prime) for root in moving_roots
    ]
    locator_rank = residue.rank(locators, prime)
    residues = [
        parent.pad(
            residue.matrix_vector(
                inverse,
                plane.polynomial_values(locator, source, prime),
                prime,
            ),
            source_size,
        )
        for locator in locators
    ]
    residue_rank = residue.rank(residues, prime)
    need(locator_rank == 2, "one-root pencil polynomial rank")
    need(residue_rank <= 2, "one-root pencil residue rank")
    need(
        len(locators) == carrier_size - locator_degree + 1,
        "one-root pencil count",
    )
    need(
        all(
            set(left[:-1]) == set(right[:-1])
            for left, right in itertools.combinations(
                [[*core, root] for root in moving_roots], 2
            )
        ),
        "one-root common core",
    )
    return {
        "prime": prime,
        "source_size": source_size,
        "carrier_size": carrier_size,
        "locator_degree": locator_degree,
        "common_core_degree": locator_degree - 1,
        "actual_locator_count": len(locators),
        "polynomial_span_dimension": locator_rank,
        "residue_span_dimension": residue_rank,
        "source_and_selector_status": "FORGOTTEN_ROUTE_CUT_ONLY",
    }


def build_parent_fixture() -> dict[str, Any]:
    summary = parent.locator_cylinder_route_cut()
    prime = summary["prime"]
    source = list(range(summary["source_size"]))
    source_locator = residue.locator(source, prime)
    _, inverse = plane.evaluation_inverse(prime, len(source))
    locator_sets = summary["locator_sets"]
    reciprocal_columns = [
        [2, 5, 8, 1],
        [15, 15, 15, 0, 1],
        [4, 0, 0, 0, 0, 1],
    ]
    locators = [residue.locator(points, prime) for points in locator_sets]
    locator_values = [
        plane.polynomial_values(locator, source, prime)
        for locator in locators
    ]
    locator_residues = [
        parent.pad(
            residue.matrix_vector(inverse, values, prime), len(source)
        )
        for values in locator_values
    ]
    reciprocal_values = [
        plane.polynomial_values(column, source, prime)
        for column in reciprocal_columns
    ]
    product_rows = [
        [
            residue.trim(
                residue.matrix_vector(
                    inverse,
                    [
                        q_value * reciprocal_value % prime
                        for q_value, reciprocal_value in zip(
                            q_values, column_values
                        )
                    ],
                    prime,
                )
            )
            for column_values in reciprocal_values
        ]
        for q_values in locator_values
    ]
    basis_indices = summary["basis_indices"]
    product_basis = [product_rows[index] for index in basis_indices]
    return {
        "prime": prime,
        "source": source,
        "source_locator": source_locator,
        "inverse": inverse,
        "locator_sets": locator_sets,
        "locators": locators,
        "locator_residues": locator_residues,
        "reciprocal_columns": reciprocal_columns,
        "product_rows": product_rows,
        "basis_indices": basis_indices,
        "product_basis": product_basis,
        "parent_summary": summary,
    }


def primitive_line_control() -> dict[str, Any]:
    fixture = build_parent_fixture()
    prime = fixture["prime"]
    source_locator = fixture["source_locator"]
    product_basis = fixture["product_basis"]
    locator_residues = fixture["locator_residues"]
    basis_indices = fixture["basis_indices"]

    quotient_minors = []
    raw_minors = []
    for left, right in [(1, 2), (0, 2), (0, 1)]:
        minor = parent.minor_two(
            product_basis, 0, 1, left, right, prime
        )
        quotient, remainder = residue.divmod_poly(
            minor, source_locator, prime
        )
        need(remainder == [0], "line cofactor lacks source factor")
        need(len(quotient) - 1 <= 2, "line cofactor degree")
        raw_minors.append(minor)
        quotient_minors.append(quotient)

    cofactor_gcd = polynomial_gcd(quotient_minors, prime)
    raw_gcd = polynomial_gcd(raw_minors, prime)
    need(cofactor_gcd == [1], "F19 line must be primitive")
    need(raw_gcd == source_locator, "primitive determinantal ideal")

    line_indices = [0, 1, 2]
    line_residue_rank = residue.rank(
        [locator_residues[index] for index in line_indices], prime
    )
    need(line_residue_rank == 2, "three locators not on one residue line")
    locator_sets = fixture["locator_sets"]
    common_core = set(locator_sets[line_indices[0]])
    for index in line_indices[1:]:
        common_core &= set(locator_sets[index])
    moving_blocks = [
        set(locator_sets[index]) - common_core for index in line_indices
    ]
    need(len(common_core) == 6, "F19 common core")
    need(all(len(block) == 2 for block in moving_blocks), "F19 exchange")
    need(
        all(left.isdisjoint(right) for left, right in itertools.combinations(moving_blocks, 2)),
        "F19 moving blocks are not disjoint",
    )
    component_bound = 1 + (12 - 8) // 2
    need(component_bound == 3, "F19 component bound")
    need(len(line_indices) == component_bound, "F19 sharp component")

    reciprocal_dimension = plane.reciprocal_dimension(
        [locator_residues[index] for index in basis_indices],
        fixture["source"],
        fixture["inverse"],
        4,
        prime,
    )
    need(reciprocal_dimension == 3, "F19 complete reciprocal dimension")

    good_reciprocal_parameters = []
    for parameter in projective_triples(prime):
        left_product = combine_polynomials(
            product_basis[0], parameter, prime
        )
        right_product = combine_polynomials(
            product_basis[1], parameter, prime
        )
        if max(len(left_product), len(right_product)) - 1 != 4:
            continue
        if residue.gcd_poly(left_product, right_product, prime) != [1]:
            continue
        good_reciprocal_parameters.append(parameter)
    need(
        good_reciprocal_parameters,
        "F19 lacks coprime exact-degree reciprocal direction",
    )
    generic_parameter = good_reciprocal_parameters[0]
    generic_products = [
        combine_polynomials(row, generic_parameter, prime)
        for row in fixture["product_rows"]
    ]
    generic_exact_edges = 0
    generic_nonzero_edges = 0
    for left, right in itertools.combinations(line_indices, 2):
        left_set = set(locator_sets[left])
        right_set = set(locator_sets[right])
        left_moving = residue.locator(
            sorted(left_set - right_set), prime
        )
        right_moving = residue.locator(
            sorted(right_set - left_set), prime
        )
        cross = add_poly(
            residue.mul(
                generic_products[left], right_moving, prime
            ),
            scale_poly(
                residue.mul(
                    generic_products[right], left_moving, prime
                ),
                -1,
                prime,
            ),
            prime,
        )
        quotient, remainder = residue.divmod_poly(
            cross, source_locator, prime
        )
        need(remainder == [0], "F19 generic exchange source divisibility")
        if quotient == [0]:
            generic_exact_edges += 1
        else:
            generic_nonzero_edges += 1
    need(generic_exact_edges == 0, "F19 generic low swap remained exact")
    need(generic_nonzero_edges == 3, "F19 generic nonzero edge count")
    generic_component_bound = 1 + (12 - 8) // 4
    need(generic_component_bound == 2, "F19 generic component bound")
    return {
        "prime": prime,
        "source_size": 6,
        "source_degree": 4,
        "c": 2,
        "carrier_size": 12,
        "locator_degree": 8,
        "complete_reciprocal_dimension": reciprocal_dimension,
        "line_locator_indices": line_indices,
        "line_residue_dimension": line_residue_rank,
        "cofactor_quotients": quotient_minors,
        "cofactor_gcd": cofactor_gcd,
        "determinantal_gcd": raw_gcd,
        "common_core_size": len(common_core),
        "exchange_size": 2,
        "exact_swap_component_size": len(line_indices),
        "exact_swap_component_bound": component_bound,
        "coprime_exact_degree_reciprocal_parameter_count": len(
            good_reciprocal_parameters
        ),
        "selected_coprime_exact_degree_reciprocal_parameter": list(
            generic_parameter
        ),
        "generic_reciprocal_resultant_degree_cap": 8,
        "generic_exact_swap_edges": generic_exact_edges,
        "generic_nonzero_exchange_edges": generic_nonzero_edges,
        "generic_exact_swap_component_bound": generic_component_bound,
    }


def four_component_line_control() -> dict[str, Any]:
    prime = 23
    source = list(range(6))
    source_locator = residue.locator(source, prime)
    source_square = residue.mul(source_locator, source_locator, prime)
    _, inverse = plane.evaluation_inverse(prime, len(source))
    line_locator_sets = [
        [6, 7, 8, 10, 11, 15, 16, 17, 18, 19],
        [6, 7, 9, 12, 13, 14, 15, 16, 17, 18],
        [7, 8, 9, 10, 11, 13, 15, 16, 17, 19],
        [7, 8, 10, 11, 12, 14, 15, 16, 17, 19],
    ]
    outside_locator_set = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    locator_sets = [*line_locator_sets, outside_locator_set]
    reciprocal_columns = [
        [18, 12, 21, 1],
        [21, 5, 8, 0, 1],
        [1, 14, 7, 0, 0, 1],
    ]
    locators = [residue.locator(points, prime) for points in locator_sets]
    locator_values = [
        plane.polynomial_values(locator, source, prime)
        for locator in locators
    ]
    locator_residues = [
        parent.pad(
            residue.matrix_vector(inverse, values, prime), len(source)
        )
        for values in locator_values
    ]
    need(
        residue.rank(locator_residues[:4], prime) == 2,
        "F23 four-component locators not on one line",
    )
    need(
        residue.rank(locator_residues, prime) == 3,
        "F23 occupied residue span",
    )
    need(
        plane.reciprocal_dimension(
            locator_residues, source, inverse, 4, prime
        )
        == 3,
        "F23 complete reciprocal dimension",
    )

    reciprocal_values = [
        plane.polynomial_values(column, source, prime)
        for column in reciprocal_columns
    ]
    product_rows = [
        [
            residue.trim(
                residue.matrix_vector(
                    inverse,
                    [
                        q_value * reciprocal_value % prime
                        for q_value, reciprocal_value in zip(
                            q_values, column_values
                        )
                    ],
                    prime,
                )
            )
            for column_values in reciprocal_values
        ]
        for q_values in locator_values
    ]
    determinant = parent.determinant_three(
        [product_rows[index] for index in [0, 1, 4]], prime
    )
    quotient, remainder = residue.divmod_poly(
        determinant, source_square, prime
    )
    need(remainder == [0], "F23 rank-three determinant source square")
    need(quotient != [0], "F23 product rank is not three")

    quotient_minors = []
    for left, right in [(1, 2), (0, 2), (0, 1)]:
        minor = parent.minor_two(
            product_rows, 0, 1, left, right, prime
        )
        quotient, remainder = residue.divmod_poly(
            minor, source_locator, prime
        )
        need(remainder == [0], "F23 line minor source factor")
        quotient_minors.append(quotient)
    need(
        polynomial_gcd(quotient_minors, prime) == [1],
        "F23 four-component line must be primitive",
    )
    collision_minor = parent.minor_two(
        product_rows, 0, 1, 0, 1, prime
    )
    collision_divisor, remainder = residue.divmod_poly(
        collision_minor, source_locator, prime
    )
    need(remainder == [0], "F23 collision divisor source factor")
    need(
        len(collision_divisor) - 1 == 2,
        "F23 collision divisor degree",
    )
    carrier = list(range(6, 20))
    collision_values = plane.polynomial_values(
        collision_divisor, carrier, prime
    )
    need(
        all(value != 0 for value in collision_values),
        "F23 collision divisor carrier root",
    )

    good_parameters = []
    for parameter in projective_triples(prime):
        products = [
            combine_polynomials(row, parameter, prime)
            for row in product_rows[:4]
        ]
        if max(len(products[0]), len(products[1])) - 1 != 4:
            continue
        if residue.gcd_poly(products[0], products[1], prime) != [1]:
            continue
        good_parameters.append((parameter, products))
    need(
        len(good_parameters) == 403,
        "F23 generic reciprocal parameter count",
    )
    selected_parameter, products = good_parameters[0]

    exact_edges = []
    nonzero_edges = []
    distances = []
    for left, right in itertools.combinations(range(4), 2):
        left_set = set(line_locator_sets[left])
        right_set = set(line_locator_sets[right])
        distances.append(len(left_set - right_set))
        left_moving = residue.locator(
            sorted(left_set - right_set), prime
        )
        right_moving = residue.locator(
            sorted(right_set - left_set), prime
        )
        cross = add_poly(
            residue.mul(products[left], right_moving, prime),
            scale_poly(
                residue.mul(products[right], left_moving, prime),
                -1,
                prime,
            ),
            prime,
        )
        quotient, remainder = residue.divmod_poly(
            cross, source_locator, prime
        )
        need(remainder == [0], "F23 exchange source divisibility")
        if quotient == [0]:
            exact_edges.append([left, right])
        else:
            nonzero_edges.append([left, right])
    need(min(distances) == 2, "F23 pair-distance guard")
    need(not exact_edges, "F23 unexpected generic exact edge")
    need(len(nonzero_edges) == 6, "F23 nonzero edge count")

    return {
        "prime": prime,
        "source_size": 6,
        "source_degree": 4,
        "c": 2,
        "carrier_size": 14,
        "locator_degree": 10,
        "line_projective_point_count": 4,
        "line_residue_dimension": 2,
        "occupied_residue_dimension": 3,
        "complete_reciprocal_dimension": 3,
        "product_rank": 3,
        "cofactor_gcd": [1],
        "source_coordinate_collision_divisor": collision_divisor,
        "source_coordinate_collision_divisor_degree": (
            len(collision_divisor) - 1
        ),
        "source_coordinate_collision_divisor_carrier_roots": 0,
        "minimum_exchange": min(distances),
        "coprime_exact_degree_reciprocal_parameter_count": len(
            good_parameters
        ),
        "selected_coprime_exact_degree_reciprocal_parameter": list(
            selected_parameter
        ),
        "generic_exact_edges": exact_edges,
        "generic_nonzero_edges": nonzero_edges,
        "generic_exact_swap_component_sizes": [1, 1, 1, 1],
        "selector_and_first_match_status": "NOT_CONSTRUCTED_ROUTE_CUT_ONLY",
    }


def partition_cofactor_control() -> dict[str, Any]:
    prime = 19
    source = list(range(6))
    source_locator = residue.locator(source, prime)
    source_square = residue.mul(source_locator, source_locator, prime)
    partition = residue.locator([0, 1], prime)
    diagonal = [
        residue.locator([0, 1, 2, 3], prime),
        residue.locator([0, 1, 4, 5], prime),
        residue.locator([2, 3, 4, 5], prime),
    ]
    matrix = [
        [diagonal[0], [0], [0]],
        [[0], diagonal[1], [0]],
        [[0], [0], diagonal[2]],
    ]
    determinant = parent.determinant_three(matrix, prime)
    need(determinant == source_square, "partition fixture determinant")
    quotient_minors = []
    for left, right in [(1, 2), (0, 2), (0, 1)]:
        minor = parent.minor_two(matrix, 0, 1, left, right, prime)
        if minor == [0]:
            quotient_minors.append([0])
            continue
        quotient, remainder = residue.divmod_poly(
            minor, source_locator, prime
        )
        need(remainder == [0], "partition cofactor source factor")
        quotient_minors.append(quotient)
    cofactor_gcd = polynomial_gcd(quotient_minors, prime)
    need(cofactor_gcd == partition, "partition cofactor gcd")
    quotient, remainder = residue.divmod_poly(
        source_locator, cofactor_gcd, prime
    )
    need(remainder == [0] and len(quotient) - 1 == 4, "proper partition")
    pointwise_ranks = []
    for point in source:
        evaluated = [
            [residue.evaluate(entry, point, prime) for entry in row]
            for row in matrix
        ]
        pointwise_ranks.append(residue.rank(evaluated, prime))
    need(pointwise_ranks == [1] * len(source), "pointwise rank-one fixture")
    return {
        "prime": prime,
        "source_size": len(source),
        "source_degree": 4,
        "c": 2,
        "determinant_quotient": 1,
        "cofactor_quotients": quotient_minors,
        "cofactor_gcd": cofactor_gcd,
        "partition_roots": [0, 1],
        "partition_degree": len(cofactor_gcd) - 1,
        "pointwise_ranks": pointwise_ranks,
        "source_product_identity_status": (
            "NOT_SATISFIED_ALGEBRAIC_ROUTE_CUT_ONLY"
        ),
    }


def component_rank_precursor_control() -> dict[str, Any]:
    rows = []
    previous_common_zero_size = None
    for component_size in range(2, MAX_EXACT_SWAP_COMPONENT + 1):
        common_zero_size = (
            CARRIER_SIZE
            - LOCATOR_DEGREE
            - (component_size - 1) * E
        )
        quotient_degree_cap = (
            CARRIER_CODE_DIMENSION - 1 - common_zero_size
        )
        expected_quotient_cap = (component_size - 1) * E - C
        moving_block_size = component_size * E
        moving_block_weight_floor = (
            moving_block_size - expected_quotient_cap
        )
        need(
            quotient_degree_cap == expected_quotient_cap,
            "component quotient degree identity",
        )
        need(
            moving_block_weight_floor == MIN_COMPONENT_MOVING_BLOCK_WEIGHT,
            "component moving-block weight floor",
        )
        need(common_zero_size > 0, "component common-zero positivity")
        if previous_common_zero_size is not None:
            need(
                common_zero_size == previous_common_zero_size - E,
                "component common-zero decrement",
            )
        previous_common_zero_size = common_zero_size
        rows.append(
            {
                "component_size": component_size,
                "common_zero_size": common_zero_size,
                "selector_restriction_rank_cap": 7,
                "nonzero_k0_word_exists": True,
                "grs_quotient_degree_cap": quotient_degree_cap,
                "moving_block_size": moving_block_size,
                "minimum_nonzero_k0_weight_on_moving_blocks": (
                    moving_block_weight_floor
                ),
            }
        )
    need(
        rows[0]["common_zero_size"]
        == TWO_POINT_COMPONENT_COMMON_ZERO_SIZE,
        "two-point component common-zero size",
    )
    need(
        rows[0]["grs_quotient_degree_cap"]
        == TWO_POINT_COMPONENT_QUOTIENT_DEGREE_CAP,
        "two-point component quotient degree cap",
    )
    need(
        rows[-1]["common_zero_size"] == MIN_COMPONENT_COMMON_ZERO_SIZE,
        "minimum component common-zero size",
    )
    need(
        rows[-1]["grs_quotient_degree_cap"]
        == MAX_COMPONENT_QUOTIENT_DEGREE_CAP,
        "maximum component quotient degree cap",
    )
    return {
        "selector_dimension": 8,
        "carrier_code_redundancy": CODE_REDUNDANCY,
        "carrier_code_dimension": CARRIER_CODE_DIMENSION,
        "carrier_code_minimum_distance": CODE_REDUNDANCY + 1,
        "two_point_per_moving_block_weight_floor": (
            TWO_POINT_PER_MOVING_BLOCK_WEIGHT_FLOOR
        ),
        "rows": rows,
        "payment_status": "OPEN_SAME_OBJECT_OWNER_ADAPTER_REQUIRED",
    }


def exact_arithmetic() -> dict[str, Any]:
    need(H == 0, "equality extra common factor degree")
    need(E == 2 * C, "e=2c")
    need(SOURCE_SIZE == 3 * C, "s=3c")
    need(OUTSIDE_ROOTS == 913_631, "outside root count")
    need(
        UNRESTRICTED_ONE_SWAP_COUNT == 913_632,
        "deployed one-root pencil count",
    )
    need(UNRESTRICTED_ONE_SWAP_COUNT > 130, "bare line cap route cut")
    need(
        COARSE_MAX_EXACT_SWAP_COMPONENT == 14,
        "coarse exact-swap component cap",
    )
    need(MAX_EXACT_SWAP_COMPONENT == 7, "generic exact-swap component cap")
    need(2 * E == 269_888, "resultant degree cap")
    need(2 * E < FIELD_P, "finite-field resultant avoidance")
    need(FIELD_P == 2_130_706_433, "base field")
    need(
        SOURCE_MAP_POINT_CAP == 142_911_842_578,
        "source-map occupied-point cap",
    )
    need(
        UNWEIGHTED_GLOBAL_POINT_CAP == 142_757_331_079,
        "cap-68 global point count",
    )
    need(
        UNWEIGHTED_LINE_CHARGE == 270_487_454_459_300_144,
        "cap-68 source-map charge",
    )
    need(
        UNWEIGHTED_LINE_MARGIN == 292_758_501_275_736,
        "cap-68 reserve margin",
    )
    need(
        ADJACENT_GLOBAL_POINT_CAP == 144_888_037_513,
        "cap-69 global point count",
    )
    need(
        ADJACENT_UNWEIGHTED_LINE_CHARGE
        == 274_524_580_645_231_568,
        "cap-69 source-map charge",
    )
    need(
        ADJACENT_UNWEIGHTED_LINE_DEFICIT
        == 3_744_367_684_655_688,
        "cap-69 reserve deficit",
    )
    need(
        MIN_COMPONENTS_IN_69_POINT_FALSIFIER == 10,
        "69-point packet needs at least ten exact-swap components",
    )
    need(CODE_REDUNDANCY == 1_048_576, "carrier code redundancy")
    need(
        CARRIER_CODE_DIMENSION == 846_160,
        "carrier code dimension",
    )
    need(
        TWO_POINT_COMPONENT_COMMON_ZERO_SIZE == 778_687,
        "two-point component common-zero size",
    )
    need(
        MIN_COMPONENT_COMMON_ZERO_SIZE == 103_967,
        "minimum component common-zero size",
    )
    need(
        TWO_POINT_COMPONENT_QUOTIENT_DEGREE_CAP == C,
        "two-point component quotient cap equals c",
    )
    need(
        MAX_COMPONENT_QUOTIENT_DEGREE_CAP == 742_192,
        "maximum component quotient degree cap",
    )
    need(
        SOURCE_RATIONAL_DEGREE_THRESHOLD == 101_207,
        "source-rational degree threshold",
    )
    need(
        TWO_POINT_COMPONENT_QUOTIENT_DEGREE_CAP
        < SOURCE_RATIONAL_DEGREE_THRESHOLD,
        "two-point quotient is numerically below rational threshold",
    )
    need(
        ACTUAL_SOURCE_MAP_DEGREE_EXCESS == 33_737,
        "actual source-map degree excess",
    )
    need(
        CODE_REDUNDANCY + 1 > DEEP_ERROR_SUPPORT_THRESHOLD,
        "component K0 word is not a deep selected error",
    )
    need(
        C > FROBENIUS_EFFECTIVE_MULTIPLIER_THRESHOLD,
        "component quotient cap does not imply Frobenius degree",
    )
    need(
        MIN_COMPONENT_MOVING_BLOCK_WEIGHT == SOURCE_SIZE,
        "component moving-block mass equals source size",
    )
    need(
        TWO_POINT_PER_MOVING_BLOCK_WEIGHT_FLOOR == C,
        "two-point per-moving-block mass floor",
    )
    need(TARGET_PAIR_COUNT == 2_346, "69-point pair count")
    need(
        TARGET_PAIR_COUNT < FIELD_P,
        "simultaneous reciprocal genericization degree",
    )
    need(
        MIN_PAIR_SECANT_EXCHANGE_WEIGHT == E,
        "minimum pair-secant exchange weight",
    )
    need(
        SOURCE_AND_PAIR_FORBIDDEN_PARAMETER_CAP == 204_762,
        "source-and-pair forbidden parameter cap",
    )
    need(
        FULL_DOMAIN_SOURCE_UNIT_FORBIDDEN_PARAMETER_CAP == 130_941_546,
        "full-domain source-unit forbidden parameter cap",
    )
    need(
        FULL_DOMAIN_SOURCE_UNIT_FORBIDDEN_PARAMETER_CAP < FIELD_P,
        "full-domain source-unit projective parameter avoidance",
    )
    need(
        SOURCE_SELECTOR_SECANT_POLYNOMIAL_DEGREE_CAP == parent.K - 1,
        "source-selector secant polynomial is a K0 word",
    )
    need(
        MIN_FUNDAMENTAL_CIRCUITS_IN_69_POINT_PACKET == 60,
        "fundamental circuit count",
    )
    need(
        MAX_FUNDAMENTAL_EDGE_CIRCUIT_SIZE == 9,
        "fundamental edge-circuit size",
    )
    need(
        MAX_ACTUAL_RECORD_CIRCUIT_SIZE == 10,
        "actual-record circuit size",
    )
    need(C < SOURCE_SIZE, "proper partition degree range")
    return {
        "r": R,
        "source_size": SOURCE_SIZE,
        "e": E,
        "c": C,
        "carrier_size": CARRIER_SIZE,
        "locator_degree": LOCATOR_DEGREE,
        "roots_outside_locator": OUTSIDE_ROOTS,
        "unrestricted_one_root_pencil_count": (
            UNRESTRICTED_ONE_SWAP_COUNT
        ),
        "former_sufficient_line_cap": 130,
        "source_map_image_cap_per_projective_direction": CARRIER_SIZE,
        "source_map_occupied_point_cap": SOURCE_MAP_POINT_CAP,
        "sufficient_unweighted_line_cap": UNWEIGHTED_LINE_CAP,
        "cap_68_global_occupied_point_cap": UNWEIGHTED_GLOBAL_POINT_CAP,
        "cap_68_source_map_charge": UNWEIGHTED_LINE_CHARGE,
        "cap_68_reserve_margin": UNWEIGHTED_LINE_MARGIN,
        "adjacent_unweighted_line_cap": ADJACENT_UNWEIGHTED_LINE_CAP,
        "cap_69_global_occupied_point_cap": ADJACENT_GLOBAL_POINT_CAP,
        "cap_69_source_map_charge": ADJACENT_UNWEIGHTED_LINE_CHARGE,
        "cap_69_reserve_deficit": ADJACENT_UNWEIGHTED_LINE_DEFICIT,
        "minimum_components_in_69_point_falsifier": (
            MIN_COMPONENTS_IN_69_POINT_FALSIFIER
        ),
        "extra_common_factor_degree": H,
        "occupied_direction_gcd_degree": 0,
        "carrier_code_redundancy": CODE_REDUNDANCY,
        "carrier_code_dimension": CARRIER_CODE_DIMENSION,
        "two_point_component_common_zero_size": (
            TWO_POINT_COMPONENT_COMMON_ZERO_SIZE
        ),
        "minimum_component_common_zero_size": (
            MIN_COMPONENT_COMMON_ZERO_SIZE
        ),
        "two_point_component_grs_quotient_degree_cap": (
            TWO_POINT_COMPONENT_QUOTIENT_DEGREE_CAP
        ),
        "maximum_component_grs_quotient_degree_cap": (
            MAX_COMPONENT_QUOTIENT_DEGREE_CAP
        ),
        "source_rational_degree_threshold": (
            SOURCE_RATIONAL_DEGREE_THRESHOLD
        ),
        "actual_source_map_degree_excess_over_rational_threshold": (
            ACTUAL_SOURCE_MAP_DEGREE_EXCESS
        ),
        "deep_error_support_threshold": DEEP_ERROR_SUPPORT_THRESHOLD,
        "carrier_code_minimum_distance": CODE_REDUNDANCY + 1,
        "frobenius_effective_multiplier_threshold": (
            FROBENIUS_EFFECTIVE_MULTIPLIER_THRESHOLD
        ),
        "minimum_component_k0_weight_on_moving_blocks": (
            MIN_COMPONENT_MOVING_BLOCK_WEIGHT
        ),
        "two_point_per_moving_block_weight_floor": (
            TWO_POINT_PER_MOVING_BLOCK_WEIGHT_FLOOR
        ),
        "simultaneous_genericization_packet_size": TARGET_PACKET_SIZE,
        "simultaneous_genericization_pair_count": TARGET_PAIR_COUNT,
        "simultaneous_genericization_degree_margin": (
            FIELD_P - TARGET_PAIR_COUNT
        ),
        "minimum_pair_selector_secant_exchange_weight": (
            MIN_PAIR_SECANT_EXCHANGE_WEIGHT
        ),
        "source_and_pair_forbidden_parameter_cap": (
            SOURCE_AND_PAIR_FORBIDDEN_PARAMETER_CAP
        ),
        "full_domain_source_unit_forbidden_parameter_cap": (
            FULL_DOMAIN_SOURCE_UNIT_FORBIDDEN_PARAMETER_CAP
        ),
        "full_domain_source_unit_parameter_avoidance_margin_over_base_field": (
            FIELD_P - FULL_DOMAIN_SOURCE_UNIT_FORBIDDEN_PARAMETER_CAP
        ),
        "source_selector_secant_polynomial_degree_cap": (
            SOURCE_SELECTOR_SECANT_POLYNOMIAL_DEGREE_CAP
        ),
        "source_selector_secant_code_dimension_minus_one": parent.K - 1,
        "selector_kernel_dimension": SELECTOR_KERNEL_DIMENSION,
        "minimum_fundamental_circuits_in_69_point_packet": (
            MIN_FUNDAMENTAL_CIRCUITS_IN_69_POINT_PACKET
        ),
        "maximum_fundamental_edge_circuit_size": (
            MAX_FUNDAMENTAL_EDGE_CIRCUIT_SIZE
        ),
        "minimum_actual_record_circuit_size": (
            MIN_ACTUAL_RECORD_CIRCUIT_SIZE
        ),
        "maximum_actual_record_circuit_size": (
            MAX_ACTUAL_RECORD_CIRCUIT_SIZE
        ),
        "minimal_m_record_circuit_selector_rank_cap_formula": "10-m",
        "three_record_circuit_selector_rank_cap": (
            THREE_RECORD_CIRCUIT_SELECTOR_RANK_CAP
        ),
        "three_record_circuit_common_zero_floor": (
            THREE_RECORD_CIRCUIT_COMMON_ZERO_FLOOR
        ),
        "minimum_active_exchange": C,
        "generic_reciprocal_resultant_degree_cap": 2 * E,
        "base_field_size": FIELD_P,
        "coarse_maximum_exact_swap_component": (
            COARSE_MAX_EXACT_SWAP_COMPONENT
        ),
        "maximum_exact_swap_component": MAX_EXACT_SWAP_COMPONENT,
        "additional_charge": 0,
        "first_open_slack": R,
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "counted_object": (
                "PROJECTIVE RESIDUE LINES IN THE SCALAR-UNPAID "
                "RANK-THREE EQUALITY PACKET AT R=134943"
            ),
            "active_ledger": {
                "U_paid": parent.sweep.upper.plane.active.PAID,
                "B_remaining": B_REMAINING,
                "additional_charge": 0,
                "first_open_slack": R,
            },
            "theorem": {
                "complete_reciprocal_dimension_is_three": True,
                "bare_residue_line_cap_130_is_false": True,
                "line_congruence_module_rank": 2,
                "line_congruence_determinant_ideal": "Lambda_Sigma",
                "minimal_basis_row_degree_sum": SOURCE_SIZE,
                "cofactor_gcd_divides_source_locator": True,
                "cofactor_gcd_degree_at_most_c": True,
                "nontrivial_cofactor_gcd_would_be_source_partition": True,
                "cofactor_partition_is_projective_first_jet_locus": True,
                "source_unit_identity_forces_cofactor_gcd_one": True,
                "apparent_source_partition_branch_is_empty": True,
                "primitive_cofactor_columns_generate_complete_module": True,
                "primitive_hilbert_burch_presentation": True,
                "generic_reciprocal_resultant_is_nonzero": True,
                "generic_reciprocal_resultant_degree_below_field": True,
                "base_reciprocal_coprime_exact_degree_direction_exists": (
                    True
                ),
                "pair_exchange_dichotomy": True,
                "active_pair_exchange_at_least_c": True,
                "generic_exact_swap_exchange_equals_e": True,
                "coarse_exact_swap_component_at_most_14": True,
                "exact_swap_component_at_most_7": True,
                "projective_direction_source_map_deduplication": True,
                "source_map_image_size_at_most_carrier": True,
                "source_coordinate_line_collision_divisor_degree_at_most_c": (
                    True
                ),
                "off_collision_divisor_direction_map_is_injective": True,
                "equal_projective_source_maps_form_global_equivalence_classes": (
                    True
                ),
                "zero_collision_divisor_line_has_one_source_map_class": True,
                "nonzero_collision_divisor_line_has_pairwise_distinct_source_maps": (
                    True
                ),
                "cap_68_on_source_map_classes_is_sufficient": True,
                "equality_h_zero_removes_per_direction_gcd_budget": True,
                "occupied_source_product_pairs_are_coprime_exact_degree_e": (
                    True
                ),
                "nontrivial_exact_swap_component_forces_selector_rank_at_most_7": (
                    True
                ),
                "component_rank_defect_emits_nonzero_k0_grs_word": True,
                "every_component_kernel_word_has_source_scale_moving_block_mass": (
                    True
                ),
                "two_point_kernel_word_hits_each_moving_block_at_least_c": (
                    True
                ),
                "two_point_grs_quotient_is_below_source_rational_degree_threshold": (
                    True
                ),
                "component_grs_quotient_is_not_a_qualifying_source_rational_pair": (
                    True
                ),
                "actual_occupied_source_map_degree_exceeds_source_rational_threshold": (
                    True
                ),
                "component_rank_precursor_matches_no_current_active_owner": (
                    True
                ),
                "pair_exact_locus_is_a_proper_linear_subspace": True,
                "every_69_point_packet_has_simultaneously_nonexact_reciprocal_direction": (
                    True
                ),
                "simultaneous_pair_quotient_degree_at_most_exchange_minus_c": (
                    True
                ),
                "component_owner_adapter_is_not_required_for_69_point_reduction": (
                    True
                ),
                "every_distinct_graph_line_pair_forces_selector_rank_at_most_7_on_intersection": (
                    True
                ),
                "every_pair_has_nonzero_k0_secant_quotient_degree_at_most_exchange_minus_c": (
                    True
                ),
                "pair_k0_secant_exchange_weight_at_least_exchange_plus_c": (
                    True
                ),
                "equality_graph_lifts_factor_as_common_zero_locator_times_source_product": (
                    True
                ),
                "source_pair_quotient_equals_shortened_selector_secant_quotient": (
                    True
                ),
                "every_pair_source_plane_quotient_map_is_nonzero": True,
                "canonical_source_unit_parameter_avoids_all_source_and_pair_kernels": (
                    True
                ),
                "canonical_source_unit_parameter_avoids_all_vertex_carrier_zeros": (
                    True
                ),
                "canonical_pair_secant_is_nonzero_on_every_exchange_coordinate": (
                    True
                ),
                "oriented_source_selector_secants_satisfy_exact_cocycle": (
                    True
                ),
                "rooted_secant_star_span_dimension_at_most_eight": True,
                "every_nonbasis_star_edge_emits_canonical_fundamental_circuit": (
                    True
                ),
                "candidate_69_point_packet_emits_at_least_60_bounded_circuits": (
                    True
                ),
                "actual_record_circuit_has_between_3_and_10_records": True,
                "actual_record_circuit_carrier_partition_has_no_singleton_atom": (
                    True
                ),
                "minimal_m_record_circuit_has_m_minus_2_independent_selector_secants": (
                    True
                ),
                "minimal_m_record_circuit_selector_restriction_rank_at_most_10_minus_m": (
                    True
                ),
                "three_record_circuit_has_rank_at_most_7_on_at_least_423079_common_zeros": (
                    True
                ),
                "bounded_circuit_owner_partition_emission_status": "OPEN",
                "simultaneous_source_selector_coupling_status": (
                    "PROVED_EXACT_IDENTITY"
                ),
                "component_rank_precursor_payment_status": (
                    "OPEN_OWNER_EMISSION_REQUIRED_SAME_OBJECT_IDENTITY_PROVED"
                ),
                "unweighted_line_cap_68_is_sufficient": True,
                "unweighted_line_cap_69_is_not_sufficient_by_incidence_sum": (
                    True
                ),
                "rank16_cap130_interface_is_not_imported": True,
                "rank_three_primitive_line_can_have_four_large_exchange_components": (
                    True
                ),
                "same_owner_partition_payment_status": (
                    "NOT_NEEDED_SOURCE_VALID_BRANCH_EMPTY"
                ),
                "active_cofactor_primitivity_status": "PROVED",
                "primitive_69_point_exclusion_status": "OPEN",
                "primitive_large_exchange_incidence_status": "OPEN",
                "first_open_slack_after_packet": R,
            },
            "arithmetic": exact_arithmetic(),
            "regressions": {
                "one_root_pencils": [
                    one_root_pencil_control(17, 6, 10, 7),
                    one_root_pencil_control(19, 6, 12, 8),
                    one_root_pencil_control(23, 9, 14, 10),
                ],
                "primitive_rank_three_line": primitive_line_control(),
                "primitive_four_component_rank_three_line": (
                    four_component_line_control()
                ),
                "exact_swap_component_rank_precursor": (
                    component_rank_precursor_control()
                ),
                "nonprimitive_partition_cofactor": (
                    partition_cofactor_control()
                ),
            },
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_EQUALITY_WALL_RESIDUE_LINE_PARTITION_REDUCTION_"
                "ACTIVE_COFACTOR_PRIMITIVITY_GENERIC_RECIPROCAL_CAP7_"
                "EQUALITY_H0_NO_GCD_BUDGET_COMPONENT_RANK7_PRECURSOR_"
                "SOURCE_SCALE_MOVING_BLOCK_MASS_"
                "CURRENT_OWNER_TYPE_SEPARATION_"
                "SIMULTANEOUS_69_POINT_NONEXACT_GENERICIZATION_"
                "UNIVERSAL_PAIR_SELECTOR_SECANT_QUOTIENT_"
                "EXACT_SOURCE_SELECTOR_SECANT_IDENTIFICATION_"
                "BOUNDED_STAR_CIRCUIT_NO_SINGLETON_PARTITION_"
                "MINIMAL_CIRCUIT_COLLECTIVE_RANK_PRECURSOR_"
                "SOURCE_MAP_DEDUP_CAP68_SUFFICIENT_"
                "R134943_REMAINS_OPEN_ON_BOUNDED_CIRCUIT_OWNER_EMISSION"
            ),
        }
    )


def expected_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": True,
        "properties": {
            "architecture_id": {"const": ARCH},
            "partition_sha256": {"const": PARTITION_DIGEST},
            "payload_sha256": {"pattern": "^[0-9a-f]{64}$", "type": "string"},
        },
        "required": ["architecture_id", "partition_sha256", "payload_sha256"],
        "title": "KoalaBear equality-wall residue-line partition reduction",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_residue_line_partition_reduction_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED_REDUCTION_ROW_OPEN",
        "913{,}632",
        "\\operatorname{Fitt}_0(B[X]^2/\\mathcal M_U)",
        "g_U\\mid\\Lambda_\\Sigma",
        "projective first-jet coincidence locus",
        "\\boxed{g_U=1.}",
        "Hilbert--Burch presentation",
        "\\Delta\\ge s-d",
        "|Y_0\\setminus Y_z|\\ge c=67{,}472",
        "|\\mathcal C|",
        "=7.",
        "A coprime exact-degree reciprocal direction",
        "2e=269{,}888<p=2{,}130{,}706{,}433",
        "\\gcd(R_*,S_*)=1",
        "Projective-direction source-map deduplication",
        "|\\mathcal I_P|\\le |D\\setminus\\Sigma|",
        "Equality has no per-direction gcd budget",
        "\\sum_{P\\in\\mathscr P\\cap U}",
        "\\deg\\gcd(R_P,S_P)=0",
        "Exact-swap components force a selector rank defect",
        "\\operatorname{rank}G_{Z_{\\mathcal C}}\\le7",
        "103{,}967.",
        "\\deg H_{\\mathcal C}",
        "(m-1)e-c",
        "\\operatorname{wt}\\!\\left(w|_{\\mathcal M_{\\mathcal C}}\\right)",
        "=e+c=s=202{,}416",
        "\\operatorname{wt}\\!\\left(w|_{Z(C_i)}\\right)",
        "There is a tempting but invalid numerical shortcut here.",
        "E(s)+33{,}737",
        "component branch is not an unrecognized instance",
        "A 69-point packet can be made simultaneously nonexact",
        "\\binom{69}{2}=2{,}346",
        "T_{ij}(\\lambda_{\\mathscr Q})\\ne0",
        "\\deg T_{ij}(\\lambda_{\\mathscr Q})",
        "=\\Delta_{ij}-c",
        "Every pair also has an actual-selector secant word",
        "\\operatorname{rank}G_{Z_{ij}}\\le7",
        "\\deg H_{ij,w}\\le\\Delta_{ij}-c",
        "\\ge\\Delta_{ij}+c",
        "source maps are the same rational map",
        "N_{\\rm map}\\le67p+68",
        "\\#\\Gamma_{\\operatorname{rank}=3}\\le |V|N_{\\rm map}",
        "Lines with \\(H_U=0\\) are already deduplicated",
        "The source quotient is exactly the selector secant quotient",
        "P_i=\\Lambda_{Z_i}R_i",
        "\\Lambda_\\Sigma\\Lambda_{Z_{ij}}",
        "=k-1",
        "=130{,}941{,}546",
        "A_i^{\\rm src}(x)\\ne0",
        "T_{ij}^{\\rm src}\\ne0",
        "=2\\Delta_{ij}",
        "the same object",
        "Canonical bounded circuits and the no-singleton partition",
        "w_{ij}+w_{jk}+w_{ki}=0",
        "\\dim_F\\mathcal W_*\\le8",
        "69-1-8=60",
        "|C_j|\\le10",
        "V_{\\{i\\}}=\\varnothing",
        "Every minimal circuit forces a collective selector-rank defect",
        "\\operatorname{rank}(K_0|_{Z_C})\\le8-(m-2)=10-m",
        "=423{,}079",
        "Bounded-circuit owner/partition emission",
        "142{,}757{,}331{,}079",
        "292{,}758{,}501{,}275{,}736",
        "The adjacent cap \\(69\\) does not close",
        "Why the rank-16 cap-130 theorem does not transfer",
        "primitive 69-point exclusion",
        "# PROVED REDUCTION / ROW OPEN",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["theorem"]["same_owner_partition_payment_status"]
        == "NOT_NEEDED_SOURCE_VALID_BRANCH_EMPTY",
        "partition branch must remain empty",
    )
    need(
        cert["theorem"][
            "equal_projective_source_maps_form_global_equivalence_classes"
        ],
        "global source-map equivalence",
    )
    need(
        cert["theorem"][
            "zero_collision_divisor_line_has_one_source_map_class"
        ],
        "zero-divisor source-map-class collapse",
    )
    need(
        cert["theorem"][
            "nonzero_collision_divisor_line_has_pairwise_distinct_source_maps"
        ],
        "transversal line source-map separation",
    )
    need(
        cert["theorem"]["cap_68_on_source_map_classes_is_sufficient"],
        "source-map-class cap",
    )
    need(
        cert["theorem"]["active_cofactor_primitivity_status"] == "PROVED",
        "cofactor primitivity",
    )
    need(
        cert["theorem"]["primitive_69_point_exclusion_status"] == "OPEN",
        "primitive 69-point exclusion must remain open",
    )
    need(
        cert["theorem"]["primitive_large_exchange_incidence_status"] == "OPEN",
        "primitive incidence must remain open",
    )
    need(
        cert["theorem"]["component_rank_precursor_payment_status"]
        == "OPEN_OWNER_EMISSION_REQUIRED_SAME_OBJECT_IDENTITY_PROVED",
        "component rank precursor must remain unpaid",
    )
    need(
        cert["theorem"]["first_open_slack_after_packet"] == R,
        "first open unchanged",
    )
    need(
        cert["arithmetic"]["unrestricted_one_root_pencil_count"] > 130,
        "bare cap route cut",
    )
    need(
        cert["arithmetic"]["minimum_components_in_69_point_falsifier"]
        == 10,
        "ten-component falsifier threshold",
    )
    need(
        cert["arithmetic"]["extra_common_factor_degree"] == 0,
        "equality h=0",
    )
    need(
        cert["arithmetic"]["minimum_component_common_zero_size"]
        == 103_967,
        "large common-zero rank precursor",
    )
    need(
        cert["arithmetic"]["two_point_component_grs_quotient_degree_cap"]
        == C,
        "two-point component quotient cap",
    )
    need(
        cert["arithmetic"]["source_rational_degree_threshold"] == 101_207,
        "source-rational degree threshold",
    )
    need(
        cert["arithmetic"][
            "actual_source_map_degree_excess_over_rational_threshold"
        ]
        == 33_737,
        "actual source map remains above rational owner threshold",
    )
    need(
        cert["theorem"][
            "component_grs_quotient_is_not_a_qualifying_source_rational_pair"
        ],
        "GRS quotient/source-rational type separation",
    )
    need(
        cert["theorem"][
            "component_rank_precursor_matches_no_current_active_owner"
        ],
        "current-owner compatibility audit",
    )
    need(
        cert["arithmetic"]["minimum_component_k0_weight_on_moving_blocks"]
        == SOURCE_SIZE,
        "source-scale moving-block mass",
    )
    need(
        cert["arithmetic"]["two_point_per_moving_block_weight_floor"] == C,
        "two-point per-moving-block mass",
    )
    need(
        cert["arithmetic"]["simultaneous_genericization_pair_count"]
        == 2_346,
        "simultaneous 69-point pair count",
    )
    need(
        cert["theorem"][
            "every_69_point_packet_has_simultaneously_nonexact_reciprocal_direction"
        ],
        "simultaneous reciprocal genericization theorem",
    )
    need(
        cert["theorem"][
            "simultaneous_pair_quotient_degree_at_most_exchange_minus_c"
        ],
        "simultaneous pair quotient degree",
    )
    need(
        cert["arithmetic"]["minimum_pair_selector_secant_exchange_weight"]
        == E,
        "minimum pair-selector secant exchange weight",
    )
    need(
        cert["theorem"][
            "every_pair_has_nonzero_k0_secant_quotient_degree_at_most_exchange_minus_c"
        ],
        "pair K0 secant quotient theorem",
    )
    need(
        cert["theorem"][
            "equality_graph_lifts_factor_as_common_zero_locator_times_source_product"
        ],
        "graph-line/source-product factorization",
    )
    need(
        cert["theorem"][
            "source_pair_quotient_equals_shortened_selector_secant_quotient"
        ],
        "source quotient equals selector secant quotient",
    )
    need(
        cert["theorem"]["every_pair_source_plane_quotient_map_is_nonzero"],
        "pair source-plane quotient map",
    )
    need(
        cert["theorem"][
            "canonical_source_unit_parameter_avoids_all_source_and_pair_kernels"
        ],
        "canonical source-unit parameter",
    )
    need(
        cert["theorem"][
            "canonical_source_unit_parameter_avoids_all_vertex_carrier_zeros"
        ],
        "full-domain source-unit parameter",
    )
    need(
        cert["theorem"][
            "canonical_pair_secant_is_nonzero_on_every_exchange_coordinate"
        ],
        "full exchange-block secant support",
    )
    need(
        cert["theorem"][
            "oriented_source_selector_secants_satisfy_exact_cocycle"
        ],
        "exact secant cocycle",
    )
    need(
        cert["theorem"]["rooted_secant_star_span_dimension_at_most_eight"],
        "rooted secant-star dimension",
    )
    need(
        cert["theorem"][
            "candidate_69_point_packet_emits_at_least_60_bounded_circuits"
        ],
        "bounded circuit count",
    )
    need(
        cert["theorem"][
            "actual_record_circuit_carrier_partition_has_no_singleton_atom"
        ],
        "no-singleton carrier partition",
    )
    need(
        cert["theorem"][
            "minimal_m_record_circuit_has_m_minus_2_independent_selector_secants"
        ],
        "minimal-circuit independent selector secants",
    )
    need(
        cert["theorem"][
            "minimal_m_record_circuit_selector_restriction_rank_at_most_10_minus_m"
        ],
        "minimal-circuit selector restriction rank",
    )
    need(
        cert["theorem"][
            "three_record_circuit_has_rank_at_most_7_on_at_least_423079_common_zeros"
        ],
        "three-record circuit common-zero rank precursor",
    )
    need(
        cert["theorem"]["bounded_circuit_owner_partition_emission_status"]
        == "OPEN",
        "bounded-circuit owner emission must remain open",
    )
    need(
        cert["theorem"]["simultaneous_source_selector_coupling_status"]
        == "PROVED_EXACT_IDENTITY",
        "source-selector coupling status",
    )
    need(
        cert["arithmetic"]["source_and_pair_forbidden_parameter_cap"]
        == 204_762,
        "source-and-pair forbidden parameter cap",
    )
    need(
        cert["arithmetic"]["full_domain_source_unit_forbidden_parameter_cap"]
        == 130_941_546,
        "full-domain source-unit forbidden parameter cap",
    )
    need(
        cert["arithmetic"]["source_selector_secant_polynomial_degree_cap"]
        == parent.K - 1,
        "source-selector secant polynomial degree",
    )
    need(
        cert["arithmetic"][
            "minimum_fundamental_circuits_in_69_point_packet"
        ]
        == 60,
        "minimum bounded circuit count",
    )
    need(
        cert["arithmetic"]["maximum_fundamental_edge_circuit_size"] == 9,
        "edge-circuit size cap",
    )
    need(
        cert["arithmetic"]["maximum_actual_record_circuit_size"] == 10,
        "actual-record circuit size cap",
    )
    need(
        cert["arithmetic"][
            "minimal_m_record_circuit_selector_rank_cap_formula"
        ]
        == "10-m",
        "minimal-circuit rank formula",
    )
    need(
        cert["arithmetic"]["three_record_circuit_selector_rank_cap"] == 7,
        "three-record circuit selector rank",
    )
    need(
        cert["arithmetic"]["three_record_circuit_common_zero_floor"]
        == 423_079,
        "three-record circuit common-zero floor",
    )
    need(
        cert["regressions"]["primitive_rank_three_line"]["cofactor_gcd"]
        == [1],
        "primitive regression",
    )
    need(
        cert["regressions"]["primitive_four_component_rank_three_line"][
            "generic_exact_swap_component_sizes"
        ]
        == [1, 1, 1, 1],
        "four-component rank-three route cut",
    )
    need(
        cert["regressions"]["primitive_four_component_rank_three_line"][
            "source_coordinate_collision_divisor_carrier_roots"
        ]
        == 0,
        "transversal four-component control",
    )
    need(
        cert["regressions"]["exact_swap_component_rank_precursor"][
            "rows"
        ][0]["common_zero_size"]
        == 778_687,
        "two-point component precursor row",
    )
    need(
        cert["regressions"]["exact_swap_component_rank_precursor"][
            "rows"
        ][-1]["common_zero_size"]
        == 103_967,
        "seven-point component precursor row",
    )
    need(
        cert["regressions"]["nonprimitive_partition_cofactor"][
            "partition_degree"
        ]
        == 2,
        "partition regression",
    )
    check_sources()


def emit() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    cert = expected_certificate()
    schema = expected_schema()
    validate(cert, schema)
    mutations = [
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
        lambda d: d["active_ledger"].__setitem__("first_open_slack", R + 1),
        lambda d: d["theorem"].__setitem__(
            "complete_reciprocal_dimension_is_three", False
        ),
        lambda d: d["theorem"].__setitem__(
            "bare_residue_line_cap_130_is_false", False
        ),
        lambda d: d["theorem"].__setitem__(
            "cofactor_gcd_divides_source_locator", False
        ),
        lambda d: d["theorem"].__setitem__(
            "cofactor_partition_is_projective_first_jet_locus", False
        ),
        lambda d: d["theorem"].__setitem__(
            "source_unit_identity_forces_cofactor_gcd_one", False
        ),
        lambda d: d["theorem"].__setitem__(
            "active_pair_exchange_at_least_c", False
        ),
        lambda d: d["theorem"].__setitem__(
            "exact_swap_component_at_most_7", False
        ),
        lambda d: d["theorem"].__setitem__(
            "generic_reciprocal_resultant_is_nonzero", False
        ),
        lambda d: d["theorem"].__setitem__(
            "base_reciprocal_coprime_exact_degree_direction_exists", False
        ),
        lambda d: d["theorem"].__setitem__(
            "projective_direction_source_map_deduplication", False
        ),
        lambda d: d["theorem"].__setitem__(
            "source_coordinate_line_collision_divisor_degree_at_most_c",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "off_collision_divisor_direction_map_is_injective", False
        ),
        lambda d: d["theorem"].__setitem__(
            "equal_projective_source_maps_form_global_equivalence_classes",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "zero_collision_divisor_line_has_one_source_map_class", False
        ),
        lambda d: d["theorem"].__setitem__(
            "nonzero_collision_divisor_line_has_pairwise_distinct_source_maps",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "equality_h_zero_removes_per_direction_gcd_budget", False
        ),
        lambda d: d["theorem"].__setitem__(
            "nontrivial_exact_swap_component_forces_selector_rank_at_most_7",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "component_rank_precursor_payment_status", "PROVED"
        ),
        lambda d: d["theorem"].__setitem__(
            "component_grs_quotient_is_not_a_qualifying_source_rational_pair",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "every_component_kernel_word_has_source_scale_moving_block_mass",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "actual_occupied_source_map_degree_exceeds_source_rational_threshold",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "component_rank_precursor_matches_no_current_active_owner",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "pair_exact_locus_is_a_proper_linear_subspace",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "every_69_point_packet_has_simultaneously_nonexact_reciprocal_direction",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "component_owner_adapter_is_not_required_for_69_point_reduction",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "every_distinct_graph_line_pair_forces_selector_rank_at_most_7_on_intersection",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "every_pair_has_nonzero_k0_secant_quotient_degree_at_most_exchange_minus_c",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "equality_graph_lifts_factor_as_common_zero_locator_times_source_product",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "source_pair_quotient_equals_shortened_selector_secant_quotient",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "every_pair_source_plane_quotient_map_is_nonzero", False
        ),
        lambda d: d["theorem"].__setitem__(
            "canonical_source_unit_parameter_avoids_all_source_and_pair_kernels",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "canonical_source_unit_parameter_avoids_all_vertex_carrier_zeros",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "canonical_pair_secant_is_nonzero_on_every_exchange_coordinate",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "oriented_source_selector_secants_satisfy_exact_cocycle", False
        ),
        lambda d: d["theorem"].__setitem__(
            "rooted_secant_star_span_dimension_at_most_eight", False
        ),
        lambda d: d["theorem"].__setitem__(
            "candidate_69_point_packet_emits_at_least_60_bounded_circuits",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "actual_record_circuit_carrier_partition_has_no_singleton_atom",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "minimal_m_record_circuit_has_m_minus_2_independent_selector_secants",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "minimal_m_record_circuit_selector_restriction_rank_at_most_10_minus_m",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "three_record_circuit_has_rank_at_most_7_on_at_least_423079_common_zeros",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "bounded_circuit_owner_partition_emission_status", "PROVED"
        ),
        lambda d: d["theorem"].__setitem__(
            "simultaneous_source_selector_coupling_status", "OPEN"
        ),
        lambda d: d["theorem"].__setitem__(
            "unweighted_line_cap_68_is_sufficient", False
        ),
        lambda d: d["theorem"].__setitem__(
            "primitive_69_point_exclusion_status", "PROVED"
        ),
        lambda d: d["theorem"].__setitem__(
            "same_owner_partition_payment_status", "OPEN"
        ),
        lambda d: d["theorem"].__setitem__(
            "active_cofactor_primitivity_status", "OPEN"
        ),
        lambda d: d["theorem"].__setitem__(
            "primitive_large_exchange_incidence_status", "PROVED"
        ),
        lambda d: d["theorem"].__setitem__(
            "rank_three_primitive_line_can_have_four_large_exchange_components",
            False,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "maximum_exact_swap_component", 8
        ),
        lambda d: d["arithmetic"].__setitem__(
            "minimum_components_in_69_point_falsifier", 5
        ),
        lambda d: d["arithmetic"].__setitem__(
            "minimum_component_common_zero_size", 103_966
        ),
        lambda d: d["arithmetic"].__setitem__(
            "two_point_component_grs_quotient_degree_cap", C + 1
        ),
        lambda d: d["arithmetic"].__setitem__(
            "source_rational_degree_threshold",
            SOURCE_RATIONAL_DEGREE_THRESHOLD + 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "minimum_component_k0_weight_on_moving_blocks",
            MIN_COMPONENT_MOVING_BLOCK_WEIGHT - 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "simultaneous_genericization_pair_count",
            TARGET_PAIR_COUNT + 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "minimum_pair_selector_secant_exchange_weight",
            MIN_PAIR_SECANT_EXCHANGE_WEIGHT - 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "source_and_pair_forbidden_parameter_cap",
            SOURCE_AND_PAIR_FORBIDDEN_PARAMETER_CAP + 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "full_domain_source_unit_forbidden_parameter_cap",
            FULL_DOMAIN_SOURCE_UNIT_FORBIDDEN_PARAMETER_CAP + 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "source_selector_secant_polynomial_degree_cap",
            SOURCE_SELECTOR_SECANT_POLYNOMIAL_DEGREE_CAP + 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "minimum_fundamental_circuits_in_69_point_packet",
            MIN_FUNDAMENTAL_CIRCUITS_IN_69_POINT_PACKET - 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "maximum_fundamental_edge_circuit_size",
            MAX_FUNDAMENTAL_EDGE_CIRCUIT_SIZE + 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "three_record_circuit_common_zero_floor",
            THREE_RECORD_CIRCUIT_COMMON_ZERO_FLOOR - 1,
        ),
        lambda d: d["regressions"]["primitive_rank_three_line"].__setitem__(
            "cofactor_gcd", [1, 1]
        ),
        lambda d: d["regressions"][
            "primitive_four_component_rank_three_line"
        ].__setitem__("generic_exact_swap_component_sizes", [4]),
        lambda d: d["regressions"][
            "primitive_four_component_rank_three_line"
        ].__setitem__(
            "source_coordinate_collision_divisor_carrier_roots", 1
        ),
        lambda d: d["regressions"][
            "exact_swap_component_rank_precursor"
        ]["rows"][0].__setitem__("selector_restriction_rank_cap", 8),
        lambda d: d["upstream_certificates"][
            "equality_wall_locator_cylinder"
        ].__setitem__("payload_sha256", "0" * 64),
    ]
    passed = 0
    for mutate in mutations:
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            validate(bad, schema)
        except Failure:
            passed += 1
        else:
            raise Failure("tamper accepted")
    need(passed == len(mutations), "tamper count")
    print(f"tamper-selftest: PASS {passed}/{len(mutations)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.emit:
            emit()
        if args.check:
            cert = load(CERT_PATH)
            schema = load(SCHEMA_PATH)
            validate(cert, schema)
            print(f"architecture: {ARCH}")
            print(f"partition_sha256: {PARTITION_DIGEST}")
            print(f"equality_slack: {R}")
            print(
                "unrestricted_one_root_pencil_count: "
                f"{UNRESTRICTED_ONE_SWAP_COUNT}"
            )
            print(f"minimum_active_exchange: {C}")
            print(
                "maximum_exact_swap_component: "
                f"{MAX_EXACT_SWAP_COMPONENT}"
            )
            print(
                "minimum_component_common_zero_size: "
                f"{MIN_COMPONENT_COMMON_ZERO_SIZE}"
            )
            print(
                "two_point_component_grs_quotient_degree_cap: "
                f"{TWO_POINT_COMPONENT_QUOTIENT_DEGREE_CAP}"
            )
            print(
                "sufficient_unweighted_line_cap: "
                f"{UNWEIGHTED_LINE_CAP}"
            )
            print(
                "cap_68_reserve_margin: "
                f"{UNWEIGHTED_LINE_MARGIN}"
            )
            print(f"payload_sha256: {cert['payload_sha256']}")
            print("check: PASS")
        if args.tamper_selftest:
            tamper_selftest()
        if not (args.emit or args.check or args.tamper_selftest):
            parser.error("choose --emit, --check, or --tamper-selftest")
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
