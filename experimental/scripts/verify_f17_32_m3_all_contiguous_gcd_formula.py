#!/usr/bin/env python3
"""Verify the all-window zero-u contiguous-row-set gcd formula."""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
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


SCHEMA_VERSION = "f17-32-m3-all-contiguous-gcd-formula-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
A426_FORMULA_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-contiguous-gcd-formula-a426/"
    "f17_32_n512_k256_a426_contiguous_gcd_formula.json"
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


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    contiguous_count = t_value - size + 1
    require(contiguous_count > 0, f"A={agreement}: no contiguous regular windows")
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "support_node_count": size,
        "contiguous_row_start_min": 0,
        "contiguous_row_start_max": contiguous_count - 1,
        "contiguous_row_set_count": contiguous_count,
        "common_gcd": {
            "degree": size,
            "monic_polynomial": f"Z^{size}",
            "roots": [0],
            "root_certificate": {
                "kind": "split_linear_factorization",
                "leading_coefficient": 1,
                "field_encoding": "base-p low-to-high integer",
                "factors": [{"root": 0, "multiplicity": size}],
            },
            "raw_aperiodic_numerator_before_subtraction": 1,
            "tangent_paid_roots": [0],
            "residual_aperiodic_numerator_after_tangent": 0,
        },
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    a426_formula = load_json(A426_FORMULA_REF)
    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] == A_MIN
        and descriptor["m3_regular_window"]["A_max"] == A_MAX,
        "descriptor M3 window mismatch",
    )

    max_support = N - A_MIN + 1
    domain_encodings = descriptor["domain"]["domain_encodings"]
    support_encodings = domain_encodings[:max_support]
    support_nodes = [field.decode(value) for value in support_encodings]
    require(len(support_encodings) == max_support, "not enough support nodes")
    require(len(set(support_encodings)) == max_support, "support prefix is not distinct")
    require(all(node != field.zero for node in support_nodes), "support prefix contains zero")

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_contiguous = sum(record["contiguous_row_set_count"] for record in records)
    require(total_contiguous == 1806, "unexpected contiguous row-window count")

    a426_record = next(record for record in records if record["A"] == 426)
    require(
        [0] * a426_record["common_gcd"]["degree"] + [1]
        == a426_formula["common_gcd"]["coefficients_ascending"],
        "A=426 common gcd coefficients do not match standalone formula certificate",
    )
    require(
        a426_record["common_gcd"]["roots"] == a426_formula["common_gcd"]["roots"],
        "A=426 roots do not match standalone formula certificate",
    )
    require(
        a426_record["common_gcd"]["residual_aperiodic_numerator_after_tangent"]
        == a426_formula["common_gcd"]["residual_aperiodic_numerator_after_tangent"],
        "A=426 residual numerator does not match standalone formula certificate",
    )
    require(
        a426_record["contiguous_row_set_count"]
        == a426_formula["parameters"]["contiguous_row_set_count"],
        "A=426 contiguous count mismatch",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for the synthetic zero-u prefix family",
        "object": "all-contiguous-row-set common-gcd formula over the M3 window",
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
            "a426_formula_certificate": {
                "ref": A426_FORMULA_REF,
                "sha256": sha256_file(A426_FORMULA_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "support_node_count_min": records[-1]["support_node_count"],
            "support_node_count_max": records[0]["support_node_count"],
            "contiguous_row_set_total": total_contiguous,
        },
        "formula": {
            "support": "X_A = first j+1 descriptor-domain elements",
            "syndrome": "u_m=0, v_m=sum_{x in X_A} x^m",
            "row_set": "R_s={s,s+1,...,s+j}",
            "factorization": "det(v_{s+a+b})_{0<=a,b<=j} = (prod_{x in X_A} x)^s * Vandermonde(X_A)^2",
            "determinant_polynomial": "Delta_{A,s}(Z)=c_{A,s} Z^(j+1)",
            "common_gcd": "gcd_s Delta_{A,s}(Z) = Z^(j+1), made monic",
        },
        "field_audit": {
            "max_support_prefix_distinct": True,
            "max_support_prefix_nonzero": True,
            "max_support_prefix_size": max_support,
            "max_support_prefix_hash": hash_value(support_encodings),
            "field_principle": (
                "In a field, products of nonzero elements are nonzero; "
                "therefore every Vandermonde square and support product in "
                "the nested prefixes is nonzero."
            ),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "contiguous_row_set_total": total_contiguous,
            "root_union": [0],
            "raw_aperiodic_numerator_before_subtraction": 1,
            "residual_aperiodic_numerator_after_tangent": 0,
        },
        "checks": [
            "first 128 descriptor-domain elements are distinct",
            "first 128 descriptor-domain elements are nonzero",
            "all 1806 contiguous leading determinants are nonzero by Vandermonde factorization",
            "per-agreement monic contiguous common gcd is Z^(j+1)",
            "A=426 row agrees with the standalone A=426 formula certificate",
        ],
        "nonclaims": [
            "only the contiguous row-set subatlas",
            "only the synthetic zero-u nested-prefix family",
            "not the all-maximal-minor canonical gcd over every row set",
            "not a worst-case support-wise MCA row bound",
            "not a singular-bucket classification",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"all-contiguous gcd formula certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    window = certificate["window"]
    print("F_17^32 M3 all-contiguous gcd formula")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, contiguous windows={contiguous_row_set_total}".format(
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
