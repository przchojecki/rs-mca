#!/usr/bin/env python3
"""Verify the first-gap complement-locator residue linearization."""

from __future__ import annotations

import argparse
import copy
import itertools
import random
import sys
from collections import Counter
from math import comb
from pathlib import Path
from typing import Any, Iterable

import verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1 as active
import verify_kb_mca_v4_first_gap_source_interpolation_pencil_v1 as pencil

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-first-gap-complement-locator-linearization-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_first_gap_complement_locator_linearization_v1.schema.json"
)

ARCH = active.ARCH
PARTITION_DIGEST = active.partition()["partition_sha256"]

SOURCE_PATHS = [
    (
        "experimental/data/certificates/"
        "kb-mca-v4-c5-twist-frobenius9208-adapter-v1/manifest.json"
    ),
    (
        "experimental/data/certificates/"
        "kb-mca-v4-active-full-histogram-replay-v1/certificate.json"
    ),
    (
        "experimental/data/certificates/"
        "kb-mca-v4-first-gap-source-interpolation-pencil-v1/certificate.json"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_source_interpolation_pencil_v1.md"
    ),
    "experimental/m1.tex",
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_complement_locator_linearization_v1.md"
    ),
]

Failure = active.Failure
need = active.need
seal = active.seal
dump = active.dump
load = active.load
file_digest = active.file_digest


def source_bindings() -> list[dict[str, str]]:
    result = []
    for index, path_text in enumerate(SOURCE_PATHS):
        path = ROOT / path_text
        need(path.is_file(), f"missing source: {path_text}")
        result.append(
            {
                "binding_id": (
                    f"SOURCE_{index:02d}_{path.stem.upper().replace('-', '_')}"
                ),
                "hash": file_digest(path),
                "hash_kind": "SHA256",
                "path": path_text,
            }
        )
    return result


