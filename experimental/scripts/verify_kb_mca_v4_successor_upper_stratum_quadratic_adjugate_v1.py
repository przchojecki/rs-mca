#!/usr/bin/env python3
"""Verify the r=67,473 upper-stratum quadratic-adjugate reduction."""

from __future__ import annotations

import argparse
import copy
import functools
import itertools
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_first_gap_complement_locator_linearization_v1 as residue
import verify_kb_mca_v4_first_gap_source_interpolation_pencil_v1 as pencil
import verify_kb_mca_v4_next_slack_source_plane_closure_v1 as plane

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-successor-upper-stratum-quadratic-adjugate-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_successor_upper_stratum_quadratic_adjugate_v1.schema.json"
)

ARCH = plane.ARCH
PARTITION_DIGEST = plane.PARTITION_DIGEST
R_SUCCESSOR = pencil.T + 1
X_SUCCESSOR = 1
SOURCE_SIZE = pencil.T + R_SUCCESSOR + 1
REDUCED_DEGREE = pencil.T + 2
COMMON_GCD_DEGREE = pencil.K - 1 - REDUCED_DEGREE
CARRIER_SIZE = pencil.N - SOURCE_SIZE
COMPLEMENT_SIZE = pencil.J + X_SUCCESSOR
COMMON_ZERO_SIZE = CARRIER_SIZE - COMPLEMENT_SIZE
PROJECTIVE_POINT_CAP = plane.active.prev.BASE_PRIME + 1
DIRECT_BRANCH_CAP = PROJECTIVE_POINT_CAP * CARRIER_SIZE
RESERVE_MARGIN = plane.active.REMAINING - DIRECT_BRANCH_CAP

Failure = plane.Failure
need = plane.need
seal = plane.seal
dump = plane.dump
load = plane.load
file_digest = plane.file_digest

UPSTREAM_CERTIFICATES = {
    "next_slack_source_plane": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-next-slack-source-plane-closure-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'e4d51dcaea7ba2591ca314ecd73248fe0a79e07244176dab8b20c78d8d1e4064'
        ),
    },
    "post_next_slack_histogram": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-post-next-slack-full-histogram-replay-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '53a70a678e6669ac4d3083ec0dcd0a29d86aa127997cfdf2f8c9318eb844c902'
        ),
    },
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_next_slack_source_plane_closure_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_next_slack_full_histogram_replay_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_successor_upper_stratum_quadratic_adjugate_v1.md"
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
        payload = load(path)
        need(
            payload.get("payload_sha256") == contract["payload_sha256"],
            f"upstream payload mismatch: {key}",
        )
        bindings[key] = {**contract, "file_sha256": file_digest(path)}
    return bindings


def poly_add(left: list[int], right: list[int], prime: int) -> list[int]:
    size = max(len(left), len(right))
    return residue.trim(
        [
            (
                (left[index] if index < len(left) else 0)
                + (right[index] if index < len(right) else 0)
            )
            % prime
            for index in range(size)
        ]
    )


def poly_sub(left: list[int], right: list[int], prime: int) -> list[int]:
    size = max(len(left), len(right))
    return residue.trim(
        [
            (
                (left[index] if index < len(left) else 0)
                - (right[index] if index < len(right) else 0)
            )
            % prime
            for index in range(size)
        ]
    )


def determinant3(matrix: list[list[list[int]]], prime: int) -> list[int]:
    positive = [[(0, 0), (1, 1), (2, 2)],
                [(0, 1), (1, 2), (2, 0)],
                [(0, 2), (1, 0), (2, 1)]]
    negative = [[(0, 2), (1, 1), (2, 0)],
                [(0, 1), (1, 0), (2, 2)],
                [(0, 0), (1, 2), (2, 1)]]
    result = [0]
    for term in positive:
        product = [1]
        for row, column in term:
            product = residue.mul(product, matrix[row][column], prime)
        result = poly_add(result, product, prime)
    for term in negative:
        product = [1]
        for row, column in term:
            product = residue.mul(product, matrix[row][column], prime)
        result = poly_sub(result, product, prime)
    return residue.trim(result)


def choose_basis_with_constant(
    basis: list[list[int]], prime: int
) -> list[list[int]]:
    size = len(basis[0])
    result = [[1] + [0] * (size - 1)]
    need(
        residue.rank([*basis, result[0]], prime) == len(basis),
        "constant is outside source space",
    )
    for vector in basis:
        if residue.rank([*result, vector], prime) > len(result):
            result.append(vector)
        if len(result) == 3:
            break
    need(len(result) == 3, "three source directions")
    return result


def choose_full_basis_with_constant(
    basis: list[list[int]], prime: int
) -> list[list[int]]:
    size = len(basis[0])
    result = [[1] + [0] * (size - 1)]
    need(
        residue.rank([*basis, result[0]], prime) == len(basis),
        "constant is outside full source space",
    )
    for vector in basis:
        if residue.rank([*result, vector], prime) > len(result):
            result.append(vector)
        if len(result) == 4:
            break
    need(len(result) == 4, "four source directions")
    return result


def choose_reciprocal_unit(
    basis: list[list[int]], points: list[int], prime: int
) -> list[int]:
    for coefficients in itertools.product(range(prime), repeat=len(basis)):
        if not any(coefficients):
            continue
        vector = [
            sum(
                coefficients[index] * basis[index][coordinate]
                for index in range(len(basis))
            )
            % prime
            for coordinate in range(len(points))
        ]
        if all(plane.polynomial_values(vector, points, prime)):
            return vector
    raise Failure("missing reciprocal unit")


def pad(polynomial: list[int], size: int) -> list[int]:
    need(len(polynomial) <= size, "polynomial fits source algebra")
    return [*polynomial, *([0] * (size - len(polynomial)))]


def choose_source_plane_unit_outside(
    left: list[int],
    right: list[int],
    cyclic_plane: list[list[int]],
    points: list[int],
    prime: int,
) -> list[int]:
    """Choose a source-plane unit outside one prescribed cyclic plane."""

    size = len(points)
    left_padded = pad(left, size)
    right_padded = pad(right, size)
    need(
        residue.rank([left_padded, right_padded], prime) == 2,
        "translated source plane",
    )
    for left_scale in range(prime):
        for right_scale in range(prime):
            if left_scale == 0 and right_scale == 0:
                continue
            candidate = [
                (
                    left_scale * left_value
                    + right_scale * right_value
                )
                % prime
                for left_value, right_value in zip(
                    left_padded, right_padded
                )
            ]
            if residue.rank([*cyclic_plane, candidate], prime) != 3:
                continue
            if all(plane.polynomial_values(candidate, points, prime)):
                return candidate
    raise Failure("missing source-plane unit outside cyclic plane")


def product_matrix(
    source_basis: list[list[int]],
    reciprocal_basis: list[list[int]],
    points: list[int],
    inverse: list[list[int]],
    degree: int,
    prime: int,
) -> list[list[list[int]]]:
    result = []
    for source in source_basis:
        source_values = plane.polynomial_values(source, points, prime)
        row = []
        for reciprocal in reciprocal_basis:
            reciprocal_values = plane.polynomial_values(
                reciprocal, points, prime
            )
            values = [
                left * right % prime
                for left, right in zip(source_values, reciprocal_values)
            ]
            coefficients = residue.matrix_vector(inverse, values, prime)
            need(
                all(value == 0 for value in coefficients[degree + 1 :]),
                "product outside degree code",
            )
            row.append(residue.trim(coefficients[: degree + 1]))
        result.append(row)
    return result


def combine_vectors(
    vectors: list[list[int]], coefficients: list[int], prime: int
) -> list[int]:
    return [
        sum(
            coefficient * vector[index]
            for coefficient, vector in zip(coefficients, vectors)
        )
        % prime
        for index in range(len(vectors[0]))
    ]


def interpolated_product(
    left: list[int],
    right: list[int],
    points: list[int],
    inverse: list[list[int]],
    prime: int,
) -> list[int]:
    values = [
        a * b % prime
        for a, b in zip(
            plane.polynomial_values(left, points, prime),
            plane.polynomial_values(right, points, prime),
        )
    ]
    return residue.trim(residue.matrix_vector(inverse, values, prime))


def linear_syzygies(
    matrix: list[list[list[int]]], prime: int, *, left: bool
) -> list[list[int]]:
    equations = []
    for outer in range(3):
        polynomials = []
        for inner in range(3):
            polynomial = (
                matrix[inner][outer] if left else matrix[outer][inner]
            )
            polynomials.extend([polynomial, [0, *polynomial]])
        for degree in range(max(len(polynomial) for polynomial in polynomials)):
            equations.append(
                [
                    (
                        polynomial[degree]
                        if degree < len(polynomial)
                        else 0
                    )
                    for polynomial in polynomials
                ]
            )
    return residue.nullspace(equations, prime)


def matrix_and_reciprocal(
    left: list[int],
    right: list[int],
    prime: int,
    degree: int,
) -> tuple[
    list[list[int]],
    list[list[int]],
    list[list[int]],
    list[list[list[int]]],
]:
    source_size = 2 * degree - 2
    points, inverse = plane.evaluation_inverse(prime, source_size)
    left_values = plane.polynomial_values(left, points, prime)
    right_values = plane.polynomial_values(right, points, prime)
    source_space = plane.source_residue_space(
        left_values, right_values, points, inverse, degree, prime
    )
    need(len(source_space) == 4, "four-dimensional source space")
    q_basis = choose_basis_with_constant(source_space, prime)
    q_values = [
        plane.polynomial_values(vector, points, prime)
        for vector in q_basis
    ]
    reciprocal_matrix = plane.multiplication_constraint(
        q_values, points, inverse, degree, prime
    )
    reciprocal_space = residue.nullspace(reciprocal_matrix, prime)
    unit = choose_reciprocal_unit(reciprocal_space, points, prime)
    v_basis = [unit]
    for vector in reciprocal_space:
        if residue.rank([*v_basis, vector], prime) > len(v_basis):
            v_basis.append(vector)
        if len(v_basis) == 3:
            break
    need(len(v_basis) == 3, "three reciprocal directions")
    product = product_matrix(
        q_basis, v_basis, points, inverse, degree, prime
    )
    return source_space, q_basis, reciprocal_space, product


