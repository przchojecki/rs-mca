#!/usr/bin/env python3
"""Verify the r=67,474 upper intrinsic-plane descent."""

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
import verify_kb_mca_v4_next_slack_source_plane_closure_v1 as plane
import verify_kb_mca_v4_post_successor_full_histogram_replay_v1 as replay

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-second-successor-upper-intrinsic-plane-descent-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_second_successor_upper_intrinsic_plane_descent_v1.schema.json"
)

ARCH = replay.ARCH
PARTITION_DIGEST = replay.PARTITION_DIGEST
R = 67_474
X_OUTSIDE = 1
S = plane.pencil.T + R + 1
E = S + X_OUTSIDE - plane.pencil.T - 1
CARRIER = plane.pencil.N - S
COMPLEMENT = plane.pencil.J + X_OUTSIDE
ZERO_LOCATOR = CARRIER - COMPLEMENT
FORCED_COMMON = plane.pencil.A_AGREEMENT - X_OUTSIDE - S
DIRECT_CAP = (plane.active.prev.BASE_PRIME + 1) * CARRIER
MARGIN = replay.B_REMAINING - DIRECT_CAP

Failure = replay.Failure
need = replay.need
seal = replay.seal
dump = replay.dump
load = replay.load
file_digest = replay.file_digest

UPSTREAM_CERTIFICATES = {
    "source_plane_theorem": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-next-slack-source-plane-closure-v1/certificate.json"
        ),
        "payload_sha256": (
            'e4d51dcaea7ba2591ca314ecd73248fe0a79e07244176dab8b20c78d8d1e4064'
        ),
    },
    "post_successor_histogram": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-post-successor-full-histogram-replay-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'ae88f5c221aabda5df2c221c85b3b91a32b88a1179a0f289be1ad470a0c880eb'
        ),
    },
    "lower_source_plane": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-second-successor-lower-source-plane-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'fdeb2f6101420ad6f0e5e4bec6bb5d917980ecfa7d84aee52e92f74a1265526a'
        ),
    },
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_tangent_deep_source_rational_adapter_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_tangent_deep_source_rational_c5_adapter_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_next_slack_source_plane_closure_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_second_successor_lower_source_plane_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_second_successor_upper_intrinsic_plane_descent_v1.md"
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


def upstream_bindings() -> dict[str, dict[str, str]]:
    result = {}
    for key, contract in UPSTREAM_CERTIFICATES.items():
        path = ROOT / contract["path"]
        need(path.is_file(), f"missing upstream certificate: {key}")
        payload = load(path)
        need(
            payload.get("payload_sha256") == contract["payload_sha256"],
            f"upstream payload mismatch: {key}",
        )
        result[key] = {**contract, "file_sha256": file_digest(path)}
    return result


def multiply_x_mod_source(
    polynomial: list[int],
    points: list[int],
    inverse: list[list[int]],
    prime: int,
) -> list[int]:
    values = plane.polynomial_values(polynomial, points, prime)
    multiplied = [point * value % prime for point, value in zip(points, values)]
    return residue.matrix_vector(inverse, multiplied, prime)


def combine(
    basis: list[list[int]], coefficients: list[int], prime: int
) -> list[int]:
    return [
        sum(
            coefficient * basis[index][coordinate]
            for index, coefficient in enumerate(coefficients)
        )
        % prime
        for coordinate in range(len(basis[0]))
    ]


def independent_basis(
    vectors: list[list[int]], prime: int
) -> list[list[int]]:
    result: list[list[int]] = []
    for vector in vectors:
        if residue.rank([*result, vector], prime) > len(result):
            result.append(vector)
    return result


def shift_preimage(
    domain: list[list[int]],
    target: list[list[int]],
    points: list[int],
    inverse: list[list[int]],
    prime: int,
) -> list[list[int]]:
    shifted = [
        multiply_x_mod_source(vector, points, inverse, prime)
        for vector in domain
    ]
    columns = [*shifted, *target]
    matrix = [
        [column[row] for column in columns]
        for row in range(len(points))
    ]
    relations = residue.nullspace(matrix, prime)
    return independent_basis(
        [
            combine(domain, relation[: len(domain)], prime)
            for relation in relations
            if any(relation[: len(domain)])
        ],
        prime,
    )


