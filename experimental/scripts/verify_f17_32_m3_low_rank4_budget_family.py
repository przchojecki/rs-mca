#!/usr/bin/env python3
"""Verify the F_17^32 M3 rank-4 low-rank budget family certificate.

For each 385 <= A <= 426, put r=j+1=513-A and use the first r
descriptor-domain nodes as X, with the next four descriptor nodes as Y.  The
low-rank template gives

    Delta_r(Z)=det(H_X) det(I+ZK),
    K_ab=sum_i L_i(y_a)L_i(y_b).

This verifier does not enumerate finite roots.  For update rank 4 that is not
needed for the M3 projective budget: once Delta_r is proved nonzero of degree
4, the finite root bound is <=4 and the corrected low-rank projective endpoint
adds at most one infinity point, giving <=5 projective regular roots against
budget numerator 6.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, permutations
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
    hash_json,
    render,
)


SCHEMA_VERSION = "f17-32-m3-low-rank4-budget-family-v1"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
UPDATE_RANK = 4
TWO128 = 2**128
ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_RANK_TEMPLATE = REPO_ROOT / (
    "experimental/data/certificates/hankel-low-rank-update-template/"
    "hankel_low_rank_update_template_certificate.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank4-budget-family/"
    "f17_32_n512_k256_m3_low_rank4_budget_family_certificate.json"
)


PERMUTATIONS_BY_SIZE = {
    size: list(permutations(range(size))) for size in range(UPDATE_RANK + 1)
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = 0
    for left_index, left in enumerate(permutation):
        for right in permutation[left_index + 1 :]:
            if left > right:
                inversions += 1
    return -1 if inversions % 2 else 1


PERMUTATION_SIGNS = {
    size: {
        permutation: permutation_sign(permutation)
        for permutation in PERMUTATIONS_BY_SIZE[size]
    }
    for size in PERMUTATIONS_BY_SIZE
}


def small_determinant(
    matrix: list[list[tuple[int, ...]]],
    field: PolynomialBasisField,
) -> tuple[int, ...]:
    """Determinant by Leibniz expansion, avoiding extension-field inversions."""

    size = len(matrix)
    if size == 0:
        return field.one
    total = field.zero
    for permutation in PERMUTATIONS_BY_SIZE[size]:
        term = field.one
        for row, col in enumerate(permutation):
            term = field.mul(term, matrix[row][col])
        if PERMUTATION_SIGNS[size][permutation] < 0:
            total = field.sub(total, term)
        else:
            total = field.add(total, term)
    return total


def characteristic_polynomial_coefficients(
    kernel: list[list[tuple[int, ...]]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    """Return coefficients of det(I+ZK) in ascending powers of Z."""

    size = len(kernel)
    coefficients = [field.one]
    for degree in range(1, size + 1):
        coefficient = field.zero
        for subset in combinations(range(size), degree):
            principal_minor = [[kernel[row][col] for col in subset] for row in subset]
            coefficient = field.add(
                coefficient,
                small_determinant(principal_minor, field),
            )
        coefficients.append(coefficient)
    return coefficients


def low_rank_sidecar_from_prefix(
    field: PolynomialBasisField,
    base_nodes: list[tuple[int, ...]],
    base_denominators: list[tuple[int, ...]],
    base_determinant: tuple[int, ...],
    update_nodes: list[tuple[int, ...]],
) -> tuple[list[tuple[int, ...]], dict[str, Any]]:
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

    kernel = []
    for left_values in basis_values_by_update:
        row = []
        for right_values in basis_values_by_update:
            entry = field.zero
            for left, right in zip(left_values, right_values):
                entry = field.add(entry, field.mul(left, right))
            row.append(entry)
        kernel.append(row)

    kernel_coefficients = characteristic_polynomial_coefficients(kernel, field)
    hankel_coefficients = [
        field.mul(base_determinant, coefficient)
        for coefficient in kernel_coefficients
    ]
    sidecar = {
        "kind": "square_base_lagrange_kernel_rank4_budget",
        "formula": "Delta(Z)=det(H_X) det(I+Z K), K_ab=sum_i L_i(y_a)L_i(y_b)",
        "coefficient_method": "principal-minor coefficients of det(I+ZK)",
        "base_node_count": len(base_nodes),
        "update_rank": len(update_nodes),
        "base_hankel_determinant": field.encode(base_determinant),
        "kernel": [[field.encode(entry) for entry in row] for row in kernel],
        "kernel_det_coefficients_ascending": [
            field.encode(coefficient) for coefficient in kernel_coefficients
        ],
        "hankel_coefficients_ascending": [
            field.encode(coefficient) for coefficient in hankel_coefficients
        ],
    }
    return hankel_coefficients, sidecar


def build_records(
    field: PolynomialBasisField,
    domain: list[tuple[int, ...]],
) -> list[dict[str, Any]]:
    template = load_json(LOW_RANK_TEMPLATE)
    require(
        template["schema_version"] == "m1-hankel-low-rank-update-template-v4",
        "low-rank template schema mismatch",
    )
    gate = template["m3_low_rank_packet_gate"]
    require(
        UPDATE_RANK in gate["projective_safe_without_extra_certificate_update_ranks"],
        "rank-4 projective gate is not marked safe",
    )
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
        update_nodes = domain[size : size + UPDATE_RANK]
        coefficients, sidecar = low_rank_sidecar_from_prefix(
            field,
            base_nodes,
            denominators,
            base_determinant,
            update_nodes,
        )
        encoded_coefficients = [
            field.encode(coefficient) for coefficient in coefficients
        ]
        require(
            fpoly_degree(coefficients, field) == UPDATE_RANK,
            f"A={agreement}: rank-4 polynomial is not degree 4",
        )
        require(
            not field.is_zero(coefficients[-1]),
            f"A={agreement}: compressed leading coefficient vanishes",
        )
        records.append(
            {
                "A": agreement,
                "j": N - agreement,
                "t": agreement - K,
                "prefix_row_set": [0, size - 1],
                "base_node_count": size,
                "update_node_encodings": [
                    field.encode(node) for node in update_nodes
                ],
                "degree_bound": UPDATE_RANK,
                "polynomial_degree": UPDATE_RANK,
                "root_count_status": "not_enumerated_degree_bound_sufficient",
                "finite_root_bound": UPDATE_RANK,
                "projective_infinity": {
                    "projective_point": "[0:1]",
                    "status": "nonempty_not_excluded_by_regular_minor",
                    "contribution": 1,
                    "top_degree": size,
                    "top_coefficient_encoding": field.encode(field.zero),
                    "compressed_degree": UPDATE_RANK,
                    "compressed_leading_coefficient_encoding": (
                        encoded_coefficients[-1]
                    ),
                    "reason": (
                        "projective infinity is controlled by the original "
                        "regular-minor top degree j+1.  The low-rank update "
                        "direction has rank 4 < j+1, so det H(v)=0 and this "
                        "regular minor does not exclude [0:1]; the nonzero "
                        "compressed quartic leading coefficient only controls "
                        "the finite affine degree"
                    ),
                },
                "regular_budget_table": {
                    "finite_affine_roots_bound": UPDATE_RANK,
                    "projective_infinity_roots": 1,
                    "projective_regular_roots_bound": UPDATE_RANK + 1,
                    "finite_budget_numerator": finite_budget,
                    "projective_budget_numerator": projective_budget,
                    "finite_budget_gap": finite_budget - UPDATE_RANK,
                    "projective_budget_gap": projective_budget - UPDATE_RANK - 1,
                    "within_finite_budget": UPDATE_RANK <= finite_budget,
                    "within_projective_budget": (
                        UPDATE_RANK + 1 <= projective_budget
                    ),
                    "tangent_overlap_status": "not_enumerated_not_needed_for_upper_bound",
                    "quotient_image_subtraction_status": "not_audited",
                },
                "hankel_coefficients_ascending": encoded_coefficients,
                "low_rank_compression": sidecar,
                "sidecar_hash": hash_json(sidecar),
            }
        )
    return sorted(records, key=lambda record: record["A"])


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
    require(len(records) == AGREEMENT_MAX - AGREEMENT_MIN + 1, "record count mismatch")

    finite_budget = field.size // TWO128
    projective_budget = (field.size + 1) // TWO128
    require(UPDATE_RANK <= finite_budget, "rank-4 family exceeds finite budget")
    require(
        UPDATE_RANK + 1 <= projective_budget,
        "rank-4 family exceeds projective budget",
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
            "update_nodes": "next four descriptor-domain elements",
            "certificate_mode": "low_rank_update_budget_bound",
            "rank": UPDATE_RANK,
        },
        "endpoint_conventions": {
            "finite_affine_slope_denominator": field.size,
            "projective_slope_denominator": field.size + 1,
            "finite_budget_numerator": finite_budget,
            "projective_budget_numerator": projective_budget,
            "extra_projective_point": "[0:1]",
        },
        "method": {
            "identity": "Delta_r(Z)=det(H_X) det(I+ZK)",
            "kernel": "K_ab=sum_i L_i(y_a)L_i(y_b)",
            "coefficient_replay": "principal-minor coefficients of det(I+ZK)",
            "finite_root_bound": "degree Delta_r = 4, so at most 4 finite roots",
            "projective_root_bound": (
                "corrected low-rank endpoint contributes one possible infinity "
                "point, so at most 5 projective regular roots"
            ),
            "exact_root_counts": "not enumerated; unnecessary for rank-4 projective budget",
        },
        "aggregate": {
            "agreement_count": len(records),
            "per_agreement_degree_bound": UPDATE_RANK,
            "degree_bound_sum": UPDATE_RANK * len(records),
            "polynomial_degree_histogram": {"4": len(records)},
            "projective_infinity_contribution_sum": len(records),
            "max_finite_roots_per_agreement_bound": UPDATE_RANK,
            "max_projective_regular_roots_per_agreement_bound": UPDATE_RANK + 1,
            "all_rows_within_finite_budget": True,
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
            "does not enumerate exact finite roots",
            "does not perform a quotient/tangent subtraction table",
            "budget comparison is per-agreement regular-root accounting before removed-ledger subtraction",
            "quotient-image overlap is not audited here",
        ],
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-4 low-rank budget family mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank-4 budget family")
    print(f"status: {certificate['status']}")
    print(
        "agreements: {lo}..{hi}, records={count}".format(
            lo=certificate["agreement_range"][0],
            hi=certificate["agreement_range"][1],
            count=aggregate["agreement_count"],
        )
    )
    print(
        "degree_bound_sum={cap}, generic window sum={generic}".format(
            cap=aggregate["degree_bound_sum"],
            generic=aggregate["generic_degree_bound_sum_for_window"],
        )
    )
    print(
        "max finite roots/agreement <= {finite}, max projective roots/agreement <= {projective}, budget={budget}".format(
            finite=aggregate["max_finite_roots_per_agreement_bound"],
            projective=aggregate[
                "max_projective_regular_roots_per_agreement_bound"
            ],
            budget=certificate["endpoint_conventions"][
                "projective_budget_numerator"
            ],
        )
    )
    print("exact finite roots: not enumerated; degree bound is sufficient")


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