def transpose_linear_pencil(
    matrix: list[list[list[int]]],
) -> list[list[list[int]]]:
    return [
        [matrix[row][column] for row in range(len(matrix))]
        for column in range(len(matrix[0]))
    ]


def bounded_linear_pencil_kernel_dimension(
    matrix: list[list[list[int]]],
    vector_degree: int,
    prime: int,
) -> int:
    row_count = len(matrix)
    column_count = len(matrix[0])
    equations = []
    for row in range(row_count):
        for power in range(vector_degree + 2):
            equation = [0] * (column_count * (vector_degree + 1))
            for column in range(column_count):
                for entry_degree in range(2):
                    coefficient_degree = power - entry_degree
                    if 0 <= coefficient_degree <= vector_degree:
                        index = (
                            column * (vector_degree + 1)
                            + coefficient_degree
                        )
                        equation[index] = (
                            equation[index]
                            + matrix[row][column][entry_degree]
                        ) % prime
            equations.append(equation)
    return len(residue.nullspace(equations, prime))


def linear_pencil_kernel_profile(
    matrix: list[list[list[int]]], prime: int
) -> dict[str, list[int]]:
    transpose = transpose_linear_pencil(matrix)
    return {
        "right_bounded_kernel_dimensions": [
            bounded_linear_pencil_kernel_dimension(matrix, degree, prime)
            for degree in range(3)
        ],
        "left_bounded_kernel_dimensions": [
            bounded_linear_pencil_kernel_dimension(
                transpose, degree, prime
            )
            for degree in range(3)
        ],
    }


def full_degree_one_syzygy_profile(
    q_values: list[list[int]],
    source_pair_values: tuple[list[int], list[int]],
    points: list[int],
    inverse: list[list[int]],
    source_degree: int,
    prime: int,
) -> dict[str, Any]:
    equations = []
    for source_index, point in enumerate(points):
        equation = []
        for values in q_values:
            equation.extend(
                [
                    values[source_index],
                    point * values[source_index] % prime,
                ]
            )
        equations.append(equation)
    syzygies = residue.nullspace(equations, prime)
    slope_coordinates = [
        [row[2 * index + 1] for index in range(len(q_values))]
        for row in syzygies
    ]
    slope_values = [
        [
            sum(
                coefficient * q_values[index][source_index]
                for index, coefficient in enumerate(coordinates)
            )
            % prime
            for source_index in range(len(points))
        ]
        for coordinates in slope_coordinates
    ]
    common_zeros = [
        point
        for source_index, point in enumerate(points)
        if all(values[source_index] == 0 for values in slope_values)
    ]
    lowered_pairs = []
    for values in slope_values:
        pair = []
        for source_values in source_pair_values:
            product_values = [
                left * right % prime
                for left, right in zip(values, source_values)
            ]
            polynomial = residue.trim(
                residue.matrix_vector(inverse, product_values, prime)
            )
            need(
                len(polynomial) - 1 <= source_degree - 1,
                "lowered syzygy product degree",
            )
            pair.append(polynomial)
        lowered_pairs.append(pair)
    determinant_branch = "not_two_dimensional"
    determinant_quotient = []
    if len(lowered_pairs) == 2:
        determinant = poly_sub(
            residue.mul(
                lowered_pairs[0][0], lowered_pairs[1][1], prime
            ),
            residue.mul(
                lowered_pairs[0][1], lowered_pairs[1][0], prime
            ),
            prime,
        )
        quotient, remainder = residue.divmod_poly(
            determinant, residue.locator(points, prime), prime
        )
        need(remainder == [0], "lowered pencil source divisibility")
        determinant_quotient = residue.trim(quotient)
        if determinant_quotient == [0]:
            determinant_branch = "rank_one"
        else:
            need(
                len(determinant_quotient) == 1,
                "lowered pencil constant quotient",
            )
            determinant_branch = "saturated"
    return {
        "dimension": len(syzygies),
        "slope_coordinate_rank": residue.rank(
            slope_coordinates, prime
        ),
        "common_slope_source_zeros": common_zeros,
        "lowered_pair_determinant_branch": determinant_branch,
        "lowered_pair_determinant_quotient": determinant_quotient,
    }


