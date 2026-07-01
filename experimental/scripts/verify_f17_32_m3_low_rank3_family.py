#!/usr/bin/env python3
"""Verify the F_17^32 M3 rank-3 low-rank family certificate.

This is the rank-3 companion to the rank-2 all-window low-rank family.  For
each 385 <= A <= 426, put r=j+1=513-A and use the first r descriptor-domain
nodes as X, with the next three descriptor nodes as Y.  The low-rank theorem
gives

    Delta_r(Z)=det(H_X) det(I+ZK),
    K_ab=sum_i L_i(y_a)L_i(y_b),

so each regular minor has degree at most 3.  The verifier computes the exact
number of finite F_17^32 roots from gcd(Delta_r(Z), Z^q-Z), without enumerating
the field.  Degree-three split rows are kept as count certificates rather than
expanded root lists.
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
    fpoly_determinant,
    fpoly_eval,
    fpoly_gcd,
    fpoly_mul,
    fpoly_scale,
    fpoly_trim,
    hash_json,
    quadratic_roots_field,
    render,
)


SCHEMA_VERSION = "f17-32-m3-low-rank3-family-v1"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
UPDATE_RANK = 3
TWO128 = 2**128
ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank3-family/"
    "f17_32_n512_k256_m3_low_rank3_family_certificate.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def multiply_mod_monic(
    left: list[tuple[int, ...]],
    right: list[tuple[int, ...]],
    modulus: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    """Multiply two polynomials modulo a monic modulus without division."""

    require(not field.is_zero(modulus[-1]), "zero leading coefficient")
    require(modulus[-1] == field.one, "modulus must be monic")
    work = fpoly_mul(left, right, field)
    degree = len(modulus) - 1
    while len(work) > degree:
        coefficient = work[-1]
        shift = len(work) - len(modulus)
        if not field.is_zero(coefficient):
            for index in range(degree):
                work[shift + index] = field.sub(
                    work[shift + index],
                    field.mul(coefficient, modulus[index]),
                )
        work.pop()
    return fpoly_trim(work, field)


def x_power_mod_monic(
    exponent: int,
    modulus: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    result = [field.one]
    base = [field.zero, field.one]
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = multiply_mod_monic(result, base, modulus, field)
        remaining >>= 1
        if remaining:
            base = multiply_mod_monic(base, base, modulus, field)
    return fpoly_trim(result, field)


def monic_polynomial(
    coefficients: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    polynomial = fpoly_trim(coefficients, field)
    require(not field.is_zero(polynomial[-1]), "zero leading coefficient")
    inverse = field.inv(polynomial[-1])
    return [field.mul(coefficient, inverse) for coefficient in polynomial]


def frobenius_linear_root_gcd(
    coefficients: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], list[tuple[int, ...]]]:
    """Return monic Delta, Z^q-Z mod Delta, and their monic gcd."""

    monic = monic_polynomial(coefficients, field)
    remainder = x_power_mod_monic(field.size, monic, field)
    if len(remainder) < 2:
        remainder += [field.zero] * (2 - len(remainder))
    remainder[1] = field.sub(remainder[1], field.one)
    remainder = fpoly_trim(remainder, field)
    gcd = fpoly_gcd(monic, remainder, field)
    return monic, remainder, gcd


def listed_roots_from_gcd(
    gcd: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[int] | None:
    degree = fpoly_degree(gcd, field)
    if degree == 0:
        return []
    if degree == 1:
        root = field.neg(field.div(gcd[0], gcd[1]))
        return [field.encode(root)]
    if degree == 2:
        roots = quadratic_roots_field(gcd, field)
        require(roots is not None, "quadratic gcd root extraction failed")
        encoded_roots = sorted(field.encode(root) for root in roots)
        require(len(encoded_roots) == 2, "quadratic gcd is not squarefree")
        return encoded_roots
    return None


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

    kernel_polynomial_matrix = [
        [
            [field.one if row == col else field.zero, kernel[row][col]]
            for col in range(len(update_nodes))
        ]
        for row in range(len(update_nodes))
    ]
    kernel_coefficients = fpoly_determinant(kernel_polynomial_matrix, field)
    hankel_coefficients = fpoly_scale(kernel_coefficients, base_determinant, field)
    sidecar = {
        "kind": "square_base_lagrange_kernel",
        "formula": "Delta(Z)=det(H_X) det(I+Z K), K_ab=sum_i L_i(y_a)L_i(y_b)",
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


def root_status(root_count: int) -> str:
    return {
        0: "exact_no_finite_roots",
        1: "exact_one_finite_root",
        2: "exact_two_finite_roots",
        3: "exact_three_finite_roots_count_only",
    }[root_count]


def common_code_line_audit(
    field: PolynomialBasisField,
    base_node_count: int,
    root_gcd: list[tuple[int, ...]],
    root_count: int,
) -> dict[str, Any]:
    u_zero_moment = field.normalize(base_node_count)
    v_zero_moment = field.normalize(UPDATE_RANK)
    common_code_line_slope = field.neg(field.div(u_zero_moment, v_zero_moment))
    gcd_value = fpoly_eval(root_gcd, common_code_line_slope, field)
    require(
        not field.is_zero(gcd_value),
        "common-code-line slope is a regular root",
    )
    return {
        "method": "frobenius_gcd_exclusion_at_moment_0",
        "finite_roots_checked": root_count,
        "overlap_count": 0,
        "witness_moment": 0,
        "u_m_encoding": field.encode(u_zero_moment),
        "v_m_encoding": field.encode(v_zero_moment),
        "common_code_line_slope_encoding": field.encode(common_code_line_slope),
        "linear_root_gcd_value_at_common_code_line_slope": field.encode(gcd_value),
        "reason": (
            "finite roots are the roots of the Frobenius gcd; evaluating that "
            "gcd at the only possible common-code-line slope from "
            "Syn_0(u+zv)=|X|+3z is nonzero"
        ),
    }


def build_records(
    field: PolynomialBasisField,
    domain: list[tuple[int, ...]],
) -> list[dict[str, Any]]:
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
            f"A={agreement}: rank-3 polynomial is not cubic",
        )
        require(
            not field.is_zero(coefficients[-1]),
            f"A={agreement}: projective leading coefficient vanishes",
        )
        monic, frobenius_remainder, root_gcd = frobenius_linear_root_gcd(
            coefficients, field
        )
        root_count_value = fpoly_degree(root_gcd, field)
        require(
            0 <= root_count_value <= UPDATE_RANK,
            f"A={agreement}: invalid Frobenius gcd degree",
        )
        listed_roots = listed_roots_from_gcd(root_gcd, field)
        if listed_roots is not None:
            require(
                len(listed_roots) == root_count_value,
                f"A={agreement}: listed root count mismatch",
            )
        tangent_audit = common_code_line_audit(
            field, size, root_gcd, root_count_value
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
                    "monic_delta_coefficients_ascending": [
                        field.encode(coefficient) for coefficient in monic
                    ],
                    "frobenius_remainder_coefficients_ascending": [
                        field.encode(coefficient) for coefficient in frobenius_remainder
                    ],
                    "linear_root_gcd_coefficients_ascending": [
                        field.encode(coefficient) for coefficient in root_gcd
                    ],
                    "linear_root_count": root_count_value,
                    "listed_roots_status": (
                        "listed" if listed_roots is not None else "count_only"
                    ),
                    "reason": (
                        "gcd(Delta,Z^q-Z) is the squarefree product of the "
                        "finite field linear factors of Delta"
                    ),
                },
                "projective_infinity": {
                    "projective_point": "[0:1]",
                    "status": "empty",
                    "contribution": 0,
                    "leading_coefficient_encoding": encoded_coefficients[-1],
                    "reason": (
                        "the homogenized cubic evaluates to the nonzero "
                        "leading coefficient at [0:1]"
                    ),
                },
                "regular_budget_table": {
                    "finite_affine_roots": root_count_value,
                    "B_tan_common_code_line": 0,
                    "regular_roots_after_common_code_line": root_count_value,
                    "projective_infinity_roots": 0,
                    "projective_regular_roots": root_count_value,
                    "finite_budget_numerator": finite_budget,
                    "projective_budget_numerator": projective_budget,
                    "finite_budget_gap": finite_budget - root_count_value,
                    "projective_budget_gap": projective_budget - root_count_value,
                    "within_finite_budget": root_count_value <= finite_budget,
                    "within_projective_budget": root_count_value <= projective_budget,
                    "quotient_image_subtraction_status": "not_audited",
                },
                "tangent_common_code_line_audit": tangent_audit,
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

    root_histogram = Counter(record["root_count"] for record in records)
    exact_root_count_sum = sum(record["root_count"] for record in records)
    degree_bound_sum = UPDATE_RANK * len(records)
    finite_budget = field.size // TWO128
    projective_budget = (field.size + 1) // TWO128
    max_root_count = max(record["root_count"] for record in records)
    tangent_overlap_sum = sum(
        record["tangent_common_code_line_audit"]["overlap_count"]
        for record in records
    )
    tangent_checked_sum = sum(
        record["tangent_common_code_line_audit"]["finite_roots_checked"]
        for record in records
    )
    roots_after_tangent_sum = sum(
        record["regular_budget_table"]["regular_roots_after_common_code_line"]
        for record in records
    )
    require(max_root_count <= finite_budget, "rank-3 family exceeds finite budget")
    require(tangent_overlap_sum == 0, "rank-3 family tangent overlap is nonzero")
    require(
        tangent_checked_sum == exact_root_count_sum,
        "rank-3 family tangent audit did not check all roots",
    )
    require(
        max(
            record["regular_budget_table"]["projective_regular_roots"]
            for record in records
        )
        <= projective_budget,
        "rank-3 family exceeds projective budget",
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
        "source_descriptor": {
            "ref": str(ROW_DESCRIPTOR.relative_to(REPO_ROOT)),
            "sha256": file_sha256(ROW_DESCRIPTOR),
        },
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "construction": {
            "base_nodes": "first j+1 descriptor-domain elements",
            "update_nodes": "next three descriptor-domain elements",
            "certificate_mode": "low_rank_update_bound",
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
            "lagrange_basis": (
                "L_i(y)=prod_j(y-x_j)/((y-x_i) prod_{j != i}(x_i-x_j))"
            ),
            "finite_root_count": "deg gcd(Delta_r(Z), Z^q-Z)",
            "prefix_replay": (
                "Vandermonde denominators and base determinants are updated "
                "incrementally across nested prefixes"
            ),
        },
        "aggregate": {
            "agreement_count": len(records),
            "per_agreement_degree_bound": UPDATE_RANK,
            "degree_bound_sum": degree_bound_sum,
            "exact_regular_root_count_sum": exact_root_count_sum,
            "linear_root_count_histogram": {
                str(key): root_histogram[key] for key in sorted(root_histogram)
            },
            "projective_infinity_contribution_sum": 0,
            "common_code_line_tangent_overlap_sum": tangent_overlap_sum,
            "finite_roots_checked_for_common_code_line": tangent_checked_sum,
            "exact_regular_roots_after_common_code_line": roots_after_tangent_sum,
            "max_finite_roots_per_agreement": max_root_count,
            "max_projective_regular_roots_per_agreement": max_root_count,
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
            "not a worst-case row root table over F_17^32",
            "does not perform a full quotient/tangent subtraction table",
            "exact root counts are for this synthetic rank-3 family only",
            "degree-three split rows are count certificates, not expanded root lists",
            "budget comparison is per-agreement regular-root accounting before removed-ledger subtraction",
            "quotient-image overlap is not audited here",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-3 low-rank family certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank-3 family")
    print(f"status: {certificate['status']}")
    print(
        "agreements: {lo}..{hi}, records={count}".format(
            lo=certificate["agreement_range"][0],
            hi=certificate["agreement_range"][1],
            count=aggregate["agreement_count"],
        )
    )
    print(
        "exact_root_count_sum={exact} (degree cap={cap}, generic window sum={generic})".format(
            exact=aggregate["exact_regular_root_count_sum"],
            cap=aggregate["degree_bound_sum"],
            generic=aggregate["generic_degree_bound_sum_for_window"],
        )
    )
    print(
        "root histogram: {hist}".format(
            hist=aggregate["linear_root_count_histogram"]
        )
    )
    print(
        "projective infinity: contribution=0, max projective roots/agreement={roots}, budget={budget}".format(
            roots=aggregate["max_projective_regular_roots_per_agreement"],
            budget=certificate["endpoint_conventions"][
                "projective_budget_numerator"
            ],
        )
    )
    print(
        "common-code-line tangent overlap: {overlap} of {checked} checked roots".format(
            overlap=aggregate["common_code_line_tangent_overlap_sum"],
            checked=aggregate["finite_roots_checked_for_common_code_line"],
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
        check_certificate(args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
