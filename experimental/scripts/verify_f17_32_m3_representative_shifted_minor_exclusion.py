#!/usr/bin/env python3
"""Verify shifted-minor exclusion for representative M3 low-rank packets.

The regular-minor packets bound bad finite slopes by roots of one selected
square Hankel minor.  A true exact-support witness must make the full
``t x (j+1)`` Hankel matrix rank-deficient, hence it must kill every consecutive
``(j+1) x (j+1)`` square minor.  This verifier checks the row-shift-1 minor for
the six representative projective-line packets in the rank-6..11 low-rank
ladder and proves that all listed finite roots of the selected first minor fail
that shifted minor.
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
    fpoly_eval,
    fpoly_gcd,
    hash_json,
    render,
)
from experimental.scripts.verify_f17_32_m3_low_rank9_11_slack_sweep import (  # noqa: E402
    characteristic_polynomial_coefficients,
    update_basis_values,
)


SCHEMA_VERSION = "f17-32-m3-representative-shifted-minor-exclusion-v1"
N = 512
K = 256
SHIFT = 1

PACKET_REFS = [
    (
        6,
        426,
        "experimental/data/certificates/"
        "hankel-f17-32-m3-low-rank-rank6-a426-projective-line/"
        "f17_32_n512_k256_a426_rank6_projective_line_packet.json",
    ),
    (
        7,
        393,
        "experimental/data/certificates/"
        "hankel-f17-32-m3-low-rank-rank7-a393-projective-line/"
        "f17_32_n512_k256_a393_rank7_projective_line_packet.json",
    ),
    (
        8,
        393,
        "experimental/data/certificates/"
        "hankel-f17-32-m3-low-rank-rank8-a393-projective-line/"
        "f17_32_n512_k256_a393_rank8_projective_line_packet.json",
    ),
    (
        9,
        398,
        "experimental/data/certificates/"
        "hankel-f17-32-m3-low-rank-rank9-a398-projective-line/"
        "f17_32_n512_k256_a398_rank9_projective_line_packet.json",
    ),
    (
        10,
        411,
        "experimental/data/certificates/"
        "hankel-f17-32-m3-low-rank-rank10-a411-projective-line/"
        "f17_32_n512_k256_a411_rank10_projective_line_packet.json",
    ),
    (
        11,
        391,
        "experimental/data/certificates/"
        "hankel-f17-32-m3-low-rank-rank11-a391-projective-line/"
        "f17_32_n512_k256_a391_rank11_projective_line_packet.json",
    ),
]

OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-representative-shifted-minor-exclusion/"
    "f17_32_n512_k256_m3_representative_shifted_minor_exclusion.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = REPO_ROOT / ref if isinstance(ref, str) else ref
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(ref: str) -> str:
    return sha256((REPO_ROOT / ref).read_bytes()).hexdigest()


def object_sha256(value: Any) -> str:
    return sha256(render(value).encode("utf-8")).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def field_from_input(input_object: dict[str, Any]) -> PolynomialBasisField:
    model = input_object["field_model"]
    return PolynomialBasisField(model["p"], model["modulus"])


def prefix_state(
    field: PolynomialBasisField,
    base_nodes: list[tuple[int, ...]],
) -> tuple[list[tuple[int, ...]], tuple[int, ...]]:
    denominators: list[tuple[int, ...]] = []
    seen: list[tuple[int, ...]] = []
    base_determinant = field.one
    for node in base_nodes:
        new_denominator = field.one
        for old_node in seen:
            new_denominator = field.mul(
                new_denominator, field.sub(node, old_node)
            )
        for old_index, old_node in enumerate(seen):
            denominators[old_index] = field.mul(
                denominators[old_index], field.sub(old_node, node)
            )
        denominators.append(new_denominator)
        seen.append(node)
        base_determinant = field.mul(
            base_determinant, field.mul(new_denominator, new_denominator)
        )
    return denominators, base_determinant


def shifted_low_rank_coefficients(
    field: PolynomialBasisField,
    base_nodes: list[tuple[int, ...]],
    base_denominators: list[tuple[int, ...]],
    base_determinant: tuple[int, ...],
    update_nodes: list[tuple[int, ...]],
    shift: int,
) -> list[tuple[int, ...]]:
    rank = len(update_nodes)
    basis_values = update_basis_values(
        field, base_nodes, base_denominators, update_nodes
    )
    if shift == 0:
        base_scale = base_determinant
        base_weights = [field.one] * len(base_nodes)
        update_weights = [field.one] * rank
    else:
        base_scale = base_determinant
        base_weights = []
        for node in base_nodes:
            node_power = field.pow(node, shift)
            base_scale = field.mul(base_scale, node_power)
            base_weights.append(field.inv(node_power))
        update_weights = [field.pow(node, shift) for node in update_nodes]

    kernel = []
    for row_index, left_values in enumerate(basis_values):
        row = []
        for right_values in basis_values:
            entry = field.zero
            for weight, left, right in zip(base_weights, left_values, right_values):
                entry = field.add(entry, field.mul(weight, field.mul(left, right)))
            row.append(field.mul(update_weights[row_index], entry))
        kernel.append(row)

    kernel_coefficients = characteristic_polynomial_coefficients(kernel, field)
    return [field.mul(base_scale, coefficient) for coefficient in kernel_coefficients]


def validate_packet_shape(
    packet: dict[str, Any],
    input_object: dict[str, Any],
    rank: int,
    agreement: int,
) -> dict[str, Any]:
    require(packet["schema_version"] == "aperiodic-hankel-eliminant-v1", "packet schema")
    require(packet["status"] == "PROVED / AUDIT", "packet status")
    require(packet["agreement_threshold"] == agreement, "agreement mismatch")
    require(packet["sampler"] == "projective_line", "sampler mismatch")
    require(input_object["row"]["n"] == N and input_object["row"]["k"] == K, "row")
    require(input_object["agreement_threshold"] == agreement, "input agreement")
    item = packet["exact_agreements"][0]
    require(item["A"] == agreement, "item agreement mismatch")
    require(item["regular_minor"]["degree"] == rank, "rank/degree mismatch")
    require(item["regular_minor_data"]["roots"] == packet["root_union"], "roots")
    require(
        item["regular_minor_data"]["linear_root_count_certificate"][
            "linear_root_count"
        ]
        == len(packet["root_union"]),
        "linear root count mismatch",
    )
    require(input_object["low_rank_update"]["update_rank"] == rank, "input rank")
    return item


def build_record(rank: int, agreement: int, packet_ref: str) -> dict[str, Any]:
    packet = load_json(packet_ref)
    input_ref = packet["extractor"]["input_ref"]
    input_object = load_json(input_ref)
    item = validate_packet_shape(packet, input_object, rank, agreement)
    field = field_from_input(input_object)
    base_encodings = input_object["low_rank_update"]["base_node_encodings"]
    update_encodings = input_object["low_rank_update"]["update_node_encodings"]
    base_nodes = [field.decode(value) for value in base_encodings]
    update_nodes = [field.decode(value) for value in update_encodings]
    base_denominators, base_determinant = prefix_state(field, base_nodes)

    first_coefficients = shifted_low_rank_coefficients(
        field,
        base_nodes,
        base_denominators,
        base_determinant,
        update_nodes,
        0,
    )
    first_encoded = [field.encode(coefficient) for coefficient in first_coefficients]
    require(
        first_encoded == item["regular_minor_data"]["coefficients_ascending"],
        f"rank-{rank} A={agreement}: first minor replay mismatch",
    )

    shifted_coefficients = shifted_low_rank_coefficients(
        field,
        base_nodes,
        base_denominators,
        base_determinant,
        update_nodes,
        SHIFT,
    )
    shifted_encoded = [
        field.encode(coefficient) for coefficient in shifted_coefficients
    ]
    root_gcd = [
        field.decode(value)
        for value in item["regular_minor_data"]["linear_root_count_certificate"][
            "linear_root_gcd_coefficients_ascending"
        ]
    ]
    common_gcd = fpoly_gcd(root_gcd, shifted_coefficients, field)
    common_degree = fpoly_degree(common_gcd, field)
    require(common_degree == 0, f"rank-{rank} A={agreement}: shifted gcd nontrivial")

    cleared_roots = []
    for root in packet["root_union"]:
        value = field.decode(root)
        shifted_value = fpoly_eval(shifted_coefficients, value, field)
        require(
            shifted_value != field.zero,
            f"rank-{rank} A={agreement}: root survives shifted minor",
        )
        cleared_roots.append(
            {
                "root": root,
                "shifted_minor_value_hash": hash_json(field.encode(shifted_value)),
            }
        )

    return {
        "rank": rank,
        "A": agreement,
        "j": item["j"],
        "t": item["t"],
        "packet_ref": packet_ref,
        "packet_sha256": file_sha256(packet_ref),
        "input_ref": input_ref,
        "input_sha256": file_sha256(input_ref),
        "first_minor_row_shift": 0,
        "shifted_minor_row_shift": SHIFT,
        "available_shift_count": item["t"] - (item["j"] + 1),
        "first_minor_root_count": len(packet["root_union"]),
        "first_minor_root_gcd_degree": fpoly_degree(root_gcd, field),
        "shifted_minor_degree": fpoly_degree(shifted_coefficients, field),
        "shifted_minor_coefficient_hash": hash_json(shifted_encoded),
        "common_gcd_degree": common_degree,
        "cleared_root_count": len(cleared_roots),
        "cleared_roots": cleared_roots,
        "support_witness_status": "excluded_by_shifted_minor",
        "reason": (
            "a full exact-support Hankel witness must make every consecutive "
            "(j+1)x(j+1) minor vanish; the row-shift-1 minor is nonzero at "
            "each listed finite root of the first minor"
        ),
    }


def build_certificate() -> dict[str, Any]:
    records = [
        build_record(rank, agreement, packet_ref)
        for rank, agreement, packet_ref in PACKET_REFS
    ]
    require(len(records) == 6, "record count mismatch")
    require(
        all(record["common_gcd_degree"] == 0 for record in records),
        "some representative root survived the shifted-minor check",
    )
    total_roots = sum(record["first_minor_root_count"] for record in records)
    require(total_roots == 18, "representative finite-root total mismatch")
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": "F_17^32",
        },
        "packet_count": len(records),
        "row_shift_tested": SHIFT,
        "claim": (
            "For the six representative rank-6..11 projective-line packets, "
            "every listed finite root of the first regular minor is excluded "
            "as an actual full-Hankel support witness by the shifted row-1 "
            "minor."
        ),
        "method": {
            "test": (
                "compute gcd(root_gcd(first minor), shifted row-1 minor); "
                "degree zero means no listed first-minor root kills both minors"
            ),
            "mathematical_reason": (
                "a true exact-support witness makes the full t by j+1 Hankel "
                "matrix rank-deficient, so all consecutive square minors must "
                "vanish"
            ),
            "shifted_minor_formula": (
                "det(H_X^(q)+Z H_Y^(q)) = det(H_X^(q)) det(I+Z K_q), "
                "with K_q_ab=y_a^q sum_i x_i^{-q} L_i(y_a)L_i(y_b)"
            ),
        },
        "aggregate": {
            "representative_ranks": [record["rank"] for record in records],
            "representative_agreements": [record["A"] for record in records],
            "first_minor_root_total": total_roots,
            "cleared_root_total": sum(record["cleared_root_count"] for record in records),
            "all_representative_roots_excluded_as_support_witnesses": True,
            "common_gcd_degree_histogram": {
                "0": len(records),
            },
        },
        "records": records,
        "records_sha256": object_sha256({"records": records}),
        "nonclaims": [
            "representative packet rows only, not all rank-6..11 rows",
            "does not audit quotient image or quotient support for finite roots",
            "does not prove anything about roots not listed in these packets",
            "does not replace the full singular/pivot chart program",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"representative shifted-minor certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 representative shifted-minor exclusion")
    print(f"status: {certificate['status']}")
    print(
        "packets={packets}, first_minor_roots={roots}, cleared={cleared}".format(
            packets=certificate["packet_count"],
            roots=aggregate["first_minor_root_total"],
            cleared=aggregate["cleared_root_total"],
        )
    )
    print(f"row shift tested: {certificate['row_shift_tested']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate")
    parser.add_argument("--check", type=Path, help="check deterministic certificate")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(certificate, args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