@functools.lru_cache(maxsize=1)
def deterministic_scan() -> dict[str, Any]:
    prime = 13
    degree = 5
    source_size = 2 * degree - 2
    points, inverse = plane.evaluation_inverse(prime, source_size)
    rng = random.Random(55)
    histogram: Counter[int] = Counter()
    reduced_degree_histogram: Counter[int] = Counter()
    paired_product_degree_histogram: Counter[int] = Counter()
    bezout_quotient_histogram: Counter[int] = Counter()
    q_direction_unit_count = 0
    v_direction_unit_count = 0
    selected_locator_outside_cyclic_plane_count = 0
    source_plane_unit_outside_cyclic_plane_count = 0
    four_triple_signature_histogram: Counter[tuple[int, ...]] = Counter()
    all_four_rank_excess_syzygy_rank_histogram: Counter[int] = Counter()
    all_four_rank_excess_pencil_profile_histogram: Counter[
        tuple[int, ...]
    ] = Counter()
    all_four_rank_excess_full_syzygy_profile_histogram: Counter[
        tuple[int, ...]
    ] = Counter()
    all_four_rank_excess_count = 0
    first_all_four_rank_excess = None
    accepted = 0
    rank_excess_example = None

    for _ in range(10_000):
        left = [rng.randrange(prime) for _ in range(degree + 1)]
        right = [rng.randrange(prime) for _ in range(degree + 1)]
        if left[-1] == 0 and right[-1] == 0:
            continue
        if residue.gcd_poly(left, right, prime) != [1]:
            continue
        left_values = plane.polynomial_values(left, points, prime)
        right_values = plane.polynomial_values(right, points, prime)
        if any(
            a == 0 and b == 0
            for a, b in zip(left_values, right_values)
        ):
            continue
        source_space = plane.source_residue_space(
            left_values, right_values, points, inverse, degree, prime
        )
        need(len(source_space) == 4, "scan source dimension")
        q_full_basis = choose_full_basis_with_constant(source_space, prime)
        q_basis = q_full_basis[:3]
        q_values = [
            plane.polynomial_values(vector, points, prime)
            for vector in q_basis
        ]
        reciprocal_matrix = plane.multiplication_constraint(
            q_values, points, inverse, degree, prime
        )
        reciprocal_space = residue.nullspace(reciprocal_matrix, prime)
        reciprocal_dimension = len(reciprocal_space)
        need(reciprocal_dimension in [2, 3], "scan reciprocal dimension")
        histogram[reciprocal_dimension] += 1

        four_dimensions = []
        for omitted in range(4):
            triple_values = [
                plane.polynomial_values(vector, points, prime)
                for index, vector in enumerate(q_full_basis)
                if index != omitted
            ]
            four_dimensions.append(
                len(
                    residue.nullspace(
                        plane.multiplication_constraint(
                            triple_values,
                            points,
                            inverse,
                            degree,
                            prime,
                        ),
                        prime,
                    )
                )
            )
        signature = tuple(sorted(four_dimensions))
        four_triple_signature_histogram[signature] += 1
        if min(four_dimensions) >= 3:
            all_four_rank_excess_count += 1
            relation_rows = []
            for omitted in range(4):
                indices = [
                    index for index in range(4) if index != omitted
                ]
                triple_values = [
                    plane.polynomial_values(
                        q_full_basis[index], points, prime
                    )
                    for index in indices
                ]
                relations = locator_syzygies(
                    triple_values, points, prime
                )
                need(relations, "four-triple degree-one syzygy")
                row = [[0, 0] for _ in range(4)]
                for local, index in enumerate(indices):
                    row[index] = relations[0][
                        2 * local : 2 * local + 2
                    ]
                relation_rows.append(row)
            evaluated_ranks = []
            for point in range(prime):
                evaluated_ranks.append(
                    residue.rank(
                        [
                            [
                                (
                                    coefficient[0]
                                    + point * coefficient[1]
                                )
                                % prime
                                for coefficient in row
                            ]
                            for row in relation_rows
                        ],
                        prime,
                    )
                )
            generic_rank = max(evaluated_ranks)
            all_four_rank_excess_syzygy_rank_histogram[generic_rank] += 1
            pencil_profile = linear_pencil_kernel_profile(
                relation_rows, prime
            )
            pencil_signature = tuple(
                pencil_profile["right_bounded_kernel_dimensions"]
                + pencil_profile["left_bounded_kernel_dimensions"]
            )
            all_four_rank_excess_pencil_profile_histogram[
                pencil_signature
            ] += 1
            full_syzygy_profile = full_degree_one_syzygy_profile(
                [
                    plane.polynomial_values(vector, points, prime)
                    for vector in q_full_basis
                ],
                (left_values, right_values),
                points,
                inverse,
                degree,
                prime,
            )
            full_syzygy_signature = (
                full_syzygy_profile["dimension"],
                full_syzygy_profile["slope_coordinate_rank"],
                len(full_syzygy_profile["common_slope_source_zeros"]),
                (
                    1
                    if full_syzygy_profile[
                        "lowered_pair_determinant_branch"
                    ]
                    == "saturated"
                    else 0
                ),
            )
            all_four_rank_excess_full_syzygy_profile_histogram[
                full_syzygy_signature
            ] += 1
            if first_all_four_rank_excess is None:
                first_all_four_rank_excess = {
                    "left": left,
                    "right": right,
                    "reciprocal_dimensions": four_dimensions,
                    "syzygy_matrix_generic_rank": generic_rank,
                    "syzygy_matrix_rank_histogram": {
                        str(key): value
                        for key, value in sorted(
                            Counter(evaluated_ranks).items()
                        )
                    },
                    "syzygy_matrix": relation_rows,
                    "linear_pencil_kernel_profile": pencil_profile,
                    "full_degree_one_syzygy_profile": (
                        full_syzygy_profile
                    ),
                }
        accepted += 1
        if reciprocal_dimension != 3:
            continue

        unit = choose_reciprocal_unit(reciprocal_space, points, prime)
        v_basis = [unit]
        for vector in reciprocal_space:
            if residue.rank([*v_basis, vector], prime) > len(v_basis):
                v_basis.append(vector)
            if len(v_basis) == 3:
                break
        need(len(v_basis) == 3, "scan reciprocal basis")
        product = product_matrix(
            q_basis, v_basis, points, inverse, degree, prime
        )
        left_syzygy = linear_syzygies(product, prime, left=True)[0]
        right_syzygy = linear_syzygies(product, prime, left=False)[0]
        beta = left_syzygy[0::2]
        gamma = left_syzygy[1::2]
        alpha = right_syzygy[0::2]
        delta = right_syzygy[1::2]
        q_direction = combine_vectors(q_basis, gamma, prime)
        v_direction = combine_vectors(v_basis, delta, prime)
        q_x_direction = combine_vectors(
            q_basis,
            [(-coefficient) % prime for coefficient in beta],
            prime,
        )
        v_x_direction = combine_vectors(
            v_basis,
            [(-coefficient) % prime for coefficient in alpha],
            prime,
        )
        need(
            residue.rank([q_direction, q_x_direction], prime) == 2,
            "source cyclic plane",
        )
        need(
            residue.rank(
                [q_direction, q_x_direction, q_basis[0]], prime
            )
            == 3,
            "selected locator outside source cyclic plane",
        )
        selected_locator_outside_cyclic_plane_count += 1
        need(
            residue.rank([v_direction, v_x_direction], prime) == 2,
            "reciprocal cyclic plane",
        )
        source_plane_unit = choose_source_plane_unit_outside(
            left,
            right,
            [v_direction, v_x_direction],
            points,
            prime,
        )
        source_plane_unit_outside_cyclic_plane_count += 1
        if all(plane.polynomial_values(q_direction, points, prime)):
            q_direction_unit_count += 1
        if all(plane.polynomial_values(v_direction, points, prime)):
            v_direction_unit_count += 1

        q_left = interpolated_product(
            q_direction, left, points, inverse, prime
        )
        q_right = interpolated_product(
            q_direction, right, points, inverse, prime
        )
        common = residue.gcd_poly(q_left, q_right, prime)
        reduced_left, remainder_left = residue.divmod_poly(
            q_left, common, prime
        )
        reduced_right, remainder_right = residue.divmod_poly(
            q_right, common, prime
        )
        need(
            remainder_left == [0] and remainder_right == [0],
            "scan degree-drop gcd",
        )
        reduced_degree_histogram[
            max(len(reduced_left), len(reduced_right)) - 1
        ] += 1

        paired_product = interpolated_product(
            q_direction, v_direction, points, inverse, prime
        )
        paired_product_degree_histogram[
            -1 if paired_product == [0] else len(paired_product) - 1
        ] += 1

        bezout_a = interpolated_product(
            q_direction, source_plane_unit, points, inverse, prime
        )
        bezout_b = interpolated_product(
            q_basis[0], v_direction, points, inverse, prime
        )
        bezout_c = interpolated_product(
            q_basis[0], source_plane_unit, points, inverse, prime
        )
        need(
            paired_product == [0]
            or len(paired_product) - 1 <= degree - 2,
            "Bezout w degree",
        )
        need(len(bezout_a) - 1 <= degree - 1, "Bezout A degree")
        need(len(bezout_b) - 1 <= degree - 1, "Bezout B degree")
        need(len(bezout_c) - 1 <= degree, "Bezout C degree")
        source_locator = residue.locator(points, prime)
        bezout_determinant = poly_sub(
            residue.mul(paired_product, bezout_c, prime),
            residue.mul(bezout_a, bezout_b, prime),
            prime,
        )
        quotient, remainder = residue.divmod_poly(
            bezout_determinant, source_locator, prime
        )
        need(remainder == [0], "saturated Bezout divisibility")
        need(
            len(quotient) == 1 and quotient[0] != 0,
            "nonzero Bezout scalar",
        )
        bezout_quotient_histogram[quotient[0]] += 1

        if rank_excess_example is None:
            rank_excess_example = (left, right)

    need(accepted == 9_189, "scan accepted count")
    need(histogram == Counter({2: 8_449, 3: 740}), "scan histogram")
    need(
        four_triple_signature_histogram
        == Counter(
            {
                (2, 2, 2, 3): 7_215,
                (2, 2, 2, 4): 53,
                (2, 2, 3, 3): 1_763,
                (2, 2, 3, 4): 14,
                (2, 3, 3, 3): 138,
                (3, 3, 3, 3): 6,
            }
        ),
        "four-triple reciprocal signature histogram",
    )
    need(all_four_rank_excess_count == 6, "all-four rank excess count")
    need(
        all_four_rank_excess_syzygy_rank_histogram == Counter({2: 6}),
        "all-four rank-excess syzygy ranks",
    )
    need(
        all_four_rank_excess_pencil_profile_histogram
        == Counter({(0, 2, 4, 2, 4, 6): 6}),
        "all-four rank-excess pencil minimal-index profiles",
    )
    need(
        all_four_rank_excess_full_syzygy_profile_histogram
        == Counter({(2, 2, 0, 1): 6}),
        "all-four rank-excess full syzygy profiles",
    )
    need(
        first_all_four_rank_excess is not None
        and first_all_four_rank_excess["left"]
        == [8, 10, 11, 9, 9, 12]
        and first_all_four_rank_excess["right"]
        == [7, 2, 4, 11, 9, 10],
        "first all-four rank-excess example",
    )
    need(
        reduced_degree_histogram
        == Counter({4: 372, 3: 277, 2: 76, 1: 14, 0: 1}),
        "scan reduced-degree histogram",
    )
    need(
        paired_product_degree_histogram
        == Counter({3: 687, 2: 47, 1: 5, -1: 1}),
        "scan paired-product degree histogram",
    )
    need(q_direction_unit_count == 377, "scan q-direction units")
    need(v_direction_unit_count == 406, "scan v-direction units")
    need(
        selected_locator_outside_cyclic_plane_count == 740,
        "scan selected-locator cyclic-plane exclusion",
    )
    need(
        source_plane_unit_outside_cyclic_plane_count == 740,
        "scan source-plane unit construction",
    )
    need(
        sum(bezout_quotient_histogram.values()) == 740
        and set(bezout_quotient_histogram) == set(range(1, prime)),
        "scan saturated Bezout quotients",
    )
    need(
        rank_excess_example
        == ([5, 1, 10, 8, 3, 6], [7, 0, 7, 4, 7, 10]),
        "rank-excess example",
    )

    left, right = rank_excess_example
    _, q_basis, reciprocal_space, product = matrix_and_reciprocal(
        left, right, prime, degree
    )
    need(len(reciprocal_space) == 3, "example reciprocal dimension")
    determinant = determinant3(product, prime)
    need(determinant == [0], "example determinant")
    right_syzygies = linear_syzygies(product, prime, left=False)
    left_syzygies = linear_syzygies(product, prime, left=True)
    need(
        right_syzygies == [[3, 12, 0, 10, 1, 0]],
        "right linear syzygy",
    )
    need(
        left_syzygies == [[0, 3, 5, 12, 1, 0]],
        "left linear syzygy",
    )

    return {
        "field_prime": prime,
        "source_degree": degree,
        "source_size": source_size,
        "random_seed": 55,
        "trials": 10_000,
        "accepted_exact_coprime_pairs": accepted,
        "reciprocal_dimension_histogram": {
            str(key): histogram[key] for key in sorted(histogram)
        },
        "four_triple_reciprocal_dimension_signature_histogram": {
            ",".join(map(str, key)): four_triple_signature_histogram[key]
            for key in sorted(four_triple_signature_histogram)
        },
        "all_four_rank_excess_count": all_four_rank_excess_count,
        "all_four_rank_excess_syzygy_generic_rank_histogram": {
            str(key): all_four_rank_excess_syzygy_rank_histogram[key]
            for key in sorted(
                all_four_rank_excess_syzygy_rank_histogram
            )
        },
        "all_four_rank_excess_pencil_kernel_profile_histogram": {
            ",".join(map(str, key)): value
            for key, value in sorted(
                all_four_rank_excess_pencil_profile_histogram.items()
            )
        },
        "all_four_rank_excess_full_degree_one_syzygy_profile_histogram": {
            ",".join(map(str, key)): value
            for key, value in sorted(
                all_four_rank_excess_full_syzygy_profile_histogram.items()
            )
        },
        "first_all_four_rank_excess": first_all_four_rank_excess,
        "syzygy_direction_source_map_reduced_degree_histogram": {
            str(key): reduced_degree_histogram[key]
            for key in sorted(reduced_degree_histogram)
        },
        "paired_direction_product_degree_histogram": {
            str(key): paired_product_degree_histogram[key]
            for key in sorted(paired_product_degree_histogram)
        },
        "q_direction_unit_count": q_direction_unit_count,
        "v_direction_unit_count": v_direction_unit_count,
        "selected_locator_outside_cyclic_plane_count": (
            selected_locator_outside_cyclic_plane_count
        ),
        "source_plane_unit_outside_cyclic_plane_count": (
            source_plane_unit_outside_cyclic_plane_count
        ),
        "saturated_bezout_nonzero_scalar_count": sum(
            bezout_quotient_histogram.values()
        ),
        "saturated_bezout_quotient_histogram": {
            str(key): bezout_quotient_histogram[key]
            for key in sorted(bezout_quotient_histogram)
        },
        "direct_source_rational_implication_fails": (
            reduced_degree_histogram[degree - 1] > 0
        ),
        "paired_direction_product_can_vanish": (
            paired_product_degree_histogram[-1] > 0
        ),
        "rank_excess_example": {
            "left": left,
            "right": right,
            "source_basis": q_basis,
            "reciprocal_dimension": len(reciprocal_space),
            "right_linear_syzygy": right_syzygies[0],
            "left_linear_syzygy": left_syzygies[0],
            "determinant_zero": True,
        },
    }


