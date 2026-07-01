#!/usr/bin/env python3
"""Verify shifted-minor exclusion for M3 low-rank ranks 2..5.

Ranks 2 and 3 already have exact finite-root counts, while ranks 4 and 5 use
degree bounds because those bounds are projectively safe.  This verifier proves
the stronger full-Hankel statement for all four ranks: the selected first
regular square minor is coprime to the row-shift-1 square minor in every
rank/agreement row.  Hence every finite first-minor root, enumerated or only
degree-bounded, is excluded as an actual full-Hankel exact-support witness.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.extract_regular_hankel_minors import (  # noqa: E402
    PolynomialBasisField,
    fpoly_degree,
    fpoly_gcd,
    hash_json,
    render,
)
from experimental.scripts.verify_f17_32_m3_low_rank6_11_shifted_minor_exclusion import (  # noqa: E402
    build_kernel,
    coefficients_from_kernel,
    field_from_descriptor,
)
from experimental.scripts.verify_f17_32_m3_low_rank9_11_slack_sweep import (  # noqa: E402
    update_basis_values,
)


SCHEMA_VERSION = "f17-32-m3-low-rank2-5-shifted-minor-exclusion-v1"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = [2, 3, 4, 5]
SHIFT = 1
EXPECTED_RECORDS = len(RANKS) * (AGREEMENT_MAX - AGREEMENT_MIN + 1)
EXPECTED_EXACT_ROOT_TOTAL = 82
EXPECTED_DEGREE_BOUND_LOCUS_TOTAL = 378
EXPECTED_FINITE_ROOT_UPPER_TOTAL = (
    EXPECTED_EXACT_ROOT_TOTAL + EXPECTED_DEGREE_BOUND_LOCUS_TOTAL
)

ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_RANK_SOURCE_REFS = {
    2: (
        "experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/"
        "f17_32_n512_k256_m3_low_rank2_family_certificate.json",
        "f17-32-m3-low-rank2-family-v5",
    ),
    3: (
        "experimental/data/certificates/hankel-f17-32-m3-low-rank3-family/"
        "f17_32_n512_k256_m3_low_rank3_family_certificate.json",
        "f17-32-m3-low-rank3-family-v2",
    ),
    4: (
        "experimental/data/certificates/hankel-f17-32-m3-low-rank4-budget-family/"
        "f17_32_n512_k256_m3_low_rank4_budget_family_certificate.json",
        "f17-32-m3-low-rank4-budget-family-v1",
    ),
    5: (
        "experimental/data/certificates/hankel-f17-32-m3-low-rank5-budget-family/"
        "f17_32_n512_k256_m3_low_rank5_budget_family_certificate.json",
        "f17-32-m3-low-rank5-budget-family-v1",
    ),
}
SHIFTED_MINOR_CRITERION_REF = (
    "experimental/notes/m1/hankel_shifted_minor_exclusion_criterion.md"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-5-shifted-minor-exclusion/"
    "f17_32_n512_k256_m3_low_rank2_5_shifted_minor_exclusion.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = REPO_ROOT / ref if isinstance(ref, str) else ref
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(ref: str) -> str:
    return sha256((REPO_ROOT / ref).read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_source_records() -> tuple[dict[tuple[int, int], dict[str, Any]], dict[str, Any]]:
    source_records: dict[tuple[int, int], dict[str, Any]] = {}
    source_artifacts: dict[str, Any] = {
        "row_descriptor": {
            "ref": ROW_DESCRIPTOR_REF,
            "schema_version": "f17-32-hankel-row-descriptor-v1",
            "sha256": file_sha256(ROW_DESCRIPTOR_REF),
        },
        "shifted_minor_exclusion_criterion": {
            "ref": SHIFTED_MINOR_CRITERION_REF,
            "status": "PROVED / AUDIT",
            "sha256": file_sha256(SHIFTED_MINOR_CRITERION_REF),
        },
        "low_rank_source_certificates": [],
    }
    for rank, (ref, schema_version) in LOW_RANK_SOURCE_REFS.items():
        certificate = load_json(ref)
        require(certificate["schema_version"] == schema_version, f"rank {rank}: schema")
        require(certificate["status"] == "PROVED / AUDIT", f"rank {rank}: status")
        require(
            certificate["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
            f"rank {rank}: agreement range",
        )
        source_artifacts["low_rank_source_certificates"].append(
            {
                "rank": rank,
                "ref": ref,
                "schema_version": schema_version,
                "sha256": file_sha256(ref),
            }
        )
        for record in certificate["records"]:
            key = (rank, record["A"])
            require(key not in source_records, f"duplicate source record {key}")
            source_records[key] = record
    require(len(source_records) == EXPECTED_RECORDS, "source record count")
    return source_records, source_artifacts


def validate_source_record(
    field: PolynomialBasisField,
    record: dict[str, Any],
    rank: int,
    agreement: int,
    size: int,
    domain: list[tuple[int, ...]],
) -> None:
    require(record["A"] == agreement, f"rank-{rank} A={agreement}: A")
    require(record["j"] == N - agreement, f"rank-{rank} A={agreement}: j")
    require(record["t"] == agreement - K, f"rank-{rank} A={agreement}: t")
    require(
        record["base_node_count"] == size
        and record["prefix_row_set"] == [0, size - 1],
        f"rank-{rank} A={agreement}: prefix row set",
    )
    require(
        record["degree_bound"] == rank,
        f"rank-{rank} A={agreement}: degree bound",
    )
    expected_update = [field.encode(node) for node in domain[size : size + rank]]
    require(
        record["update_node_encodings"] == expected_update,
        f"rank-{rank} A={agreement}: update nodes",
    )
    if rank <= 3:
        require(record["root_count"] >= 0, f"rank-{rank} A={agreement}: root count")
        if rank == 3:
            require(
                record["linear_root_count_certificate"]["linear_root_count"]
                == record["root_count"],
                f"rank-{rank} A={agreement}: linear root count",
            )
        else:
            require(
                record["root_count"] == len(record["roots"]),
                f"rank-{rank} A={agreement}: listed root count",
            )
    else:
        require(
            record["polynomial_degree"] == rank
            and record["finite_root_bound"] == rank
            and record["root_count_status"] == "not_enumerated_degree_bound_sufficient",
            f"rank-{rank} A={agreement}: degree-bound source",
        )


def finite_source_counts(record: dict[str, Any], rank: int) -> tuple[int, int]:
    if rank <= 3:
        return record["root_count"], record["root_count"]
    return 0, record["finite_root_bound"]


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    require(
        descriptor["schema_version"] == "f17-32-hankel-row-descriptor-v1",
        "row descriptor schema",
    )
    field = field_from_descriptor(descriptor)
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    require(len(domain) == N, "domain length")
    domain_inverses = []
    for node in domain:
        require(not field.is_zero(node), "shifted formula needs nonzero domain")
        domain_inverses.append(field.inv(node))

    source_records, source_artifacts = load_source_records()
    base_nodes: list[tuple[int, ...]] = []
    denominators: list[tuple[int, ...]] = []
    base_determinant = field.one
    base_product = field.one
    records = []
    common_gcd_histogram: Counter[int] = Counter()
    rank_record_totals: Counter[int] = Counter()
    rank_exact_root_totals: Counter[int] = Counter()
    rank_upper_totals: Counter[int] = Counter()
    rank_degree_histograms: dict[int, Counter[int]] = defaultdict(Counter)

    for size in range(1, N - AGREEMENT_MIN + 2):
        new_node = domain[size - 1]
        new_denominator = field.one
        for old_node in base_nodes:
            new_denominator = field.mul(
                new_denominator, field.sub(new_node, old_node)
            )
        for index, old_node in enumerate(base_nodes):
            denominators[index] = field.mul(
                denominators[index], field.sub(old_node, new_node)
            )
        denominators.append(new_denominator)
        base_nodes.append(new_node)
        base_determinant = field.mul(
            base_determinant, field.mul(new_denominator, new_denominator)
        )
        base_product = field.mul(base_product, new_node)

        agreement = N - size + 1
        if not (AGREEMENT_MIN <= agreement <= AGREEMENT_MAX):
            continue

        update_nodes = domain[size : size + max(RANKS)]
        basis_values = update_basis_values(field, base_nodes, denominators, update_nodes)
        shifted_kernel = build_kernel(
            field,
            basis_values,
            domain_inverses[:size],
            update_nodes,
        )
        shifted_base_scale = field.mul(base_determinant, base_product)

        for rank in RANKS:
            source_record = source_records[(rank, agreement)]
            validate_source_record(field, source_record, rank, agreement, size, domain)
            first_coefficients = [
                field.decode(value)
                for value in source_record["hankel_coefficients_ascending"]
            ]
            shifted_coefficients = coefficients_from_kernel(
                field,
                shifted_kernel,
                shifted_base_scale,
                rank,
            )
            common_degree = fpoly_degree(
                fpoly_gcd(first_coefficients, shifted_coefficients, field),
                field,
            )
            require(
                common_degree == 0,
                f"rank-{rank} A={agreement}: first/shifted gcd nontrivial",
            )
            first_degree = fpoly_degree(first_coefficients, field)
            shifted_degree = fpoly_degree(shifted_coefficients, field)
            exact_root_count, finite_root_upper_bound = finite_source_counts(
                source_record,
                rank,
            )
            rank_record_totals[rank] += 1
            rank_exact_root_totals[rank] += exact_root_count
            rank_upper_totals[rank] += finite_root_upper_bound
            rank_degree_histograms[rank][first_degree] += 1
            common_gcd_histogram[common_degree] += 1
            source_kind = (
                "exact_finite_roots"
                if rank <= 3
                else "degree_bound_root_locus"
            )
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": source_record["j"],
                    "t": source_record["t"],
                    "source_kind": source_kind,
                    "first_minor_degree": first_degree,
                    "first_minor_coefficient_hash": hash_json(
                        [field.encode(coefficient) for coefficient in first_coefficients]
                    ),
                    "shifted_minor_row_shift": SHIFT,
                    "shifted_minor_degree": shifted_degree,
                    "shifted_minor_coefficient_hash": hash_json(
                        [
                            field.encode(coefficient)
                            for coefficient in shifted_coefficients
                        ]
                    ),
                    "first_shifted_minor_gcd_degree": common_degree,
                    "exact_finite_root_count_from_source": exact_root_count,
                    "finite_root_upper_bound_from_source": finite_root_upper_bound,
                    "finite_full_hankel_witness_upper": 0,
                    "support_witness_status": "excluded_by_shifted_minor",
                }
            )

    exact_root_total = sum(record["exact_finite_root_count_from_source"] for record in records)
    finite_root_upper_total = sum(
        record["finite_root_upper_bound_from_source"] for record in records
    )
    degree_bound_locus_total = sum(
        record["finite_root_upper_bound_from_source"]
        for record in records
        if record["source_kind"] == "degree_bound_root_locus"
    )
    require(len(records) == EXPECTED_RECORDS, "record count")
    require(exact_root_total == EXPECTED_EXACT_ROOT_TOTAL, "exact root total")
    require(
        degree_bound_locus_total == EXPECTED_DEGREE_BOUND_LOCUS_TOTAL,
        "degree-bound root-locus total",
    )
    require(
        finite_root_upper_total == EXPECTED_FINITE_ROOT_UPPER_TOTAL,
        "finite root upper total",
    )
    require(dict(common_gcd_histogram) == {0: EXPECTED_RECORDS}, "gcd histogram")

    rank_summaries = {}
    for rank in RANKS:
        rank_summaries[str(rank)] = {
            "rank": rank,
            "agreement_count": AGREEMENT_MAX - AGREEMENT_MIN + 1,
            "record_count": rank_record_totals[rank],
            "source_kind": (
                "exact_finite_roots"
                if rank <= 3
                else "degree_bound_root_locus"
            ),
            "exact_finite_root_count_from_source": rank_exact_root_totals[rank],
            "finite_root_upper_bound_from_source": rank_upper_totals[rank],
            "cleared_finite_root_upper_bound": rank_upper_totals[rank],
            "finite_full_hankel_witness_upper_sum": 0,
            "first_minor_degree_histogram": {
                str(key): value
                for key, value in sorted(rank_degree_histograms[rank].items())
            },
            "all_first_minor_loci_excluded_as_support_witnesses": True,
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
        },
        "source_artifacts": source_artifacts,
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "ranks": RANKS,
        "row_shift_tested": SHIFT,
        "claim": (
            "For the synthetic rank-2..5 low-rank M3 ladder, the selected "
            "first regular minor is coprime to the row-shift-1 minor in every "
            "rank/agreement row.  Thus every finite first-minor root counted "
            "exactly in ranks 2..3, and every degree-bounded finite first-minor "
            "root locus in ranks 4..5, is excluded as an actual full-Hankel "
            "support witness."
        ),
        "method": {
            "criterion": "Hankel shifted-minor exclusion criterion",
            "test": "compute gcd(first minor, shifted row-1 minor) in F_17^32[Z]",
            "mathematical_reason": (
                "a true exact-support witness makes the full t by j+1 Hankel "
                "matrix rank-deficient, so all consecutive square minors must "
                "vanish"
            ),
            "scope_upgrade": (
                "for ranks 4..5, coprimality clears the whole first-minor "
                "root locus without enumerating finite roots"
            ),
        },
        "aggregate": {
            "source_record_count": len(source_records),
            "record_count": len(records),
            "exact_finite_root_count_from_source": exact_root_total,
            "degree_bound_root_locus_upper_total": degree_bound_locus_total,
            "finite_root_upper_bound_from_source": finite_root_upper_total,
            "cleared_finite_root_upper_bound": finite_root_upper_total,
            "finite_full_hankel_witness_upper_total": 0,
            "surviving_finite_root_upper_bound": 0,
            "common_gcd_degree_histogram": {
                str(key): value for key, value in sorted(common_gcd_histogram.items())
            },
            "all_first_minor_loci_excluded_as_support_witnesses": True,
            "rank_summaries": rank_summaries,
        },
        "records": sorted(records, key=lambda record: (record["rank"], record["A"])),
        "nonclaims": [
            "synthetic low-rank ladder only, not arbitrary M3 rows",
            "finite first-minor roots only, not the projective endpoint",
            "ranks 4 and 5 use degree-bound root loci rather than enumerated root tables",
            "does not audit quotient image or quotient support",
            "does not replace the singular/pivot chart program outside this ladder",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"rank-2..5 shifted-minor certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 rank-2..5 shifted-minor exclusion")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, exact_roots={exact}, finite_upper={upper}, surviving={surviving}".format(
            records=aggregate["record_count"],
            exact=aggregate["exact_finite_root_count_from_source"],
            upper=aggregate["finite_root_upper_bound_from_source"],
            surviving=aggregate["surviving_finite_root_upper_bound"],
        )
    )
    print(f"common gcd degree histogram: {aggregate['common_gcd_degree_histogram']}")


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
