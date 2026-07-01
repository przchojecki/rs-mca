#!/usr/bin/env python3
"""Build the M3 rank-6, A=426 finite-affine low-rank v9 packet.

This packet turns one row of the rank-6 finite-slack family into a replayable
v9 regular-minor packet.  The regular-minor coefficients are checked from a
low-rank update input, and the exact finite root table is certified by
gcd(Delta,Z^q-Z) over F_17^32.
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
    hash_json,
    render,
)


PACKET_SCHEMA = "f17-32-m3-low-rank-rank6-a426-finite-affine-v1"
N = 512
K = 256
A = 426
J = N - A
T = A - K
MINOR_SIZE = J + 1
UPDATE_RANK = 6
SYNDROME_LENGTH = N - K

ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_RANK6_SLACK = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/"
    "f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json"
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
    "f17_32_n512_k256_a426_low_rank6_input.json"
)
PACKET_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank6-a426-finite-affine/"
    "f17_32_n512_k256_a426_rank6_finite_affine_packet.json"
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


def power_sums(
    field: PolynomialBasisField,
    nodes: list[tuple[int, ...]],
    length: int,
) -> list[int]:
    powers = [field.one for _ in nodes]
    out = []
    for _ in range(length):
        total = field.zero
        for power in powers:
            total = field.add(total, power)
        out.append(field.encode(total))
        powers = [field.mul(power, node) for power, node in zip(powers, nodes)]
    return out


def field_from_descriptor(descriptor: dict[str, Any]) -> PolynomialBasisField:
    model = descriptor["field_model"]
    return PolynomialBasisField(model["p"], model["modulus"])


def rank6_record(slack: dict[str, Any]) -> dict[str, Any]:
    records = [record for record in slack["records"] if record["A"] == A]
    require(len(records) == 1, "expected exactly one rank-6 A=426 record")
    record = records[0]
    require(record["j"] == J and record["t"] == T, "rank-6 record window mismatch")
    require(record["root_count"] == 1, "rank-6 A=426 should have one root")
    require(len(record["listed_roots"]) == 1, "rank-6 A=426 root list mismatch")
    return record


def validate_sources(descriptor: dict[str, Any], slack: dict[str, Any]) -> None:
    require(descriptor["row"]["n"] == N, "row descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "row descriptor k mismatch")
    require(descriptor["row"]["syndrome_length"] == SYNDROME_LENGTH, "bad syndrome length")
    require(
        slack["schema_version"] == "f17-32-m3-low-rank6-slack-family-v1",
        "rank-6 slack schema mismatch",
    )
    require(slack["agreement_range"] == [385, 426], "rank-6 slack window mismatch")
    require(slack["construction"]["rank"] == UPDATE_RANK, "rank mismatch")


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
        "sampler": "finite_affine_line",
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
                "synthetic M3 rank-6 low-rank update syndrome uses the first "
                "87 elements and the next 6 descriptor-domain elements"
            ),
        },
        "claim_scope": {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "enumerated",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Rank-6 low-rank update replay input for the A=426 finite-affine "
                "v9 packet; this is not actual-row data."
            ),
        },
        "row_set_strategy": {"type": "prefix"},
        "line_syndrome": {
            "description": (
                "synthetic M3 rank-6 low-rank update witness: "
                "u_m=sum_{x in X}x^m for the first 87 descriptor-domain "
                "elements and v_m=sum_{y in Y}y^m for the next 6 elements"
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
    input_object: dict[str, Any],
) -> dict[str, Any]:
    record = rank6_record(slack)
    roots = record["listed_roots"]
    coefficients = record["hankel_coefficients_ascending"]
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
                "synthetic rank-6 low-rank update syndrome at A=426"
            ),
        },
        "agreement_threshold": A,
        "sampler": "finite_affine_line",
        "sampler_audit": {
            "sampler": "finite_affine_line",
            "slope_field": descriptor["row"]["field"],
            "slope_field_order": descriptor["row"]["field_order"],
            "denominator": descriptor["row"]["field_order"],
            "denominator_formula": "|F|",
            "field_role": "q_line",
            "extension_denominator_warning": (
                "finite affine extension-valued line packets are divided by "
                "the slope field order, not by the base field"
            ),
        },
        "claim_scope": {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "enumerated",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Finite-affine regular-minor packet for one synthetic rank-6 "
                "low-rank row.  It is a v9 replay packet, not an actual-row "
                "safe-side threshold certificate."
            ),
        },
        "extractor": {
            "name": "regular-hankel-minor-extractor",
            "method": (
                "low-rank update regular-minor replay plus Frobenius-gcd "
                "exact root count over a polynomial-basis finite field"
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
            "rank6_slack_family": {
                "ref": str(LOW_RANK6_SLACK.relative_to(REPO_ROOT)),
                "sha256": file_sha256(LOW_RANK6_SLACK),
                "schema_version": slack["schema_version"],
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
                    "linear_root_count_certificate": record[
                        "linear_root_count_certificate"
                    ],
                },
                "regular_minor_polynomial_data": {
                    "coefficients_ascending": coefficients,
                    "field_encoding": "base-p low-to-high integer",
                    "field_extension_degree": 32,
                    "p": 17,
                },
                "extractor_audit": {
                    "certificate_mode": "low_rank_update_bound",
                    "row_set_source": "low_rank_update_prefix_rank6",
                    "tested_row_sets": 1,
                    "degree_bound": UPDATE_RANK,
                    "root_count": len(roots),
                    "field_size": descriptor["row"]["field_order"],
                    "finite_root_count_certificate": "frobenius_linear_root_gcd",
                    "projective_infinity_status": (
                        "handled by the companion projective-infinity packet"
                    ),
                },
            }
        ],
        "root_union": roots,
        "enumerated_bad_slope_union": [],
        "declared_aperiodic_numerator": len(roots),
        "root_union_table_ref": "inline:root_union",
        "finite_affine_numerator": len(roots),
        "nonclaims": [
            "synthetic syndrome-pencil packet only",
            "regular-minor roots are an upper-bound root table, not proved actual bad slopes",
            "projective infinity is handled by the companion rank-6 A=426 projective packet",
            "not a quotient-image subtraction table",
            "not a worst-case or actual-row M3 threshold bound",
        ],
    }


def build_objects() -> tuple[dict[str, Any], dict[str, Any]]:
    descriptor = load_json(ROW_DESCRIPTOR)
    slack = load_json(LOW_RANK6_SLACK)
    validate_sources(descriptor, slack)
    input_object = build_input(descriptor)
    packet = build_packet(descriptor, slack, input_object)
    return input_object, packet


def check_file(path: Path, expected: dict[str, Any], label: str) -> None:
    actual = path.read_text(encoding="utf-8")
    expected_text = render(expected)
    if actual != expected_text:
        raise AssertionError(f"{label} mismatch: {path}")


def print_summary(packet: dict[str, Any]) -> None:
    item = packet["exact_agreements"][0]
    print("F_17^32 M3 rank-6 A=426 finite-affine v9 packet")
    print(f"status: {packet['status']}")
    print(
        "degree={degree}, finite_roots={roots}, declared_numerator={num}".format(
            degree=item["regular_minor"]["degree"],
            roots=item["regular_minor_data"]["roots"],
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
        check_file(INPUT_PATH, input_object, "rank-6 finite packet input")
        check_file(PACKET_PATH, packet, "rank-6 finite packet")
    if args.json:
        print(render(packet), end="")
        return
    print_summary(packet)


if __name__ == "__main__":
    main()
