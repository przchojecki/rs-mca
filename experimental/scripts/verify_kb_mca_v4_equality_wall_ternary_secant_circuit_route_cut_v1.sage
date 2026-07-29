#!/usr/bin/env sage
"""Independent Sage replay of the KoalaBear ternary-secant route cut."""

from itertools import combinations, product
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
    "kb-mca-v4-equality-wall-ternary-secant-circuit-route-cut-v1/"
    "certificate.json"
)

P = 2130706433
N = 1894736
J = 981105
Z = N - J
GRS_DISTANCE = 1048577
EXCHANGE_FLOOR = GRS_DISTANCE - J
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


def affine_rank(indices):
    root = sign_vector(indices[0])
    rows = [sign_vector(index) - root for index in indices[1:]]
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


def reject_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite_constant(value):
    raise VerificationError(f"nonfinite JSON constant: {value}")


def main():
    raw = CERTIFICATE.read_bytes()
    document = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=reject_duplicate_pairs,
        parse_constant=reject_nonfinite_constant,
    )
    canonical = (
        json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    need(raw == canonical, "canonical JSON bytes")
    need(
        document["schema"]
        == "rs-mca-kb-v4-equality-wall-ternary-secant-circuit-route-cut-v1",
        "schema",
    )
    need(
        document["status"]
        == "PROVED_TERNARY_SECANT_CIRCUIT_ROUTE_CUT_ROW_OPEN",
        "status",
    )
    need(document["architecture_id"] is None, "abstract architecture is null")
    need(document["partition_sha256"] is None, "abstract partition is null")
    need(document["payload_sha256"] == payload_digest(document), "payload")
    need(len(INDICES) == 69 and len(set(INDICES)) == 69, "vertices")

    row = document["row_contract"]
    need(row["agreement"] == 1116048, "row agreement")
    need(row["row_length"] == 2097152, "row length")
    need(row["code_dimension"] == 1048576, "row dimension")
    need(row["B_star"] == 274980728111395087, "row budget")
    need(row["field_base_prime"] == P, "row prime")
    need(row["field_extension_degree"] == 6, "row extension degree")
    need(row["active_U_paid"] is None, "active U_paid null")
    need(row["active_partition_sha256"] is None, "active partition null")

    profile = document["abstract_carrier_profile"]
    need(profile["carrier_size"] == N, "abstract carrier size")
    need(profile["locator_degree"] == J, "abstract locator degree")
    need(profile["zero_count"] == Z, "abstract zero count")
    need(
        profile["shortened_grs_minimum_distance"] == GRS_DISTANCE,
        "distance target",
    )
    need(
        profile["minimum_pair_exchange"] == GRS_DISTANCE - J,
        "exchange target",
    )
    need(profile["candidate_record_count"] == 69, "record target")
    need(
        document["construction"]["scalar_extension"]
        == (
            "F_P_VALUES_VIEWED_IN_F_P6_PRESERVE_HAMMING_WEIGHT_AND_"
            "BASE_FIELD_RANK"
        ),
        "scalar-extension declaration",
    )

    rows = document["exact_results"]["coordinate_types"]
    need(len(rows) == 225, "coordinate types")
    witness = []
    seen = set()
    for row in rows:
        need(set(row) == {"normal", "offset", "multiplicity"}, "row keys")
        normal_raw = tuple(ZZ(value) for value in row["normal"])
        normal = vector(F, normal_raw)
        offset = ZZ(row["offset"])
        multiplicity = ZZ(row["multiplicity"])
        need(len(normal) == 8, "normal length")
        need(all(value in (-1, 0, 1) for value in normal), "normal entries")
        need(-8 <= offset <= 8 or offset == 99, "offset declaration")
        need(multiplicity > 0, "multiplicity")
        if any(normal_raw):
            need(
                next(value for value in normal_raw if value) == 1,
                "normalized normal",
            )
            occupied = any(
                sign_vector(index).dot_product(normal) == F(offset)
                for index in INDICES
            )
            need(occupied or offset == 99, "occupied or empty level")
        else:
            need(offset == 0, "zero normal common-zero level")
        need((normal_raw, offset) not in seen, "distinct type")
        seen.add((normal_raw, offset))
        witness.append((normal, F(offset), multiplicity))
    need(sum(multiplicity for _, _, multiplicity in witness) == N, "length")

    values = {}
    for index in INDICES:
        vertex = sign_vector(index)
        values[index] = tuple(
            vertex.dot_product(normal) - offset
            for normal, offset, _ in witness
        )
        zero_count = sum(
            multiplicity
            for value, (_, _, multiplicity) in zip(
                values[index], witness, strict=True
            )
            if value == 0
        )
        need(zero_count == Z, "constant zero count")

    need(affine_rank(INDICES) == 8, "affine rank")
    need(affine_rank((0,) + BASIS) == 8, "basis rank")
    secant_rows = [
        vector(
            F,
            [
                left - right
                for left, right in zip(
                    values[index], values[0], strict=True
                )
            ],
        )
        for index in BASIS
    ]
    need(matrix(F, secant_rows).rank() == 8, "secant rank")
    need(
        matrix(
            F,
            [vector(F, values[index]) for index in INDICES],
        ).rank()
        == 9,
        "full function rank",
    )

    minimum_distance = N
    maximum_pair_zero = 0
    minimum_exchange = N
    maximum_exchange = 0
    pair_count = 0
    for left, right in combinations(INDICES, 2):
        pair_count += 1
        pair_zero = 0
        left_only = 0
        right_only = 0
        common_zero = 0
        for left_value, right_value, (_, _, multiplicity) in zip(
            values[left], values[right], witness, strict=True
        ):
            pair_zero += multiplicity * (left_value == right_value)
            left_nonzero = left_value != 0
            right_nonzero = right_value != 0
            left_only += multiplicity * (left_nonzero and not right_nonzero)
            right_only += multiplicity * (right_nonzero and not left_nonzero)
            common_zero += multiplicity * (
                not left_nonzero and not right_nonzero
            )
        need(left_only == right_only, "directed exchange")
        need(common_zero + left_only == Z, "zero decomposition")
        distance = N - pair_zero
        need(distance >= GRS_DISTANCE, "selected-pair distance threshold")
        need(left_only >= EXCHANGE_FLOOR, "exchange floor")
        need(distance <= J + left_only, "union support")
        minimum_distance = min(minimum_distance, distance)
        maximum_pair_zero = max(maximum_pair_zero, pair_zero)
        minimum_exchange = min(minimum_exchange, left_only)
        maximum_exchange = max(maximum_exchange, left_only)
    need(pair_count == binomial(69, 2) == 2346, "pair count")
    need(maximum_pair_zero == 840990, "maximum pair zero")
    need(minimum_distance == 1053746, "minimum pair distance")
    need(minimum_exchange == 121284, "minimum exchange")
    need(maximum_exchange == 616161, "maximum exchange")

    normal_weights = {}
    for normal, _, multiplicity in witness:
        key = tuple(
            ZZ(value) if ZZ(value) <= 1 else ZZ(value) - P
            for value in normal
        )
        normal_weights[key] = normal_weights.get(key, 0) + multiplicity
    ternary_rows = []
    maximum_ternary_zero = 0
    maximum_direction = None
    directions = [
        coefficient
        for coefficient in product((-1, 0, 1), repeat=8)
        if any(coefficient)
        and next(value for value in coefficient if value) == 1
    ]
    need(len(directions) == 3280, "projective ternary directions")
    for coefficient in directions:
        zero_coordinates = sum(
            multiplicity
            for normal, multiplicity in normal_weights.items()
            if sum(
                left * right
                for left, right in zip(coefficient, normal, strict=True)
            )
            % P
            == 0
        )
        need(zero_coordinates <= N - GRS_DISTANCE, "ternary threshold")
        if zero_coordinates > maximum_ternary_zero:
            maximum_ternary_zero = zero_coordinates
            maximum_direction = coefficient
        ternary_rows.append(
            {
                "coefficient": [int(value) for value in coefficient],
                "zero_coordinates": int(zero_coordinates),
                "distance": int(N - zero_coordinates),
            }
        )
    need(maximum_ternary_zero == 841778, "maximum ternary zero")
    need(
        maximum_direction == (1, 0, 0, 0, 0, 0, 0, 1),
        "maximum ternary direction",
    )
    ternary_digest = hashlib.sha256(
        (
            json.dumps(
                ternary_rows, sort_keys=True, separators=(",", ":")
            )
            + "\n"
        ).encode("utf-8")
    ).hexdigest()

    triangle_count = 0
    for triple in combinations(INDICES, 3):
        triangle_count += affine_rank(triple) < 2
    need(triangle_count == 0, "no affine triangles")

    nonbasis = [index for index in INDICES[1:] if index not in set(BASIS)]
    need(len(nonbasis) == 60, "nonbasis count")
    circuit_histogram = {}
    restriction_histogram = {}
    for index in nonbasis:
        basis_vertices = tuple(
            1 << coordinate
            for coordinate in range(8)
            if ((index >> coordinate) & 1)
        )
        weight = len(basis_vertices)
        vertices = (0,) + basis_vertices + (index,)
        coefficients = {0: weight - 1, index: 1}
        coefficients.update(
            {basis_vertex: -1 for basis_vertex in basis_vertices}
        )
        need(
            sum(coefficients[vertex] for vertex in vertices) == 0,
            "coefficient sum",
        )
        relation = sum(
            F(coefficients[vertex]) * sign_vector(vertex)
            for vertex in vertices
        )
        need(relation == vector(F, [0] * 8), "vertex relation")
        size = len(vertices)
        need(affine_rank(vertices) == size - 2, "circuit rank")
        for deleted in range(size):
            subset = vertices[:deleted] + vertices[deleted + 1 :]
            need(
                affine_rank(subset) == len(subset) - 1,
                "circuit minimality",
            )

        common_zero_types = []
        for type_index in range(len(witness)):
            coordinate_values = [
                values[vertex][type_index] for vertex in vertices
            ]
            need(
                sum(
                    F(coefficients[vertex]) * value
                    for vertex, value in zip(
                        vertices, coordinate_values, strict=True
                    )
                )
                == 0,
                "coordinate relation",
            )
            occupied = sum(value != 0 for value in coordinate_values)
            need(occupied != 1, "no singleton")
            if occupied == 0:
                common_zero_types.append(type_index)

        restriction_rows = [
            vector(
                F,
                [
                    values[basis_index][type_index]
                    - values[0][type_index]
                    for type_index in common_zero_types
                ],
            )
            for basis_index in BASIS
        ]
        restriction_rank = matrix(F, restriction_rows).rank()
        need(restriction_rank <= 10 - size, "restriction rank")
        circuit_histogram[size] = circuit_histogram.get(size, 0) + 1
        restriction_histogram[restriction_rank] = (
            restriction_histogram.get(restriction_rank, 0) + 1
        )

    need(
        circuit_histogram == {4: 17, 5: 21, 6: 15, 7: 6, 8: 1},
        "circuit histogram",
    )
    need(
        restriction_histogram == {2: 13, 3: 15, 4: 7, 5: 10, 6: 15},
        "restriction histogram",
    )

    results = document["exact_results"]
    need(results["record_count"] == 69, "certificate records")
    need(results["coordinate_type_count"] == 225, "certificate types")
    need(results["affine_rank"] == 8, "certificate affine rank")
    need(results["secant_rank"] == 8, "certificate secant rank")
    need(results["full_vertex_function_rank"] == 9, "certificate full rank")
    need(
        results["minimum_pair_secant_distance"] == minimum_distance,
        "certificate pair distance",
    )
    need(
        results["minimum_directed_exchange"] == minimum_exchange,
        "certificate exchange",
    )
    need(
        results["canonical_circuit_restriction_rank_histogram"]
        == {"2": 13, "3": 15, "4": 7, "5": 10, "6": 15},
        "certificate restriction histogram",
    )
    need(
        results["projective_ternary_direction_count"] == 3280,
        "certificate ternary count",
    )
    need(
        results["maximum_projective_ternary_zero_coordinates"]
        == maximum_ternary_zero,
        "certificate ternary zero",
    )
    need(
        results["minimum_projective_ternary_secant_distance"]
        == N - maximum_ternary_zero,
        "certificate ternary distance",
    )
    need(
        results["projective_ternary_digest"] == ternary_digest,
        "certificate ternary digest",
    )
    need(
        results["full_secant_span_distance_certified"] is False,
        "full span not certified",
    )
    need(
        document["route_cut"]["actual_grs_subcode_constructed"] is False,
        "GRS embedding absent",
    )
    need(
        document["route_cut"]["full_secant_span_distance_certified"]
        is False,
        "route full span absent",
    )
    need(
        document["route_cut"]["full_primitive_69_point_theorem_refuted"]
        is False,
        "full theorem open",
    )
    need(document["closure_state"]["additional_charge"] == 0, "zero charge")
    need(document["closure_state"]["U_paid_before"] is None, "U_paid null")
    need(document["closure_state"]["U_paid_after"] is None, "U_paid stays null")
    need(
        document["closure_state"]["B_remaining_before"] is None,
        "remaining budget undefined",
    )
    need(
        document["closure_state"]["B_remaining_after"] is None,
        "remaining budget remains undefined",
    )
    need(document["closure_state"]["row_closed"] is False, "row open")

    print("PASS: independent Sage ternary-secant/circuit route-cut replay")
    print(f"checks={CHECKS}")
    print("records=69")
    print("coordinate_types=225")
    print("secant_rank=8")
    print(f"minimum_pair_secant_distance={minimum_distance}")
    print(
        "minimum_projective_ternary_secant_distance="
        f"{N - maximum_ternary_zero}"
    )
    print(f"minimum_directed_exchange={minimum_exchange}")
    print("canonical_circuits=60")
    print("ledger_movement=0")


try:
    main()
except (OSError, ValueError, KeyError, VerificationError) as exc:
    print(f"FAIL: {exc}")
    raise SystemExit(1)
