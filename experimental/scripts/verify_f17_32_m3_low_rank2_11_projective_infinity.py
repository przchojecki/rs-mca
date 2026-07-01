#!/usr/bin/env python3
"""Verify the projective-infinity endpoint for M3 low-rank ranks 2..11.

For the nested low-rank synthetic pencils in the F_17^32 M3 regular window,

    u_m = sum_{x in X} x^m,      v_m = sum_{y in Y} y^m,

where X is the first j+1 descriptor-domain nodes and Y is the next s nodes.
The projective endpoint [0:1] is the word with syndrome v.  It is explained on
the support D\\Y because v lies in the span of the parity-check columns indexed
by Y.  The pair (u,v) is not simultaneously explained on D\\Y: u lies in the
span of the columns indexed by X, and the columns indexed by X union Y are
Vandermonde independent because |X|+|Y| <= n-k and all domain points are
distinct.

Thus the one projective endpoint counted by the low-rank regular packets is
not merely "not excluded" by the top-degree regular minor; it is an actual
support-wise noncontained projective parameter for this synthetic family.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-low-rank2-11-projective-infinity-v1"
N = 512
K = 256
SYNDROME_LENGTH = N - K
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = list(range(2, 12))

ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_RANK_TEMPLATE = REPO_ROOT / (
    "experimental/data/certificates/hankel-low-rank-update-template/"
    "hankel_low_rank_update_template_certificate.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/"
    "f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json"
)


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def object_sha256(value: Any) -> str:
    return sha256(render(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_inputs(descriptor: dict[str, Any], template: dict[str, Any]) -> None:
    require(descriptor["row"]["n"] == N, "row descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "row descriptor k mismatch")
    require(
        descriptor["field_model"]["p"] == 17
        and len(descriptor["field_model"]["modulus"]) == 33,
        "row descriptor field-model mismatch",
    )
    domain = descriptor["domain"]["domain_encodings"]
    require(len(domain) == N, "domain length mismatch")
    require(len(set(domain)) == N, "domain encodings are not distinct")
    require(
        template["schema_version"] == "m1-hankel-low-rank-update-template-v4",
        "low-rank template schema mismatch",
    )


def build_records() -> list[dict[str, Any]]:
    records = []
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        j = N - agreement
        base_node_count = j + 1
        for rank in RANKS:
            update_start = base_node_count
            update_end = base_node_count + rank - 1
            endpoint_support_size = N - rank
            vandermonde_column_count = base_node_count + rank
            require(update_end < N, "update-node range exceeds domain")
            require(
                vandermonde_column_count <= SYNDROME_LENGTH,
                "Vandermonde independence range exceeds syndrome length",
            )
            require(
                endpoint_support_size >= agreement,
                "endpoint support does not cover the agreement threshold",
            )
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": j,
                    "t": agreement - K,
                    "base_node_count": base_node_count,
                    "base_node_range": [0, base_node_count - 1],
                    "update_node_range": [update_start, update_end],
                    "update_node_count": rank,
                    "projective_point": "[0:1]",
                    "endpoint_co_support": "update nodes Y",
                    "endpoint_support_size": endpoint_support_size,
                    "threshold_covered": True,
                    "vandermonde_independence_audit": {
                        "column_sets": "X union Y",
                        "column_count": vandermonde_column_count,
                        "syndrome_length": SYNDROME_LENGTH,
                        "domain_points_distinct": True,
                        "status": "independent",
                    },
                    "support_wise_noncontainment_audit": {
                        "g_explained_on_D_minus_Y": True,
                        "reason_g": (
                            "Syn(g)=v lies in the parity-column span W_Y; "
                            "equivalently the locator L_Y gives the syndrome "
                            "recurrence on D minus Y"
                        ),
                        "f_explained_on_D_minus_Y": False,
                        "reason_f": (
                            "Syn(f)=u lies in W_X and W_X intersects W_Y "
                            "trivially because the scaled Vandermonde columns "
                            "on X union Y are independent"
                        ),
                        "status": "support_wise_noncontained",
                    },
                    "projective_infinity_contribution": 1,
                }
            )
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    rank_summaries = {}
    for rank in RANKS:
        rank_records = [record for record in records if record["rank"] == rank]
        require(len(rank_records) == 42, f"rank={rank}: record count mismatch")
        rank_summaries[str(rank)] = {
            "rank": rank,
            "agreement_count": len(rank_records),
            "endpoint_support_size": N - rank,
            "minimum_threshold": AGREEMENT_MIN,
            "maximum_threshold": AGREEMENT_MAX,
            "thresholds_covered": True,
            "projective_infinity_contribution_sum": len(rank_records),
            "maximum_vandermonde_column_count": max(
                record["vandermonde_independence_audit"]["column_count"]
                for record in rank_records
            ),
        }
    return {
        "rank_summaries": rank_summaries,
        "rank_count": len(RANKS),
        "record_count": len(records),
        "agreement_count": AGREEMENT_MAX - AGREEMENT_MIN + 1,
        "projective_point": "[0:1]",
        "projective_infinity_contribution_per_record": 1,
        "projective_infinity_contribution_sum": len(records),
        "minimum_endpoint_support_size": min(N - rank for rank in RANKS),
        "maximum_agreement_threshold": AGREEMENT_MAX,
        "maximum_vandermonde_column_count": max(
            record["vandermonde_independence_audit"]["column_count"]
            for record in records
        ),
        "syndrome_length": SYNDROME_LENGTH,
        "all_thresholds_covered": True,
        "all_vandermonde_independence_checks_pass": True,
        "all_endpoint_noncontainment_checks_pass": True,
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR)
    template = load_json(LOW_RANK_TEMPLATE)
    validate_inputs(descriptor, template)
    records = build_records()
    aggregate = summarize(records)
    require(aggregate["record_count"] == len(RANKS) * 42, "record total mismatch")
    require(
        aggregate["minimum_endpoint_support_size"] == N - max(RANKS),
        "minimum endpoint support mismatch",
    )
    require(
        aggregate["maximum_vandermonde_column_count"]
        == (N - AGREEMENT_MIN + 1) + max(RANKS),
        "maximum Vandermonde column count mismatch",
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": descriptor["row"]["domain_description"],
        },
        "source_artifacts": {
            "row_descriptor": {
                "ref": str(ROW_DESCRIPTOR.relative_to(REPO_ROOT)),
                "sha256": file_sha256(ROW_DESCRIPTOR),
            },
            "low_rank_template": {
                "ref": str(LOW_RANK_TEMPLATE.relative_to(REPO_ROOT)),
                "sha256": file_sha256(LOW_RANK_TEMPLATE),
                "schema_version": template["schema_version"],
            },
        },
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "construction": {
            "base_nodes": "first j+1 descriptor-domain elements",
            "update_nodes": "first s nodes after the base prefix",
            "ranks": RANKS,
            "projective_point": "[0:1]",
            "certificate_mode": "low_rank_projective_infinity_endpoint",
        },
        "deterministic_records": {
            "storage": (
                "compressed; verifier rebuilds all rows from agreement_range "
                "and ranks"
            ),
            "record_count": len(records),
            "record_sha256": object_sha256({"records": records}),
            "first_record": records[0],
            "last_record": records[-1],
        },
        "method": {
            "theorem": (
                "For u_m=sum_{x in X}x^m and v_m=sum_{y in Y}y^m with "
                "X and Y disjoint and |X|+|Y|<=n-k, the projective endpoint "
                "[0:1] is support-wise noncontained on D\\Y."
            ),
            "g_endpoint_witness": "Syn(g)=v is in the parity-column span W_Y",
            "noncontainment_test": (
                "Syn(f)=u is not in W_Y because u is a nonzero vector in W_X "
                "and W_X cap W_Y is zero by Vandermonde independence on X union Y"
            ),
            "agreement_check": "D\\Y has size n-s, which is at least every A in 385..426 for s<=11",
            "consequence": (
                "the projective infinity point contributes exactly one "
                "support-wise noncontained projective parameter in each checked "
                "rank/agreement row"
            ),
        },
        "aggregate": aggregate,
        "nonclaims": [
            "synthetic syndrome-pencil family only",
            "does not enumerate finite affine roots",
            "not a quotient-image subtraction audit",
            "not a worst-case M3 row bound",
            "does not classify arbitrary non-proportional pencils",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-2..11 projective-infinity mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank-2..11 projective-infinity endpoint")
    print(f"status: {certificate['status']}")
    print(
        "agreements: {lo}..{hi}, ranks={ranks}, records={records}".format(
            lo=certificate["agreement_range"][0],
            hi=certificate["agreement_range"][1],
            ranks=certificate["construction"]["ranks"],
            records=aggregate["record_count"],
        )
    )
    print(
        (
            "projective endpoint {point}: contribution_sum={count}, "
            "min_support={support}, max_A={max_a}"
        ).format(
            point=aggregate["projective_point"],
            count=aggregate["projective_infinity_contribution_sum"],
            support=aggregate["minimum_endpoint_support_size"],
            max_a=aggregate["maximum_agreement_threshold"],
        )
    )
    print(
        "max Vandermonde columns={columns} <= syndrome_length={length}".format(
            columns=aggregate["maximum_vandermonde_column_count"],
            length=aggregate["syndrome_length"],
        )
    )


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
