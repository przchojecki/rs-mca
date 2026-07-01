#!/usr/bin/env python3
"""Verify the c=2 quotient-image capacity for M3 projective endpoints.

For the synthetic M3 low-rank ladder at agreement A, put j=512-A and let the
update block Y start immediately after the j+1 base nodes.  The projective
endpoint [0:1] is the update syndrome direction v.  This verifier proves that
the endpoint has a c=2 quotient-remainder witness for every synthetic rank

    2 <= rank <= 256 - floor(A/2) = ceil((512-A)/2).

The bound is the exact full-fiber capacity for this construction: a full c=2
fiber used by the agreement support must avoid Y, and there are exactly
256-rank such fibers.  When A is odd, the final residual point may be taken from
the paired point of a blocked fiber at the boundary rank.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-endpoint-c2-capacity-v1"
N = 512
K = 256
SYNDROME_LENGTH = N - K
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANK_MIN = 2
FIBER_SIZE = 2
QUOTIENT_ORDER = N // FIBER_SIZE

V10_PAPER_REF = REPO_ROOT / "tex/cs25_cap_v10.tex"
ROW_DESCRIPTOR_REF = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-endpoint-c2-capacity/"
    "f17_32_n512_k256_m3_endpoint_c2_capacity.json"
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


def validate_descriptor(descriptor: dict[str, Any]) -> None:
    require(
        descriptor["schema_version"] == "f17-32-hankel-row-descriptor-v1",
        "row descriptor schema",
    )
    require(descriptor["status"] == "AUDIT", "row descriptor status")
    require(descriptor["row"]["n"] == N, "row descriptor n")
    require(descriptor["row"]["k"] == K, "row descriptor k")
    require(descriptor["row"]["field"] == "F_17^32", "row descriptor field")
    domain = descriptor["domain"]["domain_encodings"]
    require(len(domain) == N, "domain length")
    require(len(set(domain)) == N, "domain distinctness")


def c2_fiber(residue: int) -> list[int]:
    return [residue, residue + QUOTIENT_ORDER]


def rank_capacity(agreement: int) -> int:
    return QUOTIENT_ORDER - agreement // FIBER_SIZE


def max_square_update_rank(agreement: int) -> int:
    return N - agreement + 1


def full_fiber_avoidance_obstruction(
    agreement: int,
    rank: int,
) -> dict[str, Any]:
    j = N - agreement
    update_start = j + 1
    update_exponents = set(range(update_start, update_start + rank))
    require(max(update_exponents) < QUOTIENT_ORDER, "update block crosses residue line")
    hit_residues = {exponent % QUOTIENT_ORDER for exponent in update_exponents}
    safe_full_fibers = QUOTIENT_ORDER - len(hit_residues)
    required_full_fibers = agreement // FIBER_SIZE
    full_fiber_deficit = required_full_fibers - safe_full_fibers
    return {
        "rank": rank,
        "update_node_range": [update_start, update_start + rank - 1],
        "required_full_fiber_count": required_full_fibers,
        "safe_full_fiber_count": safe_full_fibers,
        "full_fiber_deficit": full_fiber_deficit,
        "remainder_size": agreement % FIBER_SIZE,
        "obstructed_by_full_fiber_count": full_fiber_deficit > 0,
    }


def quotient_remainder_support(
    agreement: int,
    update_start: int,
    rank: int,
) -> dict[str, Any]:
    update_exponents = set(range(update_start, update_start + rank))
    require(max(update_exponents) < QUOTIENT_ORDER, "update block crosses residue line")
    hit_residues = {exponent % QUOTIENT_ORDER for exponent in update_exponents}
    safe_residues = [
        residue for residue in range(QUOTIENT_ORDER) if residue not in hit_residues
    ]
    full_fiber_count = agreement // FIBER_SIZE
    remainder_size = agreement % FIBER_SIZE
    require(
        len(safe_residues) >= full_fiber_count,
        "not enough full c=2 fibers avoiding Y",
    )

    full_fiber_residues = safe_residues[:full_fiber_count]
    support: set[int] = set()
    for residue in full_fiber_residues:
        support.update(c2_fiber(residue))

    residual_strategy = "none"
    remainder_exponents: list[int] = []
    if remainder_size:
        unused_safe_residues = safe_residues[full_fiber_count:]
        if unused_safe_residues:
            residue = unused_safe_residues[0]
            remainder_exponents = [residue]
            residual_strategy = "unused_safe_residue"
        else:
            residue = min(hit_residues)
            paired = residue + QUOTIENT_ORDER
            require(paired not in update_exponents, "paired residual hits Y")
            remainder_exponents = [paired]
            residual_strategy = "paired_point_of_blocked_residue"
        support.update(remainder_exponents)

    require(len(support) == agreement, "support size mismatch")
    require(support.isdisjoint(update_exponents), "support hits update block")
    return {
        "fiber_size": FIBER_SIZE,
        "quotient_order": QUOTIENT_ORDER,
        "support_size": agreement,
        "full_fiber_count": full_fiber_count,
        "remainder_size": remainder_size,
        "full_fiber_residue_count": len(full_fiber_residues),
        "hit_update_residue_count": len(hit_residues),
        "safe_full_fiber_count": len(safe_residues),
        "residual_strategy": residual_strategy,
        "remainder_exponents": remainder_exponents,
        "support_avoids_update_block": True,
        "support_exponent_hash": object_sha256(sorted(support)),
        "co_support_size": N - len(support),
        "co_support_contains_update_block": True,
    }


def build_records() -> list[dict[str, Any]]:
    records = []
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        j = N - agreement
        t = agreement - K
        base_node_count = j + 1
        capacity = rank_capacity(agreement)
        require(capacity == (j + 1) // 2, "capacity formula")
        for rank in range(RANK_MIN, capacity + 1):
            update_start = base_node_count
            update_end = update_start + rank - 1
            support = quotient_remainder_support(agreement, update_start, rank)
            require(support["co_support_size"] == j, "co-support size mismatch")
            vandermonde_union_bound = base_node_count + j
            require(
                vandermonde_union_bound <= SYNDROME_LENGTH,
                "Vandermonde independence range too large",
            )
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": j,
                    "t": t,
                    "rank_capacity": capacity,
                    "base_node_count": base_node_count,
                    "update_node_range": [update_start, update_end],
                    "projective_point": "[0:1]",
                    "quotient_remainder_witness_support": support,
                    "endpoint_image_audit": {
                        "v_explained_on_quotient_co_support": True,
                        "u_explained_on_quotient_co_support": False,
                        "vandermonde_union_bound": vandermonde_union_bound,
                        "syndrome_length": SYNDROME_LENGTH,
                        "status": "quotient_image_witness",
                    },
                }
            )
    return records


def build_capacity_table(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    table = []
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        agreement_records = [record for record in records if record["A"] == agreement]
        j = N - agreement
        capacity = rank_capacity(agreement)
        max_update_rank = max_square_update_rank(agreement)
        require(len(agreement_records) == capacity - RANK_MIN + 1, "agreement count")
        boundary = agreement_records[-1]
        first_blocked_rank = capacity + 1
        first_blocked = full_fiber_avoidance_obstruction(
            agreement,
            first_blocked_rank,
        )
        last_blocked = full_fiber_avoidance_obstruction(
            agreement,
            max_update_rank,
        )
        for blocked_rank in range(first_blocked_rank, max_update_rank + 1):
            blocked = full_fiber_avoidance_obstruction(agreement, blocked_rank)
            require(
                blocked["obstructed_by_full_fiber_count"],
                "rank above capacity unexpectedly has enough full fibers",
            )
        table.append(
            {
                "A": agreement,
                "j": j,
                "t": agreement - K,
                "rank_min_recorded": RANK_MIN,
                "rank_capacity": capacity,
                "record_count": len(agreement_records),
                "full_fiber_count": agreement // FIBER_SIZE,
                "remainder_size": agreement % FIBER_SIZE,
                "boundary_residual_strategy": boundary[
                    "quotient_remainder_witness_support"
                ]["residual_strategy"],
                "boundary_safe_full_fiber_count": boundary[
                    "quotient_remainder_witness_support"
                ]["safe_full_fiber_count"],
                "max_square_update_rank_audited": max_update_rank,
                "first_rank_without_c2_full_fiber_avoidance_witness": first_blocked_rank,
                "blocked_rank_count_to_square_size": max_update_rank - capacity,
                "first_blocked_obstruction": first_blocked,
                "last_blocked_obstruction": last_blocked,
            }
        )
    return table


def summarize(records: list[dict[str, Any]], capacity_table: list[dict[str, Any]]) -> dict[str, Any]:
    capacities = [row["rank_capacity"] for row in capacity_table]
    blocked_counts = [row["blocked_rank_count_to_square_size"] for row in capacity_table]
    return {
        "record_count": len(records),
        "agreement_count": AGREEMENT_MAX - AGREEMENT_MIN + 1,
        "rank_min_recorded": RANK_MIN,
        "uniform_rank_capacity": min(capacities),
        "maximum_rank_capacity": max(capacities),
        "minimum_blocked_rank_count_to_square_size": min(blocked_counts),
        "maximum_blocked_rank_count_to_square_size": max(blocked_counts),
        "all_ranks_above_capacity_obstructed_for_c2_full_fiber_avoidance": True,
        "fiber_size": FIBER_SIZE,
        "quotient_order": QUOTIENT_ORDER,
        "projective_point": "[0:1]",
        "endpoint_quotient_image_witness_count": len(records),
        "all_recorded_projective_endpoints_have_quotient_image_witness": True,
        "maximum_vandermonde_union_bound": max(
            record["endpoint_image_audit"]["vandermonde_union_bound"]
            for record in records
        ),
        "syndrome_length": SYNDROME_LENGTH,
        "odd_boundary_uses_paired_residual": all(
            row["boundary_residual_strategy"] == "paired_point_of_blocked_residue"
            for row in capacity_table
            if row["remainder_size"] == 1
        ),
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    validate_descriptor(descriptor)
    records = build_records()
    capacity_table = build_capacity_table(records)
    aggregate = summarize(records, capacity_table)
    expected_records = sum(row["record_count"] for row in capacity_table)
    require(aggregate["record_count"] == expected_records, "record total")
    require(aggregate["uniform_rank_capacity"] == 43, "uniform capacity")
    require(aggregate["maximum_rank_capacity"] == 64, "maximum capacity")
    require(
        aggregate["minimum_blocked_rank_count_to_square_size"] == 44,
        "minimum blocked rank count",
    )
    require(
        aggregate["maximum_blocked_rank_count_to_square_size"] == 64,
        "maximum blocked rank count",
    )
    require(aggregate["maximum_vandermonde_union_bound"] == 255, "Vandermonde maximum")

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
        "rank_policy": {
            "rank_min_recorded": RANK_MIN,
            "rank_capacity_formula": "256 - floor(A/2) = ceil((512-A)/2)",
            "uniform_rank_capacity_over_window": aggregate["uniform_rank_capacity"],
            "necessity_audit_range": "rank_capacity(A)+1 <= rank <= j+1",
            "max_square_update_rank_formula": "j+1 = 513-A",
            "rank_1_omitted_by_low_rank2_convention": True,
        },
        "source_artifacts": {
            "paper_d_v10": {
                "ref": str(V10_PAPER_REF.relative_to(REPO_ROOT)),
                "sha256": file_sha256(V10_PAPER_REF),
            },
            "row_descriptor": {
                "ref": str(ROW_DESCRIPTOR_REF.relative_to(REPO_ROOT)),
                "sha256": file_sha256(ROW_DESCRIPTOR_REF),
                "schema_version": descriptor["schema_version"],
            },
        },
        "method": {
            "capacity_argument": (
                "A c=2 quotient-remainder support of size A needs floor(A/2) "
                "full c=2 fibers avoiding the update block Y.  In this "
                "synthetic ladder Y occupies rank distinct residues below the "
                "quotient modulus, so exactly 256-rank full fibers avoid Y.  "
                "Thus rank <= 256-floor(A/2) is the full-fiber capacity."
            ),
            "necessity_argument": (
                "For rank > 256-floor(A/2), fewer than floor(A/2) complete "
                "c=2 fibers avoid Y.  Therefore no c=2 quotient-remainder "
                "support whose complete fibers avoid Y can pay the endpoint "
                "in that rank range.  The verifier checks every rank up to "
                "the square-minor update size j+1."
            ),
            "odd_agreement_residual": (
                "When A is odd and the boundary rank exhausts the safe full "
                "fibers, the single residual point is taken from the paired "
                "point residue+256 of a blocked residue; this point is outside Y."
            ),
            "image_map": (
                "The quotient co-support contains Y and explains v.  The base "
                "syndrome u is excluded by Vandermonde independence because "
                "|X|=j+1, |T|=j, and |X union T|<=n-k."
            ),
        },
        "capacity_table": capacity_table,
        "aggregate": aggregate,
        "deterministic_records": {
            "storage": "compressed; verifier rebuilds all endpoint witnesses",
            "record_count": len(records),
            "record_sha256": object_sha256({"records": records}),
            "first_record": records[0],
            "last_record": records[-1],
        },
        "claim": (
            "For every A=385..426 and every synthetic rank "
            "2 <= rank <= 256-floor(A/2), the projective endpoint [0:1] "
            "lies in the c=2 quotient-image branch.  In particular, endpoint "
            "charging is available uniformly through rank 43 across the M3 "
            "window.  Conversely, for rank_capacity(A)<rank<=j+1, this "
            "specific c=2 full-fiber avoidance mechanism is obstructed by "
            "the full-fiber count."
        ),
        "nonclaims": [
            "endpoint quotient-image witnesses only",
            "synthetic low-rank update blocks only",
            "does not audit finite affine regular-minor roots",
            "does not claim an arbitrary-row M3 threshold bound",
            "does not rule out other endpoint ledgers beyond the c=2 full-fiber avoidance mechanism",
            "does not claim the minimal endpoint support D minus Y is quotient-remainder",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"endpoint c=2 capacity mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 endpoint c=2 quotient-image capacity")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, uniform_rank_capacity={uniform}, max_rank_capacity={max_rank}, max_vandermonde={max_v}".format(
            records=aggregate["record_count"],
            uniform=aggregate["uniform_rank_capacity"],
            max_rank=aggregate["maximum_rank_capacity"],
            max_v=aggregate["maximum_vandermonde_union_bound"],
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