def boundary_degree_control() -> dict[str, Any]:
    prime = 11
    degree = 4
    source_size = 2 * degree - 2
    left = [4, 9, 2, 0, 8]
    right = [4, 7, 4, 2, 2]
    _, _, reciprocal_space, product = matrix_and_reciprocal(
        left, right, prime, degree
    )
    determinant = determinant3(product, prime)
    points = list(range(source_size))
    source_locator = residue.locator(points, prime)
    locator_square = residue.mul(source_locator, source_locator, prime)
    quotient, remainder = residue.divmod_poly(
        determinant, locator_square, prime
    )
    need(residue.trim(remainder) == [0], "boundary double-root divisibility")
    need(residue.trim(quotient) != [0], "boundary determinant nonzero")
    need(2 * source_size == 3 * degree, "boundary degree equality")
    return {
        "field_prime": prime,
        "source_degree": degree,
        "source_size": source_size,
        "reciprocal_dimension": len(reciprocal_space),
        "twice_source_size": 2 * source_size,
        "determinant_degree_cap": 3 * degree,
        "degree_gate_is_equality": True,
        "determinant_is_nonzero_source_locator_square_multiple": True,
        "quotient": residue.trim(quotient),
    }


def locator_syzygies(
    q_values: list[list[int]], points: list[int], prime: int
) -> list[list[int]]:
    matrix = []
    for index, point in enumerate(points):
        row = []
        for values in q_values:
            row.extend([values[index], point * values[index] % prime])
        matrix.append(row)
    return residue.nullspace(matrix, prime)


def classify_locator_syzygy(
    *,
    zeros: list[tuple[int, ...]],
    relation: list[int],
    points: list[int],
    prime: int,
) -> dict[str, Any]:
    beta = relation[0::2]
    gamma = relation[1::2]
    zero_polynomials = [
        residue.locator(list(zero_set), prime) for zero_set in zeros
    ]
    numerator = [0]
    for index in range(3):
        others = [
            zero_polynomials[item]
            for item in range(3)
            if item != index
        ]
        coefficient = residue.trim([beta[index], gamma[index]])
        numerator = poly_add(
            numerator,
            residue.mul(
                coefficient,
                residue.mul(others[0], others[1], prime),
                prime,
            ),
            prime,
        )
    quotient, remainder = residue.divmod_poly(
        numerator, residue.locator(points, prime), prime
    )
    need(remainder == [0], "locator syzygy source divisibility")

    sets = [set(zero_set) for zero_set in zeros]
    common = set.intersection(*sets)
    pair_atoms = [
        (sets[0] & sets[1]) - sets[2],
        (sets[0] & sets[2]) - sets[1],
        (sets[1] & sets[2]) - sets[0],
    ]
    unique_atoms = [
        sets[index]
        - set.union(
            *(sets[item] for item in range(3) if item != index)
        )
        for index in range(3)
    ]
    exterior_spreads = [
        len((sets[(index + 1) % 3] | sets[(index + 2) % 3]) - sets[index])
        for index in range(3)
    ]
    need(
        len(set(exterior_spreads)) == 1,
        "equal locator sizes give equal exterior spread",
    )
    zero_coefficients = [
        index
        for index in range(3)
        if beta[index] == 0 and gamma[index] == 0
    ]
    numerator_zero = residue.trim(numerator) == [0]
    if numerator_zero and not zero_coefficients:
        need(
            max(map(len, unique_atoms)) <= 1,
            "private locator atom divides its linear coefficient",
        )
        branch = "three_block_pencil"
    elif numerator_zero:
        need(len(zero_coefficients) == 1, "one zero coefficient")
        other = [
            index for index in range(3) if index not in zero_coefficients
        ]
        need(
            len(sets[other[0]] ^ sets[other[1]]) // 2 <= 1,
            "zero coefficient gives one-root swap",
        )
        branch = "one_root_swap"
    else:
        need(
            exterior_spreads[0] + 1 >= len(points),
            "nonzero numerator needs full-source spread",
        )
        branch = "full_source_spread"
    return {
        "branch": branch,
        "zero_coefficient_count": len(zero_coefficients),
        "triple_common_size": len(common),
        "pair_atom_sizes": [len(atom) for atom in pair_atoms],
        "unique_atom_sizes": [len(atom) for atom in unique_atoms],
        "exterior_spread": exterior_spreads[0],
        "numerator_degree": len(residue.trim(numerator)) - 1,
        "quotient_degree": -1 if quotient == [0] else len(quotient) - 1,
    }


def fixed_reciprocal_image_divisors(
    *,
    zero_sets: list[tuple[int, ...]],
    records: dict[tuple[int, ...], dict[str, Any]],
    points: list[int],
    inverse: list[list[int]],
    degree: int,
    prime: int,
) -> dict[str, Any]:
    selected = [records[zero_set] for zero_set in zero_sets]
    reciprocal_space = residue.nullspace(
        plane.multiplication_constraint(
            [record["values"] for record in selected],
            points,
            inverse,
            degree,
            prime,
        ),
        prime,
    )
    fixed_divisors = []
    exterior_locators = []
    sets = [set(zero_set) for zero_set in zero_sets]
    for index, record in enumerate(selected):
        products = [
            interpolated_product(
                record["residue"], vector, points, inverse, prime
            )
            for vector in reciprocal_space
        ]
        common = products[0]
        for product in products[1:]:
            common = residue.gcd_poly(common, product, prime)
        exterior = set()
        for other_index, zero_set in enumerate(sets):
            if other_index != index:
                exterior |= zero_set
        exterior -= sets[index]
        exterior_locator = residue.locator(sorted(exterior), prime)
        need(
            residue.projective(common, prime)
            == residue.projective(exterior_locator, prime),
            "fixed reciprocal divisor is the exterior locator",
        )
        fixed_divisors.append(len(common) - 1)
        exterior_locators.append(len(exterior))
    return {
        "zero_sets": [list(zero_set) for zero_set in zero_sets],
        "reciprocal_dimension": len(reciprocal_space),
        "fixed_divisor_degrees": fixed_divisors,
        "exterior_locator_degrees": exterior_locators,
    }


