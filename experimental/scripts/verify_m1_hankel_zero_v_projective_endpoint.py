#!/usr/bin/env python3
"""Verify the zero-v projective endpoint lemma for the M3 regular window."""

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


SCHEMA_VERSION = "f17-32-m3-zero-v-projective-endpoint-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
PROJECTIVE_INFINITY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/"
    "f17_32_n512_k256_m3_projective_infinity_rank_criterion.json"
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
        "zero_v_assumption": "v_m=0 for 0<=m<256",
        "affine_pencil": "M_A(Z)=H_{t,j}(u)",
        "projective_pencil": "M_A[Z0:Z1]=Z0 H_{t,j}(u)",
        "outcomes": {
            "base_full_column_rank": {
                "condition": "rank H_{t,j}(u) = j+1",
                "finite_affine_status": "closed_by_nonzero_constant_minor",
                "finite_affine_root_count": 0,
                "projective_infinity_status": "paid_common_code_line_endpoint",
                "projective_infinity_raw_endpoint_count": 1,
                "projective_infinity_residual_after_tangent": 0,
                "reason": (
                    "Some det(H_R(u)) is nonzero, so no finite affine root "
                    "exists.  At [0:1], the direction syndrome v is zero, so "
                    "the endpoint is a codeword direction paid by the "
                    "tangent/common-code-line ledger."
                ),
            },
            "base_rank_deficient": {
                "condition": "rank H_{t,j}(u) <= j",
                "finite_affine_status": "singular_all_maximal_minors_zero",
                "finite_affine_residual_label": "unknown",
                "projective_infinity_status": "paid_common_code_line_endpoint",
                "projective_infinity_raw_endpoint_count": 1,
                "projective_infinity_residual_after_tangent": 0,
                "next_step": "M5 pivot charts or separate paid classification for the finite singular bucket",
            },
        },
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    projective = load_json(PROJECTIVE_INFINITY_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        projective["schema_version"] == "f17-32-m3-projective-infinity-rank-criterion-v1",
        "unexpected projective-infinity certificate schema",
    )
    require(
        projective["window"]["A_min"] == A_MIN and projective["window"]["A_max"] == A_MAX,
        "projective-infinity window mismatch",
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
        total_row_sets == projective["window"]["all_row_set_total"],
        "row-set count mismatch",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "zero-direction projective endpoint lemma for M3 regular buckets",
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
            "projective_infinity_rank_criterion": {
                "ref": PROJECTIVE_INFINITY_REF,
                "sha256": sha256_file(PROJECTIVE_INFINITY_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "lemma": {
            "hypothesis": "The full direction syndrome satisfies v=0.",
            "affine_identity": "M_A(Z)=H_{t,j}(u), independent of Z.",
            "projective_identity": "M_A[Z0:Z1]=Z0 H_{t,j}(u).",
            "full_rank_conclusion": (
                "If H_{t,j}(u) has full column rank, some maximal minor is a "
                "nonzero constant in the finite affine patch.  Hence there are "
                "no finite regular roots."
            ),
            "infinity_payment": (
                "The projective endpoint [0:1] has syndrome v=0.  It is a "
                "codeword direction and is paid by the tangent/common-code-line "
                "ledger, not counted as residual aperiodic mass."
            ),
            "rank_deficient_conclusion": (
                "If H_{t,j}(u) has rank at most j, the finite regular bucket is "
                "singular and still requires M5 pivots or a separate paid "
                "classification; only the infinity endpoint is removed here."
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
            "full_rank_finite_affine_root_count": 0,
            "projective_infinity_residual_after_tangent": 0,
            "rank_deficient_finite_residual_label": "unknown",
        },
        "checks": [
            "v=0 makes finite regular minors independent of the affine slope",
            "full column rank of H(u) gives a nonzero constant maximal minor",
            "the projective infinity endpoint has zero direction syndrome and is tangent/common-code-line paid",
            "rank-deficient finite buckets remain named singular residuals",
        ],
        "nonclaims": [
            "does not classify arbitrary v nonzero pencils",
            "does not close finite rank-deficient zero-v singular buckets",
            "does not prove rank-deficient finite buckets are empty",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"zero-v projective endpoint certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 zero-v projective endpoint lemma")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print("full-rank finite affine roots={full_rank_finite_affine_root_count}".format(**summary))
    print(
        "projective infinity residual after tangent={projective_infinity_residual_after_tangent}".format(
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
