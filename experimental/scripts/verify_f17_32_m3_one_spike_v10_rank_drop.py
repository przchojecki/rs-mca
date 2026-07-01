#!/usr/bin/env python3
"""Verify the v10 rank-drop gcd certificate for the M3 one-spike window."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.verify_f17_32_m3_low_rank6_11_shifted_minor_exclusion import (  # noqa: E402
    field_from_descriptor,
)
from experimental.scripts.verify_f17_32_m3_one_spike_window_full_hankel import (  # noqa: E402
    AGREEMENT_MAX,
    AGREEMENT_MIN,
    BUDGET_NUMERATOR,
    K,
    N,
    OUTPUT_PATH as FULL_HANKEL_OUTPUT_PATH,
    ROW_DESCRIPTOR_REF,
    build_records,
    hash_json,
    load_json,
)


SCHEMA_VERSION = "f17-32-m3-one-spike-v10-rank-drop-v1"
V10_PAPER_REF = "tex/cs25_cap_v10.tex"
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-one-spike-v10-rank-drop/"
    "f17_32_n512_k256_m3_one_spike_v10_rank_drop.json"
)


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def file_sha256(ref: str | Path) -> str:
    path = ref if isinstance(ref, Path) else REPO_ROOT / ref
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def source_record(
    name: str,
    ref: str | Path,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ref_text = str(ref)
    if isinstance(ref, Path):
        ref_text = str(ref.relative_to(REPO_ROOT))
    record = {
        "name": name,
        "ref": ref_text,
        "sha256": file_sha256(ref),
    }
    if data is not None:
        record["schema_version"] = data.get("schema_version")
        record["status"] = data.get("status")
    return record


def rank_drop_record(record: dict[str, Any]) -> dict[str, Any]:
    agreement = record["A"]
    j = record["j"]
    t = record["t"]
    minor_size = record["minor_size"]
    prefix_row_set = list(range(minor_size))
    shifted_row_set = list(range(1, minor_size + 1))
    require(minor_size == j + 1, f"A={agreement}: minor size mismatch")
    require(shifted_row_set[-1] < t, f"A={agreement}: shifted row set outside t")
    require(record["regular_minor_degree"] == 1, f"A={agreement}: prefix degree")
    require(record["common_gcd_degree"] == 0, f"A={agreement}: gcd is not constant")
    require(
        record["finite_regular_roots_excluded_by_shifted_minor"] == 1,
        f"A={agreement}: shifted minor does not exclude prefix root",
    )
    require(
        record["endpoint_quotient_image_witness"] == 1,
        f"A={agreement}: endpoint image witness missing",
    )

    return {
        "A": agreement,
        "j": j,
        "t": t,
        "minor_size": minor_size,
        "prefix_row_set": [prefix_row_set[0], prefix_row_set[-1]],
        "shifted_row_set": [shifted_row_set[0], shifted_row_set[-1]],
        "prefix_minor_coefficients_ascending": (
            record["regular_minor_coefficients_ascending"]
        ),
        "shifted_minor_coefficients_ascending": (
            record["shifted_minor_coefficients_ascending"]
        ),
        "prefix_first_minor_root": record["finite_root"],
        "shifted_minor_value_at_prefix_root": (
            record["shifted_minor_value_at_root"]
        ),
        "two_minor_common_gcd_degree": record["common_gcd_degree"],
        "v10_canonical_affine_rank_drop_gcd_degree": 0,
        "v10_canonical_affine_rank_drop_root_count": 0,
        "projective_endpoint": {
            "point": "[0:1]",
            "rank_drop_status": "nonempty",
            "reason": (
                "both displayed affine minors have degree 1, below the "
                "homogenizing degree j+1"
            ),
            "quotient_image_witness": 1,
        },
        "aperiodic_projective_residual_after_endpoint_image": 0,
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    full_hankel = load_json(FULL_HANKEL_OUTPUT_PATH)
    field = field_from_descriptor(descriptor)
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    records = build_records(domain, field)
    rank_drop_records = [rank_drop_record(record) for record in records]
    gcd_histogram = Counter(
        row["two_minor_common_gcd_degree"] for row in rank_drop_records
    )

    require(full_hankel["status"] == "PROVED / AUDIT", "full-Hankel status")
    require(full_hankel["aggregate"]["record_count"] == 42, "full-Hankel count")
    require(len(rank_drop_records) == 42, "record count")
    require(
        all(row["v10_canonical_affine_rank_drop_gcd_degree"] == 0 for row in rank_drop_records),
        "nonconstant canonical gcd",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the pinned F_17^32 row descriptor"
            ),
        },
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "construction": {
            "branch": "non_proportional_one_spike",
            "v10_object": "canonical affine rank-drop gcd for regular Hankel buckets",
            "displayed_maximal_minors": [
                "prefix rows 0..j",
                "row-shift-1 rows 1..j+1",
            ],
            "argument": (
                "The v10 affine rank-drop gcd divides the gcd of any two "
                "nonzero maximal minors.  In every row the prefix minor and "
                "row-shift-1 minor are coprime, so the canonical affine "
                "rank-drop gcd is 1 and has no finite roots."
            ),
        },
        "source_artifacts": [
            source_record("paper_d_v10", V10_PAPER_REF),
            source_record("row_descriptor", ROW_DESCRIPTOR_REF, descriptor),
            source_record(
                "one_spike_window_full_hankel",
                FULL_HANKEL_OUTPUT_PATH,
                full_hankel,
            ),
        ],
        "records": rank_drop_records,
        "aggregate": {
            "record_count": len(rank_drop_records),
            "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
            "two_minor_common_gcd_degree_histogram": {
                str(key): value for key, value in sorted(gcd_histogram.items())
            },
            "finite_prefix_roots_seen_before_v10_gcd": len(
                {record["prefix_first_minor_root"] for record in rank_drop_records}
            ),
            "v10_canonical_affine_rank_drop_root_count_sum": sum(
                row["v10_canonical_affine_rank_drop_root_count"]
                for row in rank_drop_records
            ),
            "projective_endpoint_rows": len(rank_drop_records),
            "projective_endpoint_quotient_image_witness_sum": sum(
                row["projective_endpoint"]["quotient_image_witness"]
                for row in rank_drop_records
            ),
            "max_aperiodic_projective_residual_after_endpoint_image": max(
                row["aperiodic_projective_residual_after_endpoint_image"]
                for row in rank_drop_records
            ),
            "projective_budget_numerator": BUDGET_NUMERATOR,
            "all_records_have_empty_affine_rank_drop_gcd": True,
            "all_projective_endpoints_charged_to_quotient_image": True,
        },
        "claim": (
            "For the synthetic non-proportional one-spike M3 branch over the "
            "pinned F_17^32 row and every A=385..426, the v10 canonical "
            "affine rank-drop gcd is constant because the prefix and "
            "row-shift-1 maximal minors are coprime.  Thus the affine "
            "rank-drop root set is empty.  The remaining projective endpoint "
            "is charged to quotient-image, leaving aperiodic projective "
            "residual zero for this branch."
        ),
        "nonclaims": [
            "synthetic one-spike branch only, not arbitrary M3 row data",
            "not an actual-row safe-side threshold certificate",
            "does not enumerate or classify arbitrary singular pivot charts",
        ],
        "deterministic_record_hash": hash_json(rank_drop_records),
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"one-spike v10 rank-drop certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 one-spike v10 rank-drop certificate")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, affine_roots={roots}, endpoint_rows={endpoints}, residual={residual}".format(
            records=aggregate["record_count"],
            roots=aggregate["v10_canonical_affine_rank_drop_root_count_sum"],
            endpoints=aggregate["projective_endpoint_rows"],
            residual=aggregate[
                "max_aperiodic_projective_residual_after_endpoint_image"
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