def primitive_three_petal_control() -> dict[str, Any]:
    prime = 29
    degree = 5
    source_size = 2 * degree - 2
    j = 8
    points, inverse = plane.evaluation_inverse(prime, source_size)
    carrier = list(range(source_size, source_size + 2 * j - 2))
    carrier_set = set(carrier)
    zero_sets = [
        (9, 13, 16, 17, 19),
        (8, 10, 16, 19, 21),
        (8, 9, 10, 17, 18),
    ]
    source_left = [24, 10, 6, 10, 13, 12, 22, 18]
    source_right = [22, 9, 26, 28, 8, 13, 7, 20]
    source_values = [
        plane.polynomial_values(source, points, prime)
        for source in (source_left, source_right)
    ]
    need(
        all(a != 0 or b != 0 for a, b in zip(*source_values)),
        "primitive petal source pair is pointwise nonzero",
    )
    q_records = []
    for zero_set in zero_sets:
        complement = sorted(carrier_set - set(zero_set))
        q_values = plane.polynomial_values(
            residue.locator(complement, prime), points, prime
        )
        q_records.append(
            {
                "values": q_values,
                "residue": residue.matrix_vector(inverse, q_values, prime),
            }
        )
    q_basis = [record["residue"] for record in q_records]
    need(residue.rank(q_basis, prime) == 3, "independent petal locators")
    reciprocal_space = residue.nullspace(
        plane.multiplication_constraint(
            [record["values"] for record in q_records],
            points,
            inverse,
            degree,
            prime,
        ),
        prime,
    )
    need(len(reciprocal_space) == 3, "post-C5 petal reciprocal dimension")
    need(
        all(
            residue.rank([*reciprocal_space, source], prime) == 3
            for source in (source_left, source_right)
        ),
        "petal source coordinates lie in reciprocal space",
    )
    products = []
    for q in q_basis:
        pair = [
            interpolated_product(q, source, points, inverse, prime)
            for source in (source_left, source_right)
        ]
        need(max(map(len, pair)) - 1 == degree, "petal exact degree")
        need(residue.gcd_poly(pair[0], pair[1], prime) == [1], "petal coprime")
        products.append(pair)
    source_space = plane.source_residue_space(
        source_values[0],
        source_values[1],
        points,
        inverse,
        degree,
        prime,
    )
    need(len(source_space) == 4, "petal source residue dimension")
    relations = locator_syzygies(
        [record["values"] for record in q_records], points, prime
    )
    need(relations, "petal packet has a degree-one source syzygy")
    relation = relations[0]
    constant_coordinates = relation[0::2]
    slope_coordinates = relation[1::2]
    need(any(slope_coordinates), "petal syzygy has nonzero slope part")
    v_values = combine_vectors(
        [record["values"] for record in q_records],
        slope_coordinates,
        prime,
    )
    xv_values = [point * value % prime for point, value in zip(points, v_values)]
    relation_xv_values = combine_vectors(
        [record["values"] for record in q_records],
        [(-value) % prime for value in constant_coordinates],
        prime,
    )
    need(xv_values == relation_xv_values, "petal cyclic shift relation")
    v = residue.matrix_vector(inverse, v_values, prime)
    xv = residue.matrix_vector(inverse, xv_values, prime)
    need(residue.rank([v, xv], prime) == 2, "petal cyclic two-space")
    q_circle = next(
        q
        for q in q_basis
        if residue.rank([v, xv, q], prime) == 3
    )
    petal_basis = [q_circle, v, xv]
    need(residue.rank(petal_basis, prime) == 3, "petal quotient basis")
    v_pair = [
        interpolated_product(v, source, points, inverse, prime)
        for source in (source_left, source_right)
    ]
    xv_pair = [
        interpolated_product(xv, source, points, inverse, prime)
        for source in (source_left, source_right)
    ]
    q_circle_pair = [
        interpolated_product(q_circle, source, points, inverse, prime)
        for source in (source_left, source_right)
    ]
    need(
        all(len(product) - 1 <= degree - 1 for product in v_pair),
        "petal cyclic multiplier lowers source degree",
    )
    need(
        all(
            shifted == residue.trim([0, *base])
            for base, shifted in zip(v_pair, xv_pair)
        ),
        "petal cyclic product shift is exact",
    )

    def vector_coordinates(vector: list[int]) -> tuple[int, int, int]:
        for coordinates in itertools.product(range(prime), repeat=3):
            if combine_vectors(petal_basis, list(coordinates), prime) == vector:
                return coordinates
        raise Failure("missing petal quotient coordinates")

    def projective_pair(left: int, right: int) -> tuple[int, int] | None:
        if left == 0 and right == 0:
            return None
        if left:
            return (1, right * pow(left, -1, prime) % prime)
        return (0, 1)

    same_root_checks = 0
    actual_coordinates = []
    for q, pair in zip(q_basis, products):
        a, b, c = vector_coordinates(q)
        actual_coordinates.append([a, b, c])
        for root in carrier:
            actual_pair = projective_pair(
                residue.evaluate(pair[0], root, prime),
                residue.evaluate(pair[1], root, prime),
            )
            if actual_pair is None:
                continue
            if a == 0:
                expected_pair = projective_pair(
                    residue.evaluate(v_pair[0], root, prime),
                    residue.evaluate(v_pair[1], root, prime),
                )
            else:
                parameter = (
                    (b + c * root) * pow(a, -1, prime)
                ) % prime
                expected_pair = projective_pair(
                    (
                        residue.evaluate(q_circle_pair[0], root, prime)
                        + parameter * residue.evaluate(v_pair[0], root, prime)
                    )
                    % prime,
                    (
                        residue.evaluate(q_circle_pair[1], root, prime)
                        + parameter * residue.evaluate(v_pair[1], root, prime)
                    )
                    % prime,
                )
            need(
                actual_pair == expected_pair,
                "petal same-moving-root source-image containment",
            )
            same_root_checks += 1
    need(same_root_checks > 0, "petal source-image checks")

    classified = [
        classify_locator_syzygy(
            zeros=zero_sets,
            relation=relation,
            points=points,
            prime=prime,
        )
        for relation in relations
    ]
    petal = next(
        item for item in classified if item["branch"] == "three_block_pencil"
    )
    need(petal["pair_atom_sizes"] == [2, 2, 2], "sharp petal sizes")
    need(petal["unique_atom_sizes"] == [1, 1, 1], "sharp private atoms")
    need(petal["exterior_spread"] == 4, "sharp exterior spread")
    need(
        petal["exterior_spread"] < 2 * degree - 3,
        "petal control is outside full-spread branch",
    )
    return {
        "field_prime": prime,
        "degree": degree,
        "source_size": source_size,
        "j": j,
        "zero_locator_degree": j - 3,
        "zero_sets": [list(zero_set) for zero_set in zero_sets],
        "source_left": source_left,
        "source_right": source_right,
        "locator_rank": residue.rank(q_basis, prime),
        "reciprocal_dimension": len(reciprocal_space),
        "source_residue_dimension": len(source_space),
        "all_three_reduced_pairs_exact_degree_coprime": True,
        "classification": petal,
        "three_petal_floor_is_sharp": True,
        "cyclic_multiplier_source_degree_cap": degree - 1,
        "cyclic_space_dimension": 2,
        "occupied_space_quotient_dimension": 1,
        "source_image_family_size": prime + 1,
        "actual_locator_cyclic_coordinates": actual_coordinates,
        "same_moving_root_image_checks": same_root_checks,
        "same_moving_root_image_containment": True,
    }


@functools.lru_cache(maxsize=1)
def rank_four_actual_locator_c5_guardrail() -> dict[str, Any]:
    prime = 29
    degree = 5
    source_size = 2 * degree - 2
    j = 8
    points, inverse = plane.evaluation_inverse(prime, source_size)
    carrier = list(range(source_size, source_size + 2 * j - 2))
    carrier_set = set(carrier)
    zero_sets = [
        (8, 9, 10, 17, 18),
        (8, 10, 16, 19, 21),
        (9, 13, 16, 17, 19),
        (10, 12, 13, 16, 18),
    ]
    source_left = [23, 27, 27, 25, 2, 27, 1, 0]
    source_right = [22, 16, 20, 6, 2, 10, 0, 1]
    source_values = [
        plane.polynomial_values(source, points, prime)
        for source in (source_left, source_right)
    ]
    source_space = plane.source_residue_space(
        source_values[0],
        source_values[1],
        points,
        inverse,
        degree,
        prime,
    )
    need(len(source_space) == 4, "rank-four guardrail source dimension")

    records = []
    for zero_set in zero_sets:
        complement = sorted(carrier_set - set(zero_set))
        values = plane.polynomial_values(
            residue.locator(complement, prime), points, prime
        )
        q = residue.matrix_vector(inverse, values, prime)
        products = [
            interpolated_product(
                q, source, points, inverse, prime
            )
            for source in (source_left, source_right)
        ]
        need(
            max(map(len, products)) - 1 == degree,
            "rank-four guardrail exact degree",
        )
        need(
            residue.gcd_poly(products[0], products[1], prime) == [1],
            "rank-four guardrail coprime pair",
        )
        need(
            residue.rank([*source_space, q], prime) == len(source_space),
            "rank-four guardrail locator admission",
        )
        records.append({"zero": zero_set, "values": values, "q": q})

    need(
        residue.rank([record["q"] for record in records], prime) == 4,
        "rank-four guardrail locator rank",
    )
    triple_data = []
    dimensions = []
    relation_counts = []
    relation_branches: Counter[str] = Counter()
    for triple in itertools.combinations(records, 3):
        values = [record["values"] for record in triple]
        dimension = len(
            residue.nullspace(
                plane.multiplication_constraint(
                    values, points, inverse, degree, prime
                ),
                prime,
            )
        )
        relations = locator_syzygies(values, points, prime)
        classifications = [
            classify_locator_syzygy(
                zeros=[record["zero"] for record in triple],
                relation=relation,
                points=points,
                prime=prime,
            )
            for relation in relations
        ]
        dimensions.append(dimension)
        relation_counts.append(len(relations))
        relation_branches.update(
            result["branch"] for result in classifications
        )
        triple_data.append(
            {
                "zero_sets": [
                    list(record["zero"]) for record in triple
                ],
                "reciprocal_dimension": dimension,
                "relation_count": len(relations),
                "classifications": classifications,
            }
        )

    need(dimensions == [3, 2, 3, 2], "rank-four guardrail dimensions")
    need(relation_counts == [1, 0, 1, 0], "rank-four relation counts")
    need(
        relation_branches == Counter({"three_block_pencil": 2}),
        "rank-four relation branches",
    )
    return {
        "field_prime": prime,
        "degree": degree,
        "source_size": source_size,
        "j": j,
        "zero_locator_degree": j - 3,
        "source_left": source_left,
        "source_right": source_right,
        "source_residue_dimension": len(source_space),
        "actual_locator_count": len(records),
        "actual_locator_rank": 4,
        "all_actual_reduced_pairs_exact_degree_coprime": True,
        "triple_reciprocal_dimensions": dimensions,
        "triple_relation_counts": relation_counts,
        "triple_relation_branches": dict(relation_branches),
        "triples": triple_data,
        "strong_three_locator_closure_is_false": True,
        "rank_four_extension_is_deleted_by_c5": True,
    }


