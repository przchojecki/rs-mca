#!/usr/bin/env python3
"""Verify the F_17^32 M3 rank-9..11 low-rank finite-slack sweep.

For each 385 <= A <= 426, put r=j+1=513-A and use the first r
descriptor-domain nodes as X.  For update rank s in {9,10,11}, use the next s
descriptor nodes as Y and compute

    Delta_s(Z)=det(H_X) det(I+ZK_s),
    (K_s)_ab=sum_i L_i(y_a)L_i(y_b).

Ranks 9..11 are far outside the v4 low-rank degree envelope: degree-only
projective accounting gives s+1 in {10,11,12}, all above the budget numerator
6.  This sweep checks exact finite-field roots by gcd(Delta_s,Z^q-Z).  In this
nested synthetic family every rank in the sweep has at most three finite roots
per agreement, so the corrected projective count is at most 3+1=4.
"""

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

from experimental.scripts.extract_regular_hankel_minors import (
    PolynomialBasisField,
    field_batch_inverses,
    fpoly_degree,
    fpoly_gcd,
    fpoly_trim,
    hash_json,
    render,
)
from experimental.scripts.verify_f17_32_m3_low_rank3_family import (
    listed_roots_from_gcd,
    monic_polynomial,
    x_power_mod_monic,
)


SCHEMA_VERSION = "f17-32-m3-low-rank9-11-slack-sweep-v1"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = [9, 10, 11]
MAX_RANK = max(RANKS)
TWO128 = 2**128
EXPECTED_ROOT_HISTOGRAMS = {
    9: {"0": 17, "1": 17, "2": 6, "3": 2},
    10: {"0": 8, "1": 23, "2": 9, "3": 2},
    11: {"0": 15, "1": 16, "2": 5, "3": 6},
}
EXPECTED_ROOT_SUMS = {9: 35, 10: 47, 11: 44}

ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_RANK_TEMPLATE = REPO_ROOT / (
    "experimental/data/certificates/hankel-low-rank-update-template/"
    "hankel_low_rank_update_template_certificate.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/"
    "f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def matrix_multiply(
    left: list[list[tuple[int, ...]]],
    right: list[list[tuple[int, ...]]],
    field: PolynomialBasisField,
) -> list[list[tuple[int, ...]]]:
    rows = len(left)
    inner = len(right)
    cols = len(right[0])
    out = []
    for row in range(rows):
        out_row = []
        for col in range(cols):
            entry = field.zero
            for index in range(inner):
                entry = field.add(
                    entry,
                    field.mul(left[row][index], right[index][col]),
                )
            out_row.append(entry)
        out.append(out_row)
    return out


def matrix_trace(
    matrix: list[list[tuple[int, ...]]],
    field: PolynomialBasisField,
) -> tuple[int, ...]:
    total = field.zero
    for index in range(len(matrix)):
        total = field.add(total, matrix[index][index])
    return total


