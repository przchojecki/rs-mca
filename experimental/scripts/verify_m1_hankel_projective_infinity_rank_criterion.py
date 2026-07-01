#!/usr/bin/env python3
"""Verify the projective-infinity rank criterion for the M3 regular window."""

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


SCHEMA_VERSION = "f17-32-m3-projective-infinity-rank-criterion-v1"
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
        "projective_pencil": "Z0 H_{t,j}(u) + Z1 H_{t,j}(v)",
        "infinity_point": "[0:1]",
        "infinity_minor_value": "Delta_R(0,1)=det(H_R(v))",
        "outcomes": {
            "direction_full_column_rank": {
                "condition": "rank H_{t,j}(v) = j+1",
                "projective_infinity_status": "excluded_by_regular_minor",
                "reason": (
                    "Some maximal row set R has det(H_R(v)) nonzero, so the "
                    "projective regular minors do not all vanish at [0:1]."
                ),
                "projective_infinity_contribution": 0,
            },
            "direction_rank_deficient": {
                "condition": "rank H_{t,j}(v) <= j",
                "projective_infinity_status": "singular_infinity_chart_required",
                "residual_label": "unknown",
                "reason": (
                    "Every maximal row-set determinant det(H_R(v)) vanishes, "
                    "so the regular minors alone do not close the infinity endpoint."
                ),
                "next_step": "projective infinity pivot chart or separate paid endpoint classification",
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
        require(
            record["outcomes"]["direction_full_column_rank"]["condition"]
            == zero_record["outcomes"]["full_column_rank"]["condition"],
            f"A={record['A']}: full-rank condition mismatch",
        )
        require(
            record["outcomes"]["direction_rank_deficient"]["condition"]
            == zero_record["outcomes"]["rank_deficient"]["condition"],
            f"A={record['A']}: rank-deficient condition mismatch",
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "projective-infinity rank criterion for M3 regular buckets",
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
        "theorem": {
            "homogenized_pencil": "M_A[Z0:Z1]=Z0 H_{t,j}(u)+Z1 H_{t,j}(v)",
            "minor_identity_at_infinity": (
                "For every maximal row set R, "
                "Delta_R(0,1)=det(H_R(v))."
            ),
            "full_rank_conclusion": (
                "If H_{t,j}(v) has full column rank j+1, at least one "
                "maximal minor is nonzero at [0:1], so projective infinity "
                "is excluded by the regular-minor chart."
            ),
            "rank_deficient_conclusion": (
                "If rank H_{t,j}(v)<=j, every maximal minor vanishes at "
                "[0:1].  The endpoint is a singular projective-infinity "
                "chart requiring a pivot packet or separate paid classification."
            ),
            "m4_consequence": (
                "A projective regular-root table may add the infinity endpoint "
                "only in the direction-rank-deficient branch.  Full-rank "
                "direction pencils have projective-infinity contribution 0."
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
            "direction_full_rank_projective_infinity_contribution": 0,
            "direction_rank_deficient_status": "singular_infinity_chart_required",
            "direction_rank_deficient_residual_label": "unknown",
        },
        "checks": [
            "homogenized maximal minors specialize at infinity to maximal minors of H(v)",
            "full column rank of H(v) gives a nonzero infinity minor",
            "rank deficiency of H(v) makes all infinity minors vanish",
            "row-set counts match the zero-u rank dichotomy certificate",
        ],
        "nonclaims": [
            "does not prove rank-deficient infinity endpoints are actual bad projective slopes",
            "does not classify quotient, tangent, or extension payment for rank-deficient infinity charts",
            "does not compute arbitrary finite affine root tables",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"projective-infinity criterion certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 projective-infinity rank criterion")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "direction full-rank infinity contribution={direction_full_rank_projective_infinity_contribution}".format(
            **summary
        )
    )
    print("direction rank-deficient: {direction_rank_deficient_status}".format(**summary))


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
