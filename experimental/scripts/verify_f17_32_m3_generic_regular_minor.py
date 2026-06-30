#!/usr/bin/env python3
"""Verify generic maximal-row-set regular-minor nonsingularity for M3.

For each agreement 385 <= A <= 426 in the F_17^32, n=512, k=256 row,
this script certifies that every maximal (j+1)x(j+1) Hankel row-set minor is
not identically zero as a polynomial in a generic syndrome pencil.

The all-row-set proof is formal.  For a sorted row set r_0<...<r_j, the
leading Z^(j+1) coefficient is

    det(y_{r_a+c})_{0 <= a,c <= j}.

In its determinant expansion, the identity permutation contributes the monomial
prod_a y_{r_a+a}.  This monomial is unique by induction on the smallest
available row and column, so its coefficient is +1.  Hence no maximal row-set
minor is structurally zero over any field.

The certificate also keeps the previous explicit shifted-Vandermonde audit for
the contiguous subatlas.  There the specialization is u=0 and

    v_m = sum_{i=0}^j x_i^m,

using the first j+1 domain elements x_i.  For row set s..s+j, the determinant is

    (prod_i x_i^s) * Vandermonde(x_0,...,x_j)^2.

This gives a concrete finite-field audit of the contiguous charts.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from math import comb
from pathlib import Path
from typing import Any

from emit_f17_32_hankel_row_descriptor import Field, K, MODULUS, N, P


ROOT = Path(__file__).resolve().parents[2]
ROW_DESCRIPTOR = ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
CERTIFICATE_PATH = ROOT / (
    "experimental/data/certificates/hankel-f17-32-generic-regular-minor/"
    "f17_32_n512_k256_m3_generic_all_row_set_regular_minor_certificate.json"
)
SCHEMA_VERSION = "f17-32-m3-generic-all-row-set-regular-minor-v1"
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sub(field: Field, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((left[index] - right[index]) % field.p for index in range(field.degree))


def prefix_vandermonde_products(
    field: Field, nodes: list[tuple[int, ...]]
) -> dict[int, tuple[int, ...]]:
    products = {1: field.one}
    product = field.one
    for size in range(2, len(nodes) + 1):
        new_node = nodes[size - 1]
        for old_node in nodes[: size - 1]:
            diff = sub(field, new_node, old_node)
            if diff == field.zero:
                raise AssertionError("duplicate node in Vandermonde witness")
            product = field.mul(product, diff)
        products[size] = product
    return products


def product_of_nodes(field: Field, nodes: list[tuple[int, ...]]) -> tuple[int, ...]:
    product = field.one
    for node in nodes:
        if node == field.zero:
            raise AssertionError("zero node in multiplicative subgroup witness")
        product = field.mul(product, node)
    return product


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_descriptor(descriptor: dict[str, Any]) -> None:
    require(descriptor["schema_version"] == "f17-32-hankel-row-descriptor-v1", "bad row descriptor schema")
    require(descriptor["row"]["field"] == "F_17^32", "row field mismatch")
    require(descriptor["row"]["n"] == N, "row n mismatch")
    require(descriptor["row"]["k"] == K, "row k mismatch")
    require(descriptor["field_model"]["p"] == P, "field prime mismatch")
    require(descriptor["field_model"]["degree"] == len(MODULUS) - 1, "field degree mismatch")
    require(descriptor["field_model"]["modulus"] == MODULUS, "field modulus mismatch")
    require(all(check["status"] == "PASS" for check in descriptor["checks"]), "row descriptor has failing checks")


def agreement_record(
    field: Field,
    descriptor: dict[str, Any],
    agreement: int,
    prefix_products: dict[int, tuple[int, ...]],
) -> dict[str, Any]:
    j = N - agreement
    t = agreement - K
    size = j + 1
    all_row_set_count = comb(t, size)
    encoded_domain = descriptor["domain"]["domain_encodings"]
    prefix_encodings = encoded_domain[:size]
    require(len(set(prefix_encodings)) == size, f"domain prefix not distinct at A={agreement}")
    nodes = [field.decode(value) for value in prefix_encodings]
    vandermonde = prefix_products[size]
    node_product = product_of_nodes(field, nodes)
    prefix_leading = field.mul(vandermonde, vandermonde)
    require(vandermonde != field.zero, f"zero Vandermonde product at A={agreement}")
    require(prefix_leading != field.zero, f"zero leading coefficient at A={agreement}")
    start_max = t - size
    contiguous_leading_coefficients = []
    for start in range(start_max + 1):
        leading = field.mul(prefix_leading, field.pow(node_product, start))
        require(
            leading != field.zero,
            f"zero contiguous leading coefficient at A={agreement}, start={start}",
        )
        contiguous_leading_coefficients.append(field.encode(leading))
    return {
        "A": agreement,
        "j": j,
        "t": t,
        "minor_size": size,
        "row_set": {"type": "prefix", "start": 0, "stop_exclusive": size},
        "witness_specialization": {
            "u": "zero syndrome",
            "v_m": "sum_{i=0}^j x_i^m using the first j+1 descriptor-domain elements",
            "node_source": "row_descriptor.domain.domain_encodings",
            "node_prefix_count": size,
            "node_prefix_hash": hash_json(prefix_encodings),
        },
        "vandermonde_product_encoding": field.encode(vandermonde),
        "node_product_encoding": field.encode(node_product),
        "leading_coefficient_encoding": field.encode(prefix_leading),
        "all_row_set_atlas": {
            "row_set_type": "arbitrary",
            "ambient_row_count": t,
            "minor_size": size,
            "count": all_row_set_count,
            "all_generic_nonzero": True,
            "proof": "identity initial monomial prod_a y_{r_a+a} has coefficient +1",
            "valid_for_every_field": True,
        },
        "contiguous_row_set_atlas": {
            "row_set_type": "contiguous",
            "start_min": 0,
            "start_max": start_max,
            "count": start_max + 1,
            "leading_coefficient_formula": "prefix_leading_coefficient * node_product^start",
            "all_generic_nonzero": True,
            "leading_coefficient_hash": hash_json(contiguous_leading_coefficients),
            "first_leading_coefficient_encoding": contiguous_leading_coefficients[0],
            "last_leading_coefficient_encoding": contiguous_leading_coefficients[-1],
        },
        "generic_degree": size,
        "status": "PASS",
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR)
    validate_descriptor(descriptor)
    field = Field(P, MODULUS)
    max_size = N - AGREEMENT_MIN + 1
    prefix_nodes = [
        field.decode(value)
        for value in descriptor["domain"]["domain_encodings"][:max_size]
    ]
    prefix_products = prefix_vandermonde_products(field, prefix_nodes)
    records = [
        agreement_record(field, descriptor, agreement, prefix_products)
        for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1)
    ]
    degree_sum = sum(record["generic_degree"] for record in records)
    all_row_set_count_sum = sum(
        record["all_row_set_atlas"]["count"] for record in records
    )
    contiguous_count_sum = sum(
        record["contiguous_row_set_atlas"]["count"] for record in records
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "field": "F_17^32",
            "n": N,
            "k": K,
            "domain_hash": descriptor["row"]["domain_hash"],
            "row_descriptor_ref": str(ROW_DESCRIPTOR.relative_to(ROOT)),
            "row_descriptor_sha256": sha256(ROW_DESCRIPTOR.read_bytes()).hexdigest(),
        },
        "claim": {
            "summary": (
                "For every 385 <= A <= 426, every maximal row-set regular "
                "Hankel minor det(H_{t,j}(u)+Z H_{t,j}(v)) is generically "
                "nonzero and has exact degree j+1."
            ),
            "regular_window": {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
            "proof_method": "identity initial monomial for all row sets; shifted Vandermonde audit for contiguous row sets",
            "degree_sum": degree_sum,
            "all_row_set_count_sum": all_row_set_count_sum,
            "contiguous_row_set_count_sum": contiguous_count_sum,
            "degree_only_budget_closes_safe_side": False,
            "finite_slope_budget_numerator": (P ** (len(MODULUS) - 1)) // (2**128),
        },
        "agreements": records,
        "checks": [
            {
                "name": "all_records_pass",
                "status": "PASS" if all(record["status"] == "PASS" for record in records) else "FAIL",
            },
            {
                "name": "degree_sum",
                "status": "PASS" if degree_sum == 4515 else "FAIL",
                "value": degree_sum,
            },
            {
                "name": "all_row_set_records_pass",
                "status": "PASS" if all(
                    record["all_row_set_atlas"]["all_generic_nonzero"]
                    for record in records
                ) else "FAIL",
            },
            {
                "name": "contiguous_row_set_count_sum",
                "status": "PASS" if contiguous_count_sum == 1806 else "FAIL",
                "value": contiguous_count_sum,
            },
            {
                "name": "budget_numerator",
                "status": "PASS" if (P ** (len(MODULUS) - 1)) // (2**128) == 6 else "FAIL",
                "value": (P ** (len(MODULUS) - 1)) // (2**128),
            },
        ],
        "nonclaims": [
            "does not prove any particular syndrome pencil is nonsingular",
            "does not enumerate roots over F_17^32",
            "does not clear the finite-slope 2^-128 budget",
            "does not classify determinant-zero singular strata",
        ],
    }


def render(certificate: dict[str, Any]) -> str:
    return json.dumps(certificate, indent=2, sort_keys=True) + "\n"


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["claim"]["regular_window"]
    print("F_17^32 M3 generic all-row-set regular-minor certificate")
    print(
        "row: n={n}, k={k}, domain_hash={domain_hash}".format(
            **certificate["row"]
        )
    )
    print("window: A={A_min}..{A_max}".format(**window))
    print(
        "records={records}, degree_sum={degree_sum}, budget={budget}".format(
            records=len(certificate["agreements"]),
            degree_sum=certificate["claim"]["degree_sum"],
            budget=certificate["claim"]["finite_slope_budget_numerator"],
        )
    )
    print(
        "all row-set charts={}".format(
            certificate["claim"]["all_row_set_count_sum"]
        )
    )
    print(
        "contiguous subatlas charts={}".format(
            certificate["claim"]["contiguous_row_set_count_sum"]
        )
    )
    print("status={}".format(certificate["status"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate JSON")
    parser.add_argument("--check", type=Path, help="check deterministic certificate JSON")
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