def characteristic_polynomial_coefficients(
    kernel: list[list[tuple[int, ...]]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    """Return coefficients of det(I+ZK) by Newton identities."""

    size = len(kernel)
    coefficients = [field.one]
    powers = []
    current_power = kernel
    for power in range(1, size + 1):
        if power > 1:
            current_power = matrix_multiply(current_power, kernel, field)
        powers.append(matrix_trace(current_power, field))
    for degree in range(1, size + 1):
        total = field.zero
        for index in range(1, degree + 1):
            term = field.mul(coefficients[degree - index], powers[index - 1])
            if index % 2:
                total = field.add(total, term)
            else:
                total = field.sub(total, term)
        coefficients.append(field.div(total, field.normalize(degree)))
    return coefficients


def update_basis_values(
    field: PolynomialBasisField,
    base_nodes: list[tuple[int, ...]],
    base_denominators: list[tuple[int, ...]],
    update_nodes: list[tuple[int, ...]],
) -> list[list[tuple[int, ...]]]:
    denominator_inverses = field_batch_inverses(base_denominators, field)
    basis_values_by_update = []
    for update in update_nodes:
        differences = []
        product_all = field.one
        for base in base_nodes:
            difference = field.sub(update, base)
            differences.append(difference)
            product_all = field.mul(product_all, difference)
        difference_inverses = field_batch_inverses(differences, field)
        basis_values_by_update.append(
            [
                field.mul(product_all, field.mul(diff_inv, denom_inv))
                for diff_inv, denom_inv in zip(
                    difference_inverses, denominator_inverses
                )
            ]
        )
    return basis_values_by_update


def low_rank_coefficients_from_basis_values(
    field: PolynomialBasisField,
    basis_values_by_update: list[list[tuple[int, ...]]],
    base_determinant: tuple[int, ...],
    rank: int,
) -> list[tuple[int, ...]]:
    kernel = []
    for left_values in basis_values_by_update[:rank]:
        row = []
        for right_values in basis_values_by_update[:rank]:
            entry = field.zero
            for left, right in zip(left_values, right_values):
                entry = field.add(entry, field.mul(left, right))
            row.append(entry)
        kernel.append(row)

    kernel_coefficients = characteristic_polynomial_coefficients(kernel, field)
    return [
        field.mul(base_determinant, coefficient)
        for coefficient in kernel_coefficients
    ]


def frobenius_linear_root_gcd(
    coefficients: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], list[tuple[int, ...]]]:
    monic = monic_polynomial(coefficients, field)
    remainder = x_power_mod_monic(field.size, monic, field)
    if len(remainder) < 2:
        remainder += [field.zero] * (2 - len(remainder))
    remainder[1] = field.sub(remainder[1], field.one)
    remainder = fpoly_trim(remainder, field)
    gcd = fpoly_gcd(monic, remainder, field)
    return monic, remainder, gcd


def root_status(root_count: int) -> str:
    return {
        0: "exact_no_finite_roots",
        1: "exact_one_finite_root",
        2: "exact_two_finite_roots",
        3: "exact_three_finite_roots",
    }[root_count]


def validate_low_rank_template() -> None:
    template = load_json(LOW_RANK_TEMPLATE)
    require(
        template["schema_version"] == "m1-hankel-low-rank-update-template-v4",
        "low-rank template schema mismatch",
    )
    gate = template["m3_low_rank_packet_gate"]
    finite_safe_ranks = gate["finite_safe_update_ranks"]
    projective_safe_ranks = gate[
        "projective_safe_without_extra_certificate_update_ranks"
    ]
    require(
        min(RANKS) > max(finite_safe_ranks)
        and all(rank not in finite_safe_ranks for rank in RANKS)
        and all(rank not in projective_safe_ranks for rank in RANKS),
        "rank sweep is not beyond the v4 low-rank degree envelope",
    )


def build_records(
    field: PolynomialBasisField,
    domain: list[tuple[int, ...]],
) -> list[dict[str, Any]]:
    validate_low_rank_template()
    records = []
    base_nodes: list[tuple[int, ...]] = []
    denominators: list[tuple[int, ...]] = []
    base_determinant = field.one
    finite_budget = field.size // TWO128
    projective_budget = (field.size + 1) // TWO128

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

        agreement = N - size + 1
        if agreement < AGREEMENT_MIN or agreement > AGREEMENT_MAX:
            continue
        update_nodes = domain[size : size + MAX_RANK]
        basis_values_by_update = update_basis_values(
            field,
            base_nodes,
            denominators,
            update_nodes,
        )
        for rank in RANKS:
            coefficients = low_rank_coefficients_from_basis_values(
                field,
                basis_values_by_update,
                base_determinant,
                rank,
            )
            require(
                fpoly_degree(coefficients, field) == rank,
                f"A={agreement}, rank={rank}: polynomial degree mismatch",
            )
            require(
                not field.is_zero(coefficients[-1]),
                f"A={agreement}, rank={rank}: leading coefficient vanishes",
            )
            monic, frobenius_remainder, root_gcd = frobenius_linear_root_gcd(
                coefficients, field
            )
            root_count_value = fpoly_degree(root_gcd, field)
            require(
                0 <= root_count_value <= 3,
                f"A={agreement}, rank={rank}: rank sweep finite-root slack failed",
            )
            listed_roots = listed_roots_from_gcd(root_gcd, field)
            if listed_roots is not None:
                require(
                    len(listed_roots) == root_count_value,
                    f"A={agreement}, rank={rank}: listed finite roots mismatch",
                )
            else:
                require(
                    root_count_value > 2,
                    f"A={agreement}, rank={rank}: small-degree roots should be listed",
                )
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": N - agreement,
                    "t": agreement - K,
                    "prefix_row_set": [0, size - 1],
                    "base_node_count": size,
                    "update_node_range": [size, size + rank - 1],
                    "degree_bound": rank,
                    "polynomial_degree": rank,
                    "coefficient_hash": hash_json(
                        [field.encode(coefficient) for coefficient in coefficients]
                    ),
                    "root_status": root_status(root_count_value),
                    "root_count": root_count_value,
                    "listed_roots": listed_roots,
                    "root_count_hash": hash_json(
                        {
                            "root_count": root_count_value,
                            "linear_root_gcd": [
                                field.encode(coefficient) for coefficient in root_gcd
                            ],
                        }
                    ),
                    "linear_root_count_certificate": {
                        "kind": "frobenius_linear_root_gcd",
                        "field_encoding": "base-p low-to-high integer",
                        "field_order": field.size,
                        "polynomial": "Z^q-Z",
                        "monic_delta_hash": hash_json(
                            [field.encode(coefficient) for coefficient in monic]
                        ),
                        "frobenius_remainder_hash": hash_json(
                            [
                                field.encode(coefficient)
                                for coefficient in frobenius_remainder
                            ]
                        ),
                        "linear_root_gcd_hash": hash_json(
                            [field.encode(coefficient) for coefficient in root_gcd]
                        ),
                        "linear_root_count": root_count_value,
                        "listed_roots_status": (
                            "listed" if listed_roots is not None else "count_only"
                        ),
                    },
                    "projective_infinity": {
                        "projective_point": "[0:1]",
                        "status": "nonempty_not_excluded_by_regular_minor",
                        "contribution": 1,
                        "reason": (
                            "the update direction has rank below the original "
                            "regular-minor top degree j+1, so this regular "
                            "minor does not exclude the projective infinity point"
                        ),
                    },
                    "regular_budget_table": {
                        "finite_affine_roots": root_count_value,
                        "degree_only_finite_root_bound": rank,
                        "projective_infinity_roots": 1,
                        "projective_regular_roots": root_count_value + 1,
                        "degree_only_projective_bound": rank + 1,
                        "finite_budget_numerator": finite_budget,
                        "projective_budget_numerator": projective_budget,
                        "finite_budget_gap": finite_budget - root_count_value,
                        "projective_budget_gap": projective_budget
                        - root_count_value
                        - 1,
                        "degree_only_projective_budget_gap": (
                            projective_budget - rank - 1
                        ),
                        "within_finite_budget": root_count_value <= finite_budget,
                        "within_projective_budget": (
                            root_count_value + 1 <= projective_budget
                        ),
                        "finite_root_slack_certificate": "frobenius_gcd_root_count",
                        "quotient_image_subtraction_status": "not_audited",
                    },
                }
            )
    return sorted(records, key=lambda record: (record["rank"], record["A"]))