@functools.lru_cache(maxsize=1)
def actual_locator_triple_control() -> dict[str, Any]:
    prime = 19
    degree = 5
    source_size = 2 * degree - 2
    j = 5
    zero_size = j - 3
    points, inverse = plane.evaluation_inverse(prime, source_size)
    carrier = list(range(source_size, source_size + 2 * j - 2))
    carrier_set = set(carrier)
    records = []
    records_by_zero = {}
    for zero_set in itertools.combinations(carrier, zero_size):
        complement = sorted(carrier_set - set(zero_set))
        values = plane.polynomial_values(
            residue.locator(complement, prime), points, prime
        )
        record = {
            "zero": zero_set,
            "values": values,
            "residue": residue.matrix_vector(inverse, values, prime),
        }
        records.append(record)
        records_by_zero[zero_set] = record

    independent_triples = 0
    syzygy_triples = 0
    relation_nullities: Counter[int] = Counter()
    classified_relations: Counter[str] = Counter()
    branch_dimensions: Counter[tuple[str, int]] = Counter()
    for triple in itertools.combinations(records, 3):
        if residue.rank(
            [record["residue"] for record in triple], prime
        ) != 3:
            continue
        independent_triples += 1
        kernel = locator_syzygies(
            [record["values"] for record in triple], points, prime
        )
        relation_nullities[len(kernel)] += 1
        if not kernel:
            continue
        syzygy_triples += 1
        reciprocal_dimension = len(
            residue.nullspace(
                plane.multiplication_constraint(
                    [record["values"] for record in triple],
                    points,
                    inverse,
                    degree,
                    prime,
                ),
                prime,
            )
        )
        for relation in kernel:
            result = classify_locator_syzygy(
                zeros=[record["zero"] for record in triple],
                relation=relation,
                points=points,
                prime=prime,
            )
            classified_relations[result["branch"]] += 1
            branch_dimensions[
                (result["branch"], reciprocal_dimension)
            ] += 1

    need(independent_triples == 3_220, "independent locator triples")
    need(syzygy_triples == 2_800, "locator syzygy triples")
    need(
        relation_nullities == Counter({0: 420, 1: 1_680, 2: 1_120}),
        "locator relation nullities",
    )
    need(
        classified_relations
        == Counter({"one_root_swap": 3_080, "three_block_pencil": 840}),
        "locator relation branches",
    )

    examples = {
        "one_root_swap_dim3": fixed_reciprocal_image_divisors(
            zero_sets=[(8, 9), (8, 10), (11, 12)],
            records=records_by_zero,
            points=points,
            inverse=inverse,
            degree=degree,
            prime=prime,
        ),
        "one_root_swap_dim4": fixed_reciprocal_image_divisors(
            zero_sets=[(8, 9), (8, 10), (8, 11)],
            records=records_by_zero,
            points=points,
            inverse=inverse,
            degree=degree,
            prime=prime,
        ),
        "three_block_pencil_dim4": fixed_reciprocal_image_divisors(
            zero_sets=[(8, 10), (9, 11), (10, 11)],
            records=records_by_zero,
            points=points,
            inverse=inverse,
            degree=degree,
            prime=prime,
        ),
    }
    need(
        examples["one_root_swap_dim3"]["fixed_divisor_degrees"]
        == [3, 3, 3],
        "dimension-three fixed divisors",
    )
    need(
        examples["one_root_swap_dim4"]["fixed_divisor_degrees"]
        == [2, 2, 2],
        "dimension-four swap fixed divisors",
    )
    need(
        examples["three_block_pencil_dim4"]["fixed_divisor_degrees"]
        == [2, 2, 2],
        "dimension-four petal fixed divisors",
    )

    return {
        "field_prime": prime,
        "degree": degree,
        "source_size": source_size,
        "carrier_size": len(carrier),
        "zero_locator_degree": zero_size,
        "split_locator_count": len(records),
        "independent_triples": independent_triples,
        "syzygy_triples": syzygy_triples,
        "relation_nullities": {
            str(key): value for key, value in sorted(relation_nullities.items())
        },
        "classified_relations": dict(sorted(classified_relations.items())),
        "branch_reciprocal_dimensions": {
            f"{branch}:dim{dimension}": count
            for (branch, dimension), count in sorted(branch_dimensions.items())
        },
        "fixed_divisor_examples": examples,
        "primitive_three_petal_positive_control": (
            primitive_three_petal_control()
        ),
        "rank_four_actual_locator_c5_guardrail": (
            rank_four_actual_locator_c5_guardrail()
        ),
    }


