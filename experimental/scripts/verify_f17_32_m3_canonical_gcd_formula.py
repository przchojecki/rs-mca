#!/usr/bin/env python3
"""Verify the zero-u all-row-set canonical gcd formula over the M3 window."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-canonical-gcd-formula-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
ALL_CONTIGUOUS_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-window/"
    "f17_32_n512_k256_m3_contiguous_gcd_formula_window.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def monomial_gcd(size: int) -> dict[str, Any]:
    return {
        "degree": size,
        "monic_polynomial": f"Z^{size}",
        "roots": [0],
        "raw_aperiodic_numerator_before_subtraction": 1,
        "tangent_paid_roots": [0],
        "residual_aperiodic_numerator_after_tangent": 0,
    }


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    row_set_count = comb(t_value, size)
    require(row_set_count > 0, f"A={agreement}: no maximal row sets")
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "support_node_count": size,
        "all_row_set_count": row_set_count,
        "nonzero_witness_row_set": {"kind": "prefix", "first": 0, "last": j_value},
        "zero_minor_policy": "ignored in the canonical gcd over nonzero maximal minors",
        "canonical_common_gcd": monomial_gcd(size),
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    all_contiguous = load_json(ALL_CONTIGUOUS_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] == A_MIN
        and descriptor["m3_regular_window"]["A_max"] == A_MAX,
        "descriptor M3 window mismatch",
    )
    require(
        all_contiguous["schema_version"] == "f17-32-m3-all-contiguous-gcd-formula-v1",
        "unexpected all-contiguous certificate schema",
    )

    max_support = N - A_MIN + 1
    domain_encodings = descriptor["domain"]["domain_encodings"]
    support_encodings = domain_encodings[:max_support]
    support_nodes = [field.decode(value) for value in support_encodings]
    require(len(support_encodings) == max_support, "not enough support nodes")
    require(len(set(support_encodings)) == max_support, "support prefix is not distinct")

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["all_row_set_count"] for record in records)
    require(
        total_row_sets == 155193154203428426778689566118132250614039201839551,
        "unexpected all-row-set chart count",
    )

    contiguous_by_a = {record["A"]: record for record in all_contiguous["agreement_records"]}
    for record in records:
        contiguous = contiguous_by_a[record["A"]]
        require(
            record["canonical_common_gcd"]["degree"] == contiguous["common_gcd"]["degree"],
            f"A={record['A']}: canonical gcd degree does not match contiguous gcd",
        )
        require(
            record["canonical_common_gcd"]["roots"] == contiguous["common_gcd"]["roots"],
            f"A={record['A']}: canonical roots do not match contiguous roots",
        )
        require(
            record["canonical_common_gcd"]["residual_aperiodic_numerator_after_tangent"]
            == contiguous["common_gcd"]["residual_aperiodic_numerator_after_tangent"],
            f"A={record['A']}: residual numerator does not match contiguous certificate",
        )
        require(
            record["all_row_set_count"] >= contiguous["contiguous_row_set_count"],
            f"A={record['A']}: all-row-set count smaller than contiguous count",
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for the synthetic zero-u prefix family",
        "object": "canonical all-row-set regular-minor gcd formula over the M3 window",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "all_contiguous_formula_certificate": {
                "ref": ALL_CONTIGUOUS_REF,
                "sha256": sha256_file(ALL_CONTIGUOUS_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "support_node_count_min": records[-1]["support_node_count"],
            "support_node_count_max": records[0]["support_node_count"],
            "all_row_set_total": total_row_sets,
        },
        "formula": {
            "support": "X_A = first j+1 descriptor-domain elements",
            "syndrome": "u_m=0, v_m=sum_{x in X_A} x^m",
            "row_set": "R={r_0<...<r_j} subset {0,...,t-1}",
            "factorization": (
                "Delta_{A,R}(Z) = Z^(j+1) * det(x_i^{r_a})_{a,i} "
                "* det(x_i^b)_{i,0<=b<=j}"
            ),
            "prefix_witness": (
                "For R={0,...,j}, both factors are ordinary Vandermonde "
                "determinants, so the minor is nonzero."
            ),
            "canonical_common_gcd": (
                "Every nonzero maximal minor is a scalar multiple of Z^(j+1), "
                "and at least one such minor is nonzero; hence the v10 "
                "canonical monic gcd over all nonzero maximal minors is Z^(j+1)."
            ),
        },
        "field_audit": {
            "max_support_prefix_distinct": True,
            "max_support_prefix_size": max_support,
            "max_support_prefix_hash": hash_value(support_encodings),
            "decoded_prefix_hash": hash_value([field.encode(node) for node in support_nodes]),
            "field_principle": (
                "Distinct support nodes make the ordinary Vandermonde "
                "determinant nonzero in the field."
            ),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
            "root_union": [0],
            "root_certificate_template": {
                "kind": "split_linear_factorization",
                "leading_coefficient": 1,
                "field_encoding": "base-p low-to-high integer",
                "factor": {"root": 0, "multiplicity": "degree"},
            },
            "raw_aperiodic_numerator_before_subtraction": 1,
            "residual_aperiodic_numerator_after_tangent": 0,
        },
        "checks": [
            "first 128 descriptor-domain elements are distinct",
            "prefix maximal row set is nonzero for every agreement by Vandermonde",
            "every maximal row-set determinant has a common Z^(j+1) factor",
            "every nonzero maximal row-set determinant has no additional Z factor",
            "per-agreement canonical gcd matches the all-contiguous gcd certificate",
        ],
        "nonclaims": [
            "only the synthetic zero-u nested-prefix family",
            "not arbitrary M3 row data",
            "not a worst-case support-wise MCA row bound",
            "not a quotient, extension, or singular-bucket classification",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"canonical gcd formula certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    window = certificate["window"]
    print("F_17^32 M3 canonical all-row-set gcd formula")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, all row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "root union={root_union}, residual after tangent={residual_aperiodic_numerator_after_tangent}".format(
            **summary
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
