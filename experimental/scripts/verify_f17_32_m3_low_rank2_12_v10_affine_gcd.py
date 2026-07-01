#!/usr/bin/env python3
"""Verify a v10 affine rank-drop gcd packet for M3 low-rank ranks 2..12."""

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

from experimental.scripts.extract_regular_hankel_minors import (  # noqa: E402
    PolynomialBasisField,
    field_batch_inverses,
    fpoly_degree,
    fpoly_gcd,
    hash_json,
    render,
)


SCHEMA_VERSION = "f17-32-m3-low-rank2-12-v10-affine-gcd-v1"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
RANKS = list(range(2, 13))
SHIFT = 1
EXPECTED_RECORDS = len(RANKS) * (AGREEMENT_MAX - AGREEMENT_MIN + 1)
EXPECTED_DEGREE_SUM = (AGREEMENT_MAX - AGREEMENT_MIN + 1) * sum(RANKS)

V10_PAPER_REF = "tex/cs25_cap_v10.tex"
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
WINDOW_PLAN_REF = (
    "experimental/data/certificates/hankel-regular-window-f17-385-426/"
    "f17_32_n512_k256_regular_window_plan.json"
)
GENERIC_REGULAR_REF = (
    "experimental/data/certificates/hankel-f17-32-generic-regular-minor/"
    "f17_32_n512_k256_m3_generic_all_row_set_regular_minor_certificate.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-12-v10-affine-gcd/"
    "f17_32_n512_k256_m3_low_rank2_12_v10_affine_gcd.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = REPO_ROOT / ref if isinstance(ref, str) else ref
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(ref: str | Path) -> str:
    path = REPO_ROOT / ref if isinstance(ref, str) else ref
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


def field_from_descriptor(descriptor: dict[str, Any]) -> PolynomialBasisField:
    return PolynomialBasisField.from_spec(
        {
            "kind": "polynomial_basis",
            "p": descriptor["field_model"]["p"],
            "modulus": descriptor["field_model"]["modulus"],
        }
    )


def lagrange_basis_values(
    field: PolynomialBasisField,
    base_nodes: list[tuple[int, ...]],
    denominators: list[tuple[int, ...]],
    update_nodes: list[tuple[int, ...]],
) -> list[list[tuple[int, ...]]]:
    denominator_inverses = field_batch_inverses(denominators, field)
    values_by_update = []
    for update in update_nodes:
        differences = [field.sub(update, base) for base in base_nodes]
        difference_inverses = field_batch_inverses(differences, field)
        product_all = field.one
        for difference in differences:
            product_all = field.mul(product_all, difference)
        values_by_update.append(
            [
                field.mul(product_all, field.mul(diff_inv, denom_inv))
                for diff_inv, denom_inv in zip(
                    difference_inverses,
                    denominator_inverses,
                )
            ]
        )
    return values_by_update


def weighted_kernel(
    field: PolynomialBasisField,
    basis_values: list[list[tuple[int, ...]]],
    base_weights: list[tuple[int, ...]],
    update_row_weights: list[tuple[int, ...]],
) -> list[list[tuple[int, ...]]]:
    kernel = []
    for row_index, left_values in enumerate(basis_values):
        row = []
        for right_values in basis_values:
            entry = field.zero
            for weight, left, right in zip(base_weights, left_values, right_values):
                entry = field.add(entry, field.mul(weight, field.mul(left, right)))
            row.append(field.mul(update_row_weights[row_index], entry))
        kernel.append(row)
    return kernel


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
    traces = []
    current_power = kernel
    for power in range(1, size + 1):
        if power > 1:
            current_power = matrix_multiply(current_power, kernel, field)
        traces.append(matrix_trace(current_power, field))
    for degree in range(1, size + 1):
        total = field.zero
        for index in range(1, degree + 1):
            term = field.mul(coefficients[degree - index], traces[index - 1])
            if index % 2:
                total = field.add(total, term)
            else:
                total = field.sub(total, term)
        coefficients.append(field.div(total, field.normalize(degree)))
    return coefficients


def determinant_coefficients_from_kernel(
    field: PolynomialBasisField,
    kernel: list[list[tuple[int, ...]]],
    rank: int,
    scale: tuple[int, ...],
) -> list[tuple[int, ...]]:
    subkernel = [row[:rank] for row in kernel[:rank]]
    return [
        field.mul(scale, coefficient)
        for coefficient in characteristic_polynomial_coefficients(subkernel, field)
    ]


def validate_sources(
    row_descriptor: dict[str, Any],
    window_plan: dict[str, Any],
    generic_regular: dict[str, Any],
) -> None:
    require(
        row_descriptor["schema_version"] == "f17-32-hankel-row-descriptor-v1",
        "row descriptor schema",
    )
    require(row_descriptor["status"] == "AUDIT", "row descriptor status")
    require(
        row_descriptor["row"]["n"] == N
        and row_descriptor["row"]["k"] == K
        and row_descriptor["row"]["field"] == "F_17^32",
        "row descriptor row",
    )
    require(
        window_plan["schema_version"] == "regular-hankel-window-plan-v1",
        "window plan schema",
    )
    require(
        window_plan["window"]["A_min"] == AGREEMENT_MIN
        and window_plan["window"]["A_max"] == AGREEMENT_MAX,
        "window plan range",
    )
    require(
        generic_regular["schema_version"]
        == "f17-32-m3-generic-all-row-set-regular-minor-v1",
        "generic regular schema",
    )
    require(generic_regular["status"] == "PROVED / AUDIT", "generic regular status")
    require(
        generic_regular["claim"]["regular_window"]
        == {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
        "generic regular window",
    )


def build_records(
    domain: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[dict[str, Any]]:
    base_nodes: list[tuple[int, ...]] = []
    denominators: list[tuple[int, ...]] = []
    base_determinant = field.one
    base_product = field.one
    records = []

    for size in range(1, N - AGREEMENT_MIN + 2):
        new_node = domain[size - 1]
        new_denominator = field.one
        for old_node in base_nodes:
            new_denominator = field.mul(
                new_denominator,
                field.sub(new_node, old_node),
            )
        for index, old_node in enumerate(base_nodes):
            denominators[index] = field.mul(
                denominators[index],
                field.sub(old_node, new_node),
            )
        denominators.append(new_denominator)
        base_nodes.append(new_node)
        base_determinant = field.mul(
            base_determinant,
            field.mul(new_denominator, new_denominator),
        )
        base_product = field.mul(base_product, new_node)

        agreement = N - size + 1
        if not (AGREEMENT_MIN <= agreement <= AGREEMENT_MAX):
            continue

        j = N - agreement
        t = agreement - K
        require(size == j + 1, f"A={agreement}: size mismatch")
        require(t > j + SHIFT, f"A={agreement}: shifted rows unavailable")

        update_nodes = domain[size : size + max(RANKS)]
        basis_values = lagrange_basis_values(
            field,
            base_nodes,
            denominators,
            update_nodes,
        )
        prefix_kernel = weighted_kernel(
            field,
            basis_values,
            [field.one] * size,
            [field.one] * max(RANKS),
        )
        shifted_kernel = weighted_kernel(
            field,
            basis_values,
            [field.inv(node) for node in base_nodes],
            update_nodes,
        )
        shifted_scale = field.mul(base_determinant, base_product)

        for rank in RANKS:
            prefix_coefficients = determinant_coefficients_from_kernel(
                field,
                prefix_kernel,
                rank,
                base_determinant,
            )
            shifted_coefficients = determinant_coefficients_from_kernel(
                field,
                shifted_kernel,
                rank,
                shifted_scale,
            )
            prefix_degree = fpoly_degree(prefix_coefficients, field)
            shifted_degree = fpoly_degree(shifted_coefficients, field)
            common_degree = fpoly_degree(
                fpoly_gcd(prefix_coefficients, shifted_coefficients, field),
                field,
            )
            require(prefix_degree == rank, f"rank-{rank} A={agreement}: prefix degree")
            require(shifted_degree == rank, f"rank-{rank} A={agreement}: shifted degree")
            require(common_degree == 0, f"rank-{rank} A={agreement}: gcd degree")
            records.append(
                {
                    "rank": rank,
                    "A": agreement,
                    "j": j,
                    "t": t,
                    "displayed_maximal_minors": {
                        "prefix_row_set": [0, j],
                        "shifted_row_set": [SHIFT, j + SHIFT],
                    },
                    "prefix_minor_degree": prefix_degree,
                    "prefix_minor_hash": hash_json(
                        [field.encode(coefficient) for coefficient in prefix_coefficients]
                    ),
                    "shifted_minor_degree": shifted_degree,
                    "shifted_minor_hash": hash_json(
                        [field.encode(coefficient) for coefficient in shifted_coefficients]
                    ),
                    "two_minor_common_gcd_degree": common_degree,
                    "v10_canonical_affine_rank_drop_gcd_degree": 0,
                    "v10_canonical_affine_rank_drop_root_count": 0,
                }
            )
    return records


def build_certificate() -> dict[str, Any]:
    row_descriptor = load_json(ROW_DESCRIPTOR_REF)
    window_plan = load_json(WINDOW_PLAN_REF)
    generic_regular = load_json(GENERIC_REGULAR_REF)
    validate_sources(row_descriptor, window_plan, generic_regular)
    field = field_from_descriptor(row_descriptor)
    domain = [
        field.decode(value)
        for value in row_descriptor["domain"]["domain_encodings"]
    ]
    require(len(domain) == N, "domain length")
    require(all(not field.is_zero(node) for node in domain), "domain contains zero")
    records = sorted(build_records(domain, field), key=lambda row: (row["rank"], row["A"]))
    gcd_histogram = Counter(record["two_minor_common_gcd_degree"] for record in records)
    prefix_degree_sum = sum(record["prefix_minor_degree"] for record in records)
    shifted_degree_sum = sum(record["shifted_minor_degree"] for record in records)
    rank_summaries = {}
    for rank in RANKS:
        rank_records = [record for record in records if record["rank"] == rank]
        rank_summaries[str(rank)] = {
            "rank": rank,
            "record_count": len(rank_records),
            "agreement_count": AGREEMENT_MAX - AGREEMENT_MIN + 1,
            "prefix_minor_degree_histogram": {str(rank): len(rank_records)},
            "shifted_minor_degree_histogram": {str(rank): len(rank_records)},
            "two_minor_common_gcd_degree_histogram": {"0": len(rank_records)},
            "v10_canonical_affine_rank_drop_root_count_sum": 0,
        }

    require(len(records) == EXPECTED_RECORDS, "record count")
    require(dict(gcd_histogram) == {0: EXPECTED_RECORDS}, "gcd histogram")
    require(prefix_degree_sum == EXPECTED_DEGREE_SUM, "prefix degree sum")
    require(shifted_degree_sum == EXPECTED_DEGREE_SUM, "shifted degree sum")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": row_descriptor["row"]["field"],
            "domain_hash": row_descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the accepted F_17^32 row descriptor"
            ),
        },
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "ranks": RANKS,
        "construction": {
            "branch": "synthetic_low_rank_ladder",
            "rank_range": [min(RANKS), max(RANKS)],
            "accepted_inputs_only": True,
            "v10_object": "canonical affine rank-drop gcd for regular Hankel buckets",
            "displayed_maximal_minors": [
                "prefix rows 0..j",
                "row-shift-1 rows 1..j+1",
            ],
            "argument": (
                "The v10 affine rank-drop gcd divides the gcd of any two "
                "nonzero maximal minors.  In every rank/agreement row, the "
                "displayed prefix and row-shift-1 minors are coprime, so the "
                "canonical affine rank-drop gcd is 1 and has no finite affine roots."
            ),
            "shifted_minor_formula": (
                "det(H_X^(1)+Z H_Y^(1)) = det(V_X)^2 prod(X) "
                "det(I+Z K_1), where K_1,ab = y_a sum_i x_i^-1 L_i(y_a)L_i(y_b)"
            ),
        },
        "source_artifacts": [
            source_record("paper_d_v10", V10_PAPER_REF),
            source_record("row_descriptor", ROW_DESCRIPTOR_REF, row_descriptor),
            source_record("regular_window_plan", WINDOW_PLAN_REF, window_plan),
            source_record("generic_regular_minor", GENERIC_REGULAR_REF, generic_regular),
        ],
        "records": records,
        "aggregate": {
            "record_count": len(records),
            "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
            "ranks": RANKS,
            "prefix_minor_degree_sum": prefix_degree_sum,
            "shifted_minor_degree_sum": shifted_degree_sum,
            "two_minor_common_gcd_degree_histogram": {
                str(key): value for key, value in sorted(gcd_histogram.items())
            },
            "v10_canonical_affine_rank_drop_root_count_sum": 0,
            "all_records_have_empty_affine_rank_drop_gcd": True,
            "rank_summaries": rank_summaries,
            "projective_endpoint_status": "not_claimed_in_this_packet",
        },
        "claim": (
            "For the synthetic low-rank M3 ladder of ranks 2..12 over the "
            "accepted F_17^32 row and every A=385..426, the v10 canonical "
            "affine rank-drop gcd is constant because the prefix and "
            "row-shift-1 maximal minors are coprime.  Thus the finite affine "
            "rank-drop root set is empty for these structured branches."
        ),
        "nonclaims": [
            "synthetic low-rank ladder only, not arbitrary M3 row data",
            "affine rank-drop roots only; projective endpoint charging is not claimed",
            "not an actual-row safe-side threshold certificate",
            "does not enumerate or classify arbitrary singular pivot charts",
            "does not use the rejected broad low-rank packet as a source artifact",
        ],
        "deterministic_record_hash": hash_json(records),
    }


def check_certificate(certificate: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(certificate)
    if actual != expected:
        raise AssertionError(f"low-rank2..12 v10 affine-gcd certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank2..12 v10 affine-gcd certificate")
    print(f"status: {certificate['status']}")
    print(
        "records={records}, prefix_degree_sum={prefix}, shifted_degree_sum={shifted}, affine_roots={roots}".format(
            records=aggregate["record_count"],
            prefix=aggregate["prefix_minor_degree_sum"],
            shifted=aggregate["shifted_minor_degree_sum"],
            roots=aggregate["v10_canonical_affine_rank_drop_root_count_sum"],
        )
    )
    print(f"common gcd degree histogram: {aggregate['two_minor_common_gcd_degree_histogram']}")
    print(f"projective endpoint: {aggregate['projective_endpoint_status']}")


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
