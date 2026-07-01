#!/usr/bin/env python3
"""Verify the F_17^32 M3 rank-2 low-rank family certificate.

This is the all-window companion to the single A=426 low-rank packet.  For
each 385 <= A <= 426, put r=j+1=513-A and use the first r descriptor-domain
nodes as X, with the next two descriptor nodes as Y.  The low-rank theorem gives

    Delta_r(Z)=det(H_X) det(I+ZK),
    K_ab=sum_i L_i(y_a)L_i(y_b),

so each regular minor has degree at most 2.  The verifier reuses prefix
Vandermonde denominators across all r to keep the certificate replayable.  It
also applies the rank-2 discriminant gate to produce exact split/nonsquare root
certificates for every row in the family.
"""

from __future__ import annotations

import argparse
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
    hash_json,
    quadratic_root_certificate_field,
    quadratic_roots_field,
    render,
    split_linear_root_certificate_field,
)


SCHEMA_VERSION = "f17-32-m3-low-rank2-family-v2"
N = 512
K = 256
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
UPDATE_RANK = 2
ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
ENDPOINT_PACKET = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-a426/"
    "f17_32_n512_k256_a426_low_rank2_packet.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/"
    "f17_32_n512_k256_m3_low_rank2_family_certificate.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


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

    trace = field.add(kernel[0][0], kernel[1][1])
    determinant = field.sub(
        field.mul(kernel[0][0], kernel[1][1]),
        field.mul(kernel[0][1], kernel[1][0]),
    )
    kernel_coefficients = [field.one, trace, determinant]
    hankel_coefficients = [
        field.mul(base_determinant, coefficient)
        for coefficient in kernel_coefficients
    ]
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


def build_records(
    field: PolynomialBasisField,
    domain: list[tuple[int, ...]],
) -> list[dict[str, Any]]:
    records = []
    base_nodes: list[tuple[int, ...]] = []
    denominators: list[tuple[int, ...]] = []
    base_determinant = field.one

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
        roots = quadratic_roots_field(coefficients, field)
        require(roots is not None, f"A={agreement}: low-rank row is not quadratic")
        encoded_roots = sorted(field.encode(root) for root in roots)
        quadratic_certificate = quadratic_root_certificate_field(
            coefficients, roots, field
        )
        require(
            quadratic_certificate is not None,
            f"A={agreement}: quadratic certificate missing",
        )
        root_status = (
            "exact_nonsquare"
            if quadratic_certificate["kind"] == "quadratic_discriminant_nonsquare"
            else "exact_split"
        )
        root_certificate = split_linear_root_certificate_field(
            coefficients, roots, field
        )
        if root_status == "exact_split":
            require(
                root_certificate is not None,
                f"A={agreement}: split root certificate missing",
            )
        else:
            require(
                root_certificate is None and encoded_roots == [],
                f"A={agreement}: nonsquare row should have no split roots",
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
                "root_status": root_status,
                "root_count": len(encoded_roots),
                "roots": encoded_roots,
                "root_hash": hash_json(encoded_roots),
                "quadratic_root_certificate": quadratic_certificate,
                "root_certificate": root_certificate,
                "hankel_coefficients_ascending": encoded_coefficients,
                "low_rank_compression": sidecar,
                "sidecar_hash": hash_json(sidecar),
            }
        )
    return sorted(records, key=lambda record: record["A"])


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR)
    endpoint_packet = load_json(ENDPOINT_PACKET)
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

    endpoint_record = next(record for record in records if record["A"] == AGREEMENT_MAX)
    endpoint_item = endpoint_packet["exact_agreements"][0]
    endpoint_coefficients = endpoint_item["regular_minor_polynomial_data"][
        "coefficients_ascending"
    ]
    endpoint_sidecar = endpoint_item["regular_minor_polynomial_data"][
        "low_rank_compression"
    ]
    endpoint_roots = endpoint_item["regular_minor_data"]["roots"]
    endpoint_root_certificate = endpoint_item["regular_minor_data"]["root_certificate"]
    endpoint_quadratic_certificate = endpoint_item["regular_minor_data"][
        "quadratic_root_certificate"
    ]
    require(
        endpoint_record["hankel_coefficients_ascending"] == endpoint_coefficients,
        "A=426 endpoint coefficients do not match v9 packet",
    )
    require(
        endpoint_record["low_rank_compression"] == endpoint_sidecar,
        "A=426 endpoint sidecar does not match v9 packet",
    )
    require(
        endpoint_record["roots"] == endpoint_roots,
        "A=426 endpoint roots do not match v9 packet",
    )
    require(
        endpoint_record["root_certificate"] == endpoint_root_certificate,
        "A=426 endpoint root certificate does not match v9 packet",
    )
    require(
        endpoint_record["quadratic_root_certificate"] == endpoint_quadratic_certificate,
        "A=426 endpoint quadratic certificate does not match v9 packet",
    )

    split_rows = sum(record["root_status"] == "exact_split" for record in records)
    nonsquare_rows = sum(
        record["root_status"] == "exact_nonsquare" for record in records
    )
    exact_root_count_sum = sum(record["root_count"] for record in records)
    degree_bound_sum = UPDATE_RANK * len(records)

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
        "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
        "construction": {
            "base_nodes": "first j+1 descriptor-domain elements",
            "update_nodes": "next two descriptor-domain elements",
            "certificate_mode": "low_rank_update_bound",
            "rank": UPDATE_RANK,
        },
        "method": {
            "identity": "Delta_r(Z)=det(H_X) det(I+ZK)",
            "kernel": "K_ab=sum_i L_i(y_a)L_i(y_b)",
            "lagrange_basis": (
                "L_i(y)=prod_j(y-x_j)/((y-x_i) prod_{j != i}(x_i-x_j))"
            ),
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
            "split_quadratic_rows": split_rows,
            "nonsquare_quadratic_rows": nonsquare_rows,
            "generic_degree_bound_sum_for_window": sum(
                N - agreement + 1
                for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1)
            ),
        },
        "endpoint_crosscheck": {
            "packet_ref": str(ENDPOINT_PACKET.relative_to(REPO_ROOT)),
            "packet_sha256": file_sha256(ENDPOINT_PACKET),
            "agreement": AGREEMENT_MAX,
            "coefficients_match": True,
            "sidecar_match": True,
            "roots_match": True,
            "root_certificate_match": True,
            "quadratic_certificate_match": True,
        },
        "records": records,
        "nonclaims": [
            "synthetic syndrome-pencil family only",
            "not a worst-case MCA row bound",
            "not a worst-case row root table over F_17^32",
            "does not perform quotient/tangent subtraction",
            "exact roots are for this synthetic rank-2 family only",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"low-rank family certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    aggregate = certificate["aggregate"]
    print("F_17^32 M3 low-rank-2 family")
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
        "quadratics: split={split}, nonsquare={nonsquare}".format(
            split=aggregate["split_quadratic_rows"],
            nonsquare=aggregate["nonsquare_quadratic_rows"],
        )
    )
    print("endpoint A=426 crosscheck: PASS")


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
