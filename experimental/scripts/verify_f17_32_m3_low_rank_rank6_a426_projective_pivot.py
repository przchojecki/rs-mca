#!/usr/bin/env python3
"""Build/check a v9 projective-infinity pivot packet for one M3 low-rank row.

The packet is deliberately narrow.  It packages the rank-6, A=426 synthetic
low-rank endpoint into the v9 pivot-atlas shape:

    projective-infinity chart B=0, A!=0 is nonempty and contributes [0:1].

Finite affine roots are not enumerated here; they remain covered by the
rank-6 finite-slack family certificate.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-low-rank-rank6-a426-projective-pivot-v1"
PACKET_SCHEMA_VERSION = "aperiodic-hankel-eliminant-v1"
N = 512
K = 256
A = 426
RANK = 6
P = 17
FIELD_DEGREE = 32
FIELD_ORDER = P**FIELD_DEGREE
SYNDROME_LENGTH = N - K

ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
ENDPOINT_CERT = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/"
    "f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json"
)
OUTPUT_PACKET = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/"
    "f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json"
)
OUTPUT_REF = str(OUTPUT_PACKET.relative_to(REPO_ROOT))
ENDPOINT_REF = str(ENDPOINT_CERT.relative_to(REPO_ROOT))


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_inputs(descriptor: dict[str, Any], endpoint: dict[str, Any]) -> None:
    require(descriptor["row"]["n"] == N, "row descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "row descriptor k mismatch")
    require(
        descriptor["field_model"]["p"] == P
        and len(descriptor["field_model"]["modulus"]) == FIELD_DEGREE + 1,
        "row descriptor field mismatch",
    )
    require(
        endpoint["schema_version"]
        == "f17-32-m3-low-rank2-11-projective-infinity-v1",
        "endpoint certificate schema mismatch",
    )
    require(endpoint["agreement_range"] == [385, 426], "endpoint window mismatch")
    require(RANK in endpoint["construction"]["ranks"], "rank missing from endpoint")
    aggregate = endpoint["aggregate"]
    require(aggregate["record_count"] == 420, "endpoint record-count mismatch")
    require(
        aggregate["rank_summaries"][str(RANK)]["endpoint_support_size"] == N - RANK,
        "endpoint rank support mismatch",
    )
    require(
        aggregate["maximum_agreement_threshold"] == A,
        "endpoint maximum agreement mismatch",
    )


def endpoint_geometry() -> dict[str, Any]:
    j = N - A
    base_node_count = j + 1
    update_start = base_node_count
    update_end = base_node_count + RANK - 1
    endpoint_support_size = N - RANK
    vandermonde_column_count = base_node_count + RANK
    require(endpoint_support_size >= A, "endpoint support misses threshold")
    require(
        vandermonde_column_count <= SYNDROME_LENGTH,
        "Vandermonde columns exceed syndrome length",
    )
    return {
        "A": A,
        "j": j,
        "t": A - K,
        "rank": RANK,
        "base_node_count": base_node_count,
        "base_node_range": [0, base_node_count - 1],
        "update_node_count": RANK,
        "update_node_range": [update_start, update_end],
        "endpoint_support_size": endpoint_support_size,
        "vandermonde_column_count": vandermonde_column_count,
    }


def build_packet() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR)
    endpoint = load_json(ENDPOINT_CERT)
    validate_inputs(descriptor, endpoint)
    geometry = endpoint_geometry()
    coverage_ref = f"{OUTPUT_REF}#/projective_infinity_coverage"
    return {
        "schema_version": PACKET_SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "packet_certificate_schema": SCHEMA_VERSION,
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
        "claim_scope": {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "not_enumerated",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "Chart packet for the projective-infinity endpoint only; finite "
                "affine roots are intentionally outside this packet."
            ),
        },
        "agreement_threshold": A,
        "sampler": "projective_line",
        "sampler_audit": {
            "sampler": "projective_line",
            "slope_field": descriptor["row"]["field"],
            "slope_field_order": FIELD_ORDER,
            "denominator": FIELD_ORDER + 1,
            "denominator_formula": "|P^1(F)| = |F| + 1",
            "field_role": "q_line",
            "extension_denominator_warning": (
                "projective extension-valued line packets are divided by "
                "|P^1(F)|, not by the base field"
            ),
        },
        "removed_ledgers": [],
        "exact_agreements": [
            {
                "A": A,
                "j": geometry["j"],
                "t": geometry["t"],
                "status": "pivot_atlas",
                "charts": [
                    {
                        "chart_id": "projective_infinity",
                        "equations_ref": "inline:B=0",
                        "inequations_ref": "inline:A!=0",
                        "coverage_ref": coverage_ref,
                        "pivot_records": [
                            {
                                "pivot": "projective_infinity_B_zero_A_nonzero",
                                "status": "dimension_degree",
                                "dimension": 0,
                                "variety_degree": 1,
                            }
                        ],
                    }
                ],
            }
        ],
        "projective_infinity_coverage": {
            "status": "nonempty",
            "support_count": 1,
            "projective_point": "[0:1]",
            "source_endpoint_certificate": f"{ENDPOINT_REF}#/deterministic_records",
            "rank": RANK,
            "A": A,
            "j": geometry["j"],
            "t": geometry["t"],
            "witness_support": "D minus the rank-6 update node set Y",
            "endpoint_co_support": "update nodes Y",
            "base_node_range": geometry["base_node_range"],
            "update_node_range": geometry["update_node_range"],
            "endpoint_support_size": geometry["endpoint_support_size"],
            "threshold_covered": True,
            "vandermonde_independence": {
                "column_sets": "X union Y",
                "column_count": geometry["vandermonde_column_count"],
                "syndrome_length": SYNDROME_LENGTH,
                "domain_points_distinct": True,
                "status": "independent",
            },
            "support_wise_noncontainment": {
                "g_explained_on_D_minus_Y": True,
                "f_explained_on_D_minus_Y": False,
                "reason": (
                    "Syn(g)=v lies in W_Y, while Syn(f)=u lies in W_X and "
                    "W_X cap W_Y is zero by scaled Vandermonde independence."
                ),
            },
        },
        "source_artifacts": {
            "row_descriptor": {
                "ref": str(ROW_DESCRIPTOR.relative_to(REPO_ROOT)),
                "sha256": file_sha256(ROW_DESCRIPTOR),
            },
            "rank2_11_projective_infinity_endpoint": {
                "ref": ENDPOINT_REF,
                "sha256": file_sha256(ENDPOINT_CERT),
            },
        },
        "root_union_table_ref": "not_enumerated",
        "finite_affine_roots_status": "not_enumerated_in_this_chart_packet",
        "projective_infinity_numerator": 1,
        "nonclaims": [
            "synthetic syndrome-pencil chart only",
            "finite affine roots are not enumerated in this packet",
            "not a full projective-line numerator certificate",
            "not a quotient-image subtraction table",
            "not a worst-case or actual-row M3 threshold bound",
        ],
    }


def check_packet(packet: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(packet)
    if actual != expected:
        raise AssertionError(f"projective pivot packet mismatch: {path}")


def print_summary(packet: dict[str, Any]) -> None:
    coverage = packet["projective_infinity_coverage"]
    print("F_17^32 M3 rank-6 A=426 projective-infinity pivot packet")
    print(f"status: {packet['status']}")
    print(
        "chart={chart}, point={point}, contribution={count}, support={support}".format(
            chart=packet["exact_agreements"][0]["charts"][0]["chart_id"],
            point=coverage["projective_point"],
            count=coverage["support_count"],
            support=coverage["endpoint_support_size"],
        )
    )
    print(
        "Vandermonde columns={columns} <= syndrome_length={length}".format(
            columns=coverage["vandermonde_independence"]["column_count"],
            length=coverage["vandermonde_independence"]["syndrome_length"],
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic packet")
    parser.add_argument("--check", type=Path, help="check deterministic packet")
    parser.add_argument("--json", action="store_true", help="print packet JSON")
    args = parser.parse_args()

    packet = build_packet()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(packet), encoding="utf-8")
    if args.check:
        check_packet(packet, args.check)
    if args.json:
        print(render(packet), end="")
        return
    print_summary(packet)


if __name__ == "__main__":
    main()
