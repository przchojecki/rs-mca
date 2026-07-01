#!/usr/bin/env python3
"""Verify shifted-minor exclusion for the M3 rank-6..11 low-rank ladder.

The rank-6..11 low-rank slack certificates count finite roots of the first
regular square Hankel minor.  A true exact-support witness must make the full
``t x (j+1)`` Hankel matrix rank-deficient, hence it must kill every consecutive
``(j+1) x (j+1)`` square minor.  This verifier checks the row-shift-1 square
minor against every finite first-minor root counted in those slack certificates.
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
    fpoly_mul,
    hash_json,
    render,
)
from experimental.scripts.verify_f17_32_m3_low_rank9_11_slack_sweep import (  # noqa: E402
    characteristic_polynomial_coefficients,
    update_basis_values,
)


SCHEMA_VERSION = "f17-32-m3-low-rank6-11-shifted-minor-exclusion-v1"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = [6, 7, 8, 9, 10, 11]
SHIFT = 1
EXPECTED_ROOT_TOTAL = 238
EXPECTED_ROOT_BEARING_RECORDS = 158
EXPECTED_METHOD_HISTOGRAM = {
    "source_root_gcd": 72,
    "listed_root_locator": 76,
    "first_shifted_minor_gcd": 10,
}

ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
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
LOW_RANK9_11_SLACK_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/"
    "f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json"
)
SHIFTED_MINOR_CRITERION_REF = (
    "experimental/notes/m1/hankel_shifted_minor_exclusion_criterion.md"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank6-11-shifted-minor-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_shifted_minor_exclusion.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = REPO_ROOT / ref if isinstance(ref, str) else ref
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(ref: str) -> str:
    return sha256((REPO_ROOT / ref).read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def field_from_descriptor(descriptor: dict[str, Any]) -> PolynomialBasisField:
    return PolynomialBasisField.from_spec(
        {
            "kind": "polynomial_basis",
            "p": descriptor["field_model"]["p"],
            "modulus": descriptor["field_model"]["modulus"],
        }
    )


def root_locator_from_list(
    roots: list[int],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    polynomial = [field.one]
    for encoded_root in roots:
        root = field.decode(encoded_root)
        polynomial = fpoly_mul(polynomial, [field.neg(root), field.one], field)
    return polynomial


def load_source_records() -> tuple[dict[tuple[int, int], dict[str, Any]], dict[str, Any]]:
    sources = [
        (LOW_RANK6_SLACK_REF, "f17-32-m3-low-rank6-slack-family-v1"),
        (LOW_RANK7_SLACK_REF, "f17-32-m3-low-rank7-slack-family-v1"),
        (LOW_RANK8_SLACK_REF, "f17-32-m3-low-rank8-slack-family-v1"),
        (LOW_RANK9_11_SLACK_REF, "f17-32-m3-low-rank9-11-slack-sweep-v1"),
    ]
    records: dict[tuple[int, int], dict[str, Any]] = {}
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
        "slack_certificates": [],
    }
    for ref, schema_version in sources:
        certificate = load_json(ref)
        require(certificate["schema_version"] == schema_version, f"{ref}: schema")
        require(certificate["status"] == "PROVED / AUDIT", f"{ref}: status")
        require(
            certificate["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
            f"{ref}: agreement range",
        )
        source_artifacts["slack_certificates"].append(
            {
                "ref": ref,
                "schema_version": schema_version,
                "sha256": file_sha256(ref),
            }
        )
        for record in certificate["records"]:
            rank = record.get("rank") or record["degree_bound"]
            key = (rank, record["A"])
            require(key not in records, f"duplicate record {key}")
            records[key] = record
    require(
        len(records) == len(RANKS) * (AGREEMENT_MAX - AGREEMENT_MIN + 1),
        "source record count",
    )
    return records, source_artifacts


def build_kernel(
    field: PolynomialBasisField,
    basis_values: list[list[tuple[int, ...]]],
    base_weights: list[tuple[int, ...]],
    update_weights: list[tuple[int, ...]],
) -> list[list[tuple[int, ...]]]:
    max_rank = len(update_weights)
    kernel = []
    for row_index in range(max_rank):
        left_values = basis_values[row_index]
        row = []
        for right_values in basis_values[:max_rank]:
            entry = field.zero
            for weight, left, right in zip(base_weights, left_values, right_values):
                entry = field.add(entry, field.mul(weight, field.mul(left, right)))
            row.append(field.mul(update_weights[row_index], entry))
        kernel.append(row)
    return kernel


def coefficients_from_kernel(
    field: PolynomialBasisField,
    kernel: list[list[tuple[int, ...]]],
    base_scale: tuple[int, ...],
    rank: int,
) -> list[tuple[int, ...]]:
    subkernel = [row[:rank] for row in kernel[:rank]]
    return [
        field.mul(base_scale, coefficient)
        for coefficient in characteristic_polynomial_coefficients(subkernel, field)
    ]


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
        f"rank-{rank} A={agreement}: prefix",
    )
    require(
        record["degree_bound"] == rank
        and record["polynomial_degree"] == rank,
        f"rank-{rank} A={agreement}: degree",
    )
    if rank <= 8:
        expected_update = [field.encode(node) for node in domain[size : size + rank]]
        require(
            record["update_node_encodings"] == expected_update,
            f"rank-{rank} A={agreement}: update nodes",
        )
        require(
            record["linear_root_count_certificate"]["linear_root_count"]
            == record["root_count"],
            f"rank-{rank} A={agreement}: root count certificate",
        )
    else:
        require(
            record["update_node_range"] == [size, size + rank - 1],
            f"rank-{rank} A={agreement}: update range",
        )


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
    all_row_root_histograms: dict[int, Counter[int]] = defaultdict(Counter)
    method_histogram: Counter[str] = Counter()
    rank_root_totals: Counter[int] = Counter()
    rank_record_totals: Counter[int] = Counter()
    count_only_rows = []

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

        root_bearing_ranks = []
        for rank in RANKS:
            source_record = source_records[(rank, agreement)]
            validate_source_record(field, source_record, rank, agreement, size, domain)
            root_count = source_record["root_count"]
            all_row_root_histograms[rank][root_count] += 1
            if root_count:
                root_bearing_ranks.append(rank)
        if not root_bearing_ranks:
            continue

        max_rank = max(root_bearing_ranks)
        update_nodes = domain[size : size + max_rank]
        basis_values = update_basis_values(field, base_nodes, denominators, update_nodes)
        shifted_kernel = build_kernel(
            field,
            basis_values,
            domain_inverses[:size],
            update_nodes,
        )
        shifted_base_scale = field.mul(base_determinant, base_product)
        count_only_ranks = [
            rank
            for rank in root_bearing_ranks
            if rank >= 9 and source_records[(rank, agreement)]["listed_roots"] is None
        ]
        first_kernel = None
        if count_only_ranks:
            first_kernel = build_kernel(
                field,
                basis_values,
                [field.one] * size,
                [field.one] * max(count_only_ranks),
            )

        for rank in root_bearing_ranks:
            source_record = source_records[(rank, agreement)]
            root_count = source_record["root_count"]
            shifted_coefficients = coefficients_from_kernel(
                field,
                shifted_kernel,
                shifted_base_scale,
                rank,
            )
            shifted_encoded = [
                field.encode(coefficient) for coefficient in shifted_coefficients
            ]
            output_record = {
                "rank": rank,
                "A": agreement,
                "j": source_record["j"],
                "t": source_record["t"],
                "root_count": root_count,
                "shifted_minor_row_shift": SHIFT,
                "shifted_minor_degree": fpoly_degree(shifted_coefficients, field),
                "shifted_minor_coefficient_hash": hash_json(shifted_encoded),
            }
            rank_root_totals[rank] += root_count
            rank_record_totals[rank] += 1

            if rank <= 8:
                root_gcd = [
                    field.decode(value)
                    for value in source_record["linear_root_count_certificate"][
                        "linear_root_gcd_coefficients_ascending"
                    ]
                ]
                require(
                    fpoly_degree(root_gcd, field) == root_count,
                    f"rank-{rank} A={agreement}: source root gcd degree",
                )
                common_degree = fpoly_degree(
                    fpoly_gcd(root_gcd, shifted_coefficients, field),
                    field,
                )
                require(
                    common_degree == 0,
                    f"rank-{rank} A={agreement}: shifted root-gcd overlap",
                )
                method = "source_root_gcd"
                output_record.update(
                    {
                        "exclusion_method": method,
                        "source_root_gcd_hash": hash_json(
                            [
                                field.encode(coefficient)
                                for coefficient in root_gcd
                            ]
                        ),
                        "common_gcd_degree": common_degree,
                        "cleared_root_count": root_count,
                    }
                )
            elif source_record["listed_roots"] is not None:
                root_gcd = root_locator_from_list(
                    source_record["listed_roots"],
                    field,
                )
                require(
                    fpoly_degree(root_gcd, field) == root_count,
                    f"rank-{rank} A={agreement}: listed root degree",
                )
                common_degree = fpoly_degree(
                    fpoly_gcd(root_gcd, shifted_coefficients, field),
                    field,
                )
                require(
                    common_degree == 0,
                    f"rank-{rank} A={agreement}: listed shifted overlap",
                )
                method = "listed_root_locator"
                output_record.update(
                    {
                        "exclusion_method": method,
                        "listed_root_locator_hash": hash_json(
                            [
                                field.encode(coefficient)
                                for coefficient in root_gcd
                            ]
                        ),
                        "common_gcd_degree": common_degree,
                        "cleared_root_count": root_count,
                    }
                )
            else:
                require(first_kernel is not None, "missing first-minor kernel")
                first_coefficients = coefficients_from_kernel(
                    field,
                    first_kernel,
                    base_determinant,
                    rank,
                )
                first_encoded = [
                    field.encode(coefficient) for coefficient in first_coefficients
                ]
                require(
                    hash_json(first_encoded) == source_record["coefficient_hash"],
                    f"rank-{rank} A={agreement}: first-minor hash",
                )
                common_degree = fpoly_degree(
                    fpoly_gcd(first_coefficients, shifted_coefficients, field),
                    field,
                )
                require(
                    common_degree == 0,
                    f"rank-{rank} A={agreement}: first/shifted overlap",
                )
                method = "first_shifted_minor_gcd"
                count_only_rows.append(
                    {"rank": rank, "A": agreement, "root_count": root_count}
                )
                output_record.update(
                    {
                        "exclusion_method": method,
                        "source_first_minor_coefficient_hash": (
                            source_record["coefficient_hash"]
                        ),
                        "first_shifted_minor_gcd_degree": common_degree,
                        "cleared_root_count": root_count,
                    }
                )
            method_histogram[method] += 1
            records.append(output_record)

    finite_root_total = sum(record["root_count"] for record in records)
    cleared_root_total = sum(record["cleared_root_count"] for record in records)
    require(finite_root_total == EXPECTED_ROOT_TOTAL, "finite root total")
    require(cleared_root_total == EXPECTED_ROOT_TOTAL, "cleared root total")
    require(
        len(records) == EXPECTED_ROOT_BEARING_RECORDS,
        "root-bearing record count",
    )
    require(
        dict(method_histogram) == EXPECTED_METHOD_HISTOGRAM,
        "method histogram",
    )

    rank_summaries = {}
    for rank in RANKS:
        rank_summaries[str(rank)] = {
            "rank": rank,
            "agreement_count": AGREEMENT_MAX - AGREEMENT_MIN + 1,
            "root_bearing_record_count": rank_record_totals[rank],
            "finite_root_count": rank_root_totals[rank],
            "cleared_root_count": rank_root_totals[rank],
            "root_count_histogram": {
                str(key): all_row_root_histograms[rank][key]
                for key in sorted(all_row_root_histograms[rank])
            },
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
            "For the synthetic rank-6..11 low-rank M3 slack ladder, every "
            "finite first-minor root counted by the source slack certificates "
            "is excluded as an actual full-Hankel support witness by the "
            "row-shift-1 square minor."
        ),
        "method": {
            "criterion": "Hankel shifted-minor exclusion criterion",
            "test": (
                "roots supplied by source gcds or listed root locators are "
                "checked by gcd(root_gcd, shifted minor); count-only cubic "
                "rows are checked by the stronger gcd(first minor, shifted "
                "minor)"
            ),
            "mathematical_reason": (
                "a true exact-support witness makes the full t by j+1 Hankel "
                "matrix rank-deficient, so all consecutive square minors must "
                "vanish"
            ),
            "shifted_minor_formula": (
                "det(H_X^(1)+Z H_Y^(1)) = det(H_X^(1)) det(I+Z K_1), "
                "with K_1,ab=y_a sum_i x_i^{-1} L_i(y_a)L_i(y_b)"
            ),
        },
        "aggregate": {
            "source_record_count": len(source_records),
            "root_bearing_record_count": len(records),
            "finite_root_total": finite_root_total,
            "cleared_root_total": cleared_root_total,
            "surviving_root_total": finite_root_total - cleared_root_total,
            "all_finite_roots_excluded_as_support_witnesses": True,
            "method_histogram": dict(method_histogram),
            "rank_summaries": rank_summaries,
            "count_only_rows": count_only_rows,
        },
        "records": sorted(records, key=lambda record: (record["rank"], record["A"])),
        "nonclaims": [
            "synthetic low-rank slack ladder only, not arbitrary M3 rows",
            "finite first-minor roots only, not the projective endpoint",
            "does not audit quotient image or quotient support",
            "does not replace the singular/pivot chart program outside this ladder",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"rank-6..11 shifted-minor certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 rank-6..11 shifted-minor exclusion")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, finite_roots={roots}, cleared={cleared}".format(
            records=aggregate["root_bearing_record_count"],
            roots=aggregate["finite_root_total"],
            cleared=aggregate["cleared_root_total"],
        )
    )
    print(f"method histogram: {aggregate['method_histogram']}")


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