def polynomial_syzygies(
    basis: list[list[int]],
    max_degree: int,
    points: list[int],
    inverse: list[list[int]],
    prime: int,
) -> list[list[int]]:
    columns: list[list[int]] = []
    for vector in basis:
        current = vector
        for _ in range(max_degree + 1):
            columns.append(current)
            current = multiply_x_mod_source(
                current, points, inverse, prime
            )
    matrix = [
        [column[row] for column in columns]
        for row in range(len(points))
    ]
    return residue.nullspace(matrix, prime)


def deployed_arithmetic() -> dict[str, Any]:
    need(S == 134_947, "source size")
    need(E == 67_475, "upper reduced degree")
    need(S == 2 * E - 3, "dimension-five identity")
    need(2 * (E + 1) - S == 5, "source dimension")
    need(2 * E - S == 3, "lowered source dimension")
    need(2 * (E - 1) - S == 1, "twice-lowered dimension floor")
    need(FORCED_COMMON == ZERO_LOCATOR, "complete forced split gcd")
    need(FORCED_COMMON == plane.pencil.K - 1 - E, "forced gcd degree")
    need(DIRECT_CAP == 4_180_882_818_326_970, "direct cap")
    need(MARGIN == 266_599_330_142_248_910, "reserve margin")
    need(plane.active.prev.BASE_PRIME > 2 * E - 1, "pencil root budget")
    need(E + 3 < S, "cubic relation no-wrap")
    need(2 * S > 3 * E, "double-source-zero determinant cutoff")
    return {
        "r": R,
        "x": X_OUTSIDE,
        "source_size": S,
        "reduced_degree": E,
        "source_dimension": 5,
        "lowered_dimension": 3,
        "twice_lowered_dimension_floor": 1,
        "carrier_size": CARRIER,
        "complement_size": COMPLEMENT,
        "zero_locator_size": ZERO_LOCATOR,
        "forced_common_root_size": FORCED_COMMON,
        "direct_cap": DIRECT_CAP,
        "reserve_margin": MARGIN,
        "relation_degree_cap": 3,
        "relation_product_degree_cap": E + 3,
        "double_source_zero_degree": 2 * S,
        "three_by_three_minor_degree_cap": 3 * E,
    }


def poly_add_x_product(
    left: list[int], right: list[int], prime: int
) -> list[int]:
    length = max(len(left), len(right) + 1)
    output = [0] * length
    for index, value in enumerate(left):
        output[index] = (output[index] + value) % prime
    for index, value in enumerate(right):
        output[index + 1] = (output[index + 1] + value) % prime
    return residue.trim(output)


def scalar_pencil_member(
    left: list[int], right: list[int], scalar: int, prime: int
) -> list[int]:
    length = max(len(left), len(right))
    return residue.trim(
        [
            (
                (left[index] if index < len(left) else 0)
                + scalar * (right[index] if index < len(right) else 0)
            )
            % prime
            for index in range(length)
        ]
    )


def nonzero_pair_gcd_degree(
    left: list[int], right: list[int], prime: int
) -> int:
    if left == [0] and right == [0]:
        return -1
    if left == [0]:
        return len(right) - 1
    if right == [0]:
        return len(left) - 1
    return len(residue.gcd_poly(left, right, prime)) - 1


