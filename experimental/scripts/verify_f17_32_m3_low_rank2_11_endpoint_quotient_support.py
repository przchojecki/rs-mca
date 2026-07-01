#!/usr/bin/env python3
"""Verify quotient-support exclusion for M3 low-rank projective endpoints.

For the synthetic low-rank ladder the projective endpoint [0:1] is witnessed on
``D \\ Y``, where ``Y`` is a consecutive block of descriptor-domain nodes of
size ``s``.  This script checks that these endpoint supports are not
quotient-remainder supports for any nontrivial proper quotient fiber size
``2 <= c <= 256``.

Criterion used.  Let the quotient fibers have size ``c``.  A support ``D \\ Y``
of size ``n-s`` is a quotient-remainder support only if ``Y`` meets the minimum
possible number ``ceil(s/c)`` of quotient fibers.  In the order-512 cyclic
domain, quotient fibers are exponent classes modulo ``n/c``.  A consecutive
block of length ``2..11`` meets strictly more than ``ceil(s/c)`` such classes for
every nontrivial proper divisor ``c`` of 512.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-low-rank2-11-endpoint-quotient-support-v1"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = list(range(2, 12))
NONTRIVIAL_PROPER_FIBER_SIZES = [2, 4, 8, 16, 32, 64, 128, 256]
TRIVIAL_FIBER_SIZES = [1, 512]

ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
ENDPOINT_CERT = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/"
    "f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-11-endpoint-quotient-support/"
    "f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_support.json"
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


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def validate_inputs(descriptor: dict[str, Any], endpoint: dict[str, Any]) -> None:
    require(descriptor["row"]["n"] == N, "row descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "row descriptor k mismatch")
    domain = descriptor["domain"]["domain_encodings"]
    require(len(domain) == N, "domain length mismatch")
    require(len(set(domain)) == N, "domain encodings are not distinct")
    require(
        endpoint["schema_version"]
        == "f17-32-m3-low-rank2-11-projective-infinity-v1",
        "endpoint certificate schema mismatch",
    )
    require(
        endpoint["aggregate"]["record_count"] == len(RANKS) * 42,
        "endpoint record count mismatch",
    )
    require(
        endpoint["aggregate"]["all_endpoint_noncontainment_checks_pass"] is True,
        "endpoint noncontainment audit not passed",
    )


def quotient_check(update_start: int, rank: int, fiber_size: int) -> dict[str, Any]:
    quotient_order = N // fiber_size
    update_exponents = list(range(update_start, update_start + rank))
    hit_residues = sorted({exponent % quotient_order for exponent in update_exponents})
    minimum_required = ceil_div(rank, fiber_size)
    gap = len(hit_residues) - minimum_required
    return {
        "fiber_size": fiber_size,
        "quotient_order": quotient_order,
        "minimum_quotient_fibers_for_rank": minimum_required,
        "hit_quotient_fiber_count": len(hit_residues),
        "excess_hit_fibers": gap,
        "support_is_quotient_remainder": gap == 0,
        "hit_residue_sample": hit_residues[:12],
    }


def build_records() -> list[dict[str, Any]]:
    records = []
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        j = N - agreement
        base_node_count = j + 1
        for rank in RANKS:
            update_start = base_node_count
            update_end = update_start + rank - 1
            checks = [
                quotient_check(update_start, rank, fiber_size)
                for fiber_size in NONTRIVIAL_PROPER_FIBER_SIZES
            ]
            require(
                all(not check["support_is_quotient_remainder"] for check in checks),
                f"rank={rank}, A={agreement}: quotient support was not excluded",
            )
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": j,
                    "t": agreement - K,
                    "endpoint_support_size": N - rank,
                    "endpoint_co_support": "rank-s consecutive update block Y",
                    "update_node_range": [update_start, update_end],
                    "nontrivial_quotient_checks": checks,
                    "trivial_fiber_sizes_not_claimed": TRIVIAL_FIBER_SIZES,
                    "nontrivial_quotient_support_status": "excluded",
                }
            )
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    all_checks = [
        check
        for record in records
        for check in record["nontrivial_quotient_checks"]
    ]
    worst_gap = min(check["excess_hit_fibers"] for check in all_checks)
    worst_records = []
    for record in records:
        for check in record["nontrivial_quotient_checks"]:
            if check["excess_hit_fibers"] == worst_gap:
                worst_records.append(
                    {
                        "rank": record["rank"],
                        "A": record["A"],
                        "fiber_size": check["fiber_size"],
                        "quotient_order": check["quotient_order"],
                        "hit_quotient_fiber_count": check[
                            "hit_quotient_fiber_count"
                        ],
                        "minimum_quotient_fibers_for_rank": check[
                            "minimum_quotient_fibers_for_rank"
                        ],
                        "excess_hit_fibers": check["excess_hit_fibers"],
                    }
                )
    rank_summaries = {}
    for rank in RANKS:
        rank_records = [record for record in records if record["rank"] == rank]
        rank_checks = [
            check
            for record in rank_records
            for check in record["nontrivial_quotient_checks"]
        ]
        rank_summaries[str(rank)] = {
            "rank": rank,
            "agreement_count": len(rank_records),
            "endpoint_support_size": N - rank,
            "nontrivial_quotient_checks": len(rank_checks),
            "minimum_excess_hit_fibers": min(
                check["excess_hit_fibers"] for check in rank_checks
            ),
            "all_nontrivial_quotient_supports_excluded": all(
                not check["support_is_quotient_remainder"]
                for check in rank_checks
            ),
        }
    return {
        "record_count": len(records),
        "rank_count": len(RANKS),
        "agreement_count": AGREEMENT_MAX - AGREEMENT_MIN + 1,
        "nontrivial_fiber_sizes": NONTRIVIAL_PROPER_FIBER_SIZES,
        "trivial_fiber_sizes_not_claimed": TRIVIAL_FIBER_SIZES,
        "nontrivial_quotient_check_count": len(all_checks),
        "minimum_excess_hit_fibers": worst_gap,
        "worst_record_count": len(worst_records),
        "worst_record_samples": worst_records[:20],
        "all_nontrivial_quotient_supports_excluded": all(
            not check["support_is_quotient_remainder"] for check in all_checks
        ),
        "rank_summaries": rank_summaries,
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR)
    endpoint = load_json(ENDPOINT_CERT)
    validate_inputs(descriptor, endpoint)
    records = build_records()
    aggregate = summarize(records)
    require(aggregate["record_count"] == 420, "record total mismatch")
    require(
        aggregate["nontrivial_quotient_check_count"] == 420 * 8,
        "quotient check total mismatch",
    )
    require(
        aggregate["minimum_excess_hit_fibers"] >= 1,
        "some nontrivial quotient support was not excluded",
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
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "ranks": RANKS,
        "source_artifacts": {
            "row_descriptor": {
                "ref": str(ROW_DESCRIPTOR.relative_to(REPO_ROOT)),
                "sha256": file_sha256(ROW_DESCRIPTOR),
            },
            "projective_infinity_endpoint": {
                "ref": str(ENDPOINT_CERT.relative_to(REPO_ROOT)),
                "sha256": file_sha256(ENDPOINT_CERT),
                "schema_version": endpoint["schema_version"],
            },
        },
        "method": {
            "criterion": (
                "D minus Y is a quotient-remainder support for fiber size c "
                "only if Y meets exactly ceil(|Y|/c) quotient fibers"
            ),
            "quotient_fibers": "exponent classes modulo n/c in the order-512 cyclic domain",
            "co_support_shape": "consecutive descriptor exponent block of length rank",
            "excluded_fiber_sizes": NONTRIVIAL_PROPER_FIBER_SIZES,
            "trivial_fiber_sizes_not_claimed": TRIVIAL_FIBER_SIZES,
        },
        "aggregate": aggregate,
        "deterministic_records": {
            "storage": "compressed; verifier rebuilds all rank/agreement quotient checks",
            "record_count": len(records),
            "record_sha256": object_sha256({"records": records}),
            "first_record": records[0],
            "last_record": records[-1],
        },
        "claim": (
            "For every synthetic rank-2..11 projective endpoint support D\\Y "
            "and every nontrivial proper quotient fiber size c in "
            "{2,4,8,16,32,64,128,256}, the support is not in the "
            "quotient-remainder support family."
        ),
        "nonclaims": [
            "trivial c=1 and c=512 support families are not excluded",
            "finite affine regular-minor roots are not audited here",
            "not a quotient-image audit for arbitrary supports",
            "not an actual-row M3 threshold bound",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"endpoint quotient-support mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank endpoint quotient-support exclusion")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, quotient_checks={checks}, min_excess={gap}".format(
            records=aggregate["record_count"],
            checks=aggregate["nontrivial_quotient_check_count"],
            gap=aggregate["minimum_excess_hit_fibers"],
        )
    )
    print(
        "nontrivial fiber sizes excluded={sizes}".format(
            sizes=aggregate["nontrivial_fiber_sizes"]
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