def rank_summary(records: list[dict[str, Any]], rank: int) -> dict[str, Any]:
    rank_records = [record for record in records if record["rank"] == rank]
    require(
        len(rank_records) == AGREEMENT_MAX - AGREEMENT_MIN + 1,
        f"rank={rank}: record count mismatch",
    )
    root_histogram = Counter(record["root_count"] for record in rank_records)
    histogram = {str(key): root_histogram[key] for key in sorted(root_histogram)}
    root_sum = sum(record["root_count"] for record in rank_records)
    max_finite_roots = max(record["root_count"] for record in rank_records)
    require(
        histogram == EXPECTED_ROOT_HISTOGRAMS[rank],
        f"rank={rank}: root histogram mismatch",
    )
    require(root_sum == EXPECTED_ROOT_SUMS[rank], f"rank={rank}: root sum mismatch")
    require(max_finite_roots == 3, f"rank={rank}: finite-root max mismatch")
    return {
        "rank": rank,
        "agreement_count": len(rank_records),
        "degree_bound_sum": rank * len(rank_records),
        "polynomial_degree_histogram": {str(rank): len(rank_records)},
        "exact_regular_root_count_sum": root_sum,
        "linear_root_count_histogram": histogram,
        "projective_infinity_contribution_sum": len(rank_records),
        "max_finite_roots_per_agreement": max_finite_roots,
        "max_projective_regular_roots_per_agreement": max_finite_roots + 1,
        "degree_only_projective_bound_without_slack": rank + 1,
        "degree_only_projective_bound_within_budget": False,
        "all_rows_within_finite_budget": True,
        "all_rows_within_projective_budget": True,
        "worst_agreements": [
            record["A"]
            for record in rank_records
            if record["root_count"] == max_finite_roots
        ],
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR)
    field = PolynomialBasisField.from_spec(
        {
            "kind": "polynomial_basis",
            "p": descriptor["field_model"]["p"],
            "modulus": descriptor["field_model"]["modulus"],
        }
    )
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    require(len(domain) == N, "descriptor domain length mismatch")
    records = build_records(field, domain)
    rank_summaries = {str(rank): rank_summary(records, rank) for rank in RANKS}
    projective_budget = (field.size + 1) // TWO128
    require(
        all(
            summary["max_projective_regular_roots_per_agreement"] <= projective_budget
            for summary in rank_summaries.values()
        ),
        "projective budget fail",
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
        "source_artifacts": {
            "row_descriptor": {
                "ref": str(ROW_DESCRIPTOR.relative_to(REPO_ROOT)),
                "sha256": file_sha256(ROW_DESCRIPTOR),
            },
            "low_rank_template": {
                "ref": str(LOW_RANK_TEMPLATE.relative_to(REPO_ROOT)),
                "schema_version": "m1-hankel-low-rank-update-template-v4",
                "sha256": file_sha256(LOW_RANK_TEMPLATE),
            },
        },
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "construction": {
            "base_nodes": "first j+1 descriptor-domain elements",
            "update_nodes": "first s nodes after the base prefix",
            "ranks": RANKS,
            "certificate_mode": "low_rank_update_finite_slack_sweep",
        },
        "endpoint_conventions": {
            "finite_affine_slope_denominator": field.size,
            "projective_slope_denominator": field.size + 1,
            "finite_budget_numerator": field.size // TWO128,
            "projective_budget_numerator": projective_budget,
            "extra_projective_point": "[0:1]",
        },
        "method": {
            "identity": "Delta_s(Z)=det(H_X) det(I+ZK_s)",
            "kernel": "(K_s)_ab=sum_i L_i(y_a)L_i(y_b)",
            "coefficient_replay": "Newton identities from traces of K_s^i",
            "finite_root_count": "deg gcd(Delta_s(Z), Z^q-Z)",
            "finite_slack": (
                "ranks 9..11 have at most three finite roots per agreement "
                "in this nested synthetic family"
            ),
            "projective_root_bound": (
                "adding the one nonexcluded projective infinity point gives "
                "at most four projective regular roots"
            ),
        },
        "aggregate": {
            "rank_summaries": rank_summaries,
            "rank_count": len(RANKS),
            "record_count": len(records),
            "max_projective_regular_roots_over_sweep": max(
                summary["max_projective_regular_roots_per_agreement"]
                for summary in rank_summaries.values()
            ),
            "all_rows_within_projective_budget": True,
            "generic_degree_bound_sum_for_window": sum(
                N - agreement + 1
                for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1)
            ),
        },
        "records": records,
        "nonclaims": [
            "synthetic syndrome-pencil family only",
            "not a worst-case MCA row bound",
            "does not perform a quotient/tangent subtraction table",
            "does not claim the same slack beyond rank 11",
            "quotient-image overlap is not audited here",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-9..11 low-rank slack sweep mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank-9..11 finite-slack sweep")
    print(f"status: {certificate['status']}")
    print(
        "agreements: {lo}..{hi}, ranks={ranks}, records={count}".format(
            lo=certificate["agreement_range"][0],
            hi=certificate["agreement_range"][1],
            ranks=certificate["construction"]["ranks"],
            count=aggregate["record_count"],
        )
    )
    for rank in certificate["construction"]["ranks"]:
        summary = aggregate["rank_summaries"][str(rank)]
        print(
            "rank {rank}: root_sum={root_sum}, histogram={hist}, max_projective={max_projective}".format(
                rank=rank,
                root_sum=summary["exact_regular_root_count_sum"],
                hist=summary["linear_root_count_histogram"],
                max_projective=summary[
                    "max_projective_regular_roots_per_agreement"
                ],
            )
        )
    print(
        "sweep max projective roots/agreement={max_projective}, budget={budget}".format(
            max_projective=aggregate["max_projective_regular_roots_over_sweep"],
            budget=certificate["endpoint_conventions"][
                "projective_budget_numerator"
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
