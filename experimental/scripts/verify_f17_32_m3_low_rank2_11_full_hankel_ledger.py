#!/usr/bin/env python3
"""Verify the M3 low-rank rank-2..11 full-Hankel residual ledger.

This ledger packages the synthetic low-rank M3 ladder after the shifted-minor
and endpoint quotient-image audits.  It is not a new root computation.  It
combines:

* ranks 2..5: first/shifted minor coprimality clears finite first-minor roots
  and degree-bound root loci as full-Hankel witnesses;
* ranks 6..11: the exact slack root tables plus shifted-minor audit clear the
  finite first-minor roots, with the known-ledger v4 table as an aggregate
  cross-check;
* ranks 2..11: the projective endpoint is charged to quotient-image by the
  c=2 endpoint witness.

The result is a compact all-rank synthetic residual statement: regular-minor
projective upper max is 6, full-Hankel witness upper max is 1 before endpoint
quotient-image charging, and aperiodic full-Hankel residual max is 0 after
that charge.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-low-rank2-11-full-hankel-ledger-v1"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = list(range(2, 12))
BUDGET_NUMERATOR = 6

LOW_RANK2_5_SHIFTED_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-5-shifted-minor-exclusion/"
    "f17_32_n512_k256_m3_low_rank2_5_shifted_minor_exclusion.json"
)
LOW_RANK6_11_KNOWN_LEDGER_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-known-ledger-table/"
    "f17_32_n512_k256_m3_low_rank6_11_known_ledger_table.json"
)
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
LOW_RANK9_11_SLACK_SWEEP_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/"
    "f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json"
)
LOW_RANK6_11_SHIFTED_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-shifted-minor-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_shifted_minor_exclusion.json"
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
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-11-full-hankel-ledger/"
    "f17_32_n512_k256_m3_low_rank2_11_full_hankel_ledger.json"
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


def source_record(name: str, ref: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "ref": ref,
        "schema_version": data["schema_version"],
        "sha256": file_sha256(ref),
        "status": data["status"],
    }


def validate_single_rank_slack_source(
    source: dict[str, Any],
    rank: int,
    expected_schema: str,
    expected_root_sum: int,
    expected_max_projective: int,
) -> None:
    require(source["schema_version"] == expected_schema, f"rank-{rank} schema")
    require(
        source["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX]
        and source["row"]["n"] == N
        and source["row"]["k"] == K
        and source["aggregate"]["agreement_count"] == 42
        and source["aggregate"]["exact_regular_root_count_sum"]
        == expected_root_sum
        and source["aggregate"]["max_projective_regular_roots_per_agreement"]
        == expected_max_projective
        and source["aggregate"]["all_rows_within_projective_budget"] is True,
        f"rank-{rank} aggregate",
    )
    agreements = {record["A"] for record in source["records"]}
    require(
        agreements == set(range(AGREEMENT_MIN, AGREEMENT_MAX + 1)),
        f"rank-{rank} agreement set",
    )
    require(
        sum(record["root_count"] for record in source["records"])
        == expected_root_sum,
        f"rank-{rank} root sum",
    )


def validate_sources(sources: dict[str, dict[str, Any]]) -> None:
    require(
        sources["rank2_5_shifted"]["schema_version"]
        == "f17-32-m3-low-rank2-5-shifted-minor-exclusion-v1",
        "rank-2..5 shifted schema mismatch",
    )
    require(
        sources["rank2_5_shifted"]["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX]
        and sources["rank2_5_shifted"]["ranks"] == [2, 3, 4, 5]
        and sources["rank2_5_shifted"]["aggregate"]["record_count"] == 168
        and sources["rank2_5_shifted"]["aggregate"][
            "finite_root_upper_bound_from_source"
        ]
        == 460
        and sources["rank2_5_shifted"]["aggregate"][
            "cleared_finite_root_upper_bound"
        ]
        == 460
        and sources["rank2_5_shifted"]["aggregate"][
            "surviving_finite_root_upper_bound"
        ]
        == 0
        and sources["rank2_5_shifted"]["aggregate"][
            "all_first_minor_loci_excluded_as_support_witnesses"
        ]
        is True,
        "rank-2..5 shifted aggregate mismatch",
    )
    require(
        sources["rank6_11_known"]["schema_version"]
        == "f17-32-m3-low-rank6-11-known-ledger-table-v4",
        "rank-6..11 known-ledger schema mismatch",
    )
    require(
        sources["rank6_11_known"]["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX]
        and sources["rank6_11_known"]["ranks"] == [6, 7, 8, 9, 10, 11]
        and sources["rank6_11_known"]["aggregate"]["record_count"] == 252
        and sources["rank6_11_known"]["aggregate"][
            "finite_regular_root_count_sum"
        ]
        == 238
        and sources["rank6_11_known"]["aggregate"][
            "finite_regular_roots_excluded_by_shifted_minor_sum"
        ]
        == 238
        and sources["rank6_11_known"]["aggregate"][
            "max_known_residual_full_hankel_projective_per_record"
        ]
        == 1
        and sources["rank6_11_known"]["aggregate"][
            "max_known_residual_aperiodic_full_hankel_projective_per_record"
        ]
        == 0,
        "rank-6..11 known-ledger aggregate mismatch",
    )
    validate_single_rank_slack_source(
        sources["rank6_slack"],
        6,
        "f17-32-m3-low-rank6-slack-family-v1",
        35,
        3,
    )
    validate_single_rank_slack_source(
        sources["rank7_slack"],
        7,
        "f17-32-m3-low-rank7-slack-family-v1",
        43,
        5,
    )
    validate_single_rank_slack_source(
        sources["rank8_slack"],
        8,
        "f17-32-m3-low-rank8-slack-family-v1",
        34,
        5,
    )
    require(
        sources["rank9_11_slack"]["schema_version"]
        == "f17-32-m3-low-rank9-11-slack-sweep-v1",
        "rank-9..11 slack-sweep schema mismatch",
    )
    require(
        sources["rank9_11_slack"]["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX]
        and sources["rank9_11_slack"]["aggregate"]["record_count"] == 126
        and sources["rank9_11_slack"]["aggregate"][
            "all_rows_within_projective_budget"
        ]
        is True
        and sources["rank9_11_slack"]["aggregate"][
            "max_projective_regular_roots_over_sweep"
        ]
        == 4,
        "rank-9..11 slack-sweep aggregate mismatch",
    )
    require(
        {
            rank: sources["rank9_11_slack"]["aggregate"]["rank_summaries"][
                str(rank)
            ]["exact_regular_root_count_sum"]
            for rank in (9, 10, 11)
        }
        == {9: 35, 10: 47, 11: 44},
        "rank-9..11 root sums mismatch",
    )
    require(
        sources["rank6_11_shifted"]["schema_version"]
        == "f17-32-m3-low-rank6-11-shifted-minor-exclusion-v1",
        "rank-6..11 shifted schema mismatch",
    )
    require(
        sources["rank6_11_shifted"]["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX]
        and sources["rank6_11_shifted"]["ranks"] == [6, 7, 8, 9, 10, 11]
        and sources["rank6_11_shifted"]["aggregate"]["source_record_count"]
        == 252
        and sources["rank6_11_shifted"]["aggregate"]["finite_root_total"]
        == 238
        and sources["rank6_11_shifted"]["aggregate"]["cleared_root_total"]
        == 238
        and sources["rank6_11_shifted"]["aggregate"]["surviving_root_total"]
        == 0
        and sources["rank6_11_shifted"]["aggregate"][
            "all_finite_roots_excluded_as_support_witnesses"
        ]
        is True,
        "rank-6..11 shifted aggregate mismatch",
    )
    require(
        sources["projective_infinity"]["schema_version"]
        == "f17-32-m3-low-rank2-11-projective-infinity-v1",
        "projective-infinity schema mismatch",
    )
    require(
        sources["projective_infinity"]["aggregate"]["record_count"] == 420
        and sources["projective_infinity"]["aggregate"][
            "projective_infinity_contribution_sum"
        ]
        == 420
        and sources["projective_infinity"]["aggregate"][
            "all_endpoint_noncontainment_checks_pass"
        ]
        is True,
        "projective-infinity aggregate mismatch",
    )
    require(
        sources["endpoint_support"]["schema_version"]
        == "f17-32-m3-low-rank2-11-endpoint-quotient-support-v1",
        "endpoint quotient-support schema mismatch",
    )
    require(
        sources["endpoint_support"]["aggregate"]["record_count"] == 420
        and sources["endpoint_support"]["aggregate"][
            "all_nontrivial_quotient_supports_excluded"
        ]
        is True,
        "endpoint quotient-support aggregate mismatch",
    )
    require(
        sources["endpoint_image"]["schema_version"]
        == "f17-32-m3-low-rank2-11-endpoint-quotient-image-v1",
        "endpoint quotient-image schema mismatch",
    )
    require(
        sources["endpoint_image"]["aggregate"]["record_count"] == 420
        and sources["endpoint_image"]["aggregate"][
            "endpoint_quotient_image_witness_count"
        ]
        == 420
        and sources["endpoint_image"]["aggregate"][
            "all_projective_endpoints_have_quotient_image_witness"
        ]
        is True,
        "endpoint quotient-image aggregate mismatch",
    )


def shifted_2_5_records(source: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    out = {}
    for record in source["records"]:
        key = (record["rank"], record["A"])
        require(key not in out, f"duplicate rank-2..5 shifted record {key}")
        out[key] = record
    require(len(out) == 168, "rank-2..5 shifted record count")
    return out


def rank6_11_finite_root_records(
    sources: dict[str, dict[str, Any]],
) -> dict[tuple[int, int], dict[str, Any]]:
    out = {}
    for rank, source_name in (
        (6, "rank6_slack"),
        (7, "rank7_slack"),
        (8, "rank8_slack"),
    ):
        for record in sources[source_name]["records"]:
            key = (rank, record["A"])
            require(key not in out, f"duplicate rank-6..11 source record {key}")
            out[key] = {
                "rank": rank,
                "A": record["A"],
                "root_count": record["root_count"],
                "root_status": record["root_status"],
            }
    for record in sources["rank9_11_slack"]["records"]:
        rank = record["rank"]
        require(rank in (9, 10, 11), f"unexpected slack-sweep rank {rank}")
        key = (rank, record["A"])
        require(key not in out, f"duplicate rank-6..11 source record {key}")
        out[key] = {
            "rank": rank,
            "A": record["A"],
            "root_count": record["root_count"],
            "root_status": record["root_status"],
        }

    shifted = {
        (record["rank"], record["A"]): record
        for record in sources["rank6_11_shifted"]["records"]
    }
    require(len(out) == 252, "rank-6..11 source record count")
    require(
        {key for key, record in out.items() if record["root_count"] > 0}
        == set(shifted),
        "rank-6..11 shifted support set",
    )
    for key, record in out.items():
        root_count = record["root_count"]
        shifted_record = shifted.get(key)
        if root_count == 0:
            require(shifted_record is None, f"{key}: zero-root shifted row")
            continue
        require(shifted_record is not None, f"{key}: missing shifted row")
        require(
            shifted_record["root_count"] == root_count
            and shifted_record["cleared_root_count"] == root_count
            and shifted_record.get(
                "common_gcd_degree",
                shifted_record.get("first_shifted_minor_gcd_degree"),
            )
            == 0,
            f"{key}: shifted root clearing mismatch",
        )
    require(
        sum(record["root_count"] for record in out.values()) == 238,
        "rank-6..11 source root total",
    )
    return out


def build_records(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rank2_5 = shifted_2_5_records(sources["rank2_5_shifted"])
    rank6_11 = rank6_11_finite_root_records(sources)
    records = []
    for rank in RANKS:
        for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
            key = (rank, agreement)
            if rank <= 5:
                source = rank2_5[key]
                finite_regular_upper = source["finite_root_upper_bound_from_source"]
                finite_full_hankel_upper = source[
                    "finite_full_hankel_witness_upper"
                ]
                regular_projective_upper = finite_regular_upper + 1
                full_hankel_projective_upper = finite_full_hankel_upper + 1
                aperiodic_full_hankel_upper = 0
                source_kind = source["source_kind"]
            else:
                source = rank6_11[key]
                finite_regular_upper = source["root_count"]
                finite_full_hankel_upper = 0
                regular_projective_upper = finite_regular_upper + 1
                full_hankel_projective_upper = 1
                aperiodic_full_hankel_upper = 0
                source_kind = "exact_finite_roots"
            require(finite_full_hankel_upper == 0, f"{key}: finite witness upper")
            require(full_hankel_projective_upper == 1, f"{key}: full-Hankel upper")
            require(aperiodic_full_hankel_upper == 0, f"{key}: aperiodic upper")
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": N - agreement,
                    "t": agreement - K,
                    "source_kind": source_kind,
                    "finite_regular_root_upper": finite_regular_upper,
                    "projective_endpoint_contribution": 1,
                    "regular_projective_upper": regular_projective_upper,
                    "finite_full_hankel_witness_upper": finite_full_hankel_upper,
                    "full_hankel_projective_upper_before_endpoint_image": (
                        full_hankel_projective_upper
                    ),
                    "endpoint_quotient_image_witness": 1,
                    "aperiodic_full_hankel_projective_upper": (
                        aperiodic_full_hankel_upper
                    ),
                    "within_regular_projective_budget": (
                        regular_projective_upper <= BUDGET_NUMERATOR
                    ),
                    "within_full_hankel_projective_budget": (
                        full_hankel_projective_upper <= BUDGET_NUMERATOR
                    ),
                    "within_aperiodic_full_hankel_budget": (
                        aperiodic_full_hankel_upper <= BUDGET_NUMERATOR
                    ),
                }
            )
    require(len(records) == 420, "combined record count")
    return records


def summarize(records: list[dict[str, Any]]) -> dict[str, Any]:
    rank_summaries = {}
    for rank in RANKS:
        rank_records = [record for record in records if record["rank"] == rank]
        regular_counts = [
            record["regular_projective_upper"] for record in rank_records
        ]
        full_counts = [
            record["full_hankel_projective_upper_before_endpoint_image"]
            for record in rank_records
        ]
        aperiodic_counts = [
            record["aperiodic_full_hankel_projective_upper"]
            for record in rank_records
        ]
        finite_counts = [
            record["finite_regular_root_upper"] for record in rank_records
        ]
        rank_summaries[str(rank)] = {
            "rank": rank,
            "agreement_count": len(rank_records),
            "source_kind_histogram": {
                key: value
                for key, value in sorted(
                    Counter(record["source_kind"] for record in rank_records).items()
                )
            },
            "finite_regular_root_upper_sum": sum(finite_counts),
            "finite_regular_root_upper_histogram": {
                str(key): value for key, value in sorted(Counter(finite_counts).items())
            },
            "finite_full_hankel_witness_upper_sum": 0,
            "projective_endpoint_contribution_sum": len(rank_records),
            "endpoint_quotient_image_witness_sum": len(rank_records),
            "max_regular_projective_upper": max(regular_counts),
            "max_full_hankel_projective_upper_before_endpoint_image": max(
                full_counts
            ),
            "max_aperiodic_full_hankel_projective_upper": max(aperiodic_counts),
            "all_records_within_regular_projective_budget": all(
                record["within_regular_projective_budget"] for record in rank_records
            ),
            "all_records_within_full_hankel_projective_budget": all(
                record["within_full_hankel_projective_budget"]
                for record in rank_records
            ),
            "all_records_within_aperiodic_full_hankel_budget": all(
                record["within_aperiodic_full_hankel_budget"]
                for record in rank_records
            ),
        }
    regular_counts = [record["regular_projective_upper"] for record in records]
    full_counts = [
        record["full_hankel_projective_upper_before_endpoint_image"]
        for record in records
    ]
    aperiodic_counts = [
        record["aperiodic_full_hankel_projective_upper"] for record in records
    ]
    return {
        "record_count": len(records),
        "rank_count": len(RANKS),
        "agreement_count_per_rank": AGREEMENT_MAX - AGREEMENT_MIN + 1,
        "finite_regular_root_upper_sum": sum(
            record["finite_regular_root_upper"] for record in records
        ),
        "finite_regular_roots_or_loci_excluded_by_shifted_minor_sum": sum(
            record["finite_regular_root_upper"] for record in records
        ),
        "finite_full_hankel_witness_upper_sum": 0,
        "projective_infinity_contribution_sum": len(records),
        "projective_endpoint_quotient_image_witness_sum": len(records),
        "regular_projective_upper_sum": sum(regular_counts),
        "max_regular_projective_upper_per_record": max(regular_counts),
        "full_hankel_projective_upper_before_endpoint_image_sum": sum(full_counts),
        "max_full_hankel_projective_upper_before_endpoint_image_per_record": max(
            full_counts
        ),
        "aperiodic_full_hankel_projective_upper_sum": sum(aperiodic_counts),
        "max_aperiodic_full_hankel_projective_upper_per_record": max(
            aperiodic_counts
        ),
        "projective_budget_numerator": BUDGET_NUMERATOR,
        "all_records_within_regular_projective_budget": all(
            record["within_regular_projective_budget"] for record in records
        ),
        "all_records_within_full_hankel_projective_budget": all(
            record["within_full_hankel_projective_budget"] for record in records
        ),
        "all_records_within_aperiodic_full_hankel_budget": all(
            record["within_aperiodic_full_hankel_budget"] for record in records
        ),
        "rank_summaries": rank_summaries,
    }


def build_certificate() -> dict[str, Any]:
    sources = {
        "rank2_5_shifted": load_json(LOW_RANK2_5_SHIFTED_REF),
        "rank6_11_known": load_json(LOW_RANK6_11_KNOWN_LEDGER_REF),
        "rank6_slack": load_json(LOW_RANK6_SLACK_REF),
        "rank7_slack": load_json(LOW_RANK7_SLACK_REF),
        "rank8_slack": load_json(LOW_RANK8_SLACK_REF),
        "rank9_11_slack": load_json(LOW_RANK9_11_SLACK_SWEEP_REF),
        "rank6_11_shifted": load_json(LOW_RANK6_11_SHIFTED_REF),
        "projective_infinity": load_json(PROJECTIVE_INFINITY_REF),
        "endpoint_support": load_json(ENDPOINT_QUOTIENT_SUPPORT_REF),
        "endpoint_image": load_json(ENDPOINT_QUOTIENT_IMAGE_REF),
    }
    validate_sources(sources)
    records = build_records(sources)
    aggregate = summarize(records)
    require(aggregate["record_count"] == 420, "aggregate record count")
    require(
        aggregate["finite_regular_root_upper_sum"] == 698,
        "finite regular upper sum",
    )
    require(
        aggregate["max_regular_projective_upper_per_record"] == 6,
        "regular projective max",
    )
    require(
        aggregate["max_full_hankel_projective_upper_before_endpoint_image_per_record"]
        == 1,
        "full-Hankel max",
    )
    require(
        aggregate["max_aperiodic_full_hankel_projective_upper_per_record"] == 0,
        "aperiodic full-Hankel max",
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": sources["rank6_11_known"]["row"]["field"],
            "domain_hash": sources["rank6_11_known"]["row"]["domain_hash"],
        },
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "ranks": RANKS,
        "source_artifacts": [
            source_record("rank2_5_shifted", LOW_RANK2_5_SHIFTED_REF, sources["rank2_5_shifted"]),
            source_record("rank6_11_known", LOW_RANK6_11_KNOWN_LEDGER_REF, sources["rank6_11_known"]),
            source_record("rank6_slack", LOW_RANK6_SLACK_REF, sources["rank6_slack"]),
            source_record("rank7_slack", LOW_RANK7_SLACK_REF, sources["rank7_slack"]),
            source_record("rank8_slack", LOW_RANK8_SLACK_REF, sources["rank8_slack"]),
            source_record("rank9_11_slack", LOW_RANK9_11_SLACK_SWEEP_REF, sources["rank9_11_slack"]),
            source_record("rank6_11_shifted", LOW_RANK6_11_SHIFTED_REF, sources["rank6_11_shifted"]),
            source_record("projective_infinity", PROJECTIVE_INFINITY_REF, sources["projective_infinity"]),
            source_record("endpoint_quotient_support", ENDPOINT_QUOTIENT_SUPPORT_REF, sources["endpoint_support"]),
            source_record("endpoint_quotient_image", ENDPOINT_QUOTIENT_IMAGE_REF, sources["endpoint_image"]),
        ],
        "method": {
            "finite_full_hankel_column": (
                "shifted-minor exclusion removes every finite first-minor root "
                "or degree-bound root locus from the full-Hankel witness column"
            ),
            "endpoint_column": (
                "the projective endpoint contributes one full-Hankel witness "
                "before quotient-image charging"
            ),
            "aperiodic_column": (
                "the endpoint quotient-image certificate charges that endpoint, "
                "leaving zero aperiodic full-Hankel residual"
            ),
        },
        "aggregate": aggregate,
        "deterministic_records": {
            "storage": "compressed; verifier rebuilds all 420 rank/agreement rows",
            "record_count": len(records),
            "record_sha256": object_sha256({"records": records}),
            "first_record": records[0],
            "last_record": records[-1],
        },
        "claim": (
            "For the synthetic rank-2..11 low-rank M3 ladder, finite "
            "first-minor roots/loci contribute zero full-Hankel witness mass "
            "after shifted-minor exclusion, and the remaining projective "
            "endpoint is charged to quotient-image.  The aperiodic full-Hankel "
            "projective residual upper bound is therefore zero in every "
            "checked rank/agreement row."
        ),
        "nonclaims": [
            "synthetic low-rank ladder only, not arbitrary M3 rows",
            "ranks 4 and 5 use degree-bound root loci rather than enumerated root tables",
            "finite-root quotient image/support is not audited as a regular-minor ledger",
            "does not replace the singular/pivot chart program outside this ladder",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"rank-2..11 full-Hankel ledger mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 rank-2..11 full-Hankel low-rank ledger")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, finite_upper={finite}, full_max={full}, aperiodic_max={aper}".format(
            records=aggregate["record_count"],
            finite=aggregate["finite_regular_root_upper_sum"],
            full=aggregate[
                "max_full_hankel_projective_upper_before_endpoint_image_per_record"
            ],
            aper=aggregate[
                "max_aperiodic_full_hankel_projective_upper_per_record"
            ],
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
