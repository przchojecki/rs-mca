#!/usr/bin/env python3
"""Build the M3 rank-6, A=426 projective-line low-rank v9 packet.

This promotes the finite-affine rank-6 packet to the projective-line sampler.
The finite root table is still checked by gcd(Delta,Z^q-Z) over F_17^32, and
the point at infinity is checked by the original regular-minor top coefficient
at degree j+1.
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

from experimental.scripts import (  # noqa: E402
    verify_f17_32_m3_low_rank_rank6_a426_finite_packet as finite,
)


PACKET_SCHEMA = "f17-32-m3-low-rank-rank6-a426-projective-line-v1"
INPUT_PATH = REPO_ROOT / (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a426_low_rank6_projective_line_input.json"
)
PACKET_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank6-a426-projective-line/"
    "f17_32_n512_k256_a426_rank6_projective_line_packet.json"
)
PROJECTIVE_PIVOT_PACKET = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/"
    "f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json"
)
PROJECTIVE_PIVOT_REF = str(PROJECTIVE_PIVOT_PACKET.relative_to(REPO_ROOT))


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_projective_input(descriptor: dict[str, Any]) -> dict[str, Any]:
    input_object = finite.build_input(descriptor)
    input_object["sampler"] = "projective_line"
    input_object["claim_scope"]["note"] = (
        "Projective-line replay input for the A=426 rank-6 v9 packet; "
        "this is not actual-row data."
    )
    input_object["nonclaims"] = [
        "synthetic syndrome pencil only",
        "not a worst-case or actual-row M3 threshold bound",
        "not a quotient-image subtraction table",
    ]
    return input_object


def validate_projective_pivot(packet: dict[str, Any]) -> None:
    require(
        packet["schema_version"] == "aperiodic-hankel-eliminant-v1",
        "projective pivot packet schema mismatch",
    )
    require(
        packet["packet_certificate_schema"]
        == "f17-32-m3-low-rank-rank6-a426-projective-pivot-v1",
        "projective pivot packet certificate schema mismatch",
    )
    coverage = packet["projective_infinity_coverage"]
    require(coverage["A"] == finite.A, "projective pivot A mismatch")
    require(coverage["rank"] == finite.UPDATE_RANK, "projective pivot rank mismatch")
    require(coverage["status"] == "nonempty", "projective pivot status mismatch")
    require(coverage["support_count"] == 1, "projective pivot support mismatch")
    require(
        coverage["projective_point"] == "[0:1]",
        "projective pivot point mismatch",
    )


def build_packet(
    descriptor: dict[str, Any],
    slack: dict[str, Any],
    projective_pivot: dict[str, Any],
    input_object: dict[str, Any],
) -> dict[str, Any]:
    record = finite.rank6_record(slack)
    roots = record["listed_roots"]
    packet = finite.build_packet(descriptor, slack, input_object)
    packet["packet_certificate_schema"] = PACKET_SCHEMA
    packet["sampler"] = "projective_line"
    packet["sampler_audit"] = {
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
    }
    packet["claim_scope"]["note"] = (
        "Projective-line regular-minor packet for one synthetic rank-6 "
        "low-rank row. It is a v9 replay packet, not an actual-row "
        "safe-side threshold certificate."
    )
    packet["extractor"]["method"] = (
        "low-rank update regular-minor replay, Frobenius-gcd exact finite "
        "root count, and original-top-degree projective infinity audit"
    )
    packet["extractor"]["input_ref"] = str(INPUT_PATH.relative_to(REPO_ROOT))
    packet["extractor"]["input_sha256"] = finite.object_sha256(input_object)
    packet["source_artifacts"]["rank6_projective_pivot_packet"] = {
        "ref": PROJECTIVE_PIVOT_REF,
        "sha256": file_sha256(PROJECTIVE_PIVOT_PACKET),
        "packet_certificate_schema": projective_pivot["packet_certificate_schema"],
    }

    infinity = record["projective_infinity"]
    item = packet["exact_agreements"][0]
    item["projective_infinity"] = {
        "projective_point": "[0:1]",
        "status": "nonempty",
        "top_degree": infinity["top_degree"],
        "top_coefficient": infinity["top_coefficient_encoding"],
        "field_encoding": "base-p low-to-high integer",
        "contribution": infinity["contribution"],
        "reason": (
            "The projective-line regular minor is homogenized to the original "
            "degree j+1.  Since the low-rank compressed determinant has "
            "degree 6 < j+1=87, the top coefficient is zero and the regular "
            "minor does not exclude [0:1].  The companion pivot packet "
            "records an actual support witness for this endpoint."
        ),
        "support_certificate_ref": (
            f"{PROJECTIVE_PIVOT_REF}#/projective_infinity_coverage"
        ),
    }
    item["extractor_audit"]["projective_infinity_status"] = (
        "checked inline by the original regular-minor top degree j+1"
    )
    item["extractor_audit"]["projective_infinity_contribution"] = (
        infinity["contribution"]
    )
    item["extractor_audit"]["projective_regular_root_count"] = (
        len(roots) + infinity["contribution"]
    )

    packet["declared_aperiodic_numerator"] = len(roots) + infinity["contribution"]
    packet["finite_affine_numerator"] = len(roots)
    packet["projective_infinity_numerator"] = infinity["contribution"]
    packet["projective_line_numerator"] = packet["declared_aperiodic_numerator"]
    packet["nonclaims"] = [
        "synthetic syndrome-pencil packet only",
        "regular-minor roots are an upper-bound root table, not proved actual bad slopes",
        "projective infinity is counted as a regular-minor endpoint and witnessed by a companion pivot packet",
        "not a quotient-image subtraction table",
        "not a worst-case or actual-row M3 threshold bound",
    ]
    return packet


def build_objects() -> tuple[dict[str, Any], dict[str, Any]]:
    descriptor = finite.load_json(finite.ROW_DESCRIPTOR)
    slack = finite.load_json(finite.LOW_RANK6_SLACK)
    projective_pivot = load_json(PROJECTIVE_PIVOT_PACKET)
    finite.validate_sources(descriptor, slack)
    validate_projective_pivot(projective_pivot)
    input_object = build_projective_input(descriptor)
    packet = build_packet(descriptor, slack, projective_pivot, input_object)
    return input_object, packet


def check_file(path: Path, expected: dict[str, Any], label: str) -> None:
    actual = path.read_text(encoding="utf-8")
    expected_text = render(expected)
    if actual != expected_text:
        raise AssertionError(f"{label} mismatch: {path}")


def print_summary(packet: dict[str, Any]) -> None:
    item = packet["exact_agreements"][0]
    infinity = item["projective_infinity"]
    print("F_17^32 M3 rank-6 A=426 projective-line v9 packet")
    print(f"status: {packet['status']}")
    print(
        "finite_roots={finite}, infinity={infinity}, declared_numerator={num}".format(
            finite=packet["finite_affine_numerator"],
            infinity=infinity["contribution"],
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
        check_file(INPUT_PATH, input_object, "rank-6 projective-line packet input")
        check_file(PACKET_PATH, packet, "rank-6 projective-line packet")
    if args.json:
        print(render(packet), end="")
        return
    print_summary(packet)


if __name__ == "__main__":
    main()
