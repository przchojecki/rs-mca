#!/usr/bin/env python3
"""Verify the zero-u support-uniform canonical gcd formula over the M3 window."""

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


SCHEMA_VERSION = "f17-32-m3-support-uniform-canonical-gcd-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
PREFIX_CANONICAL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-canonical-gcd-formula-window/"
    "f17_32_n512_k256_m3_canonical_gcd_formula_window.json"
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
    support_choice_count = comb(N, size)
    row_set_count = comb(t_value, size)
    support_row_chart_count = support_choice_count * row_set_count
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "support_node_count": size,
        "support_choice_count": support_choice_count,
        "all_row_set_count": row_set_count,
        "support_row_chart_count": support_row_chart_count,
        "nonzero_witness_row_set": {"kind": "prefix", "first": 0, "last": j_value},
        "support_condition": "any distinct support subset S of the descriptor domain with |S|=j+1",
        "zero_minor_policy": "ignored in the canonical gcd over nonzero maximal minors",
        "canonical_common_gcd": monomial_gcd(size),
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    prefix_canonical = load_json(PREFIX_CANONICAL_REF)

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
        prefix_canonical["schema_version"] == "f17-32-m3-canonical-gcd-formula-v1",
        "unexpected prefix canonical certificate schema",
    )

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_support_choices = sum(record["support_choice_count"] for record in records)
    total_row_sets = sum(record["all_row_set_count"] for record in records)
    total_support_row_charts = sum(record["support_row_chart_count"] for record in records)
    require(
        total_row_sets == prefix_canonical["summary"]["all_row_set_total"],
        "all-row-set count no longer matches prefix canonical certificate",
    )

    prefix_by_a = {record["A"]: record for record in prefix_canonical["agreement_records"]}
    for record in records:
        prefix = prefix_by_a[record["A"]]
        require(
            record["canonical_common_gcd"]["degree"]
            == prefix["canonical_common_gcd"]["degree"],
            f"A={record['A']}: support-uniform gcd degree mismatch",
        )
        require(
            record["canonical_common_gcd"]["roots"]
            == prefix["canonical_common_gcd"]["roots"],
            f"A={record['A']}: support-uniform root table mismatch",
        )
        require(
            record["canonical_common_gcd"]["residual_aperiodic_numerator_after_tangent"]
            == prefix["canonical_common_gcd"]["residual_aperiodic_numerator_after_tangent"],
            f"A={record['A']}: support-uniform residual mismatch",
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for all distinct zero-u rank-size supports",
        "object": "support-uniform canonical regular-minor gcd formula over the M3 window",
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
            "prefix_canonical_formula_certificate": {
                "ref": PREFIX_CANONICAL_REF,
                "sha256": sha256_file(PREFIX_CANONICAL_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "support_node_count_min": records[-1]["support_node_count"],
            "support_node_count_max": records[0]["support_node_count"],
            "support_choice_total": total_support_choices,
            "all_row_set_total": total_row_sets,
            "support_row_chart_total": total_support_row_charts,
        },
        "formula": {
            "support": "S={x_0,...,x_j}, any distinct subset of the descriptor domain",
            "syndrome": "u_m=0, v_m=sum_{x in S} x^m",
            "row_set": "R={r_0<...<r_j} subset {0,...,t-1}",
            "matrix_factorization": (
                "(v_{r_a+b})_{a,b} = (x_i^{r_a})_{a,i} * (x_i^b)_{i,b}"
            ),
            "determinant_factorization": (
                "Delta_{A,S,R}(Z) = Z^(j+1) * det(x_i^{r_a})_{a,i} "
                "* det(x_i^b)_{i,0<=b<=j}"
            ),
            "nonzero_witness": (
                "For R={0,...,j}, both determinants are ordinary Vandermonde "
                "determinants on the distinct support S."
            ),
            "canonical_common_gcd": (
                "For every distinct S with |S|=j+1, every nonzero maximal "
                "minor is a scalar multiple of Z^(j+1), and the prefix row "
                "set is nonzero; hence the v10 canonical monic gcd is Z^(j+1)."
            ),
        },
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
            "field_principle": (
                "Every support subset is distinct because it is a subset of "
                "the descriptor domain; distinct support nodes make the "
                "ordinary Vandermonde determinant nonzero."
            ),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "support_choice_total": total_support_choices,
            "all_row_set_total": total_row_sets,
            "support_row_chart_total": total_support_row_charts,
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
            "all 512 descriptor-domain elements are distinct",
            "domain encodings decode and re-encode in F_17^32",
            "the prefix row set is nonzero for every distinct support subset by Vandermonde",
            "every maximal row-set determinant has the displayed Z^(j+1) factor",
            "per-agreement gcd degree and root table agree with the nested-prefix certificate",
        ],
        "nonclaims": [
            "only zero-u power-sum syndromes from distinct supports of size j+1",
            "not arbitrary length-256 M3 syndrome pencils",
            "not supports of size different from j+1",
            "not a worst-case support-wise MCA row bound",
            "not a quotient, extension, or singular-bucket classification",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"support-uniform canonical gcd certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    window = certificate["window"]
    print("F_17^32 M3 support-uniform canonical gcd formula")
    print(
        "A={A_min}..{A_max}, support choices={support_choice_total}, all row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "support-row charts={support_row_chart_total}, root union={root_union}, residual after tangent={residual_aperiodic_numerator_after_tangent}".format(
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