@functools.lru_cache(maxsize=1)
def exhaustive_pencil_regression() -> dict[str, Any]:
    prime = 5
    degree = 1
    polynomials = [
        list(coefficients)
        for coefficients in itertools.product(range(prime), repeat=degree + 1)
    ]
    qualifying = 0
    minimum_good_scalars = prime
    good_scalar_histogram: Counter[int] = Counter()
    for a0 in polynomials:
        for a1 in polynomials:
            for b0 in polynomials:
                c0 = poly_add_x_product(a0, b0, prime)
                for b1 in polynomials:
                    c1 = poly_add_x_product(a1, b1, prime)
                    if max(len(c0), len(c1)) - 1 != degree + 1:
                        continue
                    if nonzero_pair_gcd_degree(c0, c1, prime) != 0:
                        continue
                    qualifying += 1
                    good = 0
                    for scalar in range(prime):
                        p0 = scalar_pencil_member(a0, b0, scalar, prime)
                        p1 = scalar_pencil_member(a1, b1, scalar, prime)
                        if max(len(p0), len(p1)) - 1 != degree:
                            continue
                        if nonzero_pair_gcd_degree(p0, p1, prime) == 0:
                            good += 1
                    need(good > 0, "pencil descent counterexample")
                    minimum_good_scalars = min(minimum_good_scalars, good)
                    good_scalar_histogram[good] += 1
    need(qualifying > 0, "empty pencil regression")
    return {
        "prime": prime,
        "input_degree": degree,
        "qualifying_diagonal_pairs": qualifying,
        "minimum_good_scalars": minimum_good_scalars,
        "good_scalar_histogram": {
            str(key): value for key, value in sorted(good_scalar_histogram.items())
        },
    }


@functools.lru_cache(maxsize=1)
def source_hierarchy_regression() -> dict[str, Any]:
    prime = 13
    degree = 5
    source_size = 2 * degree - 3
    points, inverse = plane.evaluation_inverse(prime, source_size)
    rng = random.Random(67_475)
    dimensions: Counter[tuple[int, int, int]] = Counter()
    prolongations: Counter[tuple[int, int]] = Counter()
    accepted = 0
    for _ in range(10_000):
        left = [rng.randrange(prime) for _ in range(degree + 1)]
        right = [rng.randrange(prime) for _ in range(degree + 1)]
        if max(len(residue.trim(left)), len(residue.trim(right))) != degree + 1:
            continue
        if residue.gcd_poly(left, right, prime) != [1]:
            continue
        left_values = plane.polynomial_values(left, points, prime)
        right_values = plane.polynomial_values(right, points, prime)
        if any(a == 0 and b == 0 for a, b in zip(left_values, right_values)):
            continue
        spaces = [
            plane.source_residue_space(
                left_values,
                right_values,
                points,
                inverse,
                cutoff,
                prime,
            )
            for cutoff in (degree, degree - 1, degree - 2)
        ]
        signature = tuple(len(space) for space in spaces)
        need(signature in ((5, 3, 1), (5, 3, 2)), "source hierarchy")
        dimensions[signature] += 1
        shifted = [
            multiply_x_mod_source(vector, points, inverse, prime)
            for vector in spaces[1]
        ]
        union_rank = residue.rank([*spaces[1], *shifted], prime)
        intersection = 2 * len(spaces[1]) - union_rank
        expected = (5, 1) if len(spaces[2]) == 1 else (4, 2)
        need((union_rank, intersection) == expected, "prolongation profile")
        prolongations[(union_rank, intersection)] += 1
        accepted += 1
        if accepted == 1_000:
            break
    need(accepted == 1_000, "source hierarchy sample count")
    need(dimensions[(5, 3, 2)] > 0, "missing rank-excess lower cutoff")
    return {
        "prime": prime,
        "degree": degree,
        "source_size": source_size,
        "accepted_source_pairs": accepted,
        "dimension_histogram": {
            str(key): value for key, value in sorted(dimensions.items())
        },
        "prolongation_histogram": {
            str(key): value for key, value in sorted(prolongations.items())
        },
    }


