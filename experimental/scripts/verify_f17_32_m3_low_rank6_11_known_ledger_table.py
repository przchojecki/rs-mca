#!/usr/bin/env python3
"""Verify the known-ledger residual table for M3 low-rank ranks 6..11.

This combines existing synthetic-family certificates:

* exact finite-root slack for ranks 6..11,
* the projective-infinity endpoint audit for ranks 2..11,
* common-code-line tangent exclusion for ranks 6..11,
* proper-subfield/confinement exclusion for ranks 6..11.

It deliberately leaves quotient-support and quotient-image subtraction as
``not_audited``.  The useful conclusion is narrower: after the known ledgers
above, every checked synthetic rank/agreement row still has projective
regular-root upper count at most five, hence below the F_17^32 budget numerator
six even before any quotient-image subtraction.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-low-rank6-11-known-ledger-table-v1"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = list(range(6, 12))
BUDGET_NUMERATOR = 6

LOW_RANK6_SLACK_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/"
    "f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json"
)
LOW_RANK7_SLACK_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank7-slack-family/"
    "f17_32_n512_k256_m3_low_rank7_slack_family_certificate.json"
)
LOW_RANK8_SLACK_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank8-slack-family/"
    "f17_32_n512_k256_m3_low_rank8_slack_family_certificate.json"
)
LOW_RANK9_11_SWEEP_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/"
    "f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json"
)
PROJECTIVE_INFINITY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/"
    "f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json"
)
TANGENT_EXCLUSION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json"
)
SUBFIELD_EXCLUSION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank6-11-known-ledger-table/"
    "f17_32_n512_k256_m3_low_rank6_11_known_ledger_table.json"
)


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def object_sha256(value: Any) -> str:
    return sha256(render(value).encode("utf-8")).hexdigest()


def load_json(ref: str) -> dict[str, Any]:
    return json.loads((REPO_ROOT / ref).read_text(encoding="utf-8"))


def file_sha256(ref: str) -> str:
    return sha256((REPO_ROOT / ref).read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_sources(sources: dict[str, dict[str, Any]]) -> None:
    expected_schemas = {
        "rank6": "f17-32-m3-low-rank6-slack-family-v1",
        "rank7": "f17-32-m3-low-rank7-slack-family-v1",
        "rank8": "f17-32-m3-low-rank8-slack-family-v1",
        "rank9_11": "f17-32-m3-low-rank9-11-slack-sweep-v1",
        "projective_infinity": "f17-32-m3-low-rank2-11-projective-infinity-v1",
        "tangent": "f17-32-m3-low-rank6-11-tangent-exclusion-v1",
        "subfield": "f17-32-m3-low-rank6-11-subfield-exclusion-v1",
    }
    for name, schema in expected_schemas.items():
        require(
            sources[name]["schema_version"] == schema,
            f"{name}: schema mismatch",
        )
    for name in ["rank6", "rank7", "rank8", "rank9_11", "tangent", "subfield"]:
        require(
            sources[name]["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
            f"{name}: agreement range mismatch",
        )
    require(
        sources["projective_infinity"]["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX],
        "projective infinity agreement range mismatch",
    )
    require(
        sources["tangent"]["aggregate"]["common_code_line_tangent_overlap_sum"]
        == 0,
        "tangent overlap is not zero",
    )
    require(
        sources["subfield"]["aggregate"]["proper_subfield_overlap_sum"] == 0,
        "proper-subfield overlap is not zero",
    )


def root_count_records(sources: dict[str, dict[str, Any]]) -> dict[tuple[int, int], int]:
    records: dict[tuple[int, int], int] = {}
    for rank, name in [(6, "rank6"), (7, "rank7"), (8, "rank8")]:
        for record in sources[name]["records"]:
            key = (rank, record["A"])
            require(key not in records, f"duplicate root-count record {key}")
            records[key] = record["root_count"]
    for record in sources["rank9_11"]["records"]:
        rank = record["rank"]
        require(rank in {9, 10, 11}, f"unexpected sweep rank {rank}")
        key = (rank, record["A"])
        require(key not in records, f"duplicate sweep record {key}")
        records[key] = record["root_count"]
    require(len(records) == len(RANKS) * 42, "root-count record total mismatch")
    return records


def audit_maps(
    sources: dict[str, dict[str, Any]],
) -> tuple[dict[tuple[int, int], dict[str, Any]], dict[tuple[int, int], dict[str, Any]]]:
    tangent = {
        (record["rank"], record["A"]): record
        for record in sources["tangent"]["records"]
    }
    subfield = {
        (record["rank"], record["A"]): record
        for record in sources["subfield"]["records"]
    }
    require(len(tangent) == len(RANKS) * 42, "tangent record total mismatch")
    require(len(subfield) == len(RANKS) * 42, "subfield record total mismatch")
    return tangent, subfield


def build_records(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    root_counts = root_count_records(sources)
    tangent, subfield = audit_maps(sources)
    endpoint_summaries = sources["projective_infinity"]["aggregate"][
        "rank_summaries"
    ]
    records = []
    for rank in RANKS:
        endpoint_summary = endpoint_summaries[str(rank)]
        require(
            endpoint_summary["endpoint_support_size"] == N - rank,
            f"rank {rank}: endpoint support mismatch",
        )
        for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
            key = (rank, agreement)
            finite_roots = root_counts[key]
            tangent_record = tangent[key]
            subfield_record = subfield[key]
            require(
                tangent_record["root_count_from_source"] == finite_roots,
                f"{key}: tangent root count mismatch",
            )
            require(
                tangent_record["tangent_common_code_line_audit"][
                    "overlap_count"
                ]
                == 0,
                f"{key}: tangent overlap mismatch",
            )
            require(
                subfield_record["root_count_from_source"] == finite_roots,
                f"{key}: subfield root count mismatch",
            )
            require(
                subfield_record["subfield_confinement_audit"][
                    "proper_subfield_overlap_count"
                ]
                == 0,
                f"{key}: proper-subfield overlap mismatch",
            )
            residual = finite_roots + 1
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": N - agreement,
                    "t": agreement - K,
                    "finite_regular_root_count": finite_roots,
                    "projective_infinity_contribution": 1,
                    "known_tangent_overlap_removed": 0,
                    "known_proper_subfield_overlap_removed": 0,
                    "known_residual_projective_upper": residual,
                    "projective_budget_numerator": BUDGET_NUMERATOR,
                    "within_projective_budget_after_known_ledgers": (
                        residual <= BUDGET_NUMERATOR
                    ),
                    "quotient_support_status": "not_audited",
                    "quotient_image_status": "not_audited",
                    "known_lower_bound_status": "not_supplied",
                }
            )
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    rank_summaries = {}
    for rank in RANKS:
        rank_records = [record for record in records if record["rank"] == rank]
        finite_counts = [
            record["finite_regular_root_count"] for record in rank_records
        ]
        residual_counts = [
            record["known_residual_projective_upper"] for record in rank_records
        ]
        rank_summaries[str(rank)] = {
            "rank": rank,
            "agreement_count": len(rank_records),
            "finite_root_count_sum": sum(finite_counts),
            "finite_root_histogram": {
                str(key): value for key, value in sorted(Counter(finite_counts).items())
            },
            "projective_infinity_contribution_sum": len(rank_records),
            "known_residual_projective_sum": sum(residual_counts),
            "max_known_residual_projective_per_record": max(residual_counts),
            "worst_agreements": [
                record["A"]
                for record in rank_records
                if record["known_residual_projective_upper"] == max(residual_counts)
            ],
            "all_records_within_projective_budget_after_known_ledgers": all(
                record["within_projective_budget_after_known_ledgers"]
                for record in rank_records
            ),
        }
    residual_counts = [
        record["known_residual_projective_upper"] for record in records
    ]
    return {
        "record_count": len(records),
        "rank_count": len(RANKS),
        "agreement_count_per_rank": AGREEMENT_MAX - AGREEMENT_MIN + 1,
        "finite_regular_root_count_sum": sum(
            record["finite_regular_root_count"] for record in records
        ),
        "projective_infinity_contribution_sum": len(records),
        "known_tangent_overlap_removed_sum": 0,
        "known_proper_subfield_overlap_removed_sum": 0,
        "known_residual_projective_sum": sum(residual_counts),
        "max_known_residual_projective_per_record": max(residual_counts),
        "projective_budget_numerator": BUDGET_NUMERATOR,
        "all_records_within_projective_budget_after_known_ledgers": all(
            record["within_projective_budget_after_known_ledgers"]
            for record in records
        ),
        "quotient_support_status": "not_audited",
        "quotient_image_status": "not_audited",
        "rank_summaries": rank_summaries,
    }


def source_record(name: str, ref: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "ref": ref,
        "schema_version": data["schema_version"],
        "sha256": file_sha256(ref),
        "status": data["status"],
    }


def build_certificate() -> dict[str, Any]:
    refs = {
        "rank6": LOW_RANK6_SLACK_REF,
        "rank7": LOW_RANK7_SLACK_REF,
        "rank8": LOW_RANK8_SLACK_REF,
        "rank9_11": LOW_RANK9_11_SWEEP_REF,
        "projective_infinity": PROJECTIVE_INFINITY_REF,
        "tangent": TANGENT_EXCLUSION_REF,
        "subfield": SUBFIELD_EXCLUSION_REF,
    }
    sources = {name: load_json(ref) for name, ref in refs.items()}
    validate_sources(sources)
    records = build_records(sources)
    aggregate = summarize(records)
    require(aggregate["record_count"] == 252, "record total mismatch")
    require(
        aggregate["finite_regular_root_count_sum"] == 238,
        "finite root total mismatch",
    )
    require(
        aggregate["max_known_residual_projective_per_record"] == 5,
        "residual maximum mismatch",
    )
    require(
        aggregate["all_records_within_projective_budget_after_known_ledgers"],
        "known-ledger projective budget failure",
    )
    worst_records = [
        record
        for record in records
        if record["known_residual_projective_upper"]
        == aggregate["max_known_residual_projective_per_record"]
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": sources["rank6"]["row"]["field"],
            "domain_hash": sources["rank6"]["row"]["domain_hash"],
            "domain_description": sources["rank6"]["row"]["domain_description"],
        },
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "ranks": RANKS,
        "source_artifacts": {
            name: source_record(name, refs[name], sources[name])
            for name in refs
        },
        "ledger_columns": {
            "finite_regular_roots": "exact Frobenius-gcd counts from slack certificates",
            "projective_infinity": "proved nonempty endpoint contribution [0:1]",
            "tangent_common_code_line_overlap": "proved zero",
            "proper_subfield_overlap": "proved zero for F_17^d, d in {1,2,4,8,16}",
            "quotient_support": "not_audited",
            "quotient_image": "not_audited",
            "known_lower_bound": "not_supplied",
        },
        "aggregate": aggregate,
        "deterministic_records": {
            "storage": "compressed; verifier rebuilds all 252 rank/agreement rows",
            "record_count": len(records),
            "record_sha256": object_sha256({"records": records}),
            "first_record": records[0],
            "last_record": records[-1],
            "worst_records": worst_records,
        },
        "claim": (
            "For the synthetic low-rank ranks 6..11 block, known ledgers leave "
            "at most five projective regular-root parameters in every checked "
            "rank/agreement row, below budget numerator six.  Quotient-support "
            "and quotient-image subtraction are not audited here."
        ),
        "nonclaims": [
            "synthetic low-rank family only",
            "not a quotient-support or quotient-image subtraction table",
            "not an actual-row M3 threshold bound",
            "does not prove finite affine roots are actual bad slopes",
            "does not classify arbitrary singular buckets",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"known-ledger table mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 rank-6..11 low-rank known-ledger table")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, finite_roots={finite}, endpoint_sum={endpoint}".format(
            records=aggregate["record_count"],
            finite=aggregate["finite_regular_root_count_sum"],
            endpoint=aggregate["projective_infinity_contribution_sum"],
        )
    )
    print(
        "max residual projective upper={max_residual} <= budget={budget}".format(
            max_residual=aggregate["max_known_residual_projective_per_record"],
            budget=aggregate["projective_budget_numerator"],
        )
    )
    print(
        "quotient_support={support}, quotient_image={image}".format(
            support=aggregate["quotient_support_status"],
            image=aggregate["quotient_image_status"],
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
