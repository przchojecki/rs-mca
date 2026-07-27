#!/usr/bin/env python3
"""Verify the first-gap outlier-basis/residue transform."""

from __future__ import annotations

import argparse
import copy
import itertools
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1 as active
import verify_kb_mca_v4_first_gap_complement_locator_linearization_v1 as residue

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-first-gap-outlier-basis-residue-transform-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.schema.json"
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
        "experimental/notes/m1/"
        "m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
    ),
    (
        "experimental/notes/m1/"
        "m1_kb_rank9_active_source_matroid_reindex_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.md"
    ),
]


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


def determinant(matrix: list[list[int]], p: int) -> int:
    rows = [[entry % p for entry in row] for row in matrix]
    size = len(rows)
    need(all(len(row) == size for row in rows), "square determinant")
    result = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if rows[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            result = -result
        pivot_value = rows[column][column]
        result = result * pivot_value % p
        inverse = pow(pivot_value, -1, p)
        for row in range(column + 1, size):
            scale = rows[row][column] * inverse % p
            for index in range(column, size):
                rows[row][index] = (
                    rows[row][index] - scale * rows[column][index]
                ) % p
    return result % p


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
        need(pivot is not None, "singular basis")
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


def vector_add(
    left: Iterable[int], right: Iterable[int], p: int
) -> tuple[int, ...]:
    return tuple((a + b) % p for a, b in zip(left, right))


def vector_scale(vector: Iterable[int], scale: int, p: int) -> tuple[int, ...]:
    return tuple(scale * value % p for value in vector)


def dot(left: Iterable[int], right: Iterable[int], p: int) -> int:
    return sum(a * b for a, b in zip(left, right)) % p


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


def locator(points: Iterable[int], p: int) -> list[int]:
    result = [1]
    for point in points:
        result = mul(result, [(-point) % p, 1], p)
    return result


def evaluate(poly: list[int], x: int, p: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * x + coefficient) % p
    return result


def basis_line(
    basis: tuple[int, ...],
    rows: dict[int, tuple[int, ...]],
    u: dict[int, int],
    v: dict[int, int],
    p: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    matrix = [list(rows[x]) for x in basis]
    inverse = inverse_matrix(matrix, p)
    alpha = tuple(
        (-value) % p
        for value in matrix_vector(inverse, [u[x] for x in basis], p)
    )
    beta = tuple(
        (-value) % p
        for value in matrix_vector(inverse, [v[x] for x in basis], p)
    )
    return alpha, beta


def line_values(
    alpha: tuple[int, ...],
    beta: tuple[int, ...],
    slopes: Iterable[int],
    p: int,
) -> dict[int, tuple[int, ...]]:
    return {
        eta: vector_add(alpha, vector_scale(beta, eta, p), p)
        for eta in slopes
    }


def finite_model() -> dict[str, Any]:
    p = 17
    carrier = tuple(range(8))
    rank = 2
    threshold = 2
    rows = {x: (1, x) for x in carrier}
    u = {x: (x**2 + 3 * x + 1) % p for x in carrier}
    v = {x: (x**3 + 2 * x + 5) % p for x in carrier}

    seed_bases = ((0, 1), (3, 5))
    seed_groups = ((0, 1, 2, 3, 4), (5, 6, 7, 8))
    graph_points: dict[int, tuple[int, ...]] = {}
    for basis, slopes in zip(seed_bases, seed_groups):
        alpha, beta = basis_line(basis, rows, u, v, p)
        graph_points.update(line_values(alpha, beta, slopes, p))

    errors = {}
    for eta, zeta in graph_points.items():
        errors[eta] = {
            x: (u[x] + eta * v[x] + dot(rows[x], zeta, p)) % p
            for x in carrier
        }

    bases = [
        basis
        for basis in itertools.combinations(carrier, rank)
        if determinant([list(rows[x]) for x in basis], p)
    ]
    basis_records = []
    rich_lines: dict[
        tuple[tuple[int, ...], tuple[int, ...]], dict[str, Any]
    ] = {}
    for basis in bases:
        alpha, beta = basis_line(basis, rows, u, v, p)
        delta = determinant([list(rows[x]) for x in basis], p)
        common_zero = []
        minor_support = []
        moving_map = {}
        for x in carrier:
            bordered_u = [list(rows[y]) + [u[y]] for y in basis]
            bordered_u.append(list(rows[x]) + [u[x]])
            bordered_v = [list(rows[y]) + [v[y]] for y in basis]
            bordered_v.append(list(rows[x]) + [v[x]])
            minor_u = determinant(bordered_u, p)
            minor_v = determinant(bordered_v, p)
            a_value = (u[x] + dot(rows[x], alpha, p)) % p
            b_value = (v[x] + dot(rows[x], beta, p)) % p
            need(minor_u == delta * a_value % p, "u bordered minor")
            need(minor_v == delta * b_value % p, "v bordered minor")
            if minor_u == 0 and minor_v == 0:
                common_zero.append(x)
            else:
                minor_support.append(x)
                if minor_v:
                    moving_map[x] = (-minor_u * pow(minor_v, -1, p)) % p

        multiplicity_slopes = tuple(
            eta
            for eta in sorted(graph_points)
            if all(errors[eta][x] == 0 for x in basis)
        )
        line_slopes = tuple(
            eta
            for eta in sorted(graph_points)
            if graph_points[eta]
            == vector_add(alpha, vector_scale(beta, eta, p), p)
        )
        need(multiplicity_slopes == line_slopes, "basis-to-line slopes")
        need(set(basis).issubset(common_zero), "basis inside common zero")
        record = {
            "basis": list(basis),
            "basis_determinant": delta,
            "alpha": list(alpha),
            "beta": list(beta),
            "common_zero": common_zero,
            "complement": minor_support,
            "J_B": len(line_slopes),
            "selected_slopes": list(line_slopes),
        }
        basis_records.append(record)
        if len(line_slopes) > threshold:
            key = (alpha, beta)
            line = rich_lines.setdefault(
                key,
                {
                    "alpha": list(alpha),
                    "beta": list(beta),
                    "selected_slopes": list(line_slopes),
                    "J_L": len(line_slopes),
                    "bases": [],
                    "common_zero": common_zero,
                    "complement": minor_support,
                },
            )
            need(line["selected_slopes"] == list(line_slopes), "line slopes")
            need(line["common_zero"] == common_zero, "line common zero")
            line["bases"].append(list(basis))

    line_weighted = sum(
        len(line["bases"]) * (line["J_L"] - threshold)
        for line in rich_lines.values()
    )
    basis_weighted = sum(
        max(record["J_B"] - threshold, 0) for record in basis_records
    )
    need(line_weighted == basis_weighted, "weighted atlas transform")
    need(line_weighted > 0, "nontrivial weighted atlas")
    maximum_multiplicity = max(record["J_B"] for record in basis_records)
    richness_tail = {
        level: sum(record["J_B"] >= level for record in basis_records)
        for level in range(threshold + 1, maximum_multiplicity + 1)
    }
    need(
        sum(richness_tail.values()) == basis_weighted,
        "basis richness layer cake",
    )

    source = (9, 10, 11)
    shortening_checks = 0
    for record in basis_records:
        if record["J_B"] <= threshold:
            continue
        basis = set(record["basis"])
        common_zero = set(record["common_zero"])
        complement = set(record["complement"])
        need(basis.issubset(common_zero), "shortening basis")
        shortened_carrier = set(carrier) - basis
        shortened_zero = common_zero - basis
        need(
            shortened_zero | complement == shortened_carrier,
            "shortened partition union",
        )
        need(
            shortened_zero.isdisjoint(complement),
            "shortened partition disjointness",
        )
        loc_v = locator(carrier, p)
        loc_z = locator(common_zero, p)
        loc_y = locator(complement, p)
        loc_vb = locator(shortened_carrier, p)
        loc_zb = locator(shortened_zero, p)
        for h in source:
            values = {
                "V": evaluate(loc_v, h, p),
                "Z": evaluate(loc_z, h, p),
                "Y": evaluate(loc_y, h, p),
                "VB": evaluate(loc_vb, h, p),
                "ZB": evaluate(loc_zb, h, p),
            }
            need(all(values.values()), "source locator unit")
            need(values["Z"] * values["Y"] % p == values["V"], "ZY=V")
            need(
                values["ZB"] * values["Y"] % p == values["VB"],
                "shortened ZY=V",
            )
            need(
                pow(values["Z"], -1, p)
                == values["Y"] * pow(values["V"], -1, p) % p,
                "original inverse identity",
            )
            need(
                pow(values["ZB"], -1, p)
                == values["Y"] * pow(values["VB"], -1, p) % p,
                "shortened inverse identity",
            )
        shortening_checks += 1
    need(shortening_checks > 0, "shortening coverage")

    histogram: dict[int, int] = defaultdict(int)
    for record in basis_records:
        histogram[record["J_B"]] += 1

    return {
        "field": p,
        "carrier_size": len(carrier),
        "matroid_rank": rank,
        "independent_basis_count": len(bases),
        "selected_slope_count": len(graph_points),
        "rich_threshold": threshold,
        "rich_line_count": len(rich_lines),
        "line_weighted_excess": line_weighted,
        "basis_weighted_excess": basis_weighted,
        "basis_multiplicity_histogram": {
            str(key): histogram[key] for key in sorted(histogram)
        },
        "basis_richness_tail": {
            str(key): richness_tail[key] for key in sorted(richness_tail)
        },
        "basis_richness_layer_cake": sum(richness_tail.values()),
        "shortened_locator_records_checked": shortening_checks,
        "bordered_minor_identities": True,
        "basis_to_line_bijection": True,
        "shortened_locator_identity": True,
    }


def source_coupled_f17_census() -> dict[str, Any]:
    """Exhaust a small source/locator row with an actual RS K0 subspace."""

    p = 17
    degree = 2
    j = 6
    source_size = 2 * degree
    sigma = list(range(source_size))
    carrier = list(range(source_size, 2 * (degree + j)))
    zero_size = j - 1
    rank_k0 = degree + 2
    rich_threshold = 2

    vandermonde = [
        [pow(point, exponent, p) for exponent in range(source_size)]
        for point in sigma
    ]
    inverse_vandermonde = inverse_matrix(vandermonde, p)
    high_rows = inverse_vandermonde[degree + 1 :]
    sigma_locator = locator(sigma, p)
    rows = {
        x: tuple(
            evaluate(sigma_locator, x, p) * pow(x, exponent, p) % p
            for exponent in range(rank_k0)
        )
        for x in carrier
    }
    canonical_basis = tuple(carrier[:rank_k0])
    canonical_inverse = inverse_matrix(
        [list(rows[x]) for x in canonical_basis], p
    )
    bases = list(itertools.combinations(carrier, rank_k0))
    need(
        all(determinant([list(rows[x]) for x in basis], p) for basis in bases),
        "F17 K0 is MDS",
    )

    carrier_set = set(carrier)
    carrier_locator = locator(carrier, p)
    carrier_values = [evaluate(carrier_locator, h, p) for h in sigma]
    locator_records = []
    for zero in itertools.combinations(carrier, zero_size):
        zero_set = set(zero)
        complement = tuple(sorted(carrier_set - zero_set))
        zero_locator = locator(zero, p)
        complement_locator = locator(complement, p)
        zero_values = [evaluate(zero_locator, h, p) for h in sigma]
        complement_values = [
            evaluate(complement_locator, h, p) for h in sigma
        ]
        locator_records.append(
            {
                "zero": zero,
                "complement": complement,
                "zero_locator": zero_locator,
                "zero_values": zero_values,
                "complement_values": complement_values,
            }
        )

    source_cases = residue.structured_pairs(p, degree, carrier)
    rng = random.Random(0x4F55544C494552)
    for index in range(32):
        left, right = residue.random_pair(rng, p, degree)
        source_cases.append((f"random_{index:02d}", left, right))

    case_results = []
    for case_index, (name, left, right) in enumerate(source_cases):
        base = locator_records[
            (case_index * 104729 + degree * 8191 + j * 127)
            % len(locator_records)
        ]
        epsilon_0 = [
            base["zero_values"][index] * evaluate(left, h, p) % p
            for index, h in enumerate(sigma)
        ]
        epsilon_1 = [
            base["zero_values"][index] * evaluate(right, h, p) % p
            for index, h in enumerate(sigma)
        ]

        primitive_lines = []
        for record in locator_records:
            inverse_zero = [pow(value, -1, p) for value in record["zero_values"]]
            quotient_0_values = [
                epsilon_0[index] * inverse_zero[index] % p
                for index in range(source_size)
            ]
            quotient_1_values = [
                epsilon_1[index] * inverse_zero[index] % p
                for index in range(source_size)
            ]
            coefficients_0 = matrix_vector(
                inverse_vandermonde, quotient_0_values, p
            )
            coefficients_1 = matrix_vector(
                inverse_vandermonde, quotient_1_values, p
            )
            if any(
                value
                for value in matrix_vector(high_rows, quotient_0_values, p)
                + matrix_vector(high_rows, quotient_1_values, p)
            ):
                continue
            reduced_0 = trim(coefficients_0[: degree + 1])
            reduced_1 = trim(coefficients_1[: degree + 1])
            if residue.gcd_poly(reduced_0, reduced_1, p) != [1]:
                continue
            if max(len(reduced_0), len(reduced_1)) - 1 != degree:
                continue
            polynomial_0 = mul(record["zero_locator"], reduced_0, p)
            polynomial_1 = mul(record["zero_locator"], reduced_1, p)
            a = {x: (-evaluate(polynomial_0, x, p)) % p for x in carrier}
            b = {x: (-evaluate(polynomial_1, x, p)) % p for x in carrier}
            common_zero = tuple(
                x for x in carrier if a[x] == 0 and b[x] == 0
            )
            need(common_zero == record["zero"], "primitive common zero")
            primitive_lines.append(
                {
                    "zero": record["zero"],
                    "complement": record["complement"],
                    "a": a,
                    "b": b,
                }
            )

        primitive_lines.sort(key=lambda item: item["complement"])
        if not primitive_lines:
            continue
        u = primitive_lines[0]["a"]
        v = primitive_lines[0]["b"]
        for line in primitive_lines:
            difference_a = [
                (line["a"][x] - u[x]) % p for x in canonical_basis
            ]
            difference_b = [
                (line["b"][x] - v[x]) % p for x in canonical_basis
            ]
            alpha = tuple(
                matrix_vector(canonical_inverse, difference_a, p)
            )
            beta = tuple(
                matrix_vector(canonical_inverse, difference_b, p)
            )
            for x in carrier:
                need(
                    vector_add((u[x],), (dot(rows[x], alpha, p),), p)[0]
                    == line["a"][x],
                    "source-coupled alpha representation",
                )
                need(
                    vector_add((v[x],), (dot(rows[x], beta, p),), p)[0]
                    == line["b"][x],
                    "source-coupled beta representation",
                )
            line["alpha"] = alpha
            line["beta"] = beta
            line["slope_values"] = sorted(
                {
                    (-line["a"][x] * pow(line["b"][x], -1, p)) % p
                    for x in line["complement"]
                    if line["b"][x]
                }
            )

        candidates_by_slope: dict[int, list[int]] = defaultdict(list)
        for line_index, line in enumerate(primitive_lines):
            for eta in line["slope_values"]:
                candidates_by_slope[eta].append(line_index)

        selected = []
        selected_by_line: dict[int, list[int]] = defaultdict(list)
        for eta in sorted(candidates_by_slope):
            line_index = min(
                candidates_by_slope[eta],
                key=lambda index: primitive_lines[index]["complement"],
            )
            line = primitive_lines[line_index]
            zeta = vector_add(
                line["alpha"], vector_scale(line["beta"], eta, p), p
            )
            error = {
                x: (u[x] + eta * v[x] + dot(rows[x], zeta, p)) % p
                for x in carrier
            }
            selected.append(
                {
                    "eta": eta,
                    "line_index": line_index,
                    "zeta": zeta,
                    "error": error,
                }
            )
            selected_by_line[line_index].append(eta)

        basis_multiplicities = {}
        admitted_rich_bases = 0
        rich_basis_lines: dict[
            tuple[tuple[int, ...], tuple[int, ...]], dict[str, Any]
        ] = {}
        primitive_complements = {
            line["complement"] for line in primitive_lines
        }
        for basis in bases:
            multiplicity = sum(
                all(record["error"][x] == 0 for x in basis)
                for record in selected
            )
            basis_multiplicities[basis] = multiplicity
            if multiplicity <= rich_threshold:
                continue
            alpha, beta = basis_line(basis, rows, u, v, p)
            common_zero = tuple(
                x
                for x in carrier
                if (u[x] + dot(rows[x], alpha, p)) % p == 0
                and (v[x] + dot(rows[x], beta, p)) % p == 0
            )
            complement = tuple(x for x in carrier if x not in common_zero)
            need(set(basis).issubset(common_zero), "rich basis common zero")
            line_slopes = tuple(
                record["eta"]
                for record in selected
                if record["zeta"]
                == vector_add(alpha, vector_scale(beta, record["eta"], p), p)
            )
            need(len(line_slopes) == multiplicity, "rich basis line slopes")
            key = (alpha, beta)
            previous = rich_basis_lines.setdefault(
                key,
                {
                    "common_zero": common_zero,
                    "complement": complement,
                    "selected_slopes": line_slopes,
                    "J": multiplicity,
                },
            )
            need(previous["common_zero"] == common_zero, "rich line zero")
            need(previous["selected_slopes"] == line_slopes, "rich line slopes")
            if (
                len(complement) == j + 1
                and complement in primitive_complements
            ):
                admitted_rich_bases += 1

        line_weighted = 0
        for line in rich_basis_lines.values():
            beta_mass = sum(
                set(basis).issubset(line["common_zero"]) for basis in bases
            )
            line_weighted += beta_mass * (line["J"] - rich_threshold)
        basis_weighted = sum(
            max(value - rich_threshold, 0)
            for value in basis_multiplicities.values()
        )
        need(line_weighted == basis_weighted, "F17 weighted atlas")
        maximum_multiplicity = max(basis_multiplicities.values(), default=0)
        tail_sum = sum(
            sum(value >= level for value in basis_multiplicities.values())
            for level in range(rich_threshold + 1, maximum_multiplicity + 1)
        )
        need(tail_sum == basis_weighted, "F17 layer cake")
        case_results.append(
            {
                "case": name,
                "primitive_source_lines": len(primitive_lines),
                "selected_slopes": len(selected),
                "rich_selected_lines": sum(
                    len(slopes) > rich_threshold
                    for slopes in selected_by_line.values()
                ),
                "admitted_rich_bases": admitted_rich_bases,
                "basis_count": len(bases),
                "maximum_basis_multiplicity": maximum_multiplicity,
                "weighted_excess": basis_weighted,
            }
        )

    need(case_results, "F17 source-coupled cases")
    maximum_admitted = max(
        case_results, key=lambda item: item["admitted_rich_bases"]
    )
    maximum_weighted = max(
        case_results, key=lambda item: item["weighted_excess"]
    )
    maximum_multiplicity = max(
        case_results, key=lambda item: item["maximum_basis_multiplicity"]
    )
    return {
        "field": p,
        "source_size": len(sigma),
        "carrier_size": len(carrier),
        "K0_rank": rank_k0,
        "K0_basis_count": len(bases),
        "source_cases_checked": len(case_results),
        "canonical_selector_rule": "LEXICOGRAPHIC_COMPLEMENT_PER_SLOPE",
        "maximum_admitted_rich_basis_case": maximum_admitted,
        "maximum_weighted_excess_case": maximum_weighted,
        "maximum_basis_multiplicity_case": maximum_multiplicity,
        "all_weighted_atlas_identities": True,
        "all_layer_cake_identities": True,
        "all_source_coset_representations": True,
    }


def deployed_arithmetic() -> dict[str, int]:
    j = 981_104
    e = 67_472
    carrier_size = 2 * j
    basis_floor = math.comb(e + 8, 8)
    ambient_eight_subsets = math.comb(carrier_size, 8)
    active_excess_allowance = (
        (active.REMAINING + 1) * basis_floor
        - 20 * ambient_eight_subsets
        - 1
    )
    line_multiplicity_cap = j + 1
    admitted_basis_cardinality_cap = (
        active_excess_allowance // (line_multiplicity_cap - 20)
    )
    admitted_basis_exclusion_floor = (
        ambient_eight_subsets - admitted_basis_cardinality_cap
    )
    coarse_tail_cut = 537_696
    coarse_tail_remainder = (
        active_excess_allowance
        - (coarse_tail_cut - 20) * ambient_eight_subsets
    )
    high_richness_basis_cap = (
        coarse_tail_remainder
        // (line_multiplicity_cap - coarse_tail_cut)
    )
    need(active_excess_allowance >= 0, "positive active excess allowance")
    need(
        20 * ambient_eight_subsets + active_excess_allowance
        == (active.REMAINING + 1) * basis_floor - 1,
        "active excess normalization",
    )
    need(
        admitted_basis_cardinality_cap * (line_multiplicity_cap - 20)
        <= active_excess_allowance
        < (admitted_basis_cardinality_cap + 1)
        * (line_multiplicity_cap - 20),
        "admitted basis cardinality cap",
    )
    need(coarse_tail_remainder >= 0, "coarse tail remainder")
    need(
        (coarse_tail_cut - 20) * ambient_eight_subsets
        + (line_multiplicity_cap - coarse_tail_cut)
        * high_richness_basis_cap
        <= active_excess_allowance
        < (coarse_tail_cut - 20) * ambient_eight_subsets
        + (line_multiplicity_cap - coarse_tail_cut)
        * (high_richness_basis_cap + 1),
        "high richness basis cap",
    )
    return {
        "r": 67_471,
        "x": 1,
        "source_size": 2 * e,
        "carrier_size": carrier_size,
        "basis_rank": 8,
        "basis_incidence_floor_per_slope": basis_floor,
        "ambient_eight_subset_count": ambient_eight_subsets,
        "active_excess_allowance": active_excess_allowance,
        "active_excess_allowance_quotient_by_ambient_subsets": (
            active_excess_allowance // ambient_eight_subsets
        ),
        "line_multiplicity_cap": line_multiplicity_cap,
        "admitted_basis_cardinality_sufficient_cap": (
            admitted_basis_cardinality_cap
        ),
        "ambient_basis_exclusion_sufficient_floor": (
            admitted_basis_exclusion_floor
        ),
        "coarse_tail_cut": coarse_tail_cut,
        "coarse_tail_remainder": coarse_tail_remainder,
        "high_richness_basis_sufficient_cap": high_richness_basis_cap,
        "active_compiler_average_multiplicity_floor": (
            ((active.REMAINING + 1) * basis_floor - 1)
            // ambient_eight_subsets
        ),
        "shortened_carrier_size": carrier_size - 8,
        "complement_locator_degree": j + 1,
        "shortened_zero_locator_degree": j - 9,
        "source_residue_dimension": 2,
        "cylinder_projective_dimension": j + 3 - 2 * e,
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
                "independent_basis_reconstructs_unique_graph_line": True,
                "bordered_minors_reconstruct_common_zero_set": True,
                "basis_is_contained_in_common_zero_set": True,
                "line_weighted_excess_equals_basis_weighted_excess": True,
                "each_basis_has_at_most_one_rich_line": True,
                "eight_shortened_locator_identity": True,
                "source_residue_test_unchanged_under_shortening": True,
                "active_excess_allowance_is_exact": True,
                "active_excess_gate_implies_slope_budget": True,
                "basis_richness_layer_cake_is_exact": True,
                "cardinality_only_sufficient_gate_is_exact": True,
                "high_richness_tail_sufficient_gate_is_exact": True,
                "determinant_mass_paid": False,
            },
            "deployed_arithmetic": deployed_arithmetic(),
            "finite_model": finite_model(),
            "source_coupled_f17_census": source_coupled_f17_census(),
            "source_bindings": source_bindings(),
            "status": (
                "PROVED_OUTLIER_BASIS_RESIDUE_TRANSFORM_"
                "WEIGHTED_INCIDENCE_OPEN_ROW_OPEN"
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
        "title": "KoalaBear first-gap outlier-basis/residue transform",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED OUTLIER-BASIS/RESIDUE TRANSFORM",
        "\\boxed{B\\subseteq Z_B.}",
        "\\sum_{B\\in\\mathcal B(K_0)}(J_B-20)_+",
        "Selected-basis source-residue packing",
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
    need(certificate == expected, "certificate differs from exact replay")
    need(schema == expected_schema_value, "schema differs from exact replay")
    need(
        certificate["active_ledger"]["additional_charge"] == 0,
        "zero ledger movement",
    )
    need(
        certificate["theorem"]["determinant_mass_paid"] is False,
        "open determinant status",
    )
    need(
        certificate["finite_model"]["line_weighted_excess"]
        == certificate["finite_model"]["basis_weighted_excess"],
        "finite weighted identity",
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
            "independent_basis_reconstructs_unique_graph_line", False
        ),
        lambda data: data["theorem"].__setitem__(
            "bordered_minors_reconstruct_common_zero_set", False
        ),
        lambda data: data["theorem"].__setitem__(
            "line_weighted_excess_equals_basis_weighted_excess", False
        ),
        lambda data: data["theorem"].__setitem__(
            "eight_shortened_locator_identity", False
        ),
        lambda data: data["deployed_arithmetic"].__setitem__(
            "shortened_carrier_size", 1_962_201
        ),
        lambda data: data["deployed_arithmetic"].__setitem__(
            "active_excess_allowance",
            data["deployed_arithmetic"]["active_excess_allowance"] + 1,
        ),
        lambda data: data["finite_model"].__setitem__(
            "basis_weighted_excess",
            data["finite_model"]["basis_weighted_excess"] + 1,
        ),
        lambda data: data["finite_model"].__setitem__(
            "basis_richness_layer_cake",
            data["finite_model"]["basis_richness_layer_cake"] + 1,
        ),
        lambda data: data["finite_model"].__setitem__(
            "shortened_locator_identity", False
        ),
        lambda data: data["source_coupled_f17_census"].__setitem__(
            "all_source_coset_representations", False
        ),
        lambda data: data["active_ledger"].__setitem__("additional_charge", 1),
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
    model = certificate["finite_model"]
    coupled = certificate["source_coupled_f17_census"]
    arithmetic = certificate["deployed_arithmetic"]
    print(f"architecture: {certificate['architecture_id']}")
    print(f"partition_sha256: {certificate['partition_sha256']}")
    print(
        "deployed first gap: "
        f"carrier={arithmetic['carrier_size']} "
        f"shortened={arithmetic['shortened_carrier_size']} "
        f"residue_dim={arithmetic['source_residue_dimension']}"
    )
    print(
        "active excess gate: "
        f"E20<={arithmetic['active_excess_allowance']} "
        "avg_excess_floor="
        f"{arithmetic['active_excess_allowance_quotient_by_ambient_subsets']}"
    )
    print(
        "sufficient basis gates: "
        "admitted<="
        f"{arithmetic['admitted_basis_cardinality_sufficient_cap']} "
        f"J>{arithmetic['coarse_tail_cut']} bases<="
        f"{arithmetic['high_richness_basis_sufficient_cap']}"
    )
    print(
        "finite transform: "
        f"bases={model['independent_basis_count']} "
        f"rich_lines={model['rich_line_count']} "
        f"line_sum={model['line_weighted_excess']} "
        f"basis_sum={model['basis_weighted_excess']}"
    )
    print(
        "source-coupled F17: "
        f"cases={coupled['source_cases_checked']} "
        "max_admitted="
        f"{coupled['maximum_admitted_rich_basis_case']['admitted_rich_bases']}"
        f"/{coupled['K0_basis_count']} "
        "max_weighted="
        f"{coupled['maximum_weighted_excess_case']['weighted_excess']} "
        "max_J="
        f"{coupled['maximum_basis_multiplicity_case']['maximum_basis_multiplicity']}"
    )
    print(f"payload_sha256: {certificate['payload_sha256']}")


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
            certificate = load(CERT_PATH)
            schema = load(SCHEMA_PATH)
            validate(certificate, schema)
            print_summary(certificate)
            print("check: PASS")
        if args.tamper_selftest:
            tamper_selftest()
        if not (args.emit or args.check or args.tamper_selftest):
            parser.error("choose --emit, --check, or --tamper-selftest")
    except (Failure, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