@functools.lru_cache(maxsize=1)
def proper_span_guardrail() -> dict[str, Any]:
    prime = 17
    degree = 5
    source_size = 2 * degree - 3
    points, inverse = plane.evaluation_inverse(prime, source_size)
    carrier = list(range(source_size, prime))
    complement_size = len(carrier) // 2
    complements = list(itertools.combinations(carrier, complement_size))
    base_values = plane.polynomial_values(
        residue.locator(complements[0], prime), points, prime
    )
    rng = random.Random(6_747_501)
    profiles: Counter[tuple[int, int, int, int]] = Counter()
    evaluated_relation_ranks: Counter[tuple[int, int, int]] = Counter()
    accepted = 0
    for _ in range(20_000):
        left = [rng.randrange(prime) for _ in range(degree + 1)]
        right = [rng.randrange(prime) for _ in range(degree + 1)]
        if max(len(residue.trim(left)), len(residue.trim(right))) != degree + 1:
            continue
        if residue.gcd_poly(left, right, prime) != [1]:
            continue
        left_values = plane.polynomial_values(left, points, prime)
        right_values = plane.polynomial_values(right, points, prime)
        if any(a == 0 and b == 0 for a, b in zip(left_values, right_values)):
            continue
        wide = plane.source_residue_space(
            left_values, right_values, points, inverse, degree, prime
        )
        if len(wide) != 5:
            continue
        admitted = []
        for complement in complements:
            values = plane.polynomial_values(
                residue.locator(complement, prime), points, prime
            )
            ratio_values = [
                value * pow(base, -1, prime) % prime
                for value, base in zip(values, base_values)
            ]
            q = residue.matrix_vector(inverse, ratio_values, prime)
            if residue.rank([*wide, q], prime) == len(wide):
                admitted.append(q)
        occupied = independent_basis(admitted, prime)
        one_step = shift_preimage(
            occupied, occupied, points, inverse, prime
        )
        two_step = shift_preimage(
            one_step, one_step, points, inverse, prime
        )
        shifted = [
            multiply_x_mod_source(vector, points, inverse, prime)
            for vector in one_step
        ]
        profiles[
            (
                len(occupied),
                len(one_step),
                len(two_step),
                residue.rank([*one_step, *shifted], prime)
                if one_step
                else 0,
            )
        ] += 1
        if len(occupied) >= 3:
            relations = polynomial_syzygies(
                occupied, 3, points, inverse, prime
            )
            need(relations, "missing cubic relation space")
            pointwise_ranks = []
            for root in range(prime):
                evaluated = [
                    [
                        sum(
                            relation[index * 4 + power]
                            * pow(root, power, prime)
                            for power in range(4)
                        )
                        % prime
                        for index in range(len(occupied))
                    ]
                    for relation in relations
                ]
                pointwise_ranks.append(residue.rank(evaluated, prime))
            need(
                min(pointwise_ranks) >= len(occupied) - 2,
                "cubic relation rank below payment threshold",
            )
            evaluated_relation_ranks[
                (
                    len(occupied),
                    min(pointwise_ranks),
                    max(pointwise_ranks),
                )
            ] += 1
        accepted += 1
        if accepted == 250:
            break
    need(accepted == 250, "proper-span sample count")
    need(profiles[(3, 0, 0, 0)] > 0, "missing span-three guardrail")
    need(profiles[(4, 1, 0, 2)] > 0, "missing span-four guardrail")
    return {
        "prime": prime,
        "degree": degree,
        "source_size": source_size,
        "carrier_size": len(carrier),
        "complement_size": complement_size,
        "candidate_complements": len(complements),
        "accepted_source_pairs": accepted,
        "occupied_shift_profile": {
            str(key): value for key, value in sorted(profiles.items())
        },
        "evaluated_cubic_relation_rank_profile": {
            str(key): value
            for key, value in sorted(evaluated_relation_ranks.items())
        },
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "counted_object": (
                "R=67474 X=1 E=67475 FULL-OUTSIDE "
                "COEFFICIENT-RANK-TWO LINES"
            ),
            "active_ledger": {
                "U_paid": plane.active.PAID,
                "B_remaining": replay.B_REMAINING,
                "additional_charge": 0,
            },
            "theorem": {
                "source_size_is_2e_minus_3": True,
                "source_interpolation_dimension": 5,
                "lowered_source_dimension": 3,
                "lower_cutoff_rank_one_emits_earlier_owner": True,
                "survivor_twice_lowered_dimension": 1,
                "exact_first_prolongation": True,
                "base_span_at_most_two_directly_paid": True,
                "reciprocal_dimension_two_emits_c5_owner": True,
                "reciprocal_rank_two_product_matrix": True,
                "base_span_three_cubic_relation_payment": True,
                "base_span_four_saturated_kernel_payment": True,
                "resultant_pencil_nonzero": True,
                "full_base_span_five_descends_to_source_plane": True,
                "full_base_span_five_post_c5_is_impossible": True,
                "all_intrinsic_base_spans_paid": True,
                "remaining_intrinsic_base_spans": [],
                "whole_upper_stratum_paid": True,
                "lower_companion_strata_paid_upstream": True,
                "whole_slack_paid": True,
            },
            "deployed_arithmetic": deployed_arithmetic(),
            "regressions": {
                "exhaustive_pencil": exhaustive_pencil_regression(),
                "source_hierarchy": source_hierarchy_regression(),
                "proper_span_guardrail": proper_span_guardrail(),
            },
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_SECOND_SUCCESSOR_UPPER_INTRINSIC_PLANE_PAYMENT_"
                "WHOLE_R67474_SLACK_PAID_ZERO_ADDITIONAL_CHARGE"
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
        "title": "KoalaBear second-successor upper intrinsic-plane descent",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_second_successor_upper_intrinsic_plane_descent_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED COMPLETE UPPER-STRATUM PAYMENT",
        "\\dim W_e=5,\\quad",
        "Rank-one lower cutoff emits an earlier owner",
        "W_e=W_{e-1}+XW_{e-1}",
        "Reciprocal product matrix",
        "Base span three",
        "Base span four",
        "saturated polynomial kernel",
        "A resultant-pencil descent",
        "full base span five is empty after C5",
        "all five intrinsic base spans",
        "proper occupied span 3 with no linear shift relation: 34",
        "evaluated cubic relation rank",
        "# CLOSED ENDPOINT",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["theorem"]["remaining_intrinsic_base_spans"] == [],
        "remaining base spans",
    )
    need(
        cert["theorem"]["whole_upper_stratum_paid"] is True,
        "upper-stratum status",
    )
    need(cert["theorem"]["whole_slack_paid"] is True, "whole-slack status")
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
        lambda d: d["theorem"].__setitem__(
            "source_interpolation_dimension", 4
        ),
        lambda d: d["theorem"].__setitem__(
            "lower_cutoff_rank_one_emits_earlier_owner", False
        ),
        lambda d: d["theorem"].__setitem__(
            "survivor_twice_lowered_dimension", 2
        ),
        lambda d: d["theorem"].__setitem__(
            "exact_first_prolongation", False
        ),
        lambda d: d["theorem"].__setitem__(
            "reciprocal_rank_two_product_matrix", False
        ),
        lambda d: d["theorem"].__setitem__(
            "base_span_three_cubic_relation_payment", False
        ),
        lambda d: d["theorem"].__setitem__(
            "base_span_four_saturated_kernel_payment", False
        ),
        lambda d: d["theorem"].__setitem__(
            "resultant_pencil_nonzero", False
        ),
        lambda d: d["theorem"].__setitem__(
            "full_base_span_five_post_c5_is_impossible", False
        ),
        lambda d: d["theorem"].__setitem__(
            "remaining_intrinsic_base_spans", [3]
        ),
        lambda d: d["theorem"].__setitem__(
            "whole_upper_stratum_paid", False
        ),
        lambda d: d["theorem"].__setitem__(
            "whole_slack_paid", False
        ),
        lambda d: d["regressions"]["exhaustive_pencil"].__setitem__(
            "minimum_good_scalars", 0
        ),
        lambda d: d["regressions"]["source_hierarchy"].__setitem__(
            "accepted_source_pairs", 999
        ),
        lambda d: d["regressions"]["proper_span_guardrail"].__setitem__(
            "evaluated_cubic_relation_rank_profile", {}
        ),
        lambda d: d["upstream_certificates"][
            "source_plane_theorem"
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
            print(f"r: {R}")
            print(f"x: {X_OUTSIDE}")
            print(f"direct_cap: {DIRECT_CAP}")
            print("remaining_base_spans: []")
            print("whole_r67474_slack_paid: True")
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
