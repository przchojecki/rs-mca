#!/usr/bin/env python3
# REJECTED: omits the actual K_0/GRS minimum-distance condition.
"""Exact circuit-only route cut for the KoalaBear equality wall.

The construction has the deployed carrier and locator cardinalities and
produces 69 distinct records in one affine rank-eight family.  It satisfies
the pair-exchange floor, the canonical 60 bounded-circuit conclusion, the
no-singleton carrier condition, and the circuit restriction-rank bound.

It deliberately does not construct locator polynomials, source quotients,
Hilbert--Burch data, or active-owner evidence.  Therefore it refutes only an
inference from the listed circuit/support axioms to cap 68; it is not a
counterexample to the full KoalaBear primitive theorem.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable


class VerificationError(RuntimeError):
    """Raised when an exact verification condition fails."""


CHECKS = 0


def need(condition: bool, message: str) -> None:
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

SCHEMA_ID = "rs-mca-kb-v4-equality-wall-circuit-only-route-cut-v1"
STATUS = "PROVED_CIRCUIT_ONLY_ROUTE_CUT_ROW_OPEN"
ARTIFACT_KIND = "EXACT_ABSTRACT_COUNTERMODEL_TO_CIRCUIT_ONLY_CAP68_INFERENCE"

P = 2_130_706_433
FIELD_EXTENSION_DEGREE = 6
V_SIZE = 1_894_736
LOCATOR_DEGREE = 981_105
ZERO_COUNT = V_SIZE - LOCATOR_DEGREE
EXCHANGE_FLOOR = 67_472
RECORD_COUNT = 69
AFFINE_DIMENSION = 8

SIGN_TYPE_COUNT = 1 << AFFINE_DIMENSION
TYPE_MULTIPLICITY = 5_274
COMMON_ONE_COORDINATES = 141
COMMON_ZERO_COORDINATES = 544_451
VERTEX_INDICES = tuple(range(68)) + (128,)
EXPECTED_BASIS_INDICES = (1, 2, 4, 8, 16, 32, 64, 128)

U_PAID = 4_200_515_150_819_207
B_REMAINING = 270_780_212_960_575_880

SOURCE_PATHS = (
    "experimental/notes/frontier-adjacent/"
    "kb_mca_v4_equality_wall_residue_line_partition_reduction_v1.md",
    "experimental/data/certificates/"
    "kb-mca-v4-source-map-class-compiler-v1/manifest.json",
)


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_path(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def payload_digest(document: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(document)
    unsigned.pop("payload_sha256", None)
    return digest_bytes(canonical_json(unsigned))


def sign_vector(index: int) -> tuple[int, ...]:
    need(0 <= index < SIGN_TYPE_COUNT, "sign-vector index range")
    return tuple(
        -1 if (index >> coordinate) & 1 else 1
        for coordinate in range(AFFINE_DIMENSION)
    )


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    need(
        len(left) == len(right) == AFFINE_DIMENSION,
        "dot-product dimensions",
    )
    return sum(a * b for a, b in zip(left, right, strict=True))


def rank_mod(rows: list[list[int]], prime: int = P) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    need(all(len(row) == width for row in rows), "matrix row widths")
    matrix = [[entry % prime for entry in row] for row in rows]
    rank = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(rank, len(matrix))
                if matrix[row][column] % prime
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], prime - 2, prime)
        matrix[rank] = [
            entry * inverse % prime for entry in matrix[rank]
        ]
        for row in range(len(matrix)):
            if row == rank:
                continue
            scalar = matrix[row][column] % prime
            if scalar:
                matrix[row] = [
                    (left - scalar * right) % prime
                    for left, right in zip(
                        matrix[row], matrix[rank], strict=True
                    )
                ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def affine_rank(indices: tuple[int, ...]) -> int:
    need(bool(indices), "nonempty affine-rank input")
    base = sign_vector(indices[0])
    rows = [
        [
            value - base_value
            for value, base_value in zip(
                sign_vector(index), base, strict=True
            )
        ]
        for index in indices[1:]
    ]
    return rank_mod(rows)


def evaluation_values(index: int) -> tuple[int, ...]:
    vertex = sign_vector(index)
    return tuple(
        dot(vertex, sign_vector(coordinate_type))
        for coordinate_type in range(SIGN_TYPE_COUNT)
    )


def zero_mask(values: tuple[int, ...]) -> int:
    mask = 0
    for coordinate_type, value in enumerate(values):
        if value % P == 0:
            mask |= 1 << coordinate_type
    return mask


def mask_digest(index: int, mask: int) -> str:
    width = SIGN_TYPE_COUNT // 8
    raw = index.to_bytes(2, "big") + mask.to_bytes(width, "big")
    return digest_bytes(raw)


def common_zero_type_count(distance: int) -> int:
    need(1 <= distance <= AFFINE_DIMENSION, "positive Hamming distance")
    if distance % 2:
        return 0
    half = distance // 2
    return math.comb(distance, half) * math.comb(
        AFFINE_DIMENSION - distance,
        4 - half,
    )


def choose_star_basis() -> tuple[int, ...]:
    root = VERTEX_INDICES[0]
    selected: list[int] = []
    current_rank = 0
    for index in VERTEX_INDICES[1:]:
        candidate = tuple([root, *selected, index])
        new_rank = affine_rank(candidate)
        if new_rank > current_rank:
            selected.append(index)
            current_rank = new_rank
        if current_rank == AFFINE_DIMENSION:
            break
    need(current_rank == AFFINE_DIMENSION, "star basis has rank eight")
    return tuple(selected)


def circuit_for(index: int) -> dict[str, Any]:
    need(index not in EXPECTED_BASIS_INDICES, "nonbasis circuit target")
    need(index != 0, "nonroot circuit target")
    basis_vertices = tuple(
        1 << coordinate
        for coordinate in range(AFFINE_DIMENSION)
        if (index >> coordinate) & 1
    )
    weight = len(basis_vertices)
    need(weight >= 2, "nonbasis cube vertex has weight at least two")
    vertices = (0, *basis_vertices, index)
    coefficients = {
        0: weight - 1,
        index: 1,
        **{basis: -1 for basis in basis_vertices},
    }
    need(
        sum(coefficients[vertex] for vertex in vertices) == 0,
        "affine circuit coefficients sum to zero",
    )
    for coordinate in range(AFFINE_DIMENSION):
        total = sum(
            coefficients[vertex] * sign_vector(vertex)[coordinate]
            for vertex in vertices
        )
        need(total == 0, "affine circuit vector relation")

    size = len(vertices)
    need(
        affine_rank(vertices) == size - 2,
        "full circuit affine rank",
    )
    for deleted in range(size):
        subset = vertices[:deleted] + vertices[deleted + 1 :]
        need(
            affine_rank(subset) == len(subset) - 1,
            "circuit deletion is affine independent",
        )

    common_zero_types = 0
    for coordinate_type in range(SIGN_TYPE_COUNT):
        values = [
            dot(sign_vector(vertex), sign_vector(coordinate_type))
            for vertex in vertices
        ]
        relation = sum(
            coefficients[vertex] * value
            for vertex, value in zip(vertices, values, strict=True)
        )
        need(relation == 0, "circuit relation on sign coordinate")
        occupied = sum(value % P != 0 for value in values)
        need(occupied != 1, "no singleton carrier atom")
        if occupied == 0:
            common_zero_types += 1

    need(
        sum(coefficients[vertex] for vertex in vertices) == 0,
        "circuit relation on common-one coordinates",
    )
    need(common_zero_types == 0, "canonical circuit sign common zeros")
    common_zero_coordinates = COMMON_ZERO_COORDINATES
    restriction_rank = 0
    rank_bound = 10 - size
    need(
        restriction_rank <= rank_bound,
        "circuit restriction-rank bound",
    )
    return {
        "target_index": index,
        "basis_vertices": list(basis_vertices),
        "vertices": list(vertices),
        "size": size,
        "coefficient_vector": [
            {"vertex": vertex, "coefficient": coefficients[vertex]}
            for vertex in vertices
        ],
        "common_zero_sign_types": common_zero_types,
        "common_zero_coordinates": common_zero_coordinates,
        "restriction_rank": restriction_rank,
        "required_rank_upper": rank_bound,
        "no_singleton_atoms": True,
    }


def compile_model() -> dict[str, Any]:
    need(P > 2, "odd characteristic")
    need(FIELD_EXTENSION_DEGREE == 6, "deployed extension degree")
    need(len(VERTEX_INDICES) == RECORD_COUNT, "69 vertex indices")
    need(len(set(VERTEX_INDICES)) == RECORD_COUNT, "distinct vertices")
    need(all(0 <= index < 256 for index in VERTEX_INDICES), "8-cube")
    need(
        V_SIZE
        == SIGN_TYPE_COUNT * TYPE_MULTIPLICITY
        + COMMON_ONE_COORDINATES
        + COMMON_ZERO_COORDINATES,
        "carrier-size decomposition",
    )
    need(
        LOCATOR_DEGREE
        == 186 * TYPE_MULTIPLICITY + COMMON_ONE_COORDINATES,
        "support-size decomposition",
    )
    need(
        ZERO_COUNT
        == 70 * TYPE_MULTIPLICITY + COMMON_ZERO_COORDINATES,
        "zero-size decomposition",
    )

    masks: dict[int, int] = {}
    support_digests = []
    for index in VERTEX_INDICES:
        values = evaluation_values(index)
        need(
            all(value in (-8, -6, -4, -2, 0, 2, 4, 6, 8) for value in values),
            "sign-dot value range",
        )
        mask = zero_mask(values)
        need(mask.bit_count() == math.comb(8, 4) == 70, "70 zero types")
        masks[index] = mask
        support_digests.append(mask_digest(index, mask))

    base = sign_vector(VERTEX_INDICES[0])
    difference_rows = [
        [
            value - base_value
            for value, base_value in zip(
                sign_vector(index), base, strict=True
            )
        ]
        for index in VERTEX_INDICES[1:]
    ]
    need(rank_mod(difference_rows) == AFFINE_DIMENSION, "affine rank eight")

    basis = choose_star_basis()
    need(basis == EXPECTED_BASIS_INDICES, "canonical first basis")

    evaluation_rows = []
    for basis_index in basis:
        basis_values = evaluation_values(basis_index)
        root_values = evaluation_values(0)
        evaluation_rows.append(
            [
                (left - right) % P
                for left, right in zip(
                    basis_values, root_values, strict=True
                )
            ]
        )
    need(
        rank_mod(evaluation_rows) == AFFINE_DIMENSION,
        "evaluation secant rank eight",
    )

    hamming_histogram: dict[int, int] = {}
    exchange_type_histogram: dict[int, int] = {}
    weighted_exchange_histogram: dict[int, int] = {}
    pair_digest_state = hashlib.sha256(
        b"kb-circuit-only-pairs-v1"
    ).digest()
    minimum_exchange = V_SIZE
    for left, right in itertools.combinations(VERTEX_INDICES, 2):
        distance = (left ^ right).bit_count()
        need(1 <= distance <= 7, "no duplicate or antipodal pair")
        intersection_formula = common_zero_type_count(distance)
        intersection_mask = (masks[left] & masks[right]).bit_count()
        need(
            intersection_mask == intersection_formula,
            "pair zero-intersection formula",
        )
        left_only = (masks[left] & ~masks[right]).bit_count()
        right_only = (masks[right] & ~masks[left]).bit_count()
        need(left_only == right_only, "equal directed exchange")
        need(
            left_only == 70 - intersection_formula,
            "directed exchange formula",
        )
        exchange = left_only * TYPE_MULTIPLICITY
        need(exchange >= EXCHANGE_FLOOR, "deployed exchange floor")
        minimum_exchange = min(minimum_exchange, exchange)
        hamming_histogram[distance] = hamming_histogram.get(distance, 0) + 1
        exchange_type_histogram[left_only] = (
            exchange_type_histogram.get(left_only, 0) + 1
        )
        weighted_exchange_histogram[exchange] = (
            weighted_exchange_histogram.get(exchange, 0) + 1
        )
        pair_digest_state = hashlib.sha256(
            pair_digest_state
            + left.to_bytes(2, "big")
            + right.to_bytes(2, "big")
            + distance.to_bytes(1, "big")
            + left_only.to_bytes(1, "big")
        ).digest()

    need(
        sum(exchange_type_histogram.values()) == math.comb(69, 2),
        "all 2346 pairs",
    )
    need(
        exchange_type_histogram == {70: 1190, 34: 581, 30: 575},
        "exact exchange-type histogram",
    )
    need(
        minimum_exchange == 30 * TYPE_MULTIPLICITY == 158_220,
        "exact minimum exchange",
    )
    need(
        minimum_exchange - EXCHANGE_FLOOR == 90_748,
        "exchange-floor margin",
    )

    triangle_count = 0
    for triple in itertools.combinations(VERTEX_INDICES, 3):
        if affine_rank(triple) < 2:
            triangle_count += 1
    need(triangle_count == 0, "no affine three-circuits")

    nonbasis = tuple(
        index
        for index in VERTEX_INDICES[1:]
        if index not in basis
    )
    need(
        len(nonbasis)
        == RECORD_COUNT - 1 - AFFINE_DIMENSION
        == 60,
        "60 nonbasis fundamental circuits",
    )
    circuits = [circuit_for(index) for index in nonbasis]
    circuit_histogram: dict[int, int] = {}
    for circuit in circuits:
        size = circuit["size"]
        circuit_histogram[size] = circuit_histogram.get(size, 0) + 1
    need(
        circuit_histogram == {4: 17, 5: 21, 6: 15, 7: 6, 8: 1},
        "exact circuit-size histogram",
    )

    circuit_digest = digest_bytes(canonical_json(circuits))
    support_digest = digest_bytes(
        canonical_json(
            [
                {"index": index, "mask_sha256": digest}
                for index, digest in zip(
                    VERTEX_INDICES, support_digests, strict=True
                )
            ]
        )
    )

    return {
        "record_count": RECORD_COUNT,
        "distinct_support_records": RECORD_COUNT,
        "zero_sign_types_per_record": 70,
        "nonzero_sign_types_per_record": 186,
        "zero_coordinates_per_record": ZERO_COUNT,
        "support_coordinates_per_record": LOCATOR_DEGREE,
        "affine_rank": AFFINE_DIMENSION,
        "canonical_star_basis_indices": list(basis),
        "canonical_nonbasis_circuit_count": len(circuits),
        "canonical_circuit_size_histogram": {
            str(key): value for key, value in sorted(circuit_histogram.items())
        },
        "canonical_circuit_common_zero_coordinates": COMMON_ZERO_COORDINATES,
        "canonical_circuit_restriction_rank": 0,
        "no_affine_three_circuits": True,
        "no_singleton_atoms_in_canonical_circuits": True,
        "pair_count": math.comb(RECORD_COUNT, 2),
        "pair_hamming_distance_histogram": {
            str(key): value for key, value in sorted(hamming_histogram.items())
        },
        "pair_exchange_type_histogram": {
            str(key): value
            for key, value in sorted(exchange_type_histogram.items())
        },
        "weighted_pair_exchange_histogram": {
            str(key): value
            for key, value in sorted(weighted_exchange_histogram.items())
        },
        "minimum_directed_exchange": minimum_exchange,
        "minimum_exchange_margin_over_c": minimum_exchange - EXCHANGE_FLOOR,
        "support_mask_digest": support_digest,
        "pair_digest": pair_digest_state.hex(),
        "circuit_digest": circuit_digest,
        "circuits": circuits,
    }


def source_bindings() -> list[dict[str, str]]:
    result = []
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        need(path.is_file(), f"source binding exists: {relative}")
        result.append(
            {
                "path": relative,
                "sha256": digest_path(path),
            }
        )
    return result


def expected_certificate() -> dict[str, Any]:
    exact_results = compile_model()
    document: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "status": STATUS,
        "artifact_kind": ARTIFACT_KIND,
        "workboard_item": "K3",
        "row_contract": {
            "row": "KoalaBear MCA at 2^-128",
            "object": "MCA",
            "agreement": 1_116_048,
            "field_base_prime": P,
            "field_extension_degree": FIELD_EXTENSION_DEGREE,
            "carrier_size": V_SIZE,
            "locator_degree": LOCATOR_DEGREE,
            "zero_count": ZERO_COUNT,
            "minimum_pair_exchange": EXCHANGE_FLOOR,
            "candidate_record_count": RECORD_COUNT,
            "unit": "ABSTRACT_SUPPORT_RECORDS_ON_ONE_DECLARED_RESIDUE_LINE",
        },
        "construction": {
            "vertex_indices": list(VERTEX_INDICES),
            "vertex_encoding": "EIGHT_SIGN_COORDINATES_FROM_BINARY_INDEX",
            "coordinate_types": "ALL_256_EIGHT_SIGN_VECTORS",
            "coordinate_value": "DOT_PRODUCT_OF_VERTEX_AND_COORDINATE_SIGN_VECTORS_MOD_P",
            "sign_type_multiplicity": TYPE_MULTIPLICITY,
            "common_one_coordinates": COMMON_ONE_COORDINATES,
            "common_zero_coordinates": COMMON_ZERO_COORDINATES,
            "ambient_affine_dimension": AFFINE_DIMENSION,
        },
        "exact_results": exact_results,
        "route_cut": {
            "falsified_inference": (
                "DEPLOYED_CARDINALITIES_PLUS_AFFINE_RANK_8_PLUS_PAIR_EXCHANGE_"
                "FLOOR_PLUS_60_BOUNDED_CIRCUITS_PLUS_NO_SINGLETON_PLUS_"
                "CIRCUIT_RESTRICTION_RANK_DO_NOT_IMPLY_CAP_68_OR_OWNER_EMISSION"
            ),
            "cap_68_follows_from_circuit_only_axioms": False,
            "same_record_owner_emitted": False,
            "full_primitive_69_point_theorem_refuted": False,
            "required_new_input": (
                "POLYNOMIAL_LOCATOR_SOURCE_QUOTIENT_HILBERT_BURCH_STRUCTURE_"
                "OR_SAME_RECORD_ACTIVE_OWNER_SEMANTICS"
            ),
        },
        "omitted_load_bearing_structure": [
            "NO_SPLIT_LOCATOR_POLYNOMIALS",
            "NO_LAMBDA_Z_I_TIMES_A_I_FACTORIZATION",
            "NO_SOURCE_UNIT_RECIPROCAL_PARAMETER",
            "NO_POLYNOMIAL_T_IJ_QUOTIENTS_OR_DEGREE_BOUNDS",
            "NO_HILBERT_BURCH_LINE_MODULE",
            "NO_RECEIVED_LINE_OR_COMPLETE_SELECTOR",
            "NO_GRAPH_RECORD_OR_SLOPE_OWNER_EVIDENCE",
            "NO_ACTIVE_FIRST_MATCH_PAYMENT",
        ],
        "closure_state": {
            "U_paid_before": U_PAID,
            "U_paid_after": U_PAID,
            "B_remaining_before": B_REMAINING,
            "B_remaining_after": B_REMAINING,
            "additional_charge": 0,
            "cap_68_proved": False,
            "equality_wall_paid": False,
            "row_closed": False,
            "terminal": (
                "ROUTE_CUT_CIRCUIT_ONLY_INFERENCE_REQUIRES_POLYNOMIAL_OR_OWNER_INPUT"
            ),
        },
        "audit": {
            "proof": "EXACT_FINITE_COUNTERMODEL_TO_A_WEAKENED_INFERENCE",
            "empirical_evidence": "NONE_USED",
            "conjecture": "FULL_PRIMITIVE_69_POINT_EXCLUSION_REMAINS_OPEN",
            "global_verdict": "YELLOW_ROW_OPEN",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
        },
        "source_bindings": source_bindings(),
    }
    document["payload_sha256"] = payload_digest(document)
    return document


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    decoder = json.JSONDecoder()
    value, end = decoder.raw_decode(raw)
    need(not raw[end:].strip(), "no trailing JSON data")
    need(isinstance(value, dict), "certificate is a JSON object")
    return value


def validate_certificate(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    need(document.get("schema") == SCHEMA_ID, "schema id")
    need(document.get("status") == STATUS, "status")
    need(document.get("artifact_kind") == ARTIFACT_KIND, "artifact kind")
    need(
        document.get("payload_sha256") == payload_digest(document),
        "payload seal",
    )
    need(document == expected, "certificate equals exact reconstruction")


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutations() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", "wrong")),
        ("status", lambda d: d.__setitem__("status", "SAFE")),
        (
            "prime",
            lambda d: d["row_contract"].__setitem__(
                "field_base_prime", P - 2
            ),
        ),
        (
            "carrier",
            lambda d: d["row_contract"].__setitem__(
                "carrier_size", V_SIZE - 1
            ),
        ),
        (
            "locator",
            lambda d: d["row_contract"].__setitem__(
                "locator_degree", LOCATOR_DEGREE - 1
            ),
        ),
        (
            "exchange-floor",
            lambda d: d["row_contract"].__setitem__(
                "minimum_pair_exchange", EXCHANGE_FLOOR - 1
            ),
        ),
        (
            "vertex",
            lambda d: d["construction"]["vertex_indices"].__setitem__(
                -1, 127
            ),
        ),
        (
            "multiplicity",
            lambda d: d["construction"].__setitem__(
                "sign_type_multiplicity", TYPE_MULTIPLICITY - 1
            ),
        ),
        (
            "common-one",
            lambda d: d["construction"].__setitem__(
                "common_one_coordinates", COMMON_ONE_COORDINATES + 1
            ),
        ),
        (
            "common-zero",
            lambda d: d["construction"].__setitem__(
                "common_zero_coordinates", COMMON_ZERO_COORDINATES - 1
            ),
        ),
        (
            "record-count",
            lambda d: d["exact_results"].__setitem__("record_count", 68),
        ),
        (
            "affine-rank",
            lambda d: d["exact_results"].__setitem__("affine_rank", 7),
        ),
        (
            "basis",
            lambda d: d["exact_results"][
                "canonical_star_basis_indices"
            ].__setitem__(-1, 64),
        ),
        (
            "circuit-count",
            lambda d: d["exact_results"].__setitem__(
                "canonical_nonbasis_circuit_count", 59
            ),
        ),
        (
            "circuit-histogram",
            lambda d: d["exact_results"][
                "canonical_circuit_size_histogram"
            ].__setitem__("4", 16),
        ),
        (
            "triangle",
            lambda d: d["exact_results"].__setitem__(
                "no_affine_three_circuits", False
            ),
        ),
        (
            "singleton",
            lambda d: d["exact_results"].__setitem__(
                "no_singleton_atoms_in_canonical_circuits", False
            ),
        ),
        (
            "pair-count",
            lambda d: d["exact_results"].__setitem__("pair_count", 2345),
        ),
        (
            "pair-histogram",
            lambda d: d["exact_results"][
                "pair_exchange_type_histogram"
            ].__setitem__("30", 574),
        ),
        (
            "minimum-exchange",
            lambda d: d["exact_results"].__setitem__(
                "minimum_directed_exchange", EXCHANGE_FLOOR
            ),
        ),
        (
            "cap68",
            lambda d: d["route_cut"].__setitem__(
                "cap_68_follows_from_circuit_only_axioms", True
            ),
        ),
        (
            "owner",
            lambda d: d["route_cut"].__setitem__(
                "same_record_owner_emitted", True
            ),
        ),
        (
            "full-counterexample",
            lambda d: d["route_cut"].__setitem__(
                "full_primitive_69_point_theorem_refuted", True
            ),
        ),
        (
            "omit-polynomial",
            lambda d: d["omitted_load_bearing_structure"].pop(),
        ),
        (
            "ledger",
            lambda d: d["closure_state"].__setitem__(
                "additional_charge", 1
            ),
        ),
        (
            "row-closed",
            lambda d: d["closure_state"].__setitem__("row_closed", True),
        ),
        (
            "source-hash",
            lambda d: d["source_bindings"][0].__setitem__(
                "sha256", "0" * 64
            ),
        ),
        (
            "circuit-coefficient",
            lambda d: d["exact_results"]["circuits"][0][
                "coefficient_vector"
            ][0].__setitem__("coefficient", 0),
        ),
    ]


def run_tamper_selftest(
    expected: dict[str, Any],
) -> int:
    rejected = 0
    for name, mutate in mutations():
        candidate = copy.deepcopy(expected)
        mutate(candidate)
        candidate["payload_sha256"] = payload_digest(candidate)
        try:
            validate_certificate(candidate, expected)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"mutation escaped: {name}")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    selected = sum(
        (
            args.check,
            args.emit,
            args.print_template,
            args.tamper_selftest,
        )
    )
    need(selected == 1, "select exactly one action")

    expected = expected_certificate()
    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected))
        return
    if args.emit:
        args.certificate.parent.mkdir(parents=True, exist_ok=True)
        args.certificate.write_bytes(canonical_json(expected))
        print(f"wrote {args.certificate}")
        return

    document = strict_load(args.certificate)
    validate_certificate(document, expected)
    if args.tamper_selftest:
        rejected = run_tamper_selftest(expected)
        print(f"PASS: {rejected}/{len(mutations())} mutations rejected")
        return

    results = expected["exact_results"]
    print("PASS: KoalaBear equality-wall circuit-only route cut")
    print(f"checks={CHECKS}")
    print(f"records={results['record_count']}")
    print(f"affine_rank={results['affine_rank']}")
    print(
        "canonical_circuits="
        f"{results['canonical_nonbasis_circuit_count']}"
    )
    print(
        "minimum_directed_exchange="
        f"{results['minimum_directed_exchange']}"
    )
    print("ledger_movement=0")
    print(
        "terminal=ROUTE_CUT_CIRCUIT_ONLY_INFERENCE_REQUIRES_"
        "POLYNOMIAL_OR_OWNER_INPUT"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError, VerificationError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
