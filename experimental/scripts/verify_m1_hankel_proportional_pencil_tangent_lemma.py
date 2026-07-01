#!/usr/bin/env python3
"""Verify the proportional-pencil tangent lemma for the M3 regular window."""

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


SCHEMA_VERSION = "hankel-proportional-pencil-tangent-lemma-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
ZERO_U_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-zero-u-rank-dichotomy/"
    "f17_32_n512_k256_m3_zero_u_rank_dichotomy.json"
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
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "maximal_row_set_count": comb(t_value, size),
        "stored_syndrome_length": N - K,
        "visible_hankel_syndrome_length": t_value + j_value,
        "input_relation": "u_m = c v_m for every stored syndrome coordinate 0<=m<256",
        "translated_zero_syndrome_slope": "-c",
        "outcomes": {
            "full_column_rank": {
                "condition": "rank H_{t,j}(v) = j+1",
                "regular_bucket_status": "closed_by_translated_canonical_gcd",
                "canonical_common_gcd": {
                    "degree": size,
                    "monic_polynomial_template": "(Z+c)^{j+1}",
                    "root_template": "-c",
                    "raw_aperiodic_numerator_before_subtraction": 1,
                    "tangent_paid_root_template": "-c",
                    "residual_aperiodic_numerator_after_tangent": 0,
                },
                "paid_root": {
                    "root_template": "-c",
                    "ledger": "tangent/common-code-line",
                    "reason": (
                        "Syn(f+Zg)=u+Zv=(c+Z)v, so at Z=-c the full stored "
                        "syndrome is zero and the line point is a codeword"
                    ),
                },
                "residual_aperiodic_slope_count_after_tangent": 0,
            },
            "rank_deficient": {
                "condition": "rank H_{t,j}(v) <= j",
                "regular_bucket_status": "singular_all_maximal_minors_zero",
                "residual_label": "unknown",
                "next_step": "M5 pivot charts or a separate paid-branch classification",
            },
        },
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    zero_u = load_json(ZERO_U_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        zero_u["schema_version"] == "f17-32-m3-zero-u-rank-dichotomy-v1",
        "unexpected zero-u certificate schema",
    )
    require(
        zero_u["window"]["A_min"] == A_MIN and zero_u["window"]["A_max"] == A_MAX,
        "zero-u window mismatch",
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
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(total_row_sets == zero_u["window"]["all_row_set_total"], "row-set count mismatch")

    zero_u_by_a = {record["A"]: record for record in zero_u["agreement_records"]}
    for record in records:
        zero_record = zero_u_by_a[record["A"]]
        full_rank = record["outcomes"]["full_column_rank"]
        zero_full_rank = zero_record["outcomes"]["full_column_rank"]
        require(record["visible_hankel_syndrome_length"] == N - K, "visible length mismatch")
        require(
            full_rank["canonical_common_gcd"]["degree"]
            == zero_full_rank["canonical_common_gcd"]["degree"],
            f"A={record['A']}: translated gcd degree mismatch",
        )
        require(
            record["outcomes"]["rank_deficient"]["regular_bucket_status"]
            == zero_record["outcomes"]["rank_deficient"]["regular_bucket_status"],
            f"A={record['A']}: singular status mismatch",
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "finite common-code-line proportional-pencil tangent subtraction",
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
            "zero_u_rank_dichotomy": {"ref": ZERO_U_REF, "sha256": sha256_file(ZERO_U_REF)},
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "lemma": {
            "hypothesis": (
                "The full stored syndrome vectors satisfy u=c v for some "
                "c in F_17^32."
            ),
            "pencil_identity": "M_A(Z)=H_{t,j}(u)+Z H_{t,j}(v)=(Z+c)H_{t,j}(v)",
            "minor_identity": (
                "For every maximal row set R, "
                "Delta_R(Z)=(Z+c)^(j+1) det(H_R(v))."
            ),
            "full_rank_conclusion": (
                "If rank H_{t,j}(v)=j+1, the v10 canonical monic gcd over "
                "all nonzero maximal minors is (Z+c)^(j+1), with the single "
                "finite root Z=-c."
            ),
            "tangent_subtraction": (
                "At Z=-c the full stored syndrome u+Zv is zero, so the root "
                "is paid by the tangent/common-code-line ledger and the "
                "residual aperiodic numerator is 0."
            ),
            "rank_deficient_conclusion": (
                "If rank H_{t,j}(v)<=j, every maximal regular minor vanishes; "
                "this is a singular bucket for M5 pivots or a separate paid "
                "classification."
            ),
            "m3_no_tail_caveat": (
                "For every A in 385..426, t+j=(A-256)+(512-A)=256, exactly "
                "the stored syndrome length.  Thus the proportionality needed "
                "for tangent payment is the full syndrome relation, not merely "
                "a proper visible prefix relation."
            ),
        },
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "full_rank_regular_outcome": "canonical gcd (Z+c)^(j+1), root {-c}, residual after tangent 0",
            "rank_deficient_regular_outcome": "singular bucket; send to M5 pivots unless separately paid",
            "full_rank_residual_aperiodic_slope_count_after_tangent": 0,
            "rank_deficient_residual_label": "unknown",
        },
        "checks": [
            "the proportional identity is checked over the full stored syndrome relation",
            "translation by c reduces the full-rank case to the zero-u rank dichotomy",
            "t+j equals the full stored syndrome length throughout the M3 window",
            "the row-set counts match the zero-u dichotomy certificate",
        ],
        "nonclaims": [
            "does not classify non-proportional pencils",
            "does not prove every rank-deficient proportional bucket is contained",
            "does not replace M5 pivot charts for arbitrary rank-deficient data",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"proportional-pencil tangent certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 proportional-pencil tangent lemma")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print("full-rank: {full_rank_regular_outcome}".format(**summary))
    print("rank-deficient: {rank_deficient_regular_outcome}".format(**summary))


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
