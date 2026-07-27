#!/usr/bin/env python3
"""Verify the KoalaBear r=67,472 source-plane branch closure."""

from __future__ import annotations

import argparse
import copy
import functools
import itertools
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import verify_kb_mca_v4_first_gap_complement_locator_linearization_v1 as residue
import verify_kb_mca_v4_first_gap_source_interpolation_pencil_v1 as pencil
import verify_kb_mca_v4_first_gap_source_pencil_image_owner_v1 as active

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-next-slack-source-plane-closure-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_next_slack_source_plane_closure_v1.schema.json"
)

ARCH = active.ARCH
PARTITION_DIGEST = active.partition()["partition_sha256"]

R_NEXT = pencil.T
X_NEXT = 1
SOURCE_SIZE = pencil.T + R_NEXT + 1
REDUCED_DEGREE = pencil.T + 1
COMMON_GCD_DEGREE = pencil.K - 1 - REDUCED_DEGREE
CARRIER_SIZE = pencil.N - SOURCE_SIZE
COMPLEMENT_SIZE = pencil.J + X_NEXT
COMMON_ZERO_SIZE = CARRIER_SIZE - COMPLEMENT_SIZE
PROJECTIVE_POINT_CAP = active.prev.BASE_PRIME + 1
DIRECT_BRANCH_CAP = PROJECTIVE_POINT_CAP * CARRIER_SIZE
RESERVE_MARGIN = active.REMAINING - DIRECT_BRANCH_CAP

Failure = active.Failure
need = active.need
seal = active.seal
dump = active.dump
load = active.load
file_digest = active.file_digest

UPSTREAM_CERTIFICATES = {
    "first_gap_source_interpolation": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-first-gap-source-interpolation-pencil-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '12ee94cc29fe136af4ae9c801fbb1c0ad8291d0be08cf4b51b0ce43c5c910afa'
        ),
    },
    "first_gap_locator_linearization": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-first-gap-complement-locator-linearization-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '2e324cf51a372b92741e6efeb114c8b8e458a2d20e47c8f5899d94470ea57963'
        ),
    },
    "first_gap_projective_rank": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-first-gap-projective-residue-c5-rank-dichotomy-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '99bb10644bf532974e723e47c5875494598d5ed2ea5507c15d4111916272f92c'
        ),
    },
    "seven_owner_partition": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-first-gap-source-pencil-image-owner-v1/"
            "manifest.json"
        ),
        "payload_sha256": (
            '0ba2155dea1a337b17fe23d7da303b5fa3b13d4958777b977a9e768842072bf5'
        ),
    },
    "seven_owner_histogram": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-post-first-gap-full-histogram-replay-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '2b7006af6a7249d121b19e806e0e6bb4bf3abb17d462ef2a0aa28aeeaf6b52cb'
        ),
    },
}

