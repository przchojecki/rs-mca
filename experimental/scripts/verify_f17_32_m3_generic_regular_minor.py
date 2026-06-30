#!/usr/bin/env python3
"""Verify generic prefix regular-minor nonsingularity for the M3 window.

For each agreement 385 <= A <= 426 in the F_17^32, n=512, k=256 row,
this script certifies that the prefix (j+1)x(j+1) Hankel minor is not
identically zero as a polynomial in a generic syndrome pencil.

The witness specialization is u=0 and

    v_m = sum_{i=0}^j x_i^m

for the first j+1 domain elements x_i.  Then the prefix Hankel matrix is
V^T V, so its determinant is the square of the Vandermonde determinant and is
nonzero.  Thus the leading Z^(j+1) coefficient of det(H(u)+Z H(v)) is nonzero
under this specialization, proving the generic determinant has exact degree
j+1.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
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
    "f17_32_n512_k256_m3_generic_prefix_regular_minor_certificate.json"
)
SCHEMA_VERSION = "f17-32-m3-generic-prefix-regular-minor-v1"
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
    encoded_domain = descriptor["domain"]["domain_encodings"]
    prefix_encodings = encoded_domain[:size]
    require(len(set(prefix_encodings)) == size, f"domain prefix not distinct at A={agreement}")
    product = prefix_products[size]
    leading = field.mul(product, product)
    require(product != field.zero, f"zero Vandermonde product at A={agreement}")
    require(leading != field.zero, f"zero leading coefficient at A={agreement}")
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
        "vandermonde_product_encoding": field.encode(product),
        "leading_coefficient_encoding": field.encode(leading),
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
                "For every 385 <= A <= 426, the prefix regular Hankel minor "
                "det(H_{t,j}(u)+Z H_{t,j}(v)) is generically nonzero and has "
                "exact degree j+1."
            ),
            "regular_window": {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
            "proof_method": "Vandermonde moment specialization",
            "degree_sum": degree_sum,
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
    print("F_17^32 M3 generic prefix regular-minor certificate")
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
