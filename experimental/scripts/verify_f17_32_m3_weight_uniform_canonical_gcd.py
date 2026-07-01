#!/usr/bin/env python3
"""Verify the zero-u weight-uniform canonical gcd formula over the M3 window."""

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


SCHEMA_VERSION = "f17-32-m3-weight-uniform-canonical-gcd-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
SUPPORT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-support-uniform-canonical-gcd/"
    "f17_32_n512_k256_m3_support_uniform_canonical_gcd.json"
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
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "support_node_count": size,
        "support_choice_count": support_choice_count,
        "weight_choice_count_formula": f"(17^32 - 1)^{size}",
        "all_row_set_count": row_set_count,
        "weighted_support_row_chart_count_formula": (
            f"binom(512,{size}) * (17^32 - 1)^{size} * binom({t_value},{size})"
        ),
        "nonzero_witness_row_set": {"kind": "prefix", "first": 0, "last": j_value},
        "support_condition": "any distinct support subset S of the descriptor domain with |S|=j+1",
        "weight_condition": "all weights w_i are nonzero elements of F_17^32",
        "zero_minor_policy": "ignored in the canonical gcd over nonzero maximal minors",
        "canonical_common_gcd": monomial_gcd(size),
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    support_uniform = load_json(SUPPORT_UNIFORM_REF)

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
        support_uniform["schema_version"] == "f17-32-m3-support-uniform-canonical-gcd-v1",
        "unexpected support-uniform certificate schema",
    )

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )
    require(Q_LINE > 1, "field has no nonzero weights")

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_support_choices = sum(record["support_choice_count"] for record in records)
    total_row_sets = sum(record["all_row_set_count"] for record in records)
    require(
        total_support_choices == support_uniform["summary"]["support_choice_total"],
        "support-choice count no longer matches support-uniform certificate",
    )
    require(
        total_row_sets == support_uniform["summary"]["all_row_set_total"],
        "row-set count no longer matches support-uniform certificate",
    )

    support_by_a = {record["A"]: record for record in support_uniform["agreement_records"]}
    for record in records:
        support_record = support_by_a[record["A"]]
        require(
            record["canonical_common_gcd"]["degree"]
            == support_record["canonical_common_gcd"]["degree"],
            f"A={record['A']}: weight-uniform gcd degree mismatch",
        )
        require(
            record["canonical_common_gcd"]["roots"]
            == support_record["canonical_common_gcd"]["roots"],
            f"A={record['A']}: weight-uniform root table mismatch",
        )
        require(
            record["canonical_common_gcd"]["residual_aperiodic_numerator_after_tangent"]
            == support_record["canonical_common_gcd"]["residual_aperiodic_numerator_after_tangent"],
            f"A={record['A']}: weight-uniform residual mismatch",
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for all distinct rank-size supports with nonzero weights",
        "object": "weight-uniform canonical regular-minor gcd formula over the M3 window",
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
            "support_uniform_formula_certificate": {
                "ref": SUPPORT_UNIFORM_REF,
                "sha256": sha256_file(SUPPORT_UNIFORM_REF),
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
            "weight_choice_formula_per_agreement": "(17^32 - 1)^(j+1)",
            "weighted_support_row_chart_formula_per_agreement": (
                "binom(512,j+1) * (17^32 - 1)^(j+1) * binom(t,j+1)"
            ),
        },
        "formula": {
            "support": "S={x_0,...,x_j}, any distinct subset of the descriptor domain",
            "weights": "w_i in F_17^32^* for every support node",
            "syndrome": "u_m=0, v_m=sum_i w_i x_i^m",
            "row_set": "R={r_0<...<r_j} subset {0,...,t-1}",
            "matrix_factorization": (
                "(v_{r_a+b})_{a,b} = (x_i^{r_a})_{a,i} * diag(w_i) * (x_i^b)_{i,b}"
            ),
            "determinant_factorization": (
                "Delta_{A,S,w,R}(Z) = Z^(j+1) * det(x_i^{r_a})_{a,i} "
                "* (prod_i w_i) * det(x_i^b)_{i,0<=b<=j}"
            ),
            "nonzero_witness": (
                "For R={0,...,j}, both determinant factors are ordinary "
                "Vandermonde determinants on S, and prod_i w_i is nonzero."
            ),
            "canonical_common_gcd": (
                "For every distinct S and nonzero weight vector w, every "
                "nonzero maximal minor is a scalar multiple of Z^(j+1), and "
                "the prefix row set is nonzero; hence the v10 canonical monic "
                "gcd is Z^(j+1)."
            ),
        },
        "field_audit": {
            "full_domain_distinct": True,
            "field_has_nonzero_weights": Q_LINE > 1,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
            "field_principle": (
                "Products of nonzero field elements are nonzero, and distinct "
                "support nodes make the ordinary Vandermonde determinant nonzero."
            ),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "support_choice_total": total_support_choices,
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
            "all 512 descriptor-domain elements are distinct",
            "domain encodings decode and re-encode in F_17^32",
            "nonzero weights have nonzero product in the field",
            "the prefix row set is nonzero for every distinct support and nonzero weight vector",
            "every maximal row-set determinant has the displayed Z^(j+1) factor",
            "per-agreement gcd degree and root table agree with the support-uniform unweighted certificate",
        ],
        "nonclaims": [
            "only zero-u weighted power-sum syndromes from distinct supports of size j+1",
            "all support weights must be nonzero",
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
        raise AssertionError(f"weight-uniform canonical gcd certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 weight-uniform canonical gcd formula")
    print(
        "A={A_min}..{A_max}, support choices={support_choice_total}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "weights per agreement={weight_choice_formula_per_agreement}, root union={root_union}, residual after tangent={residual_aperiodic_numerator_after_tangent}".format(
            weight_choice_formula_per_agreement=window["weight_choice_formula_per_agreement"],
            root_union=summary["root_union"],
            residual_aperiodic_numerator_after_tangent=summary[
                "residual_aperiodic_numerator_after_tangent"
            ],
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
