#!/usr/bin/env python3
"""Verify the zero-u regular-rank dichotomy over the M3 window."""

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


SCHEMA_VERSION = "f17-32-m3-zero-u-rank-dichotomy-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
WEIGHT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-weight-uniform-canonical-gcd/"
    "f17_32_n512_k256_m3_weight_uniform_canonical_gcd.json"
)
LOWER_RANK_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-lower-rank-contained/"
    "f17_32_n512_k256_m3_lower_rank_contained.json"
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
        "maximal_row_set_count": row_set_count,
        "visible_syndrome_length": N - K,
        "zero_u_assumption": "u_m=0 for 0<=m<256",
        "outcomes": {
            "full_column_rank": {
                "condition": "rank H_{t,j}(v) = j+1",
                "regular_bucket_status": "closed_by_canonical_gcd",
                "canonical_common_gcd": monomial_gcd(size),
                "paid_root": {
                    "root": 0,
                    "ledger": "tangent/common-code-line",
                    "reason": "u=0 means the line point at Z=0 has zero syndrome and is a codeword",
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
    weight_uniform = load_json(WEIGHT_UNIFORM_REF)
    lower_rank = load_json(LOWER_RANK_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] == A_MIN
        and descriptor["m3_regular_window"]["A_max"] == A_MAX,
        "descriptor M3 window mismatch",
    )
    require(
        weight_uniform["schema_version"] == "f17-32-m3-weight-uniform-canonical-gcd-v1",
        "unexpected weight-uniform certificate schema",
    )
    require(
        lower_rank["schema_version"] == "f17-32-m3-lower-rank-contained-v1",
        "unexpected lower-rank certificate schema",
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
    require(
        total_row_sets == weight_uniform["summary"]["all_row_set_total"],
        "row-set count no longer matches weight-uniform certificate",
    )

    weight_by_a = {record["A"]: record for record in weight_uniform["agreement_records"]}
    lower_by_a = {record["A"]: record for record in lower_rank["agreement_records"]}
    for record in records:
        weight_record = weight_by_a[record["A"]]
        lower_record = lower_by_a[record["A"]]
        full_rank = record["outcomes"]["full_column_rank"]
        rank_deficient = record["outcomes"]["rank_deficient"]
        require(
            full_rank["canonical_common_gcd"]["degree"]
            == weight_record["canonical_common_gcd"]["degree"],
            f"A={record['A']}: full-rank gcd degree mismatch",
        )
        require(
            full_rank["canonical_common_gcd"]["roots"]
            == weight_record["canonical_common_gcd"]["roots"],
            f"A={record['A']}: full-rank root table mismatch",
        )
        require(
            rank_deficient["regular_bucket_status"]
            == lower_record["regular_bucket_status"],
            f"A={record['A']}: rank-deficient status mismatch",
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for arbitrary zero-u regular buckets",
        "object": "zero-u regular-rank dichotomy over the M3 window",
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
            "weight_uniform_formula_certificate": {
                "ref": WEIGHT_UNIFORM_REF,
                "sha256": sha256_file(WEIGHT_UNIFORM_REF),
            },
            "lower_rank_contained_certificate": {
                "ref": LOWER_RANK_REF,
                "sha256": sha256_file(LOWER_RANK_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "formula": {
            "zero_u_pencil": "M_A(Z)=H_{t,j}(u)+Z H_{t,j}(v)=Z H_{t,j}(v)",
            "maximal_minor": (
                "For every row set R of size j+1, "
                "Delta_R(Z)=det(Z H_R(v))=Z^(j+1) det(H_R(v))."
            ),
            "full_rank_case": (
                "If rank H_{t,j}(v)=j+1, at least one maximal minor is nonzero "
                "and every nonzero maximal minor is a scalar multiple of Z^(j+1); "
                "the v10 canonical monic gcd is Z^(j+1)."
            ),
            "rank_deficient_case": (
                "If rank H_{t,j}(v)<=j, every maximal minor vanishes and the "
                "regular bucket is singular rather than a regular root-table certificate."
            ),
            "paid_root": (
                "The only full-rank root is Z=0. Since u=0 on the full stored "
                "syndrome, the line point at Z=0 is a codeword and is paid by "
                "the tangent/common-code-line ledger."
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
            "full_rank_regular_outcome": "canonical gcd Z^(j+1), roots {0}, residual after tangent 0",
            "rank_deficient_regular_outcome": "singular bucket; send to M5 pivots unless separately paid",
            "full_rank_residual_aperiodic_slope_count_after_tangent": 0,
            "rank_deficient_residual_label": "unknown",
        },
        "checks": [
            "u=0 makes every maximal regular minor a monomial in Z",
            "full column rank gives at least one nonzero maximal minor",
            "rank deficiency makes every maximal regular minor vanish",
            "the full-rank gcd degree and root table agree with the weighted rank-size certificate",
            "the rank-deficient status agrees with the lower-rank contained certificate status",
        ],
        "nonclaims": [
            "does not classify nonzero-u pencils",
            "does not prove every rank-deficient zero-u bucket is contained",
            "does not replace M5 pivot charts for arbitrary rank-deficient zero-u data",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"zero-u rank dichotomy certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 zero-u regular-rank dichotomy")
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