def trim(poly: list[int]) -> list[int]:
    result = poly[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def mul(left: list[int], right: list[int], p: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % p
    return trim(result)


def divmod_poly(
    numerator: list[int], denominator: list[int], p: int
) -> tuple[list[int], list[int]]:
    numerator = trim([value % p for value in numerator])
    denominator = trim([value % p for value in denominator])
    need(denominator != [0], "zero polynomial divisor")
    if len(numerator) < len(denominator):
        return [0], numerator
    quotient = [0] * (len(numerator) - len(denominator) + 1)
    inverse = pow(denominator[-1], -1, p)
    while numerator != [0] and len(numerator) >= len(denominator):
        shift = len(numerator) - len(denominator)
        scale = numerator[-1] * inverse % p
        quotient[shift] = scale
        for index, value in enumerate(denominator):
            numerator[index + shift] = (
                numerator[index + shift] - scale * value
            ) % p
        numerator = trim(numerator)
    return trim(quotient), numerator


def gcd_poly(left: list[int], right: list[int], p: int) -> list[int]:
    left, right = trim(left), trim(right)
    while right != [0]:
        _, remainder = divmod_poly(left, right, p)
        left, right = right, remainder
    inverse = pow(left[-1], -1, p)
    return [(value * inverse) % p for value in left]


def evaluate(poly: list[int], x: int, p: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * x + coefficient) % p
    return result


def locator(points: Iterable[int], p: int) -> list[int]:
    result = [1]
    for point in points:
        result = mul(result, [(-point) % p, 1], p)
    return result


def rank(matrix: list[list[int]], p: int) -> int:
    rows = [[entry % p for entry in row] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if rows[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, p)
        rows[pivot_row] = [
            entry * inverse % p for entry in rows[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (entry - scale * pivot_entry) % p
                for entry, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def nullspace(matrix: list[list[int]], p: int) -> list[list[int]]:
    if not matrix:
        return []
    rows = [[entry % p for entry in row] for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_columns = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if rows[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, p)
        rows[pivot_row] = [
            entry * inverse % p for entry in rows[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (entry - scale * pivot_entry) % p
                for entry, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    free_columns = [
        column
        for column in range(column_count)
        if column not in pivot_columns
    ]
    basis = []
    for free_column in free_columns:
        vector = [0] * column_count
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivot_columns):
            vector[pivot_column] = (-rows[row][free_column]) % p
        basis.append(vector)
    need(
        len(basis) == column_count - len(pivot_columns),
        "nullspace dimension",
    )
    return basis


def inverse_matrix(matrix: list[list[int]], p: int) -> list[list[int]]:
    size = len(matrix)
    rows = [
        [entry % p for entry in row]
        + [1 if i == j else 0 for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if rows[row][column]),
            None,
        )
        need(pivot is not None, "singular interpolation matrix")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        inverse = pow(rows[column][column], -1, p)
        rows[column] = [entry * inverse % p for entry in rows[column]]
        for row in range(size):
            if row == column or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (entry - scale * pivot_entry) % p
                for entry, pivot_entry in zip(rows[row], rows[column])
            ]
    return [row[size:] for row in rows]


def matrix_vector(
    matrix: list[list[int]], vector: list[int], p: int
) -> list[int]:
    return [
        sum(entry * value for entry, value in zip(row, vector)) % p
        for row in matrix
    ]


def projective(vector: Iterable[int], p: int) -> tuple[int, ...]:
    values = tuple(value % p for value in vector)
    pivot = next((value for value in values if value), None)
    need(pivot is not None, "zero projective vector")
    inverse = pow(pivot, -1, p)
    return tuple(value * inverse % p for value in values)


def rref_two(
    left: tuple[int, ...], right: tuple[int, ...], p: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    rows = [list(left), list(right)]
    pivot_row = 0
    for column in range(len(left)):
        pivot = next(
            (
                row
                for row in range(pivot_row, 2)
                if rows[row][column] % p
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, p)
        rows[pivot_row] = [
            entry * inverse % p for entry in rows[pivot_row]
        ]
        for row in range(2):
            if row == pivot_row or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (entry - scale * pivot_entry) % p
                for entry, pivot_entry in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == 2:
            break
    need(pivot_row == 2, "dependent projective points")
    return tuple(rows[0]), tuple(rows[1])


def line_points(
    basis: tuple[tuple[int, ...], tuple[int, ...]], p: int
) -> set[tuple[int, ...]]:
    left, right = basis
    points = {projective(right, p)}
    for scalar in range(p):
        points.add(
            projective(
                [
                    (left[index] + scalar * right[index]) % p
                    for index in range(len(left))
                ],
                p,
            )
        )
    need(len(points) == p + 1, "projective line size")
    return points


def universal_line_maximum(
    histogram: Counter[tuple[int, ...]], p: int
) -> dict[str, Any]:
    points = sorted(histogram)
    line_keys: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for left_index, left in enumerate(points):
        for right in points[left_index + 1 :]:
            line_keys.add(rref_two(left, right, p))
    maximum = max(histogram.values(), default=0)
    maximizer: tuple[tuple[int, ...], tuple[int, ...]] | None = None
    for key in line_keys:
        weight = sum(histogram.get(point, 0) for point in line_points(key, p))
        if weight > maximum:
            maximum = weight
            maximizer = key
    return {
        "occupied_projective_points": len(points),
        "projective_lines_checked": len(line_keys),
        "maximum_point_occupancy": max(histogram.values(), default=0),
        "maximum_two_dimensional_subspace_occupancy": maximum,
        "maximizing_line_rref": (
            [list(row) for row in maximizer] if maximizer else None
        ),
    }


def realize_residue_line(
    *,
    line_basis: tuple[tuple[int, ...], tuple[int, ...]],
    records: list[dict[str, Any]],
    sigma: list[int],
    inverse_vandermonde: list[list[int]],
    high_rows: list[list[int]],
    degree: int,
    p: int,
) -> dict[str, Any]:
    points = line_points(line_basis, p)
    occupied = [
        record
        for record in records
        if projective(record["residue"], p) in points
    ]
    need(occupied, "realization needs an occupied base point")
    target_occupancy = sum(
        1
        for record in records
        if projective(record["residue"], p) in points
    )
    attempted_bases = 0
    maximum_source_space_dimension = 0
    obstruction_counts: Counter[str] = Counter()
    obstruction_examples: dict[str, dict[str, Any]] = {}
    for base in occupied:
        base_point = projective(base["residue"], p)
        base_values = [
            evaluate(list(base["residue"]), point, p) for point in sigma
        ]
        need(all(base_values), "base residue vanishes on source")
        second_residue = (
            line_basis[1]
            if projective(line_basis[0], p) == base_point
            else line_basis[0]
        )
        need(
            projective(second_residue, p) != base_point,
            "dependent line basis",
        )
        attempted_bases += 1
        second_values = [
            evaluate(list(second_residue), point, p) for point in sigma
        ]
        multiplier_values = [
            second_values[index] * pow(base_values[index], -1, p) % p
            for index in range(len(sigma))
        ]

        constraint_columns = []
        for exponent in range(degree + 1):
            product_values = [
                multiplier_values[index] * pow(point, exponent, p) % p
                for index, point in enumerate(sigma)
            ]
            coefficients = matrix_vector(
                inverse_vandermonde, product_values, p
            )
            constraint_columns.append(coefficients[degree + 1 :])
        constraint_matrix = [
            [
                constraint_columns[column][row]
                for column in range(degree + 1)
            ]
            for row in range(degree - 1)
        ]
        source_space = nullspace(constraint_matrix, p)
        maximum_source_space_dimension = max(
            maximum_source_space_dimension, len(source_space)
        )
        need(len(source_space) >= 2, "source realization dimension")
        source_gcd = source_space[0]
        for polynomial in source_space[1:]:
            source_gcd = gcd_poly(source_gcd, polynomial, p)
        source_max_degree = max(len(trim(polynomial)) - 1 for polynomial in source_space)

        projective_polynomials: dict[tuple[int, ...], list[int]] = {}
        for coefficients in itertools.product(
            range(p), repeat=len(source_space)
        ):
            if not any(coefficients):
                continue
            polynomial = [
                sum(
                    coefficients[basis_index]
                    * source_space[basis_index][coefficient_index]
                    for basis_index in range(len(source_space))
                )
                % p
                for coefficient_index in range(degree + 1)
            ]
            key = projective(polynomial, p)
            projective_polynomials.setdefault(key, trim(polynomial))

        witness: tuple[list[int], list[int]] | None = None
        polynomial_values = list(projective_polynomials.values())
        for left_index, left in enumerate(polynomial_values):
            for right in polynomial_values[left_index + 1 :]:
                if (
                    max(len(trim(left)), len(trim(right))) - 1
                    != degree
                ):
                    continue
                if gcd_poly(left, right, p) == [1]:
                    witness = (left, right)
                    break
            if witness is not None:
                break
        if witness is None:
            if source_max_degree < degree:
                obstruction = "DEGREE_DEFECT"
            elif len(trim(source_gcd)) - 1 > 0:
                obstruction = "COMMON_DIVISOR"
            else:
                obstruction = "FINITE_PAIR_OBSTRUCTION"
            obstruction_counts[obstruction] += 1
            obstruction_examples.setdefault(
                obstruction,
                {
                    "base_zero_set": list(base["zero"]),
                    "source_space_basis": source_space,
                    "source_space_gcd": source_gcd,
                    "source_space_max_degree": source_max_degree,
                },
            )
            continue
        left, right = witness

        left_values = [evaluate(left, point, p) for point in sigma]
        right_values = [evaluate(right, point, p) for point in sigma]
        need(
            all(
                (left_values[index], right_values[index]) != (0, 0)
                for index in range(len(sigma))
            ),
            "realized source vanishes",
        )
        epsilon_0 = [
            base["zero_values"][index] * left_values[index] % p
            for index in range(len(sigma))
        ]
        epsilon_1 = [
            base["zero_values"][index] * right_values[index] % p
            for index in range(len(sigma))
        ]

        realized_candidates = []
        for record in records:
            inverse_zero = [
                pow(value, -1, p) for value in record["zero_values"]
            ]
            quotient_left = [
                epsilon_0[index] * inverse_zero[index] % p
                for index in range(len(sigma))
            ]
            quotient_right = [
                epsilon_1[index] * inverse_zero[index] % p
                for index in range(len(sigma))
            ]
            if all(
                value == 0
                for value in matrix_vector(high_rows, quotient_left, p)
                + matrix_vector(high_rows, quotient_right, p)
            ):
                realized_candidates.append(record)
        if len(realized_candidates) != target_occupancy:
            obstruction_counts["CANDIDATE_SET_MISMATCH"] += 1
            continue
        need(
            {
                projective(record["residue"], p)
                for record in realized_candidates
            }
            <= points,
            "realization escaped target line",
        )
        return {
            "target_line_rref": [list(row) for row in line_basis],
            "target_line_occupancy": target_occupancy,
            "base_zero_set": list(base["zero"]),
            "second_residue_coefficients": list(second_residue),
            "multiplier_source_space_dimension": len(source_space),
            "reduced_left_coefficients": left,
            "reduced_right_coefficients": right,
            "reduced_pair_coprime": gcd_poly(left, right, p) == [1],
            "reduced_pair_exact_degree": (
                max(len(trim(left)), len(trim(right))) - 1 == degree
            ),
            "realized_candidate_count": len(realized_candidates),
            "occupied_bases_tested": attempted_bases,
            "realizable": True,
        }
    return {
        "target_line_rref": [list(row) for row in line_basis],
        "target_line_occupancy": target_occupancy,
        "occupied_bases_tested": attempted_bases,
        "maximum_multiplier_source_space_dimension": (
            maximum_source_space_dimension
        ),
        "obstruction_counts": dict(sorted(obstruction_counts.items())),
        "obstruction_examples": obstruction_examples,
        "realizable": False,
    }


def primitive_source_line_maximum(
    *,
    histogram: Counter[tuple[int, ...]],
    records: list[dict[str, Any]],
    sigma: list[int],
    inverse_vandermonde: list[list[int]],
    high_rows: list[list[int]],
    degree: int,
    p: int,
) -> dict[str, Any]:
    points = sorted(histogram)
    line_keys: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for left_index, left in enumerate(points):
        for right in points[left_index + 1 :]:
            line_keys.add(rref_two(left, right, p))
    weighted_lines = sorted(
        (
            (
                sum(
                    histogram.get(point, 0)
                    for point in line_points(key, p)
                ),
                key,
            )
            for key in line_keys
        ),
        key=lambda item: (-item[0], item[1]),
    )
    rejected_by_reason: Counter[str] = Counter()
    occupancy_levels_rejected: Counter[int] = Counter()
    for index, (occupancy, key) in enumerate(weighted_lines, start=1):
        realization = realize_residue_line(
            line_basis=key,
            records=records,
            sigma=sigma,
            inverse_vandermonde=inverse_vandermonde,
            high_rows=high_rows,
            degree=degree,
            p=p,
        )
        if realization["realizable"]:
            return {
                "maximum_coprime_exact_degree_source_line_occupancy": (
                    occupancy
                ),
                "lines_tested_until_witness": index,
                "higher_or_equal_lines_rejected": index - 1,
                "rejected_by_reason": dict(sorted(rejected_by_reason.items())),
                "rejected_occupancy_histogram": {
                    str(level): count
                    for level, count in sorted(
                        occupancy_levels_rejected.items(), reverse=True
                    )
                },
                "witness": realization,
            }
        occupancy_levels_rejected[occupancy] += 1
        for reason, count in realization["obstruction_counts"].items():
            rejected_by_reason[reason] += count
    raise Failure("no primitive source-realizable occupied residue line")


def structured_pairs(
    p: int, degree: int, carrier: list[int]
) -> list[tuple[str, list[int], list[int]]]:
    monomial = [1] + [0] * (degree - 1) + [1]
    split_left = locator(carrier[:degree], p)
    split_right = locator(carrier[degree : 2 * degree], p)
    power_left = [1]
    power_right = [1]
    for _ in range(degree):
        power_left = mul(power_left, [(-carrier[0]) % p, 1], p)
        power_right = mul(power_right, [(-carrier[1]) % p, 1], p)
    dense_left = [(2 * index + 1) % p for index in range(degree + 1)]
    dense_right = [(3 * index + 2) % p for index in range(degree + 1)]
    if gcd_poly(dense_left, dense_right, p) != [1]:
        dense_right[0] = (dense_right[0] + 1) % p
    result = [
        ("constant_monomial", [1], monomial),
        ("disjoint_split", split_left, split_right),
        ("two_powers", power_left, power_right),
        ("dense_fixed", dense_left, dense_right),
    ]
    for name, left, right in result:
        need(
            max(len(trim(left)), len(trim(right))) - 1 == degree,
            f"structured degree: {name}",
        )
        need(gcd_poly(left, right, p) == [1], f"structured gcd: {name}")
    return result


def random_pair(
    rng: random.Random, p: int, degree: int
) -> tuple[list[int], list[int]]:
    while True:
        left = [rng.randrange(p) for _ in range(degree)] + [
            rng.randrange(1, p)
        ]
        right = [rng.randrange(p) for _ in range(degree)] + [
            rng.randrange(1, p)
        ]
        if gcd_poly(left, right, p) == [1]:
            return left, right


def minimum_exchange(
    members: list[tuple[int, ...]]
) -> int | None:
    if len(members) < 2:
        return None
    result = min(
        len(set(left) - set(right))
        for index, left in enumerate(members)
        for right in members[index + 1 :]
    )
    return result


def row_census(
    *,
    name: str,
    p: int,
    degree: int,
    j: int,
    random_trials: int,
    compute_universal_line: bool,
) -> dict[str, Any]:
    source_size = 2 * degree
    domain_size = 2 * (degree + j)
    need(domain_size < p, f"domain not embedded: {name}")
    sigma = list(range(source_size))
    carrier = list(range(source_size, domain_size))
    zero_size = j - 1
    complement_size = j + 1
    need(len(carrier) == 2 * j, "carrier size")

    vandermonde = [
        [pow(point, exponent, p) for exponent in range(source_size)]
        for point in sigma
    ]
    inverse_vandermonde = inverse_matrix(vandermonde, p)
    high_rows = inverse_vandermonde[degree + 1 :]
    need(len(high_rows) == degree - 1, "parity row count")

    carrier_set = set(carrier)
    carrier_locator = locator(carrier, p)
    carrier_values = [evaluate(carrier_locator, point, p) for point in sigma]
    need(all(carrier_values), "carrier/source disjointness")

    records = []
    projective_histogram: Counter[tuple[int, ...]] = Counter()
    exact_histogram: Counter[tuple[int, ...]] = Counter()
    for zero_tuple in itertools.combinations(carrier, zero_size):
        zero_set = set(zero_tuple)
        complement = tuple(sorted(carrier_set - zero_set))
        need(len(complement) == complement_size, "complement size")
        zero_locator = locator(zero_tuple, p)
        complement_locator = locator(complement, p)
        zero_values = [evaluate(zero_locator, point, p) for point in sigma]
        complement_values = [
            evaluate(complement_locator, point, p) for point in sigma
        ]
        need(all(zero_values), "zero/source disjointness")
        need(
            all(
                zero_values[index] * complement_values[index] % p
                == carrier_values[index]
                for index in range(source_size)
            ),
            "complement identity",
        )
        residue = tuple(
            matrix_vector(inverse_vandermonde, complement_values, p)
        )
        projective_histogram[projective(residue, p)] += 1
        exact_histogram[residue] += 1
        records.append(
            {
                "zero": zero_tuple,
                "complement": complement,
                "zero_values": zero_values,
                "complement_values": complement_values,
                "residue": residue,
            }
        )

    expected_total = comb(2 * j, j - 1)
    need(len(records) == expected_total, "locator census size")
    need(sum(projective_histogram.values()) == expected_total, "histogram mass")

    rng = random.Random(0x4B425249444745 + p * 1000 + degree * 100 + j)
    source_cases = structured_pairs(p, degree, carrier)
    for trial in range(random_trials):
        left, right = random_pair(rng, p, degree)
        source_cases.append((f"random_{trial:03d}", left, right))

    maximum_joint = -1
    maximum_case: dict[str, Any] | None = None
    case_summaries = []
    for case_index, (case_name, left, right) in enumerate(source_cases):
        base_index = (
            case_index * 104729 + degree * 8191 + j * 127
        ) % len(records)
        base = records[base_index]
        left_values = [evaluate(left, point, p) for point in sigma]
        right_values = [evaluate(right, point, p) for point in sigma]
        need(
            all(
                (left_values[index], right_values[index]) != (0, 0)
                for index in range(source_size)
            ),
            "source pair vanishes",
        )
        epsilon_0 = [
            base["zero_values"][index] * left_values[index] % p
            for index in range(source_size)
        ]
        epsilon_1 = [
            base["zero_values"][index] * right_values[index] % p
            for index in range(source_size)
        ]
        inverse_carrier = [
            pow(value, -1, p) for value in carrier_values
        ]
        u0 = [
            epsilon_0[index] * inverse_carrier[index] % p
            for index in range(source_size)
        ]
        u1 = [
            epsilon_1[index] * inverse_carrier[index] % p
            for index in range(source_size)
        ]

        constraint_columns = []
        for exponent in range(source_size):
            q_values = [pow(point, exponent, p) for point in sigma]
            outputs = []
            for source_coordinate in (u0, u1):
                product_values = [
                    q_values[index] * source_coordinate[index] % p
                    for index in range(source_size)
                ]
                coefficients = matrix_vector(
                    inverse_vandermonde, product_values, p
                )
                outputs.extend(coefficients[degree + 1 :])
            constraint_columns.append(outputs)
        constraint_matrix = [
            [constraint_columns[column][row] for column in range(source_size)]
            for row in range(2 * (degree - 1))
        ]
        residue_kernel_rank = rank(constraint_matrix, p)
        residue_kernel_nullity = source_size - residue_kernel_rank
        need(residue_kernel_nullity == 2, "residue-line dimension")

        pass_left = 0
        pass_right = 0
        joint = []
        exact_buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
        projective_buckets: dict[
            tuple[int, ...], list[tuple[int, ...]]
        ] = {}
        for record in records:
            inverse_zero = [
                pow(value, -1, p) for value in record["zero_values"]
            ]
            quotient_left = [
                epsilon_0[index] * inverse_zero[index] % p
                for index in range(source_size)
            ]
            quotient_right = [
                epsilon_1[index] * inverse_zero[index] % p
                for index in range(source_size)
            ]
            left_high = matrix_vector(high_rows, quotient_left, p)
            right_high = matrix_vector(high_rows, quotient_right, p)
            left_ok = all(value == 0 for value in left_high)
            right_ok = all(value == 0 for value in right_high)
            pass_left += int(left_ok)
            pass_right += int(right_ok)

            linear_left = [
                record["complement_values"][index] * u0[index] % p
                for index in range(source_size)
            ]
            linear_right = [
                record["complement_values"][index] * u1[index] % p
                for index in range(source_size)
            ]
            linear_ok = all(
                value == 0
                for value in matrix_vector(high_rows, linear_left, p)
                + matrix_vector(high_rows, linear_right, p)
            )
            need(
                linear_ok == (left_ok and right_ok),
                "nonlinear/linear candidate mismatch",
            )
            if not linear_ok:
                continue
            joint.append(record)
            exact_buckets.setdefault(record["residue"], []).append(
                record["complement"]
            )
            projective_buckets.setdefault(
                projective(record["residue"], p), []
            ).append(record["complement"])

        need(base in joint, "constructed candidate missing")
        exact_minima = [
            minimum_exchange(members)
            for members in exact_buckets.values()
            if len(members) >= 2
        ]
        projective_minima = [
            minimum_exchange(members)
            for members in projective_buckets.values()
            if len(members) >= 2
        ]
        if exact_minima:
            need(min(exact_minima) >= source_size + 1, "exact distance")
        if projective_minima:
            need(min(projective_minima) >= source_size, "projective distance")

        summary = {
            "case": case_name,
            "base_zero_index": base_index,
            "left_only_pass_count": pass_left,
            "right_only_pass_count": pass_right,
            "joint_candidate_count": len(joint),
            "residue_kernel_rank": residue_kernel_rank,
            "residue_kernel_dimension": residue_kernel_nullity,
            "projective_parameter_count": len(projective_buckets),
            "maximum_exact_residue_multiplicity": max(
                (len(value) for value in exact_buckets.values()), default=0
            ),
            "maximum_projective_residue_multiplicity": max(
                (len(value) for value in projective_buckets.values()),
                default=0,
            ),
            "minimum_exact_residue_exchange": (
                min(exact_minima) if exact_minima else None
            ),
            "minimum_projective_residue_exchange": (
                min(projective_minima) if projective_minima else None
            ),
        }
        case_summaries.append(summary)
        if len(joint) > maximum_joint:
            maximum_joint = len(joint)
            maximum_case = summary

    cylinder_projective_dimension = j + 3 - 2 * degree
    need(cylinder_projective_dimension >= 0, "negative cylinder dimension")
    fixed_dim_bound = comb(2 * j, cylinder_projective_dimension)
    need(maximum_joint <= fixed_dim_bound, "fixed-dimensional bound")

    result = {
        "row": name,
        "field_prime": p,
        "source_degree": degree,
        "source_size": source_size,
        "j": j,
        "carrier_size": len(carrier),
        "zero_locator_degree": zero_size,
        "complement_locator_degree": complement_size,
        "candidate_locator_count": expected_total,
        "source_parity_constraints": 2 * (degree - 1),
        "residue_line_dimension": 2,
        "cylinder_vector_dimension": j - 2 * degree + 4,
        "cylinder_projective_dimension": cylinder_projective_dimension,
        "fixed_dimensional_bound": fixed_dim_bound,
        "maximum_projective_point_occupancy": max(
            projective_histogram.values()
        ),
        "maximum_exact_residue_occupancy": max(exact_histogram.values()),
        "source_cases_checked": len(source_cases),
        "maximum_sampled_source_compatible_candidates": maximum_joint,
        "maximum_sampled_source_case": maximum_case,
        "structured_cases": case_summaries[:4],
    }
    if compute_universal_line:
        result["universal_residue_line_census"] = universal_line_maximum(
            projective_histogram, p
        )
        maximizing_line = result["universal_residue_line_census"][
            "maximizing_line_rref"
        ]
        need(maximizing_line is not None, "missing maximizing line")
        realization = realize_residue_line(
                line_basis=(
                    tuple(maximizing_line[0]),
                    tuple(maximizing_line[1]),
                ),
                records=records,
                sigma=sigma,
                inverse_vandermonde=inverse_vandermonde,
                high_rows=high_rows,
                degree=degree,
                p=p,
            )
        result["universal_extremizer_source_realization"] = realization
        if realization["realizable"]:
            need(
                realization["realized_candidate_count"]
                == result["universal_residue_line_census"][
                    "maximum_two_dimensional_subspace_occupancy"
                ],
                "universal extremizer realization mismatch",
            )
        need(
            maximum_joint
            <= result["universal_residue_line_census"][
                "maximum_two_dimensional_subspace_occupancy"
            ],
            "source maximum exceeds universal line maximum",
        )
        result["primitive_source_line_census"] = (
            primitive_source_line_maximum(
                histogram=projective_histogram,
                records=records,
                sigma=sigma,
                inverse_vandermonde=inverse_vandermonde,
                high_rows=high_rows,
                degree=degree,
                p=p,
            )
        )
        need(
            result["primitive_source_line_census"][
                "maximum_coprime_exact_degree_source_line_occupancy"
            ]
            <= result["universal_residue_line_census"][
                "maximum_two_dimensional_subspace_occupancy"
            ],
            "primitive maximum exceeds universal maximum",
        )
    return result


def deployed_arithmetic() -> dict[str, Any]:
    e = pencil.REDUCED_DEGREE
    j = pencil.J
    source_size = pencil.SOURCE_SIZE
    carrier_size = 2 * j
    zero_degree = j - 1
    complement_degree = j + 1
    need(source_size == 2 * e, "deployed source size")
    need(pencil.N - source_size == carrier_size, "full carrier")
    cylinder_vector_dimension = complement_degree - source_size + 3
    cylinder_projective_dimension = cylinder_vector_dimension - 1
    need(
        cylinder_vector_dimension == j - 2 * e + 4,
        "deployed cylinder dimension",
    )
    need(cylinder_projective_dimension == 846_163, "deployed dimension")
    return {
        "n": pencil.N,
        "source_degree": e,
        "source_size": source_size,
        "j": j,
        "carrier_size": carrier_size,
        "zero_locator_degree": zero_degree,
        "complement_locator_degree": complement_degree,
        "source_residue_dimension": source_size,
        "residue_line_dimension": 2,
        "source_parity_codimension": source_size - 2,
        "cylinder_vector_dimension": cylinder_vector_dimension,
        "cylinder_projective_dimension": cylinder_projective_dimension,
        "fixed_dimensional_bound_symbolic": (
            f"C({carrier_size},{cylinder_projective_dimension})"
        ),
        "active_budget": active.REMAINING,
        "fixed_dimensional_bound_budget_fitting": False,
    }


def finite_censuses() -> list[dict[str, Any]]:
    return [
        row_census(
            name="F17_E2_J6",
            p=17,
            degree=2,
            j=6,
            random_trials=96,
            compute_universal_line=True,
        ),
        row_census(
            name="F19_E2_J7",
            p=19,
            degree=2,
            j=7,
            random_trials=48,
            compute_universal_line=False,
        ),
        row_census(
            name="F23_E3_J8",
            p=23,
            degree=3,
            j=8,
            random_trials=16,
            compute_universal_line=False,
        ),
    ]


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
                "complement_identity": "L_Z*L_Y=L_V",
                "quotient_tests_linearize": True,
                "source_multiplier_map_injective": True,
                "source_residue_space_dimension": 2,
                "candidate_iff_complement_residue_in_source_line": True,
                "polynomial_preimage_is_linear_cylinder": True,
                "residue_line_admission_dichotomy": (
                    "RANK_EXCESS_OR_DEGREE_DEFECT_OR_COMMON_DIVISOR_"
                    "OR_COPRIME_EXACT_DEGREE_REALIZATION"
                ),
                "same_exact_residue_exchange_floor": "2e+1",
                "same_projective_residue_exchange_floor": "2e",
                "fixed_dimensional_incidence_bound_applies": True,
                "universal_toy_extremizer_realizability_exhausted": True,
                "determinant_mass_paid": False,
            },
            "deployed_arithmetic": deployed_arithmetic(),
            "finite_censuses": finite_censuses(),
            "source_bindings": source_bindings(),
            "status": (
                "PROVED_COMPLEMENT_LOCATOR_LINEARIZATION_"
                "GROWING_DIMENSIONAL_INCIDENCE_OPEN_ROW_OPEN"
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
        "title": "KoalaBear first-gap complement-locator linearization",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_complement_locator_linearization_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED COMPLEMENT-LOCATOR LINEARIZATION",
        "\\boxed{L_Z^{-1}=L_YL_V^{-1}\\quad\\text{in }A_\\Sigma.}",
        "\\boxed{Z\\text{ is admissible}\\iff[L_Y]\\in W_\\Sigma.}",
        "\\boxed{d=j+3-2e=846{,}163.}",
        "growing-dimensional residue-cylinder incidence",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(
    certificate: dict[str, Any],
    schema: dict[str, Any],
    *,
    expected: dict[str, Any] | None = None,
    expected_schema_value: dict[str, Any] | None = None,
) -> None:
    if expected is None:
        expected = expected_certificate()
    if expected_schema_value is None:
        expected_schema_value = expected_schema()
    need(
        certificate == expected,
        "certificate differs from exact replay",
    )
    need(
        schema == expected_schema_value,
        "schema differs from exact replay",
    )
    need(
        certificate["active_ledger"]["additional_charge"] == 0,
        "zero ledger movement",
    )
    need(
        certificate["theorem"]["determinant_mass_paid"] is False,
        "open determinant status",
    )
    check_sources()


def emit() -> None:
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    certificate = expected_certificate()
    schema = expected_schema()
    mutations = [
        lambda data: data["theorem"].__setitem__(
            "quotient_tests_linearize", False
        ),
        lambda data: data["theorem"].__setitem__(
            "source_residue_space_dimension", 3
        ),
        lambda data: data["theorem"].__setitem__(
            "candidate_iff_complement_residue_in_source_line", False
        ),
        lambda data: data["deployed_arithmetic"].__setitem__(
            "cylinder_projective_dimension", 846_164
        ),
        lambda data: data["finite_censuses"][0].__setitem__(
            "maximum_sampled_source_compatible_candidates", 0
        ),
        lambda data: data["theorem"].__setitem__(
            "universal_toy_extremizer_realizability_exhausted", False
        ),
        lambda data: data["theorem"].__setitem__(
            "residue_line_admission_dichotomy", "UNBOUND"
        ),
        lambda data: data["active_ledger"].__setitem__(
            "additional_charge", 1
        ),
    ]
    passed = 0
    for mutate in mutations:
        bad = copy.deepcopy(certificate)
        mutate(bad)
        try:
            validate(
                bad,
                schema,
                expected=certificate,
                expected_schema_value=schema,
            )
        except Failure:
            passed += 1
        else:
            raise Failure("tamper accepted")
    need(passed == len(mutations), "tamper count")
    print(f"tamper-selftest: PASS {passed}/{len(mutations)}")


def print_summary(certificate: dict[str, Any]) -> None:
    arithmetic = certificate["deployed_arithmetic"]
    print(f"architecture: {certificate['architecture_id']}")
    print(f"partition_sha256: {certificate['partition_sha256']}")
    print(
        "deployed cylinder: "
        f"residue_dim=2 projective_dim="
        f"{arithmetic['cylinder_projective_dimension']} "
        f"codim={arithmetic['source_parity_codimension']}"
    )
    for row in certificate["finite_censuses"]:
        print(
            f"{row['row']}: total={row['candidate_locator_count']} "
            "sampled_source_max="
            f"{row['maximum_sampled_source_compatible_candidates']} "
            f"fixed_dim_bound={row['fixed_dimensional_bound']}"
        )
        if "universal_residue_line_census" in row:
            universal = row["universal_residue_line_census"]
            print(
                "  universal_line_max="
                f"{universal['maximum_two_dimensional_subspace_occupancy']} "
                f"lines={universal['projective_lines_checked']}"
            )
        if "primitive_source_line_census" in row:
            primitive = row["primitive_source_line_census"]
            print(
                "  coprime_exact_degree_line_max="
                f"{primitive['maximum_coprime_exact_degree_source_line_occupancy']} "
                f"lines_until_witness={primitive['lines_tested_until_witness']}"
            )
    print(f"payload_sha256: {certificate['payload_sha256']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--scan", action="store_true")
    args = parser.parse_args()
    try:
        if args.scan:
            certificate = seal(
                {
                    "deployed_arithmetic": deployed_arithmetic(),
                    "finite_censuses": finite_censuses(),
                }
            )
            print_summary(
                {
                    "architecture_id": ARCH,
                    "partition_sha256": PARTITION_DIGEST,
                    "deployed_arithmetic": certificate["deployed_arithmetic"],
                    "finite_censuses": certificate["finite_censuses"],
                    "payload_sha256": certificate["payload_sha256"],
                }
            )
        if args.emit:
            emit()
        if args.check:
            certificate = load(CERT_PATH)
            schema = load(SCHEMA_PATH)
            validate(certificate, schema)
            print_summary(certificate)
            print("check: PASS")
        if args.tamper_selftest:
            tamper_selftest()
        if not (
            args.emit or args.check or args.tamper_selftest or args.scan
        ):
            parser.error(
                "choose --emit, --check, --tamper-selftest, or --scan"
            )
    except (Failure, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
