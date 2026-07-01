#!/usr/bin/env python3
"""Build the M3 rank-7, A=393 projective-line low-rank v9 packet.

This is a hard-row packet for the synthetic low-rank ladder.  Rank 7 is beyond
the degree-only M3 projective envelope: the regular minor has degree 7 and the
projective endpoint may contribute one more point.  For A=393 the Frobenius
gcd has four linear factors, so exact root slack gives projective numerator
4+1=5 <= 6.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.extract_regular_hankel_minors import (  # noqa: E402
    PolynomialBasisField,
    fpoly_degree,
    fpoly_divmod,
    fpoly_gcd,
    fpoly_trim,
    hash_json,
    quadratic_roots_field,
    render,
)
from experimental.scripts.verify_f17_32_m3_low_rank3_family import (  # noqa: E402
    multiply_mod_monic,
)
from experimental.scripts.verify_f17_32_m3_low_rank_rank6_a426_finite_packet import (  # noqa: E402
    power_sums,
)


PACKET_SCHEMA = "f17-32-m3-low-rank-rank7-a393-projective-line-v1"
N = 512
K = 256
A = 393
J = N - A
T = A - K
MINOR_SIZE = J + 1
UPDATE_RANK = 7
SYNDROME_LENGTH = N - K
PROJECTIVE_BUDGET_NUMERATOR = 6

ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_RANK7_SLACK = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank7-slack-family/"
    "f17_32_n512_k256_m3_low_rank7_slack_family_certificate.json"
)
PROJECTIVE_INFINITY_CERT = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/"
    "f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json"
)
TANGENT_EXCLUSION = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json"
)
SUBFIELD_EXCLUSION = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json"
)
INPUT_PATH = REPO_ROOT / (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a393_low_rank7_projective_line_input.json"
)
PACKET_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank7-a393-projective-line/"
    "f17_32_n512_k256_a393_rank7_projective_line_packet.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def object_sha256(value: Any) -> str:
    return sha256(render(value).encode("utf-8")).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def poly_sub(
    left: list[tuple[int, ...]],
    right: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    size = max(len(left), len(right))
    out = []
    for index in range(size):
        left_value = left[index] if index < len(left) else field.zero
        right_value = right[index] if index < len(right) else field.zero
        out.append(field.sub(left_value, right_value))
    return fpoly_trim(out, field)


def poly_pow_mod_monic(
    base: list[tuple[int, ...]],
    exponent: int,
    modulus: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    result = [field.one]
    power = fpoly_trim(base, field)
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = multiply_mod_monic(result, power, modulus, field)
        remaining >>= 1
        if remaining:
            power = multiply_mod_monic(power, power, modulus, field)
    return fpoly_trim(result, field)


def divide_exact(
    polynomial: list[tuple[int, ...]],
    divisor: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    quotient, remainder = fpoly_divmod(polynomial, divisor, field)
    require(
        len(remainder) == 1 and field.is_zero(remainder[0]),
        "non-exact split divisor",
    )
    return quotient


def split_linear_roots(
    polynomial: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[int]:
    """Deterministically split a small squarefree polynomial known to split."""

    polynomial = fpoly_trim(polynomial, field)
    degree = fpoly_degree(polynomial, field)
    if degree == 0:
        return []
    if degree == 1:
        root = field.neg(field.div(polynomial[0], polynomial[1]))
        return [field.encode(root)]
    if degree == 2:
        roots = quadratic_roots_field(polynomial, field)
        require(roots is not None and len(roots) == 2, "quadratic split failed")
        return sorted(field.encode(root) for root in roots)

    exponent = (field.size - 1) // 2
    targets = [field.zero, field.one, field.neg(field.one)]
    for seed in range(200):
        shift = field.normalize(seed)
        probe = poly_pow_mod_monic([shift, field.one], exponent, polynomial, field)
        for target in targets:
            factor = fpoly_gcd(polynomial, poly_sub(probe, [target], field), field)
            factor_degree = fpoly_degree(factor, field)
            if 0 < factor_degree < degree:
                quotient = divide_exact(polynomial, factor, field)
                return sorted(
                    split_linear_roots(factor, field)
                    + split_linear_roots(quotient, field)
                )
    raise AssertionError("failed to split small Frobenius gcd")


def field_from_descriptor(descriptor: dict[str, Any]) -> PolynomialBasisField:
    model = descriptor["field_model"]
    return PolynomialBasisField(model["p"], model["modulus"])


def rank7_record(slack: dict[str, Any]) -> dict[str, Any]:
    records = [record for record in slack["records"] if record["A"] == A]
    require(len(records) == 1, "expected exactly one rank-7 A=393 record")
    record = records[0]
    require(record["j"] == J and record["t"] == T, "rank-7 record mismatch")
    require(record["root_count"] == 4, "rank-7 A=393 should have four roots")
    require(record["listed_roots"] is None, "source row should be count-only")
    return record


def validate_sources(
    descriptor: dict[str, Any],
    slack: dict[str, Any],
    projective_infinity: dict[str, Any],
) -> None:
    require(descriptor["row"]["n"] == N, "row descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "row descriptor k mismatch")
    require(
        slack["schema_version"] == "f17-32-m3-low-rank7-slack-family-v1",
        "rank-7 slack schema mismatch",
    )
    require(slack["agreement_range"] == [385, 426], "rank-7 slack window mismatch")
    require(slack["construction"]["rank"] == UPDATE_RANK, "rank mismatch")
    require(
        slack["aggregate"]["max_finite_roots_per_agreement"] == 4
        and slack["aggregate"]["max_projective_regular_roots_per_agreement"] == 5,
        "rank-7 slack aggregate mismatch",
    )
    require(
        projective_infinity["schema_version"]
        == "f17-32-m3-low-rank2-11-projective-infinity-v1",
        "projective-infinity schema mismatch",
    )
    require(
        projective_infinity["aggregate"]["rank_summaries"][str(UPDATE_RANK)][
            "endpoint_support_size"
        ]
        == N - UPDATE_RANK,
        "rank-7 endpoint support mismatch",
    )


def roots_for_record(
    record: dict[str, Any],
    field: PolynomialBasisField,
) -> list[int]:
    gcd_coefficients = [
        field.decode(coefficient)
        for coefficient in record["linear_root_count_certificate"][
            "linear_root_gcd_coefficients_ascending"
        ]
    ]
    roots = split_linear_roots(gcd_coefficients, field)
    require(len(roots) == record["root_count"], "split root count mismatch")
    for root in roots:
        root_value = field.decode(root)
        total = field.zero
        power = field.one
        for coefficient in gcd_coefficients:
            total = field.add(total, field.mul(coefficient, power))
            power = field.mul(power, root_value)
        require(field.is_zero(total), "listed root does not satisfy gcd")
    return roots


def build_input(descriptor: dict[str, Any]) -> dict[str, Any]:
    field = field_from_descriptor(descriptor)
    domain_encodings = descriptor["domain"]["domain_encodings"]
    base_encodings = domain_encodings[:MINOR_SIZE]
    update_encodings = domain_encodings[MINOR_SIZE : MINOR_SIZE + UPDATE_RANK]
    base_nodes = [field.decode(value) for value in base_encodings]
    update_nodes = [field.decode(value) for value in update_encodings]
    return {
        "schema_version": "regular-hankel-minor-extractor-input-v1",
        "status": "PROVED / AUDIT",
        "agreement_threshold": A,
        "exact_agreements": [A],
        "sampler": "projective_line",
        "certificate_mode": "low_rank_update_bound",
        "field_model": {
            "kind": "polynomial_basis",
            "p": descriptor["field_model"]["p"],
            "degree": descriptor["field_model"]["degree"],
            "modulus": descriptor["field_model"]["modulus"],
            "encoding": "base-p low-to-high integer",
        },
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the pinned F_17^32 row descriptor; "
                "synthetic M3 rank-7 low-rank update syndrome uses the first "
                "120 elements and the next 7 descriptor-domain elements"
            ),
        },
        "claim_scope": {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "enumerated",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Rank-7 low-rank update replay input for the A=393 "
                "projective-line v9 packet; this is not actual-row data."
            ),
        },
        "row_set_strategy": {"type": "prefix"},
        "line_syndrome": {
            "description": (
                "synthetic M3 rank-7 low-rank update witness: "
                "u_m=sum_{x in X}x^m for the first 120 descriptor-domain "
                "elements and v_m=sum_{y in Y}y^m for the next 7 elements"
            ),
            "field_encoding": "base-p low-to-high integer",
            "length": SYNDROME_LENGTH,
            "rank_witness_reason": (
                "low-rank Cauchy-Binet update makes the prefix determinant "
                "degree-bounded by the update rank"
            ),
            "u": power_sums(field, base_nodes, SYNDROME_LENGTH),
            "v": power_sums(field, update_nodes, SYNDROME_LENGTH),
        },
        "low_rank_update": {
            "base_node_count": MINOR_SIZE,
            "update_rank": UPDATE_RANK,
            "base_node_encodings": base_encodings,
            "update_node_encodings": update_encodings,
        },
        "nonclaims": [
            "synthetic syndrome pencil only",
            "not a worst-case or actual-row M3 threshold bound",
            "not a quotient-image subtraction table",
        ],
    }


def build_packet(
    descriptor: dict[str, Any],
    slack: dict[str, Any],
    projective_infinity: dict[str, Any],
    input_object: dict[str, Any],
) -> dict[str, Any]:
    field = field_from_descriptor(descriptor)
    record = rank7_record(slack)
    roots = roots_for_record(record, field)
    coefficients = record["hankel_coefficients_ascending"]
    infinity = record["projective_infinity"]
    root_hash = hash_json(roots)
    input_ref = str(INPUT_PATH.relative_to(REPO_ROOT))
    return {
        "schema_version": "aperiodic-hankel-eliminant-v1",
        "packet_certificate_schema": PACKET_SCHEMA,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the pinned F_17^32 row descriptor; "
                "synthetic rank-7 low-rank update syndrome at A=393"
            ),
        },
        "agreement_threshold": A,
        "sampler": "projective_line",
        "sampler_audit": {
            "sampler": "projective_line",
            "slope_field": descriptor["row"]["field"],
            "slope_field_order": descriptor["row"]["field_order"],
            "denominator": descriptor["row"]["field_order"] + 1,
            "denominator_formula": "|P^1(F)| = |F| + 1",
            "field_role": "q_line",
            "extension_denominator_warning": (
                "projective extension-valued line packets are divided by "
                "|P^1(F)|, not by the base field"
            ),
        },
        "claim_scope": {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "enumerated",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Projective-line regular-minor packet for one hard synthetic "
                "rank-7 low-rank row. It is a v9 replay packet, not an "
                "actual-row safe-side threshold certificate."
            ),
        },
        "extractor": {
            "name": "regular-hankel-minor-extractor",
            "method": (
                "low-rank update regular-minor replay, deterministic splitting "
                "of the Frobenius-gcd finite root table, and original-top-degree "
                "projective infinity audit"
            ),
            "scope": "prime-power syndrome pencils with explicit polynomial-basis model",
            "certificate_mode": "low_rank_update_bound",
            "row_set_strategy": {"type": "prefix"},
            "input_ref": input_ref,
            "input_sha256": object_sha256(input_object),
            "field_model": input_object["field_model"],
        },
        "source_artifacts": {
            "row_descriptor": {
                "ref": str(ROW_DESCRIPTOR.relative_to(REPO_ROOT)),
                "sha256": file_sha256(ROW_DESCRIPTOR),
            },
            "rank7_slack_family": {
                "ref": str(LOW_RANK7_SLACK.relative_to(REPO_ROOT)),
                "sha256": file_sha256(LOW_RANK7_SLACK),
                "schema_version": slack["schema_version"],
            },
            "rank2_11_projective_infinity_endpoint": {
                "ref": str(PROJECTIVE_INFINITY_CERT.relative_to(REPO_ROOT)),
                "sha256": file_sha256(PROJECTIVE_INFINITY_CERT),
                "schema_version": projective_infinity["schema_version"],
            },
        },
        "removed_ledgers": [
            {
                "name": "common_code_line_tangent_overlap",
                "numerator": 0,
                "certificate_ref": (
                    str(TANGENT_EXCLUSION.relative_to(REPO_ROOT))
                    + "#/aggregate/common_code_line_tangent_overlap_sum"
                ),
            },
            {
                "name": "proper_subfield_overlap",
                "numerator": 0,
                "certificate_ref": (
                    str(SUBFIELD_EXCLUSION.relative_to(REPO_ROOT))
                    + "#/aggregate/proper_subfield_overlap_sum"
                ),
            },
        ],
        "exact_agreements": [
            {
                "A": A,
                "j": J,
                "t": T,
                "status": "regular_minor",
                "regular_minor": {
                    "row_set": list(range(MINOR_SIZE)),
                    "polynomial_ref": "inline:regular_minor.coefficients_ascending",
                    "degree": record["polynomial_degree"],
                    "root_hash": root_hash,
                },
                "regular_minor_data": {
                    "coefficients_ascending": coefficients,
                    "field_encoding": "base-p low-to-high integer",
                    "field_extension_degree": 32,
                    "p": 17,
                    "roots": roots,
                    "linear_root_count_certificate": {
                        **record["linear_root_count_certificate"],
                        "listed_roots_status": "listed",
                    },
                    "root_listing_certificate": {
                        "kind": "deterministic_cantor_zassenhaus_small_degree",
                        "input": "linear_root_gcd_coefficients_ascending",
                        "degree": record["root_count"],
                        "seed_range": [0, 199],
                        "roots": roots,
                    },
                },
                "regular_minor_polynomial_data": {
                    "coefficients_ascending": coefficients,
                    "field_encoding": "base-p low-to-high integer",
                    "field_extension_degree": 32,
                    "p": 17,
                },
                "projective_infinity": {
                    "projective_point": "[0:1]",
                    "status": "nonempty",
                    "top_degree": infinity["top_degree"],
                    "top_coefficient": infinity["top_coefficient_encoding"],
                    "field_encoding": "base-p low-to-high integer",
                    "contribution": infinity["contribution"],
                    "reason": (
                        "The projective-line regular minor is homogenized to "
                        "the original degree j+1. Since the rank-7 compressed "
                        "determinant has degree 7 < j+1=120, the top "
                        "coefficient is zero and the regular minor does not "
                        "exclude [0:1]."
                    ),
                    "support_certificate_ref": (
                        str(PROJECTIVE_INFINITY_CERT.relative_to(REPO_ROOT))
                        + "#/deterministic_records"
                    ),
                },
                "extractor_audit": {
                    "certificate_mode": "low_rank_update_bound",
                    "row_set_source": "low_rank_update_prefix_rank7",
                    "tested_row_sets": 1,
                    "degree_bound": UPDATE_RANK,
                    "root_count": len(roots),
                    "field_size": descriptor["row"]["field_order"],
                    "finite_root_count_certificate": "frobenius_linear_root_gcd",
                    "root_listing": "deterministic_small_degree_split",
                    "projective_infinity_contribution": infinity["contribution"],
                    "projective_regular_root_count": len(roots)
                    + infinity["contribution"],
                    "projective_budget_numerator": PROJECTIVE_BUDGET_NUMERATOR,
                },
            }
        ],
        "root_union": roots,
        "enumerated_bad_slope_union": [],
        "declared_aperiodic_numerator": len(roots) + infinity["contribution"],
        "root_union_table_ref": "inline:root_union",
        "finite_affine_numerator": len(roots),
        "projective_infinity_numerator": infinity["contribution"],
        "projective_line_numerator": len(roots) + infinity["contribution"],
        "nonclaims": [
            "synthetic syndrome-pencil packet only",
            "regular-minor roots are an upper-bound root table, not proved actual bad slopes",
            "projective infinity is counted as a regular-minor endpoint",
            "not a quotient-image subtraction table",
            "not a worst-case or actual-row M3 threshold bound",
        ],
    }


def build_objects() -> tuple[dict[str, Any], dict[str, Any]]:
    descriptor = load_json(ROW_DESCRIPTOR)
    slack = load_json(LOW_RANK7_SLACK)
    projective_infinity = load_json(PROJECTIVE_INFINITY_CERT)
    validate_sources(descriptor, slack, projective_infinity)
    input_object = build_input(descriptor)
    packet = build_packet(descriptor, slack, projective_infinity, input_object)
    return input_object, packet


def check_file(path: Path, expected: dict[str, Any], label: str) -> None:
    actual = path.read_text(encoding="utf-8")
    expected_text = render(expected)
    if actual != expected_text:
        raise AssertionError(f"{label} mismatch: {path}")


def print_summary(packet: dict[str, Any]) -> None:
    item = packet["exact_agreements"][0]
    print("F_17^32 M3 rank-7 A=393 projective-line v9 packet")
    print(f"status: {packet['status']}")
    print(
        "degree={degree}, finite_roots={finite}, infinity={infinity}, "
        "declared_numerator={num}".format(
            degree=item["regular_minor"]["degree"],
            finite=packet["finite_affine_numerator"],
            infinity=packet["projective_infinity_numerator"],
            num=packet["declared_aperiodic_numerator"],
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write input and packet")
    parser.add_argument("--check", action="store_true", help="check input and packet")
    parser.add_argument("--json", action="store_true", help="print packet JSON")
    args = parser.parse_args()

    input_object, packet = build_objects()
    if args.write:
        INPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        PACKET_PATH.parent.mkdir(parents=True, exist_ok=True)
        INPUT_PATH.write_text(render(input_object), encoding="utf-8")
        PACKET_PATH.write_text(render(packet), encoding="utf-8")
    if args.check:
        check_file(INPUT_PATH, input_object, "rank-7 projective-line packet input")
        check_file(PACKET_PATH, packet, "rank-7 projective-line packet")
    if args.json:
        print(render(packet), end="")
        return
    print_summary(packet)


if __name__ == "__main__":
    main()
