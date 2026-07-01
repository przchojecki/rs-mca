#!/usr/bin/env python3
"""Verify the known-ledger residual table for M3 low-rank ranks 6..11.

This combines existing synthetic-family certificates:

* exact finite-root slack for ranks 6..11,
* the projective-infinity endpoint audit for ranks 2..11,
* the endpoint quotient-support exclusion for ranks 2..11,
* the endpoint quotient-image witness for ranks 2..11,
* common-code-line tangent exclusion for ranks 6..11,
* proper-subfield/confinement exclusion for ranks 6..11,
* shifted-minor exclusion for finite first-minor roots in ranks 6..11.

It keeps two distinct columns.  The regular-minor upper-bound column still has
projective count at most five, while the full-Hankel witness column removes all
finite first-minor roots by the shifted row-1 minor and leaves only the
projective endpoint.  The endpoint has an explicit c=2 quotient-image witness,
so the aperiodic full-Hankel residual column is zero.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-low-rank6-11-known-ledger-table-v4"
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
ENDPOINT_QUOTIENT_SUPPORT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-11-endpoint-quotient-support/"
    "f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_support.json"
)
ENDPOINT_QUOTIENT_IMAGE_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-11-endpoint-quotient-image/"
    "f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_image.json"
)
TANGENT_EXCLUSION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json"
)
SUBFIELD_EXCLUSION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json"
)
SHIFTED_MINOR_EXCLUSION_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank6-11-shifted-minor-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_shifted_minor_exclusion.json"
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
        "endpoint_quotient_support": (
            "f17-32-m3-low-rank2-11-endpoint-quotient-support-v1"
        ),
        "endpoint_quotient_image": (
            "f17-32-m3-low-rank2-11-endpoint-quotient-image-v1"
        ),
        "tangent": "f17-32-m3-low-rank6-11-tangent-exclusion-v1",
        "subfield": "f17-32-m3-low-rank6-11-subfield-exclusion-v1",
        "shifted_minor": "f17-32-m3-low-rank6-11-shifted-minor-exclusion-v1",
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
        sources["endpoint_quotient_support"]["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX],
        "endpoint quotient-support agreement range mismatch",
    )
    require(
        sources["endpoint_quotient_support"]["aggregate"][
            "all_nontrivial_quotient_supports_excluded"
        ]
        is True,
        "endpoint quotient-support audit not passed",
    )
    require(
        sources["endpoint_quotient_image"]["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX]
        and sources["endpoint_quotient_image"]["ranks"] == list(range(2, 12))
        and sources["endpoint_quotient_image"]["aggregate"]["fiber_size"] == 2
        and sources["endpoint_quotient_image"]["aggregate"][
            "endpoint_quotient_image_witness_count"
        ]
        == 420
        and sources["endpoint_quotient_image"]["aggregate"][
            "all_projective_endpoints_have_quotient_image_witness"
        ]
        is True,
        "endpoint quotient-image aggregate mismatch",
    )
    for rank in RANKS:
        summary = sources["endpoint_quotient_support"]["aggregate"][
            "rank_summaries"
        ][str(rank)]
        require(
            summary["all_nontrivial_quotient_supports_excluded"] is True
            and summary["endpoint_support_size"] == N - rank,
            f"rank={rank}: endpoint quotient-support summary mismatch",
        )
        image_summary = sources["endpoint_quotient_image"]["aggregate"][
            "rank_summaries"
        ][str(rank)]
        require(
            image_summary["endpoint_quotient_image_witness_count"] == 42
            and image_summary["all_witnesses_use_c2"] is True,
            f"rank={rank}: endpoint quotient-image summary mismatch",
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
    require(
        sources["shifted_minor"]["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX]
        and sources["shifted_minor"]["ranks"] == RANKS
        and sources["shifted_minor"]["row_shift_tested"] == 1,
        "shifted-minor source range/rank mismatch",
    )
    require(
        sources["shifted_minor"]["aggregate"]["root_bearing_record_count"] == 158
        and sources["shifted_minor"]["aggregate"]["finite_root_total"] == 238
        and sources["shifted_minor"]["aggregate"]["cleared_root_total"] == 238
        and sources["shifted_minor"]["aggregate"]["surviving_root_total"] == 0
        and sources["shifted_minor"]["aggregate"][
            "all_finite_roots_excluded_as_support_witnesses"
        ]
        is True,
        "shifted-minor aggregate mismatch",
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
) -> tuple[
    dict[tuple[int, int], dict[str, Any]],
    dict[tuple[int, int], dict[str, Any]],
    dict[tuple[int, int], dict[str, Any]],
]:
    tangent = {
        (record["rank"], record["A"]): record
        for record in sources["tangent"]["records"]
    }
    subfield = {
        (record["rank"], record["A"]): record
        for record in sources["subfield"]["records"]
    }
    shifted_minor = {
        (record["rank"], record["A"]): record
        for record in sources["shifted_minor"]["records"]
    }
    require(len(tangent) == len(RANKS) * 42, "tangent record total mismatch")
    require(len(subfield) == len(RANKS) * 42, "subfield record total mismatch")
    require(len(shifted_minor) == 158, "shifted-minor record total mismatch")
    return tangent, subfield, shifted_minor


def build_records(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    root_counts = root_count_records(sources)
    tangent, subfield, shifted_minor = audit_maps(sources)
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
            if finite_roots:
                shifted_record = shifted_minor[key]
                require(
                    shifted_record["root_count"] == finite_roots
                    and shifted_record["cleared_root_count"] == finite_roots,
                    f"{key}: shifted-minor cleared-root mismatch",
                )
                finite_full_hankel_witness_upper = 0
                finite_shifted_status = "excluded_by_row_shift_1_minor"
            else:
                require(
                    key not in shifted_minor,
                    f"{key}: unexpected shifted-minor zero-root record",
                )
                finite_full_hankel_witness_upper = 0
                finite_shifted_status = "no_finite_roots"
            regular_residual = finite_roots + 1
            full_hankel_residual = finite_full_hankel_witness_upper + 1
            aperiodic_full_hankel_residual = 0
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
                    "finite_regular_roots_excluded_by_shifted_minor": finite_roots,
                    "finite_regular_root_full_hankel_witness_upper": (
                        finite_full_hankel_witness_upper
                    ),
                    "finite_regular_root_full_hankel_witness_status": (
                        finite_shifted_status
                    ),
                    "projective_endpoint_quotient_image_status": (
                        "covered_by_c2_quotient_remainder_image"
                    ),
                    "projective_endpoint_quotient_image_certificate": (
                        ENDPOINT_QUOTIENT_IMAGE_REF
                    ),
                    "projective_endpoint_quotient_image_fiber_size": 2,
                    "projective_endpoint_quotient_support_status": (
                        "excluded_nontrivial_proper_quotient_remainder_support"
                    ),
                    "projective_endpoint_quotient_support_certificate": (
                        ENDPOINT_QUOTIENT_SUPPORT_REF
                    ),
                    "finite_regular_root_quotient_support_status": "not_audited",
                    "finite_regular_root_quotient_image_status": "not_audited",
                    "known_residual_projective_upper": regular_residual,
                    "known_residual_full_hankel_projective_upper": (
                        full_hankel_residual
                    ),
                    "known_residual_aperiodic_full_hankel_projective_upper": (
                        aperiodic_full_hankel_residual
                    ),
                    "projective_budget_numerator": BUDGET_NUMERATOR,
                    "within_projective_budget_after_known_ledgers": (
                        regular_residual <= BUDGET_NUMERATOR
                    ),
                    "within_projective_budget_after_shifted_minor": (
                        full_hankel_residual <= BUDGET_NUMERATOR
                    ),
                    "within_projective_budget_after_endpoint_quotient_image": (
                        aperiodic_full_hankel_residual <= BUDGET_NUMERATOR
                    ),
                    "quotient_support_status": (
                        "endpoint_excluded_finite_roots_not_audited"
                    ),
                    "quotient_image_status": "finite_roots_not_audited",
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
        full_hankel_counts = [
            record["known_residual_full_hankel_projective_upper"]
            for record in rank_records
        ]
        aperiodic_counts = [
            record["known_residual_aperiodic_full_hankel_projective_upper"]
            for record in rank_records
        ]
        rank_summaries[str(rank)] = {
            "rank": rank,
            "agreement_count": len(rank_records),
            "finite_root_count_sum": sum(finite_counts),
            "finite_roots_excluded_by_shifted_minor_sum": sum(finite_counts),
            "finite_full_hankel_witness_upper_sum": sum(
                record["finite_regular_root_full_hankel_witness_upper"]
                for record in rank_records
            ),
            "finite_root_histogram": {
                str(key): value for key, value in sorted(Counter(finite_counts).items())
            },
            "projective_infinity_contribution_sum": len(rank_records),
            "projective_endpoint_quotient_image_witness_sum": len(rank_records),
            "known_residual_projective_sum": sum(residual_counts),
            "max_known_residual_projective_per_record": max(residual_counts),
            "known_residual_full_hankel_projective_sum": sum(full_hankel_counts),
            "max_known_residual_full_hankel_projective_per_record": max(
                full_hankel_counts
            ),
            "known_residual_aperiodic_full_hankel_projective_sum": sum(
                aperiodic_counts
            ),
            "max_known_residual_aperiodic_full_hankel_projective_per_record": max(
                aperiodic_counts
            ),
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
    full_hankel_counts = [
        record["known_residual_full_hankel_projective_upper"]
        for record in records
    ]
    aperiodic_counts = [
        record["known_residual_aperiodic_full_hankel_projective_upper"]
        for record in records
    ]
    return {
        "record_count": len(records),
        "rank_count": len(RANKS),
        "agreement_count_per_rank": AGREEMENT_MAX - AGREEMENT_MIN + 1,
        "finite_regular_root_count_sum": sum(
            record["finite_regular_root_count"] for record in records
        ),
        "finite_regular_roots_excluded_by_shifted_minor_sum": sum(
            record["finite_regular_roots_excluded_by_shifted_minor"]
            for record in records
        ),
        "finite_regular_root_full_hankel_witness_upper_sum": sum(
            record["finite_regular_root_full_hankel_witness_upper"]
            for record in records
        ),
        "projective_infinity_contribution_sum": len(records),
        "projective_endpoint_quotient_image_witness_sum": len(records),
        "projective_endpoint_quotient_image_status": (
            "covered_by_c2_quotient_remainder_image"
        ),
        "known_tangent_overlap_removed_sum": 0,
        "known_proper_subfield_overlap_removed_sum": 0,
        "projective_endpoint_quotient_support_excluded_sum": len(records),
        "projective_endpoint_quotient_support_status": (
            "excluded_nontrivial_proper_quotient_remainder_supports"
        ),
        "finite_regular_root_quotient_support_status": "not_audited",
        "finite_regular_root_quotient_image_status": "not_audited",
        "known_residual_projective_sum": sum(residual_counts),
        "max_known_residual_projective_per_record": max(residual_counts),
        "known_residual_full_hankel_projective_sum": sum(full_hankel_counts),
        "max_known_residual_full_hankel_projective_per_record": max(
            full_hankel_counts
        ),
        "known_residual_aperiodic_full_hankel_projective_sum": sum(
            aperiodic_counts
        ),
        "max_known_residual_aperiodic_full_hankel_projective_per_record": max(
            aperiodic_counts
        ),
        "projective_budget_numerator": BUDGET_NUMERATOR,
        "all_records_within_projective_budget_after_known_ledgers": all(
            record["within_projective_budget_after_known_ledgers"]
            for record in records
        ),
        "all_records_within_projective_budget_after_shifted_minor": all(
            record["within_projective_budget_after_shifted_minor"]
            for record in records
        ),
        "all_records_within_projective_budget_after_endpoint_quotient_image": all(
            record["within_projective_budget_after_endpoint_quotient_image"]
            for record in records
        ),
        "quotient_support_status": "endpoint_excluded_finite_roots_not_audited",
        "quotient_image_status": "finite_roots_not_audited",
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
        "endpoint_quotient_support": ENDPOINT_QUOTIENT_SUPPORT_REF,
        "endpoint_quotient_image": ENDPOINT_QUOTIENT_IMAGE_REF,
        "tangent": TANGENT_EXCLUSION_REF,
        "subfield": SUBFIELD_EXCLUSION_REF,
        "shifted_minor": SHIFTED_MINOR_EXCLUSION_REF,
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
        aggregate["finite_regular_roots_excluded_by_shifted_minor_sum"] == 238
        and aggregate["finite_regular_root_full_hankel_witness_upper_sum"] == 0,
        "shifted-minor finite-root removal mismatch",
    )
    require(
        aggregate["max_known_residual_full_hankel_projective_per_record"] == 1,
        "full-Hankel residual maximum mismatch",
    )
    require(
        aggregate["projective_endpoint_quotient_image_witness_sum"] == 252
        and aggregate[
            "max_known_residual_aperiodic_full_hankel_projective_per_record"
        ]
        == 0,
        "endpoint quotient-image residual mismatch",
    )
    require(
        aggregate["all_records_within_projective_budget_after_known_ledgers"],
        "known-ledger projective budget failure",
    )
    require(
        aggregate["all_records_within_projective_budget_after_shifted_minor"],
        "shifted-minor projective budget failure",
    )
    require(
        aggregate["all_records_within_projective_budget_after_endpoint_quotient_image"],
        "endpoint quotient-image projective budget failure",
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
            "projective_endpoint_quotient_support": (
                "proved not a nontrivial proper quotient-remainder support"
            ),
            "projective_endpoint_quotient_image": (
                "proved the endpoint parameter has a c=2 quotient-remainder witness"
            ),
            "tangent_common_code_line_overlap": "proved zero",
            "proper_subfield_overlap": "proved zero for F_17^d, d in {1,2,4,8,16}",
            "shifted_minor_finite_roots": (
                "proved all finite first-minor roots are not full-Hankel witnesses"
            ),
            "finite_regular_root_quotient_support": "not_audited",
            "finite_regular_root_quotient_image": "not_audited",
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
            "at most five projective regular-minor upper-bound parameters in "
            "every checked rank/agreement row, below budget numerator six.  "
            "The shifted-minor ledger further proves all finite first-minor "
            "roots are not full-Hankel exact-support witnesses, leaving at "
            "most the projective endpoint in the full-Hankel witness column.  "
            "The endpoint quotient-image ledger charges that endpoint to an "
            "explicit c=2 quotient-remainder witness support, leaving zero "
            "aperiodic full-Hankel projective residual in every row.  The "
            "minimal endpoint support D minus Y is excluded from all "
            "nontrivial proper quotient-remainder support families."
        ),
        "nonclaims": [
            "synthetic low-rank family only",
            "not a finite-root quotient-support or quotient-image subtraction table",
            "not an actual-row M3 threshold bound",
            "finite affine first-minor roots are proved not to be full-Hankel witnesses, but arbitrary M3 rows are not covered",
            "does not claim the minimal endpoint support D minus Y is quotient-remainder",
            "does not classify arbitrary singular buckets",
            "trivial quotient fiber sizes c=1 and c=512 are not excluded",
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
        "max regular-minor residual upper={max_residual} <= budget={budget}".format(
            max_residual=aggregate["max_known_residual_projective_per_record"],
            budget=aggregate["projective_budget_numerator"],
        )
    )
    print(
        "max full-Hankel witness residual upper={max_residual} <= budget={budget}".format(
            max_residual=aggregate[
                "max_known_residual_full_hankel_projective_per_record"
            ],
            budget=aggregate["projective_budget_numerator"],
        )
    )
    print(
        "max aperiodic full-Hankel residual upper={max_residual} <= budget={budget}".format(
            max_residual=aggregate[
                "max_known_residual_aperiodic_full_hankel_projective_per_record"
            ],
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
