#!/usr/bin/env python3
"""Verify the first-gap projective-residue C5/rank dichotomy."""

from __future__ import annotations

import argparse
import copy
import itertools
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1 as active
import verify_kb_mca_v4_first_gap_complement_locator_linearization_v1 as residue
import verify_kb_mca_v4_first_gap_source_interpolation_pencil_v1 as pencil

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-first-gap-projective-residue-c5-rank-dichotomy-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_first_gap_projective_residue_c5_rank_dichotomy_v1.schema.json"
)

ARCH = active.ARCH
PARTITION_DIGEST = active.partition()["partition_sha256"]

Failure = active.Failure
need = active.need
seal = active.seal
dump = active.dump
load = active.load
file_digest = active.file_digest

SOURCE_PATHS = [
    (
        "experimental/data/certificates/"
        "kb-mca-v4-c5-twist-frobenius9208-adapter-v1/manifest.json"
    ),
    (
        "experimental/data/certificates/"
        "kb-mca-v4-first-gap-source-interpolation-pencil-v1/certificate.json"
    ),
    (
        "experimental/data/certificates/"
        "kb-mca-v4-first-gap-complement-locator-linearization-v1/"
        "certificate.json"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_tangent_deep_source_rational_c5_adapter_v1.md"
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
        "kb_mca_v4_first_gap_projective_residue_c5_rank_dichotomy_v1.md"
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


# F_9 = F_3[a]/(a^2+1), encoded as x0 + 3*x1.
def f9_pair(value: int) -> tuple[int, int]:
    return value % 3, value // 3


def f9_code(left: int, right: int) -> int:
    return left % 3 + 3 * (right % 3)


def f9_add(left: int, right: int) -> int:
    a0, a1 = f9_pair(left)
    b0, b1 = f9_pair(right)
    return f9_code(a0 + b0, a1 + b1)


def f9_mul(left: int, right: int) -> int:
    a0, a1 = f9_pair(left)
    b0, b1 = f9_pair(right)
    # a^2 = -1 = 2 in F_3.
    return f9_code(a0 * b0 + 2 * a1 * b1, a0 * b1 + a1 * b0)


def f9_pow(value: int, exponent: int) -> int:
    result = 1
    base = value
    while exponent:
        if exponent & 1:
            result = f9_mul(result, base)
        base = f9_mul(base, base)
        exponent //= 2
    return result


def f9_inv(value: int) -> int:
    need(value != 0, "F9 inverse of zero")
    result = f9_pow(value, 7)
    need(f9_mul(value, result) == 1, "F9 inverse")
    return result


def f9_projective(vector: Iterable[int]) -> tuple[int, ...]:
    values = tuple(vector)
    pivot = next((value for value in values if value != 0), None)
    need(pivot is not None, "zero F9 projective vector")
    inverse = f9_inv(pivot)
    return tuple(f9_mul(inverse, value) for value in values)


def f9_dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    total = 0
    for a, b in zip(left, right):
        total = f9_add(total, f9_mul(a, b))
    return total


def projective_rational_point_control() -> dict[str, Any]:
    points = {
        f9_projective(vector)
        for vector in itertools.product(range(9), repeat=3)
        if any(vector)
    }
    functionals = points
    base_points = {
        point
        for point in points
        if all(f9_pair(coordinate)[1] == 0 for coordinate in point)
    }
    need(len(points) == 91, "P2(F9) point count")
    need(len(base_points) == 13, "P2(F3) point count")

    histogram: Counter[int] = Counter()
    for functional in functionals:
        line = {point for point in points if f9_dot(functional, point) == 0}
        need(len(line) == 10, "F9 projective line size")
        histogram[len(line & base_points)] += 1

    need(histogram == Counter({1: 78, 4: 13}), "Baer line histogram")
    return {
        "extension": "F9_over_F3",
        "ambient_projective_points": len(points),
        "base_projective_points": len(base_points),
        "projective_lines_checked": len(functionals),
        "base_rational_intersection_histogram": {
            str(key): histogram[key] for key in sorted(histogram)
        },
        "allowed_two_dimensional_intersection_sizes": [0, 1, 4],
        "two_base_points_force_base_line": True,
    }


def evaluation_data(
    p: int, degree: int
) -> tuple[list[int], list[list[int]], list[list[int]]]:
    source_size = 2 * degree
    sigma = list(range(source_size))
    vandermonde = [
        [pow(point, exponent, p) for exponent in range(source_size)]
        for point in sigma
    ]
    inverse = residue.inverse_matrix(vandermonde, p)
    high_rows = inverse[degree + 1 :]
    need(len(high_rows) == degree - 1, "source parity rows")
    return sigma, inverse, high_rows


def polynomial_values(
    polynomial: list[int], points: Iterable[int], p: int
) -> list[int]:
    return [residue.evaluate(polynomial, point, p) for point in points]


def multiplication_constraint(
    multipliers: list[list[int]],
    sigma: list[int],
    inverse: list[list[int]],
    high_rows: list[list[int]],
    p: int,
) -> list[list[int]]:
    source_size = len(sigma)
    columns = []
    for exponent in range(source_size):
        monomial = [pow(point, exponent, p) for point in sigma]
        output = []
        for multiplier in multipliers:
            product = [
                multiplier[index] * monomial[index] % p
                for index in range(source_size)
            ]
            coefficients = residue.matrix_vector(inverse, product, p)
            output.extend(coefficients[len(high_rows) + 2 :])
        columns.append(output)
    # The degree is source_size/2 and len(high_rows)=degree-1, so
    # degree+1 = len(high_rows)+2.
    return [
        [columns[column][row] for column in range(source_size)]
        for row in range(len(multipliers) * len(high_rows))
    ]


def reciprocal_rank_examples() -> dict[str, Any]:
    p = 17
    degree = 3
    sigma, inverse, high_rows = evaluation_data(p, degree)
    q0 = [1] * len(sigma)

    normal_poly = residue.mul([-7 % p, 1], [-8 % p, 1], p)
    normal_q1 = polynomial_values(normal_poly, sigma, p)
    need(all(normal_q1), "normal multiplier unit")
    normal_matrix = multiplication_constraint(
        [q0, normal_q1], sigma, inverse, high_rows, p
    )
    normal_rank = residue.rank(normal_matrix, p)
    normal_nullity = len(sigma) - normal_rank
    need(normal_nullity == 2, "normal reciprocal nullity")

    excess_poly = [-7 % p, 1]
    excess_q1 = polynomial_values(excess_poly, sigma, p)
    need(all(excess_q1), "excess multiplier unit")
    excess_matrix = multiplication_constraint(
        [q0, excess_q1], sigma, inverse, high_rows, p
    )
    excess_rank = residue.rank(excess_matrix, p)
    excess_nullity = len(sigma) - excess_rank
    need(excess_nullity == 3, "rank-excess reciprocal nullity")

    return {
        "field_prime": p,
        "source_degree": degree,
        "source_size": 2 * degree,
        "generic_expected_rank": 2 * degree - 2,
        "normal": {
            "second_multiplier": normal_poly,
            "matrix_rank": normal_rank,
            "kernel_dimension": normal_nullity,
        },
        "rank_excess": {
            "second_multiplier": excess_poly,
            "matrix_rank": excess_rank,
            "kernel_dimension": excess_nullity,
            "rank_deficiency": excess_nullity - 2,
        },
    }


def poly_subtract(left: list[int], right: list[int], p: int) -> list[int]:
    size = max(len(left), len(right))
    result = [
        (
            (left[index] if index < len(left) else 0)
            - (right[index] if index < len(right) else 0)
        )
        % p
        for index in range(size)
    ]
    return residue.trim(result)


def poly_linear_combination(
    polynomials: list[list[int]], coefficients: list[int], p: int
) -> list[int]:
    size = max(len(polynomial) for polynomial in polynomials)
    result = [0] * size
    for scalar, polynomial in zip(coefficients, polynomials):
        for index, value in enumerate(polynomial):
            result[index] = (result[index] + scalar * value) % p
    return residue.trim(result)


def exact_quotient(
    numerator: list[int], denominator: list[int], p: int
) -> list[int]:
    quotient, remainder = residue.divmod_poly(numerator, denominator, p)
    need(residue.trim(remainder) == [0], "nonexact polynomial quotient")
    return residue.trim(quotient)


def reciprocal_matrix_and_graph(
    q0: list[int],
    q1: list[int],
    sigma: list[int],
    inverse: list[list[int]],
    high_rows: list[list[int]],
    p: int,
) -> tuple[list[list[int]], list[tuple[list[int], list[int]]]]:
    matrix = multiplication_constraint(
        [q0, q1], sigma, inverse, high_rows, p
    )
    graph = []
    for vector in residue.nullspace(matrix, p):
        values = [
            sum(
                coefficient * pow(point, exponent, p)
                for exponent, coefficient in enumerate(vector)
            )
            % p
            for point in sigma
        ]
        pair = []
        for multiplier in (q0, q1):
            product = [
                multiplier[index] * values[index] % p
                for index in range(len(sigma))
            ]
            coefficients = residue.matrix_vector(inverse, product, p)
            need(
                all(value == 0 for value in coefficients[len(high_rows) + 2 :]),
                "graph high coefficient",
            )
            pair.append(residue.trim(coefficients))
        graph.append((pair[0], pair[1]))
    return matrix, graph


def rational_graph_normal_form(
    graph: list[tuple[list[int], list[int]]],
    degree: int,
    p: int,
) -> dict[str, Any]:
    dimension = len(graph)
    need(dimension >= 3, "normal form requires rank excess")
    leading_matrix = [
        [
            pair[coordinate][degree]
            if degree < len(pair[coordinate])
            else 0
            for pair in graph
        ]
        for coordinate in range(2)
    ]
    low_combinations = residue.nullspace(leading_matrix, p)
    need(low_combinations, "missing low-degree graph pair")
    combination = low_combinations[0]
    low_left = poly_linear_combination(
        [pair[0] for pair in graph], combination, p
    )
    low_right = poly_linear_combination(
        [pair[1] for pair in graph], combination, p
    )
    need(
        max(len(low_left), len(low_right)) - 1 <= degree - 1,
        "low graph degree",
    )
    common = residue.gcd_poly(low_left, low_right, p)
    left = exact_quotient(low_left, common, p)
    right = exact_quotient(low_right, common, p)
    rational_degree = max(len(left), len(right)) - 1
    need(
        rational_degree == degree - dimension + 1,
        "reciprocal degree/dimension identity",
    )
    need(
        residue.gcd_poly(left, right, p) == [1],
        "rational pair coprimality",
    )

    multipliers = []
    for graph_left, graph_right in graph:
        determinant = poly_subtract(
            residue.mul(left, graph_right, p),
            residue.mul(right, graph_left, p),
            p,
        )
        need(determinant == [0], "graph rational identity")
        multiplier = exact_quotient(graph_left, left, p)
        need(
            residue.mul(right, multiplier, p)
            == residue.trim(graph_right),
            "graph common multiplier",
        )
        need(len(multiplier) - 1 <= degree - rational_degree, "multiplier degree")
        multipliers.append(multiplier)

    need(
        residue.rank(
            [
                [
                    multiplier[index] if index < len(multiplier) else 0
                    for multiplier in multipliers
                ]
                for index in range(degree - rational_degree + 1)
            ],
            p,
        )
        == dimension,
        "full multiplier space",
    )
    return {
        "kernel_dimension": dimension,
        "rational_degree": rational_degree,
        "left": left,
        "right": right,
    }


def locator_rank_excess_row(
    *, p: int, degree: int, j: int
) -> dict[str, Any]:
    sigma, inverse, high_rows = evaluation_data(p, degree)
    carrier = list(range(2 * degree, 2 * (degree + j)))
    complements = []
    for points in itertools.combinations(carrier, j + 1):
        polynomial = residue.locator(points, p)
        values = polynomial_values(polynomial, sigma, p)
        need(all(values), "locator/source disjointness")
        coefficients = tuple(residue.matrix_vector(inverse, values, p))
        complements.append(
            {
                "points": points,
                "polynomial": polynomial,
                "values": values,
                "projective": residue.projective(coefficients, p),
            }
        )

    same_projective = 0
    same_projective_min_exchange = None
    rank_histogram: Counter[int] = Counter()
    excess_branches: Counter[str] = Counter()
    rational_degrees: Counter[int] = Counter()
    minimum_large_exchange = None
    maximum_low_swap_exchange = 0

    for left_index, left_record in enumerate(complements):
        left_set = set(left_record["points"])
        for right_record in complements[left_index + 1 :]:
            right_set = set(right_record["points"])
            exchange = len(left_set - right_set)
            if left_record["projective"] == right_record["projective"]:
                same_projective += 1
                if same_projective_min_exchange is None:
                    same_projective_min_exchange = exchange
                else:
                    same_projective_min_exchange = min(
                        same_projective_min_exchange, exchange
                    )
                need(exchange >= 2 * degree, "projective exchange floor")
                continue

            matrix, graph = reciprocal_matrix_and_graph(
                left_record["values"],
                right_record["values"],
                sigma,
                inverse,
                high_rows,
                p,
            )
            dimension = len(graph)
            need(
                dimension == len(sigma) - residue.rank(matrix, p),
                "reciprocal graph dimension",
            )
            need(dimension >= 2, "reciprocal dimension floor")
            rank_histogram[dimension] += 1
            if dimension == 2:
                continue

            normal = rational_graph_normal_form(graph, degree, p)
            rational_degree = normal["rational_degree"]
            rational_degrees[rational_degree] += 1

            common = left_set & right_set
            left_only = residue.locator(sorted(left_set - common), p)
            right_only = residue.locator(sorted(right_set - common), p)
            # graph orientation is (q_left*v,q_right*v), hence
            # left_polynomial*q_right = right_polynomial*q_left.
            difference = poly_subtract(
                residue.mul(normal["left"], right_only, p),
                residue.mul(normal["right"], left_only, p),
                p,
            )
            if difference == [0]:
                excess_branches["LOW_DEGREE_EXACT_SWAP"] += 1
                maximum_low_swap_exchange = max(
                    maximum_low_swap_exchange, exchange
                )
                need(exchange <= rational_degree, "low-swap degree cap")
                exact_quotient(normal["left"], left_only, p)
                exact_quotient(normal["right"], right_only, p)
            else:
                excess_branches["LARGE_EXCHANGE"] += 1
                need(
                    all(
                        residue.evaluate(difference, point, p) == 0
                        for point in sigma
                    ),
                    "large-exchange source divisibility",
                )
                need(
                    exchange + rational_degree >= 2 * degree,
                    "rational large-exchange floor",
                )
                if minimum_large_exchange is None:
                    minimum_large_exchange = exchange
                else:
                    minimum_large_exchange = min(
                        minimum_large_exchange, exchange
                    )

    need(rank_histogram, "empty reciprocal rank histogram")
    need(excess_branches["LOW_DEGREE_EXACT_SWAP"] > 0, "missing low swap")
    return {
        "field_prime": p,
        "source_degree": degree,
        "j": j,
        "source_size": 2 * degree,
        "complement_locators": len(complements),
        "locator_pairs": len(complements) * (len(complements) - 1) // 2,
        "same_projective_pairs": same_projective,
        "same_projective_minimum_exchange": same_projective_min_exchange,
        "distinct_projective_reciprocal_dimension_histogram": {
            str(key): rank_histogram[key] for key in sorted(rank_histogram)
        },
        "rank_excess_rational_degree_histogram": {
            str(key): rational_degrees[key] for key in sorted(rational_degrees)
        },
        "rank_excess_branch_histogram": {
            key: excess_branches[key] for key in sorted(excess_branches)
        },
        "minimum_large_exchange": minimum_large_exchange,
        "maximum_low_swap_exchange": maximum_low_swap_exchange,
    }


def locator_rank_excess_controls() -> list[dict[str, Any]]:
    return [
        locator_rank_excess_row(p=23, degree=3, j=4),
        locator_rank_excess_row(p=31, degree=4, j=5),
    ]


def f17_source_reciprocal_scan() -> dict[str, Any]:
    p = 17
    degree = 2
    j = 6
    source_size = 2 * degree
    domain_size = 2 * (degree + j)
    sigma, inverse, high_rows = evaluation_data(p, degree)
    carrier = list(range(source_size, domain_size))
    zero_size = j - 1
    carrier_locator = residue.locator(carrier, p)
    carrier_values = [
        residue.evaluate(carrier_locator, point, p) for point in sigma
    ]
    inverse_carrier = [pow(value, -1, p) for value in carrier_values]

    records = []
    carrier_set = set(carrier)
    for zero_tuple in itertools.combinations(carrier, zero_size):
        complement = tuple(sorted(carrier_set - set(zero_tuple)))
        zero_locator = residue.locator(zero_tuple, p)
        complement_locator = residue.locator(complement, p)
        zero_values = [
            residue.evaluate(zero_locator, point, p) for point in sigma
        ]
        complement_values = [
            residue.evaluate(complement_locator, point, p)
            for point in sigma
        ]
        records.append(
            {
                "zero_values": zero_values,
                "complement_values": complement_values,
            }
        )
    need(len(records) == 792, "F17 locator records")

    cases = residue.structured_pairs(p, degree, carrier)
    rng = random.Random(0xC5A11CE)
    for trial in range(32):
        left, right = residue.random_pair(rng, p, degree)
        cases.append((f"random_{trial:02d}", left, right))

    histogram: Counter[int] = Counter()
    for case_index, (case_name, left, right) in enumerate(cases):
        base = records[(case_index * 104729 + 8446) % len(records)]
        left_values = polynomial_values(left, sigma, p)
        right_values = polynomial_values(right, sigma, p)
        need(
            all(
                (left_values[index], right_values[index]) != (0, 0)
                for index in range(source_size)
            ),
            f"vanishing source pair: {case_name}",
        )
        epsilon0 = [
            base["zero_values"][index] * left_values[index] % p
            for index in range(source_size)
        ]
        epsilon1 = [
            base["zero_values"][index] * right_values[index] % p
            for index in range(source_size)
        ]
        u0 = [
            epsilon0[index] * inverse_carrier[index] % p
            for index in range(source_size)
        ]
        u1 = [
            epsilon1[index] * inverse_carrier[index] % p
            for index in range(source_size)
        ]

        source_constraint = multiplication_constraint(
            [u0, u1], sigma, inverse, high_rows, p
        )
        source_kernel = residue.nullspace(source_constraint, p)
        need(len(source_kernel) == 2, "source residue-line dimension")
        q_values = [
            [
                sum(
                    coefficient * pow(point, exponent, p)
                    for exponent, coefficient in enumerate(q)
                )
                % p
                for point in sigma
            ]
            for q in source_kernel
        ]
        reciprocal_matrix = multiplication_constraint(
            q_values, sigma, inverse, high_rows, p
        )
        reciprocal_nullity = source_size - residue.rank(
            reciprocal_matrix, p
        )
        need(reciprocal_nullity >= 2, "reciprocal nullity floor")

        u0_coefficients = residue.matrix_vector(inverse, u0, p)
        u1_coefficients = residue.matrix_vector(inverse, u1, p)
        for coefficients in (u0_coefficients, u1_coefficients):
            need(
                all(
                    value == 0
                    for value in residue.matrix_vector(
                        reciprocal_matrix, coefficients, p
                    )
                ),
                "source coordinate outside reciprocal kernel",
            )
        histogram[reciprocal_nullity] += 1

    need(sum(histogram.values()) == len(cases), "source scan mass")
    return {
        "field_prime": p,
        "source_degree": degree,
        "locator_records": len(records),
        "source_cases_checked": len(cases),
        "reciprocal_kernel_dimension_histogram": {
            str(key): histogram[key] for key in sorted(histogram)
        },
        "minimum_reciprocal_kernel_dimension": min(histogram),
        "all_source_coordinates_replayed_in_reciprocal_kernel": True,
    }


def deployed_arithmetic() -> dict[str, Any]:
    e = pencil.REDUCED_DEGREE
    source_size = pencil.SOURCE_SIZE
    p = active.BASE_PRIME
    need(source_size == 2 * e, "first-gap source size")
    need(e == 67_472, "first-gap degree")
    need(source_size == 134_944, "first-gap source cardinality")
    need(p == 2_130_706_433, "KoalaBear base field")
    return {
        "base_field_order": p,
        "source_degree": e,
        "source_size": source_size,
        "residue_space_dimension": source_size,
        "source_residue_line_dimension": 2,
        "base_projective_line_size": p + 1,
        "reciprocal_constraint_rows": 2 * (e - 1),
        "reciprocal_constraint_columns": source_size,
        "generic_reciprocal_rank": source_size - 2,
        "generic_reciprocal_kernel_dimension": 2,
        "rank_excess_threshold": 3,
        "same_projective_residue_exchange_floor": source_size,
        "same_exact_residue_exchange_floor": source_size + 1,
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "active_ledger": {
                "U_paid": active.PAID,
                "B_remaining": active.REMAINING,
                "additional_charge": 0,
            },
            "theorem": {
                "base_rational_points_on_residue_line": "0_OR_1_OR_P_PLUS_1",
                "two_base_points_force_base_defined_residue_line": True,
                "reciprocal_multiplier_kernel_is_base_defined": True,
                "reciprocal_kernel_dimension_floor": 2,
                "dimension_two_and_source_rank_two_force_projective_descent": True,
                "dimension_two_branch_is_owned_by_active_c5": True,
                "rank_excess_has_base_rational_normal_form": True,
                "reciprocal_degree_identity": "d=e-r+1",
                "rank_excess_locator_pair_dichotomy": (
                    "EXCHANGE_AT_LEAST_2e_MINUS_d_OR_EXACT_d_ROOT_SWAP"
                ),
                "post_c5_dichotomy": (
                    "ONE_BASE_PROJECTIVE_RESIDUE_POINT_OR_"
                    "RECIPROCAL_KERNEL_DIMENSION_AT_LEAST_3"
                ),
                "one_point_branch_has_global_projective_exchange_floor": True,
                "rank_excess_is_paid": False,
                "determinant_excess_is_paid": False,
            },
            "deployed_arithmetic": deployed_arithmetic(),
            "finite_controls": {
                "projective_rational_points": (
                    projective_rational_point_control()
                ),
                "reciprocal_rank_examples": reciprocal_rank_examples(),
                "rank_excess_locator_rows": locator_rank_excess_controls(),
                "f17_source_scan": f17_source_reciprocal_scan(),
            },
            "source_bindings": source_bindings(),
            "status": (
                "PROVED_PROJECTIVE_RESIDUE_C5_RANK_DICHOTOMY_"
                "RANK_PAYMENT_AND_PACKING_OPEN_ROW_OPEN"
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
        "title": "KoalaBear first-gap projective residue C5/rank dichotomy",
        "type": "object",
    }


def check_sources() -> None:
    path = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_projective_residue_c5_rank_dichotomy_v1.md"
    )
    note = path.read_text(encoding="utf-8")
    for anchor in [
        "Projective rational-point dichotomy",
        "Reciprocal multiplier kernel",
        "\\dim_B\\mathcal R(q_0,q_1)=2",
        "active C5 owner",
        "one-point-or-rank-excess",
        "2e=134{,}944",
        "rank-excess branch is not paid",
        "Reciprocal rational normal form",
        "d=e-r+1",
        "low-degree root swap",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero movement")
    need(
        cert["theorem"]["rank_excess_is_paid"] is False,
        "rank branch status",
    )
    need(
        cert["theorem"]["determinant_excess_is_paid"] is False,
        "packing status",
    )
    check_sources()


def emit() -> None:
    CERT.mkdir(parents=True, exist_ok=True)
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    cert = expected_certificate()
    schema = expected_schema()
    mutations = [
        lambda d: d["theorem"].__setitem__(
            "two_base_points_force_base_defined_residue_line", False
        ),
        lambda d: d["theorem"].__setitem__(
            "dimension_two_branch_is_owned_by_active_c5", False
        ),
        lambda d: d["theorem"].__setitem__(
            "post_c5_dichotomy", "UNBOUND"
        ),
        lambda d: d["theorem"].__setitem__(
            "reciprocal_degree_identity", "UNBOUND"
        ),
        lambda d: d["theorem"].__setitem__("rank_excess_is_paid", True),
        lambda d: d["deployed_arithmetic"].__setitem__(
            "rank_excess_threshold", 2
        ),
        lambda d: d["deployed_arithmetic"].__setitem__(
            "same_projective_residue_exchange_floor", 134_943
        ),
        lambda d: d["finite_controls"]["projective_rational_points"][
            "base_rational_intersection_histogram"
        ].__setitem__("1", 77),
        lambda d: d["finite_controls"]["reciprocal_rank_examples"][
            "rank_excess"
        ].__setitem__("kernel_dimension", 2),
        lambda d: d["finite_controls"]["rank_excess_locator_rows"][0][
            "rank_excess_branch_histogram"
        ].__setitem__("LOW_DEGREE_EXACT_SWAP", 0),
        lambda d: d["finite_controls"]["f17_source_scan"].__setitem__(
            "all_source_coordinates_replayed_in_reciprocal_kernel", False
        ),
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
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
            finite = cert["finite_controls"]
            print(f"architecture: {ARCH}")
            print(f"partition_sha256: {PARTITION_DIGEST}")
            print(
                "projective_control: "
                f"{finite['projective_rational_points'][
                    'base_rational_intersection_histogram'
                ]}"
            )
            print(
                "reciprocal_examples: "
                f"normal={finite['reciprocal_rank_examples']['normal'][
                    'kernel_dimension'
                ]} "
                f"excess={finite['reciprocal_rank_examples']['rank_excess'][
                    'kernel_dimension'
                ]}"
            )
            print(
                "f17_source_scan: "
                f"{finite['f17_source_scan'][
                    'reciprocal_kernel_dimension_histogram'
                ]}"
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