def deployed_arithmetic() -> dict[str, Any]:
    source_rational_limit = (SOURCE_SIZE - 1) // 2
    degree_lower = source_rational_limit + 1
    degree_upper = SOURCE_SIZE + X_SUCCESSOR - pencil.T - 1
    forced_common_roots = pencil.A_AGREEMENT - X_SUCCESSOR - SOURCE_SIZE
    nullity_floor = 2 * (REDUCED_DEGREE + 1) - SOURCE_SIZE
    dual_degree = SOURCE_SIZE - REDUCED_DEGREE - 2

    need(R_SUCCESSOR == 67_473, "successor slack")
    need(SOURCE_SIZE == 134_946, "source size")
    need(degree_lower == 67_473, "degree lower")
    need(degree_upper == REDUCED_DEGREE == 67_474, "upper stratum")
    need(SOURCE_SIZE == 2 * REDUCED_DEGREE - 2, "quadratic threshold")
    need(forced_common_roots == COMMON_GCD_DEGREE, "complete split gcd")
    need(COMMON_ZERO_SIZE == COMMON_GCD_DEGREE, "common zero size")
    need(nullity_floor == 4, "source dimension floor")
    need(dual_degree == REDUCED_DEGREE - 4, "dual degree")
    need(2 * SOURCE_SIZE > 3 * REDUCED_DEGREE, "double-root gate")
    need(DIRECT_BRANCH_CAP == 4_180_884_949_033_404, "direct cap")
    need(RESERVE_MARGIN == 266_599_328_011_542_476, "reserve margin")
    need(REDUCED_DEGREE - 2 == 67_472, "paired-product degree cap")
    need(REDUCED_DEGREE - 1 == 67_473, "balanced source block size")
    need(2 * REDUCED_DEGREE - 3 == 134_945, "exterior spread floor")
    need(REDUCED_DEGREE - 3 == 67_471, "pair-petal floor")

    return {
        "base_field_order": plane.active.prev.BASE_PRIME,
        "n": pencil.N,
        "k": pencil.K,
        "agreement": pencil.A_AGREEMENT,
        "j": pencil.J,
        "t": pencil.T,
        "r": R_SUCCESSOR,
        "x": X_SUCCESSOR,
        "source_size": SOURCE_SIZE,
        "source_rational_limit": source_rational_limit,
        "reduced_degree_lower": degree_lower,
        "reduced_degree_upper": degree_upper,
        "treated_reduced_degree": REDUCED_DEGREE,
        "full_gcd_degree": COMMON_GCD_DEGREE,
        "carrier_size": CARRIER_SIZE,
        "common_zero_size": COMMON_ZERO_SIZE,
        "complement_size": COMPLEMENT_SIZE,
        "source_kernel_dimension": nullity_floor,
        "dual_rs_polynomial_degree": dual_degree,
        "double_root_degree": 2 * SOURCE_SIZE,
        "determinant_degree_cap": 3 * REDUCED_DEGREE,
        "minor_quotient_degree": 2,
        "paired_direction_product_degree_cap": REDUCED_DEGREE - 2,
        "balanced_source_partition_block_size": REDUCED_DEGREE - 1,
        "distinct_actual_locator_exchange_floor": REDUCED_DEGREE - 2,
        "full_source_exterior_spread_floor": 2 * REDUCED_DEGREE - 3,
        "three_petal_pair_atom_floor": REDUCED_DEGREE - 3,
        "three_petal_private_atom_cap": 1,
        "direct_branch_cap": DIRECT_BRANCH_CAP,
        "current_remaining_reserve": plane.active.REMAINING,
        "reserve_margin": RESERVE_MARGIN,
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "active_ledger": {
                "U_paid": plane.active.PAID,
                "B_remaining": plane.active.REMAINING,
                "additional_charge": 0,
            },
            "theorem": {
                "successor_slack": R_SUCCESSOR,
                "treated_degree_stratum": REDUCED_DEGREE,
                "source_constraints_independent": True,
                "source_residue_dimension": 4,
                "base_span_at_most_two_directly_paid": True,
                "triple_reciprocal_dimension_two_owned_by_c5": True,
                "rank_excess_determinant_zero": True,
                "rank_excess_adjugate_quotient_degree": 2,
                "zero_adjugate_contradicts_coprime_exact_degree": True,
                "surviving_adjugate_is_nonzero_rank_one": True,
                "surviving_left_syzygy_degree": 1,
                "surviving_right_syzygy_degree": 1,
                "left_syzygy_direction_row_degree_drop": 1,
                "right_syzygy_direction_column_degree_drop": 1,
                "paired_syzygy_direction_degree_drop": 2,
                "zero_paired_product_forces_balanced_source_partition": True,
                "nonzero_paired_product_source_zero_union_cap": (
                    REDUCED_DEGREE - 2
                ),
                "selected_locator_outside_source_cyclic_plane": True,
                "source_plane_unit_outside_reciprocal_cyclic_plane": True,
                "saturated_bezout_normal_form": True,
                "saturated_bezout_degree_profile": {
                    "w": REDUCED_DEGREE - 2,
                    "A": REDUCED_DEGREE - 1,
                    "B": REDUCED_DEGREE - 1,
                    "C": REDUCED_DEGREE,
                },
                "saturated_bezout_scalar_is_nonzero": True,
                "canonical_three_part_source_stratification": True,
                "occupied_actual_locator_span_at_most_two_directly_paid": True,
                "three_independent_actual_locators_enable_source_syzygy": True,
                "span_three_lowered_multiplier_dimension_floor": 1,
                "span_three_cyclic_space_dimension": 2,
                "span_three_occupied_quotient_dimension": 1,
                "span_three_source_image_family_size": PROJECTIVE_POINT_CAP,
                "span_three_source_image_cap": DIRECT_BRANCH_CAP,
                "span_three_same_locator_containment": True,
                "occupied_span_three_directly_paid": True,
                "distinct_actual_locator_exchange_floor": (
                    REDUCED_DEGREE - 2
                ),
                "actual_locator_venn_factor_identity": True,
                "zero_coefficient_one_root_swap_excluded": True,
                "nonzero_venn_numerator_exterior_spread_floor": (
                    2 * REDUCED_DEGREE - 3
                ),
                "zero_venn_numerator_private_atom_cap": 1,
                "zero_venn_numerator_pair_atom_floor": REDUCED_DEGREE - 3,
                "four_independent_post_c5_actual_locators_give_four_rank_excess_triples": True,
                "four_syzygy_matrix_is_zero_diagonal_linear": True,
                "four_syzygy_matrix_generic_rank_one_excluded": True,
                "four_syzygy_matrix_generic_rank_three_excluded_by_cubic_cyclic_contradiction": True,
                "four_syzygy_matrix_generic_rank": 2,
                "degree_one_syzygy_space_identifies_with_lowered_multiplier_space": True,
                "lowered_multiplier_dimension_floor": 2,
                "lowered_multiplier_dimension_at_least_three_emits_degree_drop_two": True,
                "lowered_multiplier_dimension_two_gives_constant_left_factorization": True,
                "lowered_pencil_determinant_is_zero_or_source_locator_multiple": True,
                "common_source_zero_forces_zero_lowered_pencil_determinant": True,
                "shift_is_injective_on_lowered_multiplier_space": True,
                "transverse_two_dimensional_first_prolongation_directly_paid": True,
                "transverse_first_prolongation_cap": DIRECT_BRANCH_CAP,
                "nontransverse_span_four_emits_three_step_multiplier": True,
                "three_step_multiplier_source_product_degree_cap": (
                    REDUCED_DEGREE - 2
                ),
                "three_step_cyclic_space_dimension": 3,
                "three_step_quotient_dimension": 1,
                "three_step_source_image_family_size": PROJECTIVE_POINT_CAP,
                "three_step_source_image_cap": DIRECT_BRANCH_CAP,
                "three_step_same_locator_containment": True,
                "occupied_span_four_directly_paid": True,
                "remaining_actual_locator_packets": [],
                "rank_two_collective_syzygy_payment_open": False,
                "lowered_pencil_slope_synchronization_open": False,
                "three_step_multiplier_payment_open": False,
                "span_three_spread_petal_payment_open": False,
                "direct_source_rational_implication_is_false": True,
                "paired_direction_product_can_be_zero": True,
                "upper_stratum_paid": True,
                "lower_degree_stratum_treated": False,
                "row_closed": False,
            },
            "deployed_arithmetic": deployed_arithmetic(),
            "finite_controls": {
                "deterministic_scan": deterministic_scan(),
                "strict_degree_boundary": boundary_degree_control(),
                "actual_locator_triples": actual_locator_triple_control(),
            },
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_SUCCESSOR_UPPER_STRATUM_QUADRATIC_ADJUGATE_"
                "SATURATED_BEZOUT_AND_ACTUAL_LOCATOR_PARTITION_"
                "TRICHOTOMY_COMPLETE_SPAN_THREE_AND_SPAN_FOUR_"
                "SOURCE_IMAGE_PAYMENT_UPPER_STRATUM_PAID_"
                "LOWER_STRATUM_SEPARATE"
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
        "title": "KoalaBear successor upper-stratum quadratic adjugate",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_successor_upper_stratum_quadratic_adjugate_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED COMPLETE UPPER-STRATUM PAYMENT",
        "\\dim_F\\mathcal K_\\Sigma(e)=4",
        "Low base span is paid",
        "Quadratic adjugate theorem",
        "\\deg L_{ij}\\le2",
        "\\mathcal P(X)a(X)=0",
        "Canonical two-step degree drop",
        "\\deg\\operatorname{rep}(q_\\star v_\\star)\\le e-2",
        "Exact source-zero dichotomy",
        "A_\\star B_\\star=c\\Lambda_\\Sigma",
        "Z_\\Sigma(q_\\star)\\cup Z_\\Sigma(v_\\star)",
        "Selected-locator saturated Bezout normal form",
        "wC-AB=c\\Lambda_\\Sigma",
        "\\Sigma_\\times",
        "Actual-locator span and split-locator trichotomy",
        "d_{ik}\\ge e-2",
        "\\Lambda_\\Sigma\\mid\\Phi",
        "\\Delta\\ge2e-3",
        "m_0H_{12}+m_1H_{02}+m_2H_{01}=0",
        "|H_{01}|,|H_{02}|,|H_{12}|\\ge e-3",
        "The span-three cyclic quotient pays both packets",
        "\\mathcal V_U=\\{v\\in U_\\Sigma:Xv\\in U_\\Sigma\\}",
        "C_v=\\langle v,Xv\\rangle_B",
        "t=b+cx\\in B",
        "selected slopes in the occupied span-three branch",
        "Four-locator collective-rank closure",
        "\\operatorname{rank}_{F(X)}\\mathcal L=2",
        "punctured cubic cyclic space",
        "rank-two collective linear-syzygy packet",
        "The rank-two rows come from the lowered source pencil",
        "degree-one syzygies on }W_\\Sigma",
        "\\mathcal L(X)=U\\,\\mathcal R(X)",
        "source-multiplier packet (4.62)",
        "saturated first prolongation",
        "Transverse first prolongations are directly paid",
        "W_\\Sigma=V_\\Sigma\\oplus XV_\\Sigma",
        "P_q=P_a+XP_b",
        "4{,}180{,}884{,}949{,}033{,}404",
        "v,\\ Xv,\\ X^2v\\in W_\\Sigma",
        "The three-step packet also has only",
        "C_v=\\langle v,Xv,X^2v\\rangle_B",
        "q=q_\\circ+p(X)v",
        "t=p(x)\\in B",
        "every occupied actual-locator span-four branch is paid",
        "Upper-stratum conclusion",
        "degree 4: 372",
        "zero product:   1",
        "4{,}180{,}884{,}949{,}033{,}404",
        "740",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["theorem"]["paired_syzygy_direction_degree_drop"] == 2,
        "paired degree drop",
    )
    need(
        cert["theorem"]["direct_source_rational_implication_is_false"]
        is True,
        "source-rational route cut",
    )
    need(
        cert["theorem"][
            "zero_paired_product_forces_balanced_source_partition"
        ]
        is True,
        "balanced source partition",
    )
    need(
        cert["theorem"]["selected_locator_outside_source_cyclic_plane"]
        is True,
        "selected-locator cyclic-plane exclusion",
    )
    need(
        cert["theorem"]["saturated_bezout_normal_form"] is True,
        "saturated Bezout normal form",
    )
    need(
        cert["theorem"]["saturated_bezout_scalar_is_nonzero"] is True,
        "nonzero saturated Bezout scalar",
    )
    need(
        cert["theorem"][
            "occupied_actual_locator_span_at_most_two_directly_paid"
        ]
        is True,
        "occupied locator line payment",
    )
    need(
        cert["theorem"]["span_three_lowered_multiplier_dimension_floor"] == 1,
        "span-three lowered-multiplier floor",
    )
    need(
        cert["theorem"]["span_three_cyclic_space_dimension"] == 2,
        "span-three cyclic-space dimension",
    )
    need(
        cert["theorem"]["span_three_occupied_quotient_dimension"] == 1,
        "span-three quotient dimension",
    )
    need(
        cert["theorem"]["span_three_source_image_family_size"]
        == PROJECTIVE_POINT_CAP,
        "span-three source-image family size",
    )
    need(
        cert["theorem"]["span_three_source_image_cap"] == DIRECT_BRANCH_CAP,
        "span-three source-image cap",
    )
    need(
        cert["theorem"]["span_three_same_locator_containment"] is True,
        "span-three same-locator containment",
    )
    need(
        cert["theorem"]["occupied_span_three_directly_paid"] is True,
        "complete span-three payment",
    )
    need(
        cert["theorem"]["distinct_actual_locator_exchange_floor"]
        == REDUCED_DEGREE - 2,
        "actual locator exchange floor",
    )
    need(
        cert["theorem"]["zero_coefficient_one_root_swap_excluded"] is True,
        "one-root swap exclusion",
    )
    need(
        cert["theorem"][
            "four_syzygy_matrix_generic_rank_three_excluded_by_cubic_cyclic_contradiction"
        ]
        is True,
        "four-syzygy rank-three exclusion",
    )
    need(
        cert["theorem"]["four_syzygy_matrix_generic_rank"] == 2,
        "four-syzygy generic rank",
    )
    need(
        cert["theorem"][
            "degree_one_syzygy_space_identifies_with_lowered_multiplier_space"
        ]
        is True,
        "degree-one syzygy/lowered-multiplier identification",
    )
    need(
        cert["theorem"]["lowered_multiplier_dimension_floor"] == 2,
        "lowered multiplier dimension floor",
    )
    need(
        cert["theorem"][
            "lowered_multiplier_dimension_two_gives_constant_left_factorization"
        ]
        is True,
        "lowered-pencil constant-left factorization",
    )
    need(
        cert["theorem"][
            "lowered_pencil_determinant_is_zero_or_source_locator_multiple"
        ]
        is True,
        "lowered-pencil determinant dichotomy",
    )
    need(
        cert["theorem"][
            "transverse_two_dimensional_first_prolongation_directly_paid"
        ]
        is True,
        "transverse first-prolongation payment",
    )
    need(
        cert["theorem"]["transverse_first_prolongation_cap"]
        == DIRECT_BRANCH_CAP,
        "transverse first-prolongation cap",
    )
    need(
        cert["theorem"][
            "nontransverse_span_four_emits_three_step_multiplier"
        ]
        is True,
        "three-step multiplier emission",
    )
    need(
        cert["theorem"]["three_step_cyclic_space_dimension"] == 3,
        "three-step cyclic-space dimension",
    )
    need(
        cert["theorem"]["three_step_quotient_dimension"] == 1,
        "three-step quotient dimension",
    )
    need(
        cert["theorem"]["three_step_source_image_family_size"]
        == PROJECTIVE_POINT_CAP,
        "three-step source-image family size",
    )
    need(
        cert["theorem"]["three_step_source_image_cap"] == DIRECT_BRANCH_CAP,
        "three-step source-image cap",
    )
    need(
        cert["theorem"]["three_step_same_locator_containment"] is True,
        "three-step same-locator containment",
    )
    need(
        cert["theorem"]["occupied_span_four_directly_paid"] is True,
        "complete span-four payment",
    )
    need(
        cert["theorem"]["remaining_actual_locator_packets"] == [],
        "remaining actual-locator packets",
    )
    need(
        cert["theorem"]["rank_two_collective_syzygy_payment_open"] is False,
        "rank-two payment status",
    )
    need(
        cert["theorem"]["lowered_pencil_slope_synchronization_open"]
        is False,
        "lowered-pencil synchronization status",
    )
    need(
        cert["theorem"]["three_step_multiplier_payment_open"] is False,
        "three-step multiplier status",
    )
    need(
        cert["theorem"]["span_three_spread_petal_payment_open"] is False,
        "span-three spread/petal status",
    )
    need(cert["theorem"]["upper_stratum_paid"] is True, "upper payment")
    need(
        cert["theorem"]["lower_degree_stratum_treated"] is False,
        "lower stratum status",
    )
    need(cert["theorem"]["row_closed"] is False, "row status")
    check_sources()


