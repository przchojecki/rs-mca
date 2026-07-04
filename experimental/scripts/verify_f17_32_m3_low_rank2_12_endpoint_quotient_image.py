#!/usr/bin/env python3
r"""Verify quotient-image witnesses for low-rank2..12 projective endpoints.

For the synthetic low-rank ladder, the projective endpoint ``[0:1]`` is the
syndrome direction ``v_m=sum_{y in Y} y^m``.  This verifier constructs, for
every rank/agreement row, an agreement-size quotient-remainder support from
``c=2`` fibers that avoids the update block ``Y``.  Its co-support therefore
contains ``Y`` and explains ``v``, while it cannot explain the base syndrome
``u_m=sum_{x in X} x^m`` by Vandermonde independence on ``X union T``.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-low-rank2-12-endpoint-quotient-image-v1"
N = 512
K = 256
SYNDROME_LENGTH = N - K
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = list(range(2, 13))
FIBER_SIZE = 2
QUOTIENT_ORDER = N // FIBER_SIZE

PAPER_D_REF = REPO_ROOT / "tex/cs25_cap_v12.tex"
ROW_DESCRIPTOR_REF = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-12-endpoint-quotient-image/"
    "f17_32_n512_k256_m3_low_rank2_12_endpoint_quotient_image.json"
)


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def object_sha256(value: Any) -> str:
    return sha256(render(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def normalize_source_artifacts_for_check(value: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(value)
    artifacts = normalized.get("source_artifacts")
    if isinstance(artifacts, dict):
        if "paper_d_v12" in artifacts and "paper_d_v10" not in artifacts:
            artifacts["paper_d_v10"] = artifacts.pop("paper_d_v12")
        for record in artifacts.values():
            if isinstance(record, dict):
                if "ref" in record:
                    record["ref"] = str(record["ref"]).replace("\\", "/")
                if "sha256" in record:
                    record["sha256"] = "<source-artifact-sha256>"
    return normalized


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


def quotient_remainder_support_avoiding_y(
    agreement: int,
    update_start: int,
    rank: int,
) -> dict[str, Any]:
    update_exponents = set(range(update_start, update_start + rank))
    hit_residues = {exponent % QUOTIENT_ORDER for exponent in update_exponents}
    safe_residues = [
        residue for residue in range(QUOTIENT_ORDER) if residue not in hit_residues
    ]
    full_fiber_count = agreement // FIBER_SIZE
    remainder_size = agreement % FIBER_SIZE
    require(
        len(safe_residues) >= full_fiber_count + remainder_size,
        "not enough c=2 fibers avoiding Y",
    )

    full_fiber_residues = safe_residues[:full_fiber_count]
    support: set[int] = set()
    for residue in full_fiber_residues:
        support.update(c2_fiber(residue))
    remainder_exponents = []
    if remainder_size:
        residue = safe_residues[full_fiber_count]
        remainder_exponents = [residue]
        support.add(residue)

    require(len(support) == agreement, "support size mismatch")
    require(support.isdisjoint(update_exponents), "support hits update block")
    return {
        "fiber_size": FIBER_SIZE,
        "quotient_order": QUOTIENT_ORDER,
        "support_size": agreement,
        "full_fiber_count": full_fiber_count,
        "remainder_size": remainder_size,
        "full_fiber_residue_range": [
            full_fiber_residues[0],
            full_fiber_residues[-1],
        ],
        "full_fiber_residue_count": len(full_fiber_residues),
        "remainder_exponents": remainder_exponents,
        "hit_update_residues": sorted(hit_residues),
        "support_avoids_update_block": True,
        "support_exponent_hash": object_sha256(sorted(support)),
        "co_support_size": N - len(support),
        "co_support_contains_update_block": True,
    }


def build_records() -> list[dict[str, Any]]:
    records = []
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        j = N - agreement
        base_node_count = j + 1
        for rank in RANKS:
            update_start = base_node_count
            update_end = update_start + rank - 1
            support = quotient_remainder_support_avoiding_y(
                agreement,
                update_start,
                rank,
            )
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
                    "t": agreement - K,
                    "base_node_count": base_node_count,
                    "base_node_range": [0, base_node_count - 1],
                    "update_node_range": [update_start, update_end],
                    "projective_point": "[0:1]",
                    "quotient_remainder_witness_support": support,
                    "endpoint_image_audit": {
                        "v_explained_on_quotient_co_support": True,
                        "reason_v": (
                            "the quotient co-support contains Y, and Syn(g)=v "
                            "lies in the parity-column span W_Y"
                        ),
                        "u_explained_on_quotient_co_support": False,
                        "reason_u": (
                            "Syn(f)=u lies in W_X with |X|=j+1, while the "
                            "quotient co-support T has size j; if u lay in "
                            "W_T then the Vandermonde columns on X union T "
                            "would satisfy a nontrivial relation"
                        ),
                        "vandermonde_union_bound": vandermonde_union_bound,
                        "syndrome_length": SYNDROME_LENGTH,
                        "status": "quotient_image_witness",
                    },
                }
            )
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    rank_summaries = {}
    for rank in RANKS:
        rank_records = [record for record in records if record["rank"] == rank]
        rank_summaries[str(rank)] = {
            "rank": rank,
            "agreement_count": len(rank_records),
            "endpoint_quotient_image_witness_count": len(rank_records),
            "fiber_size": FIBER_SIZE,
            "all_witnesses_use_c2": True,
            "maximum_vandermonde_union_bound": max(
                record["endpoint_image_audit"]["vandermonde_union_bound"]
                for record in rank_records
            ),
        }
    return {
        "record_count": len(records),
        "rank_count": len(RANKS),
        "agreement_count": AGREEMENT_MAX - AGREEMENT_MIN + 1,
        "fiber_size": FIBER_SIZE,
        "quotient_order": QUOTIENT_ORDER,
        "projective_point": "[0:1]",
        "endpoint_quotient_image_witness_count": len(records),
        "all_projective_endpoints_have_quotient_image_witness": True,
        "maximum_vandermonde_union_bound": max(
            record["endpoint_image_audit"]["vandermonde_union_bound"]
            for record in records
        ),
        "syndrome_length": SYNDROME_LENGTH,
        "rank_summaries": rank_summaries,
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    validate_descriptor(descriptor)
    records = build_records()
    aggregate = summarize(records)
    require(aggregate["record_count"] == len(RANKS) * 42, "record total")
    require(
        aggregate["maximum_vandermonde_union_bound"] == 255,
        "unexpected Vandermonde union maximum",
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
            "paper_d_v12": {
                "ref": str(PAPER_D_REF.relative_to(REPO_ROOT)),
                "sha256": file_sha256(PAPER_D_REF),
            },
            "row_descriptor": {
                "ref": str(ROW_DESCRIPTOR_REF.relative_to(REPO_ROOT)),
                "sha256": file_sha256(ROW_DESCRIPTOR_REF),
                "schema_version": descriptor["schema_version"],
            },
        },
        "method": {
            "quotient_remainder_witness": (
                "construct an agreement-size support from c=2 quotient fibers "
                "plus the parity remainder, choosing only residues that avoid "
                "the update block Y"
            ),
            "image_map": (
                "because the quotient co-support contains Y, [0:1] is "
                "explained there by v; because |X|=j+1, |T|=j, and "
                "|X union T|<=n-k, u is not explained there"
            ),
            "projective_endpoint": (
                "for projective line Z0*u + Z1*v, this witness contributes "
                "the single quotient-image point [0:1]"
            ),
        },
        "aggregate": aggregate,
        "deterministic_records": {
            "storage": "compressed; verifier rebuilds all quotient-image witnesses",
            "record_count": len(records),
            "record_sha256": object_sha256({"records": records}),
            "first_record": records[0],
            "last_record": records[-1],
        },
        "claim": (
            "For every synthetic rank-2..12 projective endpoint row in the "
            "F_17^32 M3 regular window, the endpoint [0:1] lies in the "
            "quotient-image branch: it has an explicit c=2 quotient-remainder "
            "witness support of size A."
        ),
        "nonclaims": [
            "synthetic low-rank endpoint rows only",
            "finite affine regular-minor roots are not audited here",
            "does not claim the minimal endpoint support D minus Y is quotient-remainder",
            "not an arbitrary-row M3 threshold bound",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        actual_certificate = json.loads(actual)
        if normalize_source_artifacts_for_check(
            actual_certificate
        ) == normalize_source_artifacts_for_check(certificate):
            return
        raise AssertionError(f"endpoint quotient-image mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank endpoint quotient-image witness")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, fiber_size={fiber}, max_vandermonde={max_v}".format(
            records=aggregate["record_count"],
            fiber=aggregate["fiber_size"],
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
