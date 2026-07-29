#!/usr/bin/env sage
# REJECTED: omits the actual K_0/GRS minimum-distance condition.
"""Independent Sage replay of the KoalaBear circuit-only route cut."""

from itertools import combinations
from pathlib import Path
import copy
import hashlib
import json
import math


class VerificationError(RuntimeError):
    pass


CHECKS = 0


def need(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-equality-wall-circuit-only-route-cut-v1/certificate.json"
)

P = 2130706433
V_SIZE = 1894736
J = 981105
Z = V_SIZE - J
C = 67472
MULTIPLICITY = 5274
COMMON_ONE = 141
COMMON_ZERO = 544451
INDICES = tuple(range(68)) + (128,)
BASIS = (1, 2, 4, 8, 16, 32, 64, 128)
F = GF(P)


def sign_vector(index):
    return vector(
        F,
        [
            -1 if ((index >> coordinate) & 1) else 1
            for coordinate in range(8)
        ],
    )


def values(index):
    vertex = sign_vector(index)
    return tuple(
        ZZ(vertex.dot_product(sign_vector(coordinate_type)))
        for coordinate_type in range(256)
    )


def affine_rank(indices):
    base = sign_vector(indices[0])
    rows = [sign_vector(index) - base for index in indices[1:]]
    if not rows:
        return 0
    return matrix(F, rows).rank()


