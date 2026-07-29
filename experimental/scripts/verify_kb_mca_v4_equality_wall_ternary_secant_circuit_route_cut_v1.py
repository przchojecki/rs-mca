#!/usr/bin/env python3
"""Exact ternary-secant/circuit route cut for the KoalaBear equality wall.

This verifier reconstructs an explicit 69-record affine family at the
deployed KoalaBear carrier cardinalities.  The family has constant support
981,105, secant rank eight, pair exchange at least 67,472, and every
selected-pair and projective ternary secant clears the deployed
shortened-GRS distance threshold 1,048,577.  Its canonical fundamental
circuits also satisfy the no-singleton and restriction-rank consequences
printed by the equality-wall reduction.

The family is an abstract F_p-valued carrier model, viewed inside F_(p^6)
by scalar extension.  It is not claimed to be a subcode of the deployed GRS
code, and the minimum distance of the full eight-dimensional secant span is
deliberately not claimed.  It also does not construct split locators, source
quotients, degree bounds, a Hilbert--Burch module, or source-bound owner
evidence.  It therefore cuts only arguments using the explicitly verified
pairwise/ternary support, rank, distance, and circuit consequences.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import itertools
import json
import math
import sys
import zlib
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
    "kb-mca-v4-equality-wall-ternary-secant-circuit-route-cut-v1/"
    "certificate.json"
)

SCHEMA_ID = (
    "rs-mca-kb-v4-equality-wall-ternary-secant-circuit-route-cut-v1"
)
STATUS = "PROVED_TERNARY_SECANT_CIRCUIT_ROUTE_CUT_ROW_OPEN"
ARTIFACT_KIND = (
    "EXACT_ABSTRACT_COUNTERMODEL_TO_PAIRWISE_AND_TERNARY_SECANT_"
    "CIRCUIT_CAP68_INFERENCE"
)
ARCHITECTURE_ID = None
PARTITION_SHA256 = None

P = 2_130_706_433
FIELD_EXTENSION_DEGREE = 6
ROW_N = 2_097_152
ROW_K = 1_048_576
B_STAR = 274_980_728_111_395_087
V_SIZE = 1_894_736
LOCATOR_DEGREE = 981_105
ZERO_COUNT = V_SIZE - LOCATOR_DEGREE
GRS_DISTANCE = 1_048_577
EXCHANGE_FLOOR = GRS_DISTANCE - LOCATOR_DEGREE
RECORD_COUNT = 69
AFFINE_DIMENSION = 8
PROJECTIVE_TERNARY_DIRECTION_COUNT = (3**AFFINE_DIMENSION - 1) // 2
MAXIMUM_ALLOWED_SECANT_ZEROS = V_SIZE - GRS_DISTANCE

VERTEX_INDICES = tuple(range(68)) + (128,)
EXPECTED_BASIS_INDICES = (1, 2, 4, 8, 16, 32, 64, 128)

SOURCE_PATHS = (
    "agents.md",
    "experimental/experiments.tex",
    "experimental/data/certificates/four-row-exact-completion-compiler-v1/"
    "four_row_exact_completion_compiler_v1.json",
)

# Canonical JSON rows [normal in {-1,0,1}^8, affine offset, multiplicity],
# compressed with zlib level 9 and encoded with Python's base85 codec.
WITNESS_SHA256 = (
    "5fbaed397c3cf788d6805c7b203e4a94e95ea8a13bdd74e54c393220ddcdd788"
)
WITNESS_B85 = """
c-n=TX^tZ+41oW?vs5G-8v|!)<^I=r)IxayGU`@Fqc0fnZu;-<4-WV9?H|Zot9*|L@q2vmNNGv%pjv5(T01ImjSSD-x;)^5MIoM>yh1al$ng5-J_}^96kZ5N&hKfiW!K6_YHCTEqi9xggJRa6pPzTBG&F2Teqd=<tP1`f>7b@(#YgOeu$7c=HUwTWKhH(`H*$jJzcKW5DWb?Y@r<z>03y6Eb*)9BWH9K*r3@}J9NSiAaTLY|m+c^7pzuIAYMz$r%9@Jb6;&=A1QEUlXt`LaR-3mTL5kznV=yy;qo{6*@+t{b>La+j1qns22BZUP&3k@&vPk4O0+L(t(5U(R%v*{FOHF}V$LgAH4!`C-<z{my=NG5T8MgryeOta&i$J45#OmRV*((Y#6|>A-=F~w$U<+;7C7_l(eC&26GePpqSX`Q3B81-MY3lrno=p*jnxlFo=ozM_9X;K!O>6N!aXJzqDpO~<u9GTYu@r153snbQZt4-IOr7D<Lr-|%A-;~!Ox3dYsL=DB2C+l^7FhVQG`eURzx}xNxcA(Bf%|2bT-PtSm491c!}%Zzcqr^rN#l~&{E0e{yGYK$-~ICs-mh0C{8KwW4i6?NU2#pwx%h8b_rzKNcK8g%EIDEm``x&OEnnC+{owKVljRnxw|=4N=RO-j_BdLl?eToD;8A6!cl2dzZLsz3)VI`TAOvll385NuX;fdlTT>jfDJ-#MG&EYG_hlr>eZi#T-g+euhf41>m5EpMt}NKpg_iMcG`$LM!U?~*tZ!bx#P=$^jj2}A9i+Qzg2WuL$)kxfPRmVnG?N<s5%`O^k0;xPz3D=37mGKxJwk3)>|0;&LQZH`{=-tg4TZiS5fz#iTQdqv#BS$0(?vvS$NW@gV1KB6X)&jI#I~8e9RXo20dEo$hGwEx%nR5LQeF*)*6|5KZtStE%~S*<wz;F1?&i5hDH%@(-`(GxldPx~iQFR9Has;9*vybb2!WwGMG~|teK*}lw*nlo$?(0ANe;hZ(Epc*(>QkNIpzE+(y8iRi6zzSIQT@`J0T9-<P7E@-T2(+oJ?qm?*IjY8mNw7IS^geqaZ1SDfL&8$aMnamK+3k-hLalG)U%WfVPvHt!D`>wULWGu{-EHd8o-l81+W-D3PJcjX22=v2hyYRI=mX+Uh3as7ar_#Hw|Cx89A@)UGbRpSchMeEVu@(9D*KuM$&8EoXZ95kILts@S#GBffT>^>X=C4&rOX?RCPV@!j>^yvOt2U^)(wq0LoK-qS+ZcvE+O_uGqCkgn2NXv<Frk!kByW4P?qqdK+5ogTt$uMBPk{hZZd#JJPe<6qQdN6-A=+(a|PJHd;?{>_O*+Jv8YsV!H-77az&V}7giruoM$?Yfj1j-ct9%#Qk|4tiS`@bLNbSu=YWFC<&41If>s0YkA8qXq~~LDw)9aun<nSZN6Zb+1WkIagrs(hMyJYMy?Pi^6$OA)w^GptBbpls!>LM7G2QR#x|pvrWY!%BIJ>ijmq1C2!B`bNclbLJ2Gb?W21az>cA*U9Abv?0Fv)ey_ithJIk3JJ+L*W{}mS!!sOhSi|a|Y0(O2FLmqjt6a(fu6p`7rHDJKwqSQzshY_Gq|+}QG$U-v&z}#_KYCqOsaa6j{sn41_CyHgFAo_QH@IizA{?OGHBa!-kG1pm;lgcstF?Lpqn>7|#iP|Q6K9z#GkyR2ALG_(!~
""".strip()


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


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite_constant(value: str) -> None:
    raise VerificationError(f"nonfinite JSON constant: {value}")


def strict_decode(raw: bytes) -> Any:
    text = raw.decode("utf-8")
    decoder = json.JSONDecoder(
        object_pairs_hook=reject_duplicate_pairs,
        parse_constant=reject_nonfinite_constant,
    )
    value, end = decoder.raw_decode(text)
    need(not text[end:].strip(), "no trailing JSON data")
    need(raw == canonical_json(value), "canonical JSON bytes")
    return value


def decode_witness() -> list[list[Any]]:
    compressed = base64.b85decode(WITNESS_B85.encode("ascii"))
    raw = zlib.decompress(compressed)
    need(digest_bytes(raw) == WITNESS_SHA256, "sealed witness digest")
    rows = strict_decode(raw)
    need(isinstance(rows, list), "witness row list")
    return rows


def sign_vector(index: int) -> tuple[int, ...]:
    need(0 <= index < 1 << AFFINE_DIMENSION, "sign-vector index range")
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
    need(current_rank == AFFINE_DIMENSION, "star basis rank eight")
    return tuple(selected)


def normalize_witness(
    rows: list[list[Any]],
) -> list[tuple[tuple[int, ...], int, int]]:
    need(len(rows) == 225, "225 coordinate types")
    result = []
    seen: set[tuple[tuple[int, ...], int]] = set()
    for row in rows:
        need(isinstance(row, list) and len(row) == 3, "witness row shape")
        normal_raw, offset, multiplicity = row
        need(
            isinstance(normal_raw, list)
            and len(normal_raw) == AFFINE_DIMENSION,
            "normal shape",
        )
        need(
            all(type(value) is int and value in (-1, 0, 1)
                for value in normal_raw),
            "normal entries",
        )
        need(
            type(offset) is int
            and (-8 <= offset <= 8 or offset == 99),
            "offset range or declared empty level",
        )
        need(
            type(multiplicity) is int and multiplicity > 0,
            "positive integer multiplicity",
        )
        normal = tuple(normal_raw)
        if any(normal):
            first = next(value for value in normal if value)
            need(first == 1, "normalized nonzero normal")
            occupied = any(
                dot(sign_vector(index), normal) == offset
                for index in VERTEX_INDICES
            )
            need(
                occupied or offset == 99,
                "occupied affine level or declared empty level",
            )
        else:
            need(offset == 0, "zero normal is common-zero type")
        key = (normal, offset)
        need(key not in seen, "distinct coordinate types")
        seen.add(key)
        result.append((normal, offset, multiplicity))
    need(sum(row[2] for row in result) == V_SIZE, "carrier size")
    return result


def record_values(
    index: int,
    witness: list[tuple[tuple[int, ...], int, int]],
) -> tuple[int, ...]:
    vertex = sign_vector(index)
    return tuple(dot(vertex, normal) - offset for normal, offset, _ in witness)


def projective_ternary_directions() -> tuple[tuple[int, ...], ...]:
    directions = tuple(
        vector
        for vector in itertools.product((-1, 0, 1), repeat=AFFINE_DIMENSION)
        if any(vector) and next(value for value in vector if value) == 1
    )
    need(
        len(directions) == PROJECTIVE_TERNARY_DIRECTION_COUNT == 3_280,
        "all projective ternary directions",
    )
    return directions


def circuit_for(
    index: int,
    witness: list[tuple[tuple[int, ...], int, int]],
    values: dict[int, tuple[int, ...]],
) -> dict[str, Any]:
    need(index not in EXPECTED_BASIS_INDICES, "nonbasis circuit target")
    need(index != 0, "nonroot circuit target")
    basis_vertices = tuple(
        1 << coordinate
        for coordinate in range(AFFINE_DIMENSION)
        if (index >> coordinate) & 1
    )
    weight = len(basis_vertices)
    need(weight >= 2, "nonbasis cube vertex weight")
    vertices = (0, *basis_vertices, index)
    coefficients = {
        0: weight - 1,
        index: 1,
        **{basis: -1 for basis in basis_vertices},
    }
    need(
        sum(coefficients[vertex] for vertex in vertices) == 0,
        "circuit coefficient sum",
    )
    for coordinate in range(AFFINE_DIMENSION):
        need(
            sum(
                coefficients[vertex] * sign_vector(vertex)[coordinate]
                for vertex in vertices
            )
            == 0,
            "circuit vector relation",
        )

    size = len(vertices)
    need(affine_rank(vertices) == size - 2, "minimal-circuit rank")
    for deleted in range(size):
        subset = vertices[:deleted] + vertices[deleted + 1 :]
        need(
            affine_rank(subset) == len(subset) - 1,
            "circuit deletion independence",
        )

    common_zero_types: list[int] = []
    common_zero_coordinates = 0
    for type_index, (_, _, multiplicity) in enumerate(witness):
        coordinate_values = [values[vertex][type_index] for vertex in vertices]
        need(
            sum(
                coefficients[vertex] * value
                for vertex, value in zip(
                    vertices, coordinate_values, strict=True
                )
            )
            == 0,
            "circuit coordinate relation",
        )
        occupied = sum(value % P != 0 for value in coordinate_values)
        need(occupied != 1, "no singleton carrier atom")
        if occupied == 0:
            common_zero_types.append(type_index)
            common_zero_coordinates += multiplicity

    restriction_rows = []
    for basis_index in EXPECTED_BASIS_INDICES:
        restriction_rows.append(
            [
                values[basis_index][type_index] - values[0][type_index]
                for type_index in common_zero_types
            ]
        )
    restriction_rank = rank_mod(restriction_rows)
    rank_bound = 10 - size
    need(restriction_rank <= rank_bound, "circuit restriction-rank bound")
    return {
        "target_index": index,
        "basis_vertices": list(basis_vertices),
        "vertices": list(vertices),
        "size": size,
        "coefficient_vector": [
            {"vertex": vertex, "coefficient": coefficients[vertex]}
            for vertex in vertices
        ],
        "common_zero_type_count": len(common_zero_types),
        "common_zero_coordinates": common_zero_coordinates,
        "restriction_rank": restriction_rank,
        "required_rank_upper": rank_bound,
        "no_singleton_atoms": True,
    }


def compile_model() -> dict[str, Any]:
    need(P > 2, "odd characteristic")
    need(FIELD_EXTENSION_DEGREE == 6, "deployed extension degree")
    need(EXCHANGE_FLOOR == 67_472, "deployed exchange floor")
    need(len(VERTEX_INDICES) == RECORD_COUNT, "69 vertex indices")
    need(len(set(VERTEX_INDICES)) == RECORD_COUNT, "distinct vertices")
    need(affine_rank(VERTEX_INDICES) == AFFINE_DIMENSION, "affine rank eight")

    witness = normalize_witness(decode_witness())
    values = {
        index: record_values(index, witness) for index in VERTEX_INDICES
    }
    zero_counts: dict[int, int] = {}
    for index in VERTEX_INDICES:
        zero_count = sum(
            multiplicity
            for value, (_, _, multiplicity) in zip(
                values[index], witness, strict=True
            )
            if value % P == 0
        )
        need(zero_count == ZERO_COUNT, "record zero count")
        zero_counts[index] = zero_count

    basis = choose_star_basis()
    need(basis == EXPECTED_BASIS_INDICES, "canonical star basis")
    secant_rows = [
        [
            values[basis_index][type_index] - values[0][type_index]
            for type_index in range(len(witness))
        ]
        for basis_index in basis
    ]
    need(rank_mod(secant_rows) == AFFINE_DIMENSION, "secant rank eight")
    vertex_rows = [list(values[index]) for index in VERTEX_INDICES]
    full_linear_rank = rank_mod(vertex_rows)
    need(full_linear_rank == 9, "full vertex-function rank nine")

    pair_data = []
    distance_histogram: dict[int, int] = {}
    exchange_histogram: dict[int, int] = {}
    minimum_distance = V_SIZE
    maximum_pair_zero = 0
    minimum_exchange = V_SIZE
    maximum_exchange = 0
    for left, right in itertools.combinations(VERTEX_INDICES, 2):
        pair_zero = 0
        left_only = 0
        right_only = 0
        common_zero = 0
        for left_value, right_value, (_, _, multiplicity) in zip(
            values[left], values[right], witness, strict=True
        ):
            if (left_value - right_value) % P == 0:
                pair_zero += multiplicity
            left_nonzero = left_value % P != 0
            right_nonzero = right_value % P != 0
            if left_nonzero and not right_nonzero:
                left_only += multiplicity
            if right_nonzero and not left_nonzero:
                right_only += multiplicity
            if not left_nonzero and not right_nonzero:
                common_zero += multiplicity
        need(left_only == right_only, "equal directed exchange")
        need(
            common_zero + left_only == ZERO_COUNT,
            "zero-set pair decomposition",
        )
        distance = V_SIZE - pair_zero
        need(
            distance >= GRS_DISTANCE,
            "selected-pair shortened-GRS distance threshold",
        )
        need(left_only >= EXCHANGE_FLOOR, "deployed exchange floor")
        need(distance <= LOCATOR_DEGREE + left_only, "support-union bound")
        minimum_distance = min(minimum_distance, distance)
        maximum_pair_zero = max(maximum_pair_zero, pair_zero)
        minimum_exchange = min(minimum_exchange, left_only)
        maximum_exchange = max(maximum_exchange, left_only)
        distance_histogram[distance] = distance_histogram.get(distance, 0) + 1
        exchange_histogram[left_only] = exchange_histogram.get(left_only, 0) + 1
        pair_data.append(
            {
                "left": left,
                "right": right,
                "pair_zero": pair_zero,
                "distance": distance,
                "directed_exchange": left_only,
                "common_zero": common_zero,
            }
        )
    need(len(pair_data) == math.comb(RECORD_COUNT, 2), "all 2346 pairs")
    need(maximum_pair_zero == 840_990, "exact maximum pair-zero count")
    need(minimum_distance == 1_053_746, "exact minimum pair distance")
    need(
        minimum_distance - GRS_DISTANCE == 5_169,
        "exact selected-pair distance margin",
    )
    need(minimum_exchange == 121_284, "exact minimum directed exchange")
    need(maximum_exchange == 616_161, "exact maximum directed exchange")

    normal_weights: dict[tuple[int, ...], int] = {}
    for normal, _, multiplicity in witness:
        normal_weights[normal] = (
            normal_weights.get(normal, 0) + multiplicity
        )
    ternary_data = []
    maximum_ternary_zero = 0
    maximum_ternary_zero_direction: tuple[int, ...] | None = None
    for coefficient in projective_ternary_directions():
        zero_coordinates = sum(
            multiplicity
            for normal, multiplicity in normal_weights.items()
            if dot(coefficient, normal) % P == 0
        )
        need(
            zero_coordinates <= MAXIMUM_ALLOWED_SECANT_ZEROS,
            "projective ternary secant clears distance threshold",
        )
        if zero_coordinates > maximum_ternary_zero:
            maximum_ternary_zero = zero_coordinates
            maximum_ternary_zero_direction = coefficient
        ternary_data.append(
            {
                "coefficient": list(coefficient),
                "zero_coordinates": zero_coordinates,
                "distance": V_SIZE - zero_coordinates,
            }
        )
    need(
        maximum_ternary_zero == 841_778,
        "exact maximum projective ternary zero count",
    )
    need(
        maximum_ternary_zero_direction == (1, 0, 0, 0, 0, 0, 0, 1),
        "canonical maximum projective ternary direction",
    )
    minimum_ternary_distance = V_SIZE - maximum_ternary_zero
    need(
        minimum_ternary_distance == 1_052_958,
        "exact minimum projective ternary distance",
    )
    need(
        minimum_ternary_distance - GRS_DISTANCE == 4_381,
        "exact projective ternary distance margin",
    )

    triangle_count = sum(
        affine_rank(triple) < 2
        for triple in itertools.combinations(VERTEX_INDICES, 3)
    )
    need(triangle_count == 0, "no affine three-circuits")

    nonbasis = tuple(
        index for index in VERTEX_INDICES[1:] if index not in basis
    )
    need(len(nonbasis) == 60, "60 nonbasis fundamental circuits")
    circuits = [circuit_for(index, witness, values) for index in nonbasis]
    circuit_histogram: dict[int, int] = {}
    restriction_histogram: dict[int, int] = {}
    for circuit in circuits:
        size = circuit["size"]
        rank = circuit["restriction_rank"]
        circuit_histogram[size] = circuit_histogram.get(size, 0) + 1
        restriction_histogram[rank] = restriction_histogram.get(rank, 0) + 1
    need(
        circuit_histogram == {4: 17, 5: 21, 6: 15, 7: 6, 8: 1},
        "exact canonical circuit-size histogram",
    )
    need(
        restriction_histogram == {2: 13, 3: 15, 4: 7, 5: 10, 6: 15},
        "exact canonical circuit restriction-rank histogram",
    )

    coordinate_rows = [
        {
            "normal": list(normal),
            "offset": offset,
            "multiplicity": multiplicity,
        }
        for normal, offset, multiplicity in witness
    ]
    return {
        "record_count": RECORD_COUNT,
        "coordinate_type_count": len(witness),
        "coordinate_multiplicity_sum": V_SIZE,
        "zero_coordinates_per_record": ZERO_COUNT,
        "support_coordinates_per_record": LOCATOR_DEGREE,
        "affine_rank": AFFINE_DIMENSION,
        "secant_rank": AFFINE_DIMENSION,
        "full_vertex_function_rank": full_linear_rank,
        "canonical_star_basis_indices": list(basis),
        "canonical_nonbasis_circuit_count": len(circuits),
        "canonical_circuit_size_histogram": {
            str(key): value for key, value in sorted(circuit_histogram.items())
        },
        "canonical_circuit_restriction_rank_histogram": {
            str(key): value
            for key, value in sorted(restriction_histogram.items())
        },
        "no_affine_three_circuits": True,
        "no_singleton_atoms_in_canonical_circuits": True,
        "pair_count": len(pair_data),
        "minimum_pair_secant_distance": minimum_distance,
        "maximum_pair_zero_coordinates": maximum_pair_zero,
        "minimum_pair_distance_margin_over_grs": (
            minimum_distance - GRS_DISTANCE
        ),
        "minimum_directed_exchange": minimum_exchange,
        "maximum_directed_exchange": maximum_exchange,
        "projective_ternary_direction_count": len(ternary_data),
        "maximum_projective_ternary_zero_coordinates": (
            maximum_ternary_zero
        ),
        "minimum_projective_ternary_secant_distance": (
            minimum_ternary_distance
        ),
        "minimum_projective_ternary_distance_margin_over_grs": (
            minimum_ternary_distance - GRS_DISTANCE
        ),
        "maximum_projective_ternary_zero_direction": list(
            maximum_ternary_zero_direction
        ),
        "projective_ternary_digest": digest_bytes(
            canonical_json(ternary_data)
        ),
        "full_secant_span_distance_certified": False,
        "secant_distance_histogram": {
            str(key): value
            for key, value in sorted(distance_histogram.items())
        },
        "directed_exchange_histogram": {
            str(key): value
            for key, value in sorted(exchange_histogram.items())
        },
        "coordinate_type_digest": digest_bytes(canonical_json(coordinate_rows)),
        "pair_digest": digest_bytes(canonical_json(pair_data)),
        "circuit_digest": digest_bytes(canonical_json(circuits)),
        "coordinate_types": coordinate_rows,
        "circuits": circuits,
    }


def source_bindings() -> list[dict[str, str]]:
    result = []
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        need(path.is_file(), f"source binding exists: {relative}")
        raw = path.read_bytes()
        if relative == "agents.md":
            text = raw.decode("utf-8")
            need(
                "retains 405 labelled conic cases" in text,
                "live workboard 405-case K3 residual",
            )
            need(
                "live active value remains `null`" in text,
                "live workboard null U_paid",
            )
            need(
                "B^MCA_C(1116048) <= 274980728111395087." in text,
                "live workboard KoalaBear target",
            )
        elif relative == "experimental/experiments.tex":
            text = raw.decode("utf-8")
            need(r"\(405\) survivors" in text, "integrated 405-case residual")
            need(r"PR \#1119" in text, "integrated PR 1119 disposition")
            need("is not imported" in text, "unbanked compiler accounting")
        elif relative.endswith("four_row_exact_completion_compiler_v1.json"):
            manifest = json.loads(
                raw.decode("utf-8"),
                object_pairs_hook=reject_duplicate_pairs,
                parse_constant=reject_nonfinite_constant,
            )
            need(isinstance(manifest, dict), "four-row source object")
            rows = manifest.get("rows")
            need(isinstance(rows, list), "four-row source rows")
            matches = [
                row
                for row in rows
                if isinstance(row, dict) and row.get("name") == "KoalaBear MCA"
            ]
            need(len(matches) == 1, "one KoalaBear MCA row")
            row = matches[0]
            parameters = row.get("parameters")
            need(isinstance(parameters, dict), "KoalaBear parameters")
            need(parameters.get("p") == P, "KoalaBear prime")
            need(
                parameters.get("extension_degree") == FIELD_EXTENSION_DEGREE,
                "KoalaBear extension degree",
            )
            need(parameters.get("n") == ROW_N, "KoalaBear length")
            need(parameters.get("k") == ROW_K, "KoalaBear dimension")
            need(parameters.get("a_plus") == 1_116_048, "KoalaBear agreement")
            calibration = row.get("exact_calibration")
            need(isinstance(calibration, dict), "KoalaBear calibration")
            need(
                calibration.get("B_star") == str(B_STAR),
                "KoalaBear exact budget",
            )
            active = row.get("active_completion")
            need(isinstance(active, dict), "KoalaBear active completion")
            atoms = active.get("complete_atom_values")
            need(isinstance(atoms, dict), "KoalaBear active atoms")
            need(atoms.get("U_paid") is None, "live U_paid is null")
            need(
                active.get("witness_exhaustive_partition_sha256") is None,
                "live partition is null",
            )
            need(active.get("closed") is False, "KoalaBear row remains open")
        result.append({"path": relative, "sha256": digest_path(path)})
    return result


def expected_certificate() -> dict[str, Any]:
    exact_results = compile_model()
    document: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "status": STATUS,
        "artifact_kind": ARTIFACT_KIND,
        "architecture_id": ARCHITECTURE_ID,
        "partition_sha256": PARTITION_SHA256,
        "workboard_item": "K3",
        "row_contract": {
            "row": "KoalaBear MCA at 2^-128",
            "object": "MCA",
            "agreement": 1_116_048,
            "row_length": ROW_N,
            "code_dimension": ROW_K,
            "B_star": B_STAR,
            "field_base_prime": P,
            "field_extension_degree": FIELD_EXTENSION_DEGREE,
            "active_U_paid": None,
            "active_partition_sha256": None,
            "unit": "DISTINCT_BAD_SLOPES_PER_RECEIVED_LINE",
        },
        "abstract_carrier_profile": {
            "carrier_size": V_SIZE,
            "locator_degree": LOCATOR_DEGREE,
            "zero_count": ZERO_COUNT,
            "shortened_grs_minimum_distance": GRS_DISTANCE,
            "minimum_pair_exchange": EXCHANGE_FLOOR,
            "candidate_record_count": RECORD_COUNT,
            "unit": "ABSTRACT_F_P_VALUED_CARRIER_RECORDS_NOT_DEPLOYED_SLOPES",
        },
        "construction": {
            "vertex_indices": list(VERTEX_INDICES),
            "vertex_encoding": "EIGHT_SIGN_COORDINATES_FROM_BINARY_INDEX",
            "coordinate_value": "DOT_VERTEX_NORMAL_MINUS_AFFINE_OFFSET_MOD_P",
            "declared_empty_affine_level": 99,
            "sealed_witness_sha256": WITNESS_SHA256,
            "ambient_affine_dimension": AFFINE_DIMENSION,
            "scalar_extension": (
                "F_P_VALUES_VIEWED_IN_F_P6_PRESERVE_HAMMING_WEIGHT_AND_"
                "BASE_FIELD_RANK"
            ),
        },
        "exact_results": exact_results,
        "route_cut": {
            "falsified_inference": (
                "LISTED_KOALABEAR_SCALE_CARDINALITIES_PLUS_AFFINE_SECANT_"
                "RANK_8_PLUS_"
                "SELECTED_PAIR_AND_ALL_PROJECTIVE_TERNARY_SECANT_DISTANCE_"
                "THRESHOLDS_PLUS_PAIR_EXCHANGE_FLOOR_PLUS_60_BOUNDED_"
                "CIRCUITS_PLUS_NO_SINGLETON_PLUS_CIRCUIT_RESTRICTION_RANK_"
                "DO_NOT_IMPLY_CAP_68_OR_CONSTITUTE_SOURCE_BOUND_OWNER_"
                "EVIDENCE"
            ),
            "cap_68_follows_from_listed_coarse_axioms": False,
            "source_bound_owner_evidence_constituted": False,
            "all_projective_ternary_secants_checked": True,
            "full_secant_span_distance_certified": False,
            "actual_grs_subcode_constructed": False,
            "full_primitive_69_point_theorem_refuted": False,
            "required_new_input": (
                "FULL_ARBITRARY_COEFFICIENT_SECANT_SPAN_GRS_EMBEDDING_OR_"
                "POLYNOMIAL_LOCATOR_SOURCE_QUOTIENT_HILBERT_BURCH_STRUCTURE_"
                "OR_SAME_RECORD_ACTIVE_OWNER_SEMANTICS"
            ),
        },
        "omitted_load_bearing_structure": [
            "NO_FULL_ARBITRARY_COEFFICIENT_SECANT_SPAN_DISTANCE_CERTIFICATE",
            "NO_ACTUAL_GRS_EVALUATION_SUBCODE_EMBEDDING",
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
            "U_paid_before": None,
            "U_paid_after": None,
            "B_remaining_before": None,
            "B_remaining_after": None,
            "row_budget_B_star": B_STAR,
            "additional_charge": 0,
            "cap_68_proved": False,
            "equality_wall_paid": False,
            "row_closed": False,
            "terminal": (
                "ROUTE_CUT_PAIRWISE_TERNARY_CIRCUIT_INFERENCE_REQUIRES_"
                "FULL_SPAN_GRS_POLYNOMIAL_OR_OWNER_INPUT"
            ),
        },
        "audit": {
            "proof": "EXACT_FINITE_COUNTERMODEL_TO_A_WEAKENED_INFERENCE",
            "empirical_evidence": (
                "WITNESS_OPTIMIZATION_AND_FULL_SPAN_SEARCH_ARE_NOT_USED_"
                "AS_PROOF"
            ),
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
    value = strict_decode(path.read_bytes())
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
            "architecture",
            lambda d: d.__setitem__("architecture_id", "wrong"),
        ),
        (
            "partition",
            lambda d: d.__setitem__("partition_sha256", "0" * 64),
        ),
        (
            "carrier",
            lambda d: d["abstract_carrier_profile"].__setitem__(
                "carrier_size", V_SIZE - 1
            ),
        ),
        (
            "locator",
            lambda d: d["abstract_carrier_profile"].__setitem__(
                "locator_degree", LOCATOR_DEGREE - 1
            ),
        ),
        (
            "grs-distance",
            lambda d: d["abstract_carrier_profile"].__setitem__(
                "shortened_grs_minimum_distance", GRS_DISTANCE - 1
            ),
        ),
        (
            "exchange-floor",
            lambda d: d["abstract_carrier_profile"].__setitem__(
                "minimum_pair_exchange", EXCHANGE_FLOOR - 1
            ),
        ),
        (
            "witness-seal",
            lambda d: d["construction"].__setitem__(
                "sealed_witness_sha256", "0" * 64
            ),
        ),
        (
            "record-count",
            lambda d: d["exact_results"].__setitem__("record_count", 68),
        ),
        (
            "type-count",
            lambda d: d["exact_results"].__setitem__(
                "coordinate_type_count", 224
            ),
        ),
        (
            "affine-rank",
            lambda d: d["exact_results"].__setitem__("affine_rank", 7),
        ),
        (
            "secant-rank",
            lambda d: d["exact_results"].__setitem__("secant_rank", 7),
        ),
        (
            "full-rank",
            lambda d: d["exact_results"].__setitem__(
                "full_vertex_function_rank", 8
            ),
        ),
        (
            "pair-distance",
            lambda d: d["exact_results"].__setitem__(
                "minimum_pair_secant_distance", GRS_DISTANCE - 1
            ),
        ),
        (
            "pair-distance-margin",
            lambda d: d["exact_results"].__setitem__(
                "minimum_pair_distance_margin_over_grs", 0
            ),
        ),
        (
            "ternary-direction-count",
            lambda d: d["exact_results"].__setitem__(
                "projective_ternary_direction_count", 3_279
            ),
        ),
        (
            "ternary-distance",
            lambda d: d["exact_results"].__setitem__(
                "minimum_projective_ternary_secant_distance",
                GRS_DISTANCE - 1,
            ),
        ),
        (
            "ternary-digest",
            lambda d: d["exact_results"].__setitem__(
                "projective_ternary_digest", "0" * 64
            ),
        ),
        (
            "exchange",
            lambda d: d["exact_results"].__setitem__(
                "minimum_directed_exchange", EXCHANGE_FLOOR - 1
            ),
        ),
        (
            "pair-count",
            lambda d: d["exact_results"].__setitem__("pair_count", 2345),
        ),
        (
            "pair-digest",
            lambda d: d["exact_results"].__setitem__(
                "pair_digest", "0" * 64
            ),
        ),
        (
            "coordinate-normal",
            lambda d: d["exact_results"]["coordinate_types"][0][
                "normal"
            ].__setitem__(0, 1),
        ),
        (
            "coordinate-offset",
            lambda d: d["exact_results"]["coordinate_types"][0].__setitem__(
                "offset", 1
            ),
        ),
        (
            "coordinate-multiplicity",
            lambda d: d["exact_results"]["coordinate_types"][0].__setitem__(
                "multiplicity", 1
            ),
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
            "singleton",
            lambda d: d["exact_results"].__setitem__(
                "no_singleton_atoms_in_canonical_circuits", False
            ),
        ),
        (
            "circuit-rank",
            lambda d: d["exact_results"]["circuits"][0].__setitem__(
                "restriction_rank", 9
            ),
        ),
        (
            "cap68",
            lambda d: d["route_cut"].__setitem__(
                "cap_68_follows_from_listed_coarse_axioms", True
            ),
        ),
        (
            "grs-subcode",
            lambda d: d["route_cut"].__setitem__(
                "actual_grs_subcode_constructed", True
            ),
        ),
        (
            "full-span",
            lambda d: d["route_cut"].__setitem__(
                "full_secant_span_distance_certified", True
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
            lambda d: d["closure_state"].__setitem__("additional_charge", 1),
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
    ]


def run_tamper_selftest(expected: dict[str, Any]) -> int:
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


def run_raw_parser_selftest(expected: dict[str, Any]) -> int:
    need(strict_decode(canonical_json(expected)) == expected, "canonical parser")
    hostile = (
        b'{"schema":"first","schema":"second"}\n',
        b'{ "a":1}\n',
        b'{"b":1,"a":2}\n',
        b'{"a":NaN}\n',
        b'{"a":1}\n{"b":2}\n',
    )
    rejected = 0
    for raw in hostile:
        try:
            strict_decode(raw)
        except (VerificationError, json.JSONDecodeError):
            rejected += 1
        else:
            raise VerificationError("raw JSON tamper escaped")
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
        raw_rejected = run_raw_parser_selftest(expected)
        total = len(mutations()) + 5
        print(
            "PASS: "
            f"{rejected + raw_rejected}/{total} mutations rejected"
        )
        return

    results = expected["exact_results"]
    print("PASS: KoalaBear equality-wall ternary-secant/circuit route cut")
    print(f"checks={CHECKS}")
    print(f"records={results['record_count']}")
    print(f"coordinate_types={results['coordinate_type_count']}")
    print(f"secant_rank={results['secant_rank']}")
    print(
        "minimum_pair_secant_distance="
        f"{results['minimum_pair_secant_distance']}"
    )
    print(
        "minimum_projective_ternary_secant_distance="
        f"{results['minimum_projective_ternary_secant_distance']}"
    )
    print(f"minimum_directed_exchange={results['minimum_directed_exchange']}")
    print(
        "canonical_circuits="
        f"{results['canonical_nonbasis_circuit_count']}"
    )
    print("ledger_movement=0")
    print(
        "terminal=ROUTE_CUT_PAIRWISE_TERNARY_CIRCUIT_INFERENCE_REQUIRES_"
        "FULL_SPAN_GRS_POLYNOMIAL_OR_OWNER_INPUT"
    )


if __name__ == "__main__":
    try:
        main()
    except (
        OSError,
        ValueError,
        TypeError,
        UnicodeError,
        json.JSONDecodeError,
        VerificationError,
        zlib.error,
    ) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