def emit() -> None:
    CERT.mkdir(parents=True, exist_ok=True)
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    cert = expected_certificate()
    schema = expected_schema()
    validate(cert, schema)
    mutations = [
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
        lambda d: d["theorem"].__setitem__("source_residue_dimension", 3),
        lambda d: d["theorem"].__setitem__(
            "triple_reciprocal_dimension_two_owned_by_c5", False
        ),
        lambda d: d["theorem"].__setitem__(
            "zero_adjugate_contradicts_coprime_exact_degree", False
        ),
        lambda d: d["theorem"].__setitem__(
            "paired_syzygy_direction_degree_drop", 1
        ),
        lambda d: d["theorem"].__setitem__(
            "direct_source_rational_implication_is_false", False
        ),
        lambda d: d["theorem"].__setitem__(
            "zero_paired_product_forces_balanced_source_partition", False
        ),
        lambda d: d["theorem"].__setitem__(
            "nonzero_paired_product_source_zero_union_cap",
            REDUCED_DEGREE - 1,
        ),
        lambda d: d["theorem"].__setitem__(
            "selected_locator_outside_source_cyclic_plane", False
        ),
        lambda d: d["theorem"].__setitem__(
            "saturated_bezout_normal_form", False
        ),
        lambda d: d["theorem"].__setitem__(
            "saturated_bezout_scalar_is_nonzero", False
        ),
        lambda d: d["theorem"].__setitem__(
            "occupied_actual_locator_span_at_most_two_directly_paid", False
        ),
        lambda d: d["theorem"].__setitem__(
            "span_three_lowered_multiplier_dimension_floor", 0
        ),
        lambda d: d["theorem"].__setitem__(
            "span_three_cyclic_space_dimension", 1
        ),
        lambda d: d["theorem"].__setitem__(
            "span_three_occupied_quotient_dimension", 2
        ),
        lambda d: d["theorem"].__setitem__(
            "span_three_source_image_family_size", PROJECTIVE_POINT_CAP + 1
        ),
        lambda d: d["theorem"].__setitem__(
            "span_three_source_image_cap", DIRECT_BRANCH_CAP + 1
        ),
        lambda d: d["theorem"].__setitem__(
            "span_three_same_locator_containment", False
        ),
        lambda d: d["theorem"].__setitem__(
            "occupied_span_three_directly_paid", False
        ),
        lambda d: d["theorem"].__setitem__(
            "distinct_actual_locator_exchange_floor",
            REDUCED_DEGREE - 3,
        ),
        lambda d: d["theorem"].__setitem__(
            "zero_coefficient_one_root_swap_excluded", False
        ),
        lambda d: d["theorem"].__setitem__(
            "four_syzygy_matrix_generic_rank", 3
        ),
        lambda d: d["theorem"].__setitem__(
            "four_syzygy_matrix_generic_rank_three_excluded_by_cubic_cyclic_contradiction",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "degree_one_syzygy_space_identifies_with_lowered_multiplier_space",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "lowered_multiplier_dimension_floor", 1
        ),
        lambda d: d["theorem"].__setitem__(
            "lowered_multiplier_dimension_two_gives_constant_left_factorization",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "lowered_pencil_determinant_is_zero_or_source_locator_multiple",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "shift_is_injective_on_lowered_multiplier_space", False
        ),
        lambda d: d["theorem"].__setitem__(
            "transverse_two_dimensional_first_prolongation_directly_paid",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "transverse_first_prolongation_cap", DIRECT_BRANCH_CAP + 1
        ),
        lambda d: d["theorem"].__setitem__(
            "nontransverse_span_four_emits_three_step_multiplier", False
        ),
        lambda d: d["theorem"].__setitem__(
            "three_step_multiplier_source_product_degree_cap",
            REDUCED_DEGREE - 1,
        ),
        lambda d: d["theorem"].__setitem__(
            "three_step_cyclic_space_dimension", 2
        ),
        lambda d: d["theorem"].__setitem__(
            "three_step_quotient_dimension", 2
        ),
        lambda d: d["theorem"].__setitem__(
            "three_step_source_image_family_size", PROJECTIVE_POINT_CAP + 1
        ),
        lambda d: d["theorem"].__setitem__(
            "three_step_source_image_cap", DIRECT_BRANCH_CAP + 1
        ),
        lambda d: d["theorem"].__setitem__(
            "three_step_same_locator_containment", False
        ),
        lambda d: d["theorem"].__setitem__(
            "occupied_span_four_directly_paid", False
        ),
        lambda d: d["theorem"].__setitem__(
            "rank_two_collective_syzygy_payment_open", True
        ),
        lambda d: d["theorem"].__setitem__(
            "lowered_pencil_slope_synchronization_open", True
        ),
        lambda d: d["theorem"].__setitem__(
            "three_step_multiplier_payment_open", True
        ),
        lambda d: d["theorem"].__setitem__(
            "span_three_spread_petal_payment_open", True
        ),
        lambda d: d["theorem"].__setitem__(
            "remaining_actual_locator_packets",
            ["full_source_exterior_spread"],
        ),
        lambda d: d["finite_controls"]["actual_locator_triples"][
            "classified_relations"
        ].__setitem__("three_block_pencil", 839),
        lambda d: d["finite_controls"]["actual_locator_triples"][
            "primitive_three_petal_positive_control"
        ].__setitem__("same_moving_root_image_containment", False),
        lambda d: d["finite_controls"]["actual_locator_triples"][
            "rank_four_actual_locator_c5_guardrail"
        ].__setitem__("rank_four_extension_is_deleted_by_c5", False),
        lambda d: d["finite_controls"]["deterministic_scan"].__setitem__(
            "all_four_rank_excess_count", 5
        ),
        lambda d: d["finite_controls"]["deterministic_scan"][
            "all_four_rank_excess_pencil_kernel_profile_histogram"
        ].__setitem__("0,2,4,2,4,6", 5),
        lambda d: d["finite_controls"]["deterministic_scan"][
            "all_four_rank_excess_full_degree_one_syzygy_profile_histogram"
        ].__setitem__("2,2,0,1", 5),
        lambda d: d["theorem"].__setitem__("upper_stratum_paid", False),
        lambda d: d["theorem"].__setitem__(
            "lower_degree_stratum_treated", True
        ),
        lambda d: d["deployed_arithmetic"].__setitem__(
            "minor_quotient_degree", 1
        ),
        lambda d: d["finite_controls"]["deterministic_scan"][
            "reciprocal_dimension_histogram"
        ].__setitem__("3", 739),
        lambda d: d["finite_controls"]["deterministic_scan"][
            "syzygy_direction_source_map_reduced_degree_histogram"
        ].__setitem__("4", 371),
        lambda d: d["finite_controls"]["deterministic_scan"][
            "paired_direction_product_degree_histogram"
        ].__setitem__("-1", 0),
        lambda d: d["finite_controls"]["deterministic_scan"].__setitem__(
            "saturated_bezout_nonzero_scalar_count", 739
        ),
        lambda d: d["upstream_certificates"]["next_slack_source_plane"].__setitem__(
            "payload_sha256", "0" * 64
        ),
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
            print(f"successor_slack: {R_SUCCESSOR}")
            print(f"treated_degree: {REDUCED_DEGREE}")
            print(f"source_dimension: {cert['theorem']['source_residue_dimension']}")
            print(f"direct_branch_cap: {DIRECT_BRANCH_CAP}")
            print(
                "reciprocal_histogram: "
                f"{cert['finite_controls']['deterministic_scan']['reciprocal_dimension_histogram']}"
            )
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
