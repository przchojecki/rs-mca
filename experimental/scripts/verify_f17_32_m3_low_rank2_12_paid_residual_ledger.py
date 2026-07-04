#!/usr/bin/env python3
"""Verify the paid-residual ledger for the low-rank2..12 M3 packet.

This verifier composes two standalone certificates in the same PR:

* the affine-gcd packet, which proves that the v10 canonical finite affine
  rank-drop root set is empty for every synthetic rank/agreement row;
* the endpoint quotient-image packet, which charges the remaining projective
  endpoint [0:1] to an explicit c=2 quotient-remainder witness.

The output is a compact M3/M4-style residual ledger: after removing the paid
quotient-image endpoint, every synthetic projective row has zero unpaid regular
projective rank-drop numerator.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-low-rank2-12-paid-residual-ledger-v1"
N = 512
K = 256
SYNDROME_LENGTH = N - K
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = list(range(2, 13))
EXPECTED_RECORDS = len(RANKS) * (AGREEMENT_MAX - AGREEMENT_MIN + 1)
PAPER_D_REF = "tex/cs25_cap_v12.tex"
PAPER_D_SOURCE_KEYS = ("paper_d_v12", "paper_d_v10")

AFFINE_CERT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-12-v10-affine-gcd/"
    "f17_32_n512_k256_m3_low_rank2_12_v10_affine_gcd.json"
)
ENDPOINT_CERT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-12-endpoint-quotient-image/"
    "f17_32_n512_k256_m3_low_rank2_12_endpoint_quotient_image.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-12-paid-residual-ledger/"
    "f17_32_n512_k256_m3_low_rank2_12_paid_residual_ledger.json"
)


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def object_sha256(value: Any) -> str:
    return sha256(render(value).encode("utf-8")).hexdigest()


def ref_path(ref: str) -> Path:
    return REPO_ROOT / ref


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref_path(ref) if isinstance(ref, str) else ref
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(ref: str | Path) -> str:
    path = ref_path(ref) if isinstance(ref, str) else ref
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def source_record(name: str, ref: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "ref": ref,
        "sha256": file_sha256(ref),
        "schema_version": data.get("schema_version"),
        "status": data.get("status"),
    }


def source_lookup(certificate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    artifacts = certificate.get("source_artifacts", {})
    if isinstance(artifacts, list):
        return {record["name"]: record for record in artifacts}
    return artifacts


def normalized_ref(record: dict[str, Any]) -> str:
    return str(record.get("ref", "")).replace("\\", "/")


def normalize_source_artifacts_for_check(value: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(value)
    artifacts = normalized.get("source_artifacts")
    if isinstance(artifacts, list):
        for record in artifacts:
            if "ref" in record:
                record["ref"] = str(record["ref"]).replace("\\", "/")
            if "sha256" in record:
                record["sha256"] = "<source-artifact-sha256>"
    elif isinstance(artifacts, dict):
        for record in artifacts.values():
            if isinstance(record, dict):
                if "ref" in record:
                    record["ref"] = str(record["ref"]).replace("\\", "/")
                if "sha256" in record:
                    record["sha256"] = "<source-artifact-sha256>"
    return normalized


def paper_d_source_record(
    sources: dict[str, dict[str, Any]],
    label: str,
) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for key in PAPER_D_SOURCE_KEYS:
        if key in sources:
            candidates.append(sources[key])
    candidates.extend(
        record for record in sources.values() if normalized_ref(record) == PAPER_D_REF
    )
    valid = [
        record
        for record in candidates
        if normalized_ref(record) == PAPER_D_REF and "sha256" in record
    ]
    require(valid, f"{label} Paper D source record missing")
    hashes = {record["sha256"] for record in valid}
    require(len(hashes) == 1, f"{label} Paper D source hash ambiguous")
    return valid[0]


def validate_common_shape(certificate: dict[str, Any], schema: str, label: str) -> None:
    require(certificate["schema_version"] == schema, f"{label} schema")
    require(certificate["status"] == "PROVED / AUDIT", f"{label} status")
    require(certificate["row"]["n"] == N, f"{label} row n")
    require(certificate["row"]["k"] == K, f"{label} row k")
    require(certificate["row"]["field"] == "F_17^32", f"{label} field")
    require(certificate["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX], f"{label} range")
    require(certificate["ranks"] == RANKS, f"{label} ranks")


def validate_affine_certificate(certificate: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    validate_common_shape(
        certificate,
        "f17-32-m3-low-rank2-12-v10-affine-gcd-v1",
        "affine",
    )
    aggregate = certificate["aggregate"]
    require(aggregate["record_count"] == EXPECTED_RECORDS, "affine record count")
    require(
        aggregate["two_minor_common_gcd_degree_histogram"] == {"0": EXPECTED_RECORDS},
        "affine gcd histogram",
    )
    require(
        aggregate["v10_canonical_affine_rank_drop_root_count_sum"] == 0,
        "affine root sum",
    )
    require(
        aggregate["all_records_have_empty_affine_rank_drop_gcd"] is True,
        "affine empty-gcd flag",
    )
    require(
        aggregate["projective_endpoint_status"] == "not_claimed_in_this_packet",
        "affine endpoint nonclaim",
    )

    records_by_key: dict[tuple[int, int], dict[str, Any]] = {}
    for record in certificate["records"]:
        rank = record["rank"]
        agreement = record["A"]
        require(rank in RANKS, "affine record rank")
        require(AGREEMENT_MIN <= agreement <= AGREEMENT_MAX, "affine record A")
        require(record["j"] == N - agreement, "affine record j")
        require(record["t"] == agreement - K, "affine record t")
        require(record["two_minor_common_gcd_degree"] == 0, "affine record gcd")
        require(
            record["v10_canonical_affine_rank_drop_root_count"] == 0,
            "affine record roots",
        )
        key = (rank, agreement)
        require(key not in records_by_key, "duplicate affine record")
        records_by_key[key] = record

    require(len(records_by_key) == EXPECTED_RECORDS, "affine key count")
    return records_by_key


def validate_endpoint_certificate(
    certificate: dict[str, Any],
    row_hash: str,
) -> None:
    validate_common_shape(
        certificate,
        "f17-32-m3-low-rank2-12-endpoint-quotient-image-v1",
        "endpoint",
    )
    require(certificate["row"]["domain_hash"] == row_hash, "endpoint row hash")
    aggregate = certificate["aggregate"]
    require(aggregate["record_count"] == EXPECTED_RECORDS, "endpoint record count")
    require(aggregate["projective_point"] == "[0:1]", "endpoint point")
    require(
        aggregate["all_projective_endpoints_have_quotient_image_witness"] is True,
        "endpoint all-witness flag",
    )
    require(
        aggregate["endpoint_quotient_image_witness_count"] == EXPECTED_RECORDS,
        "endpoint witness count",
    )
    require(aggregate["fiber_size"] == 2, "endpoint fiber size")
    require(aggregate["quotient_order"] == N // 2, "endpoint quotient order")
    require(
        aggregate["maximum_vandermonde_union_bound"] == 255,
        "endpoint Vandermonde maximum",
    )
    require(aggregate["syndrome_length"] == SYNDROME_LENGTH, "endpoint syndrome length")


def validate_source_consistency(
    affine: dict[str, Any],
    endpoint: dict[str, Any],
) -> None:
    affine_sources = source_lookup(affine)
    endpoint_sources = source_lookup(endpoint)
    affine_paper = paper_d_source_record(affine_sources, "affine")
    endpoint_paper = paper_d_source_record(endpoint_sources, "endpoint")
    require(
        affine_paper["sha256"] == endpoint_paper["sha256"],
        "Paper D source hash mismatch",
    )
    require(
        affine_sources["row_descriptor"]["sha256"]
        == endpoint_sources["row_descriptor"]["sha256"],
        "row descriptor source hash mismatch",
    )


def build_records(
    affine_records: dict[tuple[int, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    records = []
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        for rank in RANKS:
            affine_record = affine_records[(rank, agreement)]
            finite_roots = affine_record["v10_canonical_affine_rank_drop_root_count"]
            paid_endpoint = 1
            unpaid_total = finite_roots + (1 - paid_endpoint)
            require(unpaid_total == 0, "unpaid residual is nonzero")
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": N - agreement,
                    "t": agreement - K,
                    "projective_sampler": "projective_line",
                    "finite_affine_rank_drop": {
                        "v10_canonical_root_count": finite_roots,
                        "two_minor_common_gcd_degree": affine_record[
                            "two_minor_common_gcd_degree"
                        ],
                        "prefix_minor_hash": affine_record["prefix_minor_hash"],
                        "shifted_minor_hash": affine_record["shifted_minor_hash"],
                        "status": "empty",
                    },
                    "paid_ledgers": {
                        "quotient_image_projective_endpoint": {
                            "projective_point": "[0:1]",
                            "paid_numerator": paid_endpoint,
                            "witness_family": "c=2 quotient-remainder support",
                            "status": "paid_by_endpoint_quotient_image_certificate",
                        }
                    },
                    "regular_projective_residual_after_paid_ledgers": {
                        "finite_affine_unpaid": finite_roots,
                        "projective_endpoint_unpaid": 1 - paid_endpoint,
                        "total_unpaid": unpaid_total,
                        "status": "empty",
                    },
                }
            )
    require(len(records) == EXPECTED_RECORDS, "combined record count")
    return records


def build_agreement_table(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    table = []
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        rows = [record for record in records if record["A"] == agreement]
        finite_roots = sum(
            record["finite_affine_rank_drop"]["v10_canonical_root_count"]
            for record in rows
        )
        paid_endpoints = sum(
            record["paid_ledgers"]["quotient_image_projective_endpoint"][
                "paid_numerator"
            ]
            for record in rows
        )
        unpaid = sum(
            record["regular_projective_residual_after_paid_ledgers"]["total_unpaid"]
            for record in rows
        )
        require(len(rows) == len(RANKS), "agreement row count")
        require(finite_roots == 0, "agreement finite roots")
        require(paid_endpoints == len(RANKS), "agreement paid endpoints")
        require(unpaid == 0, "agreement unpaid residual")
        table.append(
            {
                "A": agreement,
                "j": N - agreement,
                "t": agreement - K,
                "synthetic_rank_rows": len(rows),
                "finite_affine_rank_drop_roots": finite_roots,
                "quotient_image_projective_endpoints_paid": paid_endpoints,
                "regular_projective_residual_after_paid_ledgers": unpaid,
                "all_synthetic_rows_clear": True,
            }
        )
    return table


def build_certificate() -> dict[str, Any]:
    affine = load_json(AFFINE_CERT_REF)
    endpoint = load_json(ENDPOINT_CERT_REF)
    affine_records = validate_affine_certificate(affine)
    validate_endpoint_certificate(endpoint, affine["row"]["domain_hash"])
    validate_source_consistency(affine, endpoint)

    records = build_records(affine_records)
    agreement_table = build_agreement_table(records)
    finite_sum = sum(
        record["finite_affine_rank_drop"]["v10_canonical_root_count"]
        for record in records
    )
    paid_endpoint_sum = sum(
        record["paid_ledgers"]["quotient_image_projective_endpoint"]["paid_numerator"]
        for record in records
    )
    unpaid_sum = sum(
        record["regular_projective_residual_after_paid_ledgers"]["total_unpaid"]
        for record in records
    )
    require(finite_sum == 0, "finite sum")
    require(paid_endpoint_sum == EXPECTED_RECORDS, "paid endpoint sum")
    require(unpaid_sum == 0, "unpaid sum")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": affine["row"],
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "ranks": RANKS,
        "sampler": "projective_line",
        "ledger_convention": {
            "finite_part": "v10 canonical affine rank-drop gcd roots",
            "projective_endpoint": "[0:1]",
            "paid_root_removal": (
                "remove the projective endpoint only when it is certified in "
                "the quotient-image branch"
            ),
            "residual_object": (
                "regular projective rank-drop numerator after paid quotient-image "
                "endpoint removal"
            ),
        },
        "source_artifacts": [
            source_record("affine_gcd_certificate", AFFINE_CERT_REF, affine),
            source_record("endpoint_quotient_image_certificate", ENDPOINT_CERT_REF, endpoint),
        ],
        "removed_ledgers": [
            {
                "name": "quotient_image_projective_endpoint",
                "numerator_per_synthetic_row": 1,
                "total_numerator": paid_endpoint_sum,
                "certificate_ref": ENDPOINT_CERT_REF,
            }
        ],
        "agreement_table": agreement_table,
        "deterministic_records": {
            "storage": "compressed; verifier rebuilds per-rank paid residual rows",
            "record_count": len(records),
            "record_sha256": object_sha256({"records": records}),
            "first_record": records[0],
            "last_record": records[-1],
        },
        "aggregate": {
            "record_count": len(records),
            "agreement_count": AGREEMENT_MAX - AGREEMENT_MIN + 1,
            "rank_count": len(RANKS),
            "finite_affine_rank_drop_root_count_sum": finite_sum,
            "quotient_image_projective_endpoint_paid_count": paid_endpoint_sum,
            "regular_projective_unpaid_residual_count_sum": unpaid_sum,
            "all_synthetic_projective_rows_empty_after_paid_endpoint": True,
            "maximum_vandermonde_union_bound_for_endpoint_witness": endpoint[
                "aggregate"
            ]["maximum_vandermonde_union_bound"],
        },
        "claim": (
            "For the synthetic low-rank M3 ladder of ranks 2..12 over the "
            "accepted F_17^32 row and every A=385..426, the regular projective "
            "rank-drop residual is empty after paid quotient-image endpoint "
            "removal: the finite affine rank-drop root set is empty and the "
            "single projective endpoint [0:1] is quotient-image paid."
        ),
        "nonclaims": [
            "synthetic low-rank ladder only, not arbitrary M3 row data",
            "consumes the affine and endpoint certificates rather than recomputing their proofs",
            "not an actual-row safe-side threshold certificate",
            "not a singular-pivot classification",
            "does not classify quotient-image branches beyond the displayed endpoint",
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
        raise AssertionError(f"paid residual ledger mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank2..12 paid-residual ledger")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, finite_roots={finite}, paid_endpoints={paid}, unpaid_residual={unpaid}".format(
            records=aggregate["record_count"],
            finite=aggregate["finite_affine_rank_drop_root_count_sum"],
            paid=aggregate["quotient_image_projective_endpoint_paid_count"],
            unpaid=aggregate["regular_projective_unpaid_residual_count_sum"],
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
