#!/usr/bin/env python3
"""Verify the direction-rank degree cap for M3 regular Hankel minors."""

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


SCHEMA_VERSION = "f17-32-m3-direction-rank-degree-cap-v1"
Q_LINE = 17**32
TARGET_BITS = 128
BUDGET = Q_LINE // 2**TARGET_BITS
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
    finite_safe_rank = min(BUDGET, size)
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "maximal_row_set_count": comb(t_value, size),
        "generic_degree_bound": size,
        "direction_rank_symbol": "r = rank H_{t,j}(v)",
        "finite_degree_cap": "deg Delta_R(Z) <= r for every maximal row set R",
        "canonical_gcd_degree_cap": "deg gcd_nonzero_R Delta_R(Z) <= r if the regular bucket is nonsingular",
        "finite_root_count_cap": "at most r finite roots before paid-ledger subtraction",
        "finite_budget_safe_direction_rank": finite_safe_rank,
        "finite_budget_statement": (
            f"direction rank r <= {finite_safe_rank} gives finite regular root count <= {finite_safe_rank} <= {BUDGET}"
        ),
        "projective_endpoint_status": (
            "handled separately by the projective-infinity rank criterion; "
            "low direction rank normally means infinity is singular, not automatically paid"
        ),
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
    require(BUDGET == 6, "unexpected finite-slope budget")
    require(all(record["finite_budget_safe_direction_rank"] == BUDGET for record in records),
            "M3 minor sizes should all exceed the finite budget")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "direction-rank degree cap for M3 regular Hankel minors",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
            "finite_slope_budget": BUDGET,
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
        "theorem": {
            "statement": (
                "For any M3 regular pencil M_A(Z)=H_{t,j}(u)+Z H_{t,j}(v), "
                "if r=rank H_{t,j}(v), then every maximal row-set minor "
                "Delta_R(Z) has degree at most r.  If at least one maximal "
                "minor is nonzero, the v10 canonical gcd of all nonzero "
                "maximal minors also has degree at most r."
            ),
            "proof_skeleton": [
                "Write a maximal minor as det(U_R+Z V_R).",
                "By multilinearity in the columns, the coefficient of Z^d is a sum of determinants using d columns from V_R.",
                "If d>rank(V_R), any d selected columns from V_R are linearly dependent, so each such determinant is zero.",
                "Since rank(V_R)<=rank H_{t,j}(v)=r, the determinant degree is at most r.",
                "The monic gcd of nonzero minors divides each nonzero minor, so its degree is at most r.",
            ],
            "finite_budget_consequence": (
                f"For this row floor(17^32/2^128)={BUDGET}.  Therefore any "
                f"nonsingular finite regular bucket with direction rank r<={BUDGET} "
                f"has finite root count at most {BUDGET} before further paid-ledger subtraction."
            ),
            "projective_caveat": (
                "This is a finite affine root cap.  Projective infinity is "
                "separate: the companion infinity criterion excludes [0:1] only "
                "when H_{t,j}(v) has full column rank, and otherwise marks an "
                "infinity singular chart."
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
            "finite_slope_budget": BUDGET,
            "finite_safe_direction_rank_max": BUDGET,
            "degree_only_window_bound": sum(record["generic_degree_bound"] for record in records),
            "rank_cap_window_bound_if_r_le_6_each_A": BUDGET * len(records),
            "projective_endpoint": "separate criterion / singular if direction rank deficient",
        },
        "checks": [
            "minor sizes are 87..128, all above the finite budget 6",
            "row-set totals match the projective-infinity certificate",
            "the degree cap is rank-theoretic and independent of support model",
            "projective endpoint accounting is explicitly excluded from the finite cap",
        ],
        "nonclaims": [
            "does not compute exact root tables for arbitrary direction rank",
            "does not close projective infinity for rank-deficient directions",
            "does not classify singular all-minor-zero buckets",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"direction-rank degree-cap certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 direction-rank degree cap")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print("finite budget={finite_slope_budget}".format(**summary))
    print("finite safe direction rank <= {finite_safe_direction_rank_max}".format(**summary))
    print(
        "generic window degree={degree_only_window_bound}, rank<=6 window cap={rank_cap_window_bound_if_r_le_6_each_A}".format(
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