SOURCE_PATHS = [
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
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_source_pencil_image_owner_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_first_gap_full_histogram_replay_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_next_slack_source_plane_closure_v1.md"
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


def polynomial_values(
    polynomial: list[int], points: Iterable[int], prime: int
) -> list[int]:
    return [residue.evaluate(polynomial, point, prime) for point in points]


def evaluation_inverse(
    prime: int, source_size: int
) -> tuple[list[int], list[list[int]]]:
    points = list(range(source_size))
    vandermonde = [
        [pow(point, exponent, prime) for exponent in range(source_size)]
        for point in points
    ]
    return points, residue.inverse_matrix(vandermonde, prime)


def multiplication_constraint(
    multipliers: list[list[int]],
    points: list[int],
    inverse: list[list[int]],
    degree: int,
    prime: int,
) -> list[list[int]]:
    source_size = len(points)
    parity_count = source_size - (degree + 1)
    need(parity_count >= 0, "negative parity count")
    if parity_count == 0:
        return []

    columns = []
    for exponent in range(source_size):
        monomial = [pow(point, exponent, prime) for point in points]
        output = []
        for multiplier in multipliers:
            product = [
                multiplier[index] * monomial[index] % prime
                for index in range(source_size)
            ]
            coefficients = residue.matrix_vector(inverse, product, prime)
            output.extend(coefficients[degree + 1 :])
        columns.append(output)
    return [
        [columns[column][row] for column in range(source_size)]
        for row in range(len(multipliers) * parity_count)
    ]


def source_residue_space(
    left: list[int],
    right: list[int],
    points: list[int],
    inverse: list[list[int]],
    degree: int,
    prime: int,
) -> list[list[int]]:
    return residue.nullspace(
        multiplication_constraint(
            [left, right], points, inverse, degree, prime
        ),
        prime,
    )


def reciprocal_dimension(
    basis: list[list[int]],
    points: list[int],
    inverse: list[list[int]],
    degree: int,
    prime: int,
) -> int:
    basis_values = [
        polynomial_values(polynomial, points, prime)
        for polynomial in basis
    ]
    matrix = multiplication_constraint(
        basis_values, points, inverse, degree, prime
    )
    return len(points) - residue.rank(matrix, prime)


@functools.lru_cache(maxsize=1)
def exhaustive_coprime_control() -> dict[str, Any]:
    prime = 7
    degree = 3
    source_size = 2 * degree - 1
    points, inverse = evaluation_inverse(prime, source_size)
    histogram: Counter[tuple[int, int]] = Counter()
    accepted = 0

    for left_low in itertools.product(range(prime), repeat=degree):
        left = [*left_low, 1]
        left_values = polynomial_values(left, points, prime)
        for right in itertools.product(range(prime), repeat=degree):
            right_list = list(right)
            if residue.gcd_poly(left, right_list, prime) != [1]:
                continue
            right_values = polynomial_values(right_list, points, prime)
            if any(
                a == 0 and b == 0
                for a, b in zip(left_values, right_values)
            ):
                continue
            source_basis = source_residue_space(
                left_values,
                right_values,
                points,
                inverse,
                degree,
                prime,
            )
            reciprocal = reciprocal_dimension(
                source_basis, points, inverse, degree, prime
            )
            histogram[(len(source_basis), reciprocal)] += 1
            accepted += 1
            need(len(source_basis) == 3, "toy source-plane dimension")
            need(reciprocal == 2, "toy reciprocal dimension")

    need(accepted == 100_842, "exhaustive accepted count")
    need(histogram == Counter({(3, 2): 100_842}), "exhaustive histogram")
    return {
        "field_prime": prime,
        "source_degree": degree,
        "source_size": source_size,
        "family": (
            "MONIC_DEGREE_3_LEFT_AND_DEGREE_AT_MOST_2_RIGHT_"
            "COPRIME_NO_COMMON_SOURCE_ZERO"
        ),
        "accepted_pairs": accepted,
        "source_dimension_reciprocal_dimension_histogram": {
            f"{key[0]},{key[1]}": histogram[key]
            for key in sorted(histogram)
        },
        "all_exact_degree_coprime_pairs_have_generic_reciprocal_dimension": True,
    }


def rank_excess_degree_defect_control() -> dict[str, Any]:
    prime = 17
    degree = 4
    source_size = 2 * degree - 1
    points, inverse = evaluation_inverse(prime, source_size)
    left = polynomial_values([1], points, prime)
    right = polynomial_values([0, 0, 1], points, prime)
    source_basis = source_residue_space(
        left, right, points, inverse, degree, prime
    )
    reciprocal = reciprocal_dimension(
        source_basis, points, inverse, degree, prime
    )
    need(len(source_basis) == 3, "guardrail source dimension")
    need(reciprocal == 3, "guardrail rank excess")

    monomials = [
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
    ]
    need(
        residue.rank(source_basis, prime) == residue.rank(monomials, prime),
        "guardrail source span rank",
    )
    need(
        residue.rank([*source_basis, *monomials], prime)
        == len(source_basis),
        "guardrail source span",
    )
    return {
        "field_prime": prime,
        "source_degree": degree,
        "source_size": source_size,
        "source_plane_dimension": len(source_basis),
        "reciprocal_kernel_dimension": reciprocal,
        "source_plane": "SPAN_OF_1_X_X2",
        "translated_source_pair": ["1", "X2"],
        "actual_reduced_degree": 2,
        "required_reduced_degree": degree,
        "rejected_by_exact_degree_guard": True,
    }


def projective_point_control() -> dict[str, Any]:
    prime = 3
    counts = {
        dimension: (prime**dimension - 1) // (prime - 1)
        for dimension in [1, 2, 3]
    }
    need(counts == {1: 1, 2: 4, 3: 13}, "projective point counts")
    return {
        "field_prime": prime,
        "base_span_projective_point_counts": {
            str(key): value for key, value in counts.items()
        },
    }


def deployed_arithmetic() -> dict[str, Any]:
    source_rational_limit = (SOURCE_SIZE - 1) // 2
    degree_lower = source_rational_limit + 1
    degree_upper = SOURCE_SIZE + X_NEXT - pencil.T - 1
    forced_common_roots = pencil.A_AGREEMENT - X_NEXT - SOURCE_SIZE
    source_nullity_floor = 2 * (REDUCED_DEGREE + 1) - SOURCE_SIZE
    parity_codimension = SOURCE_SIZE - (REDUCED_DEGREE + 1)

    need(R_NEXT == 67_472, "next slack")
    need(SOURCE_SIZE == 134_945, "next source size")
    need(REDUCED_DEGREE == 67_473, "next reduced degree")
    need(SOURCE_SIZE == 2 * REDUCED_DEGREE - 1, "plane threshold")
    need(source_rational_limit == pencil.T, "source rational limit")
    need(degree_lower == REDUCED_DEGREE, "degree lower")
    need(degree_upper == REDUCED_DEGREE, "degree upper")
    need(forced_common_roots == COMMON_GCD_DEGREE, "full gcd")
    need(COMMON_ZERO_SIZE == COMMON_GCD_DEGREE, "common zero size")
    need(CARRIER_SIZE == 1_962_207, "carrier size")
    need(COMPLEMENT_SIZE == 981_105, "complement size")
    need(source_nullity_floor == 3, "source nullity floor")
    need(parity_codimension == REDUCED_DEGREE - 2, "parity codimension")
    need(PROJECTIVE_POINT_CAP == 2_130_706_434, "projective cap")
    need(DIRECT_BRANCH_CAP == 4_180_887_079_739_838, "direct cap")
    need(RESERVE_MARGIN == 266_599_325_880_836_042, "reserve margin")
    need(DIRECT_BRANCH_CAP < active.REMAINING, "direct branch fits")

    return {
        "base_field_order": active.prev.BASE_PRIME,
        "n": pencil.N,
        "k": pencil.K,
        "agreement": pencil.A_AGREEMENT,
        "j": pencil.J,
        "t": pencil.T,
        "r": R_NEXT,
        "x": X_NEXT,
        "source_size": SOURCE_SIZE,
        "source_rational_limit": source_rational_limit,
        "reduced_degree_lower": degree_lower,
        "reduced_degree_upper": degree_upper,
        "reduced_degree": REDUCED_DEGREE,
        "full_gcd_degree": COMMON_GCD_DEGREE,
        "carrier_size": CARRIER_SIZE,
        "common_zero_size": COMMON_ZERO_SIZE,
        "complement_size": COMPLEMENT_SIZE,
        "source_kernel_ambient_dimension": 2 * (REDUCED_DEGREE + 1),
        "source_constraint_count": SOURCE_SIZE,
        "source_kernel_nullity_floor": source_nullity_floor,
        "source_kernel_dimension": 3,
        "source_parity_codimension": parity_codimension,
        "triple_reciprocal_rows": 3 * parity_codimension,
        "triple_reciprocal_columns": SOURCE_SIZE,
        "base_span_at_most_two_projective_point_cap": PROJECTIVE_POINT_CAP,
        "finite_image_domain_size": CARRIER_SIZE,
        "direct_branch_cap": DIRECT_BRANCH_CAP,
        "current_remaining_reserve": active.REMAINING,
        "reserve_margin": RESERVE_MARGIN,
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
                "next_slack": R_NEXT,
                "source_constraints_independent": True,
                "source_residue_dimension": 3,
                "base_span_dimensions": [1, 2, 3],
                "base_span_at_most_two_directly_paid": True,
                "direct_branch_uses_map_injectivity": False,
                "full_base_span_reciprocal_dimension_two_owned_by_c5": True,
                "full_base_span_rank_excess_polynomial_adjugate_zero": True,
                "full_base_span_rank_excess_rational_normal_form": True,
                "rank_excess_contradicts_coprime_exact_degree": True,
                "post_c5_full_base_span_empty": True,
                "complete_next_slack_paid": True,
                "next_open_slack": R_NEXT + 1,
                "row_closed": False,
            },
            "deployed_arithmetic": deployed_arithmetic(),
            "finite_controls": {
                "exhaustive_coprime_family": exhaustive_coprime_control(),
                "rank_excess_degree_defect": rank_excess_degree_defect_control(),
                "projective_points": projective_point_control(),
            },
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_NEXT_SLACK_SOURCE_PLANE_ZERO_CHARGE_CLOSURE_"
                "HIGHER_SLACKS_OPEN_ROW_OPEN"
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
        "title": "KoalaBear next-slack source-plane closure",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_next_slack_source_plane_closure_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED ZERO-CHARGE BRANCH PAYMENT",
        "independence of the source constraints",
        "\\dim_F W_\\Sigma=3",
        "Base span at most two is paid directly",
        "Three-by-three polynomial rank-one theorem",
        "\\operatorname{adj}\\mathcal P=0",
        "Rank excess contradicts the actual line",
        "4{,}180{,}887{,}079{,}739{,}838",
        "67,473..213,050",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["theorem"]["complete_next_slack_paid"] is True,
        "next slack closure",
    )
    need(cert["theorem"]["row_closed"] is False, "row status")
    need(
        cert["deployed_arithmetic"]["direct_branch_cap"]
        < cert["active_ledger"]["B_remaining"],
        "strict direct payment",
    )
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
            "source_constraints_independent", False
        ),
        lambda d: d["theorem"].__setitem__("source_residue_dimension", 4),
        lambda d: d["theorem"].__setitem__(
            "full_base_span_reciprocal_dimension_two_owned_by_c5", False
        ),
        lambda d: d["theorem"].__setitem__(
            "rank_excess_contradicts_coprime_exact_degree", False
        ),
        lambda d: d["theorem"].__setitem__("complete_next_slack_paid", False),
        lambda d: d["deployed_arithmetic"].__setitem__(
            "direct_branch_cap", active.REMAINING + 1
        ),
        lambda d: d["finite_controls"]["exhaustive_coprime_family"].__setitem__(
            "accepted_pairs", 100_841
        ),
        lambda d: d["upstream_certificates"]["seven_owner_partition"].__setitem__(
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
            print(f"next_slack: {R_NEXT}")
            print(f"source_dimension: {cert['theorem']['source_residue_dimension']}")
            print(f"direct_branch_cap: {DIRECT_BRANCH_CAP}")
            print(f"reserve_margin: {RESERVE_MARGIN}")
            print(
                "exhaustive_pairs: "
                f"{cert['finite_controls']['exhaustive_coprime_family']['accepted_pairs']}"
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