def payload_digest(document):
    unsigned = copy.deepcopy(document)
    unsigned.pop("payload_sha256", None)
    raw = (
        json.dumps(unsigned, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main():
    document = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    need(
        document["schema"]
        == "rs-mca-kb-v4-equality-wall-circuit-only-route-cut-v1",
        "schema",
    )
    need(
        document["status"] == "PROVED_CIRCUIT_ONLY_ROUTE_CUT_ROW_OPEN",
        "status",
    )
    need(document["payload_sha256"] == payload_digest(document), "payload")

    need(len(INDICES) == 69 and len(set(INDICES)) == 69, "vertices")
    need(256 * MULTIPLICITY + COMMON_ONE + COMMON_ZERO == V_SIZE, "V")
    need(186 * MULTIPLICITY + COMMON_ONE == J, "J")
    need(70 * MULTIPLICITY + COMMON_ZERO == Z, "Z")

    all_values = {index: values(index) for index in INDICES}
    zero_sets = {}
    for index in INDICES:
        zero_set = frozenset(
            coordinate_type
            for coordinate_type, value in enumerate(all_values[index])
            if value == 0
        )
        need(len(zero_set) == binomial(8, 4) == 70, "zero types")
        zero_sets[index] = zero_set

    root = sign_vector(0)
    full_differences = [sign_vector(index) - root for index in INDICES[1:]]
    need(matrix(F, full_differences).rank() == 8, "affine rank")
    need(affine_rank((0,) + BASIS) == 8, "basis rank")

    evaluation_rows = []
    for basis_index in BASIS:
        evaluation_rows.append(
            vector(
                F,
                [
                    left - right
                    for left, right in zip(
                        all_values[basis_index],
                        all_values[0],
                        strict=True,
                    )
                ],
            )
        )
    need(matrix(F, evaluation_rows).rank() == 8, "evaluation rank")

    exchange_histogram = {}
    distance_histogram = {}
    minimum_exchange = V_SIZE
    for left, right in combinations(INDICES, 2):
        distance = (left ^^ right).bit_count()
        need(1 <= distance <= 7, "pair distance")
        intersection = len(zero_sets[left] & zero_sets[right])
        if distance % 2:
            formula = 0
        else:
            formula = (
                binomial(distance, distance // 2)
                * binomial(8 - distance, 4 - distance // 2)
            )
        need(intersection == formula, "intersection formula")
        directed_types = len(zero_sets[left] - zero_sets[right])
        need(
            directed_types == len(zero_sets[right] - zero_sets[left]),
            "directed symmetry",
        )
        exchange = directed_types * MULTIPLICITY
        need(exchange >= C, "exchange floor")
        minimum_exchange = min(minimum_exchange, exchange)
        exchange_histogram[directed_types] = (
            exchange_histogram.get(directed_types, 0) + 1
        )
        distance_histogram[distance] = distance_histogram.get(distance, 0) + 1

    need(
        exchange_histogram == {70: 1190, 30: 575, 34: 581},
        "exchange histogram",
    )
    need(minimum_exchange == 158220, "minimum exchange")

    triangle_count = 0
    for triple in combinations(INDICES, 3):
        if affine_rank(triple) < 2:
            triangle_count += 1
    need(triangle_count == 0, "no triangles")

    nonbasis = [
        index for index in INDICES[1:] if index not in set(BASIS)
    ]
    need(len(nonbasis) == 60, "60 nonbasis vertices")
    circuit_histogram = {}
    for index in nonbasis:
        basis_vertices = tuple(
            1 << coordinate
            for coordinate in range(8)
            if ((index >> coordinate) & 1)
        )
        weight = len(basis_vertices)
        vertices = (0,) + basis_vertices + (index,)
        coefficients = {0: weight - 1, index: 1}
        coefficients.update({basis_vertex: -1 for basis_vertex in basis_vertices})
        need(sum(coefficients[vertex] for vertex in vertices) == 0, "affine sum")
        relation = sum(
            F(coefficients[vertex]) * sign_vector(vertex)
            for vertex in vertices
        )
        need(relation == vector(F, 8, 0), "vertex relation")
        size = len(vertices)
        need(affine_rank(vertices) == size - 2, "circuit rank")
        for deleted in range(size):
            subset = vertices[:deleted] + vertices[deleted + 1 :]
            need(affine_rank(subset) == len(subset) - 1, "minimal circuit")

        common_zero_types = 0
        for coordinate_type in range(256):
            coordinate_values = [
                all_values[vertex][coordinate_type] for vertex in vertices
            ]
            need(
                sum(
                    coefficients[vertex] * value
                    for vertex, value in zip(
                        vertices, coordinate_values, strict=True
                    )
                )
                == 0,
                "evaluation relation",
            )
            occupied = sum(value != 0 for value in coordinate_values)
            need(occupied != 1, "no singleton")
            common_zero_types += occupied == 0
        need(common_zero_types == 0, "no sign common-zero type")
        need(0 <= 10 - size, "restriction rank bound")
        circuit_histogram[size] = circuit_histogram.get(size, 0) + 1

    need(
        circuit_histogram == {4: 17, 5: 21, 6: 15, 7: 6, 8: 1},
        "circuit histogram",
    )

    results = document["exact_results"]
    need(results["record_count"] == 69, "certificate records")
    need(results["affine_rank"] == 8, "certificate rank")
    need(
        results["canonical_star_basis_indices"] == list(BASIS),
        "certificate basis",
    )
    need(
        results["canonical_nonbasis_circuit_count"] == 60,
        "certificate circuits",
    )
    need(
        results["canonical_circuit_size_histogram"]
        == {"4": 17, "5": 21, "6": 15, "7": 6, "8": 1},
        "certificate circuit histogram",
    )
    need(
        results["pair_exchange_type_histogram"]
        == {"30": 575, "34": 581, "70": 1190},
        "certificate exchange histogram",
    )
    need(results["minimum_directed_exchange"] == 158220, "certificate minimum")
    need(
        document["route_cut"]["full_primitive_69_point_theorem_refuted"]
        is False,
        "full theorem remains open",
    )
    need(document["closure_state"]["additional_charge"] == 0, "zero charge")
    need(document["closure_state"]["row_closed"] is False, "row open")

    print("PASS: independent Sage circuit-only route-cut replay")
    print(f"checks={CHECKS}")
    print("records=69")
    print("affine_rank=8")
    print("canonical_circuits=60")
    print("minimum_directed_exchange=158220")
    print("ledger_movement=0")


try:
    main()
except (OSError, ValueError, KeyError, VerificationError) as exc:
    print(f"FAIL: {exc}")
    raise SystemExit(1)
