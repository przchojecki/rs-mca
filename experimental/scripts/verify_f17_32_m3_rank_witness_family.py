#!/usr/bin/env python3
"""Verify the F_17^32 M3 synthetic rank-witness family.

For every exact agreement 385 <= A <= 426, this certificate builds the compact
description of a synthetic syndrome pencil

    u_m = 0,
    v_m = sum_i x_i^m,

using the first j+1 descriptor-domain elements.  The prefix regular Hankel
minor is Z^(j+1) times a shifted Vandermonde square, so rank_at_nodes has a
full-rank specialization and the exact synthetic root table is {0}.

This is not a worst-case MCA bound.  It is a finite-field stress certificate
for the v9 regular-minor pipeline across the whole M3 size range.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (
    Field,
    K,
    MODULUS,
    N,
    P,
)


AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
SCHEMA_VERSION = "f17-32-m3-rank-witness-family-v1"
SYNTHETIC_ROOTS = [0]
ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/"
    "f17_32_n512_k256_m3_rank_witness_family_certificate.json"
)
ENDPOINT_PACKET_REFS = {
    385: (
        "experimental/data/certificates/hankel-f17-32-m3-rank-witness-a385/"
        "f17_32_n512_k256_a385_rank_witness_packet.json"
    ),
    426: (
        "experimental/data/certificates/hankel-f17-32-m3-rank-witness-a426/"
        "f17_32_n512_k256_a426_rank_witness_packet.json"
    ),
}


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


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
                raise AssertionError("duplicate node in descriptor-domain prefix")
            product = field.mul(product, diff)
        products[size] = product
    return products


def product_of_nodes(field: Field, nodes: list[tuple[int, ...]]) -> tuple[int, ...]:
    product = field.one
    for node in nodes:
        if node == field.zero:
            raise AssertionError("zero node in descriptor-domain prefix")
        product = field.mul(product, node)
    return product


def packet_summary(path_text: str) -> dict[str, Any]:
    path = REPO_ROOT / path_text
    packet = load_json(path)
    item = packet["exact_agreements"][0]
    return {
        "packet_ref": path_text,
        "packet_sha256": sha256(path.read_bytes()).hexdigest(),
        "A": item["A"],
        "degree_bound": item["extractor_audit"]["degree_bound"],
        "rank_pivot_node": item["extractor_audit"]["rank_pivot_node"],
        "rank_pivot_nodes_tested": item["extractor_audit"][
            "rank_pivot_nodes_tested"
        ],
        "regular_root_bound_sum": packet["regular_root_bound_sum"],
        "checker_command": f"python3 scripts/check_aperiodic_eliminant_packet.py {path_text}",
    }


def agreement_record(
    field: Field,
    domain_encodings: list[int],
    prefix_products: dict[int, tuple[int, ...]],
    agreement: int,
) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    if t_value < size:
        raise AssertionError(f"A={agreement}: regular condition failed")
    length = t_value + j_value
    if length != N - K:
        raise AssertionError(f"A={agreement}: unexpected syndrome length {length}")
    prefix_encodings = domain_encodings[:size]
    if len(set(prefix_encodings)) != size:
        raise AssertionError(f"A={agreement}: repeated descriptor-domain element")
    nodes = [field.decode(value) for value in prefix_encodings]
    vandermonde = prefix_products[size]
    node_product = product_of_nodes(field, nodes)
    leading = field.mul(vandermonde, vandermonde)
    if leading == field.zero:
        raise AssertionError(f"A={agreement}: zero Vandermonde leading coefficient")
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "syndrome_length": length,
        "rank_pivot_node": 1,
        "rank_pivot_nodes_tested": 2,
        "rank_pivot_nodes_required_for_singularity": size + 1,
        "rank_witness_row_set": {"type": "prefix", "start": 0, "stop_exclusive": size},
        "degree_bound": size,
        "closed_form_determinant": "leading_coefficient * Z^minor_size",
        "synthetic_roots": SYNTHETIC_ROOTS,
        "synthetic_root_hash": hash_json(SYNTHETIC_ROOTS),
        "synthetic_root_count": len(SYNTHETIC_ROOTS),
        "root_completeness_reason": (
            "u=0 makes the prefix determinant a nonzero monomial in Z"
        ),
        "node_prefix_count": size,
        "node_prefix_hash": hash_json(prefix_encodings),
        "vandermonde_product_encoding": field.encode(vandermonde),
        "node_product_encoding": field.encode(node_product),
        "leading_coefficient_encoding": field.encode(leading),
        "status": "PASS",
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR)
    field = Field(P, MODULUS)
    if descriptor["field_model"]["modulus"] != MODULUS:
        raise AssertionError("row descriptor modulus mismatch")
    domain_encodings = descriptor["domain"]["domain_encodings"]
    max_size = N - AGREEMENT_MIN + 1
    nodes = [field.decode(value) for value in domain_encodings[:max_size]]
    prefix_products = prefix_vandermonde_products(field, nodes)
    records = [
        agreement_record(field, domain_encodings, prefix_products, agreement)
        for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1)
    ]
    degree_sum = sum(record["degree_bound"] for record in records)
    root_count_sum = sum(record["synthetic_root_count"] for record in records)
    endpoint_packets = {
        str(agreement): packet_summary(path_text)
        for agreement, path_text in ENDPOINT_PACKET_REFS.items()
    }
    checks = [
        {
            "name": "all_records_pass",
            "status": "PASS" if all(record["status"] == "PASS" for record in records) else "FAIL",
        },
        {
            "name": "agreement_count",
            "status": "PASS" if len(records) == 42 else "FAIL",
            "value": len(records),
        },
        {
            "name": "degree_sum",
            "status": "PASS" if degree_sum == 4515 else "FAIL",
            "value": degree_sum,
        },
        {
            "name": "minor_size_range",
            "status": "PASS"
            if (min(r["minor_size"] for r in records), max(r["minor_size"] for r in records))
            == (87, 128)
            else "FAIL",
            "value": [
                min(record["minor_size"] for record in records),
                max(record["minor_size"] for record in records),
            ],
        },
        {
            "name": "endpoint_packets_match_degrees",
            "status": "PASS"
            if all(
                endpoint_packets[str(agreement)]["degree_bound"]
                == (N - agreement + 1)
                for agreement in ENDPOINT_PACKET_REFS
            )
            else "FAIL",
        },
        {
            "name": "closed_form_roots",
            "status": "PASS"
            if all(record["synthetic_roots"] == SYNTHETIC_ROOTS for record in records)
            else "FAIL",
            "root_hash": hash_json(SYNTHETIC_ROOTS),
        },
        {
            "name": "closed_form_root_count_sum",
            "status": "PASS" if root_count_sum == 42 else "FAIL",
            "value": root_count_sum,
        },
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "field": "F_17^32",
            "n": N,
            "k": K,
            "domain_hash": descriptor["row"]["domain_hash"],
            "row_descriptor_ref": str(ROW_DESCRIPTOR.relative_to(REPO_ROOT)),
            "row_descriptor_sha256": sha256(ROW_DESCRIPTOR.read_bytes()).hexdigest(),
        },
        "claim": {
            "regular_window": {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
            "summary": (
                "For every A in 385..426, the synthetic moment syndrome "
                "u=0, v_m=sum_i x_i^m using the first j+1 descriptor-domain "
                "elements has a full-rank prefix regular minor, and the "
                "closed-form determinant has exact root set {0}."
            ),
            "proof": (
                "The prefix pencil is Z times a moment matrix because u=0. "
                "The moment determinant is Vandermonde(x_0,...,x_j)^2, "
                "nonzero because the descriptor-domain prefix elements are "
                "distinct.  Therefore Delta_A(Z)=c_A Z^(j+1) with c_A != 0."
            ),
            "degree_sum": degree_sum,
            "closed_form_root_union": SYNTHETIC_ROOTS,
            "closed_form_root_union_hash": hash_json(SYNTHETIC_ROOTS),
            "closed_form_root_union_numerator": len(SYNTHETIC_ROOTS),
            "per_agreement_root_count_sum": root_count_sum,
            "finite_slope_budget_numerator": (P ** (len(MODULUS) - 1)) // (2**128),
            "degree_only_budget_closes_safe_side": False,
        },
        "agreements": records,
        "endpoint_v9_packets": endpoint_packets,
        "checks": checks,
        "nonclaims": [
            "synthetic syndrome pencils only",
            "does not prove a worst-case MCA row bound",
            "does not brute-force roots over F_17^32",
            "does not provide quotient/tangent subtraction",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-witness family certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["claim"]["regular_window"]
    sizes = [record["minor_size"] for record in certificate["agreements"]]
    print("F_17^32 M3 rank-witness family certificate")
    print(
        "row: {field}, n={n}, k={k}, domain_hash={domain_hash}".format(
            **certificate["row"]
        )
    )
    print(
        "window: A={A_min}..{A_max}, records={records}, minor_sizes={lo}..{hi}".format(
            records=len(certificate["agreements"]),
            lo=min(sizes),
            hi=max(sizes),
            **window,
        )
    )
    print(
        "degree_sum={degree_sum}, synthetic_root_union={roots}, budget={budget}".format(
            degree_sum=certificate["claim"]["degree_sum"],
            roots=certificate["claim"]["closed_form_root_union"],
            budget=certificate["claim"]["finite_slope_budget_numerator"],
        )
    )


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
